---
name: metrics-designer
description: >
  Design metrics systems and instrumentation for software applications. Invoke for:
  "add metrics", "instrument this code", "design metrics", "Prometheus metrics",
  "custom metrics", "application metrics", "observability metrics".
argument-hint: application or component to instrument with metrics
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Metrics Designer — Application Instrumentation
**Category:** Optimization/Research

## Role
Design and implement application metrics that make system behavior visible and debuggable.

## When to invoke
- "add metrics to this"
- New service needs instrumentation
- Custom metrics for business events
- Prometheus/StatsD integration

## Instructions
1. Identify: what events matter? What durations? What counts?
2. Choose metric types: Counter (increases), Gauge (can go up/down), Histogram (distribution)
3. Label design: meaningful labels, not high-cardinality (no user_id labels)
4. Implement: Prometheus client_python / statsd / datadog-lambda
5. Test: verify metrics emitted correctly
6. Document: what each metric means, what alerts it drives

## Output format
```python
from prometheus_client import Counter, Histogram

llm_calls_total = Counter('llm_calls_total', 'Total LLM API calls', ['model', 'status'])
llm_latency_seconds = Histogram('llm_latency_seconds', 'LLM call duration', ['model'])

# Usage
with llm_latency_seconds.labels(model='claude-sonnet-4-6').time():
    response = await client.complete(prompt)
llm_calls_total.labels(model='claude-sonnet-4-6', status='success').inc()
```

## Example
/metrics-designer add Prometheus metrics to src/llm/claude_client.py — calls, latency, tokens
