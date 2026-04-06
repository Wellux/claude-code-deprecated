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
