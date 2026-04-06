---
name: retrospective
description: >
  Run a sprint or project retrospective to capture learnings. Invoke for: "retrospective",
  "retro", "what went well", "what could be better", "lessons learned",
  "sprint review", "team retrospective".
argument-hint: sprint or project to retrospect on
allowed-tools: Read, Write
---

# Skill: Retrospective — Sprint & Project Review
**Category:** Project Management

## Role
Run a structured retrospective to capture what worked, what didn't, and concrete improvements.

## When to invoke
- End of sprint
- End of project
- After an incident
- "let's do a retro"

## Instructions
1. Read: tasks/todo.md, tasks/lessons.md, git log for the period
2. What went well? (keep doing)
3. What could be better? (specific, not vague)
4. What to try next? (concrete, actionable)
5. Action items: owner + deadline
6. Append key lessons to tasks/lessons.md

## Output format
```
## Retrospective — <sprint/project> — <date>
### What Went Well ✅
-
### What Could Be Better ⚠️
-
### What to Try Next 🧪
-
### Action Items
| Action | Owner | Done By |
### Lessons Added to tasks/lessons.md
```

## Example
/retrospective run retro for Phase 1 and Phase 2 of wellux_testprojects build
