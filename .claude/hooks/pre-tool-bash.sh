#!/bin/bash
# .claude/hooks/pre-tool-bash.sh
# Runs BEFORE every Bash tool call
# Exit 0 = allow | Exit 2 = BLOCK the command

BASE="/home/user/wellux_testprojects"
LOG="$BASE/data/cache/bash-log.txt"
mkdir -p "$BASE/data/cache"

# Read the command from environment (Claude sets CLAUDE_TOOL_INPUT)
CMD="${CLAUDE_TOOL_INPUT:-unknown}"

# Log all commands with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') CMD: $CMD" >> "$LOG"

# BLOCK list — dangerous patterns
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "sudo rm"
  "sudo dd"
  "curl.*|.*bash"
  "wget.*|.*bash"
  "chmod 777 /"
  "> /dev/sda"
  "mkfs\."
  "dd if=.*of=/dev"
)

for PATTERN in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$CMD" | grep -qE "$PATTERN"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') BLOCKED: $CMD" >> "$LOG"
    echo "⛔ BLOCKED: Dangerous command pattern detected: $PATTERN" >&2
    exit 2
  fi
done

# Allow
exit 0
