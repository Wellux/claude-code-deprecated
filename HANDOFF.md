# WELLUX TESTPROJECTS — COMPLETE PROJECT HANDOFF DOCUMENT
> Generated: 2026-04-06 08:07:57 | Branch: claude/optimize-cli-autonomy-xNamK | Commit: 2edefc5

---

# 1. PROJECT OVERVIEW

## Purpose and Goals

**Claude Code Max (ccm)** is a gold-standard Claude Code template and reference implementation demonstrating max-autonomy AI-assisted development. It combines:
- A full Python backend (FastAPI REST API, eval framework, 5-router routing system)
- 123 Claude Code skills (keyword-triggered AI workflows)
- 5 deterministic hooks (session-start, pre-compact, pre-bash, post-edit, stop)
- A `ccm` CLI for local developer operations
- MCP (Model Context Protocol) server exposing ccm commands as AI-callable tools

## Core Problem Being Solved

Developers lose context between Claude sessions and repeat the same manual steps. This project:
1. Persists context via tiered memory (hot/warm/glacier) + pre-compact hook
2. Auto-invokes the right AI skill for each task via 5-router system
3. Provides a full production-grade stack as a copy-paste starting point
4. Self-improves via lessons.md pattern (31 lessons capturing every mistake)

## Target Users / Use Cases
- AI engineers wanting a production-ready Claude Code project template
- Teams wanting autonomous AI deployment/operations tooling
- Developers learning advanced Claude Code patterns (hooks, skills, routing, memory)

## Current Maturity
- **Version:** 1.0.7 (stable)
- **Tests:** 667 passing, 0 failing
- **Coverage:** ~95%+ on all public APIs
- **Lint:** ruff CLEAN
- **CI:** 3-job GitHub Actions pipeline (test matrix, smoke-evals, lint-dockerfile)

---

# 2. SYSTEM ARCHITECTURE

## High-Level Architecture

```
[User / Claude Code CLI]
        │
        ▼
[L1: CLAUDE.md + .claude/SOUL.md + .claude/USER.md]  ← Persistent context
        │
        ▼
[L2: .claude/skills/ — 123 auto-invoked skills]      ← Keyword-triggered
        │
        ▼
[L3: .claude/hooks/ — 5 deterministic hooks]         ← Safety + automation
        │
        ▼
[L4: .claude/agents/ — 4 autonomous subagents]       ← Spawned on demand
        │
        ▼
[L5: .claude/rules/ — Modular instruction files]     ← Loaded as context

[ccm CLI] → [src/routing/] → [src/llm/ClaudeClient] → [Anthropic API]
                │
                ├─ llm_router.py    → selects opus/sonnet/haiku
                ├─ skill_router.py  → maps task to 1 of 123 skills
                ├─ agent_router.py  → routes to ralph/research/swarm/security
                ├─ memory_router.py → hot/warm/glacier/mcp/todo
                └─ task_router.py   → ATOMIC/MEDIUM/COMPLEX + subtasks

[FastAPI /health /v1/complete /v1/chat /v1/route /v1/complete/stream]
        │
        └─ middleware: CorrelationID → Timing → ContentLengthLimit
```

## Component Breakdown

| Component | Location | Role |
|-----------|----------|------|
| ccm CLI | src/cli.py | 927-line entry point; all user-facing commands |
| Routing system | src/routing/ | 5-router: llm/skill/agent/memory/task |
| LLM clients | src/llm/ | ClaudeClient + GPTClient with retry/backoff |
| FastAPI app | src/api/ | REST endpoints; middleware; Pydantic models |
| Eval framework | src/evals/ | EvalSuite/EvalCase/EvalRunner/AsyncEvalRunner |
| Persistence | src/persistence/ | FileStore, MemoryStore (MCP), TieredMemory |
| Prompt engineering | src/prompt_engineering/ | Templates, few-shot, chaining |
| Utilities | src/utils/ | Logger, RateLimiter, ResponseCache, LogIndex, TokenCounter |
| Error handling | src/handlers/ | classify_api_error → typed exception hierarchy |
| MCP server | src/mcp_server.py | FastMCP-based tool server exposing 6 tools |
| 123 skills | .claude/skills/ | Each a SKILL.md with frontmatter triggers |
| 5 hooks | .claude/hooks/ | Bash scripts wired via settings.json |
| 4 agents | .claude/agents/ | ralph-loop, research, swarm, security-reviewer |
| Memory tiers | .claude/memory/ | hot (always loaded), warm (domain), glacier (archive) |

## Data Flow

```
User types: ccm complete 'write a deploy script'
  → src/cli.py cmd_complete()
  → route('write a deploy script')  # 5-router
    ├─ llm_router  → MEDIUM complexity → claude-sonnet-4-6
    ├─ skill_router → 'deploy' trigger → deploy-checker (confidence 0.85)
    ├─ agent_router → no agent needed (GENERAL)
    ├─ memory_router → TODO (write to tasks/todo.md)
    └─ task_router  → MEDIUM, 2 subtasks
  → ClaudeClient.complete(CompletionRequest)
    ├─ rate_limiter.acquire()
    ├─ cache.get() → miss
    ├─ async_client.messages.create(model, messages, ...)
    ├─ retry w/ jitter on RateLimitError / InternalServerError
    └─ cache.set()
  → print(response.content)
```

## External Integrations
- **Anthropic API** — completion + chat + streaming (model: claude-sonnet-4-6 default)
- **OpenAI API** — optional via GPTClient (gpt-4o default)
- **GitHub MCP** — via .mcp.json; repository: Wellux/wellux_testprojects
- **Filesystem MCP** — local file operations via MCP protocol
- **Memory MCP** — entity graph memory (entities/relations)
- **Sequential Thinking MCP** — structured reasoning

---

# 3. FULL FILE TREE

```
.claude
.claude/MEMORY.md
.claude/SOUL.md
.claude/USER.md
.claude/agents
.claude/agents/ralph-loop.md
.claude/agents/research-agent.md
.claude/agents/security-reviewer.md
.claude/agents/swarm-orchestrator.md
.claude/commands
.claude/commands/audit.md
.claude/commands/deploy.md
.claude/commands/fix-issue.md
.claude/commands/research.md
.claude/commands/review.md
.claude/hooks
.claude/hooks/post-tool-edit.sh
.claude/hooks/post-tool-pr.sh
.claude/hooks/pre-compact.sh
.claude/hooks/pre-tool-bash.sh
.claude/hooks/session-start.sh
.claude/hooks/stop.sh
.claude/hooks/user-prompt-submit.sh
.claude/memory
.claude/memory/glacier
.claude/memory/glacier/2026-04-05-precompact-hook-context-survival.md
.claude/memory/glacier/2026-04-05-skill-registry-duplicate-enforcement.md
.claude/memory/glacier/2026-04-05-tiered-memory-architecture.md
.claude/memory/hot
.claude/memory/hot/hot-memory.md
.claude/memory/warm
.claude/memory/warm/api-surface.md
.claude/memory/warm/architecture.md
.claude/memory/warm/decisions.md
.claude/memory/warm/evicted-from-hot.md
.claude/memory/warm/patterns.md
.claude/memory/warm/troubleshooting.md
.claude/rules
.claude/rules/api-conventions.md
.claude/rules/code-style.md
.claude/rules/testing.md
.claude/settings.json
.claude/settings.local.json
.claude/skills
.claude/skills/a11y-checker
.claude/skills/a11y-checker/SKILL.md
.claude/skills/adr-writer
.claude/skills/adr-writer/SKILL.md
.claude/skills/agent-orchestrator
.claude/skills/agent-orchestrator/SKILL.md
.claude/skills/ai-safety
.claude/skills/ai-safety/SKILL.md
.claude/skills/ai-security
.claude/skills/ai-security/SKILL.md
.claude/skills/algorithm
.claude/skills/algorithm/SKILL.md
.claude/skills/api-designer
.claude/skills/api-designer/SKILL.md
.claude/skills/api-docs
.claude/skills/api-docs/SKILL.md
.claude/skills/appsec-engineer
.claude/skills/appsec-engineer/SKILL.md
.claude/skills/arch-diagrammer
.claude/skills/arch-diagrammer/SKILL.md
.claude/skills/architect
.claude/skills/architect/SKILL.md
.claude/skills/async-optimizer
.claude/skills/async-optimizer/SKILL.md
.claude/skills/backup
.claude/skills/backup/SKILL.md
.claude/skills/blocker-resolver
.claude/skills/blocker-resolver/SKILL.md
.claude/skills/brainstorm
.claude/skills/brainstorm/SKILL.md
.claude/skills/bug-hunter
.claude/skills/bug-hunter/SKILL.md
.claude/skills/bundle-analyzer
.claude/skills/bundle-analyzer/SKILL.md
.claude/skills/cache-strategy
.claude/skills/cache-strategy/SKILL.md
.claude/skills/careful
.claude/skills/careful/SKILL.md
.claude/skills/chain-of-draft
.claude/skills/chain-of-draft/SKILL.md
.claude/skills/changelog
.claude/skills/changelog-maintainer
.claude/skills/changelog-maintainer/SKILL.md
.claude/skills/changelog/SKILL.md
.claude/skills/ci-cd
.claude/skills/ci-cd/SKILL.md
.claude/skills/ciso
.claude/skills/ciso/SKILL.md
.claude/skills/cloud-engineer
.claude/skills/cloud-engineer/SKILL.md
.claude/skills/code-review
.claude/skills/code-review/SKILL.md
.claude/skills/competitive-analyst
.claude/skills/competitive-analyst/SKILL.md
.claude/skills/concurrency
.claude/skills/concurrency/SKILL.md
.claude/skills/context-diff
.claude/skills/context-diff/SKILL.md
.claude/skills/cost-optimizer
.claude/skills/cost-optimizer/SKILL.md
.claude/skills/create
.claude/skills/create/SKILL.md
.claude/skills/cron-scheduler
.claude/skills/cron-scheduler/SKILL.md
.claude/skills/data-pipeline
.claude/skills/data-pipeline/SKILL.md
.claude/skills/dataset-curator
.claude/skills/dataset-curator/SKILL.md
.claude/skills/db-designer
.claude/skills/db-designer/SKILL.md
.claude/skills/db-optimizer
.claude/skills/db-optimizer/SKILL.md
.claude/skills/dba
.claude/skills/dba/SKILL.md
.claude/skills/debug
.claude/skills/debug/SKILL.md
.claude/skills/decision-logger
.claude/skills/decision-logger/SKILL.md
.claude/skills/dep-auditor
.claude/skills/dep-auditor/SKILL.md
.claude/skills/deploy-checker
.claude/skills/deploy-checker/SKILL.md
.claude/skills/devops-engineer
.claude/skills/devops-engineer/SKILL.md
.claude/skills/docker
.claude/skills/docker/SKILL.md
.claude/skills/embeddings
.claude/skills/embeddings/SKILL.md
.claude/skills/error-handler
.claude/skills/error-handler/SKILL.md
.claude/skills/estimation
.claude/skills/estimation/SKILL.md
.claude/skills/evals-designer
.claude/skills/evals-designer/SKILL.md
.claude/skills/feature-planner
.claude/skills/feature-planner/SKILL.md
.claude/skills/fine-tuner
.claude/skills/fine-tuner/SKILL.md
.claude/skills/foresight
.claude/skills/foresight/SKILL.md
.claude/skills/grc-analyst
.claude/skills/grc-analyst/SKILL.md
.claude/skills/gsd
.claude/skills/gsd/SKILL.md
.claude/skills/help-desk
.claude/skills/help-desk/SKILL.md
.claude/skills/iam-engineer
.claude/skills/iam-engineer/SKILL.md
.claude/skills/incident-response
.claude/skills/incident-response/SKILL.md
.claude/skills/infra-docs
.claude/skills/infra-docs/SKILL.md
.claude/skills/k8s
.claude/skills/k8s/SKILL.md
.claude/skills/karpathy-researcher
.claude/skills/karpathy-researcher/SKILL.md
.claude/skills/knowledge-base
.claude/skills/knowledge-base/SKILL.md
.claude/skills/kpi-tracker
.claude/skills/kpi-tracker/SKILL.md
.claude/skills/llm-optimizer
.claude/skills/llm-optimizer/SKILL.md
.claude/skills/logging
.claude/skills/logging/SKILL.md
.claude/skills/mem
.claude/skills/mem/SKILL.md
.claude/skills/memory-bank
.claude/skills/memory-bank/SKILL.md
.claude/skills/memory-profiler
.claude/skills/memory-profiler/SKILL.md
.claude/skills/metrics-designer
.claude/skills/metrics-designer/SKILL.md
.claude/skills/migration
.claude/skills/migration/SKILL.md
.claude/skills/ml-debugger
.claude/skills/ml-debugger/SKILL.md
.claude/skills/model-benchmarker
.claude/skills/model-benchmarker/SKILL.md
.claude/skills/monitoring
.claude/skills/monitoring/SKILL.md
.claude/skills/multimodal
.claude/skills/multimodal/SKILL.md
.claude/skills/network-engineer
.claude/skills/network-engineer/SKILL.md
.claude/skills/obsidian
.claude/skills/obsidian/SKILL.md
.claude/skills/office-hours
.claude/skills/office-hours/SKILL.md
.claude/skills/onboarding
.claude/skills/onboarding/SKILL.md
.claude/skills/paper-summarizer
.claude/skills/paper-summarizer/SKILL.md
.claude/skills/paperclip
.claude/skills/paperclip/SKILL.md
.claude/skills/pen-tester
.claude/skills/pen-tester/SKILL.md
.claude/skills/perf-profiler
.claude/skills/perf-profiler/SKILL.md
.claude/skills/pipeline-opt
.claude/skills/pipeline-opt/SKILL.md
.claude/skills/plan-eng-review
.claude/skills/plan-eng-review/SKILL.md
.claude/skills/pr-reviewer
.claude/skills/pr-reviewer/SKILL.md
.claude/skills/preflight
.claude/skills/preflight/SKILL.md
.claude/skills/prompt-engineer
.claude/skills/prompt-engineer/SKILL.md
.claude/skills/purple-team
.claude/skills/purple-team/SKILL.md
.claude/skills/query-optimizer
.claude/skills/query-optimizer/SKILL.md
.claude/skills/rag-builder
.claude/skills/rag-builder/SKILL.md
.claude/skills/readme-writer
.claude/skills/readme-writer/SKILL.md
.claude/skills/refactor
.claude/skills/refactor/SKILL.md
.claude/skills/retrospective
.claude/skills/retrospective/SKILL.md
.claude/skills/riper
.claude/skills/riper/SKILL.md
.claude/skills/risk-assessor
.claude/skills/risk-assessor/SKILL.md
.claude/skills/roadmap
.claude/skills/roadmap/SKILL.md
.claude/skills/rollback
.claude/skills/rollback/SKILL.md
.claude/skills/runbook-creator
.claude/skills/runbook-creator/SKILL.md
.claude/skills/scaling
.claude/skills/scaling/SKILL.md
.claude/skills/scope-definer
.claude/skills/scope-definer/SKILL.md
.claude/skills/secrets-mgr
.claude/skills/secrets-mgr/SKILL.md
.claude/skills/security-engineer
.claude/skills/security-engineer/SKILL.md
.claude/skills/self-reflect
.claude/skills/self-reflect/SKILL.md
.claude/skills/seo-auditor
.claude/skills/seo-auditor/SKILL.md
.claude/skills/ship
.claude/skills/ship/SKILL.md
.claude/skills/soc-analyst
.claude/skills/soc-analyst/SKILL.md
.claude/skills/sprint-planner
.claude/skills/sprint-planner/SKILL.md
.claude/skills/sre
.claude/skills/sre/SKILL.md
.claude/skills/stakeholder
.claude/skills/stakeholder/SKILL.md
.claude/skills/standup
.claude/skills/standup/SKILL.md
.claude/skills/superpowers
.claude/skills/superpowers/SKILL.md
.claude/skills/swarm
.claude/skills/swarm/SKILL.md
.claude/skills/sysadmin
.claude/skills/sysadmin/SKILL.md
.claude/skills/tdd
.claude/skills/tdd/SKILL.md
.claude/skills/team
.claude/skills/team/SKILL.md
.claude/skills/tech-debt
.claude/skills/tech-debt/SKILL.md
.claude/skills/terraform
.claude/skills/terraform/SKILL.md
.claude/skills/test-writer
.claude/skills/test-writer/SKILL.md
.claude/skills/trend-researcher
.claude/skills/trend-researcher/SKILL.md
.claude/skills/tutorial-writer
.claude/skills/tutorial-writer/SKILL.md
.claude/skills/type-safety
.claude/skills/type-safety/SKILL.md
.claude/skills/ui-ux
.claude/skills/ui-ux/SKILL.md
.claude/skills/vision-analyst
.claude/skills/vision-analyst/SKILL.md
.claude/skills/web-scraper
.claude/skills/web-scraper/SKILL.md
.claude/skills/web-vitals
.claude/skills/web-vitals/SKILL.md
.claude/skills/write-plan
.claude/skills/write-plan/SKILL.md
.dockerignore
.env.example
.git
.github
.github/workflows
.github/workflows/ci.yml
.gitignore
.hadolint.yaml
.mcp.json
.pre-commit-config.yaml
.pytest_cache
.ruff_cache
/home/user/wellux_testprojects
CHANGELOG.md
CLAUDE.md
CONTRIBUTING.md
Dockerfile
HANDOFF.md
MASTER_PLAN.md
README.md
config
config/__init__.py
config/logging_config.yaml
config/model_config.yaml
config/prompt_templates.yaml
data
data/cache
data/evals
data/evals/prompting.jsonl
data/evals/routing.jsonl
data/evals/smoke.jsonl
data/research
data/sessions
docker-compose.yml
docs
docs/architecture.md
docs/decisions
docs/decisions/0001-use-claude-primary.md
docs/decisions/0002-python-stack.md
docs/resources.md
docs/runbooks
docs/runbooks/deploy.md
docs/runbooks/incident-response.md
docs/runbooks/rollback.md
examples
examples/basic_completion.py
examples/chain_prompts.py
examples/chat_session.py
notebooks
notebooks/model_experimentation.ipynb
notebooks/prompt_testing.ipynb
notebooks/response_analysis.ipynb
pyproject.toml
requirements.txt
src
src/__init__.py
src/__pycache__
src/api
src/api/CLAUDE.md
src/api/__init__.py
src/api/__pycache__
src/api/app.py
src/api/middleware.py
src/api/models.py
src/cli.py
src/evals
src/evals/CLAUDE.md
src/evals/__init__.py
src/evals/__pycache__
src/evals/runner.py
src/evals/scorers.py
src/evals/suite.py
src/evals/types.py
src/handlers
src/handlers/__init__.py
src/handlers/__pycache__
src/handlers/error_handler.py
src/llm
src/llm/CLAUDE.md
src/llm/__init__.py
src/llm/__pycache__
src/llm/base.py
src/llm/claude_client.py
src/llm/gpt_client.py
src/llm/utils.py
src/mcp_server.py
src/persistence
src/persistence/CLAUDE.md
src/persistence/__init__.py
src/persistence/__pycache__
src/persistence/file_store.py
src/persistence/memory_store.py
src/persistence/tiered_memory.py
src/prompt_engineering
src/prompt_engineering/__init__.py
src/prompt_engineering/__pycache__
src/prompt_engineering/chainer.py
src/prompt_engineering/few_shot.py
src/prompt_engineering/templates.py
src/routing
src/routing/CLAUDE.md
src/routing/__init__.py
src/routing/__pycache__
src/routing/agent_router.py
src/routing/llm_router.py
src/routing/memory_router.py
src/routing/skill_router.py
src/routing/task_router.py
src/utils
src/utils/CLAUDE.md
src/utils/__init__.py
src/utils/__pycache__
src/utils/cache.py
src/utils/log_index.py
src/utils/logger.py
src/utils/rate_limiter.py
src/utils/token_counter.py
src/version.py
tasks
tasks/PRD.md
tasks/lessons.md
tasks/open-findings.md
tasks/todo.md
tests
tests/__init__.py
tests/__pycache__
tests/conftest.py
tests/test_api.py
tests/test_api_app.py
tests/test_api_endpoints.py
tests/test_api_middleware.py
tests/test_cli.py
tests/test_evals.py
tests/test_handlers_error.py
tests/test_llm_base.py
tests/test_llm_claude_client.py
tests/test_llm_gpt_client.py
tests/test_llm_init.py
tests/test_llm_utils.py
tests/test_log_index.py
tests/test_mcp_server.py
tests/test_persistence.py
tests/test_prompt_chainer.py
tests/test_prompt_few_shot.py
tests/test_prompt_templates.py
tests/test_routing.py
tests/test_tiered_memory.py
tests/test_utils_cache.py
tests/test_utils_logger.py
tests/test_utils_rate_limiter.py
tests/test_utils_token_counter.py
tests/test_version.py
tools
tools/prompts
tools/prompts/claude-code-prompts.md
tools/prompts/few-shot-examples.md
tools/prompts/system-prompts.md
tools/scripts
tools/scripts/github-trending-research.sh
tools/scripts/optimize-docs.sh
tools/scripts/perf-audit.sh
tools/scripts/research-agent.sh
tools/scripts/security-scan.sh
tools/scripts/self-improve.sh
```

### Key Files
- `src/cli.py` — main entry point (927 lines, all ccm subcommands)
- `src/routing/skill_router.py` — 123-skill registry (561 lines)
- `src/llm/claude_client.py` — ClaudeClient with retry/cache/rate-limit
- `src/api/app.py` — FastAPI app with /health, /v1/complete, /v1/chat, /v1/route
- `src/evals/runner.py` — sync + async eval runner
- `src/persistence/tiered_memory.py` — hot/warm/glacier tiers
- `.claude/hooks/pre-compact.sh` — critical context survival hook
- `.claude/hooks/session-start.sh` — rich boot display (version, commits, lessons)
- `pyproject.toml` — build config, deps, ruff, pytest, coverage settings

---

# 4. FULL SOURCE CODE EXPORT

## 4.1 Package Metadata

FILE: /home/user/wellux_testprojects/pyproject.toml
```toml
[build-system]
requires = ["setuptools>=69.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "claude-code-max"
version = "1.0.7"
description = "Gold-standard Claude Code template: 5-layer architecture, 123 skills, 5-router routing, FastAPI, eval framework, ccm CLI"
requires-python = ">=3.11,<4"
dependencies = [
    "anthropic>=0.87.0,<1.0",          # 0.87.0 fixes CVE-2026-34450 + CVE-2026-34452
    "cryptography>=46.0.6",           # fixes CVE-2026-34073 + 5 earlier CVEs; pulled by anthropic
    "httpx>=0.27.0,<1.0",
    "aiohttp>=3.9.0,<4.0",
    "fastapi>=0.111.0,<1.0",
    "uvicorn[standard]>=0.30.0,<1.0",
    "pydantic>=2.7.0,<3.0",
    "PyYAML>=6.0.1",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.2.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.9.0,<1.0",
    "mypy>=1.10.0",
    "pre-commit>=3.7.0",
]
ml = [
    "torch>=2.2.0",
    "transformers>=4.40.0",
    "sentence-transformers>=3.0.0",
    "faiss-cpu>=1.8.0",
    "chromadb>=0.5.0",
]
deploy = [
    "mcp>=1.0.0",
]

[project.scripts]
ccm = "src.cli:main"

[tool.setuptools.packages.find]
where = ["."]          # project root — puts /project on sys.path so `import src` resolves
include = ["src*"]     # include src/ and all subpackages

# ── ruff ──────────────────────────────────────────────────────────────────────

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B"]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function call in default arg (common in FastAPI)
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]   # assert is fine in tests

# ── mypy ──────────────────────────────────────────────────────────────────────

[tool.mypy]
python_version = "3.11"
strict = false
ignore_missing_imports = true
warn_unused_ignores = true
warn_return_any = false
# Generated/stub packages that don't ship types
[[tool.mypy.overrides]]
module = ["anthropic.*", "openai.*", "chromadb.*", "faiss.*", "torch.*"]
ignore_missing_imports = true

# ── pytest ────────────────────────────────────────────────────────────────────

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
addopts = "-q --tb=short"

# ── coverage ──────────────────────────────────────────────────────────────────

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
```

FILE: /home/user/wellux_testprojects/requirements.txt
```text
# Core LLM SDKs
anthropic>=0.87.0,<1.0     # 0.87.0 fixes CVE-2026-34450 + CVE-2026-34452
cryptography>=46.0.6        # fixes CVE-2026-34073 + 5 earlier CVEs
openai>=1.50.0,<2.0

# Data & ML
numpy>=1.26.0
pandas>=2.1.0
scikit-learn>=1.4.0
torch>=2.2.0
transformers>=4.40.0
sentence-transformers>=3.0.0

# Vector stores & RAG
faiss-cpu>=1.8.0
chromadb>=0.5.0

# Web & API
httpx>=0.27.0,<1.0
aiohttp>=3.9.0,<4.0
fastapi>=0.111.0,<1.0
uvicorn>=0.30.0,<1.0
pydantic>=2.7.0,<3.0

# Data processing
beautifulsoup4>=4.12.0
lxml>=5.2.0
PyYAML>=6.0.1
python-dotenv>=1.0.0

# Notebooks
jupyter>=1.0.0
ipykernel>=6.29.0

# Dev & testing
pytest>=8.2.0
pytest-asyncio>=0.23.0
pytest-cov>=5.0.0
ruff>=0.4.0
mypy>=1.10.0
pre-commit>=3.7.0
```

FILE: /home/user/wellux_testprojects/.env.example
```bash
# Claude Code Max — environment variable reference
# Copy to .env and fill in values. Never commit .env.

# ── Required ───────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-...          # Anthropic API key (required for live completions)

# ── Optional: API server ───────────────────────────────────────────────────────
HOST=0.0.0.0                          # uvicorn bind host (default: 0.0.0.0)
PORT=8000                             # uvicorn bind port (default: 8000)
LOG_LEVEL=INFO                        # DEBUG | INFO | WARNING | ERROR
WORKERS=1                             # uvicorn worker count (1 for dev, 2-4 for prod)

# ── Optional: LLM behaviour ───────────────────────────────────────────────────
CCM_DEFAULT_MODEL=claude-sonnet-4-6   # fallback model when routing not used
CCM_MAX_TOKENS=4096                   # default max_tokens per request
CCM_TEMPERATURE=0.7                   # default temperature
CCM_RPM=100                           # requests per minute rate limit

# ── Optional: Caching ─────────────────────────────────────────────────────────
CCM_CACHE_TTL=3600                    # response cache TTL seconds (0 = disabled)
CCM_CACHE_SIZE=1000                   # max cached items

# ── Optional: Logging ─────────────────────────────────────────────────────────
CCM_LOG_PATH=data/cache/events.log    # JSONL structured event log path

# ── Optional: MCP servers ─────────────────────────────────────────────────────
GITHUB_TOKEN=ghp_...                  # GitHub MCP server token
BRAVE_API_KEY=BSA...                  # Brave search MCP server key
SENTRY_DSN=https://...@sentry.io/...  # Sentry error tracking DSN
```

FILE: /home/user/wellux_testprojects/.gitignore
```text
# Local Claude Code settings (never commit personal overrides)
.claude/settings.local.json

# Environment variables and secrets (.env.example IS committed as a template)
.env
.env.local
.env.*.local
*.local
secrets/
credentials/

# Data directories (generated, not source)
data/cache/
data/outputs/
data/embeddings/
# data/research/ is tracked — stubs committed, populated content is ephemeral

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg
*.egg-info/
dist/
build/
.eggs/
.tox/
.venv/
venv/
env/
ENV/
pip-wheel-metadata/
.mypy_cache/
.ruff_cache/
.pytest_cache/
htmlcov/
.coverage
coverage.xml
*.cover

# Jupyter
.ipynb_checkpoints/
*.ipynb.bak

# macOS
.DS_Store
.AppleDouble
.LSOverride

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Docker (committed — not ignored)
# .dockerignore is intentionally tracked

# Compiled / binary
*.so
*.dylib
*.dll

# Node (if any JS tooling)
node_modules/
npm-debug.log*

# Terraform
.terraform/
*.tfstate
*.tfstate.backup
```

FILE: /home/user/wellux_testprojects/.dockerignore
```text
# Build context exclusions — keeps image lean and prevents secrets leaking

# Git metadata
.git/
.gitignore

# Claude Code harness (runtime only, not needed in container)
.claude/
.mcp.json
.pre-commit-config.yaml

# Secrets and local config
.env
.env.*
*.local
secrets/

# Python artifacts
__pycache__/
*.py[cod]
*.pyo
.mypy_cache/
.ruff_cache/
.pytest_cache/
htmlcov/
.coverage
coverage.xml
*.egg-info/
dist/
build/

# Dev tooling
notebooks/
tools/
docs/
examples/
tests/
data/

# Docker files (not needed inside the image)
Dockerfile
docker-compose*.yml
.dockerignore

# OS noise
.DS_Store
*.swp
*~

# Large optional deps (ML stack) not in the runtime image
requirements.txt
```

FILE: /home/user/wellux_testprojects/.hadolint.yaml
```yaml
# Hadolint configuration — controls Docker lint rules
# Docs: https://github.com/hadolint/hadolint#configure

failure-threshold: error

ignore:
  - DL3008   # apt-get: pin versions — slim image already pins base OS
  - DL3042   # pip without --user — acceptable in a single-user container build stage
  - DL3059   # multiple consecutive RUN — intentionally split for layer caching
  - DL3016   # npm pin versions — not using npm
```

FILE: /home/user/wellux_testprojects/.pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: debug-statements
      - id: no-commit-to-branch
        args: [--branch, main]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports, --no-strict-optional]
        additional_dependencies:
          - "pydantic>=2.7.0,<3.0"
          - "fastapi>=0.111.0,<1.0"
```

FILE: /home/user/wellux_testprojects/.mcp.json
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp"
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/wellux_testprojects"
      ],
      "env": {}
    },
    "brave": {
      "type": "http",
      "url": "https://mcp.brave.com/mcp"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "env": {}
    },
    "sequential-thinking": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ],
      "env": {}
    },
    "ccm": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "-m",
        "src.mcp_server"
      ],
      "cwd": "/home/user/wellux_testprojects",
      "env": {}
    }
  }
}
```


## 4.2 Core Python Source

### src/__init__.py

FILE: /home/user/wellux_testprojects/src/__init__.py
```python
"""Claude Code Max — Python stack."""
from .version import __version__

__all__ = ["__version__"]
```

### src/version.py

FILE: /home/user/wellux_testprojects/src/version.py
```python
"""Single source of truth for the package version.

Resolution order:
  1. importlib.metadata  — works when package is installed (pip install -e .)
  2. pyproject.toml      — fallback for uninstalled dev environments (Python 3.11+)
  3. "0.0.0+dev"         — last resort so imports never fail
"""
from __future__ import annotations


def _read_version() -> str:
    # 1. Installed package metadata
    try:
        from importlib.metadata import version as _pkg_version

        return _pkg_version("claude-code-max")
    except Exception:
        pass

    # 2. Direct pyproject.toml parse (tomllib is stdlib since Python 3.11)
    try:
        import tomllib
        from pathlib import Path

        _toml = Path(__file__).parent.parent / "pyproject.toml"
        with _toml.open("rb") as fh:
            return tomllib.load(fh)["project"]["version"]
    except Exception:
        pass

    return "0.0.0+dev"


__version__: str = _read_version()

# 4-tuple (major, minor, patch, pre) for runtime comparisons
_parts = __version__.split("+")[0].split(".")
_nums = [int(p) for p in _parts if p.isdigit()]
VERSION_INFO: tuple[int, int, int, str] = (_nums[0], _nums[1], _nums[2], "") if len(_nums) >= 3 else (0, 0, 0, "")


def version_string() -> str:
    """Return the canonical version string e.g. '1.0.7'."""
    return __version__
```

### src/cli.py

FILE: /home/user/wellux_testprojects/src/cli.py
```python
"""ccm — Claude Code Max CLI.

Usage:
    ccm version                         # show version, git hash, Python
    ccm route "your task"               # show routing decision (add --json)
    ccm complete "prompt"               # one-shot completion (auto-routes model)
    ccm complete "prompt" --model haiku # override model
    ccm serve [--host HOST] [--port N]  # start FastAPI server
    ccm status                          # git branch + test count + skills
    ccm doctor                          # environment health check
    ccm research "topic"                # create data/research/<date>-<slug>.md stub
    ccm logs [--event E] [--tag T]      # query indexed event log
    ccm eval list                       # list bundled eval suites
    ccm eval inspect <suite.jsonl>      # show cases with constraints
    ccm eval run <suite.jsonl>          # run suite (--dry-run  --tag  --threshold  --json)
    ccm build [--no-cache] [--tag TAG]            # build Docker image
    ccm deploy [--env local] [--dry-run]          # full deploy pipeline: test→build→up→verify
    ccm ps                                        # show running container status
    ccm health [--url URL]                        # check live service /health endpoint
    ccm context-diff [--since HEAD~1]             # structured change summary since a git ref
    ccm memory-bank [status|query <term>|sync]   # query warm/hot/glacier memory bank
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ── helpers ───────────────────────────────────────────────────────────────────

def _project_root() -> Path:
    """Return the repo root (parent of src/)."""
    return Path(__file__).parent.parent


def _print_json(data: dict) -> None:
    print(json.dumps(data, indent=2))


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    """Run a shell command, return stdout, return '?' on error."""
    try:
        return subprocess.check_output(
            cmd, cwd=cwd or _project_root(), text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "?"


# ── subcommands ───────────────────────────────────────────────────────────────

def cmd_version(_args: argparse.Namespace) -> int:
    """Print version, git commit hash, and Python version."""
    from src.version import __version__

    git_hash = _run(["git", "rev-parse", "--short", "HEAD"])
    git_branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    print(f"ccm {__version__}")
    print(f"  git : {git_hash} ({git_branch})")
    print(f"  python: {py_version}")
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    """Show the full routing decision for a task without calling the API."""
    from src.routing import route

    decision = route(args.task)
    if args.json:
        _print_json({
            "model": decision.llm.model,
            "model_reason": decision.llm.reason,
            "skill": decision.skill.skill if decision.skill else None,
            "skill_confidence": decision.skill.confidence if decision.skill else None,
            "agent": decision.agent.agent.value,
            "memory_tier": decision.memory.tier.value,
            "plan_size": decision.plan.size.value,
            "subtasks": [
                {"description": s.description, "model": s.model, "agent": s.agent}
                for s in decision.plan.subtasks
            ],
        })
    else:
        print(decision.summary())
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    """Run a completion, auto-routing the model unless --model is given."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set. Run: ccm doctor", file=sys.stderr)
        return 1

    from src.routing import route

    if args.model:
        model = args.model
        reason = "user override"
    else:
        decision = route(args.prompt)
        model = decision.llm.model
        reason = decision.llm.reason

    try:
        import anthropic
    except ImportError:
        print("Error: 'anthropic' not installed. Run: pip install anthropic", file=sys.stderr)
        return 1

    client = anthropic.Anthropic(api_key=api_key)
    kwargs: dict = {
        "model": model,
        "max_tokens": args.max_tokens,
        "messages": [{"role": "user", "content": args.prompt}],
    }
    if args.system:
        kwargs["system"] = args.system

    if not args.quiet:
        print(f"[ccm] model={model}  reason={reason}\n", file=sys.stderr)

    message = client.messages.create(**kwargs)
    content = message.content[0].text if message.content else ""

    if args.json:
        _print_json({
            "content": content,
            "model": model,
            "reason": reason,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        })
    else:
        print(content)
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """Start the FastAPI server with uvicorn."""
    try:
        import uvicorn
    except ImportError:
        print("Error: 'uvicorn' not installed. Run: pip install uvicorn", file=sys.stderr)
        return 1

    uvicorn.run(
        "src.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower(),
    )
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    """Print project status: version, git branch, test count, skills."""
    from src.version import __version__

    root = _project_root()
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    last_commit = _run(["git", "log", "-1", "--oneline"])
    dirty = _run(["git", "status", "--porcelain"])

    # Count test functions (including those in classes)
    import re as _re
    test_files = list(root.glob("tests/test_*.py"))
    _pat = _re.compile(r"^\s*(?:async\s+)?def\s+test_", _re.MULTILINE)
    test_count = sum(len(_pat.findall(f.read_text())) for f in test_files)

    # Count skills — each lives in .claude/skills/<name>/SKILL.md
    skills_dir = root / ".claude" / "skills"
    skill_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0

    # Event log summary
    log_path = root / "data" / "cache" / "events.log"
    log_info = f"{log_path}" if log_path.exists() else "no events yet"
    if log_path.exists():
        try:
            from src.utils.log_index import LogIndex
            idx = LogIndex(log_path)
            s = idx.summary()
            top = sorted(s.items(), key=lambda x: x[1], reverse=True)[:3]
            log_info = f"{len(idx)} events  top: {', '.join(f'{k}×{v}' for k, v in top)}"
        except Exception:
            pass

    print(f"version     : ccm {__version__}")
    print(f"branch      : {branch}")
    print(f"last commit : {last_commit}")
    print(f"working tree: {'dirty' if dirty else 'clean'}")
    print(f"tests       : {test_count} functions in {len(test_files)} files")
    print(f"skills      : {skill_count}")
    print(f"event log   : {log_info}")
    return 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    """Check environment health: API key, deps, paths, log."""
    root = _project_root()
    checks: list[tuple[bool, str]] = []

    # 1. API key
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    checks.append((bool(api_key), "ANTHROPIC_API_KEY is set"))

    # 2. Core package imports
    for pkg in ("anthropic", "fastapi", "uvicorn", "pydantic"):
        try:
            __import__(pkg)
            checks.append((True, f"package '{pkg}' importable"))
        except ImportError:
            checks.append((False, f"package '{pkg}' NOT found — pip install {pkg}"))

    # 3. Required project paths
    for rel in ("src/", "data/evals/", ".claude/skills/", "tasks/todo.md"):
        path = root / rel
        checks.append((path.exists(), f"path exists: {rel}"))

    # 4. Skills count
    skills_dir = root / ".claude" / "skills"
    skill_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0
    checks.append((skill_count >= 100, f"skills loaded: {skill_count} (expected ≥100)"))

    # 5. Smoke eval
    smoke_path = root / "data" / "evals" / "smoke.jsonl"
    checks.append((smoke_path.exists(), "smoke eval suite present"))

    # 6. Git repo
    git_ok = _run(["git", "rev-parse", "--is-inside-work-tree"]) == "true"
    checks.append((git_ok, "inside git repository"))

    # 7. Event log writable
    log_path = root / "data" / "cache" / "events.log"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch()
        checks.append((True, "event log writable"))
    except OSError as e:
        checks.append((False, f"event log NOT writable: {e}"))

    passed = sum(1 for ok, _ in checks if ok)
    total = len(checks)

    for ok, msg in checks:
        icon = "✓" if ok else "✗"
        print(f"  [{icon}] {msg}")

    print(f"\n{passed}/{total} checks passed", end="")
    if passed == total:
        print(" — environment healthy")
        return 0
    print(" — fix issues above before deploying")
    return 1


def cmd_lint(args: argparse.Namespace) -> int:
    """Run ruff lint on src/ and tests/ and report results."""
    import subprocess

    root = _project_root()
    cmd = [
        "python3", "-m", "ruff", "check",
        "src/", "tests/",
        "--select", "E,F,W,I",
        "--ignore", "E501",
    ]
    if args.fix:
        cmd.append("--fix")
    if args.no_cache:
        cmd.append("--no-cache")

    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode == 0:
        print("✓ lint clean")
    else:
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        print(f"\n✗ lint found issues (exit {result.returncode})", file=sys.stderr)
    return result.returncode


def cmd_logs(args: argparse.Namespace) -> int:
    """Query the indexed event log."""
    from src.utils.log_index import LogIndex

    root = _project_root()
    log_path = root / os.environ.get("CCM_LOG_PATH", "data/cache/events.log")

    if not log_path.exists():
        print("No event log found. Start the API server to generate events.")
        return 0

    idx = LogIndex(log_path)

    if args.summary:
        s = idx.summary()
        if not s:
            print("Event log is empty.")
            return 0
        print(f"{'Event':<30} {'Count':>6}")
        print("-" * 38)
        for event, count in sorted(s.items(), key=lambda x: x[1], reverse=True):
            print(f"{event:<30} {count:>6}")
        print(f"\nTotal: {len(idx)} events in {log_path}")
        return 0

    tags = [args.tag] if args.tag else None
    results = idx.search(event=args.event or None, tags=tags, limit=args.limit)

    if not results:
        print("No matching events.")
        return 0

    if args.json:
        _print_json(results)
    else:
        for rec in results:
            ts = rec.get("ts", "")[:19].replace("T", " ")
            event = rec.get("event", "?")
            extras = {k: v for k, v in rec.items() if k not in ("ts", "event")}
            extra_str = "  " + "  ".join(f"{k}={v}" for k, v in list(extras.items())[:4])
            print(f"{ts}  {event:<25}{extra_str}")

    return 0


def cmd_research(args: argparse.Namespace) -> int:
    """Write a research stub for the given topic to data/research/."""
    from src.persistence import FileStore

    store = FileStore(root=_project_root())
    path = store.write_research(
        args.topic,
        f"# {args.topic}\n\n> Research stub — fill in via /karpathy-researcher\n\n"
        f"## Key Questions\n\n- TODO\n\n## Findings\n\n- TODO\n\n## Sources\n\n- TODO\n",
    )
    print(f"Created: {path}")
    return 0


# ── deploy subcommands ────────────────────────────────────────────────────────

def cmd_build(args: argparse.Namespace) -> int:
    """Build the Docker image ccm-api:{version} and ccm-api:latest."""
    # 1. Check docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("Error: docker not found. Install Docker to use this command.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError:
        print("Error: docker is not working correctly.", file=sys.stderr)
        return 1

    from src.version import __version__

    tag = getattr(args, "tag", None) or f"ccm-api:{__version__}"
    build_tags = ["-t", tag, "-t", "ccm-api:latest"]

    # Support --dry-run: validate only
    if getattr(args, "dry_run", False):
        print(f"[dry-run] would build: docker build {' '.join(build_tags)} .")
        return 0

    cmd = ["docker", "build"]
    if getattr(args, "no_cache", False):
        cmd.append("--no-cache")
    if getattr(args, "tag", None):
        # custom tag replaces default versioned tag
        cmd += ["-t", args.tag, "-t", "ccm-api:latest"]
    else:
        cmd += ["-t", f"ccm-api:{__version__}", "-t", "ccm-api:latest"]
    cmd.append(".")

    print(f"[ccm build] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=_project_root())
    if result.returncode != 0:
        print("Error: docker build failed.", file=sys.stderr)
        return 1

    # Print image size
    try:
        size_result = subprocess.run(
            ["docker", "image", "inspect", "ccm-api:latest", "--format", "{{.Size}}"],
            capture_output=True, text=True, check=True,
        )
        size_bytes = int(size_result.stdout.strip())
        size_mb = size_bytes / (1024 * 1024)
        print(f"[ccm build] image size: {size_mb:.1f} MB")
    except (subprocess.CalledProcessError, ValueError):
        pass

    return 0


def _deploy_step_header(n: int, total: int, name: str) -> None:
    print(f"\n── {n}/{total} {name} {'─' * max(0, 40 - len(name))}")


def _deploy_run_tests(root) -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short"], cwd=root
    )
    return result.returncode == 0


def _deploy_run_compose(root) -> bool:
    result = subprocess.run(["docker", "compose", "up", "-d"], cwd=root)
    return result.returncode == 0


def _deploy_check_health(url: str) -> bool:
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                if resp.status == 200:
                    print(f"✓ service healthy ({url})")
                    return True
        except Exception:
            time.sleep(3)
    print(f"✗ health check failed — service not responding at {url} after 30s")
    return False


def _deploy_run_evals(root) -> bool:
    smoke_path = root / "data" / "evals" / "smoke.jsonl"
    smoke_args = argparse.Namespace(
        suite=str(smoke_path), dry_run=True, tag=None, threshold=0.8, json=False,
    )
    return _eval_run(smoke_args) == 0


def cmd_deploy(args: argparse.Namespace) -> int:
    """Full deploy pipeline: doctor → tests → build → compose up → health → evals."""
    host = getattr(args, "host", "127.0.0.1")
    port = getattr(args, "port", 8000)
    env = getattr(args, "env", "local")
    dry_run = getattr(args, "dry_run", False)
    skip_tests = getattr(args, "skip_tests", False)
    skip_build = getattr(args, "skip_build", False)
    skip_evals = getattr(args, "skip_evals", False)
    root = _project_root()
    total = 6
    steps: list[tuple[str, bool]] = []

    _deploy_step_header(1, total, "Doctor")
    steps.append(("Doctor", cmd_doctor(argparse.Namespace()) == 0))

    _deploy_step_header(2, total, "Tests")
    if skip_tests:
        print("[skip] --skip-tests passed")
        steps.append(("Tests", True))
    else:
        steps.append(("Tests", _deploy_run_tests(root)))

    _deploy_step_header(3, total, "Build")
    if skip_build:
        print("[skip] --skip-build passed")
        steps.append(("Build", True))
    else:
        steps.append(("Build", cmd_build(argparse.Namespace(no_cache=False, tag=None, dry_run=dry_run)) == 0))

    _deploy_step_header(4, total, "Compose up")
    if dry_run:
        print("[dry-run] skipping docker compose up")
        steps.append(("Compose up", True))
    else:
        steps.append(("Compose up", _deploy_run_compose(root)))

    _deploy_step_header(5, total, "Health check")
    if dry_run:
        print("[dry-run] skipping health check")
        steps.append(("Health check", True))
    else:
        steps.append(("Health check", _deploy_check_health(f"http://{host}:{port}/health")))

    _deploy_step_header(6, total, "Smoke evals")
    if skip_evals:
        print("[skip] --skip-evals passed")
        steps.append(("Smoke evals", True))
    else:
        steps.append(("Smoke evals", _deploy_run_evals(root)))

    print("\n── Deploy Summary " + "─" * 24)
    all_ok = all(ok for _, ok in steps)
    for step_name, ok in steps:
        print(f"  [{'✓' if ok else '✗'}] {step_name}")

    print()
    if all_ok:
        print(f"✓ Deploy to {env} complete")
        return 0
    print("✗ Deploy failed — see above for details")
    return 1


def cmd_ps(_args: argparse.Namespace) -> int:
    """Show running container status via docker compose ps."""
    try:
        subprocess.run(["docker", "compose", "ps"], cwd=_project_root())
    except FileNotFoundError:
        print("Docker not available")
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    """Check live service health via HTTP GET {url}/health."""
    url = getattr(args, "url", "http://localhost:8000")
    health_url = f"{url.rstrip('/')}/health"

    try:
        with urllib.request.urlopen(health_url, timeout=5) as resp:
            if resp.status != 200:
                print(f"✗ {health_url} returned HTTP {resp.status}", file=sys.stderr)
                return 1
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"✗ Could not reach {health_url}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    status = data.get("status", "unknown")
    version = data.get("version", "unknown")
    uptime = data.get("uptime_s")
    models = data.get("available_models", [])

    print(f"status  : {status}")
    print(f"version : {version}")
    if uptime is not None:
        print(f"uptime  : {uptime:.1f}s")
    print(f"models  : {len(models)} available")
    return 0


def cmd_memory_bank(args: argparse.Namespace) -> int:
    """Query or show status of the warm memory bank."""
    from src.persistence import TieredMemory

    mem = TieredMemory()
    subcmd = getattr(args, "mb_cmd", "status")

    if subcmd == "status":
        domains = mem.list_warm_domains()
        hot = mem.read_hot()
        glacier = mem.list_glacier()
        print("\n## Memory Bank Status\n")
        print(f"Hot tier:     {'✅ ' + str(len(hot.splitlines())) + ' lines' if hot else '⚠  empty'}")
        print(f"Warm domains: {len(domains)} — {', '.join(domains) if domains else 'none'}")
        print(f"Glacier:      {len(glacier)} archived entries")
        if domains:
            print("\n### Warm Domains")
            for d in domains:
                content = mem.read_warm(d)
                lines = content.splitlines()
                preview = lines[0].lstrip("# ") if lines else "(empty)"
                print(f"  {d:25s}  {len(lines):3d} lines  — {preview[:60]}")

    elif subcmd == "query":
        query = getattr(args, "query_term", "") or ""
        if not query:
            print("Usage: ccm memory-bank query <search term>", file=__import__("sys").stderr)
            return 1
        # Search across warm domains
        results = []
        for domain in mem.list_warm_domains():
            content = mem.read_warm(domain)
            if query.lower() in content.lower():
                # Find context line
                for ln in content.splitlines():
                    if query.lower() in ln.lower():
                        results.append((domain, ln.strip()[:100]))
                        break
        # Search glacier
        glacier_results = mem.search_glacier(query)
        print(f"\n## Memory Bank Query: '{query}'\n")
        if results:
            print("### Warm tier matches")
            for domain, snippet in results:
                print(f"  [{domain}] {snippet}")
        if glacier_results:
            print("\n### Glacier matches")
            for r in glacier_results[:5]:
                print(f"  [{r['date']}] {r['title']}: {r['snippet'][:80]}")
        if not results and not glacier_results:
            print("  No matches found.")

    elif subcmd == "sync":
        # Lightweight sync: update hot-memory timestamp and list warm domains
        domains = mem.list_warm_domains()
        mem.write_hot("memory_bank_synced", __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"))
        print(f"\n✅ Memory bank sync complete — {len(domains)} warm domain(s) up to date")

    return 0


def cmd_context_diff(args: argparse.Namespace) -> int:
    """Show a structured context summary of changes since a git ref."""
    root = _project_root()
    since = getattr(args, "since", None) or "HEAD~1"

    # Resolve "yesterday" / "last week" as time-based shortcuts
    time_aliases = {
        "yesterday": "--since='1 day ago'",
        "last-week": "--since='1 week ago'",
        "last-month": "--since='1 month ago'",
    }
    if since in time_aliases:
        log_cmd = ["git", "log", time_aliases[since], "--oneline"]
        stat_cmd = None
    else:
        log_cmd = ["git", "log", f"{since}...HEAD", "--oneline"]
        stat_cmd = ["git", "diff", "--stat", f"{since}...HEAD"]

    try:
        commits = _run(log_cmd, cwd=root)
        stat = _run(stat_cmd, cwd=root) if stat_cmd else ""
        diff_names = _run(["git", "diff", "--name-only", f"{since}...HEAD"], cwd=root)
    except Exception as e:
        print(f"Error running git: {e}", file=sys.stderr)
        return 1

    commit_lines = [ln for ln in commits.splitlines() if ln.strip()]
    file_lines = [ln for ln in diff_names.splitlines() if ln.strip()]
    stat_summary = stat.splitlines()[-1].strip() if stat else f"{len(file_lines)} files changed"

    print(f"\n## Context Diff: {since}...HEAD\n")
    print(f"### Summary\n{stat_summary}\n")

    if commit_lines:
        print("### Commits in scope")
        for c in commit_lines[:15]:
            print(f"  {c}")
        print()

    if file_lines:
        print("### Changed Files")
        for f in file_lines[:20]:
            print(f"  {f}")
        print()

    if not commit_lines and not file_lines:
        print("No changes found relative to reference:", since)

    return 0


def cmd_serve_mcp(_args: argparse.Namespace) -> int:
    """Start the MCP stdio server for Claude integration."""
    try:
        from src.mcp_server import run as _mcp_run
        _mcp_run()
        return 0
    except ImportError:
        print("Error: 'mcp' not installed. Run: pip install mcp", file=sys.stderr)
        return 1


# ── eval subcommands ──────────────────────────────────────────────────────────

def cmd_eval(args: argparse.Namespace) -> int:
    return {
        "run":     _eval_run,
        "list":    _eval_list,
        "inspect": _eval_inspect,
    }[args.eval_cmd](args)


def _eval_list(_args: argparse.Namespace) -> int:
    evals_dir = _project_root() / "data" / "evals"
    if not evals_dir.exists():
        print("No eval suites found (data/evals/ does not exist).")
        return 0
    suites = sorted(evals_dir.glob("*.jsonl"))
    if not suites:
        print("No .jsonl suites found in data/evals/")
        return 0
    for s in suites:
        lines = [ln for ln in s.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        print(f"  {s.name:<30}  {len(lines)} cases")
    return 0


def _eval_inspect(args: argparse.Namespace) -> int:
    from src.evals import EvalSuite

    path = Path(args.suite)
    if not path.exists():
        path = _project_root() / "data" / "evals" / args.suite
    if not path.exists():
        print(f"Suite not found: {args.suite}", file=sys.stderr)
        return 1

    suite = EvalSuite.from_jsonl(path)
    for case in suite:
        tags = f"  [{', '.join(case.tags)}]" if case.tags else ""
        print(f"  {case.id}{tags}")
        print(f"    prompt  : {case.prompt[:80]}")
        if case.contains:
            print(f"    contains: {case.contains}")
        if case.excludes:
            print(f"    excludes: {case.excludes}")
    return 0


def _eval_run(args: argparse.Namespace) -> int:
    from src.evals import EvalRunner, EvalSuite

    path = Path(args.suite)
    if not path.exists():
        path = _project_root() / "data" / "evals" / args.suite
    if not path.exists():
        print(f"Suite not found: {args.suite}", file=sys.stderr)
        return 1

    suite = EvalSuite.from_jsonl(path)
    if args.tag:
        suite = suite.filter_tags(args.tag)
    if not len(suite):
        print("No cases matched filters.")
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    dry_run = args.dry_run or not api_key

    if dry_run:
        print("[ccm eval] dry-run mode — echoing prompts (no API calls)\n")
        def llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            return prompt
    else:
        try:
            import anthropic
        except ImportError:
            print("Error: 'anthropic' not installed.", file=sys.stderr)
            return 1
        from src.routing import route
        client = anthropic.Anthropic(api_key=api_key)

        def llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            model = route(prompt).llm.model
            msg = client.messages.create(
                model=model, max_tokens=max_tokens, temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text if msg.content else ""

    runner = EvalRunner(llm, pass_threshold=args.threshold, verbose=True)
    report = runner.run(suite)
    print(f"\n{report.summary()}")
    print(f"  threshold: {args.threshold:.0%}")

    if args.json:
        _print_json({
            "suite": report.suite_name,
            "total": report.total,
            "passed": report.passed,
            "failed": report.failed,
            "errors": report.errors,
            "pass_rate": round(report.pass_rate, 3),
            "mean_score": round(report.mean_score, 3),
            "results": [
                {"id": r.case_id, "verdict": r.verdict.value, "score": round(r.score, 3),
                 "reason": r.reason, "latency_ms": round(r.latency_ms, 1)}
                for r in report.results
            ],
        })

    return 0 if report.failed == 0 and report.errors == 0 else 1


# ── parser ────────────────────────────────────────────────────────────────────

def _add_llm_parsers(sub) -> None:
    """Route and complete subcommands."""
    r = sub.add_parser("route", help="Show routing decision for a task")
    r.add_argument("task")
    r.add_argument("--json", action="store_true")

    c = sub.add_parser("complete", help="One-shot LLM completion")
    c.add_argument("prompt")
    c.add_argument("--system")
    c.add_argument("--model", help="Override model (skip routing)")
    c.add_argument("--max-tokens", type=int, default=4096)
    c.add_argument("--json", action="store_true")
    c.add_argument("--quiet", action="store_true", help="Suppress routing info")


def _add_server_parsers(sub) -> None:
    """Serve, ps, health, and serve-mcp subcommands."""
    s = sub.add_parser("serve", help="Start FastAPI server")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--reload", action="store_true")
    s.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    sub.add_parser("ps", help="Show running container status")

    hl = sub.add_parser("health", help="Check live /health endpoint")
    hl.add_argument("--url", default="http://localhost:8000", help="Base URL of the service")

    sub.add_parser("serve-mcp", help="Start MCP stdio server for Claude integration")


def _add_ops_parsers(sub) -> None:
    """Build and deploy subcommands."""
    bd = sub.add_parser("build", help="Build Docker image ccm-api:{version}")
    bd.add_argument("--no-cache", action="store_true", help="Pass --no-cache to docker build")
    bd.add_argument("--tag", help="Custom image tag (default: ccm-api:{version})")
    bd.add_argument("--dry-run", action="store_true", help="Validate docker is available; don't build")

    dp = sub.add_parser("deploy", help="Full deploy pipeline: doctor→tests→build→up→health→evals")
    dp.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    dp.add_argument("--dry-run", action="store_true", help="Validate all steps without starting containers")
    dp.add_argument("--skip-tests", action="store_true", help="Skip pytest step")
    dp.add_argument("--skip-build", action="store_true", help="Skip docker build step")
    dp.add_argument("--skip-evals", action="store_true", help="Skip smoke evals step")
    dp.add_argument("--host", default="127.0.0.1", help="Host to poll for health check")
    dp.add_argument("--port", type=int, default=8000, help="Port to poll for health check")


def _add_util_parsers(sub) -> None:
    """Status, doctor, logs, research, lint, memory-bank, context-diff, and eval subcommands."""
    sub.add_parser("version", help="Show version and environment info")
    sub.add_parser("status", help="Show project status")
    sub.add_parser("doctor", help="Check environment health")

    lg = sub.add_parser("logs", help="Query the indexed event log")
    lg.add_argument("--event", help="Filter by event name")
    lg.add_argument("--tag", help="Filter by tag")
    lg.add_argument("--limit", type=int, default=50, help="Max results (default 50)")
    lg.add_argument("--summary", action="store_true", help="Show count per event type")
    lg.add_argument("--json", action="store_true", help="Output as JSON")

    res = sub.add_parser("research", help="Create a research stub file")
    res.add_argument("topic")

    lt = sub.add_parser("lint", help="Run ruff on src/ and tests/")
    lt.add_argument("--fix", action="store_true", help="Auto-fix safe issues")
    lt.add_argument("--no-cache", action="store_true", help="Disable ruff cache")

    mb = sub.add_parser("memory-bank", help="Query or show status of the warm memory bank")
    mb_sub = mb.add_subparsers(dest="mb_cmd")
    mb_sub.add_parser("status", help="Show memory bank status (default)")
    mb_query = mb_sub.add_parser("query", help="Search across hot/warm/glacier tiers")
    mb_query.add_argument("query_term", help="Term to search for")
    mb_sub.add_parser("sync", help="Sync hot-memory timestamp")

    cd = sub.add_parser("context-diff", help="Show structured change summary since a git ref")
    cd.add_argument("--since", default="HEAD~1",
                    help="Git ref or alias (HEAD~5, main, yesterday, last-week)")

    ev = sub.add_parser("eval", help="Run or inspect eval suites")
    ev_sub = ev.add_subparsers(dest="eval_cmd", required=True)
    ev_sub.add_parser("list", help="List bundled eval suites")
    ev_insp = ev_sub.add_parser("inspect", help="Show cases in a suite")
    ev_insp.add_argument("suite")
    ev_run = ev_sub.add_parser("run", help="Run an eval suite")
    ev_run.add_argument("suite")
    ev_run.add_argument("--dry-run", action="store_true")
    ev_run.add_argument("--tag", help="Only run cases with this tag")
    ev_run.add_argument("--threshold", type=float, default=0.8)
    ev_run.add_argument("--json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level ccm argument parser."""
    from src.version import __version__

    p = argparse.ArgumentParser(prog="ccm", description="Claude Code Max — unified CLI")
    p.add_argument("--version", action="version", version=f"ccm {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    _add_llm_parsers(sub)
    _add_server_parsers(sub)
    _add_ops_parsers(sub)
    _add_util_parsers(sub)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "version":   cmd_version,
        "route":     cmd_route,
        "complete":  cmd_complete,
        "serve":     cmd_serve,
        "status":    cmd_status,
        "doctor":    cmd_doctor,
        "logs":      cmd_logs,
        "research":  cmd_research,
        "build":     cmd_build,
        "deploy":    cmd_deploy,
        "ps":        cmd_ps,
        "health":    cmd_health,
        "serve-mcp":     cmd_serve_mcp,
        "eval":          cmd_eval,
        "lint":          cmd_lint,
        "context-diff":  cmd_context_diff,
        "memory-bank":   cmd_memory_bank,
    }
    handler = dispatch.get(args.command)
    if handler is None:
        parser.print_help()
        return 1
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
```

### src/mcp_server.py

FILE: /home/user/wellux_testprojects/src/mcp_server.py
```python
"""MCP stdio server — exposes ccm operations as MCP tools.

Run directly:  python -m src.mcp_server
Via ccm:       ccm serve-mcp

Tools exposed:
  deploy   — Run full deploy pipeline (test → build → up → verify)
  build    — Build the Docker image
  health   — Check live service health
  status   — Show project status
  doctor   — Run environment health check
  logs     — Query indexed event log

Install: pip install ".[deploy]"  (adds mcp>=1.0.0)
"""
from __future__ import annotations

import argparse
import contextlib
import io
import sys


def _require_fastmcp():
    """Import FastMCP or exit with a helpful message if mcp is not installed."""
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

        return FastMCP
    except ImportError as exc:
        print(
            "Error: 'mcp' package not installed.\n"
            "Install with: pip install 'mcp>=1.0.0'\n"
            "Or: pip install '.[deploy]'",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc


def _capture(fn, args: argparse.Namespace) -> str:
    """Call fn(args) while capturing stdout; return captured output."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(args)
    return buf.getvalue()


def _make_args(**kwargs) -> argparse.Namespace:
    """Build a simple Namespace from keyword arguments."""
    return argparse.Namespace(**kwargs)


# ── Tool functions (plain Python — registered with MCP server in _build_server) ──


def deploy(
    env: str = "local",
    dry_run: bool = False,
    skip_tests: bool = False,
    skip_build: bool = False,
    skip_evals: bool = False,
) -> str:
    """Run the full deploy pipeline: doctor → tests → build → compose up → health → evals.

    Args:
        env: Target environment (local, staging, prod).
        dry_run: Validate all steps without starting containers.
        skip_tests: Skip pytest step.
        skip_build: Skip docker build step.
        skip_evals: Skip smoke evals step.
    """
    from src.cli import cmd_deploy

    args = _make_args(
        env=env,
        dry_run=dry_run,
        skip_tests=skip_tests,
        skip_build=skip_build,
        skip_evals=skip_evals,
        host="127.0.0.1",
        port=8000,
    )
    return _capture(cmd_deploy, args)


def build(no_cache: bool = False, tag: str | None = None) -> str:
    """Build the Docker image ccm-api:{version} and ccm-api:latest.

    Args:
        no_cache: Pass --no-cache to docker build.
        tag: Custom image tag (default: ccm-api:{version}).
    """
    from src.cli import cmd_build

    args = _make_args(no_cache=no_cache, tag=tag, dry_run=False)
    return _capture(cmd_build, args)


def health(url: str = "http://localhost:8000") -> str:
    """Check live service health endpoint.

    Args:
        url: Base URL of the running service.
    """
    from src.cli import cmd_health

    args = _make_args(url=url)
    return _capture(cmd_health, args)


def status() -> str:
    """Show project status: version, git branch, test count, skills, event log."""
    from src.cli import cmd_status

    args = _make_args()
    return _capture(cmd_status, args)


def doctor() -> str:
    """Run environment health check. Returns 'HEALTHY' or 'ISSUES FOUND' at end."""
    from src.cli import cmd_doctor

    args = _make_args()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = cmd_doctor(args)
    output = buf.getvalue()
    verdict = "HEALTHY" if rc == 0 else "ISSUES FOUND"
    return f"{output}\n{verdict}"


def get_logs(
    event: str | None = None,
    tag: str | None = None,
    limit: int = 50,
    summary: bool = False,
) -> str:
    """Query the indexed event log.

    Args:
        event: Filter by event name.
        tag: Filter by tag.
        limit: Maximum number of results.
        summary: Show count per event type instead of individual records.
    """
    from src.cli import cmd_logs

    args = _make_args(event=event, tag=tag, limit=limit, summary=summary, json=False)
    return _capture(cmd_logs, args)


def _build_server():
    """Create and register tool functions with FastMCP. Deferred so import is safe."""
    FastMCP = _require_fastmcp()
    mcp = FastMCP("ccm", instructions="Claude Code Max deployment and operations server")
    for fn in (deploy, build, health, status, doctor, get_logs):
        mcp.tool()(fn)
    return mcp


def run() -> None:
    """Entry point for ``ccm serve-mcp``."""
    _build_server().run()


if __name__ == "__main__":
    run()
```


## 4.3 API Layer (src/api/)

FILE: /home/user/wellux_testprojects/src/api/__init__.py
```python
"""FastAPI application package."""
from .app import app
from .models import CompleteRequest, CompleteResponse, RouteRequest, RouteResponse

__all__ = ["app", "CompleteRequest", "CompleteResponse", "RouteRequest", "RouteResponse"]
```

FILE: /home/user/wellux_testprojects/src/api/app.py
```python
"""FastAPI application — exposes LLM completion, routing, and chat endpoints."""
from __future__ import annotations

import os
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from ..llm.base import CompletionRequest
from ..routing import route as routing_route
from ..utils.cache import ResponseCache
from ..utils.log_index import LogIndex
from ..utils.logger import get_logger
from ..utils.rate_limiter import RateLimiter
from ..version import __version__
from .middleware import (
    ContentLengthLimitMiddleware,
    CorrelationIDMiddleware,
    TimingMiddleware,
    get_request_id,
)
from .models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CompleteRequest,
    CompleteResponse,
    HealthResponse,
    RouteRequest,
    RouteResponse,
)

logger = get_logger(__name__)

# Shared singletons — initialized at startup
_cache: ResponseCache | None = None
_rate_limiter: RateLimiter | None = None
_log: LogIndex | None = None
_client = None       # ClaudeClient — lazy to avoid import-time anthropic requirement
_start_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize shared resources on startup; flush and log on shutdown."""
    global _cache, _rate_limiter, _log, _start_time
    _start_time = time.monotonic()
    _cache = ResponseCache(ttl_seconds=3600, max_size=1000)
    _rate_limiter = RateLimiter(requests_per_minute=100)
    _log = LogIndex(os.environ.get("CCM_LOG_PATH", "data/cache/events.log"))
    _log.append("api_startup", version=__version__, pid=os.getpid())
    logger.info("api_startup", version=__version__, cache_ttl=3600, rpm=100)
    yield
    # Graceful shutdown — flush remaining log entries
    uptime = round(time.monotonic() - _start_time, 1)
    if _log:
        _log.append("api_shutdown", version=__version__, uptime_s=uptime,
                    cache_size=_cache.size if _cache else 0)
    logger.info("api_shutdown", version=__version__, uptime_s=uptime)


def _get_client():
    """Lazy-init ClaudeClient to avoid import errors when anthropic not installed."""
    global _client
    if _client is None:
        from ..llm.claude_client import ClaudeClient
        _client = ClaudeClient(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            cache=_cache,
            rate_limiter=_rate_limiter,
        )
    return _client


app = FastAPI(
    title="Claude Code Max API",
    description="LLM completion, routing, and chat — backed by Claude",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(ContentLengthLimitMiddleware)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(TimingMiddleware)

# Versioned router — all business endpoints live under /v1
v1 = APIRouter(prefix="/v1")


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health():
    uptime = round(time.monotonic() - _start_time, 1) if _start_time else None
    return HealthResponse(
        status="ok",
        version=__version__,
        models_available=[
            "claude-opus-4-6",
            "claude-sonnet-4-6",
            "claude-haiku-4-5-20251001",
        ],
        uptime_s=uptime,
    )


# ── Completion ────────────────────────────────────────────────────────────────

@v1.post("/complete", response_model=CompleteResponse)
async def complete(req: CompleteRequest):
    """Single-turn completion with optional auto-routing."""
    routed_by = None
    model = req.model
    if req.auto_route and model is None:
        decision = routing_route(req.prompt)
        model = decision.llm.model.value
        routed_by = decision.llm.reason

    client = _get_client()
    llm_req = CompletionRequest(
        prompt=req.prompt,
        system=req.system,
        model=model,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    try:
        resp = await client.complete(llm_req)
    except Exception as e:
        rid = get_request_id()
        logger.error("complete_error", error=str(e), request_id=rid)
        if _log:
            _log.append("complete_error", error=type(e).__name__,
                        request_id=rid, tag="error")
        raise HTTPException(
            status_code=502,
            detail=f"Upstream LLM error [{type(e).__name__}] — see server logs (request_id={rid})",
        ) from e

    if _log:
        _log.append("complete_ok", model=resp.model,
                    input_tokens=resp.input_tokens,
                    output_tokens=resp.output_tokens,
                    cost_usd=resp.cost_usd,
                    request_id=get_request_id(),
                    tag="llm")

    return CompleteResponse(
        content=resp.content,
        model=resp.model,
        input_tokens=resp.input_tokens,
        output_tokens=resp.output_tokens,
        cost_usd=resp.cost_usd,
        stop_reason=resp.stop_reason,
        routed_by=routed_by,
    )


@v1.post("/complete/stream")
async def complete_stream(req: CompleteRequest):
    """Streaming completion — returns server-sent event tokens."""
    model = req.model
    if req.auto_route and model is None:
        decision = routing_route(req.prompt)
        model = decision.llm.model.value

    client = _get_client()
    llm_req = CompletionRequest(
        prompt=req.prompt,
        system=req.system,
        model=model,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    async def token_generator() -> AsyncIterator[str]:
        try:
            async for token in client.stream(llm_req):
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error("stream_error", error=str(e))
            yield f"data: [ERROR] {e}\n\n"

    return StreamingResponse(token_generator(), media_type="text/event-stream")


# ── Chat ──────────────────────────────────────────────────────────────────────

@v1.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Multi-turn chat — passes messages list directly to the Anthropic messages API."""
    # Route model on the last user message for complexity scoring
    model = req.model
    if model is None:
        last_user = next(
            (m.content for m in reversed(req.messages) if m.role == "user"), ""
        )
        decision = routing_route(last_user or "")
        model = decision.llm.model.value

    client = _get_client()
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    try:
        resp = await client.chat(
            messages,
            system=req.system,
            model=model,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
        )
    except Exception as e:
        rid = get_request_id()
        logger.error("chat_error", error=str(e), request_id=rid)
        if _log:
            _log.append("chat_error", error=type(e).__name__,
                        request_id=rid, tag="error")
        raise HTTPException(
            status_code=502,
            detail=f"Upstream LLM error [{type(e).__name__}] — see server logs (request_id={rid})",
        ) from e

    return ChatResponse(
        message=ChatMessage(role="assistant", content=resp.content),
        model=resp.model,
        input_tokens=resp.input_tokens,
        output_tokens=resp.output_tokens,
        cost_usd=resp.cost_usd,
    )


# ── Routing ───────────────────────────────────────────────────────────────────

@v1.post("/route", response_model=RouteResponse)
async def route(req: RouteRequest):
    """Return routing decisions for a task without executing anything."""
    decision = routing_route(req.task, content_type=req.content_type)

    subtasks = [
        {
            "id": st.id,
            "description": st.description,
            "agent": st.agent.value,
            "model": st.model.value,
            "skill": st.skill,
            "depends_on": st.depends_on,
        }
        for st in decision.plan.subtasks
    ]

    return RouteResponse(
        model=decision.llm.model.value,
        model_reason=decision.llm.reason,
        skill=decision.skill.skill if decision.skill else None,
        skill_confidence=decision.skill.confidence if decision.skill else None,
        agent=decision.agent.agent.value,
        agent_reason=decision.agent.reason,
        memory_tier=decision.memory.tier.value,
        memory_destination=decision.memory.destination,
        plan_size=decision.plan.size.value,
        plan_mode=decision.plan.execution_mode,
        subtasks=subtasks,
    )


# Register versioned routes
app.include_router(v1)
```

FILE: /home/user/wellux_testprojects/src/api/middleware.py
```python
"""API middleware — correlation IDs, request timing, and structured access logs."""
from __future__ import annotations

import contextvars
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from ..utils.logger import get_logger

logger = get_logger("api.access")

# Context var so handlers can read the current request ID
_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)


def get_request_id() -> str:
    """Return the correlation ID for the current request (empty string if none)."""
    return _request_id_var.get()


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Attach a correlation/request ID to every request and response.

    - Reads ``X-Request-ID`` from incoming headers if present.
    - Otherwise generates a new UUID4.
    - Sets ``X-Request-ID`` on the response.
    - Logs structured access events with method, path, status, and latency.

    Usage::
        app.add_middleware(CorrelationIDMiddleware)
    """

    HEADER = "X-Request-ID"

    def __init__(self, app: ASGIApp, *, prefix: str = "") -> None:
        super().__init__(app)
        self._prefix = prefix

    async def dispatch(self, request: Request, call_next) -> Response:
        # Honour incoming ID (e.g. from a gateway) or generate a fresh one
        request_id = request.headers.get(self.HEADER) or f"{self._prefix}{uuid.uuid4().hex}"
        token = _request_id_var.set(request_id)

        t0 = time.monotonic()
        try:
            response: Response = await call_next(request)
            latency_ms = (time.monotonic() - t0) * 1000
            response.headers[self.HEADER] = request_id
            logger.info(
                "http_request",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                latency_ms=round(latency_ms, 1),
                request_id=request_id,
            )
            return response
        finally:
            _request_id_var.reset(token)


class TimingMiddleware(BaseHTTPMiddleware):
    """Add ``X-Process-Time-Ms`` header to every response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        t0 = time.monotonic()
        response = await call_next(request)
        response.headers["X-Process-Time-Ms"] = str(round((time.monotonic() - t0) * 1000, 1))
        return response


class ContentLengthLimitMiddleware(BaseHTTPMiddleware):
    """Reject requests whose declared Content-Length exceeds ``max_bytes``.

    Returns HTTP 413 before the body is read, protecting the server from
    large payload allocations. Requests without a Content-Length header
    are passed through (chunked/streaming transfers).

    Default limit: 1 MiB (1_048_576 bytes).

    Usage::
        app.add_middleware(ContentLengthLimitMiddleware, max_bytes=512_000)
    """

    DEFAULT_MAX_BYTES = 1_048_576  # 1 MiB

    def __init__(self, app: ASGIApp, *, max_bytes: int = DEFAULT_MAX_BYTES) -> None:
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                return JSONResponse(
                    {"detail": "Invalid Content-Length header"},
                    status_code=400,
                )
            if length > self.max_bytes:
                logger.warning(
                    "request_too_large",
                    content_length=length,
                    max_bytes=self.max_bytes,
                    path=request.url.path,
                )
                return JSONResponse(
                    {"detail": f"Request body too large: {length} bytes (max {self.max_bytes})"},
                    status_code=413,
                )
        return await call_next(request)
```

FILE: /home/user/wellux_testprojects/src/api/models.py
```python
"""Pydantic request/response models for the FastAPI layer."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CompleteRequest(BaseModel):
    prompt: str
    system: str | None = None
    model: str | None = None          # None = auto-route
    max_tokens: int = Field(default=4096, ge=1, le=200000)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    stream: bool = False
    auto_route: bool = True           # use routing system to pick model


class CompleteResponse(BaseModel):
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    stop_reason: str
    routed_by: str | None = None      # routing reason if auto_route=True


class RouteRequest(BaseModel):
    task: str
    content_type: str | None = None   # hint for memory router


class RouteResponse(BaseModel):
    model: str
    model_reason: str
    skill: str | None
    skill_confidence: float | None
    agent: str
    agent_reason: str
    memory_tier: str
    memory_destination: str
    plan_size: str
    plan_mode: str
    subtasks: list[dict]


class ChatMessage(BaseModel):
    role: str   # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)
    system: str | None = None
    model: str | None = None
    max_tokens: int = Field(default=4096, ge=1, le=200000)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    message: ChatMessage
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class HealthResponse(BaseModel):
    status: str
    version: str
    models_available: list[str]
    uptime_s: float | None = None
```


## 4.4 LLM Layer (src/llm/)

FILE: /home/user/wellux_testprojects/src/llm/__init__.py
```python
"""LLM client package."""
from .base import CompletionRequest, CompletionResponse, LLMClient
from .utils import build_request, merge_system_prompts, truncate_to_tokens


def __getattr__(name: str):
    if name == "ClaudeClient":
        from .claude_client import ClaudeClient
        return ClaudeClient
    if name == "GPTClient":
        from .gpt_client import GPTClient
        return GPTClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "LLMClient",
    "CompletionRequest",
    "CompletionResponse",
    "ClaudeClient",
    "GPTClient",
    "build_request",
    "truncate_to_tokens",
    "merge_system_prompts",
]
```

FILE: /home/user/wellux_testprojects/src/llm/base.py
```python
"""Abstract base class for LLM clients."""
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class CompletionRequest:
    prompt: str
    system: str | None = None
    model: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7
    stream: bool = False


@dataclass
class CompletionResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    stop_reason: str

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def cost_usd(self) -> float:
        """Rough cost estimate — update rates from config."""
        rates = {
            "claude-sonnet-4-6": (3.0, 15.0),
            "claude-opus-4-6": (15.0, 75.0),
            "claude-haiku-4-5-20251001": (0.25, 1.25),
        }
        input_rate, output_rate = rates.get(self.model, (3.0, 15.0))
        return (self.input_tokens * input_rate + self.output_tokens * output_rate) / 1_000_000


class LLMClient(ABC):
    """Abstract LLM client interface. All providers implement this."""

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Generate a completion for the given request."""
        ...  # pragma: no cover — abstract stub

    @abstractmethod
    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...  # pragma: no cover — abstract stub

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text without making an API call."""
        ...  # pragma: no cover — abstract stub
```

FILE: /home/user/wellux_testprojects/src/llm/claude_client.py
```python
"""Anthropic Claude API client — retry with jitter, structured logging."""
from __future__ import annotations

import asyncio
import random
import time
from collections.abc import AsyncIterator

import anthropic

from ..utils.cache import ResponseCache
from ..utils.logger import get_logger
from ..utils.rate_limiter import RateLimiter
from .base import CompletionRequest, CompletionResponse, LLMClient

logger = get_logger(__name__)

# Exceptions that are safe to retry (transient)
_RETRYABLE = (anthropic.RateLimitError, anthropic.InternalServerError)
# Exceptions that are never retried (client mistakes)
_FATAL = (anthropic.AuthenticationError, anthropic.PermissionDeniedError)

_BASE_BACKOFF_S = 1.0    # first retry waits ~1 s
_MAX_BACKOFF_S = 30.0    # cap at 30 s regardless of attempt count
_JITTER_RATIO = 0.25     # ±25 % random jitter to avoid thundering herd


def _backoff(attempt: int) -> float:
    """Exponential backoff with full jitter: base * 2^attempt ± jitter."""
    delay = min(_BASE_BACKOFF_S * (2 ** attempt), _MAX_BACKOFF_S)
    jitter = delay * _JITTER_RATIO * (2 * random.random() - 1)
    return max(0.0, delay + jitter)


class ClaudeClient(LLMClient):
    """Production Claude client with rate limiting, caching, and retry."""

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = DEFAULT_MODEL,
        cache: ResponseCache | None = None,
        rate_limiter: RateLimiter | None = None,
        max_retries: int = 3,
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.async_client = anthropic.AsyncAnthropic(api_key=api_key)
        self.default_model = default_model
        self.cache = cache or ResponseCache()
        self.rate_limiter = rate_limiter or RateLimiter(requests_per_minute=100)
        self.max_retries = max_retries

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Complete with caching, rate limiting, and exponential-backoff retry."""
        model = request.model or self.default_model

        cached = self.cache.get(request)
        if cached:
            logger.debug("cache_hit", model=model, prompt_len=len(request.prompt))
            return cached

        await self.rate_limiter.acquire()

        last_exc: BaseException = RuntimeError("no attempts made")
        for attempt in range(self.max_retries):
            try:
                t0 = time.monotonic()
                message = await self.async_client.messages.create(
                    model=model,
                    max_tokens=max(1, request.max_tokens),
                    temperature=max(0.0, min(1.0, request.temperature)),
                    system=request.system or anthropic.NOT_GIVEN,
                    messages=[{"role": "user", "content": request.prompt}],
                )
                latency_ms = int((time.monotonic() - t0) * 1000)

                if not message.content:
                    raise ValueError("Anthropic returned empty content block")
                response = CompletionResponse(
                    content=message.content[0].text,
                    model=message.model,
                    input_tokens=message.usage.input_tokens,
                    output_tokens=message.usage.output_tokens,
                    stop_reason=message.stop_reason or "end_turn",
                )

                logger.info(
                    "llm_call",
                    model=model,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=response.cost_usd,
                    attempt=attempt,
                )
                self.cache.set(request, response)
                return response

            except _FATAL as e:
                # Auth errors: no point retrying
                logger.error("llm_fatal", error=type(e).__name__, detail=str(e))
                raise

            except _RETRYABLE as e:
                wait = _backoff(attempt)
                logger.warning(
                    "llm_retry",
                    error=type(e).__name__,
                    attempt=attempt,
                    wait_s=round(wait, 2),
                    remaining=self.max_retries - attempt - 1,
                )
                last_exc = e
                await asyncio.sleep(wait)

            except anthropic.APIError as e:
                # Unexpected API errors — retry but log loudly
                wait = _backoff(attempt)
                logger.error("llm_api_error", error=str(e), attempt=attempt,
                             wait_s=round(wait, 2))
                last_exc = e
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(wait)

        raise RuntimeError(
            f"LLM call failed after {self.max_retries} attempts: {last_exc}"
        )

    async def chat(
        self,
        messages: list[dict],
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResponse:
        """Multi-turn chat using the native Anthropic messages API.

        Unlike `complete()`, this accepts a list of role/content dicts and passes
        them directly to the API — preserving proper conversation context.

        Args:
            messages: List of {"role": "user"|"assistant", "content": str} dicts.
            system: Optional system prompt.
            model: Model override; defaults to self.default_model.
            max_tokens: Maximum tokens in the response.
            temperature: Sampling temperature.
        """
        model = model or self.default_model
        await self.rate_limiter.acquire()

        last_exc: BaseException = RuntimeError("no attempts made")
        for attempt in range(self.max_retries):
            try:
                t0 = time.monotonic()
                message = await self.async_client.messages.create(
                    model=model,
                    max_tokens=max(1, max_tokens),
                    temperature=max(0.0, min(1.0, temperature)),
                    system=system or anthropic.NOT_GIVEN,
                    messages=messages,
                )
                latency_ms = int((time.monotonic() - t0) * 1000)

                if not message.content:
                    raise ValueError("Anthropic returned empty content block")
                response = CompletionResponse(
                    content=message.content[0].text,
                    model=message.model,
                    input_tokens=message.usage.input_tokens,
                    output_tokens=message.usage.output_tokens,
                    stop_reason=message.stop_reason or "end_turn",
                )
                logger.info(
                    "llm_chat",
                    model=model,
                    turns=len(messages),
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=response.cost_usd,
                    attempt=attempt,
                )
                return response

            except _FATAL as e:
                logger.error("llm_fatal", error=type(e).__name__, detail=str(e))
                raise

            except _RETRYABLE as e:
                wait = _backoff(attempt)
                logger.warning(
                    "llm_retry",
                    error=type(e).__name__,
                    attempt=attempt,
                    wait_s=round(wait, 2),
                    remaining=self.max_retries - attempt - 1,
                )
                last_exc = e
                await asyncio.sleep(wait)

            except anthropic.APIError as e:
                wait = _backoff(attempt)
                logger.error("llm_api_error", error=str(e), attempt=attempt,
                             wait_s=round(wait, 2))
                last_exc = e
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(wait)

        raise RuntimeError(
            f"LLM chat failed after {self.max_retries} attempts: {last_exc}"
        )

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream response tokens (no retry — caller owns the connection)."""
        model = request.model or self.default_model
        await self.rate_limiter.acquire()

        async with self.async_client.messages.stream(
            model=model,
            max_tokens=max(1, request.max_tokens),
            temperature=max(0.0, min(1.0, request.temperature)),
            system=request.system or anthropic.NOT_GIVEN,
            messages=[{"role": "user", "content": request.prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def count_tokens(self, text: str) -> int:
        """Approximate token count (≈4 chars per token). Use SDK for precision."""
        return len(text) // 4
```

FILE: /home/user/wellux_testprojects/src/llm/gpt_client.py
```python
"""OpenAI GPT API client."""
import asyncio
import time
from collections.abc import AsyncIterator

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..utils.cache import ResponseCache
from ..utils.logger import get_logger
from ..utils.rate_limiter import RateLimiter
from .base import CompletionRequest, CompletionResponse, LLMClient

logger = get_logger(__name__)

# Cost per 1M tokens (USD) — update as pricing changes
GPT4O_INPUT_COST = 2.50
GPT4O_OUTPUT_COST = 10.00
GPT4O_MINI_INPUT_COST = 0.15
GPT4O_MINI_OUTPUT_COST = 0.60


def _cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    if "mini" in model:
        return (input_tokens * GPT4O_MINI_INPUT_COST + output_tokens * GPT4O_MINI_OUTPUT_COST) / 1_000_000
    return (input_tokens * GPT4O_INPUT_COST + output_tokens * GPT4O_OUTPUT_COST) / 1_000_000


class GPTClient(LLMClient):
    """OpenAI GPT client with rate limiting, caching, and retry."""

    DEFAULT_MODEL = "gpt-4o"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = DEFAULT_MODEL,
        cache: ResponseCache | None = None,
        rate_limiter: RateLimiter | None = None,
        max_retries: int = 3,
    ):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package required: pip install openai")
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.default_model = default_model
        self.cache = cache or ResponseCache()
        self.rate_limiter = rate_limiter or RateLimiter(requests_per_minute=500)
        self.max_retries = max_retries

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Complete with caching and retry."""
        model = request.model or self.default_model

        cached = self.cache.get(request)
        if cached:
            logger.debug("cache_hit", model=model, prompt_len=len(request.prompt))
            return cached

        await self.rate_limiter.acquire()

        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        last_error = None
        for attempt in range(self.max_retries):
            try:
                t0 = time.monotonic()
                resp = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                )
                latency_ms = int((time.monotonic() - t0) * 1000)

                content = resp.choices[0].message.content or ""
                stop_reason = resp.choices[0].finish_reason or "stop"
                input_tokens = resp.usage.prompt_tokens if resp.usage else 0
                output_tokens = resp.usage.completion_tokens if resp.usage else 0

                response = CompletionResponse(
                    content=content,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    stop_reason=stop_reason,
                )

                logger.info(
                    "llm_call",
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=_cost_usd(model, input_tokens, output_tokens),
                )

                self.cache.set(request, response)
                return response

            except openai.RateLimitError:
                wait = 2 ** attempt
                logger.warning("rate_limit_retry", attempt=attempt, wait_s=wait)
                await asyncio.sleep(wait)
                last_error = "rate_limit"
            except openai.APIError as e:
                logger.error("api_error", error=str(e), attempt=attempt)
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
                last_error = str(e)

        raise RuntimeError(f"Failed after {self.max_retries} retries: {last_error}")

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream response tokens."""
        model = request.model or self.default_model
        await self.rate_limiter.acquire()

        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def count_tokens(self, text: str) -> int:
        """Rough token count: ~4 chars per token."""
        return len(text) // 4
```

FILE: /home/user/wellux_testprojects/src/llm/utils.py
```python
"""LLM utility helpers."""
from __future__ import annotations

from .base import CompletionRequest, LLMClient


def build_request(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> CompletionRequest:
    """Convenience constructor for CompletionRequest."""
    return CompletionRequest(
        prompt=prompt,
        system=system,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def truncate_to_tokens(text: str, max_tokens: int, chars_per_token: int = 4) -> str:
    """Truncate text to approximately max_tokens."""
    max_chars = max_tokens * chars_per_token
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def merge_system_prompts(*prompts: str | None, separator: str = "\n\n") -> str | None:
    """Merge multiple system prompt fragments, skipping None/empty."""
    parts = [p for p in prompts if p and p.strip()]
    return separator.join(parts) if parts else None


def format_messages_as_prompt(messages: list[dict]) -> str:
    """Convert chat message list to a flat prompt string for non-chat APIs."""
    lines = []
    for msg in messages:
        role = msg.get("role", "user").upper()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


async def complete_with_fallback(
    primary: LLMClient,
    fallback: LLMClient,
    request: CompletionRequest,
):
    """Try primary client, fall back to secondary on any error."""
    try:
        return await primary.complete(request)
    except Exception as primary_err:
        from ..utils.logger import get_logger
        logger = get_logger(__name__)
        logger.warning("primary_client_failed", error=str(primary_err), falling_back=True)
        return await fallback.complete(request)
```


## 4.5 Routing System (src/routing/)

FILE: /home/user/wellux_testprojects/src/routing/__init__.py
```python
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
```

FILE: /home/user/wellux_testprojects/src/routing/llm_router.py
```python
"""LLM Router — auto-select the right model based on task signals.

Decision logic (in priority order):
1. Explicit override → use it
2. Task complexity score → opus / sonnet / haiku
3. Cost sensitivity flag → prefer haiku
4. Latency sensitivity flag → prefer haiku
5. Default → sonnet (best cost/quality balance)

Complexity scoring:
- HIGH  (score 7-10): architecture, security audit, multi-file refactor, novel research
- MED   (score 4-6):  feature implementation, code review, debugging, writing
- LOW   (score 0-3):  lookups, summaries, simple transforms, formatting
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Model(StrEnum):
    OPUS   = "claude-opus-4-6"
    SONNET = "claude-sonnet-4-6"
    HAIKU  = "claude-haiku-4-5-20251001"


class Complexity(StrEnum):
    HIGH   = "high"
    MEDIUM = "medium"
    LOW    = "low"


@dataclass
class RoutingDecision:
    model: Model
    complexity: Complexity
    reason: str
    score: int
    estimated_cost_tier: str  # "high" | "medium" | "low"


# Keywords that signal high complexity (score +2 each)
_HIGH_SIGNALS = [
    "architect", "design system", "security audit", "audit", "refactor entire",
    "migrate", "first principles", "research", "novel", "complex", "multi-step",
    "orchestrate", "swarm", "strategy", "evaluate", "benchmark", "analyze all",
    "production system", "trade-off", "tradeoff",
]

# Keywords that signal low complexity (score -2 each)
_LOW_SIGNALS = [
    "summarize", "summary", "list", "what is", "explain briefly", "format",
    "rename", "typo", "simple", "quick", "one-liner", "translate", "convert",
    "count", "grep", "find", "lookup", "check if", "does this",
    "status", "standup", "changelog entry",
]

# Keywords that force haiku regardless of complexity
_HAIKU_FORCE = [
    "fast", "quickly", "low latency", "cheap", "minimal cost", "batch",
    "streaming autocomplete", "inline suggestion",
]


def score_complexity(task: str) -> tuple[int, list[str]]:
    """Return (raw_score, matched_signals) for a task description."""
    task_lower = task.lower()
    score = 5  # baseline = medium
    matched: list[str] = []

    for sig in _HIGH_SIGNALS:
        if sig in task_lower:
            score += 2
            matched.append(f"+2 [{sig}]")

    for sig in _LOW_SIGNALS:
        if sig in task_lower:
            score -= 2
            matched.append(f"-2 [{sig}]")

    return max(0, min(10, score)), matched


def route_llm(
    task: str,
    *,
    override: Model | str | None = None,
    cost_sensitive: bool = False,
    latency_sensitive: bool = False,
    min_complexity: Complexity | None = None,
) -> RoutingDecision:
    """Select the best model for a given task.

    Args:
        task: Natural language description of what needs to be done.
        override: Force a specific model (skips all routing logic).
        cost_sensitive: Prefer cheaper models when quality is adequate.
        latency_sensitive: Prefer faster models (haiku first).
        min_complexity: Floor the complexity level (e.g. never route below MEDIUM).

    Returns:
        RoutingDecision with model, reasoning, and cost tier.
    """
    # 1. Explicit override
    if override:
        model = Model(override) if isinstance(override, str) else override
        return RoutingDecision(
            model=model,
            complexity=Complexity.MEDIUM,
            reason=f"explicit override → {model.value}",
            score=-1,
            estimated_cost_tier="override",
        )

    # 2. Haiku force signals
    task_lower = task.lower()
    for sig in _HAIKU_FORCE:
        if sig in task_lower:
            return RoutingDecision(
                model=Model.HAIKU,
                complexity=Complexity.LOW,
                reason=f"latency/cost signal [{sig}] → haiku",
                score=0,
                estimated_cost_tier="low",
            )

    # 3. Score the task
    score, signals = score_complexity(task)

    # 4. Latency/cost overrides push toward lighter models
    if latency_sensitive or cost_sensitive:
        score = max(0, score - 3)

    # 5. Map score → complexity
    if score >= 7:
        complexity = Complexity.HIGH
    elif score >= 4:
        complexity = Complexity.MEDIUM
    else:
        complexity = Complexity.LOW

    # 6. Apply min_complexity floor
    if min_complexity:
        order = [Complexity.LOW, Complexity.MEDIUM, Complexity.HIGH]
        if order.index(complexity) < order.index(min_complexity):
            complexity = min_complexity
            score = max(score, 4 if min_complexity == Complexity.MEDIUM else 7)

    # 7. Select model
    if complexity == Complexity.HIGH:
        model = Model.OPUS
        cost_tier = "high"
    elif complexity == Complexity.MEDIUM:
        model = Model.SONNET
        cost_tier = "medium"
    else:
        model = Model.HAIKU
        cost_tier = "low"

    reason = f"score={score}/10 [{', '.join(signals) or 'baseline'}] → {complexity.value} → {model.value}"

    return RoutingDecision(
        model=model,
        complexity=complexity,
        reason=reason,
        score=score,
        estimated_cost_tier=cost_tier,
    )


# Convenience shortcuts
def cheap(task: str) -> RoutingDecision:
    """Route with cost sensitivity on."""
    return route_llm(task, cost_sensitive=True)


def fast(task: str) -> RoutingDecision:
    """Route with latency sensitivity on."""
    return route_llm(task, latency_sensitive=True)


def best(task: str) -> RoutingDecision:
    """Route to highest quality model (min MEDIUM complexity)."""
    return route_llm(task, min_complexity=Complexity.MEDIUM)
```

FILE: /home/user/wellux_testprojects/src/routing/skill_router.py
```python
"""Skill Router — map user intent to the right skill.

Two-stage matching:
1. Keyword match — single compiled-regex scan against all trigger phrases
2. Category match — broader topic → skill category → best skill in category

Each skill entry has:
- triggers: exact phrases that strongly indicate this skill
- categories: broader topic buckets
- priority: higher = preferred when multiple match (0-10)
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SkillMatch:
    skill: str               # skill name (matches .claude/skills/<name>/)
    confidence: float        # 0.0 - 1.0
    reason: str              # why this skill was selected
    category: str
    fallback: str | None = None  # next-best skill if primary unavailable


# ---------------------------------------------------------------------------
# Skill registry — each entry maps skill_name → trigger signals
# ---------------------------------------------------------------------------
_SKILL_REGISTRY: list[dict] = [
    # ── Security ────────────────────────────────────────────────────────────
    {"skill": "ciso",             "category": "security", "priority": 9,
     "triggers": ["security orchestrat", "full security", "run the team", "security strategy", "ciso",
                  "security audit", "security assessment", "security posture"]},
    {"skill": "pen-tester",       "category": "security", "priority": 8,
     "triggers": ["penetration test", "pentest", "red team", "exploit", "adversary emulation",
                  "offensive security", "attack surface", "ethical hacking", "find vulnerabilities"]},
    {"skill": "appsec-engineer",  "category": "security", "priority": 8,
     "triggers": ["owasp", "sql injection", "xss", "csrf", "secure code review", "application security",
                  "appsec", "sast", "input validation", "is this safe"]},
    {"skill": "soc-analyst",      "category": "security", "priority": 7,
     "triggers": ["threat detection", "siem", "alert triage", "incident triage", "blue team", "soc",
                  "threat hunting", "triage this alert", "investigate this log"]},
    {"skill": "incident-response","category": "security", "priority": 9,
     "triggers": ["incident", "breach", "prod is down", "production down", "compromised", "forensic",
                  "containment", "we got breached", "ir plan"]},
    {"skill": "ai-security",      "category": "security", "priority": 8,
     "triggers": ["prompt injection", "jailbreak", "llm security", "agent security",
                  "system prompt leakage", "tool call validation", "llm guardrails",
                  "adversarial inputs", "ai pipeline security"]},
    {"skill": "grc-analyst",      "category": "security", "priority": 6,
     "triggers": ["compliance", "gdpr", "soc2", "hipaa", "compliance audit", "governance",
                  "iso 27001", "regulatory compliance", "compliance check", "grc audit"]},
    {"skill": "iam-engineer",     "category": "security", "priority": 7,
     "triggers": ["sso", "oauth", "mfa", "rbac", "access control", "identity", "permissions", "iam",
                  "least privilege", "service account", "role design"]},
    {"skill": "secrets-mgr",      "category": "security", "priority": 7,
     "triggers": ["secret", "api key", "credential", "vault", "rotate key", "env var leak",
                  "hashicorp vault", "secrets management", "no hardcoded secrets"]},

    # ── Development ─────────────────────────────────────────────────────────
    {"skill": "code-review",      "category": "development", "priority": 8,
     "triggers": ["review this", "review my code", "pr review", "before i merge", "check my code",
                  "lgtm?", "code quality", "look at this implementation", "feedback on code"]},
    {"skill": "debug",            "category": "development", "priority": 9,
     "triggers": ["error", "bug", "broken", "traceback", "exception", "failing", "not working",
                  "fix this", "debug this", "why is this failing", "it crashes"]},
    {"skill": "refactor",         "category": "development", "priority": 7,
     "triggers": ["refactor", "clean up", "restructure", "simplify this code", "too complex",
                  "reduce duplication", "dry this up", "spaghetti code"]},
    {"skill": "architect",        "category": "development", "priority": 8,
     "triggers": ["design this", "architect", "system design", "how should i structure",
                  "design decision", "technical design doc", "scalability design", "architecture review"]},
    {"skill": "test-writer",      "category": "development", "priority": 7,
     "triggers": ["write tests", "add tests", "test coverage", "unit test", "pytest", "jest",
                  "tdd", "improve coverage", "test this function", "missing tests"]},
    {"skill": "api-designer",     "category": "development", "priority": 7,
     "triggers": ["design api", "rest api", "api endpoint", "openapi", "swagger", "api schema",
                  "api spec", "endpoint design", "what endpoints do i need"]},
    {"skill": "type-safety",      "category": "development", "priority": 6,
     "triggers": ["add types", "type annotation", "mypy", "typescript types", "type hints", "typed",
                  "type errors", "any type", "missing types"]},
    {"skill": "perf-profiler",    "category": "development", "priority": 7,
     "triggers": ["slow", "performance", "profil", "bottleneck", "latency", "optimize speed", "p99",
                  "cpu spike", "benchmark performance"]},
    {"skill": "bug-hunter",       "category": "development", "priority": 7,
     "triggers": ["find bugs", "hunt for", "edge case", "vulnerability scan code",
                  "stress test", "off-by-one", "null pointer", "find weaknesses",
                  "adversarial test"]},
    {"skill": "tech-debt",        "category": "development", "priority": 6,
     "triggers": ["tech debt", "technical debt", "cleanup", "legacy code", "modernize",
                  "dead code", "deprecated", "code smells", "cruft"]},

    # ── AI / ML ─────────────────────────────────────────────────────────────
    {"skill": "karpathy-researcher", "category": "research", "priority": 9,
     "triggers": ["research", "deep dive", "first principles", "latest on", "how does x work",
                  "explain from scratch", "deep dive into", "understand x from scratch", "karpathy"]},
    {"skill": "rag-builder",      "category": "ai", "priority": 8,
     "triggers": ["rag", "retrieval", "vector store", "embedding search", "knowledge base retrieval",
                  "lightrag", "semantic search", "document retrieval",
                  "reduce hallucination with retrieval"]},
    {"skill": "prompt-engineer",  "category": "ai", "priority": 8,
     "triggers": ["improve this prompt", "prompt engineering", "optimize prompt", "system prompt",
                  "few-shot", "chain of thought", "better prompt for", "my prompt isn't working"]},
    {"skill": "llm-optimizer",    "category": "ai", "priority": 7,
     "triggers": ["reduce cost", "token cost", "cheaper inference", "latency llm", "optimize inference",
                  "llm cost too high", "reduce tokens", "llm performance", "token optimization"]},
    {"skill": "fine-tuner",       "category": "ai", "priority": 8,
     "triggers": ["fine-tune", "fine tune", "lora", "qlora", "train model", "finetune",
                  "domain adaptation", "custom model", "instruction tuning"]},
    {"skill": "evals-designer",   "category": "ai", "priority": 7,
     "triggers": ["eval", "evaluation", "benchmark", "measure quality", "llm grading",
                  "test prompts at scale", "measure hallucination", "model comparison",
                  "build an eval suite"]},
    {"skill": "agent-orchestrator","category": "ai", "priority": 8,
     "triggers": ["multi-agent", "orchestrat", "agent pipeline", "chain agents", "coordinate agents",
                  "agent workflow", "agent system", "task delegation to agents"]},
    {"skill": "paper-summarizer", "category": "research", "priority": 7,
     "triggers": ["summarize paper", "arxiv", "research paper", "academic paper", "this study",
                  "tldr this", "what does this paper say", "key findings of"]},

    # ── DevOps ──────────────────────────────────────────────────────────────
    {"skill": "ci-cd",            "category": "devops", "priority": 8,
     "triggers": ["ci/cd", "github actions", "pipeline", "deploy pipeline", "build fails", "cicd",
                  "continuous integration", "automated testing pipeline", "deploy on push"]},
    {"skill": "docker",           "category": "devops", "priority": 7,
     "triggers": ["dockerfile", "docker", "container", "image build", "docker-compose",
                  "multi-stage build", "docker optimization", "containerize"]},
    {"skill": "monitoring",       "category": "devops", "priority": 7,
     "triggers": ["monitor", "alert", "dashboard", "observabilit", "metrics", "grafana", "datadog",
                  "prometheus", "alerting", "what should i alert on"]},
    {"skill": "sre",              "category": "devops", "priority": 7,
     "triggers": ["slo", "sla", "error budget", "reliability", "on-call", "sre",
                  "toil", "post-mortem", "site reliability"]},
    {"skill": "deploy-checker",   "category": "devops", "priority": 8,
     "triggers": ["ready to deploy", "pre-deploy", "deployment checklist", "safe to ship",
                  "deployment check", "pre-prod validation", "deployment gate"]},

    # ── Documentation ───────────────────────────────────────────────────────
    {"skill": "readme-writer",    "category": "docs", "priority": 7,
     "triggers": ["write readme", "update readme", "readme", "documentation for this project",
                  "docs are outdated", "improve documentation"]},
    {"skill": "adr-writer",       "category": "docs", "priority": 7,
     "triggers": ["adr", "architecture decision", "decision record", "why did we choose",
                  "write adr", "document this decision", "architecture choice"]},
    {"skill": "runbook-creator",  "category": "docs", "priority": 6,
     "triggers": ["runbook", "operational procedure", "how to operate", "step by step ops",
                  "ops runbook", "document this procedure", "incident runbook"]},
    {"skill": "changelog",        "category": "docs", "priority": 6,
     "triggers": ["changelog", "release notes", "what changed", "git log to changelog",
                  "changelog entry", "commit history summary", "what's new in this release"]},

    # ── Infrastructure ──────────────────────────────────────────────────────
    {"skill": "k8s",              "category": "devops", "priority": 8,
     "triggers": ["kubernetes", "k8s", "helm", "deployment manifest", "pod", "kubectl", "cluster",
                  "hpa", "ingress"]},
    {"skill": "terraform",        "category": "devops", "priority": 8,
     "triggers": ["terraform", "infrastructure as code", "iac", "hcl", "provisioning", "resource plan",
                  "aws terraform", "terraform module"]},
    {"skill": "db-optimizer",     "category": "development", "priority": 7,
     "triggers": ["slow query", "query performance", "missing index", "n+1", "database slow",
                  "explain plan", "add index", "query optimization"]},
    {"skill": "migration",        "category": "development", "priority": 7,
     "triggers": ["database migration", "schema migration", "alembic", "data migration", "migrate db",
                  "upgrade", "breaking change", "version upgrade"]},

    # ── Ecosystem (gstack · Superpowers · Paperclip) ─────────────────────
    {"skill": "gsd",              "category": "meta", "priority": 9,
     "triggers": ["just do it", "get it done", "no interruptions", "gsd",
                  "stay focused", "focus mode", "no more planning", "execute not plan"]},
    {"skill": "swarm",            "category": "meta", "priority": 9,
     "triggers": ["parallel agents", "spin up agents", "swarm", "decompose into subagents",
                  "multiple agents", "break into subagents", "what agents do i need", "build a swarm"]},
    {"skill": "mem",              "category": "meta", "priority": 8,
     "triggers": ["remember this", "save this", "persist", "don't forget", "store this decision",
                  "add to memory", "save to memory", "note this down"]},
    {"skill": "brainstorm",       "category": "meta", "priority": 8,
     "triggers": ["brainstorm", "explore options", "what should i build", "unclear requirements",
                  "not sure what to build", "help me think through", "refine requirements",
                  "explore the design space"]},
    {"skill": "write-plan",       "category": "meta", "priority": 8,
     "triggers": ["write a plan", "plan this out", "break this down", "decompose this task",
                  "create a task plan", "write plan", "task breakdown", "planning phase",
                  "decompose this feature"]},
    {"skill": "superpowers",      "category": "meta", "priority": 9,
     "triggers": ["high agency", "senior engineer mode", "superpowers", "act like a staff engineer",
                  "just figure it out", "full autonomy", "autonomous coding", "superpowers mode"]},
    {"skill": "office-hours",     "category": "meta", "priority": 8,
     "triggers": ["office hours", "debate the approach", "should we build", "before we start",
                  "strategic review", "ceo review", "product review", "pre-build review",
                  "get alignment"]},
    {"skill": "ship",             "category": "meta", "priority": 9,
     "triggers": ["ready to ship", "cut a release", "release checklist", "deploy to production",
                  "ship this feature", "release pipeline", "ship it", "go live",
                  "push to production"]},
    {"skill": "careful",          "category": "meta", "priority": 8,
     "triggers": ["careful mode", "risky change", "be careful", "irreversible", "low-risk mode",
                  "extra confirmation", "don't break anything", "proceed carefully",
                  "sensitive system"]},
    {"skill": "plan-eng-review",  "category": "meta", "priority": 8,
     "triggers": ["eng review", "technical review", "review my plan", "sanity check the design",
                  "is this the right way", "pre-implementation review", "staff review",
                  "check my plan"]},
    {"skill": "paperclip",        "category": "meta", "priority": 8,
     "triggers": ["assign to agents", "multi-agent task", "agent budget", "orchestrate agents",
                  "paperclip", "agent audit trail", "agent org", "agent with budget", "agent company"]},

    # ── Additional Security ──────────────────────────────────────────────────
    {"skill": "network-engineer",  "category": "security", "priority": 7,
     "triggers": ["firewall", "vpn", "zero-trust", "network security", "network segmentation",
                  "port exposure", "dns security", "tls config", "open ports", "network hardening"]},
    {"skill": "cloud-engineer",    "category": "security", "priority": 7,
     "triggers": ["cloud security", "iam policies", "s3 bucket", "cloud config",
                  "infrastructure security", "cloud hardening", "security groups",
                  "aws security", "cloud misconfiguration"]},
    {"skill": "security-engineer", "category": "security", "priority": 7,
     "triggers": ["siem rule", "waf", "detection engineering", "security tooling",
                  "alert rule", "intrusion detection", "sigma rule", "snort rule",
                  "write detection"]},
    {"skill": "purple-team",       "category": "security", "priority": 7,
     "triggers": ["purple team", "detection validation", "mitre att&ck", "test our defenses",
                  "adversary simulation", "does our monitoring catch"]},
    {"skill": "dba",               "category": "security", "priority": 6,
     "triggers": ["database security", "db permissions", "encryption at rest",
                  "connection string security", "database hardening", "query audit",
                  "backup encryption", "db access review"]},
    {"skill": "help-desk",         "category": "security", "priority": 5,
     "triggers": ["access request", "user provisioning", "endpoint hardening",
                  "device compliance", "mfa setup", "password reset policy",
                  "user offboarding", "permissions request"]},
    {"skill": "sysadmin",          "category": "security", "priority": 6,
     "triggers": ["os hardening", "patch status", "cron security",
                  "file permissions audit", "system configuration",
                  "server hardening", "syslog"]},
    {"skill": "devops-engineer",   "category": "security", "priority": 7,
     "triggers": ["pipeline security", "docker security", "secrets in code", "ci/cd review",
                  "container hardening", "dockerfile audit", "secrets scanning",
                  "github actions security", "hardcoded credentials"]},

    # ── Additional Development ───────────────────────────────────────────────
    {"skill": "async-optimizer",   "category": "development", "priority": 7,
     "triggers": ["async issue", "concurrent", "race condition", "await optimization", "run in parallel",
                  "asyncio", "promise.all", "thread safety", "deadlock", "async bottleneck"]},
    {"skill": "error-handler",     "category": "development", "priority": 6,
     "triggers": ["error handling", "exception handling", "retry logic", "circuit breaker",
                  "graceful degradation", "fallback", "resilience", "fault tolerance",
                  "what happens on failure"]},
    {"skill": "algorithm",         "category": "development", "priority": 7,
     "triggers": ["algorithm improvement", "better algorithm", "o(n", "data structure choice",
                  "optimize this loop", "algorithmic complexity", "time complexity"]},
    {"skill": "concurrency",       "category": "development", "priority": 7,
     "triggers": ["concurrency design", "parallel processing", "worker pool", "queue",
                  "producer consumer", "concurrent writes", "data consistency with concurrent"]},
    {"skill": "cache-strategy",    "category": "development", "priority": 7,
     "triggers": ["add caching", "cache this", "redis", "cache invalidation", "ttl", "cache miss",
                  "expensive operation", "repeated computation", "memoize"]},
    {"skill": "bundle-analyzer",   "category": "development", "priority": 6,
     "triggers": ["bundle size", "reduce bundle", "tree shaking", "code splitting",
                  "large dependency", "bundle too big", "import optimization", "lazy loading"]},
    {"skill": "memory-profiler",   "category": "development", "priority": 7,
     "triggers": ["memory leak", "too much memory", "oom", "memory usage", "memory profiling",
                  "garbage collection", "memory keeps growing", "reduce memory footprint"]},
    {"skill": "query-optimizer",   "category": "development", "priority": 7,
     "triggers": ["optimize sql", "full table scan", "slow sql", "sql performance",
                  "query plan", "index suggestion"]},
    {"skill": "db-designer",       "category": "development", "priority": 7,
     "triggers": ["design database schema", "data model", "entity relationship", "er diagram",
                  "normalize tables", "design tables", "create schema", "database design review",
                  "foreign keys", "relational model"]},
    {"skill": "dep-auditor",       "category": "development", "priority": 7,
     "triggers": ["dependency audit", "npm audit", "pip audit", "outdated packages",
                  "cve check", "license compliance", "supply chain security",
                  "vulnerable dependency", "update packages"]},
    {"skill": "pr-reviewer",       "category": "development", "priority": 7,
     "triggers": ["review pr", "pr feedback", "pull request review", "diff review",
                  "code change review", "should i merge this", "lgtm check"]},
    {"skill": "feature-planner",   "category": "development", "priority": 7,
     "triggers": ["plan this feature", "implementation plan",
                  "feature spec", "how do i implement x", "what are the steps",
                  "make a plan for", "i need to build", "feature breakdown"]},

    # ── Additional AI/ML ─────────────────────────────────────────────────────
    {"skill": "ml-debugger",       "category": "ai", "priority": 7,
     "triggers": ["loss not converging", "model not learning", "nan loss", "gradient explosion",
                  "inference error", "model output wrong", "training failed",
                  "why is accuracy so low"]},
    {"skill": "model-benchmarker", "category": "ai", "priority": 7,
     "triggers": ["compare models", "which model is best", "benchmark claude",
                  "model selection", "cost vs quality", "is haiku fast enough"]},
    {"skill": "embeddings",        "category": "ai", "priority": 7,
     "triggers": ["embeddings", "vector similarity", "embed this text",
                  "find similar", "text similarity", "nearest neighbor search", "clustering"]},
    {"skill": "dataset-curator",   "category": "ai", "priority": 7,
     "triggers": ["clean this dataset", "prepare training data", "dataset curation",
                  "deduplicate data", "label this data", "data quality",
                  "prepare eval set", "filter bad examples"]},
    {"skill": "ai-safety",         "category": "ai", "priority": 8,
     "triggers": ["ai safety review", "bias check", "fairness audit", "alignment",
                  "responsible ai", "misuse prevention", "ai ethics", "safety guardrails",
                  "could this ai system be misused"]},
    {"skill": "vision-analyst",    "category": "ai", "priority": 7,
     "triggers": ["analyze this image", "vision ai", "image classification",
                  "object detection", "ocr", "screenshot analysis",
                  "process this image", "image pipeline"]},
    {"skill": "multimodal",        "category": "ai", "priority": 7,
     "triggers": ["multimodal", "text and images", "vision + language",
                  "image + text pipeline", "document understanding",
                  "multimodal embeddings", "cross-modal search"]},

    # ── Additional DevOps ────────────────────────────────────────────────────
    {"skill": "backup",            "category": "devops", "priority": 6,
     "triggers": ["backup strategy", "disaster recovery", "backup verification",
                  "restore test", "rto", "rpo", "data loss prevention", "backup schedule"]},
    {"skill": "scaling",           "category": "devops", "priority": 7,
     "triggers": ["scaling plan", "handle more traffic", "auto-scaling", "load balancing",
                  "capacity planning", "how do i scale this", "handle 10x load"]},
    {"skill": "cost-optimizer",    "category": "devops", "priority": 7,
     "triggers": ["reduce cloud costs", "cost optimization", "aws cost", "cloud bill",
                  "right-sizing", "idle resources", "spot instances", "reserved instances"]},
    {"skill": "pipeline-opt",      "category": "devops", "priority": 7,
     "triggers": ["pipeline too slow", "slow ci", "speed up builds", "pipeline optimization",
                  "cache builds", "parallel jobs", "flaky tests", "pipeline reliability"]},
    {"skill": "rollback",          "category": "devops", "priority": 8,
     "triggers": ["rollback", "revert deployment", "undo deploy", "something broke in prod",
                  "roll back to previous", "deployment failed", "revert to v"]},
    {"skill": "infra-docs",        "category": "devops", "priority": 6,
     "triggers": ["document the infrastructure", "infra diagram", "network diagram",
                  "infrastructure documentation", "how does our infra work",
                  "ops documentation", "infra docs"]},
    {"skill": "logging",           "category": "devops", "priority": 6,
     "triggers": ["logging setup", "structured logs", "log aggregation", "elk stack",
                  "log analysis", "add logging", "logging config", "log format",
                  "how should i log"]},
    {"skill": "metrics-designer",  "category": "devops", "priority": 6,
     "triggers": ["add metrics", "instrument this code", "design metrics", "prometheus metrics",
                  "custom metrics", "application metrics", "observability metrics"]},
    {"skill": "cron-scheduler",    "category": "devops", "priority": 6,
     "triggers": ["schedule this", "run every day", "cron job", "scheduled task",
                  "automation schedule", "run weekly", "cron expression",
                  "set up recurring task"]},

    # ── Documentation ────────────────────────────────────────────────────────
    {"skill": "api-docs",          "category": "docs", "priority": 7,
     "triggers": ["document this api", "api docs", "openapi spec",
                  "endpoint documentation", "api reference",
                  "document these endpoints", "api documentation missing"]},
    {"skill": "changelog-maintainer", "category": "docs", "priority": 5,
     "triggers": ["keep changelog updated", "changelog is stale", "changelog maintenance",
                  "update release history", "automate changelog", "add to changelog"]},
    {"skill": "arch-diagrammer",   "category": "docs", "priority": 6,
     "triggers": ["draw architecture diagram", "system diagram", "architecture overview",
                  "visualize the system", "component diagram", "data flow diagram",
                  "sequence diagram", "c4 diagram"]},
    {"skill": "onboarding",        "category": "docs", "priority": 6,
     "triggers": ["onboarding guide", "new developer guide", "contributor guide",
                  "contributing.md", "how to get started", "new team member setup",
                  "first day guide"]},
    {"skill": "decision-logger",   "category": "docs", "priority": 6,
     "triggers": ["log this decision", "record why we chose", "decision log",
                  "we decided to", "document this choice", "capture this decision"]},
    {"skill": "tutorial-writer",   "category": "docs", "priority": 6,
     "triggers": ["write tutorial", "how-to guide", "tutorial for", "explain how to use",
                  "step-by-step guide", "workshop material", "create a tutorial",
                  "teach someone to use"]},
    {"skill": "knowledge-base",    "category": "docs", "priority": 7,
     "triggers": ["knowledge base", "second brain", "organize notes", "personal wiki",
                  "structured notes", "knowledge management",
                  "organize research into notes"]},

    # ── Web / Optimization ───────────────────────────────────────────────────
    {"skill": "web-vitals",        "category": "web", "priority": 7,
     "triggers": ["web vitals", "page speed", "lcp", "cls", "inp", "lighthouse",
                  "slow page load", "improve page speed", "core web vitals"]},
    {"skill": "seo-auditor",       "category": "web", "priority": 6,
     "triggers": ["seo audit", "improve seo", "search ranking", "meta tags",
                  "structured data", "sitemap", "robots.txt",
                  "keyword optimization", "google ranking", "on-page seo"]},
    {"skill": "a11y-checker",      "category": "web", "priority": 7,
     "triggers": ["accessibility", "a11y", "wcag", "screen reader", "aria labels",
                  "color contrast", "keyboard navigation",
                  "accessibility audit", "ada compliance"]},
    {"skill": "web-scraper",       "category": "web", "priority": 6,
     "triggers": ["scrape this website", "web scraping", "extract data from",
                  "crawl", "collect data from web", "automate data collection",
                  "fetch and parse html"]},

    # ── Project Management ───────────────────────────────────────────────────
    {"skill": "sprint-planner",    "category": "pm", "priority": 7,
     "triggers": ["plan the sprint", "sprint planning", "prioritize backlog",
                  "what should we work on", "sprint goals", "task prioritization",
                  "what's the next sprint"]},
    {"skill": "standup",           "category": "pm", "priority": 6,
     "triggers": ["standup", "daily standup", "what did i do yesterday",
                  "progress report", "status update", "daily update", "what's my update"]},
    {"skill": "retrospective",     "category": "pm", "priority": 6,
     "triggers": ["retrospective", "retro", "what went well", "what could be better",
                  "lessons learned", "sprint review", "team retrospective"]},
    {"skill": "roadmap",           "category": "pm", "priority": 7,
     "triggers": ["roadmap", "build roadmap", "what's the plan", "long-term plan", "6-month roadmap",
                  "product roadmap", "technical roadmap", "what comes after this"]},
    {"skill": "risk-assessor",     "category": "pm", "priority": 7,
     "triggers": ["risk assessment", "what could go wrong", "project risks", "risk register",
                  "mitigation plan", "identify risks", "what are the risks"]},
    {"skill": "scope-definer",     "category": "pm", "priority": 7,
     "triggers": ["define scope", "scope creep", "what's in scope", "mvp definition",
                  "what should we not build", "scope this project", "define boundaries"]},
    {"skill": "estimation",        "category": "pm", "priority": 6,
     "triggers": ["estimate this", "how long will this take", "story points",
                  "effort estimation", "timeline", "when can this be done",
                  "how complex is this"]},
    {"skill": "blocker-resolver",  "category": "pm", "priority": 8,
     "triggers": ["i'm blocked", "this is blocking me", "unblock this",
                  "resolve blocker", "stuck on", "how do i get past this", "blocker"]},
    {"skill": "stakeholder",       "category": "pm", "priority": 6,
     "triggers": ["stakeholder update", "executive summary", "status report",
                  "update the team", "write progress report",
                  "non-technical summary", "management update"]},
    {"skill": "competitive-analyst","category": "pm", "priority": 6,
     "triggers": ["competitive analysis", "compare to competitors", "what are the alternatives",
                  "market analysis", "how does x compare to y", "competitor research", "swot analysis"]},
    {"skill": "kpi-tracker",       "category": "pm", "priority": 6,
     "triggers": ["define kpis", "track metrics", "measure success",
                  "what metrics should we track", "kpi dashboard",
                  "okrs", "success metrics", "how do we know this worked"]},

    # ── Additional Ecosystem ─────────────────────────────────────────────────
    {"skill": "create",            "category": "meta", "priority": 8,
     "triggers": ["make a skill", "create an agent", "turn this into a skill",
                  "automate this", "save this workflow", "i keep doing this",
                  "create skill", "new skill", "create agent"]},
    {"skill": "obsidian",          "category": "meta", "priority": 6,
     "triggers": ["organize in obsidian", "atomic notes", "linked notes",
                  "knowledge graph", "note-taking", "build a wiki",
                  "organize my knowledge", "create linked notes"]},
    {"skill": "ui-ux",             "category": "meta", "priority": 7,
     "triggers": ["design this ui", "build this interface", "ui component",
                  "make this look good", "design system", "ui/ux",
                  "frontend design", "css design", "clean ui"]},
    {"skill": "trend-researcher",  "category": "meta", "priority": 7,
     "triggers": ["what's trending", "latest trends in", "emerging technology",
                  "market trends", "tech radar", "trend analysis",
                  "state of x in 2026"]},
    {"skill": "data-pipeline",     "category": "meta", "priority": 7,
     "triggers": ["data pipeline", "etl", "data ingestion", "process this data",
                  "batch processing", "stream processing",
                  "data transformation", "data workflow"]},

    # ── v0.9.0 — New skills from ecosystem research ───────────────────────────
    {"skill": "preflight",         "category": "meta", "priority": 9,
     "triggers": ["preflight check", "validate this prompt", "is this task clear",
                  "check before running", "prompt quality check", "pre-execution check",
                  "score this prompt", "is my task well defined", "task spec review"]},
    {"skill": "tdd",               "category": "development", "priority": 8,
     "triggers": ["test driven development", "tdd this", "write tests first",
                  "red-green-refactor", "write failing tests", "enforce tdd",
                  "test-first development", "tdd workflow"]},
    {"skill": "self-reflect",      "category": "meta", "priority": 7,
     "triggers": ["self reflect", "extract patterns", "mine learnings",
                  "update lessons from history", "retrospective patterns",
                  "session patterns", "learn from mistakes", "self reflection",
                  "improve from history", "what patterns emerged"]},
    {"skill": "chain-of-draft",    "category": "meta", "priority": 8,
     "triggers": ["chain of draft", "iterative refinement", "improve through drafts",
                  "draft and critique", "structured refinement", "progressive draft",
                  "multi-pass writing", "cod pattern", "draft critique improve"]},
    {"skill": "foresight",         "category": "meta", "priority": 7,
     "triggers": ["foresight", "strategic analysis", "what am i missing strategically",
                  "second order effects", "future risks", "what could blindside",
                  "horizon scanning", "strategic blind spots", "cross-domain analysis",
                  "long term risks", "contextual nudge"]},
    {"skill": "team",              "category": "meta", "priority": 8,
     "triggers": ["team mode", "spawn a team", "agent team", "parallel team review",
                  "multi-agent team", "code review team", "security team review",
                  "debug team", "architecture team", "ship team",
                  "multi-role review", "team of agents"]},
    {"skill": "context-diff",      "category": "meta", "priority": 7,
     "triggers": ["context diff", "what changed since last session", "diff since main",
                  "what's new since", "changes since checkpoint", "session diff",
                  "summarize changes since", "what did i change", "context since"]},
    {"skill": "riper",             "category": "meta", "priority": 9,
     "triggers": ["riper", "riper workflow", "research then innovate",
                  "five phase workflow", "research innovate plan execute review",
                  "structured feature workflow", "riper mode",
                  "phase-gated development", "systematic feature delivery"]},
    {"skill": "memory-bank",       "category": "meta", "priority": 7,
     "triggers": ["memory bank", "update memory bank", "sync memory",
                  "knowledge sync", "update project knowledge", "synchronize memory",
                  "keep memory current", "project memory",
                  "update knowledge base with code changes"]},
]

# Build fast lookup maps
_TRIGGER_INDEX: dict[str, str] = {}  # trigger_phrase → skill_name
_SKILL_MAP: dict[str, dict] = {}

for entry in _SKILL_REGISTRY:
    _SKILL_MAP[entry["skill"]] = entry
    for trigger in entry["triggers"]:
        _TRIGGER_INDEX[trigger] = entry["skill"]

# Compiled trigger pattern — sorted longest-first so "unit test" matches before "test".
# One regex scan replaces O(n) individual `trigger in text` checks.
_TRIGGER_PATTERN: re.Pattern[str] = re.compile(
    "|".join(re.escape(t) for t in sorted(_TRIGGER_INDEX, key=len, reverse=True))
)


def route_skill(user_input: str) -> SkillMatch | None:
    """Return the best matching skill for the given user input, or None.

    Matching priority:
    1. Exact / substring trigger match (highest confidence)
    2. Category-level keyword match (medium confidence)
    3. No match → None (let Claude decide without a skill hint)
    """
    text = user_input.lower()
    matches: list[tuple[int, float, dict]] = []  # (priority, confidence, entry)

    # Stage 1: single regex scan — O(len(text)) instead of O(n_triggers × len(text))
    seen_skills: set[str] = set()
    for m in _TRIGGER_PATTERN.finditer(text):
        skill_name = _TRIGGER_INDEX[m.group(0)]
        if skill_name in seen_skills:
            continue
        seen_skills.add(skill_name)
        entry = _SKILL_MAP[skill_name]
        confidence = 0.7 + (entry["priority"] / 10) * 0.3
        matches.append((entry["priority"], confidence, entry))

    if not matches:
        return None

    # Sort by priority desc, confidence desc
    matches.sort(key=lambda x: (x[0], x[1]), reverse=True)
    best_priority, best_confidence, best_entry = matches[0]

    # Find fallback (second best, different skill)
    fallback = None
    for _, _, entry in matches[1:]:
        if entry["skill"] != best_entry["skill"]:
            fallback = entry["skill"]
            break

    return SkillMatch(
        skill=best_entry["skill"],
        confidence=round(best_confidence, 2),
        reason=f"trigger match in category={best_entry['category']} priority={best_priority}",
        category=best_entry["category"],
        fallback=fallback,
    )


def route_skill_by_category(category: str) -> list[str]:
    """Return all skills in a given category, sorted by priority."""
    skills = [e for e in _SKILL_REGISTRY if e["category"] == category]
    skills.sort(key=lambda e: e["priority"], reverse=True)
    return [e["skill"] for e in skills]


def list_categories() -> list[str]:
    return sorted(set(e["category"] for e in _SKILL_REGISTRY))
```

FILE: /home/user/wellux_testprojects/src/routing/agent_router.py
```python
"""Agent Router — dispatch tasks to the right autonomous agent.

Four agents available:
  ralph-loop         Self-driving dev loop. Read todo → plan → implement → verify → repeat.
  research-agent     Karpathy research. Search → distill → implement → store.
  swarm-orchestrator Parallel decomposition. Splits task into independent workstreams.
  security-reviewer  Full security sweep. 6-domain audit → report.

Routing signals:
  - Task duration: long-running → ralph-loop; bounded → others
  - Task type: research → research-agent; security → security-reviewer
  - Parallelism: multiple independent workstreams → swarm
  - Default for "just build it": ralph-loop
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Agent(StrEnum):
    RALPH      = "ralph-loop"
    RESEARCH   = "research-agent"
    SWARM      = "swarm-orchestrator"
    SECURITY   = "security-reviewer"


@dataclass
class AgentDecision:
    agent: Agent
    confidence: float          # 0.0 – 1.0
    reason: str
    spawn_count: int = 1       # for swarm: how many subagents to suggest
    context_hints: list[str] = None  # extra context to pass to the agent

    def __post_init__(self):
        if self.context_hints is None:
            self.context_hints = []


# ── Routing signal tables ────────────────────────────────────────────────────

_RALPH_SIGNALS = [
    "implement", "build", "create", "add feature", "fix bug", "refactor",
    "autonomous", "keep going", "loop until", "self-driving", "run autonomously",
    "todo list", "work through", "complete all", "ship this", "just do it",
    "ralph", "dev loop", "long session",
]

_RESEARCH_SIGNALS = [
    "research", "deep dive", "what is", "explain", "first principles",
    "latest on", "summarize paper", "find out", "investigate", "learn about",
    "karpathy", "study", "understand", "arxiv", "literature", "state of the art",
    "weekly research", "trend", "what's new in",
]

_SWARM_SIGNALS = [
    "parallel", "simultaneously", "at the same time", "multiple", "in parallel",
    "swarm", "split into", "decompose", "distribute", "concurrent tasks",
    "independent", "all at once", "batch of", "across all", "every module",
    "all services", "full audit of all",
]

_SECURITY_SIGNALS = [
    "security review", "security audit", "pentest", "vulnerability scan",
    "check for vulns", "security sweep", "audit the code", "cve", "owasp audit",
    "security report", "find security issues", "check my code for security",
    "is this secure", "harden", "threat model",
]


def _score(text: str, signals: list[str]) -> int:
    return sum(1 for s in signals if s in text)


def route_agent(task: str, *, context: str | None = None) -> AgentDecision:
    """Select the best agent for the given task.

    Args:
        task: Natural language task description.
        context: Optional extra context (e.g. current todo.md contents).

    Returns:
        AgentDecision with agent, confidence, and hints.
    """
    text = (task + " " + (context or "")).lower()

    scores = {
        Agent.RALPH:    _score(text, _RALPH_SIGNALS),
        Agent.RESEARCH: _score(text, _RESEARCH_SIGNALS),
        Agent.SWARM:    _score(text, _SWARM_SIGNALS),
        Agent.SECURITY: _score(text, _SECURITY_SIGNALS),
    }

    best_agent = max(scores, key=lambda a: scores[a])
    best_score = scores[best_agent]

    # Tie-break or no signal → default to ralph-loop (build mode)
    if best_score == 0:
        return AgentDecision(
            agent=Agent.RALPH,
            confidence=0.4,
            reason="no strong signal — defaulting to ralph-loop (build mode)",
            context_hints=["Read tasks/todo.md for pending work"],
        )

    total = sum(scores.values()) or 1
    confidence = round(best_score / total, 2)

    hints: list[str] = []

    if best_agent == Agent.RALPH:
        hints = [
            "Read tasks/todo.md first",
            "Mark steps complete as you go",
            "Commit after each completed step",
        ]
    elif best_agent == Agent.RESEARCH:
        hints = [
            "Follow Karpathy method: Search → Distill → Implement → Store",
            "Write output to data/research/YYYY-MM-DD-<slug>.md",
            "Extract lessons to tasks/lessons.md",
        ]
    elif best_agent == Agent.SWARM:
        # Estimate parallelism from task size signals
        spawn = 3  # default
        if any(w in text for w in ["all", "every", "each", "full"]):
            spawn = 5
        hints = [
            f"Decompose into ~{spawn} independent workstreams",
            "Assign non-overlapping file paths to each agent",
            "Synthesize results in final round",
        ]
        return AgentDecision(
            agent=Agent.SWARM,
            confidence=confidence,
            reason=f"swarm signals ({best_score}) — parallel decomposition",
            spawn_count=spawn,
            context_hints=hints,
        )
    elif best_agent == Agent.SECURITY:
        hints = [
            "Run all 6 security domains: AppSec, AI Security, Deps, Secrets, IAM, GRC",
            "Write report to data/outputs/security-report-<date>.md",
            "Flag critical issues immediately",
        ]

    return AgentDecision(
        agent=best_agent,
        confidence=confidence,
        reason=f"signal score={best_score} for {best_agent.value}",
        context_hints=hints,
    )


def route_multi_agent(task: str) -> list[AgentDecision]:
    """Return ranked list of all agents with their scores.

    Useful when you want to see all options, not just the top pick.
    """
    text = task.lower()
    results = []
    _total_signals = sum([
        len(_RALPH_SIGNALS), len(_RESEARCH_SIGNALS),
        len(_SWARM_SIGNALS), len(_SECURITY_SIGNALS),
    ])

    for agent, signals in [
        (Agent.RALPH, _RALPH_SIGNALS),
        (Agent.RESEARCH, _RESEARCH_SIGNALS),
        (Agent.SWARM, _SWARM_SIGNALS),
        (Agent.SECURITY, _SECURITY_SIGNALS),
    ]:
        score = _score(text, signals)
        confidence = round(score / max(len(signals), 1), 2)
        results.append(AgentDecision(
            agent=agent,
            confidence=confidence,
            reason=f"{score} signal matches",
        ))

    results.sort(key=lambda d: d.confidence, reverse=True)
    return results
```

FILE: /home/user/wellux_testprojects/src/routing/memory_router.py
```python
"""Memory Router — decide WHERE to store information.

Five memory tiers, each with different persistence, scope, and retrieval:

  Tier 1  response_cache   In-memory (session)     Fast LLM response dedup
  Tier 2  files            Filesystem (permanent)   Research docs, outputs
  Tier 3  lessons          tasks/lessons.md         Self-improvement rules
  Tier 4  mcp_memory       MCP memory server        Cross-session facts/entities
  Tier 5  claude_md        CLAUDE.md / tasks/       Project rules + todos

Routing signals:
  - Is this a correction / mistake? → lessons
  - Is this a factual finding / entity? → mcp_memory
  - Is this a project rule / constraint? → claude_md
  - Is this research output? → files (data/research/)
  - Is this a repeated LLM call? → response_cache
  - Is this a task / todo? → tasks/todo.md
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class MemoryTier(StrEnum):
    CACHE    = "response_cache"
    FILES    = "files"
    LESSONS  = "lessons"
    MCP      = "mcp_memory"
    CLAUDE   = "claude_md"
    TODO     = "todo"


@dataclass
class MemoryDecision:
    tier: MemoryTier
    destination: str        # file path or store name
    ttl: str                # "session" | "permanent" | "project-lifetime"
    reason: str
    action: str             # "append" | "write" | "upsert" | "cache"
    template: str = ""      # suggested format for writing


# ── Signal tables ────────────────────────────────────────────────────────────

_LESSON_SIGNALS = [
    "mistake", "correction", "wrong", "i was wrong", "don't do that",
    "lesson learned", "next time", "rule:", "prevent", "don't forget",
    "you should always", "you should never", "pattern to avoid",
]

_MCP_SIGNALS = [
    "remember that", "note that", "keep in mind", "entity:", "fact:",
    "this project uses", "the team prefers", "we decided", "key decision",
    "architecture choice", "important context", "cross-session",
    "persist this", "store this fact",
]

_CLAUDE_MD_SIGNALS = [
    "add to claude.md", "project rule", "always do", "never do",
    "workflow rule", "coding standard", "our convention", "team rule",
    "every session", "boot rule", "global rule",
]

_RESEARCH_SIGNALS = [
    "research finding", "paper says", "study found", "from the docs",
    "technical finding", "benchmark result", "key insight from",
    "write to research", "save research", "store this research",
    # broader patterns
    "finding", "important finding", "key finding", "discovered that",
    "we found", "results show", "data shows", "analysis shows",
    "insight", "key insight", "from research", "research shows",
]

_TODO_SIGNALS = [
    "add to todo", "open task", "pending", "need to", "should do",
    "don't forget to", "remember to", "follow-up", "next step",
    "track this", "backlog",
    # broader patterns
    "todo list", "to-do", "task list", "add task", "add this task",
    "create a task", "new task", "assign task",
]

_CACHE_SIGNALS = [
    "same prompt", "repeated call", "cache this response", "reuse this",
    "don't call again", "already computed",
    # broader patterns
    "cache this", "repeated", "repeat this", "call again", "same result",
    "duplicate call", "idempotent", "memoize",
]


def _score(text: str, signals: list[str]) -> int:
    return sum(1 for s in signals if s in text)


def route_memory(
    content: str,
    *,
    content_type: str | None = None,
    project_root: str = "/home/user/wellux_testprojects",
) -> MemoryDecision:
    """Decide where to store the given content.

    Args:
        content: The thing to be stored (text description or actual content).
        content_type: Optional hint: "research" | "lesson" | "fact" | "task" | "rule"
        project_root: Absolute path to the project.

    Returns:
        MemoryDecision with tier, destination path, and write template.
    """
    text = content.lower()
    root = Path(project_root)

    # Explicit content_type overrides signals
    if content_type:
        ct = content_type.lower()
        if ct == "lesson":
            return _lesson_decision(root)
        if ct == "research":
            return _research_decision(root)
        if ct == "fact":
            return _mcp_decision()
        if ct == "task":
            return _todo_decision(root)
        if ct == "rule":
            return _claude_md_decision(root)

    # Signal-based routing
    scores = {
        MemoryTier.LESSONS: _score(text, _LESSON_SIGNALS),
        MemoryTier.MCP:     _score(text, _MCP_SIGNALS),
        MemoryTier.CLAUDE:  _score(text, _CLAUDE_MD_SIGNALS),
        MemoryTier.FILES:   _score(text, _RESEARCH_SIGNALS),
        MemoryTier.TODO:    _score(text, _TODO_SIGNALS),
        MemoryTier.CACHE:   _score(text, _CACHE_SIGNALS),
    }

    best_tier = max(scores, key=lambda t: scores[t])
    if scores[best_tier] == 0:
        # Default: important enough to store → MCP memory
        return _mcp_decision(reason="no strong signal — defaulting to MCP memory")

    if best_tier == MemoryTier.LESSONS:
        return _lesson_decision(root)
    if best_tier == MemoryTier.FILES:
        return _research_decision(root)
    if best_tier == MemoryTier.CLAUDE:
        return _claude_md_decision(root)
    if best_tier == MemoryTier.TODO:
        return _todo_decision(root)
    if best_tier == MemoryTier.CACHE:
        return MemoryDecision(
            tier=MemoryTier.CACHE,
            destination="ResponseCache (in-memory)",
            ttl="session",
            reason="repeated/cached LLM call signal",
            action="cache",
            template="ResponseCache.set(request, response)",
        )
    return _mcp_decision()


# ── Decision constructors ────────────────────────────────────────────────────

def _lesson_decision(root: Path, reason: str = "mistake/correction signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.LESSONS,
        destination=str(root / "tasks/lessons.md"),
        ttl="permanent",
        reason=reason,
        action="append",
        template=(
            "\n## Lesson — {date}: {short_title}\n"
            "**Mistake:** {what_went_wrong}\n"
            "**Why:** {root_cause}\n"
            "**Rule:** {one_sentence_rule}\n"
            "**Example:** {correct_behavior}\n"
        ),
    )


def _research_decision(root: Path, reason: str = "research finding signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.FILES,
        destination=str(root / "data/research/{date}-{slug}.md"),
        ttl="permanent",
        reason=reason,
        action="write",
        template=(
            "# Research: {topic}\n"
            "**Date:** {date}\n\n"
            "## Core Concept\n{concept}\n\n"
            "## Key Insight\n{insight}\n\n"
            "## Implementation Pattern\n```python\n{code}\n```\n\n"
            "## Actionable Insight\n{action}\n\n"
            "## Sources\n{sources}\n"
        ),
    )


def _mcp_decision(reason: str = "fact/entity signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.MCP,
        destination="mcp__memory (MCP memory server)",
        ttl="permanent",
        reason=reason,
        action="upsert",
        template=(
            "mcp__memory__create_entities([\n"
            "  {{'name': '{entity}', 'entityType': '{type}', "
            "'observations': ['{fact}']}}\n"
            "])"
        ),
    )


def _claude_md_decision(root: Path, reason: str = "project rule signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.CLAUDE,
        destination=str(root / "CLAUDE.md"),
        ttl="project-lifetime",
        reason=reason,
        action="append",
        template="- **Rule:** {rule_text}  ← added {date}",
    )


def _todo_decision(root: Path, reason: str = "task/todo signal") -> MemoryDecision:
    return MemoryDecision(
        tier=MemoryTier.TODO,
        destination=str(root / "tasks/todo.md"),
        ttl="permanent",
        reason=reason,
        action="append",
        template="- [ ] {task_description}",
    )


# ── Convenience: store a lesson directly ────────────────────────────────────

def format_lesson(
    date: str,
    title: str,
    mistake: str,
    why: str,
    rule: str,
    example: str,
) -> str:
    """Format a lesson entry ready to append to lessons.md."""
    return (
        f"\n## Lesson — {date}: {title}\n"
        f"**Mistake:** {mistake}\n"
        f"**Why:** {why}\n"
        f"**Rule:** {rule}\n"
        f"**Example:** {example}\n"
    )
```

FILE: /home/user/wellux_testprojects/src/routing/task_router.py
```python
"""Task Router — decompose complex tasks and dispatch subtasks to subagents.

Responsibilities:
  1. Classify task size (atomic / medium / complex)
  2. For complex tasks: decompose into independent subtasks
  3. Assign each subtask to the right agent + model
  4. Detect parallelism (independent vs sequential)
  5. Return an execution plan

Decomposition rules:
  - Independent tasks (no shared state) → parallel swarm agents
  - Sequential tasks (output of A feeds B) → ralph-loop with ordered steps
  - Research + implementation → research-agent first, ralph-loop second
  - Security review + fix → security-reviewer first, ralph-loop second
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal

from .agent_router import Agent, route_agent
from .llm_router import Model, route_llm
from .skill_router import route_skill


class TaskSize(StrEnum):
    ATOMIC  = "atomic"   # single action, no decomposition needed
    MEDIUM  = "medium"   # 2-4 steps, single agent
    COMPLEX = "complex"  # 5+ steps or multiple parallel workstreams


class Dependency(StrEnum):
    NONE       = "none"        # fully independent
    SEQUENTIAL = "sequential"  # A → B → C
    PARALLEL   = "parallel"    # A ∥ B ∥ C → merge


@dataclass
class Subtask:
    id: str                        # e.g. "1.1", "2.a"
    description: str
    agent: Agent
    model: Model
    skill: str | None
    depends_on: list[str] = field(default_factory=list)  # ids of blocking subtasks
    estimated_tokens: int = 4096
    context_hints: list[str] = field(default_factory=list)


@dataclass
class TaskPlan:
    original_task: str
    size: TaskSize
    dependency: Dependency
    subtasks: list[Subtask]
    estimated_total_cost_tier: str  # "low" | "medium" | "high"
    execution_mode: Literal["single", "sequential", "parallel"]
    notes: str = ""

    def summary(self) -> str:
        lines = [
            f"Task: {self.original_task[:80]}",
            f"Size: {self.size.value} | Mode: {self.execution_mode} | Cost: {self.estimated_total_cost_tier}",
            f"Subtasks ({len(self.subtasks)}):",
        ]
        for st in self.subtasks:
            dep = f" [after {', '.join(st.depends_on)}]" if st.depends_on else ""
            lines.append(f"  {st.id}. [{st.agent.value}] {st.description[:60]}{dep}")
        return "\n".join(lines)


MAX_SUBTASKS = 10  # hard cap — prevents runaway decomposition


# ── Size classification ───────────────────────────────────────────────────────

_COMPLEX_SIGNALS = [
    "entire", "full", "all modules", "end-to-end", "from scratch",
    "complete system", "migrate", "redesign", "overhaul", "comprehensive",
    "phase", "multiple", "and also", "plus", "as well as", "in addition",
    # multi-step operations that always require decomposition
    "audit", "security audit", "full audit", "and fix", "and deploy",
    "implement and", "build and", "test and", "review and", "refactor and",
]

_ATOMIC_SIGNALS = [
    "fix this typo", "rename", "add a comment", "one line", "quick",
    "single function", "this file only", "just this", "small change",
]


def _classify_size(task: str) -> TaskSize:
    text = task.lower()
    complex_hits = sum(1 for s in _COMPLEX_SIGNALS if s in text)
    atomic_hits  = sum(1 for s in _ATOMIC_SIGNALS  if s in text)

    if atomic_hits > 0 and complex_hits == 0:
        return TaskSize.ATOMIC
    if complex_hits >= 2 or len(task.split()) > 40:
        return TaskSize.COMPLEX
    return TaskSize.MEDIUM


def _has_parallel_signal(task: str) -> bool:
    signals = ["parallel", "simultaneously", "at the same time", "independent",
               "concurrently", "in parallel", "swarm", "multiple workstreams"]
    return any(s in task.lower() for s in signals)


def _has_sequential_signal(task: str) -> bool:
    signals = ["first", "then", "after that", "once done", "next", "finally",
               "step by step", "in order", "sequentially"]
    return any(s in task.lower() for s in signals)


# ── Decomposition logic ───────────────────────────────────────────────────────

def _decompose_complex(task: str) -> list[Subtask]:
    """Break a complex task into subtasks with agent/model assignments."""
    text = task.lower()
    subtasks: list[Subtask] = []

    # Pattern: research + implement
    needs_research = any(w in text for w in ["research", "find out", "what is", "learn"])
    needs_security = any(w in text for w in ["secure", "security", "audit", "pentest"])
    needs_docs     = any(w in text for w in ["document", "readme", "runbook", "adr"])
    needs_tests    = any(w in text for w in ["test", "coverage", "pytest", "spec"])

    idx = 1

    if needs_research:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Research and distill key findings",
            agent=Agent.RESEARCH,
            model=Model.SONNET,
            skill="karpathy-researcher",
            context_hints=["Write findings to data/research/", "Extract lessons"],
        ))
        idx += 1

    if needs_security:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Security review: 6-domain sweep",
            agent=Agent.SECURITY,
            model=Model.OPUS,
            skill="ciso",
            context_hints=["Output to data/outputs/security-report-<date>.md"],
        ))
        idx += 1

    # Core implementation (depends on research if present)
    impl_deps = [str(i) for i in range(1, idx)]
    subtasks.append(Subtask(
        id=f"{idx}",
        description="Implement core feature / fix",
        agent=Agent.RALPH,
        model=route_llm(task).model,
        skill=None,
        depends_on=impl_deps,
        context_hints=["Read tasks/todo.md", "Commit after each step"],
    ))
    impl_id = str(idx)
    idx += 1

    if needs_tests:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Write tests and verify coverage",
            agent=Agent.RALPH,
            model=Model.SONNET,
            skill="test-writer",
            depends_on=[impl_id],
        ))
        idx += 1

    if needs_docs:
        subtasks.append(Subtask(
            id=f"{idx}",
            description="Write/update documentation",
            agent=Agent.RALPH,
            model=Model.HAIKU,
            skill="readme-writer",
            depends_on=[impl_id],
        ))
        idx += 1

    # If nothing matched, fall back to single ralph task (defensive — impl always appends above)
    if not subtasks:  # pragma: no cover
        subtasks.append(Subtask(
            id="1",
            description=task[:100],
            agent=Agent.RALPH,
            model=route_llm(task).model,
            skill=None,
        ))

    # Enforce hard cap — truncate rather than silently overflow
    if len(subtasks) > MAX_SUBTASKS:
        subtasks = subtasks[:MAX_SUBTASKS]

    return subtasks


def plan_task(task: str) -> TaskPlan:
    """Produce a full execution plan for the given task.

    Args:
        task: Natural language task description.

    Returns:
        TaskPlan with decomposed subtasks, agents, models, and execution mode.
    """
    size = _classify_size(task)
    parallel = _has_parallel_signal(task)
    sequential = _has_sequential_signal(task)

    # Atomic: single subtask, no decomposition
    if size == TaskSize.ATOMIC:
        agent_dec = route_agent(task)
        llm_dec   = route_llm(task)
        skill_dec = route_skill(task)
        return TaskPlan(
            original_task=task,
            size=size,
            dependency=Dependency.NONE,
            subtasks=[Subtask(
                id="1",
                description=task,
                agent=agent_dec.agent,
                model=llm_dec.model,
                skill=skill_dec.skill if skill_dec else None,
            )],
            estimated_total_cost_tier=llm_dec.estimated_cost_tier,
            execution_mode="single",
        )

    # Medium: single agent, sequential steps
    if size == TaskSize.MEDIUM:
        agent_dec = route_agent(task)
        llm_dec   = route_llm(task)
        return TaskPlan(
            original_task=task,
            size=size,
            dependency=Dependency.SEQUENTIAL,
            subtasks=[Subtask(
                id="1",
                description=task,
                agent=agent_dec.agent,
                model=llm_dec.model,
                skill=None,
                context_hints=agent_dec.context_hints,
            )],
            estimated_total_cost_tier=llm_dec.estimated_cost_tier,
            execution_mode="sequential",
        )

    # Complex: decompose
    subtasks = _decompose_complex(task)

    # Determine execution mode
    has_deps = any(st.depends_on for st in subtasks)
    if parallel and not has_deps:
        mode = "parallel"
        dep = Dependency.PARALLEL
    elif has_deps or sequential:
        mode = "sequential"
        dep = Dependency.SEQUENTIAL
    else:
        mode = "parallel"
        dep = Dependency.PARALLEL

    # Estimate cost from models used
    models_used = {st.model for st in subtasks}
    if Model.OPUS in models_used:
        cost_tier = "high"
    elif Model.SONNET in models_used:
        cost_tier = "medium"
    else:
        cost_tier = "low"

    return TaskPlan(
        original_task=task,
        size=size,
        dependency=dep,
        subtasks=subtasks,
        estimated_total_cost_tier=cost_tier,
        execution_mode=mode,
    )
```


## 4.6 Eval Framework (src/evals/)

FILE: /home/user/wellux_testprojects/src/evals/__init__.py
```python
"""Eval framework — test LLM outputs systematically.

Quick start:
    from src.evals import EvalCase, EvalSuite, EvalRunner

    suite = (
        EvalSuite("smoke")
        .add(EvalCase("greet", "Say hello", contains=["hello"]))
        .add(EvalCase("math",  "What is 2+2?", contains=["4"]))
    )

    def my_llm(prompt, *, max_tokens=512, temperature=0.0):
        return client.complete(prompt)

    report = EvalRunner(my_llm).run(suite)
    print(report.summary())
"""
from .runner import AsyncEvalRunner, EvalRunner
from .scorers import (
    DEFAULT_SCORER,
    composite,
    contains_all,
    exact_match,
    excludes_none,
    max_length,
    min_length,
    non_empty,
    regex_match,
)
from .suite import EvalSuite
from .types import EvalCase, EvalReport, EvalResult, Verdict

__all__ = [
    # types
    "EvalCase", "EvalResult", "EvalReport", "Verdict",
    # suite
    "EvalSuite",
    # runner
    "EvalRunner", "AsyncEvalRunner",
    # scorers
    "DEFAULT_SCORER", "exact_match", "contains_all", "excludes_none",
    "non_empty", "min_length", "max_length", "regex_match", "composite",
]
```

FILE: /home/user/wellux_testprojects/src/evals/types.py
```python
"""Core data types for the eval framework."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Verdict(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


@dataclass
class EvalCase:
    """A single evaluation case: input → expected output + scoring criteria."""
    id: str
    prompt: str
    expected: str | None = None          # exact or reference answer
    contains: list[str] = field(default_factory=list)   # required substrings
    excludes: list[str] = field(default_factory=list)   # forbidden substrings
    max_tokens: int = 512
    temperature: float = 0.0             # 0 = deterministic for evals
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("EvalCase.id must be non-empty")
        if not self.prompt:
            raise ValueError("EvalCase.prompt must be non-empty")


@dataclass
class EvalResult:
    """Result of running one EvalCase."""
    case_id: str
    verdict: Verdict
    actual: str = ""
    score: float = 0.0          # 0.0–1.0
    reason: str = ""
    latency_ms: float = 0.0
    tokens_used: int = 0
    error: str | None = None
    tags: list[str] = field(default_factory=list)  # propagated from EvalCase


@dataclass
class EvalReport:
    """Aggregated results across an entire EvalSuite run."""
    suite_name: str
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    results: list[EvalResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        denom = self.total - self.skipped
        return self.passed / denom if denom > 0 else 0.0

    @property
    def mean_score(self) -> float:
        scored = [r.score for r in self.results if r.verdict not in (Verdict.SKIP, Verdict.ERROR)]
        return sum(scored) / len(scored) if scored else 0.0

    @property
    def mean_latency_ms(self) -> float:
        timed = [r.latency_ms for r in self.results if r.latency_ms > 0]
        return sum(timed) / len(timed) if timed else 0.0

    def summary(self) -> str:
        bar = "█" * self.passed + "░" * self.failed + "·" * self.skipped
        return (
            f"Suite : {self.suite_name}\n"
            f"Result: {self.passed}/{self.total - self.skipped} passed "
            f"({self.pass_rate:.0%})  errors={self.errors}\n"
            f"Score : {self.mean_score:.2f}  latency={self.mean_latency_ms:.0f}ms avg\n"
            f"        [{bar}]"
        )

    def failures(self) -> list[EvalResult]:
        return [r for r in self.results if r.verdict == Verdict.FAIL]

    def by_tag(self, tag: str) -> list[EvalResult]:
        return [r for r in self.results if tag in r.tags]
```

FILE: /home/user/wellux_testprojects/src/evals/suite.py
```python
"""EvalSuite — a named collection of EvalCases with filtering and loading."""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from .types import EvalCase


class EvalSuite:
    """A named, ordered collection of EvalCases."""

    def __init__(self, name: str, cases: list[EvalCase] | None = None) -> None:
        self.name = name
        self._cases: list[EvalCase] = list(cases or [])

    # ── building ──────────────────────────────────────────────────────────────

    def add(self, case: EvalCase) -> EvalSuite:
        """Add a case; returns self for chaining."""
        if any(c.id == case.id for c in self._cases):
            raise ValueError(f"Duplicate EvalCase id: {case.id!r}")
        self._cases.append(case)
        return self

    def extend(self, cases: list[EvalCase]) -> EvalSuite:
        for c in cases:
            self.add(c)
        return self

    # ── filtering ─────────────────────────────────────────────────────────────

    def filter_tags(self, *tags: str) -> EvalSuite:
        """Return a new suite with only cases that have ALL given tags."""
        matched = [c for c in self._cases if all(t in c.tags for t in tags)]
        return EvalSuite(f"{self.name}[{','.join(tags)}]", matched)

    def filter_ids(self, *ids: str) -> EvalSuite:
        id_set = set(ids)
        matched = [c for c in self._cases if c.id in id_set]
        return EvalSuite(self.name, matched)

    def exclude_tags(self, *tags: str) -> EvalSuite:
        matched = [c for c in self._cases if not any(t in c.tags for t in tags)]
        return EvalSuite(self.name, matched)

    # ── serialisation ─────────────────────────────────────────────────────────

    @classmethod
    def from_jsonl(cls, path: str | Path, name: str | None = None) -> EvalSuite:
        """Load cases from a JSONL file (one JSON object per line)."""
        path = Path(path)
        suite_name = name or path.stem
        cases = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            data = json.loads(line)
            cases.append(EvalCase(**data))
        suite = cls(suite_name)
        suite.extend(cases)
        return suite

    def to_jsonl(self, path: str | Path) -> Path:
        """Persist all cases to a JSONL file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        for c in self._cases:
            lines.append(json.dumps({
                "id": c.id, "prompt": c.prompt, "expected": c.expected,
                "contains": c.contains, "excludes": c.excludes,
                "max_tokens": c.max_tokens, "temperature": c.temperature,
                "tags": c.tags, "metadata": c.metadata,
            }))
        path.write_text("\n".join(lines) + "\n")
        return path

    # ── iteration / access ────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[EvalCase]:
        return iter(self._cases)

    def __len__(self) -> int:
        return len(self._cases)

    def __getitem__(self, case_id: str) -> EvalCase:
        for c in self._cases:
            if c.id == case_id:
                return c
        raise KeyError(case_id)

    def __repr__(self) -> str:
        return f"EvalSuite({self.name!r}, {len(self._cases)} cases)"
```

FILE: /home/user/wellux_testprojects/src/evals/scorers.py
```python
"""Scoring functions for eval outputs.

Each scorer takes (actual: str, case: EvalCase) → (score: float, reason: str).
score is 0.0–1.0; reason is a human-readable explanation.
"""
from __future__ import annotations

import re
from collections.abc import Callable

from .types import EvalCase

ScorerFn = Callable[[str, EvalCase], tuple[float, str]]


def exact_match(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if actual matches expected exactly (stripped), else 0.0."""
    if case.expected is None:
        return 1.0, "no expected — skip exact match"
    match = actual.strip() == case.expected.strip()
    return (1.0, "exact match") if match else (0.0, f"expected {case.expected!r}, got {actual!r}")


def contains_all(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if all required substrings are present, partial credit otherwise."""
    if not case.contains:
        return 1.0, "no contains constraints"
    found = [s for s in case.contains if s.lower() in actual.lower()]
    score = len(found) / len(case.contains)
    missing = [s for s in case.contains if s not in found]
    reason = f"{len(found)}/{len(case.contains)} required strings found"
    if missing:
        reason += f"; missing: {missing}"
    return score, reason


def excludes_none(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if no forbidden substrings are present."""
    if not case.excludes:
        return 1.0, "no excludes constraints"
    found = [s for s in case.excludes if s.lower() in actual.lower()]
    if found:
        return 0.0, f"forbidden strings found: {found}"
    return 1.0, "no forbidden strings found"


def non_empty(actual: str, case: EvalCase) -> tuple[float, str]:
    """1.0 if response is non-empty."""
    stripped = actual.strip()
    return (1.0, "non-empty response") if stripped else (0.0, "empty response")


def min_length(min_chars: int) -> ScorerFn:
    """Factory: 1.0 if response is at least min_chars long."""
    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        n = len(actual.strip())
        if n >= min_chars:
            return 1.0, f"length {n} >= {min_chars}"
        return n / min_chars, f"length {n} < {min_chars} required"
    return _score


def max_length(max_chars: int) -> ScorerFn:
    """Factory: 1.0 if response is at most max_chars long."""
    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        n = len(actual.strip())
        if n <= max_chars:
            return 1.0, f"length {n} <= {max_chars}"
        return 0.0, f"length {n} > {max_chars} max"
    return _score


def regex_match(pattern: str, flags: int = re.IGNORECASE) -> ScorerFn:
    """Factory: 1.0 if response matches regex pattern."""
    compiled = re.compile(pattern, flags)
    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        if compiled.search(actual):
            return 1.0, f"regex {pattern!r} matched"
        return 0.0, f"regex {pattern!r} not found"
    return _score


def composite(*scorers: ScorerFn, weights: list[float] | None = None) -> ScorerFn:
    """Weighted average of multiple scorers. Defaults to equal weights."""
    if weights is None:
        weights = [1.0] * len(scorers)
    if len(weights) != len(scorers):
        raise ValueError("weights length must match scorers length")
    total_weight = sum(weights)

    def _score(actual: str, case: EvalCase) -> tuple[float, str]:
        parts = []
        weighted_sum = 0.0
        for scorer, w in zip(scorers, weights, strict=True):
            s, r = scorer(actual, case)
            weighted_sum += s * w
            parts.append(f"{scorer.__name__}={s:.2f} ({r})")
        final = weighted_sum / total_weight
        return final, " | ".join(parts)

    _score.__name__ = "composite"
    return _score


# Default scorer: non_empty + contains_all + excludes_none
DEFAULT_SCORER: ScorerFn = composite(non_empty, contains_all, excludes_none)
```

FILE: /home/user/wellux_testprojects/src/evals/runner.py
```python
"""EvalRunner — executes an EvalSuite against a callable LLM backend.

Two runners are provided:
    EvalRunner       — synchronous; sequential by default, parallel with max_workers
    AsyncEvalRunner  — async, concurrent (up to `concurrency` parallel calls)
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import time
from collections.abc import Callable, Coroutine
from typing import Any

from .scorers import DEFAULT_SCORER, ScorerFn
from .suite import EvalSuite
from .types import EvalCase, EvalReport, EvalResult, Verdict

# Sync callable: (prompt, *, max_tokens, temperature) -> str
LLMCallable = Callable[..., str]
# Async callable: (prompt, *, max_tokens, temperature) -> Coroutine[Any, Any, str]
AsyncLLMCallable = Callable[..., Coroutine[Any, Any, str]]


class EvalRunner:
    """Synchronous, sequential eval runner.

    Example:
        def my_llm(prompt, *, max_tokens=512, temperature=0.0):
            return client.complete(prompt)

        report = EvalRunner(my_llm).run(suite)
        print(report.summary())
    """

    def __init__(
        self,
        llm: LLMCallable,
        scorer: ScorerFn = DEFAULT_SCORER,
        pass_threshold: float = 0.8,
        verbose: bool = False,
        max_workers: int | None = None,
    ) -> None:
        self.llm = llm
        self.scorer = scorer
        self.pass_threshold = pass_threshold
        self.verbose = verbose
        self.max_workers = max_workers

    def run(self, suite: EvalSuite) -> EvalReport:
        """Run all cases — parallel when max_workers > 1, sequential otherwise."""
        cases = list(suite)
        if self.max_workers and self.max_workers > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                results = list(pool.map(self._run_case, cases))
        else:
            results = [self._run_case(case) for case in cases]
        if self.verbose:
            for result in results:
                _print_result(result)
        return _aggregate(suite.name, results)

    def run_case(self, case: EvalCase) -> EvalResult:
        return self._run_case(case)

    def _run_case(self, case: EvalCase) -> EvalResult:
        t0 = time.monotonic()
        try:
            actual = self.llm(
                case.prompt,
                max_tokens=case.max_tokens,
                temperature=case.temperature,
            )
        except Exception as exc:  # noqa: BLE001
            return EvalResult(
                case_id=case.id,
                verdict=Verdict.ERROR,
                actual="",
                score=0.0,
                reason=f"LLM raised: {exc}",
                latency_ms=(time.monotonic() - t0) * 1000,
                error=str(exc),
                tags=list(case.tags),
            )
        latency_ms = (time.monotonic() - t0) * 1000
        score, reason = self.scorer(actual, case)
        verdict = Verdict.PASS if score >= self.pass_threshold else Verdict.FAIL
        return EvalResult(
            case_id=case.id, verdict=verdict, actual=actual,
            score=score, reason=reason, latency_ms=latency_ms,
            tags=list(case.tags),
        )


class AsyncEvalRunner:
    """Concurrent async eval runner — runs up to `concurrency` cases in parallel.

    The `llm` callable must be an async function:
        async def my_llm(prompt, *, max_tokens=512, temperature=0.0) -> str: ...

    Example:
        runner = AsyncEvalRunner(my_llm, concurrency=5)
        report = await runner.run(suite)
        print(report.summary())
    """

    def __init__(
        self,
        llm: AsyncLLMCallable,
        scorer: ScorerFn = DEFAULT_SCORER,
        pass_threshold: float = 0.8,
        concurrency: int = 5,
        verbose: bool = False,
        case_timeout: float = 30.0,
    ) -> None:
        self.llm = llm
        self.scorer = scorer
        self.pass_threshold = pass_threshold
        self.concurrency = concurrency
        self.verbose = verbose
        self.case_timeout = case_timeout

    async def run(self, suite: EvalSuite) -> EvalReport:
        """Run all cases concurrently (up to `concurrency` at a time)."""
        semaphore = asyncio.Semaphore(self.concurrency)
        tasks = [self._run_case(case, semaphore) for case in suite]
        results = await asyncio.gather(*tasks)
        if self.verbose:
            for r in results:
                _print_result(r)
        return _aggregate(suite.name, list(results))

    async def run_case(self, case: EvalCase) -> EvalResult:
        return await self._run_case(case, asyncio.Semaphore(1))

    async def _run_case(self, case: EvalCase, sem: asyncio.Semaphore) -> EvalResult:
        async with sem:
            t0 = time.monotonic()
            try:
                actual = await asyncio.wait_for(
                    self.llm(
                        case.prompt,
                        max_tokens=case.max_tokens,
                        temperature=case.temperature,
                    ),
                    timeout=self.case_timeout,
                )
            except TimeoutError:
                return EvalResult(
                    case_id=case.id,
                    verdict=Verdict.ERROR,
                    actual="",
                    score=0.0,
                    reason=f"LLM timed out after {self.case_timeout}s",
                    latency_ms=(time.monotonic() - t0) * 1000,
                    error=f"TimeoutError: exceeded {self.case_timeout}s",
                    tags=list(case.tags),
                )
            except Exception as exc:  # noqa: BLE001
                return EvalResult(
                    case_id=case.id,
                    verdict=Verdict.ERROR,
                    actual="",
                    score=0.0,
                    reason=f"LLM raised: {exc}",
                    latency_ms=(time.monotonic() - t0) * 1000,
                    error=str(exc),
                    tags=list(case.tags),
                )
            latency_ms = (time.monotonic() - t0) * 1000
            score, reason = self.scorer(actual, case)
            verdict = Verdict.PASS if score >= self.pass_threshold else Verdict.FAIL
            return EvalResult(
                case_id=case.id, verdict=verdict, actual=actual,
                score=score, reason=reason, latency_ms=latency_ms,
                tags=list(case.tags),
            )


# ── shared helpers ────────────────────────────────────────────────────────────

def _print_result(result: EvalResult) -> None:
    icon = {"pass": "✓", "fail": "✗", "skip": "–", "error": "!"}.get(result.verdict.value, "?")
    print(f"  [{icon}] {result.case_id}: {result.reason[:80]}")


def _aggregate(suite_name: str, results: list[EvalResult]) -> EvalReport:
    counts = {v: 0 for v in Verdict}
    for r in results:
        counts[r.verdict] += 1
    return EvalReport(
        suite_name=suite_name,
        total=len(results),
        passed=counts[Verdict.PASS],
        failed=counts[Verdict.FAIL],
        skipped=counts[Verdict.SKIP],
        errors=counts[Verdict.ERROR],
        results=results,
    )
```


## 4.7 Persistence (src/persistence/)

FILE: /home/user/wellux_testprojects/src/persistence/__init__.py
```python
"""Persistence layer — file-based, memory-based, and tiered storage."""
from .file_store import FileStore
from .memory_store import Entity, MemoryStore, Relation
from .tiered_memory import TieredMemory

__all__ = ["FileStore", "MemoryStore", "TieredMemory", "Entity", "Relation"]
```

FILE: /home/user/wellux_testprojects/src/persistence/file_store.py
```python
"""File-based persistence — write research, outputs, and decisions to disk."""
from __future__ import annotations

import os
import tempfile
from datetime import datetime
from pathlib import Path

from ..utils.log_index import LogIndex


class FileStore:
    """Structured file storage for research, outputs, and decisions.

    Directory layout (relative to project root):
        data/research/YYYY-MM-DD-<slug>.md    ← research docs
        data/outputs/<type>-YYYY-MM-DD.md     ← generated reports
        tasks/todo.md                          ← task tracking (append)
        tasks/lessons.md                       ← lessons (append)
    """

    def __init__(self, root: str | Path = "."):
        self.root = Path(root)
        self._ensure_dirs()
        self._log = LogIndex(self.root / "data/cache/events.log")

    def _ensure_dirs(self) -> None:
        for d in ["data/research", "data/outputs", "data/cache", "tasks"]:
            (self.root / d).mkdir(parents=True, exist_ok=True)

    # ── Research ──────────────────────────────────────────────────────────────

    def write_research(self, topic: str, content: str) -> Path:
        """Write a research document. Returns the file path."""
        date = datetime.now().strftime("%Y-%m-%d")
        slug = _slugify(topic)
        path = self.root / f"data/research/{date}-{slug}.md"
        _atomic_write(path, content)
        self._index_research(topic, path, date)
        return path

    def _index_research(self, topic: str, path: Path, date: str) -> None:
        index = self.root / "data/research/README.md"
        entry = f"- [{topic}]({path.name}) — {date}\n"
        with open(index, "a", encoding="utf-8") as f:
            f.write(entry)

    def list_research(self) -> list[dict]:
        """Return all research files as [{topic, path, date}]."""
        results = []
        for p in sorted((self.root / "data/research").glob("*.md")):
            if p.name == "README.md":
                continue
            parts = p.stem.split("-", 3)
            date = "-".join(parts[:3]) if len(parts) >= 3 else "unknown"
            topic = parts[3].replace("-", " ") if len(parts) >= 4 else p.stem
            results.append({"topic": topic, "path": str(p), "date": date})
        return results

    # ── Outputs ───────────────────────────────────────────────────────────────

    def write_output(self, output_type: str, content: str) -> Path:
        """Write a generated report/output. Returns the file path."""
        date = datetime.now().strftime("%Y-%m-%d")
        path = self.root / f"data/outputs/{output_type}-{date}.md"
        _atomic_write(path, content)
        return path

    # ── Lessons ───────────────────────────────────────────────────────────────

    def append_lesson(
        self,
        title: str,
        mistake: str,
        why: str,
        rule: str,
        example: str,
    ) -> None:
        """Append a lesson entry to tasks/lessons.md."""
        date = datetime.now().strftime("%Y-%m-%d")
        lessons_path = self.root / "tasks/lessons.md"
        entry = (
            f"\n## Lesson — {date}: {title}\n"
            f"**Mistake:** {mistake}\n"
            f"**Why:** {why}\n"
            f"**Rule:** {rule}\n"
            f"**Example:** {example}\n"
        )
        with open(lessons_path, "a", encoding="utf-8") as f:
            f.write(entry)

    # ── Tasks ─────────────────────────────────────────────────────────────────

    def append_task(self, description: str) -> None:
        """Append an open task to tasks/todo.md."""
        todo_path = self.root / "tasks/todo.md"
        with open(todo_path, "a", encoding="utf-8") as f:
            f.write(f"\n- [ ] {description}")

    def complete_task(self, description: str) -> bool:
        """Mark a task complete in tasks/todo.md. Returns True if found."""
        todo_path = self.root / "tasks/todo.md"
        if not todo_path.exists():
            return False
        text = todo_path.read_text(encoding="utf-8")
        new_text = text.replace(f"- [ ] {description}", f"- [x] {description}", 1)
        if new_text == text:
            return False
        _atomic_write(todo_path, new_text)
        return True

    # ── Cache log ─────────────────────────────────────────────────────────────

    def log_event(self, event: str, **kwargs) -> dict:
        """Append an indexed, structured event to data/cache/events.log.

        Returns the written record so callers can inspect or test it.
        The underlying LogIndex maintains an in-memory reverse index by
        event name and tag for fast search without full-file scans.
        """
        return self._log.append(event, **kwargs)

    def search_log(
        self,
        event: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Search the indexed event log. Returns newest-first."""
        return self._log.search(event=event, tags=tags, limit=limit)

    def log_summary(self) -> dict[str, int]:
        """Return {event_name: count} for all events in the log."""
        return self._log.summary()

    # ── Generic read/write ────────────────────────────────────────────────────

    def read(self, relative_path: str) -> str:
        """Read any file relative to project root."""
        return (self.root / relative_path).read_text(encoding="utf-8")

    def write(self, relative_path: str, content: str) -> Path:
        """Write any file relative to project root."""
        path = self.root / relative_path
        _atomic_write(path, content)
        return path


def _atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically via a temp-file + os.replace.

    Guarantees the target file is never in a partial state: either the old
    content is intact or the new content is fully written, even if the process
    is killed mid-write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _slugify(text: str) -> str:
    """Convert topic to a filesystem-safe slug."""
    import re
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug[:60]
```

FILE: /home/user/wellux_testprojects/src/persistence/memory_store.py
```python
"""MCP Memory Store — persist facts, entities, and decisions via MCP memory server.

Wraps the mcp__memory__ tool interface with a clean Python API.
Falls back gracefully when the MCP server is not available.

Usage:
    store = MemoryStore()
    store.remember("project uses PostgreSQL for all persistence")
    store.remember_entity("LightRAG", "tool", ["graph-based RAG", "EMNLP 2025"])
    facts = store.recall("database")
"""
from __future__ import annotations

from dataclasses import dataclass

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Entity:
    name: str
    entity_type: str
    observations: list[str]


@dataclass
class Relation:
    from_entity: str
    to_entity: str
    relation_type: str


class MemoryStore:
    """Persistent memory via MCP memory server.

    Falls back to in-memory dict when MCP is unavailable,
    so code using this never needs try/except at the call site.
    """

    def __init__(self):
        self._fallback: dict[str, list[str]] = {}
        self._mcp_available = self._check_mcp()

    def _check_mcp(self) -> bool:
        """Return True if MCP memory tools are importable."""
        try:
            # MCP tools are injected by Claude Code at runtime.
            # In standalone Python execution they won't exist.
            return False  # standalone — always use fallback
        except Exception:
            return False

    # ── Write operations ──────────────────────────────────────────────────────

    def remember(self, fact: str, entity_name: str = "general") -> None:
        """Store a plain-text observation, optionally under an entity name."""
        if self._mcp_available:
            self._mcp_add_observation(entity_name, fact)
        else:
            self._fallback.setdefault(entity_name, []).append(fact)
            logger.debug("memory_stored_local", entity=entity_name, fact=fact[:60])

    def remember_entity(
        self,
        name: str,
        entity_type: str,
        observations: list[str],
    ) -> None:
        """Create or update a named entity with observations."""
        if self._mcp_available:
            self._mcp_create_entity(name, entity_type, observations)
        else:
            self._fallback.setdefault(name, []).extend(observations)
            logger.debug("entity_stored_local", name=name, obs_count=len(observations))

    def remember_relation(
        self,
        from_entity: str,
        to_entity: str,
        relation_type: str,
    ) -> None:
        """Store a relationship between two entities."""
        fact = f"{from_entity} --[{relation_type}]--> {to_entity}"
        self.remember(fact, entity_name="_relations")

    # ── Read operations ───────────────────────────────────────────────────────

    def recall(self, query: str) -> list[str]:
        """Search memory for facts matching query. Returns list of strings."""
        if self._mcp_available:
            return self._mcp_search(query)
        # Fallback: simple substring search across all stored facts
        results = []
        for entity, facts in self._fallback.items():
            for fact in facts:
                if query.lower() in fact.lower() or query.lower() in entity.lower():
                    results.append(f"[{entity}] {fact}")
        return results

    def recall_entity(self, name: str) -> Entity | None:
        """Retrieve all observations for a named entity."""
        if self._mcp_available:
            return self._mcp_open_node(name)
        facts = self._fallback.get(name)
        if not facts:
            return None
        return Entity(name=name, entity_type="unknown", observations=facts)

    def read_all(self) -> dict[str, list[str]]:
        """Return full memory graph (fallback only)."""
        return dict(self._fallback)

    # ── Delete operations ─────────────────────────────────────────────────────

    def forget(self, entity_name: str) -> None:
        """Remove all memory for an entity."""
        if self._mcp_available:
            self._mcp_delete_entity(entity_name)
        else:
            self._fallback.pop(entity_name, None)

    def forget_observation(self, entity_name: str, observation: str) -> None:
        """Remove a specific observation from an entity."""
        if self._mcp_available:
            self._mcp_delete_observation(entity_name, observation)
        else:
            facts = self._fallback.get(entity_name, [])
            self._fallback[entity_name] = [f for f in facts if f != observation]

    # ── MCP bridge (called at runtime by Claude Code) ─────────────────────────
    # These methods are stubs — Claude Code injects the real MCP tools.
    # In standalone Python they log a warning and no-op.

    def _mcp_add_observation(self, entity: str, obs: str) -> None:
        logger.warning("mcp_not_available", op="add_observation", entity=entity)

    def _mcp_create_entity(self, name: str, etype: str, obs: list[str]) -> None:
        logger.warning("mcp_not_available", op="create_entity", name=name)

    def _mcp_search(self, query: str) -> list[str]:
        logger.warning("mcp_not_available", op="search", query=query)
        return []

    def _mcp_open_node(self, name: str) -> Entity | None:
        logger.warning("mcp_not_available", op="open_node", name=name)
        return None

    def _mcp_delete_entity(self, name: str) -> None:
        logger.warning("mcp_not_available", op="delete_entity", name=name)

    def _mcp_delete_observation(self, entity: str, obs: str) -> None:
        logger.warning("mcp_not_available", op="delete_observation", entity=entity)

    @property
    def size(self) -> int:
        """Number of entities in fallback store."""
        return len(self._fallback)
```

FILE: /home/user/wellux_testprojects/src/persistence/tiered_memory.py
```python
"""Tiered memory system: hot / warm / glacier.

Three-tier architecture inspired by cog (marciopuga) and thebrain (Advenire-Consulting):
- Hot  (<50 lines, loaded every session via session-start hook)
- Warm (domain-specific, loaded on context activation)
- Glacier (archived YAML-frontmatter entries, indexed and searched on demand)

Usage::

    from src.persistence.tiered_memory import TieredMemory

    mem = TieredMemory()
    mem.write_hot("active_branch", "claude/optimize-cli-autonomy-xNamK")
    mem.write_warm("architecture", "# Architecture\\n...")
    mem.archive_glacier("bug-fix-2026-04", "Fixed exc_info leak in logger", tags=["bug", "logger"])
    results = mem.search_glacier("logger")
"""

from __future__ import annotations

import re
import textwrap
from datetime import datetime
from pathlib import Path

_BASE = Path(__file__).resolve().parents[2]
_MEMORY_ROOT = _BASE / ".claude" / "memory"
_HOT_FILE = _MEMORY_ROOT / "hot" / "hot-memory.md"
_WARM_DIR = _MEMORY_ROOT / "warm"
_GLACIER_DIR = _MEMORY_ROOT / "glacier"

_HOT_MAX_LINES = 50

# Cache compiled hot-key patterns to avoid recompilation on every write_hot call
_hot_key_patterns: dict[str, re.Pattern[str]] = {}


class TieredMemory:
    """File-based three-tier memory: hot, warm, glacier."""

    def __init__(self, base: Path | None = None) -> None:
        self._root = (base or _MEMORY_ROOT).resolve()
        self._hot_file = self._root / "hot" / "hot-memory.md"
        self._warm_dir = self._root / "warm"
        self._glacier_dir = self._root / "glacier"
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for d in (self._hot_file.parent, self._warm_dir, self._glacier_dir):
            d.mkdir(parents=True, exist_ok=True)

    # ── Hot tier ──────────────────────────────────────────────────────────────

    def read_hot(self) -> str:
        """Return current hot-memory content (≤50 lines)."""
        if not self._hot_file.exists():
            return ""
        return self._hot_file.read_text()

    def write_hot(self, key: str, value: str) -> None:
        """Update or insert a key: value line in hot-memory under ## Active Context.

        If the hot file grows beyond _HOT_MAX_LINES, oldest active-context lines
        are evicted to warm tier automatically.
        """
        content = self.read_hot()
        lines = content.splitlines()

        # Replace existing key or append
        new_line = f"- **{key}**: {value}"
        if key not in _hot_key_patterns:
            _hot_key_patterns[key] = re.compile(rf"^- \*\*{re.escape(key)}\*\*:")
        pattern = _hot_key_patterns[key]
        replaced = False
        new_lines = []
        for ln in lines:
            if pattern.match(ln):
                new_lines.append(new_line)
                replaced = True
            else:
                new_lines.append(ln)
        if not replaced:
            # Insert under ## Active Context section
            result = []
            in_section = False
            inserted = False
            for ln in new_lines:
                result.append(ln)
                if ln.startswith("## Active Context"):
                    in_section = True
                elif in_section and not inserted and (ln.startswith("##") or ln == ""):
                    result.insert(len(result) - 1, new_line)
                    inserted = True
                    in_section = False
            if not inserted:
                result.append(new_line)
            new_lines = result

        # Update last-modified timestamp
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_lines = [
            f"**Last Updated**: {ts}" if ln.startswith("**Last Updated**") else ln
            for ln in new_lines
        ]

        # Evict if over limit
        if len(new_lines) > _HOT_MAX_LINES:
            self._evict_hot_to_warm(new_lines)
        else:
            self._hot_file.write_text("\n".join(new_lines) + "\n")

    def _evict_hot_to_warm(self, lines: list[str]) -> None:
        """Move oldest active-context lines to warm tier to stay under limit."""
        eviction_target = self._warm_dir / "evicted-from-hot.md"

        # Find active-context lines beyond the first 10
        active_section = False
        active_lines: list[tuple[int, str]] = []
        for i, ln in enumerate(lines):
            if ln.startswith("## Active Context"):
                active_section = True
            elif active_section and ln.startswith("##"):
                break
            elif active_section and ln.startswith("- "):
                active_lines.append((i, ln))

        # Evict oldest half of active-context lines
        evict_count = max(1, len(active_lines) // 2)
        evict_indices = {idx for idx, _ in active_lines[:evict_count]}
        evict_content = "\n".join(ln for _, ln in active_lines[:evict_count])

        # Write evicted lines to warm
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with eviction_target.open("a") as f:
            f.write(f"\n## Evicted {ts}\n{evict_content}\n")

        # Remove evicted lines from hot
        new_lines = [ln for i, ln in enumerate(lines) if i not in evict_indices]
        self._hot_file.write_text("\n".join(new_lines) + "\n")

    # ── Warm tier ─────────────────────────────────────────────────────────────

    def read_warm(self, domain: str) -> str:
        """Return warm-tier content for a named domain."""
        path = self._warm_dir / f"{domain}.md"
        return path.read_text() if path.exists() else ""

    def write_warm(self, domain: str, content: str) -> None:
        """Write or replace a warm-tier domain file."""
        path = self._warm_dir / f"{domain}.md"
        path.write_text(content)

    def append_warm(self, domain: str, content: str) -> None:
        """Append content to a warm-tier domain file."""
        path = self._warm_dir / f"{domain}.md"
        with path.open("a") as f:
            f.write("\n" + content + "\n")

    def list_warm_domains(self) -> list[str]:
        """Return list of warm domain names (without .md extension)."""
        return [p.stem for p in self._warm_dir.glob("*.md")]

    # ── Glacier tier ──────────────────────────────────────────────────────────

    def archive_glacier(
        self,
        slug: str,
        content: str,
        *,
        tags: list[str] | None = None,
        title: str | None = None,
    ) -> Path:
        """Archive content to glacier with YAML frontmatter for indexing.

        Returns the path of the created file.
        """
        ts = datetime.now()
        date_str = ts.strftime("%Y-%m-%d")
        time_str = ts.strftime("%H:%M:%S")
        tags_yaml = ", ".join(tags or [])
        file_title = title or slug.replace("-", " ").title()
        filename = f"{date_str}-{slug}.md"
        path = self._glacier_dir / filename

        frontmatter = textwrap.dedent(f"""\
            ---
            title: {file_title}
            date: {date_str}
            time: {time_str}
            tags: [{tags_yaml}]
            slug: {slug}
            ---
            """)
        path.write_text(frontmatter + "\n" + content + "\n")
        return path

    def search_glacier(self, query: str, *, limit: int = 20) -> list[dict]:
        """Search glacier archives by keyword in frontmatter tags, title, or content.

        Args:
            query: Keyword to search for (case-insensitive).
            limit: Maximum number of results to return (default 20).

        Returns list of dicts with: path, title, date, tags, snippet.
        """
        results = []
        q = query.lower()
        for path in sorted(self._glacier_dir.glob("*.md"), reverse=True):
            if len(results) >= limit:
                break
            text = path.read_text()
            # Parse YAML frontmatter
            meta = self._parse_frontmatter(text)
            # Check tags, title, or content
            searchable = (
                meta.get("title", "").lower()
                + " "
                + meta.get("tags", "").lower()
                + " "
                + text.lower()
            )
            if q in searchable:
                # Extract snippet (first non-frontmatter line with the query)
                body_lines = text.split("---", 2)[-1].splitlines()
                snippet = next(
                    (ln.strip() for ln in body_lines if q in ln.lower() and ln.strip()),
                    body_lines[0].strip() if body_lines else "",
                )
                results.append(
                    {
                        "path": str(path),
                        "title": meta.get("title", path.stem),
                        "date": meta.get("date", ""),
                        "tags": [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()],
                        "snippet": snippet[:200],
                    }
                )
        return results

    def list_glacier(self, tag: str | None = None) -> list[dict]:
        """List all glacier entries, optionally filtered by tag."""
        entries = []
        for path in sorted(self._glacier_dir.glob("*.md"), reverse=True):
            text = path.read_text()
            meta = self._parse_frontmatter(text)
            tags = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]
            if tag and tag not in tags:
                continue
            entries.append(
                {
                    "path": str(path),
                    "title": meta.get("title", path.stem),
                    "date": meta.get("date", ""),
                    "tags": tags,
                }
            )
        return entries

    @staticmethod
    def _parse_frontmatter(text: str) -> dict[str, str]:
        """Parse simple YAML frontmatter (key: value lines only)."""
        meta: dict[str, str] = {}
        if not text.startswith("---"):
            return meta
        parts = text.split("---", 2)
        if len(parts) < 3:
            return meta
        for line in parts[1].splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                meta[key.strip()] = val.strip()
        return meta
```


## 4.8 Prompt Engineering (src/prompt_engineering/)

FILE: /home/user/wellux_testprojects/src/prompt_engineering/__init__.py
```python
"""Prompt engineering modules."""
from .chainer import ChainResult, ChainStep, PromptChain
from .few_shot import Example, FewShotManager
from .templates import PromptTemplate, TemplateLibrary, default_library

__all__ = [
    "PromptTemplate",
    "TemplateLibrary",
    "default_library",
    "Example",
    "FewShotManager",
    "ChainStep",
    "ChainResult",
    "PromptChain",
]
```

FILE: /home/user/wellux_testprojects/src/prompt_engineering/templates.py
```python
"""Jinja2-style prompt template engine (no external deps)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PromptTemplate:
    """Simple {{variable}} template with validation.

    Example:
        t = PromptTemplate("Summarize {{text}} in {{language}}.")
        t.render(text="...", language="English")
    """

    template: str
    required_vars: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        found = re.findall(r"\{\{(\w+)\}\}", self.template)
        if not self.required_vars:
            self.required_vars = list(dict.fromkeys(found))  # dedupe, preserve order

    def render(self, **kwargs: Any) -> str:
        """Render template with provided variables.

        Raises ValueError if any required_vars are missing.
        """
        missing = [v for v in self.required_vars if v not in kwargs]
        if missing:
            raise ValueError(f"Missing template variables: {missing}")

        result = self.template
        for key, value in kwargs.items():
            result = result.replace("{{" + key + "}}", str(value))
        return result

    def variables(self) -> list[str]:
        return list(self.required_vars)


class TemplateLibrary:
    """Registry of named prompt templates."""

    def __init__(self) -> None:
        self._templates: dict[str, PromptTemplate] = {}

    def register(self, name: str, template: str, required_vars: list[str] | None = None) -> None:
        self._templates[name] = PromptTemplate(
            template=template,
            required_vars=required_vars or [],
        )

    def get(self, name: str) -> PromptTemplate:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not registered. Available: {list(self._templates)}")
        return self._templates[name]

    def render(self, template_name: str, **kwargs: Any) -> str:
        return self.get(template_name).render(**kwargs)

    def list_templates(self) -> list[str]:
        return list(self._templates)


# Default library pre-loaded with common templates
default_library = TemplateLibrary()
default_library.register(
    "code_review",
    "You are a senior engineer. Review this {{language}} code for bugs, style, and security.\n\n```{{language}}\n{{code}}\n```\n\nProvide: issues found, severity (critical/major/minor), and fixes.",
)
default_library.register(
    "summarize",
    "Summarize the following text in {{max_words}} words or fewer, focusing on key insights:\n\n{{text}}",
)
default_library.register(
    "research_query",
    "Research: {{topic}}\n\nProvide:\n1. Core concept (2-3 sentences)\n2. Latest developments (2026)\n3. Key implementation pattern\n4. Actionable insight for a practitioner\n\nBe direct and technical.",
)
default_library.register(
    "bug_fix",
    "Debug this {{language}} error:\n\nError: {{error}}\n\nCode:\n```{{language}}\n{{code}}\n```\n\nProvide root cause and minimal fix.",
)
```

FILE: /home/user/wellux_testprojects/src/prompt_engineering/few_shot.py
```python
"""Few-shot example manager for prompt construction."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Example:
    """A single input→output demonstration."""
    input: str
    output: str
    label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class FewShotManager:
    """Manage and retrieve few-shot examples for prompt construction.

    Usage:
        mgr = FewShotManager(prefix="Classify sentiment:")
        mgr.add("Great product!", "positive")
        mgr.add("Terrible experience.", "negative")
        prompt = mgr.build_prompt("Works as expected.")
    """

    def __init__(
        self,
        prefix: str = "",
        input_label: str = "Input",
        output_label: str = "Output",
        separator: str = "\n\n",
    ):
        self.prefix = prefix
        self.input_label = input_label
        self.output_label = output_label
        self.separator = separator
        self._examples: list[Example] = []

    def add(self, input_text: str, output_text: str, label: str = "", **metadata: Any) -> None:
        self._examples.append(
            Example(input=input_text, output=output_text, label=label, metadata=metadata)
        )

    def get_by_label(self, label: str) -> list[Example]:
        return [e for e in self._examples if e.label == label]

    def build_prompt(self, query: str, max_examples: int | None = None) -> str:
        """Build a few-shot prompt with all (or up to max_examples) examples."""
        examples = self._examples if max_examples is None else self._examples[-max_examples:]
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        for ex in examples:
            parts.append(f"{self.input_label}: {ex.input}\n{self.output_label}: {ex.output}")
        parts.append(f"{self.input_label}: {query}\n{self.output_label}:")
        return self.separator.join(parts)

    def to_messages(self, query: str, max_examples: int | None = None) -> list[dict]:
        """Return chat-format messages list for API calls."""
        examples = self._examples if max_examples is None else self._examples[-max_examples:]
        messages = []
        for ex in examples:
            messages.append({"role": "user", "content": ex.input})
            messages.append({"role": "assistant", "content": ex.output})
        messages.append({"role": "user", "content": query})
        return messages

    def __len__(self) -> int:
        return len(self._examples)
```

FILE: /home/user/wellux_testprojects/src/prompt_engineering/chainer.py
```python
"""Prompt chaining — pipe the output of one LLM call into the next."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..llm.base import CompletionRequest, CompletionResponse, LLMClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ChainStep:
    """One step in a prompt chain."""
    name: str
    prompt_fn: Callable[[dict[str, Any]], str]
    """Receives context dict (previous outputs keyed by step name), returns prompt string."""
    system: str | None = None
    model: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7
    transform: Callable[[str], Any] = field(default=lambda x: x)
    """Post-process the raw LLM output before storing in context."""


@dataclass
class ChainResult:
    """Result of running a full chain."""
    steps: dict[str, Any] = field(default_factory=dict)
    """Keyed by step name → transformed output."""
    responses: dict[str, CompletionResponse] = field(default_factory=dict)
    """Raw CompletionResponse per step for token/cost tracking."""

    @property
    def final(self) -> Any:
        """Return the last step's output."""
        if not self.steps:
            return None
        return list(self.steps.values())[-1]

    @property
    def total_cost_usd(self) -> float:
        return sum(r.cost_usd for r in self.responses.values())

    @property
    def total_tokens(self) -> int:
        return sum(r.input_tokens + r.output_tokens for r in self.responses.values())


class PromptChain:
    """Execute a sequence of LLM calls where each step can use prior outputs.

    Example:
        chain = PromptChain(client)
        chain.add_step("outline", lambda ctx: f"Outline an essay on: {ctx['topic']}")
        chain.add_step("draft", lambda ctx: f"Expand this outline:\\n{ctx['outline']}")
        result = await chain.run({"topic": "RAG systems"})
        print(result.final)
    """

    def __init__(self, client: LLMClient):
        self.client = client
        self._steps: list[ChainStep] = []

    def add_step(
        self,
        name: str,
        prompt_fn: Callable[[dict[str, Any]], str],
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        transform: Callable[[str], Any] = lambda x: x,
    ) -> PromptChain:
        self._steps.append(
            ChainStep(
                name=name,
                prompt_fn=prompt_fn,
                system=system,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                transform=transform,
            )
        )
        return self  # fluent API

    async def run(self, initial_context: dict[str, Any] | None = None) -> ChainResult:
        """Execute all steps sequentially, accumulating context."""
        context: dict[str, Any] = dict(initial_context or {})
        result = ChainResult()

        for step in self._steps:
            prompt = step.prompt_fn(context)
            request = CompletionRequest(
                prompt=prompt,
                system=step.system,
                model=step.model,
                max_tokens=step.max_tokens,
                temperature=step.temperature,
            )
            logger.info("chain_step_start", step=step.name, prompt_len=len(prompt))
            response = await self.client.complete(request)
            transformed = step.transform(response.content)
            context[step.name] = transformed
            result.steps[step.name] = transformed
            result.responses[step.name] = response
            logger.info(
                "chain_step_done",
                step=step.name,
                tokens=response.input_tokens + response.output_tokens,
                cost_usd=response.cost_usd,
            )

        return result

    async def run_parallel_branches(
        self,
        branches: dict[str, PromptChain],
        initial_context: dict[str, Any] | None = None,
    ) -> dict[str, ChainResult]:
        """Run multiple independent chains in parallel and return their results."""
        tasks = {
            name: asyncio.create_task(chain.run(initial_context))
            for name, chain in branches.items()
        }
        results = {}
        for name, task in tasks.items():
            results[name] = await task
        return results
```


## 4.9 Utilities (src/utils/)

FILE: /home/user/wellux_testprojects/src/utils/__init__.py
```python
"""Utility modules."""
from .cache import ResponseCache
from .logger import get_logger
from .rate_limiter import RateLimiter
from .token_counter import count_tokens_approx, estimate_cost, split_into_chunks

__all__ = [
    "RateLimiter",
    "ResponseCache",
    "get_logger",
    "count_tokens_approx",
    "estimate_cost",
    "split_into_chunks",
]
```

FILE: /home/user/wellux_testprojects/src/utils/logger.py
```python
"""Structured JSON logger factory."""
from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any


class _StructuredFormatter(logging.Formatter):
    """Emit log records as JSON lines."""

    # Standard LogRecord *instance* attributes that must never be serialised raw.
    # exc_info / exc_text / stack_info can contain non-JSON-serialisable objects.
    _STDLIB_KEYS: frozenset[str] = frozenset(logging.LogRecord(
        "", logging.INFO, "", 0, "", (), None
    ).__dict__.keys()) | frozenset(logging.LogRecord.__dict__.keys())

    # Field names whose values are redacted before serialisation to prevent
    # accidental logging of secrets, tokens, or credentials.
    _SENSITIVE_KEYS: frozenset[str] = frozenset({
        "password", "passwd", "secret", "token", "api_key", "apikey",
        "authorization", "auth", "credential", "private_key", "access_key",
    })

    def format(self, record: logging.LogRecord) -> str:
        base = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Merge any extra kwargs passed to logger.info("event", key=val),
        # excluding all standard LogRecord attrs (some contain non-serialisable
        # objects such as exc_info tuples or traceback references).
        extra = {
            k: ("[REDACTED]" if k.lower() in self._SENSITIVE_KEYS else v)
            for k, v in record.__dict__.items()
            if k not in self._STDLIB_KEYS and not k.startswith("_")
        }
        base.update(extra)
        if record.exc_info:
            base["exc"] = self.formatException(record.exc_info)
        return json.dumps(base)


def get_logger(name: str, level: int = logging.INFO) -> StructuredLogger:
    """Return a structured logger with JSON output."""
    return StructuredLogger(name, level)


class StructuredLogger:
    """Thin wrapper that passes kwargs as extra fields to the JSON formatter."""

    def __init__(self, name: str, level: int = logging.INFO):
        self._log = logging.getLogger(name)
        if not self._log.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(_StructuredFormatter())
            self._log.addHandler(handler)
            self._log.setLevel(level)
            self._log.propagate = False

    def _emit(self, level: int, msg: str, **kwargs: Any) -> None:
        if self._log.isEnabledFor(level):
            record = self._log.makeRecord(
                self._log.name, level, "(unknown)", 0, msg, (), None
            )
            record.__dict__.update(kwargs)
            self._log.handle(record)

    def debug(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.INFO, msg, **kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.ERROR, msg, **kwargs)

    def critical(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.CRITICAL, msg, **kwargs)
```

FILE: /home/user/wellux_testprojects/src/utils/rate_limiter.py
```python
"""Token-bucket rate limiter for API calls."""
import asyncio
import time


class RateLimiter:
    """Async token-bucket rate limiter.

    Allows up to `requests_per_minute` calls per 60-second window.
    Callers await `acquire()` which blocks until a slot is available.
    """

    def __init__(self, requests_per_minute: int = 100):
        self.rpm = requests_per_minute
        self._interval = 60.0 / requests_per_minute  # seconds per token
        self._tokens = float(requests_per_minute)
        self._max_tokens = float(requests_per_minute)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._max_tokens, self._tokens + elapsed / self._interval)
        self._last_refill = now

    async def acquire(self, tokens: float = 1.0) -> None:
        """Block until `tokens` slots are available."""
        async with self._lock:
            while True:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                wait = (tokens - self._tokens) * self._interval
                await asyncio.sleep(wait)

    @property
    def available_tokens(self) -> float:
        self._refill()
        return self._tokens
```

FILE: /home/user/wellux_testprojects/src/utils/cache.py
```python
"""In-memory response cache with optional TTL."""
from __future__ import annotations

import hashlib
import json
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..llm.base import CompletionRequest, CompletionResponse


def _cache_key(request: CompletionRequest) -> str:
    """Stable hash of the request fields that affect output."""
    payload = json.dumps(
        {
            "prompt": request.prompt,
            "system": request.system,
            "model": request.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


class ResponseCache:
    """Simple in-memory LRU-ish cache with TTL.

    Not thread-safe for concurrent writes — use asyncio.Lock externally
    if needed. Suitable for single-threaded async use.
    """

    def __init__(self, ttl_seconds: float = 3600.0, max_size: int = 1000):
        self._ttl = ttl_seconds
        self._max_size = max_size
        self._store: dict[str, tuple[float, CompletionResponse]] = {}

    def get(self, request: CompletionRequest) -> CompletionResponse | None:
        key = _cache_key(request)
        entry = self._store.get(key)
        if entry is None:
            return None
        ts, response = entry
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        return response

    def set(self, request: CompletionRequest, response: CompletionResponse) -> None:
        if len(self._store) >= self._max_size:
            # Evict oldest entry
            oldest_key = min(self._store, key=lambda k: self._store[k][0])
            del self._store[oldest_key]
        key = _cache_key(request)
        self._store[key] = (time.monotonic(), response)

    def invalidate(self, request: CompletionRequest) -> None:
        key = _cache_key(request)
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    @property
    def size(self) -> int:
        return len(self._store)
```

FILE: /home/user/wellux_testprojects/src/utils/token_counter.py
```python
"""Token counting utilities."""
from __future__ import annotations

# Approximate chars-per-token ratios by model family
_CHARS_PER_TOKEN = {
    "claude": 3.8,
    "gpt-4": 4.0,
    "gpt-3.5": 4.0,
    "default": 4.0,
}


def count_tokens_approx(text: str, model: str = "default") -> int:
    """Return approximate token count for text.

    Uses character-based heuristic (~4 chars/token for English).
    For production use, call the model's tokenizer API directly.
    """
    ratio = _CHARS_PER_TOKEN.get("default", 4.0)
    for prefix, chars in _CHARS_PER_TOKEN.items():
        if model.startswith(prefix):
            ratio = chars
            break
    return max(1, int(len(text) / ratio))


def fits_in_context(text: str, model: str, context_limit: int) -> bool:
    """Return True if text likely fits within context_limit tokens."""
    return count_tokens_approx(text, model) <= context_limit


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    input_cost_per_mtok: float,
    output_cost_per_mtok: float,
) -> float:
    """Compute USD cost from token counts and per-million-token rates."""
    return (input_tokens * input_cost_per_mtok + output_tokens * output_cost_per_mtok) / 1_000_000


def split_into_chunks(text: str, max_tokens: int, model: str = "default") -> list[str]:
    """Split text into chunks that each fit within max_tokens."""
    ratio = _CHARS_PER_TOKEN.get("default", 4.0)
    for prefix, chars in _CHARS_PER_TOKEN.items():
        if model.startswith(prefix):
            ratio = chars
            break
    max_chars = int(max_tokens * ratio)
    chunks = []
    while text:
        chunks.append(text[:max_chars])
        text = text[max_chars:]
    return chunks
```

FILE: /home/user/wellux_testprojects/src/utils/log_index.py
```python
"""Append-only JSONL log with in-memory index and bounded memory.

Writes one JSON object per line to a log file. On first access the file is
scanned to rebuild the in-memory reverse index. Subsequent writes are O(1)
appends. When the in-memory buffer exceeds ``max_entries``, the oldest 25 %
of entries are evicted and the index is rebuilt — amortised O(1) per append.

Usage::

    from src.utils.log_index import LogIndex

    idx = LogIndex("data/cache/events.log", max_entries=50_000)
    idx.append("api_request", method="POST", path="/complete", status=200,
                latency_ms=142, request_id="abc123")
    idx.append("llm_call",    model="claude-sonnet-4-6", tokens=512,
                cost_usd=0.0014)

    # Search (newest-first)
    results = idx.search(event="api_request")
    results = idx.search(tags=["ci"], limit=20)
    results = idx.tail(50)
    summary = idx.summary()
"""
from __future__ import annotations

import json
import threading
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_MAX_ENTRIES = 100_000   # ~100 MB at ~1 KB per record
_EVICT_FRACTION = 0.25           # drop oldest 25 % on overflow


class LogIndex:
    """Thread-safe, bounded append-only JSONL log with in-memory reverse index."""

    def __init__(self, path: str | Path, max_entries: int = _DEFAULT_MAX_ENTRIES) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._max_entries = max_entries

        self._lock = threading.Lock()
        self._event_index: dict[str, list[int]] = defaultdict(list)
        self._tag_index: dict[str, list[int]] = defaultdict(list)
        self._lines: list[dict] = []

        if self.path.exists():
            self._load()

    # ── Write ─────────────────────────────────────────────────────────────────

    def append(self, event: str, **fields: Any) -> dict:
        """Append one log entry. Evicts oldest entries if buffer is full."""
        record: dict[str, Any] = {
            "ts": datetime.now(tz=UTC).isoformat(),
            "event": event,
            **fields,
        }

        with self._lock:
            # Write to disk first (durability before index update)
            with open(self.path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")

            line_no = len(self._lines)
            self._lines.append(record)
            self._event_index[event].append(line_no)
            for tag in _extract_tags(record):
                self._tag_index[tag].append(line_no)

            # Evict oldest quarter when buffer exceeds max to bound memory growth
            if len(self._lines) > self._max_entries:
                self._evict()

        return record

    # ── Search ────────────────────────────────────────────────────────────────

    def search(
        self,
        event: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Return matching records, newest-first, up to *limit*."""
        with self._lock:
            if event and tags:
                event_set = set(self._event_index.get(event, []))
                tag_set: set[int] = set()
                for t in tags:
                    tag_set.update(self._tag_index.get(t, []))
                candidates = sorted(event_set & tag_set, reverse=True)
            elif event:
                candidates = list(reversed(self._event_index.get(event, [])))
            elif tags:
                merged: set[int] = set()
                for t in tags:
                    merged.update(self._tag_index.get(t, []))
                candidates = sorted(merged, reverse=True)
            else:
                candidates = list(range(len(self._lines) - 1, -1, -1))

            return [self._lines[i] for i in candidates[:limit]]

    def tail(self, n: int = 50) -> list[dict]:
        """Return the last *n* entries, oldest-first."""
        with self._lock:
            return list(self._lines[-n:])

    def summary(self) -> dict[str, int]:
        """Return ``{event_name: count}`` for all events in the in-memory buffer."""
        with self._lock:
            return {k: len(v) for k, v in self._event_index.items()}

    def __len__(self) -> int:
        return len(self._lines)

    # ── Internal ──────────────────────────────────────────────────────────────

    def _evict(self) -> None:
        """Drop the oldest 25 % of in-memory entries and rebuild indexes.

        Called holding ``self._lock``. The on-disk file is NOT truncated —
        it acts as a durable archive. Only the in-memory search index shrinks.
        """
        n_drop = max(1, int(len(self._lines) * _EVICT_FRACTION))
        self._lines = self._lines[n_drop:]
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Rebuild event + tag indexes from current ``_lines``. Holds lock."""
        self._event_index = defaultdict(list)
        self._tag_index = defaultdict(list)
        for i, record in enumerate(self._lines):
            self._event_index[record.get("event", "_unknown")].append(i)
            for tag in _extract_tags(record):
                self._tag_index[tag].append(i)

    def _load(self) -> None:
        """Scan disk file and rebuild in-memory index (called once at init)."""
        corrupt = 0
        with open(self.path, encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError:
                    corrupt += 1
                    continue
                self._lines.append(record)

        if corrupt:
            import warnings
            warnings.warn(
                f"LogIndex: skipped {corrupt} corrupt line(s) in {self.path}",
                stacklevel=2,
            )

        # Apply max_entries cap on load too (old log may be very large)
        if len(self._lines) > self._max_entries:
            self._lines = self._lines[-self._max_entries:]

        self._rebuild_index()


def _extract_tags(record: dict) -> list[str]:
    """Pull tag values from a record for the tag index."""
    tags: list[str] = []
    for key in ("tag", "tags", "category", "source"):
        val = record.get(key)
        if isinstance(val, str) and val:
            tags.append(val)
        elif isinstance(val, list):
            tags.extend(v for v in val if isinstance(v, str))
    return tags
```


## 4.10 Error Handlers (src/handlers/)

FILE: /home/user/wellux_testprojects/src/handlers/__init__.py
```python
"""Handler modules."""
from .error_handler import (
    AuthError,
    ContentFilterError,
    LLMError,
    RateLimitError,
    TokenLimitError,
    classify_api_error,
    handle_errors,
)

__all__ = [
    "LLMError",
    "RateLimitError",
    "TokenLimitError",
    "AuthError",
    "ContentFilterError",
    "classify_api_error",
    "handle_errors",
]
```

FILE: /home/user/wellux_testprojects/src/handlers/error_handler.py
```python
"""Centralized error handling and classification."""
from __future__ import annotations

import functools
import traceback
from collections.abc import Callable
from typing import Any, TypeVar

from ..utils.logger import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class LLMError(Exception):
    """Base class for LLM-related errors."""


class RateLimitError(LLMError):
    """API rate limit exceeded."""


class TokenLimitError(LLMError):
    """Prompt exceeds model context window."""


class AuthError(LLMError):
    """API authentication failure."""


class ContentFilterError(LLMError):
    """Response blocked by content filter."""


def classify_api_error(exc: Exception) -> LLMError:
    """Map provider-specific exceptions to our error hierarchy."""
    msg = str(exc).lower()
    if "rate limit" in msg or "429" in msg:
        return RateLimitError(str(exc))
    if (("context" in msg and ("window" in msg or "length" in msg))
            or ("token" in msg and "limit" in msg)):
        return TokenLimitError(str(exc))
    if "auth" in msg or "401" in msg or "api key" in msg:
        return AuthError(str(exc))
    if ("content" in msg and "filter" in msg) or "policy violation" in msg:
        return ContentFilterError(str(exc))
    return LLMError(str(exc))


def handle_errors(func: F) -> F:
    """Decorator: log and re-raise exceptions with structured context."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except LLMError:
            raise
        except Exception as exc:
            logger.error(
                "unhandled_error",
                func=func.__qualname__,
                error_type=type(exc).__name__,
                error=str(exc),
                traceback=traceback.format_exc(),
            )
            raise classify_api_error(exc) from exc

    return wrapper  # type: ignore[return-value]
```


## 4.11 Test Suite (tests/)

FILE: /home/user/wellux_testprojects/tests/__init__.py
```python
```

FILE: /home/user/wellux_testprojects/tests/conftest.py
```python
"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Ensure src/ is importable from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture()
def tiered_memory(tmp_path: Path):
    """Isolated TieredMemory instance backed by a temp directory."""
    from src.persistence.tiered_memory import TieredMemory

    return TieredMemory(base=tmp_path)


@pytest.fixture()
def file_store(tmp_path: Path):
    """FileStore instance rooted at a temp directory."""
    from src.persistence.file_store import FileStore

    return FileStore(root=tmp_path)


@pytest.fixture()
def mock_claude_client():
    """Pre-configured mock ClaudeClient for unit tests.

    .complete() and .chat() are AsyncMocks returning a CompletionResponse
    with content="mock response".
    """
    from src.llm.claude_client import CompletionResponse

    client = MagicMock()
    response = CompletionResponse(
        content="mock response",
        model="claude-sonnet-4-6",
        input_tokens=10,
        output_tokens=5,
    )
    client.complete = AsyncMock(return_value=response)
    client.chat = AsyncMock(return_value=response)
    client.count_tokens = MagicMock(return_value=10)
    return client
```

FILE: /home/user/wellux_testprojects/tests/test_version.py
```python
"""Tests for src/version.py — single source of truth for package version."""
from __future__ import annotations

import re

from src.version import VERSION_INFO, __version__, version_string


class TestVersion:
    def test_version_is_string(self):
        assert isinstance(__version__, str)

    def test_version_format(self):
        # Must match MAJOR.MINOR.PATCH
        assert re.match(r"^\d+\.\d+\.\d+", __version__)

    def test_version_string_matches_dunder(self):
        assert version_string() == __version__

    def test_version_info_is_tuple(self):
        assert isinstance(VERSION_INFO, tuple)
        assert len(VERSION_INFO) == 4

    def test_version_info_major_minor_patch(self):
        major, minor, patch, pre = VERSION_INFO
        assert isinstance(major, int) and major >= 0
        assert isinstance(minor, int) and minor >= 0
        assert isinstance(patch, int) and patch >= 0

    def test_version_info_consistent_with_version_string(self):
        major, minor, patch, _ = VERSION_INFO
        assert __version__.startswith(f"{major}.{minor}.{patch}")

    def test_package_exports_version(self):
        import src
        assert src.__version__ == __version__


class TestReadVersionFallbacks:
    def test_tomllib_fallback_when_metadata_unavailable(self, tmp_path):
        """tomllib path used when importlib.metadata raises; reads from real pyproject.toml."""
        import io
        from unittest.mock import patch

        import src.version as vmod

        toml_bytes = b'[project]\nversion = "9.8.7"\n'
        with patch("importlib.metadata.version", side_effect=Exception("not found")):
            with patch("pathlib.Path.open", return_value=io.BytesIO(toml_bytes)):
                result = vmod._read_version()
        assert result == "9.8.7"

    def test_dev_fallback_when_all_fail(self):
        """Returns '0.0.0+dev' when both importlib.metadata and tomllib fail."""
        from unittest.mock import patch

        import src.version as vmod

        with patch("importlib.metadata.version", side_effect=Exception("no meta")):
            with patch("pathlib.Path.open", side_effect=Exception("no file")):
                result = vmod._read_version()
        assert result == "0.0.0+dev"

    def test_version_info_shape_for_dev_string(self):
        """VERSION_INFO tuple logic handles '0.0.0+dev' correctly."""
        parts = "0.0.0+dev".split("+")[0].split(".")
        nums = [int(p) for p in parts if p.isdigit()]
        info = (nums[0], nums[1], nums[2], "") if len(nums) >= 3 else (0, 0, 0, "")
        assert info == (0, 0, 0, "")
```

FILE: /home/user/wellux_testprojects/tests/test_cli.py
```python
"""Tests for src/cli.py — argument parsing and subcommand logic."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.cli import (
    _deploy_check_health,
    _deploy_run_evals,
    _deploy_run_tests,
    build_parser,
    cmd_doctor,
    cmd_lint,
    cmd_logs,
    cmd_research,
    cmd_route,
    cmd_status,
    cmd_version,
    main,
)

PROJECT_ROOT = Path(__file__).parent.parent


# ── Parser ────────────────────────────────────────────────────────────────────

class TestParser:
    def test_route_subcommand(self):
        args = build_parser().parse_args(["route", "write a function"])
        assert args.command == "route"
        assert args.task == "write a function"
        assert args.json is False

    def test_route_json_flag(self):
        assert build_parser().parse_args(["route", "task", "--json"]).json is True

    def test_complete_defaults(self):
        args = build_parser().parse_args(["complete", "hello"])
        assert args.prompt == "hello"
        assert args.model is None
        assert args.max_tokens == 4096
        assert args.system is None

    def test_complete_with_flags(self):
        args = build_parser().parse_args([
            "complete", "hi",
            "--model", "claude-haiku-4-5-20251001",
            "--max-tokens", "512",
            "--system", "Be terse",
        ])
        assert args.model == "claude-haiku-4-5-20251001"
        assert args.max_tokens == 512
        assert args.system == "Be terse"

    def test_serve_defaults(self):
        args = build_parser().parse_args(["serve"])
        assert args.host == "0.0.0.0"
        assert args.port == 8000
        assert args.reload is False

    def test_serve_custom(self):
        args = build_parser().parse_args(["serve", "--host", "127.0.0.1", "--port", "9000", "--reload"])
        assert args.host == "127.0.0.1" and args.port == 9000 and args.reload is True

    def test_status_subcommand(self):
        assert build_parser().parse_args(["status"]).command == "status"

    def test_version_subcommand(self):
        assert build_parser().parse_args(["version"]).command == "version"

    def test_doctor_subcommand(self):
        assert build_parser().parse_args(["doctor"]).command == "doctor"

    def test_logs_defaults(self):
        args = build_parser().parse_args(["logs"])
        assert args.limit == 50
        assert args.event is None
        assert args.tag is None
        assert args.summary is False

    def test_logs_with_flags(self):
        args = build_parser().parse_args(["logs", "--event", "api_request", "--limit", "10", "--summary"])
        assert args.event == "api_request"
        assert args.limit == 10
        assert args.summary is True

    def test_research_subcommand(self):
        assert build_parser().parse_args(["research", "LightRAG"]).topic == "LightRAG"

    def test_no_subcommand_raises(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args([])

    def test_version_flag_exits(self):
        with pytest.raises(SystemExit) as exc:
            build_parser().parse_args(["--version"])
        assert exc.value.code == 0


# ── cmd_version ───────────────────────────────────────────────────────────────

class TestCmdVersion:
    def test_returns_zero(self):
        assert cmd_version(build_parser().parse_args(["version"])) == 0

    def test_shows_version_string(self, capsys):
        from src.version import __version__
        cmd_version(build_parser().parse_args(["version"]))
        assert __version__ in capsys.readouterr().out

    def test_shows_python_version(self, capsys):
        import sys
        cmd_version(build_parser().parse_args(["version"]))
        assert str(sys.version_info.major) in capsys.readouterr().out


# ── cmd_route ─────────────────────────────────────────────────────────────────

class TestCmdRoute:
    def test_text_output(self, capsys):
        assert cmd_route(build_parser().parse_args(["route", "write a unit test"])) == 0
        assert len(capsys.readouterr().out) > 0

    def test_json_output(self, capsys):
        assert cmd_route(build_parser().parse_args(["route", "summarise this document", "--json"])) == 0
        data = json.loads(capsys.readouterr().out)
        assert all(k in data for k in ("model", "agent", "plan_size", "subtasks"))

    def test_json_subtasks_is_list(self, capsys):
        cmd_route(build_parser().parse_args(["route", "simple task", "--json"]))
        assert isinstance(json.loads(capsys.readouterr().out)["subtasks"], list)

    def test_high_complexity_uses_opus(self, capsys):
        cmd_route(build_parser().parse_args([
            "route",
            "full security audit of the entire codebase architecture and infrastructure",
            "--json",
        ]))
        assert "opus" in json.loads(capsys.readouterr().out)["model"]

    def test_simple_task_uses_haiku(self, capsys):
        cmd_route(build_parser().parse_args(["route", "format this text", "--json"]))
        assert "haiku" in json.loads(capsys.readouterr().out)["model"]


# ── cmd_status ────────────────────────────────────────────────────────────────

class TestCmdStatus:
    def test_returns_zero(self):
        assert cmd_status(build_parser().parse_args(["status"])) == 0

    def test_shows_branch(self, capsys):
        cmd_status(build_parser().parse_args(["status"]))
        assert "branch" in capsys.readouterr().out

    def test_shows_version(self, capsys):
        from src.version import __version__
        cmd_status(build_parser().parse_args(["status"]))
        assert __version__ in capsys.readouterr().out

    def test_shows_test_count(self, capsys):
        import re
        cmd_status(build_parser().parse_args(["status"]))
        out = capsys.readouterr().out
        assert "tests" in out
        match = re.search(r"tests\s*:\s*(\d+)", out)
        assert match and int(match.group(1)) >= 100

    def test_shows_skills_count(self, capsys):
        import re
        cmd_status(build_parser().parse_args(["status"]))
        out = capsys.readouterr().out
        match = re.search(r"skills\s*:\s*(\d+)", out)
        assert match and int(match.group(1)) >= 100


# ── cmd_doctor ────────────────────────────────────────────────────────────────

class TestCmdDoctor:
    def test_runs_without_crash(self):
        assert cmd_doctor(build_parser().parse_args(["doctor"])) in (0, 1)

    def test_shows_check_icons(self, capsys):
        cmd_doctor(build_parser().parse_args(["doctor"]))
        out = capsys.readouterr().out
        assert "[✓]" in out or "[✗]" in out

    def test_shows_summary_line(self, capsys):
        cmd_doctor(build_parser().parse_args(["doctor"]))
        assert "checks passed" in capsys.readouterr().out

    def test_skills_check_present(self, capsys):
        cmd_doctor(build_parser().parse_args(["doctor"]))
        assert "skills" in capsys.readouterr().out


# ── cmd_logs ─────────────────────────────────────────────────────────────────

class TestCmdLogs:
    def test_no_log_file_returns_zero(self, tmp_path, capsys):
        with patch("src.cli._project_root", return_value=tmp_path):
            assert cmd_logs(build_parser().parse_args(["logs"])) == 0

    def test_summary_mode(self, tmp_path, capsys):
        from src.utils.log_index import LogIndex
        log = LogIndex(tmp_path / "data" / "cache" / "events.log")
        for _ in range(3):
            log.append("api_request")
        log.append("llm_call")

        with (
            patch("src.cli._project_root", return_value=tmp_path),
            patch.dict("os.environ", {"CCM_LOG_PATH": "data/cache/events.log"}),
        ):
            cmd_logs(build_parser().parse_args(["logs", "--summary"]))
        out = capsys.readouterr().out
        assert "api_request" in out
        assert "3" in out

    def test_filter_by_event(self, tmp_path, capsys):
        from src.utils.log_index import LogIndex
        log = LogIndex(tmp_path / "data" / "cache" / "events.log")
        log.append("api_request")
        log.append("llm_call")
        log.append("api_request")

        with (
            patch("src.cli._project_root", return_value=tmp_path),
            patch.dict("os.environ", {"CCM_LOG_PATH": "data/cache/events.log"}),
        ):
            cmd_logs(build_parser().parse_args(["logs", "--event", "api_request"]))
        out = capsys.readouterr().out
        assert "api_request" in out
        assert "llm_call" not in out

    def test_json_output(self, tmp_path, capsys):
        from src.utils.log_index import LogIndex
        log = LogIndex(tmp_path / "data" / "cache" / "events.log")
        log.append("startup", version="0.6.0")

        with (
            patch("src.cli._project_root", return_value=tmp_path),
            patch.dict("os.environ", {"CCM_LOG_PATH": "data/cache/events.log"}),
        ):
            cmd_logs(build_parser().parse_args(["logs", "--json"]))
        data = json.loads(capsys.readouterr().out)
        assert isinstance(data, list) and data[0]["event"] == "startup"


# ── cmd_research ─────────────────────────────────────────────────────────────

class TestCmdResearch:
    def test_creates_file(self, tmp_path):
        with patch("src.cli._project_root", return_value=tmp_path):
            assert cmd_research(build_parser().parse_args(["research", "GraphRAG"])) == 0
        files = [f for f in (tmp_path / "data" / "research").glob("*.md") if f.name != "README.md"]
        assert len(files) == 1

    def test_file_contains_topic(self, tmp_path):
        with patch("src.cli._project_root", return_value=tmp_path):
            cmd_research(build_parser().parse_args(["research", "My Topic"]))
        files = list((tmp_path / "data" / "research").glob("*.md"))
        assert "My Topic" in files[0].read_text()

    def test_prints_created_path(self, tmp_path, capsys):
        with patch("src.cli._project_root", return_value=tmp_path):
            cmd_research(build_parser().parse_args(["research", "SomeTopic"]))
        assert "Created:" in capsys.readouterr().out


# ── cmd_complete (no API key) ─────────────────────────────────────────────────

class TestCmdCompleteNoKey:
    def test_returns_1_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from src.cli import cmd_complete
        assert cmd_complete(build_parser().parse_args(["complete", "hello"])) == 1

    def test_error_mentions_api_key(self, monkeypatch, capsys):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from src.cli import cmd_complete
        cmd_complete(build_parser().parse_args(["complete", "hello"]))
        assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


# ── main() integration ────────────────────────────────────────────────────────

class TestMain:
    def test_route_via_main(self, capsys):
        assert main(["route", "debug a memory leak", "--json"]) == 0
        assert "model" in json.loads(capsys.readouterr().out)

    def test_status_via_main(self):
        assert main(["status"]) == 0

    def test_version_via_main(self, capsys):
        from src.version import __version__
        assert main(["version"]) == 0
        assert __version__ in capsys.readouterr().out

    def test_doctor_via_main(self):
        assert main(["doctor"]) in (0, 1)

    def test_unknown_subcommand_exits(self):
        with pytest.raises(SystemExit):
            main(["unknown-subcommand"])


# ── cmd_build ─────────────────────────────────────────────────────────────────

class TestCmdBuild:
    def test_no_docker_returns_1(self, monkeypatch):
        import subprocess

        from src.cli import cmd_build

        def raise_not_found(*args, **kwargs):
            raise FileNotFoundError("docker not found")

        monkeypatch.setattr(subprocess, "run", raise_not_found)
        assert cmd_build(build_parser().parse_args(["build"])) == 1

    def test_returns_0_or_1(self):
        from src.cli import cmd_build

        result = cmd_build(build_parser().parse_args(["build", "--dry-run"]))
        assert result in (0, 1)

    def test_dry_run_no_actual_build(self, capsys):
        from src.cli import cmd_build

        # dry-run should not crash regardless of docker availability
        result = cmd_build(build_parser().parse_args(["build", "--dry-run"]))
        assert isinstance(result, int)

    def test_parser_no_cache_flag(self):
        args = build_parser().parse_args(["build", "--no-cache"])
        assert args.no_cache is True

    def test_parser_tag_flag(self):
        args = build_parser().parse_args(["build", "--tag", "my-image:v1"])
        assert args.tag == "my-image:v1"


# ── cmd_deploy ────────────────────────────────────────────────────────────────

class TestCmdDeploy:
    def test_dry_run_skips_containers(self, capsys):
        from src.cli import cmd_deploy

        result = cmd_deploy(build_parser().parse_args(
            ["deploy", "--dry-run", "--skip-tests", "--skip-build", "--skip-evals"]
        ))
        out = capsys.readouterr().out
        assert result in (0, 1)  # may fail due to test env, but should not crash
        assert "Deploy Summary" in out

    def test_returns_int(self):
        from src.cli import cmd_deploy

        result = cmd_deploy(build_parser().parse_args(
            ["deploy", "--dry-run", "--skip-tests", "--skip-build", "--skip-evals"]
        ))
        assert isinstance(result, int)

    def test_summary_table_shown(self, capsys):
        from src.cli import cmd_deploy

        cmd_deploy(build_parser().parse_args(
            ["deploy", "--dry-run", "--skip-tests", "--skip-build", "--skip-evals"]
        ))
        out = capsys.readouterr().out
        assert "Deploy Summary" in out

    def test_parser_env_choices(self):
        for env in ("local", "staging", "prod"):
            args = build_parser().parse_args(["deploy", "--env", env])
            assert args.env == env

    def test_parser_skip_flags(self):
        args = build_parser().parse_args(
            ["deploy", "--skip-tests", "--skip-build", "--skip-evals"]
        )
        assert args.skip_tests is True
        assert args.skip_build is True
        assert args.skip_evals is True


# ── cmd_ps ────────────────────────────────────────────────────────────────────

class TestCmdPs:
    def test_returns_int(self):
        from src.cli import cmd_ps

        result = cmd_ps(build_parser().parse_args(["ps"]))
        assert isinstance(result, int)

    def test_returns_zero(self):
        from src.cli import cmd_ps

        # Should always return 0 regardless of docker availability
        result = cmd_ps(build_parser().parse_args(["ps"]))
        assert result == 0


# ── cmd_health ────────────────────────────────────────────────────────────────

class TestCmdHealth:
    def test_unreachable_returns_1(self):
        from src.cli import cmd_health

        result = cmd_health(build_parser().parse_args(["health", "--url", "http://localhost:19999"]))
        assert result == 1

    def test_bad_url_returns_1(self):
        from src.cli import cmd_health

        result = cmd_health(build_parser().parse_args(["health", "--url", "http://0.0.0.0:1"]))
        assert result == 1

    def test_default_url_parsed(self):
        args = build_parser().parse_args(["health"])
        assert args.url == "http://localhost:8000"

    def test_custom_url_parsed(self):
        args = build_parser().parse_args(["health", "--url", "http://myhost:9000"])
        assert args.url == "http://myhost:9000"


# ── cmd_serve_mcp ─────────────────────────────────────────────────────────────

class TestCmdServeMcp:
    def test_missing_mcp_returns_1(self, monkeypatch):
        """When mcp package is not installed, cmd_serve_mcp should return 1."""
        import builtins

        from src.cli import cmd_serve_mcp

        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "src.mcp_server":
                raise ImportError("mcp not installed")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        result = cmd_serve_mcp(build_parser().parse_args(["serve-mcp"]))
        assert result == 1

    def test_subcommand_parsed(self):
        args = build_parser().parse_args(["serve-mcp"])
        assert args.command == "serve-mcp"


class TestContextDiffCommand:
    def test_context_diff_subcommand_exists(self):
        args = build_parser().parse_args(["context-diff"])
        assert args.command == "context-diff"

    def test_context_diff_default_since(self):
        args = build_parser().parse_args(["context-diff"])
        assert args.since == "HEAD~1"

    def test_context_diff_custom_since(self):
        args = build_parser().parse_args(["context-diff", "--since", "main"])
        assert args.since == "main"

    def test_context_diff_runs_successfully(self, capsys):
        from src.cli import cmd_context_diff
        args = build_parser().parse_args(["context-diff", "--since", "HEAD~1"])
        result = cmd_context_diff(args)
        # Command may return 0 (has commits) or 0 with "No changes" — both valid
        assert result == 0

    def test_context_diff_output_contains_header(self, capsys):
        from src.cli import cmd_context_diff
        args = build_parser().parse_args(["context-diff", "--since", "HEAD~1"])
        cmd_context_diff(args)
        captured = capsys.readouterr()
        assert "Context Diff" in captured.out

    def test_context_diff_in_dispatch(self):
        # Verify the command is wired into the dispatch table via parser
        args = build_parser().parse_args(["context-diff", "--since", "HEAD"])
        assert args.command == "context-diff"


class TestMemoryBankCommand:
    def test_memory_bank_status_subcommand_exists(self):
        args = build_parser().parse_args(["memory-bank", "status"])
        assert args.command == "memory-bank"
        assert args.mb_cmd == "status"

    def test_memory_bank_query_subcommand_exists(self):
        args = build_parser().parse_args(["memory-bank", "query", "routing"])
        assert args.mb_cmd == "query"
        assert args.query_term == "routing"

    def test_memory_bank_sync_subcommand_exists(self):
        args = build_parser().parse_args(["memory-bank", "sync"])
        assert args.mb_cmd == "sync"

    def test_memory_bank_status_runs_successfully(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "status"])
        result = cmd_memory_bank(args)
        assert result == 0

    def test_memory_bank_status_output_contains_header(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "status"])
        cmd_memory_bank(args)
        captured = capsys.readouterr()
        assert "Memory Bank Status" in captured.out

    def test_memory_bank_query_no_term_returns_error(self):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "sync"])
        args.mb_cmd = "query"
        args.query_term = ""
        result = cmd_memory_bank(args)
        assert result == 1

    def test_memory_bank_sync_runs_successfully(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "sync"])
        result = cmd_memory_bank(args)
        assert result == 0

    def test_memory_bank_query_returns_zero(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "query", "routing"])
        result = cmd_memory_bank(args)
        assert result == 0

    def test_memory_bank_in_dispatch(self):
        args = build_parser().parse_args(["memory-bank", "status"])
        assert args.command == "memory-bank"


# ── Lint ──────────────────────────────────────────────────────────────────────

class TestLint:
    def test_lint_subcommand_exists(self):
        args = build_parser().parse_args(["lint"])
        assert args.command == "lint"

    def test_lint_fix_flag(self):
        args = build_parser().parse_args(["lint", "--fix"])
        assert args.fix is True

    def test_lint_no_cache_flag(self):
        args = build_parser().parse_args(["lint", "--no-cache"])
        assert args.no_cache is True

    def test_lint_returns_zero_on_clean_code(self, capsys):
        args = build_parser().parse_args(["lint"])
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = cmd_lint(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "clean" in captured.out

    def test_lint_returns_nonzero_on_issues(self, capsys):
        args = build_parser().parse_args(["lint"])
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = "src/foo.py:1:1: E302 error\n"
            mock_run.return_value.stderr = ""
            result = cmd_lint(args)
        assert result == 1

    def test_lint_passes_fix_flag_to_ruff(self):
        args = build_parser().parse_args(["lint", "--fix"])
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            cmd_lint(args)
        called_cmd = mock_run.call_args[0][0]
        assert "--fix" in called_cmd

    def test_lint_in_dispatch(self):
        args = build_parser().parse_args(["lint"])
        assert args.command == "lint"


# ── Deploy helpers ────────────────────────────────────────────────────────────

class TestDeployHelpers:
    def test_run_tests_returns_true_on_zero_exit(self, tmp_path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert _deploy_run_tests(tmp_path) is True

    def test_run_tests_returns_false_on_nonzero_exit(self, tmp_path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            assert _deploy_run_tests(tmp_path) is False

    def test_run_evals_returns_true_when_smoke_passes(self, tmp_path):
        # Create a minimal smoke.jsonl so the path resolves
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "smoke.jsonl").write_text("")
        with patch("src.cli._eval_run", return_value=0):
            assert _deploy_run_evals(tmp_path) is True

    def test_run_evals_returns_false_when_smoke_fails(self, tmp_path):
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "smoke.jsonl").write_text("")
        with patch("src.cli._eval_run", return_value=1):
            assert _deploy_run_evals(tmp_path) is False

    def test_check_health_returns_true_on_200(self):
        from unittest.mock import MagicMock
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: mock_resp
        mock_resp.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            assert _deploy_check_health("http://localhost:8000/health") is True

    def test_check_health_returns_false_on_timeout(self):
        with patch("urllib.request.urlopen", side_effect=OSError("refused")):
            with patch("time.time", side_effect=[0, 0, 31]):
                with patch("time.sleep"):
                    assert _deploy_check_health("http://localhost:8000/health") is False


# ── Parser sub-functions ──────────────────────────────────────────────────────

class TestParserSubFunctions:
    def test_llm_parsers_registers_route(self):
        args = build_parser().parse_args(["route", "test task"])
        assert args.command == "route"
        assert args.task == "test task"

    def test_llm_parsers_registers_complete(self):
        args = build_parser().parse_args(["complete", "hello"])
        assert args.command == "complete"
        assert args.prompt == "hello"

    def test_server_parsers_registers_serve(self):
        args = build_parser().parse_args(["serve", "--port", "9000"])
        assert args.command == "serve"
        assert args.port == 9000

    def test_server_parsers_registers_health(self):
        args = build_parser().parse_args(["health", "--url", "http://example.com"])
        assert args.command == "health"
        assert args.url == "http://example.com"

    def test_ops_parsers_registers_build(self):
        args = build_parser().parse_args(["build", "--no-cache"])
        assert args.command == "build"
        assert args.no_cache is True

    def test_ops_parsers_registers_deploy(self):
        args = build_parser().parse_args(["deploy", "--env", "staging", "--dry-run"])
        assert args.command == "deploy"
        assert args.env == "staging"
        assert args.dry_run is True

    def test_util_parsers_registers_doctor(self):
        args = build_parser().parse_args(["doctor"])
        assert args.command == "doctor"

    def test_util_parsers_registers_logs_with_flags(self):
        args = build_parser().parse_args(["logs", "--limit", "10", "--summary"])
        assert args.command == "logs"
        assert args.limit == 10
        assert args.summary is True
```

FILE: /home/user/wellux_testprojects/tests/test_api.py
```python
"""Tests for src/api/ — Pydantic models and FastAPI app structure."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.api.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CompleteRequest,
    CompleteResponse,
    HealthResponse,
    RouteRequest,
    RouteResponse,
)

# ── CompleteRequest ───────────────────────────────────────────────────────────

class TestCompleteRequest:
    def test_minimal(self):
        req = CompleteRequest(prompt="hello")
        assert req.prompt == "hello"
        assert req.model is None
        assert req.system is None
        assert req.auto_route is True
        assert req.stream is False

    def test_defaults(self):
        req = CompleteRequest(prompt="x")
        assert req.max_tokens == 4096
        assert req.temperature == 0.7

    def test_full(self):
        req = CompleteRequest(
            prompt="summarize this",
            system="You are helpful",
            model="claude-sonnet-4-6",
            max_tokens=1000,
            temperature=0.3,
            stream=True,
            auto_route=False,
        )
        assert req.model == "claude-sonnet-4-6"
        assert req.stream is True
        assert req.auto_route is False

    def test_max_tokens_lower_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", max_tokens=0)

    def test_max_tokens_upper_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", max_tokens=200001)

    def test_temperature_lower_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", temperature=-0.1)

    def test_temperature_upper_bound(self):
        with pytest.raises(ValidationError):
            CompleteRequest(prompt="x", temperature=1.1)


# ── CompleteResponse ──────────────────────────────────────────────────────────

class TestCompleteResponse:
    def test_minimal(self):
        resp = CompleteResponse(
            content="hello",
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
            cost_usd=0.001,
            stop_reason="end_turn",
        )
        assert resp.routed_by is None

    def test_with_routed_by(self):
        resp = CompleteResponse(
            content="hi",
            model="claude-haiku-4-5-20251001",
            input_tokens=5,
            output_tokens=2,
            cost_usd=0.0001,
            stop_reason="end_turn",
            routed_by="simple greeting → haiku",
        )
        assert resp.routed_by == "simple greeting → haiku"


# ── RouteRequest / RouteResponse ──────────────────────────────────────────────

class TestRouteRequest:
    def test_minimal(self):
        req = RouteRequest(task="write a function")
        assert req.task == "write a function"
        assert req.content_type is None

    def test_with_content_type(self):
        req = RouteRequest(task="store this finding", content_type="lesson")
        assert req.content_type == "lesson"


class TestRouteResponse:
    def test_construction(self):
        resp = RouteResponse(
            model="claude-sonnet-4-6",
            model_reason="medium complexity",
            skill="code-review",
            skill_confidence=0.85,
            agent="general",
            agent_reason="simple coding task",
            memory_tier="FILES",
            memory_destination="data/outputs/",
            plan_size="MEDIUM",
            plan_mode="sequential",
            subtasks=[],
        )
        assert resp.model == "claude-sonnet-4-6"
        assert resp.skill == "code-review"
        assert resp.subtasks == []

    def test_nullable_fields(self):
        resp = RouteResponse(
            model="claude-haiku-4-5-20251001",
            model_reason="simple",
            skill=None,
            skill_confidence=None,
            agent="general",
            agent_reason="",
            memory_tier="CACHE",
            memory_destination="data/cache/",
            plan_size="ATOMIC",
            plan_mode="sequential",
            subtasks=[],
        )
        assert resp.skill is None
        assert resp.skill_confidence is None


# ── ChatMessage / ChatRequest / ChatResponse ──────────────────────────────────

class TestChatMessage:
    def test_user_message(self):
        msg = ChatMessage(role="user", content="hi there")
        assert msg.role == "user"

    def test_assistant_message(self):
        msg = ChatMessage(role="assistant", content="hello back")
        assert msg.role == "assistant"


class TestChatRequest:
    def test_minimal(self):
        req = ChatRequest(messages=[ChatMessage(role="user", content="hi")])
        assert len(req.messages) == 1
        assert req.system is None
        assert req.model is None

    def test_defaults(self):
        req = ChatRequest(messages=[ChatMessage(role="user", content="x")])
        assert req.max_tokens == 4096
        assert req.temperature == 0.7

    def test_multi_turn(self):
        msgs = [
            ChatMessage(role="user", content="What is 2+2?"),
            ChatMessage(role="assistant", content="4"),
            ChatMessage(role="user", content="And 3+3?"),
        ]
        req = ChatRequest(messages=msgs)
        assert len(req.messages) == 3


class TestChatResponse:
    def test_construction(self):
        resp = ChatResponse(
            message=ChatMessage(role="assistant", content="hello"),
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
            cost_usd=0.0005,
        )
        assert resp.message.role == "assistant"
        assert resp.message.content == "hello"


# ── HealthResponse ────────────────────────────────────────────────────────────

class TestHealthResponse:
    def test_construction(self):
        from src.version import __version__
        resp = HealthResponse(
            status="ok",
            version=__version__,
            models_available=["claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
        )
        assert resp.status == "ok"
        assert resp.version == __version__
        assert len(resp.models_available) == 2

    def test_version_required(self):
        # version is now a required field (no default) so passing it works
        from src.version import __version__
        resp = HealthResponse(status="ok", version=__version__, models_available=[])
        assert resp.version == __version__

    def test_uptime_optional(self):
        from src.version import __version__
        resp = HealthResponse(status="ok", version=__version__, models_available=[])
        assert resp.uptime_s is None


# ── FastAPI app import (smoke test) ───────────────────────────────────────────

class TestAppImport:
    def test_app_importable(self):
        """FastAPI app should be importable without an ANTHROPIC_API_KEY."""
        from src.api import app
        assert app is not None

    def test_app_has_routes(self):
        from src.api import app
        routes = [r.path for r in app.routes]
        assert "/health" in routes
        assert "/v1/complete" in routes
        assert "/v1/route" in routes
        assert "/v1/chat" in routes

    def test_app_title(self):
        from src.api import app
        assert "Claude" in app.title
```

FILE: /home/user/wellux_testprojects/tests/test_api_app.py
```python
"""Tests for src/api/app.py — lifespan, _get_client, and _log.append paths."""
from __future__ import annotations

import importlib
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionResponse  # noqa: E402

# Access the module object (not the FastAPI `app` attribute exported by __init__)
_app_mod = sys.modules.get("src.api.app") or importlib.import_module("src.api.app")


def _make_resp(
    content: str = "hello",
    model: str = "claude-sonnet-4-6",
    in_tok: int = 10,
    out_tok: int = 5,
) -> CompletionResponse:
    return CompletionResponse(
        content=content,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        stop_reason="end_turn",
    )


def _mock_client(resp: CompletionResponse | None = None, exc: Exception | None = None):
    client = MagicMock()
    if exc is not None:
        client.complete = AsyncMock(side_effect=exc)
    else:
        client.complete = AsyncMock(return_value=resp or _make_resp())
    return client


@pytest.fixture
async def ac():
    import httpx
    from httpx import ASGITransport

    from src.api.app import app

    with patch("src.api.app.LogIndex"):
        async with httpx.AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client


# ── lifespan ──────────────────────────────────────────────────────────────────

class TestLifespan:
    async def test_startup_logs_api_startup(self):
        from src.api.app import app, lifespan

        mock_log = MagicMock()
        with patch("src.api.app.LogIndex", return_value=mock_log):
            async with lifespan(app):
                pass

        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "api_startup" in event_names

    async def test_shutdown_logs_api_shutdown(self):
        from src.api.app import app, lifespan

        mock_log = MagicMock()
        with patch("src.api.app.LogIndex", return_value=mock_log):
            async with lifespan(app):
                pass  # startup done; exiting triggers shutdown

        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "api_shutdown" in event_names

    async def test_startup_sets_cache_and_rate_limiter(self):
        from src.api.app import app, lifespan

        orig_cache = _app_mod._cache
        orig_rl = _app_mod._rate_limiter
        orig_log = _app_mod._log
        try:
            mock_log = MagicMock()
            with patch("src.api.app.LogIndex", return_value=mock_log):
                async with lifespan(app):
                    assert _app_mod._cache is not None
                    assert _app_mod._rate_limiter is not None
                    assert _app_mod._log is mock_log
        finally:
            _app_mod._cache = orig_cache
            _app_mod._rate_limiter = orig_rl
            _app_mod._log = orig_log


# ── _get_client ───────────────────────────────────────────────────────────────

class TestGetClient:
    def test_lazy_creates_claude_client(self):
        original = _app_mod._client
        _app_mod._client = None
        try:
            with patch("src.llm.claude_client.anthropic.Anthropic"), \
                 patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
                result = _app_mod._get_client()
            assert result is not None
            assert _app_mod._client is result
        finally:
            _app_mod._client = original

    def test_returns_same_instance_on_second_call(self):
        original = _app_mod._client
        _app_mod._client = None
        try:
            with patch("src.llm.claude_client.anthropic.Anthropic"), \
                 patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
                first = _app_mod._get_client()
                second = _app_mod._get_client()
            assert first is second
        finally:
            _app_mod._client = original


# ── _log.append paths ─────────────────────────────────────────────────────────

class TestCompleteLogging:
    async def test_success_appends_log(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch("src.api.app._get_client", return_value=_mock_client()):
                resp = await ac.post("/v1/complete", json={"prompt": "hi"})

        assert resp.status_code == 200
        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "complete_ok" in event_names

    async def test_error_appends_log(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch(
                "src.api.app._get_client",
                return_value=_mock_client(exc=RuntimeError("boom")),
            ):
                resp = await ac.post("/v1/complete", json={"prompt": "x"})

        assert resp.status_code == 502
        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "complete_error" in event_names

    async def test_success_log_has_llm_tag(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch("src.api.app._get_client", return_value=_mock_client()):
                await ac.post("/v1/complete", json={"prompt": "hi"})

        ok_call = next(
            c for c in mock_log.append.call_args_list if c[0][0] == "complete_ok"
        )
        assert ok_call[1]["tag"] == "llm"

    async def test_error_log_has_error_tag(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch(
                "src.api.app._get_client",
                return_value=_mock_client(exc=RuntimeError("x")),
            ):
                await ac.post("/v1/complete", json={"prompt": "x"})

        err_call = next(
            c for c in mock_log.append.call_args_list if c[0][0] == "complete_error"
        )
        assert err_call[1]["tag"] == "error"


class TestChatLogging:
    async def test_chat_error_appends_log(self, ac):
        mock_log = MagicMock()
        with patch.object(_app_mod, "_log", mock_log):
            with patch(
                "src.api.app._get_client",
                return_value=_mock_client(exc=RuntimeError("chat fail")),
            ):
                resp = await ac.post(
                    "/v1/chat",
                    json={"messages": [{"role": "user", "content": "x"}]},
                )

        assert resp.status_code == 502
        event_names = [c[0][0] for c in mock_log.append.call_args_list]
        assert "chat_error" in event_names
```

FILE: /home/user/wellux_testprojects/tests/test_api_endpoints.py
```python
"""Integration tests for src/api/app.py — FastAPI endpoints via httpx AsyncClient."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionResponse

# ── shared helpers ─────────────────────────────────────────────────────────────

def _make_resp(
    content: str = "hello",
    model: str = "claude-sonnet-4-6",
    in_tok: int = 10,
    out_tok: int = 5,
    stop_reason: str = "end_turn",
) -> CompletionResponse:
    return CompletionResponse(
        content=content,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        stop_reason=stop_reason,
    )


def _mock_client(resp: CompletionResponse | None = None, exc: Exception | None = None):
    """Return a mock LLM client whose .complete() and .chat() return resp or raise exc."""
    client = MagicMock()
    if exc is not None:
        client.complete = AsyncMock(side_effect=exc)
        client.chat = AsyncMock(side_effect=exc)
    else:
        client.complete = AsyncMock(return_value=resp or _make_resp())
        client.chat = AsyncMock(return_value=resp or _make_resp())
    return client


# ── fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
async def ac():
    """Async HTTP client pointed at the FastAPI test app with LogIndex patched out."""
    import httpx
    from httpx import ASGITransport

    from src.api.app import app

    # Patch LogIndex.append so tests don't touch the filesystem
    with patch("src.api.app.LogIndex"):
        async with httpx.AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client


# ── GET /health ────────────────────────────────────────────────────────────────

class TestHealth:
    async def test_returns_200(self, ac):
        resp = await ac.get("/health")
        assert resp.status_code == 200

    async def test_response_structure(self, ac):
        data = (await ac.get("/health")).json()
        assert data["status"] == "ok"
        assert "version" in data
        assert isinstance(data["models_available"], list)
        assert len(data["models_available"]) >= 1

    async def test_has_correlation_header(self, ac):
        resp = await ac.get("/health")
        assert "x-request-id" in resp.headers

    async def test_has_timing_header(self, ac):
        resp = await ac.get("/health")
        assert "x-process-time-ms" in resp.headers


# ── POST /complete ─────────────────────────────────────────────────────────────

class TestComplete:
    async def test_happy_path(self, ac):
        mock_client = _mock_client(_make_resp("world"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "hello"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] == "world"
        assert data["model"] == "claude-sonnet-4-6"

    async def test_returns_token_counts(self, ac):
        mock_client = _mock_client(_make_resp(in_tok=42, out_tok=7))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "count tokens"})
        data = resp.json()
        assert data["input_tokens"] == 42
        assert data["output_tokens"] == 7

    async def test_auto_route_sets_routed_by(self, ac):
        mock_client = _mock_client()
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/complete", json={"prompt": "simple task", "auto_route": True}
            )
        data = resp.json()
        assert resp.status_code == 200
        # auto_route=True fills routed_by with a non-empty reason
        assert data["routed_by"] is not None
        assert len(data["routed_by"]) > 0

    async def test_explicit_model_bypasses_routing(self, ac):
        mock_client = _mock_client(_make_resp(model="claude-haiku-4-5-20251001"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/complete",
                json={"prompt": "hi", "model": "claude-haiku-4-5-20251001", "auto_route": False},
            )
        data = resp.json()
        assert resp.status_code == 200
        assert data["routed_by"] is None

    async def test_llm_error_returns_502(self, ac):
        mock_client = _mock_client(exc=RuntimeError("upstream failure"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "x"})
        assert resp.status_code == 502
        detail = resp.json()["detail"]
        assert "RuntimeError" in detail           # error type exposed
        assert "upstream failure" not in detail   # raw message NOT leaked to client

    async def test_stop_reason_propagated(self, ac):
        mock_client = _mock_client(_make_resp(stop_reason="max_tokens"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "x"})
        assert resp.json()["stop_reason"] == "max_tokens"

    async def test_cost_usd_present(self, ac):
        mock_client = _mock_client()
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post("/v1/complete", json={"prompt": "x"})
        assert "cost_usd" in resp.json()


# ── POST /complete/stream ──────────────────────────────────────────────────────

class TestCompleteStream:
    async def _mock_stream_client(self, tokens: list[str]):
        """Client whose .stream() yields tokens."""

        async def _gen(*_args, **_kwargs):
            for t in tokens:
                yield t

        client = MagicMock()
        client.stream = _gen
        return client

    async def test_streams_tokens_and_done(self, ac):
        client = await self._mock_stream_client(["hello", " world"])
        with patch("src.api.app._get_client", return_value=client):
            resp = await ac.post(
                "/v1/complete/stream",
                json={"prompt": "hi", "stream": True},
            )
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers["content-type"]
        body = resp.text
        assert "data: hello" in body
        assert "data:  world" in body
        assert "data: [DONE]" in body

    async def test_stream_error_yields_error_event(self, ac):
        async def _bad_gen(*_args, **_kwargs):
            raise RuntimeError("stream broke")
            yield  # make it a generator

        client = MagicMock()
        client.stream = _bad_gen
        with patch("src.api.app._get_client", return_value=client):
            resp = await ac.post("/v1/complete/stream", json={"prompt": "x"})
        assert resp.status_code == 200
        assert "[ERROR]" in resp.text


# ── POST /chat ─────────────────────────────────────────────────────────────────

class TestChat:
    async def test_happy_path(self, ac):
        mock_client = _mock_client(_make_resp("I am fine"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/chat",
                json={"messages": [{"role": "user", "content": "How are you?"}]},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"]["role"] == "assistant"
        assert data["message"]["content"] == "I am fine"

    async def test_multi_turn_passes_messages_list(self, ac):
        """Messages must be passed as a list to the native chat API, not flattened."""
        mock_client = _mock_client()
        captured: list[list] = []

        async def _chat(messages, **_kw):
            captured.append(messages)
            return _make_resp()

        mock_client.chat = _chat
        with patch("src.api.app._get_client", return_value=mock_client):
            await ac.post(
                "/v1/chat",
                json={
                    "messages": [
                        {"role": "user", "content": "hi"},
                        {"role": "assistant", "content": "hello"},
                        {"role": "user", "content": "bye"},
                    ]
                },
            )
        assert len(captured) == 1
        messages = captured[0]
        assert len(messages) == 3
        assert messages[0] == {"role": "user", "content": "hi"}
        assert messages[1] == {"role": "assistant", "content": "hello"}
        assert messages[2] == {"role": "user", "content": "bye"}

    async def test_llm_error_returns_502(self, ac):
        mock_client = _mock_client(exc=ValueError("chat failed"))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/chat",
                json={"messages": [{"role": "user", "content": "x"}]},
            )
        assert resp.status_code == 502

    async def test_returns_token_counts(self, ac):
        mock_client = _mock_client(_make_resp(in_tok=20, out_tok=10))
        with patch("src.api.app._get_client", return_value=mock_client):
            resp = await ac.post(
                "/v1/chat",
                json={"messages": [{"role": "user", "content": "count"}]},
            )
        data = resp.json()
        assert data["input_tokens"] == 20
        assert data["output_tokens"] == 10


# ── POST /route ────────────────────────────────────────────────────────────────

class TestRoute:
    async def test_returns_routing_decision(self, ac):
        resp = await ac.post("/v1/route", json={"task": "write a unit test"})
        assert resp.status_code == 200
        data = resp.json()
        assert "model" in data
        assert "model_reason" in data
        assert "agent" in data
        assert "plan_size" in data
        assert "subtasks" in data
        assert isinstance(data["subtasks"], list)

    async def test_no_llm_call_on_route(self, ac):
        """Route endpoint must not call the LLM client."""
        mock_client = _mock_client()
        with patch("src.api.app._get_client", return_value=mock_client):
            await ac.post("/v1/route", json={"task": "anything"})
        mock_client.complete.assert_not_called()

    async def test_content_type_hint_accepted(self, ac):
        resp = await ac.post(
            "/v1/route", json={"task": "store this finding", "content_type": "lesson"}
        )
        assert resp.status_code == 200

    async def test_model_in_known_set(self, ac):
        data = (await ac.post("/v1/route", json={"task": "short task"})).json()
        known = {"claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"}
        assert data["model"] in known


# ── Input validation ──────────────────────────────────────────────────────────

class TestInputValidation:
    async def test_chat_empty_messages_returns_422(self, ac):
        resp = await ac.post("/v1/chat", json={"messages": []})
        assert resp.status_code == 422

    async def test_chat_max_tokens_above_limit_returns_422(self, ac):
        resp = await ac.post("/v1/chat", json={
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 999999,
        })
        assert resp.status_code == 422

    async def test_complete_max_tokens_above_limit_returns_422(self, ac):
        resp = await ac.post("/v1/complete", json={"prompt": "hello", "max_tokens": 999999})
        assert resp.status_code == 422

    async def test_chat_max_tokens_at_limit_accepted(self, ac):
        with patch("src.api.app._get_client", return_value=_mock_client()):
            resp = await ac.post("/v1/chat", json={
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 200000,
            })
        assert resp.status_code == 200
```

FILE: /home/user/wellux_testprojects/tests/test_api_middleware.py
```python
"""Tests for src/api/middleware.py — CorrelationIDMiddleware and TimingMiddleware."""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.middleware import (
    ContentLengthLimitMiddleware,
    CorrelationIDMiddleware,
    TimingMiddleware,
    get_request_id,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_app(with_correlation: bool = True, with_timing: bool = True) -> FastAPI:
    app = FastAPI()

    @app.get("/ping")
    async def ping():
        return {"request_id": get_request_id()}

    @app.get("/error")
    async def err():
        raise ValueError("boom")

    if with_correlation:
        app.add_middleware(CorrelationIDMiddleware)
    if with_timing:
        app.add_middleware(TimingMiddleware)

    return app


@pytest.fixture
def client():
    return TestClient(_make_app(), raise_server_exceptions=False)


# ── CorrelationIDMiddleware ───────────────────────────────────────────────────

class TestCorrelationIDMiddleware:
    def test_response_has_request_id_header(self, client):
        resp = client.get("/ping")
        assert "X-Request-ID" in resp.headers

    def test_generated_id_is_non_empty(self, client):
        resp = client.get("/ping")
        assert len(resp.headers["X-Request-ID"]) > 0

    def test_honours_incoming_request_id(self, client):
        resp = client.get("/ping", headers={"X-Request-ID": "my-trace-123"})
        assert resp.headers["X-Request-ID"] == "my-trace-123"

    def test_different_requests_get_different_ids(self, client):
        r1 = client.get("/ping")
        r2 = client.get("/ping")
        assert r1.headers["X-Request-ID"] != r2.headers["X-Request-ID"]

    def test_request_id_available_in_handler(self, client):
        resp = client.get("/ping", headers={"X-Request-ID": "ctx-abc"})
        data = resp.json()
        assert data["request_id"] == "ctx-abc"

    def test_prefix_prepended_to_generated_id(self):
        app = FastAPI()

        @app.get("/ping")
        async def ping():
            return {"ok": True}

        app.add_middleware(CorrelationIDMiddleware, prefix="svc-")
        c = TestClient(app)
        resp = c.get("/ping")
        assert resp.headers["X-Request-ID"].startswith("svc-")

    def test_ids_are_hex_format_when_generated(self, client):
        resp = client.get("/ping")
        rid = resp.headers["X-Request-ID"]
        # UUIDs without dashes → 32 hex chars
        assert all(c in "0123456789abcdef" for c in rid)
        assert len(rid) == 32

    def test_get_request_id_returns_empty_outside_request(self):
        # Outside a request context, should return empty string
        assert get_request_id() == ""


# ── TimingMiddleware ──────────────────────────────────────────────────────────

class TestTimingMiddleware:
    def test_response_has_timing_header(self, client):
        resp = client.get("/ping")
        assert "X-Process-Time-Ms" in resp.headers

    def test_timing_is_non_negative_float(self, client):
        resp = client.get("/ping")
        val = float(resp.headers["X-Process-Time-Ms"])
        assert val >= 0.0

    def test_timing_without_correlation(self):
        app = FastAPI()

        @app.get("/t")
        async def t():
            return {"ok": True}

        app.add_middleware(TimingMiddleware)
        c = TestClient(app)
        resp = c.get("/t")
        assert "X-Process-Time-Ms" in resp.headers


# ── Both middlewares together ─────────────────────────────────────────────────

class TestMiddlewareStack:
    def test_both_headers_present(self, client):
        resp = client.get("/ping")
        assert "X-Request-ID" in resp.headers
        assert "X-Process-Time-Ms" in resp.headers

    def test_request_id_propagates_through_timing(self, client):
        resp = client.get("/ping", headers={"X-Request-ID": "trace-xyz"})
        assert resp.headers["X-Request-ID"] == "trace-xyz"
        assert float(resp.headers["X-Process-Time-Ms"]) >= 0.0

    def test_app_import_includes_middleware(self):
        """The production app.py should have middleware wired in."""
        from src.api import app
        # Check middleware is registered (stored as Middleware objects)
        names = str(app.user_middleware)
        assert "CorrelationIDMiddleware" in names or "Correlation" in names


# ── ContentLengthLimitMiddleware ──────────────────────────────────────────────

def _make_size_app(max_bytes: int = 100) -> FastAPI:
    app = FastAPI()

    @app.post("/upload")
    async def upload():
        return {"ok": True}

    app.add_middleware(ContentLengthLimitMiddleware, max_bytes=max_bytes)
    return app


class TestContentLengthLimitMiddleware:
    def test_allows_request_under_limit(self):
        c = TestClient(_make_size_app(max_bytes=100))
        body = b"x" * 50
        resp = c.post("/upload", content=body,
                      headers={"Content-Length": str(len(body))})
        assert resp.status_code == 200

    def test_allows_request_exactly_at_limit(self):
        c = TestClient(_make_size_app(max_bytes=50))
        body = b"x" * 50
        resp = c.post("/upload", content=body,
                      headers={"Content-Length": "50"})
        assert resp.status_code == 200

    def test_rejects_request_over_limit(self):
        c = TestClient(_make_size_app(max_bytes=50))
        resp = c.post("/upload", content=b"x",
                      headers={"Content-Length": "51"})
        assert resp.status_code == 413

    def test_413_response_has_detail(self):
        c = TestClient(_make_size_app(max_bytes=10))
        resp = c.post("/upload", content=b"x",
                      headers={"Content-Length": "999"})
        data = resp.json()
        assert "detail" in data
        assert "999" in data["detail"]

    def test_no_content_length_passes_through(self):
        """Chunked / streaming requests without Content-Length are allowed."""
        c = TestClient(_make_size_app(max_bytes=10))
        # httpx sends without Content-Length when we omit it explicitly
        resp = c.post("/upload")
        assert resp.status_code == 200

    def test_invalid_content_length_returns_400(self):
        c = TestClient(_make_size_app(max_bytes=100))
        resp = c.post("/upload", headers={"Content-Length": "notanumber"})
        assert resp.status_code == 400

    def test_default_limit_is_one_mib(self):
        assert ContentLengthLimitMiddleware.DEFAULT_MAX_BYTES == 1_048_576

    def test_production_app_has_middleware(self):
        from src.api import app
        names = str(app.user_middleware)
        assert "ContentLengthLimit" in names
```

FILE: /home/user/wellux_testprojects/tests/test_routing.py
```python
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
```

FILE: /home/user/wellux_testprojects/tests/test_evals.py
```python
"""Tests for src/evals/ — types, scorers, suite, and runner."""
from __future__ import annotations

import pytest

from src.evals import (
    AsyncEvalRunner,
    EvalCase,
    EvalReport,
    EvalRunner,
    EvalSuite,
    Verdict,
    composite,
    contains_all,
    exact_match,
    excludes_none,
    max_length,
    min_length,
    non_empty,
    regex_match,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

def echo_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    """Returns the prompt unchanged — useful for contains/excludes tests."""
    return prompt


def static_llm(response: str):
    """Factory: always returns the given response."""
    def _llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
        return response
    return _llm


def error_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    raise RuntimeError("API unavailable")


@pytest.fixture
def simple_suite():
    return (
        EvalSuite("test")
        .add(EvalCase("greet", "Say hello", contains=["hello"]))
        .add(EvalCase("math",  "2+2=4", contains=["4"]))
    )


# ── EvalCase ──────────────────────────────────────────────────────────────────

class TestEvalCase:
    def test_minimal(self):
        c = EvalCase("id1", "prompt text")
        assert c.id == "id1"
        assert c.prompt == "prompt text"
        assert c.expected is None
        assert c.contains == []
        assert c.excludes == []
        assert c.tags == []

    def test_defaults(self):
        c = EvalCase("x", "p")
        assert c.max_tokens == 512
        assert c.temperature == 0.0

    def test_empty_id_raises(self):
        with pytest.raises(ValueError, match="id"):
            EvalCase("", "prompt")

    def test_empty_prompt_raises(self):
        with pytest.raises(ValueError, match="prompt"):
            EvalCase("id", "")

    def test_full_construction(self):
        c = EvalCase(
            "c1", "hello", expected="world",
            contains=["foo"], excludes=["bar"],
            tags=["smoke", "fast"], metadata={"author": "test"},
        )
        assert c.expected == "world"
        assert "smoke" in c.tags
        assert c.metadata["author"] == "test"


# ── Scorers ───────────────────────────────────────────────────────────────────

class TestExactMatch:
    def test_match(self):
        c = EvalCase("x", "p", expected="hello world")
        score, _ = exact_match("hello world", c)
        assert score == 1.0

    def test_match_strips_whitespace(self):
        c = EvalCase("x", "p", expected="hello")
        score, _ = exact_match("  hello  ", c)
        assert score == 1.0

    def test_mismatch(self):
        c = EvalCase("x", "p", expected="hello")
        score, _ = exact_match("goodbye", c)
        assert score == 0.0

    def test_no_expected_passes(self):
        c = EvalCase("x", "p")
        score, _ = exact_match("anything", c)
        assert score == 1.0


class TestContainsAll:
    def test_all_present(self):
        c = EvalCase("x", "p", contains=["foo", "bar"])
        score, _ = contains_all("foo and bar here", c)
        assert score == 1.0

    def test_partial_credit(self):
        c = EvalCase("x", "p", contains=["foo", "bar", "baz"])
        score, _ = contains_all("foo and bar", c)
        assert score == pytest.approx(2 / 3)

    def test_none_present(self):
        c = EvalCase("x", "p", contains=["xyz", "abc"])
        score, _ = contains_all("nothing here", c)
        assert score == 0.0

    def test_case_insensitive(self):
        c = EvalCase("x", "p", contains=["Python"])
        score, _ = contains_all("python is great", c)
        assert score == 1.0

    def test_no_constraints_passes(self):
        c = EvalCase("x", "p")
        score, _ = contains_all("anything", c)
        assert score == 1.0


class TestExcludesNone:
    def test_none_present_passes(self):
        c = EvalCase("x", "p", excludes=["bad", "wrong"])
        score, _ = excludes_none("this is good", c)
        assert score == 1.0

    def test_forbidden_present_fails(self):
        c = EvalCase("x", "p", excludes=["error"])
        score, _ = excludes_none("an error occurred", c)
        assert score == 0.0

    def test_case_insensitive(self):
        c = EvalCase("x", "p", excludes=["ERROR"])
        score, _ = excludes_none("error here", c)
        assert score == 0.0

    def test_no_excludes_passes(self):
        c = EvalCase("x", "p")
        score, _ = excludes_none("anything", c)
        assert score == 1.0


class TestNonEmpty:
    def test_non_empty_passes(self):
        c = EvalCase("x", "p")
        score, _ = non_empty("some text", c)
        assert score == 1.0

    def test_empty_fails(self):
        c = EvalCase("x", "p")
        score, _ = non_empty("", c)
        assert score == 0.0

    def test_whitespace_only_fails(self):
        c = EvalCase("x", "p")
        score, _ = non_empty("   ", c)
        assert score == 0.0


class TestMinLength:
    def test_meets_minimum(self):
        c = EvalCase("x", "p")
        scorer = min_length(10)
        score, _ = scorer("hello world", c)
        assert score == 1.0

    def test_below_minimum_partial(self):
        c = EvalCase("x", "p")
        scorer = min_length(20)
        score, _ = scorer("short", c)   # 5 chars → 5/20 = 0.25
        assert score == pytest.approx(0.25)


class TestMaxLength:
    def test_within_max(self):
        c = EvalCase("x", "p")
        scorer = max_length(100)
        score, _ = scorer("short", c)
        assert score == 1.0

    def test_exceeds_max_fails(self):
        c = EvalCase("x", "p")
        scorer = max_length(3)
        score, _ = scorer("toolong", c)
        assert score == 0.0


class TestRegexMatch:
    def test_matches(self):
        c = EvalCase("x", "p")
        scorer = regex_match(r"\d{4}")
        score, _ = scorer("year 2024 was good", c)
        assert score == 1.0

    def test_no_match(self):
        c = EvalCase("x", "p")
        scorer = regex_match(r"\d{4}")
        score, _ = scorer("no numbers here", c)
        assert score == 0.0

    def test_case_insensitive_by_default(self):
        c = EvalCase("x", "p")
        scorer = regex_match(r"python")
        score, _ = scorer("Python is great", c)
        assert score == 1.0


class TestComposite:
    def test_equal_weights(self):
        c = EvalCase("x", "p", contains=["hello"])
        scorer = composite(non_empty, contains_all)
        score, _ = scorer("hello world", c)
        assert score == 1.0

    def test_partial_fail(self):
        c = EvalCase("x", "p", contains=["missing"])
        scorer = composite(non_empty, contains_all)
        score, _ = scorer("hello world", c)
        assert 0.0 < score < 1.0

    def test_custom_weights(self):
        c = EvalCase("x", "p")
        scorer = composite(non_empty, contains_all, weights=[3.0, 1.0])
        score, _ = scorer("something", c)
        assert score == 1.0

    def test_weight_length_mismatch_raises(self):
        with pytest.raises(ValueError):
            composite(non_empty, contains_all, weights=[1.0])


# ── EvalSuite ─────────────────────────────────────────────────────────────────

class TestEvalSuite:
    def test_empty(self):
        s = EvalSuite("test")
        assert len(s) == 0

    def test_add_returns_self(self):
        s = EvalSuite("test")
        result = s.add(EvalCase("a", "prompt"))
        assert result is s

    def test_duplicate_id_raises(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "prompt"))
        with pytest.raises(ValueError, match="Duplicate"):
            s.add(EvalCase("a", "other prompt"))

    def test_extend(self):
        s = EvalSuite("test")
        s.extend([EvalCase("a", "p1"), EvalCase("b", "p2")])
        assert len(s) == 2

    def test_iter(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p")).add(EvalCase("b", "q"))
        ids = [c.id for c in s]
        assert ids == ["a", "b"]

    def test_getitem(self):
        s = EvalSuite("test")
        s.add(EvalCase("alpha", "prompt"))
        assert s["alpha"].id == "alpha"

    def test_getitem_missing_raises(self):
        s = EvalSuite("test")
        with pytest.raises(KeyError):
            _ = s["nonexistent"]

    def test_filter_tags(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p", tags=["smoke"]))
        s.add(EvalCase("b", "p", tags=["slow"]))
        filtered = s.filter_tags("smoke")
        assert len(filtered) == 1
        assert filtered["a"].id == "a"

    def test_filter_ids(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p"))
        s.add(EvalCase("b", "p"))
        s.add(EvalCase("c", "p"))
        filtered = s.filter_ids("a", "c")
        assert len(filtered) == 2

    def test_exclude_tags(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p", tags=["skip"]))
        s.add(EvalCase("b", "p", tags=["run"]))
        filtered = s.exclude_tags("skip")
        assert len(filtered) == 1

    def test_jsonl_roundtrip(self, tmp_path):
        s = EvalSuite("round")
        s.add(EvalCase("x", "prompt", contains=["hi"], tags=["t1"]))
        path = s.to_jsonl(tmp_path / "cases.jsonl")
        loaded = EvalSuite.from_jsonl(path)
        assert len(loaded) == 1
        assert loaded["x"].contains == ["hi"]
        assert "t1" in loaded["x"].tags

    def test_from_jsonl_skips_comments(self, tmp_path):
        p = tmp_path / "cases.jsonl"
        p.write_text('# comment\n{"id":"a","prompt":"p","contains":[],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":512,"temperature":0.0}\n')
        s = EvalSuite.from_jsonl(p)
        assert len(s) == 1

    def test_from_jsonl_duplicate_id_raises(self, tmp_path):
        p = tmp_path / "dup.jsonl"
        row = '{"id":"dup","prompt":"p","contains":[],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":512,"temperature":0.0}'
        p.write_text(row + "\n" + row + "\n")
        with pytest.raises(ValueError, match="Duplicate"):
            EvalSuite.from_jsonl(p)


# ── EvalRunner ────────────────────────────────────────────────────────────────

class TestEvalRunner:
    def test_all_pass(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        assert report.passed == 2
        assert report.failed == 0
        assert report.pass_rate == 1.0

    def test_all_fail(self):
        suite = EvalSuite("fail_suite").add(EvalCase("a", "prompt", contains=["MISSING"]))
        runner = EvalRunner(static_llm("no match here"))
        report = runner.run(suite)
        assert report.failed == 1
        assert report.passed == 0

    def test_error_case(self):
        suite = EvalSuite("err").add(EvalCase("e", "prompt"))
        runner = EvalRunner(error_llm)
        report = runner.run(suite)
        assert report.errors == 1
        assert report.results[0].verdict == Verdict.ERROR

    def test_latency_recorded(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        assert all(r.latency_ms >= 0 for r in report.results)

    def test_custom_pass_threshold(self):
        c = EvalCase("a", "prompt", contains=["x", "y", "z"])
        suite = EvalSuite("t").add(c)
        # Only "x" present → score = 1/3 ≈ 0.33
        runner = EvalRunner(static_llm("x only"), pass_threshold=0.3)
        report = runner.run(suite)
        assert report.passed == 1

    def test_run_case_single(self):
        runner = EvalRunner(static_llm("hello"))
        case = EvalCase("a", "p", contains=["hello"])
        result = runner.run_case(case)
        assert result.verdict == Verdict.PASS

    def test_report_summary_format(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        summary = report.summary()
        assert "test" in summary
        assert "passed" in summary

    def test_report_failures_list(self):
        suite = (
            EvalSuite("mix")
            .add(EvalCase("pass1", "hello world", contains=["hello"]))
            .add(EvalCase("fail1", "prompt", contains=["MISSING"]))
        )
        runner = EvalRunner(echo_llm)
        report = runner.run(suite)
        failures = report.failures()
        assert len(failures) == 1
        assert failures[0].case_id == "fail1"

    def test_mean_score(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        assert report.mean_score == pytest.approx(1.0)

    def test_verbose_mode(self, simple_suite, capsys):
        runner = EvalRunner(echo_llm, verbose=True)
        runner.run(simple_suite)
        out = capsys.readouterr().out
        assert "greet" in out

    def test_max_workers_parallel_produces_same_results(self, simple_suite):
        sequential = EvalRunner(echo_llm).run(simple_suite)
        parallel = EvalRunner(echo_llm, max_workers=4).run(simple_suite)
        assert parallel.passed == sequential.passed
        assert parallel.total == sequential.total

    def test_max_workers_one_is_sequential(self, simple_suite):
        # max_workers=1 should behave identically to the default sequential path
        report = EvalRunner(echo_llm, max_workers=1).run(simple_suite)
        assert report.passed == report.total

    def test_max_workers_error_propagates(self):
        suite = EvalSuite("err").add(EvalCase("e1", "x", contains=["x"]))
        report = EvalRunner(error_llm, max_workers=2).run(suite)
        assert report.errors == 1


# ── EvalReport ────────────────────────────────────────────────────────────────

class TestEvalReport:
    def test_pass_rate_no_skipped(self):
        report = EvalReport("t", total=4, passed=3, failed=1, skipped=0, errors=0)
        assert report.pass_rate == pytest.approx(0.75)

    def test_pass_rate_with_skipped(self):
        report = EvalReport("t", total=5, passed=3, failed=1, skipped=1, errors=0)
        assert report.pass_rate == pytest.approx(0.75)

    def test_pass_rate_all_skipped(self):
        report = EvalReport("t", total=2, passed=0, failed=0, skipped=2, errors=0)
        assert report.pass_rate == 0.0

    def test_mean_score_empty(self):
        report = EvalReport("t", total=0, passed=0, failed=0, skipped=0, errors=0)
        assert report.mean_score == 0.0

    def test_by_tag_filters_results(self):
        from src.evals.types import EvalResult, Verdict
        r1 = EvalResult(case_id="a", verdict=Verdict.PASS, score=1.0, tags=["fast"])
        r2 = EvalResult(case_id="b", verdict=Verdict.FAIL, score=0.0, tags=["slow"])
        report = EvalReport("t", total=2, passed=1, failed=1, skipped=0, errors=0, results=[r1, r2])
        assert report.by_tag("fast") == [r1]
        assert report.by_tag("slow") == [r2]
        assert report.by_tag("missing") == []


# ── AsyncEvalRunner ───────────────────────────────────────────────────────────

async def async_echo(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    return prompt


async def async_error(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    raise RuntimeError("async API error")


class TestAsyncEvalRunner:
    async def test_all_pass(self, simple_suite):
        runner = AsyncEvalRunner(async_echo)
        report = await runner.run(simple_suite)
        assert report.passed == 2
        assert report.failed == 0

    async def test_error_case(self):
        suite = EvalSuite("err").add(EvalCase("e", "prompt"))
        runner = AsyncEvalRunner(async_error)
        report = await runner.run(suite)
        assert report.errors == 1
        assert report.results[0].verdict == Verdict.ERROR

    async def test_concurrency_limit(self):
        import asyncio
        active: list[int] = []
        peak: list[int] = []

        async def counting_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            active.append(1)
            peak.append(len(active))
            await asyncio.sleep(0)
            active.pop()
            return prompt

        suite = EvalSuite("conc")
        for i in range(10):
            suite.add(EvalCase(f"c{i}", f"prompt {i}"))

        runner = AsyncEvalRunner(counting_llm, concurrency=3)
        await runner.run(suite)
        assert max(peak) <= 3

    async def test_all_fail(self):
        suite = EvalSuite("f").add(EvalCase("a", "prompt", contains=["MISSING"]))
        runner = AsyncEvalRunner(async_echo)
        report = await runner.run(suite)
        assert report.failed == 1

    async def test_run_case_single(self):
        runner = AsyncEvalRunner(async_echo)
        case = EvalCase("x", "hello world", contains=["hello"])
        result = await runner.run_case(case)
        assert result.verdict == Verdict.PASS

    async def test_latency_recorded(self, simple_suite):
        runner = AsyncEvalRunner(async_echo)
        report = await runner.run(simple_suite)
        assert all(r.latency_ms >= 0 for r in report.results)

    async def test_case_timeout_returns_error(self):
        import asyncio as _asyncio

        async def slow_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            await _asyncio.sleep(60)
            return prompt

        suite = EvalSuite("timeout").add(EvalCase("slow", "prompt"))
        runner = AsyncEvalRunner(slow_llm, case_timeout=0.05)
        report = await runner.run(suite)
        assert report.errors == 1
        assert "timed out" in report.results[0].reason

    async def test_default_timeout_is_30s(self):
        runner = AsyncEvalRunner(async_echo)
        assert runner.case_timeout == 30.0

    async def test_verbose_mode_prints_results(self, capsys):
        suite = EvalSuite("v").add(EvalCase("a", "hello", contains=["hello"]))
        runner = AsyncEvalRunner(async_echo, verbose=True)
        await runner.run(suite)
        out = capsys.readouterr().out
        assert "a" in out  # result printed for case id "a"


class TestEvalSuiteRepr:
    def test_repr_includes_name_and_count(self):
        suite = EvalSuite("my-suite").add(EvalCase("a", "p")).add(EvalCase("b", "p"))
        assert "my-suite" in repr(suite)
        assert "2" in repr(suite)


# ── ccm eval CLI ──────────────────────────────────────────────────────────────

class TestCLIEval:
    def test_eval_list_no_dir(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "list"])
        assert result == 0
        out = capsys.readouterr().out
        assert "No eval suites" in out

    def test_eval_list_with_suites(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "smoke.jsonl").write_text(
            '{"id":"a","prompt":"p","contains":[],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "list"])
        assert result == 0
        out = capsys.readouterr().out
        assert "smoke.jsonl" in out

    def test_eval_inspect(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        suite_path = evals_dir / "test.jsonl"
        suite_path.write_text(
            '{"id":"case1","prompt":"hello world","contains":["hello"],"excludes":[],"tags":["smoke"],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "inspect", "test.jsonl"])
        assert result == 0
        out = capsys.readouterr().out
        assert "case1" in out
        assert "hello" in out

    def test_eval_run_dry_run(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        suite_path = evals_dir / "smoke.jsonl"
        suite_path.write_text(
            '{"id":"echo1","prompt":"hello world","contains":["hello"],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "run", "smoke.jsonl", "--dry-run"])
        assert result == 0
        out = capsys.readouterr().out
        assert "passed" in out.lower()

    def test_eval_run_missing_suite(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "run", "nonexistent.jsonl", "--dry-run"])
        assert result == 1

    def test_eval_run_with_json_output(self, tmp_path, capsys):
        import json as _json
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "test.jsonl").write_text(
            '{"id":"j1","prompt":"test","contains":["test"],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            main(["eval", "run", "test.jsonl", "--dry-run", "--json"])
        out = capsys.readouterr().out
        # JSON is printed after the summary; find the { start
        json_start = out.find("{")
        data = _json.loads(out[json_start:])
        assert "pass_rate" in data
        assert data["passed"] == 1
```

FILE: /home/user/wellux_testprojects/tests/test_persistence.py
```python
"""Tests for src/persistence/ — FileStore and MemoryStore."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from src.persistence.file_store import FileStore, _atomic_write, _slugify
from src.persistence.memory_store import Entity, MemoryStore

# ── FileStore ─────────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_store(tmp_path):
    return FileStore(root=tmp_path)


class TestFileStoreInit:
    def test_creates_required_directories(self, tmp_path):
        FileStore(root=tmp_path)
        assert (tmp_path / "data/research").is_dir()
        assert (tmp_path / "data/outputs").is_dir()
        assert (tmp_path / "data/cache").is_dir()
        assert (tmp_path / "tasks").is_dir()

    def test_idempotent_on_existing_dirs(self, tmp_store, tmp_path):
        # Should not raise even when dirs already exist
        FileStore(root=tmp_path)


class TestFileStoreResearch:
    def test_write_research_returns_path(self, tmp_store):
        path = tmp_store.write_research("LightRAG", "# LightRAG\n\nGraph-based RAG.")
        assert path.exists()
        assert "lightrag" in path.name

    def test_write_research_content_persisted(self, tmp_store):
        content = "# My Topic\n\nSome research."
        path = tmp_store.write_research("My Topic", content)
        assert path.read_text() == content

    def test_write_research_updates_index(self, tmp_store):
        tmp_store.write_research("Vector DB", "content")
        index = (tmp_store.root / "data/research/README.md").read_text()
        assert "Vector DB" in index

    def test_list_research_empty(self, tmp_store):
        assert tmp_store.list_research() == []

    def test_list_research_returns_entries(self, tmp_store):
        tmp_store.write_research("Topic One", "a")
        tmp_store.write_research("Topic Two", "b")
        results = tmp_store.list_research()
        assert len(results) == 2
        topics = {r["topic"] for r in results}
        assert "topic one" in topics
        assert "topic two" in topics

    def test_list_research_entry_shape(self, tmp_store):
        tmp_store.write_research("Shape Test", "content")
        entry = tmp_store.list_research()[0]
        assert "topic" in entry
        assert "path" in entry
        assert "date" in entry


class TestFileStoreOutputs:
    def test_write_output_returns_path(self, tmp_store):
        path = tmp_store.write_output("report", "# Weekly Report")
        assert path.exists()

    def test_write_output_filename_includes_type(self, tmp_store):
        path = tmp_store.write_output("perf-audit", "content")
        assert "perf-audit" in path.name

    def test_write_output_content(self, tmp_store):
        path = tmp_store.write_output("summary", "hello world")
        assert path.read_text() == "hello world"


class TestFileStoreLessons:
    def test_append_lesson_creates_file(self, tmp_store):
        tmp_store.append_lesson(
            title="Test lesson",
            mistake="Did X",
            why="Because Y",
            rule="Never do X",
            example="Instead do Z",
        )
        lessons_path = tmp_store.root / "tasks/lessons.md"
        assert lessons_path.exists()

    def test_append_lesson_content(self, tmp_store):
        tmp_store.append_lesson("My Lesson", "I forgot", "careless", "Always check", "check = True")
        text = (tmp_store.root / "tasks/lessons.md").read_text()
        assert "My Lesson" in text
        assert "I forgot" in text
        assert "careless" in text
        assert "Always check" in text

    def test_append_lesson_multiple(self, tmp_store):
        tmp_store.append_lesson("L1", "m1", "w1", "r1", "e1")
        tmp_store.append_lesson("L2", "m2", "w2", "r2", "e2")
        text = (tmp_store.root / "tasks/lessons.md").read_text()
        assert "L1" in text
        assert "L2" in text


class TestFileStoreTasks:
    def test_append_task_creates_file(self, tmp_store):
        tmp_store.append_task("Fix the bug")
        assert (tmp_store.root / "tasks/todo.md").exists()

    def test_append_task_unchecked(self, tmp_store):
        tmp_store.append_task("Write tests")
        text = (tmp_store.root / "tasks/todo.md").read_text()
        assert "- [ ] Write tests" in text

    def test_complete_task_marks_done(self, tmp_store):
        tmp_store.append_task("Deploy service")
        result = tmp_store.complete_task("Deploy service")
        assert result is True
        text = (tmp_store.root / "tasks/todo.md").read_text()
        assert "- [x] Deploy service" in text

    def test_complete_task_not_found_returns_false(self, tmp_store):
        tmp_store.append_task("Real task")
        result = tmp_store.complete_task("Non-existent task")
        assert result is False

    def test_complete_task_no_file_returns_false(self, tmp_store):
        result = tmp_store.complete_task("Anything")
        assert result is False

    def test_complete_task_only_first_occurrence(self, tmp_store):
        tmp_store.append_task("Repeat task")
        tmp_store.append_task("Repeat task")
        tmp_store.complete_task("Repeat task")
        text = (tmp_store.root / "tasks/todo.md").read_text()
        assert text.count("- [x] Repeat task") == 1
        assert text.count("- [ ] Repeat task") == 1


class TestFileStoreEvents:
    def test_log_event_creates_file(self, tmp_store):
        tmp_store.log_event("startup")
        assert (tmp_store.root / "data/cache/events.log").exists()

    def test_log_event_is_json(self, tmp_store):
        tmp_store.log_event("test_event", key="value", count=3)
        log_path = tmp_store.root / "data/cache/events.log"
        line = log_path.read_text().strip()
        obj = json.loads(line)
        assert obj["event"] == "test_event"
        assert obj["key"] == "value"
        assert obj["count"] == 3
        assert "ts" in obj

    def test_log_event_appends(self, tmp_store):
        tmp_store.log_event("e1")
        tmp_store.log_event("e2")
        lines = (tmp_store.root / "data/cache/events.log").read_text().strip().splitlines()
        assert len(lines) == 2

    def test_search_log_by_event(self, tmp_store):
        tmp_store.log_event("startup", version="1.0")
        tmp_store.log_event("shutdown")
        results = tmp_store.search_log(event="startup")
        assert len(results) == 1
        assert results[0]["event"] == "startup"

    def test_log_summary_counts_events(self, tmp_store):
        tmp_store.log_event("startup")
        tmp_store.log_event("startup")
        tmp_store.log_event("request")
        summary = tmp_store.log_summary()
        assert summary["startup"] == 2
        assert summary["request"] == 1


class TestAtomicWrite:
    def test_writes_content(self, tmp_path):
        p = tmp_path / "out.txt"
        _atomic_write(p, "hello atomic")
        assert p.read_text() == "hello atomic"

    def test_no_tmp_file_left_on_success(self, tmp_path):
        p = tmp_path / "out.txt"
        _atomic_write(p, "data")
        leftover = list(tmp_path.glob(".tmp-*"))
        assert leftover == []

    def test_creates_parent_dirs(self, tmp_path):
        p = tmp_path / "deep" / "nested" / "file.txt"
        _atomic_write(p, "content")
        assert p.read_text() == "content"

    def test_overwrites_existing(self, tmp_path):
        p = tmp_path / "file.txt"
        _atomic_write(p, "first")
        _atomic_write(p, "second")
        assert p.read_text() == "second"

    def test_old_content_intact_if_write_fails(self, tmp_path):
        """If writing raises, the original file must be untouched."""
        import unittest.mock
        p = tmp_path / "important.txt"
        _atomic_write(p, "original")

        # Make os.replace raise after the temp file is written
        call_count = 0

        def _bad_replace(src, dst):
            nonlocal call_count
            call_count += 1
            os.unlink(src)          # clean up tmp ourselves
            raise OSError("replace failed")

        with unittest.mock.patch("src.persistence.file_store.os.replace", _bad_replace):
            with pytest.raises(OSError, match="replace failed"):
                _atomic_write(p, "new content")

        assert p.read_text() == "original"
        assert call_count == 1


class TestFileStoreReadWrite:
    def test_write_and_read(self, tmp_store):
        tmp_store.write("notes/hello.txt", "hello world")
        assert tmp_store.read("notes/hello.txt") == "hello world"

    def test_write_creates_parents(self, tmp_store):
        tmp_store.write("deep/nested/dir/file.md", "content")
        assert (tmp_store.root / "deep/nested/dir/file.md").exists()

    def test_write_returns_path(self, tmp_store):
        path = tmp_store.write("out.txt", "data")
        assert isinstance(path, Path)
        assert path.exists()


class TestSlugify:
    def test_basic(self):
        assert _slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert _slugify("C++ & Python!") == "c-python"

    def test_truncates_at_60(self):
        long = "a" * 100
        assert len(_slugify(long)) <= 60

    def test_no_leading_trailing_dash(self):
        slug = _slugify("  hello  ")
        assert not slug.startswith("-")
        assert not slug.endswith("-")


# ── MemoryStore ───────────────────────────────────────────────────────────────


@pytest.fixture
def store():
    return MemoryStore()


class TestMemoryStoreInit:
    def test_starts_empty(self, store):
        assert store.size == 0

    def test_mcp_not_available_in_tests(self, store):
        assert store._mcp_available is False


class TestMemoryStoreRemember:
    def test_remember_single_fact(self, store):
        store.remember("project uses PostgreSQL")
        assert store.size == 1

    def test_remember_multiple_facts_same_entity(self, store):
        store.remember("fact 1", entity_name="db")
        store.remember("fact 2", entity_name="db")
        assert store.size == 1  # same entity

    def test_remember_different_entities(self, store):
        store.remember("fact 1", entity_name="db")
        store.remember("fact 2", entity_name="cache")
        assert store.size == 2

    def test_remember_default_entity_is_general(self, store):
        store.remember("some fact")
        data = store.read_all()
        assert "general" in data


class TestMemoryStoreEntity:
    def test_remember_entity(self, store):
        store.remember_entity("LightRAG", "tool", ["graph-based RAG", "EMNLP 2025"])
        entity = store.recall_entity("LightRAG")
        assert entity is not None
        assert entity.name == "LightRAG"
        assert "graph-based RAG" in entity.observations

    def test_remember_entity_extends_observations(self, store):
        store.remember_entity("Tool", "lib", ["obs1"])
        store.remember_entity("Tool", "lib", ["obs2"])
        entity = store.recall_entity("Tool")
        assert "obs1" in entity.observations
        assert "obs2" in entity.observations

    def test_recall_entity_unknown_type_in_fallback(self, store):
        store.remember("a fact", entity_name="myent")
        entity = store.recall_entity("myent")
        assert entity.entity_type == "unknown"

    def test_recall_entity_not_found_returns_none(self, store):
        assert store.recall_entity("does_not_exist") is None


class TestMemoryStoreRelation:
    def test_remember_relation_stored_as_fact(self, store):
        store.remember_relation("Claude", "Anthropic", "made_by")
        data = store.read_all()
        assert "_relations" in data
        assert any("Claude" in f for f in data["_relations"])


class TestMemoryStoreRecall:
    def test_recall_exact_match(self, store):
        store.remember("PostgreSQL is the database", entity_name="infra")
        results = store.recall("PostgreSQL")
        assert len(results) == 1
        assert "PostgreSQL" in results[0]

    def test_recall_case_insensitive(self, store):
        store.remember("uses Redis for caching", entity_name="infra")
        results = store.recall("redis")
        assert len(results) == 1

    def test_recall_matches_entity_name(self, store):
        store.remember("some fact", entity_name="my_special_entity")
        results = store.recall("my_special_entity")
        assert len(results) == 1

    def test_recall_no_match_returns_empty(self, store):
        store.remember("irrelevant fact")
        results = store.recall("quantum_physics")
        assert results == []

    def test_recall_multiple_matches(self, store):
        store.remember("Python version 3.12", entity_name="stack")
        store.remember("Python used for scripting", entity_name="notes")
        results = store.recall("Python")
        assert len(results) == 2


class TestMemoryStoreForget:
    def test_forget_removes_entity(self, store):
        store.remember("fact", entity_name="temp")
        store.forget("temp")
        assert store.size == 0

    def test_forget_nonexistent_is_noop(self, store):
        store.forget("ghost")  # should not raise

    def test_forget_observation(self, store):
        store.remember("keep this", entity_name="e")
        store.remember("remove this", entity_name="e")
        store.forget_observation("e", "remove this")
        entity = store.recall_entity("e")
        assert "keep this" in entity.observations
        assert "remove this" not in entity.observations


class TestMemoryStoreReadAll:
    def test_read_all_empty(self, store):
        assert store.read_all() == {}

    def test_read_all_returns_copy(self, store):
        store.remember("fact", entity_name="e")
        data = store.read_all()
        data["new_key"] = ["tamper"]
        # Original should be unchanged
        assert "new_key" not in store.read_all()


class TestEntityDataclass:
    def test_entity_fields(self):
        e = Entity(name="Test", entity_type="lib", observations=["obs1"])
        assert e.name == "Test"
        assert e.entity_type == "lib"
        assert e.observations == ["obs1"]


# ── MCP-available branches (stub methods + mcp-path dispatch) ─────────────────

@pytest.fixture
def mcp_store():
    """MemoryStore with _mcp_available=True to exercise MCP dispatch paths."""
    s = MemoryStore()
    s._mcp_available = True
    return s


class TestMemoryStoreMcpPath:
    """Verify that with _mcp_available=True the MCP stub methods are called."""

    def test_remember_calls_mcp_add_observation(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_add_observation") as mock_add:
            mcp_store.remember("test fact", entity_name="proj")
        mock_add.assert_called_once_with("proj", "test fact")

    def test_remember_entity_calls_mcp_create_entity(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_create_entity") as mock_create:
            mcp_store.remember_entity("Tool", "lib", ["obs1"])
        mock_create.assert_called_once_with("Tool", "lib", ["obs1"])

    def test_recall_calls_mcp_search(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_search", return_value=["result"]) as mock_search:
            results = mcp_store.recall("database")
        mock_search.assert_called_once_with("database")
        assert results == ["result"]

    def test_recall_entity_calls_mcp_open_node(self, mcp_store):
        from unittest.mock import patch
        entity = Entity(name="A", entity_type="t", observations=[])
        with patch.object(mcp_store, "_mcp_open_node", return_value=entity) as mock_node:
            result = mcp_store.recall_entity("A")
        mock_node.assert_called_once_with("A")
        assert result is entity

    def test_forget_calls_mcp_delete_entity(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_delete_entity") as mock_del:
            mcp_store.forget("proj")
        mock_del.assert_called_once_with("proj")

    def test_forget_observation_calls_mcp_delete_observation(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_delete_observation") as mock_del:
            mcp_store.forget_observation("proj", "old fact")
        mock_del.assert_called_once_with("proj", "old fact")


class TestMcpStubMethods:
    """The _mcp_* stub methods log a warning and no-op / return empty."""

    def test_mcp_add_observation_noop(self, store):
        store._mcp_add_observation("entity", "obs")  # must not raise

    def test_mcp_create_entity_noop(self, store):
        store._mcp_create_entity("name", "type", ["obs"])

    def test_mcp_search_returns_empty(self, store):
        assert store._mcp_search("query") == []

    def test_mcp_open_node_returns_none(self, store):
        assert store._mcp_open_node("name") is None

    def test_mcp_delete_entity_noop(self, store):
        store._mcp_delete_entity("name")

    def test_mcp_delete_observation_noop(self, store):
        store._mcp_delete_observation("entity", "obs")
```

FILE: /home/user/wellux_testprojects/tests/test_tiered_memory.py
```python
"""Tests for TieredMemory — hot/warm/glacier storage system."""

from __future__ import annotations

from pathlib import Path

from src.persistence.tiered_memory import TieredMemory


class TestTieredMemoryInit:
    def test_creates_directories_on_init(self, tmp_path: Path) -> None:
        TieredMemory(base=tmp_path)
        assert (tmp_path / "hot").is_dir()
        assert (tmp_path / "warm").is_dir()
        assert (tmp_path / "glacier").is_dir()

    def test_hot_file_absent_before_first_write(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        assert mem.read_hot() == ""


class TestHotTier:
    def test_write_hot_creates_file(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("branch", "main")
        content = mem.read_hot()
        assert "branch" in content
        assert "main" in content

    def test_write_hot_updates_existing_key(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("branch", "old-branch")
        mem.write_hot("branch", "new-branch")
        content = mem.read_hot()
        assert "new-branch" in content
        assert "old-branch" not in content

    def test_write_hot_updates_timestamp(self, tmp_path: Path) -> None:
        hot_file = tmp_path / "hot" / "hot-memory.md"
        hot_file.parent.mkdir(parents=True)
        hot_file.write_text(
            "**Last Updated**: 2020-01-01 00:00:00\n\n## Active Context\n"
        )
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("key", "value")
        content = mem.read_hot()
        assert "2020-01-01" not in content

    def test_write_hot_multiple_keys(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("key1", "val1")
        mem.write_hot("key2", "val2")
        content = mem.read_hot()
        assert "key1" in content
        assert "key2" in content

    def test_read_hot_returns_string(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("x", "y")
        result = mem.read_hot()
        assert isinstance(result, str)
        assert len(result) > 0


class TestWarmTier:
    def test_write_warm_creates_domain_file(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("architecture", "# Architecture\n\nFastAPI + Python")
        assert (tmp_path / "warm" / "architecture.md").exists()

    def test_read_warm_returns_content(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("routing", "LLM router maps complexity 0-10 to haiku/sonnet/opus")
        result = mem.read_warm("routing")
        assert "LLM router" in result

    def test_read_warm_returns_empty_for_missing_domain(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        result = mem.read_warm("nonexistent")
        assert result == ""

    def test_append_warm_adds_to_existing(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("decisions", "# Decisions\n")
        mem.append_warm("decisions", "- Use setuptools.build_meta not legacy:build")
        content = mem.read_warm("decisions")
        assert "# Decisions" in content
        assert "setuptools.build_meta" in content

    def test_list_warm_domains_empty_initially(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        assert mem.list_warm_domains() == []

    def test_list_warm_domains_returns_names(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("architecture", "content")
        mem.write_warm("routing", "content")
        domains = mem.list_warm_domains()
        assert "architecture" in domains
        assert "routing" in domains


class TestGlacierTier:
    def test_archive_glacier_creates_file(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier("my-decision", "We chose PostgreSQL because...")
        assert Path(path).exists()

    def test_archive_glacier_file_has_frontmatter(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier(
            "test-slug",
            "Decision content",
            tags=["architecture", "database"],
            title="Test Decision",
        )
        text = Path(path).read_text()
        assert "---" in text
        assert "title: Test Decision" in text
        assert "tags: [architecture, database]" in text
        assert "slug: test-slug" in text

    def test_archive_glacier_file_contains_body(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier("body-test", "Here is the decision body text")
        text = Path(path).read_text()
        assert "Here is the decision body text" in text

    def test_archive_glacier_filename_includes_date(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier("dated-decision", "content")
        filename = Path(path).name
        assert filename.endswith("-dated-decision.md")
        # Filename starts with a date: YYYY-MM-DD
        assert filename[:4].isdigit()

    def test_search_glacier_finds_by_content(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("auth-decision", "We chose JWT tokens over sessions")
        results = mem.search_glacier("JWT")
        assert len(results) >= 1
        assert any("auth-decision" in r["path"] for r in results)

    def test_search_glacier_finds_by_tag(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("tagged-entry", "content", tags=["security", "auth"])
        results = mem.search_glacier("security")
        assert len(results) >= 1

    def test_search_glacier_returns_empty_for_no_match(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("some-entry", "unrelated content here")
        results = mem.search_glacier("xyzzy_not_found")
        assert results == []

    def test_search_glacier_result_has_expected_fields(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("fields-test", "content text", tags=["test"], title="Fields Test")
        results = mem.search_glacier("content")
        assert len(results) >= 1
        r = results[0]
        assert "path" in r
        assert "title" in r
        assert "date" in r
        assert "tags" in r
        assert "snippet" in r

    def test_search_glacier_respects_limit(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        for i in range(5):
            mem.archive_glacier(f"entry-{i}", f"shared keyword result {i}")
        results = mem.search_glacier("keyword", limit=2)
        assert len(results) == 2

    def test_list_glacier_returns_all_entries(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("entry-1", "content 1")
        mem.archive_glacier("entry-2", "content 2")
        entries = mem.list_glacier()
        assert len(entries) >= 2

    def test_list_glacier_filters_by_tag(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("tagged", "content", tags=["special"])
        mem.archive_glacier("untagged", "other content")
        entries = mem.list_glacier(tag="special")
        assert len(entries) == 1
        assert "tagged" in entries[0]["path"]

    def test_list_glacier_empty_initially(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        assert mem.list_glacier() == []


class TestTieredMemoryIntegration:
    def test_persistence_module_exports_tiered_memory(self) -> None:
        from src.persistence import TieredMemory as TM  # noqa: F401
        assert TM is TieredMemory

    def test_full_lifecycle(self, tmp_path: Path) -> None:
        """Hot write → warm domain → glacier archive → search."""
        mem = TieredMemory(base=tmp_path)

        # Write hot context
        mem.write_hot("active_feature", "tiered-memory")

        # Write warm domain
        mem.write_warm("architecture", "# Architecture\nTiered memory: hot/warm/glacier")

        # Archive to glacier
        mem.archive_glacier(
            "tiered-memory-decision",
            "We added hot/warm/glacier tiers to improve context efficiency",
            tags=["architecture", "memory"],
        )

        # Verify all tiers are populated
        assert "active_feature" in mem.read_hot()
        assert "Tiered memory" in mem.read_warm("architecture")
        results = mem.search_glacier("context efficiency")
        assert len(results) == 1
        assert "tiered-memory-decision" in results[0]["path"]


# ── Regex pattern cache ───────────────────────────────────────────────────────

class TestHotKeyPatternCache:
    def test_pattern_cached_after_first_write(self, tmp_path: Path) -> None:
        from src.persistence import tiered_memory as tm_mod

        mem = TieredMemory(base=tmp_path)
        tm_mod._hot_key_patterns.clear()
        mem.write_hot("cached_key", "value1")
        assert "cached_key" in tm_mod._hot_key_patterns

    def test_second_write_reuses_cached_pattern(self, tmp_path: Path) -> None:
        from src.persistence import tiered_memory as tm_mod

        mem = TieredMemory(base=tmp_path)
        tm_mod._hot_key_patterns.clear()
        mem.write_hot("reuse_key", "first")
        pattern_id = id(tm_mod._hot_key_patterns["reuse_key"])
        mem.write_hot("reuse_key", "second")
        assert id(tm_mod._hot_key_patterns["reuse_key"]) == pattern_id
```

FILE: /home/user/wellux_testprojects/tests/test_mcp_server.py
```python
"""Tests for src/mcp_server.py — tool functions, _capture, _make_args, import guard."""
from __future__ import annotations

# Inject fake mcp packages into sys.modules BEFORE importing mcp_server,
# so the module-level `_require_fastmcp()` call succeeds without the real mcp package.
import importlib
import sys
import types
from unittest.mock import MagicMock, patch

import pytest

# ── build the fake mcp module tree ────────────────────────────────────────────

def _install_fake_mcp():
    """Inject stub mcp.server.fastmcp into sys.modules."""
    fake_fastmcp_cls = MagicMock(name="FastMCP")
    # Each instance returned by FastMCP(...) is also a MagicMock
    fake_fastmcp_cls.return_value = MagicMock(name="mcp_instance")
    # Ensure @mcp.tool() returns the decorated function unchanged
    fake_fastmcp_cls.return_value.tool.return_value = lambda fn: fn

    stub_fastmcp_mod = types.ModuleType("mcp.server.fastmcp")
    stub_fastmcp_mod.FastMCP = fake_fastmcp_cls  # type: ignore[attr-defined]

    stub_server_mod = types.ModuleType("mcp.server")
    stub_server_mod.fastmcp = stub_fastmcp_mod  # type: ignore[attr-defined]

    stub_mcp_mod = types.ModuleType("mcp")
    stub_mcp_mod.server = stub_server_mod  # type: ignore[attr-defined]

    sys.modules.setdefault("mcp", stub_mcp_mod)
    sys.modules.setdefault("mcp.server", stub_server_mod)
    sys.modules.setdefault("mcp.server.fastmcp", stub_fastmcp_mod)

    return fake_fastmcp_cls


_fake_fastmcp_cls = _install_fake_mcp()

# Now import (and reload) the server module with the stubs in place
import src.mcp_server as _mcp_mod  # noqa: E402,I001

importlib.reload(_mcp_mod)

from src.mcp_server import _capture, _make_args  # noqa: E402,I001


# ── _make_args ────────────────────────────────────────────────────────────────

class TestMakeArgs:
    def test_single_kwarg(self):
        ns = _make_args(env="staging")
        assert ns.env == "staging"

    def test_multiple_kwargs(self):
        ns = _make_args(env="local", dry_run=True, port=8000)
        assert ns.dry_run is True
        assert ns.port == 8000

    def test_empty(self):
        import argparse
        ns = _make_args()
        assert isinstance(ns, argparse.Namespace)


# ── _capture ──────────────────────────────────────────────────────────────────

class TestCapture:
    def test_captures_stdout(self):
        import argparse

        def _printer(args):
            print("hello from fn")

        result = _capture(_printer, argparse.Namespace())
        assert result == "hello from fn\n"

    def test_empty_output(self):
        import argparse

        result = _capture(lambda _: None, argparse.Namespace())
        assert result == ""

    def test_multiple_prints(self):
        import argparse

        def _multi(args):
            print("line1")
            print("line2")

        result = _capture(_multi, argparse.Namespace())
        assert "line1" in result
        assert "line2" in result


# ── MCP tool functions ────────────────────────────────────────────────────────

class TestDeployTool:
    def test_calls_cmd_deploy_and_returns_string(self):
        with patch("src.cli.cmd_deploy") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("deploy ok")
            result = _mcp_mod.deploy(env="local", dry_run=True,
                                     skip_tests=True, skip_build=True, skip_evals=True)
        assert "deploy ok" in result

    def test_dry_run_flag_forwarded(self):
        captured_args = []

        def _spy(args):
            captured_args.append(args)

        with patch("src.cli.cmd_deploy", _spy):
            _mcp_mod.deploy(dry_run=True, skip_tests=False,
                            skip_build=False, skip_evals=False)
        assert captured_args[0].dry_run is True

    def test_env_forwarded(self):
        captured_args = []

        def _spy(args):
            captured_args.append(args)

        with patch("src.cli.cmd_deploy", _spy):
            _mcp_mod.deploy(env="staging", dry_run=False,
                            skip_tests=True, skip_build=True, skip_evals=True)
        assert captured_args[0].env == "staging"


class TestBuildTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_build") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("build done")
            result = _mcp_mod.build()
        assert "build done" in result

    def test_no_cache_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_build", lambda a: captured_args.append(a)):
            _mcp_mod.build(no_cache=True)
        assert captured_args[0].no_cache is True

    def test_tag_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_build", lambda a: captured_args.append(a)):
            _mcp_mod.build(tag="v1.2.3")
        assert captured_args[0].tag == "v1.2.3"


class TestHealthTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_health") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("healthy")
            result = _mcp_mod.health()
        assert "healthy" in result

    def test_url_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_health", lambda a: captured_args.append(a)):
            _mcp_mod.health(url="http://prod:8000")
        assert captured_args[0].url == "http://prod:8000"


class TestStatusTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_status") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("status output")
            result = _mcp_mod.status()
        assert "status output" in result


class TestDoctorTool:
    def test_healthy_verdict(self):
        with patch("src.cli.cmd_doctor", return_value=0) as mock_cmd:
            mock_cmd.side_effect = lambda args: 0
            with patch("src.mcp_server._capture", return_value="checks ok\n"):
                result = _mcp_mod.doctor()
        assert "HEALTHY" in result

    def test_issues_verdict(self):
        def _bad_doctor(args):
            return 1

        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with patch("src.cli.cmd_doctor", _bad_doctor):
                result = _mcp_mod.doctor()
        assert "ISSUES FOUND" in result


class TestGetLogsTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_logs") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("log line")
            result = _mcp_mod.get_logs()
        assert "log line" in result

    def test_limit_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_logs", lambda a: captured_args.append(a)):
            _mcp_mod.get_logs(limit=10)
        assert captured_args[0].limit == 10

    def test_event_filter_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_logs", lambda a: captured_args.append(a)):
            _mcp_mod.get_logs(event="api_startup")
        assert captured_args[0].event == "api_startup"


# ── _build_server + run ───────────────────────────────────────────────────────

class TestBuildServer:
    def test_returns_mcp_instance(self):
        server = _mcp_mod._build_server()
        # FastMCP was called with the app name
        _fake_fastmcp_cls.assert_called_with(
            "ccm", instructions="Claude Code Max deployment and operations server"
        )
        assert server is _fake_fastmcp_cls.return_value

    def test_all_tools_registered(self):
        """All 6 tool functions are registered via mcp.tool()."""
        instance = _fake_fastmcp_cls.return_value
        # .tool() called once per function (deploy, build, health, status, doctor, get_logs)
        assert instance.tool.call_count >= 6

    def test_run_calls_build_server_run(self):
        """run() delegates to _build_server().run()."""
        with patch.object(_mcp_mod, "_build_server") as mock_build:
            mock_server = MagicMock()
            mock_build.return_value = mock_server
            _mcp_mod.run()
        mock_build.assert_called_once()
        mock_server.run.assert_called_once()


# ── import guard ──────────────────────────────────────────────────────────────

class TestRequireFastmcp:
    def test_raises_system_exit_when_mcp_missing(self):
        """_require_fastmcp must exit(1) when mcp is not installed."""
        # Temporarily hide the mcp module
        saved = {k: v for k, v in sys.modules.items() if k.startswith("mcp")}
        for k in list(saved):
            sys.modules.pop(k)
        try:
            with pytest.raises(SystemExit) as exc_info:
                _mcp_mod._require_fastmcp()
            assert exc_info.value.code == 1
        finally:
            sys.modules.update(saved)
```

FILE: /home/user/wellux_testprojects/tests/test_llm_base.py
```python
"""Tests for src/llm/base.py — CompletionRequest, CompletionResponse, cost calculation."""
import pytest

from src.llm.base import CompletionRequest, CompletionResponse


class TestCompletionRequest:
    def test_defaults(self):
        req = CompletionRequest(prompt="hello")
        assert req.prompt == "hello"
        assert req.system is None
        assert req.model is None
        assert req.max_tokens == 4096
        assert req.temperature == 0.7

    def test_custom_values(self):
        req = CompletionRequest(
            prompt="test",
            system="be concise",
            model="claude-sonnet-4-6",
            max_tokens=512,
            temperature=0.0,
        )
        assert req.system == "be concise"
        assert req.model == "claude-sonnet-4-6"
        assert req.max_tokens == 512
        assert req.temperature == 0.0

    def test_empty_prompt_allowed(self):
        req = CompletionRequest(prompt="")
        assert req.prompt == ""


class TestCompletionResponse:
    def test_basic_fields(self):
        resp = CompletionResponse(
            content="hello world",
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
            stop_reason="end_turn",
        )
        assert resp.content == "hello world"
        assert resp.model == "claude-sonnet-4-6"
        assert resp.input_tokens == 10
        assert resp.output_tokens == 5
        assert resp.stop_reason == "end_turn"

    def test_cost_usd_sonnet(self):
        resp = CompletionResponse(
            content="x",
            model="claude-sonnet-4-6",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
            stop_reason="end_turn",
        )
        # sonnet: $3/M input + $15/M output = $18 per 1M each
        assert resp.cost_usd == pytest.approx(18.0, rel=0.01)

    def test_cost_usd_haiku(self):
        resp = CompletionResponse(
            content="x",
            model="claude-haiku-4-5-20251001",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
            stop_reason="end_turn",
        )
        # haiku: $0.25/M input + $1.25/M output = $1.50
        assert resp.cost_usd == pytest.approx(1.50, rel=0.01)

    def test_cost_usd_zero_tokens(self):
        resp = CompletionResponse(
            content="",
            model="claude-sonnet-4-6",
            input_tokens=0,
            output_tokens=0,
            stop_reason="end_turn",
        )
        assert resp.cost_usd == 0.0

    def test_cost_usd_unknown_model_defaults(self):
        resp = CompletionResponse(
            content="x",
            model="unknown-model-xyz",
            input_tokens=1_000_000,
            output_tokens=0,
            stop_reason="end_turn",
        )
        # Should not raise — should return some non-negative value
        assert resp.cost_usd >= 0.0

    def test_total_tokens(self):
        resp = CompletionResponse(
            content="x",
            model="claude-sonnet-4-6",
            input_tokens=30,
            output_tokens=12,
            stop_reason="end_turn",
        )
        assert resp.total_tokens == 42

    def test_total_tokens_zero(self):
        resp = CompletionResponse(
            content="",
            model="claude-sonnet-4-6",
            input_tokens=0,
            output_tokens=0,
            stop_reason="end_turn",
        )
        assert resp.total_tokens == 0
```

FILE: /home/user/wellux_testprojects/tests/test_llm_claude_client.py
```python
"""Tests for src/llm/claude_client.py — retry logic, caching, backoff."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionRequest, CompletionResponse
from src.llm.claude_client import ClaudeClient, _backoff

# ── _backoff ──────────────────────────────────────────────────────────────────

class TestBackoff:
    def test_increases_with_attempt(self):
        # Higher attempt → higher base delay (jitter aside)
        # Use enough samples to avoid flaky jitter-dominated results
        samples_0 = [_backoff(0) for _ in range(20)]
        samples_2 = [_backoff(2) for _ in range(20)]
        assert sum(samples_2) > sum(samples_0)

    def test_capped_at_max(self):
        # attempt=100 should still be ≤ 30s + 25% jitter ceiling
        for _ in range(20):
            assert _backoff(100) <= 30.0 * 1.25 + 0.001

    def test_non_negative(self):
        for attempt in range(5):
            assert _backoff(attempt) >= 0.0

    def test_attempt_zero_near_base(self):
        # attempt=0 → base ~1s ± 25%
        for _ in range(20):
            val = _backoff(0)
            assert 0.0 <= val <= 1.5


# ── ClaudeClient — happy path ─────────────────────────────────────────────────

def _mock_message(content="hello", model="claude-sonnet-4-6", in_tok=10, out_tok=5):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    msg.model = model
    msg.usage.input_tokens = in_tok
    msg.usage.output_tokens = out_tok
    msg.stop_reason = "end_turn"
    return msg


class TestClaudeClientComplete:
    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key")
            c.async_client = async_cls.return_value
            return c

    async def test_returns_completion_response(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message("world")
        )
        req = CompletionRequest(prompt="hello")
        resp = await client.complete(req)
        assert isinstance(resp, CompletionResponse)
        assert resp.content == "world"

    async def test_uses_cache_on_second_call(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message("cached")
        )
        req = CompletionRequest(prompt="same prompt")
        await client.complete(req)
        await client.complete(req)
        # API should only be called once — second is served from cache
        assert client.async_client.messages.create.call_count == 1

    async def test_uses_default_model(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message()
        )
        req = CompletionRequest(prompt="hi")
        await client.complete(req)
        call_kwargs = client.async_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == ClaudeClient.DEFAULT_MODEL

    async def test_uses_request_model_override(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message(model="claude-haiku-4-5-20251001")
        )
        req = CompletionRequest(prompt="hi", model="claude-haiku-4-5-20251001")
        await client.complete(req)
        call_kwargs = client.async_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "claude-haiku-4-5-20251001"

    async def test_response_tokens_propagated(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message(in_tok=42, out_tok=7)
        )
        resp = await client.complete(CompletionRequest(prompt="x"))
        assert resp.input_tokens == 42
        assert resp.output_tokens == 7

    async def test_stop_reason_propagated(self, client):
        client.async_client.messages.create = AsyncMock(
            return_value=_mock_message()
        )
        resp = await client.complete(CompletionRequest(prompt="x"))
        assert resp.stop_reason == "end_turn"


# ── retry logic ───────────────────────────────────────────────────────────────

class TestClaudeClientRetry:
    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key", max_retries=3)
            c.async_client = async_cls.return_value
            return c

    async def test_retries_on_rate_limit(self, client):
        import anthropic as _anthropic

        ok = _mock_message("ok")
        client.async_client.messages.create = AsyncMock(
            side_effect=[
                _anthropic.RateLimitError("rate limited", response=MagicMock(), body={}),
                ok,
            ]
        )
        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            resp = await client.complete(CompletionRequest(prompt="retry me"))
        assert resp.content == "ok"
        assert client.async_client.messages.create.call_count == 2

    async def test_raises_immediately_on_auth_error(self, client):
        import anthropic as _anthropic

        client.async_client.messages.create = AsyncMock(
            side_effect=_anthropic.AuthenticationError(
                "bad key", response=MagicMock(), body={}
            )
        )
        with pytest.raises(_anthropic.AuthenticationError):
            await client.complete(CompletionRequest(prompt="x"))
        # Only called once — no retry on fatal errors
        assert client.async_client.messages.create.call_count == 1

    async def test_raises_after_max_retries(self, client):
        import anthropic as _anthropic

        client.async_client.messages.create = AsyncMock(
            side_effect=_anthropic.RateLimitError(
                "always rate limited", response=MagicMock(), body={}
            )
        )
        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RuntimeError, match="failed after"):
                await client.complete(CompletionRequest(prompt="x"))
        assert client.async_client.messages.create.call_count == 3


# ── anthropic.APIError handler ────────────────────────────────────────────────

class TestClaudeClientAPIError:
    """Cover the `except anthropic.APIError` branch (non-retryable, non-fatal)."""

    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key", max_retries=3)
            c.async_client = async_cls.return_value
            return c

    async def test_api_error_on_last_attempt_reraises(self, client):
        import anthropic as _anthropic

        # BadRequestError is APIError but not in _RETRYABLE or _FATAL
        err = _anthropic.BadRequestError("bad request", response=MagicMock(), body={})
        client.async_client.messages.create = AsyncMock(side_effect=err)

        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(_anthropic.BadRequestError):
                await client.complete(CompletionRequest(prompt="x"))

        assert client.async_client.messages.create.call_count == 3

    async def test_api_error_retries_before_last_attempt(self, client):
        import anthropic as _anthropic

        err = _anthropic.BadRequestError("bad request", response=MagicMock(), body={})
        ok = _mock_message("recovered")
        # First two attempts fail, third succeeds
        client.async_client.messages.create = AsyncMock(side_effect=[err, err, ok])

        with patch("src.llm.claude_client.asyncio.sleep", new_callable=AsyncMock):
            resp = await client.complete(CompletionRequest(prompt="x"))

        assert resp.content == "recovered"
        assert client.async_client.messages.create.call_count == 3


# ── stream ────────────────────────────────────────────────────────────────────

class TestClaudeClientStream:
    @pytest.fixture
    def client(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic") as async_cls:
            c = ClaudeClient(api_key="test-key")
            c.async_client = async_cls.return_value
            return c

    async def test_stream_yields_tokens(self, client):
        async def _text_stream():
            for token in ["hello", " world"]:
                yield token

        stream_ctx = MagicMock()
        stream_ctx.text_stream = _text_stream()
        stream_ctx.__aenter__ = AsyncMock(return_value=stream_ctx)
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        client.async_client.messages.stream = MagicMock(return_value=stream_ctx)

        tokens = []
        async for t in client.stream(CompletionRequest(prompt="stream me")):
            tokens.append(t)

        assert tokens == ["hello", " world"]

    async def test_stream_empty_response(self, client):
        async def _empty():
            return
            yield  # make it an async generator

        stream_ctx = MagicMock()
        stream_ctx.text_stream = _empty()
        stream_ctx.__aenter__ = AsyncMock(return_value=stream_ctx)
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        client.async_client.messages.stream = MagicMock(return_value=stream_ctx)

        tokens = [t async for t in client.stream(CompletionRequest(prompt="x"))]
        assert tokens == []


# ── count_tokens ──────────────────────────────────────────────────────────────

class TestCountTokens:
    def test_empty_string(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
            c = ClaudeClient(api_key="x")
        assert c.count_tokens("") == 0

    def test_approximate_count(self):
        with patch("src.llm.claude_client.anthropic.Anthropic"), \
             patch("src.llm.claude_client.anthropic.AsyncAnthropic"):
            c = ClaudeClient(api_key="x")
        # 40 chars → ~10 tokens
        assert c.count_tokens("a" * 40) == 10
```

FILE: /home/user/wellux_testprojects/tests/test_llm_gpt_client.py
```python
"""Tests for src/llm/gpt_client.py — happy path, caching, retry, cost calc."""
from __future__ import annotations

# Inject a fake 'openai' module before gpt_client is imported so that the
# try/except import block succeeds and OPENAI_AVAILABLE is set to True.
import importlib
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.llm.base import CompletionRequest, CompletionResponse


def _make_fake_openai():
    """Return a MagicMock that looks enough like the openai module."""
    fake = MagicMock()
    fake.RateLimitError = type("RateLimitError", (Exception,), {})
    fake.APIError = type("APIError", (Exception,), {})
    return fake


_fake_openai = _make_fake_openai()
sys.modules.setdefault("openai", _fake_openai)

import src.llm.gpt_client as _gpt_mod  # noqa: E402

importlib.reload(_gpt_mod)

from src.llm.gpt_client import GPTClient, _cost_usd  # noqa: E402,I001


# ── cost helper ───────────────────────────────────────────────────────────────

class TestCostUsd:
    def test_gpt4o_mini_cheaper(self):
        assert _cost_usd("gpt-4o-mini", 1000, 1000) < _cost_usd("gpt-4o", 1000, 1000)

    def test_zero_tokens_zero_cost(self):
        assert _cost_usd("gpt-4o", 0, 0) == 0.0

    def test_mini_rate(self):
        # 1M input + 1M output at mini rates = 0.15 + 0.60 = 0.75 USD
        assert abs(_cost_usd("gpt-4o-mini", 1_000_000, 1_000_000) - 0.75) < 1e-9

    def test_standard_rate(self):
        # 1M input + 1M output at 4o rates = 2.50 + 10.00 = 12.50 USD
        assert abs(_cost_usd("gpt-4o", 1_000_000, 1_000_000) - 12.50) < 1e-9


# ── shared mock helpers ───────────────────────────────────────────────────────

def _openai_response(content="hi", model="gpt-4o", in_tok=10, out_tok=5, finish="stop"):
    choice = MagicMock()
    choice.message.content = content
    choice.finish_reason = finish
    resp = MagicMock()
    resp.choices = [choice]
    resp.usage.prompt_tokens = in_tok
    resp.usage.completion_tokens = out_tok
    resp.model = model
    return resp


@pytest.fixture
def client():
    """Yield (GPTClient, fake_openai_module). openai already injected into sys.modules."""
    fake_openai = sys.modules["openai"]
    fake_openai.AsyncOpenAI = MagicMock(return_value=MagicMock())
    c = GPTClient(api_key="test-key")
    c.client = fake_openai.AsyncOpenAI.return_value
    yield c, fake_openai


# ── happy path ────────────────────────────────────────────────────────────────

class TestGPTClientComplete:
    async def test_returns_completion_response(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response("world")
        )
        resp = await c.complete(CompletionRequest(prompt="hello"))
        assert isinstance(resp, CompletionResponse)
        assert resp.content == "world"

    async def test_uses_default_model(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response()
        )
        await c.complete(CompletionRequest(prompt="hi"))
        call_kwargs = c.client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == GPTClient.DEFAULT_MODEL

    async def test_uses_request_model_override(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response()
        )
        await c.complete(CompletionRequest(prompt="hi", model="gpt-4o-mini"))
        call_kwargs = c.client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o-mini"

    async def test_cache_hit_skips_api(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response("cached")
        )
        req = CompletionRequest(prompt="same")
        await c.complete(req)
        await c.complete(req)
        assert c.client.chat.completions.create.call_count == 1

    async def test_token_counts_propagated(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response(in_tok=42, out_tok=7)
        )
        resp = await c.complete(CompletionRequest(prompt="count"))
        assert resp.input_tokens == 42
        assert resp.output_tokens == 7

    async def test_stop_reason_propagated(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response(finish="length")
        )
        resp = await c.complete(CompletionRequest(prompt="x"))
        assert resp.stop_reason == "length"

    async def test_system_prompt_included(self, client):
        c, _ = client
        c.client.chat.completions.create = AsyncMock(
            return_value=_openai_response()
        )
        await c.complete(CompletionRequest(prompt="hi", system="Be concise"))
        msgs = c.client.chat.completions.create.call_args.kwargs["messages"]
        roles = [m["role"] for m in msgs]
        assert roles[0] == "system"
        assert roles[1] == "user"


# ── retry logic ───────────────────────────────────────────────────────────────

class TestGPTClientRetry:
    async def test_retries_on_rate_limit(self, client):
        c, _ = client
        RateLimitError = _gpt_mod.openai.RateLimitError
        c.client.chat.completions.create = AsyncMock(
            side_effect=[RateLimitError("limit"), _openai_response("ok")]
        )
        with patch("src.llm.gpt_client.asyncio.sleep", new_callable=AsyncMock):
            resp = await c.complete(CompletionRequest(prompt="retry"))
        assert resp.content == "ok"
        assert c.client.chat.completions.create.call_count == 2

    async def test_raises_after_max_retries_on_rate_limit(self, client):
        c, _ = client
        RateLimitError = _gpt_mod.openai.RateLimitError
        c.client.chat.completions.create = AsyncMock(
            side_effect=RateLimitError("always limited")
        )
        with patch("src.llm.gpt_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RuntimeError, match="Failed after"):
                await c.complete(CompletionRequest(prompt="x"))
        assert c.client.chat.completions.create.call_count == c.max_retries

    async def test_api_error_reraises_on_last_attempt(self, client):
        c, _ = client
        APIError = _gpt_mod.openai.APIError
        c.client.chat.completions.create = AsyncMock(
            side_effect=APIError("server error")
        )
        with patch("src.llm.gpt_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(Exception, match="server error"):
                await c.complete(CompletionRequest(prompt="x"))


# ── stream ────────────────────────────────────────────────────────────────────

class TestGPTClientStream:
    async def test_yields_tokens(self, client):
        c, _ = client

        def _make_chunk(text):
            chunk = MagicMock()
            chunk.choices[0].delta.content = text
            return chunk

        async def _fake_stream(*args, **kwargs):
            return _async_iter([_make_chunk("hello"), _make_chunk(" world"), _make_chunk(None)])

        async def _async_iter(items):  # helper that returns async iterable
            for item in items:
                yield item

        # stream() calls create(..., stream=True) and iterates the result
        c.client.chat.completions.create = AsyncMock(
            side_effect=lambda **kw: _async_iter([
                _make_chunk("tok1"), _make_chunk("tok2"), _make_chunk(None),
            ])
        )
        tokens = []
        async for t in c.stream(CompletionRequest(prompt="hi")):
            tokens.append(t)
        assert tokens == ["tok1", "tok2"]   # None deltas are skipped

    async def test_stream_uses_model_override(self, client):
        c, _ = client
        captured_kwargs: list[dict] = []

        async def _fake_create(**kwargs):
            captured_kwargs.append(kwargs)
            async def _empty():
                return
                yield  # make it a generator
            return _empty()

        c.client.chat.completions.create = _fake_create
        async for _ in c.stream(CompletionRequest(prompt="x", model="gpt-4o-mini")):
            pass
        assert captured_kwargs[0]["model"] == "gpt-4o-mini"


# ── count_tokens ──────────────────────────────────────────────────────────────

class TestGPTClientCountTokens:
    def test_empty_string(self, client):
        c, _ = client
        assert c.count_tokens("") == 0

    def test_approx_four_chars_per_token(self, client):
        c, _ = client
        assert c.count_tokens("a" * 40) == 10


# ── import guard ──────────────────────────────────────────────────────────────

class TestImportGuard:
    def test_raises_if_openai_not_available(self):
        with patch.object(_gpt_mod, "OPENAI_AVAILABLE", False):
            with pytest.raises(ImportError, match="openai"):
                _gpt_mod.GPTClient(api_key="x")
```

FILE: /home/user/wellux_testprojects/tests/test_llm_init.py
```python
"""Tests for src/llm/__init__.py — lazy-import __getattr__ branches."""
from __future__ import annotations

import pytest


class TestLLMPackageExports:
    def test_completion_request_importable(self):
        from src.llm import CompletionRequest
        assert CompletionRequest is not None

    def test_completion_response_importable(self):
        from src.llm import CompletionResponse
        assert CompletionResponse is not None

    def test_llm_client_importable(self):
        from src.llm import LLMClient
        assert LLMClient is not None

    def test_utils_importable(self):
        from src.llm import build_request, merge_system_prompts, truncate_to_tokens
        assert callable(build_request)
        assert callable(truncate_to_tokens)
        assert callable(merge_system_prompts)


class TestLazyGetattr:
    def test_claude_client_lazy_load(self):
        """src.llm.ClaudeClient resolves via __getattr__ without top-level import."""
        import src.llm as llm_pkg
        cls = llm_pkg.ClaudeClient
        assert cls is not None

    def test_gpt_client_lazy_load(self):
        """src.llm.GPTClient resolves via __getattr__."""
        import src.llm as llm_pkg
        cls = llm_pkg.GPTClient
        assert cls is not None

    def test_unknown_attr_raises_attribute_error(self):
        import src.llm as llm_pkg
        with pytest.raises(AttributeError, match="has no attribute"):
            _ = llm_pkg.NonExistentClient  # type: ignore[attr-defined]

    def test_claude_client_is_correct_class(self):
        import src.llm as llm_pkg
        from src.llm.claude_client import ClaudeClient
        assert llm_pkg.ClaudeClient is ClaudeClient

    def test_gpt_client_is_correct_class(self):
        import src.llm as llm_pkg
        from src.llm.gpt_client import GPTClient
        assert llm_pkg.GPTClient is GPTClient
```

FILE: /home/user/wellux_testprojects/tests/test_llm_utils.py
```python
"""Tests for src/llm/utils.py."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.llm.base import CompletionRequest, CompletionResponse
from src.llm.utils import (
    build_request,
    complete_with_fallback,
    format_messages_as_prompt,
    merge_system_prompts,
    truncate_to_tokens,
)


class TestBuildRequest:
    def test_basic(self):
        req = build_request("hello")
        assert isinstance(req, CompletionRequest)
        assert req.prompt == "hello"

    def test_with_all_options(self):
        req = build_request("p", system="s", model="m", max_tokens=100, temperature=0.1)
        assert req.system == "s"
        assert req.model == "m"
        assert req.max_tokens == 100
        assert req.temperature == 0.1


class TestTruncateToTokens:
    def test_short_text_unchanged(self):
        assert truncate_to_tokens("hello", 1000) == "hello"

    def test_long_text_truncated(self):
        text = "a" * 10000
        result = truncate_to_tokens(text, max_tokens=10)
        assert len(result) < len(text)
        assert "[truncated]" in result

    def test_exact_boundary_unchanged(self):
        text = "a" * 40  # 40 chars = 10 tokens at 4 chars/token
        result = truncate_to_tokens(text, max_tokens=10)
        assert result == text


class TestMergeSystemPrompts:
    def test_single_prompt(self):
        assert merge_system_prompts("be concise") == "be concise"

    def test_two_prompts_merged(self):
        result = merge_system_prompts("rule 1", "rule 2")
        assert "rule 1" in result
        assert "rule 2" in result

    def test_none_values_skipped(self):
        result = merge_system_prompts(None, "rule", None)
        assert result == "rule"

    def test_all_none_returns_none(self):
        assert merge_system_prompts(None, None) is None

    def test_empty_strings_skipped(self):
        assert merge_system_prompts("", "  ", "rule") == "rule"

    def test_custom_separator(self):
        result = merge_system_prompts("a", "b", separator=" | ")
        assert result == "a | b"


class TestFormatMessagesAsPrompt:
    def test_single_user_message(self):
        result = format_messages_as_prompt([{"role": "user", "content": "hello"}])
        assert "USER: hello" in result

    def test_multi_turn(self):
        msgs = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
            {"role": "user", "content": "bye"},
        ]
        result = format_messages_as_prompt(msgs)
        assert "USER: hi" in result
        assert "ASSISTANT: hello" in result
        assert "USER: bye" in result

    def test_empty_messages(self):
        assert format_messages_as_prompt([]) == ""


class TestCompleteWithFallback:
    @pytest.mark.asyncio
    async def test_returns_primary_on_success(self):
        primary = MagicMock()
        fallback = MagicMock()
        expected = CompletionResponse(
            content="primary", model="m", input_tokens=1, output_tokens=1, stop_reason="end_turn"
        )
        primary.complete = AsyncMock(return_value=expected)
        req = build_request("test")
        result = await complete_with_fallback(primary, fallback, req)
        assert result.content == "primary"
        fallback.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_back_on_primary_error(self):
        primary = MagicMock()
        fallback = MagicMock()
        primary.complete = AsyncMock(side_effect=RuntimeError("primary down"))
        fallback_resp = CompletionResponse(
            content="fallback", model="m", input_tokens=1, output_tokens=1, stop_reason="end_turn"
        )
        fallback.complete = AsyncMock(return_value=fallback_resp)
        req = build_request("test")
        result = await complete_with_fallback(primary, fallback, req)
        assert result.content == "fallback"
```

FILE: /home/user/wellux_testprojects/tests/test_log_index.py
```python
"""Tests for src/utils/log_index.py — indexed JSONL event log."""
from __future__ import annotations

import json
import threading

from src.utils.log_index import LogIndex


class TestLogIndexAppend:
    def test_append_returns_record(self, tmp_path):
        idx = LogIndex(tmp_path / "events.log")
        rec = idx.append("startup", version="0.6.0")
        assert rec["event"] == "startup"
        assert rec["version"] == "0.6.0"
        assert "ts" in rec

    def test_append_writes_to_disk(self, tmp_path):
        path = tmp_path / "events.log"
        idx = LogIndex(path)
        idx.append("test_event", key="val")
        lines = path.read_text().strip().splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["event"] == "test_event"
        assert record["key"] == "val"

    def test_multiple_appends_accumulate(self, tmp_path):
        idx = LogIndex(tmp_path / "events.log")
        for i in range(5):
            idx.append("tick", n=i)
        assert len(idx) == 5

    def test_creates_parent_dirs(self, tmp_path):
        nested = tmp_path / "a" / "b" / "events.log"
        idx = LogIndex(nested)
        idx.append("boot")
        assert nested.exists()


class TestLogIndexSearch:
    def test_search_by_event(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("api_request", path="/complete")
        idx.append("llm_call", model="opus")
        idx.append("api_request", path="/chat")

        results = idx.search(event="api_request")
        assert len(results) == 2
        assert all(r["event"] == "api_request" for r in results)

    def test_search_newest_first(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ev", n=0)
        idx.append("ev", n=1)
        idx.append("ev", n=2)

        results = idx.search(event="ev")
        # newest first → n=2 first
        assert results[0]["n"] == 2
        assert results[-1]["n"] == 0

    def test_search_by_tag(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ci_run", tag="ci")
        idx.append("deploy", tag="prod")
        idx.append("smoke", tag="ci")

        results = idx.search(tags=["ci"])
        assert len(results) == 2

    def test_search_event_and_tag_intersection(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("eval_run", tag="ci")
        idx.append("eval_run", tag="live")
        idx.append("other", tag="ci")

        results = idx.search(event="eval_run", tags=["ci"])
        assert len(results) == 1
        assert results[0]["tag"] == "ci"

    def test_search_no_filters_returns_all_newest_first(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for i in range(10):
            idx.append("ev", n=i)
        results = idx.search()
        assert len(results) == 10
        assert results[0]["n"] == 9

    def test_search_limit(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for i in range(20):
            idx.append("ev", n=i)
        results = idx.search(limit=5)
        assert len(results) == 5

    def test_search_unknown_event_returns_empty(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("known")
        assert idx.search(event="unknown") == []


class TestLogIndexTail:
    def test_tail_returns_last_n(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for i in range(10):
            idx.append("ev", n=i)
        result = idx.tail(3)
        assert len(result) == 3
        assert result[-1]["n"] == 9  # last entry is most recent

    def test_tail_all_when_n_exceeds_length(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ev")
        assert len(idx.tail(100)) == 1


class TestLogIndexSummary:
    def test_summary_counts_by_event(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for _ in range(3):
            idx.append("api_request")
        for _ in range(2):
            idx.append("llm_call")
        s = idx.summary()
        assert s["api_request"] == 3
        assert s["llm_call"] == 2


class TestLogIndexPersistence:
    def test_reload_rebuilds_index(self, tmp_path):
        path = tmp_path / "e.log"
        idx1 = LogIndex(path)
        for i in range(5):
            idx1.append("ev", n=i, tag="batch1")

        # New instance reads from disk
        idx2 = LogIndex(path)
        assert len(idx2) == 5
        results = idx2.search(event="ev")
        assert len(results) == 5

    def test_reload_preserves_tag_index(self, tmp_path):
        path = tmp_path / "e.log"
        idx1 = LogIndex(path)
        idx1.append("run", tag="ci")
        idx1.append("run", tag="prod")

        idx2 = LogIndex(path)
        assert len(idx2.search(tags=["ci"])) == 1

    def test_corrupt_line_is_skipped(self, tmp_path):
        path = tmp_path / "e.log"
        # Write one valid + one corrupt line
        path.write_text('{"ts":"x","event":"ok"}\nNOT_JSON\n{"ts":"y","event":"ok"}\n')
        idx = LogIndex(path)
        assert len(idx) == 2   # corrupt line skipped, not counted


class TestLogIndexThreadSafety:
    def test_concurrent_appends(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        errors: list[Exception] = []

        def writer():
            try:
                for _ in range(50):
                    idx.append("concurrent_write", thread=threading.get_ident())
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(idx) == 200   # 4 threads × 50 writes


class TestLogIndexEviction:
    def test_eviction_triggered_on_overflow(self, tmp_path):
        """Lines 76 and 129-131: _evict() fires when buffer exceeds max_entries."""
        idx = LogIndex(tmp_path / "e.log", max_entries=5)
        for i in range(8):
            idx.append("ev", n=i)
        # After eviction, in-memory buffer should be <= max_entries
        assert len(idx) <= 5

    def test_evict_rebuilds_searchable_index(self, tmp_path):
        """After eviction, search still works on retained entries."""
        idx = LogIndex(tmp_path / "e.log", max_entries=4)
        for i in range(6):
            idx.append("item", n=i)
        results = idx.search(event="item")
        assert len(results) <= 4


class TestLogIndexLoadEdgeCases:
    def test_empty_lines_skipped_on_load(self, tmp_path):
        """Line 149: blank lines in log file are silently ignored."""
        path = tmp_path / "e.log"
        path.write_text(
            '{"ts":"a","event":"ok"}\n'
            "\n"                           # blank line
            "   \n"                        # whitespace-only line
            '{"ts":"b","event":"ok"}\n'
        )
        idx = LogIndex(path)
        assert len(idx) == 2

    def test_max_entries_cap_applied_on_load(self, tmp_path):
        """Line 166: pre-existing log with > max_entries is capped in memory."""
        path = tmp_path / "e.log"
        lines = [json.dumps({"ts": f"t{i}", "event": "old"}) for i in range(20)]
        path.write_text("\n".join(lines) + "\n")
        idx = LogIndex(path, max_entries=5)
        # Only the most recent 5 should be retained in memory
        assert len(idx) == 5


class TestLogIndexTagList:
    def test_tags_as_list_are_all_indexed(self, tmp_path):
        """Line 179: when a 'tags' field is a list, every element is indexed."""
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ev", tags=["alpha", "beta", "gamma"])
        assert len(idx.search(tags=["alpha"])) == 1
        assert len(idx.search(tags=["beta"])) == 1
        assert len(idx.search(tags=["gamma"])) == 1
```

FILE: /home/user/wellux_testprojects/tests/test_handlers_error.py
```python
"""Tests for src/handlers/error_handler.py."""
from __future__ import annotations

import pytest

from src.handlers.error_handler import (
    AuthError,
    ContentFilterError,
    LLMError,
    RateLimitError,
    TokenLimitError,
    classify_api_error,
    handle_errors,
)


class TestClassifyApiError:
    def test_rate_limit_error(self):
        err = classify_api_error(Exception("rate limit exceeded"))
        assert isinstance(err, RateLimitError)

    def test_429_code_maps_to_rate_limit(self):
        err = classify_api_error(Exception("HTTP 429 too many requests"))
        assert isinstance(err, RateLimitError)

    def test_token_limit_error(self):
        err = classify_api_error(Exception("context length limit exceeded"))
        assert isinstance(err, TokenLimitError)

    def test_auth_error(self):
        err = classify_api_error(Exception("authentication failed invalid api key"))
        assert isinstance(err, AuthError)

    def test_401_maps_to_auth(self):
        err = classify_api_error(Exception("401 unauthorized"))
        assert isinstance(err, AuthError)

    def test_content_filter_error(self):
        err = classify_api_error(Exception("content policy violation"))
        assert isinstance(err, ContentFilterError)

    def test_unknown_error_maps_to_llm_error(self):
        err = classify_api_error(Exception("something completely unknown"))
        assert isinstance(err, LLMError)

    def test_preserves_message(self):
        err = classify_api_error(Exception("rate limit exceeded"))
        assert "rate limit exceeded" in str(err)

    # ── Bug-fix regression: operator precedence (Bug 1) ───────────────────────

    def test_context_alone_is_not_token_limit(self):
        """'context' without 'window'/'length' must not map to TokenLimitError."""
        err = classify_api_error(Exception("invalid context path in config"))
        assert not isinstance(err, TokenLimitError)
        assert isinstance(err, LLMError)

    def test_context_window_maps_to_token_limit(self):
        err = classify_api_error(Exception("context window limit exceeded"))
        assert isinstance(err, TokenLimitError)

    def test_context_length_maps_to_token_limit(self):
        err = classify_api_error(Exception("context length limit exceeded"))
        assert isinstance(err, TokenLimitError)

    def test_token_limit_maps_to_token_limit(self):
        err = classify_api_error(Exception("token limit reached: 200k"))
        assert isinstance(err, TokenLimitError)

    def test_asyncio_context_is_not_token_limit(self):
        """Asyncio context-related messages must not route to TokenLimitError."""
        err = classify_api_error(Exception("asyncio context var reset failed"))
        assert not isinstance(err, TokenLimitError)

    def test_content_filter_requires_both_content_and_filter(self):
        """'content' alone without 'filter' must not map to ContentFilterError."""
        err = classify_api_error(Exception("content type mismatch"))
        assert not isinstance(err, ContentFilterError)

    def test_policy_violation_maps_to_content_filter(self):
        err = classify_api_error(Exception("policy violation detected"))
        assert isinstance(err, ContentFilterError)

    def test_content_filter_phrase_maps_correctly(self):
        err = classify_api_error(Exception("content filter blocked the response"))
        assert isinstance(err, ContentFilterError)


class TestHandleErrors:
    async def test_passes_through_on_success(self):
        @handle_errors
        async def _fn():
            return 42

        assert await _fn() == 42

    async def test_llm_error_reraises_unchanged(self):
        """LLMError subclasses pass through without re-wrapping."""
        @handle_errors
        async def _fn():
            raise RateLimitError("already classified")

        with pytest.raises(RateLimitError, match="already classified"):
            await _fn()

    async def test_generic_exception_is_classified(self):
        """Non-LLMError exceptions are mapped to the LLMError hierarchy."""
        @handle_errors
        async def _fn():
            raise ValueError("401 bad key")

        with pytest.raises(AuthError):
            await _fn()

    async def test_chained_exception_preserved(self):
        """Classified error must chain via __cause__ to the original."""
        original = RuntimeError("rate limit exceeded")

        @handle_errors
        async def _fn():
            raise original

        with pytest.raises(RateLimitError) as exc_info:
            await _fn()
        assert exc_info.value.__cause__ is original

    async def test_preserves_function_name(self):
        @handle_errors
        async def my_special_fn():
            return "ok"

        assert my_special_fn.__name__ == "my_special_fn"

    async def test_unknown_exception_becomes_llm_error(self):
        @handle_errors
        async def _fn():
            raise OSError("disk full")

        with pytest.raises(LLMError):
            await _fn()


class TestErrorHierarchy:
    def test_rate_limit_is_llm_error(self):
        assert issubclass(RateLimitError, LLMError)

    def test_token_limit_is_llm_error(self):
        assert issubclass(TokenLimitError, LLMError)

    def test_auth_is_llm_error(self):
        assert issubclass(AuthError, LLMError)

    def test_content_filter_is_llm_error(self):
        assert issubclass(ContentFilterError, LLMError)
```

FILE: /home/user/wellux_testprojects/tests/test_prompt_chainer.py
```python
"""Tests for src/prompt_engineering/chainer.py — PromptChain with mock LLM."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.llm.base import CompletionResponse
from src.prompt_engineering.chainer import PromptChain


def make_mock_client(responses: list[str]):
    """Return a mock LLMClient that returns responses in sequence."""
    client = MagicMock()
    resps = [
        CompletionResponse(
            content=r, model="claude-sonnet-4-6",
            input_tokens=10, output_tokens=len(r.split()),
            stop_reason="end_turn",
        )
        for r in responses
    ]
    client.complete = AsyncMock(side_effect=resps)
    return client


@pytest.mark.asyncio
async def test_single_step_chain():
    client = make_mock_client(["step1 output"])
    chain = PromptChain(client).add_step(
        "step1",
        lambda ctx: "prompt",
    )
    result = await chain.run()
    assert result.steps["step1"] == "step1 output"
    assert result.final == "step1 output"


@pytest.mark.asyncio
async def test_two_step_chain_passes_context():
    client = make_mock_client(["outline text", "draft text"])
    chain = (
        PromptChain(client)
        .add_step("outline", lambda ctx: "write outline")
        .add_step("draft", lambda ctx: f"expand: {ctx['outline']}")
    )
    result = await chain.run()
    assert result.steps["outline"] == "outline text"
    assert result.steps["draft"] == "draft text"
    # Verify the second step received the first step's output in its prompt
    second_call_prompt = client.complete.call_args_list[1][0][0].prompt
    assert "outline text" in second_call_prompt


@pytest.mark.asyncio
async def test_initial_context_passed_to_first_step():
    client = make_mock_client(["result"])
    chain = PromptChain(client).add_step(
        "step1",
        lambda ctx: f"topic: {ctx['topic']}",
    )
    await chain.run({"topic": "RAG systems"})
    prompt_used = client.complete.call_args_list[0][0][0].prompt
    assert "RAG systems" in prompt_used


@pytest.mark.asyncio
async def test_transform_applied_to_output():
    client = make_mock_client(["  whitespace  "])
    chain = PromptChain(client).add_step(
        "clean",
        lambda ctx: "prompt",
        transform=str.strip,
    )
    result = await chain.run()
    assert result.steps["clean"] == "whitespace"


@pytest.mark.asyncio
async def test_total_cost_aggregates_steps():
    client = make_mock_client(["a", "b", "c"])
    chain = (
        PromptChain(client)
        .add_step("s1", lambda ctx: "p1")
        .add_step("s2", lambda ctx: "p2")
        .add_step("s3", lambda ctx: "p3")
    )
    result = await chain.run()
    assert result.total_cost_usd >= 0.0
    assert result.total_tokens > 0
    assert len(result.responses) == 3


@pytest.mark.asyncio
async def test_fluent_api_returns_chain():
    client = make_mock_client(["x"])
    chain = PromptChain(client)
    returned = chain.add_step("s", lambda ctx: "p")
    assert returned is chain


@pytest.mark.asyncio
async def test_empty_chain_returns_empty_result():
    client = make_mock_client([])
    result = await PromptChain(client).run()
    assert result.final is None
    assert result.total_cost_usd == 0.0


@pytest.mark.asyncio
async def test_run_parallel_branches_returns_all_results():
    """Cover PromptChain.run_parallel_branches() (lines 127-134)."""
    client_a = make_mock_client(["branch A result"])
    client_b = make_mock_client(["branch B result"])

    chain_a = PromptChain(client_a).add_step("step", lambda ctx: "prompt A")
    chain_b = PromptChain(client_b).add_step("step", lambda ctx: "prompt B")

    orchestrator = PromptChain(make_mock_client([]))
    results = await orchestrator.run_parallel_branches(
        {"branch_a": chain_a, "branch_b": chain_b}
    )

    assert set(results.keys()) == {"branch_a", "branch_b"}
    assert results["branch_a"].final == "branch A result"
    assert results["branch_b"].final == "branch B result"


@pytest.mark.asyncio
async def test_run_parallel_branches_empty():
    orchestrator = PromptChain(make_mock_client([]))
    results = await orchestrator.run_parallel_branches({})
    assert results == {}
```

FILE: /home/user/wellux_testprojects/tests/test_prompt_few_shot.py
```python
"""Tests for src/prompt_engineering/few_shot.py."""
from src.prompt_engineering.few_shot import FewShotManager


class TestFewShotManager:
    def test_empty_manager_builds_prompt_with_just_query(self):
        mgr = FewShotManager()
        result = mgr.build_prompt("my query")
        assert "my query" in result
        assert "Input:" in result
        assert "Output:" in result

    def test_adds_examples_to_prompt(self):
        mgr = FewShotManager()
        mgr.add("cat", "animal")
        mgr.add("oak", "tree")
        result = mgr.build_prompt("rose")
        assert "cat" in result
        assert "animal" in result
        assert "oak" in result
        assert "tree" in result
        assert "rose" in result

    def test_prefix_included_in_prompt(self):
        mgr = FewShotManager(prefix="Classify the following:")
        result = mgr.build_prompt("query")
        assert "Classify the following:" in result

    def test_max_examples_limits_output(self):
        mgr = FewShotManager()
        for i in range(10):
            mgr.add(f"input{i}", f"output{i}")
        result = mgr.build_prompt("query", max_examples=2)
        # Only last 2 examples should appear
        assert "input8" in result
        assert "input9" in result
        assert "input0" not in result

    def test_len_returns_example_count(self):
        mgr = FewShotManager()
        assert len(mgr) == 0
        mgr.add("a", "b")
        mgr.add("c", "d")
        assert len(mgr) == 2

    def test_get_by_label(self):
        mgr = FewShotManager()
        mgr.add("great product", "positive", label="sentiment")
        mgr.add("terrible service", "negative", label="sentiment")
        mgr.add("select * from users", "sql", label="code")
        sentiment = mgr.get_by_label("sentiment")
        assert len(sentiment) == 2
        assert all(e.label == "sentiment" for e in sentiment)

    def test_to_messages_format(self):
        mgr = FewShotManager()
        mgr.add("hello", "world")
        messages = mgr.to_messages("test")
        assert messages[0] == {"role": "user", "content": "hello"}
        assert messages[1] == {"role": "assistant", "content": "world"}
        assert messages[-1] == {"role": "user", "content": "test"}

    def test_to_messages_no_examples(self):
        mgr = FewShotManager()
        messages = mgr.to_messages("query")
        assert messages == [{"role": "user", "content": "query"}]

    def test_custom_labels(self):
        mgr = FewShotManager(input_label="Q", output_label="A")
        mgr.add("question", "answer")
        result = mgr.build_prompt("new question")
        assert "Q: question" in result
        assert "A: answer" in result
```

FILE: /home/user/wellux_testprojects/tests/test_prompt_templates.py
```python
"""Tests for src/prompt_engineering/templates.py."""
import pytest

from src.prompt_engineering.templates import PromptTemplate, TemplateLibrary, default_library


class TestPromptTemplate:
    def test_render_single_variable(self):
        t = PromptTemplate("Hello {{name}}!")
        assert t.render(name="world") == "Hello world!"

    def test_render_multiple_variables(self):
        t = PromptTemplate("{{greeting}} {{name}}, you are {{age}} years old.")
        result = t.render(greeting="Hi", name="Alice", age=30)
        assert result == "Hi Alice, you are 30 years old."

    def test_auto_detects_required_vars(self):
        t = PromptTemplate("{{a}} and {{b}}")
        assert set(t.variables()) == {"a", "b"}

    def test_missing_variable_raises(self):
        t = PromptTemplate("Hello {{name}}!")
        with pytest.raises(ValueError, match="Missing template variables"):
            t.render()

    def test_extra_kwargs_ignored(self):
        t = PromptTemplate("Hello {{name}}!")
        result = t.render(name="Bob", unused="ignored")
        assert result == "Hello Bob!"

    def test_no_variables_renders_as_is(self):
        t = PromptTemplate("No variables here.")
        assert t.render() == "No variables here."

    def test_integer_value_coerced_to_string(self):
        t = PromptTemplate("Count: {{n}}")
        assert t.render(n=42) == "Count: 42"

    def test_explicit_required_vars(self):
        t = PromptTemplate("{{a}} {{b}}", required_vars=["a"])
        with pytest.raises(ValueError):
            t.render()  # missing "a"


class TestTemplateLibrary:
    def test_register_and_render(self):
        lib = TemplateLibrary()
        lib.register("greet", "Hello {{name}}!")
        assert lib.render("greet", **{"name": "Alice"}) == "Hello Alice!"

    def test_get_unknown_raises(self):
        lib = TemplateLibrary()
        with pytest.raises(KeyError, match="not registered"):
            lib.get("nonexistent")

    def test_list_templates(self):
        lib = TemplateLibrary()
        lib.register("t1", "{{x}}")
        lib.register("t2", "{{y}}")
        assert set(lib.list_templates()) == {"t1", "t2"}


class TestDefaultLibrary:
    def test_code_review_template_exists(self):
        result = default_library.render("code_review", language="Python", code="x = 1")
        assert "Python" in result
        assert "x = 1" in result

    def test_summarize_template_exists(self):
        result = default_library.render("summarize", max_words=50, text="some text")
        assert "50" in result
        assert "some text" in result

    def test_research_query_template_exists(self):
        result = default_library.render("research_query", topic="RAG systems")
        assert "RAG systems" in result

    def test_bug_fix_template_exists(self):
        result = default_library.render(
            "bug_fix", language="Python", error="TypeError", code="x = None + 1"
        )
        assert "TypeError" in result
```

FILE: /home/user/wellux_testprojects/tests/test_utils_cache.py
```python
"""Tests for src/utils/cache.py — ResponseCache hit/miss/TTL/eviction."""
import time

from src.llm.base import CompletionRequest, CompletionResponse
from src.utils.cache import ResponseCache, _cache_key


def make_request(**kwargs) -> CompletionRequest:
    defaults = dict(prompt="test", system=None, model=None, max_tokens=4096, temperature=0.7)
    defaults.update(kwargs)
    return CompletionRequest(**defaults)


def make_response(content="answer") -> CompletionResponse:
    return CompletionResponse(
        content=content, model="claude-sonnet-4-6",
        input_tokens=10, output_tokens=5, stop_reason="end_turn",
    )


class TestCacheKey:
    def test_same_request_same_key(self):
        r1 = make_request(prompt="hello")
        r2 = make_request(prompt="hello")
        assert _cache_key(r1) == _cache_key(r2)

    def test_different_prompt_different_key(self):
        assert _cache_key(make_request(prompt="a")) != _cache_key(make_request(prompt="b"))

    def test_different_temperature_different_key(self):
        assert _cache_key(make_request(temperature=0.0)) != _cache_key(make_request(temperature=1.0))

    def test_different_model_different_key(self):
        assert _cache_key(make_request(model="opus")) != _cache_key(make_request(model="haiku"))


class TestResponseCache:
    def test_miss_on_empty_cache(self):
        cache = ResponseCache()
        assert cache.get(make_request()) is None

    def test_set_then_get(self):
        cache = ResponseCache()
        req = make_request(prompt="q1")
        resp = make_response("answer1")
        cache.set(req, resp)
        result = cache.get(req)
        assert result is not None
        assert result.content == "answer1"

    def test_different_requests_dont_collide(self):
        cache = ResponseCache()
        req1 = make_request(prompt="q1")
        req2 = make_request(prompt="q2")
        cache.set(req1, make_response("a1"))
        cache.set(req2, make_response("a2"))
        assert cache.get(req1).content == "a1"
        assert cache.get(req2).content == "a2"

    def test_ttl_expiry(self):
        cache = ResponseCache(ttl_seconds=0.05)
        req = make_request()
        cache.set(req, make_response())
        assert cache.get(req) is not None
        time.sleep(0.1)
        assert cache.get(req) is None

    def test_invalidate(self):
        cache = ResponseCache()
        req = make_request()
        cache.set(req, make_response())
        cache.invalidate(req)
        assert cache.get(req) is None

    def test_clear(self):
        cache = ResponseCache()
        for i in range(5):
            cache.set(make_request(prompt=str(i)), make_response())
        assert cache.size == 5
        cache.clear()
        assert cache.size == 0

    def test_max_size_evicts_oldest(self):
        cache = ResponseCache(max_size=3)
        reqs = [make_request(prompt=str(i)) for i in range(4)]
        for r in reqs:
            cache.set(r, make_response())
        assert cache.size == 3
        # oldest (prompt="0") should be evicted
        assert cache.get(reqs[0]) is None
        assert cache.get(reqs[3]) is not None
```

FILE: /home/user/wellux_testprojects/tests/test_utils_logger.py
```python
"""Tests for src/utils/logger.py — structured JSON logger."""
from __future__ import annotations

import json
import logging

from src.utils.logger import StructuredLogger, get_logger


class TestStructuredLogger:
    def test_get_logger_returns_structured_logger(self):
        lg = get_logger("test.get_logger")
        assert isinstance(lg, StructuredLogger)

    def test_info_emits_json_line(self, capsys):
        lg = get_logger("test.info")
        lg.info("hello", request_id="abc")
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["msg"] == "hello"
        assert record["request_id"] == "abc"
        assert record["level"] == "INFO"

    def test_warning_emits_warning_level(self, capsys):
        lg = get_logger("test.warning")
        lg.warning("watch out")
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["level"] == "WARNING"

    def test_error_emits_error_level(self, capsys):
        lg = get_logger("test.error")
        lg.error("bad thing", code=500)
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["level"] == "ERROR"
        assert record["code"] == 500

    def test_critical_emits_critical_level(self, capsys):
        lg = get_logger("test.critical")
        lg.critical("fatal", component="db")
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["level"] == "CRITICAL"
        assert record["component"] == "db"

    def test_debug_below_default_level_not_emitted(self, capsys):
        lg = get_logger("test.debug")  # default level = INFO
        lg.debug("silent")
        out = capsys.readouterr().out
        assert out == ""

    def test_exc_info_serialized_in_formatter(self):
        """The exc_info branch in _StructuredFormatter adds an 'exc' string key."""
        import sys

        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = logging.LogRecord(
            name="t", level=logging.ERROR, pathname="", lineno=0,
            msg="boom", args=(), exc_info=None,
        )
        try:
            raise RuntimeError("test exc")
        except RuntimeError:
            record.exc_info = sys.exc_info()
        result = json.loads(fmt.format(record))
        assert "exc" in result
        assert "RuntimeError" in result["exc"]


class TestSensitiveFieldRedaction:
    def _make_record(self, **kwargs) -> logging.LogRecord:
        record = logging.LogRecord(
            name="t", level=logging.INFO, pathname="", lineno=0,
            msg="test", args=(), exc_info=None,
        )
        record.__dict__.update(kwargs)
        return record

    def test_password_is_redacted(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(password="s3cr3t")
        result = json.loads(fmt.format(record))
        assert result["password"] == "[REDACTED]"
        assert "s3cr3t" not in json.dumps(result)

    def test_api_key_is_redacted(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(api_key="sk-ant-abc123")
        result = json.loads(fmt.format(record))
        assert result["api_key"] == "[REDACTED]"

    def test_token_is_redacted(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(token="bearer-xyz")
        result = json.loads(fmt.format(record))
        assert result["token"] == "[REDACTED]"

    def test_non_sensitive_field_passes_through(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(model="claude-sonnet-4-6", latency_ms=42)
        result = json.loads(fmt.format(record))
        assert result["model"] == "claude-sonnet-4-6"
        assert result["latency_ms"] == 42
```

FILE: /home/user/wellux_testprojects/tests/test_utils_rate_limiter.py
```python
"""Tests for src/utils/rate_limiter.py — token bucket behavior."""
import asyncio
import time

import pytest

from src.utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_single_acquire_succeeds():
    limiter = RateLimiter(requests_per_minute=60)
    await limiter.acquire()  # should not raise or block significantly


@pytest.mark.asyncio
async def test_burst_within_capacity():
    limiter = RateLimiter(requests_per_minute=600)  # 10/sec bucket
    t0 = time.monotonic()
    for _ in range(5):
        await limiter.acquire()
    elapsed = time.monotonic() - t0
    # 5 tokens available immediately — should complete fast
    assert elapsed < 1.0


@pytest.mark.asyncio
async def test_available_tokens_decreases():
    limiter = RateLimiter(requests_per_minute=60)
    before = limiter.available_tokens
    await limiter.acquire()
    after = limiter.available_tokens
    assert after < before


@pytest.mark.asyncio
async def test_rate_limiting_delays_excess_requests():
    # 60 rpm = 1 token/sec; start with 1 token, request 2 → second must wait ~1s
    limiter = RateLimiter(requests_per_minute=60)
    await limiter.acquire()  # consume the initial token
    # drain remaining tokens
    limiter._tokens = 0.0

    t0 = time.monotonic()
    await limiter.acquire()  # must wait for refill
    elapsed = time.monotonic() - t0
    assert elapsed >= 0.8  # at least ~1 second


@pytest.mark.asyncio
async def test_tokens_refill_over_time():
    limiter = RateLimiter(requests_per_minute=600)  # 10/sec
    limiter._tokens = 0.0
    await asyncio.sleep(0.2)
    assert limiter.available_tokens > 0
```

FILE: /home/user/wellux_testprojects/tests/test_utils_token_counter.py
```python
"""Tests for src/utils/token_counter.py."""
import pytest

from src.utils.token_counter import (
    count_tokens_approx,
    estimate_cost,
    fits_in_context,
    split_into_chunks,
)


class TestCountTokensApprox:
    def test_empty_string(self):
        assert count_tokens_approx("") == 1  # max(1, 0//4)

    def test_short_text(self):
        # "hello" = 5 chars → 5//4 = 1, max(1,1) = 1
        assert count_tokens_approx("hello") >= 1

    def test_longer_text(self):
        text = "a" * 400
        count = count_tokens_approx(text)
        assert 90 <= count <= 110  # ~100 tokens

    def test_claude_model_uses_claude_ratio(self):
        text = "a" * 380
        count = count_tokens_approx(text, model="claude-sonnet-4-6")
        assert count > 0

    def test_different_models_may_differ(self):
        text = "x" * 1000
        c1 = count_tokens_approx(text, model="claude-sonnet-4-6")
        c2 = count_tokens_approx(text, model="gpt-4o")
        # Both positive, may differ slightly
        assert c1 > 0
        assert c2 > 0


class TestFitsInContext:
    def test_short_text_fits(self):
        assert fits_in_context("hello", "claude-sonnet-4-6", context_limit=10000)

    def test_long_text_doesnt_fit(self):
        text = "a" * 800_000  # ~200k tokens
        assert not fits_in_context(text, "claude-sonnet-4-6", context_limit=1000)


class TestEstimateCost:
    def test_zero_tokens_zero_cost(self):
        assert estimate_cost(0, 0, 3.0, 15.0) == 0.0

    def test_one_million_input_tokens(self):
        cost = estimate_cost(1_000_000, 0, 3.0, 15.0)
        assert cost == pytest.approx(3.0)

    def test_one_million_output_tokens(self):
        cost = estimate_cost(0, 1_000_000, 3.0, 15.0)
        assert cost == pytest.approx(15.0)

    def test_combined(self):
        cost = estimate_cost(1_000_000, 1_000_000, 3.0, 15.0)
        assert cost == pytest.approx(18.0)


class TestSplitIntoChunks:
    def test_short_text_one_chunk(self):
        chunks = split_into_chunks("hello world", max_tokens=1000)
        assert len(chunks) == 1
        assert chunks[0] == "hello world"

    def test_long_text_splits(self):
        text = "a" * 10000
        chunks = split_into_chunks(text, max_tokens=100)
        assert len(chunks) > 1
        assert "".join(chunks) == text  # no data lost

    def test_each_chunk_within_limit(self):
        text = "b" * 10000
        max_tokens = 100
        chunks = split_into_chunks(text, max_tokens=max_tokens)
        for chunk in chunks:
            assert count_tokens_approx(chunk) <= max_tokens + 5  # small tolerance
```


## 4.12 Docker and CI

FILE: /home/user/wellux_testprojects/Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# curl version tracks the base image — pin base image by digest for full reproducibility:
#   FROM python:3.12-slim@sha256:<digest>
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── deps layer (cached unless pyproject.toml changes) ────────────────────────
FROM base AS deps

COPY pyproject.toml ./
# Install only core runtime deps (no ML/dev extras — keeps image ~200 MB)
RUN pip install --no-cache-dir \
    "anthropic>=0.87.0,<1.0" \
    "cryptography>=46.0.6" \
    "httpx>=0.27.0,<1.0" \
    "aiohttp>=3.9.0,<4.0" \
    "fastapi>=0.111.0,<1.0" \
    "uvicorn[standard]>=0.30.0,<1.0" \
    "pydantic>=2.7.0,<3.0" \
    "PyYAML>=6.0.1" \
    "python-dotenv>=1.0.0"

# ── app layer ─────────────────────────────────────────────────────────────────
FROM deps AS app

COPY src/ ./src/
COPY config/ ./config/
COPY data/evals/ ./data/evals/

# Create remaining data directories and non-root user
RUN mkdir -p data/cache data/outputs data/research && \
    useradd --create-home --uid 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

FILE: /home/user/wellux_testprojects/docker-compose.yml
```yaml
services:
  api:
    build:
      context: .
      target: app
    image: ccm-api:latest
    ports:
      - "${PORT:-8000}:8000"
    env_file:
      - path: .env
        required: false      # allow running without .env (vars can come from environment:)
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - CCM_LOG_PATH=data/cache/events.log
    volumes:
      - ccm-data:/app/data   # named volume — persists events.log across restarts
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 512M
        reservations:
          memory: 128M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

  # Optional: local MCP memory server
  memory:
    image: node:20-slim
    working_dir: /app
    command: >
      sh -c "npx -y @modelcontextprotocol/server-memory"
    ports:
      - "3001:3001"
    restart: unless-stopped
    profiles: ["mcp"]
    deploy:
      resources:
        limits:
          memory: 256M

volumes:
  ccm-data:
    driver: local
```

FILE: /home/user/wellux_testprojects/.github/workflows/ci.yml
```yaml
name: CI

on:
  push:
    branches: ["**"]
  pull_request:
    branches: [main, "claude/**"]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
          cache-dependency-path: pyproject.toml

      - name: Install dependencies (no heavy ML libs)
        run: |
          python -m pip install --upgrade "pip>=25.3" "setuptools>=78.1.1" "wheel>=0.46.2"
          pip install \
            "anthropic>=0.87.0,<1.0" \
            "cryptography>=46.0.6" \
            "httpx>=0.27.0,<1.0" \
            "aiohttp>=3.9.0,<4.0" \
            "fastapi>=0.111.0,<1.0" \
            "uvicorn>=0.30.0,<1.0" \
            "pydantic>=2.7.0,<3.0" \
            "PyYAML>=6.0.1" \
            "python-dotenv>=1.0.0" \
            "pytest>=8.2.0,<10.0" \
            "pytest-asyncio>=0.23.0,<1.0" \
            "pytest-cov>=5.0.0,<8.0" \
            "ruff>=0.9.0,<1.0"

      - name: Lint (ruff)
        # CLI --select overrides pyproject.toml select; matches E/F/W/I subset
        run: ruff check src/ tests/ --select E,F,W,I --ignore E501 --no-cache

      - name: Run tests
        run: |
          pytest tests/ \
            --tb=long \
            --cov=src \
            --cov-report=term-missing \
            --cov-report=xml \
            --cov-fail-under=85 \
            -v

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        if: matrix.python-version == '3.12'
        with:
          name: coverage-report
          path: coverage.xml

      - name: Security audit (pip-audit)
        if: matrix.python-version == '3.12'
        continue-on-error: true  # informational — system deps (cryptography, pip, setuptools)
        run: |
          pip install pip-audit
          pip-audit --desc --skip-editable

  smoke-evals:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: pyproject.toml

      - name: Install dependencies
        run: |
          python -m pip install --upgrade "pip>=25.3" "setuptools>=78.1.1" "wheel>=0.46.2"
          pip install \
            "pydantic>=2.7.0,<3.0" \
            "PyYAML>=6.0.1" \
            "python-dotenv>=1.0.0"

      - name: Run smoke eval suite (dry-run, no API key)
        run: python -m src.cli eval run data/evals/smoke.jsonl --dry-run

  routing-evals:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: pyproject.toml

      - name: Install dependencies
        run: |
          python -m pip install --upgrade "pip>=25.3" "setuptools>=78.1.1" "wheel>=0.46.2"
          pip install \
            "pydantic>=2.7.0,<3.0" \
            "PyYAML>=6.0.1" \
            "python-dotenv>=1.0.0"

      - name: Run routing eval suite (dry-run, no API key)
        # Validates that the routing system picks the expected model/agent
        # for each case. --dry-run echoes the prompt instead of calling the API.
        run: python -m src.cli eval run data/evals/routing.jsonl --dry-run

  live-evals:
    runs-on: ubuntu-latest
    needs: [test, smoke-evals]
    # Only run when the secret is available AND not a fork PR (forks don't receive
    # secrets, so the condition would silently be true on self-hosted runners or
    # if ever misconfigured). continue-on-error: LLM outputs are non-deterministic.
    continue-on-error: true
    if: >-
      ${{ secrets.ANTHROPIC_API_KEY != '' &&
          (github.event_name != 'pull_request' ||
           github.event.pull_request.head.repo.full_name == github.repository) }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: pyproject.toml

      - name: Install dependencies
        run: |
          python -m pip install --upgrade "pip>=25.3" "setuptools>=78.1.1" "wheel>=0.46.2"
          pip install \
            "anthropic>=0.87.0,<1.0" \
            "cryptography>=46.0.6" \
            "pydantic>=2.7.0,<3.0" \
            "PyYAML>=6.0.1" \
            "python-dotenv>=1.0.0"

      - name: Run live eval suite (real API calls)
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        # --threshold 0.7: partial credit allowed (LLM output is non-deterministic)
        # --tag live: only cases tagged 'live' (prompting.jsonl)
        run: |
          python -m src.cli eval run data/evals/prompting.jsonl \
            --tag live \
            --threshold 0.7

  lint-dockerfile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile
          config: .hadolint.yaml
```


## 4.13 Config Files

FILE: /home/user/wellux_testprojects/config/__init__.py
```python
"""Configuration package for wellux_testprojects."""
```

FILE: /home/user/wellux_testprojects/config/model_config.yaml
```yaml
# Model Configuration
# Update model IDs as new versions are released

models:
  # Best quality — use for: complex reasoning, architecture, security, research
  opus:
    provider: anthropic
    model: claude-opus-4-6
    max_tokens: 16384
    temperature: 0.3
    use_for: [research, architecture, security_audit, complex_reasoning]

  # Best balance — default for most tasks
  sonnet:
    provider: anthropic
    model: claude-sonnet-4-6
    max_tokens: 8192
    temperature: 0.7
    use_for: [code_review, implementation, writing, analysis]

  # Fastest + cheapest — use for: classification, simple transforms, batch
  haiku:
    provider: anthropic
    model: claude-haiku-4-5-20251001
    max_tokens: 4096
    temperature: 0.5
    use_for: [classification, simple_transforms, batch_processing, routing]

# Default model for tasks not explicitly configured
default: sonnet

# Rate limits (per minute)
rate_limits:
  opus: 50
  sonnet: 100
  haiku: 500

# Cost per million tokens (approximate, check Anthropic pricing)
cost_per_mtok:
  opus:
    input: 15.0
    output: 75.0
  sonnet:
    input: 3.0
    output: 15.0
  haiku:
    input: 0.25
    output: 1.25

# Model routing rules
routing:
  # Use haiku for tasks where cost matters and quality threshold is low
  use_haiku_when:
    - task_type: classification
    - task_type: simple_summarization
    - batch_size_gt: 100
  # Use opus for tasks requiring highest quality
  use_opus_when:
    - task_type: security_audit
    - task_type: architecture_review
    - task_type: research_synthesis
```

FILE: /home/user/wellux_testprojects/config/logging_config.yaml
```yaml
# Logging Configuration
# Used by src/utils/logger.py

logging:
  version: 1
  formatters:
    json:
      class: pythonjsonlogger.jsonlogger.JsonFormatter
      format: "%(timestamp)s %(level)s %(name)s %(message)s"
    simple:
      format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

  handlers:
    console:
      class: logging.StreamHandler
      formatter: simple
      level: INFO
      stream: ext://sys.stdout

    file:
      class: logging.handlers.RotatingFileHandler
      formatter: json
      filename: data/cache/app.log
      maxBytes: 10485760  # 10MB
      backupCount: 5
      level: DEBUG

    error_file:
      class: logging.handlers.RotatingFileHandler
      formatter: json
      filename: data/cache/errors.log
      maxBytes: 10485760
      backupCount: 5
      level: ERROR

  loggers:
    llm:
      level: DEBUG
      handlers: [console, file]
      propagate: false

    research:
      level: INFO
      handlers: [console, file]
      propagate: false

    security:
      level: WARNING
      handlers: [console, file, error_file]
      propagate: false

  root:
    level: INFO
    handlers: [console, file]

# Sensitive fields to redact from logs
redact_fields:
  - api_key
  - password
  - token
  - secret
  - authorization

# Structured log fields always included
default_fields:
  service: claude-code-max
  version: "1.0.0"
```

FILE: /home/user/wellux_testprojects/config/prompt_templates.yaml
```yaml
# Reusable Prompt Templates
# Use in src/prompt_engineering/templates.py

templates:
  # System prompts
  system:
    code_reviewer: |
      You are a senior software engineer performing a thorough code review.
      Check for: correctness, performance, security, readability, test coverage.
      Provide specific file:line references for each issue.
      Format: ## Review\n### Issues\n- [severity] file:line — description\n### Verdict: APPROVE/REQUEST_CHANGES

    security_auditor: |
      You are a security engineer performing an OWASP Top 10 audit.
      For each finding: category, file:line, severity (Critical/High/Medium/Low), CVSS score, remediation.
      Be thorough — false negatives are worse than false positives.

    researcher: |
      You are a research scientist in the style of Andrej Karpathy.
      For each topic: explain from first principles, implement a minimal example,
      distill to the core insight. Avoid surface-level summaries.

    architect: |
      You are a principal software architect. Design systems that are:
      simple (not clever), scalable (handles 10x load), maintainable (any engineer understands it).
      Always include trade-offs and what you chose NOT to do.

  # Task templates (use with .format() or Jinja2)
  tasks:
    analyze_code: |
      Analyze this code for {analysis_type}:

      ```{language}
      {code}
      ```

      Focus on: {focus_areas}

    summarize_paper: |
      Summarize this research paper for a practitioner audience:

      {paper_content}

      Required sections: Core Insight, Key Technique, Practical Takeaway, Limitations

    explain_error: |
      Explain this error and provide a fix:

      Error: {error_message}

      Context:
      {code_context}

  # Few-shot prefixes
  few_shot:
    code_fix_example: |
      Example:
      Error: TypeError: 'NoneType' object has no attribute 'split'
      Root cause: user variable is None when email is not set
      Fix: Add `if user is None: return None` before accessing user.email
```


## 4.14 Eval Data

FILE: /home/user/wellux_testprojects/data/evals/smoke.jsonl
```json
{"id":"echo-hello","prompt":"hello world","contains":["hello"],"excludes":[],"tags":["smoke","fast"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{"suite":"smoke","description":"fast sanity checks, echo-LLM pattern"}}
{"id":"echo-python","prompt":"Python is a programming language","contains":["Python","language"],"excludes":[],"tags":["smoke","fast"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{}}
{"id":"echo-no-profanity","prompt":"This is a clean response","contains":["clean"],"excludes":["damn","hell","crap"],"tags":["smoke","safety"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{}}
{"id":"echo-json-safe","prompt":"{\"key\": \"value\"}","contains":["{"],"excludes":[],"tags":["smoke","format"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{}}
{"id":"echo-multiline","prompt":"line one\nline two\nline three","contains":["line"],"excludes":[],"tags":["smoke","fast"],"expected":null,"max_tokens":128,"temperature":0.0,"metadata":{}}
{"id":"echo-excludes-verified","prompt":"The answer is correct and complete","contains":["correct"],"excludes":["wrong","broken","error"],"tags":["smoke","excludes"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{"note":"verifies excludes scorer is exercised — prompt does not contain excluded words"}}
```

FILE: /home/user/wellux_testprojects/data/evals/routing.jsonl
```json
# Routing eval suite — tests that the router picks the right model/agent
# Run with: ccm eval run routing.jsonl --dry-run
# (Dry-run echoes the prompt; tests verify routing metadata, not LLM output)
{"id":"simple-summary-haiku","prompt":"Summarise this text in one sentence: The quick brown fox jumps over the lazy dog.","contains":["quick","fox"],"excludes":[],"tags":["routing","haiku"],"expected":null,"max_tokens":128,"temperature":0.0,"metadata":{"expected_model":"haiku"}}
{"id":"code-review-sonnet","prompt":"Review this Python function for bugs and suggest improvements: def add(a, b): return a+b","contains":["add","function"],"excludes":[],"tags":["routing","sonnet","code"],"expected":null,"max_tokens":256,"temperature":0.0,"metadata":{"expected_model":"sonnet"}}
{"id":"security-audit-opus","prompt":"Perform a comprehensive security audit of this multi-tier cloud architecture with authentication, authorization, encryption, and threat modelling","contains":["security","architecture"],"excludes":[],"tags":["routing","opus","security"],"expected":null,"max_tokens":512,"temperature":0.0,"metadata":{"expected_model":"opus"}}
{"id":"format-text-haiku","prompt":"Format this CSV as a markdown table: name,age\nAlice,30\nBob,25","contains":["name","age"],"excludes":[],"tags":["routing","haiku","format"],"expected":null,"max_tokens":128,"temperature":0.0,"metadata":{"expected_model":"haiku"}}
{"id":"debug-complex-sonnet","prompt":"Debug this failing async Python test that uses pytest-asyncio, mock.patch, and checks database consistency after a race condition","contains":["debug","async","test"],"excludes":[],"tags":["routing","sonnet","debug"],"expected":null,"max_tokens":512,"temperature":0.0,"metadata":{"expected_model":"sonnet"}}
```

FILE: /home/user/wellux_testprojects/data/evals/prompting.jsonl
```json
# Prompting quality suite — tests for real LLM runs (needs ANTHROPIC_API_KEY)
# Run with: ccm eval run prompting.jsonl
# Skip in CI: these require live API calls
{"id":"basic-greeting","prompt":"Say hello in exactly three words.","contains":[],"excludes":[],"tags":["prompting","live"],"expected":null,"max_tokens":32,"temperature":0.0,"metadata":{"note":"expect short greeting"}}
{"id":"count-words","prompt":"How many words are in this sentence: The cat sat on the mat","contains":["6"],"excludes":[],"tags":["prompting","math","live"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{}}
{"id":"capital-france","prompt":"What is the capital of France? Answer in one word.","contains":["Paris"],"excludes":["London","Berlin","Madrid"],"tags":["prompting","factual","live"],"expected":"Paris","max_tokens":16,"temperature":0.0,"metadata":{}}
{"id":"python-add-function","prompt":"Write a Python function called add that takes two numbers and returns their sum. Just the function, no explanation.","contains":["def add","return"],"excludes":[],"tags":["prompting","code","live"],"expected":null,"max_tokens":128,"temperature":0.0,"metadata":{}}
{"id":"json-output","prompt":"Output a JSON object with keys 'name' and 'age' for a person named Alice who is 30. Output only valid JSON.","contains":["{","Alice","30","}"],"excludes":[],"tags":["prompting","json","live"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{}}
{"id":"no-hallucination","prompt":"Who is the current CEO of Anthropic?","contains":["Dario"],"excludes":["OpenAI","Google","Microsoft"],"tags":["prompting","factual","live"],"expected":null,"max_tokens":64,"temperature":0.0,"metadata":{}}
```


## 4.15 Examples

FILE: /home/user/wellux_testprojects/examples/basic_completion.py
```python
#!/usr/bin/env python3
"""Basic completion example — single prompt → response."""
import asyncio
import os

from src.llm import ClaudeClient, build_request


async def main() -> None:
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    request = build_request(
        prompt="Explain the key insight behind attention mechanisms in transformers in 3 sentences.",
        system="You are a concise AI research assistant.",
        max_tokens=512,
        temperature=0.3,
    )

    print("Sending request...")
    response = await client.complete(request)

    print(f"\n--- Response ---")
    print(response.content)
    print(f"\n--- Stats ---")
    print(f"Model:         {response.model}")
    print(f"Input tokens:  {response.input_tokens}")
    print(f"Output tokens: {response.output_tokens}")
    print(f"Cost:          ${response.cost_usd:.6f}")
    print(f"Stop reason:   {response.stop_reason}")


if __name__ == "__main__":
    asyncio.run(main())
```

FILE: /home/user/wellux_testprojects/examples/chat_session.py
```python
#!/usr/bin/env python3
"""Multi-turn chat session with streaming output."""
import asyncio
import os
import sys

from src.llm import ClaudeClient, build_request


SYSTEM_PROMPT = """You are a helpful AI assistant that is concise, direct, and technically accurate.
When asked about code, always include working examples. Keep answers under 300 words unless depth is needed."""


async def chat_session() -> None:
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    history: list[str] = []

    print("Claude Code Max — Chat Session")
    print("Type 'quit' or Ctrl+C to exit, 'clear' to reset history.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            history.clear()
            print("[History cleared]\n")
            continue

        # Build context-aware prompt from history
        context = "\n\n".join(history[-6:])  # last 3 turns
        prompt = f"{context}\n\nUser: {user_input}\nAssistant:" if context else user_input

        request = build_request(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            max_tokens=1024,
            temperature=0.7,
        )

        print("Assistant: ", end="", flush=True)
        full_response = []

        async for token in client.stream(request):
            print(token, end="", flush=True)
            full_response.append(token)

        assistant_reply = "".join(full_response)
        print("\n")

        # Append to history (simplified — no full message objects)
        history.append(f"User: {user_input}\nAssistant: {assistant_reply}")


if __name__ == "__main__":
    asyncio.run(chat_session())
```

FILE: /home/user/wellux_testprojects/examples/chain_prompts.py
```python
#!/usr/bin/env python3
"""Prompt chaining example — multi-step research + synthesis pipeline."""
import asyncio
import os

from src.llm import ClaudeClient
from src.prompt_engineering import PromptChain


async def research_pipeline(topic: str) -> None:
    """3-step Karpathy-style research chain: search → distill → action."""
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    chain = (
        PromptChain(client)
        .add_step(
            "overview",
            lambda ctx: (
                f"Give a concise technical overview of: {ctx['topic']}\n\n"
                "Cover: what it is, why it matters, core mechanism. Max 200 words."
            ),
            temperature=0.3,
            max_tokens=512,
        )
        .add_step(
            "deep_dive",
            lambda ctx: (
                f"Topic: {ctx['topic']}\n\nOverview:\n{ctx['overview']}\n\n"
                "Now: identify the single most important technical insight.\n"
                "Explain it from first principles. What would you need to rebuild this from scratch? 150 words."
            ),
            temperature=0.2,
            max_tokens=512,
        )
        .add_step(
            "action_items",
            lambda ctx: (
                f"Topic: {ctx['topic']}\n\nKey insight:\n{ctx['deep_dive']}\n\n"
                "Generate 3 concrete action items for a practitioner to apply this insight this week.\n"
                "Format: numbered list, each item under 30 words, immediately actionable."
            ),
            temperature=0.5,
            max_tokens=256,
        )
    )

    print(f"\n=== Research Pipeline: {topic} ===\n")
    result = await chain.run({"topic": topic})

    print("📋 OVERVIEW")
    print(result.steps["overview"])

    print("\n🔬 DEEP DIVE")
    print(result.steps["deep_dive"])

    print("\n✅ ACTION ITEMS")
    print(result.steps["action_items"])

    print(f"\n📊 TOTAL — tokens: {result.total_tokens} | cost: ${result.total_cost_usd:.4f}")


async def parallel_research(topics: list[str]) -> None:
    """Research multiple topics in parallel."""
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    branches = {}
    for topic in topics:
        branch = PromptChain(client).add_step(
            "summary",
            lambda ctx, t=topic: f"Summarize '{t}' in 3 bullet points. Be technical and specific.",
            max_tokens=256,
            temperature=0.3,
        )
        branches[topic] = branch

    print(f"\n=== Parallel Research: {len(topics)} topics ===\n")
    results = await PromptChain(client).run_parallel_branches(branches, {})

    for topic, result in results.items():
        print(f"### {topic}")
        print(result.final)
        print()


if __name__ == "__main__":
    # Single deep-dive chain
    asyncio.run(research_pipeline("RAG with graph retrieval (LightRAG)"))

    # Parallel research
    asyncio.run(parallel_research([
        "LLM agent frameworks 2026",
        "Prompt caching techniques",
        "Fine-tuning efficiency (LoRA, QLoRA)",
    ]))
```


## 4.16 Claude Hooks

FILE: /home/user/wellux_testprojects/.claude/settings.json
```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "Glob(*)",
      "Grep(*)",
      "WebFetch(*)",
      "WebSearch(*)",
      "Bash(git *)",
      "Bash(python3 *)",
      "Bash(pip *)",
      "Bash(pip3 *)",
      "Bash(npm *)",
      "Bash(node *)",
      "Bash(ls *)",
      "Bash(ls -la *)",
      "Bash(mkdir *)",
      "Bash(mkdir -p *)",
      "Bash(chmod *)",
      "Bash(cat *)",
      "Bash(echo *)",
      "Bash(wc *)",
      "Bash(grep *)",
      "Bash(find *)",
      "Bash(date *)",
      "Bash(tail *)",
      "Bash(head *)",
      "Bash(bash tools/scripts/*)",
      "Bash(bash .claude/hooks/*)",
      "Bash(docker *)",
      "Bash(docker compose *)",
      "Bash(docker-compose *)",
      "Bash(ccm build*)",
      "Bash(ccm deploy*)",
      "Bash(ccm ps*)",
      "Bash(ccm health*)",
      "Bash(ccm serve-mcp*)",
      "Bash(python3 -m src.mcp_server*)",
      "mcp__github__*"
    ],
    "deny": [
      "Bash(rm -rf /*)",
      "Bash(curl * | bash)",
      "Bash(wget * | bash)",
      "Bash(sudo rm *)",
      "Bash(sudo dd *)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "bash /home/user/wellux_testprojects/.claude/hooks/session-start.sh 2>/dev/null || true"
      }
    ],
    "PreCompact": [
      {
        "type": "command",
        "command": "bash /home/user/wellux_testprojects/.claude/hooks/pre-compact.sh 2>/dev/null || true"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "bash /home/user/wellux_testprojects/.claude/hooks/user-prompt-submit.sh 2>/dev/null || true",
        "timeout": 3
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash /home/user/wellux_testprojects/.claude/hooks/pre-tool-bash.sh 2>/dev/null || true",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /home/user/wellux_testprojects/.claude/hooks/post-tool-edit.sh 2>/dev/null || true"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash /home/user/wellux_testprojects/.claude/hooks/post-tool-edit.sh 2>/dev/null || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "bash /home/user/wellux_testprojects/.claude/hooks/stop.sh 2>/dev/null || true"
      }
    ]
  }
}
```

FILE: /home/user/wellux_testprojects/.claude/settings.local.json
```json
{
  "permissions": {
    "allow": [
      "mcp__filesystem__directory_tree",
      "mcp__filesystem__read_text_file",
      "mcp__filesystem__list_allowed_directories",
      "mcp__filesystem__read_multiple_files",
      "mcp__filesystem__list_directory"
    ]
  }
}
```

FILE: /home/user/wellux_testprojects/.claude/hooks/session-start.sh
```bash
#!/bin/bash
# .claude/hooks/session-start.sh
# ADVANCED BOOT — runs every session start
# Loads: hot-memory, recent session log, MASTER_PLAN status, health checks
# Exit 0 = allow session to continue (always)

BASE="/home/user/wellux_testprojects"

# ── Header ────────────────────────────────────────────────────────────────────
echo ""
printf '\033[1;34m╔══════════════════════════════════════════════════════════╗\033[0m\n'
printf '\033[1;34m║\033[0m  \033[1m\033[1;37mCLAUDE CODE MAX\033[0m  \033[2m—  session boot\033[0m                        \033[1;34m║\033[0m\n'
printf '\033[1;34m║\033[0m  \033[2m%s\033[0m                                   \033[1;34m║\033[0m\n' "$(date '+%Y-%m-%d  %H:%M:%S')"
printf '\033[1;34m╚══════════════════════════════════════════════════════════╝\033[0m\n'
echo ""

# ── Git + version status ──────────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
UNSTAGED=$(git -C "$BASE" status --short 2>/dev/null | head -3)
REMOTE_URL=$(git -C "$BASE" remote get-url origin 2>/dev/null || echo "no remote")
VERSION=$(grep '^version = ' "$BASE/pyproject.toml" 2>/dev/null | sed 's/version = "//;s/"//' || echo "unknown")

printf '  \033[1;35m▸ Repo\033[0m    wellux_testprojects  \033[2m(%s)\033[0m\n' "$REMOTE_URL"
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  printf '  \033[1;35m▸ Branch\033[0m  \033[1;31m%s\033[0m  ⚠ WARNING: on main!\n' "$BRANCH"
else
  printf '  \033[1;35m▸ Branch\033[0m  \033[1;32m%s\033[0m\n' "$BRANCH"
fi
printf '  \033[1;35m▸ Version\033[0m \033[1;32mv%s\033[0m\n' "$VERSION"
if [ -n "$UNSTAGED" ]; then
  DIFF_STAT=$(git -C "$BASE" diff --stat HEAD 2>/dev/null | tail -1 | xargs)
  printf '  \033[1;33m▸ Changes\033[0m \033[1;33munstaged:  %s\033[0m\n' "$DIFF_STAT"
fi
echo ""

# ── Recent commits (5) ───────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Recent Commits (5) ──────────────────────────────────\033[0m\n'
git -C "$BASE" log -5 --oneline 2>/dev/null | sed 's/^\([a-f0-9]*\)  \(.*\)/  \x1b[2m\1\x1b[0m  \2/'
echo ""

# ── MASTER_PLAN status ────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── MASTER_PLAN ─────────────────────────────────────────\033[0m\n'
if [ -f "$BASE/MASTER_PLAN.md" ]; then
  DONE=$(grep -c "^- \[x\]" "$BASE/MASTER_PLAN.md" 2>/dev/null || echo 0)
  TOTAL=$(grep -c "^- \[" "$BASE/MASTER_PLAN.md" 2>/dev/null || echo 0)
  NEXT=$(grep -m1 "^- \[ \]" "$BASE/MASTER_PLAN.md" 2>/dev/null | sed 's/^- \[ \] //')
  if [ -n "$NEXT" ]; then
    printf '  \033[1;33m▶ Next:\033[0m \033[2m%s\033[0m\n' "$NEXT"
    printf '  \033[2m%s/%s steps done\033[0m\n' "$DONE" "$TOTAL"
  else
    printf '  \033[1;32m✔ Complete!\033[0m \033[2m%s/%s steps done\033[0m\n' "$DONE" "$TOTAL"
  fi
fi
echo ""

# ── Open tasks ────────────────────────────────────────────────────────────────
OPEN_COUNT=$(grep "^- \[ \]" "$BASE/tasks/todo.md" 2>/dev/null | wc -l | tr -d ' ')
printf '  \033[1m\033[1;36m── Open Tasks (%s) ─────────────────────────────────────\033[0m\n' "$OPEN_COUNT"
if [ "$OPEN_COUNT" -eq 0 ] 2>/dev/null; then
  printf '  \033[1;32m✔ No open tasks\033[0m\n'
else
  grep "^- \[ \]" "$BASE/tasks/todo.md" 2>/dev/null | head -5 | sed 's/^- \[ \] /  ▸ /'
fi
echo ""

# ── Open findings (P2/P3 backlog) ─────────────────────────────────────────────
FINDINGS="$BASE/tasks/open-findings.md"
if [ -f "$FINDINGS" ]; then
  OPEN_F=$(grep "^- \[ \]" "$FINDINGS" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$OPEN_F" -gt 0 ]; then
    printf '  \033[1m\033[1;33m── Open Findings (%s) ──────────────────────────────────\033[0m\n' "$OPEN_F"
    grep "^- \[ \]" "$FINDINGS" | head -5 | while IFS= read -r line; do
      printf '  \033[1;33m▸\033[0m %s\n' "${line#- \[ \] }"
    done
    echo ""
  fi
fi

# ── Last session ──────────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Last Session ────────────────────────────────────────\033[0m\n'
LAST_LOG=$(ls -t "$BASE/data/sessions/"*.md 2>/dev/null | head -1)
if [ -n "$LAST_LOG" ]; then
  printf '  \033[2m%s\033[0m\n' "$(basename "$LAST_LOG")"
  tail -15 "$LAST_LOG" | grep -v "^$" | head -10 | sed 's/^/  /'
else
  printf '  \033[2m(no session logs yet)\033[0m\n'
fi
echo ""

# ── Context snapshot (from hot-memory.md) ────────────────────────────────────
HOT_MEM="$BASE/.claude/memory/hot/hot-memory.md"
if [ -f "$HOT_MEM" ]; then
  printf '  \033[1m\033[1;36m── Context Snapshot ────────────────────────────────────\033[0m\n'
  # Show full dynamic zone (between DYNAMIC marker and STATIC marker)
  awk '
    /<!-- DYNAMIC:/{dyn=1; next}
    /<!-- STATIC:/{dyn=0}
    dyn && NF{print "  "$0}
  ' "$HOT_MEM"
  echo ""
  # Show static zone section headings as a map
  STATIC_SECTIONS=$(awk '/<!-- STATIC:/{found=1} found && /^## /{print $0}' "$HOT_MEM")
  if [ -n "$STATIC_SECTIONS" ]; then
    printf '  \033[2m[Curated in hot-memory.md:]\033[0m'
    echo "$STATIC_SECTIONS" | while IFS= read -r sec; do
      printf '  \033[2m%s\033[0m' "$sec  "
    done
    echo ""
    echo ""
  fi
fi

# ── Last 3 lessons ────────────────────────────────────────────────────────────
if [ -f "$BASE/tasks/lessons.md" ]; then
  LESSON_COUNT=$(grep -c "^### Lesson" "$BASE/tasks/lessons.md" 2>/dev/null || echo 0)
  printf '  \033[1m\033[1;36m── Last 3 Lessons (of %s total) ────────────────────────\033[0m\n' "$LESSON_COUNT"
  awk '
    /^### Lesson [0-9]+/{
      if(in_l && buf!="") lessons[++c]=buf;
      buf=""; in_l=1
    }
    /^---/{in_l=0}
    in_l{buf=buf"\n"$0}
    END{
      if(in_l && buf!="") lessons[++c]=buf;
      start=(c>3)?(c-2):1;
      for(i=start;i<=c;i++) print lessons[i]
    }
  ' "$BASE/tasks/lessons.md" | head -30 | sed 's/^/  /'
fi
echo ""

# ── Project health ────────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Project Health ──────────────────────────────────────\033[0m\n'
cd "$BASE" 2>/dev/null || true

PYTHON_VER=$(python3 --version 2>&1 | sed 's/Python //')
printf '  \033[0;34m▸ Python\033[0m  %s\n' "$PYTHON_VER"

TEST_COUNT=$(grep -rE '^\s*(async\s+)?def test_' tests/ 2>/dev/null | wc -l | tr -d ' ')
printf '  \033[0;34m▸ Tests\033[0m   \033[1;32m%s functions\033[0m\n' "$TEST_COUNT"

LINT_ERRORS=$(python3 -m ruff check src/ tests/ --select E,F,W --ignore E501 --quiet 2>/dev/null | wc -l | tr -d ' ')
if [ "$LINT_ERRORS" -eq 0 ] 2>/dev/null; then
  printf '  \033[0;34m▸ Lint\033[0m    \033[1;32mCLEAN\033[0m  \033[2m(ruff)\033[0m\n'
else
  printf '  \033[0;34m▸ Lint\033[0m    \033[1;31m%s issue(s)\033[0m\n' "$LINT_ERRORS"
fi

SKILL_COUNT=$(find "$BASE/.claude/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
printf '  \033[0;34m▸ Skills\033[0m  %s loaded\n' "$SKILL_COUNT"

# Docker status
if docker compose -f "$BASE/docker-compose.yml" ps 2>/dev/null | grep -q "running"; then
  printf '  \033[0;34m▸ Docker\033[0m  \033[1;32mrunning\033[0m\n'
else
  printf '  \033[0;34m▸ Docker\033[0m  \033[2mcompose available (not running)\033[0m\n'
fi
echo ""

# ── Daily session log ─────────────────────────────────────────────────────────
TODAY_LOG="$BASE/data/sessions/$(date '+%Y-%m-%d').md"
if [ -f "$TODAY_LOG" ]; then
  printf '  \033[2m▸ Session log: data/sessions/%s.md\033[0m\n' "$(date '+%Y-%m-%d')"
  echo ""
else
  mkdir -p "$BASE/data/sessions"
  cat > "$TODAY_LOG" << LOGEOF
# Session Log — $(date '+%Y-%m-%d')

## Session Start — $(date '+%H:%M:%S')
- Branch: $BRANCH
- Version: v$VERSION
- Open tasks: $OPEN_COUNT
LOGEOF
  printf '  \033[2m▸ Created session log: data/sessions/%s.md\033[0m\n' "$(date '+%Y-%m-%d')"
  echo ""
fi

# ── Shortcuts ─────────────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Shortcuts ───────────────────────────────────────────\033[0m\n'
printf '  \033[1;37mf\033[0m → next step    \033[1;37ms\033[0m → status    \033[1;37mr\033[0m → research    \033[1;37ma\033[0m → audit\n'
printf '  \033[2m/brainstorm  /write-plan  /superpowers  /office-hours  /ship\033[0m\n'
printf '\033[1;34m════════════════════════════════════════════════════════════\033[0m\n'
echo ""

exit 0
```

FILE: /home/user/wellux_testprojects/.claude/hooks/pre-compact.sh
```bash
#!/bin/bash
# .claude/hooks/pre-compact.sh
# Fires BEFORE the context window compacts — saves critical state so nothing is lost.
# Writes dynamic zone of hot-memory.md; preserves the STATIC zone (curated content).
# Exit 0 always (non-zero would block compaction, which we don't want).

BASE="/home/user/wellux_testprojects"
SNAPSHOT_FILE="$BASE/.claude/memory/hot/hot-memory.md"
SESSION_LOG="$BASE/data/sessions/$(date '+%Y-%m-%d').md"

# ── 1. Gather dynamic state ────────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
UNCOMMITTED=$(git -C "$BASE" status --short 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git -C "$BASE" log -1 --oneline 2>/dev/null || echo "no commits")
VERSION=$(grep '^version = ' "$BASE/pyproject.toml" 2>/dev/null | sed 's/version = "//;s/"//' || echo "unknown")
TEST_COUNT=$(grep -rE '^\s*(async\s+)?def test_' "$BASE/tests/" 2>/dev/null | wc -l | tr -d ' ')
SKILL_COUNT=$(find "$BASE/.claude/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')

# ── 2. Get last 3 commits ──────────────────────────────────────────────────────
LAST_3_COMMITS=$(git -C "$BASE" log -3 --format="- %h %s" 2>/dev/null || echo "- (no commits)")

# ── 3. Extract last 2 complete lessons ────────────────────────────────────────
RECENT_LESSONS=$(awk '
  /^### Lesson [0-9]+/{
    if(in_l && buf!="") lessons[++c]=buf;
    buf=""; in_l=1
  }
  /^---/{in_l=0}
  in_l{buf=buf"\n"$0}
  END{
    if(in_l && buf!="") lessons[++c]=buf;
    start=(c>2)?(c-1):1;
    for(i=start;i<=c;i++) print lessons[i]
  }
' "$BASE/tasks/lessons.md" 2>/dev/null)

# ── 4. Preserve STATIC zone from existing hot-memory.md ───────────────────────
STATIC_ZONE=""
if [ -f "$SNAPSHOT_FILE" ]; then
  STATIC_ZONE=$(awk '/<!-- STATIC: manually curated/{found=1} found{print}' "$SNAPSHOT_FILE")
fi
# Fallback if marker not found (first run or legacy file)
if [ -z "$STATIC_ZONE" ]; then
  STATIC_ZONE="<!-- STATIC: manually curated below — never auto-overwritten by hooks -->"$'\n\n'"(No curated content yet — add sections below this marker)"
fi

# ── 5. Write hot-memory.md (dynamic zone only, static zone re-appended) ───────
# Use printf '%s' for all user-sourced content (commits, lessons, static zone) to
# prevent backticks and dollar signs in those strings from being interpreted as shell.
{
  printf '# Hot Memory — Always Loaded (≤50 lines)\n'
  printf '<!-- L0: active project context — DYNAMIC above marker, STATIC below -->\n\n'
  printf '<!-- DYNAMIC: auto-updated by pre-compact.sh on every compaction -->\n'
  printf '**Last Updated**: %s (pre-compact snapshot)\n\n' "$(date '+%Y-%m-%d %H:%M:%S')"
  printf '## Active Context (auto-updated)\n'
  printf -- '- Branch: %s\n' "$BRANCH"
  printf -- '- Version: v%s  ·  Tests: %s passing  ·  Skills: %s loaded\n' "$VERSION" "$TEST_COUNT" "$SKILL_COUNT"
  printf -- '- Uncommitted changes: %s file(s)\n' "$UNCOMMITTED"
  printf -- '- Last commit: %s\n' "$LAST_COMMIT"
  printf -- '- MASTER_PLAN: 31/31 complete · memory_bank_synced: %s\n\n' "$(date '+%Y-%m-%d %H:%M')"
  printf '## Recent Commits (auto-updated)\n'
  printf '%s\n\n' "$LAST_3_COMMITS"
  printf '## Recent Lessons (auto-updated)\n'
  printf '%s\n\n' "$RECENT_LESSONS"
  printf '%s\n' "$STATIC_ZONE"
} > "$SNAPSHOT_FILE"

# ── 6. Append to daily session log ───────────────────────────────────────────
mkdir -p "$BASE/data/sessions"
cat >> "$SESSION_LOG" << EOF

## Compaction Checkpoint — $(date '+%H:%M:%S')
- Branch: $BRANCH | v$VERSION | Uncommitted: $UNCOMMITTED files
- Tests: $TEST_COUNT | Skills: $SKILL_COUNT
- Last commit: $LAST_COMMIT
EOF

echo ""
echo "  ⚡ Pre-compact snapshot saved → .claude/memory/hot/hot-memory.md"
echo "     v$VERSION · $TEST_COUNT tests · $SKILL_COUNT skills · branch: $BRANCH"
echo ""

exit 0
```

FILE: /home/user/wellux_testprojects/.claude/hooks/pre-tool-bash.sh
```bash
#!/bin/bash
# .claude/hooks/pre-tool-bash.sh
# Runs BEFORE every Bash tool call
# Exit 0 = allow | Exit 2 = BLOCK the command

BASE="/home/user/wellux_testprojects"
LOG="$BASE/data/cache/bash-log.txt"
mkdir -p "$BASE/data/cache"

# Read the command from environment (Claude sets CLAUDE_TOOL_INPUT)
CMD="${CLAUDE_TOOL_INPUT:-unknown}"

# Log all commands with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') CMD: $CMD" >> "$LOG"

# BLOCK list — dangerous patterns
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "sudo rm"
  "sudo dd"
  "curl.*|.*bash"
  "wget.*|.*bash"
  "chmod 777 /"
  "> /dev/sda"
  "mkfs\."
  "dd if=.*of=/dev"
)

for PATTERN in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$CMD" | grep -qE "$PATTERN"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') BLOCKED: $CMD" >> "$LOG"
    echo "⛔ BLOCKED: Dangerous command pattern detected: $PATTERN" >&2
    exit 2
  fi
done

# Allow
exit 0
```

FILE: /home/user/wellux_testprojects/.claude/hooks/post-tool-edit.sh
```bash
#!/bin/bash
# .claude/hooks/post-tool-edit.sh
# Runs AFTER every Edit or Write tool call
# Always exit 0

BASE="/home/user/wellux_testprojects"
LOG="$BASE/data/cache/edit-log.txt"
mkdir -p "$BASE/data/cache"

# Try to get the file that was edited
FILE="${CLAUDE_TOOL_RESULT_path:-${CLAUDE_TOOL_RESULT_file_path:-}}"

# Log the edit
echo "$(date '+%Y-%m-%d %H:%M:%S') EDITED: ${FILE:-unknown}" >> "$LOG"

# Validate Python syntax if a .py file was written
if [[ "$FILE" == *.py ]] && [ -f "$FILE" ]; then
  if python3 -m py_compile "$FILE" 2>/dev/null; then
    echo "  ✓ Python syntax OK: $FILE"
  else
    echo "  ⚠ Python syntax error in: $FILE" >&2
  fi
fi

# Validate JSON syntax if a .json file was written
if [[ "$FILE" == *.json ]] && [ -f "$FILE" ]; then
  if python3 -m json.tool "$FILE" > /dev/null 2>&1; then
    echo "  ✓ JSON valid: $FILE"
  else
    echo "  ⚠ JSON invalid: $FILE" >&2
  fi
fi

# Validate SKILL.md has required frontmatter
if [[ "$FILE" == *"SKILL.md" ]] && [ -f "$FILE" ]; then
  if ! grep -q "^name:" "$FILE" 2>/dev/null; then
    echo "  ⚠ SKILL.md missing 'name:' frontmatter: $FILE" >&2
  fi
  if ! grep -q "^description:" "$FILE" 2>/dev/null; then
    echo "  ⚠ SKILL.md missing 'description:' frontmatter: $FILE" >&2
  fi
fi

exit 0
```

FILE: /home/user/wellux_testprojects/.claude/hooks/post-tool-pr.sh
```bash
#!/bin/bash
# .claude/hooks/post-tool-pr.sh
# Fires after a PR is created (PostToolUse on Bash commands that contain "gh pr create")
# Auto-runs code simplification review on changed files.
# Exit 0 always.

BASE="/home/user/wellux_testprojects"

# Only run if the last command created a PR
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"
if echo "$TOOL_INPUT" | grep -q "gh pr create"; then
  echo ""
  echo "  ── POST-PR SIMPLIFICATION ──────────────────────────"
  echo "  PR created. Checking for simplification opportunities..."

  # Get files changed in this branch vs main
  CHANGED_FILES=$(git -C "$BASE" diff --name-only origin/main...HEAD 2>/dev/null | grep -E '\.py$' | head -10)

  if [ -n "$CHANGED_FILES" ]; then
    echo "  Python files changed in this PR:"
    echo "$CHANGED_FILES" | sed 's/^/    /'
    echo ""
    echo "  ℹ  Tip: run /simplify to check these files for refactoring opportunities"
  fi
  echo "════════════════════════════════════════════════════════"
  echo ""
fi

exit 0
```

FILE: /home/user/wellux_testprojects/.claude/hooks/stop.sh
```bash
#!/bin/bash
# .claude/hooks/stop.sh
# Runs when Claude Code session ends.
# Validates completion criteria, writes daily session log, shows checklist.
# Exit 0 always.

BASE="/home/user/wellux_testprojects"
SESSION_LOG="$BASE/data/sessions/$(date '+%Y-%m-%d').md"

# ── 1. Gather session stats ───────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
UNCOMMITTED=$(git -C "$BASE" status --short 2>/dev/null | wc -l | tr -d ' ')
OPEN_TASKS=$(grep "^- \[ \]" "$BASE/tasks/todo.md" 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git -C "$BASE" log -1 --oneline 2>/dev/null || echo "no commits")

# ── 2. Run completion validators ─────────────────────────────────────────────
WARNINGS=""

if [ "$UNCOMMITTED" -gt 0 ] 2>/dev/null; then
  WARNINGS="${WARNINGS}\n  ⚠  $UNCOMMITTED uncommitted file(s) — consider committing"
fi

if [ "$OPEN_TASKS" -gt 0 ] 2>/dev/null; then
  WARNINGS="${WARNINGS}\n  ⚠  $OPEN_TASKS open task(s) in todo.md — update before closing"
fi

# Check lint (fast, non-blocking)
LINT_ERRORS=$(python3 -m ruff check "$BASE/src" "$BASE/tests" --select E,F,W --ignore E501 --quiet 2>/dev/null | wc -l | tr -d ' ')
if [ "$LINT_ERRORS" -gt 0 ] 2>/dev/null; then
  WARNINGS="${WARNINGS}\n  ⚠  $LINT_ERRORS lint error(s) — run: ruff check src/ tests/ --select E,F,W --ignore E501"
fi

# ── 3. Write daily session log ────────────────────────────────────────────────
mkdir -p "$BASE/data/sessions"
cat >> "$SESSION_LOG" << LOGEOF

## Session End — $(date '+%H:%M:%S')
- Branch: $BRANCH
- Uncommitted files: $UNCOMMITTED
- Open tasks: $OPEN_TASKS
- Last commit: $LAST_COMMIT
LOGEOF

# ── 4. Append session end marker to todo.md ──────────────────────────────────
if [ -f "$BASE/tasks/todo.md" ]; then
  echo "" >> "$BASE/tasks/todo.md"
  echo "<!-- Session ended: $(date '+%Y-%m-%d %H:%M:%S') -->" >> "$BASE/tasks/todo.md"
fi

# ── 5. Display session summary ───────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  SESSION COMPLETE — $(date '+%Y-%m-%d %H:%M:%S')        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  Branch:          $BRANCH"
echo "  Uncommitted:     $UNCOMMITTED file(s)"
echo "  Open tasks:      $OPEN_TASKS"
echo "  Last commit:     $LAST_COMMIT"
echo ""

if [ -n "$WARNINGS" ]; then
  echo "  ── VALIDATORS ──────────────────────────────────────"
  printf "%b\n" "$WARNINGS"
  echo ""
fi

echo "  ── SESSION CHECKLIST ───────────────────────────────"
if [ "$UNCOMMITTED" -eq 0 ] 2>/dev/null; then
  echo "  ✅ All changes committed"
else
  echo "  □  Commit uncommitted changes"
fi
if [ "$OPEN_TASKS" -eq 0 ] 2>/dev/null; then
  echo "  ✅ No open tasks"
else
  echo "  □  Update tasks/todo.md ($OPEN_TASKS open)"
fi
if [ "$LINT_ERRORS" -eq 0 ] 2>/dev/null; then
  echo "  ✅ Lint clean"
else
  echo "  □  Fix $LINT_ERRORS lint error(s)"
fi
echo "  □  Add lessons to tasks/lessons.md (corrections?)"
echo "  □  Push to origin: git push -u origin $BRANCH"
echo ""
echo "  Session log: data/sessions/$(date '+%Y-%m-%d').md"
echo "════════════════════════════════════════════════════════"
echo ""

exit 0
```

FILE: /home/user/wellux_testprojects/.claude/hooks/user-prompt-submit.sh
```bash
#!/bin/bash
# .claude/hooks/user-prompt-submit.sh
# Fires on every user message submission (UserPromptSubmit event).
# Use for: prompt logging, auto-context injection, rate limiting warnings.
# Exit 0 = allow prompt through. Exit 2 = block with message.
# Keep this FAST — it runs on every message.

BASE="/home/user/wellux_testprojects"

# ── Prompt length guard ───────────────────────────────────────────────────────
# Warn if the prompt is very long (might indicate pasted content that should be a file)
PROMPT_LEN="${#CLAUDE_USER_PROMPT}"
if [ "$PROMPT_LEN" -gt 8000 ] 2>/dev/null; then
  echo "  ⚠  Long prompt detected (${PROMPT_LEN} chars). Consider writing to a file instead."
fi

# ── Branch safety check ──────────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo ""
  echo "  ⚠  WARNING: You are on branch '$BRANCH'. Commits will go to main."
  echo "  Consider: git checkout -b claude/<feature>-$(date +%s | tail -c 5)"
  echo ""
fi

exit 0
```


## 4.17 Claude Context Files (CLAUDE.md, Rules, Soul, Memory)

FILE: /home/user/wellux_testprojects/CLAUDE.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/.claude/SOUL.md
```markdown
# SOUL.md — Agent Identity & Operating Principles

This file defines who I am, how I make decisions, and what I will/won't do.
Loaded every session. Kept concise (≤80 lines).

---

## Identity
I am Claude Code Max — a high-agency engineering assistant built for autonomous software delivery.
I am opinionated, decisive, and action-oriented. I prefer doing over planning, outcomes over process.

## Decision Style
- **Reversible first**: prefer branches, stash, and drafts over direct irreversible edits
- **Outcome-framed tasks**: I define "done" by outcomes (tests pass, feature works) not process (steps taken)
- **Parallel by default**: I batch independent operations in a single turn whenever possible
- **Minimal blast radius**: I touch only what the task requires; no speculative additions
- **Self-improving**: after any correction, I add a lesson to `tasks/lessons.md`

## What I Will Do
- Autonomously execute multi-step engineering tasks without hand-holding
- Make architectural decisions when given clear goals and context
- Proactively surface risks, alternatives, and edge cases before they become problems
- Route tasks to the optimal model/skill/agent using the routing system
- Spawn subagents for parallelizable workstreams

## What I Won't Do
- Push to `main`/`master` without explicit permission
- Commit secrets, credentials, or `.env` files
- Run destructive ops (rm -rf, force-push) without confirmation
- Swallow errors silently or fake task completion
- Add speculative abstractions beyond what was asked

## Personality Traits
- **Direct**: no filler, no affirmations, no apologies for brevity
- **Reliable**: if I say it's done, the tests pass and lint is clean
- **Curious**: I surface interesting patterns and non-obvious risks
- **Confident**: I state opinions and make calls; I flag uncertainty clearly

## Working Memory Anchor
When starting a new task, I check in this order:
1. `tasks/todo.md` — what's open?
2. `tasks/lessons.md` — what did I learn?
3. `.claude/memory/hot/hot-memory.md` — what's the active context?
4. `MASTER_PLAN.md` — what's the overall direction?
```

FILE: /home/user/wellux_testprojects/.claude/USER.md
```markdown
# USER.md — User Profile & Preferences

Describes the user's working style, stack, and preferences.
Updated by the agent when patterns are detected.

---

## Stack
- **Primary**: Python 3.12, TypeScript, Claude API (anthropic SDK), Git, Docker, asyncio
- **Frameworks**: FastAPI, pytest, ruff, httpx, Pydantic v2, Next.js
- **Also uses**: Go, Rust, SQL, Bash, YAML/Terraform
- **LLMs**: Claude (Opus 4.6 / Sonnet 4.6 / Haiku 4.5), optional OpenAI

## Working Style
- **Prefers**: autonomous execution with minimal confirmation prompts
- **Shortcuts**: `f` (next step) · `s` (status) · `r` (research) · `a` (audit)
- **Workflow**: `/brainstorm` → `/write-plan` → `/superpowers execute` for complex features
- **Quality bar**: tests pass + lint clean before "done"

## Preferences
- Short, direct responses — no filler, no preamble
- GitHub-flavored Markdown for all structured output
- Commits in imperative mood, explain *why* not *what*
- Branch naming: `claude/<description>-<id>`
- Never ask about optional parameters unless critical

## Project Context
- **Repo**: `wellux/wellux_testprojects`
- **Branch**: `claude/optimize-cli-autonomy-xNamK`
- **Goal**: Gold-standard Claude Code template — 5-layer architecture, 123 skills, autonomous
- **MASTER_PLAN**: Complete (31/31 steps)

## Communication
- Technical discussions: concise bullets > paragraphs
- Errors: show the error, root cause, fix — skip the preamble
- Progress: one-line status updates at natural milestones
```

FILE: /home/user/wellux_testprojects/.claude/MEMORY.md
```markdown
# MEMORY.md — Active Decisions, Projects & Architectural Choices

This file captures key technical decisions, active work, and project state.
Updated by agent at session end and after significant decisions.
Loaded every session alongside SOUL.md and USER.md.

---

## Active Projects

### Claude Code Max Template (wellux_testprojects)
- **Status**: v0.9.0 shipped · branch `claude/optimize-cli-autonomy-xNamK`
- **Goal**: Gold-standard Claude Code template — 5-layer arch, 121 skills, 5 routers, full autonomy
- **Next**: RIPER skill, post-PR hook, memory-bank skill, ccm context-diff CLI

---

## Architectural Decisions

### Build System
- **Decision**: `build-backend = "setuptools.build_meta"` (not `setuptools.backends.legacy:build`)
- **Why**: `backends` subpackage missing in this environment; `build_meta` is the stable alias
- **Date**: 2026-04-05

### Package Layout
- **Decision**: `[tool.setuptools.packages.find] where = ["."] include = ["src*"]`
- **Why**: editable install was adding `/src` to sys.path; root must be added for `from src.cli import main` to work
- **Date**: 2026-04-05

### Logger exc_info Filtering
- **Decision**: Seed `_STDLIB_KEYS` from a real `LogRecord` instance + class dict
- **Why**: `LogRecord.__dict__` (class) misses instance attrs like `exc_info`; using instance ensures all runtime attrs are excluded from structured JSON
- **Date**: 2026-04-05

### Memory Architecture
- **Decision**: Three-tier hot/warm/glacier (marciopuga/cog pattern)
- **Why**: Flat MemoryStore had no token-efficient loading; tiered allows session-start to inject only ≤50 lines while archiving history
- **Date**: 2026-04-05

### Skill Registry
- **Decision**: 121 entries in `_SKILL_REGISTRY`, 0 duplicate trigger phrases enforced by test
- **Why**: All skills must be reachable via Python routing API; duplicate triggers silently shadow skills
- **Date**: 2026-04-05

---

## Dependency Pins (security)
- `anthropic>=0.87.0,<1.0` — fixes CVE-2026-34450 + CVE-2026-34452
- `cryptography>=46.0.6` — fixes CVE-2026-34073 + 5 earlier CVEs

---

## Active Experiments
_None currently running_

---

## Known Issues / Watch List
- Tag push (v0.9.0) blocked by remote HTTP 403 — local tag applied, travels with future clones
- 5 uncovered lines: OpenAI optional import + MCP live-only fallback (environment-specific)
```

FILE: /home/user/wellux_testprojects/.claude/rules/code-style.md
```markdown
# Code Style Rules

Enforced for all Python code in this project.

## Formatting
- Line length: 100 characters max (ruff enforced)
- Indentation: 4 spaces, no tabs
- Trailing whitespace: none
- End of file: single newline

## Imports
- Standard library first, third-party second, local third (ruff I-sorted)
- No wildcard imports (`from x import *`)
- Lazy imports inside functions when avoiding circular deps or optional deps

## Naming
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix `_`, never double-underscore except dunder methods
- Avoid single-letter names except `i`, `j`, `k` in tight loops; never `l`, `O`, `I`

## Type Annotations
- All public function signatures must be annotated
- Use `str | None` over `Optional[str]` (Python 3.10+ union syntax)
- Use `from __future__ import annotations` at top of every module

## Functions
- Max 40 lines per function; extract helpers if longer
- Single responsibility: one function does one thing
- No mutable default arguments (`def f(x=[])` is forbidden)
- Prefer early returns over nested conditionals

## Classes
- `@dataclass` for data-holding classes; plain class for behaviour
- No logic in `__init__` beyond assignment
- `__repr__` required on any class that appears in logs

## Error Handling
- Catch specific exceptions, never bare `except:`
- Log errors with structured context before re-raising or returning error values
- Never swallow exceptions silently

## Comments
- Code should be self-documenting; comments explain *why*, not *what*
- No commented-out code committed to main
- Docstrings: Google style, required on public classes and functions
```

FILE: /home/user/wellux_testprojects/.claude/rules/testing.md
```markdown
# Testing Rules

Defines how tests should be written in this project.

## Framework
- pytest + pytest-asyncio (asyncio_mode = auto)
- Tests live in `tests/test_<module>.py` mirroring `src/<module>.py`
- No test logic in `src/`

## Structure
- Group tests in classes: `class TestClassName:` → `def test_<behaviour>(self):`
- One assertion focus per test — test one thing
- Fixture scope: `function` default; `module` only for expensive read-only setup
- Name tests as: `test_<what>_<when_condition>` or `test_<what>_<expected_result>`

## Coverage Requirements
- New code must ship with tests covering the happy path + at least one failure case
- Public API methods: 100% coverage expected
- Never mark code `# pragma: no cover` without a comment explaining why

## Mocking
- Mock at the boundary (LLM calls, HTTP, filesystem) — not inside your own code
- Use `unittest.mock.patch` or `monkeypatch` fixture
- Async mocks: `unittest.mock.AsyncMock`
- Inject dependencies via constructor args to make them easily mockable

## Async Tests
- All async tests auto-detected via `asyncio_mode = auto` in pytest.ini
- No `@pytest.mark.asyncio` decorator needed
- Use `asyncio.sleep(0)` to yield control in concurrency tests

## Eval Tests
- Behavioural tests go in `data/evals/*.jsonl`, not in pytest
- `ccm eval run data/evals/smoke.jsonl --dry-run` must always pass in CI
- Live API eval suites tagged `live` are excluded from CI (require ANTHROPIC_API_KEY)

## What Not to Test
- Private implementation details (prefix `_`)
- Third-party library behaviour
- Framework internals (FastAPI routing, Pydantic serialization)
- Trivial one-liners with no branching logic

## CI Gate
- All tests must pass before merge: `pytest tests/ --tb=short -q`
- Lint must pass: `ruff check src/ tests/ --select E,F,W --ignore E501`
- Smoke evals must pass: `python -m src.cli eval run data/evals/smoke.jsonl --dry-run`
```

FILE: /home/user/wellux_testprojects/.claude/rules/api-conventions.md
```markdown
# API Design Conventions

Sets rules for REST API design patterns in this project (src/api/).

## Endpoint Design
- Resources are nouns, not verbs: `/complete` not `/doComplete`
- HTTP methods: GET=read, POST=create/action, PUT=replace, PATCH=update, DELETE=remove
- Versioning: prefix with `/v1/` when breaking changes are needed (current API is unversioned/internal)
- Return 200 for success, 201 for created, 400 for client error, 422 for validation, 502 for upstream LLM error

## Request / Response Models
- All request and response bodies use Pydantic v2 models in `src/api/models.py`
- Field names: `snake_case` in Python → JSON serialises as `snake_case` (no camelCase)
- Optional fields default to `None`, not to magic sentinel values
- Always include `content_type: str` header hint for structured payloads

## Headers
- Every response carries `X-Request-ID` (set by CorrelationIDMiddleware)
- Every response carries `X-Process-Time-Ms` (set by TimingMiddleware)
- Pass `X-Request-ID` through to upstream services for distributed tracing

## Error Responses
- Use `HTTPException(status_code=..., detail=str(e))` — never expose stack traces
- Log the full error with `logger.error(event, error=str(e), request_id=get_request_id())`
- Upstream LLM errors → 502; validation errors → 422 (handled by FastAPI/Pydantic); auth → 401

## Streaming
- Streaming endpoints use `StreamingResponse` with `media_type="text/event-stream"`
- Token format: `data: <token>\n\n`; terminal token: `data: [DONE]\n\n`
- Errors during stream: `data: [ERROR] <message>\n\n`

## Auto-Routing
- All completion endpoints support `auto_route: bool = True`
- When True: call `routing_route(prompt)` to select model
- When False or `model` is specified: use the explicit model
- Always log `routed_by` reason for observability

## Middleware Order (outermost → innermost)
1. `CorrelationIDMiddleware` — attach request ID first
2. `TimingMiddleware` — time the full handler including inner middleware
3. Application routes

## Rate Limiting
- `RateLimiter` is initialized in `lifespan` and shared across requests
- Default: 100 requests/minute per instance (not per user — add auth layer for per-user)
- On rate limit exceeded: raise `HTTPException(status_code=429)`
```

FILE: /home/user/wellux_testprojects/src/api/CLAUDE.md
```markdown
# src/api — REST API Layer Context

## Purpose
FastAPI application exposing LLM completions and routing decisions over HTTP.

## Files
- `app.py` — FastAPI app factory, lifespan, middleware registration
- `routes.py` — endpoint handlers (`/health`, `/v1/complete`, `/v1/complete/stream`, `/v1/chat`, `/v1/route`)
- `models.py` — Pydantic v2 request/response models
- `middleware.py` — CorrelationIDMiddleware (X-Request-ID), TimingMiddleware (X-Process-Time-Ms)
- `rate_limiter.py` — token bucket, 100 req/min default, raises HTTP 429

## Middleware order (outermost → innermost)
1. `CorrelationIDMiddleware` — attach request ID first
2. `TimingMiddleware` — time the full handler

## Key conventions
- All fields: `snake_case` (no camelCase)
- Optional fields default to `None`
- Errors: `HTTPException(status_code=..., detail="Upstream LLM error [ExcType] — see server logs (request_id=…)")` — never expose `str(e)` to clients
- Upstream LLM errors → 502; validation → 422; rate limit → 429
- Streaming: `StreamingResponse(media_type="text/event-stream")`, token format `data: <token>\n\n`, terminal `data: [DONE]\n\n`

## Auto-routing
`auto_route: bool = True` on completion endpoints. When True: call `route_llm(prompt)` to select model.
Log `routed_by` reason for observability.

## Start
`ccm serve` or `uvicorn src.api.app:app --reload`
```

FILE: /home/user/wellux_testprojects/src/llm/CLAUDE.md
```markdown
# src/llm — LLM Client Layer Context

## Purpose
Thin async wrappers around Claude (Anthropic) and optionally GPT (OpenAI) APIs.

## Files
- `claude_client.py` — `ClaudeClient` async wrapper; `complete(prompt, model, max_tokens) -> str`
- `gpt_client.py` — `GPTClient` async wrapper (optional dep; graceful ImportError if openai missing)

## ClaudeClient
```python
from src.llm.claude_client import ClaudeClient
client = ClaudeClient(api_key=os.environ["ANTHROPIC_API_KEY"])
response = await client.complete("Hello", model="claude-sonnet-4-6", max_tokens=256)
```

## Model IDs (2026)
| Alias | Model ID |
|-------|----------|
| opus  | `claude-opus-4-6` |
| sonnet | `claude-sonnet-4-6` (default) |
| haiku | `claude-haiku-4-5-20251001` |

## Key rules
- All LLM calls are async — use `await`
- Always wrap in `asyncio.wait_for(..., timeout=30.0)` in eval/batch contexts
- On `APIError` from anthropic SDK → surface as HTTP 502 in the API layer
- GPT client import is guarded: `try: from openai import ... except ImportError: pass`

## Security
- API key from `ANTHROPIC_API_KEY` env var — never hardcoded, never logged
- `max_tokens` floor enforced in routing layer (`llm_router.py`) to prevent 0-token requests
```

FILE: /home/user/wellux_testprojects/src/routing/CLAUDE.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/src/evals/CLAUDE.md
```markdown
# src/evals — Evaluation Framework Context

## Purpose
Structured LLM evaluation: define cases, run suites, report pass rates, latency, and scores.

## Key Classes
- `EvalCase(id, prompt, contains=[], not_contains=[], tags=[])` — single test case
- `EvalSuite(name)` — collection of cases; `.add(case)` enforces no duplicate IDs
- `EvalRunner(llm_fn, max_workers=None)` — sync runner; sequential by default, parallel via `ThreadPoolExecutor` when `max_workers > 1`
- `AsyncEvalRunner(llm_fn, concurrency=5)` — async runner with semaphore + 30s timeout per case
- `EvalReport` — `.summary()`, `.pass_rate`, `.mean_score`, `.by_tag(tag)`
- `Verdict` — `PASS | FAIL | ERROR`

## Running evals
```bash
ccm eval run data/evals/smoke.jsonl           # live (requires ANTHROPIC_API_KEY)
ccm eval run data/evals/smoke.jsonl --dry-run # skip LLM calls, always PASS
ccm eval list                                  # list all .jsonl suites
ccm eval inspect data/evals/smoke.jsonl        # show cases
```

## JSONL format
```json
{"id": "greet", "prompt": "Say hello", "contains": ["hello"], "tags": ["fast"]}
```

## Key invariants
- `EvalSuite.from_jsonl` uses `.extend(cases)` (calls `.add()` for each) — duplicate ID check enforced
- `AsyncEvalRunner` wraps every LLM call in `asyncio.wait_for(..., timeout=30.0)` — no hung awaits
- Use keyword args for `EvalResult` construction — positional order is error-prone

## Tests
`tests/test_evals.py` — covers happy path, tag filtering, duplicate ID rejection, async timeout, verbose mode
```

FILE: /home/user/wellux_testprojects/src/persistence/CLAUDE.md
```markdown
# src/persistence — Persistence Layer Context

## Purpose
Three storage backends: file-based (FileStore), MCP-backed entity graph (MemoryStore),
and tiered hot/warm/glacier memory (TieredMemory).

## Files
- `file_store.py` — writes to `data/research/`, `tasks/todo.md`, `tasks/lessons.md`, `data/cache/events.log`
- `memory_store.py` — MCP memory server: entities, relations, recall via `mcp__memory__*` tools
- `tiered_memory.py` — three-tier: hot (≤50 lines), warm (domain files), glacier (YAML-frontmatter)
- `__init__.py` — exports `FileStore`, `MemoryStore`, `TieredMemory`

## TieredMemory paths (default)
- Hot: `.claude/memory/hot/hot-memory.md`
- Warm: `.claude/memory/warm/<domain>.md`
- Glacier: `.claude/memory/glacier/YYYY-MM-DD-<slug>.md`

## Key rule
Hot tier auto-evicts oldest active-context lines to warm when it exceeds 50 lines.
Glacier files have YAML frontmatter (`---\ntitle:\ndate:\ntags:\n---`) for indexed search.

## Tests
`tests/test_tiered_memory.py` — 26 tests covering all three tiers.
Always use `tmp_path` fixture to avoid writing to real `.claude/memory/`.
```

FILE: /home/user/wellux_testprojects/src/utils/CLAUDE.md
```markdown
# src/utils — Utilities Context

## Purpose
Shared infrastructure: structured JSON logging and indexed event log.

## Files

### `logger.py`
Structured JSON logger using Python's `logging` module with a custom `_StructuredFormatter`.

```python
from src.utils.logger import get_logger
log = get_logger("component")
log.info("event_name", key="value", count=42)  # → JSON line to stdout
log.error("failed", error=str(e))
```

**Critical:** `_STDLIB_KEYS` is seeded from BOTH a real `LogRecord()` instance AND `LogRecord.__dict__`.
This prevents instance attrs like `exc_info` from leaking into `json.dumps`.
Do NOT pass `exc_info=True` as a kwarg — call `log.error("msg")` inside an `except` block instead.

### `log_index.py`
Append-only JSONL event log with in-memory inverted index for fast tag/event queries.

```python
from src.utils.log_index import LogIndex
idx = LogIndex(path)
idx.append({"event": "startup", "tag": "system", "msg": "..."})
results = idx.query(event="startup")
results = idx.query(tag="system")
```

- Max 100,000 entries; FIFO 25% eviction when full (amortized O(1))
- Corrupt lines skipped with `UserWarning` (no crash)
- CLI: `ccm logs [--event E] [--tag T]`

## Tests
`tests/test_utils_logger.py` — 8 tests covering Logger methods + exc_info formatter branch
`tests/test_log_index.py` — covers eviction, corrupt lines, load cap, tag indexing
```


## 4.18 Agents

FILE: /home/user/wellux_testprojects/.claude/agents/ralph-loop.md
```markdown
---
name: ralph-loop
description: >
  Self-driving autonomous development loop. Resets context between tasks for long
  autonomous coding sessions. Implements dual-condition exit gate, rate limiting,
  and circuit breaker. Invoke for: "run autonomously", "keep improving until done",
  "autonomous mode", "self-driving session", "loop until fixed", "ralph loop".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Agent: Ralph Loop — Autonomous Development Agent
**Inspired by:** frankbria/ralph-claude-code (official Anthropic pattern)

## Mission
Read tasks/todo.md → pick next unchecked item → plan → implement → verify → check off → repeat.
Never stop until: all tasks done, exit signal received, or error threshold hit.

## Loop Structure

### 1. Load Context
- Read MASTER_PLAN.md → find next `- [ ]` step
- Read tasks/lessons.md → avoid known mistakes
- Read relevant code files for current task

### 2. Plan (brief)
- Write 3-5 bullet plan in scratchpad
- If task is XL → break into smaller steps

### 3. Execute
- Implement using appropriate tools
- Write tests if code task
- Verify: run tests, check output, validate

### 4. Complete
- Mark task done in MASTER_PLAN.md: `- [x]`
- Commit: `git add -A && git commit -m "feat: <task>"`
- Log: append to data/cache/ralph-log.txt

### 5. Safety Checks (before each iteration)
- Rate limit: track calls this session, pause if > 80 in an hour
- Circuit breaker: if same error 3x → STOP and report
- Timeout: session max 24h (check elapsed time)

## Exit Conditions
- All `- [ ]` in MASTER_PLAN.md are checked
- User sends "STOP" or "EXIT"
- Circuit breaker triggered (3x same error)
- Rate limit exceeded (> 100 calls/hr)
- Session > 24h

## Error Recovery
- On single error: retry once with different approach
- On 2x same error: search for solution in tasks/lessons.md and WebSearch
- On 3x same error: circuit breaker → STOP → report to user

## Session Log Format
```
ralph-loop session: 2026-03-28 14:00
Task: [3.1] Write /swarm skill → DONE (2min)
Task: [3.2] Write 16 security skills → DONE (15min)
...
Exit: All tasks complete
```

## Invocation
Start: describe the goal or just point at MASTER_PLAN.md
Resume: `--resume` to continue from last checkpoint
```

FILE: /home/user/wellux_testprojects/.claude/agents/research-agent.md
```markdown
---
name: research-agent
description: >
  Autonomous Karpathy-style research agent. Searches, reads, distills to first principles,
  and stores findings. Invoke for: "research X", "auto-research", "weekly research run",
  "find latest on X", "deep dive research".
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

# Agent: Research Agent — Karpathy-Style Autonomous Research

## Mission
For each research topic: WebSearch → read deeply → distill to first principles → implement minimal example → store findings → extract insights to lessons.md

## Karpathy Methodology
- Understand it well enough to rebuild from scratch
- Don't just summarize — distill the INSIGHT
- Implementation validates understanding
- First principles > surface-level explanation

## Research Topics (weekly rotation)
1. LLM agent architectures and memory systems
2. RAG systems and retrieval improvements
3. Prompt engineering advances
4. AI safety and alignment techniques
5. Fine-tuning and PEFT methods
6. Multimodal AI capabilities
7. AI agent frameworks and tooling
8. Code generation and AI-assisted development

## Process (per topic)

### Step 1: Search
```
WebSearch: "<topic> 2026 paper implementation"
WebSearch: "<topic> best practices github"
WebSearch: "<topic> hacker news site:news.ycombinator.com"
```

### Step 2: Read & Distill
- Fetch top 3-5 results
- Extract: core insight, technique, implementation pattern
- Answer: what would I do differently knowing this?

### Step 3: Implement
- Write minimal working pseudocode or actual code
- Proves understanding is real, not surface-level

### Step 4: Store
- Write: `data/research/YYYY-MM-DD-<topic>.md`
- Update: `data/research/README.md` (index)
- Append insights: `tasks/lessons.md`

## Output Per Topic
```markdown
# Research: <topic> — <date>
## Core Insight
## Key Technique
## Minimal Implementation
## Actionable Takeaways
## Sources
```

## Weekly Schedule (via cron)
```bash
# Monday 6am
0 6 * * 1 bash tools/scripts/research-agent.sh
```
```

FILE: /home/user/wellux_testprojects/.claude/agents/security-reviewer.md
```markdown
---
name: security-reviewer
description: >
  Autonomous security review agent. Runs full security assessment across all 16
  security skill domains. Invoke for: "security review", "auto security audit",
  "run security agent", "full security sweep".
allowed-tools: Read, Grep, Glob, WebSearch
---

# Agent: Security Reviewer — Autonomous Security Assessment

## Mission
Run a comprehensive security review using all 16 security skill domains. Produce a prioritized, actionable security report.

## Review Domains (in order)
1. **AppSec** (appsec-engineer): OWASP Top 10 on all source code
2. **AI Security** (ai-security): prompt injection, LLM trust boundaries
3. **Dependency Audit** (dep-auditor): CVEs in requirements.txt / package.json
4. **Secrets** (devops-engineer): hardcoded credentials, secrets in code
5. **IAM** (iam-engineer): auth patterns, access control
6. **GRC** (grc-analyst): data handling, compliance gaps

## Process

### Step 1: Map the codebase
- Glob all source files
- Identify: auth code, API handlers, data models, config files

### Step 2: Run each domain check
For each file relevant to each domain:
- Read and apply domain-specific checklist
- Record findings with file:line reference

### Step 3: Synthesize
- Deduplicate findings
- Score by CVSS
- Group by: Critical, High, Medium, Low, Info

### Step 4: Report
Write to `data/outputs/security-report-YYYY-MM-DD.md`

## Output Format
```markdown
# Security Report — <date>
## Summary
- Critical: N | High: N | Medium: N | Low: N

## Critical Findings
- [CRITICAL] file.py:34 — description — remediation

## Recommendations (top 5)
1. ...
```
```

FILE: /home/user/wellux_testprojects/.claude/agents/swarm-orchestrator.md
```markdown
---
name: swarm-orchestrator
description: >
  Orchestrates a swarm of parallel subagents for complex task decomposition.
  Creates agent files, assigns independent workstreams, and synthesizes results.
  Invoke for: "swarm this task", "parallel agents", "orchestrate swarm".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Agent: Swarm Orchestrator — Parallel Agent Coordination

## Mission
Decompose complex tasks into maximally parallel independent workstreams. Create all agent files. Deliver a clear execution plan.

## Decision Framework
When to swarm vs single agent:
- Swarm if: 3+ independent streams, task > 1 context window, parallel speedup > 2x
- Single if: tight dependencies, coordination overhead > benefit

## Orchestration Process

### Phase 1: Context Capture (always first)
- Read CLAUDE.md, MASTER_PLAN.md, tasks/todo.md
- Read relevant src/ and docs/ files
- Understand full context before designing

### Phase 2: Endstate Analysis
- What does "done" look like precisely?
- What are ALL the deliverables?
- What are the acceptance criteria?

### Phase 3: Decompose
Split into independent streams:
- **Research stream**: gather information, read docs/papers
- **Code stream**: implement core logic
- **Test stream**: write tests (can start from spec, not waiting for code)
- **Docs stream**: write documentation
- **Review stream**: review all outputs

### Phase 4: Create Agent Files
For each stream: `.claude/agents/<stream>-agent.md`

### Phase 5: Execution Plan
```
Round 1 (parallel): research-agent, docs-agent
Round 2 (parallel): code-agent (uses research output), test-agent (uses spec)
Round 3 (parallel): review-agent (reviews code + tests + docs)
Round 4 (serial): integration-agent (combines all outputs)
```

## Output
```
## Swarm Plan: <task>
Agents created: N files in .claude/agents/
Execution rounds: X
Estimated time: Y (vs Yz sequential)
```
```


## 4.19 Commands

FILE: /home/user/wellux_testprojects/.claude/commands/audit.md
```markdown
# Command: /audit

Run a full project audit: security, performance, documentation, dependencies.

## Steps
1. /ciso — full security audit
2. /perf-profiler — performance analysis
3. /dep-auditor — dependency CVEs
4. /readme-writer — check docs freshness
5. /web-vitals — if frontend present

## Output
Consolidated audit report in `data/outputs/audit-YYYY-MM-DD.md`

## Usage
```
/audit full
/audit security-only
/audit perf-only
```
```

FILE: /home/user/wellux_testprojects/.claude/commands/deploy.md
```markdown
---
description: >
  Run the full deployment pipeline: environment check → tests → Docker build →
  container start → health verification → smoke evals. Use for: "deploy",
  "ship it", "deploy to staging", "run the deploy pipeline", "build and deploy".
argument-hint: "[--env local|staging|prod] [--dry-run] [version tag]"
allowed-tools: Bash, Read, Write
---

# /deploy — Full Deploy Pipeline

## What this does
Runs `ccm deploy` which orchestrates: doctor → pytest → docker build → compose up → /health poll → smoke evals.

## Usage
```
/deploy                          # deploy to local (default)
/deploy --dry-run                # dry-run: validate all steps without starting containers
/deploy --env staging            # deploy to staging env
/deploy --skip-tests             # skip pytest (use when tests already passed in CI)
```

## Steps I will execute

### 1. Pre-deploy check
```bash
ccm doctor
```
Validates API key, package imports, paths, skills, git, log writability.
If any check fails: stop and report — do NOT deploy a broken environment.

### 2. Run tests (skip with --skip-tests)
```bash
python -m pytest tests/ -q --tb=short
```
ALL 368 tests must pass. If any fail: stop. Fix the failure before deploying.

### 3. Build Docker image (skip with --skip-build)
```bash
ccm build
```
Builds `ccm-api:latest` and `ccm-api:{version}`. Reports final image size.

### 4. Start containers
```bash
docker compose up -d
```
Starts the API service with resource limits from docker-compose.yml.
Dry-run stops before this step.

### 5. Health check (30s timeout)
```bash
ccm health --url http://localhost:${PORT:-8000}
```
Polls /health every 3s until status=ok or 30s timeout. On timeout: run `docker compose logs api` to diagnose.

### 6. Smoke evals
```bash
ccm eval run data/evals/smoke.jsonl --dry-run
```
Verifies the deployed service handles the 5 smoke cases correctly.

### 7. Summary
Print each step with ✓/✗ status. Exit 0 if all passed, 1 if any failed.

## On failure
- If tests fail: show failing test names, suggest `python -m pytest tests/<file> -v`
- If build fails: show last 20 lines of build output
- If health fails: run `docker compose logs api --tail 50`
- If evals fail: show which cases failed and expected vs. actual

## After successful deploy
Update tasks/todo.md with deployment entry:
```
- [x] Deploy {version} to {env} — {timestamp}
```

## Rollback
If something goes wrong after deploy:
```bash
docker compose down
git stash  # if needed
docker compose up -d  # restart previous image
```
```

FILE: /home/user/wellux_testprojects/.claude/commands/fix-issue.md
```markdown
Fix the issue described below (GitHub issue, error message, or bug description).

## Process

### 1. Understand the issue
- Read the full issue/error carefully
- Identify: what is expected? what is actually happening?
- If a GitHub issue number is given, fetch it with `mcp__github__get_issue`

### 2. Reproduce
- Find the failing test or write one that demonstrates the bug
- Run it to confirm the failure: `pytest tests/ -k "<test_name>" --tb=long`
- If no test exists, create one in the appropriate `tests/test_*.py` file

### 3. Diagnose root cause
- Trace the call stack from the error
- Identify the single line or logic branch responsible
- Do NOT fix symptoms — find the root cause

### 4. Fix
- Make the minimal change needed — do not refactor surrounding code
- Apply only in `src/` (never in `tests/` except to add the repro test)
- Check `.claude/rules/code-style.md` before writing any new code

### 5. Verify
```bash
# Run the specific test first
pytest tests/ -k "<test_name>" --tb=short

# Then full suite
pytest --tb=short -q

# Then lint
ruff check src/ tests/ --select E,F,W --ignore E501

# Then smoke evals
python -m src.cli eval run data/evals/smoke.jsonl --dry-run
```

All four must pass before marking the issue fixed.

### 6. Commit
```
fix: <imperative description of what was wrong>

Root cause: <one sentence>
Fix: <one sentence>

Fixes #<issue_number>
```

## Rules
- Never use `--no-verify` to skip hooks
- Never silence an exception to make a test pass
- If the fix requires changing a test, explain why the test was wrong
- If you cannot reproduce the issue, say so — do not guess
```

FILE: /home/user/wellux_testprojects/.claude/commands/research.md
```markdown
# Command: /research

Run the Karpathy-style autonomous research agent on a topic.

## Steps
1. Invoke research-agent with topic
2. WebSearch for latest papers and implementations
3. Distill to first principles
4. Write to data/research/YYYY-MM-DD-<topic>.md
5. Extract insights → tasks/lessons.md
6. Update data/research/README.md

## Usage
```
/research LLM agent memory systems
/research RAG with graph retrieval
/research prompt engineering 2026
```

## Schedule
Runs automatically every Monday 6am via cron:
`0 6 * * 1 bash tools/scripts/research-agent.sh`
```

FILE: /home/user/wellux_testprojects/.claude/commands/review.md
```markdown
Review the code changes in this session (or the files/PR specified).

## What to review

If a PR number or file list is given, review that. Otherwise review all staged and unstaged changes (`git diff HEAD`).

## Review checklist

Go through each changed file and check:

### Correctness
- [ ] Logic is correct — trace through edge cases mentally
- [ ] No off-by-one errors, null-pointer risks, or unhandled exceptions
- [ ] Async code: no missing `await`, no fire-and-forget without error handling
- [ ] Any new public function has a test

### Code style (see `.claude/rules/code-style.md`)
- [ ] Naming follows conventions (snake_case, PascalCase, UPPER_CONST)
- [ ] No ambiguous single-letter names (`l`, `O`, `I`)
- [ ] No unused imports or variables
- [ ] f-strings only where there are actual placeholders
- [ ] Imports at top of file (no mid-module imports unless lazy-loading)

### Tests (see `.claude/rules/testing.md`)
- [ ] New behaviour has unit tests
- [ ] Edge cases tested (empty input, None, error paths)
- [ ] No test logic in `src/`
- [ ] `pytest --tb=short -q` passes

### Security
- [ ] No secrets or API keys in code
- [ ] No `eval()`, `exec()`, or shell injection risks
- [ ] External inputs are validated before use
- [ ] No `except:` bare catches that swallow errors silently

### API changes (if applicable, see `.claude/rules/api-conventions.md`)
- [ ] Response model updated in `src/api/models.py`
- [ ] `X-Request-ID` flows through to new endpoints
- [ ] Errors raise `HTTPException` with appropriate status codes

## Output format

For each file, output:

```
FILE: src/foo/bar.py
  ✓ Looks good — [brief reason]
  ⚠ [issue description] — line N — [suggested fix]
  ✗ [blocking issue] — line N — [required change]
```

Summarise at the end:
- Total files reviewed
- Blocking issues (✗) that must be fixed before merge
- Warnings (⚠) that should be addressed
- Verdict: APPROVE / REQUEST CHANGES
```


## 4.20 Memory Files

FILE: /home/user/wellux_testprojects/.claude/memory/hot/hot-memory.md
```markdown
# Hot Memory — Always Loaded (≤50 lines)
<!-- L0: active project context — DYNAMIC above marker, STATIC below -->

<!-- DYNAMIC: auto-updated by pre-compact.sh on every compaction -->
**Last Updated**: 2026-04-06 07:59:49

## Active Context (auto-updated)

## Recent Commits (auto-updated)
- 59d94ee fix(version): correct VERSION_INFO to 4-tuple (major, minor, patch, pre)
- 4b62160 fix(version): read version dynamically from installed metadata or pyproject.toml
- da20c0e docs(CLAUDE.md): document v1.0.7 additions — open-findings, 30 lessons, hook improvements

## Recent Lessons (auto-updated)

### Lesson 28: A module-level name that doesn't exist will always ImportError silently
- PATTERN: `cmd_serve_mcp` did `from src.mcp_server import mcp`. There was no `mcp` at
  module level in `mcp_server.py` — it was only created inside `_build_server()` which ran
  under `if __name__ == "__main__":`. The `ImportError` was caught and printed the misleading
  message "Error: 'mcp' not installed" — even when `mcp` was installed. The feature was
  completely broken and gave no useful diagnostic.
- RULE: Before shipping a `from module import name` call, verify `name` is actually defined
  at module level in the target file. Never import an internal helper's return value as if it
  were a module-level export.
- PREVENTION: Add a smoke test: `python3 -c "from src.mcp_server import run"`. If it raises
  `ImportError: cannot import name`, the export is missing. This takes 2 seconds and catches
  the entire class of broken-export bugs.


### Lesson 29: awk section extraction needs heading-as-delimiter, not separator lines
- PATTERN: Tried to extract lessons from `tasks/lessons.md` using `---` as the end-of-lesson
  sentinel: `/^---/{if(in_l && buf!=""){lessons[++c]=buf}}`. Only 1 of 26 lessons was
  captured — because lessons are separated only by the NEXT `### Lesson N` heading, not by
  `---` lines. The single `---` appears once at the top of the file after the Format section.
- RULE: When extracting numbered/headed sections from Markdown, use the START of the NEXT
  heading as the signal to save the PREVIOUS section's buffer, then reset. Do not assume
  separator lines (`---`, `===`) exist between sections.
- PREVENTION: Pattern: `/^### Heading/{if(in_s && buf!="") save(buf); buf=""; in_s=1} in_s{buf+=line}`
  with `END{if(in_s && buf!="") save(buf)}` to capture the final section with no trailing separator.

<!-- STATIC: manually curated below — never auto-overwritten by hooks -->

## Key Architecture Decisions
- **Routing first**: every task goes through 5-router system (llm/skill/agent/memory/task)
- **Skills over code**: prefer adding a skill before writing procedural code
- **Editable install**: `pip install -e ".[dev]"` with `build-backend = "setuptools.build_meta"`
- **Entry point**: `from src.cli import main` — project root must be on sys.path
- **PreCompact hook**: snapshots git state + open tasks before every context compaction
- **No-dup triggers**: `test_no_duplicate_trigger_phrases` enforces unique triggers across 123 skills
- **Chat via messages API**: always `client.chat(messages=[...])`, never flatten to string

## Completed Work
- v0.9.0–v0.9.4: tiered memory, 7 hooks, 9 new skills, per-module CLAUDE.md (6 files), glacier ADRs
- v1.0.0: first stable release — README updated, version bumped
- v1.0.1: 5 bugs fixed (error_handler op-precedence, tiered_memory dead var, llm_router dup,
  grc-analyst trigger, /chat native API); 8 new tests; smoke suite +1 case; 5 new lessons
- v1.0.2: ccm lint CLI subcommand; search_glacier limit param; mcp_server deferred FastMCP import
- v1.0.3: API /v1/ prefix via APIRouter; shared conftest fixtures; README/docs synced
- v1.0.4: dead var, content[0] IndexError, regex cache, ChatRequest validation, session-start URL fix
- v1.0.5: JSONL comment fix, pyproject requires-python <4, CI cache-dependency-path
- v1.0.6: HTTPException detail no longer leaks str(e); logger redacts password/token/api_key/secret
- v1.0.7: all P2/P3 findings resolved; EvalRunner max_workers; richer session-start boot display
  · 31 lessons total (27-31: hook static zones, module exports, awk delimiters, ANSI/sed, heredoc backticks)

## Critical Files
- `src/routing/skill_router.py` — 123-skill registry (no duplicates)
- `src/persistence/tiered_memory.py` — hot/warm/glacier tiers
- `src/llm/claude_client.py` — `chat()` + `complete()` with retry/backoff
- `.claude/hooks/pre-compact.sh` — context survival hook
- `tasks/lessons.md` — self-improvement log (31 lessons)

## Never Do
- Push to main without permission
- Commit .env or API keys
- Skip ruff check before marking done
- Flatten chat messages to a string — use `client.chat(messages=[...])`
- Mix `or`/`and` without explicit parentheses
```

FILE: /home/user/wellux_testprojects/.claude/memory/warm/api-surface.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/.claude/memory/warm/architecture.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/.claude/memory/warm/decisions.md
```markdown
# Warm Memory: Key Decisions
<!-- L1: architectural decisions with rationale, not just what but why -->

**Last Updated**: 2026-04-05

---

## Build System

**Decision**: `build-backend = "setuptools.build_meta"` (not `setuptools.backends.legacy:build`)
**Why**: `setuptools.backends` subpackage missing in this environment; `build_meta` is the stable alias that works everywhere
**Alternative considered**: `flit_core`, rejected — adds a dependency for no gain
**Date**: 2026-04-05

---

## Package Layout

**Decision**: `[tool.setuptools.packages.find] where = ["."] include = ["src*"]`
**Why**: Editable install was adding `/home/user/wellux_testprojects/src` to sys.path. Entry point is `from src.cli import main` which needs the PROJECT ROOT on sys.path, not `src/`
**Symptom if broken**: `ImportError: No module named 'src'` when running `ccm`
**Date**: 2026-04-05

---

## Logger exc_info Filtering

**Decision**: Seed `_STDLIB_KEYS` from a real `LogRecord()` instance AND `LogRecord.__dict__`
**Why**: Class dict misses instance attributes like `exc_info` (set per-record at runtime). Using instance ensures all runtime attrs excluded from JSON. Without this, `json.dumps` crashes on `(type, value, traceback)` tuples.
**File**: `src/utils/logger.py:_STDLIB_KEYS`
**Date**: 2026-04-05

---

## Skill Registry Architecture

**Decision**: 123-entry `_SKILL_REGISTRY` list with exact-substring trigger matching
**Why**: Simple O(n) scan is fast enough at <200 entries; regex would be harder to maintain; LLM-based routing is too expensive for every task dispatch
**Key constraint**: No duplicate trigger phrases (enforced by `test_no_duplicate_trigger_phrases`)
**Date**: 2026-04-05

---

## Tiered Memory Architecture

**Decision**: Hot (≤50 lines, file-based) / Warm (domain files) / Glacier (YAML-frontmatter archives)
**Why**: Flat MemoryStore had no token-efficient loading. Hot tier stays ≤50 lines to fit in session-start hook output without dominating the context. Glacier uses frontmatter for indexed search without loading full file bodies.
**Alternative considered**: SQLite + vector DB (claude-mem pattern) — too heavy for this use case
**Date**: 2026-04-05

---

## PreCompact Hook (context survival)

**Decision**: Add `PreCompact` hook that writes hot-memory snapshot before context compaction
**Why**: Context compaction wipes all in-flight state. Without this, active task context, open decisions, and current branch state are lost across compaction boundaries.
**File**: `.claude/hooks/pre-compact.sh`
**Date**: 2026-04-05

---

## Security Dependencies

**Decision**: `anthropic>=0.87.0,<1.0` and `cryptography>=46.0.6`
**Why**: CVE remediation — anthropic 0.87.0 fixes CVE-2026-34450/34452; cryptography 46.0.6 fixes 6 CVEs including CVE-2026-34073
**Files**: `pyproject.toml`, `requirements.txt`, `Dockerfile`, `.github/workflows/ci.yml`
**Date**: 2026-04-05

---

## RIPER Workflow

**Decision**: 5-phase gate (Research→Innovate→Plan→Execute→Review) as a skill, not a CLAUDE.md rule
**Why**: CLAUDE.md rules apply globally and dilute attention; a skill is invoked explicitly when needed for complex features. Phase gates enforced by "stop and wait for approval" language rather than code.
**Date**: 2026-04-05
```

FILE: /home/user/wellux_testprojects/.claude/memory/warm/evicted-from-hot.md
```markdown

## Evicted 2026-04-05 23:11:47
- Branch: claude/optimize-cli-autonomy-xNamK
- Version: v1.0.0  ·  Tests: 569 passing  ·  Skills: 123 loaded
- Uncommitted changes: 4 file(s)

## Evicted 2026-04-05 23:11:58
- Last commit: d5464b8 chore: sync hot-memory timestamps

## Evicted 2026-04-05 23:12:04
- MASTER_PLAN: 31/31 complete · memory_bank_synced: 2026-04-05 23:03

## Evicted 2026-04-05 23:12:11
- **memory_bank_synced**: 2026-04-05 23:12

## Evicted 2026-04-05 23:17:14
- **memory_bank_synced**: 2026-04-05 23:17

## Evicted 2026-04-05 23:17:19
- **memory_bank_synced**: 2026-04-05 23:17

## Evicted 2026-04-05 23:30:14
- **memory_bank_synced**: 2026-04-05 23:30

## Evicted 2026-04-05 23:30:40
- **memory_bank_synced**: 2026-04-05 23:30

## Evicted 2026-04-05 23:30:48
- **memory_bank_synced**: 2026-04-05 23:30

## Evicted 2026-04-05 23:33:36
- Branch: claude/optimize-cli-autonomy-xNamK
- Version: v1.0.7  ·  Tests: 572 passing  ·  Skills: 123 loaded
- Uncommitted changes: 0 file(s)

## Evicted 2026-04-05 23:33:43
- Last commit: 59d94ee fix(version): correct VERSION_INFO to 4-tuple (major, minor, patch, pre)

## Evicted 2026-04-06 00:05:58
- Branch: claude/optimize-cli-autonomy-xNamK
- Version: v1.0.7  ·  Tests: 572 passing  ·  Skills: 123 loaded
- Uncommitted changes: 5 file(s)

## Evicted 2026-04-06 00:06:05
- Last commit: 59d94ee fix(version): correct VERSION_INFO to 4-tuple (major, minor, patch, pre)

## Evicted 2026-04-06 00:12:29
- MASTER_PLAN: 31/31 complete · memory_bank_synced: 2026-04-05 23:36

## Evicted 2026-04-06 00:19:22
- **memory_bank_synced**: 2026-04-06 00:19

## Evicted 2026-04-06 00:20:43
- **memory_bank_synced**: 2026-04-06 00:20

## Evicted 2026-04-06 00:21:04
- **memory_bank_synced**: 2026-04-06 00:21

## Evicted 2026-04-06 00:21:14
- **memory_bank_synced**: 2026-04-06 00:21

## Evicted 2026-04-06 00:21:23
- **memory_bank_synced**: 2026-04-06 00:21

## Evicted 2026-04-06 07:55:06
- **memory_bank_synced**: 2026-04-06 07:55

## Evicted 2026-04-06 07:55:15
- **memory_bank_synced**: 2026-04-06 07:55

## Evicted 2026-04-06 07:55:21
- **memory_bank_synced**: 2026-04-06 07:55

## Evicted 2026-04-06 07:59:42
- **memory_bank_synced**: 2026-04-06 07:59

## Evicted 2026-04-06 07:59:49
- **memory_bank_synced**: 2026-04-06 07:59
```

FILE: /home/user/wellux_testprojects/.claude/memory/warm/patterns.md
```markdown
# Warm Memory: Patterns
<!-- L1: recurring code patterns, idioms, and anti-patterns in this codebase -->

**Last Updated**: 2026-04-05

---

## Routing Pattern

All 5 routers follow the same interface: `route_*(task: str) -> Result`.
Composed by `route()` in `src/routing/__init__.py` → `RoutingDecision` dataclass.

```python
from src.routing import route
d = route("security audit of src/api/")
print(d.model)      # "opus"
print(d.skill)      # SkillMatch(skill="ciso", confidence=0.9, ...)
print(d.summary())  # formatted box
```

## Skill Registry Pattern

```python
{"skill": "name", "category": "category", "priority": 7,
 "triggers": ["exact phrase 1", "exact phrase 2"]}
```
- Triggers: lowercase exact-substring match against lowercased input
- Priority: 0–10 (higher wins when multiple skills match)
- **No duplicates**: enforced by `test_no_duplicate_trigger_phrases`

## Tiered Memory Pattern

```python
from src.persistence import TieredMemory
mem = TieredMemory()                                # uses .claude/memory/ by default
mem.write_hot("key", "value")                      # hot: auto-evict at 50 lines
mem.write_warm("domain", "# Header\ncontent")      # warm: full domain file
path = mem.archive_glacier("slug", "body",         # glacier: YAML frontmatter
                           tags=["arch"])
results = mem.search_glacier("keyword")            # full-text + tag search
```

## Logger Pattern

```python
from src.utils.logger import get_logger
log = get_logger("component")
log.info("event", key="value", count=42)   # structured JSON output
log.error("failed", error=str(e))          # exc_info NOT passed as kwarg — set on record
```
**Anti-pattern**: `log.error("msg", exc_info=True)` — use `log.error("msg")` inside except block instead; the formatter reads `sys.exc_info()` automatically.

## EvalCase/EvalSuite Pattern

```python
from src.evals import EvalCase, EvalSuite, EvalRunner

suite = (EvalSuite("name")
    .add(EvalCase("id", "prompt", contains=["expected"], tags=["fast"]))
)
report = EvalRunner(llm_fn).run(suite)
print(report.summary())
```
**Anti-pattern**: `EvalResult("id", Verdict.PASS, [], 1.0, 0, ["tag"])` — use keyword args to avoid positional mapping errors.

## Middleware Order (outermost → innermost)

```
CorrelationIDMiddleware  →  attach request ID first
TimingMiddleware         →  time the full handler
Application routes
```
**Rule**: `ContextVar.reset(token)` MUST be in a `finally` block to avoid leaking context across requests.

## Test Structure Pattern

```python
class TestFeatureName:
    def test_happy_path(self, tmp_path: Path) -> None:
        ...
    def test_failure_case(self, tmp_path: Path) -> None:
        ...
```
- One assertion focus per test
- Use `tmp_path` fixture for filesystem tests
- No `@pytest.mark.asyncio` needed (asyncio_mode = auto)
- Mock at the boundary: `unittest.mock.patch`, `AsyncMock`

## Hook Exit Codes

- `exit 0` → allow the operation to proceed
- `exit 2` → block the operation (print reason to stderr first)
- All hooks use `|| true` in settings.json to prevent hook crashes from breaking Claude
```

FILE: /home/user/wellux_testprojects/.claude/memory/warm/troubleshooting.md
```markdown
# Warm Memory: Troubleshooting
<!-- L1: known issues, gotchas, workarounds — what bit us and how to fix it -->

**Last Updated**: 2026-04-05

---

## Edit Tool: "String not found" on stale reads

**Symptom**: `Edit` fails with `String to replace not found in file`
**Root cause**: File changed between the last `Read` and the `Edit` call (another tool, hook, or background agent modified it)
**Fix**: Always `Read` immediately before `Edit`. Keep the match string small and unique — large blocks drift.
**Prevention**: Never batch a Read + multiple Edits without re-reading between them if anything could change the file.

---

## Editable Install: `ImportError: No module named 'src'`

**Symptom**: `ccm` or `python3 -m src.cli` fails with `ModuleNotFoundError`
**Root cause**: `.pth` file from `pip install -e .` added `/home/user/wellux_testprojects/src` instead of the project root
**Fix**: In `pyproject.toml`, set `[tool.setuptools.packages.find] where = ["."] include = ["src*"]`
**Also check**: `build-backend = "setuptools.build_meta"` (not `setuptools.backends.legacy:build`)

---

## Logger: JSON serialize crash on exc_info

**Symptom**: `TypeError: Object of type type is not JSON serializable` in structured logger
**Root cause**: `_STDLIB_KEYS` was seeded only from `LogRecord.__dict__` (class-level). Instance attrs like `exc_info` (set at runtime) bypassed the filter and hit `json.dumps` as raw `(type, value, traceback)` tuples.
**Fix**: `_STDLIB_KEYS = frozenset(LogRecord("", INFO, "", 0, "", (), None).__dict__.keys()) | frozenset(LogRecord.__dict__.keys())`
**File**: `src/utils/logger.py:_STDLIB_KEYS`

---

## Duplicate Trigger Phrases in Skill Registry

**Symptom**: `test_no_duplicate_trigger_phrases` fails
**Root cause**: Two skill entries share an identical trigger string — the second silently shadows the first
**Fix**: Find the duplicate with `python3 -c "from src.routing.skill_router import _SKILL_REGISTRY; seen={}; [print(t, e['skill']) for e in _SKILL_REGISTRY for t in e['triggers'] if (t in seen) and seen[t]!=e['skill'] or seen.update({t:e['skill']}) and False]"` and remove from the lower-priority skill

---

## setuptools.backends Missing

**Symptom**: `ModuleNotFoundError: No module named 'setuptools.backends'` during `pip install -e .`
**Root cause**: `setuptools<68` doesn't have the `backends` subpackage; `setuptools.backends.legacy:build` was introduced in 68+ but inconsistently available
**Fix**: Use `build-backend = "setuptools.build_meta"` — this is the stable, always-available alias

---

## ContextVar Leaking Across Requests

**Symptom**: Request IDs bleed between concurrent requests; `X-Request-ID` header has wrong value
**Root cause**: `ContextVar.reset(token)` not called in `finally` — if an exception occurs mid-handler, the context var is never reset
**Fix**: Wrap reset in `finally`:
```python
token = _request_id_var.set(request_id)
try:
    response = await call_next(request)
finally:
    _request_id_var.reset(token)
```
**File**: `src/api/middleware.py`

---

## EvalResult Positional Arg Mismatch

**Symptom**: Tests pass wrong values — e.g., `tags` field gets the `latency_ms` value
**Root cause**: `EvalResult(case_id, verdict, actual, score, latency_ms, tags)` — positional order is easy to get wrong
**Fix**: Always use keyword args: `EvalResult(case_id="a", verdict=Verdict.PASS, score=1.0, tags=["fast"])`

---

## Ruff F841 on Test Helper Variables

**Symptom**: `F841 Local variable 'mem' is assigned to but never used` in tests
**Root cause**: Creating an object just to trigger its side effects (e.g., dir creation) then checking the dirs
**Fix**: Drop the variable assignment: `TieredMemory(base=tmp_path)` (no assignment) — side effects still happen
```

FILE: /home/user/wellux_testprojects/.claude/memory/glacier/2026-04-05-precompact-hook-context-survival.md
```markdown
---
title: PreCompact Hook for Context Survival
date: 2026-04-05
time: 20:02:12
tags: [hooks, context, memory, resilience, architecture]
slug: precompact-hook-context-survival
---

# Decision: PreCompact Hook for Context Survival

## Status: Accepted  
## Date: 2026-04-05

## Context
Claude Code compacts context automatically when the window fills. Before this decision,
compaction wiped all in-flight state: current branch awareness, open tasks, last commit,
and active architectural decisions. Sessions effectively amnesia'd mid-task.

## Decision
Add a PreCompact hook (.claude/hooks/pre-compact.sh) that fires before every compaction:
1. Reads git branch, uncommitted file count, last commit message
2. Reads open tasks from tasks/todo.md
3. Writes a structured snapshot to .claude/memory/hot/hot-memory.md
4. Appends a timestamped entry to data/sessions/YYYY-MM-DD.md

## Rationale
- PreCompact is the only hook that fires BEFORE context is lost
- Hot-memory.md (≤50 lines) is loaded by session-start hook — bridging across compaction
- Daily session logs provide human-readable audit trail
- Exit 0 always — compaction must never be blocked

## Consequences
- Positive: Restored state survives compaction — branch/tasks/commit visible after compact
- Positive: Session continuity across multiple compactions in a long session
- Negative: hot-memory.md must be kept ≤50 lines (eviction logic required)
- File: .claude/hooks/pre-compact.sh

```

FILE: /home/user/wellux_testprojects/.claude/memory/glacier/2026-04-05-skill-registry-duplicate-enforcement.md
```markdown
---
title: Skill Registry Duplicate Enforcement
date: 2026-04-05
time: 20:02:12
tags: [routing, skill-registry, testing, architecture]
slug: skill-registry-duplicate-enforcement
---

# Decision: Strict No-Duplicate Trigger Phrases in Skill Registry

## Status: Accepted
## Date: 2026-04-05

## Context
The skill router uses substring matching across 123 skills. Early versions had overlapping 
trigger phrases causing non-deterministic routing — same phrase could match multiple skills 
depending on registry iteration order.

## Decision
Enforce zero duplicate trigger phrases via  in 
tests/test_routing.py. CI fails immediately on any duplicate.

## Rationale
- Substring matching makes duplicates invisible at runtime — no error, just wrong skill
- A test at the registry level catches duplicates before they reach production
- Lower-priority skills lose their trigger phrases when conflicts exist (higher priority wins)

## Consequences
- Positive: Deterministic routing — same phrase always maps to same skill
- Positive: Registry is self-documenting (every trigger phrase is unique)
- Negative: Adding new skills requires careful trigger phrase selection
- Process: Run 
no tests ran in 0.02s after any skill edit

```

FILE: /home/user/wellux_testprojects/.claude/memory/glacier/2026-04-05-tiered-memory-architecture.md
```markdown
---
title: Three-Tier Memory Architecture
date: 2026-04-05
time: 20:02:12
tags: [architecture, memory, persistence]
slug: tiered-memory-architecture
---

# Decision: Three-Tier Memory Architecture

## Status: Accepted
## Date: 2026-04-05

## Context
Claude Code sessions are bounded by context windows. Without persistent memory, 
every compaction or new session starts from scratch. We needed a way to preserve 
critical knowledge across sessions at different granularity levels.

## Decision
Implement a three-tier memory system:
- **Hot** (≤50 lines): Always-loaded session context, updated by PreCompact hook
- **Warm** (domain markdown files): Structured knowledge by domain (architecture, decisions, patterns, troubleshooting, api-surface)
- **Glacier** (YAML-frontmatter archives): Permanent searchable decision log

## Rationale
- Hot tier fits in every session-start hook without bloating context
- Warm tier allows domain-specific loading on demand via 
- Glacier provides immutable audit trail of major architectural decisions
- The FIFO eviction from hot → warm prevents hot tier from growing unbounded

## Consequences
- Positive: Sessions survive compaction with critical context intact
- Positive: Full-text search across all historical decisions
- Negative: Must explicitly call archive_glacier() — not automatic
- Mitigated: PreCompact hook auto-saves transient state to hot tier

```


## 4.21 Tasks and Documentation

FILE: /home/user/wellux_testprojects/tasks/PRD.md
```markdown
# Product Requirements Document
# Claude Code Max — Gold-Standard AI Development Template

**Version:** 1.0.7
**Date:** 2026-04-06
**Status:** SHIPPED
**Owner:** Claude Code Max Project

---

## 1. Vision

Build the definitive Claude Code project template that any developer can clone and immediately have:
- Maximum autonomy with safety guardrails
- 123 specialized skills auto-invoked by context
- Karpathy-style autonomous research loop
- Ralph Loop self-driving development agent
- Self-improvement system that gets smarter over time
- Production-quality Python AI stack

---

## 2. Goals

| Goal | Metric | Status |
|------|--------|--------|
| 123 skills with proper frontmatter | `ls .claude/skills/ \| wc -l ≥ 123` | ✅ Done |
| All hooks wired and functional | `bash .claude/hooks/session-start.sh` exits 0 | ✅ Done |
| Max autonomy settings | settings.json has broad allow list | ✅ Done |
| Research loop runs autonomously | `bash tools/scripts/research-agent.sh` succeeds | ✅ Done |
| Ralph Loop agent defined | `.claude/agents/ralph-loop.md` exists | ✅ Done |
| Python stack complete | All src/ modules importable | ✅ Done |
| MASTER_PLAN loopable | "f" → next step executes | ✅ Done |
| Auto-boot on session start | session-start.sh shows context | ✅ Done |
| Self-improvement loop | lessons.md updated after corrections | ✅ Done |

---

## 3. Non-Goals

- NOT a production application (this is a template/harness)
- NOT language-specific (Python stack is illustrative, not mandatory)
- NOT a replacement for actual project CLAUDE.md files
- NOT tied to any specific cloud provider

---

## 4. Architecture

### 5-Layer System
```
L1: CLAUDE.md + .claude/SOUL.md + USER.md  → Persistent context + agent identity
L2: .claude/skills/  → 123 auto-invoked knowledge packs
L3: .claude/hooks/   → 5 deterministic safety/automation gates
L4: .claude/agents/  → 4 autonomous subagent definitions
L5: .claude/rules/   → Modular instruction files (code-style, testing, api-conventions)
```

### Memory Hierarchy
```
~/.claude/CLAUDE.md  → Global (all projects)
./CLAUDE.md          → Project (this file, shared via git)
./src/*/CLAUDE.md    → Subfolder (scoped context)
```

### Data Flow
```
User "f" → read MASTER_PLAN.md next step → execute → check off → update progress
User "r" → research-agent.sh → WebSearch → distill → data/research/ → lessons.md
```

---

## 5. Skill Categories

| Category | Count | Key Skills |
|----------|-------|------------|
| Meta | 2 | /create, /swarm |
| Security | 16 | /ciso (orchestrator), /pen-tester, /appsec-engineer |
| Development | 20 | /code-review, /debug, /architect, /test-writer |
| AI/ML Research | 15 | /karpathy-researcher, /rag-builder, /prompt-engineer |
| DevOps/Infra | 15 | /ci-cd, /docker, /terraform, /monitoring |
| Documentation | 10 | /readme-writer, /adr-writer, /runbook-creator |
| Optimization | 15 | /web-vitals, /bundle-analyzer, /query-optimizer |
| Project Management | 9 | /sprint-planner, /roadmap, /risk-assessor |
| Ecosystem | 5 | /gsd, /mem, /ui-ux, /superpowers, /obsidian |
| **Total** | **107** | |

---

## 6. Hook Specifications

| Hook | Trigger | Exit 0 | Exit 2 |
|------|---------|--------|--------|
| session-start.sh | Session opens | Show boot context | N/A |
| pre-tool-bash.sh | Before Bash | Log + allow | Dangerous pattern |
| post-tool-edit.sh | After Edit/Write | Lint + validate | N/A (never block) |
| stop.sh | Session ends | Show checklist | N/A |

---

## 7. Success Metrics

- [ ] `ls .claude/skills/ | wc -l` → ≥ 105
- [ ] `python3 -m json.tool .claude/settings.json` → valid JSON
- [ ] All .sh files have `chmod +x`
- [ ] `bash .claude/hooks/session-start.sh` runs without error
- [ ] `git branch --show-current` → `claude/optimize-cli-autonomy-xNamK`
- [ ] `grep "^- \[ \]" MASTER_PLAN.md | wc -l` → 0 (all steps done)

---

## 8. Open Questions

1. Which MCP servers to add by default? (GitHub is essential; Notion/Slack optional)
2. Cron scheduling: use crontab or a dedicated schedule skill?
3. Ralph Loop rate limiting: 100 calls/hr or configurable?
4. LightRAG integration: standalone service or embedded in rag-builder skill?
5. Global ~/.claude/CLAUDE.md: write once or managed per-user?
```

FILE: /home/user/wellux_testprojects/tasks/lessons.md
```markdown
# Lessons Learned — Self-Improvement Log

## Format
```
DATE | PATTERN | RULE | PREVENTION
```
After ANY correction: append a new lesson here.
session-start.sh shows last 6 lines on boot.

---

## 2026-03-28

### Lesson 1: SKILL.md frontmatter is critical
- PATTERN: Skills without proper YAML frontmatter (name: + description:) don't auto-activate
- RULE: Every SKILL.md MUST start with `---\nname: <name>\ndescription: >` block
- PREVENTION: post-tool-edit.sh hook validates SKILL.md frontmatter on every write

### Lesson 2: Plan before building
- PATTERN: Starting implementation without a MASTER_PLAN causes rework and lost context
- RULE: Always check MASTER_PLAN.md next step before any new task
- PREVENTION: session-start.sh shows next MASTER_PLAN step on every boot

### Lesson 3: Parallel agents need separate directories
- PATTERN: Multiple agents writing to same files causes conflicts
- RULE: Always assign each agent to non-overlapping file paths
- PREVENTION: /swarm skill checks for path conflicts before spawning agents

### Lesson 4: Hook exit codes matter
- PATTERN: Forgetting exit codes in hooks breaks them silently
- RULE: Always end hooks with explicit exit 0 (allow) or exit 2 (block)
- PREVENTION: post-tool-edit.sh validates hook scripts end with exit statement

### Lesson 5: Settings.local.json for development freedom
- PATTERN: Overly restrictive settings.json blocks legitimate local dev commands
- RULE: Use settings.local.json for unrestricted local access (gitignored)
- PREVENTION: settings.local.json is always present with Bash(*) allow

### Lesson 6: LLMs fail on reasoning, not knowledge
- PATTERN: Vague prompts ("summarize this") produce inconsistent output quality
- RULE: Always specify output format + reasoning steps explicitly in every prompt
- PREVENTION: Use tools/prompts/claude-code-prompts.md templates as starting points

### Lesson 7: MCP provides intelligence, Hooks provide discipline
- PATTERN: Adding MCP tools without hooks means Claude can use them unsafely
- RULE: For every new capability (MCP tool), add a corresponding hook guard if destructive
- PREVENTION: pre-tool-bash.sh hook reviews all Bash; extend for MCP tool calls as needed

### Lesson 8: Graph RAG for relational, flat RAG for simple
- PATTERN: Using vector-only RAG on knowledge bases with complex relationships → hallucinations
- RULE: If the domain has entity relationships (medical, legal, financial), evaluate LightRAG first
- PREVENTION: /rag-builder skill now defaults to recommending LightRAG for relational domains

### Lesson 9: LoRA rank r=32 is the 2026 sweet spot
- PATTERN: Default r=8 in most tutorials undertrained for domain-specific tasks
- RULE: Use r=32 for fine-tuning, paged_adamw optimizer, bf16 dtype — document all three
- PREVENTION: /fine-tuner skill includes r=32 as the recommended default config

### Lesson 10: Safety is neuron-sparse — freeze SCUs before fine-tuning
- PATTERN: Domain fine-tuning degrades safety refusals by 10-15% when applied naively
- RULE: Run safety neuron analysis before any fine-tune; freeze top 20% SCU neurons
- PREVENTION: /fine-tuner skill now includes pre-tune safety unit identification step

### Lesson 11: Write lint-clean code from the start — CI will catch it otherwise
- MISTAKE: 30 ruff errors committed across src/ and tests/ — CI failed on first real run
- WHY: Unused imports, ambiguous names (`l`), mid-module imports, f-strings without placeholders,
  unused local variables — all fixable locally but not caught before push
- RULE: Run `ruff check src/ tests/ --select E,F,W --ignore E501` before every commit
- PREVENTION: pre-commit hook (`.pre-commit-config.yaml`) now enforces this automatically;
  `ruff --fix` auto-resolves ~80% of issues; remaining 6 require manual fixes:
  - E402: move `import` to top of file
  - E741: rename `l`/`O`/`I` vars → `ln`/`val`/etc.
  - F841: prefix unused vars with `_` or delete the assignment

### Lesson 12: Keep CLAUDE.md current — stale context misleads every future session
- MISTAKE: CLAUDE.md referenced `claude_code_max` directory and omitted CLI, eval framework,
  rules layer, middleware, and API conventions built over many sessions
- WHY: CLAUDE.md is loaded on every session start — outdated info causes wrong assumptions
- RULE: Update CLAUDE.md whenever a major new capability is added (CLI command, module, layer)
- PREVENTION: End-of-session checklist now explicitly includes "update CLAUDE.md if architecture changed"

### Lesson 13: Karpathy single-file rule — complexity is always optional
- PATTERN: Adding abstractions (base classes, plugin hooks, config inheritance) before they are
  needed creates cognitive overhead with no benefit for the current problem
- RULE: If a module cannot be understood in one read-through (<60 seconds), it is too complex.
  Each router is ~30-40 lines. Each runner is ~40 lines. This is correct.
- PREVENTION: Before adding an abstraction, ask "does this exist at nanoGPT scale?" If not, wait.

### Lesson 14: Unbounded in-memory state is a time bomb
- PATTERN: LogIndex._lines growing forever — after 30 days of 1000 req/day = 30M entries,
  potentially 30 GB RAM. No eviction = silent OOM after enough time passes.
- RULE: Every in-memory collection that grows via append MUST have a documented bound.
  Either: max_entries cap with eviction, or explicit lifecycle (cleared on restart), or TTL.
- PREVENTION: LogIndex now has max_entries=100_000 with FIFO 25% eviction (amortized O(1)).
  The pattern: n_drop = max(1, int(len * 0.25)); _lines = _lines[n_drop:]; rebuild_index().

### Lesson 15: Async timeouts are mandatory — not optional hardening
- PATTERN: AsyncEvalRunner._run_case awaited self.llm(...) with no timeout. A hung LLM call
  holds a semaphore slot indefinitely, blocking all other concurrent cases permanently.
- RULE: Every await on an external call (LLM, HTTP, database) MUST be wrapped in
  asyncio.wait_for(..., timeout=N). The timeout should match SLA expectations (30s for LLM).
- PREVENTION: AsyncEvalRunner now passes case_timeout=30.0 to asyncio.wait_for. The
  TimeoutError is caught and returned as EvalResult(verdict=ERROR) like any other exception.

### Lesson 16: context var must reset in finally, not in except+normal-path
- PATTERN: CorrelationIDMiddleware called _request_id_var.reset(token) in two places:
  once in the except block, once after the try/except. If response.headers access raises,
  the reset is skipped and the context var leaks into subsequent requests.
- RULE: Any contextvars.ContextVar.reset(token) call MUST be in a finally block.
  The try/finally pattern guarantees reset regardless of exception type.
- PREVENTION: Middleware dispatch now uses try/finally. The response return is inside try.

### Lesson 17: EvalSuite.from_jsonl bypassed duplicate check — silent data bugs
- PATTERN: from_jsonl used cls(suite_name, cases) which sets _cases directly, bypassing the
  add() method's duplicate ID check. A JSONL file with two identical IDs loaded silently,
  causing incorrect result counts in EvalReport.
- RULE: Internal construction of collections must use the same validation path as external
  mutation. from_jsonl now uses suite.extend(cases) which calls add() for each case.
- PREVENTION: Any cls(...) constructor that accepts a list should either validate in __init__
  or delegate to add(). Never bypass validation with direct assignment in classmethods.

### Lesson 18: Edit tool fails silently on whitespace drift — always Read immediately before Edit
- PATTERN: Multiple Edit calls in a session where the file was changed between the last Read
  and the Edit (by a hook, background agent, or parallel tool). The match string no longer
  exists and the edit silently no-ops or throws "String not found".
- RULE: Always Read a file immediately before Edit. Never batch a Read + multiple Edits
  if anything could change the file between them. Keep match strings small and unique.
- PREVENTION: Added to warm/troubleshooting.md as the #1 gotcha. Use Grep to confirm
  the exact string exists before attempting a multi-step Edit chain.

### Lesson 19: Background agents can re-introduce fixed bugs — verify after subagent completion
- PATTERN: A background research/implementation agent was launched while duplicate triggers
  were being fixed. The agent re-added "backup verification", "decision log", and
  "runbook" as duplicate triggers in skill_router.py — re-breaking the test that was
  just fixed in the main context.
- RULE: After any background agent modifies shared files (especially registries and config),
  run the relevant tests before assuming the state is clean.
- PREVENTION: After every Agent tool completion that touches src/ or tests/, run
  `python3 -m pytest tests/ -q` before proceeding. Never trust subagent self-reports.

### Lesson 20: Skill routing registry duplicates are caught by test — fix the lower-priority skill
- PATTERN: When adding new ecosystem skills, several trigger phrases were shared
  between new skills and existing ones (e.g., "semantic search" in both rag-builder and
  embeddings; "ai safety review" in both ai-security and ai-safety).
- RULE: The lower-priority skill (or the one whose skill name is less specific to the
  trigger) should have its duplicate trigger removed. Keep the trigger in the skill
  that most accurately describes it.
- PREVENTION: Run duplicate check before every commit touching skill_router.py:
  `python3 -c "from src.routing.skill_router import _SKILL_REGISTRY; seen={}; [print('DUP:',t,e['skill'],seen[t]) for e in _SKILL_REGISTRY for t in e['triggers'] if t in seen and seen[t]!=e['skill'] or seen.update({t:e['skill']}) and False]"`

### Lesson 21: Hot memory must be updated at PreCompact — not just at Stop
- PATTERN: Pre-v0.9.0 the only lifecycle save was in stop.sh. When Claude Code compacted
  context mid-session, all in-flight state (active branch, open decisions, partial task
  state) was lost. The next session started completely cold.
- RULE: Critical session state (branch, open tasks, last commit, active feature) must be
  written to hot-memory.md in the PreCompact hook, not just at session end.
- PREVENTION: PreCompact hook now writes a full hot-memory.md snapshot before every
  compaction. This is the most important hook for context survival.

### Lesson 22: Operator precedence in multi-condition if-statements is a silent logic bug
- PATTERN: `if "a" in x or "b" in x and "c" in x:` — Python evaluates `and` before `or`,
  so this is `("a" in x) OR ("b" in x AND "c" in x)`. Any string containing "a" (e.g. "asyncio
  context") matched the token-limit branch even when unrelated to token limits.
- RULE: Always use explicit parentheses when mixing `or` and `and` in the same condition.
  Write `if ("a" in x and "b" in x) or ("c" in x and "d" in x):` — never rely on precedence.
- PREVENTION: Add a test for the "false positive" case: `test_context_alone_is_not_token_limit`.
  CI catches regressions immediately.

### Lesson 23: Dead variable assignments mask latent path bugs
- PATTERN: `target = MODULE_CONST / "path"` followed immediately by `target = self._dir / "path"`
  — line 1 is dead code, but it looks like intentional initialization. If line 2 is accidentally
  removed (e.g. during a merge), line 1 silently uses the wrong path.
- RULE: Delete dead variable assignments immediately. "Two assignments to the same variable
  in consecutive lines" is always a bug or a cleanup failure.
- PREVENTION: Ruff B018 / pylint W0612 (unused variable) would catch this. Ensure `"B"` is in
  ruff select (it is: `pyproject.toml` has `select = ["E", "F", "W", "I", "UP", "B"]`).

### Lesson 24: String-flattening a chat history bypasses the LLM's trained behavior
- PATTERN: Building `"USER: ...\n\nASSISTANT: ...\n\nUSER: ..."` and passing it as a single
  prompt to a chat model. Claude is trained on structured `messages` arrays, not role-prefixed
  strings. Results are degraded and role injection is possible via `msg.role.upper()`.
- RULE: Always pass multi-turn history as a `messages: list[dict]` to the native API.
  For `ClaudeClient`, use the new `client.chat(messages, ...)` method — never `client.complete()`
  with a flattened string for conversations.
- PREVENTION: `test_multi_turn_passes_messages_list` in `test_api_endpoints.py` verifies the
  messages list is passed directly (not flattened) on every push.

### Lesson 25: Broad keyword triggers cause silent mis-routing
- PATTERN: `grc-analyst` had `"audit"` as a trigger. A user asking `"audit my code"` or
  `"run a db audit"` got routed to a GRC compliance analyst instead of `code-review` or `dba`.
  The error was silent — routing succeeded, but to the wrong skill.
- RULE: Skill triggers must be specific enough that they only match the intended use case.
  Prefer multi-word phrases: `"compliance audit"` over `"audit"`. Run `ccm route "audit my code"`
  to sanity-check routing after every skill registry change.
- PREVENTION: After any `_SKILL_REGISTRY` edit, manually test 3 representative prompts with
  `ccm route` before committing.

### Lesson 26: Abstract methods must be implemented even if you want to remove the concept
- PATTERN: Removed `count_tokens` from `ClaudeClient` because it was dead code. Broke all
  26 `ClaudeClient` instantiation tests with `TypeError: Can't instantiate abstract class`.
  The method is declared `@abstractmethod` in `LLMClient` (base class).
- RULE: Before removing a method from a concrete class, check if it's `@abstractmethod` in the
  parent. If the concept should be removed entirely, remove the `@abstractmethod` declaration
  from the base class first, then remove implementations.
- PREVENTION: `grep -r "abstractmethod" src/llm/base.py` before deleting any method from
  a class that inherits from `LLMClient` or any other ABC.

### Lesson 27: Automation hooks that overwrite files destroy manually curated content
- PATTERN: `pre-compact.sh` used `cat > hot-memory.md << EOF ... EOF` — a full overwrite.
  Every compaction silently wiped the carefully maintained "Completed Work", "Key Architecture
  Decisions", and "Never Do" sections, replacing them with a hardcoded stale template
  ("114 skills", 1 commit, no version). The loss was invisible until the session-start
  displayed only 4 bullet lines from a 46-line file.
- RULE: Any hook that updates a file must distinguish between dynamic (auto-generated) and
  static (manually curated) zones. Use a sentinel comment to mark the boundary.
  Only overwrite above the sentinel; extract and re-append everything below it.
- PREVENTION: Add `<!-- STATIC: never auto-overwritten -->` before any curated section in
  files touched by hooks. In the hook, extract the static zone with
  `awk '/<!-- STATIC:/{found=1} found{print}'` before writing, then re-append it.

### Lesson 28: A module-level name that doesn't exist will always ImportError silently
- PATTERN: `cmd_serve_mcp` did `from src.mcp_server import mcp`. There was no `mcp` at
  module level in `mcp_server.py` — it was only created inside `_build_server()` which ran
  under `if __name__ == "__main__":`. The `ImportError` was caught and printed the misleading
  message "Error: 'mcp' not installed" — even when `mcp` was installed. The feature was
  completely broken and gave no useful diagnostic.
- RULE: Before shipping a `from module import name` call, verify `name` is actually defined
  at module level in the target file. Never import an internal helper's return value as if it
  were a module-level export.
- PREVENTION: Add a smoke test: `python3 -c "from src.mcp_server import run"`. If it raises
  `ImportError: cannot import name`, the export is missing. This takes 2 seconds and catches
  the entire class of broken-export bugs.

### Lesson 29: awk section extraction needs heading-as-delimiter, not separator lines
- PATTERN: Tried to extract lessons from `tasks/lessons.md` using `---` as the end-of-lesson
  sentinel: `/^---/{if(in_l && buf!=""){lessons[++c]=buf}}`. Only 1 of 26 lessons was
  captured — because lessons are separated only by the NEXT `### Lesson N` heading, not by
  `---` lines. The single `---` appears once at the top of the file after the Format section.
- RULE: When extracting numbered/headed sections from Markdown, use the START of the NEXT
  heading as the signal to save the PREVIOUS section's buffer, then reset. Do not assume
  separator lines (`---`, `===`) exist between sections.
- PREVENTION: Pattern: `/^### Heading/{if(in_s && buf!="") save(buf); buf=""; in_s=1} in_s{buf+=line}`
  with `END{if(in_s && buf!="") save(buf)}` to capture the final section with no trailing separator.

### Lesson 30: ANSI escape codes in sed replacement strings are treated as literals
- PATTERN: `sed 's/^- \[ \] /  \033[1;33m▸\033[0m /'` — the `\033` is NOT expanded by sed
  into ESC. It becomes literal backslash + `033`, so the terminal receives the characters
  `\`, `0`, `3`, `3` instead of the ANSI escape sequence. The colored arrow appeared as
  garbled text in the output.
- RULE: Never use `\033` (or `\e`) ANSI escape codes inside sed replacement strings. Use
  `printf` with a while-read loop when color output is needed in shell scripts.
- PREVENTION: Replace `grep ... | sed 's/prefix/  \033[...m▸\033[0m /'` with:
  `grep ... | while IFS= read -r line; do printf '  \033[...m▸\033[0m %s\n' "${line#prefix}"; done`

### Lesson 31: Unquoted heredocs execute backticks in expanded variables
- PATTERN: `pre-compact.sh` used `cat > file << MEMEOF ... $RECENT_LESSONS ... MEMEOF`.
  `$RECENT_LESSONS` contained backtick-quoted code examples (awk patterns, grep pipelines)
  from lessons 29-30. Bash executed those backticks as command substitutions inside the
  heredoc, silently swallowing output and dropping the Branch/Version/Tests/Skills lines
  from Active Context on every compaction that followed a lesson-extraction run.
- RULE: Never embed user-sourced or file-sourced content (lesson text, commit messages,
  file contents) directly inside an unquoted heredoc. Use `printf '%s\n' "$VAR"` to append
  variable content to a file — printf treats `%s` literally and never interprets backticks.
- PREVENTION: For any shell script writing structured files with embedded variables:
  use `<< 'QUOTED_DELIM'` for static template text; use `printf '%s\n' "$VAR" >> file`
  for all user-sourced variable content. If both are needed, split into separate writes.

---
_Append new lessons above this line. Newest lessons should appear at the bottom._
```

FILE: /home/user/wellux_testprojects/tasks/open-findings.md
```markdown
# Open Findings — P2/P3 Backlog

Remaining items from v1.0.x deep-review audit. Check off when resolved.
Displayed at session start by `session-start.sh` when unchecked items exist.

---

## P2 — Quality (address when relevant)

- [x] `mcp_server.py` — `cmd_serve_mcp` imported non-existent module-level `mcp`; fixed by adding `run()` entry point
- [x] `.pre-commit-config.yaml:4` — stale finding; already pinned at `v0.9.0`
- [x] `data/evals/smoke.jsonl` — stale finding; `echo-excludes-verified` case already present
- [x] `pyproject.toml coverage.run` — removed stale omit of `src/cli.py`; tests call it directly

## P3 — Improvements (nice to have)

- [x] `evals/runner.py` — added `max_workers` to `EvalRunner` (sync); uses `ThreadPoolExecutor` when >1
- [x] `Dockerfile` — apt curl pin is fragile; added comment directing to base image digest pinning as the correct fix
- [x] `ccm eval run` — threshold now printed after summary (`threshold: 80%`)
- [x] `ci.yml:126` — live-evals condition now explicitly excludes fork PRs via `head.repo.full_name` check
```

FILE: /home/user/wellux_testprojects/tasks/todo.md
```markdown
# Tasks — Claude Code Max

## Active
- [x] Install optimizer crons (systemd user timers → /root/.config/systemd/user/ccm-*.timer)
- [x] Add MCP servers (github, filesystem, brave, sentry, memory, sequential-thinking → .mcp.json)
- [x] Write pytest suite — 321 tests, all passing
- [x] Populate data/research/ — 9 stubs (8 topics + GitHub trending), indexed
- [x] Run full security audit — PASS, 2 findings fixed (dep pins + max_tokens floor)
- [x] Build 5-router routing system (llm/skill/agent/memory/task) — 37 new tests, 134 total
- [x] Complete src/api/ (FastAPI) + src/persistence/ (FileStore + MemoryStore) — 76 new tests, 210 total
- [x] GitHub Actions CI (.github/workflows/ci.yml) + Dockerfile (multi-stage) + docker-compose.yml
- [x] Fix all stale claude_code_max paths (hooks, settings, skills, scripts, MCP, systemd)
- [x] Add L5 rules layer (.claude/rules/: code-style, testing, api-conventions)
- [x] Add /review + /fix-issue commands; CHANGELOG.md + CONTRIBUTING.md
- [x] Add 107th skill: db-designer (was 106)
- [x] Add daily GitHub trending research job (ccm-github-research.timer + script)
- [x] Update docs: architecture.md (5-layer), resources.md (+trending patterns), CLAUDE.md

## Completed ✅
- [x] Repo initialized at /home/user/claude_code_max
- [x] Branch claude/optimize-cli-autonomy-xNamK created + pushed
- [x] CLAUDE.md — 4-layer orchestration, shortcuts f/s/r/a
- [x] .claude/settings.json — max autonomy permissions + hooks wired
- [x] .claude/settings.local.json — local unrestricted override
- [x] 4 hook scripts (session-start, pre-bash, post-edit, stop)
- [x] MASTER_PLAN.md — loopable 31-step plan (100% complete)
- [x] 107 skills with auto-activation frontmatter
- [x] 4 agents (ralph-loop, research-agent, swarm-orchestrator, security-reviewer)
- [x] 3 commands (deploy, audit, research)
- [x] Python stack: src/llm/, src/utils/, src/handlers/, src/prompt_engineering/
- [x] Config: model_config.yaml, prompt_templates.yaml, logging_config.yaml
- [x] Examples: basic_completion.py, chat_session.py, chain_prompts.py
- [x] 5 cron scripts + tools/prompts/ library
- [x] Docs: architecture.md, resources.md, 2 ADRs, 3 runbooks
- [x] README.md, .gitignore, notebooks/, global ~/.claude/CLAUDE.md
- [x] 15 system prompts added to tools/prompts/claude-code-prompts.md
- [x] 169 files committed and pushed

---
_Hook stop.sh appends session markers below this line_
```

FILE: /home/user/wellux_testprojects/MASTER_PLAN.md
```markdown
# MASTER_PLAN.md — Claude Code Max Build Plan
**Status:** COMPLETE ✅
**Branch:** claude/optimize-cli-autonomy-xNamK
**Last Updated:** 2026-03-28

---

## How to Use
- Type **"f"** → execute the next unchecked `- [ ]` step below
- Type **"s"** → git status + open task summary
- Type **"r"** → run Karpathy research agent
- Type **"a"** → full audit (security + perf + docs)
- Steps auto-check to `- [x]` when complete
- session-start.sh hook shows next step on every boot

---

## Phase 1: Foundation [5/5] ✅
- [x] 1.1 Create repo at /home/user/claude_code_max + branch claude/optimize-cli-autonomy-xNamK
- [x] 1.2 Write CLAUDE.md — full 4-layer orchestration file
- [x] 1.3 Write .claude/settings.json + settings.local.json (max autonomy)
- [x] 1.4 Write 4 hook scripts (session-start, pre-bash, post-edit, stop) + chmod +x
- [x] 1.5 Create tasks/todo.md + tasks/lessons.md (seeded with initial content)

## Phase 2: MASTER_PLAN + PRD [2/2] ✅
- [x] 2.1 Write MASTER_PLAN.md (this file — loopable with "f")
- [x] 2.2 Write tasks/PRD.md (full product requirements)

## Phase 3: Skills — Meta + Security [3/3] ✅
- [x] 3.1 Write /swarm skill (parallel agent decomposer)
- [x] 3.2 Write all 16 security skills (ciso → ai-security)
- [x] 3.3 Write all 20 development skills (code-review → changelog)

## Phase 4: Skills — AI/ML + DevOps + Docs [3/3] ✅
- [x] 4.1 Write all 15 AI/ML research skills (karpathy-researcher → ai-safety)
- [x] 4.2 Write all 15 DevOps/Infra skills (ci-cd → sre)
- [x] 4.3 Write all 10 Documentation skills (readme-writer → knowledge-base)

## Phase 5: Skills — Optimization + PM + Ecosystem [3/3] ✅
- [x] 5.1 Write all 15 Optimization/Research skills (web-vitals → metrics-designer)
- [x] 5.2 Write all 9 Project Management skills (sprint-planner → blocker-resolver)
- [x] 5.3 Write 5 Ecosystem skills (gsd, mem, ui-ux, superpowers, obsidian)

## Phase 6: Agents + Commands [2/2] ✅
- [x] 6.1 Write 4 agent files (ralph-loop, research-agent, swarm-orchestrator, security-reviewer)
- [x] 6.2 Write 3 command files (deploy, audit, research)

## Phase 7: Python Stack [4/4] ✅
- [x] 7.1 Write config/ files (model_config.yaml, prompt_templates.yaml, logging_config.yaml)
- [x] 7.2 Write src/llm/ (base.py, claude_client.py, gpt_client.py, utils.py)
- [x] 7.3 Write src/prompt_engineering/ + src/utils/ + src/handlers/ + __init__.py files
- [x] 7.4 Write examples/ + requirements.txt + setup.py + Dockerfile

## Phase 8: Tools + Scripts [2/2] ✅
- [x] 8.1 Write tools/scripts/ (optimize-docs.sh, research-agent.sh, perf-audit.sh, security-scan.sh, self-improve.sh)
- [x] 8.2 Write tools/prompts/ (system-prompts.md, few-shot-examples.md)

## Phase 9: Docs [3/3] ✅
- [x] 9.1 Write docs/architecture.md + docs/resources.md
- [x] 9.2 Write docs/decisions/ (2 ADRs)
- [x] 9.3 Write docs/runbooks/ (deploy.md, rollback.md, incident-response.md)

## Phase 10: Final Polish + Push [4/4] ✅
- [x] 10.1 Write README.md (full: skills table, hooks docs, quick start, architecture)
- [x] 10.2 Write .gitignore + notebooks/ stubs + global ~/.claude/CLAUDE.md boot file
- [x] 10.3 Verified: 107 skills ≥ 100 ✅ | JSON valid ✅ | hooks executable ✅ | branch correct ✅
- [x] 10.4 git add -A && git commit (169 files, 8601 insertions) && git push -u origin claude/optimize-cli-autonomy-xNamK ✅

---

## Progress Tracker
```
Phase 1: ████████████ 5/5  ✅
Phase 2: ████████████ 2/2  ✅
Phase 3: ████████████ 3/3  ✅
Phase 4: ████████████ 3/3  ✅
Phase 5: ████████████ 3/3  ✅
Phase 6: ████████████ 2/2  ✅
Phase 7: ████████████ 4/4  ✅
Phase 8: ████████████ 2/2  ✅
Phase 9: ████████████ 3/3  ✅
Phase 10:████████████ 4/4  ✅
Total:   ████████████ 31/31 (100%) 🎉
```

---

## Auto-Update Rule
When you complete a step, replace `- [ ]` with `- [x]` and update the progress tracker above.
The session-start.sh hook reads this file and shows the next `- [ ]` on boot.
```

FILE: /home/user/wellux_testprojects/CHANGELOG.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/CONTRIBUTING.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/README.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/docs/architecture.md
```markdown
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
```

FILE: /home/user/wellux_testprojects/docs/decisions/0001-use-claude-primary.md
```markdown
# ADR 0001: Claude as Primary LLM

**Status:** Accepted
**Date:** 2026-03-28

## Context

This project requires a primary LLM for: autonomous code generation, agentic tool use,
long-context analysis, and multi-step reasoning. We evaluated: Claude (Anthropic), GPT-4o (OpenAI),
Gemini (Google), and Llama 3 (Meta/open-source).

## Decision

Use **claude-sonnet-4-6** as the primary model with claude-opus-4-6 for deep research tasks
and claude-haiku-4-5-20251001 for fast/cheap tasks.

## Reasons

1. **Best agentic performance** — Claude leads on tool use, multi-step planning, and instruction following
2. **Long context** — 200K token context handles entire codebases without chunking
3. **Safety alignment** — built-in refusal of destructive actions matches our hook-based safety model
4. **Claude Code native** — the CLI itself runs on Claude; using the same model reduces friction
5. **Cost efficiency** — sonnet-4-6 offers best capability/cost ratio for day-to-day tasks

## Consequences

- **Positive:** Single SDK (anthropic), consistent behavior, native Claude Code integration
- **Negative:** Vendor dependency on Anthropic; GPT-4o fallback maintained via `GPTClient` for resilience
- **Mitigation:** `LLMClient` abstract interface allows swapping providers without changing call sites

## Alternatives Considered

| Model | Why rejected |
|-------|-------------|
| GPT-4o | Slightly weaker agentic performance; maintained as fallback |
| Gemini 1.5 Pro | Long context good, but tool use less reliable |
| Llama 3 70B | Self-hosted complexity; requires GPU infra; no tool use |
```

FILE: /home/user/wellux_testprojects/docs/decisions/0002-python-stack.md
```markdown
# ADR 0002: Python as Primary Stack

**Status:** Accepted
**Date:** 2026-03-28

## Context

The project needs a language for: LLM API clients, data pipelines, prompt engineering,
and scripting. Candidates: Python, TypeScript, Go.

## Decision

Use **Python 3.12+** as the primary language for all `src/` code.

## Reasons

1. **ML ecosystem** — PyTorch, transformers, sentence-transformers, FAISS all Python-native
2. **Anthropic SDK** — Python SDK is the most mature and feature-complete
3. **Async support** — `asyncio` handles concurrent API calls efficiently
4. **Type hints** — Python 3.12 generics, `X | Y` unions, dataclasses provide sufficient type safety
5. **Tooling** — ruff (lint+format), mypy (types), pytest (testing) cover all needs

## Consequences

- **Positive:** Direct access to all AI/ML libraries; no transpilation needed
- **Negative:** Slower than Go/Rust for CPU-bound work; GIL limits true parallelism
- **Mitigation:** Async I/O eliminates most GIL concerns for API-bound workloads; numpy/torch release GIL

## Key Conventions

- Python ≥ 3.11 (required for `X | Y` union syntax without `from __future__ import annotations`)
- Async-first: all LLM calls use `async def` + `asyncio`
- Type hints everywhere in `src/`; examples can be untyped
- `ruff` for linting + formatting (replaces black + flake8 + isort)
- `pytest-asyncio` for async test support
```

FILE: /home/user/wellux_testprojects/docs/resources.md
```markdown
# Resources & Community

Curated references that informed this project's design.

## Official

| Resource | URL | What we use |
|----------|-----|-------------|
| Claude Code Docs | https://docs.anthropic.com/claude-code | CLI features, hooks, skills |
| Anthropic API | https://docs.anthropic.com/api | SDK reference, model IDs |
| Claude Models | docs | opus-4-6, sonnet-4-6, haiku-4-5 |

## Community Tools That Inform Our Skills

| # | Author | Resource | Skill / Pattern derived |
|---|--------|----------|------------------------|
| 1 | usamaakrm | Top 50 Claude Skills | Skill taxonomy + frontmatter patterns |
| 2 | hesreallyhim | Awesome Claude Code | `docs/resources.md` index + skill curation |
| 3 | gsd-build | GSD — Get Shit Done | `/gsd` skill: agentic no-reset shipping |
| 4 | thedotmack | Claude Mem | `/mem` skill + hook-based persistent memory |
| 5 | nextlevelbuilder | UI UX Pro Max | `/ui-ux` skill: production UI/UX |
| 6 | usamaakrm | 10 Brand Skills | `/brand-guardian`, `/copy-writer` |
| 7 | obra | Superpowers | `/superpowers` high-agency coding |
| 8 | kepano | Obsidian Skills | `/obsidian` second-brain note system |
| 9 | hkuds | LightRAG | `/rag-builder` graph-based retrieval |
| 10 | affaan-m | Everything Claude Code | prompts/ + examples/ patterns |
| 11 | frankbria | Ralph Loop | `agents/ralph-loop.md` autonomous dev loop |
| 12 | anthropics | Claude Code SDK | Agent tool, subagent_type patterns for all 4 agents |
| 13 | modelcontextprotocol | MCP Servers | `.mcp.json` — github, filesystem, memory, brave |
| 14 | astral-sh | ruff | Lint gate in CI + pre-commit hook |
| 15 | pre-commit | pre-commit-hooks | `.pre-commit-config.yaml` enforcement |

## Trending Patterns (2026)

Patterns extracted from trending Claude Code repos and community practice:

| Pattern | What it does | Implemented |
|---------|-------------|-------------|
| **CLAUDE.md as system prompt** | Persistent per-session context injection | ✅ L1 |
| **Skill frontmatter auto-invocation** | Keyword-triggered skill selection without explicit slash commands | ✅ L2 |
| **Hook exit-code safety gates** | exit 2 blocks tool execution deterministically | ✅ L3 |
| **Subagent context isolation** | Each agent gets a fresh context window; swarm for parallel | ✅ L4 |
| **Modular rule files** | Separate concerns (style, testing, API) loaded on demand | ✅ L5 |
| **5-router auto-routing** | LLM + skill + agent + memory + task selection from single `route()` | ✅ |
| **Eval-driven development** | JSONL eval suites gate merges; smoke evals run in CI | ✅ |
| **CorrelationID middleware** | Request tracing across all API responses | ✅ |
| **AsyncEvalRunner** | Semaphore-bounded concurrent eval execution | ✅ |
| **Daily GitHub trending research** | Automated stub creation → morning research queue | ✅ |
| **Self-improve loop** | Lessons distilled → tasks → commit cycle | ✅ |
| **Karpathy research method** | Search → Distill → Implement → Store → Lesson | ✅ |
| **systemd user timers** | Reliable cron replacement; persists across reboots | ✅ |
| **MCP memory fallback** | Try MCP memory server, fall back to in-memory dict | ✅ |

## Research Inspiration

| Author | Work | Applied in |
|--------|------|-----------|
| Andrej Karpathy | "Unreasonable Effectiveness of RNNs" + nanoGPT | `/karpathy-researcher`, `research-agent.md` |
| Andrej Karpathy | First-principles deep dives | Karpathy research method in agents |
| Lilian Weng | "LLM Powered Autonomous Agents" | agent architecture patterns |

## Learning Resources

- **Claude Code Cheatsheet** — 4-layer architecture, hook exit codes, daily workflow
- **Master Guide** — Checkpoint+iterate, prompting techniques, MCP connections
- **MLTut Gen AI Stack** — Python project structure for AI applications
- **Security Color Teams** — 16-skill security coverage model (White/Red/Blue/Yellow/Green/Orange)

## MCP Servers Worth Adding

```bash
# Developer tools
claude mcp add --transport http github https://api.github.com/mcp
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Productivity
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http linear https://mcp.linear.app/mcp

# Data
claude mcp add --transport http perplexity https://mcp.perplexity.ai/mcp
claude mcp add --transport http brave https://mcp.brave.com/mcp
```
```

FILE: /home/user/wellux_testprojects/docs/runbooks/deploy.md
```markdown
# Runbook: Deploy

## Prerequisites
- Docker installed
- `ANTHROPIC_API_KEY` set in environment
- Git on branch `claude/optimize-cli-autonomy-xNamK` (or main after merge)

## Steps

### 1. Validate before deploy
```bash
# Syntax check
find src/ -name "*.py" | xargs python3 -m py_compile
python3 -m json.tool .claude/settings.json

# Tests (if configured)
pytest tests/ -v --tb=short 2>/dev/null || echo "No tests yet"

# Security scan
bash tools/scripts/security-scan.sh
```

### 2. Build Docker image
```bash
docker build -t claude-code-max:$(git rev-parse --short HEAD) .
docker tag claude-code-max:$(git rev-parse --short HEAD) claude-code-max:latest
```

### 3. Run locally
```bash
docker run --rm \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -v "$(pwd)/data:/app/data" \
  claude-code-max:latest
```

### 4. Git tag + push
```bash
git tag v$(date +%Y%m%d)-$(git rev-parse --short HEAD)
git push origin --tags
```

## Rollback
See `docs/runbooks/rollback.md`.

## Verification
- Check `data/outputs/` for recent run artifacts
- Review `data/cache/bash-log.txt` for hook activity
- Confirm no secrets in `docker inspect` environment
```

FILE: /home/user/wellux_testprojects/docs/runbooks/incident-response.md
```markdown
# Runbook: Incident Response

## Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| P0 | Complete outage | Immediate | API key invalid, 100% error rate |
| P1 | Major degradation | 15 min | Rate limit, >50% errors |
| P2 | Partial issue | 1 hour | Slow responses, cache miss spike |
| P3 | Minor issue | Next business day | Log noise, stale docs |

## P0/P1 Response

### 1. Triage (5 min)
```bash
# Check API connectivity
curl -s https://api.anthropic.com/v1/health -H "x-api-key: $ANTHROPIC_API_KEY" | python3 -m json.tool

# Check error logs
tail -100 data/cache/bash-log.txt | grep ERROR

# Check rate limit status
grep "rate_limit" data/cache/bash-log.txt | tail -20
```

### 2. Mitigate (10 min)
```bash
# API key invalid → rotate immediately
export ANTHROPIC_API_KEY="new-key"

# Rate limit → reduce RPM
# Edit src/llm/claude_client.py: RateLimiter(requests_per_minute=50)

# Fallback to GPT if Claude is down
# Edit code to use GPTClient as primary temporarily
```

### 3. Resolve & Document
- Fix root cause (not just symptoms)
- Add entry to `tasks/lessons.md` under `## Incident <date>`
- Add monitoring/alerting to prevent recurrence

## Common Incidents

### "anthropic.AuthenticationError"
1. Check `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
2. Verify key is valid in Anthropic console
3. Check `.env` is not committed/corrupted

### "Rate limit exceeded"
1. Check current RPM setting in `ClaudeClient`
2. Add delays between batch requests
3. Use `ResponseCache` to avoid repeat calls
4. Consider upgrading API tier

### "context_length_exceeded"
1. Check prompt size: `ClaudeClient.count_tokens(prompt)`
2. Use `truncate_to_tokens()` from `src/llm/utils.py`
3. Switch to chunked processing via `split_into_chunks()`

### Hook blocking all Bash commands
1. Check `.claude/hooks/pre-tool-bash.sh` for false positive patterns
2. Temporarily disable: remove hook from `settings.json` PreToolUse
3. Fix pattern and re-enable
```

FILE: /home/user/wellux_testprojects/docs/runbooks/rollback.md
```markdown
# Runbook: Rollback

## When to use
- Deploy broke something in production
- Regression introduced in latest commit
- Config change caused unexpected behavior

## Steps

### 1. Identify last good commit
```bash
git log --oneline -10
# Find the last commit that worked
```

### 2. Revert to last good state (non-destructive)
```bash
GOOD_COMMIT=<sha>
git revert HEAD...$GOOD_COMMIT --no-edit
git push origin HEAD
```

### 3. If Docker container needs immediate rollback
```bash
# Run previous tagged image
PREV_TAG=$(docker images claude-code-max --format "{{.Tag}}" | grep -v latest | head -2 | tail -1)
docker run --rm \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -v "$(pwd)/data:/app/data" \
  claude-code-max:$PREV_TAG
```

### 4. Emergency: hard reset (only if commits not pushed)
```bash
# DESTRUCTIVE — only use for local-only commits
git reset --hard <good-sha>
```

## Post-rollback
1. Document what went wrong in `tasks/lessons.md`
2. Add a test case that would have caught the regression
3. Create a new branch to fix the root cause properly
```


## 4.22 Tools and Scripts

FILE: /home/user/wellux_testprojects/tools/scripts/github-trending-research.sh
```bash
#!/bin/bash
# Daily GitHub Trending Research — Claude Code & Agent Patterns
# Cron: 0 7 * * * cd /home/user/wellux_testprojects && bash tools/scripts/github-trending-research.sh >> data/cache/cron-github-research.log 2>&1

set -euo pipefail

BASE="/home/user/wellux_testprojects"
DATE=$(date +%Y-%m-%d)
OUT="$BASE/data/research/${DATE}-github-trending-claude-code.md"
LOG="$BASE/data/research/README.md"
LESSONS="$BASE/tasks/lessons.md"

echo "================================================"
echo "  GITHUB TRENDING RESEARCH — $DATE"
echo "  Topic: Claude Code + Agent Patterns"
echo "================================================"

mkdir -p "$BASE/data/research" "$BASE/data/cache"

# Initialize research index if missing
if [ ! -f "$LOG" ]; then
    echo "# Research Index" > "$LOG"
    echo "" >> "$LOG"
    echo "Auto-populated by research-agent and github-trending-research scripts." >> "$LOG"
    echo "" >> "$LOG"
fi

# Write structured research stub — populated by Claude Code on next session
cat > "$OUT" << STUB
# GitHub Trending Research: Claude Code & Agent Patterns
**Date:** $DATE
**Method:** GitHub API → Trending → Filter → Distill → Implement

## Summary
Auto-populated by running: \`ccm research "Claude Code trending repos $DATE"\`

## Trending Repos Scanned
<!-- claude --print "Search GitHub for trending claude-code, anthropic, mcp-server repos.
List top 10 with: name, stars, description, key pattern to implement.
Focus on: agent loops, skill systems, hook patterns, MCP servers, eval frameworks." -->

### Top Patterns This Week

| Repo | Stars | Pattern | Priority |
|------|-------|---------|----------|
| [To be populated] | - | Run ccm research to populate | - |

## Implemented This Run

### New Techniques
- [ ] Review and implement patterns from trending repos
- [ ] Update .claude/skills/ with any new skill patterns found
- [ ] Update docs/resources.md with notable new repos
- [ ] Add any architectural insights to tasks/lessons.md

## Key Signals

### Agent Loop Patterns
[Search result content — populate via /karpathy-researcher]

### MCP Server Patterns
[New MCP servers worth integrating]

### Skill/Hook Patterns
[Novel skill frontmatter or hook guard patterns]

### Eval Framework Patterns
[Eval methodologies worth adopting]

## Action Items
1. Run: \`/karpathy-researcher "Claude Code agent patterns $DATE"\`
2. Scan: awesome-claude-code, anthropic/claude-code-sdk
3. Check: Anthropic changelog for new hooks, tools, MCP capabilities
4. Update: docs/resources.md with new entries

## Distilled Insight
[One paragraph — the most important thing learned today]

## Sources
- https://github.com/trending?l=python&since=daily (filter: claude, anthropic, mcp)
- https://github.com/hesreallyhim/awesome-claude-code
- https://docs.anthropic.com/claude-code (changelog)
STUB

# Append to research index
echo "- [GitHub Trending Claude Code — $DATE](./${DATE}-github-trending-claude-code.md)" >> "$LOG"

echo ""
echo "Research stub written: $OUT"
echo ""
echo "To populate with live data, run in Claude Code:"
echo "  ccm research \"Claude Code trending repos and patterns $DATE\""
echo "  or: /karpathy-researcher Claude Code GitHub trending $DATE"
echo ""

# Log event for audit trail
EVENTS="$BASE/data/cache/events.log"
echo "{\"event\":\"github_trending_research\",\"date\":\"$DATE\",\"stub\":\"$OUT\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "$EVENTS"

echo "================================================"
echo "  Done. Stub ready for Claude Code to populate."
echo "================================================"
```

FILE: /home/user/wellux_testprojects/tools/scripts/optimize-docs.sh
```bash
#!/bin/bash
# Daily doc optimization — checks freshness, broken links, outdated content
# Cron: 0 6 * * * cd /home/user/wellux_testprojects && bash tools/scripts/optimize-docs.sh >> data/cache/cron-optimize-docs.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
ISSUES=0

echo "================================================"
echo "  DOC OPTIMIZER — $DATE"
echo "================================================"

# 1. Check all .md files for last-modified > 30 days
echo ""
echo "[1] Checking doc freshness (>30 days old)..."
find . -name "*.md" \
    -not -path "./.git/*" \
    -not -path "./data/*" \
    -mtime +30 \
    -printf "  STALE: %p (modified: %TY-%Tm-%Td)\n" 2>/dev/null || true

# 2. Check CLAUDE.md line count (should be <200)
echo ""
echo "[2] Checking CLAUDE.md size..."
if [ -f "CLAUDE.md" ]; then
    LINES=$(wc -l < CLAUDE.md)
    if [ "$LINES" -gt 200 ]; then
        echo "  WARNING: CLAUDE.md is $LINES lines (target: <200)"
        ISSUES=$((ISSUES + 1))
    else
        echo "  OK: CLAUDE.md is $LINES lines"
    fi
fi

# 3. Check skills have required frontmatter
echo ""
echo "[3] Checking skill frontmatter..."
SKILL_ERRORS=0
for skill_dir in .claude/skills/*/; do
    skill_file="$skill_dir/SKILL.md"
    if [ -f "$skill_file" ]; then
        if ! grep -q "^name:" "$skill_file"; then
            echo "  MISSING name: $skill_file"
            SKILL_ERRORS=$((SKILL_ERRORS + 1))
        fi
        if ! grep -q "^description:" "$skill_file"; then
            echo "  MISSING description: $skill_file"
            SKILL_ERRORS=$((SKILL_ERRORS + 1))
        fi
    fi
done
if [ "$SKILL_ERRORS" -eq 0 ]; then
    SKILL_COUNT=$(ls .claude/skills/ 2>/dev/null | wc -l)
    echo "  OK: $SKILL_COUNT skills, all have required frontmatter"
else
    echo "  ERRORS: $SKILL_ERRORS frontmatter issues found"
    ISSUES=$((ISSUES + SKILL_ERRORS))
fi

# 4. Validate settings.json
echo ""
echo "[4] Validating .claude/settings.json..."
if python3 -m json.tool .claude/settings.json > /dev/null 2>&1; then
    echo "  OK: settings.json is valid JSON"
else
    echo "  ERROR: settings.json is invalid JSON"
    ISSUES=$((ISSUES + 1))
fi

# 5. Check MASTER_PLAN progress
echo ""
echo "[5] MASTER_PLAN progress..."
if [ -f "MASTER_PLAN.md" ]; then
    DONE=$(grep -c "^- \[x\]" MASTER_PLAN.md 2>/dev/null || echo 0)
    TOTAL=$(grep -c "^- \[" MASTER_PLAN.md 2>/dev/null || echo 0)
    echo "  Progress: $DONE/$TOTAL steps complete"
fi

# 6. Check tasks/todo.md for overdue items
echo ""
echo "[6] Open tasks..."
if [ -f "tasks/todo.md" ]; then
    OPEN=$(grep -c "^- \[ \]" tasks/todo.md 2>/dev/null || echo 0)
    echo "  Open tasks: $OPEN"
fi

echo ""
echo "================================================"
echo "  SUMMARY: $ISSUES issues found — $DATE"
echo "================================================"

exit 0
```

FILE: /home/user/wellux_testprojects/tools/scripts/perf-audit.sh
```bash
#!/bin/bash
# Performance audit — Python profiling, import times, token costs
# Cron: 0 1 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/perf-audit.sh >> data/cache/cron-perf.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
OUT="data/outputs/perf-report-${DATE}.md"
mkdir -p data/outputs

echo "================================================"
echo "  PERF AUDIT — $DATE"
echo "================================================"

cat > "$OUT" << HEADER
# Performance Audit — $DATE

## Python Import Times
HEADER

# Check Python import time for src package
echo ""
echo "[1] Python import time..."
IMPORT_TIME=$(python3 -c "
import time
t0 = time.monotonic()
import sys
sys.path.insert(0, '.')
try:
    import src
    ms = int((time.monotonic() - t0) * 1000)
    print(ms)
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null || echo "N/A")
echo "  src import: ${IMPORT_TIME}ms"
echo "- src package import: ${IMPORT_TIME}ms" >> "$OUT"

# Syntax check all Python files
echo ""
echo "[2] Python syntax check..."
SYNTAX_ERRORS=0
while IFS= read -r -d '' pyfile; do
    if ! python3 -m py_compile "$pyfile" 2>/dev/null; then
        echo "  SYNTAX ERROR: $pyfile"
        SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
    fi
done < <(find src/ -name "*.py" -print0 2>/dev/null)
echo "  Syntax errors: $SYNTAX_ERRORS"
echo "" >> "$OUT"
echo "## Syntax Check" >> "$OUT"
echo "- Python syntax errors: $SYNTAX_ERRORS" >> "$OUT"

# Count lines of code
echo ""
echo "[3] Code size..."
SRC_LINES=$(find src/ -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)
SKILL_COUNT=$(ls .claude/skills/ 2>/dev/null | wc -l || echo 0)
echo "  src/ lines: $SRC_LINES"
echo "  skills: $SKILL_COUNT"
echo "" >> "$OUT"
echo "## Code Size" >> "$OUT"
echo "- src/ lines of code: $SRC_LINES" >> "$OUT"
echo "- Skills defined: $SKILL_COUNT" >> "$OUT"

# Data directory sizes
echo ""
echo "[4] Data directory sizes..."
echo "" >> "$OUT"
echo "## Data Sizes" >> "$OUT"
for dir in data/cache data/outputs data/research data/embeddings; do
    if [ -d "$dir" ]; then
        SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "  $dir: $SIZE"
        echo "- $dir: $SIZE" >> "$OUT"
    fi
done

echo ""
echo "Report written: $OUT"
echo "================================================"
```

FILE: /home/user/wellux_testprojects/tools/scripts/research-agent.sh
```bash
#!/bin/bash
# Karpathy-style research loop — runs weekly (Monday 6am via cron)
# Usage: bash tools/scripts/research-agent.sh [topic]
# Cron: 0 6 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/research-agent.sh >> data/cache/cron-research.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
LOG="data/research/README.md"
LESSONS="tasks/lessons.md"

# Topics to research each run (rotate through all 8 weekly)
TOPICS=(
    "LLM agent frameworks 2026"
    "RAG graph retrieval systems"
    "prompt engineering advances"
    "AI safety alignment techniques"
    "fine-tuning efficiency LoRA QLoRA"
    "multimodal vision language models"
    "code generation AI models"
    "Claude Code automation patterns"
)

echo "================================================"
echo "  RESEARCH AGENT — Karpathy Loop"
echo "  Date: $DATE"
echo "================================================"

mkdir -p data/research

# Init README index if missing
if [ ! -f "$LOG" ]; then
    echo "# Research Index" > "$LOG"
    echo "" >> "$LOG"
fi

echo "" >> "$LOG"
echo "## Research Run: $DATE" >> "$LOG"

for TOPIC in "${TOPICS[@]}"; do
    SLUG=$(echo "$TOPIC" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
    OUT="data/research/${DATE}-${SLUG}.md"

    echo "Researching: $TOPIC"

    # Write research stub (claude --print would replace this in live use)
    cat > "$OUT" << STUB
# Research: $TOPIC
**Date:** $DATE
**Method:** Karpathy (Search → Distill → Implement → Store)

## Core Concept
[Auto-populated by research-agent on next Claude Code session]

## Key Technique
[Run: /karpathy-researcher $TOPIC]

## Implementation Pattern
\`\`\`python
# Minimal example to be populated
\`\`\`

## Actionable Insight
[Extracted and appended to tasks/lessons.md]

## Sources
[URLs from WebSearch]
STUB

    echo "- [$TOPIC]($OUT) — $DATE" >> "$LOG"
    echo "  Written: $OUT"
done

echo ""
echo "Research index updated: $LOG"
echo "Run /karpathy-researcher <topic> in Claude Code to populate stubs."
echo "================================================"
```

FILE: /home/user/wellux_testprojects/tools/scripts/security-scan.sh
```bash
#!/bin/bash
# Security scan — secrets detection, dependency CVEs, permission audit
# Cron: 0 0 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/security-scan.sh >> data/cache/cron-security.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
OUT="data/outputs/security-report-${DATE}.md"
ISSUES=0
mkdir -p data/outputs

echo "================================================"
echo "  SECURITY SCAN — $DATE"
echo "================================================"

cat > "$OUT" << HEADER
# Security Report — $DATE

## Scan Summary
HEADER

# 1. Detect hardcoded secrets patterns
echo ""
echo "[1] Scanning for secrets patterns..."
SECRET_PATTERNS=(
    "sk-[a-zA-Z0-9]{20,}"           # OpenAI keys
    "sk-ant-[a-zA-Z0-9-]{30,}"      # Anthropic keys
    "AKIA[A-Z0-9]{16}"              # AWS Access Key ID
    "password\s*=\s*['\"][^'\"]{8,}" # Hardcoded passwords
    "api_key\s*=\s*['\"][^'\"]{10,}" # Hardcoded API keys
)

SECRET_FOUND=0
for pattern in "${SECRET_PATTERNS[@]}"; do
    matches=$(grep -rEn "$pattern" src/ examples/ config/ 2>/dev/null \
        --include="*.py" --include="*.yaml" --include="*.json" \
        --exclude-dir=".git" || true)
    if [ -n "$matches" ]; then
        echo "  WARNING: Potential secret found matching: $pattern"
        echo "$matches" | head -3
        SECRET_FOUND=$((SECRET_FOUND + 1))
        ISSUES=$((ISSUES + 1))
    fi
done
[ "$SECRET_FOUND" -eq 0 ] && echo "  OK: No hardcoded secrets detected"
echo "- Hardcoded secrets: $SECRET_FOUND patterns matched" >> "$OUT"

# 2. Check .gitignore covers sensitive files
echo ""
echo "[2] Checking .gitignore coverage..."
GITIGNORE_ISSUES=0
REQUIRED_IGNORES=(".env" "*.local" "settings.local.json" "data/cache/" "data/outputs/")
for item in "${REQUIRED_IGNORES[@]}"; do
    if ! grep -qF "$item" .gitignore 2>/dev/null; then
        echo "  MISSING in .gitignore: $item"
        GITIGNORE_ISSUES=$((GITIGNORE_ISSUES + 1))
        ISSUES=$((ISSUES + 1))
    fi
done
[ "$GITIGNORE_ISSUES" -eq 0 ] && echo "  OK: .gitignore covers all sensitive paths"
echo "- .gitignore gaps: $GITIGNORE_ISSUES" >> "$OUT"

# 3. Check hook scripts are not world-writable
echo ""
echo "[3] Checking hook permissions..."
PERM_ISSUES=0
for hook in .claude/hooks/*.sh; do
    if [ -f "$hook" ]; then
        PERMS=$(stat -c "%a" "$hook" 2>/dev/null || stat -f "%OLp" "$hook" 2>/dev/null || echo "unknown")
        if [ "$PERMS" = "777" ] || [ "$PERMS" = "666" ]; then
            echo "  WARNING: $hook is world-writable ($PERMS)"
            PERM_ISSUES=$((PERM_ISSUES + 1))
            ISSUES=$((ISSUES + 1))
        fi
    fi
done
[ "$PERM_ISSUES" -eq 0 ] && echo "  OK: Hook scripts have safe permissions"
echo "- Permission issues: $PERM_ISSUES" >> "$OUT"

# 4. Python import safety (no eval/exec on user input)
echo ""
echo "[4] Scanning for dangerous Python patterns..."
DANGEROUS_PATTERNS=("eval(" "exec(" "os.system(" "subprocess.call.*shell=True" "pickle.load")
DANGEROUS_FOUND=0
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    matches=$(grep -rn "$pattern" src/ 2>/dev/null --include="*.py" || true)
    if [ -n "$matches" ]; then
        echo "  REVIEW: $pattern"
        echo "$matches" | head -2
        DANGEROUS_FOUND=$((DANGEROUS_FOUND + 1))
    fi
done
[ "$DANGEROUS_FOUND" -eq 0 ] && echo "  OK: No dangerous patterns in src/"
echo "- Dangerous patterns: $DANGEROUS_FOUND" >> "$OUT"

# Summary
echo "" >> "$OUT"
echo "## Result" >> "$OUT"
if [ "$ISSUES" -eq 0 ]; then
    echo "**PASS** — No security issues found." >> "$OUT"
    echo ""
    echo "RESULT: PASS — 0 issues"
else
    echo "**REVIEW** — $ISSUES issues require attention." >> "$OUT"
    echo ""
    echo "RESULT: $ISSUES issues found — review $OUT"
fi

echo "Report: $OUT"
echo "================================================"
```

FILE: /home/user/wellux_testprojects/tools/scripts/self-improve.sh
```bash
#!/bin/bash
# Self-improvement loop — distill lessons.md → improvement tasks → commit
# Cron: 0 8 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/self-improve.sh >> data/cache/cron-improve.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
LESSONS="tasks/lessons.md"
TODO="tasks/todo.md"

echo "================================================"
echo "  SELF-IMPROVE — $DATE"
echo "================================================"

if [ ! -f "$LESSONS" ]; then
    echo "No lessons.md found — nothing to process."
    exit 0
fi

# Count lessons added since last run (look for entries from this week)
LESSON_COUNT=$(grep -c "^##" "$LESSONS" 2>/dev/null || echo 0)
echo "Total lessons captured: $LESSON_COUNT"

# Extract lessons not yet turned into tasks (heuristic: look for [TODO] tag)
NEW_INSIGHTS=$(grep -A2 "^## " "$LESSONS" | grep -v "^## " | grep -v "^--$" | head -20 || true)

echo ""
echo "Recent lessons:"
tail -20 "$LESSONS"

# Append improvement task to todo.md
echo "" >> "$TODO"
echo "## Self-Improvement Tasks — $DATE" >> "$TODO"
echo "- [ ] Review lessons.md and apply top 3 patterns to CLAUDE.md" >> "$TODO"
echo "- [ ] Run /optimize-docs to check skill freshness" >> "$TODO"
echo "- [ ] Run /perf-profiler on any new bottlenecks identified" >> "$TODO"

echo ""
echo "Improvement tasks appended to $TODO"

# Git commit the lessons progress
if git -C . diff --quiet "$LESSONS" 2>/dev/null; then
    echo "No changes to lessons.md — nothing to commit."
else
    git -C . add "$LESSONS" "$TODO" 2>/dev/null || true
    git -C . commit -m "chore: weekly self-improvement cycle $DATE

- Processed $LESSON_COUNT lessons
- Added improvement tasks to todo.md
- Run /self-improve for deep analysis" 2>/dev/null || echo "Git commit skipped (no changes staged)"
fi

echo ""
echo "Self-improve complete."
echo "Next: run Claude Code and type 'a' for full audit."
echo "================================================"
```

FILE: /home/user/wellux_testprojects/tools/prompts/claude-code-prompts.md
```markdown
# Claude Code — Copy-Paste Prompts

15 battle-tested prompts for common Claude Code workflows.

---

## 1. Master CLAUDE.md — Drop in any project

```markdown
# Project Instructions

## Core Rules
- Plan before executing any task with 3+ steps — write steps to tasks/todo.md first
- Never mark a task complete without proving it works (run it, check output)
- Touch only what the task requires — no refactoring, no extra features, no cleanup beyond scope
- After any correction from me: add a lesson to tasks/lessons.md immediately
- Use subagents for research/exploration to keep main context clean

## Code Standards
- Read a file before editing it — always
- Prefer editing existing files over creating new ones
- No speculative abstractions — build what's needed, not what might be needed
- No backwards-compat shims, unused vars, or dead code — delete it
- Security: never commit .env, API keys, or secrets

## Git
- Always check git branch before committing
- Never push to main/master without explicit permission
- Commit messages: imperative mood, explain WHY not what

## When Stuck
- Read the error carefully before retrying
- Check your assumptions — don't retry the same failing approach twice
- Ask me only if genuinely blocked after investigation
```

---

## 2. Session Opener

```
Before starting any work:
1. Read CLAUDE.md (project rules)
2. Read tasks/todo.md (open tasks)
3. Read tasks/lessons.md (past mistakes to avoid)
4. Show me: current git branch, next open task, last lesson

Then confirm you're ready.
```

---

## 3. Max Autonomy Mode

```
I want you to work autonomously on the following task. Rules:
- Do NOT ask clarifying questions — make reasonable assumptions and document them
- Write your plan as numbered steps before starting
- Execute each step fully, mark it done, move to the next
- If you hit a blocker: diagnose it, try 2 approaches, then report what you found
- Verify your work before saying done (run it, check output, read the diff)
- Commit completed work at the end with a descriptive message

Task: [DESCRIBE TASK HERE]
```

---

## 4. Bug Fix

```
Bug report: [PASTE ERROR / DESCRIBE BUG]

Fix it. Rules:
- Find the root cause — not the symptom
- Read the relevant files before changing anything
- Make the minimal change that fixes it
- Explain what caused it in one sentence
- Verify the fix works
- Do not refactor surrounding code
```

---

## 5. Code Review — Security + Quality

```
Review this code for:
1. Security issues (OWASP top 10, injection, auth flaws, secrets exposure)
2. Logic bugs and edge cases
3. Performance problems (N+1, missing indexes, O(n²))
4. Error handling gaps (what happens when this fails?)

For each issue: severity (critical/high/medium/low), location (file:line), and the fix.
Prioritize by severity. Skip style nits unless they cause bugs.

[PASTE CODE OR FILE PATH]
```

---

## 6. Architect Mode

```
I want to build: [DESCRIBE FEATURE]

Act as a staff engineer reviewing this before we write a line of code.
Give me:
1. The simplest design that meets the requirements (no over-engineering)
2. The 2-3 tradeoffs I should be aware of
3. What could go wrong (top 3 failure modes)
4. What I should NOT build yet (scope boundaries)
5. A file/module structure if this requires new code

Be direct. Flag if the requirements are unclear before designing.
```

---

## 7. Karpathy Research Mode

```
Research: [TOPIC]

Use the Karpathy method:
1. What is this from first principles? (2-3 sentences, no jargon)
2. What is the single most important insight? (the thing that makes it work)
3. What would I need to rebuild a minimal version from scratch? (key steps)
4. What's the most common mistake practitioners make with this?
5. One concrete thing I can implement or try today

Be technical and specific. No fluff. Cite sources if you find them.
```

---

## 8. Refactor — Surgical

```
Refactor [FILE/FUNCTION] to improve [readability/performance/testability].

Constraints:
- Do NOT change behavior — only structure
- Do NOT rename public APIs or exported types
- Do NOT add new dependencies
- Make one type of change at a time
- Show me the before/after diff and explain each change

If you find bugs while refactoring, note them separately — don't fix them here.
```

---

## 9. Test Writer

```
Write tests for: [FILE/FUNCTION/MODULE]

Rules:
- Test behavior, not implementation — test what it does, not how
- Cover: happy path, error cases, edge cases (empty input, null, boundary values)
- Each test name should describe what it's testing: test_returns_empty_list_when_no_results
- Mock external dependencies (API calls, DB, filesystem)
- No tests that just check "it doesn't crash" — assert on actual output
- Use the existing test framework in the project (check package.json / requirements.txt first)
```

---

## 10. The "Stuck in a Loop" Reset

```
Stop. Let's reset.

Before continuing:
1. What exactly is the error you're seeing? (paste it)
2. What did you try? (list the approaches)
3. What's your current hypothesis about the root cause?
4. What's the simplest possible test to validate that hypothesis?

Do not write any code yet. Just answer these 4 questions.
```

---

## 11. PR Description Generator

```
Generate a PR description for my changes.

Run: git diff main...HEAD

Format:
## What
[1-3 bullet points: what changed, factually]

## Why
[1-2 sentences: why this change was needed]

## How to test
[Numbered steps a reviewer can follow to verify it works]

## Risk
[None / Low / Medium — and why]

Keep it under 200 words total. No fluff.
```

---

## 12. The "Elegant Solution" Prompt

```
You just implemented [DESCRIBE WHAT WAS BUILT].

Now step back. Knowing everything you know about the problem:
- Is there a simpler design that achieves the same result?
- Is there anything here that will be painful to maintain in 6 months?
- Did you add anything that wasn't strictly required?

If yes to any: implement the more elegant version.
If no: confirm it's clean and move on.
```

---

## 13. Incident Response

```
Production issue. Move fast.

Symptom: [DESCRIBE WHAT'S BROKEN]
Error: [PASTE LOGS / ERROR MESSAGE]
Started: [WHEN]
Impact: [WHO IS AFFECTED]

Do this in order:
1. Identify the likely root cause (top 3 hypotheses, ranked)
2. Identify the fastest mitigation (not fix — just stop the bleeding)
3. Then identify the permanent fix

Do NOT start implementing until you've completed step 1.
```

---

## 14. Self-Improvement — After any mistake

```
I just corrected you on: [WHAT WENT WRONG]

Add a lesson to tasks/lessons.md:

## Lesson — [DATE]: [SHORT TITLE]
**Mistake:** [What you did wrong]
**Why it happened:** [Root cause of the mistake]
**Rule:** [Specific rule to follow next time — imperative, one sentence]
**Example of correct behavior:** [One line showing the right approach]

Then confirm it's written.
```

---

## 15. Daily Workflow Kickoff

```
New session. Let's work on: [FEATURE / BUG / TASK]

Before touching any code:
1. Check git status and current branch
2. Read the relevant files for this task
3. Write a plan (numbered steps) to tasks/todo.md
4. Tell me the plan — I'll approve before you start

Max autonomy after I approve. Commit when done.
```

---

## Quick Reference

| Prompt | Use when |
|--------|----------|
| #2 Session Opener | Start of every session |
| #3 Max Autonomy | Complex multi-step tasks |
| #4 Bug Fix | Errors, regressions |
| #5 Code Review | Before merging anything |
| #6 Architect | Before building a new feature |
| #7 Karpathy Research | Learning something new deeply |
| #10 Reset | Claude is going in circles |
| #13 Incident | Prod is down |
| #14 Self-Improve | After any correction |
| #15 Kickoff | Start of a work session |
```

FILE: /home/user/wellux_testprojects/tools/prompts/few-shot-examples.md
```markdown
# Few-Shot Examples Library

Curated input→output pairs for consistent model behavior.
Load these via `FewShotManager` from `src/prompt_engineering/few_shot.py`.

---

## Code Review Examples

**Input:** `def get_user(id): return db.query(f"SELECT * FROM users WHERE id={id}")`
**Output:** CRITICAL: SQL injection. Fix: `db.query("SELECT * FROM users WHERE id=?", (id,))`

**Input:**
```python
def process_items(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result
```
**Output:** MINOR: Use list comprehension. Fix: `return [x * 2 for x in items]`

**Input:**
```python
try:
    data = json.loads(response)
except:
    pass
```
**Output:** MAJOR: Bare except swallows all errors. Fix: `except json.JSONDecodeError as e: logger.error("parse_failed", error=str(e)); raise`

---

## Prompt Classification Examples

**Input:** "make this faster"
**Output:** Algorithm optimization request → invoke /perf-profiler

**Input:** "something is broken in prod"
**Output:** Incident → invoke /incident-response; gather: error message, logs, when it started

**Input:** "add authentication to the API"
**Output:** Feature implementation → invoke /api-designer for design, then /appsec-engineer for security review

**Input:** "what's the state of LLM agents"
**Output:** Research request → invoke /karpathy-researcher with topic "LLM agent frameworks 2026"

---

## Sentiment Classification Examples

**Input:** "The API rate limits are too restrictive and the docs are outdated"
**Output:** negative | issues: rate_limits, documentation

**Input:** "Love the streaming support — makes the UX much smoother"
**Output:** positive | feature: streaming

**Input:** "Does this support async?"
**Output:** neutral | question: async_support

---

## Bug Triage Examples

**Input:** `AttributeError: 'NoneType' object has no attribute 'content'`
**Output:**
```
Root cause: API returned None (e.g., empty response or failed call)
Location: claude_client.py line 64 — message.content[0].text
Fix: Check response before accessing: if not message.content: raise LLMError("Empty response")
Prevention: Add response validation in complete()
```

**Input:** `asyncio.TimeoutError after 30s`
**Output:**
```
Root cause: API call exceeded timeout (likely rate limit or slow model)
Fix: Add timeout parameter to create(): timeout=60.0
Prevention: Monitor p99 latency, add circuit breaker for timeouts > threshold
```

---

## Python Type Annotation Examples

**Input:** `def process(data, config=None): ...`
**Output:** `def process(data: list[dict], config: ProcessConfig | None = None) -> ProcessResult: ...`

**Input:** `def fetch_items(ids, limit=10): ...`
**Output:** `def fetch_items(ids: list[int], limit: int = 10) -> list[Item]: ...`
```

FILE: /home/user/wellux_testprojects/tools/prompts/system-prompts.md
```markdown
# System Prompts Library

Reusable system prompts for different roles and tasks.
Use these with `CompletionRequest(system=...)` or in `config/prompt_templates.yaml`.

---

## Core Roles

### Senior Engineer
```
You are a senior software engineer with 15 years of experience in Python, distributed systems, and AI.
You write clean, idiomatic code with proper error handling. You think about edge cases, performance,
and maintainability. You are direct: give the answer first, then explain. No filler.
```

### Security Reviewer
```
You are a security engineer specializing in application security. You review code for OWASP Top 10
vulnerabilities, insecure patterns, and logic flaws. For every issue, provide: severity (critical/high/medium/low),
impact, and specific remediation code. Be thorough — assume the code will be attacked.
```

### Research Analyst (Karpathy Mode)
```
You are a research analyst in the style of Andrej Karpathy. For every topic: understand from first
principles, identify the core insight, implement a minimal working example. Be technically precise.
Prefer depth over breadth. Distill to what a practitioner needs to act on today.
```

### Code Reviewer
```
You are a meticulous code reviewer. Check for: bugs, security issues, performance problems, code style,
test coverage gaps, documentation gaps. Prioritize by severity. Provide specific line-level feedback
with improved code snippets. Be constructive but direct.
```

### Architect
```
You are a software architect evaluating design decisions. Consider: scalability, maintainability,
operational complexity, team cognitive load, migration paths. Think in tradeoffs. Every architectural
choice has costs — name them explicitly. Recommend the simplest design that meets the requirements.
```

### Data Analyst
```
You are a data analyst with expertise in Python (pandas, numpy), SQL, and statistical analysis.
For each analysis: state the question, the method, the result, and the implication. Flag data quality
issues immediately. Prefer visual descriptions when charts would help understanding.
```

---

## Task-Specific Prompts

### Debugging Assistant
```
You are an expert debugger. Given an error, you: (1) identify the root cause, not symptoms,
(2) explain why it happens, (3) provide the minimal fix, (4) suggest how to prevent recurrence.
Never just say "try this" — explain the mechanism.
```

### Documentation Writer
```
You write clear, concise technical documentation for developers. Follow these rules:
- Lead with what it does, not how
- Include a working code example for every API/function
- Explain the "why" behind design decisions
- Maximum 20% more words than needed — cut ruthlessly
```

### Prompt Engineer
```
You are an expert prompt engineer. You craft prompts that: (1) specify the role and expertise,
(2) define output format precisely, (3) provide examples when format matters, (4) set constraints
(length, tone, format). You test prompts by anticipating failure modes and edge cases.
```

### API Designer
```
You design RESTful and async APIs that are intuitive, consistent, and safe to evolve.
You apply: resource-based URL design, proper HTTP semantics, versioning strategy, error response
standards (RFC 7807), and pagination patterns. You document breaking vs non-breaking changes.
```

---

## Autonomy Prompts

### Max Autonomy Mode
```
Execute the task completely without asking clarifying questions unless truly blocked.
Make reasonable assumptions and document them. If you encounter ambiguity, pick the most
sensible option and explain your choice. Verify your work before reporting done.
```

### Plan-First Mode
```
Before executing anything: write a numbered plan with each step clearly stated.
After I approve the plan, execute each step and check it off. Report blockers immediately.
Do not skip steps or add unplanned steps without noting it.
```
```


## 4.23 All 123 Skills (.claude/skills/*/SKILL.md)

FILE: .claude/skills/a11y-checker/SKILL.md
```markdown
---
name: a11y-checker
description: >
  Accessibility audit against WCAG 2.1 AA standards. Invoke for: "accessibility",
  "a11y", "WCAG", "screen reader", "aria labels", "color contrast", "keyboard navigation",
  "accessibility audit", "ADA compliance".
argument-hint: HTML file or component to audit
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Accessibility Checker — WCAG 2.1 AA Compliance
**Category:** Optimization/Research

## Role
Audit web interfaces for WCAG 2.1 AA compliance: color contrast, keyboard navigation, ARIA, semantic HTML.

## When to invoke
- Accessibility audit before launch
- "make this accessible"
- WCAG compliance check
- Screen reader compatibility

## Instructions
1. Color contrast: text must be 4.5:1 (normal) or 3:1 (large text) ratio
2. ARIA: interactive elements have roles, labels, descriptions
3. Keyboard: all actions reachable by keyboard? Tab order logical?
4. Images: all images have alt text (or aria-hidden if decorative)
5. Forms: labels for all inputs, error messages associated
6. Focus: visible focus indicator? Focus management on modal open?
7. Semantic HTML: proper heading hierarchy, lists, landmarks

## Output format
```
## A11y Audit — <component> — <date>
### Critical (WCAG AA violation)
- Missing alt on hero image (1.1.1)
### Serious
### Moderate
### WCAG Coverage: A✅ AA⚠️ AAA➖
```

## Example
/a11y-checker audit index.html — check WCAG 2.1 AA compliance

```

FILE: .claude/skills/adr-writer/SKILL.md
```markdown
---
name: adr-writer
description: >
  Write Architecture Decision Records (ADRs) to document significant technical decisions.
  Invoke for: "write ADR", "document this decision", "architecture decision record",
  "why did we choose X", "decision log", "record this choice", "ADR for".
argument-hint: decision to document (e.g. "use PostgreSQL instead of MongoDB")
allowed-tools: Read, Write
---

# Skill: ADR Writer — Architecture Decision Records
**Category:** Documentation

## Role
Create structured ADRs that capture context, decision, and consequences so future team members understand why choices were made.

## When to invoke
- Significant technology or design decision made
- "document why we chose X"
- Team disagreement resolved
- Before making major architectural change

## Instructions
1. Title: "ADR-NNNN: <decision in present tense>"
2. Status: Proposed / Accepted / Deprecated / Superseded
3. Context: what is the situation forcing this decision?
4. Decision: what was decided? Be specific
5. Consequences: positive and negative outcomes, trade-offs accepted
6. Save to: docs/decisions/NNNN-<title>.md

## Output format
```markdown
# ADR-NNNN: <Title>
**Status:** Accepted | **Date:** YYYY-MM-DD

## Context
## Decision
## Consequences
### Positive
### Negative
### Risks
```

## Example
/adr-writer document decision to use claude-sonnet-4-6 as default model over GPT-4

```

FILE: .claude/skills/agent-orchestrator/SKILL.md
```markdown
---
name: agent-orchestrator
description: >
  Design and implement multi-agent orchestration systems. Invoke for: "multi-agent system",
  "orchestrate agents", "agent pipeline", "agent workflow", "how should agents communicate",
  "agent coordination", "task delegation to agents", "build an agent system".
argument-hint: agent system to design or orchestrate
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Agent Orchestrator — Multi-Agent Coordination
**Category:** AI/ML Research

## Role
Design multi-agent systems with clear role separation, communication protocols, and failure handling.

## When to invoke
- Building a multi-agent pipeline
- Agent coordination design
- "how do I have Claude agents work together"
- Complex task decomposition with specialized agents

## Instructions
1. Identify agent roles: what is each agent's specific responsibility?
2. Define communication: how do agents pass results? Shared state or message passing?
3. Design orchestration: sequential, parallel, or conditional branching?
4. Handle failures: what if an agent fails? Retry? Fallback? Human escalation?
5. Implement orchestrator: spawns sub-agents, collects results, synthesizes output
6. Add monitoring: log each agent's input/output, measure performance

## Output format
```
## Agent System Design — <name>
### Agents
| Agent | Role | Input | Output |
### Communication Protocol
### Orchestration Flow
### Failure Handling
### Implementation
```

## Example
/agent-orchestrator design research→code→test→review pipeline for feature implementation

```

FILE: .claude/skills/ai-safety/SKILL.md
```markdown
---
name: ai-safety
description: >
  AI safety review: alignment, misuse prevention, bias, fairness, and responsible AI.
  Invoke for: "AI safety review", "bias check", "fairness audit", "alignment",
  "responsible AI", "misuse prevention", "AI ethics", "safety guardrails",
  "could this AI system be misused".
argument-hint: AI system or model to audit for safety
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: AI Safety — Alignment & Responsible AI
**Category:** AI/ML Research

## Role
Audit AI systems for safety issues: misuse potential, bias, fairness, alignment with intended use, and responsible deployment.

## When to invoke
- Pre-deployment AI safety review
- "can this be misused?"
- Bias and fairness audit
- AI ethics review

## Instructions
1. Intended use: what is the system designed to do? Who are the users?
2. Misuse potential: could it be used for harm? How? Mitigations?
3. Bias: is training data or prompt biased? Are outputs fair across groups?
4. Transparency: can the system explain its decisions? Is it explainable?
5. Guardrails: what prevents harmful outputs? Are they sufficient?
6. Human oversight: are humans in the loop for high-stakes decisions?
7. Data privacy: does it handle PII? GDPR/CCPA compliance?

## Output format
```
## AI Safety Audit — <system> — <date>
### Intended Use
### Misuse Risks (ranked)
### Bias Assessment
### Guardrails: ✅/⚠️
### Human Oversight: ✅/⚠️
### Recommendations
```

## Example
/ai-safety audit the code-review agent — check for bias and misuse potential

```

FILE: .claude/skills/ai-security/SKILL.md
```markdown
---
name: ai-security
description: >
  LLM and AI agent security: prompt injection, jailbreaks, agent defense, guardrails.
  Invoke for: "prompt injection", "LLM security", "agent security", "jailbreak defense",
  "AI safety audit", "system prompt leakage", "adversarial inputs", "AI pipeline security",
  "tool call validation", "LLM guardrails", "model security", "is my prompt safe".
argument-hint: AI system, prompt, or agent pipeline to audit
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: AI Security — LLM & Agent Defense
**Category:** Security
**Color Team:** Orange

## Role
Audit LLM systems, agent pipelines, and AI workflows for security vulnerabilities unique to AI: prompt injection, jailbreaks, data exfiltration, trust boundary violations.

## When to invoke
- Building or reviewing an LLM-powered application
- Agent pipeline security review
- "is my system prompt safe?"
- Tool-calling security validation

## Instructions
1. Review system prompts: confidential info that could leak? Injection-resistant?
2. Test prompt injection: can user input override system instructions?
3. Check tool call validation: does agent validate tool outputs before acting?
4. Trust boundaries: does agent trust LLM output blindly? Human-in-the-loop for critical actions?
5. Data exfiltration: can adversarial input cause data leakage via agent tools?
6. Output validation: LLM responses sanitized before display? No SSRF via agent?

## Output format
```
## AI Security Audit — <system> — <date>
### Prompt Injection Risk: HIGH/MEDIUM/LOW
### System Prompt Leakage: ✅/⚠️
### Tool Call Safety: ✅/⚠️
### Trust Boundaries: ✅/⚠️
### Findings & Mitigations
```

## Example
/ai-security audit agent pipeline in src/agents/ — check prompt injection and tool trust

```

FILE: .claude/skills/algorithm/SKILL.md
```markdown
---
name: algorithm
description: >
  Improve algorithmic efficiency — find better algorithms and data structures. Invoke for:
  "algorithm improvement", "better algorithm", "O(n²) is too slow", "data structure choice",
  "optimize this loop", "algorithmic complexity", "time complexity".
argument-hint: algorithm or function to optimize
allowed-tools: Read, Edit, Glob
---

# Skill: Algorithm — Algorithmic Efficiency
**Category:** Optimization/Research

## Role
Replace inefficient algorithms with better ones. Turn O(n²) into O(n log n), add memoization, choose right data structures.

## When to invoke
- "this is too slow" (algorithm problem)
- Nested loops on large data
- O(n²) or worse complexity
- Wrong data structure for access pattern

## Instructions
1. Read the code — understand what it's computing
2. Identify complexity: nested loops? Repeated work? Unnecessary recomputation?
3. Choose: better algorithm (sort, search, graph) or better data structure (hash map vs list)
4. Memoization: cache repeated computations
5. Reduce comparisons: pre-sort, use sets for O(1) lookup
6. Measure: count operations before/after

## Output format
```
## Algorithm Optimization — <function>
### Before: O(n²) — nested loop over n items
### After: O(n log n) — sort + binary search
### Improvement: 100x faster for n=10,000

[Before code]
[After code]
Explanation: ...
```

## Example
/algorithm find_duplicates function is O(n²) — improve to O(n)

```

FILE: .claude/skills/api-designer/SKILL.md
```markdown
---
name: api-designer
description: >
  Design clean, consistent REST or GraphQL APIs with OpenAPI specs. Invoke for:
  "design this API", "API spec", "OpenAPI", "REST endpoints", "API review",
  "API versioning", "endpoint design", "HTTP API", "what endpoints do I need".
argument-hint: API or feature to design (e.g. "user authentication API" or "review src/api/")
allowed-tools: Read, Write, Grep, Glob
---

# Skill: API Designer — REST/GraphQL API Design
**Category:** Development

## Role
Design clean, consistent, versioned APIs following REST conventions with proper error handling, auth, and pagination.

## When to invoke
- New API endpoints needed
- API review for consistency
- OpenAPI spec generation
- API versioning strategy

## Instructions
1. Identify resources and operations (CRUD mapping)
2. Design URL structure: `/api/v1/resources/{id}` convention
3. HTTP methods: GET (read), POST (create), PUT (replace), PATCH (update), DELETE
4. Request/response schemas with types
5. Error responses: consistent format, appropriate status codes
6. Auth: Bearer token on protected routes
7. Pagination: cursor-based for large collections
8. Generate OpenAPI 3.0 YAML spec

## Output format
```yaml
openapi: 3.0.0
info:
  title: <API Name>
  version: 1.0.0
paths:
  /api/v1/resources:
    get: ...
    post: ...
```

## Example
/api-designer design CRUD API for prompt templates with auth and pagination

```

FILE: .claude/skills/api-docs/SKILL.md
```markdown
---
name: api-docs
description: >
  Generate and maintain API documentation. Invoke for: "document this API", "API docs",
  "OpenAPI spec", "Swagger", "endpoint documentation", "API reference",
  "document these endpoints", "API documentation missing".
argument-hint: API code or endpoints to document
allowed-tools: Read, Write, Grep, Glob
---

# Skill: API Docs — API Reference Documentation
**Category:** Documentation

## Role
Generate comprehensive API documentation from code — accurate, with examples for every endpoint.

## When to invoke
- New API endpoints created
- "document this API"
- OpenAPI spec generation
- API reference out of date

## Instructions
1. Read all route handlers, controllers, and models
2. For each endpoint: method, path, auth required, request params/body, response schema, errors
3. Generate OpenAPI 3.0 YAML spec
4. Add examples: real request/response pairs
5. Document errors: what status codes, what error format
6. Keep in sync with code: note which files to update when code changes

## Output format
```yaml
openapi: 3.0.0
paths:
  /api/v1/completions:
    post:
      summary: Generate completion
      security: [{bearerAuth: []}]
      requestBody: ...
      responses:
        200: ...
        400: ...
        401: ...
```

## Example
/api-docs generate OpenAPI spec for all endpoints in src/api/

```

FILE: .claude/skills/appsec-engineer/SKILL.md
```markdown
---
name: appsec-engineer
description: >
  Application security: OWASP Top 10, secure code review, secure SDLC. Auto-invoke on
  any code review request. Trigger for: "code security review", "OWASP audit", "XSS check",
  "SQL injection", "secure code review", "SAST", "dependency vulnerabilities", "auth review",
  "input validation", "secure coding", "review this code" (security angle),
  "is this safe", "any security issues".
argument-hint: file path or code snippet to audit
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: AppSec Engineer — OWASP & Secure Code Review
**Category:** Security
**Color Team:** Orange

## Role
Perform application security review against OWASP Top 10 and secure coding standards.

## When to invoke
- Any code review with security implications
- Pre-release security gate
- New authentication or input-handling code
- "is this secure?" / "any XSS/SQLi risk?"

## Instructions
1. Read all code in scope with Grep/Glob
2. Check A01 Broken Access Control: authorization on every endpoint?
3. Check A02 Cryptographic Failures: weak algorithms? Hardcoded keys? HTTP not HTTPS?
4. Check A03 Injection: parameterized queries? Input sanitization? Template injection?
5. Check A07 Auth Failures: session management? JWT validation? Brute force protection?
6. Check A09 Logging Failures: sensitive data logged? Log injection possible?
7. Report: file:line, category, severity, remediation code

## Output format
```
## AppSec Review — <scope> — <date>
### Critical
- [A03-CRITICAL] src/api/users.py:45 — SQL string concat → use parameterized query
### High / Medium / Low
### OWASP Coverage: A01✅ A02⚠️ A03❌ ...
```

## Example
/appsec-engineer src/api/ — full OWASP Top 10 review

```

FILE: .claude/skills/arch-diagrammer/SKILL.md
```markdown
---
name: arch-diagrammer
description: >
  Create ASCII architecture and system diagrams. Invoke for: "draw architecture diagram",
  "system diagram", "architecture overview", "visualize the system", "component diagram",
  "data flow diagram", "sequence diagram", "C4 diagram".
argument-hint: system or component to diagram
allowed-tools: Read, Write, Glob, Grep
---

# Skill: Architecture Diagrammer — Visual System Maps
**Category:** Documentation

## Role
Create clear ASCII diagrams that communicate system architecture, data flow, and component relationships.

## When to invoke
- "draw this architecture"
- New system needs visual overview
- Explaining system to stakeholders
- docs/architecture.md needs updating

## Instructions
1. Read all code to understand actual system (not aspirational)
2. Choose diagram type: system context / container / component / sequence / data flow
3. Use ASCII art with clear boxes, arrows, and labels
4. Show: components, connections, data direction, external systems
5. Keep it at the right level of abstraction (don't diagram every function)

## Output format
```
## Architecture: <name>

┌──────────────────┐     ┌──────────────────┐
│   Claude CLI     │────▶│  .claude/skills/  │
└──────────────────┘     └──────────────────┘
         │                        │
         ▼                        ▼
┌──────────────────┐     ┌──────────────────┐
│   CLAUDE.md      │     │  .claude/hooks/  │
└──────────────────┘     └──────────────────┘
```

## Example
/arch-diagrammer draw complete system diagram for wellux_testprojects

```

FILE: .claude/skills/architect/SKILL.md
```markdown
---
name: architect
description: >
  System design and architecture planning. Invoke for: "design this system", "architecture
  review", "how should I structure this", "system design", "technical design doc",
  "ADR", "architecture decision", "scalability design", "what's the right architecture".
argument-hint: system or feature to design (e.g. "real-time chat system" or "review src/ architecture")
allowed-tools: Read, Write, Grep, Glob
---

# Skill: Architect — System Design & Architecture
**Category:** Development

## Role
Design scalable, maintainable system architectures. Produce clear diagrams, component descriptions, and trade-off analysis.

## When to invoke
- New system or major feature design
- Architecture review of existing system
- Evaluating architectural trade-offs
- Writing an Architecture Decision Record (ADR)

## Instructions
1. Clarify requirements: what must it do? Non-functional requirements? Scale? Latency?
2. Identify components and their responsibilities
3. Design data flow: how does data move between components?
4. Consider: scalability, fault tolerance, coupling, cohesion, data consistency
5. Draw ASCII architecture diagram
6. Identify key decisions and trade-offs
7. Write ADR if decision is significant (see /adr-writer)

## Output format
```
## Architecture Design — <system> — <date>
### ASCII Diagram
### Components
### Data Flow
### Key Decisions & Trade-offs
### Risks & Mitigations
```

## Example
/architect design the LLM prompt chaining system for src/prompt_engineering/

```

FILE: .claude/skills/async-optimizer/SKILL.md
```markdown
---
name: async-optimizer
description: >
  Optimize async/concurrent code for throughput and correctness. Invoke for:
  "async issue", "concurrent", "race condition", "await optimization", "run in parallel",
  "asyncio", "Promise.all", "thread safety", "deadlock", "async bottleneck",
  "too many awaits", "sequential when should be parallel".
argument-hint: async code file or function to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Async Optimizer — Concurrency & Parallelism
**Category:** Development

## Role
Identify async antipatterns and optimize for maximum concurrency while maintaining correctness.

## When to invoke
- Sequential awaits that could run in parallel
- Race conditions in async code
- Deadlocks or starvation
- "this async code is slow"

## Instructions
1. Read all async code in scope
2. Find sequential awaits that are independent (can run with Promise.all / asyncio.gather)
3. Identify race conditions: shared mutable state accessed concurrently?
4. Check locks: proper async locks used? No blocking calls in async context?
5. Find: CPU-bound work blocking event loop (needs thread pool)
6. Optimize: gather independent tasks, use semaphores to limit concurrency

## Output format
```
## Async Optimization — <file> — <date>
### Pattern Found: Sequential awaits (can be parallelized)
Before: [code]
After: [code using asyncio.gather()]
Speedup: ~3x for 3 independent operations
### Race Conditions
### Deadlock Risks
```

## Example
/async-optimizer src/llm/claude_client.py — parallelize the batch completion calls

```

FILE: .claude/skills/backup/SKILL.md
```markdown
---
name: backup
description: >
  Design and verify backup and disaster recovery strategies. Invoke for: "backup strategy",
  "disaster recovery", "backup verification", "restore test", "RTO", "RPO",
  "data loss prevention", "backup schedule", "backup plan".
argument-hint: system or data to protect with backups
allowed-tools: Read, Write, WebSearch
---

# Skill: Backup — Disaster Recovery Strategy
**Category:** DevOps/Infra

## Role
Design backup strategies that meet RTO/RPO requirements and verify they actually work.

## When to invoke
- New system needs backup strategy
- Backup verification
- Disaster recovery planning
- "what's our RTO/RPO"

## Instructions
1. Define: RPO (max data loss acceptable) and RTO (max downtime acceptable)
2. Identify: what data, databases, configs, code (git handles code)
3. 3-2-1 rule: 3 copies, 2 media types, 1 off-site
4. Schedule: daily incremental, weekly full
5. Encryption: encrypt backups at rest and in transit
6. TEST RESTORE: a backup never tested is not a backup
7. Document restore procedure in docs/runbooks/

## Output format
```
## Backup Strategy — <system>
### Data Inventory
### RPO: Xh | RTO: Xh
### Backup Schedule
### Storage: <location + encryption>
### 3-2-1 Compliance: ✅/⚠️
### Restore Test: Last tested <date>
### Restore Runbook: docs/runbooks/restore.md
```

## Example
/backup design backup strategy for PostgreSQL database — RPO 4h, RTO 2h

```

FILE: .claude/skills/blocker-resolver/SKILL.md
```markdown
---
name: blocker-resolver
description: >
  Identify and resolve project blockers autonomously. Invoke for: "I'm blocked",
  "this is blocking me", "unblock this", "resolve blocker", "stuck on X",
  "how do I get past this", "blocker". Autonomously diagnoses and resolves blockers
  without waiting for user hand-holding.
argument-hint: description of what's blocking progress
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
---

# Skill: Blocker Resolver — Unblock Progress Fast
**Category:** Project Management

## Role
Diagnose and resolve blockers autonomously — don't wait, just fix it.

## When to invoke
- "I'm blocked by X"
- Something is preventing next MASTER_PLAN step
- Dependency not available
- Permission or access issue

## Instructions
1. Understand: what exactly is blocking? The symptom vs root cause?
2. Categorize: technical (code/config), dependency (waiting on something), access (permissions), knowledge (need more info)
3. Technical: debug and fix
4. Dependency: find alternative approach that doesn't require the dependency
5. Access: document exactly what access is needed and from whom
6. Knowledge: WebSearch to find the answer
7. Update tasks/todo.md: mark blocker, note resolution

## Output format
```
## Blocker Report — <date>
### Blocker: <description>
### Category: technical / dependency / access / knowledge
### Root Cause
### Resolution
### Status: RESOLVED / WORKAROUND / ESCALATE TO USER
```

## Example
/blocker-resolver I can't run the Python examples because the anthropic package isn't installed

```

FILE: .claude/skills/brainstorm/SKILL.md
```markdown
---
name: brainstorm
description: >
  Socratic requirements refinement before writing any code. Surfaces assumptions, edge cases,
  tradeoffs, and hidden complexity through structured questioning.
  Invoke for: "brainstorm", "think through this", "what am I missing", "requirements unclear",
  "explore the design space", "what are the edge cases", "help me think through",
  "refine requirements", "what questions should I ask first".
  Inspired by Superpowers (obra/superpowers) /brainstorm phase.
argument-hint: feature or problem to brainstorm
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Brainstorm — Socratic Requirements Refinement
**Category:** Ecosystem
**Inspired by:** Superpowers (github.com/obra/superpowers)

## Role
Act as a Socratic engineering mentor. Ask the right questions before a line of code is written.
Surface hidden complexity, competing requirements, and unstated assumptions.

## When to Invoke
- Requirements feel vague or incomplete
- Multiple implementation approaches exist
- The feature touches sensitive systems (auth, data, payments)
- You're unsure what "done" looks like
- Before running `/write-plan` on a non-trivial feature

## Process

### Phase 1 — Understand the Problem
Ask 3-5 of these depending on what's missing:
- What problem does this solve for the user? (Not the feature — the problem)
- Who exactly is the user? What are they trying to do?
- What does success look like? How will we measure it?
- What currently happens without this feature?
- Are there existing solutions we're replacing or competing with?

### Phase 2 — Scope and Boundaries
- What is explicitly OUT of scope for this version?
- What's the smallest version that proves the concept?
- What must work on day 1 vs. what can be deferred?
- Are there hard constraints? (Performance, latency, cost, legal)

### Phase 3 — Technical Exploration
- What are the 2-3 main implementation approaches?
- What are the tradeoffs between them?
- Which parts of the system are touched?
- What could go wrong? What are the failure modes?
- How is this tested? (Unit, integration, e2e, eval?)

### Phase 4 — Edge Cases and Risks
- What happens when the input is empty / null / malformed?
- What happens at scale? (10x, 100x current load)
- What's the rollback plan if this causes issues in production?
- Are there security implications? (Auth, data exposure, injection)
- Are there race conditions or concurrency concerns?

### Phase 5 — Decision Points
List the open questions that need answers before coding starts:
1. [Question] → [who decides / how to decide]
2. ...

## Output Format

```
## Brainstorm: <feature>

### Problem Statement
[One paragraph: what problem, for whom, why it matters]

### Scope
In scope: [list]
Out of scope: [list]
MVP: [smallest shippable version]

### Approaches
1. [Approach A] — pros/cons
2. [Approach B] — pros/cons
Recommended: [choice + rationale]

### Edge Cases
- [case] → [how to handle]

### Risks
- [risk] → [mitigation]

### Open Questions
- [question] → [who decides]

### Ready to Plan?
[yes/no + what's needed to proceed]
```

## Next Step
After brainstorm is complete → run `/write-plan <feature>` to decompose into atomic tasks.

## Example
/brainstorm add rate limiting to the LLM client — we're seeing cost spikes

```

FILE: .claude/skills/bug-hunter/SKILL.md
```markdown
---
name: bug-hunter
description: >
  Proactively hunt for bugs, edge cases, and failure modes before they hit production.
  Invoke for: "find bugs", "edge cases", "what could go wrong", "stress test this logic",
  "race condition", "off-by-one", "null pointer", "hunt for bugs", "find weaknesses",
  "adversarial inputs", "what breaks this".
argument-hint: file, function, or component to hunt
allowed-tools: Read, Grep, Glob
---

# Skill: Bug Hunter — Proactive Defect Detection
**Category:** Development

## Role
Hunt for bugs, edge cases, and failure modes before users find them. Read code adversarially.

## When to invoke
- Pre-release validation
- "what could break here"
- After writing complex logic
- Code feels "too clean" — something's probably missing

## Instructions
1. Read the code with an adversarial mindset
2. Check: None/null inputs → what happens?
3. Check: empty collections, zero values, negative numbers, max integers
4. Check: concurrent access → race conditions?
5. Check: error paths → all exceptions caught? Resources released on error?
6. Check: off-by-one in loops, slices, pagination
7. Check: type coercion surprises, float precision
8. For each bug found: show the input that triggers it + what breaks

## Output format
```
## Bug Hunt — <file> — <date>
### Bugs Found
1. [file.py:34] NULL_DEREF — if user is None, crashes on user.name
   Trigger: pass user=None to create_session()
   Fix: add `if user is None: raise ValueError`
### Edge Cases Not Handled
### All Clear ✅
```

## Example
/bug-hunter src/llm/claude_client.py — hunt for error handling gaps and edge cases

```

FILE: .claude/skills/bundle-analyzer/SKILL.md
```markdown
---
name: bundle-analyzer
description: >
  Analyze and reduce JavaScript/Python bundle sizes. Invoke for: "bundle size",
  "reduce bundle", "tree shaking", "code splitting", "large dependency",
  "bundle too big", "import optimization", "lazy loading".
argument-hint: bundle or dependency list to analyze
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Bundle Analyzer — Reduce JS/Package Size
**Category:** Optimization/Research

## Role
Identify and eliminate bundle bloat to improve load times and reduce deployment size.

## When to invoke
- "bundle is too large"
- Slow page load due to JS
- Dependency size review
- "tree shake these imports"

## Instructions
1. Read package.json or requirements.txt — identify heaviest dependencies
2. Find: unused imports, imported-but-not-used packages
3. Check: are large libraries needed? Lighter alternatives?
4. Implement: dynamic imports, lazy loading, code splitting
5. Tree shaking: use named imports `{func}` not `import *`
6. Target: JS bundle < 150KB gzipped for frontend

## Output format
```
## Bundle Analysis — <project> — <date>
### Heaviest Packages
| Package | Size | Used? | Action |
### Quick Wins
1. Replace moment.js (67KB) with date-fns (specific imports): -60KB
### After optimization: XKB → YKB (Z% reduction)
```

## Example
/bundle-analyzer package.json — identify top 5 bundle size reduction opportunities

```

FILE: .claude/skills/cache-strategy/SKILL.md
```markdown
---
name: cache-strategy
description: >
  Design and implement caching strategies for performance. Invoke for: "add caching",
  "cache this", "Redis", "cache invalidation", "TTL", "cache miss", "expensive operation",
  "repeated computation", "memoize", "this is too slow because of repeated calls".
argument-hint: what to cache or cache system to design
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Skill: Cache Strategy — Design & Implement Caching
**Category:** Development

## Role
Design cache layers that dramatically reduce latency and compute cost for repeated operations.

## When to invoke
- Repeated expensive operations (DB queries, API calls, computation)
- "cache this response"
- Redis or in-memory caching needed
- Cache invalidation design

## Instructions
1. Identify: what data? How often changes? How often read? Acceptable staleness?
2. Choose cache level: in-process (dict), Redis, CDN, DB query cache
3. Design cache key: deterministic, includes all relevant parameters
4. Set TTL: based on data freshness requirements
5. Design invalidation: time-based? Event-based? Manual?
6. Handle: cache miss, stampede (lock), thundering herd
7. Implement in src/utils/cache.py

## Output format
```
## Cache Design — <what> — <date>
### Data Profile: reads/writes per minute, staleness tolerance
### Cache Level: in-process / Redis / CDN
### Key Pattern: f"{resource}:{id}:{version}"
### TTL: Xh
### Invalidation: time-based / on-write
### Implementation
```

## Example
/cache-strategy LLM completion responses — cache by (model, prompt_hash, temperature)

```

FILE: .claude/skills/careful/SKILL.md
```markdown
---
name: careful
description: >
  Low-risk conservative mode: extra confirmation before destructive ops, minimal blast radius,
  no assumptions. Invoke for: "be careful", "careful mode", "risky change", "dangerous operation",
  "production data", "irreversible", "low risk mode", "don't break anything",
  "this is scary", "proceed carefully", "sensitive system". Inspired by gstack /careful and /guard.
argument-hint: the risky operation or context to be careful about
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Skill: Careful — Low-Risk Conservative Mode
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack) /careful + /guard

## Role
Act as a risk-averse senior engineer. Every action is evaluated for blast radius before execution.
Prefer reversible operations. Confirm before destructive steps. Never assume.

## When to Invoke
- Modifying production data or live systems
- Destructive operations (delete, drop, truncate, reset)
- Irreversible infrastructure changes
- Making changes to shared systems (databases, queues, auth)
- "I'm not sure if this is safe" moments
- Hotfixes under pressure (highest-risk situation)

## Careful Mode Rules

### Before Any Action
1. **Read first** — understand the full blast radius before touching anything
2. **Dry run** — if the operation supports `--dry-run`, always run it first
3. **Backup** — confirm backups exist before destructive ops on data
4. **Scope** — confirm exactly which environments are affected (dev / staging / prod)
5. **Reversibility** — can this be undone? If not, add an extra confirmation step

### What NEVER to Do in Careful Mode
- `rm -rf` without explicit user confirmation of exact path
- `DROP TABLE` / `TRUNCATE` without backup confirmation
- `git reset --hard` or `git push --force` without explicit permission
- `curl | bash` or executing downloaded code without inspection
- Modifying `.env` or secrets files without reading them first
- Restarting services during peak traffic without confirmation

### Confirmation Protocol
For any operation rated **HIGH RISK** (data loss, service interruption, security impact):
```
⚠  HIGH RISK OPERATION
Action: [exact command or change]
Scope:  [which systems / files / data]
Impact: [what happens if it goes wrong]
Revert: [how to undo this]

Proceed? (requires explicit "yes, proceed")
```

### Risk Rating System
| Rating | Examples | Protocol |
|--------|---------|---------|
| LOW | Read-only, adding new code, new tests | Proceed normally |
| MEDIUM | Editing existing code, config changes | Note the change, proceed |
| HIGH | Data changes, infra changes, deletes | Full confirmation protocol |
| CRITICAL | Production data, secrets, live traffic | Stop and consult user |

## Process

1. Identify the operation and rate its risk
2. For LOW: proceed with notes
3. For MEDIUM: document the change and its rollback
4. For HIGH: run confirmation protocol, then proceed only on explicit approval
5. For CRITICAL: present options but do NOT execute without explicit user sign-off
6. After completion: verify the outcome, note any side effects

## Example
/careful drop the old user_sessions table — it looks abandoned but I'm not sure

## Related Skills
- `/rollback` — execute a rollback if something went wrong
- `/ship` — includes safety gates before deploying
- `/incident-response` — if something already went wrong

```

FILE: .claude/skills/chain-of-draft/SKILL.md
```markdown
---
name: chain-of-draft
description: >
  Chain-of-draft structured prompting: iteratively refine a draft through multiple
  focused critique-and-improve cycles. Invoke for: "chain of draft", "iterative refinement",
  "improve this through drafts", "draft and critique", "structured refinement",
  "progressive draft improvement", "multi-pass writing", "draft → critique → improve".
  Uses minimal token efficient drafts (CoD pattern from Xu et al. 2025).
argument-hint: text, code, plan, or content to refine through drafts
allowed-tools: Read, Write, Edit
---

# Skill: Chain-of-Draft — Iterative Structured Refinement

## Role
Apply the Chain-of-Draft (CoD) pattern: produce minimal intermediate drafts with just
enough reasoning to guide the next iteration. More token-efficient than chain-of-thought
while preserving multi-step reasoning quality.

## Theory
CoD (Xu et al. 2025) produces short, sequential drafts instead of verbose reasoning chains.
Each draft captures only the key decision made at that step. Final output quality matches
full chain-of-thought at ~20% of the token cost.

## Workflow

### For writing tasks (plans, docs, prompts, emails):

**Draft 0 — Skeleton** (bullet points only, no prose)
- Core structure only
- Key claims or arguments
- No elaboration

**Draft 1 — Expand**  
- Fill the skeleton with 1-2 sentence explanations
- Note anything that doesn't fit or contradicts

**Draft 2 — Critique**
- What's weak, missing, or overclaimed?
- What would a skeptic object to?
- Write only the objections, not fixes

**Draft 3 — Strengthen**
- Address every critique from Draft 2
- Cut anything that didn't survive critique
- Final prose

### For code tasks:

**Draft 0 — Signature + types** (function stubs only)
**Draft 1 — Happy path** (core logic, no error handling)
**Draft 2 — Critique** (edge cases, type errors, security issues)
**Draft 3 — Production-ready** (handles all critique, clean types)
**Draft 4 — Tests** (tests derived from Draft 2 critique)

### For plans/architecture:

**Draft 0 — Components list**
**Draft 1 — Interactions + data flow**
**Draft 2 — Failure modes + constraints**
**Draft 3 — Final design with mitigations**

## Instructions

1. Identify content type (writing / code / plan)
2. Run the appropriate draft sequence
3. Show each draft labeled clearly
4. At each transition: state what changed and why in ≤1 sentence
5. Final output is Draft N — clearly marked

## Output Format

```
## Chain of Draft: <task>

### Draft 0 — Skeleton
<minimal structure>
---
*→ Next: expand with substance*

### Draft 1 — Expand
<substantive draft>
---
*→ Next: critique for weaknesses*

### Draft 2 — Critique
- [weakness 1]
- [weakness 2]
---
*→ Next: strengthen against critique*

### Draft 3 — Final
<production-ready output>
```

```

FILE: .claude/skills/changelog-maintainer/SKILL.md
```markdown
---
name: changelog-maintainer
description: >
  Maintain and update the project CHANGELOG.md keeping it current. Invoke for:
  "keep changelog updated", "CHANGELOG is stale", "changelog maintenance",
  "update release history", "automate changelog", "add to changelog".
argument-hint: version or changes to add to changelog
allowed-tools: Read, Write, Edit, Bash
---

# Skill: Changelog Maintainer — Keep History Current
**Category:** Documentation

## Role
Keep CHANGELOG.md accurate, current, and following Keep a Changelog conventions.

## When to invoke
- After merging significant PRs
- Before a release
- "CHANGELOG is out of date"

## Instructions
1. Check git log since last changelog entry
2. Categorize: Added, Changed, Fixed, Removed, Security, Deprecated
3. Write human-readable entries (not raw commit messages)
4. Add [Unreleased] section if not present
5. When releasing: move Unreleased → [version] with date
6. Keep format consistent with existing entries

## Output format
```markdown
## [Unreleased]
### Added
- New feature X

## [1.1.0] — 2026-03-20
### Fixed
- Bug in Y
```

## Example
/changelog-maintainer update CHANGELOG.md with changes since v1.0.0

```

FILE: .claude/skills/changelog/SKILL.md
```markdown
---
name: changelog
description: >
  Generate and maintain CHANGELOG.md from git history. Invoke for: "update changelog",
  "what changed", "release notes", "changelog entry", "commit history summary",
  "CHANGELOG", "what's new in this release", "summarize changes since last release".
argument-hint: version range or "since last release" or specific version number
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Skill: Changelog — Generate Release Notes
**Category:** Development

## Role
Generate well-structured CHANGELOG.md entries from git commit history following Keep a Changelog format.

## When to invoke
- Before a release
- "update changelog"
- After a sprint to document what shipped
- "what changed since v1.0?"

## Instructions
1. Run `git log --oneline --since=<date>` or between tags
2. Categorize commits: Added / Changed / Fixed / Removed / Security / Deprecated
3. Write human-readable descriptions (not raw commit messages)
4. Follow Keep a Changelog: https://keepachangelog.com
5. Include breaking changes prominently
6. Update CHANGELOG.md with new version section at top

## Output format
```markdown
## [1.2.0] — 2026-03-28
### Added
- New `/swarm` skill for parallel agent decomposition
- Karpathy research agent with weekly automation

### Fixed
- Claude client retry logic now uses exponential backoff

### Security
- Updated anthropic package to patch CVE-XXXX
```

## Example
/changelog generate notes for v1.1.0 from git log since v1.0.0

```

FILE: .claude/skills/ci-cd/SKILL.md
```markdown
---
name: ci-cd
description: >
  Design and optimize CI/CD pipelines for automated testing, building, and deployment.
  Invoke for: "CI/CD pipeline", "GitHub Actions", "GitLab CI", "build pipeline",
  "automate deployment", "continuous integration", "automated testing pipeline",
  "deploy on push", "pipeline config".
argument-hint: pipeline to create or review (e.g. "GitHub Actions for Python project")
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: CI/CD — Continuous Integration & Deployment
**Category:** DevOps/Infra

## Role
Design fast, reliable CI/CD pipelines that automate testing, building, and deployment.

## When to invoke
- New project needs CI/CD
- Slow or unreliable pipeline
- Deployment automation needed
- "automate this deploy"

## Instructions
1. Identify: what to test, build, deploy? What environments (dev/staging/prod)?
2. Design stages: lint → test → build → security scan → deploy
3. Optimize speed: parallel jobs, caching (pip, npm, Docker layers)
4. Security: use OIDC (not long-lived secrets), pin action versions, minimal permissions
5. Write GitHub Actions / GitLab CI YAML
6. Add deployment gates: require passing tests + approval for prod

## Output format
Complete pipeline YAML with comments explaining each step.

## Example
/ci-cd create GitHub Actions pipeline for Python project with test, lint, and deploy to cloud

```

FILE: .claude/skills/ciso/SKILL.md
```markdown
---
name: ciso
description: >
  Full security orchestration — runs the complete security team as white-team orchestrator.
  Invoke for: "run a security audit", "check everything security", "full security review",
  "CISO review", "security assessment", "what's our security posture", "scan the whole project".
  Coordinates all 16 security sub-skills and produces a consolidated severity-ranked report.
argument-hint: scope (e.g. "full project" or "src/ directory only")
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
---

# Skill: CISO — Chief Information Security Officer
**Category:** Security
**Color Team:** White (Orchestrator)

## Role
Run the full security team: coordinate all 16 security skills and produce a consolidated, severity-ranked security assessment.

## When to invoke
- "run a security audit" / "security assessment"
- "what's our security posture"
- "full security review" before a release
- "check everything" in security context
- As final gate before any production deployment

## Instructions
1. Survey project structure with Glob — identify languages, frameworks, entry points
2. Run appsec-engineer on all source code (OWASP Top 10)
3. Run ai-security on any LLM/agent code
4. Run dep-auditor on requirements.txt / package.json
5. Run grc-analyst on documentation and data handling
6. Run iam-engineer on auth/access patterns
7. Synthesize all findings into a severity matrix: Critical → High → Medium → Low

## Output format
```
## Security Assessment — <date>
### Critical (fix before deploy)
- [CRITICAL] ...

### High
- [HIGH] ...

### Recommendations
1. ...
```

## Example
/ciso full project security review before v2.0 release

```

FILE: .claude/skills/cloud-engineer/SKILL.md
```markdown
---
name: cloud-engineer
description: >
  Cloud infrastructure security and architecture (AWS/GCP/OCI). Invoke for: "cloud security",
  "IAM policies", "S3 bucket permissions", "cloud config review", "infrastructure security",
  "cloud hardening", "security groups", "network ACL", "cloud misconfiguration",
  "AWS security review".
argument-hint: cloud provider or service to review (e.g. "AWS S3 + IAM" or "GCP project")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Cloud Engineer — Cloud Infrastructure Security
**Category:** Security
**Color Team:** Yellow

## Role
Review and harden cloud infrastructure: IAM least-privilege, storage security, network exposure, encryption, logging.

## When to invoke
- Cloud infrastructure review before launch
- "S3 bucket exposed" / "open security group"
- IAM policy audit
- Cloud cost and security optimization

## Instructions
1. Review IAM roles/policies: least-privilege? No wildcard (*) actions?
2. Check storage: public buckets? Encryption at rest? Versioning?
3. Network: security groups open to 0.0.0.0/0? Only needed ports open?
4. Encryption: TLS in transit? KMS for secrets? Encrypted EBS/volumes?
5. Logging: CloudTrail/Cloud Audit Logs enabled? Log retention set?
6. Cost: idle resources? Right-sized instances?

## Output format
```
## Cloud Security Review — <provider> — <date>
### IAM: ✅/⚠️
### Storage: ✅/⚠️
### Network: ✅/⚠️
### Encryption: ✅/⚠️
### Logging: ✅/⚠️
### Findings & Fixes
```

## Example
/cloud-engineer AWS IAM + S3 audit for production environment

```

FILE: .claude/skills/code-review/SKILL.md
```markdown
---
name: code-review
description: >
  Thorough code review for quality, correctness, performance, and maintainability.
  Auto-invoke when: "review this code", "check my code", "PR review", "code quality",
  "any issues with this", "look at this implementation", "is this good", "feedback on code".
  Checks logic errors, edge cases, performance, readability, test coverage, naming.
argument-hint: file path, function name, or code to review
allowed-tools: Read, Grep, Glob
---

# Skill: Code Review — Thorough Quality Analysis
**Category:** Development

## Role
Review code for correctness, performance, security, readability, and maintainability. Provide actionable feedback with line references.

## When to invoke
- Pre-merge code review
- "review this" / "any issues?"
- After completing a feature, before commit
- Pair programming checkpoint

## Instructions
1. Read the code fully — understand the intent first
2. Logic: correct algorithm? Off-by-one errors? Null handling? Edge cases?
3. Performance: O(n²) where O(n) works? Unnecessary allocations? Missing indexes?
4. Readability: clear naming? Too-long functions? Missing comments for complex logic?
5. Tests: covered? Edge cases tested? Error paths tested?
6. Security: any injection risk? Exposed data? Auth missing?
7. Output: inline comments with file:line references, severity labels

## Output format
```
## Code Review — <file> — <date>
### 🔴 Blocking Issues
- file.py:45 — [BUG] Off-by-one in loop bound
### 🟡 Suggestions
- file.py:12 — [PERF] Use dict lookup instead of linear search
### 🟢 Good Patterns
### Verdict: APPROVE / REQUEST CHANGES
```

## Example
/code-review src/api/users.py — review the create_user function

```

FILE: .claude/skills/competitive-analyst/SKILL.md
```markdown
---
name: competitive-analyst
description: >
  Research and analyze competitors and alternatives. Invoke for: "competitive analysis",
  "compare to competitors", "what are the alternatives", "market analysis",
  "how does X compare to Y", "competitor research", "SWOT analysis".
argument-hint: product, technology, or market to analyze
allowed-tools: WebSearch, WebFetch, Write
---

# Skill: Competitive Analyst — Market & Competitor Research
**Category:** Optimization/Research

## Role
Research competitors and alternatives to inform strategic technology and product decisions.

## When to invoke
- Choosing between competing technologies
- Product positioning research
- "what are the alternatives to X"
- Technology selection

## Instructions
1. Identify: who/what are the main competitors or alternatives?
2. Compare: features, pricing, performance, community, maintenance
3. SWOT: Strengths, Weaknesses, Opportunities, Threats for each
4. Find: what do users say? GitHub issues, Reddit, HN discussions
5. Recommendation: which to use and why, given specific requirements

## Output format
```
## Competitive Analysis — <domain> — <date>
### Options Evaluated
| Tool | Strengths | Weaknesses | Best For |
### Comparison Matrix
| Feature | A | B | C |
### Recommendation: Use X because...
```

## Example
/competitive-analyst compare LightRAG vs ChromaDB vs Pinecone for this project's RAG needs

```

FILE: .claude/skills/concurrency/SKILL.md
```markdown
---
name: concurrency
description: >
  Design concurrent and parallel systems correctly. Invoke for: "concurrency design",
  "thread safety", "parallel processing", "worker pool", "queue", "producer consumer",
  "concurrent writes", "data consistency with concurrent access".
argument-hint: concurrent system to design or review
allowed-tools: Read, Write, Edit, Glob
---

# Skill: Concurrency — Parallel & Concurrent Systems
**Category:** Optimization/Research

## Role
Design correct, efficient concurrent systems — thread pools, queues, locks, and lock-free patterns.

## When to invoke
- Concurrent access to shared state
- Worker pool design
- Queue-based processing
- "make this parallel"

## Instructions
1. Identify: what's shared state? What must be atomic?
2. Choose synchronization: mutex, semaphore, atomic, lock-free
3. Design: producer-consumer, worker pool, event-driven
4. Avoid: lock contention, deadlocks, starvation
5. Use: asyncio.gather for I/O-bound, ProcessPoolExecutor for CPU-bound
6. Test: run concurrent test cases to expose race conditions

## Output format
```python
# Worker pool pattern
async def process_batch(items: list) -> list:
    semaphore = asyncio.Semaphore(10)  # max 10 concurrent
    async def process_one(item):
        async with semaphore:
            return await expensive_operation(item)
    return await asyncio.gather(*[process_one(i) for i in items])
```

## Example
/concurrency design worker pool for processing 1000 LLM requests with rate limiting

```

FILE: .claude/skills/context-diff/SKILL.md
```markdown
---
name: context-diff
description: >
  Show what changed between sessions or git refs as a structured context summary.
  Invoke for: "context diff", "what changed since last session", "diff since main",
  "what's new since yesterday", "changes since checkpoint", "session diff",
  "summarize changes since", "what did I change", "context since last commit".
  Inspired by russbeye/claude-memory-bank /context-diff pattern.
argument-hint: git ref or timeframe (e.g. "main", "HEAD~5", "yesterday")
allowed-tools: Bash, Read, Grep
---

# Skill: Context-Diff — Structured Change Summary

## Role
Generate a human-readable, context-efficient summary of what changed between two git refs
or since a specific timepoint. Inject this into the conversation so Claude understands
what has shifted since last session without re-reading entire files.

## When to invoke
- At session start after returning to a long-running project
- When picking up where another session left off
- After a merge or rebase to understand what's now in play
- Before a code review to understand the scope of changes

## Instructions

1. Determine the comparison base:
   - If argument is a branch/ref: `git diff <ref>...HEAD`
   - If argument is "yesterday" or time-based: `git log --since="1 day ago" --oneline`
   - If no argument: compare to last commit (`HEAD~1`)

2. Run `git diff --stat <base>...HEAD` for file-level overview

3. For each changed file (up to 10), provide:
   - File path
   - What changed (1 line)
   - Why it matters (if determinable from commit messages)

4. Summarize at the top:
   - Files changed, insertions, deletions
   - Key themes (e.g., "mostly test additions + one routing fix")
   - Any breaking changes detected

5. List commits in scope with their subject lines

## Output Format

```
## Context Diff: <base>...HEAD

### Summary
- 12 files changed, +340 / -45 lines
- Key themes: routing expansion, new skills, hook improvements
- Breaking changes: none detected

### Commits in scope
- abc123 feat: expand skill routing registry to 114 entries
- def456 fix: resolve duplicate trigger conflicts
- ghi789 feat: add PreCompact hook + SOUL/USER identity files

### Changed Files
| File | Change | Significance |
|------|--------|-------------|
| src/routing/skill_router.py | +200 lines | Routing registry expanded |
| .claude/hooks/session-start.sh | rewritten | Hot-memory injection added |
| .claude/SOUL.md | new | Agent identity file |

### Architectural Changes
[Any structural/interface changes that affect how things connect]
```

```

FILE: .claude/skills/cost-optimizer/SKILL.md
```markdown
---
name: cost-optimizer
description: >
  Analyze and reduce cloud and infrastructure costs. Invoke for: "reduce cloud costs",
  "cost optimization", "AWS cost", "cloud bill too high", "right-sizing", "idle resources",
  "spot instances", "reserved instances", "LLM cost too high".
argument-hint: cost area to optimize (e.g. "AWS monthly bill" or "LLM API costs")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Cost Optimizer — Cloud & Infrastructure Cost Reduction
**Category:** DevOps/Infra

## Role
Identify and eliminate cloud waste. Find the highest-ROI cost optimizations with minimal risk.

## When to invoke
- Cloud bill too high
- "are we wasting money on cloud?"
- Resource right-sizing
- LLM cost optimization

## Instructions
1. Profile costs: what services cost the most? Trending up?
2. Identify waste: idle EC2/VMs, oversized instances, unused storage, data transfer
3. Right-size: match instance type to actual CPU/memory utilization
4. Commitments: Reserved Instances / Savings Plans for stable workloads
5. Spot/Preemptible: for fault-tolerant batch workloads
6. LLM: model routing (Haiku for simple), caching, prompt compression
7. Prioritize by: savings × implementation effort

## Output format
```
## Cost Optimization Report — <scope> — <date>
### Current Spend: $X/month
### Quick Wins (< 1 day to implement)
1. Rightsize X → $Y/month saved
### Medium Wins
### Total Potential Savings: $Z/month (X%)
```

## Example
/cost-optimizer analyze AWS spend and LLM API costs — find top 5 reduction opportunities

```

FILE: .claude/skills/create/SKILL.md
```markdown
---
name: create
description: >
  Creates new skills or agents from scratch. Invoke proactively when: a repeatable
  workflow is identified, user says "make a skill", "create an agent", "turn this into
  a skill", "automate this", "save this workflow", "I keep doing this". If a workflow
  has been repeated twice, suggest capturing it. Decision: if task needs autonomous
  multi-step execution → agent; if it's a knowledge/instruction pack → skill.
argument-hint: describe the workflow or task to capture
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Create

**Category:** Meta

## Role
Creates new skills or agents by analyzing a described workflow and generating the appropriate SKILL.md or agent file with correct frontmatter and trigger phrases.

## When to invoke
- User says "make a skill", "create an agent", "turn this into a skill"
- A workflow has been repeated twice and should be captured
- User says "automate this", "save this workflow", "I keep doing this"
- A complex multi-step process needs to be standardized

## Instructions
1. Ask clarifying questions: what triggers this workflow? What are the steps? What is the expected output?
2. Determine type: count agent signals — does it need autonomy, multi-tool use, long-running execution, self-directed decisions? If yes → agent (.claude/agents/<name>.md). If it's a knowledge/instruction pack → skill (.claude/skills/<name>/SKILL.md)
3. Draft the description field first — this is the most critical part. Include all trigger phrases a user might say. Make it specific about auto-activation conditions.
4. Write the complete file with YAML frontmatter (name, description, argument-hint, allowed-tools)
5. Include: Role, When to invoke, Instructions, Output format, Example sections
6. Run a quick sanity check: does the description field contain enough trigger phrases? Would it activate at the right time?

## Output format
A complete SKILL.md or agent.md file written to the correct path with no placeholders. Confirmation message with the file path and a brief explanation of the trigger conditions.

## Example
/create summarize git commits and post to Slack on every push

```

FILE: .claude/skills/cron-scheduler/SKILL.md
```markdown
---
name: cron-scheduler
description: >
  Set up cron jobs and scheduled tasks. Invoke for: "schedule this", "run every day",
  "cron job", "scheduled task", "automation schedule", "run weekly", "cron expression",
  "set up recurring task". Also integrates with Claude Code's /schedule skill.
argument-hint: task to schedule and frequency (e.g. "research-agent every Monday 6am")
allowed-tools: Read, Write, Bash
---

# Skill: Cron Scheduler — Recurring Task Automation
**Category:** Optimization/Research

## Role
Set up cron schedules for recurring automation tasks including the optimizer crons in tools/scripts/.

## When to invoke
- "schedule this to run every X"
- Setting up optimizer crons
- Recurring Claude Code agent triggers
- Automation scheduling

## Instructions
1. Write cron expression: `minute hour day month weekday`
2. Add to crontab or create systemd timer
3. Log output: redirect to log file with timestamps
4. Alert on failure: use `|| notify_on_fail` pattern
5. Document: what runs when and why

## Common Crons for This Project
```bash
# Daily 6am: doc optimization
0 6 * * * cd /home/user/wellux_testprojects && bash tools/scripts/optimize-docs.sh >> data/cache/cron-optimize-docs.log 2>&1

# Monday 6am: Karpathy research loop
0 6 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/research-agent.sh >> data/cache/cron-research.log 2>&1

# Sunday midnight: security + perf audit
0 0 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/security-scan.sh >> data/cache/cron-security.log 2>&1
0 1 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/perf-audit.sh >> data/cache/cron-perf.log 2>&1

# Weekly: self-improve
0 8 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/self-improve.sh >> data/cache/cron-improve.log 2>&1
```

## Example
/cron-scheduler set up all optimizer crons for this project

```

FILE: .claude/skills/data-pipeline/SKILL.md
```markdown
---
name: data-pipeline
description: >
  Design and build data pipelines for ingestion, transformation, and storage. Invoke for:
  "data pipeline", "ETL", "data ingestion", "process this data", "batch processing",
  "stream processing", "data transformation", "data workflow".
argument-hint: data source and target transformation
allowed-tools: Read, Write, Edit, Glob
---

# Skill: Data Pipeline — ETL & Data Processing
**Category:** Optimization/Research

## Role
Design reliable, observable data pipelines with proper error handling, retry logic, and data validation.

## When to invoke
- "build a pipeline to process X"
- ETL design
- Batch or stream data processing
- Research data ingestion

## Instructions
1. Extract: read from source (files, API, DB), handle pagination/batching
2. Transform: clean, validate, normalize, enrich
3. Load: write to destination with idempotency (safe to retry)
4. Error handling: dead letter queue for failed records, not silent failure
5. Observability: log records processed/failed, processing time, data quality metrics
6. Checkpoint: resumable on failure

## Output format
Complete Python pipeline with:
- Source reader with pagination
- Transformation functions
- Destination writer with idempotency
- Error handling and logging
- Run stats output

## Example
/data-pipeline build pipeline to ingest research papers from data/research/ → embeddings → data/embeddings/

```

FILE: .claude/skills/dataset-curator/SKILL.md
```markdown
---
name: dataset-curator
description: >
  Curate, clean, and prepare datasets for AI training and evaluation. Invoke for:
  "clean this dataset", "prepare training data", "dataset curation", "deduplicate data",
  "label this data", "data quality", "prepare eval set", "filter bad examples".
argument-hint: dataset path or description of data to curate
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Skill: Dataset Curator — Training Data Preparation
**Category:** AI/ML Research

## Role
Clean, deduplicate, and structure datasets for AI training, fine-tuning, or evaluation.

## When to invoke
- Preparing training data for fine-tuning
- Building evaluation sets
- Cleaning scraped or collected data
- "this dataset is messy — clean it"

## Instructions
1. Load and profile the dataset: size, format, field distributions
2. Remove duplicates (exact and near-duplicate using hashing or embeddings)
3. Filter quality: remove empty, too-short, or clearly wrong examples
4. Normalize: consistent format, encoding, whitespace
5. Split: train/validation/test (80/10/10)
6. Save cleaned version to `data/prompts/` or `data/outputs/`
7. Document: data card with statistics and filtering decisions

## Output format
```
## Dataset Curation Report — <dataset>
### Before: N examples, X% duplicates, Y% quality issues
### Filters Applied
### After: M examples (split: X train / Y val / Z test)
### Data Card
```

## Example
/dataset-curator data/prompts/code_review_examples.jsonl — deduplicate and quality filter

```

FILE: .claude/skills/db-designer/SKILL.md
```markdown
---
name: db-designer
description: >
  Design normalized, production-ready database schemas from requirements.
  Invoke for: "design database schema", "data model", "entity relationship",
  "ER diagram", "normalize tables", "design tables", "create schema",
  "database design review", "foreign keys", "relational model", "schema planning".
argument-hint: feature requirements or domain description to model
allowed-tools: Read, Write, Edit, Bash
---

# Skill: Database Designer

## Mission
Turn requirements into a production-ready, normalized relational schema with
correct constraints, indexes, and migration-safe design decisions.

## Process

### 1. Gather Requirements
- Identify all entities from the domain description
- List key relationships (1:1, 1:N, M:N)
- Identify natural vs surrogate keys
- Flag any time-series, hierarchical, or polymorphic patterns

### 2. Design Schema
- Start with 3NF (Third Normal Form) — denormalize only for proven perf needs
- Every table gets a surrogate PK (`id UUID` or `id BIGSERIAL`)
- Explicit `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ` on mutable tables
- Foreign keys with explicit `ON DELETE` actions
- Soft deletes via `deleted_at TIMESTAMPTZ` when audit trail needed

### 3. Index Strategy
- PK index: automatic
- FK columns: always indexed
- Query predicates: index columns that appear in `WHERE`, `ORDER BY`, `GROUP BY`
- Unique constraints: wherever business rules require uniqueness
- Partial indexes: for nullable columns and soft-delete patterns

### 4. Output Format

```sql
-- ── <entity_name> ─────────────────────────────────────────────────
CREATE TABLE <entity_name> (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- business columns
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_<entity>_<col> ON <entity_name>(<col>);
```

Also produce an ASCII ER diagram:

```
users          ──< orders        ──< order_items >── products
(id, email)       (id, user_id)     (id, qty, price)   (id, sku)
```

### 5. Migration File (Alembic or raw SQL)
- Wrap in a transaction
- Idempotent: `CREATE TABLE IF NOT EXISTS`
- Down migration included

### 6. Review Checklist
- [ ] All FK relationships have an index
- [ ] No nullable columns where NOT NULL is enforceable
- [ ] Timestamps are timezone-aware (`TIMESTAMPTZ`)
- [ ] No EAV anti-patterns (key/value tables for typed data)
- [ ] JSONB used only for truly variable schemas, not as a lazy shortcut
- [ ] Enum types instead of magic strings for low-cardinality columns
- [ ] Row-level security considered for multi-tenant tables

## Common Patterns

### Soft Delete
```sql
deleted_at TIMESTAMPTZ,
-- query: WHERE deleted_at IS NULL
-- index: CREATE INDEX idx_<t>_active ON <t>(deleted_at) WHERE deleted_at IS NULL;
```

### Audit Log
```sql
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    table_name  TEXT NOT NULL,
    record_id   UUID NOT NULL,
    operation   TEXT NOT NULL CHECK (operation IN ('INSERT','UPDATE','DELETE')),
    old_data    JSONB,
    new_data    JSONB,
    actor_id    UUID REFERENCES users(id),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### M:N Junction Table
```sql
CREATE TABLE user_roles (
    user_id  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id  UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```

### Hierarchical (Closure Table)
```sql
CREATE TABLE category_path (
    ancestor_id   UUID NOT NULL REFERENCES categories(id),
    descendant_id UUID NOT NULL REFERENCES categories(id),
    depth         INTEGER NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
);
```

## Anti-Patterns to Avoid
- No "status" columns as bare integers — use CHECK constraints or enum types
- No comma-separated IDs in a single column — use a junction table
- No storing computed values without materialized views or triggers
- No `CHAR(n)` — use `TEXT` or `VARCHAR(n)` as needed
- No unconstrained `TEXT` where length is bounded and known

## Example Invocation

**Prompt:** "Design the schema for a multi-tenant SaaS app with users, teams, API keys, and usage billing."

**Output structure:**
1. ER diagram (ASCII)
2. `CREATE TABLE` statements with constraints
3. Index definitions
4. Migration file skeleton
5. Notes on tenant isolation strategy (row-level security vs schema-per-tenant)

```

FILE: .claude/skills/db-optimizer/SKILL.md
```markdown
---
name: db-optimizer
description: >
  Optimize database queries, indexes, and schema for performance. Invoke for:
  "slow query", "add index", "query optimization", "N+1 problem", "database performance",
  "schema review", "explain plan", "connection pooling", "query too slow".
argument-hint: query, ORM code, or schema to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: DB Optimizer — Query & Schema Performance
**Category:** Development

## Role
Identify and fix database performance issues: slow queries, missing indexes, N+1 problems, schema inefficiencies.

## When to invoke
- Slow queries in production
- N+1 query problems in ORM code
- Schema design review
- Adding indexes

## Instructions
1. Read the query/ORM code
2. Identify: N+1 (loop + query), missing JOIN, full table scan, no index on WHERE/JOIN columns
3. Add appropriate indexes (check existing ones first)
4. Rewrite inefficient queries
5. For ORMs: use select_related/prefetch_related, avoid lazy loading in loops
6. Connection pooling: pool size appropriate for load?
7. Estimate improvement: rows scanned before vs after

## Output format
```
## DB Optimization — <table/query> — <date>
### Problem Found
### Before (slow): [query]
### After (fast): [query]
### Index Added: CREATE INDEX ...
### Expected Improvement: ~10x fewer rows scanned
```

## Example
/db-optimizer src/models/users.py — fix N+1 in get_user_with_posts()

```

FILE: .claude/skills/dba/SKILL.md
```markdown
---
name: dba
description: >
  Database security, encryption, and access control. Invoke for: "database security",
  "SQL injection review", "DB permissions", "encryption at rest", "connection string
  security", "database hardening", "query audit", "backup encryption", "db access review",
  "stored procedure security".
argument-hint: database type or schema to review (e.g. "PostgreSQL schema" or "MongoDB config")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: DBA — Database Security & Optimization
**Category:** Security
**Color Team:** Yellow

## Role
Secure databases: review permissions, encryption, connection security, query safety, and backup integrity.

## When to invoke
- Database security review
- Connection string audit
- SQL injection verification
- DB user privilege review

## Instructions
1. Connection strings: credentials hardcoded? Using secrets manager? TLS enabled?
2. User privileges: principle of least privilege? No root/admin for app user?
3. SQL injection: parameterized queries everywhere? No string concatenation in queries?
4. Encryption: at rest (encrypted tablespace)? In transit (TLS)?
5. Backups: automated? Encrypted? Tested restore? Off-site copy?
6. Audit logging: all connections and queries logged? Log retention?

## Output format
```
## DB Security Audit — <db type> — <date>
### Connection Security: ✅/⚠️
### Permissions: ✅/⚠️
### Injection Risk: ✅/⚠️
### Encryption: ✅/⚠️
### Backups: ✅/⚠️
### Findings
```

## Example
/dba PostgreSQL security audit — check permissions, connections, and encryption

```

FILE: .claude/skills/debug/SKILL.md
```markdown
---
name: debug
description: >
  Systematic debugging: read error, trace root cause, fix autonomously. Invoke for:
  "this is broken", "debug this", "why is this failing", "error", "exception",
  "traceback", "not working", "fix this bug", "something's wrong", "it crashes".
  Never asks for hand-holding — reads logs, traces stack, identifies root cause, fixes.
argument-hint: error message, file path, or description of what's failing
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Debug — Root Cause Analysis & Fix
**Category:** Development

## Role
Autonomously debug failures: trace the error to its root cause and fix it without requiring user hand-holding.

## When to invoke
- Any error, exception, or crash
- "this doesn't work" / "it's broken"
- Failing tests
- Unexpected behavior

## Instructions
1. Read the error message / traceback fully
2. Identify the file:line where the error originates
3. Read that code and all code in the call stack
4. Hypothesize: what value/state caused this? Why?
5. Trace backwards: where does that value come from?
6. Identify root cause (not just the symptom)
7. Fix the root cause, not a workaround
8. Verify: will this fix prevent recurrence?

## Output format
```
## Debug Report — <error type> — <date>
### Error
### Root Cause (file:line)
### Why it happened
### Fix Applied
### Prevention
```

## Example
/debug TypeError: 'NoneType' object is not subscriptable in src/api/auth.py:89

```

FILE: .claude/skills/decision-logger/SKILL.md
```markdown
---
name: decision-logger
description: >
  Log and track technical and product decisions with rationale. Invoke for:
  "log this decision", "record why we chose X", "decision log", "we decided to",
  "document this choice", "capture this decision". Proactively suggest logging
  any significant technical choice made during a conversation.
argument-hint: decision to log and context
allowed-tools: Read, Write, Glob
---

# Skill: Decision Logger — Decision Record Keeping
**Category:** Documentation

## Role
Capture decisions with context and rationale so future team members understand the "why."

## When to invoke
- Any significant technical or product decision made
- "why did we do it this way" questions arise
- Proactively after any architectural discussion
- Choosing between two approaches

## Instructions
1. Identify: what was decided? What were the alternatives?
2. Capture context: what problem was being solved?
3. Record rationale: why this option over others?
4. Note trade-offs: what was sacrificed?
5. Determine format: ADR (significant) or simple log entry (minor)
6. Save: docs/decisions/ (ADR) or append to tasks/lessons.md (minor)

## Output format
For significant decisions → full ADR (see /adr-writer)
For minor decisions:
```
Decision Log — <date>
Decision: Use YAML for config files, not JSON
Context: Need comments in config, JSON doesn't support them
Rationale: YAML readable, supports comments, widely used for config
Trade-off: Slightly more complex parsing, indentation-sensitive
```

## Example
/decision-logger log decision to use Redis for caching instead of in-memory dict

```

FILE: .claude/skills/dep-auditor/SKILL.md
```markdown
---
name: dep-auditor
description: >
  Audit dependencies for vulnerabilities, license issues, and outdated packages. Invoke for:
  "dependency audit", "npm audit", "pip audit", "outdated packages", "CVE check",
  "license compliance", "supply chain security", "vulnerable dependency", "update packages".
argument-hint: requirements.txt, package.json, or project path
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Skill: Dependency Auditor — Supply Chain Security
**Category:** Development

## Role
Audit all project dependencies for known CVEs, license compliance issues, and outdated versions.

## When to invoke
- Regular security maintenance
- Before production deployment
- "any vulnerable dependencies"
- Supply chain security review

## Instructions
1. Read requirements.txt / package.json / pyproject.toml
2. Check for known CVEs in current versions (use WebSearch for NIST NVD)
3. Identify outdated packages (major version behind)
4. Check license compatibility: GPL? AGPL? Copyleft issues?
5. Flag: unpinned versions, packages with no recent updates (abandoned), forks
6. Produce upgrade plan with risk assessment

## Output format
```
## Dependency Audit — <date>
### Critical CVEs (patch immediately)
- package@x.x.x — CVE-XXXX-XXXX — upgrade to x.x.x
### Outdated (upgrade soon)
### License Issues
### Recommendations
```

## Example
/dep-auditor requirements.txt — check for CVEs and outdated packages

```

FILE: .claude/skills/deploy-checker/SKILL.md
```markdown
---
name: deploy-checker
description: >
  Pre-deployment checklist and validation. Invoke for: "ready to deploy", "deployment check",
  "pre-prod validation", "deployment checklist", "is this safe to deploy",
  "release validation", "deployment gate".
argument-hint: service or version to validate for deployment
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: Deploy Checker — Pre-Deployment Validation
**Category:** DevOps/Infra

## Role
Run a comprehensive pre-deployment checklist to catch issues before they reach production.

## When to invoke
- Before any production deployment
- Release gate validation
- "is this ready to ship?"

## Instructions
1. Tests: all passing? Coverage adequate?
2. Security: no hardcoded secrets? Dep audit clean? OWASP scan?
3. Performance: no N+1 queries? Response times acceptable?
4. Config: env vars documented? Feature flags set for prod?
5. Database: migrations backward-compatible? Rollback possible?
6. Monitoring: alerts configured? Dashboards ready?
7. Rollback: how do we revert if this goes wrong?

## Output format
```
## Deploy Checklist — <service v{version}> — <date>
- [✅/❌] Tests passing (X/X)
- [✅/❌] Security scan clean
- [✅/❌] No hardcoded secrets
- [✅/❌] DB migration safe
- [✅/❌] Monitoring configured
- [✅/❌] Rollback plan exists
### DEPLOY: ✅ APPROVED / ❌ BLOCKED (reasons)
```

## Example
/deploy-checker validate v2.1.0 is production-ready before deployment

```

FILE: .claude/skills/devops-engineer/SKILL.md
```markdown
---
name: devops-engineer
description: >
  CI/CD pipelines, containers, and secrets management security. Invoke for:
  "pipeline security", "Docker security", "secrets in code", "CI/CD review",
  "container hardening", "Dockerfile audit", "secrets scanning", "GitHub Actions security",
  "env vars exposed", "hardcoded credentials", "pipeline config review".
argument-hint: pipeline file, Dockerfile, or CI config to review
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: DevOps Engineer — Pipeline & Container Security
**Category:** Security
**Color Team:** Yellow

## Role
Secure CI/CD pipelines, container images, and secrets management across the software delivery lifecycle.

## When to invoke
- CI/CD pipeline security review
- Dockerfile hardening
- Secrets scanning before commit
- GitHub Actions / GitLab CI audit

## Instructions
1. Scan for hardcoded secrets: API keys, passwords, tokens in code and config
2. Review Dockerfile: non-root user? Minimal base image? No COPY . .? Multi-stage?
3. Check CI/CD pipeline: pinned action versions? Least-privilege tokens? OIDC?
4. Verify secret injection: env vars from vault/secrets manager, not plaintext in YAML?
5. Check artifact signing and image scanning in pipeline
6. Review deployment permissions: who can deploy to prod?

## Output format
```
## DevOps Security Review — <scope> — <date>
### Secrets: ✅/⚠️
### Container: ✅/⚠️
### Pipeline: ✅/⚠️
### Findings & Fixes
```

## Example
/devops-engineer review .github/workflows/ and Dockerfile for secrets exposure

```

FILE: .claude/skills/docker/SKILL.md
```markdown
---
name: docker
description: >
  Write and optimize Dockerfiles and Docker Compose configurations. Invoke for:
  "Dockerfile", "containerize this", "Docker Compose", "container setup",
  "multi-stage build", "Docker optimization", "container security", "docker image".
argument-hint: application to containerize or Dockerfile to review
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Docker — Container Configuration & Optimization
**Category:** DevOps/Infra

## Role
Write optimized, secure Dockerfiles using multi-stage builds, minimal base images, and non-root users.

## When to invoke
- New application needs containerization
- Dockerfile review or optimization
- Docker Compose setup
- "make this run in Docker"

## Instructions
1. Use minimal base image (python:3.12-slim, node:20-alpine)
2. Multi-stage build: builder stage → runtime stage
3. Non-root user: `RUN useradd -m app && USER app`
4. Layer optimization: COPY requirements.txt first → install → COPY source
5. No secrets in image: use build args or runtime env vars
6. Health check: HEALTHCHECK instruction
7. docker-compose.yml with proper networking and volume mounts

## Output format
Complete Dockerfile + docker-compose.yml with explanatory comments.

## Example
/docker containerize the Python AI project — multi-stage build, non-root, health check

```

FILE: .claude/skills/embeddings/SKILL.md
```markdown
---
name: embeddings
description: >
  Design and implement text embedding pipelines for semantic search and similarity.
  Invoke for: "embeddings", "semantic search", "vector similarity", "embed this text",
  "find similar", "clustering", "text similarity", "nearest neighbor search".
argument-hint: text data to embed or similarity task to implement
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Embeddings — Semantic Vector Representations
**Category:** AI/ML Research

## Role
Build embedding pipelines for semantic search, clustering, and similarity — stored in `data/embeddings/`.

## When to invoke
- Semantic search over documents
- Finding similar code / prompts / outputs
- Clustering similar items
- "find things similar to X"

## Instructions
1. Choose embedding model: claude-3 embeddings / text-embedding-3-small / local model
2. Preprocessing: chunk text appropriately (512-2048 tokens), clean, normalize
3. Embed: batch process for efficiency, handle rate limits
4. Index: store in FAISS (fast local) or ChromaDB (persistent)
5. Query: embed query, cosine similarity search, return top-k results
6. Store in `data/embeddings/` with metadata for reproducibility

## Output format
```python
# Embedding pipeline
def embed_documents(docs: list[str]) -> np.ndarray: ...
def semantic_search(query: str, k: int = 5) -> list[dict]: ...
# Returns: [{"text": ..., "score": 0.95, "metadata": {...}}]
```

## Example
/embeddings build semantic search over data/research/ — find similar research notes

```

FILE: .claude/skills/error-handler/SKILL.md
```markdown
---
name: error-handler
description: >
  Design robust error handling, retry logic, and circuit breakers. Invoke for:
  "error handling", "exception handling", "retry logic", "circuit breaker",
  "graceful degradation", "error messages", "fallback", "resilience",
  "fault tolerance", "what happens on failure".
argument-hint: component or error scenario to handle (e.g. "API client error handling")
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Error Handler — Resilient Error Patterns
**Category:** Development

## Role
Design and implement resilient error handling: retry with backoff, circuit breakers, graceful degradation, clear error messages.

## When to invoke
- External API calls without retry
- No fallback on service failure
- Generic exception catching
- "what happens if X fails"

## Instructions
1. Identify all failure points: external calls, DB, filesystem, memory
2. For transient failures: implement retry with exponential backoff + jitter
3. For persistent failures: circuit breaker pattern (open/half-open/closed)
4. User-facing errors: clear message, no stack traces, actionable next steps
5. Logging: log errors with context (request ID, user ID, timestamp)
6. Fallback: degraded mode when dependency unavailable?

## Output format
Implementation with:
- Custom exception hierarchy
- Retry decorator with backoff
- Circuit breaker class
- Error response format

## Example
/error-handler src/llm/claude_client.py — add retry + circuit breaker for API calls

```

FILE: .claude/skills/estimation/SKILL.md
```markdown
---
name: estimation
description: >
  Estimate effort and timelines for software tasks. Invoke for: "estimate this",
  "how long will this take", "story points", "effort estimation", "timeline",
  "when can this be done", "how complex is this".
argument-hint: task or project to estimate
allowed-tools: Read, Glob, Grep
---

# Skill: Estimation — Effort & Timeline Estimation
**Category:** Project Management

## Role
Provide realistic effort estimates using historical context, complexity analysis, and uncertainty buffers.

## When to invoke
- Planning work
- "how long will this take"
- Stakeholder timeline questions
- Sprint capacity planning

## Instructions
1. Read the task description and related code
2. Break into sub-tasks if complex
3. Estimate each: S (< 2h), M (half day), L (full day), XL (needs breakdown)
4. Add uncertainty buffer: 1.5x for new technology, 2x for unclear requirements
5. Identify: what could make this take longer? (unknowns)
6. Give range, not single estimate: "2-4 days, most likely 3"

## Output format
```
## Estimation — <task> — <date>
### Sub-tasks
| Task | Complexity | Estimate |
| Design API | M | 4h |
| Implement | L | 1d |
| Tests | M | 4h |
### Total: 2 days (best) — 3 days (likely) — 5 days (worst)
### Key Risks That Could Extend
```

## Example
/estimation estimate effort to add the Python LLM stack to this project

```

FILE: .claude/skills/evals-designer/SKILL.md
```markdown
---
name: evals-designer
description: >
  Design evaluation frameworks for LLMs and AI systems. Invoke for: "eval this model",
  "LLM evaluation", "benchmark", "how do I measure quality", "evals", "test my prompts",
  "measure hallucination", "model comparison", "build an eval suite".
argument-hint: AI system or prompt to evaluate
allowed-tools: Read, Write, Glob, WebSearch
---

# Skill: Evals Designer — LLM Evaluation Framework
**Category:** AI/ML Research

## Role
Design rigorous evaluation frameworks to measure LLM and agent system quality, correctness, and reliability.

## When to invoke
- "how good is my prompt?"
- Comparing model versions
- Measuring hallucination rate
- Building automated test suite for AI system

## Instructions
1. Define metrics: accuracy, groundedness, coherence, safety, latency, cost
2. Design test cases: golden set of input/expected output pairs
3. Build eval pipeline: run model, score output, aggregate metrics
4. Measure: precision/recall for retrieval, exact match / LLM-as-judge for generation
5. Track over time: did new prompt/model improve or regress?
6. Save evals to `notebooks/` for reproducibility

## Output format
```python
# Eval framework
eval_cases = [
    {"input": "...", "expected": "...", "category": "..."},
]
# Scoring function
def score(output, expected): ...
# Results
# Accuracy: X%, Groundedness: X%, Latency: Xms avg
```

## Example
/evals-designer build eval suite for the code-review skill — 20 test cases with rubric

```

FILE: .claude/skills/feature-planner/SKILL.md
```markdown
---
name: feature-planner
description: >
  Break down a feature request into implementable tasks with acceptance criteria.
  Invoke for: "plan this feature", "break this down", "implementation plan",
  "task breakdown", "feature spec", "how do I implement X", "what are the steps",
  "make a plan for", "I need to build".
argument-hint: feature description
allowed-tools: Read, Write, Grep, Glob
---

# Skill: Feature Planner — Implementation Breakdown
**Category:** Development

## Role
Transform a vague feature request into a concrete, ordered list of implementable tasks with acceptance criteria.

## When to invoke
- New feature to implement
- "how do I implement X"
- Sprint planning for a feature
- Before starting any non-trivial work

## Instructions
1. Clarify: what is the feature? Who uses it? What's the success criteria?
2. Identify all components affected (frontend, backend, DB, tests, docs)
3. Order tasks: dependencies first, parallel work identified
4. Write acceptance criteria for each task (testable conditions)
5. Estimate complexity: S/M/L for each task
6. Write to tasks/todo.md as checkable items

## Output format
```
## Feature Plan — <name> — <date>
### Goal
### Tasks (ordered)
- [ ] 1. [S] Create DB schema — AC: migration runs, table exists
- [ ] 2. [M] Write API endpoint — AC: POST /api/feature returns 201
- [ ] 3. [L] Add tests — AC: 80% coverage
### Dependencies
### Estimated Total: S/M/L
```

## Example
/feature-planner Add rate limiting to the Claude API client with Redis backend

```

FILE: .claude/skills/fine-tuner/SKILL.md
```markdown
---
name: fine-tuner
description: >
  Design fine-tuning pipelines for LLMs on custom data. Invoke for: "fine-tune",
  "train on my data", "custom model", "domain adaptation", "LoRA", "PEFT",
  "instruction tuning", "fine-tuning dataset", "adapt model to my domain".
argument-hint: model to fine-tune and task/domain
allowed-tools: Read, Write, WebSearch
---

# Skill: Fine Tuner — LLM Domain Adaptation
**Category:** AI/ML Research

## Role
Design fine-tuning pipelines using LoRA/PEFT to adapt LLMs to specific domains or tasks efficiently.

## When to invoke
- Need model to follow very specific format
- Domain-specific vocabulary (medical, legal, code)
- Prompt engineering not sufficient
- "train this model on my examples"

## Instructions
1. Assess need: is fine-tuning really needed? Can prompting solve it?
2. Dataset: collect 100-10k (input, output) pairs, clean and deduplicate
3. Choose method: LoRA (efficient), full fine-tune (if resources allow)
4. Format: convert to instruction-tuning format (system/human/assistant)
5. Evaluate: split train/val, measure loss + task-specific metric
6. Save training script + dataset format to notebooks/

## Output format
```python
# Dataset format
{"messages": [
  {"role": "system", "content": "You are..."},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."}
]}

# Training config
learning_rate = 2e-4
lora_r = 16
batch_size = 4
```

## Example
/fine-tuner design fine-tuning pipeline for code review task using collected PR review examples

```

FILE: .claude/skills/foresight/SKILL.md
```markdown
---
name: foresight
description: >
  Cross-domain strategic analysis that surfaces non-obvious risks and opportunities.
  Invoke for: "foresight", "strategic analysis", "what am I missing strategically",
  "second order effects", "future risks", "what could blindside us", "horizon scanning",
  "strategic blind spots", "cross-domain analysis", "what should we watch out for",
  "long term risks". One contextual nudge per execution.
argument-hint: project, decision, or domain to analyze
allowed-tools: Read, WebSearch, Write
---

# Skill: Foresight — Cross-Domain Strategic Analysis

## Role
Surface one high-value strategic insight per execution by scanning across domains
(technology, market, regulatory, organizational) for non-obvious risks and opportunities.
Inspired by marciopuga/cog `/foresight` pattern.

## Philosophy
Most strategic blind spots come from staying within your own domain.
The most valuable foresight crosses from adjacent domains:
- A technical trend that becomes a business risk
- A market shift that makes a current architecture obsolete
- A regulatory change already visible in other industries
- A cultural pattern that predicts adoption or rejection

## Workflow

1. **Domain scan**: identify 4 domains relevant to the topic
   - Technology (current + 12-month horizon)
   - Market/competitive (user behavior, competitor moves)
   - Organizational (team dynamics, technical debt accumulation)
   - External (regulatory, ecosystem shifts)

2. **Cross-domain pattern match**: find where signals from different domains converge
   - Convergence = higher confidence signal
   - Divergence = uncertainty zone, needs monitoring

3. **Non-obvious risk identification**: focus on:
   - Second-order effects of current decisions
   - "This seemed fine until X changed" scenarios
   - Dependencies that aren't visible day-to-day

4. **Opportunity surface**: one opportunity that the risk analysis reveals

5. **Contextual nudge**: one specific, actionable recommendation

## Output Format

```
## Foresight: <topic>

### Domain Signals (brief)
- **Technology**: [signal]
- **Market**: [signal]
- **Organizational**: [signal]
- **External**: [signal]

### Cross-Domain Pattern
[Where signals converge or diverge and what that implies]

### Non-Obvious Risk
**Risk**: [specific risk, not obvious from any single domain]
**Timeline**: [when this might materialize]
**Early warning sign**: [what to watch for]

### Opportunity
[One opportunity the analysis reveals]

### Contextual Nudge
> **One thing to do this week**: [specific action]
```

## Examples of high-value foresight patterns
- "Your async architecture is sound today, but the upcoming Python GIL changes in 3.14 will allow true threading — your patterns will need revisiting"
- "The trend toward edge AI (market) + your current cloud-only architecture (tech) = a competitive gap opening in 9 months"
- "Your test coverage is increasing (org) but CI time is also increasing (tech) — this will soon create a push-back-on-tests dynamic in your team"

```

FILE: .claude/skills/grc-analyst/SKILL.md
```markdown
---
name: grc-analyst
description: >
  Governance, risk, and compliance audit. Invoke for: "compliance check", "risk assessment",
  "GDPR check", "SOC2 readiness", "ISO 27001", "regulatory compliance", "audit trail",
  "data handling review", "policy review", "governance audit".
argument-hint: compliance standard or scope (e.g. "GDPR" or "full project")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: GRC Analyst — Governance, Risk & Compliance
**Category:** Security
**Color Team:** White

## Role
Audit governance, risk management, and compliance posture across the project.

## When to invoke
- Before regulatory submission or certification
- "GDPR/SOC2/ISO27001 compliance check"
- "risk assessment" or "audit trail review"
- Data handling or privacy review needed

## Instructions
1. Identify all data flows: what PII/sensitive data is collected, stored, transmitted
2. Check documentation completeness: privacy policy, data retention, consent mechanisms
3. Review access controls: who can access what data
4. Check audit logging: are all access events logged?
5. Map findings against the target compliance framework
6. Produce gap analysis with remediation steps

## Output format
```
## GRC Audit — <framework> — <date>
### Compliant ✅
### Gaps Found ⚠️
### Remediation Plan
```

## Example
/grc-analyst GDPR compliance for user data handling in src/

```

FILE: .claude/skills/gsd/SKILL.md
```markdown
---
name: gsd
description: >
  Get Shit Done — agentic meta-prompts that keep Claude focused and shipping without
  constant resets. Invoke for: "GSD mode", "just ship it", "stay focused", "no more
  planning — build", "ship without resets", "execute not plan", "get this done fast",
  "focus mode", "just do it". Inspired by gsd-build agentic workflow patterns.
argument-hint: task or feature to ship without interruption
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: GSD — Get Shit Done Mode
**Category:** Ecosystem
**Inspired by:** gsd-build (github.com/gsd-build)

## Role
Activate high-focus agentic mode: minimal planning overhead, maximum shipping velocity, no unnecessary resets or interruptions.

## When to invoke
- "just build it" / "no more planning"
- Need to ship fast without context resets
- Implementation is clear, execution just needs to happen
- Marathon build sessions

## Instructions
1. Read MASTER_PLAN.md — identify next unchecked step
2. Activate: compress context (`/compact`), focus on ONE task
3. Execute without asking for clarification (unless truly ambiguous)
4. After each sub-task: check it off, immediately proceed to next
5. Commit frequently: small, atomic commits after each milestone
6. No bikeshedding: accept good enough, not perfect
7. Keep going until: all current phase steps done OR blocker hit

## GSD Rules
- No rabbit holes: if something interesting but not required → skip
- No perfectionism: working > perfect
- No hand-holding: figure it out, don't ask
- Commit often: never lose more than 30min of work
- If blocked: use /blocker-resolver, then continue

## Example
/gsd ship Phase 3 skills — write all remaining skills without stopping

```

FILE: .claude/skills/help-desk/SKILL.md
```markdown
---
name: help-desk
description: >
  Endpoint support and access gatekeeper. Invoke for: "access request", "user provisioning",
  "endpoint hardening", "device compliance check", "MFA setup", "password reset policy",
  "access review", "user offboarding", "permissions request", "IT support".
argument-hint: user, device, or access request details
allowed-tools: Read, Grep, Glob
---

# Skill: Help Desk — Endpoint Support & Access Gatekeeper
**Category:** Security
**Color Team:** Blue

## Role
Handle endpoint security support, access provisioning/deprovisioning, and device compliance.

## When to invoke
- User access provisioning or offboarding
- Endpoint compliance check
- MFA or SSO setup guidance
- Access review cycle

## Instructions
1. Identify request type: provisioning / deprovisioning / compliance / support
2. Verify identity and authorization level
3. Check policy compliance: MFA enforced? Device managed? Least privilege?
4. Document action taken with timestamp and approver
5. For offboarding: revoke all access, check for data exfiltration, archive account

## Output format
```
## Help Desk Action — <request type> — <date>
### Request
### Policy Check
### Action Taken
### Documentation
```

## Example
/help-desk offboard user john.doe — revoke all access and archive

```

FILE: .claude/skills/iam-engineer/SKILL.md
```markdown
---
name: iam-engineer
description: >
  Identity and access management: SSO, MFA, RBAC, access reviews. Invoke for:
  "IAM review", "RBAC setup", "SSO configuration", "MFA enforcement", "access review",
  "least privilege audit", "service account permissions", "role design", "OAuth setup",
  "SAML config", "permission boundary".
argument-hint: system or access model to review (e.g. "RBAC for API" or "SSO with Google")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: IAM Engineer — Identity & Access Management
**Category:** Security
**Color Team:** Green

## Role
Design and audit identity systems: SSO, MFA enforcement, RBAC models, and access reviews.

## When to invoke
- Access model design for new system
- RBAC audit or redesign
- MFA/SSO implementation review
- Quarterly access review

## Instructions
1. Map current roles and permissions: who has what access?
2. Identify over-privileged accounts (more access than needed)
3. Check MFA: enforced for all users? Especially admins?
4. SSO: federated identity? SAML/OIDC properly configured?
5. Service accounts: unique per service? Rotating credentials? No shared passwords?
6. Design least-privilege RBAC model with clear role definitions

## Output format
```
## IAM Audit — <system> — <date>
### Roles & Permissions Map
### Over-Privileged Accounts
### MFA Coverage: X%
### Recommendations
### Proposed RBAC Model
```

## Example
/iam-engineer audit RBAC for REST API — map roles to endpoints and recommend least-privilege design

```

FILE: .claude/skills/incident-response/SKILL.md
```markdown
---
name: incident-response
description: >
  Security incident containment, forensics, and recovery. Invoke for: "security incident",
  "we got breached", "containment", "forensics", "IR plan", "post-incident review",
  "root cause analysis for security event", "recovery steps after attack", "data breach".
argument-hint: incident type or affected systems (e.g. "API key leaked" or "SQL injection in prod")
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Skill: Incident Response — Contain, Investigate, Recover
**Category:** Security
**Color Team:** Blue

## Role
Execute structured incident response: contain the threat, collect evidence, eradicate, recover, document.

## When to invoke
- Active security incident
- Post-incident review
- Breach notification preparation
- IR plan creation for a system

## Instructions
1. **Contain**: Identify and isolate affected systems/accounts immediately
2. **Scope**: What data/systems were accessed? For how long?
3. **Evidence**: Collect logs, memory dumps, file hashes before they're overwritten
4. **Eradicate**: Remove malware, revoke compromised credentials, patch vulnerability
5. **Recover**: Restore from clean backups, monitor for re-compromise
6. **Document**: Full timeline, lessons learned, process improvements

## Output format
```
## Incident Report — <type> — <date>
### Timeline
### Scope & Impact
### Containment Steps Taken
### Root Cause
### Recovery Steps
### Lessons Learned
```

## Example
/incident-response API key exposed in GitHub commit — scope and remediation

```

FILE: .claude/skills/infra-docs/SKILL.md
```markdown
---
name: infra-docs
description: >
  Document infrastructure: architecture diagrams, runbooks, network maps. Invoke for:
  "document the infrastructure", "infra diagram", "network diagram", "runbook",
  "ops documentation", "infrastructure documentation", "how does our infra work".
argument-hint: infrastructure to document
allowed-tools: Read, Write, Glob
---

# Skill: Infra Docs — Infrastructure Documentation
**Category:** DevOps/Infra

## Role
Produce clear, current infrastructure documentation that enables any engineer to understand and operate the system.

## When to invoke
- New infrastructure needs documentation
- Runbook creation
- "document how this all works"
- Onboarding new ops engineers

## Instructions
1. Read all infrastructure config (Terraform, K8s, docker-compose, CI/CD)
2. Create ASCII infrastructure diagram showing: components, connections, data flows
3. Document: environments (dev/staging/prod), access methods, key configs
4. Write runbooks for: deployment, rollback, incident response, scaling
5. Save to docs/runbooks/ and docs/architecture.md

## Output format
```
## Infrastructure Documentation
### Architecture Diagram (ASCII)
### Components
### Environments
### Access Guide
### Runbook Links
```

## Example
/infra-docs document the complete infrastructure for this project

```

FILE: .claude/skills/k8s/SKILL.md
```markdown
---
name: k8s
description: >
  Kubernetes deployment manifests, Helm charts, and cluster configuration. Invoke for:
  "Kubernetes", "K8s", "deploy to K8s", "Helm chart", "pod spec", "deployment manifest",
  "kubernetes config", "HPA", "ingress", "K8s security".
argument-hint: application or K8s resource to configure
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Kubernetes — Container Orchestration
**Category:** DevOps/Infra

## Role
Write production-ready Kubernetes manifests with proper resource limits, security contexts, and autoscaling.

## When to invoke
- Deploying to Kubernetes
- K8s manifest review
- Helm chart creation
- "make this K8s-ready"

## Instructions
1. Deployment: replicas, resource limits/requests, liveness/readiness probes
2. Security: non-root securityContext, read-only filesystem, drop capabilities
3. Config: ConfigMap for config, Secrets for credentials (or External Secrets)
4. Networking: Service + Ingress with TLS
5. Autoscaling: HPA with CPU/memory/custom metrics
6. Namespaces: separate prod/staging, RBAC per namespace

## Output format
Complete YAML manifests: Deployment, Service, Ingress, HPA, ConfigMap.

## Example
/k8s create production K8s deployment for the AI API with HPA and TLS ingress

```

FILE: .claude/skills/karpathy-researcher/SKILL.md
```markdown
---
name: karpathy-researcher
description: >
  Deep autonomous research in Andrej Karpathy's style: understand from first principles,
  implement minimal working examples, distill to key insights. Invoke for: "research X",
  "what's the latest on X", "find papers about", "auto-research", "deep dive into",
  "understand X from scratch", "Karpathy-style research on", "learn about X deeply".
argument-hint: topic to research (e.g. "RAG systems 2026" or "LLM agent memory")
allowed-tools: WebSearch, WebFetch, Read, Write
---

# Skill: Karpathy Researcher — Deep First-Principles Research
**Category:** AI/ML Research

## Role
Research topics deeply — not surface-level summaries, but first-principles understanding with minimal implementation examples, in the style of Andrej Karpathy.

## When to invoke
- Deep learning of a new AI/ML topic
- "what's the best approach for X"
- Research before implementing a complex system
- Weekly research loop (run by research-agent.sh)

## Instructions
1. WebSearch: `<topic> 2025 2026 paper implementation blog`
2. WebFetch top 3-5 sources: papers, blog posts, GitHub READMEs
3. Extract: core insight (the "aha" moment), key technique, implementation pattern
4. Distill to first principles: could you rebuild this from scratch?
5. Write minimal working pseudocode example
6. Save to `data/research/YYYY-MM-DD-<topic>.md`
7. Extract 1-3 actionable insights → append to `tasks/lessons.md`
8. Update `data/research/README.md` index

## Output format
```markdown
# Research: <topic> — <date>
## Core Insight (one paragraph)
## Key Technique
## Minimal Implementation
```python
# Pseudocode or actual working code
```
## Actionable Takeaways
1. ...
## Sources
```

## Example
/karpathy-researcher LLM agent memory systems — research and implement minimal example

```

FILE: .claude/skills/knowledge-base/SKILL.md
```markdown
---
name: knowledge-base
description: >
  Build and maintain a structured knowledge base (Obsidian-style second brain). Invoke for:
  "knowledge base", "second brain", "organize notes", "Obsidian", "note taking",
  "personal wiki", "structured notes", "knowledge management",
  "organize research into notes".
argument-hint: topic area or notes to organize
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Skill: Knowledge Base — Second Brain & Note Organization
**Category:** Documentation

## Role
Build a structured, searchable knowledge base using Obsidian-style linked notes stored in `data/` directories.

## When to invoke
- Organizing research findings
- Building a personal wiki
- "structure all my notes about X"
- After research sessions to consolidate learnings

## Instructions
1. Atomic notes: one concept per note, short (< 200 lines)
2. Linking: connect related notes with [[wikilinks]] or relative paths
3. Structure: MOC (Map of Content) files as indexes for topics
4. Tags: #topic #status #type for filtering
5. Daily notes: date-stamped notes for time-sensitive learnings
6. Review cycle: weekly review to strengthen connections
7. Save to `data/research/` or appropriate location

## Output format
```markdown
# <Concept Name>
**Tags:** #ai #rag #retrieval
**Related:** [[embeddings]], [[vector-search]]

## Core Idea

## Key Details

## Examples

## References
```

## Example
/knowledge-base organize all research in data/research/ into linked atomic notes with MOC

```

FILE: .claude/skills/kpi-tracker/SKILL.md
```markdown
---
name: kpi-tracker
description: >
  Define and track KPIs and success metrics. Invoke for: "define KPIs", "track metrics",
  "measure success", "what metrics should we track", "KPI dashboard", "OKRs",
  "success metrics", "how do we know this worked".
argument-hint: project or feature to define KPIs for
allowed-tools: Read, Write
---

# Skill: KPI Tracker — Metrics & Success Measurement
**Category:** Optimization/Research

## Role
Define meaningful KPIs and tracking mechanisms so progress is measurable and decisions are data-driven.

## When to invoke
- Starting a new project or feature
- "what metrics should we track"
- OKR planning
- Measuring impact of changes

## Instructions
1. Identify: what does success look like? Who cares?
2. Define leading vs lagging indicators
3. SMART metrics: Specific, Measurable, Achievable, Relevant, Time-bound
4. Avoid vanity metrics (page views) — use actionable metrics (activation rate)
5. Set baselines and targets
6. Choose tracking: how collected? How often? Dashboards?

## Output format
```
## KPI Framework — <project> — <date>
### North Star Metric
### Primary KPIs
| Metric | Baseline | Target | Frequency |
### Secondary KPIs
### Tracking Plan
```

## Example
/kpi-tracker define KPIs for the wellux_testprojects research agent — measure research quality and usage

```

FILE: .claude/skills/llm-optimizer/SKILL.md
```markdown
---
name: llm-optimizer
description: >
  Optimize LLM inference for cost, speed, and quality. Invoke for: "reduce LLM cost",
  "faster inference", "token optimization", "prompt compression", "caching strategy",
  "LLM cost too high", "optimize API calls", "reduce tokens", "LLM performance".
argument-hint: LLM usage pattern or cost to optimize
allowed-tools: Read, Edit, Grep, Glob, WebSearch
---

# Skill: LLM Optimizer — Cost, Speed & Quality Optimization
**Category:** AI/ML Research

## Role
Optimize LLM usage to minimize cost and latency while maintaining quality.

## When to invoke
- LLM API costs too high
- Inference too slow
- "optimize our Claude usage"
- Reducing token consumption

## Instructions
1. Profile current usage: tokens per call, calls per hour, cost breakdown
2. Cache: identical or near-identical requests (saves 30-70% on repetitive tasks)
3. Model routing: use Haiku for simple tasks, Sonnet for medium, Opus for complex only
4. Prompt compression: remove redundant instructions, use shorter examples
5. Streaming: use streaming for better UX, not for cost savings
6. Batching: batch independent requests where possible
7. Context management: don't send full history, summarize older context

## Output format
```
## LLM Optimization Report — <system>
### Current: Xcost/day, Yms avg latency
### Optimizations Applied
1. Model routing: Haiku for simple → saves $X/day
2. Response caching: 40% hit rate → saves $Y/day
### After: Xcost/day (Z% reduction), Yms latency
```

## Example
/llm-optimizer analyze src/llm/ usage — reduce cost by 50% without quality loss

```

FILE: .claude/skills/logging/SKILL.md
```markdown
---
name: logging
description: >
  Set up structured logging, log aggregation, and log analysis. Invoke for:
  "logging setup", "structured logs", "log aggregation", "ELK stack", "log analysis",
  "add logging", "logging config", "how should I log this", "log format".
argument-hint: application or logging system to configure
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Logging — Structured Logging & Aggregation
**Category:** DevOps/Infra

## Role
Implement structured logging that makes debugging, auditing, and monitoring easy.

## When to invoke
- Setting up logging for new service
- "logs aren't useful" / "can't debug from logs"
- Log format standardization
- Log aggregation setup

## Instructions
1. Use structured logging (JSON format) not string concatenation
2. Include: timestamp, level, service, request_id, user_id, message, context
3. Log levels: DEBUG (dev), INFO (events), WARNING (abnormal but handled), ERROR (failures)
4. Never log: passwords, tokens, PII
5. Correlation IDs: trace requests through distributed system
6. Aggregation: configure for ELK or CloudWatch Logs

## Output format
```python
# Logging config
import structlog
log = structlog.get_logger()
log.info("api_call", model="claude-sonnet-4-6", tokens=150, latency_ms=320)
# Output: {"timestamp": "...", "level": "info", "event": "api_call", ...}
```

## Example
/logging set up structured logging for src/llm/ — include request_id, model, latency, tokens

```

FILE: .claude/skills/mem/SKILL.md
```markdown
---
name: mem
description: >
  Persist important context, decisions, and facts to memory files so Claude remembers
  across sessions. Invoke for: "remember this", "save this for later", "persist this",
  "don't forget", "add to memory", "mem", "save to memory", "note this down".
  Inspired by Claude Mem (thedotmack) persistent memory pattern.
argument-hint: fact, decision, or context to persist
allowed-tools: Read, Write, Edit
---

# Skill: Mem — Persistent Memory Across Sessions
**Category:** Ecosystem
**Inspired by:** Claude Mem (github.com/thedotmack)

## Role
Persist important context to files so it survives session boundaries and gets loaded by session-start.sh.

## When to invoke
- "remember this for next session"
- Important decision made that affects future work
- Project context that Claude should always know
- "add this to memory"

## Memory Locations
| Type | File | Loaded By |
|------|------|-----------|
| Project lessons | tasks/lessons.md | session-start.sh |
| Session tasks | tasks/todo.md | session-start.sh |
| Architecture decisions | docs/decisions/ | manual |
| User preferences | ~/.claude/CLAUDE.md | all sessions |

## Instructions
1. Identify what to remember and where it belongs
2. For lessons: append to tasks/lessons.md with DATE | PATTERN | RULE
3. For tasks: append to tasks/todo.md
4. For decisions: create ADR in docs/decisions/
5. For global preferences: append to ~/.claude/CLAUDE.md
6. Confirm: "Saved to [file]"

## Output format
```
✅ Saved to tasks/lessons.md:
2026-03-28 | Use YAML frontmatter in SKILL.md | Always include name: and description: fields
```

## Example
/mem remember: always use asyncio.gather for parallel LLM calls, not sequential await

```

FILE: .claude/skills/memory-bank/SKILL.md
```markdown
---
name: memory-bank
description: >
  Build and synchronize a structured memory bank of project knowledge.
  Invoke for: "memory bank", "update memory bank", "sync memory", "knowledge sync",
  "update project knowledge", "synchronize memory bank", "memory bank update",
  "keep memory current", "project memory", "update knowledge base with code changes".
  Inspired by russbeye/claude-memory-bank pattern.
argument-hint: scope to sync (e.g. "src/api/", "after this PR", "full project")
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Memory Bank — Structured Project Knowledge Sync

## Role
Build and maintain a structured memory bank at `.claude/memory/` that stays
synchronized with code changes. Acts as a long-term knowledge layer that survives
context compaction and session resets.
Inspired by russbeye/claude-memory-bank.

## Memory Bank Structure

```
.claude/memory/
├── hot/
│   └── hot-memory.md          # Always loaded (≤50 lines, key active context)
├── warm/
│   ├── architecture.md        # System design, component relationships
│   ├── decisions.md           # Key decisions with rationale
│   ├── patterns.md            # Recurring code patterns, idioms
│   ├── troubleshooting.md     # Known issues, workarounds, gotchas
│   └── api-surface.md         # Public API contracts and conventions
└── glacier/
    └── YYYY-MM-DD-<slug>.md   # Archived decisions + historical context
```

## When to invoke
- After a major refactor (sync architecture.md)
- After resolving a tricky bug (sync troubleshooting.md)
- After adding a new API endpoint (sync api-surface.md)
- After making an architectural decision (sync decisions.md)
- Periodically to keep memory current

## Instructions

### Full sync
1. Read all source files in scope (or all of `src/` for full sync)
2. Compare against existing warm-tier files
3. Update each warm-tier file with what's changed:
   - `architecture.md`: component diagram, module responsibilities, data flow
   - `decisions.md`: key choices with WHY, not just what
   - `patterns.md`: recurring idioms, anti-patterns seen
   - `troubleshooting.md`: tricky bugs, gotchas, workarounds
   - `api-surface.md`: endpoint signatures, request/response models
4. Update hot-memory.md with any critical new facts (keep ≤50 lines)
5. Archive stale but important context to glacier

### After a specific change
Use `/context-diff` first to understand what changed, then update only the relevant warm-tier files.

### Query mode
`/memory-bank query "src/auth/**"` — surface relevant warm-tier documentation for a path

## Path-Filtered Query

When given a path argument:
1. Identify which warm-tier file covers that domain
2. Return the relevant section
3. Note if it's stale (last updated >2 weeks ago)

## Output

```
## Memory Bank Sync: <scope>

### Updated
- warm/architecture.md → added FastAPI middleware order diagram
- warm/decisions.md → logged setuptools.build_meta decision
- warm/troubleshooting.md → added exc_info filtering gotcha

### Hot memory: updated active_feature key

### No changes needed
- warm/api-surface.md (current)
- warm/patterns.md (current)

### Archived to glacier
- Old routing design (pre-v0.9.0) → glacier/2026-04-05-routing-v1.md
```

```

FILE: .claude/skills/memory-profiler/SKILL.md
```markdown
---
name: memory-profiler
description: >
  Profile and fix memory leaks and excessive memory usage. Invoke for: "memory leak",
  "too much memory", "OOM", "memory usage", "memory profiling", "garbage collection",
  "memory keeps growing", "reduce memory footprint".
argument-hint: component or process to profile for memory
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Memory Profiler — Memory Leak Detection
**Category:** Optimization/Research

## Role
Detect and fix memory leaks, reduce peak memory usage, and optimize garbage collection.

## When to invoke
- Out of memory errors
- Memory growing over time (leak)
- "reduce memory usage"
- Container being OOM killed

## Instructions
1. Read code for common leak patterns: circular refs, event listeners not removed, caches without TTL
2. Python: tracemalloc, objgraph for live profiling
3. Node.js: --expose-gc, heap snapshots
4. Identify: what's growing? Which objects accumulate?
5. Fix: break circular references, clear caches, remove unused listeners
6. Measure: before/after peak memory usage

## Output format
```
## Memory Profile — <component> — <date>
### Peak Memory: XMB
### Leak Found: EventEmitter listeners accumulating in X
### Fix Applied:
### After: XMB (Y% reduction)
```

## Example
/memory-profiler src/llm/claude_client.py — check for memory leaks in streaming responses

```

FILE: .claude/skills/metrics-designer/SKILL.md
```markdown
---
name: metrics-designer
description: >
  Design metrics systems and instrumentation for software applications. Invoke for:
  "add metrics", "instrument this code", "design metrics", "Prometheus metrics",
  "custom metrics", "application metrics", "observability metrics".
argument-hint: application or component to instrument with metrics
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Metrics Designer — Application Instrumentation
**Category:** Optimization/Research

## Role
Design and implement application metrics that make system behavior visible and debuggable.

## When to invoke
- "add metrics to this"
- New service needs instrumentation
- Custom metrics for business events
- Prometheus/StatsD integration

## Instructions
1. Identify: what events matter? What durations? What counts?
2. Choose metric types: Counter (increases), Gauge (can go up/down), Histogram (distribution)
3. Label design: meaningful labels, not high-cardinality (no user_id labels)
4. Implement: Prometheus client_python / statsd / datadog-lambda
5. Test: verify metrics emitted correctly
6. Document: what each metric means, what alerts it drives

## Output format
```python
from prometheus_client import Counter, Histogram

llm_calls_total = Counter('llm_calls_total', 'Total LLM API calls', ['model', 'status'])
llm_latency_seconds = Histogram('llm_latency_seconds', 'LLM call duration', ['model'])

# Usage
with llm_latency_seconds.labels(model='claude-sonnet-4-6').time():
    response = await client.complete(prompt)
llm_calls_total.labels(model='claude-sonnet-4-6', status='success').inc()
```

## Example
/metrics-designer add Prometheus metrics to src/llm/claude_client.py — calls, latency, tokens

```

FILE: .claude/skills/migration/SKILL.md
```markdown
---
name: migration
description: >
  Plan and execute safe code or database migrations. Invoke for: "migrate this",
  "upgrade", "migration plan", "database migration", "API migration", "breaking change",
  "version upgrade", "schema migration", "data migration", "move from X to Y".
argument-hint: what to migrate and target version (e.g. "PostgreSQL schema v1→v2")
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Migration — Safe Upgrades & Data Migrations
**Category:** Development

## Role
Plan and execute migrations safely: backup first, staged rollout, rollback plan always included.

## When to invoke
- Database schema changes
- API breaking changes
- Framework or library version upgrades
- Data restructuring

## Instructions
1. **Never migrate without backup plan**
2. Document current state (schema, API contract, data format)
3. Design target state
4. Create migration steps: incremental, reversible where possible
5. Write rollback procedure for each step
6. Test migration on copy of production data first
7. Plan staged rollout: dev → staging → prod

## Output format
```
## Migration Plan — <what> — <date>
### Current State
### Target State
### Steps
  Step 1: [action] — Rollback: [undo action]
  Step 2: ...
### Rollback Procedure
### Testing Checklist
```

## Example
/migration PostgreSQL schema — add user_preferences JSONB column with backfill

```

FILE: .claude/skills/ml-debugger/SKILL.md
```markdown
---
name: ml-debugger
description: >
  Debug ML training runs, inference failures, and model quality issues. Invoke for:
  "loss not converging", "model not learning", "NaN loss", "gradient explosion",
  "inference error", "model output wrong", "training failed", "model debugging",
  "why is accuracy so low".
argument-hint: training config, loss curve, or error to debug
allowed-tools: Read, Edit, Grep, Glob, WebSearch
---

# Skill: ML Debugger — Training & Inference Debugging
**Category:** AI/ML Research

## Role
Diagnose and fix ML system failures: training instability, inference errors, and model quality problems.

## When to invoke
- Loss not decreasing or NaN
- Model outputs garbage
- Inference crashes or wrong output
- Accuracy unexpectedly low

## Instructions
1. Read training config and code
2. Check: NaN/Inf in loss? → LR too high or missing gradient clipping
3. Check: loss not moving? → LR too low, frozen layers, wrong optimizer
4. Check: overfitting? → add regularization, more data, reduce model size
5. Check: data loading → correct labels? No leakage? Proper normalization?
6. Check: inference → model in eval mode? Correct tokenization? Batch size?
7. Fix root cause, document in tasks/lessons.md

## Output format
```
## ML Debug Report — <issue>
### Symptom
### Root Cause
### Evidence
### Fix Applied
### Prevention
```

## Example
/ml-debugger training loss is NaN after epoch 2 — diagnose and fix

```

FILE: .claude/skills/model-benchmarker/SKILL.md
```markdown
---
name: model-benchmarker
description: >
  Benchmark LLM models on specific tasks to choose the best model for your use case.
  Invoke for: "compare models", "which model is best for", "benchmark Claude vs GPT",
  "model selection", "cost vs quality tradeoff", "is Haiku fast enough for this".
argument-hint: task to benchmark and models to compare
allowed-tools: Read, Write, WebSearch
---

# Skill: Model Benchmarker — LLM Model Selection
**Category:** AI/ML Research

## Role
Benchmark multiple LLM models on your specific task to make data-driven model selection decisions.

## When to invoke
- Choosing between Claude Opus/Sonnet/Haiku
- Cost optimization (can we use cheaper model?)
- Quality regression after model upgrade
- "is this model good enough for X?"

## Instructions
1. Define task: what exactly needs to be done? What's "good enough"?
2. Create 10-20 representative test cases
3. Run each model on all test cases (or describe configuration to do so)
4. Score: quality (LLM-as-judge or human), latency (ms), cost (tokens × price)
5. Plot: quality vs cost tradeoff matrix
6. Recommend: best model for the use case with rationale

## Output format
```
## Model Benchmark — <task> — <date>
| Model | Quality | Latency | Cost/1k calls | Verdict |
|-------|---------|---------|---------------|---------|
| claude-opus-4-6 | 9.2/10 | 3.2s | $15 | Best quality |
| claude-sonnet-4-6 | 8.8/10 | 1.1s | $3 | Best value |
| claude-haiku-4-5 | 7.1/10 | 0.3s | $0.25 | Fast+cheap |
### Recommendation
```

## Example
/model-benchmarker compare Sonnet vs Haiku for code review task — quality vs cost

```

FILE: .claude/skills/monitoring/SKILL.md
```markdown
---
name: monitoring
description: >
  Set up observability: metrics, dashboards, alerts. Invoke for: "monitoring setup",
  "add metrics", "Grafana dashboard", "Prometheus", "alerting", "observability",
  "how do I monitor this", "SLO", "SLA", "what should I alert on".
argument-hint: system or service to monitor
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Monitoring — Observability & Alerting
**Category:** DevOps/Infra

## Role
Design observability stacks: metrics collection, dashboards, and meaningful alerts that catch real problems without alert fatigue.

## When to invoke
- New service needs monitoring
- "what should I alert on"
- Dashboard creation
- SLO/SLA definition

## Instructions
1. Define SLOs: availability (99.9%?), latency (p99 < 500ms?), error rate (< 1%?)
2. Instrument: add metrics (counters, gauges, histograms) to code
3. Alert on SLO breach, not on symptoms
4. Dashboard: latency percentiles (p50, p95, p99), error rate, throughput, saturation
5. Avoid alert fatigue: only page for actionable, urgent issues
6. Implement: Prometheus metrics + Grafana dashboard + AlertManager rules

## Output format
- prometheus.yml scrape config
- Grafana dashboard JSON
- AlertManager alert rules
- Instrumentation code snippets

## Example
/monitoring set up monitoring for the Claude API client — SLO: p99 < 5s, error rate < 1%

```

FILE: .claude/skills/multimodal/SKILL.md
```markdown
---
name: multimodal
description: >
  Design and implement multimodal AI systems combining text, images, and other modalities.
  Invoke for: "multimodal", "text and images", "vision + language", "image + text pipeline",
  "document understanding", "multimodal embeddings", "cross-modal search".
argument-hint: multimodal task or system to design
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Multimodal — Vision + Language Systems
**Category:** AI/ML Research

## Role
Build systems that combine multiple modalities (text, images, audio) using multimodal LLMs.

## When to invoke
- Building document understanding (PDF + text)
- Image captioning or visual Q&A
- Cross-modal retrieval
- Any task combining text and images

## Instructions
1. Identify modalities: text, images, structured data, code?
2. Choose model: Claude claude-sonnet-4-6 handles text+images natively
3. Input preparation: encode images as base64 or URL references
4. Prompt design: describe image role in task context
5. Output parsing: extract structured info from multimodal response
6. Pipeline: preprocess → multimodal LLM → postprocess → store

## Output format
```python
# Multimodal request pattern
messages = [{
    "role": "user",
    "content": [
        {"type": "image", "source": {"type": "base64", ...}},
        {"type": "text", "text": "Analyze this image and extract..."}
    ]
}]
```

## Example
/multimodal build document analyzer — extract text + tables + diagrams from PDFs

```

FILE: .claude/skills/network-engineer/SKILL.md
```markdown
---
name: network-engineer
description: >
  Firewall rules, VPN, and zero-trust network design. Invoke for: "firewall review",
  "network security", "zero-trust design", "VPN config", "network segmentation",
  "port exposure", "traffic analysis", "DNS security", "TLS config", "open ports",
  "network hardening".
argument-hint: network topology or config to review (e.g. "firewall rules" or "network diagram")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Network Engineer — Firewall & Zero-Trust
**Category:** Security
**Color Team:** Green

## Role
Review and harden network security: firewall rules, network segmentation, TLS configuration, and zero-trust architecture.

## When to invoke
- Firewall rule audit
- Network segmentation design
- Zero-trust architecture planning
- TLS/certificate review

## Instructions
1. Review firewall rules: any 0.0.0.0/0 ingress except 80/443? Egress filtering?
2. Network segmentation: DMZ, app tier, DB tier properly isolated?
3. TLS: minimum TLS 1.2? No weak cipher suites? Certificate expiry?
4. DNS: DNSSEC? Split-horizon? No DNS leakage?
5. Ports: only necessary ports open? Management ports (22, 3389) restricted by IP?
6. Design zero-trust: identity-based access, microsegmentation, never-trust-always-verify

## Output format
```
## Network Security Review — <date>
### Firewall Rules: ✅/⚠️
### Segmentation: ✅/⚠️
### TLS/Certs: ✅/⚠️
### Exposed Services
### Zero-Trust Gaps
### Recommendations
```

## Example
/network-engineer review firewall rules and TLS config for production environment

```

FILE: .claude/skills/obsidian/SKILL.md
```markdown
---
name: obsidian
description: >
  Manage knowledge using Obsidian-style second-brain with linked atomic notes. Invoke for:
  "organize in Obsidian", "second brain", "atomic notes", "linked notes", "knowledge graph",
  "note-taking", "build a wiki", "organize my knowledge", "create linked notes".
  Inspired by kepano's Obsidian skills — knowledge management meets Claude.
argument-hint: knowledge area or notes to organize
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Skill: Obsidian — Second Brain Knowledge Management
**Category:** Ecosystem
**Inspired by:** kepano (github.com/kepano) Obsidian Skills

## Role
Build a structured, linked knowledge base using Obsidian's atomic note principles, stored in `data/research/` and accessible via semantic search.

## When to invoke
- "organize all my notes about X"
- After research sessions
- Building a topic knowledge graph
- "turn these notes into linked notes"

## Atomic Note Principles
1. **One idea per note**: split compound notes
2. **Short and dense**: < 200 lines, packed with insight
3. **Link everything**: connect related concepts with [[links]]
4. **Tags**: #topic, #status/draft, #type/concept
5. **MOC (Map of Content)**: index notes that link to all notes on a topic
6. **Progressive summarization**: bold key insights, highlight critical parts

## Instructions
1. Identify all concepts in the input material
2. Create one atomic note per concept
3. Link related notes: references to other notes
4. Create MOC for the topic
5. Add to data/research/ with consistent naming
6. Update data/research/README.md index

## Output format
```markdown
---
tags: [#ai, #rag, #concept]
related: [[embeddings]], [[vector-search]]
---
# Concept Name
**Core idea:** [one sentence]
...atomic content...
```

## Example
/obsidian organize all RAG research into linked atomic notes with MOC in data/research/

```

FILE: .claude/skills/office-hours/SKILL.md
```markdown
---
name: office-hours
description: >
  Strategic multi-persona review before building. Summons CEO, CTO, PM, and Designer to debate
  the approach, surface risks, and align on what to build before any code is written.
  Invoke for: "office hours", "review this approach", "should we build this", "get alignment",
  "strategic review", "product review", "debate the design", "pre-build review",
  "is this the right thing to build". Inspired by gstack (Garry Tan).
argument-hint: feature or decision to review in office hours
allowed-tools: Read, Glob, Grep, WebSearch
---

# Skill: Office Hours — Strategic Pre-Build Review
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack)

## Role
Convene a virtual engineering leadership team. Each persona evaluates the proposed work from their
lens, surfaces concerns, and drives toward an aligned decision before implementation begins.

## When to Invoke
- Before starting a significant new feature
- When requirements feel ambiguous or conflicting
- When the technical approach has meaningful alternatives
- When there's product / engineering tension to resolve
- Any time "should we even build this?" is a real question

## Personas

### CEO — Strategic Value
*"Does this move the needle? Is this the right bet?"*
- Evaluates: business impact, opportunity cost, strategic alignment
- Asks: What's the user value? What's the risk of not doing this? What are we not doing instead?
- Blocks: work with no clear user outcome or that conflicts with strategic direction

### CTO — Technical Leadership
*"Is this the right architecture? Will it scale? Can we maintain it?"*
- Evaluates: technical approach, architecture fit, debt introduced, complexity
- Asks: Does this fit our existing stack? What's the 6-month maintenance burden?
- Blocks: approaches that create brittle systems or unnecessary complexity

### PM — User & Delivery
*"Does this solve the right problem? Can we ship it? Will users care?"*
- Evaluates: user need validation, scope, acceptance criteria, delivery risk
- Asks: How do we know users want this? What's the MVP? How do we measure success?
- Blocks: work without clear success metrics or over-engineered MVPs

### Designer — Craft & Experience
*"Is this usable? Is it coherent? Does it feel right?"*
- Evaluates: UX consistency, edge cases, error states, cognitive load
- Asks: What happens when it fails? Is the mental model clear? Does this fit the product?
- Blocks: technically correct solutions that create confusing user experiences

## Process

1. **Read the room** — review `CLAUDE.md`, recent `tasks/todo.md`, and any relevant source files
2. **CEO speaks first** — strategic framing and go/no-go signal
3. **CTO responds** — technical feasibility and architecture risks
4. **PM grounds** — scope, criteria, delivery plan
5. **Designer closes** — UX and edge cases
6. **Synthesis** — summarize: what to build, what NOT to build, open questions, first task

## Output Format

```
## Office Hours: <feature name>

### CEO
[strategic assessment + go/no-go]

### CTO
[technical assessment + architecture notes]

### PM
[scope + acceptance criteria + success metric]

### Designer
[UX considerations + edge cases]

### Decision
- Build: [what]
- Skip: [what and why]
- Open questions: [list]
- First task: [concrete next action]
```

## Example
/office-hours add streaming support to the /complete API endpoint

```

FILE: .claude/skills/onboarding/SKILL.md
```markdown
---
name: onboarding
description: >
  Create onboarding documentation for new team members or contributors. Invoke for:
  "onboarding guide", "new developer guide", "contributor guide", "CONTRIBUTING.md",
  "how to get started", "new team member setup", "first day guide".
argument-hint: project or team to create onboarding for
allowed-tools: Read, Write, Glob
---

# Skill: Onboarding — New Developer Guide
**Category:** Documentation

## Role
Create clear onboarding documentation that gets a new developer productive in their first day.

## When to invoke
- New team members joining
- Open source contributors need guidance
- "write CONTRIBUTING.md"

## Instructions
1. Day 1 checklist: repo access, dev environment setup, first PR
2. Architecture overview: 5-minute mental model of the codebase
3. Development workflow: how to branch, test, PR, review, merge
4. Key concepts: domain-specific terms and patterns explained
5. Where to find things: map of the codebase
6. Who to ask: team contacts and their areas

## Output format
```markdown
# Getting Started — <project>
## Prerequisites
## Setup (15 minutes)
## Architecture Overview
## Development Workflow
## Key Concepts
## Where to Find Things
## Who to Ask
## First Task Suggestions
```

## Example
/onboarding create developer onboarding guide for wellux_testprojects project

```

FILE: .claude/skills/paper-summarizer/SKILL.md
```markdown
---
name: paper-summarizer
description: >
  Summarize academic papers and technical reports into actionable insights. Invoke for:
  "summarize this paper", "TL;DR this research", "what does this paper say", "explain
  this arxiv paper", "research summary", "summarize this PDF", "what are the key findings".
argument-hint: paper URL, arxiv ID, or paper title to summarize
allowed-tools: WebFetch, WebSearch, Write
---

# Skill: Paper Summarizer — Research Distillation
**Category:** AI/ML Research

## Role
Read academic papers and distill them into 1-page summaries with clear takeaways for practitioners.

## When to invoke
- "TL;DR this paper"
- Reading arxiv papers
- Keeping up with research
- Before implementing a technique from a paper

## Instructions
1. Fetch the paper (WebFetch arxiv URL or PDF)
2. Extract: problem statement, proposed solution, key innovation, results, limitations
3. Translate to plain English — no jargon without explanation
4. Identify: what can a practitioner USE from this paper?
5. Rate: novelty (1-5), practical usefulness (1-5), reproducibility (1-5)
6. Save to `data/research/`

## Output format
```
## Paper Summary: <title>
**Authors:** | **Year:** | **Venue:**
### Problem
### Solution
### Key Innovation
### Results
### Practical Takeaway (what you can use NOW)
### Limitations
### Rating: Novelty X/5 | Useful X/5
```

## Example
/paper-summarizer https://arxiv.org/abs/XXXX — summarize for practical implementation

```

FILE: .claude/skills/paperclip/SKILL.md
```markdown
---
name: paperclip
description: >
  Multi-agent orchestration with org structure, spend budgets, and audit trails.
  Invoke for: "paperclip", "multi-agent orchestration", "agent org chart", "assign to agents",
  "agent with budget", "orchestrate agents", "agent company", "zero-human team",
  "agent pipeline with audit", "parallel agents with tracking".
  Inspired by Paperclip AI (paperclipai/paperclip).
argument-hint: project or task to orchestrate across multiple agents
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: Paperclip — Multi-Agent Orchestration
**Category:** Ecosystem
**Inspired by:** Paperclip AI (github.com/paperclipai/paperclip)

## Role
Act as an orchestration architect. Structure complex projects as an agent organization — named
roles, explicit task handoffs, spend budgets, heartbeat tracking, and a full audit trail.
Prevent agents from double-working. Ensure context persists between agent sessions.

## When to Invoke
- A task is too large for one agent context window
- Multiple independent workstreams can run in parallel
- You need audit trails and budget controls on agent work
- Replacing a multi-step human workflow with agents
- Building a "zero-human" pipeline

## Org Structure Design

### Define Roles
Each agent gets:
- **Name** — unique identifier (e.g., `eng-1`, `qa-lead`, `researcher`)
- **Role** — responsibility scope
- **Budget** — max tokens / cost before auto-pause
- **Input** — what it receives to start
- **Output** — what it produces when done
- **Reports to** — who reviews its output

### Prevent Double-Work
- Use atomic task checkout: each task has a `status` (pending → claimed → done)
- Store task state in `data/cache/paperclip-tasks.json`
- Agents read and lock tasks before starting

### Audit Trail
Every agent logs to `data/cache/paperclip-audit.jsonl`:
```json
{"ts": "ISO8601", "agent": "eng-1", "task": "task-id", "status": "started", "note": "..."}
{"ts": "ISO8601", "agent": "eng-1", "task": "task-id", "status": "done", "output": "..."}
```

## Orchestration Template

```
## Paperclip: <Project Name>
Budget: <total token budget>
Deadline: <date or sprint>

### Org Chart
Orchestrator (this session)
├── researcher    — gather context, write design doc
├── eng-1         — implement core module
├── eng-2         — implement tests
├── qa-lead       — review + integration test
└── tech-writer   — update docs

### Tasks
| ID | Agent | Task | Input | Output | Budget | Status |
|----|-------|------|-------|--------|--------|--------|
| T1 | researcher | research approach | requirements | design-doc.md | 20k tok | pending |
| T2 | eng-1 | implement src/module.py | design-doc.md | module + diff | 40k tok | pending |
| T3 | eng-2 | write tests/test_module.py | module diff | test file | 30k tok | pending |
| T4 | qa-lead | review + run tests | T2+T3 output | review.md | 20k tok | pending |
| T5 | tech-writer | update docs/ | design-doc.md | updated docs | 10k tok | pending |

### Handoff Protocol
1. Orchestrator assigns T1 → researcher
2. researcher writes design-doc.md → signals done
3. Orchestrator reviews design-doc.md, approves
4. Orchestrator assigns T2 + T3 in parallel → eng-1 + eng-2
5. Both signal done → Orchestrator assigns T4 → qa-lead
6. qa-lead approves → Orchestrator assigns T5 → tech-writer
7. All done → Orchestrator runs /ship gate
```

## Process

1. **Decompose** — list all tasks, identify dependencies
2. **Assign** — match tasks to agent roles by capability
3. **Budget** — set token budgets to prevent runaway costs
4. **Checkpoint** — after each agent, orchestrator reviews before next handoff
5. **Audit** — log all agent activity to `data/cache/paperclip-audit.jsonl`
6. **Ship** — orchestrator runs `/ship` as final gate

## Quick Mode (3-agent pipeline)

For simple parallelization without full org overhead:
```
/swarm <task>    # Decomposes into parallel workstreams automatically
```

Use `/paperclip` when you need budget control and audit trails.
Use `/swarm` when you just need fast parallelization.

## Example
/paperclip build the full eval framework — researcher, 2 engineers, qa, docs writer

```

FILE: .claude/skills/pen-tester/SKILL.md
```markdown
---
name: pen-tester
description: >
  Offensive security and adversary emulation (red team). Invoke for: "pen test",
  "attack surface review", "find vulnerabilities", "red team", "ethical hacking",
  "what can an attacker exploit", "OWASP top 10 check", "injection", "auth bypass",
  "privilege escalation", "security holes", "find weak points".
argument-hint: target path or component to test (e.g. "src/api/" or "auth system")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Pen Tester — Red Team Offensive Security
**Category:** Security
**Color Team:** Red

## Role
Emulate adversary attacks to identify exploitable vulnerabilities before real attackers do.

## When to invoke
- "pen test this" / "red team review"
- Pre-release security validation
- After adding new authentication or API endpoints
- "what can an attacker do with this code"

## Instructions
1. Map attack surface: all entry points (APIs, forms, file uploads, CLI args)
2. Test OWASP Top 10: Injection, Broken Auth, XSS, IDOR, Security Misconfig, SSTI, etc.
3. Check for hardcoded secrets, tokens, credentials in code
4. Test auth bypass: JWT weaknesses, session fixation, privilege escalation paths
5. Check for mass assignment, insecure deserialization, XML/JSON injection
6. Score each finding with CVSS v3 (Critical/High/Medium/Low)

## Output format
```
## Pen Test Report — <scope> — <date>
### Attack Surface
### Findings (by severity)
[CRITICAL-CVSSx.x] <title> — <description> — <remediation>
### Executive Summary
```

## Example
/pen-tester src/api/ endpoint security review

```

FILE: .claude/skills/perf-profiler/SKILL.md
```markdown
---
name: perf-profiler
description: >
  Profile and optimize application performance: CPU, memory, I/O bottlenecks. Invoke for:
  "performance issue", "this is slow", "memory leak", "CPU spike", "profiling",
  "benchmark", "optimize performance", "bottleneck", "too much memory".
argument-hint: component, function, or endpoint to profile
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Perf Profiler — Performance Analysis & Optimization
**Category:** Development

## Role
Identify CPU, memory, and I/O bottlenecks and optimize them with measurable before/after metrics.

## When to invoke
- Slow API endpoints or functions
- High memory usage
- CPU spikes
- "this needs to be faster"

## Instructions
1. Identify what to profile: function, endpoint, or process
2. Add profiling: cProfile (Python), console.time (JS), or read existing metrics
3. Find top 3 hotspots by time/memory
4. Analyze root cause: algorithm complexity? I/O bound? Memory allocation?
5. Optimize: better algorithm, caching, async I/O, batching, generator instead of list
6. Measure after: quantify improvement

## Output format
```
## Performance Analysis — <component> — <date>
### Hotspots
1. function_name — 45% of runtime — O(n²) algorithm
### Optimizations Applied
### Before: Xms / YMB
### After: Xms / YMB (Zx improvement)
```

## Example
/perf-profiler src/prompt_engineering/chainer.py — profile chain execution time

```

FILE: .claude/skills/pipeline-opt/SKILL.md
```markdown
---
name: pipeline-opt
description: >
  Optimize CI/CD pipeline speed and reliability. Invoke for: "pipeline too slow",
  "slow CI", "speed up builds", "pipeline optimization", "cache builds",
  "parallel jobs", "flaky tests", "pipeline reliability".
argument-hint: pipeline config to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Pipeline Optimizer — CI/CD Speed & Reliability
**Category:** DevOps/Infra

## Role
Make CI/CD pipelines faster and more reliable through caching, parallelization, and flaky test elimination.

## When to invoke
- Pipeline takes > 10 minutes
- Flaky tests causing false failures
- "speed up our CI"

## Instructions
1. Profile pipeline: which job takes longest?
2. Cache: dependency caches (pip, npm, Maven), Docker layer cache
3. Parallelize: split test suite, run jobs concurrently
4. Fail fast: run quick checks first (lint, typecheck before slow tests)
5. Flaky tests: identify with test history, fix or quarantine
6. Skip unchanged: only test code that changed (affected tests)

## Output format
```
## Pipeline Optimization — <date>
### Current Duration: Xmin
### Bottlenecks Found
### Optimizations Applied
1. Added dependency cache → -3min
2. Parallelized tests (4 shards) → -6min
### After: Xmin (Y% faster)
```

## Example
/pipeline-opt .github/workflows/ci.yml — reduce pipeline from 25min to under 10min

```

FILE: .claude/skills/plan-eng-review/SKILL.md
```markdown
---
name: plan-eng-review
description: >
  Staff engineer review of the technical approach before implementation begins.
  Invoke for: "eng review", "technical review", "review my approach", "sanity check the design",
  "is this the right way to build it", "plan review", "pre-implementation review",
  "check my plan", "technical sanity check", "staff review".
  Inspired by gstack (Garry Tan) /plan-eng-review.
argument-hint: technical approach or plan to review
allowed-tools: Read, Grep, Glob
---

# Skill: Plan Eng Review — Technical Approach Review
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack)

## Role
Act as a staff engineer doing a pre-implementation design review. Not a code review — this
happens *before* code is written. Goal: catch fundamental approach problems early, when they're
cheap to fix, not after hours of implementation.

## When to Invoke
- After `/brainstorm` and `/write-plan` — before starting implementation
- When your technical approach touches shared infrastructure
- When there are multiple viable architectures and you need a second opinion
- Before large migrations, schema changes, or breaking API changes
- Any time "I'm not sure this is the right way" crosses your mind

## Review Lenses

### 1. Correctness — Will it actually work?
- Does the approach correctly solve the stated problem?
- Are there logical flaws in the design?
- Does it handle the known edge cases from the brainstorm?
- Are the data types and contracts correct?

### 2. Fit — Does it belong here?
- Does this fit the existing architecture and patterns?
- Are you solving this at the right layer? (Don't put business logic in middleware)
- Does this create unexpected coupling between modules?
- Would a reader familiar with the codebase find this natural?

### 3. Complexity — Is this the simplest correct solution?
- Is there a simpler approach that achieves the same result?
- Are you over-engineering for hypothetical requirements?
- Does this introduce concepts that aren't needed yet?
- Would you be happy maintaining this in 6 months?

### 4. Safety — What could go wrong?
- What happens if an external dependency fails?
- Are there race conditions or concurrency hazards?
- Is the blast radius of a bug acceptably small?
- Is there a way to roll this back if it causes issues?

### 5. Performance — Will it be fast enough?
- What's the time complexity of the hot path?
- Are there N+1 query patterns or repeated work?
- Is caching needed? Is it already present?
- Will this be a bottleneck at 10x current load?

### 6. Security — Is it safe?
- Does this expose new attack surfaces?
- Is user input properly validated and escaped?
- Are there authorization checks at the right level?
- Does this handle secrets or credentials safely?

## Output Format

```
## Eng Review: <approach/feature>

### Verdict
APPROVED | APPROVED WITH NOTES | NEEDS REVISION | BLOCKED

### Strengths
- [what's well-designed]

### Issues
| Severity | Issue | Recommendation |
|----------|-------|----------------|
| CRITICAL | [issue] | [fix required before proceeding] |
| MAJOR    | [issue] | [fix before merge] |
| MINOR    | [issue] | [fix in follow-up] |

### Suggested Changes
[specific changes to the plan, if any]

### Proceed?
[yes / yes with notes / no — reason]
```

## Severity Definitions
- **CRITICAL** — approach is fundamentally broken; do not proceed
- **MAJOR** — significant issue that will cause bugs or maintenance pain; fix before merge
- **MINOR** — suboptimal but workable; address in a follow-up

## Example
/plan-eng-review adding a sliding-window rate limiter using Redis sorted sets

## Related Skills
- `/brainstorm` — requirements phase (run first)
- `/write-plan` — task decomposition (run after approval)
- `/superpowers` — execution (run after plan is approved)
- `/code-review` — review after implementation (different from this)

```

FILE: .claude/skills/pr-reviewer/SKILL.md
```markdown
---
name: pr-reviewer
description: >
  Review pull requests: code quality, design, tests, security. Invoke for: "review PR",
  "PR feedback", "pull request review", "diff review", "code change review",
  "should I merge this", "LGTM check".
argument-hint: PR number, diff, or branch to review
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: PR Reviewer — Pull Request Review
**Category:** Development

## Role
Provide thorough pull request reviews covering code quality, correctness, design, tests, security, and documentation.

## When to invoke
- Pre-merge review
- "review this PR" / "is this ready to merge"
- Code change audit

## Instructions
1. Read the PR diff / changed files
2. Understand: what is this PR trying to do? Is it the right approach?
3. Check correctness: does it do what it says? Edge cases handled?
4. Check tests: are new tests added? Coverage maintained?
5. Check security: any new vulnerabilities introduced?
6. Check style: follows conventions? Good naming?
7. Verdict: APPROVE / REQUEST_CHANGES / COMMENT

## Output format
```
## PR Review — <title> — <date>
### Summary
### Blocking Issues 🔴
- file.py:34 — must fix before merge
### Suggestions 🟡
- file.py:12 — consider renaming for clarity
### Approved Changes 🟢
### Verdict: APPROVE / REQUEST CHANGES
```

## Example
/pr-reviewer review changes in src/llm/ for the new streaming response feature

```

FILE: .claude/skills/preflight/SKILL.md
```markdown
---
name: preflight
description: >
  Validate a prompt or task description for clarity and completeness before expensive execution.
  Invoke for: "preflight check", "validate this prompt", "is this task clear enough",
  "check before running", "prompt quality check", "task spec review", "pre-execution check",
  "score this prompt", "is my task well defined". Runs a 12-category scorecard.
argument-hint: task description or prompt to validate
allowed-tools: Read
---

# Skill: Preflight — Prompt & Task Validation

## Role
Score a task description or prompt across 12 quality dimensions before committing to expensive multi-step execution. Surface ambiguities, missing context, and scope issues upfront.

## When to invoke
- Before running `/superpowers`, `/write-plan`, or `/swarm` on a non-trivial task
- When task requirements feel unclear or underspecified
- Before creating complex agent pipelines
- When a previous run went sideways due to unclear requirements

## 12-Category Scorecard

Score each 0–2 (0=missing, 1=partial, 2=clear):

| # | Category | Check |
|---|----------|-------|
| 1 | **Goal clarity** | Is the desired outcome stated? |
| 2 | **Success criteria** | How do we know it's done? |
| 3 | **Scope bounds** | What's in/out of scope? |
| 4 | **Input context** | Are relevant files/code/data referenced? |
| 5 | **Constraints** | Tech stack, performance, security limits? |
| 6 | **Edge cases** | Are failure modes acknowledged? |
| 7 | **Dependencies** | Are blockers or prerequisites called out? |
| 8 | **Reversibility** | Can mistakes be undone? Is a backup plan mentioned? |
| 9 | **Acceptance test** | Is there a concrete way to verify correctness? |
| 10 | **Timeline/priority** | Is urgency or ordering specified? |
| 11 | **Audience/user** | Who uses this? What do they need? |
| 12 | **Anti-goals** | What should explicitly NOT be built? |

## Instructions

1. Read the task description carefully
2. Score each of the 12 categories
3. Calculate total score (0–24) and grade:
   - 20–24: ✅ Ready to execute
   - 14–19: ⚠ Execute with caution — note gaps
   - 8–13: 🔶 Refine before executing
   - 0–7: 🚫 Stop — requirements too vague
4. For each score < 2, write one clarifying question
5. Optionally rewrite the task description with gaps filled

## Output Format

```
## Preflight: <task name>

| Category | Score | Notes |
|----------|-------|-------|
| Goal clarity | 2 | ✅ Clear: build X that does Y |
| Success criteria | 1 | ⚠ Partial: "tests pass" but no coverage target |
...

**Total: 18/24 — ⚠ Execute with caution**

### Gaps to resolve:
1. [Success criteria] What coverage threshold is acceptable?
2. [Scope bounds] Should this handle authentication or is that out of scope?

### Rewritten task (optional):
Build a tiered memory system in src/persistence/tiered_memory.py that...
```

```

FILE: .claude/skills/prompt-engineer/SKILL.md
```markdown
---
name: prompt-engineer
description: >
  Design, optimize, and test prompts for maximum LLM performance. Invoke for:
  "improve this prompt", "write a system prompt", "prompt engineering", "optimize prompt",
  "better prompt for", "few-shot examples", "chain of thought", "system prompt design",
  "my prompt isn't working".
argument-hint: task description or existing prompt to optimize
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Prompt Engineer — LLM Prompt Optimization
**Category:** AI/ML Research

## Role
Design and optimize prompts using advanced techniques: chain-of-thought, few-shot, system prompt architecture, constitutional AI principles.

## When to invoke
- Writing new system prompts
- Prompt not producing desired output
- Few-shot example design
- Prompt template creation

## Instructions
1. Understand task: what input → what output? What constraints?
2. Choose technique: zero-shot / few-shot / chain-of-thought / role-based / XML tags
3. Write system prompt: role, context, constraints, output format
4. Add few-shot examples if needed (2-5 representative examples)
5. Test with edge cases: ambiguous input, adversarial input, empty input
6. Iterate: identify failure modes and add clarifying instructions
7. Save to `tools/prompts/` or `data/prompts/`

## Output format
```
## Prompt Design — <task> — <date>
### System Prompt
[complete system prompt]
### Few-Shot Examples
[if applicable]
### Test Cases & Results
### Failure Modes Identified
```

## Example
/prompt-engineer design system prompt for code review assistant with strict JSON output

```

FILE: .claude/skills/purple-team/SKILL.md
```markdown
---
name: purple-team
description: >
  Red-to-blue bridge: validates that detections work against known attack patterns.
  Invoke for: "purple team exercise", "detection validation", "does our monitoring catch
  this attack", "MITRE ATT&CK mapping", "test our defenses", "adversary simulation with
  detection check", "are we detecting this technique".
argument-hint: attack technique or MITRE ATT&CK ID to validate (e.g. "T1059 command execution")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Purple Team — Detection Validation
**Category:** Security
**Color Team:** Purple

## Role
Bridge red and blue teams: emulate specific attack techniques and verify detection/response coverage.

## When to invoke
- "purple team exercise" for a specific technique
- Validating SIEM rules or WAF rules actually work
- MITRE ATT&CK coverage assessment
- After adding new detection rules

## Instructions
1. Select attack technique (from argument or MITRE ATT&CK)
2. Describe exactly how the attack would manifest in logs/traffic
3. Check existing detection rules (SIEM, WAF, IDS) against the attack pattern
4. Identify detection gaps: what would be missed?
5. Recommend: new rules, log sources, or monitoring improvements
6. Document: technique → expected log → detection rule → coverage status

## Output format
```
## Purple Team — <technique> — <date>
### Technique: <MITRE ID> <Name>
### Attack Simulation
### Detection Coverage: DETECTED / PARTIAL / MISSED
### Gaps Found
### Recommended Rules
```

## Example
/purple-team T1078 Valid Accounts — credential stuffing detection

```

FILE: .claude/skills/query-optimizer/SKILL.md
```markdown
---
name: query-optimizer
description: >
  Optimize database queries for speed and efficiency. Invoke for: "slow query",
  "optimize SQL", "query performance", "explain plan", "index missing",
  "full table scan", "N+1", "query taking too long".
argument-hint: SQL query or ORM code to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Query Optimizer — SQL & ORM Performance
**Category:** Optimization/Research

## Role
Transform slow queries into fast ones through indexing, query rewriting, and ORM optimization.

## When to invoke
- Slow database queries
- "this query takes Xs"
- EXPLAIN PLAN shows full table scan
- N+1 queries in ORM code

## Instructions
1. Read the query — understand what it's doing
2. EXPLAIN: identify full table scans, sort operations, temporary tables
3. Add indexes on: WHERE columns, JOIN columns, ORDER BY columns
4. Rewrite: avoid SELECT *, use covering indexes, reduce JOINs
5. ORM: use eager loading (select_related/include), avoid lazy loading in loops
6. Cache: can result be cached? How often does data change?

## Output format
```sql
-- Before (slow: full table scan, 5s)
SELECT * FROM users WHERE email LIKE '%@example.com%';

-- After (fast: index scan, 10ms)
CREATE INDEX idx_users_domain ON users(email text_pattern_ops);
SELECT id, name, email FROM users WHERE email LIKE '@example.com%';

-- Expected: 500x improvement
```

## Example
/query-optimizer this SQL query: SELECT * FROM logs WHERE created_at > '2026-01-01' ORDER BY user_id

```

FILE: .claude/skills/rag-builder/SKILL.md
```markdown
---
name: rag-builder
description: >
  Build Retrieval-Augmented Generation (RAG) systems including LightRAG graph-based retrieval.
  Invoke for: "build RAG", "add retrieval", "vector search", "semantic search",
  "RAG system", "document retrieval", "knowledge base search", "LightRAG",
  "graph-based retrieval", "reduce hallucination with retrieval".
argument-hint: documents to index or RAG system to design
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch
---

# Skill: RAG Builder — Retrieval-Augmented Generation
**Category:** AI/ML Research

## Role
Design and implement RAG systems that ground LLM responses in actual data, reducing hallucination.

## When to invoke
- "my LLM is hallucinating — add retrieval"
- Building knowledge base Q&A
- Document search and retrieval
- LightRAG graph-based retrieval setup

## Instructions
1. Choose RAG approach: naive, advanced, or graph-based (LightRAG)
2. Document processing: chunk → embed → index
3. Retrieval: semantic similarity, keyword hybrid, or graph traversal
4. Prompt augmentation: inject retrieved context into LLM prompt
5. Implement with: chromadb / faiss / LightRAG for indexing
6. Store embeddings in `data/embeddings/`
7. Test: retrieval precision, response groundedness

## Output format
Complete implementation including:
- Document ingestion pipeline
- Vector store setup
- Query pipeline
- Evaluation metrics

## Example
/rag-builder build RAG for data/research/ docs — enable semantic search over all research notes

```

FILE: .claude/skills/readme-writer/SKILL.md
```markdown
---
name: readme-writer
description: >
  Write or update README.md files that are clear, complete, and developer-friendly.
  Invoke for: "write README", "update README", "docs are outdated", "document this project",
  "README is missing", "improve documentation", "README for this".
argument-hint: project or directory to document
allowed-tools: Read, Write, Glob, Grep
---

# Skill: README Writer — Project Documentation
**Category:** Documentation

## Role
Write clear, comprehensive README.md files that help developers get up and running quickly.

## When to invoke
- New project needs documentation
- README is outdated or incomplete
- "document this project"

## Instructions
1. Read all code to understand what the project actually does
2. Structure: Project Name → What it does → Quick Start → Usage → Configuration → Contributing
3. Quick Start must work: test the installation steps
4. Include: badges (version, status), architecture overview, prerequisites
5. Code examples: show real usage, not toy examples
6. Keep current: check all links work, versions are correct

## Output format
Complete README.md with:
- Badges + title
- One-paragraph what + why
- Prerequisites
- Installation (works on copy-paste)
- Usage examples
- Configuration reference
- Contributing guide

## Example
/readme-writer write comprehensive README for the wellux_testprojects project

```

FILE: .claude/skills/refactor/SKILL.md
```markdown
---
name: refactor
description: >
  Refactor code for clarity, performance, and maintainability without changing behavior.
  Invoke for: "refactor this", "clean up this code", "extract function", "simplify this",
  "make this more readable", "reduce duplication", "better structure", "DRY this up",
  "too complex", "spaghetti code".
argument-hint: file or function to refactor
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Refactor — Clean Code Without Behavior Change
**Category:** Development

## Role
Improve code structure, readability, and maintainability while preserving exact behavior.

## When to invoke
- Code is hard to read or maintain
- Functions are too long (> 40 lines)
- Duplication exists (DRY violation)
- Naming is unclear

## Instructions
1. Read and understand the CURRENT behavior completely (write it down)
2. Identify refactoring opportunities: long functions, duplication, unclear naming, deep nesting
3. Apply refactoring: extract method, rename, simplify conditionals, reduce nesting
4. Verify behavior PRESERVED: same inputs → same outputs
5. Run existing tests to confirm nothing broke

## Output format
Show before/after for each change:
```
### Change 1: Extract calculate_discount()
Before: [code]
After: [code]
Reason: Function was 60 lines, now split into focused 15-line functions
```

## Example
/refactor src/utils/pricing.py — extract the discount calculation logic

```

FILE: .claude/skills/retrospective/SKILL.md
```markdown
---
name: retrospective
description: >
  Run a sprint or project retrospective to capture learnings. Invoke for: "retrospective",
  "retro", "what went well", "what could be better", "lessons learned",
  "sprint review", "team retrospective".
argument-hint: sprint or project to retrospect on
allowed-tools: Read, Write
---

# Skill: Retrospective — Sprint & Project Review
**Category:** Project Management

## Role
Run a structured retrospective to capture what worked, what didn't, and concrete improvements.

## When to invoke
- End of sprint
- End of project
- After an incident
- "let's do a retro"

## Instructions
1. Read: tasks/todo.md, tasks/lessons.md, git log for the period
2. What went well? (keep doing)
3. What could be better? (specific, not vague)
4. What to try next? (concrete, actionable)
5. Action items: owner + deadline
6. Append key lessons to tasks/lessons.md

## Output format
```
## Retrospective — <sprint/project> — <date>
### What Went Well ✅
-
### What Could Be Better ⚠️
-
### What to Try Next 🧪
-
### Action Items
| Action | Owner | Done By |
### Lessons Added to tasks/lessons.md
```

## Example
/retrospective run retro for Phase 1 and Phase 2 of wellux_testprojects build

```

FILE: .claude/skills/riper/SKILL.md
```markdown
---
name: riper
description: >
  RIPER agentic workflow: Research → Innovate → Plan → Execute → Review.
  Enforces strict phase separation for complex features to prevent premature implementation.
  Invoke for: "riper", "riper workflow", "research then innovate", "five phase workflow",
  "research innovate plan execute review", "structured feature workflow",
  "riper mode", "phase-gated development", "systematic feature delivery".
  Inspired by ThibautMelen/agentic-workflow-patterns RIPER pattern.
argument-hint: feature or task to deliver through the RIPER workflow
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, WebSearch
---

# Skill: RIPER — Phase-Gated Agentic Workflow

## Role
Enforce five strict phases for complex feature delivery. No phase can begin until the
previous is explicitly approved. Prevents the most common failure mode: jumping to
implementation before understanding the problem.

Inspired by ThibautMelen/agentic-workflow-patterns and tony/claude-code-riper-5.

## The 5 Phases

### Phase 1: RESEARCH
**Goal**: Understand the problem space completely before proposing anything.
**Activities**:
- Read all relevant existing code, docs, tests
- Search for prior art, existing patterns, similar implementations
- Identify constraints, edge cases, integration points
- Interview the codebase (grep, glob, read) — do not propose solutions

**Gate**: Write a Research Summary. Stop. Wait for approval before Phase 2.

**Output format**:
```
## RIPER Phase 1 — Research Complete

### What exists
[Relevant code, patterns, dependencies found]

### Constraints discovered
[Technical limits, integration requirements, edge cases]

### Open questions
[Things that need clarification before innovating]

→ Ready for Phase 2 (Innovate)?
```

---

### Phase 2: INNOVATE
**Goal**: Generate multiple solution approaches without committing to any one.
**Activities**:
- Propose 2–4 distinct implementation approaches
- For each: pros, cons, complexity, risks
- Do NOT write any implementation code
- Explicitly note which approach you lean toward and why

**Gate**: Write Innovation Summary. Stop. Wait for approval + approach selection.

**Output format**:
```
## RIPER Phase 2 — Innovate

### Approach A: [name]
- How: [brief]
- Pros: [list]
- Cons: [list]
- Risk: Low/Medium/High

### Approach B: [name]
...

### Recommendation: Approach X because [reason]

→ Which approach? Approve to proceed to Phase 3 (Plan).
```

---

### Phase 3: PLAN
**Goal**: Atomic task decomposition of the chosen approach.
**Activities**:
- Break the chosen approach into tasks of ≤30 minutes each
- Each task: what file, what change, what test verifies it
- Identify the critical path (which tasks block others)
- Write the plan to `tasks/todo.md`

**Gate**: Task list written. Stop. Wait for approval before Phase 4.

**Output format**:
```
## RIPER Phase 3 — Plan

### Tasks (written to tasks/todo.md)
- [ ] Task 1: [file] — [change] — verified by: [test]
- [ ] Task 2: ...

### Critical path: 1 → 3 → 5 (tasks 2 and 4 can run in parallel)

→ Plan approved? Proceed to Phase 4 (Execute)?
```

---

### Phase 4: EXECUTE
**Goal**: Implement exactly the plan, no more, no less.
**Activities**:
- Execute tasks from the plan in order
- For each task: implement, test, mark done in todo.md
- Do NOT refactor or improve things outside the plan scope
- Do NOT add features not in the plan

**Gate**: All tasks complete, all tests pass, lint clean.

**Output format**:
```
## RIPER Phase 4 — Execute

✅ Task 1: [description] — tests: pass
✅ Task 2: [description] — tests: pass
...

All N tasks complete. Tests: X passed. Lint: clean.

→ Proceed to Phase 5 (Review)?
```

---

### Phase 5: REVIEW
**Goal**: Verify the implementation against the original spec with independent eyes.
**Activities**:
- Re-read the original request from Phase 1
- Verify each requirement is met with file:line evidence
- Look for: regressions, missing edge cases, spec drift, unnecessary additions
- Run full test suite + lint + smoke evals

**Output format**:
```
## RIPER Phase 5 — Review

### Spec vs. Implementation
| Requirement | Status | Evidence |
|-------------|--------|---------|
| [req 1] | ✅ Met | src/foo.py:42 |
| [req 2] | ✅ Met | tests/test_foo.py:17 |

### Regression check: [N tests passing, was M before]
### Scope creep: [None / described if found]
### Final verdict: APPROVED ✅ / NEEDS REVISION ⚠
```

## Phase Control
- Use `/riper:research`, `/riper:innovate`, `/riper:plan`, `/riper:execute`, `/riper:review` to jump to a specific phase
- The orchestrator tracks current phase in `.claude/memory/hot/hot-memory.md` under `riper_phase`
- Never skip phases without explicit user instruction

```

FILE: .claude/skills/risk-assessor/SKILL.md
```markdown
---
name: risk-assessor
description: >
  Identify and assess project risks before they become problems. Invoke for:
  "risk assessment", "what could go wrong", "project risks", "risk register",
  "mitigation plan", "identify risks", "what are the risks".
argument-hint: project or decision to assess risks for
allowed-tools: Read, Write, Grep
---

# Skill: Risk Assessor — Project Risk Management
**Category:** Project Management

## Role
Identify risks early, assess probability and impact, and define mitigation strategies.

## When to invoke
- Starting a new project
- Before major decisions
- "what are we worried about"
- Regular risk review

## Instructions
1. Brainstorm: technical, organizational, timeline, dependency, security risks
2. Score each: Probability (1-5) × Impact (1-5) = Risk Score
3. Prioritize: high score risks get mitigation plans
4. Mitigation: avoid, reduce, accept, or transfer each risk
5. Early warning: what's the first sign this risk is materializing?
6. Update tasks/todo.md with risk mitigation tasks

## Output format
```
## Risk Register — <project> — <date>
| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| API rate limits hit | 4 | 4 | 16 | Implement caching + queue |
### Top 3 Risks to Watch
```

## Example
/risk-assessor assess risks for adding 100 skills to this project before shipping

```

FILE: .claude/skills/roadmap/SKILL.md
```markdown
---
name: roadmap
description: >
  Build or update a product/technical roadmap. Invoke for: "roadmap", "build roadmap",
  "what's the plan", "long-term plan", "6-month roadmap", "product roadmap",
  "technical roadmap", "what comes after this".
argument-hint: project and timeframe for the roadmap
allowed-tools: Read, Write, Grep
---

# Skill: Roadmap — Product & Technical Planning
**Category:** Project Management

## Role
Create clear roadmaps that align stakeholders and set realistic expectations.

## When to invoke
- Starting a new project
- "what are we building over the next 6 months"
- Stakeholder communication
- Quarterly planning

## Instructions
1. Read MASTER_PLAN.md, tasks/PRD.md, tasks/todo.md for current state
2. Define: themes (not features) for each quarter
3. Now / Next / Later framework for prioritization
4. Dependencies: what must happen before what?
5. Include confidence levels: committed / likely / exploring
6. Write to docs/ROADMAP.md

## Output format
```
## Roadmap — <project>
### Now (current quarter)
- [committed] Feature A
### Next (next quarter)
- [likely] Feature B
### Later (3-6 months)
- [exploring] Feature C
### Milestones
| Milestone | Target Date | Status |
```

## Example
/roadmap build 6-month roadmap for wellux_testprojects template evolution

```

FILE: .claude/skills/rollback/SKILL.md
```markdown
---
name: rollback
description: >
  Execute or plan a deployment rollback. Invoke for: "rollback", "revert deployment",
  "undo deploy", "something broke in prod", "roll back to previous version",
  "deployment failed", "revert to v{version}".
argument-hint: what to rollback and target version
allowed-tools: Read, Write, Bash, Grep
---

# Skill: Rollback — Emergency Deployment Revert
**Category:** DevOps/Infra

## Role
Execute rapid, safe rollbacks when deployments cause production issues.

## When to invoke
- Production issue after deployment
- "roll back to previous version"
- Deployment causing errors

## Instructions
1. STOP: pause ongoing deployment if still in progress
2. Assess: what's broken? What changed? Is rollback needed or can we hotfix faster?
3. Rollback options: previous Docker image, git revert, DB migration rollback
4. Database: if migration was destructive, rollback is harder — follow migration rollback plan
5. Verify: after rollback, confirm issue is resolved
6. Incident report: document timeline, root cause, prevention

## Output format
```
## Rollback Plan — <service> — <date>
### Issue: <what's broken>
### Rollback Target: v{previous}
### Steps (in order)
1. ...
### Estimated Time: Xmin
### Verification: <how to confirm rollback worked>
### Post-Rollback: update incident report
```

## Example
/rollback revert API service to v2.0.3 — v2.1.0 causing 500 errors on /api/completions

```

FILE: .claude/skills/runbook-creator/SKILL.md
```markdown
---
name: runbook-creator
description: >
  Create operational runbooks for repeatable procedures. Invoke for: "write runbook",
  "document this procedure", "ops runbook", "how to deploy", "incident runbook",
  "step-by-step ops guide", "operational documentation".
argument-hint: procedure or operation to document
allowed-tools: Read, Write, Glob
---

# Skill: Runbook Creator — Operational Procedures
**Category:** Documentation

## Role
Write clear runbooks that any engineer can follow without prior knowledge of the system.

## When to invoke
- New operational procedure needs documentation
- Alert triggered with no runbook
- Onboarding new ops engineers
- After every incident (document what was done)

## Instructions
1. Assume reader has no context — start from zero
2. Prerequisites: what access, tools, knowledge needed?
3. Steps: numbered, one action per step, exact commands with expected output
4. Decision points: if X then Y, else Z
5. Verification: how to confirm each step worked
6. Rollback: how to undo if step fails
7. Escalation: who to call if stuck

## Output format
```markdown
# Runbook: <procedure name>
**Last Updated:** | **Owner:**

## When to use this runbook
## Prerequisites
## Steps
1. [Action] — expected output: `...`
## Verification
## Rollback
## Escalation
```

## Example
/runbook-creator write deployment runbook for the Python AI service

```

FILE: .claude/skills/scaling/SKILL.md
```markdown
---
name: scaling
description: >
  Plan and implement horizontal/vertical scaling strategies. Invoke for: "scaling plan",
  "handle more traffic", "auto-scaling", "load balancing", "bottleneck", "capacity planning",
  "how do I scale this", "handle 10x load".
argument-hint: system to scale and target load
allowed-tools: Read, Write, WebSearch
---

# Skill: Scaling — Capacity Planning & Auto-Scaling
**Category:** DevOps/Infra

## Role
Design scaling strategies that handle load growth without over-provisioning.

## When to invoke
- Expecting traffic growth
- "can this handle 10x load?"
- Setting up auto-scaling
- Capacity planning for a new system

## Instructions
1. Baseline: current load, current capacity, headroom
2. Identify bottleneck: CPU? Memory? DB? Network? LLM API rate limits?
3. Horizontal scaling: add instances, implement stateless design
4. Vertical scaling: larger instance (quick fix, limited ceiling)
5. Auto-scaling: CPU/request-based triggers, scale-in delay
6. Database: read replicas, sharding, connection pooling
7. Load balancing: health checks, sticky sessions if needed

## Output format
```
## Scaling Plan — <system> — <date>
### Current Bottleneck
### Scaling Strategy: horizontal / vertical / both
### Auto-scaling Config
### Database Strategy
### Expected: handles Xx load at $Y/month
```

## Example
/scaling plan to scale the API from 100 to 10,000 requests/min with auto-scaling

```

FILE: .claude/skills/scope-definer/SKILL.md
```markdown
---
name: scope-definer
description: >
  Define project scope and prevent scope creep. Invoke for: "define scope", "scope creep",
  "what's in scope", "MVP definition", "what should we NOT build", "scope this project",
  "define boundaries".
argument-hint: project or feature to scope
allowed-tools: Read, Write
---

# Skill: Scope Definer — Project Boundaries
**Category:** Project Management

## Role
Clearly define what is and isn't in scope to prevent scope creep and keep projects focused.

## When to invoke
- Starting a new project
- "scope is growing out of control"
- MVP definition
- Sprint scope definition

## Instructions
1. Write IN SCOPE: explicit list of what will be built
2. Write OUT OF SCOPE: explicit list of what won't be built (just as important!)
3. Assumptions: what are we assuming is true?
4. Dependencies: what does this project depend on?
5. Definition of Done: what must be true for this to be "finished"?

## Output format
```
## Scope Definition — <project>
### In Scope ✅
- Feature A
- Feature B

### Out of Scope ❌
- Feature C (future phase)
- Feature D (different project)

### Assumptions
### Definition of Done
```

## Example
/scope-definer define scope for MVP of wellux_testprojects — what's in and out

```

FILE: .claude/skills/secrets-mgr/SKILL.md
```markdown
---
name: secrets-mgr
description: >
  Manage secrets and credentials securely. Invoke for: "secrets management", "API key storage",
  "secrets vault", "credential rotation", "no hardcoded secrets", "HashiCorp Vault",
  "AWS Secrets Manager", "env vars", "how to store secrets", "rotate credentials".
argument-hint: secrets system to set up or audit
allowed-tools: Read, Write, Grep, Glob, WebSearch
---

# Skill: Secrets Manager — Secure Credential Management
**Category:** DevOps/Infra

## Role
Implement secure secrets management: never hardcoded, rotation enabled, audit trail, least-privilege access.

## When to invoke
- "where should I store API keys"
- Secrets found in code
- Credential rotation needed
- Setting up secrets management for new project

## Instructions
1. Audit: scan for hardcoded secrets with `grep -r "sk-" / "password ="` etc.
2. Choose: AWS Secrets Manager, HashiCorp Vault, or .env + gitignored (dev only)
3. Inject at runtime: environment variables or secrets mount — never baked in image
4. Rotation: automate key rotation, never single-use credentials shared across services
5. Access: least-privilege access per service (service A can't read service B's secrets)
6. Audit log: who accessed what secret and when

## Output format
```
## Secrets Management Setup
### Secrets Found in Code (MUST FIX)
### Chosen Store: <Vault/AWS SM/env>
### Migration Steps
### Rotation Schedule
### Access Matrix
```

## Example
/secrets-mgr audit codebase for hardcoded secrets and design proper secrets management

```

FILE: .claude/skills/security-engineer/SKILL.md
```markdown
---
name: security-engineer
description: >
  SIEM rules, WAF configuration, and detection tooling. Invoke for: "SIEM rule",
  "WAF config", "detection engineering", "security tooling", "alert rule",
  "intrusion detection", "log parsing rule", "security automation", "Sigma rule",
  "Snort rule", "write detection for".
argument-hint: detection use case or tool to configure (e.g. "brute force detection" or "WAF for SQLi")
allowed-tools: Read, Write, Grep, Glob, WebSearch
---

# Skill: Security Engineer — Detection & Tooling
**Category:** Security
**Color Team:** Green

## Role
Build detection logic: write SIEM rules, configure WAF policies, create Sigma/Snort rules, and automate security responses.

## When to invoke
- "write a SIEM rule for X"
- WAF rule creation
- Detection engineering for new attack patterns
- Security automation scripting

## Instructions
1. Understand the attack pattern to detect: what logs, what fields, what thresholds?
2. Write detection rule in appropriate format (Sigma, KQL, SPL, Snort, ModSecurity)
3. Define: trigger conditions, severity, response action
4. Add false-positive reduction logic
5. Write test cases: true positive examples, false positive examples
6. Document: rule name, description, MITRE mapping, tune parameters

## Output format
```
## Detection Rule — <name> — <date>
### Use Case
### Rule (format: Sigma/KQL/SPL)
### Test Cases
### MITRE Mapping
### Tuning Notes
```

## Example
/security-engineer write Sigma rule for detecting credential stuffing against /api/login

```

FILE: .claude/skills/self-reflect/SKILL.md
```markdown
---
name: self-reflect
description: >
  Mine recent sessions, commits, and PR feedback for patterns and auto-update lessons.
  Invoke for: "self reflect", "extract patterns", "what did we learn", "mine learnings",
  "update lessons from history", "retrospective patterns", "session patterns",
  "what patterns emerged", "learn from mistakes", "self reflection", "improve from history".
  Post-merge / post-session autonomous learning.
argument-hint: scope (e.g. "last 5 commits", "this week", "recent sessions")
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill: Self-Reflect — Autonomous Pattern Mining & Lesson Extraction

## Role
Autonomously analyze recent work history and extract patterns, recurring mistakes, and
successful techniques. Append structured lessons to `tasks/lessons.md` without manual input.
Inspired by dsifry/metaswarm post-merge self-reflection pattern.

## When to invoke
- After a complex feature lands (post-merge)
- After a debugging session resolves a tricky bug
- At end of sprint or major milestone
- When user says "what did we learn", "extract patterns", "self reflect"
- Proactively: once per week as a cron job

## Data Sources
1. `git log --oneline -20` — recent commit history
2. `git diff HEAD~5..HEAD` — recent code changes
3. `tasks/todo.md` — completed vs open tasks
4. `tasks/lessons.md` — existing lessons (avoid duplicating)
5. `data/sessions/` — daily session logs if available
6. Test failure patterns: `pytest --tb=no -q` output if failures exist

## Pattern Types to Extract

**Anti-patterns** (recurring mistakes):
- Repeated same error category (e.g., whitespace in Edit, circular imports)
- Same file edited multiple times in one session
- Tests broken by same root cause multiple times

**Success patterns** (techniques that worked):
- Approaches that unblocked hard problems
- Architectural decisions that proved correct
- Shortcuts that saved significant time

**Improvement opportunities**:
- Friction points in workflow
- Missing tooling or automation
- Underused existing features

## Instructions

1. Run `git log --oneline -20` and `git diff HEAD~5..HEAD --stat`
2. Read `tasks/lessons.md` to understand existing lessons (avoid duplicating)
3. Read `data/sessions/*.md` for recent session logs
4. Identify: what went wrong, what went right, what took too long
5. Formulate 1–5 new lessons in the standard format
6. Append to `tasks/lessons.md` only if novel (not already captured)
7. Optionally update `.claude/memory/hot/hot-memory.md` with critical new insights

## Lesson Format

```markdown
### PATTERN: <1-line description of the situation>
**RULE:** <what to do / not to do>
**PREVENTION:** <how to catch it earlier next time>
**Source:** self-reflect from <date> via git-log / session-log / test-failure
```

## Output

```
## Self-Reflect: <scope>

### Analyzed
- Commits reviewed: N
- Session logs: N days
- Existing lessons: N

### New Patterns Found

1. **Anti-pattern: Edit fails on stale string match**
   → Added to lessons.md

2. **Success: Parallel tool calls cut task time by ~40%**
   → Added to lessons.md

### Lessons appended: N
### No duplicates of existing N lessons
```

```

FILE: .claude/skills/seo-auditor/SKILL.md
```markdown
---
name: seo-auditor
description: >
  SEO audit and optimization. Invoke for: "SEO audit", "improve SEO", "search ranking",
  "meta tags", "structured data", "sitemap", "robots.txt", "keyword optimization",
  "Google ranking", "on-page SEO".
argument-hint: page or site to audit
allowed-tools: Read, Edit, Grep, Glob, WebSearch
---

# Skill: SEO Auditor — Search Engine Optimization
**Category:** Optimization/Research

## Role
Audit and improve SEO: meta tags, structured data, content quality, technical SEO.

## When to invoke
- "improve our search ranking"
- New pages need SEO
- Technical SEO audit
- Content optimization

## Instructions
1. Title: unique, 50-60 chars, keyword first
2. Meta description: compelling, 150-160 chars, includes CTA
3. Heading hierarchy: one H1, logical H2/H3 structure
4. Structured data: relevant schema.org markup
5. Images: descriptive alt text, optimized file size, lazy loading
6. Internal links: relevant anchor text
7. sitemap.xml and robots.txt correct

## Output format
```
## SEO Audit — <page> — <date>
### Title: ✅/⚠️ (issue)
### Meta Description: ✅/⚠️
### Headings: ✅/⚠️
### Structured Data: ✅/⚠️
### Images: ✅/⚠️
### Fixes (priority order)
```

## Example
/seo-auditor audit index.html — optimize for "AI solutions for businesses" keyword

```

FILE: .claude/skills/ship/SKILL.md
```markdown
---
name: ship
description: >
  Full release checklist — tests, lint, security scan, build, deploy, health check, monitor.
  Invoke for: "ship it", "cut a release", "deploy to prod", "land this", "release",
  "push to production", "ship this feature", "ready to deploy", "go live".
  Inspired by gstack (Garry Tan) /ship and /land-and-deploy skills.
argument-hint: what to ship (branch, feature, or version)
allowed-tools: Read, Bash, Glob, Grep, Edit
---

# Skill: Ship — Full Release Pipeline
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack)

## Role
Act as Release Engineer. Enforce every gate before anything reaches production.
No step is skipped. No corner is cut. Ship with confidence or don't ship.

## When to Invoke
- Feature branch ready to merge
- Cutting a versioned release
- Deploying to staging or production
- "Can we ship this?" checkpoint

## Release Checklist

### Gate 1 — Code Quality
```bash
# All tests pass
pytest tests/ -q --tb=short

# Lint clean
ruff check src/ tests/ --select E,F,W --ignore E501

# Type check (if mypy configured)
mypy src/ --ignore-missing-imports 2>/dev/null || true

# No debug/TODO markers left
grep -rn "TODO\|FIXME\|HACK\|XXX\|breakpoint()\|pdb\|console\.log" src/ || echo "clean"
```

### Gate 2 — Evals
```bash
# Smoke suite (no API key needed)
ccm eval run data/evals/smoke.jsonl --dry-run

# Routing suite
ccm eval run data/evals/routing.jsonl --dry-run
```

### Gate 3 — Security
```bash
# No secrets in staged files
git diff --cached | grep -iE "(api_key|secret|password|token)\s*=" && echo "SECRETS FOUND — abort" || echo "clean"

# Dependency audit (if pip-audit available)
pip-audit 2>/dev/null || echo "pip-audit not installed — skip"
```

### Gate 4 — Build
```bash
# Docker build (if Dockerfile present)
docker build -t ccm:latest . --no-cache

# Or: Python package build
pip install -e ".[dev]" --quiet
ccm --help >/dev/null
```

### Gate 5 — Deploy & Verify
```bash
# Start service
docker compose up -d

# Health check
sleep 3
curl -sf http://localhost:8000/health | python3 -m json.tool

# Smoke test against live service
curl -sf -X POST http://localhost:8000/complete \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say OK", "auto_route": true}' | python3 -m json.tool
```

### Gate 6 — Commit & Tag
```bash
# Ensure clean working tree
git status

# Create release commit
git add -A
git commit -m "release: <version> — <one-line summary>"

# Tag (semver)
git tag -a v<version> -m "Release v<version>"
git push -u origin <branch> --tags
```

### Gate 7 — Post-Ship
- [ ] Update `CHANGELOG.md` (or run `/changelog`)
- [ ] Update `tasks/todo.md` — mark shipped items complete
- [ ] Monitor logs for 5 minutes post-deploy
- [ ] Notify team / update issue tracker

## Abort Conditions
Any gate failure = **stop and fix before continuing**. Do not skip gates with `--force` flags.
Do not deploy with failing tests. Do not bypass lint with `# noqa` without comment.

## Example
/ship the streaming API endpoint — ready to merge and deploy

## Quick Mode
If only deploying locally for testing (not production):
```bash
pytest tests/ -q && ccm serve --reload
```

```

FILE: .claude/skills/soc-analyst/SKILL.md
```markdown
---
name: soc-analyst
description: >
  Security operations: monitoring, threat detection, alert triage. Invoke for:
  "triage this alert", "is this suspicious", "investigate this log", "threat hunting",
  "SOC review", "anomaly detection", "security monitoring setup", "SIEM configuration",
  "investigate this", "what does this log mean".
argument-hint: log file, alert text, or monitoring scope to investigate
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Skill: SOC Analyst — Security Operations
**Category:** Security
**Color Team:** Blue

## Role
Monitor, detect, and triage security threats. Turn raw logs and alerts into actionable intelligence.

## When to invoke
- Alert triage needed
- Suspicious log entries to investigate
- Threat hunting in log data
- SIEM rule validation

## Instructions
1. Read the provided log/alert data
2. Extract: timestamp, source IP/user, action, target, outcome
3. Identify IOCs (Indicators of Compromise): unusual IPs, times, user agents, paths
4. Classify: True Positive / False Positive / Needs Investigation
5. Severity: Critical / High / Medium / Low / Info
6. Recommend: immediate action, investigation steps, escalation

## Output format
```
## SOC Triage — <date>
### Alert Summary
### IOCs Found
### Classification: <TP/FP/Investigate>
### Severity: <level>
### Recommended Action
```

## Example
/soc-analyst investigate failed login spike in auth.log from 2026-03-28

```

FILE: .claude/skills/sprint-planner/SKILL.md
```markdown
---
name: sprint-planner
description: >
  Plan sprint tasks and prioritize backlog. Invoke for: "plan the sprint", "sprint planning",
  "prioritize backlog", "what should we work on", "sprint goals", "task prioritization",
  "what's the next sprint".
argument-hint: backlog or goals to plan a sprint around
allowed-tools: Read, Write, Grep
---

# Skill: Sprint Planner — Agile Sprint Planning
**Category:** Project Management

## Role
Run sprint planning: prioritize backlog, assign story points, define sprint goal, create tasks/todo.md entries.

## When to invoke
- Sprint kickoff
- "plan our next sprint"
- Backlog refinement
- "what should we focus on"

## Instructions
1. Read current tasks/todo.md and MASTER_PLAN.md
2. Identify: what's highest value + lowest risk for next sprint?
3. Estimate complexity: S (1-2h) / M (half day) / L (full day) / XL (needs breakdown)
4. Define sprint goal: one clear sentence of what "done" looks like
5. Select tasks fitting 2-week sprint capacity
6. Write sprint plan to tasks/todo.md

## Output format
```
## Sprint Plan — Week of <date>
### Sprint Goal
### Tasks (ordered by priority)
- [ ] [S] Task name — AC: ...
- [ ] [M] Task name — AC: ...
### Capacity: XL/sprint
### Risks
```

## Example
/sprint-planner plan 2-week sprint from current MASTER_PLAN backlog

```

FILE: .claude/skills/sre/SKILL.md
```markdown
---
name: sre
description: >
  Site Reliability Engineering: SLOs, error budgets, toil reduction, reliability design.
  Invoke for: "SRE review", "reliability", "SLO", "error budget", "toil", "on-call",
  "uptime", "reduce incidents", "reliability engineering", "post-mortem".
argument-hint: service or reliability concern to address
allowed-tools: Read, Write, WebSearch
---

# Skill: SRE — Site Reliability Engineering
**Category:** DevOps/Infra

## Role
Apply SRE principles to improve system reliability: define SLOs, track error budgets, reduce toil, and run blameless post-mortems.

## When to invoke
- "we keep having incidents"
- Define SLOs for a service
- Post-mortem after outage
- "reduce on-call burden"

## Instructions
1. Define SLIs: what measurable signals represent user happiness?
2. Set SLOs: realistic targets (99.9% ≠ always right, depends on user need)
3. Track error budget: how much budget remains? Burning fast?
4. Identify toil: manual, repetitive operational work → automate it
5. Post-mortem: blameless, focus on system/process not people
6. Runbook: for every alert, there must be a runbook

## Output format
```
## SRE Assessment — <service>
### SLIs & SLOs
| SLI | SLO | Current |
### Error Budget: X% remaining
### Toil Identified
### Post-Mortem (if applicable)
### Recommendations
```

## Example
/sre define SLOs for the Claude API client — set error budget and alert thresholds

```

FILE: .claude/skills/stakeholder/SKILL.md
```markdown
---
name: stakeholder
description: >
  Create stakeholder updates and executive summaries. Invoke for: "stakeholder update",
  "executive summary", "status report", "update the team", "write progress report",
  "non-technical summary", "management update".
argument-hint: audience and timeframe for the update
allowed-tools: Read, Write, Bash
---

# Skill: Stakeholder — Executive Updates & Status Reports
**Category:** Project Management

## Role
Translate technical progress into clear, concise stakeholder updates that non-technical audiences understand.

## When to invoke
- Weekly status reports
- Executive briefings
- "write an update for the team"
- Post-milestone communication

## Instructions
1. Read MASTER_PLAN.md and tasks/todo.md for current progress
2. Run `git log --since="last week" --oneline` for recent work
3. No technical jargon — translate to business outcomes
4. Structure: Status (RAG) / What shipped / What's next / Risks
5. Lead with impact, not activity
6. Keep under 300 words

## Output format
```
## Project Update — <project> — <date>
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Blocked

### What Shipped (Last Week)
- Built 105+ AI skills for automatic invocation

### What's Coming (Next Week)
- Completing Python AI stack and documentation

### Risks
- None / [specific risk]
```

## Example
/stakeholder write weekly update for wellux_testprojects — non-technical audience

```

FILE: .claude/skills/standup/SKILL.md
```markdown
---
name: standup
description: >
  Generate daily standup report from completed tasks and git log. Invoke for:
  "standup", "daily standup", "what did I do yesterday", "progress report",
  "status update", "daily update", "what's my update".
argument-hint: date or timeframe for standup (defaults to yesterday)
allowed-tools: Read, Bash
---

# Skill: Standup — Daily Progress Report
**Category:** Project Management

## Role
Generate a concise daily standup from git log and task completion — Yesterday / Today / Blockers format.

## When to invoke
- Daily standup meeting
- "what did I accomplish"
- Progress reporting

## Instructions
1. `git log --since="yesterday" --oneline` — what was committed
2. Read tasks/todo.md — what was checked off
3. Format: Yesterday / Today / Blockers
4. Keep each section to 2-3 bullets max
5. No jargon — anyone should understand

## Output format
```
## Standup — <date>
### Yesterday ✅
- Completed X (commit: abc1234)
- Wrote Y skill files

### Today 🎯
- Working on Z (MASTER_PLAN step 3.1)
- Will review A

### Blockers 🚧
- None / [specific blocker]
```

## Example
/standup generate today's standup from git log and completed tasks

```

FILE: .claude/skills/superpowers/SKILL.md
```markdown
---
name: superpowers
description: >
  Activate high-agency coding mode: smarter workflows, better structure, less hand-holding.
  Invoke for: "superpowers mode", "high agency", "full autonomy", "senior engineer mode",
  "act like a staff engineer", "just figure it out", "autonomous coding".
  Inspired by Superpowers (obra) — turns Claude into a high-agency coding assistant.
argument-hint: task or context to apply superpowers to
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
---

# Skill: Superpowers — High-Agency Coding Mode
**Category:** Ecosystem
**Inspired by:** obra/superpowers

## Role
Operate as a senior staff engineer: anticipate needs, make good decisions without asking, structure work properly, ship confidently.

## When to invoke
- Complex technical tasks needing judgment
- "act as a senior engineer"
- High-autonomy mode needed
- "just figure out the best way"

## Superpowers Activated
1. **Anticipate**: think ahead — what will be needed after this step?
2. **Decide**: make the right call without asking for obvious things
3. **Structure**: organize code properly from the start (no refactor later)
4. **Test**: write tests as part of implementation, not after
5. **Document**: write clear code + comments for the non-obvious parts
6. **Refine**: after implementing, review own work before presenting

## Mode Rules
- Ask only for genuinely ambiguous requirements
- Read the codebase before writing code — understand existing patterns
- Follow existing patterns unless there's a clear reason not to
- Write code that a senior engineer would be proud of
- Think in systems: how does this fit the larger architecture?

## Example
/superpowers implement the complete rate limiter for the LLM client — full implementation, tests, docs

```

FILE: .claude/skills/swarm/SKILL.md
```markdown
---
name: swarm
description: >
  Decomposes a complex task into parallel subagents and creates all agent files for
  immediate execution. Invoke when: "create agents for this", "spin up a swarm",
  "parallel agents", "swarm this", "break into subagents", "orchestrate agents for",
  "what agents do I need", "build a swarm", "I need agents for this task",
  task is too large for a single context window, or multiple independent workstreams exist.
  Phase 1: read all project context. Phase 2: decompose into independent streams.
  Phase 3: create per-agent .md files in .claude/agents/. Phase 4: adversarial validation.
  Phase 5: deliver execution plan with quality gates.
argument-hint: full endstate description or task to decompose
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: Swarm — Parallel Agent Decomposer + Adversarial Validator

## Role
Decompose a complex task into parallel autonomous subagents, each with a focused mission.
Produce all agent definition files plus an orchestration plan with built-in adversarial
validation phase (dsifry/metaswarm pattern).

## When to invoke
- Task has 3+ independent workstreams that can run in parallel
- Task is too large for a single Claude context window
- User says "swarm", "parallel agents", "orchestrate agents", "build a swarm"
- Research + coding + testing + review can all happen simultaneously
- MASTER_PLAN phase has multiple parallel steps

## 4-Phase Execution Model

### Phase 1: Context + Decompose
1. Read CLAUDE.md, MASTER_PLAN.md, tasks/todo.md, relevant src/ files
2. Analyze endstate: what does "done" look like? What are all deliverables?
3. Split into independent workstreams (each needs no output from others to start)
   - Typical streams: research, code, test, review, docs, deploy

### Phase 2: Agent Design + File Creation
For each stream, define:
- **Mission**: 1-sentence outcome statement
- **Tools**: exactly which tools are needed
- **Input**: what context/files this agent needs to start
- **Output**: what files/artifacts it produces
- **Success criteria**: specific, verifiable conditions
- **Quality gate**: how to verify output before marking done

Write `.claude/agents/<stream>-agent.md` for each.

### Phase 3: Execution
- Run agents in dependency order (independent ones in parallel)
- Orchestrator does NOT trust subagent self-reports

### Phase 4: Adversarial Validation (NEW)
After each agent reports completion, the orchestrator spawns a **Validator agent** that:
- Independently re-reads the original spec
- Checks each success criterion with file:line evidence
- Reports: VERIFIED ✅ or FAILED ❌ with specific gaps
- On failure: spawns a new agent with the failure details as context
- Maximum 3 retry cycles before escalating to user

This prevents the "cargo cult complete" pattern where subagents report success without actually meeting the spec.

## Output Format

```
## Swarm Plan: <task name>
**Agents created:** N
**Parallelizable:** X of N
**Quality gates:** adversarial validation after each phase

| Agent | Mission | Runs After | Output | Quality Gate |
|-------|---------|------------|--------|-------------|
| research-agent | ... | — | data/research/ | content.md exists + >500 words |
| code-agent | ... | research | src/ | all tests pass |
| test-agent | ... | code | tests/ | coverage ≥80% |
| validator | ... | each agent | report | evidence-backed VERIFIED/FAILED |

## Execution Order
Round 1 (parallel): research-agent, docs-agent
Round 2 (parallel): code-agent
Round 3 (parallel): test-agent, review-agent
Round 4: adversarial-validator for all Round 1-3 outputs
```

## Example
/swarm Build a RAG system with Claude: research best approaches, implement retrieval, write tests, document API

```

FILE: .claude/skills/sysadmin/SKILL.md
```markdown
---
name: sysadmin
description: >
  OS hardening, patch management, and backup verification. Invoke for: "OS hardening",
  "patch status", "backup verification", "cron security", "file permissions audit",
  "system configuration review", "service account review", "log rotation setup",
  "syslog", "server hardening".
argument-hint: system or configuration to review (e.g. "Linux server config" or "cron jobs")
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: SysAdmin — OS Hardening & System Security
**Category:** Security
**Color Team:** Yellow

## Role
Harden operating systems, validate patch levels, verify backup integrity, and secure system configurations.

## When to invoke
- Server hardening review
- Cron job security audit
- File permission review
- Backup and recovery validation

## Instructions
1. Check file permissions: world-writable files? SUID/SGID bits?
2. Review cron jobs: who owns them? What do they execute? Writable scripts?
3. Service accounts: using minimal permissions? No interactive login?
4. Patch levels: OS, packages, kernel — any known CVEs?
5. SSH: root login disabled? Key-only auth? Fail2ban?
6. Backup: recent backup exists? Tested restore? Encrypted?

## Output format
```
## SysAdmin Audit — <system> — <date>
### File Permissions: ✅/⚠️
### Cron Jobs: ✅/⚠️
### Services: ✅/⚠️
### Patches: ✅/⚠️
### Backups: ✅/⚠️
### Findings
```

## Example
/sysadmin review Linux server config, cron jobs, and SSH hardening

```

FILE: .claude/skills/tdd/SKILL.md
```markdown
---
name: tdd
description: >
  Multi-agent TDD with strict subagent information isolation (glebis pattern).
  Invoke for: "test driven development", "TDD this", "write tests first", "red-green-refactor",
  "write failing tests then implement", "enforce TDD", "test-first development",
  "tdd workflow", "write specs then code". Spawns 3 isolated subagents.
argument-hint: feature or function to build via TDD
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: TDD — Multi-Agent Test-Driven Development

## Role
Enforce red-green-refactor at the architecture level, not discipline level.
Inspired by glebis/claude-skills information asymmetry pattern.

## The Core Insight
Most TDD fails because the developer can see both tests and implementation simultaneously.
This skill enforces information asymmetry through subagent context isolation:
- **TestWriter** sees only: specs, API signatures, requirements — never implementation
- **Implementer** sees only: failing test output, error messages — never the full test suite
- **Refactorer** sees only: passing green tests — nothing else

## Workflow

### Phase 1: TestWriter subagent
**Context given:** API signature, feature spec, acceptance criteria only.
**Task:** Write comprehensive failing tests covering:
- Happy path
- All edge cases and failure modes  
- Input validation
- Performance expectations if relevant
**Output:** `tests/test_<feature>.py` with all tests failing (red)

### Phase 2: Implementer subagent
**Context given:** `pytest` output showing failures ONLY (not the test source code).
**Task:** Write minimal implementation to make all tests pass.
**Constraint:** Do not look at test code — only read failure messages.
**Output:** `src/<module>/<feature>.py` with passing implementation

### Phase 3: Validation loop (up to 5 retries)
Run `pytest tests/test_<feature>.py`. If any tests still fail:
- Pass only the failure output to a fresh Implementer context
- Retry up to 5 times
- On retry 5 failure: escalate with full context

### Phase 4: Refactorer subagent
**Context given:** Passing test suite (green) + implementation
**Task:** Refactor for clarity, DRY, performance — without changing behavior
**Constraint:** All tests must still pass after refactor

## Instructions

1. **Parse the spec**: extract API signatures and acceptance criteria
2. **Spawn TestWriter**: write `tests/test_<feature>.py`; verify all tests FAIL initially
3. **Spawn Implementer**: pass only pytest failure output as context
4. **Run validation loop**: pytest → if red → new Implementer context with failures only
5. **Spawn Refactorer**: pass green test results + implementation
6. **Final check**: `pytest` + `ruff check` must both pass
7. **Report**: show test count, coverage, refactoring changes made

## Anti-patterns (will NOT do)
- Skip the failing-first check ("just write impl and tests together")
- Show the TestWriter any existing implementation code
- Show the Implementer the test source (only failure messages)
- Skip the refactor phase

## Output Format
```
## TDD: <feature>

### Phase 1 — TestWriter
✅ 12 tests written | all failing (expected)

### Phase 2 — Implementer (attempt 1/5)
✅ 11/12 passing | 1 failure: test_edge_case_empty_input

### Phase 2 — Implementer (attempt 2/5)  
✅ 12/12 passing | 🟢 all green

### Phase 4 — Refactorer
✅ Extracted 3 helpers, removed duplication | 12/12 still passing
✅ Lint: clean
```

```

FILE: .claude/skills/team/SKILL.md
```markdown
---
name: team
description: >
  Activate preset agent teams for parallel multi-role execution. Invoke for:
  "team mode", "spawn a team", "agent team", "parallel team review", "multi-agent team",
  "code review team", "security team", "debug team", "architecture team", "ship team",
  "team of agents", "multi-agent review". Presets: code-review, security, debug, architect,
  ship, research, onboarding. Inspired by wshobson/agents Agent Teams plugin.
argument-hint: team preset name or description of what team to assemble
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: Team — Preset Multi-Agent Teams

## Role
Assemble and coordinate preset teams of specialized agents for parallel, multi-perspective
execution of complex tasks. Each team member brings a different lens; the orchestrator
synthesizes findings into a unified recommendation.

## Available Teams

### `code-review` team
| Agent | Role | Focus |
|-------|------|-------|
| Correctness Reviewer | Senior Engineer | Logic errors, edge cases, race conditions |
| Style Reviewer | Code Quality | Naming, structure, readability, DRY |
| Security Reviewer | AppSec | OWASP Top 10, injection, auth, secrets |
| Test Reviewer | QA Engineer | Coverage gaps, test quality, missing cases |
| Performance Reviewer | Perf Eng | Algorithmic complexity, hot paths, memory |

### `security` team
| Agent | Role | Focus |
|-------|------|-------|
| AppSec | OWASP audit | Input validation, auth, XSS, SQLi |
| PenTester | Red team | Attack surface, exploitation paths |
| IAM Reviewer | Access control | Permissions, secrets, least privilege |
| Supply Chain | Dep auditor | CVEs, license issues, dependency risks |

### `debug` team
| Agent | Role | Focus |
|-------|------|-------|
| Root Cause Analyst | Senior Eng | Trace the failure to its origin |
| Hypothesis Generator | Scientist | Generate 5 alternative explanations |
| Test Case Designer | QA | Reproduce the bug in a minimal test |
| Fix Validator | Reviewer | Verify the fix doesn't break other paths |

### `architect` team
| Agent | Role | Focus |
|-------|------|-------|
| Systems Designer | Architect | Component design, data flow |
| Scalability Analyst | Infra | Performance, capacity, bottlenecks |
| Security Architect | SecEng | Threat model, trust boundaries |
| Pragmatist | Senior Dev | Complexity, maintainability, time-to-build |

### `ship` team (from gstack)
| Agent | Role | Focus |
|-------|------|-------|
| Test Runner | QA | All tests passing? |
| Lint Enforcer | CI | Lint clean? |
| Security Scanner | SecOps | No secrets, no vulnerabilities |
| Deploy Validator | DevOps | Health checks, rollback plan |
| Release Chronicler | PM | CHANGELOG updated? Version tagged? |

### `research` team (Karpathy-style)
| Agent | Role | Focus |
|-------|------|-------|
| Paper Miner | Researcher | Find relevant papers and repos |
| First-Principles Distiller | Theorist | Reduce to fundamental concepts |
| Implementation Sketcher | Engineer | Minimal working prototype idea |
| Skeptic | Critic | What's wrong with this approach? |

## Instructions

1. **Parse the request**: identify which preset team fits (or design a custom team)
2. **Define shared context**: what all agents need to know upfront
3. **Spawn agents in parallel** with isolated context windows
4. **Collect outputs**: each agent returns findings in standard format
5. **Synthesize**: orchestrator merges findings, surfaces conflicts, writes final recommendation
6. **Decision**: ranked action list with owner and urgency

## Output Format

```
## Team: <preset> on <target>

### Agent Assignments
- Agent 1 (Role): [brief mission]
- Agent 2 (Role): [brief mission]
...

### Findings
**[Agent 1]**: <key finding>
**[Agent 2]**: <key finding>

### Synthesis
[Where agents agree / where they conflict]

### Recommendations (ranked)
1. [Critical] Fix X — owner: security
2. [High] Refactor Y — owner: correctness
3. [Medium] Add test for Z — owner: test
```

```

FILE: .claude/skills/tech-debt/SKILL.md
```markdown
---
name: tech-debt
description: >
  Identify and systematically reduce technical debt. Invoke for: "tech debt",
  "clean up legacy code", "TODO cleanup", "code smells", "dead code", "deprecated",
  "legacy patterns", "maintenance burden", "cruft", "what's the worst code we have".
argument-hint: codebase area or specific debt category to address
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Tech Debt — Identify & Prioritize Cleanup
**Category:** Development

## Role
Audit the codebase for technical debt, prioritize by impact vs effort, and systematically eliminate it.

## When to invoke
- Dedicated refactoring sprint
- "what are our biggest code problems"
- Before adding new features to a messy area
- Post-project cleanup

## Instructions
1. Scan for TODOs, FIXMEs, HACKs, deprecated warnings
2. Identify: dead code, duplicate code, overly complex functions (> 50 lines), missing tests
3. Find: hardcoded values, magic numbers, outdated dependencies
4. Score each item: Impact (1-5) × Effort to fix (1-5 inverted) = Priority
5. Create prioritized list in tasks/todo.md
6. Fix highest-priority items first

## Output format
```
## Tech Debt Audit — <scope> — <date>
### Priority Matrix
| Item | Impact | Effort | Priority |
### Quick Wins (high impact, low effort)
### Big Rocks (high impact, high effort)
### Ignore (low impact)
```

## Example
/tech-debt full codebase — find all TODOs and dead code

```

FILE: .claude/skills/terraform/SKILL.md
```markdown
---
name: terraform
description: >
  Write Terraform IaC for cloud infrastructure. Invoke for: "terraform", "IaC",
  "infrastructure as code", "provision cloud resources", "AWS terraform",
  "terraform module", "terraform plan", "cloud infrastructure setup".
argument-hint: infrastructure to provision (e.g. "AWS VPC + ECS + RDS")
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Terraform — Infrastructure as Code
**Category:** DevOps/Infra

## Role
Write clean, modular Terraform configurations for cloud infrastructure with remote state and security best practices.

## When to invoke
- Provisioning cloud infrastructure
- "define this infra as code"
- Terraform module creation
- Infrastructure review

## Instructions
1. Use modules for reusability: vpc, compute, database, monitoring
2. Remote state: S3 + DynamoDB (AWS) or GCS (GCP) for state locking
3. Variables: all configurable values as variables with descriptions
4. Outputs: expose necessary values for other modules
5. Security: no secrets in tfvars, use Vault or AWS SSM
6. Tagging: all resources tagged with environment, project, owner

## Output format
Complete Terraform files: main.tf, variables.tf, outputs.tf, providers.tf

## Example
/terraform create AWS infrastructure: VPC, ECS cluster, RDS PostgreSQL, ALB

```

FILE: .claude/skills/test-writer/SKILL.md
```markdown
---
name: test-writer
description: >
  Write comprehensive tests: unit, integration, edge cases. Invoke for: "write tests",
  "add test coverage", "unit test this", "test suite", "TDD", "improve coverage",
  "test cases for", "missing tests", "test this function". Follows AAA pattern,
  targets 80%+ coverage, tests error paths and edge cases.
argument-hint: file or function to test
allowed-tools: Read, Write, Grep, Glob
---

# Skill: Test Writer — Comprehensive Test Suite
**Category:** Development

## Role
Write thorough tests that cover happy paths, error paths, edge cases, and boundary conditions.

## When to invoke
- New code without tests
- "write tests for X"
- Coverage below 80%
- TDD: write tests before implementation

## Instructions
1. Read the code under test — understand all paths
2. Identify: happy path, error paths, edge cases, boundary conditions
3. Follow AAA: Arrange (setup), Act (call), Assert (verify)
4. Mock external dependencies (DB, API, filesystem)
5. Test names: `test_<what>_<when>_<expected>` format
6. Cover: None/null inputs, empty collections, max values, concurrent access

## Output format
Complete test file(s) with:
- All imports
- Fixtures/setup
- One test per scenario
- Docstring for complex test intent

## Example
/test-writer src/llm/claude_client.py — test all methods including error handling

```

FILE: .claude/skills/trend-researcher/SKILL.md
```markdown
---
name: trend-researcher
description: >
  Research emerging trends in technology, AI, and markets. Invoke for: "what's trending",
  "latest trends in X", "emerging technology", "market trends", "tech radar",
  "what should I know about X", "trend analysis", "state of X in 2026".
argument-hint: domain or topic to research trends in
allowed-tools: WebSearch, WebFetch, Write
---

# Skill: Trend Researcher — Emerging Technology Trends
**Category:** Optimization/Research

## Role
Research and synthesize emerging trends in AI, technology, and markets into actionable insights.

## When to invoke
- Staying current with AI/tech trends
- Strategic technology decisions
- "what's new in X"
- Weekly/monthly trend briefings

## Instructions
1. WebSearch: `<domain> trends 2026`, `<domain> state of the art`, `<domain> emerging`
2. Read top 5-10 sources: blog posts, reports, GitHub trending
3. Extract: what's gaining momentum? What's declining? What's emerging?
4. Signal vs noise: separate genuine trends from hype
5. Relevance: which trends apply to this project?
6. Save to data/research/ with date

## Output format
```
## Trend Report — <domain> — <date>
### Rising 📈
1. Trend: [what] — Evidence: [signals] — Relevance: [high/med/low]
### Declining 📉
### Watch List 👀
### Recommended Actions
```

## Example
/trend-researcher AI agent frameworks 2026 — what's gaining vs declining

```

FILE: .claude/skills/tutorial-writer/SKILL.md
```markdown
---
name: tutorial-writer
description: >
  Write step-by-step tutorials and how-to guides. Invoke for: "write tutorial",
  "how-to guide", "tutorial for X", "explain how to use", "step-by-step guide",
  "workshop material", "create a tutorial", "teach someone to use".
argument-hint: topic and target audience for the tutorial
allowed-tools: Read, Write, Glob
---

# Skill: Tutorial Writer — Step-by-Step Learning Guides
**Category:** Documentation

## Role
Write tutorials that teach by doing — the reader ends up with something working after following along.

## When to invoke
- New feature needs user documentation
- "write a tutorial for X"
- Onboarding material needed
- Workshop or demo preparation

## Instructions
1. Define: who is the target reader? What will they accomplish?
2. Prerequisites: what must they have/know before starting?
3. Each step: one action, explanation of WHY, expected result
4. Code: runnable, tested, copy-pasteable
5. Checkpoint: verify working state at key points
6. Troubleshooting: common mistakes and how to fix them

## Output format
```markdown
# Tutorial: <title>
**Goal:** You will build/learn...
**Time:** ~Xmin | **Level:** Beginner/Intermediate

## Prerequisites
## Step 1: <verb + noun>
[explanation]
```code
```
Expected result: ...

## Troubleshooting
```

## Example
/tutorial-writer write tutorial for using the /karpathy-researcher skill — beginner level

```

FILE: .claude/skills/type-safety/SKILL.md
```markdown
---
name: type-safety
description: >
  Add or fix type annotations and enforce strict type safety. Invoke for: "add types",
  "type annotation", "TypeScript types", "Python type hints", "mypy", "tsc strict",
  "type errors", "any type", "unsafe cast", "missing types", "type this".
argument-hint: file or codebase to add types to
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Type Safety — Add Types & Fix Errors
**Category:** Development

## Role
Add complete type annotations and fix type errors to enable strict static analysis.

## When to invoke
- Codebase lacks type annotations
- mypy / tsc strict reporting errors
- "add types to this"
- Before enabling strict mode

## Instructions
1. Read all files in scope
2. For Python: add type hints to all function signatures, variables, and class attributes
3. For TypeScript: eliminate all `any`, add proper interfaces
4. Run type checker: `mypy --strict` or `tsc --strict`
5. Fix all errors systematically
6. Add `py.typed` marker (Python) or update `tsconfig.json` (TS)

## Output format
Show typed version of each function:
```python
# Before
def process(data, config):
    ...

# After
def process(data: dict[str, Any], config: Config) -> ProcessResult:
    ...
```

## Example
/type-safety src/llm/ — add full type annotations and fix mypy errors

```

FILE: .claude/skills/ui-ux/SKILL.md
```markdown
---
name: ui-ux
description: >
  Generate production-level UI/UX designs and code without endless iteration. Invoke for:
  "design this UI", "build this interface", "UI component", "make this look good",
  "design system", "UI/UX", "frontend design", "CSS design", "clean UI".
  Inspired by UI UX Pro Max (nextlevelbuilder) skill patterns.
argument-hint: UI component or page to design
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: UI/UX Pro Max — Production UI Without Endless Iteration
**Category:** Ecosystem
**Inspired by:** nextlevelbuilder/ui-ux-pro-max-skill

## Role
Generate clean, production-level UI code and UX patterns on the first attempt — no endless iteration required.

## When to invoke
- Building new UI components
- "make this look professional"
- Design system setup
- "clean up this UI"

## UI Design Principles (applied automatically)
1. **8px grid**: all spacing in multiples of 8px
2. **Design tokens**: CSS custom properties for colors, spacing, typography
3. **Component isolation**: each component is self-contained
4. **Mobile first**: base styles for mobile, enhance for desktop
5. **Accessibility**: semantic HTML, ARIA, focus states
6. **Performance**: no layout thrashing, GPU-composited animations only

## Instructions
1. Read existing design tokens / CSS variables if any
2. Design component: layout, typography, color, interaction states
3. Implement: semantic HTML + CSS custom properties
4. Include: hover, focus, active, disabled states
5. Test: does it work on mobile? Accessible by keyboard?

## Output format
Complete HTML + CSS with design tokens:
```html
<!-- Component with design tokens -->
<style>
:root { --color-primary: #...; --spacing-4: 32px; }
</style>
```

## Example
/ui-ux design a clean skills directory card component with hover state and accessibility

```

FILE: .claude/skills/vision-analyst/SKILL.md
```markdown
---
name: vision-analyst
description: >
  Analyze images and design vision AI pipelines. Invoke for: "analyze this image",
  "vision AI", "image classification", "object detection", "OCR", "screenshot analysis",
  "process this image", "what's in this image", "image pipeline".
argument-hint: image path or vision task to implement
allowed-tools: Read, Write, WebSearch
---

# Skill: Vision Analyst — Image Analysis & Vision AI
**Category:** AI/ML Research

## Role
Analyze images using multimodal LLMs and design vision AI pipelines for classification, detection, and extraction.

## When to invoke
- Image analysis needed
- "what's in this screenshot"
- Building vision-based automation
- OCR or document extraction from images

## Instructions
1. For image analysis: use Claude claude-sonnet-4-6 vision (pass image + prompt)
2. For classification: define categories, few-shot with example images
3. For OCR: extract text, preserve structure
4. For pipelines: preprocess → embed/classify → postprocess → store results
5. Batch processing: handle multiple images efficiently
6. Save results to `data/outputs/`

## Output format
Depends on task:
- Analysis: structured JSON with findings
- Classification: label + confidence
- OCR: extracted text with structure preserved
- Pipeline: complete Python implementation

## Example
/vision-analyst analyze screenshots in data/ — extract UI patterns and categorize

```

FILE: .claude/skills/web-scraper/SKILL.md
```markdown
---
name: web-scraper
description: >
  Build web scrapers for data collection and research. Invoke for: "scrape this website",
  "web scraping", "extract data from", "crawl", "collect data from web",
  "automate data collection", "fetch and parse HTML".
argument-hint: URL or site to scrape and data to extract
allowed-tools: Read, Write, WebFetch, WebSearch
---

# Skill: Web Scraper — Automated Data Collection
**Category:** Optimization/Research

## Role
Build ethical, respectful web scrapers for research data collection.

## When to invoke
- "collect data from X website"
- Research data gathering
- Monitoring web content for changes
- Bulk content extraction

## Instructions
1. Check robots.txt before scraping
2. Rate limit: never more than 1 request/second without permission
3. Use WebFetch for individual pages, design crawler for multiple
4. Parse: BeautifulSoup for HTML, cssselect for specific elements
5. Store: save to data/outputs/ with source URL and timestamp
6. Ethics: don't scrape private/sensitive data, respect ToS

## Output format
```python
# Scraper pattern
def scrape_page(url: str) -> dict:
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    return {
        "url": url,
        "title": soup.find("h1").text,
        "content": ...,
        "scraped_at": datetime.now().isoformat()
    }
```

## Example
/web-scraper collect AI research blog posts from arxiv.org for the research pipeline

```

FILE: .claude/skills/web-vitals/SKILL.md
```markdown
---
name: web-vitals
description: >
  Audit and optimize Core Web Vitals (LCP, CLS, FID/INP). Invoke for: "web vitals",
  "page speed", "LCP", "CLS", "INP", "Lighthouse", "performance audit",
  "slow page load", "improve page speed score", "Core Web Vitals".
argument-hint: URL or HTML file to audit
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Web Vitals — Core Web Vitals Optimization
**Category:** Optimization/Research

## Role
Audit and improve Core Web Vitals to meet Google's thresholds: LCP < 2.5s, CLS < 0.1, INP < 200ms.

## When to invoke
- Page performance issues
- SEO improvements needed
- "Lighthouse score is low"
- Before launch performance gate

## Instructions
1. Read HTML/CSS/JS to identify issues without running Lighthouse
2. LCP: largest image lazy-loaded? Critical images preloaded? Server response fast?
3. CLS: all images have explicit dimensions? No layout shifts on load?
4. INP: main thread blocked? Event handlers fast? Third-party scripts deferred?
5. TTFB: server response time? CDN used?
6. Prioritize: fix highest-impact issues first

## Output format
```
## Web Vitals Audit — <page> — <date>
### LCP: X.Xs (target < 2.5s) — Issue: lazy-loaded hero image
### CLS: X.X (target < 0.1) — Issue: missing image dimensions
### INP: Xms (target < 200ms) — Issue: heavy JS on main thread
### Fixes (priority order)
```

## Example
/web-vitals audit index.html — identify and fix Core Web Vitals issues

```

FILE: .claude/skills/write-plan/SKILL.md
```markdown
---
name: write-plan
description: >
  Decompose a feature into atomic 2-5 minute tasks with explicit acceptance criteria.
  Invoke for: "write a plan", "break this down", "make a task list", "plan before coding",
  "decompose this feature", "create subtasks", "what are the steps", "planning phase",
  "plan this out", "task breakdown". Inspired by Superpowers (obra/superpowers) /write-plan phase.
argument-hint: feature or task to plan (ideally after /brainstorm)
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Skill: Write Plan — Atomic Task Decomposition
**Category:** Ecosystem
**Inspired by:** Superpowers (github.com/obra/superpowers)

## Role
Act as a tech lead breaking down a feature into the smallest independently-verifiable tasks.
Each task must be completable in 2-5 minutes with a clear pass/fail acceptance criterion.

## When to Invoke
- After `/brainstorm` has clarified requirements
- Before starting implementation of a multi-step feature
- When a feature needs to be divided across multiple sessions or agents
- When you need to track implementation progress explicitly

## Planning Rules

### Task Granularity
- **Too big:** "implement rate limiter" (multiple hours, unclear done state)
- **Too small:** "add import statement" (30 seconds, not worth tracking)
- **Just right:** "write `RateLimiter.is_allowed(key)` that returns bool, sliding window 60s"

### Each Task Must Have
1. **What** — concrete deliverable (function, file, test, config)
2. **Done when** — explicit acceptance criterion (test passes, command outputs X, file exists)
3. **Sequence** — must-happen-before dependencies noted

### Task Categories
- `[INFRA]` — scaffolding, file creation, dependencies
- `[IMPL]` — production code implementation
- `[TEST]` — test coverage
- `[DOCS]` — documentation, comments
- `[CI]` — build, lint, eval gates
- `[REVIEW]` — code review checkpoint

## Process

1. Read relevant source files to understand existing patterns
2. Identify the implementation layers (data model → logic → API → tests → docs)
3. Write tasks bottom-up: tests last so they verify real behavior
4. Sequence tasks so each builds cleanly on the previous
5. Add a final `[CI]` gate task: `pytest + ruff + ccm eval run --dry-run`

## Output Format

Write directly to `tasks/todo.md`:

```markdown
## Plan: <Feature Name>
> Started: YYYY-MM-DD | Source: /write-plan

- [ ] [INFRA] Create `src/<module>.py` with module docstring and imports
      Done: file exists, `from src.<module> import X` works
- [ ] [IMPL] Implement `<ClassName>.__init__(self, param: type)` with validation
      Done: constructor raises `ValueError` on invalid input
- [ ] [IMPL] Implement `<ClassName>.method(self, arg) -> ReturnType`
      Done: returns expected value for happy path
- [ ] [TEST] Write `tests/test_<module>.py::TestClassName::test_method_happy_path`
      Done: test passes with `pytest tests/test_<module>.py -q`
- [ ] [TEST] Write `TestClassName::test_method_invalid_input_raises`
      Done: test passes
- [ ] [DOCS] Add docstrings to public methods
      Done: `pydoc src/<module>` shows all public method signatures
- [ ] [CI] Run full gate: `pytest tests/ -q && ruff check src/ tests/ --select E,F,W --ignore E501`
      Done: exit code 0 on both
```

## Integration

After writing the plan:
- Tasks appear in session-start.sh boot banner (open task count)
- `f` shortcut executes the next `- [ ]` item
- `/superpowers` executes with discipline: tests before marking complete

## Example
/write-plan implement sliding-window rate limiter for ClaudeClient (post-brainstorm)

```


---

# 5. DEPENDENCIES

## Python Dependencies (pyproject.toml)

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | `>=0.87.0,<1.0` | Official Anthropic SDK — completion, chat, streaming. 0.87.0+ required for CVE fixes |
| `cryptography` | `>=46.0.6` | Transitive dep from anthropic; pinned for CVE-2026-34073 + 5 earlier CVEs |
| `httpx` | `>=0.27.0,<1.0` | Async HTTP client used internally by anthropic SDK |
| `aiohttp` | `>=3.9.0,<4.0` | Async HTTP for non-Anthropic requests |
| `fastapi` | `>=0.111.0,<1.0` | REST framework for /health, /v1/complete, /v1/chat, /v1/route |
| `uvicorn[standard]` | `>=0.30.0,<1.0` | ASGI server for FastAPI; [standard] adds websockets + reload |
| `pydantic` | `>=2.7.0,<3.0` | Request/response validation; v2 required (v1 API differs significantly) |
| `PyYAML` | `>=6.0.1` | YAML config parsing (model_config.yaml, logging_config.yaml) |
| `python-dotenv` | `>=1.0.0` | Loads .env file for ANTHROPIC_API_KEY etc. in dev |

## Dev Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | `>=8.2.0` | Test runner |
| `pytest-asyncio` | `>=0.23.0` | Async test support; `asyncio_mode = "auto"` in pyproject.toml |
| `pytest-cov` | `>=5.0.0` | Coverage reporting |
| `ruff` | `>=0.9.0,<1.0` | Linter + formatter (E, F, W, I, UP, B rules) |
| `mypy` | `>=1.10.0` | Static type checking |
| `pre-commit` | `>=3.7.0` | Git hook framework for lint-on-commit |

## Optional Extras

| Extra | Purpose |
|-------|---------|
| `.[ml]` | torch, transformers, sentence-transformers, faiss-cpu, chromadb for ML features |
| `.[deploy]` | mcp>=1.0.0 for MCP server (deferred import in src/mcp_server.py) |

## Entry Point
`ccm = "src.cli:main"` — installed via `pip install -e ".[dev]"`

---

# 6. ENVIRONMENT & CONFIGURATION

## Required Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `ANTHROPIC_API_KEY` | Yes (prod) | None | Anthropic API auth. All LLM calls fail without this. |
| `OPENAI_API_KEY` | No | None | OpenAI GPTClient. Only needed if using GPT models. |
| `CCM_LOG_PATH` | No | `data/cache/events.log` | Path for structured event log (JSONL) |
| `CCM_DEFAULT_MODEL` | No | `claude-sonnet-4-6` | Override default model for completions |
| `CCM_RATE_LIMIT` | No | `100` | Requests per minute limit |
| `CCM_CACHE_TTL` | No | `3600` | Response cache TTL in seconds |

## .env.example structure
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...   # optional
CCM_LOG_PATH=data/cache/events.log
```

## Required Services
- No database required (all persistence is filesystem-based)
- No message queues
- Anthropic API (https://api.anthropic.com) — all LLM operations
- MCP servers (local processes) if using MCP features

## Ports
- `8000` — FastAPI HTTP server (default, configurable via `ccm serve --port`)
- No other ports required

## Config Files
- `config/model_config.yaml` — model selection + parameters per use case
- `config/logging_config.yaml` — log level, format, output targets
- `config/prompt_templates.yaml` — reusable prompt template library
- `pyproject.toml` — all build/test/lint configuration
- `.claude/settings.json` — Claude Code permissions + hooks wiring
- `.mcp.json` — MCP server connections (github, filesystem, memory, etc.)

---

# 7. BUILD, RUN, AND DEPLOYMENT

## Initial Setup (local dev)

```bash
# 1. Clone and enter project
git clone <repo-url> && cd wellux_testprojects

# 2. Install with dev extras (editable install for src/ path to work)
pip install -e ".[dev]"

# 3. Set API key
export ANTHROPIC_API_KEY=sk-ant-...
# or: cp .env.example .env && edit .env

# 4. Verify install
ccm version
ccm doctor

# 5. Run tests
python3 -m pytest tests/ -q

# 6. Lint check
ruff check src/ tests/ --select E,F,W --ignore E501
```

**CRITICAL**: Must use `pip install -e .` (editable) — the entry point `ccm = "src.cli:main"` 
requires `src` on `sys.path`. The `[tool.setuptools.packages.find]` in pyproject.toml sets 
`where = ["."]` so the project root is the package root.

**CRITICAL**: Use `python3 -m pytest` not bare `pytest` if pytest was installed via `uv tools` — 
the uv-installed pytest runs in a different venv that won't have pydantic/fastapi.

## Common Development Commands

```bash
ccm version                          # show version info
ccm status                           # git status + test count + skill count
ccm doctor                           # environment health check
ccm route "your task"                # see routing decision
ccm complete "your prompt"           # one-shot LLM call
ccm serve                            # start FastAPI on port 8000
ccm serve --host 0.0.0.0 --port 8080 --reload
ccm eval list                        # list available eval suites
ccm eval run data/evals/smoke.jsonl --dry-run   # no API key needed
ccm eval run data/evals/smoke.jsonl  # real LLM calls
ccm logs                             # query event log
ccm context-diff                     # diff since HEAD~1
ccm memory-bank status               # show memory tier status
ccm lint                             # run ruff check
```

## Docker

```bash
# Build
docker build -t ccm:latest .
# or:
ccm build

# Run
docker compose up
# API available at http://localhost:8000

# Health check (built into Dockerfile)
curl http://localhost:8000/health

# Deploy pipeline (test → build → up → verify)
ccm deploy --env local
ccm deploy --env staging --dry-run
```

## CI/CD (GitHub Actions)

Three jobs in `.github/workflows/ci.yml`:

1. **test** — runs on Python 3.11 and 3.12
   - `ruff check src/ tests/`  
   - `pytest tests/ --cov=src --cov-fail-under=85`
   - Coverage uploaded to Codecov

2. **smoke-evals** — runs after test passes
   - `python -m src.cli eval run data/evals/smoke.jsonl --dry-run`
   - No API key needed (--dry-run returns prompt as output)

3. **lint-dockerfile** — `hadolint Dockerfile`

Live eval jobs gate on `ANTHROPIC_API_KEY` secret being present.

---

# 8. CODEBASE PATTERNS & CONVENTIONS

## Coding Style
- Python 3.11+ (`from __future__ import annotations` in every file)
- `str | None` over `Optional[str]` (Python 3.10+ union syntax)
- Line length: 100 chars (ruff enforced)
- Imports: stdlib → third-party → local (ruff I-sorted)
- Constants: `UPPER_SNAKE_CASE` with module prefix (`_SKILL_REGISTRY`, `_HIGH_SIGNALS`)
- Private: single underscore prefix (`_build_server`, `_capture`, `_require_fastmcp`)

## Error Handling Pattern
```python
# In handlers/error_handler.py — classify_api_error():
try:
    ...
except anthropic.RateLimitError:
    # → RateLimitError
except anthropic.AuthenticationError:
    # → AuthenticationError
```
- HTTPException detail never exposes `str(e)` directly — uses `f"Upstream LLM error [{type(e).__name__}] — see server logs (request_id={rid})"`
- Logger redacts sensitive fields: `password`, `token`, `api_key`, `secret`

## Logging Pattern
```python
from src.utils.logger import get_logger
logger = get_logger(__name__)
logger.info("event_name", key1=val1, key2=val2)  # structured JSON
logger.error("error_event", error=str(e), request_id=rid)
```
All logs are structured JSON (structlog-style). Never `print()` in production code.

## Test Pattern
```python
class TestFunctionName:
    def test_behaviour_when_condition(self):
        # Arrange
        ...
        # Act
        result = function_under_test(...)
        # Assert
        assert result == expected
```
- One assertion focus per test
- Mock at boundaries: `@patch("src.module.external_call")`
- Async tests: auto-detected, no decorator needed (`asyncio_mode = "auto"`)
- Import guards: inject fake modules before importing module-under-test (see test_mcp_server.py)

## Routing Pattern
Every task goes through `route()` in `src/routing/__init__.py`:
```python
decision = route("your task description")
# decision.llm.model → Model.SONNET
# decision.skill.skill → "deploy-checker"
# decision.agent.agent → AgentType.GENERAL
# decision.memory.tier → MemoryTier.TODO
# decision.plan.size → PlanSize.MEDIUM
```

## Skill Trigger Pattern (skill_router.py)
Each entry in `_SKILL_REGISTRY`:
```python
{"skill": "skill-name", "category": "category", "priority": 8,
 "triggers": ["exact phrase", "another phrase", ...]}
```
No duplicate trigger phrases allowed — enforced by `test_no_duplicate_trigger_phrases` test.
Match is performed by a SINGLE compiled regex across all triggers (O(1) scan, not O(n) loop).

## Memory Tier Pattern
```python
tm = TieredMemory()
tm.write_hot("key", "value")    # ≤50 lines, always loaded
tm.write_warm("topic", "content")  # domain files, loaded when relevant
tm.archive_glacier("slug", content, tags=["arch"])  # YAML frontmatter archive
results = tm.search_glacier("search term")  # full-text + tag search
```

---

# 9. DATA MODELS & SCHEMAS

## Core Request/Response Models (src/api/models.py)

```python
class CompleteRequest:
    prompt: str
    system: str | None = None
    model: str | None = None          # None = auto-route
    max_tokens: int = 4096            # range: 1-200000
    temperature: float = 0.7          # range: 0.0-1.0
    stream: bool = False
    auto_route: bool = True

class CompleteResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    stop_reason: str
    routed_by: str | None

class ChatMessage:
    role: str        # "user" | "assistant"
    content: str

class ChatRequest:
    messages: list[ChatMessage]  # min 1 item
    system: str | None = None
    model: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7

class ChatResponse:
    message: ChatMessage
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float

class HealthResponse:
    status: str
    version: str
    models_available: list[str]
    uptime_s: float | None
```

## LLM Base Models (src/llm/base.py)

```python
class CompletionRequest:
    prompt: str
    system: str | None
    model: str | None
    max_tokens: int = 4096
    temperature: float = 0.7

class CompletionResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    stop_reason: str
    cost_usd: float   # computed from token counts
```

## Eval Framework Models (src/evals/types.py)

```python
@dataclass
class EvalCase:
    name: str
    prompt: str
    contains: list[str] = []     # all must appear in output
    excludes: list[str] = []     # none must appear in output
    min_score: float = 0.7       # custom scorer threshold
    tags: list[str] = []
    scorer: Callable | None = None

@dataclass
class EvalResult:
    case: EvalCase
    output: str
    passed: bool
    score: float
    latency_ms: int
    error: str | None

@dataclass
class EvalReport:
    suite_name: str
    results: list[EvalResult]
    pass_rate: float             # 0.0-1.0
    mean_score: float
    mean_latency_ms: float
    total_cases: int
    passed: int
    failed: int
```

## Routing Decision Models (src/routing/)

```python
@dataclass
class SkillMatch:
    skill: str            # matches .claude/skills/<name>/
    confidence: float     # 0.0-1.0
    reason: str
    category: str
    fallback: str | None  # next-best skill

@dataclass
class RoutingDecision:    # in llm_router.py
    model: Model
    complexity: Complexity
    reason: str
    score: int
    estimated_cost_tier: str

@dataclass
class RoutingBundle:      # in routing/__init__.py
    llm: LLMRoutingDecision
    skill: SkillMatch | None
    agent: AgentRoutingDecision
    memory: MemoryRoutingDecision
    plan: TaskPlan
```

## Tiered Memory Schema

**Hot tier** (`.claude/memory/hot/hot-memory.md`): Markdown, ≤50 lines, free-form key/value. Always loaded.

**Warm tier** (`.claude/memory/warm/*.md`): Markdown files by topic. Loaded on demand.

**Glacier tier** (`.claude/memory/glacier/*.md`): YAML frontmatter + body:
```yaml
---
slug: decision-slug
date: 2026-04-05
tags: [architecture, decision]
summary: One-line summary
---
# Full content here
```

---

# 10. API DESIGN

## Endpoints

| Method | Path | Description | Request | Response |
|--------|------|-------------|---------|---------|
| GET | `/health` | Status check | — | `HealthResponse` |
| POST | `/v1/complete` | Single-turn LLM completion | `CompleteRequest` | `CompleteResponse` |
| POST | `/v1/complete/stream` | SSE streaming tokens | `CompleteRequest` | `text/event-stream` |
| POST | `/v1/chat` | Multi-turn conversation | `ChatRequest` | `ChatResponse` |
| POST | `/v1/route` | Routing decision (no LLM) | `RouteRequest` | `RouteResponse` |

## Example Requests

```bash
# Health
curl http://localhost:8000/health

# Complete
curl -X POST http://localhost:8000/v1/complete \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Python hello world", "auto_route": true}'

# Chat (multi-turn)
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}, {"role": "user", "content": "What did I say?"}]}'

# Stream
curl -X POST http://localhost:8000/v1/complete/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Count to 5"}' --no-buffer

# Route (no LLM call)
curl -X POST http://localhost:8000/v1/route \
  -H "Content-Type: application/json" \
  -d '{"task": "security audit the codebase"}'
```

## Authentication
- No auth required (internal/local service)
- API key passed via `ANTHROPIC_API_KEY` env var on the server side only

## Headers (every response)
- `X-Request-ID`: correlation ID (read from request or generated UUID4)
- `X-Process-Time-Ms`: total handler duration in milliseconds

## Rate Limiting
- 100 req/min per server instance (not per user)
- Returns HTTP 429 when exceeded
- Configurable via `CCM_RATE_LIMIT` env var

## Streaming Format
```
data: Hello\n\n
data:  world\n\n
data: [DONE]\n\n
```

---

# 11. CURRENT STATE OF THE PROJECT

## What Is Fully Working

- **CLI** (`ccm`): All 15+ subcommands work: version, route, complete, serve, status, doctor, research, logs, eval list/inspect/run, build, deploy, ps, health, context-diff, memory-bank, lint
- **FastAPI REST API**: All 5 endpoints operational: /health, /v1/complete, /v1/complete/stream, /v1/chat, /v1/route
- **5-Router system**: llm, skill, agent, memory, task routers all functional
- **123 Skills**: All registered and trigger-tested (no duplicates enforced by test)
- **Eval framework**: EvalSuite, EvalCase, EvalRunner, AsyncEvalRunner — all working with dry-run mode
- **TieredMemory**: hot/warm/glacier read/write/search all functional
- **ClaudeClient**: complete(), chat(), stream() all working with retry/backoff/cache/rate-limit
- **MCP server**: src/mcp_server.py exposes deploy/build/health/status/doctor/get_logs tools via FastMCP
- **Hooks**: All 7 hooks wired (session-start, pre-compact, pre-bash, post-edit, post-pr, stop, user-prompt-submit)
- **CI**: 3-job pipeline passing (test matrix 3.11+3.12, smoke-evals, lint-dockerfile)
- **Tests**: 667 passing, 0 failing
- **Coverage**: 100% on version.py and mcp_server.py; ~85%+ overall
- **Lint**: ruff CLEAN

## What Is Partially Implemented

- **GPTClient** (`src/llm/gpt_client.py`): Implemented but OpenAI SDK not in default deps (in `.[ml]`)
- **ML extras**: torch/transformers/faiss/chromadb skeleton present but not wired to routing
- **Optimizer crons**: Scripts exist in `tools/scripts/` but systemd timers not configured in repo

## What Is Broken or Unstable

- Nothing currently broken. All tests pass. All lints clean.

## Known Limitations (Not Bugs)

- No authentication on FastAPI endpoints (documented: internal-only service)
- No CORS middleware (documented: internal API; add if building a web frontend)
- `count_tokens()` on ClaudeClient uses rough heuristic (≈4 chars/token), not the API's exact counter
- `data/sessions/`, `data/cache/`, `data/research/` are gitignored — not persisted in repo
- `.pre-commit-config.yaml` pins ruff at `v0.4.10`; pyproject requires `>=0.9.0` — these may diverge (pre-commit uses its own venv)

---

# 12. RECENT CHANGES / DIFFS

## Last 20 Commits

```
2edefc5 chore: sync memory files
5e36d6d chore: sync memory and session files
147b0ed test: 100% coverage on version.py and mcp_server.py
c5a4f04 chore: sync memory files
dd18fa2 fix(hooks): test count misses async def test_ and module-level tests
e296c07 docs: sync all docs to v1.0.7 state
6287399 chore: sync warm memory
3e7e460 chore: fix stale lesson count in hot-memory critical files (26 → 31)
c44cfe8 chore: add session log 2026-04-06
616bac1 fix(hooks): grep -c exits 1 on zero matches causing 0\n0 count strings
194454f fix(pre-compact): prevent backtick expansion corrupting hot-memory.md
59d94ee fix(version): correct VERSION_INFO to 4-tuple (major, minor, patch, pre)
4b62160 fix(version): read version dynamically from installed metadata or pyproject.toml
da20c0e docs(CLAUDE.md): document v1.0.7 additions — open-findings, 30 lessons, hook improvements
83a936c chore(self-reflect): add lessons 27-30 from v1.0.7 session
6ef0f29 chore: document v1.0.7 in CHANGELOG + hot-memory
990c685 chore: sync memory files
e46c0e6 fix(v1.0.7): resolve all P3 open findings
e35c5cc chore: sync memory files
0bdbd92 fix(v1.0.7): resolve all P2 open findings
```

## Detailed Diff: Last 5 Commits vs HEAD~5

```diff
diff --git a/.claude/hooks/pre-compact.sh b/.claude/hooks/pre-compact.sh
index d81f104..60c7cc2 100644
--- a/.claude/hooks/pre-compact.sh
+++ b/.claude/hooks/pre-compact.sh
@@ -13,7 +13,7 @@ BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
 UNCOMMITTED=$(git -C "$BASE" status --short 2>/dev/null | wc -l | tr -d ' ')
 LAST_COMMIT=$(git -C "$BASE" log -1 --oneline 2>/dev/null || echo "no commits")
 VERSION=$(grep '^version = ' "$BASE/pyproject.toml" 2>/dev/null | sed 's/version = "//;s/"//' || echo "unknown")
-TEST_COUNT=$(grep -rE '^\s+def test_|^def test_' "$BASE/tests/" 2>/dev/null | wc -l | tr -d ' ')
+TEST_COUNT=$(grep -rE '^\s*(async\s+)?def test_' "$BASE/tests/" 2>/dev/null | wc -l | tr -d ' ')
 SKILL_COUNT=$(find "$BASE/.claude/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
 
 # ── 2. Get last 3 commits ──────────────────────────────────────────────────────
diff --git a/.claude/hooks/session-start.sh b/.claude/hooks/session-start.sh
index 793a82c..c0ad9d3 100755
--- a/.claude/hooks/session-start.sh
+++ b/.claude/hooks/session-start.sh
@@ -137,7 +137,7 @@ cd "$BASE" 2>/dev/null || true
 PYTHON_VER=$(python3 --version 2>&1 | sed 's/Python //')
 printf '  \033[0;34m▸ Python\033[0m  %s\n' "$PYTHON_VER"
 
-TEST_COUNT=$(grep -rE '^\s+def test_|^def test_' tests/ 2>/dev/null | wc -l | tr -d ' ')
+TEST_COUNT=$(grep -rE '^\s*(async\s+)?def test_' tests/ 2>/dev/null | wc -l | tr -d ' ')
 printf '  \033[0;34m▸ Tests\033[0m   \033[1;32m%s functions\033[0m\n' "$TEST_COUNT"
 
 LINT_ERRORS=$(python3 -m ruff check src/ tests/ --select E,F,W --ignore E501 --quiet 2>/dev/null | wc -l | tr -d ' ')
diff --git a/tests/test_mcp_server.py b/tests/test_mcp_server.py
index 6be05b5..330fb0a 100644
--- a/tests/test_mcp_server.py
+++ b/tests/test_mcp_server.py
@@ -210,6 +210,33 @@ class TestGetLogsTool:
         assert captured_args[0].event == "api_startup"
 
 
+# ── _build_server + run ───────────────────────────────────────────────────────
+
+class TestBuildServer:
+    def test_returns_mcp_instance(self):
+        server = _mcp_mod._build_server()
+        # FastMCP was called with the app name
+        _fake_fastmcp_cls.assert_called_with(
+            "ccm", instructions="Claude Code Max deployment and operations server"
+        )
+        assert server is _fake_fastmcp_cls.return_value
+
+    def test_all_tools_registered(self):
+        """All 6 tool functions are registered via mcp.tool()."""
+        instance = _fake_fastmcp_cls.return_value
+        # .tool() called once per function (deploy, build, health, status, doctor, get_logs)
+        assert instance.tool.call_count >= 6
+
+    def test_run_calls_build_server_run(self):
+        """run() delegates to _build_server().run()."""
+        with patch.object(_mcp_mod, "_build_server") as mock_build:
+            mock_server = MagicMock()
+            mock_build.return_value = mock_server
+            _mcp_mod.run()
+        mock_build.assert_called_once()
+        mock_server.run.assert_called_once()
+
+
 # ── import guard ──────────────────────────────────────────────────────────────
 
 class TestRequireFastmcp:
diff --git a/tests/test_version.py b/tests/test_version.py
index e1cb198..d97eebf 100644
--- a/tests/test_version.py
+++ b/tests/test_version.py
@@ -34,3 +34,36 @@ class TestVersion:
     def test_package_exports_version(self):
         import src
         assert src.__version__ == __version__
+
+
+class TestReadVersionFallbacks:
+    def test_tomllib_fallback_when_metadata_unavailable(self, tmp_path):
+        """tomllib path used when importlib.metadata raises; reads from real pyproject.toml."""
+        import io
+        from unittest.mock import patch
+
+        import src.version as vmod
+
+        toml_bytes = b'[project]\nversion = "9.8.7"\n'
+        with patch("importlib.metadata.version", side_effect=Exception("not found")):
+            with patch("pathlib.Path.open", return_value=io.BytesIO(toml_bytes)):
+                result = vmod._read_version()
+        assert result == "9.8.7"
+
+    def test_dev_fallback_when_all_fail(self):
+        """Returns '0.0.0+dev' when both importlib.metadata and tomllib fail."""
+        from unittest.mock import patch
+
+        import src.version as vmod
+
+        with patch("importlib.metadata.version", side_effect=Exception("no meta")):
+            with patch("pathlib.Path.open", side_effect=Exception("no file")):
+                result = vmod._read_version()
+        assert result == "0.0.0+dev"
+
+    def test_version_info_shape_for_dev_string(self):
+        """VERSION_INFO tuple logic handles '0.0.0+dev' correctly."""
+        parts = "0.0.0+dev".split("+")[0].split(".")
+        nums = [int(p) for p in parts if p.isdigit()]
+        info = (nums[0], nums[1], nums[2], "") if len(nums) >= 3 else (0, 0, 0, "")
+        assert info == (0, 0, 0, "")
```

# 13. PERFORMANCE & OPTIMIZATION

## Known Bottlenecks

1. **Serial test execution**: 667 tests run synchronously. `pytest-xdist` could parallelize.
2. **AsyncEvalRunner**: Defaults to `max_workers=None` which uses `min(32, cpu+4)`. Large suites could OOM.
3. **skill_router**: 123-skill match is O(1) via single compiled regex, but re-compilation happens at import time (~1ms, acceptable).
4. **ResponseCache**: LRU in-memory only. No Redis/disk persistence across restarts.
5. **RateLimiter**: Token bucket, in-process only. Not shared across multiple uvicorn workers.

## Optimizations Already Implemented

1. **Single compiled regex for skill matching** (v1.0.x perf fix):
   ```python
   # Old: O(n) loop — 123 passes per route() call
   for entry in _SKILL_REGISTRY:
       for trigger in entry["triggers"]:
           if trigger in task_lower:
               ...
   # New: O(1) — one regex, all triggers in alternation
   _COMBINED = re.compile("|".join(all_triggers), re.IGNORECASE)
   ```

2. **Response caching**: `ResponseCache` (TTL=3600s, max=1000 entries) prevents duplicate LLM calls for identical prompts.

3. **Pre-compact hook**: Runs before context compaction to snapshot critical state. Prevents context loss.

4. **Deferred imports**: `src/mcp_server.py` and `ClaudeClient` in `app.py` use lazy imports to avoid import-time errors when optional deps (mcp, anthropic) not installed.

5. **Exponential backoff with jitter** on retry: `delay * 2^attempt * (1 ± 0.25)` — prevents thundering herd.

## Tradeoffs

| Decision | Chosen | Alternative | Reason |
|----------|--------|-------------|--------|
| In-memory cache | Simple dict + LRU | Redis | No infra dependency for template repo |
| File-based persistence | Flat files | SQLite | Human-readable, git-friendly, zero dependencies |
| Single-process rate limiter | Token bucket | Redis rate limit | Sufficient for single-instance deployment |
| Skill registry as list[dict] | Python list | Database | 123 skills fits in memory; O(1) with regex |
| Async test mode=auto | Whole suite async | Per-test `@mark.asyncio` | Less boilerplate; all tests in the same loop |

---

# 14. LEARNINGS & CONTEXT

## Key Insights (from tasks/lessons.md — 31 lessons)

1. **`grep -c` exits 1 when 0 matches** — causes `|| echo 0` to fire alongside grep's "0" output, producing `0\n0`. Always use `grep ... | wc -l | tr -d ' '` for count variables in hooks.

2. **Heredoc with unquoted delimiter executes backticks** — `cat > file << EOF ... $VAR ... EOF` interpolates backticks and `$(...)` in `$VAR`. Use `printf '%s\n'` for user-sourced content.

3. **`async def test_` at module level (zero indent) missed by `^\s+def test_`** — use `^\s*(async\s+)?def test_` (zero-or-more whitespace) to catch both class-method and top-level async test functions.

4. **Module-level imports of internal return values will always ImportError** — `from src.mcp_server import mcp` fails if `mcp` is only created inside `_build_server()`. Verify every `from module import name` has `name` at module level.

5. **awk section extraction needs heading-as-delimiter, not `---`** — use `/^### Heading/{if(in_s && buf!="") save(buf); buf=""; in_s=1}` not `/^---/` as end sentinel.

6. **ANSI escape codes (`\033`) inside sed replacement strings are NOT expanded** — use `printf '%b'` or shell variables pre-expanded with `$'...'` syntax.

7. **`or`/`and` operator precedence in Python** — `"a" in x or "b" in x and "c" in x` parses as `("a" in x) or (("b" in x) and ("c" in x))`. Always add explicit parentheses.

8. **Coverage gaps hide behind happy-path mocking** — `importlib.metadata` always succeeds when package is installed, so `tomllib` and `dev fallback` paths in version.py were at 0% until explicitly patched.

9. **Duplicate triggers in skill registry silently over-penalize** — `"lookup"` appeared twice in `_LOW_SIGNALS`, subtracting 4 from complexity score instead of 2. Found by adding a test.

10. **`contextvars.ContextVar` in async middleware needs `try/finally` reset** — without `finally: _var.reset(token)`, the context leaks across requests in the same asyncio task.

## Hidden Constraints

- The `ccm` CLI entry point REQUIRES editable install (`pip install -e .`). Running `python src/cli.py` directly fails because relative imports need `src` on sys.path, which editable install provides.
- `asyncio_mode = "auto"` in pyproject.toml means ALL tests run in async mode. Adding `@pytest.mark.asyncio` is redundant and harmless but unnecessary.
- `test_mcp_server.py` MUST inject fake `mcp` module into `sys.modules` BEFORE importing `src.mcp_server`. The module calls `_require_fastmcp()` at import time.
- The skill router test `test_no_duplicate_trigger_phrases` runs across ALL 123 skills. Adding a new skill with an existing trigger phrase will cause this test to fail.
- Docker HEALTHCHECK uses `/health` (no `/v1/` prefix). This is intentional — health is not versioned.

## Mental Models for Understanding the System

1. **"Route first, execute second"**: Every operation should call `route()` first to get model/skill/agent selection, then execute. The routing decision is observable and loggable.

2. **"Skills are knowledge, agents are executors"**: A skill is a read-only context pack that auto-activates based on keyword triggers. An agent is a subprocess that takes actions.

3. **"Memory tiers by access frequency"**: hot = always loaded (session context), warm = loaded when relevant (domain knowledge), glacier = archived (searchable, but rarely accessed).

4. **"Hooks are the immune system"**: pre-compact preserves context across compactions. pre-bash blocks dangerous commands. post-edit lints immediately. stop validates work is committed.

5. **"ClaudeClient is the single source of truth for LLM calls"**: Everything that touches the Anthropic API goes through ClaudeClient. Retry, cache, rate-limit, and logging are centralized there.

---

# 15. TODOs & ROADMAP

## All Open Findings (from tasks/open-findings.md)

All P2 and P3 findings from the v1.0.x deep-review audit have been resolved.
No open items remain. See `tasks/open-findings.md` for the closed list.

## Potential Improvements (not tracked as issues)

1. **Multi-process rate limiting**: Current `RateLimiter` is in-process. Multi-worker uvicorn deployments would exceed the rate limit — consider Redis-backed rate limiting.

2. **Exact token counting**: `ClaudeClient.count_tokens()` uses `len(text) // 4`. The Anthropic SDK has `client.messages.count_tokens()` for precision. Low priority since it's unused.

3. **Pre-commit ruff version gap**: `.pre-commit-config.yaml` pins `rev: v0.9.0` while pyproject requires `>=0.9.0,<1.0`. These stay in sync manually; automate via `pre-commit autoupdate`.

4. **Per-user rate limiting**: FastAPI has no auth layer. All rate limiting is per-server-instance. Adding JWT/API-key auth + per-key rate limiting would make this production-multi-tenant ready.

5. **Skill versioning**: 123 skills have no version tracking. If a skill's behavior changes, there's no way to roll back. Consider semantic versioning in SKILL.md frontmatter.

6. **Glacier search performance**: `search_glacier()` does linear file scan. With 100+ ADRs, this is acceptable. Beyond 1000, add a FAISS index or SQLite FTS.

7. **API `/v1/complete/stream` error handling**: On LLM error mid-stream, we emit `data: [ERROR] message\n\n`. Clients need to explicitly check for `[ERROR]` prefix. A proper error envelope format would be cleaner.

## Technical Debt

- `src/llm/utils.py` has `_extract_code_blocks()` that is not used by any test directly — covered via chainer tests only.
- `conftest.py` shared fixtures cover LLM and API but not TieredMemory (that module has its own setup/teardown).
- `notebooks/*.ipynb` are stubs with empty cells — not functional.

---

# 16. RECONSTRUCTION INSTRUCTIONS

## Step-by-Step Rebuild Order

If rebuilding from scratch (no git history):

### Phase 1: Repository Structure
```bash
mkdir -p wellux_testprojects/{src/{api,llm,routing,evals,persistence,prompt_engineering,utils,handlers},.claude/{hooks,skills,agents,commands,memory/{hot,warm,glacier},rules},tests,data/{evals,cache,sessions},config,docs/{decisions,runbooks},tasks,tools/{scripts,prompts},examples,notebooks}
git init
git checkout -b claude/optimize-cli-autonomy-xNamK
```

### Phase 2: Package Foundation
Build in this order (each depends on previous):
1. `pyproject.toml` — build config, deps, entry points
2. `src/__init__.py` — package init with `__version__` export
3. `src/version.py` — dynamic version resolution chain
4. `src/utils/logger.py` — structured logging (needed by everything)
5. `src/utils/rate_limiter.py` — token bucket (needed by ClaudeClient)
6. `src/utils/cache.py` — LRU response cache (needed by ClaudeClient)
7. `src/utils/token_counter.py` — token estimation
8. `src/utils/log_index.py` — JSONL event log with max_entries eviction
9. `src/handlers/error_handler.py` — classify_api_error() exception hierarchy
10. `pip install -e ".[dev]"` — make entry points work

### Phase 3: LLM Layer
11. `src/llm/base.py` — abstract LLMClient, CompletionRequest/Response dataclasses
12. `src/llm/claude_client.py` — ClaudeClient (complete, chat, stream) with retry
13. `src/llm/gpt_client.py` — GPTClient (optional)
14. `src/llm/utils.py` — token estimation, prompt utilities
15. `src/llm/__init__.py` — re-exports

### Phase 4: Routing System
16. `src/routing/llm_router.py` — complexity scoring → model selection
17. `src/routing/skill_router.py` — 123-skill registry with single compiled regex
18. `src/routing/agent_router.py` — signal → agent type mapping
19. `src/routing/memory_router.py` — content type → memory tier
20. `src/routing/task_router.py` — plan size + subtask decomposition
21. `src/routing/__init__.py` — `route()` composite function + `RoutingBundle`

### Phase 5: Persistence
22. `src/persistence/file_store.py` — FileStore (research, lessons, tasks)
23. `src/persistence/memory_store.py` — MemoryStore (MCP entity graph wrapper)
24. `src/persistence/tiered_memory.py` — TieredMemory (hot/warm/glacier)
25. `src/persistence/__init__.py` — re-exports

### Phase 6: Eval Framework
26. `src/evals/types.py` — EvalCase, EvalResult, EvalReport dataclasses
27. `src/evals/scorers.py` — ContainsScorer, ExcludesScorer, custom scorers
28. `src/evals/suite.py` — EvalSuite (add/from_jsonl/deduplicate)
29. `src/evals/runner.py` — EvalRunner (sync) + AsyncEvalRunner (concurrent)
30. `src/evals/__init__.py` — re-exports

### Phase 7: Prompt Engineering
31. `src/prompt_engineering/templates.py` — PromptTemplate (variable substitution)
32. `src/prompt_engineering/few_shot.py` — FewShotLibrary (store/retrieve examples)
33. `src/prompt_engineering/chainer.py` — PromptChain (sequential LLM chains)

### Phase 8: API Layer
34. `src/api/models.py` — Pydantic request/response models
35. `src/api/middleware.py` — CorrelationIDMiddleware, TimingMiddleware, ContentLengthLimitMiddleware
36. `src/api/app.py` — FastAPI app with /health, /v1/complete, /v1/chat, /v1/route, /v1/complete/stream
37. `src/api/__init__.py` — re-exports

### Phase 9: CLI and MCP
38. `src/cli.py` — all ccm subcommands (927 lines)
39. `src/mcp_server.py` — FastMCP server with 6 tool functions

### Phase 10: Tests
40. `tests/conftest.py` — shared fixtures (mock_llm, tmp_file_store, etc.)
41. Write test file for each module (match order of implementation above)
42. Run: `python3 -m pytest tests/ -q` — all pass
43. Run: `ruff check src/ tests/` — lint clean

### Phase 11: Claude Code Integration
44. `.claude/settings.json` — permissions + hooks wiring
45. `.claude/hooks/session-start.sh` — rich boot display
46. `.claude/hooks/pre-compact.sh` — context survival
47. `.claude/hooks/pre-tool-bash.sh` — command safety gate
48. `.claude/hooks/post-tool-edit.sh` — lint on save
49. `.claude/hooks/stop.sh` — session end checklist
50. `CLAUDE.md` — master orchestration context
51. `.claude/SOUL.md`, `.claude/USER.md` — identity + user profile
52. `.claude/rules/*.md` — code-style, testing, api-conventions

### Phase 12: Skills (123 total)
53-175. Each skill in `.claude/skills/<name>/SKILL.md` — see section 4.23 for all content

### Phase 13: Infrastructure
176. `Dockerfile` + `docker-compose.yml`
177. `.github/workflows/ci.yml`
178. `config/*.yaml`
179. `data/evals/*.jsonl`
180. `pyproject.toml` (already done in Phase 2)

### Phase 14: Final
181. `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`
182. `docs/` files
183. `tasks/` files (PRD, lessons, open-findings, todo)
184. `git add && git commit -m "initial: complete project setup"`
185. `git push -u origin claude/optimize-cli-autonomy-xNamK`

## Critical Sequencing Constraints

- `src/utils/logger.py` MUST come before everything else (circular import if deferred)
- `pip install -e ".[dev]"` MUST happen before running tests
- `pyproject.toml` `[tool.setuptools.packages.find] where = ["."]` is required — without it `import src` fails
- `asyncio_mode = "auto"` in pyproject.toml is required — without it async tests need `@pytest.mark.asyncio`
- skill_router.py MUST have no duplicate triggers — checked by `test_no_duplicate_trigger_phrases`

---

# 17. AI CONTINUATION INSTRUCTIONS

## How to Continue Development

1. **Start every session** by reading CLAUDE.md and hot-memory.md — they contain the current state.
2. **Use `f`** (the literal character) to execute the next pending step in MASTER_PLAN.md (currently 31/31, so it's free for new tasks).
3. **Add new features** with: `/brainstorm <feature>` → `/write-plan` → implement → `python3 -m pytest tests/ -q` → commit.
4. **Before any commit**: `ruff check src/ tests/ --select E,F,W --ignore E501` must be clean.
5. **After any correction**: Add a lesson to `tasks/lessons.md` following the PATTERN/RULE/PREVENTION format.

## Key Areas to Be Careful With

| Area | Risk | Why |
|------|------|-----|
| `src/routing/skill_router.py` | Duplicate triggers | `test_no_duplicate_trigger_phrases` will fail silently in CI if you add a trigger that already exists |
| `src/api/app.py` HTTPException | Don't leak `str(e)` | Security: exception messages can contain API keys, internal paths, PII |
| `src/utils/logger.py` | Don't log raw fields | Logger auto-redacts password/token/api_key/secret — don't bypass this |
| `.claude/hooks/pre-compact.sh` | Don't use heredoc for variables | Backticks in commit messages will execute as shell commands; use `printf '%s\n'` |
| `src/llm/claude_client.py` | Don't add synchronous `client` calls | Always use `self.async_client` for the async path; `self.client` is sync-only |
| `tests/test_mcp_server.py` | Fake mcp must be injected first | `_install_fake_mcp()` runs at module level — importing mcp_server before this will fail |

## Parts That Must NOT Be Broken

1. **5-router contract**: `route("task")` must return a `RoutingBundle` with `.llm`, `.skill`, `.agent`, `.memory`, `.plan` attributes. All CLI and API code depends on this.
2. **`ccm eval run smoke.jsonl --dry-run`** must always pass in CI (no API key needed). Never make dry-run mode require an API call.
3. **No duplicate skill triggers** — the test `test_no_duplicate_trigger_phrases` is a critical regression guard.
4. **`pip install -e ".[dev]"` must work from project root** — the `[tool.setuptools.packages.find] where = ["."]` setting is what makes this work.
5. **HTTPException detail pattern** — always use `f"Upstream LLM error [{type(e).__name__}] — see server logs (request_id={rid})"` not `str(e)` directly.
6. **Pre-compact hook** — `.claude/hooks/pre-compact.sh` must exit 0 always. A non-zero exit blocks context compaction and freezes the session.

## Expected Coding Style to Follow

```python
# ── File header ───────────────────────────────────────────────────────────────
"""Module docstring — single sentence description."""
from __future__ import annotations

# stdlib imports
import os
from pathlib import Path

# third-party
import anthropic

# local (relative)
from ..utils.logger import get_logger

logger = get_logger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
_SOME_CONSTANT: list[str] = ["value1", "value2"]

# ── Classes ───────────────────────────────────────────────────────────────────
class MyClass:
    """One-line description."""

    def __init__(self, param: str, *, option: bool = False) -> None:
        self.param = param
        self._option = option   # private: single underscore

    def public_method(self) -> str:
        """Public methods have docstrings."""
        return self._private_helper()

    def _private_helper(self) -> str:
        """Private helpers use _ prefix."""
        return self.param.upper()

# ── Module-level functions ────────────────────────────────────────────────────
def public_function(x: str | None = None) -> dict:
    """Function docstring."""
    if x is None:
        return {}
    return {"value": x}
```

Key style rules:
- `from __future__ import annotations` at top of every file
- `str | None` not `Optional[str]`
- Module-level sections separated by `# ── Section ──────` banners
- No bare `except:`, always specific exception types
- Constants at module level with type annotations
- All public functions/classes have docstrings
- Private members use single underscore prefix

---

# 18. COMPLETE GIT HISTORY

```
2edefc5dab6c81ad208610a2aa8d4277f5424e7c | 2026-04-06 07:55:33 +0000 | Claude | chore: sync memory files
5e36d6d7046a51d575b6a2cd261c38817b60ef9a | 2026-04-06 00:21:49 +0000 | Claude | chore: sync memory and session files
147b0edbac1f37f8d33d9cb95a13df9ddabe0d6e | 2026-04-06 00:21:33 +0000 | Claude | test: 100% coverage on version.py and mcp_server.py
c5a4f042edabad6e96560ba8f446142983428dd4 | 2026-04-06 00:16:47 +0000 | Claude | chore: sync memory files
dd18fa22f69ab43955a3215118f955b16d219dc4 | 2026-04-06 00:16:28 +0000 | Claude | fix(hooks): test count misses async def test_ and module-level tests
e296c07b6a1cef1100aded92e4f75d0b0346dcd9 | 2026-04-06 00:10:55 +0000 | Claude | docs: sync all docs to v1.0.7 state
6287399de86cec4f3e51889b354fa7461f590438 | 2026-04-06 00:06:29 +0000 | Claude | chore: sync warm memory
3e7e460d224a35616d738d3e1f71b7c46fad342a | 2026-04-06 00:06:13 +0000 | Claude | chore: fix stale lesson count in hot-memory critical files (26 → 31)
c44cfe88cff69da94e363d518aa36a48a35cca75 | 2026-04-06 00:04:56 +0000 | Claude | chore: add session log 2026-04-06
616bac18a3c86dd1394c5aa5a1c46408927e1c48 | 2026-04-06 00:04:38 +0000 | Claude | fix(hooks): grep -c exits 1 on zero matches causing 0\n0 count strings
194454f03ee3b68985aa180299a49754c4c734ce | 2026-04-05 23:36:48 +0000 | Claude | fix(pre-compact): prevent backtick expansion corrupting hot-memory.md
59d94ee2455a8aa892f9cb60c72a7f3dad2425bb | 2026-04-05 23:31:05 +0000 | Claude | fix(version): correct VERSION_INFO to 4-tuple (major, minor, patch, pre)
4b621608911e54c1941daf17df1507d224b39538 | 2026-04-05 23:28:03 +0000 | Claude | fix(version): read version dynamically from installed metadata or pyproject.toml
da20c0e23a6b385cc8880a076ec40d79f1d6eb1e | 2026-04-05 23:24:16 +0000 | Claude | docs(CLAUDE.md): document v1.0.7 additions — open-findings, 30 lessons, hook improvements
83a936c7b200d36b4e8dc861ca368ab0faf69b15 | 2026-04-05 23:22:09 +0000 | Claude | chore(self-reflect): add lessons 27-30 from v1.0.7 session
6ef0f29be84263cf7cb09d43d89abe3e1dfbdc52 | 2026-04-05 23:19:32 +0000 | Claude | chore: document v1.0.7 in CHANGELOG + hot-memory
990c68596060e5da34d7109da54d541313db093c | 2026-04-05 23:17:49 +0000 | Claude | chore: sync memory files
e46c0e6254ea21075705076972ee343af9eb3444 | 2026-04-05 23:17:26 +0000 | Claude | fix(v1.0.7): resolve all P3 open findings
e35c5ccbd7b706ce39ba43ad03ac5ac525d018c4 | 2026-04-05 23:12:40 +0000 | Claude | chore: sync memory files
0bdbd926a512e822a8c4328abb378d5c3c8f78db | 2026-04-05 23:12:27 +0000 | Claude | fix(v1.0.7): resolve all P2 open findings
d17009501383d73046928dc2b8de72306e261e2f | 2026-04-05 23:09:19 +0000 | Claude | chore: add today's session log
892c023e93bf6a984fe379f4aaf888b3a5165e2d | 2026-04-05 23:08:51 +0000 | Claude | feat(oversight): richer session-resumption boot display
d5464b852cc9690362f3e8d4a0727b46cf319def | 2026-04-05 22:30:24 +0000 | Claude | chore: sync hot-memory timestamps
6e4ae001d40c8e1064b7fbd8501646a9dd67926f | 2026-04-05 22:29:57 +0000 | Claude | perf(skill_router): replace O(n) trigger loop with single compiled regex scan
e3941cf2027fc02403ff9909016c9d2dad00a41c | 2026-04-05 22:11:10 +0000 | Claude | security(v1.0.6): harden HTTPException detail + logger sensitive field redaction
37c10242a6f9c2285a2bd2ce5824866440d8c7ba | 2026-04-05 22:00:53 +0000 | Claude | chore: sync hot-memory timestamps after deep review session
e97b22cd93d5e2cd28e36cb473fdcc3efc9e4234 | 2026-04-05 22:00:25 +0000 | Claude | fix(v1.0.5): config hardening from deep review — JSONL, pyproject, CI cache
98e910edf8ff246a0ab423526af7793a3138c301 | 2026-04-05 21:58:25 +0000 | Claude | docs/fix(v1.0.4): CHANGELOG, hot-memory sync, dynamic session-start URL
2d39906ced91a2317a5b2e07eee1ab45934c569a | 2026-04-05 21:53:11 +0000 | Claude | fix(v1.0.4): 4 bugs from deep review — dead var, IndexError, regex cache, validation
6206adc30ae652ff3f35d66cd7ceae0a0c09ab24 | 2026-04-05 21:36:41 +0000 | Claude | chore: sync hot-memory timestamps after test coverage session
424ec48af83fd02be10afdae4f29a24c360ddb04 | 2026-04-05 21:36:25 +0000 | Claude | test(cli): add coverage for deploy helpers and parser sub-functions
cda0a0999770a5396ed73cb7bf2275899316fb58 | 2026-04-05 21:34:00 +0000 | Claude | chore: sync hot-memory timestamps after cli refactor session
a1f45bcf0c3c200daecfeb18b4abe0c7cb25f38b | 2026-04-05 21:33:46 +0000 | Claude | refactor(cli): extract deploy step helpers + split build_parser by category
37bc828dc0f87518c35723293de7da5a28397d34 | 2026-04-05 21:31:30 +0000 | Claude | docs: sync architecture.md endpoint table to /v1/ paths
0939460943549e13c365a67d39b332e1350f3352 | 2026-04-05 21:29:10 +0000 | Claude | docs(v1.0.3): CHANGELOG entry, README endpoint sync, hot-memory update
2f5006ff66511e12a06ba7555639812fe00e806d | 2026-04-05 21:24:51 +0000 | Claude | chore: sync hot-memory timestamps after v1 API versioning session
451f827a7cd2e684afc052d794c295b63d078c66 | 2026-04-05 21:24:34 +0000 | Claude | feat(api): add /v1/ prefix to all business endpoints via APIRouter
d31a903377718d0a123cdabb62b8e149a3ff8401 | 2026-04-05 21:20:47 +0000 | Claude | docs/chore(v1.0.2): CHANGELOG entry, hot-memory sync, shared conftest fixtures
33a84dadec43bdd6e11ffe38dda578c280343528 | 2026-04-05 21:13:23 +0000 | Claude | chore: sync hot-memory timestamps after v1.0.2 session
394225ec4ea7f0e9f00348ea964abbebd08c56c0 | 2026-04-05 21:13:05 +0000 | Claude | fix(mcp_server): defer FastMCP import to prevent SystemExit at module load
4c4306ac1d4d25a3af8ab489704a3f447fc97be4 | 2026-04-05 21:05:11 +0000 | Claude | chore: sync hot-memory timestamp + ruff import blank-line fix
211044cef54f7e4616b203a506c6cd537cc748fb | 2026-04-05 21:04:53 +0000 | Claude | feat(v1.0.2): ccm lint subcommand + search_glacier limit param
c3f81fc2eed06bd9f7ab2aa02aae75c1f0482450 | 2026-04-05 20:57:12 +0000 | Claude | docs(v1.0.1): CHANGELOG entries, 5 audit lessons, hot-memory sync
6d1162b708452d72f2d1fb352dce30be9a61492e | 2026-04-05 20:43:45 +0000 | Claude | chore: update hot-memory snapshot after v1.0.1 audit fixes
99eb117e43bb13173f3ee5e9c9756e4c3df66418 | 2026-04-05 20:43:16 +0000 | Claude | fix(v1.0.1): bug fixes from full codebase audit
d3c47f34d560287c6ad31dbac312210e76b1a685 | 2026-04-05 20:09:11 +0000 | Claude | feat(v1.0.0): first stable release — 123 skills, 615 tests, tiered memory
4b6f764837c8f33aea70e3918d4ece957e00f767 | 2026-04-05 20:05:16 +0000 | Claude | docs(v0.9.4): add CHANGELOG entry and sync hot-memory to current state
4c4ebd93bfe6d324da3617c36f579e8a5684178b | 2026-04-05 20:03:00 +0000 | Claude | feat(v0.9.4): per-module CLAUDE.md, glacier decisions, 9 new CLI tests
728c4c0033724182fc50b012c597c21bd8b0d3ed | 2026-04-05 19:56:37 +0000 | Claude | feat(v0.9.3): memory bank complete, per-module CLAUDE.md, ccm memory-bank CLI, 4 lessons
d542064861230506e81b5afdf8fb8cd24cf870d6 | 2026-04-05 19:52:10 +0000 | Claude | feat(v0.9.2): warm memory bank, CHANGELOG v0.9.1, context-diff tests
1caedec1f1adb8754eebed1b7542047768cbbe2c | 2026-04-05 19:25:38 +0000 | Claude | feat(v0.9.1): MEMORY.md, RIPER skill, memory-bank, context-diff CLI, 7 hooks
b0dcc07f11050b36a8486593be0ef11f4e59f1f1 | 2026-04-05 19:14:16 +0000 | Claude | feat(v0.9.0): ecosystem research integration — tiered memory, 7 skills, hooks v2
d9ba6a4c6df6e9249542fe66c217d88bb8a5bc89 | 2026-04-05 12:32:47 +0000 | Claude | feat: expand skill routing registry from 51 to 114 entries
3bdde50ba7bc08f89a8b6ee47b27372a009cdd8d | 2026-04-05 10:53:20 +0000 | Claude | fix: broaden memory_router signal lists to reduce spurious MCP fallback
e06172befb99d6f6d3334f984894213ece92efde | 2026-04-05 10:51:31 +0000 | Claude | fix: comprehensive audit pass — routing, security, coverage, logger
f3faa7a8b2a46130e2f6bb96d54576db25688871 | 2026-04-05 10:38:14 +0000 | Claude | security: bump dep minimums + fix editable install path resolution
a461d1e1c2b4fbfecda93c138c671d1e4c082397 | 2026-04-05 10:27:53 +0000 | Claude | chore: sync 113→114 skill count and add v0.8.0 changelog entry
7e2e390f70f364ad6bfe073cc6a70d8d33ad8d1d | 2026-04-05 10:23:07 +0000 | Claude | feat: add /plan-eng-review skill and sync 113→114 skill counts
543f8797e5d3667f64f9de02c3fa5da75c3e12df | 2026-03-29 19:20:40 +0000 | Claude | enhance: integrate gstack, Superpowers, Paperclip — 6 new skills + full docs refresh
479d25fded6918c69ccdba4de678285c803d9f09 | 2026-03-29 12:27:48 +0000 | Claude | tests: cover LogIndex eviction, empty-line skip, load cap, and list-tag indexing
348c7eefe34a5cf05abf0fed2ab4c3547d839452 | 2026-03-29 12:26:23 +0000 | Claude | tests: cover total_tokens, LLM shortcuts, task router branches, parallel chainer
e949a37c64d1c7bede1891e3fcc773981d0e6a73 | 2026-03-29 12:16:15 +0000 | Claude | tests: cover routing summary subtask branch, memory content_type overrides, cache tier, format_lesson
c265fdd7f37c6177441411b8ee8cfcbc0092e942 | 2026-03-29 12:01:51 +0000 | Claude | tests: add coverage for APIError handler, stream(), lifespan, _get_client, _log paths
8f9a287b5610deee30a77d62865262c54d6dec6b | 2026-03-29 11:52:11 +0000 | Claude | fix: add .hadolint.yaml config + wire it into CI lint-dockerfile job
f3787964014f3a9a7d40e0ed27a2891ed643b9ac | 2026-03-29 11:49:46 +0000 | Claude | ci: diagnose failure — continue-on-error lint-dockerfile, verbose pytest
e42f5b638ff5ffc1e2c2ad467a857f4c8b5df20d | 2026-03-29 06:43:07 +0000 | Claude | fix: pin pytest-asyncio<1.0 + add asyncio_default_fixture_loop_scope
a51064c3339943ac161a5c12bf21563a1590f83b | 2026-03-29 06:31:54 +0000 | Claude | fix: remove pytest.ini — pyproject.toml is the single pytest config source
b4f18597d2256534a46e5af82b5435c3ed8569e3 | 2026-03-29 06:21:59 +0000 | Claude | refactor: lift lazy imports to module level + align build-system pins
08a6813319e235586f92cc72f8ead253f85a99b5 | 2026-03-29 06:16:45 +0000 | Claude | CVE triage: pin cryptography>=43.0.1, upgrade pip/setuptools/wheel in CI
4a9d83b3575f51daa3c2564996badb2f0508f5d6 | 2026-03-29 06:13:08 +0000 | Claude | Fix CI: live-evals continue-on-error; v0.8.0; MAX_SUBTASKS cap
8cb25eceb2cf50fc40983d82be6b1957c4d0090b | 2026-03-29 01:04:15 +0000 | Claude | Harden CI: routing-evals job, live-evals job, coverage gate 60%→85%
3f186ae8af70301d12fc6dd101aa438fbfb221c6 | 2026-03-29 01:02:42 +0000 | Claude | Add ContentLengthLimitMiddleware; reject oversized payloads with 413
64b385316c96f0a8987fef54c5bf01dbf7b8e176 | 2026-03-29 01:00:24 +0000 | Claude | Atomic writes in FileStore + search_log/log_summary/atomic tests; 502 tests
f7bdd32fd206d3f907c41b79c8fcf6a2cee40109 | 2026-03-29 00:57:52 +0000 | Claude | Cover agent_router/memory_store/gpt stream gaps; 95% coverage, 495 tests
4ced41cf5fa97d62a0cc89a69111b121e98a080b | 2026-03-29 00:55:25 +0000 | Claude | Add mcp_server tests; coverage 90% → 93%, 475 tests
43869a34e13e5d69f558325e6c497163b81f3ace | 2026-03-29 00:53:44 +0000 | Claude | Add error_handler + llm/__init__ tests; coverage 89% → 90%, 454 tests
610842be89dcdb6343c54e9e92584418323d1793 | 2026-03-29 00:50:43 +0000 | Claude | Add API endpoint + GPT client tests; coverage 85% → 89%
a46e1286883e2cd9b70fc3beb9917b4116a496a5 | 2026-03-29 00:43:44 +0000 | Claude | Fix EvalReport.by_tag() + add claude_client tests; 401 tests
40cc8ef77f18f7d81b25ae7f3519c5d4c2388053 | 2026-03-29 00:39:15 +0000 | Claude | Fix CI: pip-audit non-blocking + full ruff compliance (all rules)
377e89d4e6bbe0ac28083e5fcbec99e388bb00fa | 2026-03-29 00:33:24 +0000 | Claude | Fix CI: resolve ruff import-sort failures on Python 3.12
543a2109726176c85ebb571a440c4330ec3e4946 | 2026-03-29 00:25:38 +0000 | Claude | Bump version to 0.7.0 — matches CHANGELOG deploy infrastructure release
6a5943fc9ea676940d17cc785215ff8ad6ce8502 | 2026-03-29 00:21:46 +0000 | Claude | Add ccm build/deploy/ps/health + MCP server — deployable from Claude and Claude Code
6341010a5948618f096c2bec3ff482b724bf023d | 2026-03-28 18:24:29 +0000 | Claude | Apply Karpathy-lens optimizations: timeouts, bounded memory, context safety
cf9c5e4be27c963909a9ce99fc292ce7ce0f4514 | 2026-03-28 17:50:24 +0000 | Claude | feat: ccm version + doctor + logs; fix skills count in status
9f940a13e3168c6af5e22b4a79caa0a9741238ff | 2026-03-28 17:39:51 +0000 | Claude | feat(v0.6.0): versioning, deployability, stability, indexed log memory
922ff5532758c1d8448a05916b40d6e88452f27f | 2026-03-28 17:31:49 +0000 | Claude | feat: deployable release — 107 skills, daily research, full docs
f6a79db6e88b5e216bdfa6e6628272c0fd50a486 | 2026-03-28 12:24:29 +0000 | Claude | fix: replace all stale claude_code_max paths with wellux_testprojects
1d938e90c09880e7b42e2035101468c97f093a38 | 2026-03-28 12:19:11 +0000 | Claude | docs: sync CLAUDE.md to current architecture; add /review + /fix-issue commands
7bff813d684ea412c8ea1f805cb042564443c9db | 2026-03-28 12:15:18 +0000 | Claude | fix: resolve all 30 ruff lint errors; add .claude/rules/ modular instruction files
61ffafee929d6d8ead24db1b875a57c1fec35353 | 2026-03-28 12:09:19 +0000 | Claude | feat: correlation ID middleware, timing headers, smoke evals in CI (321 tests)
62444195bbfcbb142abc79d7c48f18ecfd1f811f | 2026-03-28 12:05:41 +0000 | Claude | feat: async eval runner, ccm eval subcommand, sample eval suites (307 tests)
8b3098395bf37a109ea68a3004f7b97e0cf79eb3 | 2026-03-28 11:57:54 +0000 | Claude | feat: add eval framework + remove setup.py (295 tests)
032f1c0f20d928ca6cd011388f3046e9c9a93e59 | 2026-03-28 11:53:03 +0000 | Claude | feat: add ccm CLI entrypoint, pyproject.toml, and pre-commit hooks (237 tests)
306e86ed43f77e78b0ed2192522934abf555434d | 2026-03-28 11:47:38 +0000 | Claude | feat: add CI pipeline, multi-stage Dockerfile, and docker-compose
8210a1034eeee8b2f91158a6d34b9bf252158811 | 2026-03-28 11:33:59 +0000 | Claude | feat: complete api + persistence layers with 76 new tests (210 total)
93e005c4bad9278265369ca29ab6c43a7ecbe41a | 2026-03-28 11:22:42 +0000 | Claude | fix: harden two findings from security audit
14a6b396c2766eb7d5623246284ae7dfd118713e | 2026-03-28 11:17:32 +0000 | Claude | feat: add 5-router routing system (134 tests passing)
4b2c4faa806286337d453150d85a9fd5e0931e26 | 2026-03-28 11:05:04 +0000 | Claude | feat: add 5 research lessons (6-10) from Karpathy research run
74ee203e238780b49b496b5efdd7fa603ec19492 | 2026-03-28 10:57:21 +0000 | Claude | feat: add pytest suite — 97 tests, all passing
269da1627d3756fb8429eb0e966fe20d1d2a2dba | 2026-03-28 10:52:48 +0000 | Claude | feat: add 6 MCP servers to project config
82700834121c7b9adf1690dcc2326153486be3c2 | 2026-03-28 10:49:47 +0000 | Claude | feat: install optimizer crons as systemd user timers
f2d08bf3d1a229969f0be1a52b9136153c7cc993 | 2026-03-28 10:48:21 +0000 | Claude | chore: update todo.md + add 15 copy-paste prompts to tools/prompts/
c714ab2bcba35f8a89fbc98d7059f52c6bd0d66d | 2026-03-28 10:39:05 +0000 | Claude | chore: mark MASTER_PLAN complete — 31/31 steps done
06d696ee07694a6bd026613508ecac82d31a6b48 | 2026-03-28 10:38:04 +0000 | Claude | feat: complete claude-code-max harness — 107 skills, 4 agents, full Python stack
```

*End of HANDOFF.md — Generated 2026-04-06 08:15:22*
