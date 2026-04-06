"""MCP stdio server — exposes ccm operations as MCP tools.

Run directly:  python -m src.mcp_server
Via ccm:       ccm serve-mcp

Tools exposed:
  deploy   — Run full deploy pipeline (test → build → up → verify)
  build    — Build the Docker image
  health   — Check live service health
  status   — Show project status
  doctor   — Run environment health check
  logs     — Query indexed event log

Install: pip install ".[deploy]"  (adds mcp>=1.0.0)
"""
from __future__ import annotations

import argparse
import contextlib
import io
import sys


def _require_fastmcp():
    """Import FastMCP or exit with a helpful message if mcp is not installed."""
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

        return FastMCP
    except ImportError as exc:
        print(
            "Error: 'mcp' package not installed.\n"
            "Install with: pip install 'mcp>=1.0.0'\n"
            "Or: pip install '.[deploy]'",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc


def _capture(fn, args: argparse.Namespace) -> str:
    """Call fn(args) while capturing stdout; return captured output."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(args)
    return buf.getvalue()


def _make_args(**kwargs) -> argparse.Namespace:
    """Build a simple Namespace from keyword arguments."""
    return argparse.Namespace(**kwargs)


# ── Tool functions (plain Python — registered with MCP server in _build_server) ──


def deploy(
    env: str = "local",
    dry_run: bool = False,
    skip_tests: bool = False,
    skip_build: bool = False,
    skip_evals: bool = False,
) -> str:
    """Run the full deploy pipeline: doctor → tests → build → compose up → health → evals.

    Args:
        env: Target environment (local, staging, prod).
        dry_run: Validate all steps without starting containers.
        skip_tests: Skip pytest step.
        skip_build: Skip docker build step.
        skip_evals: Skip smoke evals step.
    """
    from src.cli import cmd_deploy

    args = _make_args(
        env=env,
        dry_run=dry_run,
        skip_tests=skip_tests,
        skip_build=skip_build,
        skip_evals=skip_evals,
        host="127.0.0.1",
        port=8000,
    )
    return _capture(cmd_deploy, args)


def build(no_cache: bool = False, tag: str | None = None) -> str:
    """Build the Docker image ccm-api:{version} and ccm-api:latest.

    Args:
        no_cache: Pass --no-cache to docker build.
        tag: Custom image tag (default: ccm-api:{version}).
    """
    from src.cli import cmd_build

    args = _make_args(no_cache=no_cache, tag=tag, dry_run=False)
    return _capture(cmd_build, args)


def health(url: str = "http://localhost:8000") -> str:
    """Check live service health endpoint.

    Args:
        url: Base URL of the running service.
    """
    from src.cli import cmd_health

    args = _make_args(url=url)
    return _capture(cmd_health, args)


def status() -> str:
    """Show project status: version, git branch, test count, skills, event log."""
    from src.cli import cmd_status

    args = _make_args()
    return _capture(cmd_status, args)


def doctor() -> str:
    """Run environment health check. Returns 'HEALTHY' or 'ISSUES FOUND' at end."""
    from src.cli import cmd_doctor

    args = _make_args()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = cmd_doctor(args)
    output = buf.getvalue()
    verdict = "HEALTHY" if rc == 0 else "ISSUES FOUND"
    return f"{output}\n{verdict}"


def get_logs(
    event: str | None = None,
    tag: str | None = None,
    limit: int = 50,
    summary: bool = False,
) -> str:
    """Query the indexed event log.

    Args:
        event: Filter by event name.
        tag: Filter by tag.
        limit: Maximum number of results.
        summary: Show count per event type instead of individual records.
    """
    from src.cli import cmd_logs

    args = _make_args(event=event, tag=tag, limit=limit, summary=summary, json=False)
    return _capture(cmd_logs, args)


def _build_server():
    """Create and register tool functions with FastMCP. Deferred so import is safe."""
    FastMCP = _require_fastmcp()
    mcp = FastMCP("ccm", instructions="Claude Code Max deployment and operations server")
    for fn in (deploy, build, health, status, doctor, get_logs):
        mcp.tool()(fn)
    return mcp


def run() -> None:
    """Entry point for ``ccm serve-mcp``."""
    _build_server().run()


if __name__ == "__main__":
    run()
