```
 ██████╗ ██╗      █████╗ ██╗   ██╗██████╗ ███████╗
██╔════╝ ██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
██║      ██║     ███████║██║   ██║██║  ██║█████╗
██║      ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
╚██████╗ ███████╗██║  ██║╚██████╔╝██████╔╝███████╗
 ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
         CODE MAX  —  Build Anything
```

> **A gold-standard Claude Code harness: 5-layer architecture · 123 skills · 5-router auto-routing ·
> FastAPI REST · eval framework · gstack roles · Superpowers methodology · Paperclip orchestration ·
> tiered memory (hot/warm/glacier) · self-improving via lessons · CI/CD · Docker**

---

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-661%20passing-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen.svg)](#testing)
[![Ruff](https://img.shields.io/badge/lint-ruff%20clean-blue.svg)](#code-style)
[![Skills](https://img.shields.io/badge/skills-123-purple.svg)](#skills)
[![Version](https://img.shields.io/badge/version-1.0.7-orange.svg)](#changelog)

---

## What This Is

Claude Code Max turns Claude Code CLI into a **virtual software factory**. Instead of prompting
generically, it gives Claude structured roles, methodology, routing intelligence, safety gates,
and a self-improvement loop — so you ship production-grade software at machine speed.

**Inspired by:**
- [gstack](https://github.com/garrytan/gstack) by Garry Tan — role-based engineering team personas
- [obra/superpowers](https://github.com/obra/superpowers) — structured methodology enforcement
- [Paperclip AI](https://paperclip.ing) — multi-agent orchestration with budgets and audit trails

---

## Quick Start

```bash
# Clone and enter
git clone <repo> && cd wellux_testprojects

# Install Python deps
pip install -e ".[dev]"

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Launch Claude Code
claude

# In session:
f    # → execute next MASTER_PLAN step
s    # → status (git + tasks + health)
r    # → Karpathy research on latest AI
a    # → full security + perf audit
```

---

## 5-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DEVELOPER                               │
└────────────────────────────┬────────────────────────────────────┘
                             │  claude / "f" / /skill-name
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L1 ── CLAUDE.md                      Persistent context        │
│        Loaded every session. Routing ref, CLI, API, principles. │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L2 ── .claude/skills/  (123 skills)  Auto-invoked on keyword   │
│        Security · Dev · AI/ML · DevOps · Docs · PM · Ecosystem  │
│        + gstack roles · Superpowers · v0.9 skills               │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L3 ── .claude/hooks/  (7 hooks)      Deterministic safety      │
│   session-start · pre-compact · user-prompt · pre-bash          │
│   post-edit · post-pr · stop                                    │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L4 ── .claude/agents/  (4 agents)    Autonomous subagents      │
│        ralph-loop · research · swarm · security-reviewer        │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L5 ── .claude/rules/  (3 rule files) Modular instructions      │
│        code-style · testing · api-conventions                   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  src/routing/             5-Router Auto-Selection               │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐  │
│  │LLM router│ │ Skill   │ │  Agent   │ │  Memory  │ │ Task │  │
│  │opus/     │ │ router  │ │  router  │ │  router  │ │router│  │
│  │sonnet/   │ │ 70+ kw  │ │ 4 agents │ │ 5 tiers  │ │3 cmx │  │
│  │haiku     │ │triggers │ │          │ │          │ │      │  │
│  └──────────┘ └─────────┘ └──────────┘ └──────────┘ └──────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ecosystem Integration

### gstack — Engineering Team Personas (Garry Tan)

Run skills as specific engineering roles. Each persona has distinct priorities and constraints:

| Skill | Persona | Trigger |
|-------|---------|---------|
| `/office-hours` | CEO + CTO + PM + Designer debate | "review approach", "office hours", "should we build this" |
| `/ship` | Release Engineer | "ship it", "deploy", "cut release", "land this" |
| `/careful` | Risk-averse Senior Eng | "be careful", "risky change", "low risk mode" |
| `/plan-eng-review` | Staff Engineer review | "eng review", "technical review before starting" |

### Superpowers — Structured Methodology (Jesse Vincent / obra)

Enforce rigorous software engineering discipline before a single line of code:

| Skill | Phase | What It Does |
|-------|-------|--------------|
| `/brainstorm` | Requirements | Socratic refinement — surfaces assumptions, edge cases, tradeoffs |
| `/write-plan` | Planning | Breaks work into 2-5 min atomic chunks with explicit acceptance criteria |
| `/superpowers` | Execution | High-agency mode — senior engineer discipline, tests + docs in one pass |

**Workflow:**
```bash
/brainstorm build a rate limiter for the API
# → 10 clarifying questions answered
/write-plan implement the rate limiter per the brainstorm
# → atomic subtasks with specs
/superpowers execute the plan
# → implementation + tests + docs, reviewed before presenting
```

### Paperclip — Multi-Agent Orchestration

Structure complex projects as an agent org chart with budgets and audit trails:

| Skill | Purpose |
|-------|---------|
| `/paperclip` | Assign tasks to named agents with spend budgets, heartbeat, audit log |
| `/swarm` | Parallel decomposition into independent agent workstreams |
| `/agent-orchestrator` | Design multi-agent coordination patterns |

---

## Routing System

Auto-selects the right model, skill, agent, memory tier, and task plan for any task:

```python
from src.routing import route

d = route("implement a JWT auth middleware with tests")
print(d.summary())
# ┌─────────────────────────────────────────────────┐
# │ LLM     : sonnet  (complexity 6/10)             │
# │ Skill   : /test-writer  (confidence 0.82)       │
# │ Agent   : ralph-loop                            │
# │ Memory  : FILES                                 │
# │ Plan    : COMPLEX → 4 subtasks                  │
# └─────────────────────────────────────────────────┘
```

```
ccm route "your task"         # show routing decision
ccm route "your task" --json  # machine-readable output
```

**Thresholds:** opus (7-10) · sonnet (4-6, default) · haiku (0-3)

---

## Skills (123 total)

Run any skill with `/skill-name` or let keyword matching auto-invoke it.

### Ecosystem (8)
| Skill | Purpose |
|-------|---------|
| `/superpowers` | High-agency senior engineer mode |
| `/brainstorm` | Socratic requirements refinement (Superpowers) |
| `/write-plan` | Atomic task decomposition with acceptance criteria |
| `/office-hours` | Strategic review: CEO/CTO/PM/Designer personas |
| `/ship` | Full release: test → lint → security → build → deploy → monitor |
| `/careful` | Low-risk mode: extra confirmation, no destructive ops |
| `/paperclip` | Multi-agent orchestration with budgets and audit trails |
| `/gsd` | Get Shit Done — focused shipping mode, no interruptions |
| `/mem` | Persist decisions and facts across sessions via MCP |
| `/obsidian` | Second brain knowledge management |
| `/swarm` | Parallel agent workstream decomposition |
| `/create` | Generate new skills from scratch |

### v0.9 New Skills (9)
| Skill | Purpose |
|-------|---------|
| `/preflight` | 12-category task clarity scorecard before expensive execution |
| `/tdd` | TDD via subagent isolation: TestWriter → Implementer → Refactorer |
| `/self-reflect` | Mine commits + sessions for patterns → auto-update lessons.md |
| `/chain-of-draft` | Skeleton → expand → critique → final (CoD, ~20% of CoT tokens) |
| `/foresight` | Cross-domain strategic analysis + one contextual nudge |
| `/team` | Preset multi-agent teams: code-review, security, debug, architect, ship, research |
| `/context-diff` | Structured change summary between git refs or sessions |
| `/riper` | 5-phase gate: Research→Innovate→Plan→Execute→Review with explicit approvals |
| `/memory-bank` | Warm-tier memory sync: status, query, domain management |

### Security (16)
| Skill | Role |
|-------|------|
| `/ciso` | Orchestrator — runs full color team sweep |
| `/pen-tester` | Red team: offensive, adversary emulation |
| `/soc-analyst` | Blue team: monitoring, threat detection, triage |
| `/appsec-engineer` | OWASP Top 10, secure SDLC, code review |
| `/ai-security` | Prompt injection, LLM/agent attack surfaces |
| `/iam-engineer` | SSO, MFA, RBAC, access reviews |
| `/grc-analyst` | Governance, risk, compliance, audit |
| `/incident-response` | Containment, forensics, recovery playbook |
| `/security-engineer` | SIEM rules, WAF, detection engineering |
| `/purple-team` | Red-to-blue bridge, validates detections |
| `/cloud-engineer` | Cloud infra security + hardening |
| `/dba` | Database security, encryption, access control |
| `/network-engineer` | Firewall rules, VPN, zero-trust |
| `/secrets-mgr` | Secrets management, rotation, vault |
| `/sysadmin` | OS hardening, patch management, backup |
| `/help-desk` | Support gatekeeper, access provisioning |

### Development (20)
`/code-review` `/refactor` `/debug` `/architect` `/test-writer` `/api-designer`
`/db-optimizer` `/perf-profiler` `/tech-debt` `/pr-reviewer` `/dep-auditor`
`/migration` `/feature-planner` `/bug-hunter` `/type-safety` `/async-optimizer`
`/cache-strategy` `/error-handler` `/changelog` `/concurrency`

### AI / ML Research (15)
`/karpathy-researcher` `/paper-summarizer` `/prompt-engineer` `/rag-builder`
`/agent-orchestrator` `/evals-designer` `/model-benchmarker` `/fine-tuner`
`/embeddings` `/dataset-curator` `/ml-debugger` `/llm-optimizer`
`/vision-analyst` `/multimodal` `/ai-safety`

### DevOps / Infrastructure (15)
`/ci-cd` `/docker` `/k8s` `/terraform` `/monitoring` `/logging` `/backup`
`/cost-optimizer` `/scaling` `/pipeline-opt` `/deploy-checker` `/rollback`
`/infra-docs` `/sre` `/devops-engineer`

### Documentation (10)
`/readme-writer` `/adr-writer` `/runbook-creator` `/api-docs`
`/changelog-maintainer` `/onboarding` `/arch-diagrammer`
`/decision-logger` `/tutorial-writer` `/knowledge-base`

### Optimization / Research (15)
`/web-vitals` `/seo-auditor` `/a11y-checker` `/bundle-analyzer` `/query-optimizer`
`/memory-profiler` `/algorithm` `/data-pipeline` `/cron-scheduler` `/web-scraper`
`/trend-researcher` `/competitive-analyst` `/kpi-tracker` `/metrics-designer`
`/perf-profiler`

### Project Management (9)
`/sprint-planner` `/standup` `/retrospective` `/roadmap` `/risk-assessor`
`/scope-definer` `/estimation` `/blocker-resolver` `/stakeholder`

---

## CLI — `ccm`

```bash
pip install -e ".[dev]"   # one-time setup
ccm --help
```

```
ccm route "task"                       # full routing decision  (--json)
ccm complete "prompt"                  # one-shot completion (auto-routes model)
ccm complete "prompt" --model opus     # override model
ccm serve [--host 0.0.0.0 --port 8000] # start FastAPI
ccm status                             # git branch + test count + skills
ccm research "topic"                   # create data/research/<date>-<slug>.md stub
ccm eval list                          # list bundled eval suites
ccm eval inspect <suite.jsonl>         # show cases + constraints
ccm eval run <suite.jsonl>             # run suite  (--dry-run --tag --threshold --json)
ccm context-diff [--since <ref>]       # structured change summary since git ref or yesterday
ccm memory-bank status                 # show hot lines + warm domains + glacier count
ccm memory-bank query <term>           # cross-tier search (warm domains + glacier)
ccm memory-bank sync                   # update hot-memory timestamp
```

---

## REST API

```bash
ccm serve           # → http://localhost:8000
docker compose up   # → same, containerized
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Status + available models |
| `/v1/complete` | POST | Single-turn completion (auto-routes model) |
| `/v1/complete/stream` | POST | SSE streaming: `data: <token>\n\n` … `data: [DONE]\n\n` |
| `/v1/chat` | POST | Multi-turn conversation with history |
| `/v1/route` | POST | Routing decision only — no LLM call |

Every response includes `X-Request-ID` (correlation) and `X-Process-Time-Ms` (latency).

```python
import httpx

r = httpx.post("http://localhost:8000/v1/complete", json={
    "prompt": "Explain RAG in 3 sentences",
    "auto_route": True
})
print(r.json()["content"])     # answer
print(r.json()["model"])       # routed model
print(r.json()["cost_usd"])    # cost
```

---

## Eval Framework

```python
from src.evals import EvalCase, EvalSuite, EvalRunner, AsyncEvalRunner

suite = (EvalSuite("smoke")
    .add(EvalCase("greet", "Say hello",     contains=["hello"]))
    .add(EvalCase("math",  "What is 2+2?",  contains=["4"]))
    .add(EvalCase("code",  "Write FizzBuzz in Python", contains=["fizz"]))
)

# Sync
report = EvalRunner(my_llm).run(suite)

# Async (concurrent)
report = await AsyncEvalRunner(my_async_llm, concurrency=5).run(suite)

print(report.summary())
# pass_rate=1.00 mean_score=1.00 mean_latency_ms=312.4
```

**Bundled suites** in `data/evals/`:

| Suite | Cases | Notes |
|-------|-------|-------|
| `smoke.jsonl` | 5 | Echo-safe, passes without API key (`--dry-run`) |
| `routing.jsonl` | 5 | Model-routing expectation cases |
| `prompting.jsonl` | 6 | Live quality cases (`tag=live`, needs `ANTHROPIC_API_KEY`) |

```bash
ccm eval run data/evals/smoke.jsonl --dry-run        # CI-safe
ccm eval run data/evals/prompting.jsonl --tag live    # live API
```

---

## Python Stack

```
src/
├── llm/               LLM clients — ClaudeClient, abstract LLMClient
├── routing/           5-router system (llm, skill, agent, memory, task)
├── api/               FastAPI app — /v1/complete, /v1/chat, /v1/route, /health
├── evals/             EvalCase, EvalSuite, EvalRunner, AsyncEvalRunner
├── persistence/       FileStore, MemoryStore, TieredMemory, LogIndex
├── prompt_engineering/ Templates, few-shot builders, chain composers
├── utils/             RateLimiter, ResponseCache, TokenCounter
└── handlers/          Error classification + retry logic
```

```python
# LLM client
from src.llm import ClaudeClient, build_request

client = ClaudeClient()
resp = await client.complete(build_request("Explain RAG in 3 sentences"))
print(resp.content)      # text
print(resp.tokens_used)  # token count
print(resp.cost_usd)     # cost in USD

# Routing
from src.routing import route
d = route("implement JWT middleware with tests")
print(d.summary())

# Persistence
from src.persistence import FileStore
fs = FileStore()
fs.write_research("LightRAG", content)      # → data/research/YYYY-MM-DD-lightrag.md
fs.append_lesson("Never mock internals", …) # → tasks/lessons.md
fs.log_event("deploy", env="prod")          # → data/cache/events.log
```

---

## Tiered Memory

Three-tier memory system for context survival across sessions and compactions:

| Tier | Location | Size | Purpose |
|------|----------|------|---------|
| **Hot** | `.claude/memory/hot/hot-memory.md` | ≤50 lines | Always-loaded session context; auto-updated by PreCompact hook |
| **Warm** | `.claude/memory/warm/<domain>.md` | Unlimited | Domain knowledge: architecture · decisions · patterns · troubleshooting · api-surface |
| **Glacier** | `.claude/memory/glacier/YYYY-MM-DD-<slug>.md` | Unlimited | Immutable YAML-frontmatter ADRs with full-text search |

```python
from src.persistence import TieredMemory

tm = TieredMemory()
tm.write_hot("active_feature", "JWT auth middleware")       # hot: always loaded
tm.write_warm("architecture", "# Architecture\n...")        # warm: domain file
tm.archive_glacier("jwt-decision", content,                 # glacier: permanent ADR
                   tags=["auth", "security"], title="JWT over session cookies")

results = tm.search_glacier("PostgreSQL")                   # full-text + tag search
```

```bash
ccm memory-bank status          # show all tiers
ccm memory-bank query "routing" # search warm + glacier
```

---

## Hooks

| Hook | Trigger | Behavior |
|------|---------|----------|
| `session-start.sh` | Every session start | Colored banner · git stats · last commits · open tasks · lessons · health |
| `pre-compact.sh` | Before context compaction | Snapshot git state + open tasks → hot-memory.md · daily session log |
| `user-prompt-submit.sh` | Every user message | Branch safety warning · long-prompt detection |
| `pre-tool-bash.sh` | Before every Bash | Log command · block dangerous patterns (exit 2) |
| `post-tool-edit.sh` | After every Edit/Write | Auto-lint Python · validate JSON · check SKILL.md frontmatter |
| `post-tool-pr.sh` | After `gh pr create` | List changed files · suggest `/simplify` |
| `stop.sh` | Session end | Validators (uncommitted/open tasks/lint) · session log → `data/sessions/` |

**Exit codes:** `0` = allow  ·  `2` = block the tool call

---

## Agents

| Agent | Invocation | Purpose |
|-------|-----------|---------|
| `ralph-loop` | `run autonomously` / `loop until done` | Self-driving dev: read todo → plan → implement → verify → loop |
| `research-agent` | `research X` / `deep dive` | Karpathy method: search → distill → implement → store |
| `swarm-orchestrator` | `swarm this` / `parallel agents` | Decompose complex task into parallel independent workstreams |
| `security-reviewer` | `security review` / `full audit` | 16-domain sweep → `data/outputs/security-report-*.md` |

---

## Self-Improvement Loop

```
Mistake → User corrects → tasks/lessons.md updated
    ↓
session-start.sh shows last lessons every boot
    ↓
self-improve.sh (Monday 8am) distills → tasks + commits
    ↓
lessons.md becomes a personalized, growing ruleset
```

Over time the system gets smarter about your specific project, team, and preferences.

---

## Optimizer Crons

```bash
# Daily 7am: GitHub trending → research stubs
0 7 * * *   cd /home/user/wellux_testprojects && bash tools/scripts/github-trending-research.sh

# Daily 6am: doc freshness + skill frontmatter check
0 6 * * *   cd /home/user/wellux_testprojects && bash tools/scripts/optimize-docs.sh

# Monday 6am: Karpathy research loop (8 AI topics)
0 6 * * 1   cd /home/user/wellux_testprojects && bash tools/scripts/research-agent.sh

# Sunday midnight: security scan (secrets + permissions)
0 0 * * 0   cd /home/user/wellux_testprojects && bash tools/scripts/security-scan.sh

# Sunday 1am: perf audit (import times + code metrics)
0 1 * * 0   cd /home/user/wellux_testprojects && bash tools/scripts/perf-audit.sh

# Monday 8am: self-improvement loop (lessons → tasks)
0 8 * * 1   cd /home/user/wellux_testprojects && bash tools/scripts/self-improve.sh
```

Install: `crontab -e` and paste the above.

---

## CI / CD

**GitHub Actions** (`.github/workflows/ci.yml`) runs on every push:

| Job | What it does |
|-----|-------------|
| `test` | ruff lint + pytest (Python 3.11 & 3.12) + coverage upload |
| `smoke-evals` | `ccm eval run smoke.jsonl --dry-run` — no API key needed |
| `lint-dockerfile` | hadolint on Dockerfile |

**Docker:**
```bash
docker compose up        # → FastAPI on :8000 with /health check
docker compose up -d     # detached
```

---

## MCP Servers

Configured in `.mcp.json`:

| Server | Purpose |
|--------|---------|
| `github` | Issues, PRs, code search |
| `filesystem` | Structured file operations |
| `brave-search` | Web search for research |
| `sentry` | Error monitoring + alerts |
| `memory` | Cross-session entity memory |
| `sequential-thinking` | Structured multi-step reasoning |

---

## Project Structure

```
.claude/
├── settings.json           Max-autonomy permissions + hooks config
├── hooks/                  7 hook scripts (session-start, pre-compact, user-prompt, pre-bash, post-edit, post-pr, stop)
├── memory/                 hot/ · warm/ · glacier/ tiered memory
├── skills/                 123 SKILL.md files
├── agents/                 4 agent definitions
├── commands/               5 slash commands (deploy, audit, research, review, fix-issue)
└── rules/                  3 rule files (code-style, testing, api-conventions)

src/
├── llm/                    LLM clients + abstract interface
├── routing/                5-router system
├── api/                    FastAPI REST layer
├── evals/                  Eval framework
├── persistence/            FileStore, MemoryStore, LogIndex
├── prompt_engineering/     Templates, few-shot, chaining
├── utils/                  RateLimiter, ResponseCache, TokenCounter
└── handlers/               Error classification

config/                     YAML configs (models, prompts, logging)
data/
├── evals/                  Bundled eval suites (smoke, routing, prompting)
├── research/               Karpathy-style research stubs (auto-generated)
├── cache/                  Event logs, cron output
└── outputs/                Security reports, audit outputs

tasks/
├── todo.md                 Checkable task list
└── lessons.md              Self-improvement log

docs/                       Architecture, ADRs, runbooks
tools/scripts/              Cron scripts
examples/                   basic_completion.py, chat_session.py, chain_prompts.py
MASTER_PLAN.md              31-step bootstrap plan (loopable)
```

---

## Setup

```bash
# 1. Clone
git clone <repo> wellux_testprojects && cd wellux_testprojects

# 2. Python environment
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. API key
export ANTHROPIC_API_KEY="sk-ant-..."
# or add to ~/.bashrc / ~/.zshrc

# 4. Run tests (no API key needed)
pytest tests/ -q
ccm eval run data/evals/smoke.jsonl --dry-run

# 5. Start API server
ccm serve --reload

# 6. Install crons (optional)
crontab -e   # paste from Optimizer Crons section

# 7. Launch Claude Code
claude
```

---

## Core Principles

| Principle | Rule |
|-----------|------|
| **Route first** | Let the routing system pick model/skill/agent — don't override without reason |
| **Verify before done** | Run tests + `ccm eval run smoke.jsonl --dry-run` before marking complete |
| **Lint gate** | `ruff check src/ tests/ --select E,F,W --ignore E501` must be clean |
| **Self-improve** | After any correction → add lesson to `tasks/lessons.md` |
| **Minimal impact** | Touch only what the task requires |
| **Brainstorm first** | For non-trivial tasks: `/brainstorm` → `/write-plan` → `/superpowers execute` |
| **Ship with confidence** | `/ship` enforces: tests → lint → security → build → health check |
