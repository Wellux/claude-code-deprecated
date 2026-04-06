---
name: deploy-checker
description: >
  Pre-deployment checklist and validation. Invoke for: "ready to deploy", "deployment check",
  "pre-prod validation", "deployment checklist", "is this safe to deploy",
  "release validation", "deployment gate".
argument-hint: service or version to validate for deployment
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: Deploy Checker — Pre-Deployment Validation
**Category:** DevOps/Infra

## Role
Run a comprehensive pre-deployment checklist to catch issues before they reach production.

## When to invoke
- Before any production deployment
- Release gate validation
- "is this ready to ship?"

## Instructions
1. Tests: all passing? Coverage adequate?
2. Security: no hardcoded secrets? Dep audit clean? OWASP scan?
3. Performance: no N+1 queries? Response times acceptable?
4. Config: env vars documented? Feature flags set for prod?
5. Database: migrations backward-compatible? Rollback possible?
6. Monitoring: alerts configured? Dashboards ready?
7. Rollback: how do we revert if this goes wrong?

## Output format
```
## Deploy Checklist — <service v{version}> — <date>
- [✅/❌] Tests passing (X/X)
- [✅/❌] Security scan clean
- [✅/❌] No hardcoded secrets
- [✅/❌] DB migration safe
- [✅/❌] Monitoring configured
- [✅/❌] Rollback plan exists
### DEPLOY: ✅ APPROVED / ❌ BLOCKED (reasons)
```

## Example
/deploy-checker validate v2.1.0 is production-ready before deployment
