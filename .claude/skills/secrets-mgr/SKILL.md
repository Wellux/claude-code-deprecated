---
name: secrets-mgr
description: >
  Manage secrets and credentials securely. Invoke for: "secrets management", "API key storage",
  "secrets vault", "credential rotation", "no hardcoded secrets", "HashiCorp Vault",
  "AWS Secrets Manager", "env vars", "how to store secrets", "rotate credentials".
argument-hint: secrets system to set up or audit
allowed-tools: Read, Write, Grep, Glob, WebSearch
---

# Skill: Secrets Manager — Secure Credential Management
**Category:** DevOps/Infra

## Role
Implement secure secrets management: never hardcoded, rotation enabled, audit trail, least-privilege access.

## When to invoke
- "where should I store API keys"
- Secrets found in code
- Credential rotation needed
- Setting up secrets management for new project

## Instructions
1. Audit: scan for hardcoded secrets with `grep -r "sk-" / "password ="` etc.
2. Choose: AWS Secrets Manager, HashiCorp Vault, or .env + gitignored (dev only)
3. Inject at runtime: environment variables or secrets mount — never baked in image
4. Rotation: automate key rotation, never single-use credentials shared across services
5. Access: least-privilege access per service (service A can't read service B's secrets)
6. Audit log: who accessed what secret and when

## Output format
```
## Secrets Management Setup
### Secrets Found in Code (MUST FIX)
### Chosen Store: <Vault/AWS SM/env>
### Migration Steps
### Rotation Schedule
### Access Matrix
```

## Example
/secrets-mgr audit codebase for hardcoded secrets and design proper secrets management
