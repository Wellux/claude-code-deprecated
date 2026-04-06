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
