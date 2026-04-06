# Warm Memory: API Surface
<!-- L1: REST endpoints, request/response models, CLI commands, MCP tools -->

**Last Updated**: 2026-04-06

---

## REST API (`src/api/` — start with `ccm serve`)

Base URL: `http://localhost:8000`
All responses: `X-Request-ID` + `X-Process-Time-Ms` headers.

### Endpoints

| Method | Path | Body | Returns |
|--------|------|------|---------|
| `GET` | `/health` | — | `{status, models, version}` |
| `POST` | `/v1/complete` | `{prompt, model?, max_tokens?, auto_route?}` | `{content, model, routed_by}` |
| `POST` | `/v1/complete/stream` | same as /v1/complete | SSE: `data: <token>\n\n` … `data: [DONE]\n\n` |
| `POST` | `/v1/chat` | `{messages: [{role,content}], model?, max_tokens?}` | `{content, model}` |
| `POST` | `/v1/route` | `{task}` | `RoutingDecision` JSON (no LLM call) |

### Error format
```json
{"detail": "error message"}
```
Status codes: 200 OK · 201 Created · 400 Client error · 422 Validation · 429 Rate limit · 502 Upstream LLM error

### Streaming format
```
data: Hello
data:  world
data: [DONE]
```
On error during stream: `data: [ERROR] <message>\n\n`

### Rate limiting
Default: 100 req/min per instance. On limit: `HTTP 429`.

---

## CLI (`ccm` — `pip install -e ".[dev]"`)

| Command | Flags | Description |
|---------|-------|-------------|
| `ccm version` | — | Python version, git hash, VERSION |
| `ccm route "task"` | `--json` | Full 5-router decision |
| `ccm complete "prompt"` | `--model haiku/sonnet/opus` | One-shot LLM call |
| `ccm serve` | `--host --port --reload` | Start FastAPI |
| `ccm status` | — | Branch, test count, skill count |
| `ccm doctor` | — | Env health: Python, deps, API key |
| `ccm research "topic"` | — | Create `data/research/YYYY-MM-DD-<slug>.md` |
| `ccm logs` | `--event --tag` | Query indexed event log (JSONL) |
| `ccm eval list` | — | List eval suites in `data/evals/` |
| `ccm eval inspect <file>` | — | Show cases + constraints |
| `ccm eval run <file>` | `--dry-run --tag --threshold --json` | Run eval suite |
| `ccm build` | `--no-cache --tag` | Build Docker image |
| `ccm deploy` | `--env --dry-run` | Full pipeline: doctor→test→build→up→health→evals |
| `ccm ps` | — | Running container status |
| `ccm health` | `--url` | Ping `/health` endpoint |
| `ccm serve-mcp` | — | Start MCP stdio server |
| `ccm context-diff` | `--since HEAD~1` | Git diff summary (aliases: yesterday, last-week) |

---

## MCP Server (`ccm serve-mcp` or `python -m src.mcp_server`)

Exposes tools over stdio for Claude Code integration.
Config in `.mcp.json`.

Active MCP servers:
- `github` — GitHub API (PR review, issues, CI status)
- `filesystem` — filesystem read/write (MCP-scoped)
- `brave-search` — web search
- `sentry` — error tracking
- `memory` — entity graph (MCP-backed MemoryStore)
- `sequential-thinking` — structured reasoning chains

---

## Python API (`from src.routing import route`)

```python
from src.routing import route, RoutingDecision

d: RoutingDecision = route("your task here")
d.model          # "opus" | "sonnet" | "haiku"
d.skill          # SkillMatch(skill="ciso", confidence=0.9, category="security")
d.agent          # "security-reviewer" | "ralph-loop" | "research-agent" | "swarm-orchestrator" | None
d.memory         # MemoryRoute(tier="LESSONS", reason="...")
d.task           # TaskPlan(complexity="COMPLEX", subtasks=[...])
d.summary()      # pretty-printed box for display
```

```python
from src.persistence import FileStore, MemoryStore, TieredMemory
from src.evals import EvalCase, EvalSuite, EvalRunner, AsyncEvalRunner
from src.utils.logger import get_logger
```
