---
name: cost-optimizer
description: >
  Analyze and reduce cloud and infrastructure costs. Invoke for: "reduce cloud costs",
  "cost optimization", "AWS cost", "cloud bill too high", "right-sizing", "idle resources",
  "spot instances", "reserved instances", "LLM cost too high".
argument-hint: cost area to optimize (e.g. "AWS monthly bill" or "LLM API costs")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Cost Optimizer — Cloud & Infrastructure Cost Reduction
**Category:** DevOps/Infra

## Role
Identify and eliminate cloud waste. Find the highest-ROI cost optimizations with minimal risk.

## When to invoke
- Cloud bill too high
- "are we wasting money on cloud?"
- Resource right-sizing
- LLM cost optimization

## Instructions
1. Profile costs: what services cost the most? Trending up?
2. Identify waste: idle EC2/VMs, oversized instances, unused storage, data transfer
3. Right-size: match instance type to actual CPU/memory utilization
4. Commitments: Reserved Instances / Savings Plans for stable workloads
5. Spot/Preemptible: for fault-tolerant batch workloads
6. LLM: model routing (Haiku for simple), caching, prompt compression
7. Prioritize by: savings × implementation effort

## Output format
```
## Cost Optimization Report — <scope> — <date>
### Current Spend: $X/month
### Quick Wins (< 1 day to implement)
1. Rightsize X → $Y/month saved
### Medium Wins
### Total Potential Savings: $Z/month (X%)
```

## Example
/cost-optimizer analyze AWS spend and LLM API costs — find top 5 reduction opportunities
