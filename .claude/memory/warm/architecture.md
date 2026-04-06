# Warm Memory: Architecture
<!-- L1: system design, component responsibilities, data flow -->

**Last Updated**: 2026-04-05

## 5-Layer Stack

| Layer | Files | Purpose |
|-------|-------|---------|
| L1 | `CLAUDE.md`, `SOUL.md`, `USER.md`, `MEMORY.md` | Persistent session context + agent identity |
| L2 | `.claude/skills/` (123 skills) | Auto-invoked by keyword routing |
| L3 | `.claude/hooks/` (7 hooks) | Deterministic safety gates + lifecycle events |
| L4 | `.claude/agents/` (4 agents) | Autonomous subagents with own context windows |
| L5 | `.claude/rules/` (3 rule files) | Modular instruction sets |

## Source Layout (`src/`)

```
src/
├── api/          FastAPI layer: routes, models, middleware (CORS, rate limit, timing, correlation)
├── evals/        EvalCase, EvalSuite, EvalRunner, AsyncEvalRunner, Verdict, EvalReport
├── handlers/     Message handlers for completions
├── llm/          claude_client.py, gpt_client.py
├── persistence/  FileStore, MemoryStore (MCP-backed), TieredMemory (hot/warm/glacier)
├── prompt_engineering/  Prompt templates and optimization
├── routing/      5-router system (see below)
├── utils/        logger.py (structured JSON), log_index.py
├── cli.py        ccm CLI (argparse, 15 commands)
├── mcp_server.py MCP stdio server
└── version.py    VERSION constant
```

## Routing System (`src/routing/`)

All 5 routers are composed via `route()` in `__init__.py` → `RoutingDecision`:

| Router | Input | Output |
|--------|-------|--------|
| `llm_router.py` | task text | complexity 0-10 → opus/sonnet/haiku |
| `skill_router.py` | task text | 123-entry registry → `SkillMatch(skill, confidence, category)` |
| `agent_router.py` | task text | signal match → ralph/research/swarm/security |
| `memory_router.py` | content text | type → CACHE/FILES/LESSONS/MCP/TODO |
| `task_router.py` | task text | ATOMIC/MEDIUM/COMPLEX + subtask list |

**Key:** `skill_router.py` uses exact substring matching (trigger phrases in `_SKILL_REGISTRY`).
Duplicate triggers are enforced-absent by `test_no_duplicate_trigger_phrases`.

## REST API Endpoints

```
GET  /health          → status + available models
POST /complete        → single-turn, auto-routes model
POST /complete/stream → SSE token streaming
POST /chat            → multi-turn conversation
POST /route           → routing decision only (no LLM call)
```

All responses: `X-Request-ID` + `X-Process-Time-Ms` headers.

## Persistence Tiers

```
FileStore      → data/research/, tasks/todo.md, tasks/lessons.md, data/cache/events.log
MemoryStore    → MCP memory server (entities + relations)
TieredMemory:
  hot          → .claude/memory/hot/hot-memory.md (≤50 lines, always loaded)
  warm         → .claude/memory/warm/<domain>.md (loaded on activation)
  glacier      → .claude/memory/glacier/YYYY-MM-DD-<slug>.md (YAML frontmatter, searchable)
```

## Hooks Lifecycle

```
SessionStart    → session-start.sh   (boot display + hot-memory + daily log)
UserPromptSubmit → user-prompt-submit.sh (branch guard + prompt length check)
PreCompact      → pre-compact.sh     (snapshot before context wipe)
PreToolUse[Bash] → pre-tool-bash.sh  (block destructive commands)
PostToolUse[Edit/Write] → post-tool-edit.sh (lint gate)
PostToolUse[Bash] → post-tool-pr.sh  (post-PR simplification trigger)
Stop            → stop.sh            (validators + daily session log)
```

## Skills by Category (123 total)

- **security** (17): ciso, pen-tester, appsec-engineer, soc-analyst, incident-response, ai-security, grc-analyst, iam-engineer, secrets-mgr, network-engineer, cloud-engineer, security-engineer, devops-engineer, purple-team, dba, help-desk, sysadmin
- **development** (25): code-review, debug, refactor, architect, test-writer, api-designer, type-safety, perf-profiler, bug-hunter, tech-debt, db-optimizer, migration, async-optimizer, error-handler, algorithm, concurrency, cache-strategy, bundle-analyzer, memory-profiler, query-optimizer, db-designer, dep-auditor, pr-reviewer, feature-planner, tdd
- **ai** (13): rag-builder, prompt-engineer, llm-optimizer, fine-tuner, evals-designer, agent-orchestrator, ml-debugger, model-benchmarker, embeddings, dataset-curator, ai-safety, vision-analyst, multimodal + paper-summarizer, karpathy-researcher
- **devops** (16): ci-cd, docker, monitoring, sre, deploy-checker, k8s, terraform, backup, scaling, cost-optimizer, pipeline-opt, rollback, logging, infra-docs, metrics-designer, cron-scheduler
- **meta** (24): gsd, swarm, mem, brainstorm, write-plan, superpowers, office-hours, ship, careful, plan-eng-review, paperclip, create, preflight, tdd, self-reflect, chain-of-draft, foresight, team, context-diff, riper, memory-bank + trend-researcher, data-pipeline, knowledge-base, obsidian, ui-ux
- **pm** (11): sprint-planner, standup, retrospective, roadmap, risk-assessor, scope-definer, estimation, blocker-resolver, stakeholder, kpi-tracker, competitive-analyst
- **docs** (11): readme-writer, adr-writer, runbook-creator, changelog, api-docs, changelog-maintainer, arch-diagrammer, onboarding, tutorial-writer, decision-logger, infra-docs
- **web** (4): web-vitals, seo-auditor, a11y-checker, web-scraper
