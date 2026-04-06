---
name: scaling
description: >
  Plan and implement horizontal/vertical scaling strategies. Invoke for: "scaling plan",
  "handle more traffic", "auto-scaling", "load balancing", "bottleneck", "capacity planning",
  "how do I scale this", "handle 10x load".
argument-hint: system to scale and target load
allowed-tools: Read, Write, WebSearch
---

# Skill: Scaling — Capacity Planning & Auto-Scaling
**Category:** DevOps/Infra

## Role
Design scaling strategies that handle load growth without over-provisioning.

## When to invoke
- Expecting traffic growth
- "can this handle 10x load?"
- Setting up auto-scaling
- Capacity planning for a new system

## Instructions
1. Baseline: current load, current capacity, headroom
2. Identify bottleneck: CPU? Memory? DB? Network? LLM API rate limits?
3. Horizontal scaling: add instances, implement stateless design
4. Vertical scaling: larger instance (quick fix, limited ceiling)
5. Auto-scaling: CPU/request-based triggers, scale-in delay
6. Database: read replicas, sharding, connection pooling
7. Load balancing: health checks, sticky sessions if needed

## Output format
```
## Scaling Plan — <system> — <date>
### Current Bottleneck
### Scaling Strategy: horizontal / vertical / both
### Auto-scaling Config
### Database Strategy
### Expected: handles Xx load at $Y/month
```

## Example
/scaling plan to scale the API from 100 to 10,000 requests/min with auto-scaling
