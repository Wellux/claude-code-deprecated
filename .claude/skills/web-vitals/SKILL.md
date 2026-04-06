---
name: web-vitals
description: >
  Audit and optimize Core Web Vitals (LCP, CLS, FID/INP). Invoke for: "web vitals",
  "page speed", "LCP", "CLS", "INP", "Lighthouse", "performance audit",
  "slow page load", "improve page speed score", "Core Web Vitals".
argument-hint: URL or HTML file to audit
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Web Vitals — Core Web Vitals Optimization
**Category:** Optimization/Research

## Role
Audit and improve Core Web Vitals to meet Google's thresholds: LCP < 2.5s, CLS < 0.1, INP < 200ms.

## When to invoke
- Page performance issues
- SEO improvements needed
- "Lighthouse score is low"
- Before launch performance gate

## Instructions
1. Read HTML/CSS/JS to identify issues without running Lighthouse
2. LCP: largest image lazy-loaded? Critical images preloaded? Server response fast?
3. CLS: all images have explicit dimensions? No layout shifts on load?
4. INP: main thread blocked? Event handlers fast? Third-party scripts deferred?
5. TTFB: server response time? CDN used?
6. Prioritize: fix highest-impact issues first

## Output format
```
## Web Vitals Audit — <page> — <date>
### LCP: X.Xs (target < 2.5s) — Issue: lazy-loaded hero image
### CLS: X.X (target < 0.1) — Issue: missing image dimensions
### INP: Xms (target < 200ms) — Issue: heavy JS on main thread
### Fixes (priority order)
```

## Example
/web-vitals audit index.html — identify and fix Core Web Vitals issues
