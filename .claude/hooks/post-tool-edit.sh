#!/bin/bash
# .claude/hooks/post-tool-edit.sh
# Runs AFTER every Edit or Write tool call
# Always exit 0

BASE="/home/user/wellux_testprojects"
LOG="$BASE/data/cache/edit-log.txt"
mkdir -p "$BASE/data/cache"

# Try to get the file that was edited
FILE="${CLAUDE_TOOL_RESULT_path:-${CLAUDE_TOOL_RESULT_file_path:-}}"

# Log the edit
echo "$(date '+%Y-%m-%d %H:%M:%S') EDITED: ${FILE:-unknown}" >> "$LOG"

# Validate Python syntax if a .py file was written
if [[ "$FILE" == *.py ]] && [ -f "$FILE" ]; then
  if python3 -m py_compile "$FILE" 2>/dev/null; then
    echo "  ✓ Python syntax OK: $FILE"
  else
    echo "  ⚠ Python syntax error in: $FILE" >&2
  fi
fi

# Validate JSON syntax if a .json file was written
if [[ "$FILE" == *.json ]] && [ -f "$FILE" ]; then
  if python3 -m json.tool "$FILE" > /dev/null 2>&1; then
    echo "  ✓ JSON valid: $FILE"
  else
    echo "  ⚠ JSON invalid: $FILE" >&2
  fi
fi

# Validate SKILL.md has required frontmatter
if [[ "$FILE" == *"SKILL.md" ]] && [ -f "$FILE" ]; then
  if ! grep -q "^name:" "$FILE" 2>/dev/null; then
    echo "  ⚠ SKILL.md missing 'name:' frontmatter: $FILE" >&2
  fi
  if ! grep -q "^description:" "$FILE" 2>/dev/null; then
    echo "  ⚠ SKILL.md missing 'description:' frontmatter: $FILE" >&2
  fi
fi

exit 0
