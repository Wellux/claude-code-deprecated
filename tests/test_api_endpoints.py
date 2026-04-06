"""Integration tests for src/api/app.py — FastAPI endpoints via httpx AsyncClient."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionResponse

# ── shared helpers ─────────────────────────────────────────────────────────────

def _make_resp(
    content: str = "hello",
    model: str = "claude-sonnet-4-6",
    in_tok: int = 10,
    out_tok: int = 5,
    stop_reason: str = "end_turn",
) -> CompletionResponse:
    return CompletionResponse(
        content=content,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        stop_reason=stop_reason,
    )


def _mock_client(resp: CompletionResponse | None = None, exc: Exception | None = None):
    """Return a mock LLM client whose .complete() and .chat() return resp or raise exc."""
    client = MagicMock()
    if exc is not None:
        client.complete = AsyncMock(side_effect=exc)
        client.chat = AsyncMock(side_effect=exc)
    else:
        client.complete = AsyncMock(return_value=resp or _make_resp())
        client.chat = AsyncMock(return_value=resp or _make_resp())
    return client


# ── fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
async def ac():
    """Async HTTP client pointed at the FastAPI test app with LogIndex patched out."""
    import httpx
    from httpx import ASGITransport

    from src.api.app import app

    # Patch LogIndex.append so tests don't touch the filesystem
    with patch("src.api.app.LogIndex"):
        async with httpx.AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client


# ── GET /health ────────────────────────────────────────────────────────────────

class TestHealth:
    async def test_returns_200(self, ac):
        resp = await ac.get("/health")
        assert resp.status_code == 200

    async def test_response_structure(self, ac):
        data = (await ac.get("/health")).json()
        assert data["status"] == "ok"
        assert "version" in data
        assert isinstance(data["models_available"], list)
        assert len(data["models_available"]) >= 1

    async def test_has_correlation_header(self, ac):
        resp = await ac.get("/health")
        assert "x-request-id" in resp.headers

    async def test_has_timing_header(self, ac):
        resp = await ac.get("/health")
        assert "x-process-time-ms" in resp.headers


# ── POST /complete ─────────────────────────────────────────────────────────────

class TestComplete:
    async def test_happy_path(self, ac):
        mock_client = _mock_client(_make_resp("world"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "hello"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] == "world"
        assert data["model"] == "claude-sonnet-4-6"

    async def test_returns_token_counts(self, ac):
        mock_client = _mock_client(_make_resp(in_tok=42, out_tok=7))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "count tokens"})
        data = resp.json()
        assert data["input_tokens"] == 42
        assert data["output_tokens"] == 7

    async def test_auto_route_sets_routed_by(self, ac):
        mock_client = _mock_client()
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/complete", json={"prompt": "simple task", "auto_route": True}
            )
        data = resp.json()
        assert resp.status_code == 200
        # auto_route=True fills routed_by with a non-empty reason
        assert data["routed_by"] is not None
        assert len(data["routed_by"]) > 0

    async def test_explicit_model_bypasses_routing(self, ac):
        mock_client = _mock_client(_make_resp(model="claude-haiku-4-5-20251001"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/complete",
                json={"prompt": "hi", "model": "claude-haiku-4-5-20251001", "auto_route": False},
            )
        data = resp.json()
        assert resp.status_code == 200
        assert data["routed_by"] is None

    async def test_llm_error_returns_502(self, ac):
        mock_client = _mock_client(exc=RuntimeError("upstream failure"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "x"})
        assert resp.status_code == 502
        detail = resp.json()["detail"]
        assert "RuntimeError" in detail           # error type exposed
        assert "upstream failure" not in detail   # raw message NOT leaked to client

    async def test_stop_reason_propagated(self, ac):
        mock_client = _mock_client(_make_resp(stop_reason="max_tokens"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "x"})
        assert resp.json()["stop_reason"] == "max_tokens"

    async def test_cost_usd_present(self, ac):
        mock_client = _mock_client()
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "x"})
        assert "cost_usd" in resp.json()


# ── POST /complete/stream ──────────────────────────────────────────────────────

class TestCompleteStream:
    async def _mock_stream_client(self, tokens: list[str]):
        """Client whose .stream() yields tokens."""

        async def _gen(*_args, **_kwargs):
            for t in tokens:
                yield t

        client = MagicMock()
        client.stream = _gen
        return client

    async def test_streams_tokens_and_done(self, ac):
        client = await self._mock_stream_client(["hello", " world"])
        with patch("src.api.app._get_client", return_value=client):
            resp = await ac.post(
                "/v1/complete/stream",
                json={"prompt": "hi", "stream": True},
            )
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers["content-type"]
        body = resp.text
        assert "data: hello" in body
        assert "data:  world" in body
        assert "data: [DONE]" in body

    async def test_stream_error_yields_error_event(self, ac):
        async def _bad_gen(*_args, **_kwargs):
            raise RuntimeError("stream broke")
            yield  # make it a generator

        client = MagicMock()
        client.stream = _bad_gen
        with patch("src.api.app._get_client", return_value=client):
            resp = await ac.post("/v1/complete/stream", json={"prompt": "x"})
        assert resp.status_code == 200
        assert "[ERROR]" in resp.text


# ── POST /chat ─────────────────────────────────────────────────────────────────

class TestChat:
    async def test_happy_path(self, ac):
        mock_client = _mock_client(_make_resp("I am fine"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/chat",
                json={"messages": [{"role": "user", "content": "How are you?"}]},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"]["role"] == "assistant"
        assert data["message"]["content"] == "I am fine"

    async def test_multi_turn_passes_messages_list(self, ac):
        """Messages must be passed as a list to the native chat API, not flattened."""
        mock_client = _mock_client()
        captured: list[list] = []

        async def _chat(messages, **_kw):
            captured.append(messages)
            return _make_resp()

        mock_client.chat = _chat
        with patch("src.api.app._get_client", return_value=mock_client):
            await ac.post(
                "/v1/chat",
                json={
                    "messages": [
                        {"role": "user", "content": "hi"},
                        {"role": "assistant", "content": "hello"},
                        {"role": "user", "content": "bye"},
                    ]
                },
            )
        assert len(captured) == 1
        messages = captured[0]
        assert len(messages) == 3
        assert messages[0] == {"role": "user", "content": "hi"}
        assert messages[1] == {"role": "assistant", "content": "hello"}
        assert messages[2] == {"role": "user", "content": "bye"}

    async def test_llm_error_returns_502(self, ac):
        mock_client = _mock_client(exc=ValueError("chat failed"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/chat",
                json={"messages": [{"role": "user", "content": "x"}]},
            )
        assert resp.status_code == 502

    async def test_returns_token_counts(self, ac):
        mock_client = _mock_client(_make_resp(in_tok=20, out_tok=10))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/chat",
                json={"messages": [{"role": "user", "content": "count"}]},
            )
        data = resp.json()
        assert data["input_tokens"] == 20
        assert data["output_tokens"] == 10


# ── POST /route ────────────────────────────────────────────────────────────────

class TestRoute:
    async def test_returns_routing_decision(self, ac):
        resp = await ac.post("/v1/route", json={"task": "write a unit test"})
        assert resp.status_code == 200
        data = resp.json()
        assert "model" in data
        assert "model_reason" in data
        assert "agent" in data
        assert "plan_size" in data
        assert "subtasks" in data
        assert isinstance(data["subtasks"], list)

    async def test_no_llm_call_on_route(self, ac):
        """Route endpoint must not call the LLM client."""
        mock_client = _mock_client()
        with patch("src.api.app._get_client", return_value=mock_client):
            await ac.post("/v1/route", json={"task": "anything"})
        mock_client.complete.assert_not_called()

    async def test_content_type_hint_accepted(self, ac):
        resp = await ac.post(
            "/v1/route", json={"task": "store this finding", "content_type": "lesson"}
        )
        assert resp.status_code == 200

    async def test_model_in_known_set(self, ac):
        data = (await ac.post("/v1/route", json={"task": "short task"})).json()
        known = {"claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"}
        assert data["model"] in known


# ── Input validation ──────────────────────────────────────────────────────────

class TestInputValidation:
    async def test_chat_empty_messages_returns_422(self, ac):
        resp = await ac.post("/v1/chat", json={"messages": []})
        assert resp.status_code == 422

    async def test_chat_max_tokens_above_limit_returns_422(self, ac):
        resp = await ac.post("/v1/chat", json={
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 999999,
        })
        assert resp.status_code == 422

    async def test_complete_max_tokens_above_limit_returns_422(self, ac):
        resp = await ac.post("/v1/complete", json={"prompt": "hello", "max_tokens": 999999})
        assert resp.status_code == 422

    async def test_chat_max_tokens_at_limit_accepted(self, ac):
        with patch("src.api.app._get_client", return_value=_mock_client()):
            resp = await ac.post("/v1/chat", json={
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 200000,
            })
        assert resp.status_code == 200
