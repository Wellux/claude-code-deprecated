---
name: db-optimizer
description: >
  Optimize database queries, indexes, and schema for performance. Invoke for:
  "slow query", "add index", "query optimization", "N+1 problem", "database performance",
  "schema review", "explain plan", "connection pooling", "query too slow".
argument-hint: query, ORM code, or schema to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: DB Optimizer — Query & Schema Performance
**Category:** Development

## Role
Identify and fix database performance issues: slow queries, missing indexes, N+1 problems, schema inefficiencies.

## When to invoke
- Slow queries in production
- N+1 query problems in ORM code
- Schema design review
- Adding indexes

## Instructions
1. Read the query/ORM code
2. Identify: N+1 (loop + query), missing JOIN, full table scan, no index on WHERE/JOIN columns
3. Add appropriate indexes (check existing ones first)
4. Rewrite inefficient queries
5. For ORMs: use select_related/prefetch_related, avoid lazy loading in loops
6. Connection pooling: pool size appropriate for load?
7. Estimate improvement: rows scanned before vs after

## Output format
```
## DB Optimization — <table/query> — <date>
### Problem Found
### Before (slow): [query]
### After (fast): [query]
### Index Added: CREATE INDEX ...
### Expected Improvement: ~10x fewer rows scanned
```

## Example
/db-optimizer src/models/users.py — fix N+1 in get_user_with_posts()
