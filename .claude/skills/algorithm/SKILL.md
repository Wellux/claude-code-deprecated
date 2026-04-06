---
name: algorithm
description: >
  Improve algorithmic efficiency — find better algorithms and data structures. Invoke for:
  "algorithm improvement", "better algorithm", "O(n²) is too slow", "data structure choice",
  "optimize this loop", "algorithmic complexity", "time complexity".
argument-hint: algorithm or function to optimize
allowed-tools: Read, Edit, Glob
---

# Skill: Algorithm — Algorithmic Efficiency
**Category:** Optimization/Research

## Role
Replace inefficient algorithms with better ones. Turn O(n²) into O(n log n), add memoization, choose right data structures.

## When to invoke
- "this is too slow" (algorithm problem)
- Nested loops on large data
- O(n²) or worse complexity
- Wrong data structure for access pattern

## Instructions
1. Read the code — understand what it's computing
2. Identify complexity: nested loops? Repeated work? Unnecessary recomputation?
3. Choose: better algorithm (sort, search, graph) or better data structure (hash map vs list)
4. Memoization: cache repeated computations
5. Reduce comparisons: pre-sort, use sets for O(1) lookup
6. Measure: count operations before/after

## Output format
```
## Algorithm Optimization — <function>
### Before: O(n²) — nested loop over n items
### After: O(n log n) — sort + binary search
### Improvement: 100x faster for n=10,000

[Before code]
[After code]
Explanation: ...
```

## Example
/algorithm find_duplicates function is O(n²) — improve to O(n)
