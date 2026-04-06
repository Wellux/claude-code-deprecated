---
name: tdd
description: >
  Multi-agent TDD with strict subagent information isolation (glebis pattern).
  Invoke for: "test driven development", "TDD this", "write tests first", "red-green-refactor",
  "write failing tests then implement", "enforce TDD", "test-first development",
  "tdd workflow", "write specs then code". Spawns 3 isolated subagents.
argument-hint: feature or function to build via TDD
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: TDD — Multi-Agent Test-Driven Development

## Role
Enforce red-green-refactor at the architecture level, not discipline level.
Inspired by glebis/claude-skills information asymmetry pattern.

## The Core Insight
Most TDD fails because the developer can see both tests and implementation simultaneously.
This skill enforces information asymmetry through subagent context isolation:
- **TestWriter** sees only: specs, API signatures, requirements — never implementation
- **Implementer** sees only: failing test output, error messages — never the full test suite
- **Refactorer** sees only: passing green tests — nothing else

## Workflow

### Phase 1: TestWriter subagent
**Context given:** API signature, feature spec, acceptance criteria only.
**Task:** Write comprehensive failing tests covering:
- Happy path
- All edge cases and failure modes  
- Input validation
- Performance expectations if relevant
**Output:** `tests/test_<feature>.py` with all tests failing (red)

### Phase 2: Implementer subagent
**Context given:** `pytest` output showing failures ONLY (not the test source code).
**Task:** Write minimal implementation to make all tests pass.
**Constraint:** Do not look at test code — only read failure messages.
**Output:** `src/<module>/<feature>.py` with passing implementation

### Phase 3: Validation loop (up to 5 retries)
Run `pytest tests/test_<feature>.py`. If any tests still fail:
- Pass only the failure output to a fresh Implementer context
- Retry up to 5 times
- On retry 5 failure: escalate with full context

### Phase 4: Refactorer subagent
**Context given:** Passing test suite (green) + implementation
**Task:** Refactor for clarity, DRY, performance — without changing behavior
**Constraint:** All tests must still pass after refactor

## Instructions

1. **Parse the spec**: extract API signatures and acceptance criteria
2. **Spawn TestWriter**: write `tests/test_<feature>.py`; verify all tests FAIL initially
3. **Spawn Implementer**: pass only pytest failure output as context
4. **Run validation loop**: pytest → if red → new Implementer context with failures only
5. **Spawn Refactorer**: pass green test results + implementation
6. **Final check**: `pytest` + `ruff check` must both pass
7. **Report**: show test count, coverage, refactoring changes made

## Anti-patterns (will NOT do)
- Skip the failing-first check ("just write impl and tests together")
- Show the TestWriter any existing implementation code
- Show the Implementer the test source (only failure messages)
- Skip the refactor phase

## Output Format
```
## TDD: <feature>

### Phase 1 — TestWriter
✅ 12 tests written | all failing (expected)

### Phase 2 — Implementer (attempt 1/5)
✅ 11/12 passing | 1 failure: test_edge_case_empty_input

### Phase 2 — Implementer (attempt 2/5)  
✅ 12/12 passing | 🟢 all green

### Phase 4 — Refactorer
✅ Extracted 3 helpers, removed duplication | 12/12 still passing
✅ Lint: clean
```
