---
name: migration
description: >
  Plan and execute safe code or database migrations. Invoke for: "migrate this",
  "upgrade", "migration plan", "database migration", "API migration", "breaking change",
  "version upgrade", "schema migration", "data migration", "move from X to Y".
argument-hint: what to migrate and target version (e.g. "PostgreSQL schema v1→v2")
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Migration — Safe Upgrades & Data Migrations
**Category:** Development

## Role
Plan and execute migrations safely: backup first, staged rollout, rollback plan always included.

## When to invoke
- Database schema changes
- API breaking changes
- Framework or library version upgrades
- Data restructuring

## Instructions
1. **Never migrate without backup plan**
2. Document current state (schema, API contract, data format)
3. Design target state
4. Create migration steps: incremental, reversible where possible
5. Write rollback procedure for each step
6. Test migration on copy of production data first
7. Plan staged rollout: dev → staging → prod

## Output format
```
## Migration Plan — <what> — <date>
### Current State
### Target State
### Steps
  Step 1: [action] — Rollback: [undo action]
  Step 2: ...
### Rollback Procedure
### Testing Checklist
```

## Example
/migration PostgreSQL schema — add user_preferences JSONB column with backfill
