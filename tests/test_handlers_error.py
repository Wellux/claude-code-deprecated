"""Tests for src/handlers/error_handler.py."""
from __future__ import annotations

import pytest

from src.handlers.error_handler import (
    AuthError,
    ContentFilterError,
    LLMError,
    RateLimitError,
    TokenLimitError,
    classify_api_error,
    handle_errors,
)


class TestClassifyApiError:
    def test_rate_limit_error(self):
        err = classify_api_error(Exception("rate limit exceeded"))
        assert isinstance(err, RateLimitError)

    def test_429_code_maps_to_rate_limit(self):
        err = classify_api_error(Exception("HTTP 429 too many requests"))
        assert isinstance(err, RateLimitError)

    def test_token_limit_error(self):
        err = classify_api_error(Exception("context length limit exceeded"))
        assert isinstance(err, TokenLimitError)

    def test_auth_error(self):
        err = classify_api_error(Exception("authentication failed invalid api key"))
        assert isinstance(err, AuthError)

    def test_401_maps_to_auth(self):
        err = classify_api_error(Exception("401 unauthorized"))
        assert isinstance(err, AuthError)

    def test_content_filter_error(self):
        err = classify_api_error(Exception("content policy violation"))
        assert isinstance(err, ContentFilterError)

    def test_unknown_error_maps_to_llm_error(self):
        err = classify_api_error(Exception("something completely unknown"))
        assert isinstance(err, LLMError)

    def test_preserves_message(self):
        err = classify_api_error(Exception("rate limit exceeded"))
        assert "rate limit exceeded" in str(err)

    # ── Bug-fix regression: operator precedence (Bug 1) ───────────────────────

    def test_context_alone_is_not_token_limit(self):
        """'context' without 'window'/'length' must not map to TokenLimitError."""
        err = classify_api_error(Exception("invalid context path in config"))
        assert not isinstance(err, TokenLimitError)
        assert isinstance(err, LLMError)

    def test_context_window_maps_to_token_limit(self):
        err = classify_api_error(Exception("context window limit exceeded"))
        assert isinstance(err, TokenLimitError)

    def test_context_length_maps_to_token_limit(self):
        err = classify_api_error(Exception("context length limit exceeded"))
        assert isinstance(err, TokenLimitError)

    def test_token_limit_maps_to_token_limit(self):
        err = classify_api_error(Exception("token limit reached: 200k"))
        assert isinstance(err, TokenLimitError)

    def test_asyncio_context_is_not_token_limit(self):
        """Asyncio context-related messages must not route to TokenLimitError."""
        err = classify_api_error(Exception("asyncio context var reset failed"))
        assert not isinstance(err, TokenLimitError)

    def test_content_filter_requires_both_content_and_filter(self):
        """'content' alone without 'filter' must not map to ContentFilterError."""
        err = classify_api_error(Exception("content type mismatch"))
        assert not isinstance(err, ContentFilterError)

    def test_policy_violation_maps_to_content_filter(self):
        err = classify_api_error(Exception("policy violation detected"))
        assert isinstance(err, ContentFilterError)

    def test_content_filter_phrase_maps_correctly(self):
        err = classify_api_error(Exception("content filter blocked the response"))
        assert isinstance(err, ContentFilterError)


class TestHandleErrors:
    async def test_passes_through_on_success(self):
        @handle_errors
        async def _fn():
            return 42

        assert await _fn() == 42

    async def test_llm_error_reraises_unchanged(self):
        """LLMError subclasses pass through without re-wrapping."""
        @handle_errors
        async def _fn():
            raise RateLimitError("already classified")

        with pytest.raises(RateLimitError, match="already classified"):
            await _fn()

    async def test_generic_exception_is_classified(self):
        """Non-LLMError exceptions are mapped to the LLMError hierarchy."""
        @handle_errors
        async def _fn():
            raise ValueError("401 bad key")

        with pytest.raises(AuthError):
            await _fn()

    async def test_chained_exception_preserved(self):
        """Classified error must chain via __cause__ to the original."""
        original = RuntimeError("rate limit exceeded")

        @handle_errors
        async def _fn():
            raise original

        with pytest.raises(RateLimitError) as exc_info:
            await _fn()
        assert exc_info.value.__cause__ is original

    async def test_preserves_function_name(self):
        @handle_errors
        async def my_special_fn():
            return "ok"

        assert my_special_fn.__name__ == "my_special_fn"

    async def test_unknown_exception_becomes_llm_error(self):
        @handle_errors
        async def _fn():
            raise OSError("disk full")

        with pytest.raises(LLMError):
            await _fn()


class TestErrorHierarchy:
    def test_rate_limit_is_llm_error(self):
        assert issubclass(RateLimitError, LLMError)

    def test_token_limit_is_llm_error(self):
        assert issubclass(TokenLimitError, LLMError)

    def test_auth_is_llm_error(self):
        assert issubclass(AuthError, LLMError)

    def test_content_filter_is_llm_error(self):
        assert issubclass(ContentFilterError, LLMError)
