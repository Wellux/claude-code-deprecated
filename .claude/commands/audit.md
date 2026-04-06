# Command: /audit

Run a full project audit: security, performance, documentation, dependencies.

## Steps
1. /ciso — full security audit
2. /perf-profiler — performance analysis
3. /dep-auditor — dependency CVEs
4. /readme-writer — check docs freshness
5. /web-vitals — if frontend present

## Output
Consolidated audit report in `data/outputs/audit-YYYY-MM-DD.md`

## Usage
```
/audit full
/audit security-only
/audit perf-only
```
