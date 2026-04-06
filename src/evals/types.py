"""Core data types for the eval framework."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Verdict(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


@dataclass
class EvalCase:
    """A single evaluation case: input → expected output + scoring criteria."""
    id: str
    prompt: str
    expected: str | None = None          # exact or reference answer
    contains: list[str] = field(default_factory=list)   # required substrings
    excludes: list[str] = field(default_factory=list)   # forbidden substrings
    max_tokens: int = 512
    temperature: float = 0.0             # 0 = deterministic for evals
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("EvalCase.id must be non-empty")
        if not self.prompt:
            raise ValueError("EvalCase.prompt must be non-empty")


@dataclass
class EvalResult:
    """Result of running one EvalCase."""
    case_id: str
    verdict: Verdict
    actual: str = ""
    score: float = 0.0          # 0.0–1.0
    reason: str = ""
    latency_ms: float = 0.0
    tokens_used: int = 0
    error: str | None = None
    tags: list[str] = field(default_factory=list)  # propagated from EvalCase


@dataclass
class EvalReport:
    """Aggregated results across an entire EvalSuite run."""
    suite_name: str
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    results: list[EvalResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        denom = self.total - self.skipped
        return self.passed / denom if denom > 0 else 0.0

    @property
    def mean_score(self) -> float:
        scored = [r.score for r in self.results if r.verdict not in (Verdict.SKIP, Verdict.ERROR)]
        return sum(scored) / len(scored) if scored else 0.0

    @property
    def mean_latency_ms(self) -> float:
        timed = [r.latency_ms for r in self.results if r.latency_ms > 0]
        return sum(timed) / len(timed) if timed else 0.0

    def summary(self) -> str:
        bar = "█" * self.passed + "░" * self.failed + "·" * self.skipped
        return (
            f"Suite : {self.suite_name}\n"
            f"Result: {self.passed}/{self.total - self.skipped} passed "
            f"({self.pass_rate:.0%})  errors={self.errors}\n"
            f"Score : {self.mean_score:.2f}  latency={self.mean_latency_ms:.0f}ms avg\n"
            f"        [{bar}]"
        )

    def failures(self) -> list[EvalResult]:
        return [r for r in self.results if r.verdict == Verdict.FAIL]

    def by_tag(self, tag: str) -> list[EvalResult]:
        return [r for r in self.results if tag in r.tags]
