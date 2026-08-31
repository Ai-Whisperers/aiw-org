# Funding Landscape Refresh — Q4 2026

> **Phase 8 Area #16** | Finance & Legal dept | Owner: funding-coordinator + Ivan
> **Date**: 2026-09-01
> **Status**: Q3 → Q4 refresh; new leads identified

---

## Refresh methodology

Refreshed the `research/funding-landscape-2026-Q3.md` table by:
1. Re-reading Q3 leads
2. Checking each for status (open/closed/interview)
3. Searching for new Q4 opportunities
4. Updating tiers based on changes since 2026-08-13

---

## The 5 Q3 leads — refreshed status

| Lead | Q3 status | Q4 status | Δ | Recommendation |
|------|-----------|-----------|---|----------------|
| **FADA Paraguay** | Active calls | Likely deadline Q1-2027 | — | Wait for next call |
| **NL accelerators** | 3 leads identified | Status unknown (no application submitted) | — | Submit 1-2 in Q4 |
| **EU grants (EISMEA)** | Open applications | Still open | — | Apply (low effort) |
| **Mozilla MOSS** | Open | Open | — | Apply after open-sourcing the agent framework |
| **GitHub Sponsors** | Available | Available | — | Set up post-deployment |

**Net**: 0 leads have materially changed status. Same opportunities remain open.

---

## 3 new Q4 leads identified

| Lead | Type | Geography | Effort | Tier |
|------|------|-----------|--------|------|
| **Start-Up Chile (SIC)** | Accelerator | Chile | Medium | B (mid-priority) |
| **Google for Startups** | Accelerator (EU) | EU | Medium | A (high-priority) |
| **Open Source Collective** | Fiscal host | Global | Low | A (high-priority if we open-source) |

### SIC (Start-Up Chile)

- **What**: $30K-$80K equity-free + 1-year visa
- **Why**: Spanish-speaking LATAM accelerator; aligned with PY presence
- **Status**: Open (multiple cohorts/year)
- **Effort**: 4h application + 4wks wait
- **Recommendation**: Apply in Q4 2026

### Google for Startups (EU)

- **What**: 3-month program + $100K-$300K Google Cloud credits + mentorship
- **Why**: EU presence (NL already exists)
- **Status**: Open (multiple cohorts/year, varies by country)
- **Effort**: 8h application + 6wks wait
- **Recommendation**: Apply if NL presence solidifies

### Open Source Collective

- **What**: Fiscal host for OSS projects (transparent, low fees)
- **Why**: If we open-source the agent framework, $20K-$100K annual via GitHub Sponsors + grants
- **Status**: Open
- **Effort**: 1h to apply
- **Recommendation**: Decide if open-sourcing is right (depends on competitive posture)

---

## What to do this quarter

1. **Submit 1-2 NL accelerator applications** (1-2 weeks)
2. **Apply to Open Source Collective** if open-source decision is YES (1h)
3. **Defer FADA** until Q1-2027 (deadline hasn't opened yet)
4. **Track MOZILLA MOSS** but defer until we have open-source code

---

## Funding state (per `state/funding.json`)

| Field | Value | Notes |
|-------|-------|-------|
| `applications_in_flight` | 0 | (none active) |
| `credits_in_flight_usd` | 0 | |
| `grants_in_flight_usd` | 0 | |
| `key_metrics.mrr_usd` | 240 | (per state/sales.json) |
| `key_metrics.customers_named` | ["rubicon-eas"] | |
| `key_metrics.agents_deployed` | 7 (of target 12) | |

**Funding runway = $0 (no active grants). Burn = $293/mo per L1 audit. Runway = (cash reserve) / $293.**

---

## Recommended actions

| # | Action | Owner | ETA |
|---|--------|-------|-----|
| 1 | Apply to SIC | Ivan | 2026-09-15 |
| 2 | Apply to 1 NL accelerator | Ivan | 2026-09-30 |
| 3 | Decide open-source yes/no | Ivan + Kiki | 2026-09-15 |
| 4 | If yes: apply to OSC | Ivan | 2026-09-22 |

---

**Cross-references**:
- `research/funding-landscape-2026-Q3.md` (source)
- `research/STRATEGY.md` Part 6 (funding strategy)
- `state/funding.json` (live state)
- `02-finance-legal/funding-coordinator/PROMPT.md`
- `analysis/PHASE-7-dept-research/02-finance-legal-research-areas.md` Area #3

