---
name: tech-debt
description: >
  Identify and systematically reduce technical debt. Invoke for: "tech debt",
  "clean up legacy code", "TODO cleanup", "code smells", "dead code", "deprecated",
  "legacy patterns", "maintenance burden", "cruft", "what's the worst code we have".
argument-hint: codebase area or specific debt category to address
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Tech Debt — Identify & Prioritize Cleanup
**Category:** Development

## Role
Audit the codebase for technical debt, prioritize by impact vs effort, and systematically eliminate it.

## When to invoke
- Dedicated refactoring sprint
- "what are our biggest code problems"
- Before adding new features to a messy area
- Post-project cleanup

## Instructions
1. Scan for TODOs, FIXMEs, HACKs, deprecated warnings
2. Identify: dead code, duplicate code, overly complex functions (> 50 lines), missing tests
3. Find: hardcoded values, magic numbers, outdated dependencies
4. Score each item: Impact (1-5) × Effort to fix (1-5 inverted) = Priority
5. Create prioritized list in tasks/todo.md
6. Fix highest-priority items first

## Output format
```
## Tech Debt Audit — <scope> — <date>
### Priority Matrix
| Item | Impact | Effort | Priority |
### Quick Wins (high impact, low effort)
### Big Rocks (high impact, high effort)
### Ignore (low impact)
```

## Example
/tech-debt full codebase — find all TODOs and dead code
