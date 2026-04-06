# Contributing to Claude Code Max

## Quick Start

```bash
git clone <repo> && cd wellux_testprojects
git checkout -b claude/<description>-<id>
pip install -e ".[dev]"
pre-commit install
```

## Development Workflow

```
f     → execute next MASTER_PLAN step
s     → git status + open tasks
a     → full audit (security + perf + docs)
r     → Karpathy research run
```

Run checks before commit:

```bash
ruff check src/ tests/ --select E,F,W --ignore E501   # lint
pytest tests/ --tb=short -q                           # tests
ccm eval run data/evals/smoke.jsonl --dry-run         # smoke evals
```

## Branch Naming

```
claude/<description>-<short-id>     # Claude Code sessions
feature/<description>               # human features
fix/<description>                   # bug fixes
```

Never push to `main` without explicit permission.

## Adding a Skill

1. Create `.claude/skills/<skill-name>/SKILL.md`
2. Required frontmatter:

```yaml
---
name: my-skill
description: >
  One line description. Invoke for: "use case 1", "use case 2".
  Trigger keywords that will cause auto-invocation.
---
```

3. Body: mission, steps, output format, examples
4. Verify: `ls .claude/skills/ | wc -l` should be ≥123

## Adding a Router

All routers live in `src/routing/`. Each must:
- Return a typed dataclass (see existing routers for pattern)
- Be exported from `src/routing/__init__.py`
- Have tests in `tests/test_routing.py`

## Adding an Eval Suite

Create `data/evals/<name>.jsonl` — one JSON object per line:

```json
{"id": "case-1", "prompt": "Say hello", "contains": ["hello"], "tag": "smoke"}
```

Fields: `id`, `prompt`, `contains?`, `excludes?`, `regex?`, `tag?`, `min_length?`, `max_length?`

Run: `ccm eval run data/evals/<name>.jsonl --dry-run`

## Commit Messages

Imperative mood, explain WHY not what:

```
feat: add X to solve Y
fix: prevent Z by doing W
docs: update architecture for L5 rules layer
```

## CI Gates

All must pass before merge:
- `ruff check src/ tests/ --select E,F,W --ignore E501`
- `pytest tests/ --tb=short -q`
- `ccm eval run data/evals/smoke.jsonl --dry-run`
- `hadolint Dockerfile`

## File Structure

```
.claude/
  skills/     123 auto-invoked skills (keyword-triggered)
  hooks/      7 deterministic hooks (session-start, pre-compact, user-prompt-submit, pre-bash, post-edit, post-pr, stop)
  agents/     4 autonomous subagents
  rules/      3 modular instruction files
  commands/   5 slash commands

src/
  api/        FastAPI: /health /complete /complete/stream /chat /route
  evals/      EvalCase, EvalSuite, EvalRunner, AsyncEvalRunner
  llm/        ClaudeClient, CompletionRequest/Response
  persistence/ FileStore, MemoryStore
  routing/    5 routers (llm/skill/agent/memory/task)
  utils/      cache, rate_limiter, logger

data/
  evals/      JSONL eval suites
  research/   Karpathy research stubs (populated by research-agent)

tasks/
  todo.md     Active task list
  lessons.md  Self-improvement log
```
