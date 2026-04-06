#!/bin/bash
# Karpathy-style research loop — runs weekly (Monday 6am via cron)
# Usage: bash tools/scripts/research-agent.sh [topic]
# Cron: 0 6 * * 1 cd /home/user/wellux_testprojects && bash tools/scripts/research-agent.sh >> data/cache/cron-research.log 2>&1

set -euo pipefail

DATE=$(date +%Y-%m-%d)
LOG="data/research/README.md"
LESSONS="tasks/lessons.md"

# Topics to research each run (rotate through all 8 weekly)
TOPICS=(
    "LLM agent frameworks 2026"
    "RAG graph retrieval systems"
    "prompt engineering advances"
    "AI safety alignment techniques"
    "fine-tuning efficiency LoRA QLoRA"
    "multimodal vision language models"
    "code generation AI models"
    "Claude Code automation patterns"
)

echo "================================================"
echo "  RESEARCH AGENT — Karpathy Loop"
echo "  Date: $DATE"
echo "================================================"

mkdir -p data/research

# Init README index if missing
if [ ! -f "$LOG" ]; then
    echo "# Research Index" > "$LOG"
    echo "" >> "$LOG"
fi

echo "" >> "$LOG"
echo "## Research Run: $DATE" >> "$LOG"

for TOPIC in "${TOPICS[@]}"; do
    SLUG=$(echo "$TOPIC" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
    OUT="data/research/${DATE}-${SLUG}.md"

    echo "Researching: $TOPIC"

    # Write research stub (claude --print would replace this in live use)
    cat > "$OUT" << STUB
# Research: $TOPIC
**Date:** $DATE
**Method:** Karpathy (Search → Distill → Implement → Store)

## Core Concept
[Auto-populated by research-agent on next Claude Code session]

## Key Technique
[Run: /karpathy-researcher $TOPIC]

## Implementation Pattern
\`\`\`python
# Minimal example to be populated
\`\`\`

## Actionable Insight
[Extracted and appended to tasks/lessons.md]

## Sources
[URLs from WebSearch]
STUB

    echo "- [$TOPIC]($OUT) — $DATE" >> "$LOG"
    echo "  Written: $OUT"
done

echo ""
echo "Research index updated: $LOG"
echo "Run /karpathy-researcher <topic> in Claude Code to populate stubs."
echo "================================================"
