"""OpenAI GPT API client."""
import asyncio
import time
from collections.abc import AsyncIterator

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..utils.cache import ResponseCache
from ..utils.logger import get_logger
from ..utils.rate_limiter import RateLimiter
from .base import CompletionRequest, CompletionResponse, LLMClient

logger = get_logger(__name__)

# Cost per 1M tokens (USD) — update as pricing changes
GPT4O_INPUT_COST = 2.50
GPT4O_OUTPUT_COST = 10.00
GPT4O_MINI_INPUT_COST = 0.15
GPT4O_MINI_OUTPUT_COST = 0.60


def _cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    if "mini" in model:
        return (input_tokens * GPT4O_MINI_INPUT_COST + output_tokens * GPT4O_MINI_OUTPUT_COST) / 1_000_000
    return (input_tokens * GPT4O_INPUT_COST + output_tokens * GPT4O_OUTPUT_COST) / 1_000_000


class GPTClient(LLMClient):
    """OpenAI GPT client with rate limiting, caching, and retry."""

    DEFAULT_MODEL = "gpt-4o"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = DEFAULT_MODEL,
        cache: ResponseCache | None = None,
        rate_limiter: RateLimiter | None = None,
        max_retries: int = 3,
    ):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package required: pip install openai")
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.default_model = default_model
        self.cache = cache or ResponseCache()
        self.rate_limiter = rate_limiter or RateLimiter(requests_per_minute=500)
        self.max_retries = max_retries

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Complete with caching and retry."""
        model = request.model or self.default_model

        cached = self.cache.get(request)
        if cached:
            logger.debug("cache_hit", model=model, prompt_len=len(request.prompt))
            return cached

        await self.rate_limiter.acquire()

        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        last_error = None
        for attempt in range(self.max_retries):
            try:
                t0 = time.monotonic()
                resp = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                )
                latency_ms = int((time.monotonic() - t0) * 1000)

                content = resp.choices[0].message.content or ""
                stop_reason = resp.choices[0].finish_reason or "stop"
                input_tokens = resp.usage.prompt_tokens if resp.usage else 0
                output_tokens = resp.usage.completion_tokens if resp.usage else 0

                response = CompletionResponse(
                    content=content,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    stop_reason=stop_reason,
                )

                logger.info(
                    "llm_call",
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=_cost_usd(model, input_tokens, output_tokens),
                )

                self.cache.set(request, response)
                return response

            except openai.RateLimitError:
                wait = 2 ** attempt
                logger.warning("rate_limit_retry", attempt=attempt, wait_s=wait)
                await asyncio.sleep(wait)
                last_error = "rate_limit"
            except openai.APIError as e:
                logger.error("api_error", error=str(e), attempt=attempt)
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
                last_error = str(e)

        raise RuntimeError(f"Failed after {self.max_retries} retries: {last_error}")

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream response tokens."""
        model = request.model or self.default_model
        await self.rate_limiter.acquire()

        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def count_tokens(self, text: str) -> int:
        """Rough token count: ~4 chars per token."""
        return len(text) // 4
