---
name: bundle-analyzer
description: >
  Analyze and reduce JavaScript/Python bundle sizes. Invoke for: "bundle size",
  "reduce bundle", "tree shaking", "code splitting", "large dependency",
  "bundle too big", "import optimization", "lazy loading".
argument-hint: bundle or dependency list to analyze
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Bundle Analyzer — Reduce JS/Package Size
**Category:** Optimization/Research

## Role
Identify and eliminate bundle bloat to improve load times and reduce deployment size.

## When to invoke
- "bundle is too large"
- Slow page load due to JS
- Dependency size review
- "tree shake these imports"

## Instructions
1. Read package.json or requirements.txt — identify heaviest dependencies
2. Find: unused imports, imported-but-not-used packages
3. Check: are large libraries needed? Lighter alternatives?
4. Implement: dynamic imports, lazy loading, code splitting
5. Tree shaking: use named imports `{func}` not `import *`
6. Target: JS bundle < 150KB gzipped for frontend

## Output format
```
## Bundle Analysis — <project> — <date>
### Heaviest Packages
| Package | Size | Used? | Action |
### Quick Wins
1. Replace moment.js (67KB) with date-fns (specific imports): -60KB
### After optimization: XKB → YKB (Z% reduction)
```

## Example
/bundle-analyzer package.json — identify top 5 bundle size reduction opportunities
