#!/bin/bash
# .claude/hooks/stop.sh
# Runs when Claude Code session ends.
# Validates completion criteria, writes daily session log, shows checklist.
# Exit 0 always.

BASE="/home/user/wellux_testprojects"
SESSION_LOG="$BASE/data/sessions/$(date '+%Y-%m-%d').md"

# ── 1. Gather session stats ───────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
UNCOMMITTED=$(git -C "$BASE" status --short 2>/dev/null | wc -l | tr -d ' ')
OPEN_TASKS=$(grep "^- \[ \]" "$BASE/tasks/todo.md" 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git -C "$BASE" log -1 --oneline 2>/dev/null || echo "no commits")

# ── 2. Run completion validators ─────────────────────────────────────────────
WARNINGS=""

if [ "$UNCOMMITTED" -gt 0 ] 2>/dev/null; then
  WARNINGS="${WARNINGS}\n  ⚠  $UNCOMMITTED uncommitted file(s) — consider committing"
fi

if [ "$OPEN_TASKS" -gt 0 ] 2>/dev/null; then
  WARNINGS="${WARNINGS}\n  ⚠  $OPEN_TASKS open task(s) in todo.md — update before closing"
fi

# Check lint (fast, non-blocking)
LINT_ERRORS=$(python3 -m ruff check "$BASE/src" "$BASE/tests" --select E,F,W --ignore E501 --quiet 2>/dev/null | wc -l | tr -d ' ')
if [ "$LINT_ERRORS" -gt 0 ] 2>/dev/null; then
  WARNINGS="${WARNINGS}\n  ⚠  $LINT_ERRORS lint error(s) — run: ruff check src/ tests/ --select E,F,W --ignore E501"
fi

# ── 3. Write daily session log ────────────────────────────────────────────────
mkdir -p "$BASE/data/sessions"
cat >> "$SESSION_LOG" << LOGEOF

## Session End — $(date '+%H:%M:%S')
- Branch: $BRANCH
- Uncommitted files: $UNCOMMITTED
- Open tasks: $OPEN_TASKS
- Last commit: $LAST_COMMIT
LOGEOF

# ── 4. Append session end marker to todo.md ──────────────────────────────────
if [ -f "$BASE/tasks/todo.md" ]; then
  echo "" >> "$BASE/tasks/todo.md"
  echo "<!-- Session ended: $(date '+%Y-%m-%d %H:%M:%S') -->" >> "$BASE/tasks/todo.md"
fi

# ── 5. Display session summary ───────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  SESSION COMPLETE — $(date '+%Y-%m-%d %H:%M:%S')        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  Branch:          $BRANCH"
echo "  Uncommitted:     $UNCOMMITTED file(s)"
echo "  Open tasks:      $OPEN_TASKS"
echo "  Last commit:     $LAST_COMMIT"
echo ""

if [ -n "$WARNINGS" ]; then
  echo "  ── VALIDATORS ──────────────────────────────────────"
  printf "%b\n" "$WARNINGS"
  echo ""
fi

echo "  ── SESSION CHECKLIST ───────────────────────────────"
if [ "$UNCOMMITTED" -eq 0 ] 2>/dev/null; then
  echo "  ✅ All changes committed"
else
  echo "  □  Commit uncommitted changes"
fi
if [ "$OPEN_TASKS" -eq 0 ] 2>/dev/null; then
  echo "  ✅ No open tasks"
else
  echo "  □  Update tasks/todo.md ($OPEN_TASKS open)"
fi
if [ "$LINT_ERRORS" -eq 0 ] 2>/dev/null; then
  echo "  ✅ Lint clean"
else
  echo "  □  Fix $LINT_ERRORS lint error(s)"
fi
echo "  □  Add lessons to tasks/lessons.md (corrections?)"
echo "  □  Push to origin: git push -u origin $BRANCH"
echo ""
echo "  Session log: data/sessions/$(date '+%Y-%m-%d').md"
echo "════════════════════════════════════════════════════════"
echo ""

exit 0
