"""Tests for src/llm/claude_client.py — retry logic, caching, backoff."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionRequest, CompletionResponse
from src.llm.claude_client import ClaudeClient, _backoff

# ── _backoff ──────────────────────────────────────────────────────────────────

class TestBackoff:
    def test_increases_with_attempt(self):
        # Higher attempt → higher base delay (jitter aside)
        # Use enough samples to avoid flaky jitter-dominated results
        samples_0 = [_backoff(0) for _ in range(20)]
        samples_2 = [_backoff(2) for _ in range(20)]
        assert sum(samples_2) > sum(samples_0)

    def test_capped_at_max(self):
        # attempt=100 should still be ≤ 30s + 25% jitter ceiling
        for _ in range(20):
            assert _backoff(100) <= 30.0 * 1.25 + 0.001

    def test_non_negative(self):
        for attempt in range(5):
            assert _backoff(attempt) >= 0.0

    def test_attempt_zero_near_base(self):
        # attempt=0 → base ~1s ± 25%
        for _ in range(20):
            val = _backoff(0)
            assert 0.0 <= val <= 1.5


# ── ClaudeClient — happy path ─────────────────────────────────────────────────

def _mock_message(content="hello", model="claude-sonnet-4-6", in_tok=10, out_tok=5):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    msg.model = model
    msg.usage.input_tokens = in_tok
    msg.usage.output_tokens = out_tok
    msg.stop_reason = "end_turn"
    return msg


class TestClaudeClientComplete:
    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key")
            c.async_client = async_cls.return_value
            return c

    async def test_returns_completion_response(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message("world")
        )
        req = CompletionRequest(prompt="hello")
        resp = await client.complete(req)
        assert isinstance(resp, CompletionResponse)
        assert resp.content == "world"

    async def test_uses_cache_on_second_call(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message("cached")
        )
        req = CompletionRequest(prompt="same prompt")
        await client.complete(req)
        await client.complete(req)
        # API should only be called once — second is served from cache
        assert client.async_client.messages.create.call_count == 1

    async def test_uses_default_model(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message()
        )
        req = CompletionRequest(prompt="hi")
        await client.complete(req)
        call_kwargs = client.async_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == ClaudeClient.DEFAULT_MODEL

    async def test_uses_request_model_override(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message(model="claude-haiku-4-5-20251001")
        )
        req = CompletionRequest(prompt="hi", model="claude-haiku-4-5-20251001")
        await client.complete(req)
        call_kwargs = client.async_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "claude-haiku-4-5-20251001"

    async def test_response_tokens_propagated(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message(in_tok=42, out_tok=7)
        )
        resp = await client.complete(CompletionRequest(prompt="x"))
        assert resp.input_tokens == 42
        assert resp.output_tokens == 7

    async def test_stop_reason_propagated(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message()
        )
        resp = await client.complete(CompletionRequest(prompt="x"))
        assert resp.stop_reason == "end_turn"


# ── retry logic ───────────────────────────────────────────────────────────────

class TestClaudeClientRetry:
    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key", max_retries=3)
            c.async_client = async_cls.return_value
            return c

    async def test_retries_on_rate_limit(self, client):
        import anthropic as _anthropic

        ok = _mock_message("ok")
        client.async_client.messages.create = AsyncMock(
            side_effect=[
                _anthropic.RateLimitError("rate limited", response=MagicMock(), body={}),
                ok,
            ]
        )
        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            resp = await client.complete(CompletionRequest(prompt="retry me"))
        assert resp.content == "ok"
        assert client.async_client.messages.create.call_count == 2

    async def test_raises_immediately_on_auth_error(self, client):
        import anthropic as _anthropic

        client.async_client.messages.create = AsyncMock(
            side_effect=_anthropic.AuthenticationError(
                "bad key", response=MagicMock(), body={}
            )
        )
        with pytest.raises(_anthropic.AuthenticationError):
            await client.complete(CompletionRequest(prompt="x"))
        # Only called once — no retry on fatal errors
        assert client.async_client.messages.create.call_count == 1

    async def test_raises_after_max_retries(self, client):
        import anthropic as _anthropic

        client.async_client.messages.create = AsyncMock(
            side_effect=_anthropic.RateLimitError(
                "always rate limited", response=MagicMock(), body={}
            )
        )
        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RuntimeError, match="failed after"):
                await client.complete(CompletionRequest(prompt="x"))
        assert client.async_client.messages.create.call_count == 3


# ── anthropic.APIError handler ────────────────────────────────────────────────

class TestClaudeClientAPIError:
    """Cover the `except anthropic.APIError` branch (non-retryable, non-fatal)."""

    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key", max_retries=3)
            c.async_client = async_cls.return_value
            return c

    async def test_api_error_on_last_attempt_reraises(self, client):
        import anthropic as _anthropic

        # BadRequestError is APIError but not in _RETRYABLE or _FATAL
        err = _anthropic.BadRequestError("bad request", response=MagicMock(), body={})
        client.async_client.messages.create = AsyncMock(side_effect=err)

        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(_anthropic.BadRequestError):
                await client.complete(CompletionRequest(prompt="x"))

        assert client.async_client.messages.create.call_count == 3

    async def test_api_error_retries_before_last_attempt(self, client):
        import anthropic as _anthropic

        err = _anthropic.BadRequestError("bad request", response=MagicMock(), body={})
        ok = _mock_message("recovered")
        # First two attempts fail, third succeeds
        client.async_client.messages.create = AsyncMock(side_effect=[err, err, ok])

        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            resp = await client.complete(CompletionRequest(prompt="x"))

        assert resp.content == "recovered"
        assert client.async_client.messages.create.call_count == 3


# ── stream ────────────────────────────────────────────────────────────────────

class TestClaudeClientStream:
    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key")
            c.async_client = async_cls.return_value
            return c

    async def test_stream_yields_tokens(self, client):
        async def _text_stream():
            for token in ["hello", " world"]:
                yield token

        stream_ctx = MagicMock()
        stream_ctx.text_stream = _text_stream()
        stream_ctx.__aenter__ = AsyncMock(return_value=stream_ctx)
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        client.async_client.messages.stream = MagicMock(return_value=stream_ctx)

        tokens = []
        async for t in client.stream(CompletionRequest(prompt="stream me")):
            tokens.append(t)

        assert tokens == ["hello", " world"]

    async def test_stream_empty_response(self, client):
        async def _empty():
            return
            yield  # make it an async generator

        stream_ctx = MagicMock()
        stream_ctx.text_stream = _empty()
        stream_ctx.__aenter__ = AsyncMock(return_value=stream_ctx)
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        client.async_client.messages.stream = MagicMock(return_value=stream_ctx)

        tokens = [t async for t in client.stream(CompletionRequest(prompt="x"))]
        assert tokens == []


# ── count_tokens ──────────────────────────────────────────────────────────────

class TestCountTokens:
    def test_empty_string(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
            c = ClaudeClient(api_key="x")
        assert c.count_tokens("") == 0

    def test_approximate_count(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
            c = ClaudeClient(api_key="x")
        # 40 chars → ~10 tokens
        assert c.count_tokens("a" * 40) == 10
