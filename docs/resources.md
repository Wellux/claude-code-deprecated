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
