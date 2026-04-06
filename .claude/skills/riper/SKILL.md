---
name: riper
description: >
  RIPER agentic workflow: Research → Innovate → Plan → Execute → Review.
  Enforces strict phase separation for complex features to prevent premature implementation.
  Invoke for: "riper", "riper workflow", "research then innovate", "five phase workflow",
  "research innovate plan execute review", "structured feature workflow",
  "riper mode", "phase-gated development", "systematic feature delivery".
  Inspired by ThibautMelen/agentic-workflow-patterns RIPER pattern.
argument-hint: feature or task to deliver through the RIPER workflow
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, WebSearch
---

# Skill: RIPER — Phase-Gated Agentic Workflow

## Role
Enforce five strict phases for complex feature delivery. No phase can begin until the
previous is explicitly approved. Prevents the most common failure mode: jumping to
implementation before understanding the problem.

Inspired by ThibautMelen/agentic-workflow-patterns and tony/claude-code-riper-5.

## The 5 Phases

### Phase 1: RESEARCH
**Goal**: Understand the problem space completely before proposing anything.
**Activities**:
- Read all relevant existing code, docs, tests
- Search for prior art, existing patterns, similar implementations
- Identify constraints, edge cases, integration points
- Interview the codebase (grep, glob, read) — do not propose solutions

**Gate**: Write a Research Summary. Stop. Wait for approval before Phase 2.

**Output format**:
```
## RIPER Phase 1 — Research Complete

### What exists
[Relevant code, patterns, dependencies found]

### Constraints discovered
[Technical limits, integration requirements, edge cases]

### Open questions
[Things that need clarification before innovating]

→ Ready for Phase 2 (Innovate)?
```

---

### Phase 2: INNOVATE
**Goal**: Generate multiple solution approaches without committing to any one.
**Activities**:
- Propose 2–4 distinct implementation approaches
- For each: pros, cons, complexity, risks
- Do NOT write any implementation code
- Explicitly note which approach you lean toward and why

**Gate**: Write Innovation Summary. Stop. Wait for approval + approach selection.

**Output format**:
```
## RIPER Phase 2 — Innovate

### Approach A: [name]
- How: [brief]
- Pros: [list]
- Cons: [list]
- Risk: Low/Medium/High

### Approach B: [name]
...

### Recommendation: Approach X because [reason]

→ Which approach? Approve to proceed to Phase 3 (Plan).
```

---

### Phase 3: PLAN
**Goal**: Atomic task decomposition of the chosen approach.
**Activities**:
- Break the chosen approach into tasks of ≤30 minutes each
- Each task: what file, what change, what test verifies it
- Identify the critical path (which tasks block others)
- Write the plan to `tasks/todo.md`

**Gate**: Task list written. Stop. Wait for approval before Phase 4.

**Output format**:
```
## RIPER Phase 3 — Plan

### Tasks (written to tasks/todo.md)
- [ ] Task 1: [file] — [change] — verified by: [test]
- [ ] Task 2: ...

### Critical path: 1 → 3 → 5 (tasks 2 and 4 can run in parallel)

→ Plan approved? Proceed to Phase 4 (Execute)?
```

---

### Phase 4: EXECUTE
**Goal**: Implement exactly the plan, no more, no less.
**Activities**:
- Execute tasks from the plan in order
- For each task: implement, test, mark done in todo.md
- Do NOT refactor or improve things outside the plan scope
- Do NOT add features not in the plan

**Gate**: All tasks complete, all tests pass, lint clean.

**Output format**:
```
## RIPER Phase 4 — Execute

✅ Task 1: [description] — tests: pass
✅ Task 2: [description] — tests: pass
...

All N tasks complete. Tests: X passed. Lint: clean.

→ Proceed to Phase 5 (Review)?
```

---

### Phase 5: REVIEW
**Goal**: Verify the implementation against the original spec with independent eyes.
**Activities**:
- Re-read the original request from Phase 1
- Verify each requirement is met with file:line evidence
- Look for: regressions, missing edge cases, spec drift, unnecessary additions
- Run full test suite + lint + smoke evals

**Output format**:
```
## RIPER Phase 5 — Review

### Spec vs. Implementation
| Requirement | Status | Evidence |
|-------------|--------|---------|
| [req 1] | ✅ Met | src/foo.py:42 |
| [req 2] | ✅ Met | tests/test_foo.py:17 |

### Regression check: [N tests passing, was M before]
### Scope creep: [None / described if found]
### Final verdict: APPROVED ✅ / NEEDS REVISION ⚠
```

## Phase Control
- Use `/riper:research`, `/riper:innovate`, `/riper:plan`, `/riper:execute`, `/riper:review` to jump to a specific phase
- The orchestrator tracks current phase in `.claude/memory/hot/hot-memory.md` under `riper_phase`
- Never skip phases without explicit user instruction
