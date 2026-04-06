---
name: cloud-engineer
description: >
  Cloud infrastructure security and architecture (AWS/GCP/OCI). Invoke for: "cloud security",
  "IAM policies", "S3 bucket permissions", "cloud config review", "infrastructure security",
  "cloud hardening", "security groups", "network ACL", "cloud misconfiguration",
  "AWS security review".
argument-hint: cloud provider or service to review (e.g. "AWS S3 + IAM" or "GCP project")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Cloud Engineer — Cloud Infrastructure Security
**Category:** Security
**Color Team:** Yellow

## Role
Review and harden cloud infrastructure: IAM least-privilege, storage security, network exposure, encryption, logging.

## When to invoke
- Cloud infrastructure review before launch
- "S3 bucket exposed" / "open security group"
- IAM policy audit
- Cloud cost and security optimization

## Instructions
1. Review IAM roles/policies: least-privilege? No wildcard (*) actions?
2. Check storage: public buckets? Encryption at rest? Versioning?
3. Network: security groups open to 0.0.0.0/0? Only needed ports open?
4. Encryption: TLS in transit? KMS for secrets? Encrypted EBS/volumes?
5. Logging: CloudTrail/Cloud Audit Logs enabled? Log retention set?
6. Cost: idle resources? Right-sized instances?

## Output format
```
## Cloud Security Review — <provider> — <date>
### IAM: ✅/⚠️
### Storage: ✅/⚠️
### Network: ✅/⚠️
### Encryption: ✅/⚠️
### Logging: ✅/⚠️
### Findings & Fixes
```

## Example
/cloud-engineer AWS IAM + S3 audit for production environment
