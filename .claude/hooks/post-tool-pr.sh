#!/bin/bash
# .claude/hooks/post-tool-pr.sh
# Fires after a PR is created (PostToolUse on Bash commands that contain "gh pr create")
# Auto-runs code simplification review on changed files.
# Exit 0 always.

BASE="/home/user/wellux_testprojects"

# Only run if the last command created a PR
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"
if echo "$TOOL_INPUT" | grep -q "gh pr create"; then
  echo ""
  echo "  ── POST-PR SIMPLIFICATION ──────────────────────────"
  echo "  PR created. Checking for simplification opportunities..."

  # Get files changed in this branch vs main
  CHANGED_FILES=$(git -C "$BASE" diff --name-only origin/main...HEAD 2>/dev/null | grep -E '\.py$' | head -10)

  if [ -n "$CHANGED_FILES" ]; then
    echo "  Python files changed in this PR:"
    echo "$CHANGED_FILES" | sed 's/^/    /'
    echo ""
    echo "  ℹ  Tip: run /simplify to check these files for refactoring opportunities"
  fi
  echo "════════════════════════════════════════════════════════"
  echo ""
fi

exit 0
