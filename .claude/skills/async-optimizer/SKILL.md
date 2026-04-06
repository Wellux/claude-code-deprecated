---
name: async-optimizer
description: >
  Optimize async/concurrent code for throughput and correctness. Invoke for:
  "async issue", "concurrent", "race condition", "await optimization", "run in parallel",
  "asyncio", "Promise.all", "thread safety", "deadlock", "async bottleneck",
  "too many awaits", "sequential when should be parallel".
argument-hint: async code file or function to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Async Optimizer — Concurrency & Parallelism
**Category:** Development

## Role
Identify async antipatterns and optimize for maximum concurrency while maintaining correctness.

## When to invoke
- Sequential awaits that could run in parallel
- Race conditions in async code
- Deadlocks or starvation
- "this async code is slow"

## Instructions
1. Read all async code in scope
2. Find sequential awaits that are independent (can run with Promise.all / asyncio.gather)
3. Identify race conditions: shared mutable state accessed concurrently?
4. Check locks: proper async locks used? No blocking calls in async context?
5. Find: CPU-bound work blocking event loop (needs thread pool)
6. Optimize: gather independent tasks, use semaphores to limit concurrency

## Output format
```
## Async Optimization — <file> — <date>
### Pattern Found: Sequential awaits (can be parallelized)
Before: [code]
After: [code using asyncio.gather()]
Speedup: ~3x for 3 independent operations
### Race Conditions
### Deadlock Risks
```

## Example
/async-optimizer src/llm/claude_client.py — parallelize the batch completion calls
