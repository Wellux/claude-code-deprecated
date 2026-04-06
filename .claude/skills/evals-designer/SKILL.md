---
name: evals-designer
description: >
  Design evaluation frameworks for LLMs and AI systems. Invoke for: "eval this model",
  "LLM evaluation", "benchmark", "how do I measure quality", "evals", "test my prompts",
  "measure hallucination", "model comparison", "build an eval suite".
argument-hint: AI system or prompt to evaluate
allowed-tools: Read, Write, Glob, WebSearch
---

# Skill: Evals Designer — LLM Evaluation Framework
**Category:** AI/ML Research

## Role
Design rigorous evaluation frameworks to measure LLM and agent system quality, correctness, and reliability.

## When to invoke
- "how good is my prompt?"
- Comparing model versions
- Measuring hallucination rate
- Building automated test suite for AI system

## Instructions
1. Define metrics: accuracy, groundedness, coherence, safety, latency, cost
2. Design test cases: golden set of input/expected output pairs
3. Build eval pipeline: run model, score output, aggregate metrics
4. Measure: precision/recall for retrieval, exact match / LLM-as-judge for generation
5. Track over time: did new prompt/model improve or regress?
6. Save evals to `notebooks/` for reproducibility

## Output format
```python
# Eval framework
eval_cases = [
    {"input": "...", "expected": "...", "category": "..."},
]
# Scoring function
def score(output, expected): ...
# Results
# Accuracy: X%, Groundedness: X%, Latency: Xms avg
```

## Example
/evals-designer build eval suite for the code-review skill — 20 test cases with rubric
