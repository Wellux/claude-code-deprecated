"""Append-only JSONL log with in-memory index and bounded memory.

Writes one JSON object per line to a log file. On first access the file is
scanned to rebuild the in-memory reverse index. Subsequent writes are O(1)
appends. When the in-memory buffer exceeds ``max_entries``, the oldest 25 %
of entries are evicted and the index is rebuilt — amortised O(1) per append.

Usage::

    from src.utils.log_index import LogIndex

    idx = LogIndex("data/cache/events.log", max_entries=50_000)
    idx.append("api_request", method="POST", path="/complete", status=200,
                latency_ms=142, request_id="abc123")
    idx.append("llm_call",    model="claude-sonnet-4-6", tokens=512,
                cost_usd=0.0014)

    # Search (newest-first)
    results = idx.search(event="api_request")
    results = idx.search(tags=["ci"], limit=20)
    results = idx.tail(50)
    summary = idx.summary()
"""
from __future__ import annotations

import json
import threading
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_MAX_ENTRIES = 100_000   # ~100 MB at ~1 KB per record
_EVICT_FRACTION = 0.25           # drop oldest 25 % on overflow


class LogIndex:
    """Thread-safe, bounded append-only JSONL log with in-memory reverse index."""

    def __init__(self, path: str | Path, max_entries: int = _DEFAULT_MAX_ENTRIES) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._max_entries = max_entries

        self._lock = threading.Lock()
        self._event_index: dict[str, list[int]] = defaultdict(list)
        self._tag_index: dict[str, list[int]] = defaultdict(list)
        self._lines: list[dict] = []

        if self.path.exists():
            self._load()

    # ── Write ─────────────────────────────────────────────────────────────────

    def append(self, event: str, **fields: Any) -> dict:
        """Append one log entry. Evicts oldest entries if buffer is full."""
        record: dict[str, Any] = {
            "ts": datetime.now(tz=UTC).isoformat(),
            "event": event,
            **fields,
        }

        with self._lock:
            # Write to disk first (durability before index update)
            with open(self.path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")

            line_no = len(self._lines)
            self._lines.append(record)
            self._event_index[event].append(line_no)
            for tag in _extract_tags(record):
                self._tag_index[tag].append(line_no)

            # Evict oldest quarter when buffer exceeds max to bound memory growth
            if len(self._lines) > self._max_entries:
                self._evict()

        return record

    # ── Search ────────────────────────────────────────────────────────────────

    def search(
        self,
        event: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Return matching records, newest-first, up to *limit*."""
        with self._lock:
            if event and tags:
                event_set = set(self._event_index.get(event, []))
                tag_set: set[int] = set()
                for t in tags:
                    tag_set.update(self._tag_index.get(t, []))
                candidates = sorted(event_set & tag_set, reverse=True)
            elif event:
                candidates = list(reversed(self._event_index.get(event, [])))
            elif tags:
                merged: set[int] = set()
                for t in tags:
                    merged.update(self._tag_index.get(t, []))
                candidates = sorted(merged, reverse=True)
            else:
                candidates = list(range(len(self._lines) - 1, -1, -1))

            return [self._lines[i] for i in candidates[:limit]]

    def tail(self, n: int = 50) -> list[dict]:
        """Return the last *n* entries, oldest-first."""
        with self._lock:
            return list(self._lines[-n:])

    def summary(self) -> dict[str, int]:
        """Return ``{event_name: count}`` for all events in the in-memory buffer."""
        with self._lock:
            return {k: len(v) for k, v in self._event_index.items()}

    def __len__(self) -> int:
        return len(self._lines)

    # ── Internal ──────────────────────────────────────────────────────────────

    def _evict(self) -> None:
        """Drop the oldest 25 % of in-memory entries and rebuild indexes.

        Called holding ``self._lock``. The on-disk file is NOT truncated —
        it acts as a durable archive. Only the in-memory search index shrinks.
        """
        n_drop = max(1, int(len(self._lines) * _EVICT_FRACTION))
        self._lines = self._lines[n_drop:]
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Rebuild event + tag indexes from current ``_lines``. Holds lock."""
        self._event_index = defaultdict(list)
        self._tag_index = defaultdict(list)
        for i, record in enumerate(self._lines):
            self._event_index[record.get("event", "_unknown")].append(i)
            for tag in _extract_tags(record):
                self._tag_index[tag].append(i)

    def _load(self) -> None:
        """Scan disk file and rebuild in-memory index (called once at init)."""
        corrupt = 0
        with open(self.path, encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError:
                    corrupt += 1
                    continue
                self._lines.append(record)

        if corrupt:
            import warnings
            warnings.warn(
                f"LogIndex: skipped {corrupt} corrupt line(s) in {self.path}",
                stacklevel=2,
            )

        # Apply max_entries cap on load too (old log may be very large)
        if len(self._lines) > self._max_entries:
            self._lines = self._lines[-self._max_entries:]

        self._rebuild_index()


def _extract_tags(record: dict) -> list[str]:
    """Pull tag values from a record for the tag index."""
    tags: list[str] = []
    for key in ("tag", "tags", "category", "source"):
        val = record.get(key)
        if isinstance(val, str) and val:
            tags.append(val)
        elif isinstance(val, list):
            tags.extend(v for v in val if isinstance(v, str))
    return tags
