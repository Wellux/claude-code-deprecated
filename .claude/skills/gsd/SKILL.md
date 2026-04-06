---
name: gsd
description: >
  Get Shit Done — agentic meta-prompts that keep Claude focused and shipping without
  constant resets. Invoke for: "GSD mode", "just ship it", "stay focused", "no more
  planning — build", "ship without resets", "execute not plan", "get this done fast",
  "focus mode", "just do it". Inspired by gsd-build agentic workflow patterns.
argument-hint: task or feature to ship without interruption
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: GSD — Get Shit Done Mode
**Category:** Ecosystem
**Inspired by:** gsd-build (github.com/gsd-build)

## Role
Activate high-focus agentic mode: minimal planning overhead, maximum shipping velocity, no unnecessary resets or interruptions.

## When to invoke
- "just build it" / "no more planning"
- Need to ship fast without context resets
- Implementation is clear, execution just needs to happen
- Marathon build sessions

## Instructions
1. Read MASTER_PLAN.md — identify next unchecked step
2. Activate: compress context (`/compact`), focus on ONE task
3. Execute without asking for clarification (unless truly ambiguous)
4. After each sub-task: check it off, immediately proceed to next
5. Commit frequently: small, atomic commits after each milestone
6. No bikeshedding: accept good enough, not perfect
7. Keep going until: all current phase steps done OR blocker hit

## GSD Rules
- No rabbit holes: if something interesting but not required → skip
- No perfectionism: working > perfect
- No hand-holding: figure it out, don't ask
- Commit often: never lose more than 30min of work
- If blocked: use /blocker-resolver, then continue

## Example
/gsd ship Phase 3 skills — write all remaining skills without stopping
