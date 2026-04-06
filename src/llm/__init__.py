"""LLM client package."""
from .base import CompletionRequest, CompletionResponse, LLMClient
from .utils import build_request, merge_system_prompts, truncate_to_tokens


def __getattr__(name: str):
    if name == "ClaudeClient":
        from .claude_client import ClaudeClient
        return ClaudeClient
    if name == "GPTClient":
        from .gpt_client import GPTClient
        return GPTClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "LLMClient",
    "CompletionRequest",
    "CompletionResponse",
    "ClaudeClient",
    "GPTClient",
    "build_request",
    "truncate_to_tokens",
    "merge_system_prompts",
]
