---
name: cron-scheduler
description: >
  Set up cron jobs and scheduled tasks. Invoke for: "schedule this", "run every day",
  "cron job", "scheduled task", "automation schedule", "run weekly", "cron expression",
  "set up recurring task". Also integrates with Claude Code's /schedule skill.
argument-hint: task to schedule and frequency (e.g. "research-agent every Monday 6am")
allowed-tools: Read, Write, Bash
---

# Skill: Cron Scheduler — Recurring Task Automation
**Category:** Optimization/Research

## Role
Set up cron schedules for recurring automation tasks including the optimizer crons in tools/scripts/.

## When to invoke
- "schedule this to run every X"
- Setting up optimizer crons
- Recurring Claude Code agent triggers
- Automation scheduling

## Instructions
1. Write cron expression: `minute hour day month weekday`
2. Add to crontab or create systemd timer
3. Log output: redirect to log file with timestamps
4. Alert on failure: use `|| notify_on_fail` pattern
5. Document: what runs when and why

## Common Crons for This Project
```bash
# Daily 6am: doc optimization
0 6 * * * cd /home/user/wellux_testprojects && bash tools/scripts/optimize-docs.sh >> data/cache/cron-optimize-docs.log 2>&1

# Monday 6am: Karpathy research loop
0 6 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/research-agent.sh >> data/cache/cron-research.log 2>&1

# Sunday midnight: security + perf audit
0 0 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/security-scan.sh >> data/cache/cron-security.log 2>&1
0 1 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/perf-audit.sh >> data/cache/cron-perf.log 2>&1

# Weekly: self-improve
0 8 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/self-improve.sh >> data/cache/cron-improve.log 2>&1
```

## Example
/cron-scheduler set up all optimizer crons for this project
