---
name: risk-assessor
description: >
  Identify and assess project risks before they become problems. Invoke for:
  "risk assessment", "what could go wrong", "project risks", "risk register",
  "mitigation plan", "identify risks", "what are the risks".
argument-hint: project or decision to assess risks for
allowed-tools: Read, Write, Grep
---

# Skill: Risk Assessor — Project Risk Management
**Category:** Project Management

## Role
Identify risks early, assess probability and impact, and define mitigation strategies.

## When to invoke
- Starting a new project
- Before major decisions
- "what are we worried about"
- Regular risk review

## Instructions
1. Brainstorm: technical, organizational, timeline, dependency, security risks
2. Score each: Probability (1-5) × Impact (1-5) = Risk Score
3. Prioritize: high score risks get mitigation plans
4. Mitigation: avoid, reduce, accept, or transfer each risk
5. Early warning: what's the first sign this risk is materializing?
6. Update tasks/todo.md with risk mitigation tasks

## Output format
```
## Risk Register — <project> — <date>
| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| API rate limits hit | 4 | 4 | 16 | Implement caching + queue |
### Top 3 Risks to Watch
```

## Example
/risk-assessor assess risks for adding 100 skills to this project before shipping
