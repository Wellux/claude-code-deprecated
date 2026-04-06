"""LLM Router — auto-select the right model based on task signals.

Decision logic (in priority order):
1. Explicit override → use it
2. Task complexity score → opus / sonnet / haiku
3. Cost sensitivity flag → prefer haiku
4. Latency sensitivity flag → prefer haiku
5. Default → sonnet (best cost/quality balance)

Complexity scoring:
- HIGH  (score 7-10): architecture, security audit, multi-file refactor, novel research
- MED   (score 4-6):  feature implementation, code review, debugging, writing
- LOW   (score 0-3):  lookups, summaries, simple transforms, formatting
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Model(StrEnum):
    OPUS   = "claude-opus-4-6"
    SONNET = "claude-sonnet-4-6"
    HAIKU  = "claude-haiku-4-5-20251001"


class Complexity(StrEnum):
    HIGH   = "high"
    MEDIUM = "medium"
    LOW    = "low"


@dataclass
class RoutingDecision:
    model: Model
    complexity: Complexity
    reason: str
    score: int
    estimated_cost_tier: str  # "high" | "medium" | "low"


# Keywords that signal high complexity (score +2 each)
_HIGH_SIGNALS = [
    "architect", "design system", "security audit", "audit", "refactor entire",
    "migrate", "first principles", "research", "novel", "complex", "multi-step",
    "orchestrate", "swarm", "strategy", "evaluate", "benchmark", "analyze all",
    "production system", "trade-off", "tradeoff",
]

# Keywords that signal low complexity (score -2 each)
_LOW_SIGNALS = [
    "summarize", "summary", "list", "what is", "explain briefly", "format",
    "rename", "typo", "simple", "quick", "one-liner", "translate", "convert",
    "count", "grep", "find", "lookup", "check if", "does this",
    "status", "standup", "changelog entry",
]

# Keywords that force haiku regardless of complexity
_HAIKU_FORCE = [
    "fast", "quickly", "low latency", "cheap", "minimal cost", "batch",
    "streaming autocomplete", "inline suggestion",
]


def score_complexity(task: str) -> tuple[int, list[str]]:
    """Return (raw_score, matched_signals) for a task description."""
    task_lower = task.lower()
    score = 5  # baseline = medium
    matched: list[str] = []

    for sig in _HIGH_SIGNALS:
        if sig in task_lower:
            score += 2
            matched.append(f"+2 [{sig}]")

    for sig in _LOW_SIGNALS:
        if sig in task_lower:
            score -= 2
            matched.append(f"-2 [{sig}]")

    return max(0, min(10, score)), matched


def route_llm(
    task: str,
    *,
    override: Model | str | None = None,
    cost_sensitive: bool = False,
    latency_sensitive: bool = False,
    min_complexity: Complexity | None = None,
) -> RoutingDecision:
    """Select the best model for a given task.

    Args:
        task: Natural language description of what needs to be done.
        override: Force a specific model (skips all routing logic).
        cost_sensitive: Prefer cheaper models when quality is adequate.
        latency_sensitive: Prefer faster models (haiku first).
        min_complexity: Floor the complexity level (e.g. never route below MEDIUM).

    Returns:
        RoutingDecision with model, reasoning, and cost tier.
    """
    # 1. Explicit override
    if override:
        model = Model(override) if isinstance(override, str) else override
        return RoutingDecision(
            model=model,
            complexity=Complexity.MEDIUM,
            reason=f"explicit override → {model.value}",
            score=-1,
            estimated_cost_tier="override",
        )

    # 2. Haiku force signals
    task_lower = task.lower()
    for sig in _HAIKU_FORCE:
        if sig in task_lower:
            return RoutingDecision(
                model=Model.HAIKU,
                complexity=Complexity.LOW,
                reason=f"latency/cost signal [{sig}] → haiku",
                score=0,
                estimated_cost_tier="low",
            )

    # 3. Score the task
    score, signals = score_complexity(task)

    # 4. Latency/cost overrides push toward lighter models
    if latency_sensitive or cost_sensitive:
        score = max(0, score - 3)

    # 5. Map score → complexity
    if score >= 7:
        complexity = Complexity.HIGH
    elif score >= 4:
        complexity = Complexity.MEDIUM
    else:
        complexity = Complexity.LOW

    # 6. Apply min_complexity floor
    if min_complexity:
        order = [Complexity.LOW, Complexity.MEDIUM, Complexity.HIGH]
        if order.index(complexity) < order.index(min_complexity):
            complexity = min_complexity
            score = max(score, 4 if min_complexity == Complexity.MEDIUM else 7)

    # 7. Select model
    if complexity == Complexity.HIGH:
        model = Model.OPUS
        cost_tier = "high"
    elif complexity == Complexity.MEDIUM:
        model = Model.SONNET
        cost_tier = "medium"
    else:
        model = Model.HAIKU
        cost_tier = "low"

    reason = f"score={score}/10 [{', '.join(signals) or 'baseline'}] → {complexity.value} → {model.value}"

    return RoutingDecision(
        model=model,
        complexity=complexity,
        reason=reason,
        score=score,
        estimated_cost_tier=cost_tier,
    )


# Convenience shortcuts
def cheap(task: str) -> RoutingDecision:
    """Route with cost sensitivity on."""
    return route_llm(task, cost_sensitive=True)


def fast(task: str) -> RoutingDecision:
    """Route with latency sensitivity on."""
    return route_llm(task, latency_sensitive=True)


def best(task: str) -> RoutingDecision:
    """Route to highest quality model (min MEDIUM complexity)."""
    return route_llm(task, min_complexity=Complexity.MEDIUM)
