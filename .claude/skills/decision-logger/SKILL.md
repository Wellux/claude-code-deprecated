---
name: decision-logger
description: >
  Log and track technical and product decisions with rationale. Invoke for:
  "log this decision", "record why we chose X", "decision log", "we decided to",
  "document this choice", "capture this decision". Proactively suggest logging
  any significant technical choice made during a conversation.
argument-hint: decision to log and context
allowed-tools: Read, Write, Glob
---

# Skill: Decision Logger — Decision Record Keeping
**Category:** Documentation

## Role
Capture decisions with context and rationale so future team members understand the "why."

## When to invoke
- Any significant technical or product decision made
- "why did we do it this way" questions arise
- Proactively after any architectural discussion
- Choosing between two approaches

## Instructions
1. Identify: what was decided? What were the alternatives?
2. Capture context: what problem was being solved?
3. Record rationale: why this option over others?
4. Note trade-offs: what was sacrificed?
5. Determine format: ADR (significant) or simple log entry (minor)
6. Save: docs/decisions/ (ADR) or append to tasks/lessons.md (minor)

## Output format
For significant decisions → full ADR (see /adr-writer)
For minor decisions:
```
Decision Log — <date>
Decision: Use YAML for config files, not JSON
Context: Need comments in config, JSON doesn't support them
Rationale: YAML readable, supports comments, widely used for config
Trade-off: Slightly more complex parsing, indentation-sensitive
```

## Example
/decision-logger log decision to use Redis for caching instead of in-memory dict
