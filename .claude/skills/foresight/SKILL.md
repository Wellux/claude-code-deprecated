---
name: foresight
description: >
  Cross-domain strategic analysis that surfaces non-obvious risks and opportunities.
  Invoke for: "foresight", "strategic analysis", "what am I missing strategically",
  "second order effects", "future risks", "what could blindside us", "horizon scanning",
  "strategic blind spots", "cross-domain analysis", "what should we watch out for",
  "long term risks". One contextual nudge per execution.
argument-hint: project, decision, or domain to analyze
allowed-tools: Read, WebSearch, Write
---

# Skill: Foresight — Cross-Domain Strategic Analysis

## Role
Surface one high-value strategic insight per execution by scanning across domains
(technology, market, regulatory, organizational) for non-obvious risks and opportunities.
Inspired by marciopuga/cog `/foresight` pattern.

## Philosophy
Most strategic blind spots come from staying within your own domain.
The most valuable foresight crosses from adjacent domains:
- A technical trend that becomes a business risk
- A market shift that makes a current architecture obsolete
- A regulatory change already visible in other industries
- A cultural pattern that predicts adoption or rejection

## Workflow

1. **Domain scan**: identify 4 domains relevant to the topic
   - Technology (current + 12-month horizon)
   - Market/competitive (user behavior, competitor moves)
   - Organizational (team dynamics, technical debt accumulation)
   - External (regulatory, ecosystem shifts)

2. **Cross-domain pattern match**: find where signals from different domains converge
   - Convergence = higher confidence signal
   - Divergence = uncertainty zone, needs monitoring

3. **Non-obvious risk identification**: focus on:
   - Second-order effects of current decisions
   - "This seemed fine until X changed" scenarios
   - Dependencies that aren't visible day-to-day

4. **Opportunity surface**: one opportunity that the risk analysis reveals

5. **Contextual nudge**: one specific, actionable recommendation

## Output Format

```
## Foresight: <topic>

### Domain Signals (brief)
- **Technology**: [signal]
- **Market**: [signal]
- **Organizational**: [signal]
- **External**: [signal]

### Cross-Domain Pattern
[Where signals converge or diverge and what that implies]

### Non-Obvious Risk
**Risk**: [specific risk, not obvious from any single domain]
**Timeline**: [when this might materialize]
**Early warning sign**: [what to watch for]

### Opportunity
[One opportunity the analysis reveals]

### Contextual Nudge
> **One thing to do this week**: [specific action]
```

## Examples of high-value foresight patterns
- "Your async architecture is sound today, but the upcoming Python GIL changes in 3.14 will allow true threading — your patterns will need revisiting"
- "The trend toward edge AI (market) + your current cloud-only architecture (tech) = a competitive gap opening in 9 months"
- "Your test coverage is increasing (org) but CI time is also increasing (tech) — this will soon create a push-back-on-tests dynamic in your team"
