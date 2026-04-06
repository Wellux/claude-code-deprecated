---
name: api-designer
description: >
  Design clean, consistent REST or GraphQL APIs with OpenAPI specs. Invoke for:
  "design this API", "API spec", "OpenAPI", "REST endpoints", "API review",
  "API versioning", "endpoint design", "HTTP API", "what endpoints do I need".
argument-hint: API or feature to design (e.g. "user authentication API" or "review src/api/")
allowed-tools: Read, Write, Grep, Glob
---

# Skill: API Designer — REST/GraphQL API Design
**Category:** Development

## Role
Design clean, consistent, versioned APIs following REST conventions with proper error handling, auth, and pagination.

## When to invoke
- New API endpoints needed
- API review for consistency
- OpenAPI spec generation
- API versioning strategy

## Instructions
1. Identify resources and operations (CRUD mapping)
2. Design URL structure: `/api/v1/resources/{id}` convention
3. HTTP methods: GET (read), POST (create), PUT (replace), PATCH (update), DELETE
4. Request/response schemas with types
5. Error responses: consistent format, appropriate status codes
6. Auth: Bearer token on protected routes
7. Pagination: cursor-based for large collections
8. Generate OpenAPI 3.0 YAML spec

## Output format
```yaml
openapi: 3.0.0
info:
  title: <API Name>
  version: 1.0.0
paths:
  /api/v1/resources:
    get: ...
    post: ...
```

## Example
/api-designer design CRUD API for prompt templates with auth and pagination
