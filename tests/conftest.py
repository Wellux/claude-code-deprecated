"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Ensure src/ is importable from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture()
def tiered_memory(tmp_path: Path):
    """Isolated TieredMemory instance backed by a temp directory."""
    from src.persistence.tiered_memory import TieredMemory

    return TieredMemory(base=tmp_path)


@pytest.fixture()
def file_store(tmp_path: Path):
    """FileStore instance rooted at a temp directory."""
    from src.persistence.file_store import FileStore

    return FileStore(root=tmp_path)


@pytest.fixture()
def mock_claude_client():
    """Pre-configured mock ClaudeClient for unit tests.

    .complete() and .chat() are AsyncMocks returning a CompletionResponse
    with content="mock response".
    """
    from src.llm.claude_client import CompletionResponse

    client = MagicMock()
    response = CompletionResponse(
        content="mock response",
        model="claude-sonnet-4-6",
        input_tokens=10,
        output_tokens=5,
    )
    client.complete = AsyncMock(return_value=response)
    client.chat = AsyncMock(return_value=response)
    client.count_tokens = MagicMock(return_value=10)
    return client
