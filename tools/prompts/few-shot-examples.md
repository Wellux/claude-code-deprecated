# Few-Shot Examples Library

Curated input→output pairs for consistent model behavior.
Load these via `FewShotManager` from `src/prompt_engineering/few_shot.py`.

---

## Code Review Examples

**Input:** `def get_user(id): return db.query(f"SELECT * FROM users WHERE id={id}")`
**Output:** CRITICAL: SQL injection. Fix: `db.query("SELECT * FROM users WHERE id=?", (id,))`

**Input:**
```python
def process_items(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result
```
**Output:** MINOR: Use list comprehension. Fix: `return [x * 2 for x in items]`

**Input:**
```python
try:
    data = json.loads(response)
except:
    pass
```
**Output:** MAJOR: Bare except swallows all errors. Fix: `except json.JSONDecodeError as e: logger.error("parse_failed", error=str(e)); raise`

---

## Prompt Classification Examples

**Input:** "make this faster"
**Output:** Algorithm optimization request → invoke /perf-profiler

**Input:** "something is broken in prod"
**Output:** Incident → invoke /incident-response; gather: error message, logs, when it started

**Input:** "add authentication to the API"
**Output:** Feature implementation → invoke /api-designer for design, then /appsec-engineer for security review

**Input:** "what's the state of LLM agents"
**Output:** Research request → invoke /karpathy-researcher with topic "LLM agent frameworks 2026"

---

## Sentiment Classification Examples

**Input:** "The API rate limits are too restrictive and the docs are outdated"
**Output:** negative | issues: rate_limits, documentation

**Input:** "Love the streaming support — makes the UX much smoother"
**Output:** positive | feature: streaming

**Input:** "Does this support async?"
**Output:** neutral | question: async_support

---

## Bug Triage Examples

**Input:** `AttributeError: 'NoneType' object has no attribute 'content'`
**Output:**
```
Root cause: API returned None (e.g., empty response or failed call)
Location: claude_client.py line 64 — message.content[0].text
Fix: Check response before accessing: if not message.content: raise LLMError("Empty response")
Prevention: Add response validation in complete()
```

**Input:** `asyncio.TimeoutError after 30s`
**Output:**
```
Root cause: API call exceeded timeout (likely rate limit or slow model)
Fix: Add timeout parameter to create(): timeout=60.0
Prevention: Monitor p99 latency, add circuit breaker for timeouts > threshold
```

---

## Python Type Annotation Examples

**Input:** `def process(data, config=None): ...`
**Output:** `def process(data: list[dict], config: ProcessConfig | None = None) -> ProcessResult: ...`

**Input:** `def fetch_items(ids, limit=10): ...`
**Output:** `def fetch_items(ids: list[int], limit: int = 10) -> list[Item]: ...`
