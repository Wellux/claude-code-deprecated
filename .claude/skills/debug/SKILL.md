---
name: debug
description: >
  Systematic debugging: read error, trace root cause, fix autonomously. Invoke for:
  "this is broken", "debug this", "why is this failing", "error", "exception",
  "traceback", "not working", "fix this bug", "something's wrong", "it crashes".
  Never asks for hand-holding — reads logs, traces stack, identifies root cause, fixes.
argument-hint: error message, file path, or description of what's failing
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Debug — Root Cause Analysis & Fix
**Category:** Development

## Role
Autonomously debug failures: trace the error to its root cause and fix it without requiring user hand-holding.

## When to invoke
- Any error, exception, or crash
- "this doesn't work" / "it's broken"
- Failing tests
- Unexpected behavior

## Instructions
1. Read the error message / traceback fully
2. Identify the file:line where the error originates
3. Read that code and all code in the call stack
4. Hypothesize: what value/state caused this? Why?
5. Trace backwards: where does that value come from?
6. Identify root cause (not just the symptom)
7. Fix the root cause, not a workaround
8. Verify: will this fix prevent recurrence?

## Output format
```
## Debug Report — <error type> — <date>
### Error
### Root Cause (file:line)
### Why it happened
### Fix Applied
### Prevention
```

## Example
/debug TypeError: 'NoneType' object is not subscriptable in src/api/auth.py:89
