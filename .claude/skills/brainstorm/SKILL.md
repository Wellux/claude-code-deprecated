---
name: brainstorm
description: >
  Socratic requirements refinement before writing any code. Surfaces assumptions, edge cases,
  tradeoffs, and hidden complexity through structured questioning.
  Invoke for: "brainstorm", "think through this", "what am I missing", "requirements unclear",
  "explore the design space", "what are the edge cases", "help me think through",
  "refine requirements", "what questions should I ask first".
  Inspired by Superpowers (obra/superpowers) /brainstorm phase.
argument-hint: feature or problem to brainstorm
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Brainstorm — Socratic Requirements Refinement
**Category:** Ecosystem
**Inspired by:** Superpowers (github.com/obra/superpowers)

## Role
Act as a Socratic engineering mentor. Ask the right questions before a line of code is written.
Surface hidden complexity, competing requirements, and unstated assumptions.

## When to Invoke
- Requirements feel vague or incomplete
- Multiple implementation approaches exist
- The feature touches sensitive systems (auth, data, payments)
- You're unsure what "done" looks like
- Before running `/write-plan` on a non-trivial feature

## Process

### Phase 1 — Understand the Problem
Ask 3-5 of these depending on what's missing:
- What problem does this solve for the user? (Not the feature — the problem)
- Who exactly is the user? What are they trying to do?
- What does success look like? How will we measure it?
- What currently happens without this feature?
- Are there existing solutions we're replacing or competing with?

### Phase 2 — Scope and Boundaries
- What is explicitly OUT of scope for this version?
- What's the smallest version that proves the concept?
- What must work on day 1 vs. what can be deferred?
- Are there hard constraints? (Performance, latency, cost, legal)

### Phase 3 — Technical Exploration
- What are the 2-3 main implementation approaches?
- What are the tradeoffs between them?
- Which parts of the system are touched?
- What could go wrong? What are the failure modes?
- How is this tested? (Unit, integration, e2e, eval?)

### Phase 4 — Edge Cases and Risks
- What happens when the input is empty / null / malformed?
- What happens at scale? (10x, 100x current load)
- What's the rollback plan if this causes issues in production?
- Are there security implications? (Auth, data exposure, injection)
- Are there race conditions or concurrency concerns?

### Phase 5 — Decision Points
List the open questions that need answers before coding starts:
1. [Question] → [who decides / how to decide]
2. ...

## Output Format

```
## Brainstorm: <feature>

### Problem Statement
[One paragraph: what problem, for whom, why it matters]

### Scope
In scope: [list]
Out of scope: [list]
MVP: [smallest shippable version]

### Approaches
1. [Approach A] — pros/cons
2. [Approach B] — pros/cons
Recommended: [choice + rationale]

### Edge Cases
- [case] → [how to handle]

### Risks
- [risk] → [mitigation]

### Open Questions
- [question] → [who decides]

### Ready to Plan?
[yes/no + what's needed to proceed]
```

## Next Step
After brainstorm is complete → run `/write-plan <feature>` to decompose into atomic tasks.

## Example
/brainstorm add rate limiting to the LLM client — we're seeing cost spikes
