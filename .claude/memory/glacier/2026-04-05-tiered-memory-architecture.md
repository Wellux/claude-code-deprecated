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

