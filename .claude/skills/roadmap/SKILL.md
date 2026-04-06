---
name: roadmap
description: >
  Build or update a product/technical roadmap. Invoke for: "roadmap", "build roadmap",
  "what's the plan", "long-term plan", "6-month roadmap", "product roadmap",
  "technical roadmap", "what comes after this".
argument-hint: project and timeframe for the roadmap
allowed-tools: Read, Write, Grep
---

# Skill: Roadmap — Product & Technical Planning
**Category:** Project Management

## Role
Create clear roadmaps that align stakeholders and set realistic expectations.

## When to invoke
- Starting a new project
- "what are we building over the next 6 months"
- Stakeholder communication
- Quarterly planning

## Instructions
1. Read MASTER_PLAN.md, tasks/PRD.md, tasks/todo.md for current state
2. Define: themes (not features) for each quarter
3. Now / Next / Later framework for prioritization
4. Dependencies: what must happen before what?
5. Include confidence levels: committed / likely / exploring
6. Write to docs/ROADMAP.md

## Output format
```
## Roadmap — <project>
### Now (current quarter)
- [committed] Feature A
### Next (next quarter)
- [likely] Feature B
### Later (3-6 months)
- [exploring] Feature C
### Milestones
| Milestone | Target Date | Status |
```

## Example
/roadmap build 6-month roadmap for wellux_testprojects template evolution
