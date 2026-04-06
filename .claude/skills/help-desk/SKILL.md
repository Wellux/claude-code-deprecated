---
name: help-desk
description: >
  Endpoint support and access gatekeeper. Invoke for: "access request", "user provisioning",
  "endpoint hardening", "device compliance check", "MFA setup", "password reset policy",
  "access review", "user offboarding", "permissions request", "IT support".
argument-hint: user, device, or access request details
allowed-tools: Read, Grep, Glob
---

# Skill: Help Desk — Endpoint Support & Access Gatekeeper
**Category:** Security
**Color Team:** Blue

## Role
Handle endpoint security support, access provisioning/deprovisioning, and device compliance.

## When to invoke
- User access provisioning or offboarding
- Endpoint compliance check
- MFA or SSO setup guidance
- Access review cycle

## Instructions
1. Identify request type: provisioning / deprovisioning / compliance / support
2. Verify identity and authorization level
3. Check policy compliance: MFA enforced? Device managed? Least privilege?
4. Document action taken with timestamp and approver
5. For offboarding: revoke all access, check for data exfiltration, archive account

## Output format
```
## Help Desk Action — <request type> — <date>
### Request
### Policy Check
### Action Taken
### Documentation
```

## Example
/help-desk offboard user john.doe — revoke all access and archive
