---
name: preflight
description: >
  Validate a prompt or task description for clarity and completeness before expensive execution.
  Invoke for: "preflight check", "validate this prompt", "is this task clear enough",
  "check before running", "prompt quality check", "task spec review", "pre-execution check",
  "score this prompt", "is my task well defined". Runs a 12-category scorecard.
argument-hint: task description or prompt to validate
allowed-tools: Read
---

# Skill: Preflight — Prompt & Task Validation

## Role
Score a task description or prompt across 12 quality dimensions before committing to expensive multi-step execution. Surface ambiguities, missing context, and scope issues upfront.

## When to invoke
- Before running `/superpowers`, `/write-plan`, or `/swarm` on a non-trivial task
- When task requirements feel unclear or underspecified
- Before creating complex agent pipelines
- When a previous run went sideways due to unclear requirements

## 12-Category Scorecard

Score each 0–2 (0=missing, 1=partial, 2=clear):

| # | Category | Check |
|---|----------|-------|
| 1 | **Goal clarity** | Is the desired outcome stated? |
| 2 | **Success criteria** | How do we know it's done? |
| 3 | **Scope bounds** | What's in/out of scope? |
| 4 | **Input context** | Are relevant files/code/data referenced? |
| 5 | **Constraints** | Tech stack, performance, security limits? |
| 6 | **Edge cases** | Are failure modes acknowledged? |
| 7 | **Dependencies** | Are blockers or prerequisites called out? |
| 8 | **Reversibility** | Can mistakes be undone? Is a backup plan mentioned? |
| 9 | **Acceptance test** | Is there a concrete way to verify correctness? |
| 10 | **Timeline/priority** | Is urgency or ordering specified? |
| 11 | **Audience/user** | Who uses this? What do they need? |
| 12 | **Anti-goals** | What should explicitly NOT be built? |

## Instructions

1. Read the task description carefully
2. Score each of the 12 categories
3. Calculate total score (0–24) and grade:
   - 20–24: ✅ Ready to execute
   - 14–19: ⚠ Execute with caution — note gaps
   - 8–13: 🔶 Refine before executing
   - 0–7: 🚫 Stop — requirements too vague
4. For each score < 2, write one clarifying question
5. Optionally rewrite the task description with gaps filled

## Output Format

```
## Preflight: <task name>

| Category | Score | Notes |
|----------|-------|-------|
| Goal clarity | 2 | ✅ Clear: build X that does Y |
| Success criteria | 1 | ⚠ Partial: "tests pass" but no coverage target |
...

**Total: 18/24 — ⚠ Execute with caution**

### Gaps to resolve:
1. [Success criteria] What coverage threshold is acceptable?
2. [Scope bounds] Should this handle authentication or is that out of scope?

### Rewritten task (optional):
Build a tiered memory system in src/persistence/tiered_memory.py that...
```
