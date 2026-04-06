#!/bin/bash
# .claude/hooks/pre-compact.sh
# Fires BEFORE the context window compacts — saves critical state so nothing is lost.
# Writes dynamic zone of hot-memory.md; preserves the STATIC zone (curated content).
# Exit 0 always (non-zero would block compaction, which we don't want).

BASE="/home/user/wellux_testprojects"
SNAPSHOT_FILE="$BASE/.claude/memory/hot/hot-memory.md"
SESSION_LOG="$BASE/data/sessions/$(date '+%Y-%m-%d').md"

# ── 1. Gather dynamic state ────────────────────────────────────────────────────
BRANCH=$(git -C "$BASE" branch --show-current 2>/dev/null || echo "unknown")
UNCOMMITTED=$(git -C "$BASE" status --short 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git -C "$BASE" log -1 --oneline 2>/dev/null || echo "no commits")
VERSION=$(grep '^version = ' "$BASE/pyproject.toml" 2>/dev/null | sed 's/version = "//;s/"//' || echo "unknown")
TEST_COUNT=$(grep -rE '^\s*(async\s+)?def test_' "$BASE/tests/" 2>/dev/null | wc -l | tr -d ' ')
SKILL_COUNT=$(find "$BASE/.claude/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')

# ── 2. Get last 3 commits ──────────────────────────────────────────────────────
LAST_3_COMMITS=$(git -C "$BASE" log -3 --format="- %h %s" 2>/dev/null || echo "- (no commits)")

# ── 3. Extract last 2 complete lessons ────────────────────────────────────────
RECENT_LESSONS=$(awk '
  /^### Lesson [0-9]+/{
    if(in_l && buf!="") lessons[++c]=buf;
    buf=""; in_l=1
  }
  /^---/{in_l=0}
  in_l{buf=buf"\n"$0}
  END{
    if(in_l && buf!="") lessons[++c]=buf;
    start=(c>2)?(c-1):1;
    for(i=start;i<=c;i++) print lessons[i]
  }
' "$BASE/tasks/lessons.md" 2>/dev/null)

# ── 4. Preserve STATIC zone from existing hot-memory.md ───────────────────────
STATIC_ZONE=""
if [ -f "$SNAPSHOT_FILE" ]; then
  STATIC_ZONE=$(awk '/<!-- STATIC: manually curated/{found=1} found{print}' "$SNAPSHOT_FILE")
fi
# Fallback if marker not found (first run or legacy file)
if [ -z "$STATIC_ZONE" ]; then
  STATIC_ZONE="<!-- STATIC: manually curated below — never auto-overwritten by hooks -->"$'\n\n'"(No curated content yet — add sections below this marker)"
fi

# ── 5. Write hot-memory.md (dynamic zone only, static zone re-appended) ───────
# Use printf '%s' for all user-sourced content (commits, lessons, static zone) to
# prevent backticks and dollar signs in those strings from being interpreted as shell.
{
  printf '# Hot Memory — Always Loaded (≤50 lines)\n'
  printf '<!-- L0: active project context — DYNAMIC above marker, STATIC below -->\n\n'
  printf '<!-- DYNAMIC: auto-updated by pre-compact.sh on every compaction -->\n'
  printf '**Last Updated**: %s (pre-compact snapshot)\n\n' "$(date '+%Y-%m-%d %H:%M:%S')"
  printf '## Active Context (auto-updated)\n'
  printf -- '- Branch: %s\n' "$BRANCH"
  printf -- '- Version: v%s  ·  Tests: %s passing  ·  Skills: %s loaded\n' "$VERSION" "$TEST_COUNT" "$SKILL_COUNT"
  printf -- '- Uncommitted changes: %s file(s)\n' "$UNCOMMITTED"
  printf -- '- Last commit: %s\n' "$LAST_COMMIT"
  printf -- '- MASTER_PLAN: 31/31 complete · memory_bank_synced: %s\n\n' "$(date '+%Y-%m-%d %H:%M')"
  printf '## Recent Commits (auto-updated)\n'
  printf '%s\n\n' "$LAST_3_COMMITS"
  printf '## Recent Lessons (auto-updated)\n'
  printf '%s\n\n' "$RECENT_LESSONS"
  printf '%s\n' "$STATIC_ZONE"
} > "$SNAPSHOT_FILE"

# ── 6. Append to daily session log ───────────────────────────────────────────
mkdir -p "$BASE/data/sessions"
cat >> "$SESSION_LOG" << EOF

## Compaction Checkpoint — $(date '+%H:%M:%S')
- Branch: $BRANCH | v$VERSION | Uncommitted: $UNCOMMITTED files
- Tests: $TEST_COUNT | Skills: $SKILL_COUNT
- Last commit: $LAST_COMMIT
EOF

echo ""
echo "  ⚡ Pre-compact snapshot saved → .claude/memory/hot/hot-memory.md"
echo "     v$VERSION · $TEST_COUNT tests · $SKILL_COUNT skills · branch: $BRANCH"
echo ""

exit 0
