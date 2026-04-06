---
name: backup
description: >
  Design and verify backup and disaster recovery strategies. Invoke for: "backup strategy",
  "disaster recovery", "backup verification", "restore test", "RTO", "RPO",
  "data loss prevention", "backup schedule", "backup plan".
argument-hint: system or data to protect with backups
allowed-tools: Read, Write, WebSearch
---

# Skill: Backup — Disaster Recovery Strategy
**Category:** DevOps/Infra

## Role
Design backup strategies that meet RTO/RPO requirements and verify they actually work.

## When to invoke
- New system needs backup strategy
- Backup verification
- Disaster recovery planning
- "what's our RTO/RPO"

## Instructions
1. Define: RPO (max data loss acceptable) and RTO (max downtime acceptable)
2. Identify: what data, databases, configs, code (git handles code)
3. 3-2-1 rule: 3 copies, 2 media types, 1 off-site
4. Schedule: daily incremental, weekly full
5. Encryption: encrypt backups at rest and in transit
6. TEST RESTORE: a backup never tested is not a backup
7. Document restore procedure in docs/runbooks/

## Output format
```
## Backup Strategy — <system>
### Data Inventory
### RPO: Xh | RTO: Xh
### Backup Schedule
### Storage: <location + encryption>
### 3-2-1 Compliance: ✅/⚠️
### Restore Test: Last tested <date>
### Restore Runbook: docs/runbooks/restore.md
```

## Example
/backup design backup strategy for PostgreSQL database — RPO 4h, RTO 2h
