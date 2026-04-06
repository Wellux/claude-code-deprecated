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

