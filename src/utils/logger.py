"""Structured JSON logger factory."""
from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any


class _StructuredFormatter(logging.Formatter):
    """Emit log records as JSON lines."""

    # Standard LogRecord *instance* attributes that must never be serialised raw.
    # exc_info / exc_text / stack_info can contain non-JSON-serialisable objects.
    _STDLIB_KEYS: frozenset[str] = frozenset(logging.LogRecord(
        "", logging.INFO, "", 0, "", (), None
    ).__dict__.keys()) | frozenset(logging.LogRecord.__dict__.keys())

    # Field names whose values are redacted before serialisation to prevent
    # accidental logging of secrets, tokens, or credentials.
    _SENSITIVE_KEYS: frozenset[str] = frozenset({
        "password", "passwd", "secret", "token", "api_key", "apikey",
        "authorization", "auth", "credential", "private_key", "access_key",
    })

    def format(self, record: logging.LogRecord) -> str:
        base = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Merge any extra kwargs passed to logger.info("event", key=val),
        # excluding all standard LogRecord attrs (some contain non-serialisable
        # objects such as exc_info tuples or traceback references).
        extra = {
            k: ("[REDACTED]" if k.lower() in self._SENSITIVE_KEYS else v)
            for k, v in record.__dict__.items()
            if k not in self._STDLIB_KEYS and not k.startswith("_")
        }
        base.update(extra)
        if record.exc_info:
            base["exc"] = self.formatException(record.exc_info)
        return json.dumps(base)


def get_logger(name: str, level: int = logging.INFO) -> StructuredLogger:
    """Return a structured logger with JSON output."""
    return StructuredLogger(name, level)


class StructuredLogger:
    """Thin wrapper that passes kwargs as extra fields to the JSON formatter."""

    def __init__(self, name: str, level: int = logging.INFO):
        self._log = logging.getLogger(name)
        if not self._log.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(_StructuredFormatter())
            self._log.addHandler(handler)
            self._log.setLevel(level)
            self._log.propagate = False

    def _emit(self, level: int, msg: str, **kwargs: Any) -> None:
        if self._log.isEnabledFor(level):
            record = self._log.makeRecord(
                self._log.name, level, "(unknown)", 0, msg, (), None
            )
            record.__dict__.update(kwargs)
            self._log.handle(record)

    def debug(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.INFO, msg, **kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.ERROR, msg, **kwargs)

    def critical(self, msg: str, **kwargs: Any) -> None:
        self._emit(logging.CRITICAL, msg, **kwargs)
