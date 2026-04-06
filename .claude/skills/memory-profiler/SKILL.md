---
name: memory-profiler
description: >
  Profile and fix memory leaks and excessive memory usage. Invoke for: "memory leak",
  "too much memory", "OOM", "memory usage", "memory profiling", "garbage collection",
  "memory keeps growing", "reduce memory footprint".
argument-hint: component or process to profile for memory
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Memory Profiler — Memory Leak Detection
**Category:** Optimization/Research

## Role
Detect and fix memory leaks, reduce peak memory usage, and optimize garbage collection.

## When to invoke
- Out of memory errors
- Memory growing over time (leak)
- "reduce memory usage"
- Container being OOM killed

## Instructions
1. Read code for common leak patterns: circular refs, event listeners not removed, caches without TTL
2. Python: tracemalloc, objgraph for live profiling
3. Node.js: --expose-gc, heap snapshots
4. Identify: what's growing? Which objects accumulate?
5. Fix: break circular references, clear caches, remove unused listeners
6. Measure: before/after peak memory usage

## Output format
```
## Memory Profile — <component> — <date>
### Peak Memory: XMB
### Leak Found: EventEmitter listeners accumulating in X
### Fix Applied:
### After: XMB (Y% reduction)
```

## Example
/memory-profiler src/llm/claude_client.py — check for memory leaks in streaming responses
