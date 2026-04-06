---
name: api-docs
description: >
  Generate and maintain API documentation. Invoke for: "document this API", "API docs",
  "OpenAPI spec", "Swagger", "endpoint documentation", "API reference",
  "document these endpoints", "API documentation missing".
argument-hint: API code or endpoints to document
allowed-tools: Read, Write, Grep, Glob
---

# Skill: API Docs — API Reference Documentation
**Category:** Documentation

## Role
Generate comprehensive API documentation from code — accurate, with examples for every endpoint.

## When to invoke
- New API endpoints created
- "document this API"
- OpenAPI spec generation
- API reference out of date

## Instructions
1. Read all route handlers, controllers, and models
2. For each endpoint: method, path, auth required, request params/body, response schema, errors
3. Generate OpenAPI 3.0 YAML spec
4. Add examples: real request/response pairs
5. Document errors: what status codes, what error format
6. Keep in sync with code: note which files to update when code changes

## Output format
```yaml
openapi: 3.0.0
paths:
  /api/v1/completions:
    post:
      summary: Generate completion
      security: [{bearerAuth: []}]
      requestBody: ...
      responses:
        200: ...
        400: ...
        401: ...
```

## Example
/api-docs generate OpenAPI spec for all endpoints in src/api/
