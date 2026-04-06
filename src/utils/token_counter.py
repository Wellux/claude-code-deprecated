"""Token counting utilities."""
from __future__ import annotations

# Approximate chars-per-token ratios by model family
_CHARS_PER_TOKEN = {
    "claude": 3.8,
    "gpt-4": 4.0,
    "gpt-3.5": 4.0,
    "default": 4.0,
}


def count_tokens_approx(text: str, model: str = "default") -> int:
    """Return approximate token count for text.

    Uses character-based heuristic (~4 chars/token for English).
    For production use, call the model's tokenizer API directly.
    """
    ratio = _CHARS_PER_TOKEN.get("default", 4.0)
    for prefix, chars in _CHARS_PER_TOKEN.items():
        if model.startswith(prefix):
            ratio = chars
            break
    return max(1, int(len(text) / ratio))


def fits_in_context(text: str, model: str, context_limit: int) -> bool:
    """Return True if text likely fits within context_limit tokens."""
    return count_tokens_approx(text, model) <= context_limit


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    input_cost_per_mtok: float,
    output_cost_per_mtok: float,
) -> float:
    """Compute USD cost from token counts and per-million-token rates."""
    return (input_tokens * input_cost_per_mtok + output_tokens * output_cost_per_mtok) / 1_000_000


def split_into_chunks(text: str, max_tokens: int, model: str = "default") -> list[str]:
    """Split text into chunks that each fit within max_tokens."""
    ratio = _CHARS_PER_TOKEN.get("default", 4.0)
    for prefix, chars in _CHARS_PER_TOKEN.items():
        if model.startswith(prefix):
            ratio = chars
            break
    max_chars = int(max_tokens * ratio)
    chunks = []
    while text:
        chunks.append(text[:max_chars])
        text = text[max_chars:]
    return chunks
