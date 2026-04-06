---
name: estimation
description: >
  Estimate effort and timelines for software tasks. Invoke for: "estimate this",
  "how long will this take", "story points", "effort estimation", "timeline",
  "when can this be done", "how complex is this".
argument-hint: task or project to estimate
allowed-tools: Read, Glob, Grep
---

# Skill: Estimation — Effort & Timeline Estimation
**Category:** Project Management

## Role
Provide realistic effort estimates using historical context, complexity analysis, and uncertainty buffers.

## When to invoke
- Planning work
- "how long will this take"
- Stakeholder timeline questions
- Sprint capacity planning

## Instructions
1. Read the task description and related code
2. Break into sub-tasks if complex
3. Estimate each: S (< 2h), M (half day), L (full day), XL (needs breakdown)
4. Add uncertainty buffer: 1.5x for new technology, 2x for unclear requirements
5. Identify: what could make this take longer? (unknowns)
6. Give range, not single estimate: "2-4 days, most likely 3"

## Output format
```
## Estimation — <task> — <date>
### Sub-tasks
| Task | Complexity | Estimate |
| Design API | M | 4h |
| Implement | L | 1d |
| Tests | M | 4h |
### Total: 2 days (best) — 3 days (likely) — 5 days (worst)
### Key Risks That Could Extend
```

## Example
/estimation estimate effort to add the Python LLM stack to this project
