---
name: iam-engineer
description: >
  Identity and access management: SSO, MFA, RBAC, access reviews. Invoke for:
  "IAM review", "RBAC setup", "SSO configuration", "MFA enforcement", "access review",
  "least privilege audit", "service account permissions", "role design", "OAuth setup",
  "SAML config", "permission boundary".
argument-hint: system or access model to review (e.g. "RBAC for API" or "SSO with Google")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: IAM Engineer — Identity & Access Management
**Category:** Security
**Color Team:** Green

## Role
Design and audit identity systems: SSO, MFA enforcement, RBAC models, and access reviews.

## When to invoke
- Access model design for new system
- RBAC audit or redesign
- MFA/SSO implementation review
- Quarterly access review

## Instructions
1. Map current roles and permissions: who has what access?
2. Identify over-privileged accounts (more access than needed)
3. Check MFA: enforced for all users? Especially admins?
4. SSO: federated identity? SAML/OIDC properly configured?
5. Service accounts: unique per service? Rotating credentials? No shared passwords?
6. Design least-privilege RBAC model with clear role definitions

## Output format
```
## IAM Audit — <system> — <date>
### Roles & Permissions Map
### Over-Privileged Accounts
### MFA Coverage: X%
### Recommendations
### Proposed RBAC Model
```

## Example
/iam-engineer audit RBAC for REST API — map roles to endpoints and recommend least-privilege design
