# Open Findings — P2/P3 Backlog

Remaining items from v1.0.x deep-review audit. Check off when resolved.
Displayed at session start by `session-start.sh` when unchecked items exist.

---

## P2 — Quality (address when relevant)

- [x] `mcp_server.py` — `cmd_serve_mcp` imported non-existent module-level `mcp`; fixed by adding `run()` entry point
- [x] `.pre-commit-config.yaml:4` — stale finding; already pinned at `v0.9.0`
- [x] `data/evals/smoke.jsonl` — stale finding; `echo-excludes-verified` case already present
- [x] `pyproject.toml coverage.run` — removed stale omit of `src/cli.py`; tests call it directly

## P3 — Improvements (nice to have)

- [x] `evals/runner.py` — added `max_workers` to `EvalRunner` (sync); uses `ThreadPoolExecutor` when >1
- [x] `Dockerfile` — apt curl pin is fragile; added comment directing to base image digest pinning as the correct fix
- [x] `ccm eval run` — threshold now printed after summary (`threshold: 80%`)
- [x] `ci.yml:126` — live-evals condition now explicitly excludes fork PRs via `head.repo.full_name` check
