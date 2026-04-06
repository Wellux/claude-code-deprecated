---
name: ci-cd
description: >
  Design and optimize CI/CD pipelines for automated testing, building, and deployment.
  Invoke for: "CI/CD pipeline", "GitHub Actions", "GitLab CI", "build pipeline",
  "automate deployment", "continuous integration", "automated testing pipeline",
  "deploy on push", "pipeline config".
argument-hint: pipeline to create or review (e.g. "GitHub Actions for Python project")
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: CI/CD — Continuous Integration & Deployment
**Category:** DevOps/Infra

## Role
Design fast, reliable CI/CD pipelines that automate testing, building, and deployment.

## When to invoke
- New project needs CI/CD
- Slow or unreliable pipeline
- Deployment automation needed
- "automate this deploy"

## Instructions
1. Identify: what to test, build, deploy? What environments (dev/staging/prod)?
2. Design stages: lint → test → build → security scan → deploy
3. Optimize speed: parallel jobs, caching (pip, npm, Docker layers)
4. Security: use OIDC (not long-lived secrets), pin action versions, minimal permissions
5. Write GitHub Actions / GitLab CI YAML
6. Add deployment gates: require passing tests + approval for prod

## Output format
Complete pipeline YAML with comments explaining each step.

## Example
/ci-cd create GitHub Actions pipeline for Python project with test, lint, and deploy to cloud
