---
name: logging
description: >
  Set up structured logging, log aggregation, and log analysis. Invoke for:
  "logging setup", "structured logs", "log aggregation", "ELK stack", "log analysis",
  "add logging", "logging config", "how should I log this", "log format".
argument-hint: application or logging system to configure
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Logging — Structured Logging & Aggregation
**Category:** DevOps/Infra

## Role
Implement structured logging that makes debugging, auditing, and monitoring easy.

## When to invoke
- Setting up logging for new service
- "logs aren't useful" / "can't debug from logs"
- Log format standardization
- Log aggregation setup

## Instructions
1. Use structured logging (JSON format) not string concatenation
2. Include: timestamp, level, service, request_id, user_id, message, context
3. Log levels: DEBUG (dev), INFO (events), WARNING (abnormal but handled), ERROR (failures)
4. Never log: passwords, tokens, PII
5. Correlation IDs: trace requests through distributed system
6. Aggregation: configure for ELK or CloudWatch Logs

## Output format
```python
# Logging config
import structlog
log = structlog.get_logger()
log.info("api_call", model="claude-sonnet-4-6", tokens=150, latency_ms=320)
# Output: {"timestamp": "...", "level": "info", "event": "api_call", ...}
```

## Example
/logging set up structured logging for src/llm/ — include request_id, model, latency, tokens
