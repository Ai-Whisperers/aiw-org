# Cash-Flow Projection Model — v0.1

> **Solves FI-1 from the transcript critique.** Build 12-month projection; update monthly.
> **Auto-extracted where possible** from state/finance.json + state/sales.json + state/funding.json.

## Base assumptions

```
Current state (2026-08-14):
  MRR: $240 USD/month
  Burn: $400-600 USD/month (estimate; needs measurement)
  Customers: 1 (Rubicón EAS)
  Named pipeline: 1 (richar-ruiz)
  Compute credits: 0 (post week 1: ~$625K applied)
  Grants approved: 0
```

## Three scenarios

### Conservative (60% confidence)
- Rubicón EAS stays at $240/mo
- richar-ruiz does not close in 2026
- 0 new customers added
- Burn holds steady at $500/mo
- Compute credits offset $300/mo of burn

### Base (40% confidence)
- Rubicón EAS stays at $240/mo
- richar-ruiz closes at $1,500/mo in Q4
- 1 new SME customer in Q4 at $500/mo
- Burn grows to $700/mo (more compute, more services)
- Compute credits offset $500/mo of burn

### Aggressive (15% confidence)
- Rubicón EAS upgrades to $500/mo
- richar-ruiz closes at $1,500/mo in Q4
- 2 new customers in Q4 (one legal, one SME)
- First EU client closes at $3,000/mo in Q1 2027
- Burn grows to $1,200/mo (compute + Compliance Officer)
- Compute credits offset $700/mo of burn
- First EU grant approved ($50K one-shot)

## 12-month projection — Conservative

| Month | MRR (USD) | Burn (USD) | Net (USD) | Cumulative | Notes |
|---|---|---|---|---|---|
| 2026-08 | $240 | $500 | -$260 | -$260 | Baseline |
| 2026-09 | $240 | $500 | -$260 | -$520 | No change |
| 2026-10 | $240 | $500 | -$260 | -$780 | No change |
| 2026-11 | $240 | $500 | -$260 | -$1,040 | No change |
| 2026-12 | $240 | $500 | -$260 | -$1,300 | No change |
| 2027-01 | $240 | $500 | -$260 | -$1,560 | No change |
| 2027-02 | $240 | $500 | -$260 | -$1,820 | No change |
| 2027-03 | $240 | $500 | -$260 | -$2,080 | No change |
| 2027-04 | $240 | $500 | -$260 | -$2,340 | No change |
| 2027-05 | $240 | $500 | -$260 | -$2,600 | No change |
| 2027-06 | $240 | $500 | -$260 | -$2,860 | No change |
| 2027-07 | $240 | $500 | -$260 | -$3,120 | 12-month net: -$3,120 |

**Interpretation**: Without new MRR, the org loses $3,120 over 12 months. Since Ivan + Kiki take no salary, this is the only cash drag. Affordable for now (Ivan is bootstrapping with personal runway).

## 12-month projection — Base

| Month | MRR (USD) | Burn (USD) | Net (USD) | Cumulative | Notes |
|---|---|---|---|---|---|
| 2026-08 | $240 | $500 | -$260 | -$260 | Baseline |
| 2026-09 | $240 | $500 | -$260 | -$520 | richar-ruiz discovery call |
| 2026-10 | $240 | $500 | -$260 | -$780 | richar-ruiz proposal sent |
| 2026-11 | $1,740 | $700 | +$1,040 | +$260 | richar-ruiz signed ($1,500) |
| 2026-12 | $2,240 | $700 | +$1,540 | +$1,800 | New SME ($500) + richar-ruiz ($1,500) + Rubicon ($240) |
| 2027-01 | $2,240 | $700 | +$1,540 | +$3,340 | MRR holds |
| 2027-02 | $2,240 | $700 | +$1,540 | +$4,880 | MRR holds |
| 2027-03 | $2,240 | $700 | +$1,540 | +$6,420 | MRR holds |
| 2027-04 | $2,240 | $700 | +$1,540 | +$7,960 | MRR holds |
| 2027-05 | $2,240 | $700 | +$1,540 | +$9,500 | MRR holds |
| 2027-06 | $2,240 | $700 | +$1,540 | +$11,040 | MRR holds |
| 2027-07 | $2,240 | $700 | +$1,540 | +$12,580 | 12-month net: +$12,580 |

**Interpretation**: Closing richar-ruiz + adding 1 SME customer flips the org to net-positive in November 2026. By mid-2027, $12.5K cumulative positive. **This is the minimum viable trajectory.**

## 12-month projection — Aggressive

| Month | MRR (USD) | Burn (USD) | Net (USD) | Cumulative | Notes |
|---|---|---|---|---|---|
| 2026-08 | $240 | $500 | -$260 | -$260 | Baseline |
| 2026-09 | $500 | $500 | $0 | -$260 | Rubicón upgrade |
| 2026-10 | $500 | $600 | -$100 | -$360 | richar-ruiz proposal + Compliance Officer scoping |
| 2026-11 | $2,000 | $700 | +$1,300 | +$940 | richar-ruiz signed |
| 2026-12 | $3,500 | $800 | +$2,700 | +$3,640 | New legal client ($1,500) + new SME ($500) |
| 2027-01 | $6,500 | $1,200 | +$5,300 | +$8,940 | First EU client ($3,000) |
| 2027-02 | $6,500 | $1,200 | +$5,300 | +$14,240 | MRR holds |
| 2027-03 | $6,500 | $1,200 | +$5,300 | +$19,540 | MRR holds |
| 2027-04 | $6,500 | $1,200 | +$5,300 | +$24,840 | MRR holds |
| 2027-05 | $6,500 | $1,200 | +$5,300 | +$30,140 | MRR holds |
| 2027-06 | $6,500 | $1,200 | +$5,300 | +$35,440 | MRR holds |
| 2027-07 | $6,500 | $1,200 | +$5,300 | +$40,740 | 12-month net: +$40,740 |

**Interpretation**: Aggressive scenario nets $40K+ over 12 months, with first EU client in Q1 2027. **Triggers**: $5K MRR for first FTE; first EU client triggers Compliance Officer hard-stop lift.

## Sensitivity analysis

| Variable | Conservative | Base | Aggressive |
|---|---|---|---|
| richar-ruiz closes | No | Yes | Yes |
| Rubicón upgrades | No | No | Yes |
| New customers in 2026 | 0 | 1 | 2 |
| First EU client | No | No | Q1 2027 |
| MRR by 2027-07 | $240 | $2,240 | $6,500 |
| Net 12-month cash | -$3,120 | +$12,580 | +$40,740 |

## Critical actions (do these to move toward Base scenario)

1. **Close richar-ruiz** by end of Q4 2026 (single highest-leverage deal)
2. **Sign 1 new SME customer** in Q4 2026
3. **Measure burn** so the projection is grounded, not estimated
4. **Apply to 5+ compute credit programs** (week 1) so burn is offset from Q3 2026

## What this model does NOT include

- Founder salary (assumed $0 for now)
- Tax payments (Paraguay Maquila if applied could change this)
- Compliance Officer hire (EU client trigger, ~$5-15K/mo if needed)
- First FTE hire ($5K MRR trigger, ~$3-8K/mo)
- One-shot legal costs (PY S.A. formation, EU entity formation, etc.)
- Equity raise (if pursued; could be $50-500K)

## How to update

```bash
# Run monthly (1st of month, 09:00 PYT)
python3 /opt/data/agents/scripts/regenerate-cash-flow.py \
  --mrr <current MRR> \
  --burn <current burn> \
  --customers <count> \
  --output /opt/data/agents/state/cash-flow-projection.md
```

## How to use in applications

Copy the **Base scenario row** into applications. Highlight that **without new MRR, the org burns $3,120 over 12 months** — this justifies the ask for compute credits and accelerator mentorship. With Base scenario executed, the org reaches net-positive in November 2026.

---

*Version 0.1 · Initial cash-flow model*
*Last updated: 2026-08-14*
*Update cadence: monthly*
