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
