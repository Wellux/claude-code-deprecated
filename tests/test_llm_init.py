"""Tests for src/llm/__init__.py — lazy-import __getattr__ branches."""
from __future__ import annotations

import pytest


class TestLLMPackageExports:
    def test_completion_request_importable(self):
        from src.llm import CompletionRequest
        assert CompletionRequest is not None

    def test_completion_response_importable(self):
        from src.llm import CompletionResponse
        assert CompletionResponse is not None

    def test_llm_client_importable(self):
        from src.llm import LLMClient
        assert LLMClient is not None

    def test_utils_importable(self):
        from src.llm import build_request, merge_system_prompts, truncate_to_tokens
        assert callable(build_request)
        assert callable(truncate_to_tokens)
        assert callable(merge_system_prompts)


class TestLazyGetattr:
    def test_claude_client_lazy_load(self):
        """src.llm.ClaudeClient resolves via __getattr__ without top-level import."""
        import src.llm as llm_pkg
        cls = llm_pkg.ClaudeClient
        assert cls is not None

    def test_gpt_client_lazy_load(self):
        """src.llm.GPTClient resolves via __getattr__."""
        import src.llm as llm_pkg
        cls = llm_pkg.GPTClient
        assert cls is not None

    def test_unknown_attr_raises_attribute_error(self):
        import src.llm as llm_pkg
        with pytest.raises(AttributeError, match="has no attribute"):
            _ = llm_pkg.NonExistentClient  # type: ignore[attr-defined]

    def test_claude_client_is_correct_class(self):
        import src.llm as llm_pkg
        from src.llm.claude_client import ClaudeClient
        assert llm_pkg.ClaudeClient is ClaudeClient

    def test_gpt_client_is_correct_class(self):
        import src.llm as llm_pkg
        from src.llm.gpt_client import GPTClient
        assert llm_pkg.GPTClient is GPTClient
