# ADR 0001: Claude as Primary LLM

**Status:** Accepted
**Date:** 2026-03-28

## Context

This project requires a primary LLM for: autonomous code generation, agentic tool use,
long-context analysis, and multi-step reasoning. We evaluated: Claude (Anthropic), GPT-4o (OpenAI),
Gemini (Google), and Llama 3 (Meta/open-source).

## Decision

Use **claude-sonnet-4-6** as the primary model with claude-opus-4-6 for deep research tasks
and claude-haiku-4-5-20251001 for fast/cheap tasks.

## Reasons

1. **Best agentic performance** — Claude leads on tool use, multi-step planning, and instruction following
2. **Long context** — 200K token context handles entire codebases without chunking
3. **Safety alignment** — built-in refusal of destructive actions matches our hook-based safety model
4. **Claude Code native** — the CLI itself runs on Claude; using the same model reduces friction
5. **Cost efficiency** — sonnet-4-6 offers best capability/cost ratio for day-to-day tasks

## Consequences

- **Positive:** Single SDK (anthropic), consistent behavior, native Claude Code integration
- **Negative:** Vendor dependency on Anthropic; GPT-4o fallback maintained via `GPTClient` for resilience
- **Mitigation:** `LLMClient` abstract interface allows swapping providers without changing call sites

## Alternatives Considered

| Model | Why rejected |
|-------|-------------|
| GPT-4o | Slightly weaker agentic performance; maintained as fallback |
| Gemini 1.5 Pro | Long context good, but tool use less reliable |
| Llama 3 70B | Self-hosted complexity; requires GPU infra; no tool use |
