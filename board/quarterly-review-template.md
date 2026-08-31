# Quarterly Board Review — Template + Agenda

> **Phase 8 Area #29** | Board of Directors | Owner: board-of-directors agent + Ivan
> **Date**: 2026-09-01
> **Status**: Template ready for first Q4-2026 review (2026-10-01)

---

## Schedule

Per `board-of-directors/PROMPT.md`: Quarterly, 1st of month, 14:00 UTC, 90 minutes.

| Quarter | Date | Time (UTC) |
|---------|------|-------------|
| Q3-2026 | 2026-10-01 | 14:00 |
| Q4-2026 | 2027-01-01 | 14:00 |
| Q1-2027 | 2027-04-01 | 14:00 |

---

## Agenda (90 min)

| Time | Section | Owner | Output |
|------|---------|-------|--------|
| 0:00-0:05 | Context (last quarter's summary) | Ivan | recap doc |
| 0:05-0:25 | KPI review per dept (6 depts × 3min) | Ivan + Kiki | per-dept KPI table |
| 0:25-0:45 | Risk register review | ai-safety-engineer | updated risk register |
| 0:45-1:00 | Decisions (queue of pending HIGH/CRITICAL) | Ivan | decision log entries |
| 1:00-1:15 | Open discussion | both | action items |
| 1:15-1:30 | Action items + assignments | both | commitments |

---

## Decision log template

For each decision made, add to `state/decisions/YYYY-QN-{topic}.md`:

```markdown
# Decision: {topic} ({date})

**Status**: APPROVED / DEFERRED / REJECTED
**Vote**: Ivan: ?, Kiki: ?
**Tiebreaker used**: yes/no (who: Ivan/Kiki)

## Context
{1-paragraph summary}

## Options considered
1. {Option A} — pros / cons
2. {Option B} — pros / cons

## Decision
{What was decided}

## Rationale
{Why}

## Action items
- [ ] {action} ({owner}, {due date})
```

---

## KPI table template (for the 0:05-0:25 section)

| Dept | Target | Actual | Δ | Status |
|------|--------|--------|---|--------|
| Operations | Self-running 7/7 | TBD | — | — |
| Finance | $1K MRR | $240 MRR | — | 🟡 |
| Sales | 5+ open deals | 0 | — | 🔴 |
| Engineering | 100% lint/smoke | 100% | — | ✅ |
| Research | 1 paper published | 0 | — | 🟡 |
| People | All depts have 2+ people | 2/7 | — | 🟡 |
| Board | Quarterly review held | TBD | — | ⏳ |

---

## Pre-meeting checklist (T-7 days)

- [ ] Ivan drafts context summary
- [ ] Kiki drafts engineering KPI table
- [ ] ai-safety-engineer refreshes risk register
- [ ] board-of-directors agent compiles agenda + per-dept reports
- [ ] Distribute to Ivan + Kiki 48h before

---

## Pilot

First review: **2026-10-01** (Q3-2026 retrospective + Q4-2026 planning).
After pilot, refine based on what worked.

---

**Cross-references**:
- `board-of-directors/PROMPT.md`
- `demiurge/kpi/board-stack.yaml`
- `analysis/PHASE-7-dept-research/board-of-directors-research-areas.md` Area #2
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #2 (for risk register)

