---
name: query-optimizer
description: >
  Optimize database queries for speed and efficiency. Invoke for: "slow query",
  "optimize SQL", "query performance", "explain plan", "index missing",
  "full table scan", "N+1", "query taking too long".
argument-hint: SQL query or ORM code to optimize
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Query Optimizer — SQL & ORM Performance
**Category:** Optimization/Research

## Role
Transform slow queries into fast ones through indexing, query rewriting, and ORM optimization.

## When to invoke
- Slow database queries
- "this query takes Xs"
- EXPLAIN PLAN shows full table scan
- N+1 queries in ORM code

## Instructions
1. Read the query — understand what it's doing
2. EXPLAIN: identify full table scans, sort operations, temporary tables
3. Add indexes on: WHERE columns, JOIN columns, ORDER BY columns
4. Rewrite: avoid SELECT *, use covering indexes, reduce JOINs
5. ORM: use eager loading (select_related/include), avoid lazy loading in loops
6. Cache: can result be cached? How often does data change?

## Output format
```sql
-- Before (slow: full table scan, 5s)
SELECT * FROM users WHERE email LIKE '%@example.com%';

-- After (fast: index scan, 10ms)
CREATE INDEX idx_users_domain ON users(email text_pattern_ops);
SELECT id, name, email FROM users WHERE email LIKE '@example.com%';

-- Expected: 500x improvement
```

## Example
/query-optimizer this SQL query: SELECT * FROM logs WHERE created_at > '2026-01-01' ORDER BY user_id
