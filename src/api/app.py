"""FastAPI application — exposes LLM completion, routing, and chat endpoints."""
from __future__ import annotations

import os
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from ..llm.base import CompletionRequest
from ..routing import route as routing_route
from ..utils.cache import ResponseCache
from ..utils.log_index import LogIndex
from ..utils.logger import get_logger
from ..utils.rate_limiter import RateLimiter
from ..version import __version__
from .middleware import (
    ContentLengthLimitMiddleware,
    CorrelationIDMiddleware,
    TimingMiddleware,
    get_request_id,
)
from .models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CompleteRequest,
    CompleteResponse,
    HealthResponse,
    RouteRequest,
    RouteResponse,
)

logger = get_logger(__name__)

# Shared singletons — initialized at startup
_cache: ResponseCache | None = None
_rate_limiter: RateLimiter | None = None
_log: LogIndex | None = None
_client = None       # ClaudeClient — lazy to avoid import-time anthropic requirement
_start_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize shared resources on startup; flush and log on shutdown."""
    global _cache, _rate_limiter, _log, _start_time
    _start_time = time.monotonic()
    _cache = ResponseCache(ttl_seconds=3600, max_size=1000)
    _rate_limiter = RateLimiter(requests_per_minute=100)
    _log = LogIndex(os.environ.get("CCM_LOG_PATH", "data/cache/events.log"))
    _log.append("api_startup", version=__version__, pid=os.getpid())
    logger.info("api_startup", version=__version__, cache_ttl=3600, rpm=100)
    yield
    # Graceful shutdown — flush remaining log entries
    uptime = round(time.monotonic() - _start_time, 1)
    if _log:
        _log.append("api_shutdown", version=__version__, uptime_s=uptime,
                    cache_size=_cache.size if _cache else 0)
    logger.info("api_shutdown", version=__version__, uptime_s=uptime)


def _get_client():
    """Lazy-init ClaudeClient to avoid import errors when anthropic not installed."""
    global _client
    if _client is None:
        from ..llm.claude_client import ClaudeClient
        _client = ClaudeClient(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            cache=_cache,
            rate_limiter=_rate_limiter,
        )
    return _client


app = FastAPI(
    title="Claude Code Max API",
    description="LLM completion, routing, and chat — backed by Claude",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(ContentLengthLimitMiddleware)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(TimingMiddleware)

# Versioned router — all business endpoints live under /v1
v1 = APIRouter(prefix="/v1")


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health():
    uptime = round(time.monotonic() - _start_time, 1) if _start_time else None
    return HealthResponse(
        status="ok",
        version=__version__,
        models_available=[
            "claude-opus-4-6",
            "claude-sonnet-4-6",
            "claude-haiku-4-5-20251001",
        ],
        uptime_s=uptime,
    )


# ── Completion ────────────────────────────────────────────────────────────────

@v1.post("/complete", response_model=CompleteResponse)
async def complete(req: CompleteRequest):
    """Single-turn completion with optional auto-routing."""
    routed_by = None
    model = req.model
    if req.auto_route and model is None:
        decision = routing_route(req.prompt)
        model = decision.llm.model.value
        routed_by = decision.llm.reason

    client = _get_client()
    llm_req = CompletionRequest(
        prompt=req.prompt,
        system=req.system,
        model=model,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    try:
        resp = await client.complete(llm_req)
    except Exception as e:
        rid = get_request_id()
        logger.error("complete_error", error=str(e), request_id=rid)
        if _log:
            _log.append("complete_error", error=type(e).__name__,
                        request_id=rid, tag="error")
        raise HTTPException(
            status_code=502,
            detail=f"Upstream LLM error [{type(e).__name__}] — see server logs (request_id={rid})",
        ) from e

    if _log:
        _log.append("complete_ok", model=resp.model,
                    input_tokens=resp.input_tokens,
                    output_tokens=resp.output_tokens,
                    cost_usd=resp.cost_usd,
                    request_id=get_request_id(),
                    tag="llm")

    return CompleteResponse(
        content=resp.content,
        model=resp.model,
        input_tokens=resp.input_tokens,
        output_tokens=resp.output_tokens,
        cost_usd=resp.cost_usd,
        stop_reason=resp.stop_reason,
        routed_by=routed_by,
    )


@v1.post("/complete/stream")
async def complete_stream(req: CompleteRequest):
    """Streaming completion — returns server-sent event tokens."""
    model = req.model
    if req.auto_route and model is None:
        decision = routing_route(req.prompt)
        model = decision.llm.model.value

    client = _get_client()
    llm_req = CompletionRequest(
        prompt=req.prompt,
        system=req.system,
        model=model,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    async def token_generator() -> AsyncIterator[str]:
        try:
            async for token in client.stream(llm_req):
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error("stream_error", error=str(e))
            yield f"data: [ERROR] {e}\n\n"

    return StreamingResponse(token_generator(), media_type="text/event-stream")


# ── Chat ──────────────────────────────────────────────────────────────────────

@v1.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Multi-turn chat — passes messages list directly to the Anthropic messages API."""
    # Route model on the last user message for complexity scoring
    model = req.model
    if model is None:
        last_user = next(
            (m.content for m in reversed(req.messages) if m.role == "user"), ""
        )
        decision = routing_route(last_user or "")
        model = decision.llm.model.value

    client = _get_client()
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    try:
        resp = await client.chat(
            messages,
            system=req.system,
            model=model,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
        )
    except Exception as e:
        rid = get_request_id()
        logger.error("chat_error", error=str(e), request_id=rid)
        if _log:
            _log.append("chat_error", error=type(e).__name__,
                        request_id=rid, tag="error")
        raise HTTPException(
            status_code=502,
            detail=f"Upstream LLM error [{type(e).__name__}] — see server logs (request_id={rid})",
        ) from e

    return ChatResponse(
        message=ChatMessage(role="assistant", content=resp.content),
        model=resp.model,
        input_tokens=resp.input_tokens,
        output_tokens=resp.output_tokens,
        cost_usd=resp.cost_usd,
    )


# ── Routing ───────────────────────────────────────────────────────────────────

@v1.post("/route", response_model=RouteResponse)
async def route(req: RouteRequest):
    """Return routing decisions for a task without executing anything."""
    decision = routing_route(req.task, content_type=req.content_type)

    subtasks = [
        {
            "id": st.id,
            "description": st.description,
            "agent": st.agent.value,
            "model": st.model.value,
            "skill": st.skill,
            "depends_on": st.depends_on,
        }
        for st in decision.plan.subtasks
    ]

    return RouteResponse(
        model=decision.llm.model.value,
        model_reason=decision.llm.reason,
        skill=decision.skill.skill if decision.skill else None,
        skill_confidence=decision.skill.confidence if decision.skill else None,
        agent=decision.agent.agent.value,
        agent_reason=decision.agent.reason,
        memory_tier=decision.memory.tier.value,
        memory_destination=decision.memory.destination,
        plan_size=decision.plan.size.value,
        plan_mode=decision.plan.execution_mode,
        subtasks=subtasks,
    )


# Register versioned routes
app.include_router(v1)
