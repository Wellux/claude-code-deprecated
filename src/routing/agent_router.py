"""Agent Router — dispatch tasks to the right autonomous agent.

Four agents available:
  ralph-loop         Self-driving dev loop. Read todo → plan → implement → verify → repeat.
  research-agent     Karpathy research. Search → distill → implement → store.
  swarm-orchestrator Parallel decomposition. Splits task into independent workstreams.
  security-reviewer  Full security sweep. 6-domain audit → report.

Routing signals:
  - Task duration: long-running → ralph-loop; bounded → others
  - Task type: research → research-agent; security → security-reviewer
  - Parallelism: multiple independent workstreams → swarm
  - Default for "just build it": ralph-loop
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Agent(StrEnum):
    RALPH      = "ralph-loop"
    RESEARCH   = "research-agent"
    SWARM      = "swarm-orchestrator"
    SECURITY   = "security-reviewer"


@dataclass
class AgentDecision:
    agent: Agent
    confidence: float          # 0.0 – 1.0
    reason: str
    spawn_count: int = 1       # for swarm: how many subagents to suggest
    context_hints: list[str] = None  # extra context to pass to the agent

    def __post_init__(self):
        if self.context_hints is None:
            self.context_hints = []


# ── Routing signal tables ────────────────────────────────────────────────────

_RALPH_SIGNALS = [
    "implement", "build", "create", "add feature", "fix bug", "refactor",
    "autonomous", "keep going", "loop until", "self-driving", "run autonomously",
    "todo list", "work through", "complete all", "ship this", "just do it",
    "ralph", "dev loop", "long session",
]

_RESEARCH_SIGNALS = [
    "research", "deep dive", "what is", "explain", "first principles",
    "latest on", "summarize paper", "find out", "investigate", "learn about",
    "karpathy", "study", "understand", "arxiv", "literature", "state of the art",
    "weekly research", "trend", "what's new in",
]

_SWARM_SIGNALS = [
    "parallel", "simultaneously", "at the same time", "multiple", "in parallel",
    "swarm", "split into", "decompose", "distribute", "concurrent tasks",
    "independent", "all at once", "batch of", "across all", "every module",
    "all services", "full audit of all",
]

_SECURITY_SIGNALS = [
    "security review", "security audit", "pentest", "vulnerability scan",
    "check for vulns", "security sweep", "audit the code", "cve", "owasp audit",
    "security report", "find security issues", "check my code for security",
    "is this secure", "harden", "threat model",
]


def _score(text: str, signals: list[str]) -> int:
    return sum(1 for s in signals if s in text)


def route_agent(task: str, *, context: str | None = None) -> AgentDecision:
    """Select the best agent for the given task.

    Args:
        task: Natural language task description.
        context: Optional extra context (e.g. current todo.md contents).

    Returns:
        AgentDecision with agent, confidence, and hints.
    """
    text = (task + " " + (context or "")).lower()

    scores = {
        Agent.RALPH:    _score(text, _RALPH_SIGNALS),
        Agent.RESEARCH: _score(text, _RESEARCH_SIGNALS),
        Agent.SWARM:    _score(text, _SWARM_SIGNALS),
        Agent.SECURITY: _score(text, _SECURITY_SIGNALS),
    }

    best_agent = max(scores, key=lambda a: scores[a])
    best_score = scores[best_agent]

    # Tie-break or no signal → default to ralph-loop (build mode)
    if best_score == 0:
        return AgentDecision(
            agent=Agent.RALPH,
            confidence=0.4,
            reason="no strong signal — defaulting to ralph-loop (build mode)",
            context_hints=["Read tasks/todo.md for pending work"],
        )

    total = sum(scores.values()) or 1
    confidence = round(best_score / total, 2)

    hints: list[str] = []

    if best_agent == Agent.RALPH:
        hints = [
            "Read tasks/todo.md first",
            "Mark steps complete as you go",
            "Commit after each completed step",
        ]
    elif best_agent == Agent.RESEARCH:
        hints = [
            "Follow Karpathy method: Search → Distill → Implement → Store",
            "Write output to data/research/YYYY-MM-DD-<slug>.md",
            "Extract lessons to tasks/lessons.md",
        ]
    elif best_agent == Agent.SWARM:
        # Estimate parallelism from task size signals
        spawn = 3  # default
        if any(w in text for w in ["all", "every", "each", "full"]):
            spawn = 5
        hints = [
            f"Decompose into ~{spawn} independent workstreams",
            "Assign non-overlapping file paths to each agent",
            "Synthesize results in final round",
        ]
        return AgentDecision(
            agent=Agent.SWARM,
            confidence=confidence,
            reason=f"swarm signals ({best_score}) — parallel decomposition",
            spawn_count=spawn,
            context_hints=hints,
        )
    elif best_agent == Agent.SECURITY:
        hints = [
            "Run all 6 security domains: AppSec, AI Security, Deps, Secrets, IAM, GRC",
            "Write report to data/outputs/security-report-<date>.md",
            "Flag critical issues immediately",
        ]

    return AgentDecision(
        agent=best_agent,
        confidence=confidence,
        reason=f"signal score={best_score} for {best_agent.value}",
        context_hints=hints,
    )


def route_multi_agent(task: str) -> list[AgentDecision]:
    """Return ranked list of all agents with their scores.

    Useful when you want to see all options, not just the top pick.
    """
    text = task.lower()
    results = []
    _total_signals = sum([
        len(_RALPH_SIGNALS), len(_RESEARCH_SIGNALS),
        len(_SWARM_SIGNALS), len(_SECURITY_SIGNALS),
    ])

    for agent, signals in [
        (Agent.RALPH, _RALPH_SIGNALS),
        (Agent.RESEARCH, _RESEARCH_SIGNALS),
        (Agent.SWARM, _SWARM_SIGNALS),
        (Agent.SECURITY, _SECURITY_SIGNALS),
    ]:
        score = _score(text, signals)
        confidence = round(score / max(len(signals), 1), 2)
        results.append(AgentDecision(
            agent=agent,
            confidence=confidence,
            reason=f"{score} signal matches",
        ))

    results.sort(key=lambda d: d.confidence, reverse=True)
    return results
