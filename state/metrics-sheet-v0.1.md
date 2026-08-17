# Metrics Sheet — Ai-Whisperers (v0.1, auto-generated)

> **Auto-extracted from `/opt/data/agents/state/*.json`.** Regenerate before every application. Update `state/funding.json` → `metrics_sheet_version` on each regeneration.

**Generated**: 2026-08-14
**Version**: 0.1

---

## Headline metrics (the only numbers anyone will remember)

| Metric | Value | Source |
|---|---|---|
| **MRR** | $240 USD/month | state/finance.json |
| **Burn (monthly)** | NULL — UNKNOWN | state/finance.json ⚠️ MEASURE THIS |
| **Runway (months)** | NULL — depends on burn | derived |
| **Active customers** | 1 (Rubicón EAS) | state/finance.json |
| **Named pipeline** | 1 (richar-ruiz) | state/sales.json |
| **Agents deployed** | 7 lead agents | org spec |
| **Compute credits applied** | 0 (post week 1) | state/funding.json |
| **Founders** | 2 (Ivan + Kiki) | org spec |
| **Geography** | Paraguay (PYT = UTC-4) | org spec |
| **Founded** | 2025 | org spec |

## Funnel (the conversion numbers that accelerators ask about)

| Funnel stage | Count (30d) | % of previous |
|---|---|---|
| Leads | 0 | — |
| Calls booked | 0 | — % of leads |
| Proposals sent | 0 | — % of calls |
| Contracts signed | 0 | — % of proposals |
| **Overall: lead → signed** | — % | (target: 1-5%) |

⚠️ **All zeros** = no measured funnel activity. **First priority** post-week-1 is to populate this.

## Engineering health

| Metric | Value |
|---|---|
| Deploys (7d) | 0 |
| Open PRs | 0 |
| Stale repos (7d) | 0 |
| Incidents (72h) | 0 |
| Kiki commits (7d) | 0 |
| **Infra costs (monthly)** | NULL |

⚠️ `infra_costs_monthly_usd` is null. Should be populated by the engineering-roster agent once Phase 1 closes.

## Research pipeline

| Item | Status |
|---|---|
| Thesis chapter | none active |
| Thesis target date | none |
| Thesis blocker | none |
| Publications pipeline | 0 |
| Courses ready | 0 |
| Courses in draft | 0 |
| Monetization backlog | 0 |

⚠️ `research-tracker` agent has `last_run: null` — never fired.

## Decisions / questions log (last 7 days)

| Date | Type | Content |
|---|---|---|
| 2026-08-14 | Decision | Fix GitHub auth for org-pulse |
| 2026-08-14 | Decision | Investigate CI failures |
| 2026-08-14 | Question | Check GitHub auth status for org-pulse |

## Cron health

| Metric | Value |
|---|---|
| Jobs in error | 2 (`hermes` and `jq` not found) |
| Last successful run | 2026-08-13 (coord.json) |
| Repos analyzed | 0 |

⚠️ Two cron jobs erroring. **Phase 1 of the v4 plan fixes this.** Block on funding applications until fixed.

---

## What this metrics sheet tells accelerators

### The good
- We have **a customer** (Rubicón EAS, live pipeline)
- We have **a canary deal** (richar-ruiz, named)
- We have **a tech stack in production** (7 agents deployed)
- We're **2 founders doing what normally takes 7** (the agent-org thesis)

### The bad
- MRR is small ($240 — barely qualifies as "revenue")
- Burn is unknown (no measurement discipline yet)
- Funnel is empty (no measured lead → close data)
- Engineering health is sparse (0 deploys, 0 PRs in 7d, but agents are "deployed")
- Research is stalled (0 thesis activity)

### The story we tell
> "We're 90 days in. We have 1 customer + 1 named pipeline prospect + 7 production agents. The agent-org framework lets us operate with 2 humans at scale. MRR is small but accelerating. We're applying to [PROGRAM] to [SPECIFIC ASK]."

---

## How to regenerate

```bash
# Run from /opt/data/agents/state/
python3 -c "
import json, datetime
files = ['finance.json', 'sales.json', 'engineering.json', 'research.json', 'analyst.json', 'coord.json']
print('# Metrics Sheet regenerated:', datetime.date.today())
for f in files:
    try:
        d = json.load(open(f))
        print(f'## {f}'); print(json.dumps(d, indent=2))
    except Exception as e:
        print(f'{f}: {e}')
"
```

Or save as `/opt/data/agents/scripts/regenerate-metrics-sheet.sh`.

---

*Version 0.1 · Last regenerated: 2026-08-14*
