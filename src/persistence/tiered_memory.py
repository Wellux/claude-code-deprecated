"""Tiered memory system: hot / warm / glacier.

Three-tier architecture inspired by cog (marciopuga) and thebrain (Advenire-Consulting):
- Hot  (<50 lines, loaded every session via session-start hook)
- Warm (domain-specific, loaded on context activation)
- Glacier (archived YAML-frontmatter entries, indexed and searched on demand)

Usage::

    from src.persistence.tiered_memory import TieredMemory

    mem = TieredMemory()
    mem.write_hot("active_branch", "claude/optimize-cli-autonomy-xNamK")
    mem.write_warm("architecture", "# Architecture\\n...")
    mem.archive_glacier("bug-fix-2026-04", "Fixed exc_info leak in logger", tags=["bug", "logger"])
    results = mem.search_glacier("logger")
"""

from __future__ import annotations

import re
import textwrap
from datetime import datetime
from pathlib import Path

_BASE = Path(__file__).resolve().parents[2]
_MEMORY_ROOT = _BASE / ".claude" / "memory"
_HOT_FILE = _MEMORY_ROOT / "hot" / "hot-memory.md"
_WARM_DIR = _MEMORY_ROOT / "warm"
_GLACIER_DIR = _MEMORY_ROOT / "glacier"

_HOT_MAX_LINES = 50

# Cache compiled hot-key patterns to avoid recompilation on every write_hot call
_hot_key_patterns: dict[str, re.Pattern[str]] = {}


class TieredMemory:
    """File-based three-tier memory: hot, warm, glacier."""

    def __init__(self, base: Path | None = None) -> None:
        self._root = (base or _MEMORY_ROOT).resolve()
        self._hot_file = self._root / "hot" / "hot-memory.md"
        self._warm_dir = self._root / "warm"
        self._glacier_dir = self._root / "glacier"
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for d in (self._hot_file.parent, self._warm_dir, self._glacier_dir):
            d.mkdir(parents=True, exist_ok=True)

    # ── Hot tier ──────────────────────────────────────────────────────────────

    def read_hot(self) -> str:
        """Return current hot-memory content (≤50 lines)."""
        if not self._hot_file.exists():
            return ""
        return self._hot_file.read_text()

    def write_hot(self, key: str, value: str) -> None:
        """Update or insert a key: value line in hot-memory under ## Active Context.

        If the hot file grows beyond _HOT_MAX_LINES, oldest active-context lines
        are evicted to warm tier automatically.
        """
        content = self.read_hot()
        lines = content.splitlines()

        # Replace existing key or append
        new_line = f"- **{key}**: {value}"
        if key not in _hot_key_patterns:
            _hot_key_patterns[key] = re.compile(rf"^- \*\*{re.escape(key)}\*\*:")
        pattern = _hot_key_patterns[key]
        replaced = False
        new_lines = []
        for ln in lines:
            if pattern.match(ln):
                new_lines.append(new_line)
                replaced = True
            else:
                new_lines.append(ln)
        if not replaced:
            # Insert under ## Active Context section
            result = []
            in_section = False
            inserted = False
            for ln in new_lines:
                result.append(ln)
                if ln.startswith("## Active Context"):
                    in_section = True
                elif in_section and not inserted and (ln.startswith("##") or ln == ""):
                    result.insert(len(result) - 1, new_line)
                    inserted = True
                    in_section = False
            if not inserted:
                result.append(new_line)
            new_lines = result

        # Update last-modified timestamp
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_lines = [
            f"**Last Updated**: {ts}" if ln.startswith("**Last Updated**") else ln
            for ln in new_lines
        ]

        # Evict if over limit
        if len(new_lines) > _HOT_MAX_LINES:
            self._evict_hot_to_warm(new_lines)
        else:
            self._hot_file.write_text("\n".join(new_lines) + "\n")

    def _evict_hot_to_warm(self, lines: list[str]) -> None:
        """Move oldest active-context lines to warm tier to stay under limit."""
        eviction_target = self._warm_dir / "evicted-from-hot.md"

        # Find active-context lines beyond the first 10
        active_section = False
        active_lines: list[tuple[int, str]] = []
        for i, ln in enumerate(lines):
            if ln.startswith("## Active Context"):
                active_section = True
            elif active_section and ln.startswith("##"):
                break
            elif active_section and ln.startswith("- "):
                active_lines.append((i, ln))

        # Evict oldest half of active-context lines
        evict_count = max(1, len(active_lines) // 2)
        evict_indices = {idx for idx, _ in active_lines[:evict_count]}
        evict_content = "\n".join(ln for _, ln in active_lines[:evict_count])

        # Write evicted lines to warm
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with eviction_target.open("a") as f:
            f.write(f"\n## Evicted {ts}\n{evict_content}\n")

        # Remove evicted lines from hot
        new_lines = [ln for i, ln in enumerate(lines) if i not in evict_indices]
        self._hot_file.write_text("\n".join(new_lines) + "\n")

    # ── Warm tier ─────────────────────────────────────────────────────────────

    def read_warm(self, domain: str) -> str:
        """Return warm-tier content for a named domain."""
        path = self._warm_dir / f"{domain}.md"
        return path.read_text() if path.exists() else ""

    def write_warm(self, domain: str, content: str) -> None:
        """Write or replace a warm-tier domain file."""
        path = self._warm_dir / f"{domain}.md"
        path.write_text(content)

    def append_warm(self, domain: str, content: str) -> None:
        """Append content to a warm-tier domain file."""
        path = self._warm_dir / f"{domain}.md"
        with path.open("a") as f:
            f.write("\n" + content + "\n")

    def list_warm_domains(self) -> list[str]:
        """Return list of warm domain names (without .md extension)."""
        return [p.stem for p in self._warm_dir.glob("*.md")]

    # ── Glacier tier ──────────────────────────────────────────────────────────

    def archive_glacier(
        self,
        slug: str,
        content: str,
        *,
        tags: list[str] | None = None,
        title: str | None = None,
    ) -> Path:
        """Archive content to glacier with YAML frontmatter for indexing.

        Returns the path of the created file.
        """
        ts = datetime.now()
        date_str = ts.strftime("%Y-%m-%d")
        time_str = ts.strftime("%H:%M:%S")
        tags_yaml = ", ".join(tags or [])
        file_title = title or slug.replace("-", " ").title()
        filename = f"{date_str}-{slug}.md"
        path = self._glacier_dir / filename

        frontmatter = textwrap.dedent(f"""\
            ---
            title: {file_title}
            date: {date_str}
            time: {time_str}
            tags: [{tags_yaml}]
            slug: {slug}
            ---
            """)
        path.write_text(frontmatter + "\n" + content + "\n")
        return path

    def search_glacier(self, query: str, *, limit: int = 20) -> list[dict]:
        """Search glacier archives by keyword in frontmatter tags, title, or content.

        Args:
            query: Keyword to search for (case-insensitive).
            limit: Maximum number of results to return (default 20).

        Returns list of dicts with: path, title, date, tags, snippet.
        """
        results = []
        q = query.lower()
        for path in sorted(self._glacier_dir.glob("*.md"), reverse=True):
            if len(results) >= limit:
                break
            text = path.read_text()
            # Parse YAML frontmatter
            meta = self._parse_frontmatter(text)
            # Check tags, title, or content
            searchable = (
                meta.get("title", "").lower()
                + " "
                + meta.get("tags", "").lower()
                + " "
                + text.lower()
            )
            if q in searchable:
                # Extract snippet (first non-frontmatter line with the query)
                body_lines = text.split("---", 2)[-1].splitlines()
                snippet = next(
                    (ln.strip() for ln in body_lines if q in ln.lower() and ln.strip()),
                    body_lines[0].strip() if body_lines else "",
                )
                results.append(
                    {
                        "path": str(path),
                        "title": meta.get("title", path.stem),
                        "date": meta.get("date", ""),
                        "tags": [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()],
                        "snippet": snippet[:200],
                    }
                )
        return results

    def list_glacier(self, tag: str | None = None) -> list[dict]:
        """List all glacier entries, optionally filtered by tag."""
        entries = []
        for path in sorted(self._glacier_dir.glob("*.md"), reverse=True):
            text = path.read_text()
            meta = self._parse_frontmatter(text)
            tags = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]
            if tag and tag not in tags:
                continue
            entries.append(
                {
                    "path": str(path),
                    "title": meta.get("title", path.stem),
                    "date": meta.get("date", ""),
                    "tags": tags,
                }
            )
        return entries

    @staticmethod
    def _parse_frontmatter(text: str) -> dict[str, str]:
        """Parse simple YAML frontmatter (key: value lines only)."""
        meta: dict[str, str] = {}
        if not text.startswith("---"):
            return meta
        parts = text.split("---", 2)
        if len(parts) < 3:
            return meta
        for line in parts[1].splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                meta[key.strip()] = val.strip()
        return meta
