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
