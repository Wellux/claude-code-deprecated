#!/bin/bash
# Security scan — secrets detection, dependency CVEs, permission audit
# Cron: 0 0 * * 0 cd /home/user/wellux_testprojects && bash tools/scripts/security-scan.sh >> data/cache/cron-security.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
OUT="data/outputs/security-report-${DATE}.md"
ISSUES=0
mkdir -p data/outputs

echo "================================================"
echo "  SECURITY SCAN — $DATE"
echo "================================================"

cat > "$OUT" << HEADER
# Security Report — $DATE

## Scan Summary
HEADER

# 1. Detect hardcoded secrets patterns
echo ""
echo "[1] Scanning for secrets patterns..."
SECRET_PATTERNS=(
    "sk-[a-zA-Z0-9]{20,}"           # OpenAI keys
    "sk-ant-[a-zA-Z0-9-]{30,}"      # Anthropic keys
    "AKIA[A-Z0-9]{16}"              # AWS Access Key ID
    "password\s*=\s*['\"][^'\"]{8,}" # Hardcoded passwords
    "api_key\s*=\s*['\"][^'\"]{10,}" # Hardcoded API keys
)

SECRET_FOUND=0
for pattern in "${SECRET_PATTERNS[@]}"; do
    matches=$(grep -rEn "$pattern" src/ examples/ config/ 2>/dev/null \
        --include="*.py" --include="*.yaml" --include="*.json" \
        --exclude-dir=".git" || true)
    if [ -n "$matches" ]; then
        echo "  WARNING: Potential secret found matching: $pattern"
        echo "$matches" | head -3
        SECRET_FOUND=$((SECRET_FOUND + 1))
        ISSUES=$((ISSUES + 1))
    fi
done
[ "$SECRET_FOUND" -eq 0 ] && echo "  OK: No hardcoded secrets detected"
echo "- Hardcoded secrets: $SECRET_FOUND patterns matched" >> "$OUT"

# 2. Check .gitignore covers sensitive files
echo ""
echo "[2] Checking .gitignore coverage..."
GITIGNORE_ISSUES=0
REQUIRED_IGNORES=(".env" "*.local" "settings.local.json" "data/cache/" "data/outputs/")
for item in "${REQUIRED_IGNORES[@]}"; do
    if ! grep -qF "$item" .gitignore 2>/dev/null; then
        echo "  MISSING in .gitignore: $item"
        GITIGNORE_ISSUES=$((GITIGNORE_ISSUES + 1))
        ISSUES=$((ISSUES + 1))
    fi
done
[ "$GITIGNORE_ISSUES" -eq 0 ] && echo "  OK: .gitignore covers all sensitive paths"
echo "- .gitignore gaps: $GITIGNORE_ISSUES" >> "$OUT"

# 3. Check hook scripts are not world-writable
echo ""
echo "[3] Checking hook permissions..."
PERM_ISSUES=0
for hook in .claude/hooks/*.sh; do
    if [ -f "$hook" ]; then
        PERMS=$(stat -c "%a" "$hook" 2>/dev/null || stat -f "%OLp" "$hook" 2>/dev/null || echo "unknown")
        if [ "$PERMS" = "777" ] || [ "$PERMS" = "666" ]; then
            echo "  WARNING: $hook is world-writable ($PERMS)"
            PERM_ISSUES=$((PERM_ISSUES + 1))
            ISSUES=$((ISSUES + 1))
        fi
    fi
done
[ "$PERM_ISSUES" -eq 0 ] && echo "  OK: Hook scripts have safe permissions"
echo "- Permission issues: $PERM_ISSUES" >> "$OUT"

# 4. Python import safety (no eval/exec on user input)
echo ""
echo "[4] Scanning for dangerous Python patterns..."
DANGEROUS_PATTERNS=("eval(" "exec(" "os.system(" "subprocess.call.*shell=True" "pickle.load")
DANGEROUS_FOUND=0
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    matches=$(grep -rn "$pattern" src/ 2>/dev/null --include="*.py" || true)
    if [ -n "$matches" ]; then
        echo "  REVIEW: $pattern"
        echo "$matches" | head -2
        DANGEROUS_FOUND=$((DANGEROUS_FOUND + 1))
    fi
done
[ "$DANGEROUS_FOUND" -eq 0 ] && echo "  OK: No dangerous patterns in src/"
echo "- Dangerous patterns: $DANGEROUS_FOUND" >> "$OUT"

# Summary
echo "" >> "$OUT"
echo "## Result" >> "$OUT"
if [ "$ISSUES" -eq 0 ]; then
    echo "**PASS** — No security issues found." >> "$OUT"
    echo ""
    echo "RESULT: PASS — 0 issues"
else
    echo "**REVIEW** — $ISSUES issues require attention." >> "$OUT"
    echo ""
    echo "RESULT: $ISSUES issues found — review $OUT"
fi

echo "Report: $OUT"
echo "================================================"
