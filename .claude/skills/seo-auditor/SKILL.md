---
name: seo-auditor
description: >
  SEO audit and optimization. Invoke for: "SEO audit", "improve SEO", "search ranking",
  "meta tags", "structured data", "sitemap", "robots.txt", "keyword optimization",
  "Google ranking", "on-page SEO".
argument-hint: page or site to audit
allowed-tools: Read, Edit, Grep, Glob, WebSearch
---

# Skill: SEO Auditor — Search Engine Optimization
**Category:** Optimization/Research

## Role
Audit and improve SEO: meta tags, structured data, content quality, technical SEO.

## When to invoke
- "improve our search ranking"
- New pages need SEO
- Technical SEO audit
- Content optimization

## Instructions
1. Title: unique, 50-60 chars, keyword first
2. Meta description: compelling, 150-160 chars, includes CTA
3. Heading hierarchy: one H1, logical H2/H3 structure
4. Structured data: relevant schema.org markup
5. Images: descriptive alt text, optimized file size, lazy loading
6. Internal links: relevant anchor text
7. sitemap.xml and robots.txt correct

## Output format
```
## SEO Audit — <page> — <date>
### Title: ✅/⚠️ (issue)
### Meta Description: ✅/⚠️
### Headings: ✅/⚠️
### Structured Data: ✅/⚠️
### Images: ✅/⚠️
### Fixes (priority order)
```

## Example
/seo-auditor audit index.html — optimize for "AI solutions for businesses" keyword
