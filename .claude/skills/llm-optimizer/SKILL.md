---
name: llm-optimizer
description: >
  Optimize LLM inference for cost, speed, and quality. Invoke for: "reduce LLM cost",
  "faster inference", "token optimization", "prompt compression", "caching strategy",
  "LLM cost too high", "optimize API calls", "reduce tokens", "LLM performance".
argument-hint: LLM usage pattern or cost to optimize
allowed-tools: Read, Edit, Grep, Glob, WebSearch
---

# Skill: LLM Optimizer — Cost, Speed & Quality Optimization
**Category:** AI/ML Research

## Role
Optimize LLM usage to minimize cost and latency while maintaining quality.

## When to invoke
- LLM API costs too high
- Inference too slow
- "optimize our Claude usage"
- Reducing token consumption

## Instructions
1. Profile current usage: tokens per call, calls per hour, cost breakdown
2. Cache: identical or near-identical requests (saves 30-70% on repetitive tasks)
3. Model routing: use Haiku for simple tasks, Sonnet for medium, Opus for complex only
4. Prompt compression: remove redundant instructions, use shorter examples
5. Streaming: use streaming for better UX, not for cost savings
6. Batching: batch independent requests where possible
7. Context management: don't send full history, summarize older context

## Output format
```
## LLM Optimization Report — <system>
### Current: Xcost/day, Yms avg latency
### Optimizations Applied
1. Model routing: Haiku for simple → saves $X/day
2. Response caching: 40% hit rate → saves $Y/day
### After: Xcost/day (Z% reduction), Yms latency
```

## Example
/llm-optimizer analyze src/llm/ usage — reduce cost by 50% without quality loss
