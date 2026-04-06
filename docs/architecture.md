# System Architecture

## Overview

Claude Code Max is a **5-layer autonomous development harness** built on top of Claude Code CLI.
Each layer adds a different kind of intelligence: persistent context, auto-invoked capability,
deterministic safety, autonomous subagents, and modular instructional rules.

```
┌─────────────────────────────────────────────────────────┐
│                      USER / DEVELOPER                    │
└──────────────────────────┬──────────────────────────────┘
                           │ claude / "f" / skill invocation
                           ▼
┌─────────────────────────────────────────────────────────┐
│  L1 — CLAUDE.md + SOUL.md + USER.md (Persistent)        │
│  Loaded every session. Workflow rules, routing ref,      │
│  ccm CLI, REST API, evals, MCP, core principles.         │
│  SOUL.md: agent identity, decision style, principles.    │
│  USER.md: user profile, stack, working preferences.      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│         L2 — Skills (.claude/skills/ — 121 skills)       │
│  Auto-invoked by description keyword matching.           │
│  Categories: Security(16), Dev(20), AI/ML(15),           │
│  DevOps(15), Docs(10), Optimization(15), PM(9), Meta(2), │
│  Ecosystem(12): gstack · Superpowers · Paperclip roles.  │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│         L3 — Hooks (.claude/hooks/ — 5 hooks)            │
│  Deterministic callbacks. Exit 0=allow, 2=block.         │
│  session-start.sh → boot + hot-memory injection          │
│  pre-compact.sh  → snapshot state before context wipe    │
│  pre-tool-bash.sh → block dangerous commands             │
│  post-tool-edit.sh → auto-lint + validate SKILL.md       │
│  stop.sh → validators + daily session log                │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│       L4 — Agents (.claude/agents/ — 4 agents)           │
│  Autonomous subagents with own context windows.          │
│  ralph-loop → self-driving dev loop                      │
│  research-agent → Karpathy-style auto-research           │
│  swarm-orchestrator → parallel task decomposition        │
│  security-reviewer → full security sweep                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│       L5 — Rules (.claude/rules/ — 3 rule files)         │
│  Modular instruction files loaded as context.            │
│  code-style.md    → formatting, naming, type annotations │
│  testing.md       → framework, coverage, mocking, CI     │
│  api-conventions.md → endpoints, headers, middleware     │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Python Stack (src/)                         │
│  api/            → FastAPI: /health, /v1/{complete,chat,route} │
│  evals/          → EvalRunner, AsyncEvalRunner, scorers  │
│  llm/            → ClaudeClient, CompletionRequest       │
│  persistence/    → FileStore, MemoryStore                │
│  routing/        → 5-router system (llm/skill/agent/     │
│                     memory/task)                         │
│  utils/          → RateLimiter, Cache, Logger            │
│  handlers/       → Error classification + handling       │
│  prompt_engineering/ → Templates, FewShot, Chaining      │
└─────────────────────────────────────────────────────────┘
```

## Data Flow — Single Completion Request

```
User prompt
    │
    ├─ Cache check (ResponseCache) ──→ cache hit → return immediately
    │
    ├─ Rate limit (RateLimiter token bucket)
    │
    ├─ API call (anthropic SDK, async)
    │     └─ retry loop (max 3, exponential backoff 2^attempt)
    │          ├─ RateLimitError → sleep + retry
    │          └─ APIError → log + retry, raise on final attempt
    │
    ├─ CompletionResponse built (content, model, tokens, cost_usd)
    │
    ├─ Cache set
    │
    └─ Structured log (JSON: model, tokens, latency_ms, cost_usd)
```

## Data Flow — Prompt Chain

```
initial_context dict
    │
    ▼
Step 1: prompt_fn(context) → LLM → transform(output) → context["step1"]
    │
    ▼
Step 2: prompt_fn(context) → LLM → transform(output) → context["step2"]
    │
    ▼
...
    │
    ▼
ChainResult(steps={}, responses={}, total_cost_usd, total_tokens)
```

## Memory Hierarchy

```
~/.claude/CLAUDE.md          ← Global (all projects, personal rules)
~/CLAUDE.md                  ← Monorepo root (if applicable)
./CLAUDE.md                  ← Project (shared on git) ← PRIMARY
./src/api/CLAUDE.md          ← API module context
./src/persistence/CLAUDE.md  ← Persistence context
```

Rules:
- Each file < 200 lines
- Subfolder files append context, never overwrite
- Git-committed files = team knowledge; settings.local.json = personal/local only

## MASTER_PLAN Loop

```
session-start.sh boots
    │
    └─ shows: next - [ ] step from MASTER_PLAN.md
                    ↓
                User types "f"
                    ↓
                Claude finds first - [ ] step
                    ↓
                Execute step
                    ↓
                Replace - [ ] with - [x]
                    ↓
                Loop (type "f" again)
```

## Routing System (src/routing/)

Five routers auto-select the best model, skill, agent, memory tier, and task plan:

```
route("your task") → RoutingDecision
├── .llm     → opus | sonnet | haiku  (complexity 0-10)
├── .skill   → skill name + confidence (70+ keyword triggers)
├── .agent   → ralph | research | swarm | security
├── .memory  → CACHE | FILES | LESSONS | MCP | TODO
└── .plan    → ATOMIC | MEDIUM | COMPLEX + subtask list
```

## REST API (src/api/)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Status + available models |
| `/v1/complete` | POST | Single-turn completion (auto-routes model) |
| `/v1/complete/stream` | POST | SSE streaming tokens |
| `/v1/chat` | POST | Multi-turn conversation |
| `/v1/route` | POST | Routing decision only (no LLM call) |

Every response: `X-Request-ID` (correlation) + `X-Process-Time-Ms` (timing).

## Eval Framework (src/evals/)

```python
suite = EvalSuite("smoke").add(EvalCase("greet", "Say hello", contains=["hello"]))
report = EvalRunner(llm).run(suite)                    # sync
report = await AsyncEvalRunner(llm, concurrency=5).run(suite)  # async
```

Bundled suites in `data/evals/`: `smoke.jsonl`, `routing.jsonl`, `prompting.jsonl`

## Optimizer Cron Schedule

```
Daily  07:00  github-trending-research.sh → GitHub trending → research stubs
Daily  06:00  optimize-docs.sh            → doc freshness + frontmatter check
Mon    06:00  research-agent.sh           → Karpathy research loop (8 topics)
Sun    00:00  security-scan.sh            → secrets + permissions + patterns
Sun    01:00  perf-audit.sh               → import times + code metrics
Mon    08:00  self-improve.sh             → lessons → improvement tasks → commit
```

## Ecosystem Integrations

Three external methodologies are embedded as skills in `.claude/skills/`:

### gstack (Garry Tan / Y Combinator)
Role-based engineering personas that switch Claude into a mode with distinct priorities and constraints.

| Skill | Persona | Use when |
|-------|---------|----------|
| `/office-hours` | CEO + CTO + PM + Designer | Before starting a significant feature |
| `/plan-eng-review` | Staff Engineer | Technical approach review before coding |
| `/ship` | Release Engineer | test → lint → security → build → deploy → monitor |
| `/careful` | Senior Eng (risk-averse) | Irreversible/destructive operations |

### Superpowers (obra / Jesse Vincent)
Enforces rigorous software engineering discipline. Three-phase workflow:

```
/brainstorm <feature>          ← Socratic requirements refinement
       ↓
/write-plan                    ← Decompose into 2-5 min atomic tasks
       ↓
/superpowers execute           ← High-agency implementation + tests
```

Also available standalone: `/plan-eng-review` (pre-implementation gate).

### Paperclip AI
Multi-agent orchestration with org structure, spend budgets, and audit trails.

```
/paperclip assign "feature X" --agent ralph --budget 50k-tokens
/swarm "large refactor" --parallel 5
```

---

## Key Design Decisions

See `docs/decisions/` for full ADRs.

1. **Claude as primary LLM** — best agentic capabilities, tool use, long context
2. **Python stack** — widest ML ecosystem, async support, type hints
3. **SKILL.md auto-activation** — description field triggers invocation without explicit `/skill-name`
4. **settings.local.json gitignored** — local `Bash(*)` override without committing it
5. **Hook exit codes** — exit 2 blocks the tool call deterministically, no LLM judgment needed
6. **Three-phase feature workflow** — `/brainstorm` → `/write-plan` → `/superpowers execute` prevents premature implementation
7. **Role personas over raw prompts** — gstack-style personas produce more consistent output than unstructured prompts
