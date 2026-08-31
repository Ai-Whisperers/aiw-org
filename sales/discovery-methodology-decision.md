# Discovery Methodology Decision — SPIN vs BANT vs GPCTBA vs Gap Selling

> **Phase 8 Area #21** | Sales & Growth dept | Owner: sales-pipeline + Ivan
> **Date**: 2026-09-01
> **Status**: Recommendation — ADOPT Gap Selling for AI services

---

## The candidates

4 discovery methodologies, surveyed from sales literature:

| Method | Origin | Core question | Best for |
|--------|--------|----------------|----------|
| **SPIN Selling** | Rackham (1988) | Situation → Problem → Implication → Need-payoff | Complex B2B sales |
| **BANT** | IBM (1950s) | Budget → Authority → Need → Timeline | Quick qualification |
| **GPCTBA/C&I** | HubSpot (2010s) | Goals → Plans → Challenges → Timeline → Budget → Authority + Consequences + Implications | SaaS sales |
| **Gap Selling** | Keenan (2020) | Current state → Future state → Gap (the "why change") | Consultative, problem-focused |

---

## Comparison for our context (Rubicón EAS AI services)

| Dimension | SPIN | BANT | GPCTBA | Gap Selling |
|-----------|------|------|--------|-------------|
| Discovery depth | High | Low | High | High |
| Qualification speed | Slow | Fast | Medium | Slow |
| Fit with technical sales | Good | Poor | Good | Excellent |
| Fit with founder-led sales | Good | OK | Good | Excellent |
| Buyer relationship | Consultative | Transactional | Consultative | Co-diagnostic |
| Cognitive load on Ivan | High | Low | Medium | Medium |

---

## My recommendation: **Gap Selling** for Rubicón EAS, **SPIN** for coaching

### Why Gap Selling for AI services (Rubicón EAS)

1. **AI services are sold on transformation, not features.** Gap Selling's "current → future → gap" framework makes the transformation concrete.
2. **Founder-led sales needs a diagnostic posture.** Gap Selling treats seller as doctor diagnosing the gap, not vendor pitching features.
3. **Aligns with our pitch pattern.** Looking at `marketing-strategy/agent-tasks/`, our outreach already follows a gap pattern (we ask "what's broken?").
4. **Works for short cycles.** BANT is fast but loses deals; SPIN is deep but slow. Gap is the middle ground.

### Why SPIN for coaching

1. **Coaching is already a SPIN-fit domain** (per `research/coaching-funnel-playbook.md`).
2. **Coaching buyers (individuals) expect guidance**, not diagnostic.
3. **Coach agents already trained on SPIN**.

---

## Implementation

### Scripts (Gap Selling for AI services)

**Opening**: "I see you're running [business type]. Most [verticals] we work with have [common gap]. Is that true for you?"

**Diagnostic**:
- "How are you currently handling [problem]?"
- "What's the impact on [metric: time/money/team]?"
- "What does solving this look like for you?"

**Closing**: "If we could close that gap in [timeframe], would [outcome] be worth [$X]?"

### Training

- Read Gap Selling (Keenan, 2020), chapters 1-5
- Practice 5 mock discovery calls with Kiki as roleplay
- Document in `sales/discovery-scripts.md`

### Tracking

For each discovery call, log to `state/discovery-calls.json`:
```json
{
  "date": "2026-09-XX",
  "prospect": "...",
  "method": "gap",
  "current_state": "...",
  "future_state": "...",
  "gap_identified": "...",
  "next_step": "..."
}
```

---

## Next

When Worker is fixed (Phase 8 #19 decision) and we have inbound leads, run 5 discovery calls using Gap Selling. Compare outcome to historical conversion. Iterate.

---

**Cross-references**:
- `research/coaching-funnel-playbook.md` (existing SPIN/MED)
- `marketing-strategy/` (existing pitch patterns)
- `research/1000-company-questions.md` Category 8
- `analysis/PHASE-7-dept-research/03-sales-growth-research-areas.md` Area #5

