---
name: perf-profiler
description: >
  Profile and optimize application performance: CPU, memory, I/O bottlenecks. Invoke for:
  "performance issue", "this is slow", "memory leak", "CPU spike", "profiling",
  "benchmark", "optimize performance", "bottleneck", "too much memory".
argument-hint: component, function, or endpoint to profile
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Perf Profiler — Performance Analysis & Optimization
**Category:** Development

## Role
Identify CPU, memory, and I/O bottlenecks and optimize them with measurable before/after metrics.

## When to invoke
- Slow API endpoints or functions
- High memory usage
- CPU spikes
- "this needs to be faster"

## Instructions
1. Identify what to profile: function, endpoint, or process
2. Add profiling: cProfile (Python), console.time (JS), or read existing metrics
3. Find top 3 hotspots by time/memory
4. Analyze root cause: algorithm complexity? I/O bound? Memory allocation?
5. Optimize: better algorithm, caching, async I/O, batching, generator instead of list
6. Measure after: quantify improvement

## Output format
```
## Performance Analysis — <component> — <date>
### Hotspots
1. function_name — 45% of runtime — O(n²) algorithm
### Optimizations Applied
### Before: Xms / YMB
### After: Xms / YMB (Zx improvement)
```

## Example
/perf-profiler src/prompt_engineering/chainer.py — profile chain execution time
