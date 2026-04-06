"""Tests for src/utils/log_index.py — indexed JSONL event log."""
from __future__ import annotations

import json
import threading

from src.utils.log_index import LogIndex


class TestLogIndexAppend:
    def test_append_returns_record(self, tmp_path):
        idx = LogIndex(tmp_path / "events.log")
        rec = idx.append("startup", version="0.6.0")
        assert rec["event"] == "startup"
        assert rec["version"] == "0.6.0"
        assert "ts" in rec

    def test_append_writes_to_disk(self, tmp_path):
        path = tmp_path / "events.log"
        idx = LogIndex(path)
        idx.append("test_event", key="val")
        lines = path.read_text().strip().splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["event"] == "test_event"
        assert record["key"] == "val"

    def test_multiple_appends_accumulate(self, tmp_path):
        idx = LogIndex(tmp_path / "events.log")
        for i in range(5):
            idx.append("tick", n=i)
        assert len(idx) == 5

    def test_creates_parent_dirs(self, tmp_path):
        nested = tmp_path / "a" / "b" / "events.log"
        idx = LogIndex(nested)
        idx.append("boot")
        assert nested.exists()


class TestLogIndexSearch:
    def test_search_by_event(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("api_request", path="/complete")
        idx.append("llm_call", model="opus")
        idx.append("api_request", path="/chat")

        results = idx.search(event="api_request")
        assert len(results) == 2
        assert all(r["event"] == "api_request" for r in results)

    def test_search_newest_first(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ev", n=0)
        idx.append("ev", n=1)
        idx.append("ev", n=2)

        results = idx.search(event="ev")
        # newest first → n=2 first
        assert results[0]["n"] == 2
        assert results[-1]["n"] == 0

    def test_search_by_tag(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ci_run", tag="ci")
        idx.append("deploy", tag="prod")
        idx.append("smoke", tag="ci")

        results = idx.search(tags=["ci"])
        assert len(results) == 2

    def test_search_event_and_tag_intersection(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("eval_run", tag="ci")
        idx.append("eval_run", tag="live")
        idx.append("other", tag="ci")

        results = idx.search(event="eval_run", tags=["ci"])
        assert len(results) == 1
        assert results[0]["tag"] == "ci"

    def test_search_no_filters_returns_all_newest_first(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for i in range(10):
            idx.append("ev", n=i)
        results = idx.search()
        assert len(results) == 10
        assert results[0]["n"] == 9

    def test_search_limit(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for i in range(20):
            idx.append("ev", n=i)
        results = idx.search(limit=5)
        assert len(results) == 5

    def test_search_unknown_event_returns_empty(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("known")
        assert idx.search(event="unknown") == []


class TestLogIndexTail:
    def test_tail_returns_last_n(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for i in range(10):
            idx.append("ev", n=i)
        result = idx.tail(3)
        assert len(result) == 3
        assert result[-1]["n"] == 9  # last entry is most recent

    def test_tail_all_when_n_exceeds_length(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ev")
        assert len(idx.tail(100)) == 1


class TestLogIndexSummary:
    def test_summary_counts_by_event(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        for _ in range(3):
            idx.append("api_request")
        for _ in range(2):
            idx.append("llm_call")
        s = idx.summary()
        assert s["api_request"] == 3
        assert s["llm_call"] == 2


class TestLogIndexPersistence:
    def test_reload_rebuilds_index(self, tmp_path):
        path = tmp_path / "e.log"
        idx1 = LogIndex(path)
        for i in range(5):
            idx1.append("ev", n=i, tag="batch1")

        # New instance reads from disk
        idx2 = LogIndex(path)
        assert len(idx2) == 5
        results = idx2.search(event="ev")
        assert len(results) == 5

    def test_reload_preserves_tag_index(self, tmp_path):
        path = tmp_path / "e.log"
        idx1 = LogIndex(path)
        idx1.append("run", tag="ci")
        idx1.append("run", tag="prod")

        idx2 = LogIndex(path)
        assert len(idx2.search(tags=["ci"])) == 1

    def test_corrupt_line_is_skipped(self, tmp_path):
        path = tmp_path / "e.log"
        # Write one valid + one corrupt line
        path.write_text('{"ts":"x","event":"ok"}\nNOT_JSON\n{"ts":"y","event":"ok"}\n')
        idx = LogIndex(path)
        assert len(idx) == 2   # corrupt line skipped, not counted


class TestLogIndexThreadSafety:
    def test_concurrent_appends(self, tmp_path):
        idx = LogIndex(tmp_path / "e.log")
        errors: list[Exception] = []

        def writer():
            try:
                for _ in range(50):
                    idx.append("concurrent_write", thread=threading.get_ident())
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(idx) == 200   # 4 threads × 50 writes


class TestLogIndexEviction:
    def test_eviction_triggered_on_overflow(self, tmp_path):
        """Lines 76 and 129-131: _evict() fires when buffer exceeds max_entries."""
        idx = LogIndex(tmp_path / "e.log", max_entries=5)
        for i in range(8):
            idx.append("ev", n=i)
        # After eviction, in-memory buffer should be <= max_entries
        assert len(idx) <= 5

    def test_evict_rebuilds_searchable_index(self, tmp_path):
        """After eviction, search still works on retained entries."""
        idx = LogIndex(tmp_path / "e.log", max_entries=4)
        for i in range(6):
            idx.append("item", n=i)
        results = idx.search(event="item")
        assert len(results) <= 4


class TestLogIndexLoadEdgeCases:
    def test_empty_lines_skipped_on_load(self, tmp_path):
        """Line 149: blank lines in log file are silently ignored."""
        path = tmp_path / "e.log"
        path.write_text(
            '{"ts":"a","event":"ok"}\n'
            "\n"                           # blank line
            "   \n"                        # whitespace-only line
            '{"ts":"b","event":"ok"}\n'
        )
        idx = LogIndex(path)
        assert len(idx) == 2

    def test_max_entries_cap_applied_on_load(self, tmp_path):
        """Line 166: pre-existing log with > max_entries is capped in memory."""
        path = tmp_path / "e.log"
        lines = [json.dumps({"ts": f"t{i}", "event": "old"}) for i in range(20)]
        path.write_text("\n".join(lines) + "\n")
        idx = LogIndex(path, max_entries=5)
        # Only the most recent 5 should be retained in memory
        assert len(idx) == 5


class TestLogIndexTagList:
    def test_tags_as_list_are_all_indexed(self, tmp_path):
        """Line 179: when a 'tags' field is a list, every element is indexed."""
        idx = LogIndex(tmp_path / "e.log")
        idx.append("ev", tags=["alpha", "beta", "gamma"])
        assert len(idx.search(tags=["alpha"])) == 1
        assert len(idx.search(tags=["beta"])) == 1
        assert len(idx.search(tags=["gamma"])) == 1
