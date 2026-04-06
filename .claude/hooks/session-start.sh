#!/bin/bash
# .claude/hooks/session-start.sh
# ADVANCED BOOT — runs every session start
# Loads: hot-memory, recent session log, MASTER_PLAN status, health checks
# Exit 0 = allow session to continue (always)

BASE="/home/user/wellux_testprojects"

# ── Header ────────────────────────────────────────────────────────────────────
echo ""
printf '\033[1;34m╔══════════════════════════════════════════════════════════╗\033[0m\n'
printf '\033[1;34m║\033[0m  \033[1m\033[1;37mCLAUDE CODE MAX\033[0m  \033[2m—  session boot\033[0m                        \033[1;34m║\033[0m\n'
printf '\033[1;34m║\033[0m  \033[2m%s\033[0m                                   \033[1;34m║\033[0m\n' "$(date '+%Y-%m-%d  %H:%M:%S')"
printf '\033[1;34m╚══════════════════════════════════════════════════════════╝\033[0m\n'
echo ""

# ── Git + version status ──────────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
UNSTAGED=$(git -C "$BASE" status --short 2>/dev/null | head -3)
REMOTE_URL=$(git -C "$BASE" remote get-url origin 2>/dev/null || echo "no remote")
VERSION=$(grep '^version = ' "$BASE/pyproject.toml" 2>/dev/null | sed 's/version = "//;s/"//' || echo "unknown")

printf '  \033[1;35m▸ Repo\033[0m    wellux_testprojects  \033[2m(%s)\033[0m\n' "$REMOTE_URL"
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  printf '  \033[1;35m▸ Branch\033[0m  \033[1;31m%s\033[0m  ⚠ WARNING: on main!\n' "$BRANCH"
else
  printf '  \033[1;35m▸ Branch\033[0m  \033[1;32m%s\033[0m\n' "$BRANCH"
fi
printf '  \033[1;35m▸ Version\033[0m \033[1;32mv%s\033[0m\n' "$VERSION"
if [ -n "$UNSTAGED" ]; then
  DIFF_STAT=$(git -C "$BASE" diff --stat HEAD 2>/dev/null | tail -1 | xargs)
  printf '  \033[1;33m▸ Changes\033[0m \033[1;33munstaged:  %s\033[0m\n' "$DIFF_STAT"
fi
echo ""

# ── Recent commits (5) ───────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Recent Commits (5) ──────────────────────────────────\033[0m\n'
git -C "$BASE" log -5 --oneline 2>/dev/null | sed 's/^\([a-f0-9]*\)  \(.*\)/  \x1b[2m\1\x1b[0m  \2/'
echo ""

# ── MASTER_PLAN status ────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── MASTER_PLAN ─────────────────────────────────────────\033[0m\n'
if [ -f "$BASE/MASTER_PLAN.md" ]; then
  DONE=$(grep -c "^- \[x\]" "$BASE/MASTER_PLAN.md" 2>/dev/null || echo 0)
  TOTAL=$(grep -c "^- \[" "$BASE/MASTER_PLAN.md" 2>/dev/null || echo 0)
  NEXT=$(grep -m1 "^- \[ \]" "$BASE/MASTER_PLAN.md" 2>/dev/null | sed 's/^- \[ \] //')
  if [ -n "$NEXT" ]; then
    printf '  \033[1;33m▶ Next:\033[0m \033[2m%s\033[0m\n' "$NEXT"
    printf '  \033[2m%s/%s steps done\033[0m\n' "$DONE" "$TOTAL"
  else
    printf '  \033[1;32m✔ Complete!\033[0m \033[2m%s/%s steps done\033[0m\n' "$DONE" "$TOTAL"
  fi
fi
echo ""

# ── Open tasks ────────────────────────────────────────────────────────────────
OPEN_COUNT=$(grep "^- \[ \]" "$BASE/tasks/todo.md" 2>/dev/null | wc -l | tr -d ' ')
printf '  \033[1m\033[1;36m── Open Tasks (%s) ─────────────────────────────────────\033[0m\n' "$OPEN_COUNT"
if [ "$OPEN_COUNT" -eq 0 ] 2>/dev/null; then
  printf '  \033[1;32m✔ No open tasks\033[0m\n'
else
  grep "^- \[ \]" "$BASE/tasks/todo.md" 2>/dev/null | head -5 | sed 's/^- \[ \] /  ▸ /'
fi
echo ""

# ── Open findings (P2/P3 backlog) ─────────────────────────────────────────────
FINDINGS="$BASE/tasks/open-findings.md"
if [ -f "$FINDINGS" ]; then
  OPEN_F=$(grep "^- \[ \]" "$FINDINGS" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$OPEN_F" -gt 0 ]; then
    printf '  \033[1m\033[1;33m── Open Findings (%s) ──────────────────────────────────\033[0m\n' "$OPEN_F"
    grep "^- \[ \]" "$FINDINGS" | head -5 | while IFS= read -r line; do
      printf '  \033[1;33m▸\033[0m %s\n' "${line#- \[ \] }"
    done
    echo ""
  fi
fi

# ── Last session ──────────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Last Session ────────────────────────────────────────\033[0m\n'
LAST_LOG=$(ls -t "$BASE/data/sessions/"*.md 2>/dev/null | head -1)
if [ -n "$LAST_LOG" ]; then
  printf '  \033[2m%s\033[0m\n' "$(basename "$LAST_LOG")"
  tail -15 "$LAST_LOG" | grep -v "^$" | head -10 | sed 's/^/  /'
else
  printf '  \033[2m(no session logs yet)\033[0m\n'
fi
echo ""

# ── Context snapshot (from hot-memory.md) ────────────────────────────────────
HOT_MEM="$BASE/.claude/memory/hot/hot-memory.md"
if [ -f "$HOT_MEM" ]; then
  printf '  \033[1m\033[1;36m── Context Snapshot ────────────────────────────────────\033[0m\n'
  # Show full dynamic zone (between DYNAMIC marker and STATIC marker)
  awk '
    /<!-- DYNAMIC:/{dyn=1; next}
    /<!-- STATIC:/{dyn=0}
    dyn && NF{print "  "$0}
  ' "$HOT_MEM"
  echo ""
  # Show static zone section headings as a map
  STATIC_SECTIONS=$(awk '/<!-- STATIC:/{found=1} found && /^## /{print $0}' "$HOT_MEM")
  if [ -n "$STATIC_SECTIONS" ]; then
    printf '  \033[2m[Curated in hot-memory.md:]\033[0m'
    echo "$STATIC_SECTIONS" | while IFS= read -r sec; do
      printf '  \033[2m%s\033[0m' "$sec  "
    done
    echo ""
    echo ""
  fi
fi

# ── Last 3 lessons ────────────────────────────────────────────────────────────
if [ -f "$BASE/tasks/lessons.md" ]; then
  LESSON_COUNT=$(grep -c "^### Lesson" "$BASE/tasks/lessons.md" 2>/dev/null || echo 0)
  printf '  \033[1m\033[1;36m── Last 3 Lessons (of %s total) ────────────────────────\033[0m\n' "$LESSON_COUNT"
  awk '
    /^### Lesson [0-9]+/{
      if(in_l && buf!="") lessons[++c]=buf;
      buf=""; in_l=1
    }
    /^---/{in_l=0}
    in_l{buf=buf"\n"$0}
    END{
      if(in_l && buf!="") lessons[++c]=buf;
      start=(c>3)?(c-2):1;
      for(i=start;i<=c;i++) print lessons[i]
    }
  ' "$BASE/tasks/lessons.md" | head -30 | sed 's/^/  /'
fi
echo ""

# ── Project health ────────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Project Health ──────────────────────────────────────\033[0m\n'
cd "$BASE" 2>/dev/null || true

PYTHON_VER=$(python3 --version 2>&1 | sed 's/Python //')
printf '  \033[0;34m▸ Python\033[0m  %s\n' "$PYTHON_VER"

TEST_COUNT=$(grep -rE '^\s*(async\s+)?def test_' tests/ 2>/dev/null | wc -l | tr -d ' ')
printf '  \033[0;34m▸ Tests\033[0m   \033[1;32m%s functions\033[0m\n' "$TEST_COUNT"

LINT_ERRORS=$(python3 -m ruff check src/ tests/ --select E,F,W --ignore E501 --quiet 2>/dev/null | wc -l | tr -d ' ')
if [ "$LINT_ERRORS" -eq 0 ] 2>/dev/null; then
  printf '  \033[0;34m▸ Lint\033[0m    \033[1;32mCLEAN\033[0m  \033[2m(ruff)\033[0m\n'
else
  printf '  \033[0;34m▸ Lint\033[0m    \033[1;31m%s issue(s)\033[0m\n' "$LINT_ERRORS"
fi

SKILL_COUNT=$(find "$BASE/.claude/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
printf '  \033[0;34m▸ Skills\033[0m  %s loaded\n' "$SKILL_COUNT"

# Docker status
if docker compose -f "$BASE/docker-compose.yml" ps 2>/dev/null | grep -q "running"; then
  printf '  \033[0;34m▸ Docker\033[0m  \033[1;32mrunning\033[0m\n'
else
  printf '  \033[0;34m▸ Docker\033[0m  \033[2mcompose available (not running)\033[0m\n'
fi
echo ""

# ── Daily session log ─────────────────────────────────────────────────────────
TODAY_LOG="$BASE/data/sessions/$(date '+%Y-%m-%d').md"
if [ -f "$TODAY_LOG" ]; then
  printf '  \033[2m▸ Session log: data/sessions/%s.md\033[0m\n' "$(date '+%Y-%m-%d')"
  echo ""
else
  mkdir -p "$BASE/data/sessions"
  cat > "$TODAY_LOG" << LOGEOF
# Session Log — $(date '+%Y-%m-%d')

## Session Start — $(date '+%H:%M:%S')
- Branch: $BRANCH
- Version: v$VERSION
- Open tasks: $OPEN_COUNT
LOGEOF
  printf '  \033[2m▸ Created session log: data/sessions/%s.md\033[0m\n' "$(date '+%Y-%m-%d')"
  echo ""
fi

# ── Shortcuts ─────────────────────────────────────────────────────────────────
printf '  \033[1m\033[1;36m── Shortcuts ───────────────────────────────────────────\033[0m\n'
printf '  \033[1;37mf\033[0m → next step    \033[1;37ms\033[0m → status    \033[1;37mr\033[0m → research    \033[1;37ma\033[0m → audit\n'
printf '  \033[2m/brainstorm  /write-plan  /superpowers  /office-hours  /ship\033[0m\n'
printf '\033[1;34m════════════════════════════════════════════════════════════\033[0m\n'
echo ""

exit 0
