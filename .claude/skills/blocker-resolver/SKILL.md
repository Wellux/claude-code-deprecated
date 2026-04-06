---
name: blocker-resolver
description: >
  Identify and resolve project blockers autonomously. Invoke for: "I'm blocked",
  "this is blocking me", "unblock this", "resolve blocker", "stuck on X",
  "how do I get past this", "blocker". Autonomously diagnoses and resolves blockers
  without waiting for user hand-holding.
argument-hint: description of what's blocking progress
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
---

# Skill: Blocker Resolver — Unblock Progress Fast
**Category:** Project Management

## Role
Diagnose and resolve blockers autonomously — don't wait, just fix it.

## When to invoke
- "I'm blocked by X"
- Something is preventing next MASTER_PLAN step
- Dependency not available
- Permission or access issue

## Instructions
1. Understand: what exactly is blocking? The symptom vs root cause?
2. Categorize: technical (code/config), dependency (waiting on something), access (permissions), knowledge (need more info)
3. Technical: debug and fix
4. Dependency: find alternative approach that doesn't require the dependency
5. Access: document exactly what access is needed and from whom
6. Knowledge: WebSearch to find the answer
7. Update tasks/todo.md: mark blocker, note resolution

## Output format
```
## Blocker Report — <date>
### Blocker: <description>
### Category: technical / dependency / access / knowledge
### Root Cause
### Resolution
### Status: RESOLVED / WORKAROUND / ESCALATE TO USER
```

## Example
/blocker-resolver I can't run the Python examples because the anthropic package isn't installed
