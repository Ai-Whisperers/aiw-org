# Department 3 — Sales & Growth

**Head**: Ivan
**Lead agent**: `sales-pipeline` (Daily 12:00 PYT)
**Version**: 0.2.0
**Last updated**: 2026-08-14

---

## Mission

Generate qualified leads, run outreach, close deals. Sales is the only department that directly produces revenue.

## What this department owns

- **Lead capture** — site forms (Rubicon EAS Worker), LinkedIn inbound, referral partner pings
- **Lead qualification** — ICP match (3 ICPs defined in `marketing-strategy/playbook.md`)
- **Outreach drafts** — LinkedIn DMs, cold emails (HITL only)
- **Proposal generation** — using `paraguai-proposal-pricing` skill + canonical rate card
- **Pipeline visibility** — every lead in flight, where it is, who's blocking
- **Conversion tracking** — lead → call → proposal → contract funnel metrics
- **NEW v0.2.0**: Marketing (sub-function, Tier 1) — content production, multimedia
- **NEW v0.2.0**: Customer Success (Tier 3, deferred until 5+ clients)

## What this department does NOT own

- Final contract wording (Finance & Legal)
- Proposal pricing benchmarks (Finance & Legal)
- Site copy (Engineering)
- Thesis content (Research)

## Decision rights (v0.2.0)

| Action | Authority |
|--------|-----------|
| Send cold outreach draft | Sales agent (Ivan approves within 24h) |
| Reply to inbound lead | Sales agent (logged) |
| Book discovery call | Sales agent (logs to calendar) |
| Send proposal under $1K | Ivan pre-approves scope, Sales agent sends |
| Send proposal $1K-5K | Ivan reads proposal before send |
| Send proposal > $5K | Ivan + Kiki together |
| Discount > 15% off list | Ivan only |
| New outreach channel | Ivan + Kiki |
| **NEW**: Send outbound (when enabled) | require Ivan |
| **NEW**: Marketing campaign launch | require Ivan (trademark scrub first) |

## ICPs (per `marketing-strategy/playbook.md`)

| ICP | Budget (USD) | Pain | Conversion path |
|-----|--------------|------|-----------------|
| Solo entrepreneur | $500-5K | Time poverty, no hire budget | Free resource → 15-min call → Quick-Win package ($1.5K) |
| SME ops manager | $10K-100K | Process inefficiency, ROI pressure | Complimentary audit → 30-min strategy → Pilot ($10-25K) |
| Corporate innovation lead | $100K-500K+ | Legacy systems, board pressure | Confidential briefing → exec workshop → Enterprise engagement |

**Validation trigger**: 30 days of lead data
**Refresh cadence**: annually

## Sub-roles (v0.2.0 — 18 roles from ROLES-INVENTORY.md)

| # | Role | Tier |
|---|------|------|
| 3.1 | Head of Sales / CRO | 🟢 T1 |
| 3.2 | SDR | 🟢 T1 |
| 3.3 | BDR | 🟡 T2 |
| 3.4 | Account Executive | 🟢 T1 |
| 3.5 | Sales Engineer | 🟡 T2 |
| 3.6 | Customer Success Manager | 🟡 T2 |
| 3.7 | Proposal Writer | 🟢 T1 |
| 3.8 | Marketing Manager | 🟢 T1 |
| 3.9 | Content Marketing Manager | 🟡 T2 |
| 3.10 | Performance Marketing Manager | 🟠 T3 (TRADEMARK-RESTRICTED) |
| 3.11 | SEO Specialist | 🟡 T2 |
| 3.12 | Email Marketing Specialist | 🟡 T2 |
| 3.13 | Social Media Manager | 🟠 T3 |
| 3.14 | Community Manager | 🟠 T3 |
| 3.15 | Brand Manager | 🟠 T3 |
| 3.16 | Product Marketing Manager | 🟡 T2 |
| 3.17 | Growth Marketer | 🟡 T2 |
| 3.18 | Channel Sales Manager | 🟠 T3 |

## Sub-agents (v0.2.0)

| Agent | Cadence | Class |
|-------|---------|-------|
| `sales-pipeline` | Daily 12:00 PYT | CONTENT (reflection) |
| `proposal-drafter` | On-demand | CONTENT (reflection) |
| `lead-enrichment` | Daily | OPERATIONAL |
| `marketing-content-producer` | Mon/Wed/Fri | CONTENT (reflection) |
| `multimedia-producer` | On-demand | CONTENT (reflection) |
| `customer-health-scorer` (Tier 3) | Weekly | OPERATIONAL |

## Inputs the lead agent reads

1. `/opt/data/agents/state/sales.json` — prior state (SQLite)
2. CF Worker `rubicon-eas-lead` log (inbound form submissions)
3. LinkedIn inbound (with explicit authorization)
4. Referral partner pings
5. `/opt/data/richar-ruiz-outreach/` — named deal context
6. `/opt/data/agents/state/finance.json` — pricing benchmarks
7. ICP definitions in `marketing-strategy/playbook.md`

## Conversion funnel targets (per analysis B3 SA-2)

- leads → calls: > 40%
- calls → proposals: > 60%
- proposals → signed: > 30%
- Pipeline coverage: 3x quarterly target

## Cadence

- Daily 12:00 PYT: sales-pipeline lead triage
- Daily: lead-enrichment (overnight data refresh)
- Mon/Wed/Fri: marketing-content-producer
- On-demand: proposal-drafter, multimedia-producer
- Weekly Friday 16:00 PYT: pipeline summary (handoff to finance-controller)
- Quarterly: ICP validation

## Inbound-first principle (per D2)

Outbound sequencing DEFERRED until:
- 20+ inbound leads/week sustained 4 weeks
- THEN add outbound agent

**Why**: 2026 evidence shows inbound-first outperforms outbound. Plus trademark banlist blocks Meta/TikTok/paid acquisition.

## Test deal: richar-ruiz

The named deal in `/opt/data/richar-ruiz-outreach/`. Use as canary for entire pipeline:
- Track conversion metrics specifically
- Surface in every sales-pipeline brief until signed
- Use to validate ICP scoring algorithm

## State schema (`state/sales.json`)

```json
{
  "last_run": null,
  "leads_in_flight": [
    {"name": "...", "icp": "SME", "stage": "qualified", "value_usd": 1500, "next_action": "...", "blocker": null}
  ],
  "funnel_30d": {"leads": 0, "calls_booked": 0, "proposals_sent": 0, "contracts_signed": 0},
  "outreach_queue_today": [],
  "stalled_deals": []
}
```

## Storage (v0.2.0)

- SQLite: `/opt/data/db/sales.db`
- Per-agent git repo: `/opt/data/git-repos/aiw-agents-sales-pipeline/`

## Trademark compliance (hard rule)

- **Banned**: Meta, TikTok, Twitter, Slack, Discord (per trademark-compliance-scrub)
- **Required**: trademark-scrub.sh on every external artifact

## Escalation triggers

- New lead ICP match > 80% AND value > $5K → page Ivan
- Proposal out > 14d no reply → suggest follow-up
- Any complaint/refund → Ivan direct (no agent reply)
- Negative social signal → same-day alert

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Playbook: `/opt/data/agents-v2/playbooks/02-sales-growth.md`
- Agent spec: `/opt/data/agents-v2/agents/sales-pipeline/PROMPT.md`
- Skills: `/opt/data/b2b-cold-outreach-pitch/`, `/opt/data/paraguai-proposal-pricing/`

---

## CHANGELOG

- v0.2.0 (2026-08-14): added 18 sub-roles, 6 sub-agents (including new Tier 2 marketing/content agents), Conversion targets, Inbound-first principle, Storage architecture, Cross-references.
- v0.1.0 (2026-08-13): initial ratification.
