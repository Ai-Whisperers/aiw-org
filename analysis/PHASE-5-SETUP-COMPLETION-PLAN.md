# Phase 5 — Setup-Completion Plan + Feedback Loops

> **Goal**: Bring every Tier-1 dept to the same 5/5 setup parity as Engineering/Operations. Establish feedback loops to improve as we go.
>
> **Date**: 2026-09-01
> **Author**: Hermes (AI), per Ivan's "you decide"

---

## The "Most Setiped Dept" Pattern (Engineering is the gold standard)

A dept is at **5/5** when it has:

1. ✅ `dept-lead/PROMPT.md` (with full frontmatter: name/version/owner/layer/topology/archetype/time_scale/composition)
2. ✅ `dept-lead/PROMPT-monitor.md` (4 sections: Purpose, Metrics Watched, Threshold Rules, Alert Routing)
3. ✅ `dept-lead/monitor-notes/` directory (parallel notes for MEDIUM alerts per `dept-monitors/INDEX.md`)
4. ✅ `demiurge/kpi/{dept}-stack.yaml` (5-15 KPIs with feedback_loop taxonomy)
5. ✅ `demiurge/signals/{dept}.yaml` (consumes/emits routing graph)

## Current Scorecard

| Dept | Lead | 1.Lead | 2.Monitor | 3.Notes | 4.KPIs | 5.Signals | Score |
|------|------|--------|-----------|---------|--------|-----------|-------|
| 01-operations | management-coordinator | ✓ | ✓ | ✓ | ✓ | ✓ | **5/5** |
| 02-finance-legal | finance-controller | ✓ | ✗ | ✗ | ✓ | ✓ | **3/5** |
| 03-sales-growth | sales-pipeline | ✓ | ✗ | ✗ | ✗ | ✗ | **1/5** |
| 04-engineering | engineering-roster | ✓ | ✓ | ✓ | ✓ | ✓ | **5/5** |
| 05-research-education | research-tracker | ✓ | ✗ | ✗ | ✓ | ✓ | **3/5** |
| 06-people-culture | people-hr | ✓ | ✗ | ✗ | ✓ | ✓ | **3/5** |
| board-of-directors | board-of-directors | ✗ | ✗ | ✗ | ✗ | ✗ | **0/5** |

Total: **20/35 = 57% parity**

---

## Plan — 5 Rounds, Sequenced by ROI + Feedback Loops

### Round 1 (now): Quick wins — KPI/signals + board PROMPT (4 files)

**Why first**: Highest leverage, lowest effort. Fixes the 0/5 dept + the 1/5 dept.

1. Create `demiurge/kpi/sales-stack.yaml` (mirror engineering/research pattern, 7 KPIs)
2. Create `demiurge/signals/sales-growth.yaml` (real signals, not boilerplate)
3. Create `demiurge/kpi/board-stack.yaml` (governance KPIs, 5 KPIs)
4. Create `demiurge/signals/board-of-directors.yaml` (governance routing)
5. Create `board-of-directors/PROMT.md` (the dept-lead itself, was missing!)
6. Create `board-of-directors/PROMPT-monitor.md`

**Feedback loop**: After Round 1, write `PHASE-5-ROUND-1-FEEDBACK.md` capturing:
- What worked (template mirroring is fast)
- What didn't (board PROMPT needed Ivan/Kiki leadership model decisions)
- Time spent (target: <30min)
- Delta: 20/35 → 30/35 (86% parity)

### Round 2 (then): Dept-lead PROMPT-monitor.md for 3 lagging depts (3 files)

**Why second**: The dept-lead monitors are the **most important** (Ivan looks at these first when something breaks). The 3 lagging ones (finance, sales, research, people) need them.

For each of finance/sales/research/people: write `PROMPT-monitor.md` modeled after engineering-roster/PROMPT-monitor.md, adapted to that dept's state file + KPIs.

**Feedback loop**: `PHASE-5-ROUND-2-FEEDBACK.md` captures:
- Whether template-with-substitution is fast enough OR if each dept needs unique metrics
- Whether 4 sections (Purpose/Metrics/Threshold/Routing) are sufficient OR if we need a 5th
- Time spent
- Delta: 30/35 → 38/35 → 4/7 depts at 5/5

### Round 3 (then): monitor-notes/ dirs for 3 lagging depts (3 dirs)

**Why third**: Without monitor-notes, the MEDIUM-severity alerts have nowhere to go (the state schema is `additionalProperties: false`).

For each of finance/sales/research/people: create `monitor-notes/` dir + `.gitkeep`.

**Feedback loop**: `PHASE-5-ROUND-3-FEEDBACK.md`
- Whether monitor-notes dir is enough OR if we need a starter sample file
- Time spent

### Round 4 (then): Cleanup — remove cadence-variant empty dirs (5 dirs)

**Why fourth**: We have 5 empty cadence-variant dirs (ai-ops-coordinator-daily, accounting-automation-daily, lead-enrichment-daily, proposal-drafter-on-demand, revops-pipeline-analyzer-daily) that confuse the inventory.

For each: `git rm -r` the empty dir.

**Feedback loop**: `PHASE-5-ROUND-4-FEEDBACK.md`
- Whether the cron schedule on the parent covers the missing cadence
- Time spent

### Round 5 (then): Build 4 missing engineering PROMPTs

**Why last (and only engineering)**: The 4 missing PROMPTs (drift-detector, security-auditor, delivery-tracker, qa-automation-on-pr) are catalog-listed but empty. They're real-but-deferred per the audit.

For each: write a real PROMPT.md based on the catalog's role description.

**Feedback loop**: `PHASE-5-ROUND-5-FEEDBACK.md`
- Whether the catalog role description is sufficient OR if we need Kiki's input on architecture decisions
- Time spent

---

## Final Target

**All 6 Tier-1 dept dirs + board-of-directors at 5/5** (35/35 = 100% parity).
Plus: 4 newly-built engineering PROMPTs.
Plus: 5 cadence-variant dirs cleaned up.
Plus: 6 feedback-loop notes capturing what worked.

**Estimated total**: 3-4 hours of focused work.

---

## Feedback Loop Discipline (for the AI)

Each round ends with:
1. **What worked** (what pattern/template was right)
2. **What didn't** (where I got stuck or made a mistake)
3. **Pattern update** (should we extract this into a reusable helper?)
4. **Time spent** (am I getting faster per round?)
5. **Delta** (numeric improvement from before/after)

The point: at end of Phase 5, the AI should be **noticeably better** at setup-completeness work than at the start. That's the learning loop.

---

## Out-of-Scope (deferred correctly)

- **Tier-3 depts** (Customer Success, IR, Chief of Staff, etc.): All have explicit triggers in `DEFERRED-ROLES.md`. Building them now violates the doctrine.
- **Tier-4 enterprise** (CDO, CAIO, M&A): Same — deferred until $1M+ revenue.
- **137 full roles**: 68 of those are Tier-3+ (T4). Cannot build all those now.
- **Cross-repo agents** (coach-agents): Live in `coach-agents` repo, not aiw-org.

This Phase 5 = **Tier-1 + governance = 6 depts + board** to **5/5 parity**.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Sub-agent PROMPT-monitor.md templates feel boilerplate | Round 3 feedback loop — extract helper script if needed |
| Board-of-directors PROMPT needs Ivan+Kiki leadership model | Ask 1 quick question, don't guess |
| Cadence-variant removal breaks a cron somewhere | `grep cron first`; if a cron references the removed dir, fix before removing |
| 4 engineering builds are real work (4h each) | Cap Round 5 at 1 hour; document remaining; suggest Kiki-side architecture review |

---

## Success criteria

By end of Phase 5:
- All 7 dept dirs scorecard = 5/5
- 6 round-feedback docs in `analysis/`
- 4 newly-built PROMPT.md files in `04-engineering/`
- Working tree clean
- 1 completion summary doc

**Plan ready. Starting Round 1.**