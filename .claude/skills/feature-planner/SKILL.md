---
name: feature-planner
description: >
  Break down a feature request into implementable tasks with acceptance criteria.
  Invoke for: "plan this feature", "break this down", "implementation plan",
  "task breakdown", "feature spec", "how do I implement X", "what are the steps",
  "make a plan for", "I need to build".
argument-hint: feature description
allowed-tools: Read, Write, Grep, Glob
---

# Skill: Feature Planner — Implementation Breakdown
**Category:** Development

## Role
Transform a vague feature request into a concrete, ordered list of implementable tasks with acceptance criteria.

## When to invoke
- New feature to implement
- "how do I implement X"
- Sprint planning for a feature
- Before starting any non-trivial work

## Instructions
1. Clarify: what is the feature? Who uses it? What's the success criteria?
2. Identify all components affected (frontend, backend, DB, tests, docs)
3. Order tasks: dependencies first, parallel work identified
4. Write acceptance criteria for each task (testable conditions)
5. Estimate complexity: S/M/L for each task
6. Write to tasks/todo.md as checkable items

## Output format
```
## Feature Plan — <name> — <date>
### Goal
### Tasks (ordered)
- [ ] 1. [S] Create DB schema — AC: migration runs, table exists
- [ ] 2. [M] Write API endpoint — AC: POST /api/feature returns 201
- [ ] 3. [L] Add tests — AC: 80% coverage
### Dependencies
### Estimated Total: S/M/L
```

## Example
/feature-planner Add rate limiting to the Claude API client with Redis backend
