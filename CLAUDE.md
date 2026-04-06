# Claude Code Max — Master Orchestration

## Project Overview
Gold-standard Claude Code template: 5-layer architecture, 121 skills, 5-router routing system,
FastAPI REST layer, eval framework, `ccm` CLI, CI/CD, Docker — built for max autonomy.

Integrates: **gstack** (Garry Tan role personas) · **Superpowers** (obra structured methodology) ·
**Paperclip AI** (multi-agent orchestration)

**Identity Layer:** `.claude/SOUL.md` (agent identity) · `.claude/USER.md` (user profile) · `.claude/memory/hot/hot-memory.md` (DYNAMIC + STATIC zones; auto-updated at PreCompact)

**Repo:** `Wellux/wellux_testprojects`
**Branch:** `claude/optimize-cli-autonomy-xNamK`
**Shortcuts:** `f` → next step | `s` → status | `r` → research | `a` → full audit

---

## 5-Layer Architecture

| Layer | Location | Purpose |
|-------|----------|---------|
| L1 | `CLAUDE.md` + `.claude/SOUL.md` + `.claude/USER.md` | Persistent context + agent identity |
| L2 | `.claude/skills/` | 121 auto-invoked skills (keyword-triggered) |
| L3 | `.claude/hooks/` | 5 deterministic hooks (session-start, pre-compact, pre-bash, post-edit, stop) |
| L4 | `.claude/agents/` | Autonomous subagents (ralph, research, swarm, security) |
| L5 | `.claude/rules/` | Modular instruction files loaded as context |

---

## Routing System (`src/routing/`)

Auto-selects model, skill, agent, memory tier, and task plan for any task.

```python
from src.routing import route
d = route("your task description")
print(d.summary())   # ┌─ box showing all 5 routing decisions ─┐
```

| Router | File | Logic |
|--------|------|-------|
| `route_llm(task)` | `llm_router.py` | complexity 0-10 → opus / sonnet / haiku |
| `route_skill(task)` | `skill_router.py` | 70+ keyword triggers → skill + confidence |
| `route_agent(task)` | `agent_router.py` | signal match → ralph / research / swarm / security |
| `route_memory(content)` | `memory_router.py` | content type → CACHE / FILES / LESSONS / MCP / TODO |
| `plan_task(task)` | `task_router.py` | ATOMIC / MEDIUM / COMPLEX + subtask decomposition |

**Model thresholds:** opus (score 7-10) · sonnet (4-6, default) · haiku (0-3)

---

## CLI — `ccm`

Install: `pip install -e ".[dev]"` then `ccm --help`

```
ccm route "task"                     # show full routing decision (add --json)
ccm complete "prompt"                # one-shot completion (auto-routes model)
ccm complete "prompt" --model haiku  # override model
ccm serve [--host 0.0.0.0 --port 8000 --reload]   # start FastAPI
ccm status                           # git branch + test count + skills
ccm research "topic"                 # create data/research/<date>-<slug>.md stub
ccm eval list                        # list bundled eval suites
ccm eval inspect <suite.jsonl>       # show cases with constraints
ccm eval run <suite.jsonl>           # run suite (--dry-run  --tag  --threshold  --json)
```

---

## REST API (`src/api/`)

Start: `ccm serve` or `docker compose up`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Status + available models |
| `/v1/complete` | POST | Single-turn completion (auto-routes model) |
| `/v1/complete/stream` | POST | SSE streaming tokens |
| `/v1/chat` | POST | Multi-turn conversation |
| `/v1/route` | POST | Routing decision only (no LLM call) |

Every response includes `X-Request-ID` (correlation) and `X-Process-Time-Ms` (timing).

---

## Eval Framework (`src/evals/`)

```python
from src.evals import EvalCase, EvalSuite, EvalRunner, AsyncEvalRunner

suite = (EvalSuite("smoke")
    .add(EvalCase("greet", "Say hello", contains=["hello"]))
    .add(EvalCase("math",  "2+2=?",    contains=["4"]))
)
report = EvalRunner(my_llm).run(suite)
print(report.summary())   # pass rate + mean score + latency
```

---

## Persistence (`src/persistence/`)

```python
from src.persistence import FileStore, MemoryStore, TieredMemory

# File-based storage
fs = FileStore()
fs.write_research("LightRAG", content)   # → data/research/YYYY-MM-DD-lightrag.md
fs.append_lesson("title", ...)           # → tasks/lessons.md
fs.append_task("description")            # → tasks/todo.md

# MCP-backed entity memory
mem = MemoryStore()
mem.remember("fact", entity_name="infra")
results = mem.recall("PostgreSQL")

# Tiered memory (hot/warm/glacier)
tm = TieredMemory()
tm.write_hot("active_feature", "tiered-memory")      # hot: always-loaded (≤50 lines)
tm.write_warm("architecture", "# Architecture\n...")  # warm: domain contextual files
tm.archive_glacier("decision-slug", "content",        # glacier: YAML frontmatter archive
                   tags=["architecture"])
results = tm.search_glacier("PostgreSQL")              # full-text + tag search
```

---

## Ecosystem Skills

### gstack Roles (Garry Tan)
| Skill | Persona | Use When |
|-------|---------|----------|
| `/office-hours` | CEO+CTO+PM+Designer | Before starting a significant feature |
| `/ship` | Release Engineer | Ready to cut a release |
| `/careful` | Risk-averse Senior Eng | Making risky/irreversible changes |
| `/plan-eng-review` | Staff Engineer | Technical approach review before coding |

### Superpowers Methodology (obra)
| Skill | Phase | Use When |
|-------|-------|----------|
| `/brainstorm` | Requirements | Requirements are ambiguous |
| `/write-plan` | Planning | Have requirements, need atomic tasks |
| `/superpowers` | Execution | Implementing non-trivial features |

**Standard workflow:**
```
/brainstorm <feature>  →  /write-plan  →  /superpowers execute
```

### Paperclip Orchestration
| Skill | Use When |
|-------|----------|
| `/paperclip` | Multi-agent task with budget/audit requirements |
| `/swarm` | Large task that can be parallelized (adversarial validation built-in) |

### v0.9.0 New Skills
| Skill | Use When |
|-------|----------|
| `/preflight` | Validate task clarity before expensive execution (12-category scorecard) |
| `/tdd` | Enforce TDD via subagent information isolation (TestWriter/Implementer/Refactorer) |
| `/self-reflect` | Mine commits + sessions for patterns → auto-update lessons.md |
| `/chain-of-draft` | Iterative refinement: skeleton → expand → critique → final (CoD pattern) |
| `/foresight` | Cross-domain strategic analysis + one contextual nudge |
| `/team` | Preset multi-agent teams: code-review, security, debug, architect, ship, research |
| `/context-diff` | Structured change summary between git refs or sessions |

---

## Rules Layer (`.claude/rules/`)

- `code-style.md` — formatting, naming, types, error handling
- `testing.md` — structure, coverage, mocking, CI gates
- `api-conventions.md` — endpoints, headers, streaming, middleware order

---

## Commands (`.claude/commands/`)

| Command | What it does |
|---------|-------------|
| `/deploy` | Pre-deploy checklist → Docker build → health check |
| `/audit` | Full security audit (CISO orchestration) |
| `/research` | Karpathy-style deep research on a topic |
| `/review` | Thorough code review: correctness, style, tests, security |
| `/fix-issue` | Take a GitHub issue or bug description → apply fix → verify |

---

## CI / CD

**GitHub Actions** (`.github/workflows/ci.yml`):
1. `test` — ruff lint + pytest on Python 3.11 & 3.12 + coverage upload
2. `smoke-evals` — `ccm eval run smoke.jsonl --dry-run` (no API key needed)
3. `lint-dockerfile` — hadolint on Dockerfile

**Docker**: `docker compose up` → FastAPI on port 8000 with `/health` check.

---

## Task Management
1. `tasks/todo.md` — checkable task list; `f` executes next `- [ ]` item
2. `tasks/lessons.md` — self-improvement log; 30 lessons; update after every correction
3. `tasks/open-findings.md` — P2/P3 backlog from audits; shown at session start when unchecked items exist
4. `MASTER_PLAN.md` — loopable 31-step bootstrap plan (100% complete)

## Workflow
1. `claude` in project root
2. Shift+Tab+Tab → Plan mode for non-trivial tasks
3. `f` → execute next step | `s` → check status | `a` → audit | `r` → research
4. `/compact` between unrelated tasks
5. Esc+Esc → rewind if something goes sideways

## MCP Servers (`.mcp.json`)
`github` · `filesystem` · `brave-search` · `sentry` · `memory` · `sequential-thinking`

## Hooks (`.claude/hooks/` + `.claude/settings.json`)

| Hook | File | Trigger | Purpose |
|------|------|---------|---------|
| `SessionStart` | `session-start.sh` | Every session start | Boot display: version, 5 commits, last session log, full hot-memory dynamic zone, last 3 lessons, open findings |
| `PreCompact` | `pre-compact.sh` | Before context compaction | Dynamic snapshot (version/tests/skills/commits/lessons) into hot-memory DYNAMIC zone; preserves STATIC zone |
| `PreToolUse[Bash]` | `pre-tool-bash.sh` | Every bash call | Block destructive commands (rm -rf /, curl\|bash) |
| `PostToolUse[Edit/Write]` | `post-tool-edit.sh` | After file edits | Lint gate, validation |
| `Stop` | `stop.sh` | Session end | Validators + checklist + daily session log to `data/sessions/` |

## Optimizer Crons (systemd user timers)
```
daily  07:00  github-trending-research.sh  → GitHub trending → research stubs
daily  06:00  optimize-docs.sh             → doc freshness + frontmatter check
Mon    06:00  research-agent.sh            → Karpathy research loop (8 topics)
Sun    00:00  security-scan.sh             → secrets + permissions + patterns
Sun    01:00  perf-audit.sh                → import times + code metrics
Mon    08:00  self-improve.sh              → lessons → improvement tasks
```

## Core Principles
- **Route first**: let the routing system pick the model/skill/agent
- **Brainstorm first**: `/brainstorm` → `/write-plan` → `/superpowers execute` for complex features
- **Verify before done**: run tests + `ccm eval run smoke.jsonl --dry-run`
- **Lint gate**: `ruff check src/ tests/ --select E,F,W --ignore E501` must be clean
- **Self-improve**: after any correction → add lesson to `tasks/lessons.md`
- **Minimal impact**: touch only what the task requires
