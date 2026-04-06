#!/bin/bash
# Performance audit — Python profiling, import times, token costs
# Cron: 0 1 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/perf-audit.sh >> data/cache/cron-perf.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
OUT="data/outputs/perf-report-${DATE}.md"
mkdir -p data/outputs

echo "================================================"
echo "  PERF AUDIT — $DATE"
echo "================================================"

cat > "$OUT" << HEADER
# Performance Audit — $DATE

## Python Import Times
HEADER

# Check Python import time for src package
echo ""
echo "[1] Python import time..."
IMPORT_TIME=$(python3 -c "
import time
t0 = time.monotonic()
import sys
sys.path.insert(0, '.')
try:
    import src
    ms = int((time.monotonic() - t0) * 1000)
    print(ms)
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null || echo "N/A")
echo "  src import: ${IMPORT_TIME}ms"
echo "- src package import: ${IMPORT_TIME}ms" >> "$OUT"

# Syntax check all Python files
echo ""
echo "[2] Python syntax check..."
SYNTAX_ERRORS=0
while IFS= read -r -d '' pyfile; do
    if ! python3 -m py_compile "$pyfile" 2>/dev/null; then
        echo "  SYNTAX ERROR: $pyfile"
        SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
    fi
done < <(find src/ -name "*.py" -print0 2>/dev/null)
echo "  Syntax errors: $SYNTAX_ERRORS"
echo "" >> "$OUT"
echo "## Syntax Check" >> "$OUT"
echo "- Python syntax errors: $SYNTAX_ERRORS" >> "$OUT"

# Count lines of code
echo ""
echo "[3] Code size..."
SRC_LINES=$(find src/ -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)
SKILL_COUNT=$(ls .claude/skills/ 2>/dev/null | wc -l || echo 0)
echo "  src/ lines: $SRC_LINES"
echo "  skills: $SKILL_COUNT"
echo "" >> "$OUT"
echo "## Code Size" >> "$OUT"
echo "- src/ lines of code: $SRC_LINES" >> "$OUT"
echo "- Skills defined: $SKILL_COUNT" >> "$OUT"

# Data directory sizes
echo ""
echo "[4] Data directory sizes..."
echo "" >> "$OUT"
echo "## Data Sizes" >> "$OUT"
for dir in data/cache data/outputs data/research data/embeddings; do
    if [ -d "$dir" ]; then
        SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "  $dir: $SIZE"
        echo "- $dir: $SIZE" >> "$OUT"
    fi
done

echo ""
echo "Report written: $OUT"
echo "================================================"
