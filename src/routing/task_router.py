"""Task Router — decompose complex tasks and dispatch subtasks to subagents.

Responsibilities:
  1. Classify task size (atomic / medium / complex)
  2. For complex tasks: decompose into independent subtasks
  3. Assign each subtask to the right agent + model
  4. Detect parallelism (independent vs sequential)
  5. Return an execution plan

Decomposition rules:
  - Independent tasks (no shared state) → parallel swarm agents
  - Sequential tasks (output of A feeds B) → ralph-loop with ordered steps
  - Research + implementation → research-agent first, ralph-loop second
  - Security review + fix → security-reviewer first, ralph-loop second
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal

from .agent_router import Agent, route_agent
from .llm_router import Model, route_llm
from .skill_router import route_skill


class TaskSize(StrEnum):
    ATOMIC  = "atomic"   # single action, no decomposition needed
    MEDIUM  = "medium"   # 2-4 steps, single agent
    COMPLEX = "complex"  # 5+ steps or multiple parallel workstreams


class Dependency(StrEnum):
    NONE       = "none"        # fully independent
    SEQUENTIAL = "sequential"  # A → B → C
    PARALLEL   = "parallel"    # A ∥ B ∥ C → merge


@dataclass
class Subtask:
    id: str                        # e.g. "1.1", "2.a"
    description: str
    agent: Agent
    model: Model
    skill: str | None
    depends_on: list[str] = field(default_factory=list)  # ids of blocking subtasks
    estimated_tokens: int = 4096
    context_hints: list[str] = field(default_factory=list)


@dataclass
class TaskPlan:
    original_task: str
    size: TaskSize
    dependency: Dependency
    subtasks: list[Subtask]
    estimated_total_cost_tier: str  # "low" | "medium" | "high"
    execution_mode: Literal["single", "sequential", "parallel"]
    notes: str = ""

    def summary(self) -> str:
        lines = [
            f"Task: {self.original_task[:80]}",
            f"Size: {self.size.value} | Mode: {self.execution_mode} | Cost: {self.estimated_total_cost_tier}",
            f"Subtasks ({len(self.subtasks)}):",
        ]
        for st in self.subtasks:
            dep = f" [after {', '.join(st.depends_on)}]" if st.depends_on else ""
            lines.append(f"  {st.id}. [{st.agent.value}] {st.description[:60]}{dep}")
        return "\n".join(lines)


MAX_SUBTASKS = 10  # hard cap — prevents runaway decomposition


# ── Size classification ───────────────────────────────────────────────────────

_COMPLEX_SIGNALS = [
    "entire", "full", "all modules", "end-to-end", "from scratch",
    "complete system", "migrate", "redesign", "overhaul", "comprehensive",
    "phase", "multiple", "and also", "plus", "as well as", "in addition",
    # multi-step operations that always require decomposition
    "audit", "security audit", "full audit", "and fix", "and deploy",
    "implement and", "build and", "test and", "review and", "refactor and",
]

_ATOMIC_SIGNALS = [
    "fix this typo", "rename", "add a comment", "one line", "quick",
    "single function", "this file only", "just this", "small change",
]


def _classify_size(task: str) -> TaskSize:
    text = task.lower()
    complex_hits = sum(1 for s in _COMPLEX_SIGNALS if s in text)
    atomic_hits  = sum(1 for s in _ATOMIC_SIGNALS  if s in text)

    if atomic_hits > 0 and complex_hits == 0:
        return TaskSize.ATOMIC
    if complex_hits >= 2 or len(task.split()) > 40:
        return TaskSize.COMPLEX
    return TaskSize.MEDIUM


def _has_parallel_signal(task: str) -> bool:
    signals = ["parallel", "simultaneously", "at the same time", "independent",
               "concurrently", "in parallel", "swarm", "multiple workstreams"]
    return any(s in task.lower() for s in signals)


def _has_sequential_signal(task: str) -> bool:
    signals = ["first", "then", "after that", "once done", "next", "finally",
               "step by step", "in order", "sequentially"]
    return any(s in task.lower() for s in signals)


# ── Decomposition logic ───────────────────────────────────────────────────────

def _decompose_complex(task: str) -> list[Subtask]:
    """Break a complex task into subtasks with agent/model assignments."""
    text = task.lower()
    subtasks: list[Subtask] = []

    # Pattern: research + implement
    needs_research = any(w in text for w in ["research", "find out", "what is", "learn"])
    needs_security = any(w in text for w in ["secure", "security", "audit", "pentest"])
    needs_docs     = any(w in text for w in ["document", "readme", "runbook", "adr"])
    needs_tests    = any(w in text for w in ["test", "coverage", "pytest", "spec"])

    idx = 1

    if needs_research:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Research and distill key findings",
            agent=Agent.RESEARCH,
            model=Model.SONNET,
            skill="karpathy-researcher",
            context_hints=["Write findings to data/research/", "Extract lessons"],
        ))
        idx += 1

    if needs_security:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Security review: 6-domain sweep",
            agent=Agent.SECURITY,
            model=Model.OPUS,
            skill="ciso",
            context_hints=["Output to data/outputs/security-report-<date>.md"],
        ))
        idx += 1

    # Core implementation (depends on research if present)
    impl_deps = [str(i) for i in range(1, idx)]
    subtasks.append(Subtask(
        id=f"{idx}",
        description="Implement core feature / fix",
        agent=Agent.RALPH,
        model=route_llm(task).model,
        skill=None,
        depends_on=impl_deps,
        context_hints=["Read tasks/todo.md", "Commit after each step"],
    ))
    impl_id = str(idx)
    idx += 1

    if needs_tests:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Write tests and verify coverage",
            agent=Agent.RALPH,
            model=Model.SONNET,
            skill="test-writer",
            depends_on=[impl_id],
        ))
        idx += 1

    if needs_docs:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Write/update documentation",
            agent=Agent.RALPH,
            model=Model.HAIKU,
            skill="readme-writer",
            depends_on=[impl_id],
        ))
        idx += 1

    # If nothing matched, fall back to single ralph task (defensive — impl always appends above)
    if not subtasks:  # pragma: no cover
        subtasks.append(Subtask(
            id="1",
            description=task[:100],
            agent=Agent.RALPH,
            model=route_llm(task).model,
            skill=None,
        ))

    # Enforce hard cap — truncate rather than silently overflow
    if len(subtasks) > MAX_SUBTASKS:
        subtasks = subtasks[:MAX_SUBTASKS]

    return subtasks


def plan_task(task: str) -> TaskPlan:
    """Produce a full execution plan for the given task.

    Args:
        task: Natural language task description.

    Returns:
        TaskPlan with decomposed subtasks, agents, models, and execution mode.
    """
    size = _classify_size(task)
    parallel = _has_parallel_signal(task)
    sequential = _has_sequential_signal(task)

    # Atomic: single subtask, no decomposition
    if size == TaskSize.ATOMIC:
        agent_dec = route_agent(task)
        llm_dec   = route_llm(task)
        skill_dec = route_skill(task)
        return TaskPlan(
            original_task=task,
            size=size,
            dependency=Dependency.NONE,
            subtasks=[Subtask(
                id="1",
                description=task,
                agent=agent_dec.agent,
                model=llm_dec.model,
                skill=skill_dec.skill if skill_dec else None,
            )],
            estimated_total_cost_tier=llm_dec.estimated_cost_tier,
            execution_mode="single",
        )

    # Medium: single agent, sequential steps
    if size == TaskSize.MEDIUM:
        agent_dec = route_agent(task)
        llm_dec   = route_llm(task)
        return TaskPlan(
            original_task=task,
            size=size,
            dependency=Dependency.SEQUENTIAL,
            subtasks=[Subtask(
                id="1",
                description=task,
                agent=agent_dec.agent,
                model=llm_dec.model,
                skill=None,
                context_hints=agent_dec.context_hints,
            )],
            estimated_total_cost_tier=llm_dec.estimated_cost_tier,
            execution_mode="sequential",
        )

    # Complex: decompose
    subtasks = _decompose_complex(task)

    # Determine execution mode
    has_deps = any(st.depends_on for st in subtasks)
    if parallel and not has_deps:
        mode = "parallel"
        dep = Dependency.PARALLEL
    elif has_deps or sequential:
        mode = "sequential"
        dep = Dependency.SEQUENTIAL
    else:
        mode = "parallel"
        dep = Dependency.PARALLEL

    # Estimate cost from models used
    models_used = {st.model for st in subtasks}
    if Model.OPUS in models_used:
        cost_tier = "high"
    elif Model.SONNET in models_used:
        cost_tier = "medium"
    else:
        cost_tier = "low"

    return TaskPlan(
        original_task=task,
        size=size,
        dependency=dep,
        subtasks=subtasks,
        estimated_total_cost_tier=cost_tier,
        execution_mode=mode,
    )
