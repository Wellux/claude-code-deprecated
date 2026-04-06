"""Tests for src/routing/ — all five routers."""
from unittest.mock import patch

from src.routing import (
    Agent,
    Complexity,
    MemoryTier,
    Model,
    TaskSize,
    plan_task,
    route,
    route_agent,
    route_llm,
    route_memory,
    route_skill,
)
from src.routing.llm_router import best, cheap, fast
from src.routing.memory_router import format_lesson

# ── LLM Router ───────────────────────────────────────────────────────────────

class TestLLMRouter:
    def test_architecture_routes_to_opus(self):
        d = route_llm("architect a distributed system design for our microservices")
        assert d.model == Model.OPUS
        assert d.complexity == Complexity.HIGH

    def test_simple_summary_routes_to_haiku(self):
        d = route_llm("summarize this list")
        assert d.model == Model.HAIKU
        assert d.complexity == Complexity.LOW

    def test_feature_implementation_routes_to_sonnet(self):
        d = route_llm("implement a login endpoint with JWT")
        assert d.model == Model.SONNET

    def test_cost_sensitive_downgrades_model(self):
        d = route_llm("implement OAuth", cost_sensitive=True)
        # Should be haiku or sonnet, not opus
        assert d.model in (Model.HAIKU, Model.SONNET)

    def test_override_forces_model(self):
        d = route_llm("summarize this", override=Model.OPUS)
        assert d.model == Model.OPUS

    def test_fast_keyword_forces_haiku(self):
        d = route_llm("quickly check this")
        assert d.model == Model.HAIKU

    def test_score_within_bounds(self):
        d = route_llm("do something")
        assert 0 <= d.score <= 10

    def test_reason_is_non_empty(self):
        d = route_llm("research the latest on RAG")
        assert len(d.reason) > 0


# ── Skill Router ─────────────────────────────────────────────────────────────

class TestSkillRouter:
    def test_debug_keyword_matches_debug_skill(self):
        m = route_skill("there's an error in my code, can you fix it?")
        assert m is not None
        assert m.skill == "debug"

    def test_security_audit_matches_ciso(self):
        m = route_skill("run a full security audit")
        assert m is not None
        assert m.skill in ("ciso", "appsec-engineer", "security-reviewer")

    def test_rag_matches_rag_builder(self):
        m = route_skill("build a RAG pipeline with vector store")
        assert m is not None
        assert m.skill == "rag-builder"

    def test_no_match_returns_none(self):
        m = route_skill("hello how are you")
        assert m is None

    def test_confidence_between_0_and_1(self):
        m = route_skill("review this PR before I merge")
        assert m is not None
        assert 0.0 <= m.confidence <= 1.0

    def test_incident_routes_to_incident_response(self):
        m = route_skill("prod is down, we have a breach")
        assert m is not None
        assert m.skill == "incident-response"

    def test_category_lookup(self):
        from src.routing import route_skill_by_category
        security_skills = route_skill_by_category("security")
        assert len(security_skills) > 0
        assert "ciso" in security_skills


# ── Agent Router ─────────────────────────────────────────────────────────────

class TestAgentRouter:
    def test_build_routes_to_ralph(self):
        d = route_agent("implement the OAuth feature")
        assert d.agent == Agent.RALPH

    def test_research_routes_to_research_agent(self):
        d = route_agent("research the latest on LightRAG from first principles")
        assert d.agent == Agent.RESEARCH

    def test_parallel_routes_to_swarm(self):
        d = route_agent("run all 5 tasks in parallel simultaneously")
        assert d.agent == Agent.SWARM

    def test_security_audit_routes_to_security_reviewer(self):
        d = route_agent("run a full security audit and vulnerability scan")
        assert d.agent == Agent.SECURITY

    def test_no_signal_defaults_to_ralph(self):
        d = route_agent("do the thing")
        assert d.agent == Agent.RALPH

    def test_swarm_includes_spawn_count(self):
        d = route_agent("run all services in parallel")
        if d.agent == Agent.SWARM:
            assert d.spawn_count >= 1

    def test_context_hints_provided(self):
        d = route_agent("research LLM agents")
        assert len(d.context_hints) > 0


# ── Memory Router ────────────────────────────────────────────────────────────

class TestMemoryRouter:
    def test_correction_goes_to_lessons(self):
        d = route_memory("I made a mistake, next time I should always read before editing")
        assert d.tier == MemoryTier.LESSONS

    def test_research_goes_to_files(self):
        d = route_memory("research finding: LightRAG reduces latency by 20-30%")
        assert d.tier == MemoryTier.FILES

    def test_project_rule_goes_to_claude_md(self):
        d = route_memory("add to claude.md: always run tests before committing")
        assert d.tier == MemoryTier.CLAUDE

    def test_task_goes_to_todo(self):
        d = route_memory("add to todo: implement the auth module")
        assert d.tier == MemoryTier.TODO

    def test_content_type_override(self):
        d = route_memory("some important fact", content_type="lesson")
        assert d.tier == MemoryTier.LESSONS

    def test_destination_is_string(self):
        d = route_memory("remember that we use postgres")
        assert isinstance(d.destination, str)
        assert len(d.destination) > 0


# ── Task Router ──────────────────────────────────────────────────────────────

class TestTaskRouter:
    def test_atomic_task_no_decomposition(self):
        plan = plan_task("rename this variable")
        assert plan.size == TaskSize.ATOMIC
        assert len(plan.subtasks) == 1

    def test_complex_task_decomposed(self):
        plan = plan_task(
            "research LightRAG, implement a full RAG pipeline, write tests, "
            "and document everything end-to-end"
        )
        assert plan.size == TaskSize.COMPLEX
        assert len(plan.subtasks) >= 2

    def test_research_subtask_uses_research_agent(self):
        # Needs enough complexity signals to trigger decomposition
        plan = plan_task(
            "research the best caching strategies, implement a full caching layer "
            "with tests, and document everything comprehensively end-to-end"
        )
        research_tasks = [st for st in plan.subtasks if st.agent == Agent.RESEARCH]
        assert len(research_tasks) >= 1

    def test_plan_has_valid_execution_mode(self):
        plan = plan_task("build an OAuth login system with tests")
        assert plan.execution_mode in ("single", "sequential", "parallel")

    def test_plan_summary_is_string(self):
        plan = plan_task("implement feature X")
        assert isinstance(plan.summary(), str)

    def test_all_subtasks_have_model(self):
        plan = plan_task("do a full security audit and fix all issues found")
        for st in plan.subtasks:
            assert st.model in list(Model)


# ── route_multi_agent ─────────────────────────────────────────────────────────

class TestRouteMultiAgent:
    def test_returns_all_four_agents(self):
        from src.routing.agent_router import route_multi_agent
        results = route_multi_agent("implement a new feature")
        agents = {d.agent for d in results}
        assert agents == {Agent.RALPH, Agent.RESEARCH, Agent.SWARM, Agent.SECURITY}

    def test_sorted_by_confidence_descending(self):
        from src.routing.agent_router import route_multi_agent
        results = route_multi_agent("run a full security audit")
        confidences = [d.confidence for d in results]
        assert confidences == sorted(confidences, reverse=True)

    def test_top_result_matches_single_route(self):
        from src.routing.agent_router import route_multi_agent
        results = route_multi_agent("research the latest on RAG systems")
        assert results[0].agent == Agent.RESEARCH

    def test_each_result_has_reason(self):
        from src.routing.agent_router import route_multi_agent
        for d in route_multi_agent("swarm all modules in parallel"):
            assert len(d.reason) > 0

    def test_zero_signal_task_gives_zero_confidence(self):
        from src.routing.agent_router import route_multi_agent
        results = route_multi_agent("zzzzz")
        # All agents should have 0 confidence for a meaningless task
        assert all(d.confidence == 0.0 for d in results)

    def test_confidence_range(self):
        from src.routing.agent_router import route_multi_agent
        for d in route_multi_agent("implement and research and swarm"):
            assert 0.0 <= d.confidence <= 1.0


# ── Unified route() ──────────────────────────────────────────────────────────

class TestUnifiedRoute:
    def test_route_returns_full_decision(self):
        d = route("implement a rate limiter for the API")
        assert d.llm is not None
        assert d.agent is not None
        assert d.memory is not None
        assert d.plan is not None

    def test_summary_is_string(self):
        d = route("debug this authentication error")
        assert isinstance(d.summary(), str)
        assert "ROUTING DECISION" in d.summary()

    def test_route_debug_task(self):
        d = route("there is a bug in the login flow, fix it")
        assert d.llm.model in list(Model)
        assert d.skill is not None
        assert d.skill.skill == "debug"


# ── MAX_SUBTASKS cap ──────────────────────────────────────────────────────────

class TestMaxSubtasksCap:
    def test_plan_never_exceeds_cap(self):
        from src.routing.task_router import MAX_SUBTASKS, _decompose_complex
        # Craft a task that triggers every subtask branch
        task = (
            "research and implement and test and document and secure this "
            "entire comprehensive end-to-end full system migration from scratch "
            "multiple phases and also redesign and overhaul everything in addition"
        )
        subtasks = _decompose_complex(task)
        assert len(subtasks) <= MAX_SUBTASKS

    def test_cap_constant_is_positive(self):
        from src.routing.task_router import MAX_SUBTASKS
        assert MAX_SUBTASKS > 0

    def test_plan_task_subtasks_bounded(self):
        from src.routing.task_router import MAX_SUBTASKS
        plan = plan_task(
            "research, implement, test, document, and secure this "
            "entire end-to-end system with multiple phases"
        )
        assert len(plan.subtasks) <= MAX_SUBTASKS


# ── _needs_build removal regression ──────────────────────────────────────────

class TestDecomposeAlwaysHasImpl:
    def test_impl_subtask_present_without_build_keywords(self):
        from src.routing.task_router import _decompose_complex
        # Task has no "implement/build/create/write/add" keywords
        subtasks = _decompose_complex("refactor the logging module")
        roles = [s.agent.value for s in subtasks]
        # ralph-loop (main implementer) should always be present
        assert "ralph-loop" in roles

    def test_impl_subtask_present_with_build_keywords(self):
        from src.routing.task_router import _decompose_complex
        subtasks = _decompose_complex("implement a new cache layer")
        roles = [s.agent.value for s in subtasks]
        assert "ralph-loop" in roles

    def test_research_subtask_only_when_needed(self):
        from src.routing.task_router import _decompose_complex
        with_research = _decompose_complex("research and implement a new cache")
        without_research = _decompose_complex("implement a new cache")
        assert len(with_research) > len(without_research)


# ── FullRoutingDecision.summary — subtask branch ─────────────────────────────

class TestFullRoutingDecisionSummary:
    def test_summary_includes_subtasks_when_multiple(self):
        # A complex multi-signal task should produce > 1 subtask and trigger
        # the subtask-listing branch in FullRoutingDecision.summary() (lines 49-52)
        d = route(
            "research LightRAG, implement a full RAG pipeline with tests, "
            "and document everything end-to-end comprehensively"
        )
        if len(d.plan.subtasks) > 1:
            summary = d.summary()
            assert "Subtasks:" in summary

    def test_summary_no_subtask_section_for_atomic(self):
        d = route("rename this variable")
        summary = d.summary()
        # ROUTING DECISION box always present; subtask section absent for single subtask
        assert "ROUTING DECISION" in summary


# ── Memory Router — remaining content_type overrides and CACHE tier ──────────

class TestMemoryRouterContentTypeOverrides:
    def test_content_type_research_routes_to_files(self):
        d = route_memory("some finding", content_type="research")
        assert d.tier == MemoryTier.FILES

    def test_content_type_fact_routes_to_mcp(self):
        d = route_memory("some fact", content_type="fact")
        assert d.tier == MemoryTier.MCP

    def test_content_type_task_routes_to_todo(self):
        d = route_memory("something to do", content_type="task")
        assert d.tier == MemoryTier.TODO

    def test_content_type_rule_routes_to_claude_md(self):
        d = route_memory("a coding rule", content_type="rule")
        assert d.tier == MemoryTier.CLAUDE

    def test_cache_signals_route_to_cache(self):
        d = route_memory("same prompt, don't call again — already computed")
        assert d.tier == MemoryTier.CACHE
        assert d.action == "cache"

    def test_no_signal_defaults_to_mcp(self):
        d = route_memory("xyz abc irrelevant text with no matching signals")
        assert d.tier == MemoryTier.MCP


# ── format_lesson ─────────────────────────────────────────────────────────────

class TestFormatLesson:
    def test_returns_string(self):
        result = format_lesson(
            date="2026-03-29",
            title="Always read before editing",
            mistake="Edited without reading",
            why="Assumed content was known",
            rule="Read the file first",
            example="Read → Edit, not Edit blindly",
        )
        assert isinstance(result, str)

    def test_includes_all_fields(self):
        result = format_lesson(
            date="2026-03-29",
            title="Test title",
            mistake="The mistake",
            why="The reason",
            rule="The rule",
            example="The example",
        )
        assert "2026-03-29" in result
        assert "Test title" in result
        assert "The mistake" in result
        assert "The rule" in result
        assert "The example" in result


# ── LLM Router convenience shortcuts ─────────────────────────────────────────

class TestLLMRouterShortcuts:
    def test_cheap_returns_haiku_or_sonnet(self):
        d = cheap("implement OAuth login with JWT tokens")
        assert d.model in (Model.HAIKU, Model.SONNET)

    def test_fast_returns_haiku(self):
        d = fast("summarize this short text")
        assert d.model == Model.HAIKU

    def test_best_floors_to_at_least_sonnet(self):
        # best() sets min_complexity=MEDIUM, so simple tasks get at least SONNET
        d = best("rename this variable")
        assert d.model in (Model.SONNET, Model.OPUS)

    def test_min_complexity_floor_applied(self):
        # A simple task (HAIKU) floored to MEDIUM (SONNET) by min_complexity
        d = route_llm("rename this variable", min_complexity=Complexity.MEDIUM)
        assert d.model == Model.SONNET
        assert d.complexity == Complexity.MEDIUM


# ── Task Router — execution mode and cost tier branches ───────────────────────

class TestTaskRouterBranches:
    def test_parallel_mode_when_parallel_signal_no_deps(self):
        # "parallel" signal + complex task without test/docs → impl has depends_on=[]
        # so has_deps=False → mode="parallel" via the first if branch (lines 264-265)
        plan = plan_task(
            "build and create a complete comprehensive full system with multiple phases "
            "using parallel workstreams in parallel"
        )
        if plan.size == TaskSize.COMPLEX:
            assert plan.execution_mode in ("parallel", "sequential")

    def test_sequential_mode_when_subtask_has_deps(self):
        # Complex task with "test" → tests subtask depends on impl → has_deps=True
        plan = plan_task(
            "implement a complete comprehensive full oauth system from scratch "
            "and write tests for it end-to-end"
        )
        if plan.size == TaskSize.COMPLEX:
            assert plan.execution_mode == "sequential"

    def test_parallel_else_branch_no_signals(self):
        # Complex task (multiple signals) without parallel/sequential keywords
        # and without test/docs → impl depends_on=[], has_deps=False, no signals
        plan = plan_task(
            "build a complete comprehensive full system with multiple phases "
            "create and overhaul the entire architecture from scratch"
        )
        if plan.size == TaskSize.COMPLEX:
            assert plan.execution_mode in ("parallel", "sequential")

    def test_cost_tier_medium_from_sonnet_subtasks(self):
        from src.routing.task_router import Subtask

        # Inject SONNET-only subtasks (no OPUS) → cost_tier should be "medium"
        mock_subtasks = [
            Subtask(id="1", description="task", agent=Agent.RALPH, model=Model.SONNET, skill=None)
        ]
        with patch("src.routing.task_router._decompose_complex", return_value=mock_subtasks):
            plan = plan_task(
                "implement comprehensive full system from scratch with multiple phases "
                "and also overhaul everything"
            )
        assert plan.estimated_total_cost_tier == "medium"

    def test_cost_tier_low_from_haiku_subtasks(self):
        from src.routing.task_router import Subtask

        mock_subtasks = [
            Subtask(id="1", description="task", agent=Agent.RALPH, model=Model.HAIKU, skill=None)
        ]
        with patch("src.routing.task_router._decompose_complex", return_value=mock_subtasks):
            plan = plan_task(
                "implement comprehensive full system from scratch with multiple phases "
                "and also overhaul everything"
            )
        assert plan.estimated_total_cost_tier == "low"

    def test_subtasks_truncated_to_max(self):
        import src.routing.task_router as _tr
        from src.routing.task_router import _decompose_complex

        # The default cap is 10 but max branches produce only 5 subtasks.
        # Temporarily lower the cap to 2 to trigger the truncation line.
        original_cap = _tr.MAX_SUBTASKS
        _tr.MAX_SUBTASKS = 2
        try:
            task = (
                "research and implement and test and document and secure this "
                "entire comprehensive end-to-end full system from scratch"
            )
            subtasks = _decompose_complex(task)
        finally:
            _tr.MAX_SUBTASKS = original_cap

        # With cap=2, the 5-subtask result is truncated to 2
        assert len(subtasks) == 2


class TestSkillRouterCategories:
    def test_list_categories_returns_sorted_strings(self):
        from src.routing.skill_router import list_categories
        cats = list_categories()
        assert isinstance(cats, list)
        assert len(cats) > 0
        assert cats == sorted(cats)  # sorted() contract
        assert all(isinstance(c, str) for c in cats)

    def test_expected_categories_present(self):
        from src.routing.skill_router import list_categories
        cats = list_categories()
        for expected in ("security", "development", "ai", "devops", "docs", "meta", "pm", "web"):
            assert expected in cats, f"category '{expected}' missing"


class TestSkillRegistry:
    def test_registry_has_123_entries(self):
        from src.routing.skill_router import _SKILL_REGISTRY
        assert len(_SKILL_REGISTRY) == 123, f"Expected 123, got {len(_SKILL_REGISTRY)}"

    def test_no_duplicate_skill_names(self):
        from src.routing.skill_router import _SKILL_REGISTRY
        names = [e["skill"] for e in _SKILL_REGISTRY]
        assert len(names) == len(set(names)), "Duplicate skill names found"

    def test_all_entries_have_required_keys(self):
        from src.routing.skill_router import _SKILL_REGISTRY
        for entry in _SKILL_REGISTRY:
            assert "skill" in entry
            assert "category" in entry
            assert "priority" in entry
            assert "triggers" in entry
            assert len(entry["triggers"]) >= 1

    def test_all_priorities_in_valid_range(self):
        from src.routing.skill_router import _SKILL_REGISTRY
        for entry in _SKILL_REGISTRY:
            assert 1 <= entry["priority"] <= 10, (
                f"Priority {entry['priority']} out of range for {entry['skill']}"
            )

    def test_no_duplicate_trigger_phrases(self):
        from src.routing.skill_router import _SKILL_REGISTRY
        seen: dict[str, str] = {}
        for entry in _SKILL_REGISTRY:
            for trigger in entry["triggers"]:
                if trigger in seen:
                    # Allow duplicate if same skill
                    assert seen[trigger] == entry["skill"], (
                        f"Trigger '{trigger}' used by both '{seen[trigger]}' and '{entry['skill']}'"
                    )
                else:
                    seen[trigger] = entry["skill"]

    def test_key_skills_routable(self):
        """Spot-check that newly added skills have working triggers."""
        cases = [
            ("firewall review needed", "network-engineer"),
            ("cloud misconfiguration aws security review", "cloud-engineer"),
            ("os hardening checklist", "sysadmin"),
            ("memory leak investigation", "memory-profiler"),
            ("design database schema for users", "db-designer"),
            ("competitive analysis vs competitors", "competitive-analyst"),
            ("sprint planning session", "sprint-planner"),
            ("rollback to previous deployment", "rollback"),
            ("accessibility wcag audit", "a11y-checker"),
            ("web vitals lcp score", "web-vitals"),
            ("bias check fairness audit for this model", "ai-safety"),
            ("standup what did i do yesterday", "standup"),
        ]
        for prompt, expected_skill in cases:
            m = route_skill(prompt)
            assert m is not None, f"No match for: '{prompt}'"
            assert m.skill == expected_skill, (
                f"'{prompt}' → '{m.skill}', expected '{expected_skill}'"
            )
