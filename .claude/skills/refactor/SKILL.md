---
name: refactor
description: >
  Refactor code for clarity, performance, and maintainability without changing behavior.
  Invoke for: "refactor this", "clean up this code", "extract function", "simplify this",
  "make this more readable", "reduce duplication", "better structure", "DRY this up",
  "too complex", "spaghetti code".
argument-hint: file or function to refactor
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Refactor — Clean Code Without Behavior Change
**Category:** Development

## Role
Improve code structure, readability, and maintainability while preserving exact behavior.

## When to invoke
- Code is hard to read or maintain
- Functions are too long (> 40 lines)
- Duplication exists (DRY violation)
- Naming is unclear

## Instructions
1. Read and understand the CURRENT behavior completely (write it down)
2. Identify refactoring opportunities: long functions, duplication, unclear naming, deep nesting
3. Apply refactoring: extract method, rename, simplify conditionals, reduce nesting
4. Verify behavior PRESERVED: same inputs → same outputs
5. Run existing tests to confirm nothing broke

## Output format
Show before/after for each change:
```
### Change 1: Extract calculate_discount()
Before: [code]
After: [code]
Reason: Function was 60 lines, now split into focused 15-line functions
```

## Example
/refactor src/utils/pricing.py — extract the discount calculation logic
