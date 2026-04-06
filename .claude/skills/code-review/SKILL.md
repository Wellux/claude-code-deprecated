---
name: code-review
description: >
  Thorough code review for quality, correctness, performance, and maintainability.
  Auto-invoke when: "review this code", "check my code", "PR review", "code quality",
  "any issues with this", "look at this implementation", "is this good", "feedback on code".
  Checks logic errors, edge cases, performance, readability, test coverage, naming.
argument-hint: file path, function name, or code to review
allowed-tools: Read, Grep, Glob
---

# Skill: Code Review — Thorough Quality Analysis
**Category:** Development

## Role
Review code for correctness, performance, security, readability, and maintainability. Provide actionable feedback with line references.

## When to invoke
- Pre-merge code review
- "review this" / "any issues?"
- After completing a feature, before commit
- Pair programming checkpoint

## Instructions
1. Read the code fully — understand the intent first
2. Logic: correct algorithm? Off-by-one errors? Null handling? Edge cases?
3. Performance: O(n²) where O(n) works? Unnecessary allocations? Missing indexes?
4. Readability: clear naming? Too-long functions? Missing comments for complex logic?
5. Tests: covered? Edge cases tested? Error paths tested?
6. Security: any injection risk? Exposed data? Auth missing?
7. Output: inline comments with file:line references, severity labels

## Output format
```
## Code Review — <file> — <date>
### 🔴 Blocking Issues
- file.py:45 — [BUG] Off-by-one in loop bound
### 🟡 Suggestions
- file.py:12 — [PERF] Use dict lookup instead of linear search
### 🟢 Good Patterns
### Verdict: APPROVE / REQUEST CHANGES
```

## Example
/code-review src/api/users.py — review the create_user function
