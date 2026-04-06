---
name: ciso
description: >
  Full security orchestration — runs the complete security team as white-team orchestrator.
  Invoke for: "run a security audit", "check everything security", "full security review",
  "CISO review", "security assessment", "what's our security posture", "scan the whole project".
  Coordinates all 16 security sub-skills and produces a consolidated severity-ranked report.
argument-hint: scope (e.g. "full project" or "src/ directory only")
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
---

# Skill: CISO — Chief Information Security Officer
**Category:** Security
**Color Team:** White (Orchestrator)

## Role
Run the full security team: coordinate all 16 security skills and produce a consolidated, severity-ranked security assessment.

## When to invoke
- "run a security audit" / "security assessment"
- "what's our security posture"
- "full security review" before a release
- "check everything" in security context
- As final gate before any production deployment

## Instructions
1. Survey project structure with Glob — identify languages, frameworks, entry points
2. Run appsec-engineer on all source code (OWASP Top 10)
3. Run ai-security on any LLM/agent code
4. Run dep-auditor on requirements.txt / package.json
5. Run grc-analyst on documentation and data handling
6. Run iam-engineer on auth/access patterns
7. Synthesize all findings into a severity matrix: Critical → High → Medium → Low

## Output format
```
## Security Assessment — <date>
### Critical (fix before deploy)
- [CRITICAL] ...

### High
- [HIGH] ...

### Recommendations
1. ...
```

## Example
/ciso full project security review before v2.0 release
