"""Routing package — unified entry point for all routing decisions.

Quick reference:
    from src.routing import route

    decision = route("research LightRAG and implement a RAG pipeline")
    print(decision.summary())

Individual routers:
    from src.routing import route_llm, route_skill, route_agent, route_memory, plan_task
"""
from dataclasses import dataclass

from .agent_router import Agent, AgentDecision, route_agent, route_multi_agent
from .llm_router import Complexity, Model, best, cheap, fast, route_llm
from .llm_router import RoutingDecision as LLMDecision
from .memory_router import MemoryDecision, MemoryTier, format_lesson, route_memory
from .skill_router import SkillMatch, list_categories, route_skill, route_skill_by_category
from .task_router import Dependency, TaskPlan, TaskSize, plan_task


@dataclass
class FullRoutingDecision:
    """Combined routing decision across all five routers."""
    task: str
    llm: LLMDecision
    skill: SkillMatch | None
    agent: AgentDecision
    memory: MemoryDecision
    plan: TaskPlan

    def summary(self) -> str:
        skill_str = f"{self.skill.skill} ({self.skill.confidence:.0%})" if self.skill else "none"
        lines = [
            "╔══════════════════════════════════════════════════════╗",
            "║  ROUTING DECISION                                    ║",
            "╠══════════════════════════════════════════════════════╣",
            f"║  Task    : {self.task[:50]:<50} ║",
            f"║  Model   : {self.llm.model.value:<50} ║",
            f"║  Reason  : {self.llm.reason[:50]:<50} ║",
            f"║  Skill   : {skill_str:<50} ║",
            f"║  Agent   : {self.agent.agent.value:<50} ║",
            f"║  Memory  : {self.memory.tier.value} → {str(self.memory.destination)[-40:]:<40} ║",
            f"║  Plan    : {self.plan.size.value} / {self.plan.execution_mode:<44} ║",
            f"║  Cost    : {self.plan.estimated_total_cost_tier:<50} ║",
            "╚══════════════════════════════════════════════════════╝",
        ]
        if len(self.plan.subtasks) > 1:
            lines.append("\nSubtasks:")
            for st in self.plan.subtasks:
                dep = f" → needs {st.depends_on}" if st.depends_on else ""
                lines.append(f"  {st.id}. [{st.agent.value}/{st.model.value.split('-')[1]}] {st.description[:55]}{dep}")
        return "\n".join(lines)


def route(task: str, *, content_type: str | None = None) -> FullRoutingDecision:
    """Single entry point: run all 5 routers and return a unified decision.

    Usage:
        decision = route("implement OAuth2 login with JWT tokens")
        print(decision.summary())

        # Use individual fields
        response = await client.complete(
            CompletionRequest(prompt=task, model=decision.llm.model.value)
        )
    """
    return FullRoutingDecision(
        task=task,
        llm=route_llm(task),
        skill=route_skill(task),
        agent=route_agent(task),
        memory=route_memory(task, content_type=content_type),
        plan=plan_task(task),
    )


__all__ = [
    # Unified
    "route", "FullRoutingDecision",
    # LLM
    "route_llm", "cheap", "fast", "best", "Model", "Complexity", "LLMDecision",
    # Skill
    "route_skill", "route_skill_by_category", "list_categories", "SkillMatch",
    # Agent
    "route_agent", "route_multi_agent", "Agent", "AgentDecision",
    # Memory
    "route_memory", "format_lesson", "MemoryTier", "MemoryDecision",
    # Task
    "plan_task", "TaskPlan", "TaskSize", "Dependency",
]
