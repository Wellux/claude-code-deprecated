# Command: /research

Run the Karpathy-style autonomous research agent on a topic.

## Steps
1. Invoke research-agent with topic
2. WebSearch for latest papers and implementations
3. Distill to first principles
4. Write to data/research/YYYY-MM-DD-<topic>.md
5. Extract insights → tasks/lessons.md
6. Update data/research/README.md

## Usage
```
/research LLM agent memory systems
/research RAG with graph retrieval
/research prompt engineering 2026
```

## Schedule
Runs automatically every Monday 6am via cron:
`0 6 * * 1 bash tools/scripts/research-agent.sh`
