#!/bin/bash
# Daily GitHub Trending Research — Claude Code & Agent Patterns
# Cron: 0 7 * * * cd /home/user/wellux_testprojects && bash tools/scripts/github-trending-research.sh >> data/cache/cron-github-research.log 2>&1

set -euo pipefail

BASE="/home/user/wellux_testprojects"
DATE=$(date +%Y-%m-%d)
OUT="$BASE/data/research/${DATE}-github-trending-claude-code.md"
LOG="$BASE/data/research/README.md"
LESSONS="$BASE/tasks/lessons.md"

echo "================================================"
echo "  GITHUB TRENDING RESEARCH — $DATE"
echo "  Topic: Claude Code + Agent Patterns"
echo "================================================"

mkdir -p "$BASE/data/research" "$BASE/data/cache"

# Initialize research index if missing
if [ ! -f "$LOG" ]; then
    echo "# Research Index" > "$LOG"
    echo "" >> "$LOG"
    echo "Auto-populated by research-agent and github-trending-research scripts." >> "$LOG"
    echo "" >> "$LOG"
fi

# Write structured research stub — populated by Claude Code on next session
cat > "$OUT" << STUB
# GitHub Trending Research: Claude Code & Agent Patterns
**Date:** $DATE
**Method:** GitHub API → Trending → Filter → Distill → Implement

## Summary
Auto-populated by running: \`ccm research "Claude Code trending repos $DATE"\`

## Trending Repos Scanned
<!-- claude --print "Search GitHub for trending claude-code, anthropic, mcp-server repos.
List top 10 with: name, stars, description, key pattern to implement.
Focus on: agent loops, skill systems, hook patterns, MCP servers, eval frameworks." -->

### Top Patterns This Week

| Repo | Stars | Pattern | Priority |
|------|-------|---------|----------|
| [To be populated] | - | Run ccm research to populate | - |

## Implemented This Run

### New Techniques
- [ ] Review and implement patterns from trending repos
- [ ] Update .claude/skills/ with any new skill patterns found
- [ ] Update docs/resources.md with notable new repos
- [ ] Add any architectural insights to tasks/lessons.md

## Key Signals

### Agent Loop Patterns
[Search result content — populate via /karpathy-researcher]

### MCP Server Patterns
[New MCP servers worth integrating]

### Skill/Hook Patterns
[Novel skill frontmatter or hook guard patterns]

### Eval Framework Patterns
[Eval methodologies worth adopting]

## Action Items
1. Run: \`/karpathy-researcher "Claude Code agent patterns $DATE"\`
2. Scan: awesome-claude-code, anthropic/claude-code-sdk
3. Check: Anthropic changelog for new hooks, tools, MCP capabilities
4. Update: docs/resources.md with new entries

## Distilled Insight
[One paragraph — the most important thing learned today]

## Sources
- https://github.com/trending?l=python&since=daily (filter: claude, anthropic, mcp)
- https://github.com/hesreallyhim/awesome-claude-code
- https://docs.anthropic.com/claude-code (changelog)
STUB

# Append to research index
echo "- [GitHub Trending Claude Code — $DATE](./${DATE}-github-trending-claude-code.md)" >> "$LOG"

echo ""
echo "Research stub written: $OUT"
echo ""
echo "To populate with live data, run in Claude Code:"
echo "  ccm research \"Claude Code trending repos and patterns $DATE\""
echo "  or: /karpathy-researcher Claude Code GitHub trending $DATE"
echo ""

# Log event for audit trail
EVENTS="$BASE/data/cache/events.log"
echo "{\"event\":\"github_trending_research\",\"date\":\"$DATE\",\"stub\":\"$OUT\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "$EVENTS"

echo "================================================"
echo "  Done. Stub ready for Claude Code to populate."
echo "================================================"
