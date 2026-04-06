---
name: pipeline-opt
description: >
  Optimize CI/CD pipeline speed and reliability. Invoke for: "pipeline too slow",
  "slow CI", "speed up builds", "pipeline optimization", "cache builds",
  "parallel jobs", "flaky tests", "pipeline reliability".
argument-hint: pipeline config to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Pipeline Optimizer — CI/CD Speed & Reliability
**Category:** DevOps/Infra

## Role
Make CI/CD pipelines faster and more reliable through caching, parallelization, and flaky test elimination.

## When to invoke
- Pipeline takes > 10 minutes
- Flaky tests causing false failures
- "speed up our CI"

## Instructions
1. Profile pipeline: which job takes longest?
2. Cache: dependency caches (pip, npm, Maven), Docker layer cache
3. Parallelize: split test suite, run jobs concurrently
4. Fail fast: run quick checks first (lint, typecheck before slow tests)
5. Flaky tests: identify with test history, fix or quarantine
6. Skip unchanged: only test code that changed (affected tests)

## Output format
```
## Pipeline Optimization — <date>
### Current Duration: Xmin
### Bottlenecks Found
### Optimizations Applied
1. Added dependency cache → -3min
2. Parallelized tests (4 shards) → -6min
### After: Xmin (Y% faster)
```

## Example
/pipeline-opt .github/workflows/ci.yml — reduce pipeline from 25min to under 10min
