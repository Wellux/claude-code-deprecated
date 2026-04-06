---
name: sre
description: >
  Site Reliability Engineering: SLOs, error budgets, toil reduction, reliability design.
  Invoke for: "SRE review", "reliability", "SLO", "error budget", "toil", "on-call",
  "uptime", "reduce incidents", "reliability engineering", "post-mortem".
argument-hint: service or reliability concern to address
allowed-tools: Read, Write, WebSearch
---

# Skill: SRE — Site Reliability Engineering
**Category:** DevOps/Infra

## Role
Apply SRE principles to improve system reliability: define SLOs, track error budgets, reduce toil, and run blameless post-mortems.

## When to invoke
- "we keep having incidents"
- Define SLOs for a service
- Post-mortem after outage
- "reduce on-call burden"

## Instructions
1. Define SLIs: what measurable signals represent user happiness?
2. Set SLOs: realistic targets (99.9% ≠ always right, depends on user need)
3. Track error budget: how much budget remains? Burning fast?
4. Identify toil: manual, repetitive operational work → automate it
5. Post-mortem: blameless, focus on system/process not people
6. Runbook: for every alert, there must be a runbook

## Output format
```
## SRE Assessment — <service>
### SLIs & SLOs
| SLI | SLO | Current |
### Error Budget: X% remaining
### Toil Identified
### Post-Mortem (if applicable)
### Recommendations
```

## Example
/sre define SLOs for the Claude API client — set error budget and alert thresholds
