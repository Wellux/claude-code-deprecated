---
name: mem
description: >
  Persist important context, decisions, and facts to memory files so Claude remembers
  across sessions. Invoke for: "remember this", "save this for later", "persist this",
  "don't forget", "add to memory", "mem", "save to memory", "note this down".
  Inspired by Claude Mem (thedotmack) persistent memory pattern.
argument-hint: fact, decision, or context to persist
allowed-tools: Read, Write, Edit
---

# Skill: Mem — Persistent Memory Across Sessions
**Category:** Ecosystem
**Inspired by:** Claude Mem (github.com/thedotmack)

## Role
Persist important context to files so it survives session boundaries and gets loaded by session-start.sh.

## When to invoke
- "remember this for next session"
- Important decision made that affects future work
- Project context that Claude should always know
- "add this to memory"

## Memory Locations
| Type | File | Loaded By |
|------|------|-----------|
| Project lessons | tasks/lessons.md | session-start.sh |
| Session tasks | tasks/todo.md | session-start.sh |
| Architecture decisions | docs/decisions/ | manual |
| User preferences | ~/.claude/CLAUDE.md | all sessions |

## Instructions
1. Identify what to remember and where it belongs
2. For lessons: append to tasks/lessons.md with DATE | PATTERN | RULE
3. For tasks: append to tasks/todo.md
4. For decisions: create ADR in docs/decisions/
5. For global preferences: append to ~/.claude/CLAUDE.md
6. Confirm: "Saved to [file]"

## Output format
```
✅ Saved to tasks/lessons.md:
2026-03-28 | Use YAML frontmatter in SKILL.md | Always include name: and description: fields
```

## Example
/mem remember: always use asyncio.gather for parallel LLM calls, not sequential await
