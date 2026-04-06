"""ccm — Claude Code Max CLI.

Usage:
    ccm version                         # show version, git hash, Python
    ccm route "your task"               # show routing decision (add --json)
    ccm complete "prompt"               # one-shot completion (auto-routes model)
    ccm complete "prompt" --model haiku # override model
    ccm serve [--host HOST] [--port N]  # start FastAPI server
    ccm status                          # git branch + test count + skills
    ccm doctor                          # environment health check
    ccm research "topic"                # create data/research/<date>-<slug>.md stub
    ccm logs [--event E] [--tag T]      # query indexed event log
    ccm eval list                       # list bundled eval suites
    ccm eval inspect <suite.jsonl>      # show cases with constraints
    ccm eval run <suite.jsonl>          # run suite (--dry-run  --tag  --threshold  --json)
    ccm build [--no-cache] [--tag TAG]            # build Docker image
    ccm deploy [--env local] [--dry-run]          # full deploy pipeline: test→build→up→verify
    ccm ps                                        # show running container status
    ccm health [--url URL]                        # check live service /health endpoint
    ccm context-diff [--since HEAD~1]             # structured change summary since a git ref
    ccm memory-bank [status|query <term>|sync]   # query warm/hot/glacier memory bank
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ── helpers ───────────────────────────────────────────────────────────────────

def _project_root() -> Path:
    """Return the repo root (parent of src/)."""
    return Path(__file__).parent.parent


def _print_json(data: dict) -> None:
    print(json.dumps(data, indent=2))


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    """Run a shell command, return stdout, return '?' on error."""
    try:
        return subprocess.check_output(
            cmd, cwd=cwd or _project_root(), text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "?"


# ── subcommands ───────────────────────────────────────────────────────────────

def cmd_version(_args: argparse.Namespace) -> int:
    """Print version, git commit hash, and Python version."""
    from src.version import __version__

    git_hash = _run(["git", "rev-parse", "--short", "HEAD"])
    git_branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    print(f"ccm {__version__}")
    print(f"  git : {git_hash} ({git_branch})")
    print(f"  python: {py_version}")
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    """Show the full routing decision for a task without calling the API."""
    from src.routing import route

    decision = route(args.task)
    if args.json:
        _print_json({
            "model": decision.llm.model,
            "model_reason": decision.llm.reason,
            "skill": decision.skill.skill if decision.skill else None,
            "skill_confidence": decision.skill.confidence if decision.skill else None,
            "agent": decision.agent.agent.value,
            "memory_tier": decision.memory.tier.value,
            "plan_size": decision.plan.size.value,
            "subtasks": [
                {"description": s.description, "model": s.model, "agent": s.agent}
                for s in decision.plan.subtasks
            ],
        })
    else:
        print(decision.summary())
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    """Run a completion, auto-routing the model unless --model is given."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set. Run: ccm doctor", file=sys.stderr)
        return 1

    from src.routing import route

    if args.model:
        model = args.model
        reason = "user override"
    else:
        decision = route(args.prompt)
        model = decision.llm.model
        reason = decision.llm.reason

    try:
        import anthropic
    except ImportError:
        print("Error: 'anthropic' not installed. Run: pip install anthropic", file=sys.stderr)
        return 1

    client = anthropic.Anthropic(api_key=api_key)
    kwargs: dict = {
        "model": model,
        "max_tokens": args.max_tokens,
        "messages": [{"role": "user", "content": args.prompt}],
    }
    if args.system:
        kwargs["system"] = args.system

    if not args.quiet:
        print(f"[ccm] model={model}  reason={reason}\n", file=sys.stderr)

    message = client.messages.create(**kwargs)
    content = message.content[0].text if message.content else ""

    if args.json:
        _print_json({
            "content": content,
            "model": model,
            "reason": reason,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        })
    else:
        print(content)
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """Start the FastAPI server with uvicorn."""
    try:
        import uvicorn
    except ImportError:
        print("Error: 'uvicorn' not installed. Run: pip install uvicorn", file=sys.stderr)
        return 1

    uvicorn.run(
        "src.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower(),
    )
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    """Print project status: version, git branch, test count, skills."""
    from src.version import __version__

    root = _project_root()
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    last_commit = _run(["git", "log", "-1", "--oneline"])
    dirty = _run(["git", "status", "--porcelain"])

    # Count test functions (including those in classes)
    import re as _re
    test_files = list(root.glob("tests/test_*.py"))
    _pat = _re.compile(r"^\s*(?:async\s+)?def\s+test_", _re.MULTILINE)
    test_count = sum(len(_pat.findall(f.read_text())) for f in test_files)

    # Count skills — each lives in .claude/skills/<name>/SKILL.md
    skills_dir = root / ".claude" / "skills"
    skill_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0

    # Event log summary
    log_path = root / "data" / "cache" / "events.log"
    log_info = f"{log_path}" if log_path.exists() else "no events yet"
    if log_path.exists():
        try:
            from src.utils.log_index import LogIndex
            idx = LogIndex(log_path)
            s = idx.summary()
            top = sorted(s.items(), key=lambda x: x[1], reverse=True)[:3]
            log_info = f"{len(idx)} events  top: {', '.join(f'{k}×{v}' for k, v in top)}"
        except Exception:
            pass

    print(f"version     : ccm {__version__}")
    print(f"branch      : {branch}")
    print(f"last commit : {last_commit}")
    print(f"working tree: {'dirty' if dirty else 'clean'}")
    print(f"tests       : {test_count} functions in {len(test_files)} files")
    print(f"skills      : {skill_count}")
    print(f"event log   : {log_info}")
    return 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    """Check environment health: API key, deps, paths, log."""
    root = _project_root()
    checks: list[tuple[bool, str]] = []

    # 1. API key
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    checks.append((bool(api_key), "ANTHROPIC_API_KEY is set"))

    # 2. Core package imports
    for pkg in ("anthropic", "fastapi", "uvicorn", "pydantic"):
        try:
            __import__(pkg)
            checks.append((True, f"package '{pkg}' importable"))
        except ImportError:
            checks.append((False, f"package '{pkg}' NOT found — pip install {pkg}"))

    # 3. Required project paths
    for rel in ("src/", "data/evals/", ".claude/skills/", "tasks/todo.md"):
        path = root / rel
        checks.append((path.exists(), f"path exists: {rel}"))

    # 4. Skills count
    skills_dir = root / ".claude" / "skills"
    skill_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0
    checks.append((skill_count >= 100, f"skills loaded: {skill_count} (expected ≥100)"))

    # 5. Smoke eval
    smoke_path = root / "data" / "evals" / "smoke.jsonl"
    checks.append((smoke_path.exists(), "smoke eval suite present"))

    # 6. Git repo
    git_ok = _run(["git", "rev-parse", "--is-inside-work-tree"]) == "true"
    checks.append((git_ok, "inside git repository"))

    # 7. Event log writable
    log_path = root / "data" / "cache" / "events.log"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch()
        checks.append((True, "event log writable"))
    except OSError as e:
        checks.append((False, f"event log NOT writable: {e}"))

    passed = sum(1 for ok, _ in checks if ok)
    total = len(checks)

    for ok, msg in checks:
        icon = "✓" if ok else "✗"
        print(f"  [{icon}] {msg}")

    print(f"\n{passed}/{total} checks passed", end="")
    if passed == total:
        print(" — environment healthy")
        return 0
    print(" — fix issues above before deploying")
    return 1


def cmd_lint(args: argparse.Namespace) -> int:
    """Run ruff lint on src/ and tests/ and report results."""
    import subprocess

    root = _project_root()
    cmd = [
        "python3", "-m", "ruff", "check",
        "src/", "tests/",
        "--select", "E,F,W,I",
        "--ignore", "E501",
    ]
    if args.fix:
        cmd.append("--fix")
    if args.no_cache:
        cmd.append("--no-cache")

    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode == 0:
        print("✓ lint clean")
    else:
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        print(f"\n✗ lint found issues (exit {result.returncode})", file=sys.stderr)
    return result.returncode


def cmd_logs(args: argparse.Namespace) -> int:
    """Query the indexed event log."""
    from src.utils.log_index import LogIndex

    root = _project_root()
    log_path = root / os.environ.get("CCM_LOG_PATH", "data/cache/events.log")

    if not log_path.exists():
        print("No event log found. Start the API server to generate events.")
        return 0

    idx = LogIndex(log_path)

    if args.summary:
        s = idx.summary()
        if not s:
            print("Event log is empty.")
            return 0
        print(f"{'Event':<30} {'Count':>6}")
        print("-" * 38)
        for event, count in sorted(s.items(), key=lambda x: x[1], reverse=True):
            print(f"{event:<30} {count:>6}")
        print(f"\nTotal: {len(idx)} events in {log_path}")
        return 0

    tags = [args.tag] if args.tag else None
    results = idx.search(event=args.event or None, tags=tags, limit=args.limit)

    if not results:
        print("No matching events.")
        return 0

    if args.json:
        _print_json(results)
    else:
        for rec in results:
            ts = rec.get("ts", "")[:19].replace("T", " ")
            event = rec.get("event", "?")
            extras = {k: v for k, v in rec.items() if k not in ("ts", "event")}
            extra_str = "  " + "  ".join(f"{k}={v}" for k, v in list(extras.items())[:4])
            print(f"{ts}  {event:<25}{extra_str}")

    return 0


def cmd_research(args: argparse.Namespace) -> int:
    """Write a research stub for the given topic to data/research/."""
    from src.persistence import FileStore

    store = FileStore(root=_project_root())
    path = store.write_research(
        args.topic,
        f"# {args.topic}\n\n> Research stub — fill in via /karpathy-researcher\n\n"
        f"## Key Questions\n\n- TODO\n\n## Findings\n\n- TODO\n\n## Sources\n\n- TODO\n",
    )
    print(f"Created: {path}")
    return 0


# ── deploy subcommands ────────────────────────────────────────────────────────

def cmd_build(args: argparse.Namespace) -> int:
    """Build the Docker image ccm-api:{version} and ccm-api:latest."""
    # 1. Check docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("Error: docker not found. Install Docker to use this command.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError:
        print("Error: docker is not working correctly.", file=sys.stderr)
        return 1

    from src.version import __version__

    tag = getattr(args, "tag", None) or f"ccm-api:{__version__}"
    build_tags = ["-t", tag, "-t", "ccm-api:latest"]

    # Support --dry-run: validate only
    if getattr(args, "dry_run", False):
        print(f"[dry-run] would build: docker build {' '.join(build_tags)} .")
        return 0

    cmd = ["docker", "build"]
    if getattr(args, "no_cache", False):
        cmd.append("--no-cache")
    if getattr(args, "tag", None):
        # custom tag replaces default versioned tag
        cmd += ["-t", args.tag, "-t", "ccm-api:latest"]
    else:
        cmd += ["-t", f"ccm-api:{__version__}", "-t", "ccm-api:latest"]
    cmd.append(".")

    print(f"[ccm build] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=_project_root())
    if result.returncode != 0:
        print("Error: docker build failed.", file=sys.stderr)
        return 1

    # Print image size
    try:
        size_result = subprocess.run(
            ["docker", "image", "inspect", "ccm-api:latest", "--format", "{{.Size}}"],
            capture_output=True, text=True, check=True,
        )
        size_bytes = int(size_result.stdout.strip())
        size_mb = size_bytes / (1024 * 1024)
        print(f"[ccm build] image size: {size_mb:.1f} MB")
    except (subprocess.CalledProcessError, ValueError):
        pass

    return 0


def _deploy_step_header(n: int, total: int, name: str) -> None:
    print(f"\n── {n}/{total} {name} {'─' * max(0, 40 - len(name))}")


def _deploy_run_tests(root) -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short"], cwd=root
    )
    return result.returncode == 0


def _deploy_run_compose(root) -> bool:
    result = subprocess.run(["docker", "compose", "up", "-d"], cwd=root)
    return result.returncode == 0


def _deploy_check_health(url: str) -> bool:
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                if resp.status == 200:
                    print(f"✓ service healthy ({url})")
                    return True
        except Exception:
            time.sleep(3)
    print(f"✗ health check failed — service not responding at {url} after 30s")
    return False


def _deploy_run_evals(root) -> bool:
    smoke_path = root / "data" / "evals" / "smoke.jsonl"
    smoke_args = argparse.Namespace(
        suite=str(smoke_path), dry_run=True, tag=None, threshold=0.8, json=False,
    )
    return _eval_run(smoke_args) == 0


def cmd_deploy(args: argparse.Namespace) -> int:
    """Full deploy pipeline: doctor → tests → build → compose up → health → evals."""
    host = getattr(args, "host", "127.0.0.1")
    port = getattr(args, "port", 8000)
    env = getattr(args, "env", "local")
    dry_run = getattr(args, "dry_run", False)
    skip_tests = getattr(args, "skip_tests", False)
    skip_build = getattr(args, "skip_build", False)
    skip_evals = getattr(args, "skip_evals", False)
    root = _project_root()
    total = 6
    steps: list[tuple[str, bool]] = []

    _deploy_step_header(1, total, "Doctor")
    steps.append(("Doctor", cmd_doctor(argparse.Namespace()) == 0))

    _deploy_step_header(2, total, "Tests")
    if skip_tests:
        print("[skip] --skip-tests passed")
        steps.append(("Tests", True))
    else:
        steps.append(("Tests", _deploy_run_tests(root)))

    _deploy_step_header(3, total, "Build")
    if skip_build:
        print("[skip] --skip-build passed")
        steps.append(("Build", True))
    else:
        steps.append(("Build", cmd_build(argparse.Namespace(no_cache=False, tag=None, dry_run=dry_run)) == 0))

    _deploy_step_header(4, total, "Compose up")
    if dry_run:
        print("[dry-run] skipping docker compose up")
        steps.append(("Compose up", True))
    else:
        steps.append(("Compose up", _deploy_run_compose(root)))

    _deploy_step_header(5, total, "Health check")
    if dry_run:
        print("[dry-run] skipping health check")
        steps.append(("Health check", True))
    else:
        steps.append(("Health check", _deploy_check_health(f"http://{host}:{port}/health")))

    _deploy_step_header(6, total, "Smoke evals")
    if skip_evals:
        print("[skip] --skip-evals passed")
        steps.append(("Smoke evals", True))
    else:
        steps.append(("Smoke evals", _deploy_run_evals(root)))

    print("\n── Deploy Summary " + "─" * 24)
    all_ok = all(ok for _, ok in steps)
    for step_name, ok in steps:
        print(f"  [{'✓' if ok else '✗'}] {step_name}")

    print()
    if all_ok:
        print(f"✓ Deploy to {env} complete")
        return 0
    print("✗ Deploy failed — see above for details")
    return 1


def cmd_ps(_args: argparse.Namespace) -> int:
    """Show running container status via docker compose ps."""
    try:
        subprocess.run(["docker", "compose", "ps"], cwd=_project_root())
    except FileNotFoundError:
        print("Docker not available")
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    """Check live service health via HTTP GET {url}/health."""
    url = getattr(args, "url", "http://localhost:8000")
    health_url = f"{url.rstrip('/')}/health"

    try:
        with urllib.request.urlopen(health_url, timeout=5) as resp:
            if resp.status != 200:
                print(f"✗ {health_url} returned HTTP {resp.status}", file=sys.stderr)
                return 1
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"✗ Could not reach {health_url}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    status = data.get("status", "unknown")
    version = data.get("version", "unknown")
    uptime = data.get("uptime_s")
    models = data.get("available_models", [])

    print(f"status  : {status}")
    print(f"version : {version}")
    if uptime is not None:
        print(f"uptime  : {uptime:.1f}s")
    print(f"models  : {len(models)} available")
    return 0


def cmd_memory_bank(args: argparse.Namespace) -> int:
    """Query or show status of the warm memory bank."""
    from src.persistence import TieredMemory

    mem = TieredMemory()
    subcmd = getattr(args, "mb_cmd", "status")

    if subcmd == "status":
        domains = mem.list_warm_domains()
        hot = mem.read_hot()
        glacier = mem.list_glacier()
        print("\n## Memory Bank Status\n")
        print(f"Hot tier:     {'✅ ' + str(len(hot.splitlines())) + ' lines' if hot else '⚠  empty'}")
        print(f"Warm domains: {len(domains)} — {', '.join(domains) if domains else 'none'}")
        print(f"Glacier:      {len(glacier)} archived entries")
        if domains:
            print("\n### Warm Domains")
            for d in domains:
                content = mem.read_warm(d)
                lines = content.splitlines()
                preview = lines[0].lstrip("# ") if lines else "(empty)"
                print(f"  {d:25s}  {len(lines):3d} lines  — {preview[:60]}")

    elif subcmd == "query":
        query = getattr(args, "query_term", "") or ""
        if not query:
            print("Usage: ccm memory-bank query <search term>", file=__import__("sys").stderr)
            return 1
        # Search across warm domains
        results = []
        for domain in mem.list_warm_domains():
            content = mem.read_warm(domain)
            if query.lower() in content.lower():
                # Find context line
                for ln in content.splitlines():
                    if query.lower() in ln.lower():
                        results.append((domain, ln.strip()[:100]))
                        break
        # Search glacier
        glacier_results = mem.search_glacier(query)
        print(f"\n## Memory Bank Query: '{query}'\n")
        if results:
            print("### Warm tier matches")
            for domain, snippet in results:
                print(f"  [{domain}] {snippet}")
        if glacier_results:
            print("\n### Glacier matches")
            for r in glacier_results[:5]:
                print(f"  [{r['date']}] {r['title']}: {r['snippet'][:80]}")
        if not results and not glacier_results:
            print("  No matches found.")

    elif subcmd == "sync":
        # Lightweight sync: update hot-memory timestamp and list warm domains
        domains = mem.list_warm_domains()
        mem.write_hot("memory_bank_synced", __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"))
        print(f"\n✅ Memory bank sync complete — {len(domains)} warm domain(s) up to date")

    return 0


def cmd_context_diff(args: argparse.Namespace) -> int:
    """Show a structured context summary of changes since a git ref."""
    root = _project_root()
    since = getattr(args, "since", None) or "HEAD~1"

    # Resolve "yesterday" / "last week" as time-based shortcuts
    time_aliases = {
        "yesterday": "--since='1 day ago'",
        "last-week": "--since='1 week ago'",
        "last-month": "--since='1 month ago'",
    }
    if since in time_aliases:
        log_cmd = ["git", "log", time_aliases[since], "--oneline"]
        stat_cmd = None
    else:
        log_cmd = ["git", "log", f"{since}...HEAD", "--oneline"]
        stat_cmd = ["git", "diff", "--stat", f"{since}...HEAD"]

    try:
        commits = _run(log_cmd, cwd=root)
        stat = _run(stat_cmd, cwd=root) if stat_cmd else ""
        diff_names = _run(["git", "diff", "--name-only", f"{since}...HEAD"], cwd=root)
    except Exception as e:
        print(f"Error running git: {e}", file=sys.stderr)
        return 1

    commit_lines = [ln for ln in commits.splitlines() if ln.strip()]
    file_lines = [ln for ln in diff_names.splitlines() if ln.strip()]
    stat_summary = stat.splitlines()[-1].strip() if stat else f"{len(file_lines)} files changed"

    print(f"\n## Context Diff: {since}...HEAD\n")
    print(f"### Summary\n{stat_summary}\n")

    if commit_lines:
        print("### Commits in scope")
        for c in commit_lines[:15]:
            print(f"  {c}")
        print()

    if file_lines:
        print("### Changed Files")
        for f in file_lines[:20]:
            print(f"  {f}")
        print()

    if not commit_lines and not file_lines:
        print("No changes found relative to reference:", since)

    return 0


def cmd_serve_mcp(_args: argparse.Namespace) -> int:
    """Start the MCP stdio server for Claude integration."""
    try:
        from src.mcp_server import run as _mcp_run
        _mcp_run()
        return 0
    except ImportError:
        print("Error: 'mcp' not installed. Run: pip install mcp", file=sys.stderr)
        return 1


# ── eval subcommands ──────────────────────────────────────────────────────────

def cmd_eval(args: argparse.Namespace) -> int:
    return {
        "run":     _eval_run,
        "list":    _eval_list,
        "inspect": _eval_inspect,
    }[args.eval_cmd](args)


def _eval_list(_args: argparse.Namespace) -> int:
    evals_dir = _project_root() / "data" / "evals"
    if not evals_dir.exists():
        print("No eval suites found (data/evals/ does not exist).")
        return 0
    suites = sorted(evals_dir.glob("*.jsonl"))
    if not suites:
        print("No .jsonl suites found in data/evals/")
        return 0
    for s in suites:
        lines = [ln for ln in s.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        print(f"  {s.name:<30}  {len(lines)} cases")
    return 0


def _eval_inspect(args: argparse.Namespace) -> int:
    from src.evals import EvalSuite

    path = Path(args.suite)
    if not path.exists():
        path = _project_root() / "data" / "evals" / args.suite
    if not path.exists():
        print(f"Suite not found: {args.suite}", file=sys.stderr)
        return 1

    suite = EvalSuite.from_jsonl(path)
    for case in suite:
        tags = f"  [{', '.join(case.tags)}]" if case.tags else ""
        print(f"  {case.id}{tags}")
        print(f"    prompt  : {case.prompt[:80]}")
        if case.contains:
            print(f"    contains: {case.contains}")
        if case.excludes:
            print(f"    excludes: {case.excludes}")
    return 0


def _eval_run(args: argparse.Namespace) -> int:
    from src.evals import EvalRunner, EvalSuite

    path = Path(args.suite)
    if not path.exists():
        path = _project_root() / "data" / "evals" / args.suite
    if not path.exists():
        print(f"Suite not found: {args.suite}", file=sys.stderr)
        return 1

    suite = EvalSuite.from_jsonl(path)
    if args.tag:
        suite = suite.filter_tags(args.tag)
    if not len(suite):
        print("No cases matched filters.")
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    dry_run = args.dry_run or not api_key

    if dry_run:
        print("[ccm eval] dry-run mode — echoing prompts (no API calls)\n")
        def llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            return prompt
    else:
        try:
            import anthropic
        except ImportError:
            print("Error: 'anthropic' not installed.", file=sys.stderr)
            return 1
        from src.routing import route
        client = anthropic.Anthropic(api_key=api_key)

        def llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            model = route(prompt).llm.model
            msg = client.messages.create(
                model=model, max_tokens=max_tokens, temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text if msg.content else ""

    runner = EvalRunner(llm, pass_threshold=args.threshold, verbose=True)
    report = runner.run(suite)
    print(f"\n{report.summary()}")
    print(f"  threshold: {args.threshold:.0%}")

    if args.json:
        _print_json({
            "suite": report.suite_name,
            "total": report.total,
            "passed": report.passed,
            "failed": report.failed,
            "errors": report.errors,
            "pass_rate": round(report.pass_rate, 3),
            "mean_score": round(report.mean_score, 3),
            "results": [
                {"id": r.case_id, "verdict": r.verdict.value, "score": round(r.score, 3),
                 "reason": r.reason, "latency_ms": round(r.latency_ms, 1)}
                for r in report.results
            ],
        })

    return 0 if report.failed == 0 and report.errors == 0 else 1


# ── parser ────────────────────────────────────────────────────────────────────

def _add_llm_parsers(sub) -> None:
    """Route and complete subcommands."""
    r = sub.add_parser("route", help="Show routing decision for a task")
    r.add_argument("task")
    r.add_argument("--json", action="store_true")

    c = sub.add_parser("complete", help="One-shot LLM completion")
    c.add_argument("prompt")
    c.add_argument("--system")
    c.add_argument("--model", help="Override model (skip routing)")
    c.add_argument("--max-tokens", type=int, default=4096)
    c.add_argument("--json", action="store_true")
    c.add_argument("--quiet", action="store_true", help="Suppress routing info")


def _add_server_parsers(sub) -> None:
    """Serve, ps, health, and serve-mcp subcommands."""
    s = sub.add_parser("serve", help="Start FastAPI server")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--reload", action="store_true")
    s.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    sub.add_parser("ps", help="Show running container status")

    hl = sub.add_parser("health", help="Check live /health endpoint")
    hl.add_argument("--url", default="http://localhost:8000", help="Base URL of the service")

    sub.add_parser("serve-mcp", help="Start MCP stdio server for Claude integration")


def _add_ops_parsers(sub) -> None:
    """Build and deploy subcommands."""
    bd = sub.add_parser("build", help="Build Docker image ccm-api:{version}")
    bd.add_argument("--no-cache", action="store_true", help="Pass --no-cache to docker build")
    bd.add_argument("--tag", help="Custom image tag (default: ccm-api:{version})")
    bd.add_argument("--dry-run", action="store_true", help="Validate docker is available; don't build")

    dp = sub.add_parser("deploy", help="Full deploy pipeline: doctor→tests→build→up→health→evals")
    dp.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    dp.add_argument("--dry-run", action="store_true", help="Validate all steps without starting containers")
    dp.add_argument("--skip-tests", action="store_true", help="Skip pytest step")
    dp.add_argument("--skip-build", action="store_true", help="Skip docker build step")
    dp.add_argument("--skip-evals", action="store_true", help="Skip smoke evals step")
    dp.add_argument("--host", default="127.0.0.1", help="Host to poll for health check")
    dp.add_argument("--port", type=int, default=8000, help="Port to poll for health check")


def _add_util_parsers(sub) -> None:
    """Status, doctor, logs, research, lint, memory-bank, context-diff, and eval subcommands."""
    sub.add_parser("version", help="Show version and environment info")
    sub.add_parser("status", help="Show project status")
    sub.add_parser("doctor", help="Check environment health")

    lg = sub.add_parser("logs", help="Query the indexed event log")
    lg.add_argument("--event", help="Filter by event name")
    lg.add_argument("--tag", help="Filter by tag")
    lg.add_argument("--limit", type=int, default=50, help="Max results (default 50)")
    lg.add_argument("--summary", action="store_true", help="Show count per event type")
    lg.add_argument("--json", action="store_true", help="Output as JSON")

    res = sub.add_parser("research", help="Create a research stub file")
    res.add_argument("topic")

    lt = sub.add_parser("lint", help="Run ruff on src/ and tests/")
    lt.add_argument("--fix", action="store_true", help="Auto-fix safe issues")
    lt.add_argument("--no-cache", action="store_true", help="Disable ruff cache")

    mb = sub.add_parser("memory-bank", help="Query or show status of the warm memory bank")
    mb_sub = mb.add_subparsers(dest="mb_cmd")
    mb_sub.add_parser("status", help="Show memory bank status (default)")
    mb_query = mb_sub.add_parser("query", help="Search across hot/warm/glacier tiers")
    mb_query.add_argument("query_term", help="Term to search for")
    mb_sub.add_parser("sync", help="Sync hot-memory timestamp")

    cd = sub.add_parser("context-diff", help="Show structured change summary since a git ref")
    cd.add_argument("--since", default="HEAD~1",
                    help="Git ref or alias (HEAD~5, main, yesterday, last-week)")

    ev = sub.add_parser("eval", help="Run or inspect eval suites")
    ev_sub = ev.add_subparsers(dest="eval_cmd", required=True)
    ev_sub.add_parser("list", help="List bundled eval suites")
    ev_insp = ev_sub.add_parser("inspect", help="Show cases in a suite")
    ev_insp.add_argument("suite")
    ev_run = ev_sub.add_parser("run", help="Run an eval suite")
    ev_run.add_argument("suite")
    ev_run.add_argument("--dry-run", action="store_true")
    ev_run.add_argument("--tag", help="Only run cases with this tag")
    ev_run.add_argument("--threshold", type=float, default=0.8)
    ev_run.add_argument("--json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level ccm argument parser."""
    from src.version import __version__

    p = argparse.ArgumentParser(prog="ccm", description="Claude Code Max — unified CLI")
    p.add_argument("--version", action="version", version=f"ccm {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    _add_llm_parsers(sub)
    _add_server_parsers(sub)
    _add_ops_parsers(sub)
    _add_util_parsers(sub)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "version":   cmd_version,
        "route":     cmd_route,
        "complete":  cmd_complete,
        "serve":     cmd_serve,
        "status":    cmd_status,
        "doctor":    cmd_doctor,
        "logs":      cmd_logs,
        "research":  cmd_research,
        "build":     cmd_build,
        "deploy":    cmd_deploy,
        "ps":        cmd_ps,
        "health":    cmd_health,
        "serve-mcp":     cmd_serve_mcp,
        "eval":          cmd_eval,
        "lint":          cmd_lint,
        "context-diff":  cmd_context_diff,
        "memory-bank":   cmd_memory_bank,
    }
    handler = dispatch.get(args.command)
    if handler is None:
        parser.print_help()
        return 1
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
