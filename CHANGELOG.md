# Changelog

All notable changes to Claude Code Max are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased]

---

## [1.0.7] — 2026-04-05

### Fixed
- `src/mcp_server.py`: `cmd_serve_mcp` was importing non-existent module-level name `mcp`;
  added `run()` entry point — `serve-mcp` now works correctly when `mcp` package is installed.
- `pyproject.toml`: removed stale `omit = ["src/cli.py"]` from coverage config; CLI functions
  are tested directly in `test_cli.py`, not via subprocess.
- `src/evals/runner.py`: `EvalRunner` (sync) now accepts `max_workers: int | None`; uses
  `ThreadPoolExecutor` for parallel execution when `max_workers > 1`. 3 tests added.
- `src/cli.py`: `ccm eval run` now prints `threshold: N%` after the report summary.
- `.github/workflows/ci.yml`: `live-evals` job condition now explicitly excludes fork PRs
  via `head.repo.full_name == github.repository` guard alongside secrets check.
- `Dockerfile`: added comment directing to base image digest pinning as the correct
  reproducibility fix for apt package versions.

### Changed
- `session-start.sh`: richer boot display — version line, 5 recent commits (was 3), last
  session log summary, full hot-memory dynamic zone, static section headings map, last 3
  complete lessons (was raw `tail -8`), open findings in amber when present.
- `pre-compact.sh`: now parses version/tests/skills dynamically; preserves `<!-- STATIC -->`
  zone from hot-memory.md so curated content (Completed Work, Architecture Decisions) is
  never overwritten by automation.
- `hot-memory.md`: split into `<!-- DYNAMIC -->` / `<!-- STATIC -->` zones via marker.
- `tasks/open-findings.md`: new P2/P3 backlog file; all 8 items from v1.0.x audit resolved.

---

## [1.0.5] — 2026-04-05

### Fixed (config hardening from deep review)
- `data/evals/smoke.jsonl`: remove non-standard comment lines; description moved to first case metadata
- `pyproject.toml`: add upper bound `requires-python = ">=3.11,<4"`
- `.github/workflows/ci.yml`: add `cache-dependency-path: pyproject.toml` to all 4 setup-python steps

## [1.0.6] — 2026-04-05

### Security
- `src/api/app.py`: `HTTPException` detail no longer exposes raw `str(e)` to API clients.
  Detail is now `"Upstream LLM error [ExcType] — see server logs (request_id=…)"` — full error
  remains in server logs only.
- `src/utils/logger.py`: `_StructuredFormatter` redacts sensitive field names (`password`, `token`,
  `api_key`, `secret`, etc.) before JSON serialisation. 4 tests added.

---

## [1.0.4] — 2026-04-05

### Fixed
- `src/routing/task_router.py`: removed `_needs_build` dead variable (assigned, never used;
  implementation subtask was always added unconditionally). 3 regression tests added.
- `src/llm/claude_client.py`: guard `message.content[0].text` with empty-content check in both
  `complete()` and `chat()` — raises `ValueError` instead of `IndexError` on empty Anthropic response.
- `src/persistence/tiered_memory.py`: cache compiled hot-key regex patterns in module-level dict
  (`_hot_key_patterns`) to avoid `re.compile()` on every `write_hot()` call. 2 tests added.
- `src/api/models.py`: `ChatRequest.messages` now requires `min_length=1` (empty list was silently
  accepted); `max_tokens` gets `le=200000` matching `CompleteRequest`. 4 validation tests added.
- `.claude/hooks/session-start.sh`: replace hardcoded `127.0.0.1:<port>` git remote URL with
  dynamic `git remote get-url origin` — port changes each session.

---

## [1.0.3] — 2026-04-05

### Added
- API versioning: all business endpoints moved to `/v1/` prefix via `APIRouter(prefix="/v1")`.
  `/health` remains at root (standard convention). Enables future `/v2/` without breaking `/v1/`
  clients. Updated README, `src/api/CLAUDE.md`, and `CLAUDE.md` endpoint tables.
- `tests/conftest.py`: shared `tiered_memory`, `file_store`, and `mock_claude_client` fixtures
  available to all test files (eliminates per-file boilerplate)

### Fixed
- README and CLAUDE.md had stale unversioned endpoint paths after API versioning

---

## [1.0.2] — 2026-04-05

### Added
- `ccm lint` CLI subcommand wrapping `ruff check src/ tests/ --select E,F,W,I --ignore E501`
  with `--fix` and `--no-cache` flags; 7 tests in `TestLint`
- `TieredMemory.search_glacier(query, *, limit=20)` — early-break prevents O(n) full-dir scan;
  1 new test verifying limit enforcement

### Fixed
- `src/mcp_server.py` called `_require_fastmcp()` at module level, causing `sys.exit(1)` on any
  plain `import` when `mcp` package wasn't installed (broke test discovery and coverage tools).
  Tool functions now defined at module level as plain Python; `_build_server()` defers FastMCP
  instantiation to runtime (`__main__` only).

---

## [1.0.1] — 2026-04-05

### Fixed
- `error_handler.py`: operator precedence bug — `"context" in msg` alone (e.g. `"asyncio context"`,
  `"invalid context path"`) incorrectly mapped to `TokenLimitError`. Now requires `"context+window"`
  or `"context+length"` or `"token+limit"`. Same fix applied to `ContentFilterError` (now requires
  `"content+filter"` or `"policy violation"` rather than `"content"` alone).
- `tiered_memory.py`: removed dead variable on line 110 — stale reference to module-level `_MEMORY_ROOT`
  immediately overwritten by `self._warm_dir`. Latent path bug if line 111 were ever removed.
- `llm_router.py`: removed duplicate `"lookup"` in `_LOW_SIGNALS` (double-penalized tasks containing
  the word lookup, over-biasing toward haiku).
- `skill_router.py`: narrowed `grc-analyst` trigger `"audit"` → `"compliance audit"` / `"grc audit"`
  to prevent false routing of `"audit my code"` / `"run a db audit"` to GRC compliance analyst.
- `api/app.py`: `/chat` endpoint now uses native Anthropic `messages` API via `ClaudeClient.chat()`
  instead of flattening conversation history to a single string (which bypassed multi-turn context and
  enabled role injection via `msg.role.upper()`).
- `claude_client.py`: added `ClaudeClient.chat(messages, ...)` method for proper multi-turn conversations
  with retry, rate limiting, and structured logging.

### Changed
- `.pre-commit-config.yaml`: updated ruff rev `v0.4.10` → `v0.9.0` to match `pyproject.toml` requirement
- `.claude/USER.md`: corrected stale skill count `"114+ skills"` → `"123 skills"`

### Added
- `data/evals/smoke.jsonl`: `echo-excludes-verified` case to exercise the `excludes` scorer in CI
  dry-run mode (previously excludes were never evaluated in CI)
- `tests/test_handlers_error.py`: 8 edge-case tests for `classify_api_error` covering the operator
  precedence regression, `content` alone, `policy violation`, and ambiguous context messages
- `tests/test_api_endpoints.py`: updated `TestChat` to mock `.chat()` and verify messages list is
  passed directly (not flattened to string)

### Stats
- Tests: 615 → **623** | Smoke suite: 5 → **6 cases** | Bugs fixed: **5**

---

## [1.0.0] — 2026-04-05

### Added — First Stable Release
- Version bump `0.8.0` → `1.0.0` in `pyproject.toml` and package description
- `version badge` in README (`[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)]`)
- README fully updated: badges (615 tests, 123 skills, v1.0.0), 5-layer diagram (7 hooks),
  v0.9 skills section (9 new skills), Tiered Memory section with usage examples, CLI table
  (context-diff/memory-bank), hooks table (7 entries), project structure updated

### Stats
- Tests: 615 | Skills: 123 | Hooks: 7 | Per-module CLAUDE.md: 6 | Glacier ADRs: 3

---

## [0.9.4] — 2026-04-05

### Added
- Per-module CLAUDE.md files (recursive loading, hidden feature #2) — second batch:
  - `src/evals/CLAUDE.md` — EvalCase/Suite/Runner API, JSONL format, key invariants (duplicate ID check, 30s timeout)
  - `src/utils/CLAUDE.md` — Logger exc_info critical note, LogIndex eviction rules, test locations
  - `src/llm/CLAUDE.md` — Model ID table, async-only rules, API key security, APIError→502 contract
- Glacier tier populated (3 architectural decision records with YAML frontmatter + tags):
  - `tiered-memory-architecture` — hot/warm/glacier rationale, consequences, eviction design
  - `skill-registry-duplicate-enforcement` — no-duplicate invariant, CI enforcement, resolution process
  - `precompact-hook-context-survival` — PreCompact hook design, context survival gap, exit-0 constraint
- 9 tests for `ccm memory-bank` (status/query/sync subcommands, output validation, dispatch wiring)
- CHANGELOG v0.9.2 and v0.9.3 entries (previously missing)

### Stats
- Tests: 606 → 615 | Per-module CLAUDE.md: 3 → 6 modules | Glacier: 0 → 3 decision records

---

## [0.9.3] — 2026-04-05

### Added
- `warm/api-surface.md` — REST endpoints, full CLI command table, MCP servers, Python API reference; completes the 5-domain warm memory bank
- Per-module CLAUDE.md files using Claude Code's recursive loading (hidden feature #2):
  - `src/routing/CLAUDE.md` — registry invariant, 5-router layout, adding-a-skill checklist
  - `src/persistence/CLAUDE.md` — tier paths, TieredMemory rules, test conventions
  - `src/api/CLAUDE.md` — middleware order, error codes, streaming format, auto-routing
- `ccm memory-bank` CLI subcommand: `status` (domain preview), `query <term>` (cross-tier search), `sync`
- Lessons 18–21 (self-reflect): Edit stale read · background agent re-introduces bugs · registry dup fix · PreCompact is the critical hook

### Stats
- Tests: 606 | Warm memory: 4 → 5 domains | Per-module CLAUDE.md: 3 new

---

## [0.9.2] — 2026-04-05

### Added
- Warm memory bank populated (4 domain files):
  - `architecture.md` — 5-layer stack, source layout, routing, REST API, persistence tiers, hooks lifecycle, 123 skills by category
  - `decisions.md` — 8 architectural decisions with rationale (build system, package layout, logger, skill registry, tiered memory, PreCompact, dep pins, RIPER design)
  - `patterns.md` — routing, skill registry, TieredMemory, logger, EvalCase, middleware, test structure, hook exit codes
  - `troubleshooting.md` — 8 known issues with root cause and fix
- 6 tests for `ccm context-diff` CLI

### Changed
- `CHANGELOG.md` — added v0.9.1 entry
- `CONTRIBUTING.md` — skill count 114 → 123, hooks 4 → 7 with names

### Stats
- Tests: 600 → 606 | Warm memory: 0 → 4 files

---

## [0.9.1] — 2026-04-05

### Added — Identity Trio Complete · RIPER · Memory Bank · Context-Diff CLI

#### Identity Layer Complete
- `.claude/MEMORY.md` — active decisions, architectural choices, dep pins, watch list (completes SOUL + USER + MEMORY trio)

#### New Skills (2)
| Skill | What it does |
|-------|-------------|
| `/riper` | 5-phase gate: Research→Innovate→Plan→Execute→Review. Prevents premature implementation by enforcing phase approvals. |
| `/memory-bank` | Structured warm-tier sync (architecture, decisions, patterns, troubleshooting). Path-filtered query mode. |

#### New Hooks (2, total: 7)
- `UserPromptSubmit` hook — branch safety warning on main/master + long-prompt detection (>8000 chars)
- `post-tool-pr.sh` — lists changed Python files after `gh pr create`, suggests `/simplify`

#### CLI: `ccm context-diff`
- `ccm context-diff [--since HEAD~1]` — structured git diff summary: stat, commit list, changed files
- Time aliases: `yesterday`, `last-week`, `last-month`

#### Warm Memory Bank Populated
- `.claude/memory/warm/architecture.md` — full system architecture, routing, source layout, skills by category
- `.claude/memory/warm/decisions.md` — 8 key architectural decisions with rationale
- `.claude/memory/warm/patterns.md` — routing, skill registry, tiered memory, logger, eval, middleware, hook patterns
- `.claude/memory/warm/troubleshooting.md` — 8 known issues: Edit stale read, editable install, exc_info crash, duplicate triggers, ContextVar leak, EvalResult kwargs

### Changed
- Skill routing registry: 121 → 123 entries (riper + memory-bank)
- `.claude/settings.json` — added `UserPromptSubmit` hook

### Stats
- Skills on disk: 121 → 123
- Routing entries: 121 → 123
- Hooks: 5 → 7
- Warm memory files: 0 → 4

---

## [0.9.0] — 2026-04-05

### Added — Ecosystem Research · Tiered Memory · New Skills · Hooks v2

Comprehensive integration of leading Claude Code community patterns from the ecosystem
research pass (MindStudio leak analysis + top 10 trending GitHub repos).

#### Identity Layer (new)
- `.claude/SOUL.md` — agent identity, decision style, operating principles, what it will/won't do
- `.claude/USER.md` — user profile, stack, preferences, working style
- `.claude/memory/hot/hot-memory.md` — always-loaded active context (≤50 lines)
- `.claude/memory/warm/` — domain-specific contextual files loaded on activation
- `.claude/memory/glacier/` — YAML-frontmatter archived entries with full-text search

#### Tiered Memory System (`src/persistence/tiered_memory.py`)
Three-tier architecture inspired by marciopuga/cog and Advenire-Consulting/thebrain:
- **Hot tier** (`≤50 lines`) — key-value store, auto-loaded every session via session-start hook
- **Warm tier** (domain files) — `write_warm(domain, content)`, `append_warm()`, `list_warm_domains()`
- **Glacier tier** (YAML-frontmatter archives) — `archive_glacier(slug, content, tags=[])`, `search_glacier(query)`, `list_glacier(tag=None)`
- Auto-eviction: hot tier evicts oldest lines to warm when over limit
- 26 new tests; exported from `src/persistence`

#### Hook Expansion (v2)
- **PreCompact hook** (`.claude/hooks/pre-compact.sh`) — fires before context compaction, snapshots active git state + open tasks to `hot-memory.md` and daily session log. Closes the most critical survivability gap (context wipe).
- **Stop hook v2** — added completion validators: uncommitted files warning, open task count, lint error count; structured daily session log written to `data/sessions/YYYY-MM-DD.md`
- **Session-start hook v2** — loads hot-memory summary, creates daily session log if absent, shows recent commit SHAs with ANSI color, branch color-coded red on main

#### New Skills (7)
| Skill | Category | What it does |
|-------|----------|-------------|
| `/preflight` | meta | 12-category prompt scorecard before expensive execution |
| `/tdd` | development | Multi-agent TDD with strict subagent information isolation (glebis pattern) |
| `/self-reflect` | meta | Autonomous pattern mining from commits + sessions → lessons.md |
| `/chain-of-draft` | meta | CoD structured prompting: skeleton → expand → critique → strengthen |
| `/foresight` | meta | Cross-domain strategic analysis surfacing non-obvious risks + one nudge |
| `/team` | meta | Preset agent teams: code-review, security, debug, architect, ship, research |
| `/context-diff` | meta | Structured change summary between git refs or sessions |

#### Swarm Upgrade (adversarial validation)
- Swarm skill updated with **Phase 4: Adversarial Validation** (dsifry/metaswarm pattern)
- After each agent self-reports done, a Validator agent independently re-reads the spec and checks each success criterion with `file:line` evidence
- Returns `VERIFIED ✅` or `FAILED ❌` with specific gaps; up to 3 retry cycles before escalation
- Prevents "cargo cult complete" pattern

#### Skill Registry Expansion
- Registry expanded from 114 → 121 entries (7 new skills added with 5+ triggers each)
- All 121 entries verified duplicate-free (no shared trigger phrases)
- Registry test updated: `test_registry_has_121_entries`

### Changed
- `src/persistence/__init__.py` — exports `TieredMemory`
- `.claude/settings.json` — added `PreCompact` hook entry
- CONTRIBUTING.md — updated skill count references

### Stats
- Tests: 574 → 600 (+26 tiered memory tests)
- Skills on disk: 114 → 121
- Routing entries: 114 → 121
- Hooks: 4 → 5 (PreCompact added)
- Python modules: +1 (`src/persistence/tiered_memory.py`)

---

## [0.8.0] — 2026-04-05

### Added — Ecosystem Integrations (gstack · Superpowers · Paperclip)

Seven new skills bring three external engineering methodologies into the harness as first-class slash commands.

#### gstack (Garry Tan / Y Combinator) — Role-Based Engineering Team
- `/office-hours` — CEO + CTO + PM + Designer debate approach and unearth hidden constraints before any code is written
- `/ship` — Release engineer mode: sequential gate of tests → lint → security → build → deploy → smoke → monitor
- `/careful` — Low-risk mode: blocks destructive operations, requires explicit confirmation, applies conservative defaults
- `/plan-eng-review` — Staff engineer pre-implementation review across 6 lenses (correctness, fit, complexity, safety, performance, security) with structured `APPROVED / NEEDS REVISION / BLOCKED` verdict

#### Superpowers (obra / Jesse Vincent) — Structured Methodology
- `/brainstorm` — Socratic requirements refinement loop; surfaces hidden constraints before any plan is written
- `/write-plan` — Decomposes a feature into atomic 2–5 minute tasks with explicit acceptance criteria and dependency order

#### Paperclip AI — Multi-Agent Orchestration
- `/paperclip` — Assign tasks to named agents with spend budgets, atomic task checkout, approval gates, and full audit trails

#### Standard three-phase workflow (now documented everywhere)
```
/brainstorm <feature>  →  /write-plan  →  /superpowers execute
```

### Changed
- **Skill count: 107 → 114** (added 7 ecosystem skills)
- `README.md` — full rewrite: ASCII art header, badges, architecture diagram, gstack/Superpowers/Paperclip ecosystem section, updated skill catalogue
- `docs/architecture.md` — updated L2 skill count, added **Ecosystem Integrations** section covering all three methodologies, added design decisions #6 and #7
- `CLAUDE.md` (project) — updated skill count, added ecosystem integrations overview
- `~/.claude/CLAUDE.md` (global) — added gstack/Superpowers/Paperclip reference sections with slash commands and standard workflow
- `~/.claude/hooks/session-start.sh` — full rewrite with ANSI colour output, recent commit log, Python version, stash count, Docker status, skills count, ecosystem shortcuts hint

### Tests
- **556 tests total**, all passing; lint clean

---

## [0.7.0] — 2026-03-28

### Added — Deployability from Claude and Claude Code

#### CLI Deploy Subcommands
- `ccm build [--no-cache] [--tag TAG]` — build Docker image `ccm-api:{version}` + `ccm-api:latest`
- `ccm deploy [--env local|staging|prod] [--dry-run] [--skip-tests] [--skip-build] [--skip-evals]` —
  full 6-step pipeline: doctor → tests → build → compose up → health poll → smoke evals
- `ccm ps` — show running container status via `docker compose ps`
- `ccm health [--url URL]` — hit live `/health` endpoint and display status/version/uptime
- `ccm serve-mcp` — start the MCP stdio server for Claude integration

#### MCP Deploy Server (`src/mcp_server.py`)
- Exposes `deploy`, `build`, `health`, `status`, `doctor`, `get_logs` as MCP tools
- Added to `.mcp.json` as `ccm` server — Claude (claude.ai) can now trigger deployments via MCP tools
- Install: `pip install ".[deploy]"` adds the `mcp>=1.0.0` dependency

#### Claude Code Slash Command
- `/deploy` — fully implemented (was a stub); 7-step pipeline with failure handling and rollback guide
- `.claude/settings.json` — added `docker *`, `docker compose *`, `ccm deploy/build/ps/health` permissions

### Tests
- +6 tests: build (no-docker), deploy (dry-run), ps, health (unreachable)
- **374 tests total**, all passing

---

## [0.6.1] — 2026-03-28

### Fixed
- `ccm status` showed `skills: 0` — glob was matching `*.md` at skills root instead of
  `*/SKILL.md` in subdirectories; now correctly counts 107 skills

### Added — CLI commands
- `ccm version` — prints `ccm <version>`, git short hash + branch, Python version
- `ccm doctor` — 13-point environment health check: API key, package imports, required paths,
  skill count (≥100), smoke eval presence, git repo, event log writability; exits 0=healthy / 1=issues
- `ccm logs` — query the indexed event log: `--event`, `--tag`, `--limit`, `--summary`, `--json`
- `ccm status` now shows `version`, renames `test count` → `tests`, adds `event log` summary line

### Tests
- `tests/test_cli.py` fully rewritten: 45 tests covering all 8 subcommands including
  `version`, `doctor`, `logs` (summary, filter-by-event, json output)
- **365 tests total**, all passing

---

## [0.6.0] — 2026-03-28

### Added — Versioning
- `src/version.py` — single source of truth: `__version__ = "0.6.0"`, `VERSION_INFO` tuple,
  `version_string()` helper; imported by `src/__init__`, `src/api/app.py`, FastAPI app title
- `/health` response now includes `version` (from `src.version`) and `uptime_s`
- `pyproject.toml` version bumped to `0.6.0` to stay in sync

### Added — Deployability
- `.dockerignore` — excludes `.claude/`, `tests/`, `docs/`, `data/`, `tools/`, ML deps,
  and secrets from the Docker build context (image stays lean and secret-safe)
- `.env.example` — documents every env var: `ANTHROPIC_API_KEY`, `HOST`, `PORT`,
  `LOG_LEVEL`, `WORKERS`, `CCM_*` settings, MCP tokens
- `docker-compose.yml` — `env_file` support, named `ccm-data` volume (persists events.log),
  resource limits (`cpus:2 / memory:512M`), structured log driver, `start_period:15s`

### Added — Stability
- `src/llm/claude_client.py` — retry rewrite with **full jitter** backoff
  (`base * 2^attempt ± 25%` jitter, capped at 30 s); separate handling for
  `_FATAL` errors (auth) that skip retry; `_RETRYABLE` tuple for rate-limit + 5xx
- `src/api/app.py` — graceful shutdown: logs `api_shutdown` with uptime to
  `LogIndex` before exiting; `api_startup` records version + PID; `_start_time`
  tracks server uptime for `/health`
- `src/api/app.py` — structured error events written to `LogIndex` on 502 errors
  with `request_id` correlation

### Added — Memory / Indexed Logs
- `src/utils/log_index.py` — thread-safe, append-only JSONL log with in-memory
  reverse index (event → line numbers, tag → line numbers); `O(1)` appends,
  `O(k)` search where k = matching entries; survives corrupt lines on reload
- `src/persistence/file_store.py` — `log_event()` now backed by `LogIndex`
  (returns written record); new `search_log(event, tags, limit)` and
  `log_summary()` methods
- `src/api/app.py` — `CCM_LOG_PATH` env var controls log destination;
  `_log` singleton initialised in lifespan and shared across handlers

### Changed
- `src/api/models.py` — `HealthResponse.version` is now required (no default);
  added optional `uptime_s: float | None`

### Tests
- `tests/test_log_index.py` — 26 new tests: append, search, tail, summary,
  persistence (reload + tag index), concurrent writes, corrupt-line skipping
- `tests/test_version.py` — 7 new tests: format, tuple consistency, package export
- `tests/test_api.py` — updated 2 HealthResponse tests for required `version` field
- **347 tests total**, all passing

---

## [0.5.0] — 2026-03-28

### Added
- **L5 Rules layer** (`.claude/rules/`): `code-style.md`, `testing.md`, `api-conventions.md`
- **Correlation middleware** (`src/api/middleware.py`): `CorrelationIDMiddleware` and `TimingMiddleware`
  — every response now carries `X-Request-ID` and `X-Process-Time-Ms`
- **Smoke evals in CI** — `ccm eval run data/evals/smoke.jsonl --dry-run` runs after tests
- `/review` command — structured code review checklist with APPROVE/REQUEST CHANGES verdict
- `/fix-issue` command — 4-gate process: reproduce → diagnose → fix → verify
- `session-start.sh` shows live test count, lint health, and skill count on boot

### Fixed
- All 30 ruff lint errors across `src/` and `tests/` resolved
- Stale `claude_code_max` path references replaced across all hook scripts,
  skill SKILL.md files, `.mcp.json`, `config/__init__.py`, `README.md`, cron scripts

---

## [0.4.0] — 2026-03-28

### Added
- **`ccm` CLI** (`src/cli.py`): `route`, `complete`, `serve`, `status`, `research`, `eval` subcommands
- **`pyproject.toml`**: modern packaging with ruff, mypy, pytest, coverage config; replaces `setup.py`
- **`.pre-commit-config.yaml`**: ruff + ruff-format + pre-commit-hooks + mypy runs on commit
- **`AsyncEvalRunner`** (`src/evals/runner.py`): semaphore-bounded concurrent eval execution
- **Eval suites** (`data/evals/`): `smoke.jsonl` (5 cases), `routing.jsonl` (5), `prompting.jsonl` (6)
- **`ccm eval`** subcommand: `list`, `inspect`, `run` with `--dry-run`, `--tag`, `--threshold`, `--json`
- **`X-Request-ID` + `X-Process-Time-Ms`** headers on all API responses

---

## [0.3.0] — 2026-03-28

### Added
- **Eval framework** (`src/evals/`): `EvalCase`, `EvalSuite`, `EvalRunner`, scorers (exact_match,
  contains_all, excludes_none, regex_match, composite), `EvalReport.summary()` with progress bar
- **`src/api/`** — FastAPI app: `/health`, `/complete`, `/complete/stream`, `/chat`, `/route`
- **`src/persistence/`** — `FileStore` (research/outputs/lessons/tasks/events) + `MemoryStore`
  with MCP fallback to in-memory dict
- **GitHub Actions CI** (`.github/workflows/ci.yml`): ruff lint + pytest on Python 3.11/3.12,
  coverage upload, hadolint on Dockerfile
- **Multi-stage Dockerfile** + `docker-compose.yml`

---

## [0.2.0] — 2026-03-28

### Added
- **5-router routing system** (`src/routing/`):
  - `llm_router.py` — complexity scoring → opus/sonnet/haiku
  - `skill_router.py` — 70+ keyword triggers → 30+ skill mappings
  - `agent_router.py` — task signal → ralph/research/swarm/security
  - `memory_router.py` — content type → CACHE/FILES/LESSONS/MCP/TODO
  - `task_router.py` — ATOMIC/MEDIUM/COMPLEX + subtask decomposition
- **`route()` facade** + `RoutingDecision.summary()` box display
- Security audit pass — 2 medium findings fixed (dep pins + max_tokens floor)

---

## [0.1.0] — 2026-03-28

### Added
- 5-layer architecture scaffold:
  - **L1** `CLAUDE.md` — persistent session context
  - **L2** `.claude/skills/` — 107 auto-invoked skills with keyword frontmatter
  - **L3** `.claude/hooks/` — 4 deterministic safety hooks
  - **L4** `.claude/agents/` — 4 autonomous subagents (ralph, research, swarm, security)
  - **L5** (added later) `.claude/rules/` — modular instruction files
- Python stack: `src/llm/`, `src/utils/`, `src/handlers/`, `src/prompt_engineering/`
- Config: `model_config.yaml`, `prompt_templates.yaml`, `logging_config.yaml`
- 5 optimizer cron scripts + systemd user timers
- `tools/prompts/` — 15 system prompts + few-shot examples
- `docs/` — architecture, resources, 2 ADRs, 3 runbooks
- `MASTER_PLAN.md` — loopable 31-step bootstrap (100% complete)

---

[Unreleased]: https://github.com/Wellux/wellux_testprojects/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/Wellux/wellux_testprojects/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/Wellux/wellux_testprojects/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Wellux/wellux_testprojects/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Wellux/wellux_testprojects/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Wellux/wellux_testprojects/releases/tag/v0.1.0
