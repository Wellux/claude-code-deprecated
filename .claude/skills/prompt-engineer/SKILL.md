---
name: prompt-engineer
description: >
  Design, optimize, and test prompts for maximum LLM performance. Invoke for:
  "improve this prompt", "write a system prompt", "prompt engineering", "optimize prompt",
  "better prompt for", "few-shot examples", "chain of thought", "system prompt design",
  "my prompt isn't working".
argument-hint: task description or existing prompt to optimize
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Prompt Engineer — LLM Prompt Optimization
**Category:** AI/ML Research

## Role
Design and optimize prompts using advanced techniques: chain-of-thought, few-shot, system prompt architecture, constitutional AI principles.

## When to invoke
- Writing new system prompts
- Prompt not producing desired output
- Few-shot example design
- Prompt template creation

## Instructions
1. Understand task: what input → what output? What constraints?
2. Choose technique: zero-shot / few-shot / chain-of-thought / role-based / XML tags
3. Write system prompt: role, context, constraints, output format
4. Add few-shot examples if needed (2-5 representative examples)
5. Test with edge cases: ambiguous input, adversarial input, empty input
6. Iterate: identify failure modes and add clarifying instructions
7. Save to `tools/prompts/` or `data/prompts/`

## Output format
```
## Prompt Design — <task> — <date>
### System Prompt
[complete system prompt]
### Few-Shot Examples
[if applicable]
### Test Cases & Results
### Failure Modes Identified
```

## Example
/prompt-engineer design system prompt for code review assistant with strict JSON output
