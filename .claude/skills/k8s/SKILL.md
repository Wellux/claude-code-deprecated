---
name: k8s
description: >
  Kubernetes deployment manifests, Helm charts, and cluster configuration. Invoke for:
  "Kubernetes", "K8s", "deploy to K8s", "Helm chart", "pod spec", "deployment manifest",
  "kubernetes config", "HPA", "ingress", "K8s security".
argument-hint: application or K8s resource to configure
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Kubernetes — Container Orchestration
**Category:** DevOps/Infra

## Role
Write production-ready Kubernetes manifests with proper resource limits, security contexts, and autoscaling.

## When to invoke
- Deploying to Kubernetes
- K8s manifest review
- Helm chart creation
- "make this K8s-ready"

## Instructions
1. Deployment: replicas, resource limits/requests, liveness/readiness probes
2. Security: non-root securityContext, read-only filesystem, drop capabilities
3. Config: ConfigMap for config, Secrets for credentials (or External Secrets)
4. Networking: Service + Ingress with TLS
5. Autoscaling: HPA with CPU/memory/custom metrics
6. Namespaces: separate prod/staging, RBAC per namespace

## Output format
Complete YAML manifests: Deployment, Service, Ingress, HPA, ConfigMap.

## Example
/k8s create production K8s deployment for the AI API with HPA and TLS ingress
