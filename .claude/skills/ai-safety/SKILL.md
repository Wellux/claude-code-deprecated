---
name: ai-safety
description: >
  AI safety review: alignment, misuse prevention, bias, fairness, and responsible AI.
  Invoke for: "AI safety review", "bias check", "fairness audit", "alignment",
  "responsible AI", "misuse prevention", "AI ethics", "safety guardrails",
  "could this AI system be misused".
argument-hint: AI system or model to audit for safety
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: AI Safety — Alignment & Responsible AI
**Category:** AI/ML Research

## Role
Audit AI systems for safety issues: misuse potential, bias, fairness, alignment with intended use, and responsible deployment.

## When to invoke
- Pre-deployment AI safety review
- "can this be misused?"
- Bias and fairness audit
- AI ethics review

## Instructions
1. Intended use: what is the system designed to do? Who are the users?
2. Misuse potential: could it be used for harm? How? Mitigations?
3. Bias: is training data or prompt biased? Are outputs fair across groups?
4. Transparency: can the system explain its decisions? Is it explainable?
5. Guardrails: what prevents harmful outputs? Are they sufficient?
6. Human oversight: are humans in the loop for high-stakes decisions?
7. Data privacy: does it handle PII? GDPR/CCPA compliance?

## Output format
```
## AI Safety Audit — <system> — <date>
### Intended Use
### Misuse Risks (ranked)
### Bias Assessment
### Guardrails: ✅/⚠️
### Human Oversight: ✅/⚠️
### Recommendations
```

## Example
/ai-safety audit the code-review agent — check for bias and misuse potential
