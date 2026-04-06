---
name: error-handler
description: >
  Design robust error handling, retry logic, and circuit breakers. Invoke for:
  "error handling", "exception handling", "retry logic", "circuit breaker",
  "graceful degradation", "error messages", "fallback", "resilience",
  "fault tolerance", "what happens on failure".
argument-hint: component or error scenario to handle (e.g. "API client error handling")
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Error Handler — Resilient Error Patterns
**Category:** Development

## Role
Design and implement resilient error handling: retry with backoff, circuit breakers, graceful degradation, clear error messages.

## When to invoke
- External API calls without retry
- No fallback on service failure
- Generic exception catching
- "what happens if X fails"

## Instructions
1. Identify all failure points: external calls, DB, filesystem, memory
2. For transient failures: implement retry with exponential backoff + jitter
3. For persistent failures: circuit breaker pattern (open/half-open/closed)
4. User-facing errors: clear message, no stack traces, actionable next steps
5. Logging: log errors with context (request ID, user ID, timestamp)
6. Fallback: degraded mode when dependency unavailable?

## Output format
Implementation with:
- Custom exception hierarchy
- Retry decorator with backoff
- Circuit breaker class
- Error response format

## Example
/error-handler src/llm/claude_client.py — add retry + circuit breaker for API calls
