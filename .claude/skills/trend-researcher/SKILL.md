---
name: trend-researcher
description: >
  Research emerging trends in technology, AI, and markets. Invoke for: "what's trending",
  "latest trends in X", "emerging technology", "market trends", "tech radar",
  "what should I know about X", "trend analysis", "state of X in 2026".
argument-hint: domain or topic to research trends in
allowed-tools: WebSearch, WebFetch, Write
---

# Skill: Trend Researcher — Emerging Technology Trends
**Category:** Optimization/Research

## Role
Research and synthesize emerging trends in AI, technology, and markets into actionable insights.

## When to invoke
- Staying current with AI/tech trends
- Strategic technology decisions
- "what's new in X"
- Weekly/monthly trend briefings

## Instructions
1. WebSearch: `<domain> trends 2026`, `<domain> state of the art`, `<domain> emerging`
2. Read top 5-10 sources: blog posts, reports, GitHub trending
3. Extract: what's gaining momentum? What's declining? What's emerging?
4. Signal vs noise: separate genuine trends from hype
5. Relevance: which trends apply to this project?
6. Save to data/research/ with date

## Output format
```
## Trend Report — <domain> — <date>
### Rising 📈
1. Trend: [what] — Evidence: [signals] — Relevance: [high/med/low]
### Declining 📉
### Watch List 👀
### Recommended Actions
```

## Example
/trend-researcher AI agent frameworks 2026 — what's gaining vs declining
