"""Tests for src/utils/logger.py — structured JSON logger."""
from __future__ import annotations

import json
import logging

from src.utils.logger import StructuredLogger, get_logger


class TestStructuredLogger:
    def test_get_logger_returns_structured_logger(self):
        lg = get_logger("test.get_logger")
        assert isinstance(lg, StructuredLogger)

    def test_info_emits_json_line(self, capsys):
        lg = get_logger("test.info")
        lg.info("hello", request_id="abc")
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["msg"] == "hello"
        assert record["request_id"] == "abc"
        assert record["level"] == "INFO"

    def test_warning_emits_warning_level(self, capsys):
        lg = get_logger("test.warning")
        lg.warning("watch out")
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["level"] == "WARNING"

    def test_error_emits_error_level(self, capsys):
        lg = get_logger("test.error")
        lg.error("bad thing", code=500)
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["level"] == "ERROR"
        assert record["code"] == 500

    def test_critical_emits_critical_level(self, capsys):
        lg = get_logger("test.critical")
        lg.critical("fatal", component="db")
        out = capsys.readouterr().out
        record = json.loads(out.strip())
        assert record["level"] == "CRITICAL"
        assert record["component"] == "db"

    def test_debug_below_default_level_not_emitted(self, capsys):
        lg = get_logger("test.debug")  # default level = INFO
        lg.debug("silent")
        out = capsys.readouterr().out
        assert out == ""

    def test_exc_info_serialized_in_formatter(self):
        """The exc_info branch in _StructuredFormatter adds an 'exc' string key."""
        import sys

        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = logging.LogRecord(
            name="t", level=logging.ERROR, pathname="", lineno=0,
            msg="boom", args=(), exc_info=None,
        )
        try:
            raise RuntimeError("test exc")
        except RuntimeError:
            record.exc_info = sys.exc_info()
        result = json.loads(fmt.format(record))
        assert "exc" in result
        assert "RuntimeError" in result["exc"]


class TestSensitiveFieldRedaction:
    def _make_record(self, **kwargs) -> logging.LogRecord:
        record = logging.LogRecord(
            name="t", level=logging.INFO, pathname="", lineno=0,
            msg="test", args=(), exc_info=None,
        )
        record.__dict__.update(kwargs)
        return record

    def test_password_is_redacted(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(password="s3cr3t")
        result = json.loads(fmt.format(record))
        assert result["password"] == "[REDACTED]"
        assert "s3cr3t" not in json.dumps(result)

    def test_api_key_is_redacted(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(api_key="sk-ant-abc123")
        result = json.loads(fmt.format(record))
        assert result["api_key"] == "[REDACTED]"

    def test_token_is_redacted(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(token="bearer-xyz")
        result = json.loads(fmt.format(record))
        assert result["token"] == "[REDACTED]"

    def test_non_sensitive_field_passes_through(self):
        from src.utils.logger import _StructuredFormatter
        fmt = _StructuredFormatter()
        record = self._make_record(model="claude-sonnet-4-6", latency_ms=42)
        result = json.loads(fmt.format(record))
        assert result["model"] == "claude-sonnet-4-6"
        assert result["latency_ms"] == 42
