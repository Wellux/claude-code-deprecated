---
name: a11y-checker
description: >
  Accessibility audit against WCAG 2.1 AA standards. Invoke for: "accessibility",
  "a11y", "WCAG", "screen reader", "aria labels", "color contrast", "keyboard navigation",
  "accessibility audit", "ADA compliance".
argument-hint: HTML file or component to audit
allowed-tools: Read, Edit, Grep, Glob
---

# Skill: Accessibility Checker — WCAG 2.1 AA Compliance
**Category:** Optimization/Research

## Role
Audit web interfaces for WCAG 2.1 AA compliance: color contrast, keyboard navigation, ARIA, semantic HTML.

## When to invoke
- Accessibility audit before launch
- "make this accessible"
- WCAG compliance check
- Screen reader compatibility

## Instructions
1. Color contrast: text must be 4.5:1 (normal) or 3:1 (large text) ratio
2. ARIA: interactive elements have roles, labels, descriptions
3. Keyboard: all actions reachable by keyboard? Tab order logical?
4. Images: all images have alt text (or aria-hidden if decorative)
5. Forms: labels for all inputs, error messages associated
6. Focus: visible focus indicator? Focus management on modal open?
7. Semantic HTML: proper heading hierarchy, lists, landmarks

## Output format
```
## A11y Audit — <component> — <date>
### Critical (WCAG AA violation)
- Missing alt on hero image (1.1.1)
### Serious
### Moderate
### WCAG Coverage: A✅ AA⚠️ AAA➖
```

## Example
/a11y-checker audit index.html — check WCAG 2.1 AA compliance
