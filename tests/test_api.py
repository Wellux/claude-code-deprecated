"""Tests for src/api/ — Pydantic models and FastAPI app structure."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.api.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CompleteRequest,
    CompleteResponse,
    HealthResponse,
    RouteRequest,
    RouteResponse,
)

# ── CompleteRequest ───────────────────────────────────────────────────────────

class TestCompleteRequest:
    def test_minimal(self):
        req = CompleteRequest(prompt="hello")
        assert req.prompt == "hello"
        assert req.model is None
        assert req.system is None
        assert req.auto_route is True
        assert req.stream is False

    def test_defaults(self):
        req = CompleteRequest(prompt="x")
        assert req.max_tokens == 4096
        assert req.temperature == 0.7

    def test_full(self):
        req = CompleteRequest(
            prompt="summarize this",
            system="You are helpful",
            model="claude-sonnet-4-6",
            max_tokens=1000,
            temperature=0.3,
            stream=True,
            auto_route=False,
        )
        assert req.model == "claude-sonnet-4-6"
        assert req.stream is True
        assert req.auto_route is False

    def test_max_tokens_lower_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", max_tokens=0)

    def test_max_tokens_upper_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", max_tokens=200001)

    def test_temperature_lower_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", temperature=-0.1)

    def test_temperature_upper_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", temperature=1.1)


# ── CompleteResponse ──────────────────────────────────────────────────────────

class TestCompleteResponse:
    def test_minimal(self):
        resp = CompleteResponse(
            content="hello",
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
            cost_usd=0.001,
            stop_reason="end_turn",
        )
        assert resp.routed_by is None

    def test_with_routed_by(self):
        resp = CompleteResponse(
            content="hi",
            model="claude-haiku-4-5-20251001",
            input_tokens=5,
            output_tokens=2,
            cost_usd=0.0001,
            stop_reason="end_turn",
            routed_by="simple greeting → haiku",
        )
        assert resp.routed_by == "simple greeting → haiku"


# ── RouteRequest / RouteResponse ──────────────────────────────────────────────

class TestRouteRequest:
    def test_minimal(self):
        req = RouteRequest(task="write a function")
        assert req.task == "write a function"
        assert req.content_type is None

    def test_with_content_type(self):
        req = RouteRequest(task="store this finding", content_type="lesson")
        assert req.content_type == "lesson"


class TestRouteResponse:
    def test_construction(self):
        resp = RouteResponse(
            model="claude-sonnet-4-6",
            model_reason="medium complexity",
            skill="code-review",
            skill_confidence=0.85,
            agent="general",
            agent_reason="simple coding task",
            memory_tier="FILES",
            memory_destination="data/outputs/",
            plan_size="MEDIUM",
            plan_mode="sequential",
            subtasks=[],
        )
        assert resp.model == "claude-sonnet-4-6"
        assert resp.skill == "code-review"
        assert resp.subtasks == []

    def test_nullable_fields(self):
        resp = RouteResponse(
            model="claude-haiku-4-5-20251001",
            model_reason="simple",
            skill=None,
            skill_confidence=None,
            agent="general",
            agent_reason="",
            memory_tier="CACHE",
            memory_destination="data/cache/",
            plan_size="ATOMIC",
            plan_mode="sequential",
            subtasks=[],
        )
        assert resp.skill is None
        assert resp.skill_confidence is None


# ── ChatMessage / ChatRequest / ChatResponse ──────────────────────────────────

class TestChatMessage:
    def test_user_message(self):
        msg = ChatMessage(role="user", content="hi there")
        assert msg.role == "user"

    def test_assistant_message(self):
        msg = ChatMessage(role="assistant", content="hello back")
        assert msg.role == "assistant"


class TestChatRequest:
    def test_minimal(self):
        req = ChatRequest(messages=[ChatMessage(role="user", content="hi")])
        assert len(req.messages) == 1
        assert req.system is None
        assert req.model is None

    def test_defaults(self):
        req = ChatRequest(messages=[ChatMessage(role="user", content="x")])
        assert req.max_tokens == 4096
        assert req.temperature == 0.7

    def test_multi_turn(self):
        msgs = [
            ChatMessage(role="user", content="What is 2+2?"),
            ChatMessage(role="assistant", content="4"),
            ChatMessage(role="user", content="And 3+3?"),
        ]
        req = ChatRequest(messages=msgs)
        assert len(req.messages) == 3


class TestChatResponse:
    def test_construction(self):
        resp = ChatResponse(
            message=ChatMessage(role="assistant", content="hello"),
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
            cost_usd=0.0005,
        )
        assert resp.message.role == "assistant"
        assert resp.message.content == "hello"


# ── HealthResponse ────────────────────────────────────────────────────────────

class TestHealthResponse:
    def test_construction(self):
        from src.version import __version__
        resp = HealthResponse(
            status="ok",
            version=__version__,
            models_available=["claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
        )
        assert resp.status == "ok"
        assert resp.version == __version__
        assert len(resp.models_available) == 2

    def test_version_required(self):
        # version is now a required field (no default) so passing it works
        from src.version import __version__
        resp = HealthResponse(status="ok", version=__version__, models_available=[])
        assert resp.version == __version__

    def test_uptime_optional(self):
        from src.version import __version__
        resp = HealthResponse(status="ok", version=__version__, models_available=[])
        assert resp.uptime_s is None


# ── FastAPI app import (smoke test) ───────────────────────────────────────────

class TestAppImport:
    def test_app_importable(self):
        """FastAPI app should be importable without an ANTHROPIC_API_KEY."""
        from src.api import app
        assert app is not None

    def test_app_has_routes(self):
        from src.api import app
        routes = [r.path for r in app.routes]
        assert "/health" in routes
        assert "/v1/complete" in routes
        assert "/v1/route" in routes
        assert "/v1/chat" in routes

    def test_app_title(self):
        from src.api import app
        assert "Claude" in app.title
