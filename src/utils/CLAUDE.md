# src/utils — Utilities Context

## Purpose
Shared infrastructure: structured JSON logging and indexed event log.

## Files

### `logger.py`
Structured JSON logger using Python's `logging` module with a custom `_StructuredFormatter`.

```python
from src.utils.logger import get_logger
log = get_logger("component")
log.info("event_name", key="value", count=42)  # → JSON line to stdout
log.error("failed", error=str(e))
```

**Critical:** `_STDLIB_KEYS` is seeded from BOTH a real `LogRecord()` instance AND `LogRecord.__dict__`.
This prevents instance attrs like `exc_info` from leaking into `json.dumps`.
Do NOT pass `exc_info=True` as a kwarg — call `log.error("msg")` inside an `except` block instead.

### `log_index.py`
Append-only JSONL event log with in-memory inverted index for fast tag/event queries.

```python
from src.utils.log_index import LogIndex
idx = LogIndex(path)
idx.append({"event": "startup", "tag": "system", "msg": "..."})
results = idx.query(event="startup")
results = idx.query(tag="system")
```

- Max 100,000 entries; FIFO 25% eviction when full (amortized O(1))
- Corrupt lines skipped with `UserWarning` (no crash)
- CLI: `ccm logs [--event E] [--tag T]`

## Tests
`tests/test_utils_logger.py` — 8 tests covering Logger methods + exc_info formatter branch
`tests/test_log_index.py` — covers eviction, corrupt lines, load cap, tag indexing
