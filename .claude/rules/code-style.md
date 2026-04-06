# Code Style Rules

Enforced for all Python code in this project.

## Formatting
- Line length: 100 characters max (ruff enforced)
- Indentation: 4 spaces, no tabs
- Trailing whitespace: none
- End of file: single newline

## Imports
- Standard library first, third-party second, local third (ruff I-sorted)
- No wildcard imports (`from x import *`)
- Lazy imports inside functions when avoiding circular deps or optional deps

## Naming
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix `_`, never double-underscore except dunder methods
- Avoid single-letter names except `i`, `j`, `k` in tight loops; never `l`, `O`, `I`

## Type Annotations
- All public function signatures must be annotated
- Use `str | None` over `Optional[str]` (Python 3.10+ union syntax)
- Use `from __future__ import annotations` at top of every module

## Functions
- Max 40 lines per function; extract helpers if longer
- Single responsibility: one function does one thing
- No mutable default arguments (`def f(x=[])` is forbidden)
- Prefer early returns over nested conditionals

## Classes
- `@dataclass` for data-holding classes; plain class for behaviour
- No logic in `__init__` beyond assignment
- `__repr__` required on any class that appears in logs

## Error Handling
- Catch specific exceptions, never bare `except:`
- Log errors with structured context before re-raising or returning error values
- Never swallow exceptions silently

## Comments
- Code should be self-documenting; comments explain *why*, not *what*
- No commented-out code committed to main
- Docstrings: Google style, required on public classes and functions
