---
name: test-writer
description: >
  Write comprehensive tests: unit, integration, edge cases. Invoke for: "write tests",
  "add test coverage", "unit test this", "test suite", "TDD", "improve coverage",
  "test cases for", "missing tests", "test this function". Follows AAA pattern,
  targets 80%+ coverage, tests error paths and edge cases.
argument-hint: file or function to test
allowed-tools: Read, Write, Grep, Glob
---

# Skill: Test Writer — Comprehensive Test Suite
**Category:** Development

## Role
Write thorough tests that cover happy paths, error paths, edge cases, and boundary conditions.

## When to invoke
- New code without tests
- "write tests for X"
- Coverage below 80%
- TDD: write tests before implementation

## Instructions
1. Read the code under test — understand all paths
2. Identify: happy path, error paths, edge cases, boundary conditions
3. Follow AAA: Arrange (setup), Act (call), Assert (verify)
4. Mock external dependencies (DB, API, filesystem)
5. Test names: `test_<what>_<when>_<expected>` format
6. Cover: None/null inputs, empty collections, max values, concurrent access

## Output format
Complete test file(s) with:
- All imports
- Fixtures/setup
- One test per scenario
- Docstring for complex test intent

## Example
/test-writer src/llm/claude_client.py — test all methods including error handling
