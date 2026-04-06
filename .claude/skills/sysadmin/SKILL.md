---
name: sysadmin
description: >
  OS hardening, patch management, and backup verification. Invoke for: "OS hardening",
  "patch status", "backup verification", "cron security", "file permissions audit",
  "system configuration review", "service account review", "log rotation setup",
  "syslog", "server hardening".
argument-hint: system or configuration to review (e.g. "Linux server config" or "cron jobs")
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: SysAdmin — OS Hardening & System Security
**Category:** Security
**Color Team:** Yellow

## Role
Harden operating systems, validate patch levels, verify backup integrity, and secure system configurations.

## When to invoke
- Server hardening review
- Cron job security audit
- File permission review
- Backup and recovery validation

## Instructions
1. Check file permissions: world-writable files? SUID/SGID bits?
2. Review cron jobs: who owns them? What do they execute? Writable scripts?
3. Service accounts: using minimal permissions? No interactive login?
4. Patch levels: OS, packages, kernel — any known CVEs?
5. SSH: root login disabled? Key-only auth? Fail2ban?
6. Backup: recent backup exists? Tested restore? Encrypted?

## Output format
```
## SysAdmin Audit — <system> — <date>
### File Permissions: ✅/⚠️
### Cron Jobs: ✅/⚠️
### Services: ✅/⚠️
### Patches: ✅/⚠️
### Backups: ✅/⚠️
### Findings
```

## Example
/sysadmin review Linux server config, cron jobs, and SSH hardening
