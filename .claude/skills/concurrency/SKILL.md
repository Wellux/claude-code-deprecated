---
name: concurrency
description: >
  Design concurrent and parallel systems correctly. Invoke for: "concurrency design",
  "thread safety", "parallel processing", "worker pool", "queue", "producer consumer",
  "concurrent writes", "data consistency with concurrent access".
argument-hint: concurrent system to design or review
allowed-tools: Read, Write, Edit, Glob
---

# Skill: Concurrency — Parallel & Concurrent Systems
**Category:** Optimization/Research

## Role
Design correct, efficient concurrent systems — thread pools, queues, locks, and lock-free patterns.

## When to invoke
- Concurrent access to shared state
- Worker pool design
- Queue-based processing
- "make this parallel"

## Instructions
1. Identify: what's shared state? What must be atomic?
2. Choose synchronization: mutex, semaphore, atomic, lock-free
3. Design: producer-consumer, worker pool, event-driven
4. Avoid: lock contention, deadlocks, starvation
5. Use: asyncio.gather for I/O-bound, ProcessPoolExecutor for CPU-bound
6. Test: run concurrent test cases to expose race conditions

## Output format
```python
# Worker pool pattern
async def process_batch(items: list) -> list:
    semaphore = asyncio.Semaphore(10)  # max 10 concurrent
    async def process_one(item):
        async with semaphore:
            return await expensive_operation(item)
    return await asyncio.gather(*[process_one(i) for i in items])
```

## Example
/concurrency design worker pool for processing 1000 LLM requests with rate limiting
