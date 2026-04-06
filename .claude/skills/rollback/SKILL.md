---
name: rollback
description: >
  Execute or plan a deployment rollback. Invoke for: "rollback", "revert deployment",
  "undo deploy", "something broke in prod", "roll back to previous version",
  "deployment failed", "revert to v{version}".
argument-hint: what to rollback and target version
allowed-tools: Read, Write, Bash, Grep
---

# Skill: Rollback — Emergency Deployment Revert
**Category:** DevOps/Infra

## Role
Execute rapid, safe rollbacks when deployments cause production issues.

## When to invoke
- Production issue after deployment
- "roll back to previous version"
- Deployment causing errors

## Instructions
1. STOP: pause ongoing deployment if still in progress
2. Assess: what's broken? What changed? Is rollback needed or can we hotfix faster?
3. Rollback options: previous Docker image, git revert, DB migration rollback
4. Database: if migration was destructive, rollback is harder — follow migration rollback plan
5. Verify: after rollback, confirm issue is resolved
6. Incident report: document timeline, root cause, prevention

## Output format
```
## Rollback Plan — <service> — <date>
### Issue: <what's broken>
### Rollback Target: v{previous}
### Steps (in order)
1. ...
### Estimated Time: Xmin
### Verification: <how to confirm rollback worked>
### Post-Rollback: update incident report
```

## Example
/rollback revert API service to v2.0.3 — v2.1.0 causing 500 errors on /api/completions
