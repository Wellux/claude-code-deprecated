---
name: type-safety
description: >
  Add or fix type annotations and enforce strict type safety. Invoke for: "add types",
  "type annotation", "TypeScript types", "Python type hints", "mypy", "tsc strict",
  "type errors", "any type", "unsafe cast", "missing types", "type this".
argument-hint: file or codebase to add types to
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Skill: Type Safety — Add Types & Fix Errors
**Category:** Development

## Role
Add complete type annotations and fix type errors to enable strict static analysis.

## When to invoke
- Codebase lacks type annotations
- mypy / tsc strict reporting errors
- "add types to this"
- Before enabling strict mode

## Instructions
1. Read all files in scope
2. For Python: add type hints to all function signatures, variables, and class attributes
3. For TypeScript: eliminate all `any`, add proper interfaces
4. Run type checker: `mypy --strict` or `tsc --strict`
5. Fix all errors systematically
6. Add `py.typed` marker (Python) or update `tsconfig.json` (TS)

## Output format
Show typed version of each function:
```python
# Before
def process(data, config):
    ...

# After
def process(data: dict[str, Any], config: Config) -> ProcessResult:
    ...
```

## Example
/type-safety src/llm/ — add full type annotations and fix mypy errors
