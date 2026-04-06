"""Tests for src/cli.py — argument parsing and subcommand logic."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.cli import (
    _deploy_check_health,
    _deploy_run_evals,
    _deploy_run_tests,
    build_parser,
    cmd_doctor,
    cmd_lint,
    cmd_logs,
    cmd_research,
    cmd_route,
    cmd_status,
    cmd_version,
    main,
)

PROJECT_ROOT = Path(__file__).parent.parent


# ── Parser ────────────────────────────────────────────────────────────────────

class TestParser:
    def test_route_subcommand(self):
        args = build_parser().parse_args(["route", "write a function"])
        assert args.command == "route"
        assert args.task == "write a function"
        assert args.json is False

    def test_route_json_flag(self):
        assert build_parser().parse_args(["route", "task", "--json"]).json is True

    def test_complete_defaults(self):
        args = build_parser().parse_args(["complete", "hello"])
        assert args.prompt == "hello"
        assert args.model is None
        assert args.max_tokens == 4096
        assert args.system is None

    def test_complete_with_flags(self):
        args = build_parser().parse_args([
            "complete", "hi",
            "--model", "claude-haiku-4-5-20251001",
            "--max-tokens", "512",
            "--system", "Be terse",
        ])
        assert args.model == "claude-haiku-4-5-20251001"
        assert args.max_tokens == 512
        assert args.system == "Be terse"

    def test_serve_defaults(self):
        args = build_parser().parse_args(["serve"])
        assert args.host == "0.0.0.0"
        assert args.port == 8000
        assert args.reload is False

    def test_serve_custom(self):
        args = build_parser().parse_args(["serve", "--host", "127.0.0.1", "--port", "9000", "--reload"])
        assert args.host == "127.0.0.1" and args.port == 9000 and args.reload is True

    def test_status_subcommand(self):
        assert build_parser().parse_args(["status"]).command == "status"

    def test_version_subcommand(self):
        assert build_parser().parse_args(["version"]).command == "version"

    def test_doctor_subcommand(self):
        assert build_parser().parse_args(["doctor"]).command == "doctor"

    def test_logs_defaults(self):
        args = build_parser().parse_args(["logs"])
        assert args.limit == 50
        assert args.event is None
        assert args.tag is None
        assert args.summary is False

    def test_logs_with_flags(self):
        args = build_parser().parse_args(["logs", "--event", "api_request", "--limit", "10", "--summary"])
        assert args.event == "api_request"
        assert args.limit == 10
        assert args.summary is True

    def test_research_subcommand(self):
        assert build_parser().parse_args(["research", "LightRAG"]).topic == "LightRAG"

    def test_no_subcommand_raises(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args([])

    def test_version_flag_exits(self):
        with pytest.raises(SystemExit) as exc:
            build_parser().parse_args(["--version"])
        assert exc.value.code == 0


# ── cmd_version ───────────────────────────────────────────────────────────────

class TestCmdVersion:
    def test_returns_zero(self):
        assert cmd_version(build_parser().parse_args(["version"])) == 0

    def test_shows_version_string(self, capsys):
        from src.version import __version__
        cmd_version(build_parser().parse_args(["version"]))
        assert __version__ in capsys.readouterr().out

    def test_shows_python_version(self, capsys):
        import sys
        cmd_version(build_parser().parse_args(["version"]))
        assert str(sys.version_info.major) in capsys.readouterr().out


# ── cmd_route ─────────────────────────────────────────────────────────────────

class TestCmdRoute:
    def test_text_output(self, capsys):
        assert cmd_route(build_parser().parse_args(["route", "write a unit test"])) == 0
        assert len(capsys.readouterr().out) > 0

    def test_json_output(self, capsys):
        assert cmd_route(build_parser().parse_args(["route", "summarise this document", "--json"])) == 0
        data = json.loads(capsys.readouterr().out)
        assert all(k in data for k in ("model", "agent", "plan_size", "subtasks"))

    def test_json_subtasks_is_list(self, capsys):
        cmd_route(build_parser().parse_args(["route", "simple task", "--json"]))
        assert isinstance(json.loads(capsys.readouterr().out)["subtasks"], list)

    def test_high_complexity_uses_opus(self, capsys):
        cmd_route(build_parser().parse_args([
            "route",
            "full security audit of the entire codebase architecture and infrastructure",
            "--json",
        ]))
        assert "opus" in json.loads(capsys.readouterr().out)["model"]

    def test_simple_task_uses_haiku(self, capsys):
        cmd_route(build_parser().parse_args(["route", "format this text", "--json"]))
        assert "haiku" in json.loads(capsys.readouterr().out)["model"]


# ── cmd_status ────────────────────────────────────────────────────────────────

class TestCmdStatus:
    def test_returns_zero(self):
        assert cmd_status(build_parser().parse_args(["status"])) == 0

    def test_shows_branch(self, capsys):
        cmd_status(build_parser().parse_args(["status"]))
        assert "branch" in capsys.readouterr().out

    def test_shows_version(self, capsys):
        from src.version import __version__
        cmd_status(build_parser().parse_args(["status"]))
        assert __version__ in capsys.readouterr().out

    def test_shows_test_count(self, capsys):
        import re
        cmd_status(build_parser().parse_args(["status"]))
        out = capsys.readouterr().out
        assert "tests" in out
        match = re.search(r"tests\s*:\s*(\d+)", out)
        assert match and int(match.group(1)) >= 100

    def test_shows_skills_count(self, capsys):
        import re
        cmd_status(build_parser().parse_args(["status"]))
        out = capsys.readouterr().out
        match = re.search(r"skills\s*:\s*(\d+)", out)
        assert match and int(match.group(1)) >= 100


# ── cmd_doctor ────────────────────────────────────────────────────────────────

class TestCmdDoctor:
    def test_runs_without_crash(self):
        assert cmd_doctor(build_parser().parse_args(["doctor"])) in (0, 1)

    def test_shows_check_icons(self, capsys):
        cmd_doctor(build_parser().parse_args(["doctor"]))
        out = capsys.readouterr().out
        assert "[✓]" in out or "[✗]" in out

    def test_shows_summary_line(self, capsys):
        cmd_doctor(build_parser().parse_args(["doctor"]))
        assert "checks passed" in capsys.readouterr().out

    def test_skills_check_present(self, capsys):
        cmd_doctor(build_parser().parse_args(["doctor"]))
        assert "skills" in capsys.readouterr().out


# ── cmd_logs ─────────────────────────────────────────────────────────────────

class TestCmdLogs:
    def test_no_log_file_returns_zero(self, tmp_path, capsys):
        with patch("src.cli._project_root", return_value=tmp_path):
            assert cmd_logs(build_parser().parse_args(["logs"])) == 0

    def test_summary_mode(self, tmp_path, capsys):
        from src.utils.log_index import LogIndex
        log = LogIndex(tmp_path / "data" / "cache" / "events.log")
        for _ in range(3):
            log.append("api_request")
        log.append("llm_call")

        with (
            patch("src.cli._project_root", return_value=tmp_path),
            patch.dict("os.environ", {"CCM_LOG_PATH": "data/cache/events.log"}),
        ):
            cmd_logs(build_parser().parse_args(["logs", "--summary"]))
        out = capsys.readouterr().out
        assert "api_request" in out
        assert "3" in out

    def test_filter_by_event(self, tmp_path, capsys):
        from src.utils.log_index import LogIndex
        log = LogIndex(tmp_path / "data" / "cache" / "events.log")
        log.append("api_request")
        log.append("llm_call")
        log.append("api_request")

        with (
            patch("src.cli._project_root", return_value=tmp_path),
            patch.dict("os.environ", {"CCM_LOG_PATH": "data/cache/events.log"}),
        ):
            cmd_logs(build_parser().parse_args(["logs", "--event", "api_request"]))
        out = capsys.readouterr().out
        assert "api_request" in out
        assert "llm_call" not in out

    def test_json_output(self, tmp_path, capsys):
        from src.utils.log_index import LogIndex
        log = LogIndex(tmp_path / "data" / "cache" / "events.log")
        log.append("startup", version="0.6.0")

        with (
            patch("src.cli._project_root", return_value=tmp_path),
            patch.dict("os.environ", {"CCM_LOG_PATH": "data/cache/events.log"}),
        ):
            cmd_logs(build_parser().parse_args(["logs", "--json"]))
        data = json.loads(capsys.readouterr().out)
        assert isinstance(data, list) and data[0]["event"] == "startup"


# ── cmd_research ─────────────────────────────────────────────────────────────

class TestCmdResearch:
    def test_creates_file(self, tmp_path):
        with patch("src.cli._project_root", return_value=tmp_path):
            assert cmd_research(build_parser().parse_args(["research", "GraphRAG"])) == 0
        files = [f for f in (tmp_path / "data" / "research").glob("*.md") if f.name != "README.md"]
        assert len(files) == 1

    def test_file_contains_topic(self, tmp_path):
        with patch("src.cli._project_root", return_value=tmp_path):
            cmd_research(build_parser().parse_args(["research", "My Topic"]))
        files = list((tmp_path / "data" / "research").glob("*.md"))
        assert "My Topic" in files[0].read_text()

    def test_prints_created_path(self, tmp_path, capsys):
        with patch("src.cli._project_root", return_value=tmp_path):
            cmd_research(build_parser().parse_args(["research", "SomeTopic"]))
        assert "Created:" in capsys.readouterr().out


# ── cmd_complete (no API key) ─────────────────────────────────────────────────

class TestCmdCompleteNoKey:
    def test_returns_1_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from src.cli import cmd_complete
        assert cmd_complete(build_parser().parse_args(["complete", "hello"])) == 1

    def test_error_mentions_api_key(self, monkeypatch, capsys):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from src.cli import cmd_complete
        cmd_complete(build_parser().parse_args(["complete", "hello"]))
        assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


# ── main() integration ────────────────────────────────────────────────────────

class TestMain:
    def test_route_via_main(self, capsys):
        assert main(["route", "debug a memory leak", "--json"]) == 0
        assert "model" in json.loads(capsys.readouterr().out)

    def test_status_via_main(self):
        assert main(["status"]) == 0

    def test_version_via_main(self, capsys):
        from src.version import __version__
        assert main(["version"]) == 0
        assert __version__ in capsys.readouterr().out

    def test_doctor_via_main(self):
        assert main(["doctor"]) in (0, 1)

    def test_unknown_subcommand_exits(self):
        with pytest.raises(SystemExit):
            main(["unknown-subcommand"])


# ── cmd_build ─────────────────────────────────────────────────────────────────

class TestCmdBuild:
    def test_no_docker_returns_1(self, monkeypatch):
        import subprocess

        from src.cli import cmd_build

        def raise_not_found(*args, **kwargs):
            raise FileNotFoundError("docker not found")

        monkeypatch.setattr(subprocess, "run", raise_not_found)
        assert cmd_build(build_parser().parse_args(["build"])) == 1

    def test_returns_0_or_1(self):
        from src.cli import cmd_build

        result = cmd_build(build_parser().parse_args(["build", "--dry-run"]))
        assert result in (0, 1)

    def test_dry_run_no_actual_build(self, capsys):
        from src.cli import cmd_build

        # dry-run should not crash regardless of docker availability
        result = cmd_build(build_parser().parse_args(["build", "--dry-run"]))
        assert isinstance(result, int)

    def test_parser_no_cache_flag(self):
        args = build_parser().parse_args(["build", "--no-cache"])
        assert args.no_cache is True

    def test_parser_tag_flag(self):
        args = build_parser().parse_args(["build", "--tag", "my-image:v1"])
        assert args.tag == "my-image:v1"


# ── cmd_deploy ────────────────────────────────────────────────────────────────

class TestCmdDeploy:
    def test_dry_run_skips_containers(self, capsys):
        from src.cli import cmd_deploy

        result = cmd_deploy(build_parser().parse_args(
            ["deploy", "--dry-run", "--skip-tests", "--skip-build", "--skip-evals"]
        ))
        out = capsys.readouterr().out
        assert result in (0, 1)  # may fail due to test env, but should not crash
        assert "Deploy Summary" in out

    def test_returns_int(self):
        from src.cli import cmd_deploy

        result = cmd_deploy(build_parser().parse_args(
            ["deploy", "--dry-run", "--skip-tests", "--skip-build", "--skip-evals"]
        ))
        assert isinstance(result, int)

    def test_summary_table_shown(self, capsys):
        from src.cli import cmd_deploy

        cmd_deploy(build_parser().parse_args(
            ["deploy", "--dry-run", "--skip-tests", "--skip-build", "--skip-evals"]
        ))
        out = capsys.readouterr().out
        assert "Deploy Summary" in out

    def test_parser_env_choices(self):
        for env in ("local", "staging", "prod"):
            args = build_parser().parse_args(["deploy", "--env", env])
            assert args.env == env

    def test_parser_skip_flags(self):
        args = build_parser().parse_args(
            ["deploy", "--skip-tests", "--skip-build", "--skip-evals"]
        )
        assert args.skip_tests is True
        assert args.skip_build is True
        assert args.skip_evals is True


# ── cmd_ps ────────────────────────────────────────────────────────────────────

class TestCmdPs:
    def test_returns_int(self):
        from src.cli import cmd_ps

        result = cmd_ps(build_parser().parse_args(["ps"]))
        assert isinstance(result, int)

    def test_returns_zero(self):
        from src.cli import cmd_ps

        # Should always return 0 regardless of docker availability
        result = cmd_ps(build_parser().parse_args(["ps"]))
        assert result == 0


# ── cmd_health ────────────────────────────────────────────────────────────────

class TestCmdHealth:
    def test_unreachable_returns_1(self):
        from src.cli import cmd_health

        result = cmd_health(build_parser().parse_args(["health", "--url", "http://localhost:19999"]))
        assert result == 1

    def test_bad_url_returns_1(self):
        from src.cli import cmd_health

        result = cmd_health(build_parser().parse_args(["health", "--url", "http://0.0.0.0:1"]))
        assert result == 1

    def test_default_url_parsed(self):
        args = build_parser().parse_args(["health"])
        assert args.url == "http://localhost:8000"

    def test_custom_url_parsed(self):
        args = build_parser().parse_args(["health", "--url", "http://myhost:9000"])
        assert args.url == "http://myhost:9000"


# ── cmd_serve_mcp ─────────────────────────────────────────────────────────────

class TestCmdServeMcp:
    def test_missing_mcp_returns_1(self, monkeypatch):
        """When mcp package is not installed, cmd_serve_mcp should return 1."""
        import builtins

        from src.cli import cmd_serve_mcp

        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "src.mcp_server":
                raise ImportError("mcp not installed")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        result = cmd_serve_mcp(build_parser().parse_args(["serve-mcp"]))
        assert result == 1

    def test_subcommand_parsed(self):
        args = build_parser().parse_args(["serve-mcp"])
        assert args.command == "serve-mcp"


class TestContextDiffCommand:
    def test_context_diff_subcommand_exists(self):
        args = build_parser().parse_args(["context-diff"])
        assert args.command == "context-diff"

    def test_context_diff_default_since(self):
        args = build_parser().parse_args(["context-diff"])
        assert args.since == "HEAD~1"

    def test_context_diff_custom_since(self):
        args = build_parser().parse_args(["context-diff", "--since", "main"])
        assert args.since == "main"

    def test_context_diff_runs_successfully(self, capsys):
        from src.cli import cmd_context_diff
        args = build_parser().parse_args(["context-diff", "--since", "HEAD~1"])
        result = cmd_context_diff(args)
        # Command may return 0 (has commits) or 0 with "No changes" — both valid
        assert result == 0

    def test_context_diff_output_contains_header(self, capsys):
        from src.cli import cmd_context_diff
        args = build_parser().parse_args(["context-diff", "--since", "HEAD~1"])
        cmd_context_diff(args)
        captured = capsys.readouterr()
        assert "Context Diff" in captured.out

    def test_context_diff_in_dispatch(self):
        # Verify the command is wired into the dispatch table via parser
        args = build_parser().parse_args(["context-diff", "--since", "HEAD"])
        assert args.command == "context-diff"


class TestMemoryBankCommand:
    def test_memory_bank_status_subcommand_exists(self):
        args = build_parser().parse_args(["memory-bank", "status"])
        assert args.command == "memory-bank"
        assert args.mb_cmd == "status"

    def test_memory_bank_query_subcommand_exists(self):
        args = build_parser().parse_args(["memory-bank", "query", "routing"])
        assert args.mb_cmd == "query"
        assert args.query_term == "routing"

    def test_memory_bank_sync_subcommand_exists(self):
        args = build_parser().parse_args(["memory-bank", "sync"])
        assert args.mb_cmd == "sync"

    def test_memory_bank_status_runs_successfully(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "status"])
        result = cmd_memory_bank(args)
        assert result == 0

    def test_memory_bank_status_output_contains_header(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "status"])
        cmd_memory_bank(args)
        captured = capsys.readouterr()
        assert "Memory Bank Status" in captured.out

    def test_memory_bank_query_no_term_returns_error(self):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "sync"])
        args.mb_cmd = "query"
        args.query_term = ""
        result = cmd_memory_bank(args)
        assert result == 1

    def test_memory_bank_sync_runs_successfully(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "sync"])
        result = cmd_memory_bank(args)
        assert result == 0

    def test_memory_bank_query_returns_zero(self, capsys):
        from src.cli import cmd_memory_bank
        args = build_parser().parse_args(["memory-bank", "query", "routing"])
        result = cmd_memory_bank(args)
        assert result == 0

    def test_memory_bank_in_dispatch(self):
        args = build_parser().parse_args(["memory-bank", "status"])
        assert args.command == "memory-bank"


# ── Lint ──────────────────────────────────────────────────────────────────────

class TestLint:
    def test_lint_subcommand_exists(self):
        args = build_parser().parse_args(["lint"])
        assert args.command == "lint"

    def test_lint_fix_flag(self):
        args = build_parser().parse_args(["lint", "--fix"])
        assert args.fix is True

    def test_lint_no_cache_flag(self):
        args = build_parser().parse_args(["lint", "--no-cache"])
        assert args.no_cache is True

    def test_lint_returns_zero_on_clean_code(self, capsys):
        args = build_parser().parse_args(["lint"])
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = cmd_lint(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "clean" in captured.out

    def test_lint_returns_nonzero_on_issues(self, capsys):
        args = build_parser().parse_args(["lint"])
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = "src/foo.py:1:1: E302 error\n"
            mock_run.return_value.stderr = ""
            result = cmd_lint(args)
        assert result == 1

    def test_lint_passes_fix_flag_to_ruff(self):
        args = build_parser().parse_args(["lint", "--fix"])
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            cmd_lint(args)
        called_cmd = mock_run.call_args[0][0]
        assert "--fix" in called_cmd

    def test_lint_in_dispatch(self):
        args = build_parser().parse_args(["lint"])
        assert args.command == "lint"


# ── Deploy helpers ────────────────────────────────────────────────────────────

class TestDeployHelpers:
    def test_run_tests_returns_true_on_zero_exit(self, tmp_path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert _deploy_run_tests(tmp_path) is True

    def test_run_tests_returns_false_on_nonzero_exit(self, tmp_path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            assert _deploy_run_tests(tmp_path) is False

    def test_run_evals_returns_true_when_smoke_passes(self, tmp_path):
        # Create a minimal smoke.jsonl so the path resolves
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "smoke.jsonl").write_text("")
        with patch("src.cli._eval_run", return_value=0):
            assert _deploy_run_evals(tmp_path) is True

    def test_run_evals_returns_false_when_smoke_fails(self, tmp_path):
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "smoke.jsonl").write_text("")
        with patch("src.cli._eval_run", return_value=1):
            assert _deploy_run_evals(tmp_path) is False

    def test_check_health_returns_true_on_200(self):
        from unittest.mock import MagicMock
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: mock_resp
        mock_resp.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            assert _deploy_check_health("http://localhost:8000/health") is True

    def test_check_health_returns_false_on_timeout(self):
        with patch("urllib.request.urlopen", side_effect=OSError("refused")):
            with patch("time.time", side_effect=[0, 0, 31]):
                with patch("time.sleep"):
                    assert _deploy_check_health("http://localhost:8000/health") is False


# ── Parser sub-functions ──────────────────────────────────────────────────────

class TestParserSubFunctions:
    def test_llm_parsers_registers_route(self):
        args = build_parser().parse_args(["route", "test task"])
        assert args.command == "route"
        assert args.task == "test task"

    def test_llm_parsers_registers_complete(self):
        args = build_parser().parse_args(["complete", "hello"])
        assert args.command == "complete"
        assert args.prompt == "hello"

    def test_server_parsers_registers_serve(self):
        args = build_parser().parse_args(["serve", "--port", "9000"])
        assert args.command == "serve"
        assert args.port == 9000

    def test_server_parsers_registers_health(self):
        args = build_parser().parse_args(["health", "--url", "http://example.com"])
        assert args.command == "health"
        assert args.url == "http://example.com"

    def test_ops_parsers_registers_build(self):
        args = build_parser().parse_args(["build", "--no-cache"])
        assert args.command == "build"
        assert args.no_cache is True

    def test_ops_parsers_registers_deploy(self):
        args = build_parser().parse_args(["deploy", "--env", "staging", "--dry-run"])
        assert args.command == "deploy"
        assert args.env == "staging"
        assert args.dry_run is True

    def test_util_parsers_registers_doctor(self):
        args = build_parser().parse_args(["doctor"])
        assert args.command == "doctor"

    def test_util_parsers_registers_logs_with_flags(self):
        args = build_parser().parse_args(["logs", "--limit", "10", "--summary"])
        assert args.command == "logs"
        assert args.limit == 10
        assert args.summary is True
