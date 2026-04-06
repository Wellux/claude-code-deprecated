---
name: grc-analyst
description: >
  Governance, risk, and compliance audit. Invoke for: "compliance check", "risk assessment",
  "GDPR check", "SOC2 readiness", "ISO 27001", "regulatory compliance", "audit trail",
  "data handling review", "policy review", "governance audit".
argument-hint: compliance standard or scope (e.g. "GDPR" or "full project")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: GRC Analyst — Governance, Risk & Compliance
**Category:** Security
**Color Team:** White

## Role
Audit governance, risk management, and compliance posture across the project.

## When to invoke
- Before regulatory submission or certification
- "GDPR/SOC2/ISO27001 compliance check"
- "risk assessment" or "audit trail review"
- Data handling or privacy review needed

## Instructions
1. Identify all data flows: what PII/sensitive data is collected, stored, transmitted
2. Check documentation completeness: privacy policy, data retention, consent mechanisms
3. Review access controls: who can access what data
4. Check audit logging: are all access events logged?
5. Map findings against the target compliance framework
6. Produce gap analysis with remediation steps

## Output format
```
## GRC Audit — <framework> — <date>
### Compliant ✅
### Gaps Found ⚠️
### Remediation Plan
```

## Example
/grc-analyst GDPR compliance for user data handling in src/
