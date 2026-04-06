"""Tests for src/api/app.py — lifespan, _get_client, and _log.append paths."""
from __future__ import annotations

import importlib
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionResponse  # noqa: E402

# Access the module object (not the FastAPI `app` attribute exported by __init__)
_app_mod = sys.modules.get("src.api.app") or importlib.import_module("src.api.app")


def _make_resp(
    content: str = "hello",
    model: str = "claude-sonnet-4-6",
    in_tok: int = 10,
    out_tok: int = 5,
) -> CompletionResponse:
    return CompletionResponse(
        content=content,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        stop_reason="end_turn",
    )


def _mock_client(resp: CompletionResponse | None = None, exc: Exception | None = None):
    client = MagicMock()
    if exc is not None:
        client.complete = AsyncMock(side_effect=exc)
    else:
        client.complete = AsyncMock(return_value=resp or _make_resp())
    return client


@pytest.fixture
async def ac():
    import httpx
    from httpx import ASGITransport

    from src.api.app import app

    with patch("src.api.app.LogIndex"):
        async with httpx.AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client


# ── lifespan ──────────────────────────────────────────────────────────────────

class TestLifespan:
    async def test_startup_logs_api_startup(self):
        from src.api.app import app, lifespan

        mock_log = MagicMock()
        with patch("src.api.app.LogIndex", return_value=mock_log):
            async with lifespan(app):
                pass

        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "api_startup" in event_names

    async def test_shutdown_logs_api_shutdown(self):
        from src.api.app import app, lifespan

        mock_log = MagicMock()
        with patch("src.api.app.LogIndex", return_value=mock_log):
            async with lifespan(app):
                pass  # startup done; exiting triggers shutdown

        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "api_shutdown" in event_names

    async def test_startup_sets_cache_and_rate_limiter(self):
        from src.api.app import app, lifespan

        orig_cache = _app_mod._cache
        orig_rl = _app_mod._rate_limiter
        orig_log = _app_mod._log
        try:
            mock_log = MagicMock()
            with patch("src.api.app.LogIndex", return_value=mock_log):
                async with lifespan(app):
                    assert _app_mod._cache is not None
                    assert _app_mod._rate_limiter is not None
                    assert _app_mod._log is mock_log
        finally:
            _app_mod._cache = orig_cache
            _app_mod._rate_limiter = orig_rl
            _app_mod._log = orig_log


# ── _get_client ───────────────────────────────────────────────────────────────

class TestGetClient:
    def test_lazy_creates_claude_client(self):
        original = _app_mod._client
        _app_mod._client = None
        try:
            with patch("src.llm.claude_client.anthropic.Anthropic"), \
                 patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
                result = _app_mod._get_client()
            assert result is not None
            assert _app_mod._client is result
        finally:
            _app_mod._client = original

    def test_returns_same_instance_on_second_call(self):
        original = _app_mod._client
        _app_mod._client = None
        try:
            with patch("src.llm.claude_client.anthropic.Anthropic"), \
                 patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
                first = _app_mod._get_client()
                second = _app_mod._get_client()
            assert first is second
        finally:
            _app_mod._client = original


# ── _log.append paths ─────────────────────────────────────────────────────────

class TestCompleteLogging:
    async def test_success_appends_log(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch("src.api.app._get_client", return_value=_mock_client()):
                resp = await ac.post("/v1/complete", json={"prompt": "hi"})

        assert resp.status_code == 200
        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "complete_ok" in event_names

    async def test_error_appends_log(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch(
                "src.api.app._get_client",
                return_value=_mock_client(exc=RuntimeError("boom")),
            ):
                resp = await ac.post("/v1/complete", json={"prompt": "x"})

        assert resp.status_code == 502
        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "complete_error" in event_names

    async def test_success_log_has_llm_tag(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch("src.api.app._get_client", return_value=_mock_client()):
                await ac.post("/v1/complete", json={"prompt": "hi"})

        ok_call = next(
            c for c in mock_log.append.call_args_list if c[0][0] == "complete_ok"
        )
        assert ok_call[1]["tag"] == "llm"

    async def test_error_log_has_error_tag(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch(
                "src.api.app._get_client",
                return_value=_mock_client(exc=RuntimeError("x")),
            ):
                await ac.post("/v1/complete", json={"prompt": "x"})

        err_call = next(
            c for c in mock_log.append.call_args_list if c[0][0] == "complete_error"
        )
        assert err_call[1]["tag"] == "error"


class TestChatLogging:
    async def test_chat_error_appends_log(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch(
                "src.api.app._get_client",
                return_value=_mock_client(exc=RuntimeError("chat fail")),
            ):
                resp = await ac.post(
                    "/v1/chat",
                    json={"messages": [{"role": "user", "content": "x"}]},
                )

        assert resp.status_code == 502
        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "chat_error" in event_names
