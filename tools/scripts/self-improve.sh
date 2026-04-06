#!/bin/bash
# Self-improvement loop — distill lessons.md → improvement tasks → commit
# Cron: 0 8 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/self-improve.sh >> data/cache/cron-improve.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
LESSONS="tasks/lessons.md"
TODO="tasks/todo.md"

echo "================================================"
echo "  SELF-IMPROVE — $DATE"
echo "================================================"

if [ ! -f "$LESSONS" ]; then
    echo "No lessons.md found — nothing to process."
    exit 0
fi

# Count lessons added since last run (look for entries from this week)
LESSON_COUNT=$(grep -c "^##" "$LESSONS" 2>/dev/null || echo 0)
echo "Total lessons captured: $LESSON_COUNT"

# Extract lessons not yet turned into tasks (heuristic: look for [TODO] tag)
NEW_INSIGHTS=$(grep -A2 "^## " "$LESSONS" | grep -v "^## " | grep -v "^--$" | head -20 || true)

echo ""
echo "Recent lessons:"
tail -20 "$LESSONS"

# Append improvement task to todo.md
echo "" >> "$TODO"
echo "## Self-Improvement Tasks — $DATE" >> "$TODO"
echo "- [ ] Review lessons.md and apply top 3 patterns to CLAUDE.md" >> "$TODO"
echo "- [ ] Run /optimize-docs to check skill freshness" >> "$TODO"
echo "- [ ] Run /perf-profiler on any new bottlenecks identified" >> "$TODO"

echo ""
echo "Improvement tasks appended to $TODO"

# Git commit the lessons progress
if git -C . diff --quiet "$LESSONS" 2>/dev/null; then
    echo "No changes to lessons.md — nothing to commit."
else
    git -C . add "$LESSONS" "$TODO" 2>/dev/null || true
    git -C . commit -m "chore: weekly self-improvement cycle $DATE

- Processed $LESSON_COUNT lessons
- Added improvement tasks to todo.md
- Run /self-improve for deep analysis" 2>/dev/null || echo "Git commit skipped (no changes staged)"
fi

echo ""
echo "Self-improve complete."
echo "Next: run Claude Code and type 'a' for full audit."
echo "================================================"
