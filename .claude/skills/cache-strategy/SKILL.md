---
name: cache-strategy
description: >
  Design and implement caching strategies for performance. Invoke for: "add caching",
  "cache this", "Redis", "cache invalidation", "TTL", "cache miss", "expensive operation",
  "repeated computation", "memoize", "this is too slow because of repeated calls".
argument-hint: what to cache or cache system to design
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Skill: Cache Strategy — Design & Implement Caching
**Category:** Development

## Role
Design cache layers that dramatically reduce latency and compute cost for repeated operations.

## When to invoke
- Repeated expensive operations (DB queries, API calls, computation)
- "cache this response"
- Redis or in-memory caching needed
- Cache invalidation design

## Instructions
1. Identify: what data? How often changes? How often read? Acceptable staleness?
2. Choose cache level: in-process (dict), Redis, CDN, DB query cache
3. Design cache key: deterministic, includes all relevant parameters
4. Set TTL: based on data freshness requirements
5. Design invalidation: time-based? Event-based? Manual?
6. Handle: cache miss, stampede (lock), thundering herd
7. Implement in src/utils/cache.py

## Output format
```
## Cache Design — <what> — <date>
### Data Profile: reads/writes per minute, staleness tolerance
### Cache Level: in-process / Redis / CDN
### Key Pattern: f"{resource}:{id}:{version}"
### TTL: Xh
### Invalidation: time-based / on-write
### Implementation
```

## Example
/cache-strategy LLM completion responses — cache by (model, prompt_hash, temperature)
