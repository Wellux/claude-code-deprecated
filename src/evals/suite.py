"""EvalSuite — a named collection of EvalCases with filtering and loading."""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from .types import EvalCase


class EvalSuite:
    """A named, ordered collection of EvalCases."""

    def __init__(self, name: str, cases: list[EvalCase] | None = None) -> None:
        self.name = name
        self._cases: list[EvalCase] = list(cases or [])

    # ── building ──────────────────────────────────────────────────────────────

    def add(self, case: EvalCase) -> EvalSuite:
        """Add a case; returns self for chaining."""
        if any(c.id == case.id for c in self._cases):
            raise ValueError(f"Duplicate EvalCase id: {case.id!r}")
        self._cases.append(case)
        return self

    def extend(self, cases: list[EvalCase]) -> EvalSuite:
        for c in cases:
            self.add(c)
        return self

    # ── filtering ─────────────────────────────────────────────────────────────

    def filter_tags(self, *tags: str) -> EvalSuite:
        """Return a new suite with only cases that have ALL given tags."""
        matched = [c for c in self._cases if all(t in c.tags for t in tags)]
        return EvalSuite(f"{self.name}[{','.join(tags)}]", matched)

    def filter_ids(self, *ids: str) -> EvalSuite:
        id_set = set(ids)
        matched = [c for c in self._cases if c.id in id_set]
        return EvalSuite(self.name, matched)

    def exclude_tags(self, *tags: str) -> EvalSuite:
        matched = [c for c in self._cases if not any(t in c.tags for t in tags)]
        return EvalSuite(self.name, matched)

    # ── serialisation ─────────────────────────────────────────────────────────

    @classmethod
    def from_jsonl(cls, path: str | Path, name: str | None = None) -> EvalSuite:
        """Load cases from a JSONL file (one JSON object per line)."""
        path = Path(path)
        suite_name = name or path.stem
        cases = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            data = json.loads(line)
            cases.append(EvalCase(**data))
        suite = cls(suite_name)
        suite.extend(cases)
        return suite

    def to_jsonl(self, path: str | Path) -> Path:
        """Persist all cases to a JSONL file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        for c in self._cases:
            lines.append(json.dumps({
                "id": c.id, "prompt": c.prompt, "expected": c.expected,
                "contains": c.contains, "excludes": c.excludes,
                "max_tokens": c.max_tokens, "temperature": c.temperature,
                "tags": c.tags, "metadata": c.metadata,
            }))
        path.write_text("\n".join(lines) + "\n")
        return path

    # ── iteration / access ────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[EvalCase]:
        return iter(self._cases)

    def __len__(self) -> int:
        return len(self._cases)

    def __getitem__(self, case_id: str) -> EvalCase:
        for c in self._cases:
            if c.id == case_id:
                return c
        raise KeyError(case_id)

    def __repr__(self) -> str:
        return f"EvalSuite({self.name!r}, {len(self._cases)} cases)"
