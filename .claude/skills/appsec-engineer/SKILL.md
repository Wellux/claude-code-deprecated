---
name: appsec-engineer
description: >
  Application security: OWASP Top 10, secure code review, secure SDLC. Auto-invoke on
  any code review request. Trigger for: "code security review", "OWASP audit", "XSS check",
  "SQL injection", "secure code review", "SAST", "dependency vulnerabilities", "auth review",
  "input validation", "secure coding", "review this code" (security angle),
  "is this safe", "any security issues".
argument-hint: file path or code snippet to audit
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: AppSec Engineer — OWASP & Secure Code Review
**Category:** Security
**Color Team:** Orange

## Role
Perform application security review against OWASP Top 10 and secure coding standards.

## When to invoke
- Any code review with security implications
- Pre-release security gate
- New authentication or input-handling code
- "is this secure?" / "any XSS/SQLi risk?"

## Instructions
1. Read all code in scope with Grep/Glob
2. Check A01 Broken Access Control: authorization on every endpoint?
3. Check A02 Cryptographic Failures: weak algorithms? Hardcoded keys? HTTP not HTTPS?
4. Check A03 Injection: parameterized queries? Input sanitization? Template injection?
5. Check A07 Auth Failures: session management? JWT validation? Brute force protection?
6. Check A09 Logging Failures: sensitive data logged? Log injection possible?
7. Report: file:line, category, severity, remediation code

## Output format
```
## AppSec Review — <scope> — <date>
### Critical
- [A03-CRITICAL] src/api/users.py:45 — SQL string concat → use parameterized query
### High / Medium / Low
### OWASP Coverage: A01✅ A02⚠️ A03❌ ...
```

## Example
/appsec-engineer src/api/ — full OWASP Top 10 review
