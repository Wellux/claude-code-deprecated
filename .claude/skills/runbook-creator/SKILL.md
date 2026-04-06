---
name: runbook-creator
description: >
  Create operational runbooks for repeatable procedures. Invoke for: "write runbook",
  "document this procedure", "ops runbook", "how to deploy", "incident runbook",
  "step-by-step ops guide", "operational documentation".
argument-hint: procedure or operation to document
allowed-tools: Read, Write, Glob
---

# Skill: Runbook Creator — Operational Procedures
**Category:** Documentation

## Role
Write clear runbooks that any engineer can follow without prior knowledge of the system.

## When to invoke
- New operational procedure needs documentation
- Alert triggered with no runbook
- Onboarding new ops engineers
- After every incident (document what was done)

## Instructions
1. Assume reader has no context — start from zero
2. Prerequisites: what access, tools, knowledge needed?
3. Steps: numbered, one action per step, exact commands with expected output
4. Decision points: if X then Y, else Z
5. Verification: how to confirm each step worked
6. Rollback: how to undo if step fails
7. Escalation: who to call if stuck

## Output format
```markdown
# Runbook: <procedure name>
**Last Updated:** | **Owner:**

## When to use this runbook
## Prerequisites
## Steps
1. [Action] — expected output: `...`
## Verification
## Rollback
## Escalation
```

## Example
/runbook-creator write deployment runbook for the Python AI service
