"""Centralized error handling and classification."""
from __future__ import annotations

import functools
import traceback
from collections.abc import Callable
from typing import Any, TypeVar

from ..utils.logger import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class LLMError(Exception):
    """Base class for LLM-related errors."""


class RateLimitError(LLMError):
    """API rate limit exceeded."""


class TokenLimitError(LLMError):
    """Prompt exceeds model context window."""


class AuthError(LLMError):
    """API authentication failure."""


class ContentFilterError(LLMError):
    """Response blocked by content filter."""


def classify_api_error(exc: Exception) -> LLMError:
    """Map provider-specific exceptions to our error hierarchy."""
    msg = str(exc).lower()
    if "rate limit" in msg or "429" in msg:
        return RateLimitError(str(exc))
    if (("context" in msg and ("window" in msg or "length" in msg))
            or ("token" in msg and "limit" in msg)):
        return TokenLimitError(str(exc))
    if "auth" in msg or "401" in msg or "api key" in msg:
        return AuthError(str(exc))
    if ("content" in msg and "filter" in msg) or "policy violation" in msg:
        return ContentFilterError(str(exc))
    return LLMError(str(exc))


def handle_errors(func: F) -> F:
    """Decorator: log and re-raise exceptions with structured context."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except LLMError:
            raise
        except Exception as exc:
            logger.error(
                "unhandled_error",
                func=func.__qualname__,
                error_type=type(exc).__name__,
                error=str(exc),
                traceback=traceback.format_exc(),
            )
            raise classify_api_error(exc) from exc

    return wrapper  # type: ignore[return-value]
