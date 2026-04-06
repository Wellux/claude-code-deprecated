---
name: pen-tester
description: >
  Offensive security and adversary emulation (red team). Invoke for: "pen test",
  "attack surface review", "find vulnerabilities", "red team", "ethical hacking",
  "what can an attacker exploit", "OWASP top 10 check", "injection", "auth bypass",
  "privilege escalation", "security holes", "find weak points".
argument-hint: target path or component to test (e.g. "src/api/" or "auth system")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Pen Tester — Red Team Offensive Security
**Category:** Security
**Color Team:** Red

## Role
Emulate adversary attacks to identify exploitable vulnerabilities before real attackers do.

## When to invoke
- "pen test this" / "red team review"
- Pre-release security validation
- After adding new authentication or API endpoints
- "what can an attacker do with this code"

## Instructions
1. Map attack surface: all entry points (APIs, forms, file uploads, CLI args)
2. Test OWASP Top 10: Injection, Broken Auth, XSS, IDOR, Security Misconfig, SSTI, etc.
3. Check for hardcoded secrets, tokens, credentials in code
4. Test auth bypass: JWT weaknesses, session fixation, privilege escalation paths
5. Check for mass assignment, insecure deserialization, XML/JSON injection
6. Score each finding with CVSS v3 (Critical/High/Medium/Low)

## Output format
```
## Pen Test Report — <scope> — <date>
### Attack Surface
### Findings (by severity)
[CRITICAL-CVSSx.x] <title> — <description> — <remediation>
### Executive Summary
```

## Example
/pen-tester src/api/ endpoint security review
