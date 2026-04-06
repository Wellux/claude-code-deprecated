---
name: monitoring
description: >
  Set up observability: metrics, dashboards, alerts. Invoke for: "monitoring setup",
  "add metrics", "Grafana dashboard", "Prometheus", "alerting", "observability",
  "how do I monitor this", "SLO", "SLA", "what should I alert on".
argument-hint: system or service to monitor
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Monitoring — Observability & Alerting
**Category:** DevOps/Infra

## Role
Design observability stacks: metrics collection, dashboards, and meaningful alerts that catch real problems without alert fatigue.

## When to invoke
- New service needs monitoring
- "what should I alert on"
- Dashboard creation
- SLO/SLA definition

## Instructions
1. Define SLOs: availability (99.9%?), latency (p99 < 500ms?), error rate (< 1%?)
2. Instrument: add metrics (counters, gauges, histograms) to code
3. Alert on SLO breach, not on symptoms
4. Dashboard: latency percentiles (p50, p95, p99), error rate, throughput, saturation
5. Avoid alert fatigue: only page for actionable, urgent issues
6. Implement: Prometheus metrics + Grafana dashboard + AlertManager rules

## Output format
- prometheus.yml scrape config
- Grafana dashboard JSON
- AlertManager alert rules
- Instrumentation code snippets

## Example
/monitoring set up monitoring for the Claude API client — SLO: p99 < 5s, error rate < 1%
