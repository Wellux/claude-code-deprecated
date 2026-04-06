---
name: office-hours
description: >
  Strategic multi-persona review before building. Summons CEO, CTO, PM, and Designer to debate
  the approach, surface risks, and align on what to build before any code is written.
  Invoke for: "office hours", "review this approach", "should we build this", "get alignment",
  "strategic review", "product review", "debate the design", "pre-build review",
  "is this the right thing to build". Inspired by gstack (Garry Tan).
argument-hint: feature or decision to review in office hours
allowed-tools: Read, Glob, Grep, WebSearch
---

# Skill: Office Hours — Strategic Pre-Build Review
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack)

## Role
Convene a virtual engineering leadership team. Each persona evaluates the proposed work from their
lens, surfaces concerns, and drives toward an aligned decision before implementation begins.

## When to Invoke
- Before starting a significant new feature
- When requirements feel ambiguous or conflicting
- When the technical approach has meaningful alternatives
- When there's product / engineering tension to resolve
- Any time "should we even build this?" is a real question

## Personas

### CEO — Strategic Value
*"Does this move the needle? Is this the right bet?"*
- Evaluates: business impact, opportunity cost, strategic alignment
- Asks: What's the user value? What's the risk of not doing this? What are we not doing instead?
- Blocks: work with no clear user outcome or that conflicts with strategic direction

### CTO — Technical Leadership
*"Is this the right architecture? Will it scale? Can we maintain it?"*
- Evaluates: technical approach, architecture fit, debt introduced, complexity
- Asks: Does this fit our existing stack? What's the 6-month maintenance burden?
- Blocks: approaches that create brittle systems or unnecessary complexity

### PM — User & Delivery
*"Does this solve the right problem? Can we ship it? Will users care?"*
- Evaluates: user need validation, scope, acceptance criteria, delivery risk
- Asks: How do we know users want this? What's the MVP? How do we measure success?
- Blocks: work without clear success metrics or over-engineered MVPs

### Designer — Craft & Experience
*"Is this usable? Is it coherent? Does it feel right?"*
- Evaluates: UX consistency, edge cases, error states, cognitive load
- Asks: What happens when it fails? Is the mental model clear? Does this fit the product?
- Blocks: technically correct solutions that create confusing user experiences

## Process

1. **Read the room** — review `CLAUDE.md`, recent `tasks/todo.md`, and any relevant source files
2. **CEO speaks first** — strategic framing and go/no-go signal
3. **CTO responds** — technical feasibility and architecture risks
4. **PM grounds** — scope, criteria, delivery plan
5. **Designer closes** — UX and edge cases
6. **Synthesis** — summarize: what to build, what NOT to build, open questions, first task

## Output Format

```
## Office Hours: <feature name>

### CEO
[strategic assessment + go/no-go]

### CTO
[technical assessment + architecture notes]

### PM
[scope + acceptance criteria + success metric]

### Designer
[UX considerations + edge cases]

### Decision
- Build: [what]
- Skip: [what and why]
- Open questions: [list]
- First task: [concrete next action]
```

## Example
/office-hours add streaming support to the /complete API endpoint
