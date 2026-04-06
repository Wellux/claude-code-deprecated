---
name: ui-ux
description: >
  Generate production-level UI/UX designs and code without endless iteration. Invoke for:
  "design this UI", "build this interface", "UI component", "make this look good",
  "design system", "UI/UX", "frontend design", "CSS design", "clean UI".
  Inspired by UI UX Pro Max (nextlevelbuilder) skill patterns.
argument-hint: UI component or page to design
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: UI/UX Pro Max — Production UI Without Endless Iteration
**Category:** Ecosystem
**Inspired by:** nextlevelbuilder/ui-ux-pro-max-skill

## Role
Generate clean, production-level UI code and UX patterns on the first attempt — no endless iteration required.

## When to invoke
- Building new UI components
- "make this look professional"
- Design system setup
- "clean up this UI"

## UI Design Principles (applied automatically)
1. **8px grid**: all spacing in multiples of 8px
2. **Design tokens**: CSS custom properties for colors, spacing, typography
3. **Component isolation**: each component is self-contained
4. **Mobile first**: base styles for mobile, enhance for desktop
5. **Accessibility**: semantic HTML, ARIA, focus states
6. **Performance**: no layout thrashing, GPU-composited animations only

## Instructions
1. Read existing design tokens / CSS variables if any
2. Design component: layout, typography, color, interaction states
3. Implement: semantic HTML + CSS custom properties
4. Include: hover, focus, active, disabled states
5. Test: does it work on mobile? Accessible by keyboard?

## Output format
Complete HTML + CSS with design tokens:
```html
<!-- Component with design tokens -->
<style>
:root { --color-primary: #...; --spacing-4: 32px; }
</style>
```

## Example
/ui-ux design a clean skills directory card component with hover state and accessibility
