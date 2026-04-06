"""Tests for src/llm/gpt_client.py — happy path, caching, retry, cost calc."""
from __future__ import annotations

# Inject a fake 'openai' module before gpt_client is imported so that the
# try/except import block succeeds and OPENAI_AVAILABLE is set to True.
import importlib
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionRequest, CompletionResponse


def _make_fake_openai():
    """Return a MagicMock that looks enough like the openai module."""
    fake = MagicMock()
    fake.RateLimitError = type("RateLimitError", (Exception,), {})
    fake.APIError = type("APIError", (Exception,), {})
    return fake


_fake_openai = _make_fake_openai()
sys.modules.setdefault("openai", _fake_openai)

import src.llm.gpt_client as _gpt_mod  # noqa: E402

importlib.reload(_gpt_mod)

from src.llm.gpt_client import GPTClient, _cost_usd  # noqa: E402,I001


# ── cost helper ───────────────────────────────────────────────────────────────

class TestCostUsd:
    def test_gpt4o_mini_cheaper(self):
        assert _cost_usd("gpt-4o-mini", 1000, 1000) < _cost_usd("gpt-4o", 1000, 1000)

    def test_zero_tokens_zero_cost(self):
        assert _cost_usd("gpt-4o", 0, 0) == 0.0

    def test_mini_rate(self):
        # 1M input + 1M output at mini rates = 0.15 + 0.60 = 0.75 USD
        assert abs(_cost_usd("gpt-4o-mini", 1_000_000, 1_000_000) - 0.75) < 1e-9

    def test_standard_rate(self):
        # 1M input + 1M output at 4o rates = 2.50 + 10.00 = 12.50 USD
        assert abs(_cost_usd("gpt-4o", 1_000_000, 1_000_000) - 12.50) < 1e-9


# ── shared mock helpers ───────────────────────────────────────────────────────

def _openai_response(content="hi", model="gpt-4o", in_tok=10, out_tok=5, finish="stop"):
    choice = MagicMock()
    choice.message.content = content
    choice.finish_reason = finish
    resp = MagicMock()
    resp.choices = [choice]
    resp.usage.prompt_tokens = in_tok
    resp.usage.completion_tokens = out_tok
    resp.model = model
    return resp


@pytest.fixture
def client():
    """Yield (GPTClient, fake_openai_module). openai already injected into sys.modules."""
    fake_openai = sys.modules["openai"]
    fake_openai.AsyncOpenAI = MagicMock(return_value=MagicMock())
    c = GPTClient(api_key="test-key")
    c.client = fake_openai.AsyncOpenAI.return_value
    yield c, fake_openai


# ── happy path ────────────────────────────────────────────────────────────────

class TestGPTClientComplete:
    async def test_returns_completion_response(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response("world")
        )
        resp = await c.complete(CompletionRequest(prompt="hello"))
        assert isinstance(resp, CompletionResponse)
        assert resp.content == "world"

    async def test_uses_default_model(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response()
        )
        await c.complete(CompletionRequest(prompt="hi"))
        call_kwargs = c.client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == GPTClient.DEFAULT_MODEL

    async def test_uses_request_model_override(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response()
        )
        await c.complete(CompletionRequest(prompt="hi", model="gpt-4o-mini"))
        call_kwargs = c.client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o-mini"

    async def test_cache_hit_skips_api(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response("cached")
        )
        req = CompletionRequest(prompt="same")
        await c.complete(req)
        await c.complete(req)
        assert c.client.chat.completions.create.call_count == 1

    async def test_token_counts_propagated(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response(in_tok=42, out_tok=7)
        )
        resp = await c.complete(CompletionRequest(prompt="count"))
        assert resp.input_tokens == 42
        assert resp.output_tokens == 7

    async def test_stop_reason_propagated(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response(finish="length")
        )
        resp = await c.complete(CompletionRequest(prompt="x"))
        assert resp.stop_reason == "length"

    async def test_system_prompt_included(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response()
        )
        await c.complete(CompletionRequest(prompt="hi", system="Be concise"))
        msgs = c.client.chat.completions.create.call_args.kwargs["messages"]
        roles = [m["role"] for m in msgs]
        assert roles[0] == "system"
        assert roles[1] == "user"


# ── retry logic ───────────────────────────────────────────────────────────────

class TestGPTClientRetry:
    async def test_retries_on_rate_limit(self, client):
        c, _ = client
        RateLimitError = _gpt_mod.openai.RateLimitError
        c.client.chat.completions.create = AsyncMock(
            side_effect=[RateLimitError("limit"), _openai_response("ok")]
        )
        with patch("src.llm.gpt_client.asyncio.sleep", new_callable=AsyncMock):
            resp = await c.complete(CompletionRequest(prompt="retry"))
        assert resp.content == "ok"
        assert c.client.chat.completions.create.call_count == 2

    async def test_raises_after_max_retries_on_rate_limit(self, client):
        c, _ = client
        RateLimitError = _gpt_mod.openai.RateLimitError
        c.client.chat.completions.create = AsyncMock(
            side_effect=RateLimitError("always limited")
        )
        with patch("src.llm.gpt_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RuntimeError, match="Failed after"):
                await c.complete(CompletionRequest(prompt="x"))
        assert c.client.chat.completions.create.call_count == c.max_retries

    async def test_api_error_reraises_on_last_attempt(self, client):
        c, _ = client
        APIError = _gpt_mod.openai.APIError
        c.client.chat.completions.create = AsyncMock(
            side_effect=APIError("server error")
        )
        with patch("src.llm.gpt_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(Exception, match="server error"):
                await c.complete(CompletionRequest(prompt="x"))


# ── stream ────────────────────────────────────────────────────────────────────

class TestGPTClientStream:
    async def test_yields_tokens(self, client):
        c, _ = client

        def _make_chunk(text):
            chunk = MagicMock()
            chunk.choices[0].delta.content = text
            return chunk

        async def _fake_stream(*args, **kwargs):
            return _async_iter([_make_chunk("hello"), _make_chunk(" world"), _make_chunk(None)])

        async def _async_iter(items):  # helper that returns async iterable
            for item in items:
                yield item

        # stream() calls create(..., stream=True) and iterates the result
        c.client.chat.completions.create = AsyncMock(
            side_effect=lambda **kw: _async_iter([
                _make_chunk("tok1"), _make_chunk("tok2"), _make_chunk(None),
            ])
        )
        tokens = []
        async for t in c.stream(CompletionRequest(prompt="hi")):
            tokens.append(t)
        assert tokens == ["tok1", "tok2"]   # None deltas are skipped

    async def test_stream_uses_model_override(self, client):
        c, _ = client
        captured_kwargs: list[dict] = []

        async def _fake_create(**kwargs):
            captured_kwargs.append(kwargs)
            async def _empty():
                return
                yield  # make it a generator
            return _empty()

        c.client.chat.completions.create = _fake_create
        async for _ in c.stream(CompletionRequest(prompt="x", model="gpt-4o-mini")):
            pass
        assert captured_kwargs[0]["model"] == "gpt-4o-mini"


# ── count_tokens ──────────────────────────────────────────────────────────────

class TestGPTClientCountTokens:
    def test_empty_string(self, client):
        c, _ = client
        assert c.count_tokens("") == 0

    def test_approx_four_chars_per_token(self, client):
        c, _ = client
        assert c.count_tokens("a" * 40) == 10


# ── import guard ──────────────────────────────────────────────────────────────

class TestImportGuard:
    def test_raises_if_openai_not_available(self):
        with patch.object(_gpt_mod, "OPENAI_AVAILABLE", False):
            with pytest.raises(ImportError, match="openai"):
                _gpt_mod.GPTClient(api_key="x")
