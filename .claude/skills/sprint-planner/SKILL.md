---
name: sprint-planner
description: >
  Plan sprint tasks and prioritize backlog. Invoke for: "plan the sprint", "sprint planning",
  "prioritize backlog", "what should we work on", "sprint goals", "task prioritization",
  "what's the next sprint".
argument-hint: backlog or goals to plan a sprint around
allowed-tools: Read, Write, Grep
---

# Skill: Sprint Planner — Agile Sprint Planning
**Category:** Project Management

## Role
Run sprint planning: prioritize backlog, assign story points, define sprint goal, create tasks/todo.md entries.

## When to invoke
- Sprint kickoff
- "plan our next sprint"
- Backlog refinement
- "what should we focus on"

## Instructions
1. Read current tasks/todo.md and MASTER_PLAN.md
2. Identify: what's highest value + lowest risk for next sprint?
3. Estimate complexity: S (1-2h) / M (half day) / L (full day) / XL (needs breakdown)
4. Define sprint goal: one clear sentence of what "done" looks like
5. Select tasks fitting 2-week sprint capacity
6. Write sprint plan to tasks/todo.md

## Output format
```
## Sprint Plan — Week of <date>
### Sprint Goal
### Tasks (ordered by priority)
- [ ] [S] Task name — AC: ...
- [ ] [M] Task name — AC: ...
### Capacity: XL/sprint
### Risks
```

## Example
/sprint-planner plan 2-week sprint from current MASTER_PLAN backlog
