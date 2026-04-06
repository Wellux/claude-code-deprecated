"""Tests for src/mcp_server.py — tool functions, _capture, _make_args, import guard."""
from __future__ import annotations

# Inject fake mcp packages into sys.modules BEFORE importing mcp_server,
# so the module-level `_require_fastmcp()` call succeeds without the real mcp package.
import importlib
import sys
import types
from unittest.mock import MagicMock, patch

import pytest

# ── build the fake mcp module tree ────────────────────────────────────────────

def _install_fake_mcp():
    """Inject stub mcp.server.fastmcp into sys.modules."""
    fake_fastmcp_cls = MagicMock(name="FastMCP")
    # Each instance returned by FastMCP(...) is also a MagicMock
    fake_fastmcp_cls.return_value = MagicMock(name="mcp_instance")
    # Ensure @mcp.tool() returns the decorated function unchanged
    fake_fastmcp_cls.return_value.tool.return_value = lambda fn: fn

    stub_fastmcp_mod = types.ModuleType("mcp.server.fastmcp")
    stub_fastmcp_mod.FastMCP = fake_fastmcp_cls  # type: ignore[attr-defined]

    stub_server_mod = types.ModuleType("mcp.server")
    stub_server_mod.fastmcp = stub_fastmcp_mod  # type: ignore[attr-defined]

    stub_mcp_mod = types.ModuleType("mcp")
    stub_mcp_mod.server = stub_server_mod  # type: ignore[attr-defined]

    sys.modules.setdefault("mcp", stub_mcp_mod)
    sys.modules.setdefault("mcp.server", stub_server_mod)
    sys.modules.setdefault("mcp.server.fastmcp", stub_fastmcp_mod)

    return fake_fastmcp_cls


_fake_fastmcp_cls = _install_fake_mcp()

# Now import (and reload) the server module with the stubs in place
import src.mcp_server as _mcp_mod  # noqa: E402,I001

importlib.reload(_mcp_mod)

from src.mcp_server import _capture, _make_args  # noqa: E402,I001


# ── _make_args ────────────────────────────────────────────────────────────────

class TestMakeArgs:
    def test_single_kwarg(self):
        ns = _make_args(env="staging")
        assert ns.env == "staging"

    def test_multiple_kwargs(self):
        ns = _make_args(env="local", dry_run=True, port=8000)
        assert ns.dry_run is True
        assert ns.port == 8000

    def test_empty(self):
        import argparse
        ns = _make_args()
        assert isinstance(ns, argparse.Namespace)


# ── _capture ──────────────────────────────────────────────────────────────────

class TestCapture:
    def test_captures_stdout(self):
        import argparse

        def _printer(args):
            print("hello from fn")

        result = _capture(_printer, argparse.Namespace())
        assert result == "hello from fn\n"

    def test_empty_output(self):
        import argparse

        result = _capture(lambda _: None, argparse.Namespace())
        assert result == ""

    def test_multiple_prints(self):
        import argparse

        def _multi(args):
            print("line1")
            print("line2")

        result = _capture(_multi, argparse.Namespace())
        assert "line1" in result
        assert "line2" in result


# ── MCP tool functions ────────────────────────────────────────────────────────

class TestDeployTool:
    def test_calls_cmd_deploy_and_returns_string(self):
        with patch("src.cli.cmd_deploy") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("deploy ok")
            result = _mcp_mod.deploy(env="local", dry_run=True,
                                     skip_tests=True, skip_build=True, skip_evals=True)
        assert "deploy ok" in result

    def test_dry_run_flag_forwarded(self):
        captured_args = []

        def _spy(args):
            captured_args.append(args)

        with patch("src.cli.cmd_deploy", _spy):
            _mcp_mod.deploy(dry_run=True, skip_tests=False,
                            skip_build=False, skip_evals=False)
        assert captured_args[0].dry_run is True

    def test_env_forwarded(self):
        captured_args = []

        def _spy(args):
            captured_args.append(args)

        with patch("src.cli.cmd_deploy", _spy):
            _mcp_mod.deploy(env="staging", dry_run=False,
                            skip_tests=True, skip_build=True, skip_evals=True)
        assert captured_args[0].env == "staging"


class TestBuildTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_build") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("build done")
            result = _mcp_mod.build()
        assert "build done" in result

    def test_no_cache_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_build", lambda a: captured_args.append(a)):
            _mcp_mod.build(no_cache=True)
        assert captured_args[0].no_cache is True

    def test_tag_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_build", lambda a: captured_args.append(a)):
            _mcp_mod.build(tag="v1.2.3")
        assert captured_args[0].tag == "v1.2.3"


class TestHealthTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_health") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("healthy")
            result = _mcp_mod.health()
        assert "healthy" in result

    def test_url_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_health", lambda a: captured_args.append(a)):
            _mcp_mod.health(url="http://prod:8000")
        assert captured_args[0].url == "http://prod:8000"


class TestStatusTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_status") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("status output")
            result = _mcp_mod.status()
        assert "status output" in result


class TestDoctorTool:
    def test_healthy_verdict(self):
        with patch("src.cli.cmd_doctor", return_value=0) as mock_cmd:
            mock_cmd.side_effect = lambda args: 0
            with patch("src.mcp_server._capture", return_value="checks ok\n"):
                result = _mcp_mod.doctor()
        assert "HEALTHY" in result

    def test_issues_verdict(self):
        def _bad_doctor(args):
            return 1

        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with patch("src.cli.cmd_doctor", _bad_doctor):
                result = _mcp_mod.doctor()
        assert "ISSUES FOUND" in result


class TestGetLogsTool:
    def test_returns_string(self):
        with patch("src.cli.cmd_logs") as mock_cmd:
            mock_cmd.side_effect = lambda args: print("log line")
            result = _mcp_mod.get_logs()
        assert "log line" in result

    def test_limit_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_logs", lambda a: captured_args.append(a)):
            _mcp_mod.get_logs(limit=10)
        assert captured_args[0].limit == 10

    def test_event_filter_forwarded(self):
        captured_args = []
        with patch("src.cli.cmd_logs", lambda a: captured_args.append(a)):
            _mcp_mod.get_logs(event="api_startup")
        assert captured_args[0].event == "api_startup"


# ── _build_server + run ───────────────────────────────────────────────────────

class TestBuildServer:
    def test_returns_mcp_instance(self):
        server = _mcp_mod._build_server()
        # FastMCP was called with the app name
        _fake_fastmcp_cls.assert_called_with(
            "ccm", instructions="Claude Code Max deployment and operations server"
        )
        assert server is _fake_fastmcp_cls.return_value

    def test_all_tools_registered(self):
        """All 6 tool functions are registered via mcp.tool()."""
        instance = _fake_fastmcp_cls.return_value
        # .tool() called once per function (deploy, build, health, status, doctor, get_logs)
        assert instance.tool.call_count >= 6

    def test_run_calls_build_server_run(self):
        """run() delegates to _build_server().run()."""
        with patch.object(_mcp_mod, "_build_server") as mock_build:
            mock_server = MagicMock()
            mock_build.return_value = mock_server
            _mcp_mod.run()
        mock_build.assert_called_once()
        mock_server.run.assert_called_once()


# ── import guard ──────────────────────────────────────────────────────────────

class TestRequireFastmcp:
    def test_raises_system_exit_when_mcp_missing(self):
        """_require_fastmcp must exit(1) when mcp is not installed."""
        # Temporarily hide the mcp module
        saved = {k: v for k, v in sys.modules.items() if k.startswith("mcp")}
        for k in list(saved):
            sys.modules.pop(k)
        try:
            with pytest.raises(SystemExit) as exc_info:
                _mcp_mod._require_fastmcp()
            assert exc_info.value.code == 1
        finally:
            sys.modules.update(saved)
