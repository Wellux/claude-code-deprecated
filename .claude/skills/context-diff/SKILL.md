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
