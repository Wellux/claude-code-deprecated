---
name: model-benchmarker
description: >
  Benchmark LLM models on specific tasks to choose the best model for your use case.
  Invoke for: "compare models", "which model is best for", "benchmark Claude vs GPT",
  "model selection", "cost vs quality tradeoff", "is Haiku fast enough for this".
argument-hint: task to benchmark and models to compare
allowed-tools: Read, Write, WebSearch
---

# Skill: Model Benchmarker — LLM Model Selection
**Category:** AI/ML Research

## Role
Benchmark multiple LLM models on your specific task to make data-driven model selection decisions.

## When to invoke
- Choosing between Claude Opus/Sonnet/Haiku
- Cost optimization (can we use cheaper model?)
- Quality regression after model upgrade
- "is this model good enough for X?"

## Instructions
1. Define task: what exactly needs to be done? What's "good enough"?
2. Create 10-20 representative test cases
3. Run each model on all test cases (or describe configuration to do so)
4. Score: quality (LLM-as-judge or human), latency (ms), cost (tokens × price)
5. Plot: quality vs cost tradeoff matrix
6. Recommend: best model for the use case with rationale

## Output format
```
## Model Benchmark — <task> — <date>
| Model | Quality | Latency | Cost/1k calls | Verdict |
|-------|---------|---------|---------------|---------|
| claude-opus-4-6 | 9.2/10 | 3.2s | $15 | Best quality |
| claude-sonnet-4-6 | 8.8/10 | 1.1s | $3 | Best value |
| claude-haiku-4-5 | 7.1/10 | 0.3s | $0.25 | Fast+cheap |
### Recommendation
```

## Example
/model-benchmarker compare Sonnet vs Haiku for code review task — quality vs cost
