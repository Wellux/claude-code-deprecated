---
title: Skill Registry Duplicate Enforcement
date: 2026-04-05
time: 20:02:12
tags: [routing, skill-registry, testing, architecture]
slug: skill-registry-duplicate-enforcement
---

# Decision: Strict No-Duplicate Trigger Phrases in Skill Registry

## Status: Accepted
## Date: 2026-04-05

## Context
The skill router uses substring matching across 123 skills. Early versions had overlapping 
trigger phrases causing non-deterministic routing — same phrase could match multiple skills 
depending on registry iteration order.

## Decision
Enforce zero duplicate trigger phrases via  in 
tests/test_routing.py. CI fails immediately on any duplicate.

## Rationale
- Substring matching makes duplicates invisible at runtime — no error, just wrong skill
- A test at the registry level catches duplicates before they reach production
- Lower-priority skills lose their trigger phrases when conflicts exist (higher priority wins)

## Consequences
- Positive: Deterministic routing — same phrase always maps to same skill
- Positive: Registry is self-documenting (every trigger phrase is unique)
- Negative: Adding new skills requires careful trigger phrase selection
- Process: Run 
no tests ran in 0.02s after any skill edit

