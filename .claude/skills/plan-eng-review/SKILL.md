---
name: plan-eng-review
description: >
  Staff engineer review of the technical approach before implementation begins.
  Invoke for: "eng review", "technical review", "review my approach", "sanity check the design",
  "is this the right way to build it", "plan review", "pre-implementation review",
  "check my plan", "technical sanity check", "staff review".
  Inspired by gstack (Garry Tan) /plan-eng-review.
argument-hint: technical approach or plan to review
allowed-tools: Read, Grep, Glob
---

# Skill: Plan Eng Review — Technical Approach Review
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack)

## Role
Act as a staff engineer doing a pre-implementation design review. Not a code review — this
happens *before* code is written. Goal: catch fundamental approach problems early, when they're
cheap to fix, not after hours of implementation.

## When to Invoke
- After `/brainstorm` and `/write-plan` — before starting implementation
- When your technical approach touches shared infrastructure
- When there are multiple viable architectures and you need a second opinion
- Before large migrations, schema changes, or breaking API changes
- Any time "I'm not sure this is the right way" crosses your mind

## Review Lenses

### 1. Correctness — Will it actually work?
- Does the approach correctly solve the stated problem?
- Are there logical flaws in the design?
- Does it handle the known edge cases from the brainstorm?
- Are the data types and contracts correct?

### 2. Fit — Does it belong here?
- Does this fit the existing architecture and patterns?
- Are you solving this at the right layer? (Don't put business logic in middleware)
- Does this create unexpected coupling between modules?
- Would a reader familiar with the codebase find this natural?

### 3. Complexity — Is this the simplest correct solution?
- Is there a simpler approach that achieves the same result?
- Are you over-engineering for hypothetical requirements?
- Does this introduce concepts that aren't needed yet?
- Would you be happy maintaining this in 6 months?

### 4. Safety — What could go wrong?
- What happens if an external dependency fails?
- Are there race conditions or concurrency hazards?
- Is the blast radius of a bug acceptably small?
- Is there a way to roll this back if it causes issues?

### 5. Performance — Will it be fast enough?
- What's the time complexity of the hot path?
- Are there N+1 query patterns or repeated work?
- Is caching needed? Is it already present?
- Will this be a bottleneck at 10x current load?

### 6. Security — Is it safe?
- Does this expose new attack surfaces?
- Is user input properly validated and escaped?
- Are there authorization checks at the right level?
- Does this handle secrets or credentials safely?

## Output Format

```
## Eng Review: <approach/feature>

### Verdict
APPROVED | APPROVED WITH NOTES | NEEDS REVISION | BLOCKED

### Strengths
- [what's well-designed]

### Issues
| Severity | Issue | Recommendation |
|----------|-------|----------------|
| CRITICAL | [issue] | [fix required before proceeding] |
| MAJOR    | [issue] | [fix before merge] |
| MINOR    | [issue] | [fix in follow-up] |

### Suggested Changes
[specific changes to the plan, if any]

### Proceed?
[yes / yes with notes / no — reason]
```

## Severity Definitions
- **CRITICAL** — approach is fundamentally broken; do not proceed
- **MAJOR** — significant issue that will cause bugs or maintenance pain; fix before merge
- **MINOR** — suboptimal but workable; address in a follow-up

## Example
/plan-eng-review adding a sliding-window rate limiter using Redis sorted sets

## Related Skills
- `/brainstorm` — requirements phase (run first)
- `/write-plan` — task decomposition (run after approval)
- `/superpowers` — execution (run after plan is approved)
- `/code-review` — review after implementation (different from this)
