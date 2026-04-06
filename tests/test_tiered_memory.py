"""Tests for TieredMemory — hot/warm/glacier storage system."""

from __future__ import annotations

from pathlib import Path

from src.persistence.tiered_memory import TieredMemory


class TestTieredMemoryInit:
    def test_creates_directories_on_init(self, tmp_path: Path) -> None:
        TieredMemory(base=tmp_path)
        assert (tmp_path / "hot").is_dir()
        assert (tmp_path / "warm").is_dir()
        assert (tmp_path / "glacier").is_dir()

    def test_hot_file_absent_before_first_write(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        assert mem.read_hot() == ""


class TestHotTier:
    def test_write_hot_creates_file(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("branch", "main")
        content = mem.read_hot()
        assert "branch" in content
        assert "main" in content

    def test_write_hot_updates_existing_key(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("branch", "old-branch")
        mem.write_hot("branch", "new-branch")
        content = mem.read_hot()
        assert "new-branch" in content
        assert "old-branch" not in content

    def test_write_hot_updates_timestamp(self, tmp_path: Path) -> None:
        hot_file = tmp_path / "hot" / "hot-memory.md"
        hot_file.parent.mkdir(parents=True)
        hot_file.write_text(
            "**Last Updated**: 2020-01-01 00:00:00\n\n## Active Context\n"
        )
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("key", "value")
        content = mem.read_hot()
        assert "2020-01-01" not in content

    def test_write_hot_multiple_keys(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("key1", "val1")
        mem.write_hot("key2", "val2")
        content = mem.read_hot()
        assert "key1" in content
        assert "key2" in content

    def test_read_hot_returns_string(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_hot("x", "y")
        result = mem.read_hot()
        assert isinstance(result, str)
        assert len(result) > 0


class TestWarmTier:
    def test_write_warm_creates_domain_file(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("architecture", "# Architecture\n\nFastAPI + Python")
        assert (tmp_path / "warm" / "architecture.md").exists()

    def test_read_warm_returns_content(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("routing", "LLM router maps complexity 0-10 to haiku/sonnet/opus")
        result = mem.read_warm("routing")
        assert "LLM router" in result

    def test_read_warm_returns_empty_for_missing_domain(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        result = mem.read_warm("nonexistent")
        assert result == ""

    def test_append_warm_adds_to_existing(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("decisions", "# Decisions\n")
        mem.append_warm("decisions", "- Use setuptools.build_meta not legacy:build")
        content = mem.read_warm("decisions")
        assert "# Decisions" in content
        assert "setuptools.build_meta" in content

    def test_list_warm_domains_empty_initially(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        assert mem.list_warm_domains() == []

    def test_list_warm_domains_returns_names(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.write_warm("architecture", "content")
        mem.write_warm("routing", "content")
        domains = mem.list_warm_domains()
        assert "architecture" in domains
        assert "routing" in domains


class TestGlacierTier:
    def test_archive_glacier_creates_file(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier("my-decision", "We chose PostgreSQL because...")
        assert Path(path).exists()

    def test_archive_glacier_file_has_frontmatter(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier(
            "test-slug",
            "Decision content",
            tags=["architecture", "database"],
            title="Test Decision",
        )
        text = Path(path).read_text()
        assert "---" in text
        assert "title: Test Decision" in text
        assert "tags: [architecture, database]" in text
        assert "slug: test-slug" in text

    def test_archive_glacier_file_contains_body(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier("body-test", "Here is the decision body text")
        text = Path(path).read_text()
        assert "Here is the decision body text" in text

    def test_archive_glacier_filename_includes_date(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        path = mem.archive_glacier("dated-decision", "content")
        filename = Path(path).name
        assert filename.endswith("-dated-decision.md")
        # Filename starts with a date: YYYY-MM-DD
        assert filename[:4].isdigit()

    def test_search_glacier_finds_by_content(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("auth-decision", "We chose JWT tokens over sessions")
        results = mem.search_glacier("JWT")
        assert len(results) >= 1
        assert any("auth-decision" in r["path"] for r in results)

    def test_search_glacier_finds_by_tag(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("tagged-entry", "content", tags=["security", "auth"])
        results = mem.search_glacier("security")
        assert len(results) >= 1

    def test_search_glacier_returns_empty_for_no_match(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("some-entry", "unrelated content here")
        results = mem.search_glacier("xyzzy_not_found")
        assert results == []

    def test_search_glacier_result_has_expected_fields(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("fields-test", "content text", tags=["test"], title="Fields Test")
        results = mem.search_glacier("content")
        assert len(results) >= 1
        r = results[0]
        assert "path" in r
        assert "title" in r
        assert "date" in r
        assert "tags" in r
        assert "snippet" in r

    def test_search_glacier_respects_limit(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        for i in range(5):
            mem.archive_glacier(f"entry-{i}", f"shared keyword result {i}")
        results = mem.search_glacier("keyword", limit=2)
        assert len(results) == 2

    def test_list_glacier_returns_all_entries(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("entry-1", "content 1")
        mem.archive_glacier("entry-2", "content 2")
        entries = mem.list_glacier()
        assert len(entries) >= 2

    def test_list_glacier_filters_by_tag(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        mem.archive_glacier("tagged", "content", tags=["special"])
        mem.archive_glacier("untagged", "other content")
        entries = mem.list_glacier(tag="special")
        assert len(entries) == 1
        assert "tagged" in entries[0]["path"]

    def test_list_glacier_empty_initially(self, tmp_path: Path) -> None:
        mem = TieredMemory(base=tmp_path)
        assert mem.list_glacier() == []


class TestTieredMemoryIntegration:
    def test_persistence_module_exports_tiered_memory(self) -> None:
        from src.persistence import TieredMemory as TM  # noqa: F401
        assert TM is TieredMemory

    def test_full_lifecycle(self, tmp_path: Path) -> None:
        """Hot write → warm domain → glacier archive → search."""
        mem = TieredMemory(base=tmp_path)

        # Write hot context
        mem.write_hot("active_feature", "tiered-memory")

        # Write warm domain
        mem.write_warm("architecture", "# Architecture\nTiered memory: hot/warm/glacier")

        # Archive to glacier
        mem.archive_glacier(
            "tiered-memory-decision",
            "We added hot/warm/glacier tiers to improve context efficiency",
            tags=["architecture", "memory"],
        )

        # Verify all tiers are populated
        assert "active_feature" in mem.read_hot()
        assert "Tiered memory" in mem.read_warm("architecture")
        results = mem.search_glacier("context efficiency")
        assert len(results) == 1
        assert "tiered-memory-decision" in results[0]["path"]


# ── Regex pattern cache ───────────────────────────────────────────────────────

class TestHotKeyPatternCache:
    def test_pattern_cached_after_first_write(self, tmp_path: Path) -> None:
        from src.persistence import tiered_memory as tm_mod

        mem = TieredMemory(base=tmp_path)
        tm_mod._hot_key_patterns.clear()
        mem.write_hot("cached_key", "value1")
        assert "cached_key" in tm_mod._hot_key_patterns

    def test_second_write_reuses_cached_pattern(self, tmp_path: Path) -> None:
        from src.persistence import tiered_memory as tm_mod

        mem = TieredMemory(base=tmp_path)
        tm_mod._hot_key_patterns.clear()
        mem.write_hot("reuse_key", "first")
        pattern_id = id(tm_mod._hot_key_patterns["reuse_key"])
        mem.write_hot("reuse_key", "second")
        assert id(tm_mod._hot_key_patterns["reuse_key"]) == pattern_id
