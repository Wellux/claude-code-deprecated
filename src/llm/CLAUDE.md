# src/llm — LLM Client Layer Context

## Purpose
Thin async wrappers around Claude (Anthropic) and optionally GPT (OpenAI) APIs.

## Files
- `claude_client.py` — `ClaudeClient` async wrapper; `complete(prompt, model, max_tokens) -> str`
- `gpt_client.py` — `GPTClient` async wrapper (optional dep; graceful ImportError if openai missing)

## ClaudeClient
```python
from src.llm.claude_client import ClaudeClient
client = ClaudeClient(api_key=os.environ["ANTHROPIC_API_KEY"])
response = await client.complete("Hello", model="claude-sonnet-4-6", max_tokens=256)
```

## Model IDs (2026)
| Alias | Model ID |
|-------|----------|
| opus  | `claude-opus-4-6` |
| sonnet | `claude-sonnet-4-6` (default) |
| haiku | `claude-haiku-4-5-20251001` |

## Key rules
- All LLM calls are async — use `await`
- Always wrap in `asyncio.wait_for(..., timeout=30.0)` in eval/batch contexts
- On `APIError` from anthropic SDK → surface as HTTP 502 in the API layer
- GPT client import is guarded: `try: from openai import ... except ImportError: pass`

## Security
- API key from `ANTHROPIC_API_KEY` env var — never hardcoded, never logged
- `max_tokens` floor enforced in routing layer (`llm_router.py`) to prevent 0-token requests
