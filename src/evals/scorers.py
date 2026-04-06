"""Scoring functions for eval outputs.

Each scorer takes (actual: str, case: EvalCase) → (score: float, reason: str).
score is 0.0–1.0; reason is a human-readable explanation.
"""
from __future__ import annotations

import re
from collections.abc import Callable

from .types import EvalCase

ScorerFn = Callable[[str, EvalCase], tuple[float, str]]


def exact_match(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if actual matches expected exactly (stripped), else 0.0."""
    if case.expected is None:
        return 1.0, "no expected — skip exact match"
    match = actual.strip() == case.expected.strip()
    return (1.0, "exact match") if match else (0.0, f"expected {case.expected!r}, got {actual!r}")


def contains_all(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if all required substrings are present, partial credit otherwise."""
    if not case.contains:
        return 1.0, "no contains constraints"
    found = [s for s in case.contains if s.lower() in actual.lower()]
    score = len(found) / len(case.contains)
    missing = [s for s in case.contains if s not in found]
    reason = f"{len(found)}/{len(case.contains)} required strings found"
    if missing:
        reason += f"; missing: {missing}"
    return score, reason


def excludes_none(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if no forbidden substrings are present."""
    if not case.excludes:
        return 1.0, "no excludes constraints"
    found = [s for s in case.excludes if s.lower() in actual.lower()]
    if found:
        return 0.0, f"forbidden strings found: {found}"
    return 1.0, "no forbidden strings found"


def non_empty(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if response is non-empty."""
    stripped = actual.strip()
    return (1.0, "non-empty response") if stripped else (0.0, "empty response")


def min_length(min_chars: int) -> ScorerFn:
    """Factory: 1.0 if response is at least min_chars long."""
    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        n = len(actual.strip())
        if n >= min_chars:
            return 1.0, f"length {n} >= {min_chars}"
        return n / min_chars, f"length {n} < {min_chars} required"
    return _score


def max_length(max_chars: int) -> ScorerFn:
    """Factory: 1.0 if response is at most max_chars long."""
    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        n = len(actual.strip())
        if n <= max_chars:
            return 1.0, f"length {n} <= {max_chars}"
        return 0.0, f"length {n} > {max_chars} max"
    return _score


def regex_match(pattern: str, flags: int = re.IGNORECASE) -> ScorerFn:
    """Factory: 1.0 if response matches regex pattern."""
    compiled = re.compile(pattern, flags)
    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        if compiled.search(actual):
            return 1.0, f"regex {pattern!r} matched"
        return 0.0, f"regex {pattern!r} not found"
    return _score


def composite(*scorers: ScorerFn, weights: list[float] | None = None) -> ScorerFn:
    """Weighted average of multiple scorers. Defaults to equal weights."""
    if weights is None:
        weights = [1.0] * len(scorers)
    if len(weights) != len(scorers):
        raise ValueError("weights length must match scorers length")
    total_weight = sum(weights)

    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        parts = []
        weighted_sum = 0.0
        for scorer, w in zip(scorers, weights, strict=True):
            s, r = scorer(actual, case)
            weighted_sum += s * w
            parts.append(f"{scorer.__name__}={s:.2f} ({r})")
        final = weighted_sum / total_weight
        return final, " | ".join(parts)

    _score.__name__ = "composite"
    return _score


# Default scorer: non_empty + contains_all + excludes_none
DEFAULT_SCORER: ScorerFn = composite(non_empty, contains_all, excludes_none)
