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
