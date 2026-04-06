"""LLM utility helpers."""
from __future__ import annotations

from .base import CompletionRequest, LLMClient


def build_request(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> CompletionRequest:
    """Convenience constructor for CompletionRequest."""
    return CompletionRequest(
        prompt=prompt,
        system=system,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def truncate_to_tokens(text: str, max_tokens: int, chars_per_token: int = 4) -> str:
    """Truncate text to approximately max_tokens."""
    max_chars = max_tokens * chars_per_token
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def merge_system_prompts(*prompts: str | None, separator: str = "\n\n") -> str | None:
    """Merge multiple system prompt fragments, skipping None/empty."""
    parts = [p for p in prompts if p and p.strip()]
    return separator.join(parts) if parts else None


def format_messages_as_prompt(messages: list[dict]) -> str:
    """Convert chat message list to a flat prompt string for non-chat APIs."""
    lines = []
    for msg in messages:
        role = msg.get("role", "user").upper()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


async def complete_with_fallback(
    primary: LLMClient,
    fallback: LLMClient,
    request: CompletionRequest,
):
    """Try primary client, fall back to secondary on any error."""
    try:
        return await primary.complete(request)
    except Exception as primary_err:
        from ..utils.logger import get_logger
        logger = get_logger(__name__)
        logger.warning("primary_client_failed", error=str(primary_err), falling_back=True)
        return await fallback.complete(request)
