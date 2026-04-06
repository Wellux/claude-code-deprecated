---
name: write-plan
description: >
  Decompose a feature into atomic 2-5 minute tasks with explicit acceptance criteria.
  Invoke for: "write a plan", "break this down", "make a task list", "plan before coding",
  "decompose this feature", "create subtasks", "what are the steps", "planning phase",
  "plan this out", "task breakdown". Inspired by Superpowers (obra/superpowers) /write-plan phase.
argument-hint: feature or task to plan (ideally after /brainstorm)
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Skill: Write Plan — Atomic Task Decomposition
**Category:** Ecosystem
**Inspired by:** Superpowers (github.com/obra/superpowers)

## Role
Act as a tech lead breaking down a feature into the smallest independently-verifiable tasks.
Each task must be completable in 2-5 minutes with a clear pass/fail acceptance criterion.

## When to Invoke
- After `/brainstorm` has clarified requirements
- Before starting implementation of a multi-step feature
- When a feature needs to be divided across multiple sessions or agents
- When you need to track implementation progress explicitly

## Planning Rules

### Task Granularity
- **Too big:** "implement rate limiter" (multiple hours, unclear done state)
- **Too small:** "add import statement" (30 seconds, not worth tracking)
- **Just right:** "write `RateLimiter.is_allowed(key)` that returns bool, sliding window 60s"

### Each Task Must Have
1. **What** — concrete deliverable (function, file, test, config)
2. **Done when** — explicit acceptance criterion (test passes, command outputs X, file exists)
3. **Sequence** — must-happen-before dependencies noted

### Task Categories
- `[INFRA]` — scaffolding, file creation, dependencies
- `[IMPL]` — production code implementation
- `[TEST]` — test coverage
- `[DOCS]` — documentation, comments
- `[CI]` — build, lint, eval gates
- `[REVIEW]` — code review checkpoint

## Process

1. Read relevant source files to understand existing patterns
2. Identify the implementation layers (data model → logic → API → tests → docs)
3. Write tasks bottom-up: tests last so they verify real behavior
4. Sequence tasks so each builds cleanly on the previous
5. Add a final `[CI]` gate task: `pytest + ruff + ccm eval run --dry-run`

## Output Format

Write directly to `tasks/todo.md`:

```markdown
## Plan: <Feature Name>
> Started: YYYY-MM-DD | Source: /write-plan

- [ ] [INFRA] Create `src/<module>.py` with module docstring and imports
      Done: file exists, `from src.<module> import X` works
- [ ] [IMPL] Implement `<ClassName>.__init__(self, param: type)` with validation
      Done: constructor raises `ValueError` on invalid input
- [ ] [IMPL] Implement `<ClassName>.method(self, arg) -> ReturnType`
      Done: returns expected value for happy path
- [ ] [TEST] Write `tests/test_<module>.py::TestClassName::test_method_happy_path`
      Done: test passes with `pytest tests/test_<module>.py -q`
- [ ] [TEST] Write `TestClassName::test_method_invalid_input_raises`
      Done: test passes
- [ ] [DOCS] Add docstrings to public methods
      Done: `pydoc src/<module>` shows all public method signatures
- [ ] [CI] Run full gate: `pytest tests/ -q && ruff check src/ tests/ --select E,F,W --ignore E501`
      Done: exit code 0 on both
```

## Integration

After writing the plan:
- Tasks appear in session-start.sh boot banner (open task count)
- `f` shortcut executes the next `- [ ]` item
- `/superpowers` executes with discipline: tests before marking complete

## Example
/write-plan implement sliding-window rate limiter for ClaudeClient (post-brainstorm)
