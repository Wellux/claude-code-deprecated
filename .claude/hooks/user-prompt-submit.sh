#!/bin/bash
# .claude/hooks/user-prompt-submit.sh
# Fires on every user message submission (UserPromptSubmit event).
# Use for: prompt logging, auto-context injection, rate limiting warnings.
# Exit 0 = allow prompt through. Exit 2 = block with message.
# Keep this FAST — it runs on every message.

BASE="/home/user/wellux_testprojects"

# ── Prompt length guard ───────────────────────────────────────────────────────
# Warn if the prompt is very long (might indicate pasted content that should be a file)
PROMPT_LEN="${#CLAUDE_USER_PROMPT}"
if [ "$PROMPT_LEN" -gt 8000 ] 2>/dev/null; then
  echo "  ⚠  Long prompt detected (${PROMPT_LEN} chars). Consider writing to a file instead."
fi

# ── Branch safety check ──────────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo ""
  echo "  ⚠  WARNING: You are on branch '$BRANCH'. Commits will go to main."
  echo "  Consider: git checkout -b claude/<feature>-$(date +%s | tail -c 5)"
  echo ""
fi

exit 0
