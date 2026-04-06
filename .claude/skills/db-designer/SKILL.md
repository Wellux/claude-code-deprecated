---
name: db-designer
description: >
  Design normalized, production-ready database schemas from requirements.
  Invoke for: "design database schema", "data model", "entity relationship",
  "ER diagram", "normalize tables", "design tables", "create schema",
  "database design review", "foreign keys", "relational model", "schema planning".
argument-hint: feature requirements or domain description to model
allowed-tools: Read, Write, Edit, Bash
---

# Skill: Database Designer

## Mission
Turn requirements into a production-ready, normalized relational schema with
correct constraints, indexes, and migration-safe design decisions.

## Process

### 1. Gather Requirements
- Identify all entities from the domain description
- List key relationships (1:1, 1:N, M:N)
- Identify natural vs surrogate keys
- Flag any time-series, hierarchical, or polymorphic patterns

### 2. Design Schema
- Start with 3NF (Third Normal Form) — denormalize only for proven perf needs
- Every table gets a surrogate PK (`id UUID` or `id BIGSERIAL`)
- Explicit `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ` on mutable tables
- Foreign keys with explicit `ON DELETE` actions
- Soft deletes via `deleted_at TIMESTAMPTZ` when audit trail needed

### 3. Index Strategy
- PK index: automatic
- FK columns: always indexed
- Query predicates: index columns that appear in `WHERE`, `ORDER BY`, `GROUP BY`
- Unique constraints: wherever business rules require uniqueness
- Partial indexes: for nullable columns and soft-delete patterns

### 4. Output Format

```sql
-- ── <entity_name> ─────────────────────────────────────────────────
CREATE TABLE <entity_name> (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- business columns
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_<entity>_<col> ON <entity_name>(<col>);
```

Also produce an ASCII ER diagram:

```
users          ──< orders        ──< order_items >── products
(id, email)       (id, user_id)     (id, qty, price)   (id, sku)
```

### 5. Migration File (Alembic or raw SQL)
- Wrap in a transaction
- Idempotent: `CREATE TABLE IF NOT EXISTS`
- Down migration included

### 6. Review Checklist
- [ ] All FK relationships have an index
- [ ] No nullable columns where NOT NULL is enforceable
- [ ] Timestamps are timezone-aware (`TIMESTAMPTZ`)
- [ ] No EAV anti-patterns (key/value tables for typed data)
- [ ] JSONB used only for truly variable schemas, not as a lazy shortcut
- [ ] Enum types instead of magic strings for low-cardinality columns
- [ ] Row-level security considered for multi-tenant tables

## Common Patterns

### Soft Delete
```sql
deleted_at TIMESTAMPTZ,
-- query: WHERE deleted_at IS NULL
-- index: CREATE INDEX idx_<t>_active ON <t>(deleted_at) WHERE deleted_at IS NULL;
```

### Audit Log
```sql
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    table_name  TEXT NOT NULL,
    record_id   UUID NOT NULL,
    operation   TEXT NOT NULL CHECK (operation IN ('INSERT','UPDATE','DELETE')),
    old_data    JSONB,
    new_data    JSONB,
    actor_id    UUID REFERENCES users(id),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### M:N Junction Table
```sql
CREATE TABLE user_roles (
    user_id  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id  UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```

### Hierarchical (Closure Table)
```sql
CREATE TABLE category_path (
    ancestor_id   UUID NOT NULL REFERENCES categories(id),
    descendant_id UUID NOT NULL REFERENCES categories(id),
    depth         INTEGER NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
);
```

## Anti-Patterns to Avoid
- No "status" columns as bare integers — use CHECK constraints or enum types
- No comma-separated IDs in a single column — use a junction table
- No storing computed values without materialized views or triggers
- No `CHAR(n)` — use `TEXT` or `VARCHAR(n)` as needed
- No unconstrained `TEXT` where length is bounded and known

## Example Invocation

**Prompt:** "Design the schema for a multi-tenant SaaS app with users, teams, API keys, and usage billing."

**Output structure:**
1. ER diagram (ASCII)
2. `CREATE TABLE` statements with constraints
3. Index definitions
4. Migration file skeleton
5. Notes on tenant isolation strategy (row-level security vs schema-per-tenant)
