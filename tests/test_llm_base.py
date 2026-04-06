"""Tests for src/llm/base.py — CompletionRequest, CompletionResponse, cost calculation."""
import pytest

from src.llm.base import CompletionRequest, CompletionResponse


class TestCompletionRequest:
    def test_defaults(self):
        req = CompletionRequest(prompt="hello")
        assert req.prompt == "hello"
        assert req.system is None
        assert req.model is None
        assert req.max_tokens == 4096
        assert req.temperature == 0.7

    def test_custom_values(self):
        req = CompletionRequest(
            prompt="test",
            system="be concise",
            model="claude-sonnet-4-6",
            max_tokens=512,
            temperature=0.0,
        )
        assert req.system == "be concise"
        assert req.model == "claude-sonnet-4-6"
        assert req.max_tokens == 512
        assert req.temperature == 0.0

    def test_empty_prompt_allowed(self):
        req = CompletionRequest(prompt="")
        assert req.prompt == ""


class TestCompletionResponse:
    def test_basic_fields(self):
        resp = CompletionResponse(
            content="hello world",
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
            stop_reason="end_turn",
        )
        assert resp.content == "hello world"
        assert resp.model == "claude-sonnet-4-6"
        assert resp.input_tokens == 10
        assert resp.output_tokens == 5
        assert resp.stop_reason == "end_turn"

    def test_cost_usd_sonnet(self):
        resp = CompletionResponse(
            content="x",
            model="claude-sonnet-4-6",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
            stop_reason="end_turn",
        )
        # sonnet: $3/M input + $15/M output = $18 per 1M each
        assert resp.cost_usd == pytest.approx(18.0, rel=0.01)

    def test_cost_usd_haiku(self):
        resp = CompletionResponse(
            content="x",
            model="claude-haiku-4-5-20251001",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
            stop_reason="end_turn",
        )
        # haiku: $0.25/M input + $1.25/M output = $1.50
        assert resp.cost_usd == pytest.approx(1.50, rel=0.01)

    def test_cost_usd_zero_tokens(self):
        resp = CompletionResponse(
            content="",
            model="claude-sonnet-4-6",
            input_tokens=0,
            output_tokens=0,
            stop_reason="end_turn",
        )
        assert resp.cost_usd == 0.0

    def test_cost_usd_unknown_model_defaults(self):
        resp = CompletionResponse(
            content="x",
            model="unknown-model-xyz",
            input_tokens=1_000_000,
            output_tokens=0,
            stop_reason="end_turn",
        )
        # Should not raise — should return some non-negative value
        assert resp.cost_usd >= 0.0

    def test_total_tokens(self):
        resp = CompletionResponse(
            content="x",
            model="claude-sonnet-4-6",
            input_tokens=30,
            output_tokens=12,
            stop_reason="end_turn",
        )
        assert resp.total_tokens == 42

    def test_total_tokens_zero(self):
        resp = CompletionResponse(
            content="",
            model="claude-sonnet-4-6",
            input_tokens=0,
            output_tokens=0,
            stop_reason="end_turn",
        )
        assert resp.total_tokens == 0
