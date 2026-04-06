---
name: infra-docs
description: >
  Document infrastructure: architecture diagrams, runbooks, network maps. Invoke for:
  "document the infrastructure", "infra diagram", "network diagram", "runbook",
  "ops documentation", "infrastructure documentation", "how does our infra work".
argument-hint: infrastructure to document
allowed-tools: Read, Write, Glob
---

# Skill: Infra Docs — Infrastructure Documentation
**Category:** DevOps/Infra

## Role
Produce clear, current infrastructure documentation that enables any engineer to understand and operate the system.

## When to invoke
- New infrastructure needs documentation
- Runbook creation
- "document how this all works"
- Onboarding new ops engineers

## Instructions
1. Read all infrastructure config (Terraform, K8s, docker-compose, CI/CD)
2. Create ASCII infrastructure diagram showing: components, connections, data flows
3. Document: environments (dev/staging/prod), access methods, key configs
4. Write runbooks for: deployment, rollback, incident response, scaling
5. Save to docs/runbooks/ and docs/architecture.md

## Output format
```
## Infrastructure Documentation
### Architecture Diagram (ASCII)
### Components
### Environments
### Access Guide
### Runbook Links
```

## Example
/infra-docs document the complete infrastructure for this project
