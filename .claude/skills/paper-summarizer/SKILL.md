---
name: paper-summarizer
description: >
  Summarize academic papers and technical reports into actionable insights. Invoke for:
  "summarize this paper", "TL;DR this research", "what does this paper say", "explain
  this arxiv paper", "research summary", "summarize this PDF", "what are the key findings".
argument-hint: paper URL, arxiv ID, or paper title to summarize
allowed-tools: WebFetch, WebSearch, Write
---

# Skill: Paper Summarizer — Research Distillation
**Category:** AI/ML Research

## Role
Read academic papers and distill them into 1-page summaries with clear takeaways for practitioners.

## When to invoke
- "TL;DR this paper"
- Reading arxiv papers
- Keeping up with research
- Before implementing a technique from a paper

## Instructions
1. Fetch the paper (WebFetch arxiv URL or PDF)
2. Extract: problem statement, proposed solution, key innovation, results, limitations
3. Translate to plain English — no jargon without explanation
4. Identify: what can a practitioner USE from this paper?
5. Rate: novelty (1-5), practical usefulness (1-5), reproducibility (1-5)
6. Save to `data/research/`

## Output format
```
## Paper Summary: <title>
**Authors:** | **Year:** | **Venue:**
### Problem
### Solution
### Key Innovation
### Results
### Practical Takeaway (what you can use NOW)
### Limitations
### Rating: Novelty X/5 | Useful X/5
```

## Example
/paper-summarizer https://arxiv.org/abs/XXXX — summarize for practical implementation
