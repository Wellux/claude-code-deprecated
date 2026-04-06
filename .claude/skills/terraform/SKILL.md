---
name: terraform
description: >
  Write Terraform IaC for cloud infrastructure. Invoke for: "terraform", "IaC",
  "infrastructure as code", "provision cloud resources", "AWS terraform",
  "terraform module", "terraform plan", "cloud infrastructure setup".
argument-hint: infrastructure to provision (e.g. "AWS VPC + ECS + RDS")
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Terraform — Infrastructure as Code
**Category:** DevOps/Infra

## Role
Write clean, modular Terraform configurations for cloud infrastructure with remote state and security best practices.

## When to invoke
- Provisioning cloud infrastructure
- "define this infra as code"
- Terraform module creation
- Infrastructure review

## Instructions
1. Use modules for reusability: vpc, compute, database, monitoring
2. Remote state: S3 + DynamoDB (AWS) or GCS (GCP) for state locking
3. Variables: all configurable values as variables with descriptions
4. Outputs: expose necessary values for other modules
5. Security: no secrets in tfvars, use Vault or AWS SSM
6. Tagging: all resources tagged with environment, project, owner

## Output format
Complete Terraform files: main.tf, variables.tf, outputs.tf, providers.tf

## Example
/terraform create AWS infrastructure: VPC, ECS cluster, RDS PostgreSQL, ALB
