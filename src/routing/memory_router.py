"""Memory Router — decide WHERE to store information.

Five memory tiers, each with different persistence, scope, and retrieval:

  Tier 1  response_cache   In-memory (session)     Fast LLM response dedup
  Tier 2  files            Filesystem (permanent)   Research docs, outputs
  Tier 3  lessons          tasks/lessons.md         Self-improvement rules
  Tier 4  mcp_memory       MCP memory server        Cross-session facts/entities
  Tier 5  claude_md        CLAUDE.md / tasks/       Project rules + todos

Routing signals:
  - Is this a correction / mistake? → lessons
  - Is this a factual finding / entity? → mcp_memory
  - Is this a project rule / constraint? → claude_md
  - Is this research output? → files (data/research/)
  - Is this a repeated LLM call? → response_cache
  - Is this a task / todo? → tasks/todo.md
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class MemoryTier(StrEnum):
    CACHE    = "response_cache"
    FILES    = "files"
    LESSONS  = "lessons"
    MCP      = "mcp_memory"
    CLAUDE   = "claude_md"
    TODO     = "todo"


@dataclass
class MemoryDecision:
    tier: MemoryTier
    destination: str        # file path or store name
    ttl: str                # "session" | "permanent" | "project-lifetime"
    reason: str
    action: str             # "append" | "write" | "upsert" | "cache"
    template: str = ""      # suggested format for writing


# ── Signal tables ────────────────────────────────────────────────────────────

_LESSON_SIGNALS = [
    "mistake", "correction", "wrong", "i was wrong", "don't do that",
    "lesson learned", "next time", "rule:", "prevent", "don't forget",
    "you should always", "you should never", "pattern to avoid",
]

_MCP_SIGNALS = [
    "remember that", "note that", "keep in mind", "entity:", "fact:",
    "this project uses", "the team prefers", "we decided", "key decision",
    "architecture choice", "important context", "cross-session",
    "persist this", "store this fact",
]

_CLAUDE_MD_SIGNALS = [
    "add to claude.md", "project rule", "always do", "never do",
    "workflow rule", "coding standard", "our convention", "team rule",
    "every session", "boot rule", "global rule",
]

_RESEARCH_SIGNALS = [
    "research finding", "paper says", "study found", "from the docs",
    "technical finding", "benchmark result", "key insight from",
    "write to research", "save research", "store this research",
    # broader patterns
    "finding", "important finding", "key finding", "discovered that",
    "we found", "results show", "data shows", "analysis shows",
    "insight", "key insight", "from research", "research shows",
]

_TODO_SIGNALS = [
    "add to todo", "open task", "pending", "need to", "should do",
    "don't forget to", "remember to", "follow-up", "next step",
    "track this", "backlog",
    # broader patterns
    "todo list", "to-do", "task list", "add task", "add this task",
    "create a task", "new task", "assign task",
]

_CACHE_SIGNALS = [
    "same prompt", "repeated call", "cache this response", "reuse this",
    "don't call again", "already computed",
    # broader patterns
    "cache this", "repeated", "repeat this", "call again", "same result",
    "duplicate call", "idempotent", "memoize",
]


def _score(text: str, signals: list[str]) -> int:
    return sum(1 for s in signals if s in text)


def route_memory(
    content: str,
    *,
    content_type: str | None = None,
    project_root: str = "/home/user/wellux_testprojects",
) -> MemoryDecision:
    """Decide where to store the given content.

    Args:
        content: The thing to be stored (text description or actual content).
        content_type: Optional hint: "research" | "lesson" | "fact" | "task" | "rule"
        project_root: Absolute path to the project.

    Returns:
        MemoryDecision with tier, destination path, and write template.
    """
    text = content.lower()
    root = Path(project_root)

    # Explicit content_type overrides signals
    if content_type:
        ct = content_type.lower()
        if ct == "lesson":
            return _lesson_decision(root)
        if ct == "research":
            return _research_decision(root)
        if ct == "fact":
            return _mcp_decision()
        if ct == "task":
            return _todo_decision(root)
        if ct == "rule":
            return _claude_md_decision(root)

    # Signal-based routing
    scores = {
        MemoryTier.LESSONS: _score(text, _LESSON_SIGNALS),
        MemoryTier.MCP:     _score(text, _MCP_SIGNALS),
        MemoryTier.CLAUDE:  _score(text, _CLAUDE_MD_SIGNALS),
        MemoryTier.FILES:   _score(text, _RESEARCH_SIGNALS),
        MemoryTier.TODO:    _score(text, _TODO_SIGNALS),
        MemoryTier.CACHE:   _score(text, _CACHE_SIGNALS),
    }

    best_tier = max(scores, key=lambda t: scores[t])
    if scores[best_tier] == 0:
        # Default: important enough to store → MCP memory
        return _mcp_decision(reason="no strong signal — defaulting to MCP memory")

    if best_tier == MemoryTier.LESSONS:
        return _lesson_decision(root)
    if best_tier == MemoryTier.FILES:
        return _research_decision(root)
    if best_tier == MemoryTier.CLAUDE:
        return _claude_md_decision(root)
    if best_tier == MemoryTier.TODO:
        return _todo_decision(root)
    if best_tier == MemoryTier.CACHE:
        return MemoryDecision(
            tier=MemoryTier.CACHE,
            destination="ResponseCache (in-memory)",
            ttl="session",
            reason="repeated/cached LLM call signal",
            action="cache",
            template="ResponseCache.set(request, response)",
        )
    return _mcp_decision()


# ── Decision constructors ────────────────────────────────────────────────────

def _lesson_decision(root: Path, reason: str = "mistake/correction signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.LESSONS,
        destination=str(root / "tasks/lessons.md"),
        ttl="permanent",
        reason=reason,
        action="append",
        template=(
            "\n## Lesson — {date}: {short_title}\n"
            "**Mistake:** {what_went_wrong}\n"
            "**Why:** {root_cause}\n"
            "**Rule:** {one_sentence_rule}\n"
            "**Example:** {correct_behavior}\n"
        ),
    )


def _research_decision(root: Path, reason: str = "research finding signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.FILES,
        destination=str(root / "data/research/{date}-{slug}.md"),
        ttl="permanent",
        reason=reason,
        action="write",
        template=(
            "# Research: {topic}\n"
            "**Date:** {date}\n\n"
            "## Core Concept\n{concept}\n\n"
            "## Key Insight\n{insight}\n\n"
            "## Implementation Pattern\n```python\n{code}\n```\n\n"
            "## Actionable Insight\n{action}\n\n"
            "## Sources\n{sources}\n"
        ),
    )


def _mcp_decision(reason: str = "fact/entity signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.MCP,
        destination="mcp__memory (MCP memory server)",
        ttl="permanent",
        reason=reason,
        action="upsert",
        template=(
            "mcp__memory__create_entities([\n"
            "  {{'name': '{entity}', 'entityType': '{type}', "
            "'observations': ['{fact}']}}\n"
            "])"
        ),
    )


def _claude_md_decision(root: Path, reason: str = "project rule signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.CLAUDE,
        destination=str(root / "CLAUDE.md"),
        ttl="project-lifetime",
        reason=reason,
        action="append",
        template="- **Rule:** {rule_text}  ← added {date}",
    )


def _todo_decision(root: Path, reason: str = "task/todo signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.TODO,
        destination=str(root / "tasks/todo.md"),
        ttl="permanent",
        reason=reason,
        action="append",
        template="- [ ] {task_description}",
    )


# ── Convenience: store a lesson directly ────────────────────────────────────

def format_lesson(
    date: str,
    title: str,
    mistake: str,
    why: str,
    rule: str,
    example: str,
) -> str:
    """Format a lesson entry ready to append to lessons.md."""
    return (
        f"\n## Lesson — {date}: {title}\n"
        f"**Mistake:** {mistake}\n"
        f"**Why:** {why}\n"
        f"**Rule:** {rule}\n"
        f"**Example:** {example}\n"
    )
