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
