# src/routing — Routing System Context

## Purpose
5-router system that auto-selects model, skill, agent, memory tier, and task plan for any input.

## Files
- `llm_router.py` — complexity 0-10 → opus/sonnet/haiku (thresholds: opus≥7, haiku≤3)
- `skill_router.py` — 123-entry `_SKILL_REGISTRY`, exact-substring trigger matching
- `agent_router.py` — signal match → ralph/research/swarm/security
- `memory_router.py` — content type → CACHE/FILES/LESSONS/MCP/TODO
- `task_router.py` — ATOMIC/MEDIUM/COMPLEX + subtask decomposition
- `__init__.py` — `route(task)` facade → `RoutingDecision` dataclass

## Key Invariant
`_SKILL_REGISTRY` must have **zero duplicate trigger phrases**.
Enforced by `tests/test_routing.py::TestSkillRegistry::test_no_duplicate_trigger_phrases`.

## Adding a skill to routing
1. Add entry to `_SKILL_REGISTRY` in `skill_router.py`
2. Update registry count in `test_registry_has_N_entries`
3. Verify: `python3 -c "from src.routing.skill_router import _SKILL_REGISTRY; print(len(_SKILL_REGISTRY))"`
