"""File-based persistence — write research, outputs, and decisions to disk."""
from __future__ import annotations

import os
import tempfile
from datetime import datetime
from pathlib import Path

from ..utils.log_index import LogIndex


class FileStore:
    """Structured file storage for research, outputs, and decisions.

    Directory layout (relative to project root):
        data/research/YYYY-MM-DD-<slug>.md    ← research docs
        data/outputs/<type>-YYYY-MM-DD.md     ← generated reports
        tasks/todo.md                          ← task tracking (append)
        tasks/lessons.md                       ← lessons (append)
    """

    def __init__(self, root: str | Path = "."):
        self.root = Path(root)
        self._ensure_dirs()
        self._log = LogIndex(self.root / "data/cache/events.log")

    def _ensure_dirs(self) -> None:
        for d in ["data/research", "data/outputs", "data/cache", "tasks"]:
            (self.root / d).mkdir(parents=True, exist_ok=True)

    # ── Research ──────────────────────────────────────────────────────────────

    def write_research(self, topic: str, content: str) -> Path:
        """Write a research document. Returns the file path."""
        date = datetime.now().strftime("%Y-%m-%d")
        slug = _slugify(topic)
        path = self.root / f"data/research/{date}-{slug}.md"
        _atomic_write(path, content)
        self._index_research(topic, path, date)
        return path

    def _index_research(self, topic: str, path: Path, date: str) -> None:
        index = self.root / "data/research/README.md"
        entry = f"- [{topic}]({path.name}) — {date}\n"
        with open(index, "a", encoding="utf-8") as f:
            f.write(entry)

    def list_research(self) -> list[dict]:
        """Return all research files as [{topic, path, date}]."""
        results = []
        for p in sorted((self.root / "data/research").glob("*.md")):
            if p.name == "README.md":
                continue
            parts = p.stem.split("-", 3)
            date = "-".join(parts[:3]) if len(parts) >= 3 else "unknown"
            topic = parts[3].replace("-", " ") if len(parts) >= 4 else p.stem
            results.append({"topic": topic, "path": str(p), "date": date})
        return results

    # ── Outputs ───────────────────────────────────────────────────────────────

    def write_output(self, output_type: str, content: str) -> Path:
        """Write a generated report/output. Returns the file path."""
        date = datetime.now().strftime("%Y-%m-%d")
        path = self.root / f"data/outputs/{output_type}-{date}.md"
        _atomic_write(path, content)
        return path

    # ── Lessons ───────────────────────────────────────────────────────────────

    def append_lesson(
        self,
        title: str,
        mistake: str,
        why: str,
        rule: str,
        example: str,
    ) -> None:
        """Append a lesson entry to tasks/lessons.md."""
        date = datetime.now().strftime("%Y-%m-%d")
        lessons_path = self.root / "tasks/lessons.md"
        entry = (
            f"\n## Lesson — {date}: {title}\n"
            f"**Mistake:** {mistake}\n"
            f"**Why:** {why}\n"
            f"**Rule:** {rule}\n"
            f"**Example:** {example}\n"
        )
        with open(lessons_path, "a", encoding="utf-8") as f:
            f.write(entry)

    # ── Tasks ─────────────────────────────────────────────────────────────────

    def append_task(self, description: str) -> None:
        """Append an open task to tasks/todo.md."""
        todo_path = self.root / "tasks/todo.md"
        with open(todo_path, "a", encoding="utf-8") as f:
            f.write(f"\n- [ ] {description}")

    def complete_task(self, description: str) -> bool:
        """Mark a task complete in tasks/todo.md. Returns True if found."""
        todo_path = self.root / "tasks/todo.md"
        if not todo_path.exists():
            return False
        text = todo_path.read_text(encoding="utf-8")
        new_text = text.replace(f"- [ ] {description}", f"- [x] {description}", 1)
        if new_text == text:
            return False
        _atomic_write(todo_path, new_text)
        return True

    # ── Cache log ─────────────────────────────────────────────────────────────

    def log_event(self, event: str, **kwargs) -> dict:
        """Append an indexed, structured event to data/cache/events.log.

        Returns the written record so callers can inspect or test it.
        The underlying LogIndex maintains an in-memory reverse index by
        event name and tag for fast search without full-file scans.
        """
        return self._log.append(event, **kwargs)

    def search_log(
        self,
        event: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Search the indexed event log. Returns newest-first."""
        return self._log.search(event=event, tags=tags, limit=limit)

    def log_summary(self) -> dict[str, int]:
        """Return {event_name: count} for all events in the log."""
        return self._log.summary()

    # ── Generic read/write ────────────────────────────────────────────────────

    def read(self, relative_path: str) -> str:
        """Read any file relative to project root."""
        return (self.root / relative_path).read_text(encoding="utf-8")

    def write(self, relative_path: str, content: str) -> Path:
        """Write any file relative to project root."""
        path = self.root / relative_path
        _atomic_write(path, content)
        return path


def _atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically via a temp-file + os.replace.

    Guarantees the target file is never in a partial state: either the old
    content is intact or the new content is fully written, even if the process
    is killed mid-write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _slugify(text: str) -> str:
    """Convert topic to a filesystem-safe slug."""
    import re
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug[:60]
