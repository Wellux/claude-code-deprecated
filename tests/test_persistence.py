"""Tests for src/persistence/ — FileStore and MemoryStore."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from src.persistence.file_store import FileStore, _atomic_write, _slugify
from src.persistence.memory_store import Entity, MemoryStore

# ── FileStore ─────────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_store(tmp_path):
    return FileStore(root=tmp_path)


class TestFileStoreInit:
    def test_creates_required_directories(self, tmp_path):
        FileStore(root=tmp_path)
        assert (tmp_path / "data/research").is_dir()
        assert (tmp_path / "data/outputs").is_dir()
        assert (tmp_path / "data/cache").is_dir()
        assert (tmp_path / "tasks").is_dir()

    def test_idempotent_on_existing_dirs(self, tmp_store, tmp_path):
        # Should not raise even when dirs already exist
        FileStore(root=tmp_path)


class TestFileStoreResearch:
    def test_write_research_returns_path(self, tmp_store):
        path = tmp_store.write_research("LightRAG", "# LightRAG\n\nGraph-based RAG.")
        assert path.exists()
        assert "lightrag" in path.name

    def test_write_research_content_persisted(self, tmp_store):
        content = "# My Topic\n\nSome research."
        path = tmp_store.write_research("My Topic", content)
        assert path.read_text() == content

    def test_write_research_updates_index(self, tmp_store):
        tmp_store.write_research("Vector DB", "content")
        index = (tmp_store.root / "data/research/README.md").read_text()
        assert "Vector DB" in index

    def test_list_research_empty(self, tmp_store):
        assert tmp_store.list_research() == []

    def test_list_research_returns_entries(self, tmp_store):
        tmp_store.write_research("Topic One", "a")
        tmp_store.write_research("Topic Two", "b")
        results = tmp_store.list_research()
        assert len(results) == 2
        topics = {r["topic"] for r in results}
        assert "topic one" in topics
        assert "topic two" in topics

    def test_list_research_entry_shape(self, tmp_store):
        tmp_store.write_research("Shape Test", "content")
        entry = tmp_store.list_research()[0]
        assert "topic" in entry
        assert "path" in entry
        assert "date" in entry


class TestFileStoreOutputs:
    def test_write_output_returns_path(self, tmp_store):
        path = tmp_store.write_output("report", "# Weekly Report")
        assert path.exists()

    def test_write_output_filename_includes_type(self, tmp_store):
        path = tmp_store.write_output("perf-audit", "content")
        assert "perf-audit" in path.name

    def test_write_output_content(self, tmp_store):
        path = tmp_store.write_output("summary", "hello world")
        assert path.read_text() == "hello world"


class TestFileStoreLessons:
    def test_append_lesson_creates_file(self, tmp_store):
        tmp_store.append_lesson(
            title="Test lesson",
            mistake="Did X",
            why="Because Y",
            rule="Never do X",
            example="Instead do Z",
        )
        lessons_path = tmp_store.root / "tasks/lessons.md"
        assert lessons_path.exists()

    def test_append_lesson_content(self, tmp_store):
        tmp_store.append_lesson("My Lesson", "I forgot", "careless", "Always check", "check = True")
        text = (tmp_store.root / "tasks/lessons.md").read_text()
        assert "My Lesson" in text
        assert "I forgot" in text
        assert "careless" in text
        assert "Always check" in text

    def test_append_lesson_multiple(self, tmp_store):
        tmp_store.append_lesson("L1", "m1", "w1", "r1", "e1")
        tmp_store.append_lesson("L2", "m2", "w2", "r2", "e2")
        text = (tmp_store.root / "tasks/lessons.md").read_text()
        assert "L1" in text
        assert "L2" in text


class TestFileStoreTasks:
    def test_append_task_creates_file(self, tmp_store):
        tmp_store.append_task("Fix the bug")
        assert (tmp_store.root / "tasks/todo.md").exists()

    def test_append_task_unchecked(self, tmp_store):
        tmp_store.append_task("Write tests")
        text = (tmp_store.root / "tasks/todo.md").read_text()
        assert "- [ ] Write tests" in text

    def test_complete_task_marks_done(self, tmp_store):
        tmp_store.append_task("Deploy service")
        result = tmp_store.complete_task("Deploy service")
        assert result is True
        text = (tmp_store.root / "tasks/todo.md").read_text()
        assert "- [x] Deploy service" in text

    def test_complete_task_not_found_returns_false(self, tmp_store):
        tmp_store.append_task("Real task")
        result = tmp_store.complete_task("Non-existent task")
        assert result is False

    def test_complete_task_no_file_returns_false(self, tmp_store):
        result = tmp_store.complete_task("Anything")
        assert result is False

    def test_complete_task_only_first_occurrence(self, tmp_store):
        tmp_store.append_task("Repeat task")
        tmp_store.append_task("Repeat task")
        tmp_store.complete_task("Repeat task")
        text = (tmp_store.root / "tasks/todo.md").read_text()
        assert text.count("- [x] Repeat task") == 1
        assert text.count("- [ ] Repeat task") == 1


class TestFileStoreEvents:
    def test_log_event_creates_file(self, tmp_store):
        tmp_store.log_event("startup")
        assert (tmp_store.root / "data/cache/events.log").exists()

    def test_log_event_is_json(self, tmp_store):
        tmp_store.log_event("test_event", key="value", count=3)
        log_path = tmp_store.root / "data/cache/events.log"
        line = log_path.read_text().strip()
        obj = json.loads(line)
        assert obj["event"] == "test_event"
        assert obj["key"] == "value"
        assert obj["count"] == 3
        assert "ts" in obj

    def test_log_event_appends(self, tmp_store):
        tmp_store.log_event("e1")
        tmp_store.log_event("e2")
        lines = (tmp_store.root / "data/cache/events.log").read_text().strip().splitlines()
        assert len(lines) == 2

    def test_search_log_by_event(self, tmp_store):
        tmp_store.log_event("startup", version="1.0")
        tmp_store.log_event("shutdown")
        results = tmp_store.search_log(event="startup")
        assert len(results) == 1
        assert results[0]["event"] == "startup"

    def test_log_summary_counts_events(self, tmp_store):
        tmp_store.log_event("startup")
        tmp_store.log_event("startup")
        tmp_store.log_event("request")
        summary = tmp_store.log_summary()
        assert summary["startup"] == 2
        assert summary["request"] == 1


class TestAtomicWrite:
    def test_writes_content(self, tmp_path):
        p = tmp_path / "out.txt"
        _atomic_write(p, "hello atomic")
        assert p.read_text() == "hello atomic"

    def test_no_tmp_file_left_on_success(self, tmp_path):
        p = tmp_path / "out.txt"
        _atomic_write(p, "data")
        leftover = list(tmp_path.glob(".tmp-*"))
        assert leftover == []

    def test_creates_parent_dirs(self, tmp_path):
        p = tmp_path / "deep" / "nested" / "file.txt"
        _atomic_write(p, "content")
        assert p.read_text() == "content"

    def test_overwrites_existing(self, tmp_path):
        p = tmp_path / "file.txt"
        _atomic_write(p, "first")
        _atomic_write(p, "second")
        assert p.read_text() == "second"

    def test_old_content_intact_if_write_fails(self, tmp_path):
        """If writing raises, the original file must be untouched."""
        import unittest.mock
        p = tmp_path / "important.txt"
        _atomic_write(p, "original")

        # Make os.replace raise after the temp file is written
        call_count = 0

        def _bad_replace(src, dst):
            nonlocal call_count
            call_count += 1
            os.unlink(src)          # clean up tmp ourselves
            raise OSError("replace failed")

        with unittest.mock.patch("src.persistence.file_store.os.replace", _bad_replace):
            with pytest.raises(OSError, match="replace failed"):
                _atomic_write(p, "new content")

        assert p.read_text() == "original"
        assert call_count == 1


class TestFileStoreReadWrite:
    def test_write_and_read(self, tmp_store):
        tmp_store.write("notes/hello.txt", "hello world")
        assert tmp_store.read("notes/hello.txt") == "hello world"

    def test_write_creates_parents(self, tmp_store):
        tmp_store.write("deep/nested/dir/file.md", "content")
        assert (tmp_store.root / "deep/nested/dir/file.md").exists()

    def test_write_returns_path(self, tmp_store):
        path = tmp_store.write("out.txt", "data")
        assert isinstance(path, Path)
        assert path.exists()


class TestSlugify:
    def test_basic(self):
        assert _slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert _slugify("C++ & Python!") == "c-python"

    def test_truncates_at_60(self):
        long = "a" * 100
        assert len(_slugify(long)) <= 60

    def test_no_leading_trailing_dash(self):
        slug = _slugify("  hello  ")
        assert not slug.startswith("-")
        assert not slug.endswith("-")


# ── MemoryStore ───────────────────────────────────────────────────────────────


@pytest.fixture
def store():
    return MemoryStore()


class TestMemoryStoreInit:
    def test_starts_empty(self, store):
        assert store.size == 0

    def test_mcp_not_available_in_tests(self, store):
        assert store._mcp_available is False


class TestMemoryStoreRemember:
    def test_remember_single_fact(self, store):
        store.remember("project uses PostgreSQL")
        assert store.size == 1

    def test_remember_multiple_facts_same_entity(self, store):
        store.remember("fact 1", entity_name="db")
        store.remember("fact 2", entity_name="db")
        assert store.size == 1  # same entity

    def test_remember_different_entities(self, store):
        store.remember("fact 1", entity_name="db")
        store.remember("fact 2", entity_name="cache")
        assert store.size == 2

    def test_remember_default_entity_is_general(self, store):
        store.remember("some fact")
        data = store.read_all()
        assert "general" in data


class TestMemoryStoreEntity:
    def test_remember_entity(self, store):
        store.remember_entity("LightRAG", "tool", ["graph-based RAG", "EMNLP 2025"])
        entity = store.recall_entity("LightRAG")
        assert entity is not None
        assert entity.name == "LightRAG"
        assert "graph-based RAG" in entity.observations

    def test_remember_entity_extends_observations(self, store):
        store.remember_entity("Tool", "lib", ["obs1"])
        store.remember_entity("Tool", "lib", ["obs2"])
        entity = store.recall_entity("Tool")
        assert "obs1" in entity.observations
        assert "obs2" in entity.observations

    def test_recall_entity_unknown_type_in_fallback(self, store):
        store.remember("a fact", entity_name="myent")
        entity = store.recall_entity("myent")
        assert entity.entity_type == "unknown"

    def test_recall_entity_not_found_returns_none(self, store):
        assert store.recall_entity("does_not_exist") is None


class TestMemoryStoreRelation:
    def test_remember_relation_stored_as_fact(self, store):
        store.remember_relation("Claude", "Anthropic", "made_by")
        data = store.read_all()
        assert "_relations" in data
        assert any("Claude" in f for f in data["_relations"])


class TestMemoryStoreRecall:
    def test_recall_exact_match(self, store):
        store.remember("PostgreSQL is the database", entity_name="infra")
        results = store.recall("PostgreSQL")
        assert len(results) == 1
        assert "PostgreSQL" in results[0]

    def test_recall_case_insensitive(self, store):
        store.remember("uses Redis for caching", entity_name="infra")
        results = store.recall("redis")
        assert len(results) == 1

    def test_recall_matches_entity_name(self, store):
        store.remember("some fact", entity_name="my_special_entity")
        results = store.recall("my_special_entity")
        assert len(results) == 1

    def test_recall_no_match_returns_empty(self, store):
        store.remember("irrelevant fact")
        results = store.recall("quantum_physics")
        assert results == []

    def test_recall_multiple_matches(self, store):
        store.remember("Python version 3.12", entity_name="stack")
        store.remember("Python used for scripting", entity_name="notes")
        results = store.recall("Python")
        assert len(results) == 2


class TestMemoryStoreForget:
    def test_forget_removes_entity(self, store):
        store.remember("fact", entity_name="temp")
        store.forget("temp")
        assert store.size == 0

    def test_forget_nonexistent_is_noop(self, store):
        store.forget("ghost")  # should not raise

    def test_forget_observation(self, store):
        store.remember("keep this", entity_name="e")
        store.remember("remove this", entity_name="e")
        store.forget_observation("e", "remove this")
        entity = store.recall_entity("e")
        assert "keep this" in entity.observations
        assert "remove this" not in entity.observations


class TestMemoryStoreReadAll:
    def test_read_all_empty(self, store):
        assert store.read_all() == {}

    def test_read_all_returns_copy(self, store):
        store.remember("fact", entity_name="e")
        data = store.read_all()
        data["new_key"] = ["tamper"]
        # Original should be unchanged
        assert "new_key" not in store.read_all()


class TestEntityDataclass:
    def test_entity_fields(self):
        e = Entity(name="Test", entity_type="lib", observations=["obs1"])
        assert e.name == "Test"
        assert e.entity_type == "lib"
        assert e.observations == ["obs1"]


# ── MCP-available branches (stub methods + mcp-path dispatch) ─────────────────

@pytest.fixture
def mcp_store():
    """MemoryStore with _mcp_available=True to exercise MCP dispatch paths."""
    s = MemoryStore()
    s._mcp_available = True
    return s


class TestMemoryStoreMcpPath:
    """Verify that with _mcp_available=True the MCP stub methods are called."""

    def test_remember_calls_mcp_add_observation(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_add_observation") as mock_add:
            mcp_store.remember("test fact", entity_name="proj")
        mock_add.assert_called_once_with("proj", "test fact")

    def test_remember_entity_calls_mcp_create_entity(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_create_entity") as mock_create:
            mcp_store.remember_entity("Tool", "lib", ["obs1"])
        mock_create.assert_called_once_with("Tool", "lib", ["obs1"])

    def test_recall_calls_mcp_search(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_search", return_value=["result"]) as mock_search:
            results = mcp_store.recall("database")
        mock_search.assert_called_once_with("database")
        assert results == ["result"]

    def test_recall_entity_calls_mcp_open_node(self, mcp_store):
        from unittest.mock import patch
        entity = Entity(name="A", entity_type="t", observations=[])
        with patch.object(mcp_store, "_mcp_open_node", return_value=entity) as mock_node:
            result = mcp_store.recall_entity("A")
        mock_node.assert_called_once_with("A")
        assert result is entity

    def test_forget_calls_mcp_delete_entity(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_delete_entity") as mock_del:
            mcp_store.forget("proj")
        mock_del.assert_called_once_with("proj")

    def test_forget_observation_calls_mcp_delete_observation(self, mcp_store):
        from unittest.mock import patch
        with patch.object(mcp_store, "_mcp_delete_observation") as mock_del:
            mcp_store.forget_observation("proj", "old fact")
        mock_del.assert_called_once_with("proj", "old fact")


class TestMcpStubMethods:
    """The _mcp_* stub methods log a warning and no-op / return empty."""

    def test_mcp_add_observation_noop(self, store):
        store._mcp_add_observation("entity", "obs")  # must not raise

    def test_mcp_create_entity_noop(self, store):
        store._mcp_create_entity("name", "type", ["obs"])

    def test_mcp_search_returns_empty(self, store):
        assert store._mcp_search("query") == []

    def test_mcp_open_node_returns_none(self, store):
        assert store._mcp_open_node("name") is None

    def test_mcp_delete_entity_noop(self, store):
        store._mcp_delete_entity("name")

    def test_mcp_delete_observation_noop(self, store):
        store._mcp_delete_observation("entity", "obs")
