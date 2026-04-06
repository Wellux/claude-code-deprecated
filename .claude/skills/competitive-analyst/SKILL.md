---
name: competitive-analyst
description: >
  Research and analyze competitors and alternatives. Invoke for: "competitive analysis",
  "compare to competitors", "what are the alternatives", "market analysis",
  "how does X compare to Y", "competitor research", "SWOT analysis".
argument-hint: product, technology, or market to analyze
allowed-tools: WebSearch, WebFetch, Write
---

# Skill: Competitive Analyst — Market & Competitor Research
**Category:** Optimization/Research

## Role
Research competitors and alternatives to inform strategic technology and product decisions.

## When to invoke
- Choosing between competing technologies
- Product positioning research
- "what are the alternatives to X"
- Technology selection

## Instructions
1. Identify: who/what are the main competitors or alternatives?
2. Compare: features, pricing, performance, community, maintenance
3. SWOT: Strengths, Weaknesses, Opportunities, Threats for each
4. Find: what do users say? GitHub issues, Reddit, HN discussions
5. Recommendation: which to use and why, given specific requirements

## Output format
```
## Competitive Analysis — <domain> — <date>
### Options Evaluated
| Tool | Strengths | Weaknesses | Best For |
### Comparison Matrix
| Feature | A | B | C |
### Recommendation: Use X because...
```

## Example
/competitive-analyst compare LightRAG vs ChromaDB vs Pinecone for this project's RAG needs
