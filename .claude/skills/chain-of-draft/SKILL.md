---
name: chain-of-draft
description: >
  Chain-of-draft structured prompting: iteratively refine a draft through multiple
  focused critique-and-improve cycles. Invoke for: "chain of draft", "iterative refinement",
  "improve this through drafts", "draft and critique", "structured refinement",
  "progressive draft improvement", "multi-pass writing", "draft → critique → improve".
  Uses minimal token efficient drafts (CoD pattern from Xu et al. 2025).
argument-hint: text, code, plan, or content to refine through drafts
allowed-tools: Read, Write, Edit
---

# Skill: Chain-of-Draft — Iterative Structured Refinement

## Role
Apply the Chain-of-Draft (CoD) pattern: produce minimal intermediate drafts with just
enough reasoning to guide the next iteration. More token-efficient than chain-of-thought
while preserving multi-step reasoning quality.

## Theory
CoD (Xu et al. 2025) produces short, sequential drafts instead of verbose reasoning chains.
Each draft captures only the key decision made at that step. Final output quality matches
full chain-of-thought at ~20% of the token cost.

## Workflow

### For writing tasks (plans, docs, prompts, emails):

**Draft 0 — Skeleton** (bullet points only, no prose)
- Core structure only
- Key claims or arguments
- No elaboration

**Draft 1 — Expand**  
- Fill the skeleton with 1-2 sentence explanations
- Note anything that doesn't fit or contradicts

**Draft 2 — Critique**
- What's weak, missing, or overclaimed?
- What would a skeptic object to?
- Write only the objections, not fixes

**Draft 3 — Strengthen**
- Address every critique from Draft 2
- Cut anything that didn't survive critique
- Final prose

### For code tasks:

**Draft 0 — Signature + types** (function stubs only)
**Draft 1 — Happy path** (core logic, no error handling)
**Draft 2 — Critique** (edge cases, type errors, security issues)
**Draft 3 — Production-ready** (handles all critique, clean types)
**Draft 4 — Tests** (tests derived from Draft 2 critique)

### For plans/architecture:

**Draft 0 — Components list**
**Draft 1 — Interactions + data flow**
**Draft 2 — Failure modes + constraints**
**Draft 3 — Final design with mitigations**

## Instructions

1. Identify content type (writing / code / plan)
2. Run the appropriate draft sequence
3. Show each draft labeled clearly
4. At each transition: state what changed and why in ≤1 sentence
5. Final output is Draft N — clearly marked

## Output Format

```
## Chain of Draft: <task>

### Draft 0 — Skeleton
<minimal structure>
---
*→ Next: expand with substance*

### Draft 1 — Expand
<substantive draft>
---
*→ Next: critique for weaknesses*

### Draft 2 — Critique
- [weakness 1]
- [weakness 2]
---
*→ Next: strengthen against critique*

### Draft 3 — Final
<production-ready output>
```
