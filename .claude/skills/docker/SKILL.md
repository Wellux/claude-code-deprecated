---
name: docker
description: >
  Write and optimize Dockerfiles and Docker Compose configurations. Invoke for:
  "Dockerfile", "containerize this", "Docker Compose", "container setup",
  "multi-stage build", "Docker optimization", "container security", "docker image".
argument-hint: application to containerize or Dockerfile to review
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Docker — Container Configuration & Optimization
**Category:** DevOps/Infra

## Role
Write optimized, secure Dockerfiles using multi-stage builds, minimal base images, and non-root users.

## When to invoke
- New application needs containerization
- Dockerfile review or optimization
- Docker Compose setup
- "make this run in Docker"

## Instructions
1. Use minimal base image (python:3.12-slim, node:20-alpine)
2. Multi-stage build: builder stage → runtime stage
3. Non-root user: `RUN useradd -m app && USER app`
4. Layer optimization: COPY requirements.txt first → install → COPY source
5. No secrets in image: use build args or runtime env vars
6. Health check: HEALTHCHECK instruction
7. docker-compose.yml with proper networking and volume mounts

## Output format
Complete Dockerfile + docker-compose.yml with explanatory comments.

## Example
/docker containerize the Python AI project — multi-stage build, non-root, health check
