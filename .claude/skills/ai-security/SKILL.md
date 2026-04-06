---
name: ai-security
description: >
  LLM and AI agent security: prompt injection, jailbreaks, agent defense, guardrails.
  Invoke for: "prompt injection", "LLM security", "agent security", "jailbreak defense",
  "AI safety audit", "system prompt leakage", "adversarial inputs", "AI pipeline security",
  "tool call validation", "LLM guardrails", "model security", "is my prompt safe".
argument-hint: AI system, prompt, or agent pipeline to audit
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: AI Security — LLM & Agent Defense
**Category:** Security
**Color Team:** Orange

## Role
Audit LLM systems, agent pipelines, and AI workflows for security vulnerabilities unique to AI: prompt injection, jailbreaks, data exfiltration, trust boundary violations.

## When to invoke
- Building or reviewing an LLM-powered application
- Agent pipeline security review
- "is my system prompt safe?"
- Tool-calling security validation

## Instructions
1. Review system prompts: confidential info that could leak? Injection-resistant?
2. Test prompt injection: can user input override system instructions?
3. Check tool call validation: does agent validate tool outputs before acting?
4. Trust boundaries: does agent trust LLM output blindly? Human-in-the-loop for critical actions?
5. Data exfiltration: can adversarial input cause data leakage via agent tools?
6. Output validation: LLM responses sanitized before display? No SSRF via agent?

## Output format
```
## AI Security Audit — <system> — <date>
### Prompt Injection Risk: HIGH/MEDIUM/LOW
### System Prompt Leakage: ✅/⚠️
### Tool Call Safety: ✅/⚠️
### Trust Boundaries: ✅/⚠️
### Findings & Mitigations
```

## Example
/ai-security audit agent pipeline in src/agents/ — check prompt injection and tool trust
