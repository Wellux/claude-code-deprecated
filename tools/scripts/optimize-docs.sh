#!/bin/bash
# Daily doc optimization — checks freshness, broken links, outdated content
# Cron: 0 6 * * * cd /home/user/wellux_testprojects && bash tools/scripts/optimize-docs.sh >> data/cache/cron-optimize-docs.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
ISSUES=0

echo "================================================"
echo "  DOC OPTIMIZER — $DATE"
echo "================================================"

# 1. Check all .md files for last-modified > 30 days
echo ""
echo "[1] Checking doc freshness (>30 days old)..."
find . -name "*.md" \
    -not -path "./.git/*" \
    -not -path "./data/*" \
    -mtime +30 \
    -printf "  STALE: %p (modified: %TY-%Tm-%Td)\n" 2>/dev/null || true

# 2. Check CLAUDE.md line count (should be <200)
echo ""
echo "[2] Checking CLAUDE.md size..."
if [ -f "CLAUDE.md" ]; then
    LINES=$(wc -l < CLAUDE.md)
    if [ "$LINES" -gt 200 ]; then
        echo "  WARNING: CLAUDE.md is $LINES lines (target: <200)"
        ISSUES=$((ISSUES + 1))
    else
        echo "  OK: CLAUDE.md is $LINES lines"
    fi
fi

# 3. Check skills have required frontmatter
echo ""
echo "[3] Checking skill frontmatter..."
SKILL_ERRORS=0
for skill_dir in .claude/skills/*/; do
    skill_file="$skill_dir/SKILL.md"
    if [ -f "$skill_file" ]; then
        if ! grep -q "^name:" "$skill_file"; then
            echo "  MISSING name: $skill_file"
            SKILL_ERRORS=$((SKILL_ERRORS + 1))
        fi
        if ! grep -q "^description:" "$skill_file"; then
            echo "  MISSING description: $skill_file"
            SKILL_ERRORS=$((SKILL_ERRORS + 1))
        fi
    fi
done
if [ "$SKILL_ERRORS" -eq 0 ]; then
    SKILL_COUNT=$(ls .claude/skills/ 2>/dev/null | wc -l)
    echo "  OK: $SKILL_COUNT skills, all have required frontmatter"
else
    echo "  ERRORS: $SKILL_ERRORS frontmatter issues found"
    ISSUES=$((ISSUES + SKILL_ERRORS))
fi

# 4. Validate settings.json
echo ""
echo "[4] Validating .claude/settings.json..."
if python3 -m json.tool .claude/settings.json > /dev/null 2>&1; then
    echo "  OK: settings.json is valid JSON"
else
    echo "  ERROR: settings.json is invalid JSON"
    ISSUES=$((ISSUES + 1))
fi

# 5. Check MASTER_PLAN progress
echo ""
echo "[5] MASTER_PLAN progress..."
if [ -f "MASTER_PLAN.md" ]; then
    DONE=$(grep -c "^- \[x\]" MASTER_PLAN.md 2>/dev/null || echo 0)
    TOTAL=$(grep -c "^- \[" MASTER_PLAN.md 2>/dev/null || echo 0)
    echo "  Progress: $DONE/$TOTAL steps complete"
fi

# 6. Check tasks/todo.md for overdue items
echo ""
echo "[6] Open tasks..."
if [ -f "tasks/todo.md" ]; then
    OPEN=$(grep -c "^- \[ \]" tasks/todo.md 2>/dev/null || echo 0)
    echo "  Open tasks: $OPEN"
fi

echo ""
echo "================================================"
echo "  SUMMARY: $ISSUES issues found — $DATE"
echo "================================================"

exit 0
