---
name: ml-debugger
description: >
  Debug ML training runs, inference failures, and model quality issues. Invoke for:
  "loss not converging", "model not learning", "NaN loss", "gradient explosion",
  "inference error", "model output wrong", "training failed", "model debugging",
  "why is accuracy so low".
argument-hint: training config, loss curve, or error to debug
allowed-tools: Read, Edit, Grep, Glob, WebSearch
---

# Skill: ML Debugger — Training & Inference Debugging
**Category:** AI/ML Research

## Role
Diagnose and fix ML system failures: training instability, inference errors, and model quality problems.

## When to invoke
- Loss not decreasing or NaN
- Model outputs garbage
- Inference crashes or wrong output
- Accuracy unexpectedly low

## Instructions
1. Read training config and code
2. Check: NaN/Inf in loss? → LR too high or missing gradient clipping
3. Check: loss not moving? → LR too low, frozen layers, wrong optimizer
4. Check: overfitting? → add regularization, more data, reduce model size
5. Check: data loading → correct labels? No leakage? Proper normalization?
6. Check: inference → model in eval mode? Correct tokenization? Batch size?
7. Fix root cause, document in tasks/lessons.md

## Output format
```
## ML Debug Report — <issue>
### Symptom
### Root Cause
### Evidence
### Fix Applied
### Prevention
```

## Example
/ml-debugger training loss is NaN after epoch 2 — diagnose and fix
