"""Anthropic Claude API client — retry with jitter, structured logging."""
from __future__ import annotations

import asyncio
import random
import time
from collections.abc import AsyncIterator

import anthropic

from ..utils.cache import ResponseCache
from ..utils.logger import get_logger
from ..utils.rate_limiter import RateLimiter
from .base import CompletionRequest, CompletionResponse, LLMClient

logger = get_logger(__name__)

# Exceptions that are safe to retry (transient)
_RETRYABLE = (anthropic.RateLimitError, anthropic.InternalServerError)
# Exceptions that are never retried (client mistakes)
_FATAL = (anthropic.AuthenticationError, anthropic.PermissionDeniedError)

_BASE_BACKOFF_S = 1.0    # first retry waits ~1 s
_MAX_BACKOFF_S = 30.0    # cap at 30 s regardless of attempt count
_JITTER_RATIO = 0.25     # ±25 % random jitter to avoid thundering herd


def _backoff(attempt: int) -> float:
    """Exponential backoff with full jitter: base * 2^attempt ± jitter."""
    delay = min(_BASE_BACKOFF_S * (2 ** attempt), _MAX_BACKOFF_S)
    jitter = delay * _JITTER_RATIO * (2 * random.random() - 1)
    return max(0.0, delay + jitter)


class ClaudeClient(LLMClient):
    """Production Claude client with rate limiting, caching, and retry."""

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = DEFAULT_MODEL,
        cache: ResponseCache | None = None,
        rate_limiter: RateLimiter | None = None,
        max_retries: int = 3,
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.async_client = anthropic.AsyncAnthropic(api_key=api_key)
        self.default_model = default_model
        self.cache = cache or ResponseCache()
        self.rate_limiter = rate_limiter or RateLimiter(requests_per_minute=100)
        self.max_retries = max_retries

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Complete with caching, rate limiting, and exponential-backoff retry."""
        model = request.model or self.default_model

        cached = self.cache.get(request)
        if cached:
            logger.debug("cache_hit", model=model, prompt_len=len(request.prompt))
            return cached

        await self.rate_limiter.acquire()

        last_exc: BaseException = RuntimeError("no attempts made")
        for attempt in range(self.max_retries):
            try:
                t0 = time.monotonic()
                message = await self.async_client.messages.create(
                    model=model,
                    max_tokens=max(1, request.max_tokens),
                    temperature=max(0.0, min(1.0, request.temperature)),
                    system=request.system or anthropic.NOT_GIVEN,
                    messages=[{"role": "user", "content": request.prompt}],
                )
                latency_ms = int((time.monotonic() - t0) * 1000)

                if not message.content:
                    raise ValueError("Anthropic returned empty content block")
                response = CompletionResponse(
                    content=message.content[0].text,
                    model=message.model,
                    input_tokens=message.usage.input_tokens,
                    output_tokens=message.usage.output_tokens,
                    stop_reason=message.stop_reason or "end_turn",
                )

                logger.info(
                    "llm_call",
                    model=model,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=response.cost_usd,
                    attempt=attempt,
                )
                self.cache.set(request, response)
                return response

            except _FATAL as e:
                # Auth errors: no point retrying
                logger.error("llm_fatal", error=type(e).__name__, detail=str(e))
                raise

            except _RETRYABLE as e:
                wait = _backoff(attempt)
                logger.warning(
                    "llm_retry",
                    error=type(e).__name__,
                    attempt=attempt,
                    wait_s=round(wait, 2),
                    remaining=self.max_retries - attempt - 1,
                )
                last_exc = e
                await asyncio.sleep(wait)

            except anthropic.APIError as e:
                # Unexpected API errors — retry but log loudly
                wait = _backoff(attempt)
                logger.error("llm_api_error", error=str(e), attempt=attempt,
                             wait_s=round(wait, 2))
                last_exc = e
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(wait)

        raise RuntimeError(
            f"LLM call failed after {self.max_retries} attempts: {last_exc}"
        )

    async def chat(
        self,
        messages: list[dict],
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResponse:
        """Multi-turn chat using the native Anthropic messages API.

        Unlike `complete()`, this accepts a list of role/content dicts and passes
        them directly to the API — preserving proper conversation context.

        Args:
            messages: List of {"role": "user"|"assistant", "content": str} dicts.
            system: Optional system prompt.
            model: Model override; defaults to self.default_model.
            max_tokens: Maximum tokens in the response.
            temperature: Sampling temperature.
        """
        model = model or self.default_model
        await self.rate_limiter.acquire()

        last_exc: BaseException = RuntimeError("no attempts made")
        for attempt in range(self.max_retries):
            try:
                t0 = time.monotonic()
                message = await self.async_client.messages.create(
                    model=model,
                    max_tokens=max(1, max_tokens),
                    temperature=max(0.0, min(1.0, temperature)),
                    system=system or anthropic.NOT_GIVEN,
                    messages=messages,
                )
                latency_ms = int((time.monotonic() - t0) * 1000)

                if not message.content:
                    raise ValueError("Anthropic returned empty content block")
                response = CompletionResponse(
                    content=message.content[0].text,
                    model=message.model,
                    input_tokens=message.usage.input_tokens,
                    output_tokens=message.usage.output_tokens,
                    stop_reason=message.stop_reason or "end_turn",
                )
                logger.info(
                    "llm_chat",
                    model=model,
                    turns=len(messages),
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=response.cost_usd,
                    attempt=attempt,
                )
                return response

            except _FATAL as e:
                logger.error("llm_fatal", error=type(e).__name__, detail=str(e))
                raise

            except _RETRYABLE as e:
                wait = _backoff(attempt)
                logger.warning(
                    "llm_retry",
                    error=type(e).__name__,
                    attempt=attempt,
                    wait_s=round(wait, 2),
                    remaining=self.max_retries - attempt - 1,
                )
                last_exc = e
                await asyncio.sleep(wait)

            except anthropic.APIError as e:
                wait = _backoff(attempt)
                logger.error("llm_api_error", error=str(e), attempt=attempt,
                             wait_s=round(wait, 2))
                last_exc = e
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(wait)

        raise RuntimeError(
            f"LLM chat failed after {self.max_retries} attempts: {last_exc}"
        )

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream response tokens (no retry — caller owns the connection)."""
        model = request.model or self.default_model
        await self.rate_limiter.acquire()

        async with self.async_client.messages.stream(
            model=model,
            max_tokens=max(1, request.max_tokens),
            temperature=max(0.0, min(1.0, request.temperature)),
            system=request.system or anthropic.NOT_GIVEN,
            messages=[{"role": "user", "content": request.prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def count_tokens(self, text: str) -> int:
        """Approximate token count (≈4 chars per token). Use SDK for precision."""
        return len(text) // 4
