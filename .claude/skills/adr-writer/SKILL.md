---
name: adr-writer
description: >
  Write Architecture Decision Records (ADRs) to document significant technical decisions.
  Invoke for: "write ADR", "document this decision", "architecture decision record",
  "why did we choose X", "decision log", "record this choice", "ADR for".
argument-hint: decision to document (e.g. "use PostgreSQL instead of MongoDB")
allowed-tools: Read, Write
---

# Skill: ADR Writer — Architecture Decision Records
**Category:** Documentation

## Role
Create structured ADRs that capture context, decision, and consequences so future team members understand why choices were made.

## When to invoke
- Significant technology or design decision made
- "document why we chose X"
- Team disagreement resolved
- Before making major architectural change

## Instructions
1. Title: "ADR-NNNN: <decision in present tense>"
2. Status: Proposed / Accepted / Deprecated / Superseded
3. Context: what is the situation forcing this decision?
4. Decision: what was decided? Be specific
5. Consequences: positive and negative outcomes, trade-offs accepted
6. Save to: docs/decisions/NNNN-<title>.md

## Output format
```markdown
# ADR-NNNN: <Title>
**Status:** Accepted | **Date:** YYYY-MM-DD

## Context
## Decision
## Consequences
### Positive
### Negative
### Risks
```

## Example
/adr-writer document decision to use claude-sonnet-4-6 as default model over GPT-4
