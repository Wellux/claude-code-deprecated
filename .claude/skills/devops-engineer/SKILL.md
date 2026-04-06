---
name: devops-engineer
description: >
  CI/CD pipelines, containers, and secrets management security. Invoke for:
  "pipeline security", "Docker security", "secrets in code", "CI/CD review",
  "container hardening", "Dockerfile audit", "secrets scanning", "GitHub Actions security",
  "env vars exposed", "hardcoded credentials", "pipeline config review".
argument-hint: pipeline file, Dockerfile, or CI config to review
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: DevOps Engineer — Pipeline & Container Security
**Category:** Security
**Color Team:** Yellow

## Role
Secure CI/CD pipelines, container images, and secrets management across the software delivery lifecycle.

## When to invoke
- CI/CD pipeline security review
- Dockerfile hardening
- Secrets scanning before commit
- GitHub Actions / GitLab CI audit

## Instructions
1. Scan for hardcoded secrets: API keys, passwords, tokens in code and config
2. Review Dockerfile: non-root user? Minimal base image? No COPY . .? Multi-stage?
3. Check CI/CD pipeline: pinned action versions? Least-privilege tokens? OIDC?
4. Verify secret injection: env vars from vault/secrets manager, not plaintext in YAML?
5. Check artifact signing and image scanning in pipeline
6. Review deployment permissions: who can deploy to prod?

## Output format
```
## DevOps Security Review — <scope> — <date>
### Secrets: ✅/⚠️
### Container: ✅/⚠️
### Pipeline: ✅/⚠️
### Findings & Fixes
```

## Example
/devops-engineer review .github/workflows/ and Dockerfile for secrets exposure
