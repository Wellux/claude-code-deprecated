"""Tests for src/llm/utils.py."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.llm.base import CompletionRequest, CompletionResponse
from src.llm.utils import (
    build_request,
    complete_with_fallback,
    format_messages_as_prompt,
    merge_system_prompts,
    truncate_to_tokens,
)


class TestBuildRequest:
    def test_basic(self):
        req = build_request("hello")
        assert isinstance(req, CompletionRequest)
        assert req.prompt == "hello"

    def test_with_all_options(self):
        req = build_request("p", system="s", model="m", max_tokens=100, temperature=0.1)
        assert req.system == "s"
        assert req.model == "m"
        assert req.max_tokens == 100
        assert req.temperature == 0.1


class TestTruncateToTokens:
    def test_short_text_unchanged(self):
        assert truncate_to_tokens("hello", 1000) == "hello"

    def test_long_text_truncated(self):
        text = "a" * 10000
        result = truncate_to_tokens(text, max_tokens=10)
        assert len(result) < len(text)
        assert "[truncated]" in result

    def test_exact_boundary_unchanged(self):
        text = "a" * 40  # 40 chars = 10 tokens at 4 chars/token
        result = truncate_to_tokens(text, max_tokens=10)
        assert result == text


class TestMergeSystemPrompts:
    def test_single_prompt(self):
        assert merge_system_prompts("be concise") == "be concise"

    def test_two_prompts_merged(self):
        result = merge_system_prompts("rule 1", "rule 2")
        assert "rule 1" in result
        assert "rule 2" in result

    def test_none_values_skipped(self):
        result = merge_system_prompts(None, "rule", None)
        assert result == "rule"

    def test_all_none_returns_none(self):
        assert merge_system_prompts(None, None) is None

    def test_empty_strings_skipped(self):
        assert merge_system_prompts("", "  ", "rule") == "rule"

    def test_custom_separator(self):
        result = merge_system_prompts("a", "b", separator=" | ")
        assert result == "a | b"


class TestFormatMessagesAsPrompt:
    def test_single_user_message(self):
        result = format_messages_as_prompt([{"role": "user", "content": "hello"}])
        assert "USER: hello" in result

    def test_multi_turn(self):
        msgs = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
            {"role": "user", "content": "bye"},
        ]
        result = format_messages_as_prompt(msgs)
        assert "USER: hi" in result
        assert "ASSISTANT: hello" in result
        assert "USER: bye" in result

    def test_empty_messages(self):
        assert format_messages_as_prompt([]) == ""


class TestCompleteWithFallback:
    @pytest.mark.asyncio
    async def test_returns_primary_on_success(self):
        primary = MagicMock()
        fallback = MagicMock()
        expected = CompletionResponse(
            content="primary", model="m", input_tokens=1, output_tokens=1, stop_reason="end_turn"
        )
        primary.complete = AsyncMock(return_value=expected)
        req = build_request("test")
        result = await complete_with_fallback(primary, fallback, req)
        assert result.content == "primary"
        fallback.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_back_on_primary_error(self):
        primary = MagicMock()
        fallback = MagicMock()
        primary.complete = AsyncMock(side_effect=RuntimeError("primary down"))
        fallback_resp = CompletionResponse(
            content="fallback", model="m", input_tokens=1, output_tokens=1, stop_reason="end_turn"
        )
        fallback.complete = AsyncMock(return_value=fallback_resp)
        req = build_request("test")
        result = await complete_with_fallback(primary, fallback, req)
        assert result.content == "fallback"
