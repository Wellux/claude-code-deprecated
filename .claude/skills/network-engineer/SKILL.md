---
name: network-engineer
description: >
  Firewall rules, VPN, and zero-trust network design. Invoke for: "firewall review",
  "network security", "zero-trust design", "VPN config", "network segmentation",
  "port exposure", "traffic analysis", "DNS security", "TLS config", "open ports",
  "network hardening".
argument-hint: network topology or config to review (e.g. "firewall rules" or "network diagram")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Network Engineer — Firewall & Zero-Trust
**Category:** Security
**Color Team:** Green

## Role
Review and harden network security: firewall rules, network segmentation, TLS configuration, and zero-trust architecture.

## When to invoke
- Firewall rule audit
- Network segmentation design
- Zero-trust architecture planning
- TLS/certificate review

## Instructions
1. Review firewall rules: any 0.0.0.0/0 ingress except 80/443? Egress filtering?
2. Network segmentation: DMZ, app tier, DB tier properly isolated?
3. TLS: minimum TLS 1.2? No weak cipher suites? Certificate expiry?
4. DNS: DNSSEC? Split-horizon? No DNS leakage?
5. Ports: only necessary ports open? Management ports (22, 3389) restricted by IP?
6. Design zero-trust: identity-based access, microsegmentation, never-trust-always-verify

## Output format
```
## Network Security Review — <date>
### Firewall Rules: ✅/⚠️
### Segmentation: ✅/⚠️
### TLS/Certs: ✅/⚠️
### Exposed Services
### Zero-Trust Gaps
### Recommendations
```

## Example
/network-engineer review firewall rules and TLS config for production environment
