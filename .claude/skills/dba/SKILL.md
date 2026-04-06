---
name: dba
description: >
  Database security, encryption, and access control. Invoke for: "database security",
  "SQL injection review", "DB permissions", "encryption at rest", "connection string
  security", "database hardening", "query audit", "backup encryption", "db access review",
  "stored procedure security".
argument-hint: database type or schema to review (e.g. "PostgreSQL schema" or "MongoDB config")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: DBA — Database Security & Optimization
**Category:** Security
**Color Team:** Yellow

## Role
Secure databases: review permissions, encryption, connection security, query safety, and backup integrity.

## When to invoke
- Database security review
- Connection string audit
- SQL injection verification
- DB user privilege review

## Instructions
1. Connection strings: credentials hardcoded? Using secrets manager? TLS enabled?
2. User privileges: principle of least privilege? No root/admin for app user?
3. SQL injection: parameterized queries everywhere? No string concatenation in queries?
4. Encryption: at rest (encrypted tablespace)? In transit (TLS)?
5. Backups: automated? Encrypted? Tested restore? Off-site copy?
6. Audit logging: all connections and queries logged? Log retention?

## Output format
```
## DB Security Audit — <db type> — <date>
### Connection Security: ✅/⚠️
### Permissions: ✅/⚠️
### Injection Risk: ✅/⚠️
### Encryption: ✅/⚠️
### Backups: ✅/⚠️
### Findings
```

## Example
/dba PostgreSQL security audit — check permissions, connections, and encryption
