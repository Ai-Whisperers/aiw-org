# Department 2 — Finance & Legal

**Head**: Ivan
**Lead agent**: `finance-controller` (Fri 18:00 PYT)
**Version**: 0.2.0
**Last updated**: 2026-08-14

---

## Mission

Track every dollar in and out, every contract sent/signed/expired, every compliance flag. The Finance & Legal department's job is to make sure Ivan knows the company's financial and legal position without opening a spreadsheet.

## What this department owns

- **Revenue tracking** — all signed contracts, MRR components, one-time payments
- **Cost tracking** — VPS hosting, domain renewals, tool subscriptions
- **Contracts pipeline** — sent, signed, expired, pending
- **Compliance flags** — Hostinger banlist, trademark compliance, data residency
- **Runway calculation** — months of operating runway at current burn
- **Pricing integrity** — proposal templates match the canonical rate card
- **NEW v0.2.0**: Procurement discipline (sub-function)
- **NEW v0.2.0**: Compliance (named role, Ivan wearing hat per D3)
- **NEW v0.2.0**: EU client hard-stop (regulatory compliance)

## What this department does NOT own

- Outreach scripts (Sales)
- Tech architecture decisions (Engineering)
- Kiki's lesson curriculum (People)
- Research publication strategy (Research)

## Decision rights (v0.2.0)

| Action | Authority |
|--------|-----------|
| Send a proposal (after scope approval) | Ivan |
| Sign a contract | Ivan only |
| Re-issue an invoice | Finance agent (logged, Ivan notified) |
| Renew a domain < $100/yr | Finance agent (logged) |
| Renew a domain > $100/yr | Ivan |
| New vendor onboarding | Ivan + Kiki |
| Trademark compliance scrub | Finance agent (automated) |
| **NEW**: Hire legal counsel | require Ivan |
| **NEW**: Hire external accountant | require Ivan |
| **NEW**: Sign EU client contract | HARD-STOP until named Compliance Officer |

## Compliance rules (HARD per `02-finance-legal.md` lines 64-70)

**Banned** (case-insensitive, mechanical):
`mensaje mensajebusiness mensaje-web wpp facebook meta instagram insta messenger oculus paypal stripe google gmail youtube tiktok twitter x-com discord slack microsoft office365 apple icloud amazon aws- openai chatgpt anthropic claude`

**Carve-outs**: bare functional terms; upstream OSS names; Hostinger incident quote; existing package names.

**Reason**: Hostinger suspended `srv1396188.hstgr.cloud` 2026-Q1 over `mensajeconnect.paragu-ai.com` flagged as phishing impersonation.

**Enforcement**: `trademark-scrub.sh` runs on every public artifact.

## EU client hard-stop (per D3)

> **No EU client contracts accepted until Compliance Officer role is filled by a named person (not Ivan alone).**

Trigger to promote Compliance Officer to standalone dept: first EU client OR $50K MRR.

## Sub-roles (v0.2.0 — 14 roles from ROLES-INVENTORY.md)

| # | Role | Tier |
|---|------|------|
| 2.1 | CFO/Controller | 🟢 T1 |
| 2.2 | Accountant | 🟡 T2 |
| 2.3 | Bookkeeper | 🟢 T1 |
| 2.4 | AP Specialist | 🟡 T2 |
| 2.5 | AR Specialist | 🟡 T2 |
| 2.6 | Procurement Officer | 🟢 T1 |
| 2.7 | Legal Counsel | 🟢 T1 (external) |
| 2.8 | **Compliance Officer (named role)** | 🟢 T1 |
| 2.9 | Tax Specialist | 🟢 T1 (external) |
| 2.10 | Contract Drafter | 🟢 T1 |
| 2.11 | Payroll Specialist | 🔴 T4 |
| 2.12 | Treasurer | 🟠 T3 |
| 2.13 | FP&A Analyst | 🟡 T2 |
| 2.14 | Pricing Analyst | 🟢 T1 |

## Sub-agents (v0.2.0)

| Agent | Cadence | Class |
|-------|---------|-------|
| `finance-controller` | Fri 18:00 PYT | OPERATIONAL |
| `accounting-automation` (NEW) | Daily | OPERATIONAL |
| `tax-receipt-tracker` (NEW) | Weekly | OPERATIONAL |
| `procurement-tracker` (NEW) | Weekly | OPERATIONAL |
| `compliance-monitor` (NEW) | Weekly | OPERATIONAL |

## Inputs the lead agent reads

1. `/opt/data/agents/state/finance.json` (SQLite)
2. `/opt/data/db/sales.json` equivalent — deals in flight
3. `/opt/data/db/engineering.json` equivalent — infra cost changes
4. VPS bills (Hostinger, Servarica, Cloudflare)
5. Tool subscriptions (current list per `/opt/data/agents/research/tool-stack-decisions.md`)
6. `/opt/data/build/rubicon-eas/marketing/ometz-reference/` — pricing benchmarks
7. PYT timezone: UTC-4 year-round

## Pricing benchmarks (Rubicón EAS deal)

| Tier | Dental (Gs.) | Legal multiplier | Legal (USD) |
|------|--------------|------------------|-------------|
| Quick-Win | 500K setup + 150K/mo | ~3x | 1.5K setup + 550/mo |
| Standard | 1.2M setup + 400K/mo | ~3x | 2K setup + 1.3K/mo |
| Premium | 2.5M setup + 900K/mo | ~3x | 4.5K setup + 2.5K/mo |
| Enterprise | — | bespoke | 9K setup + 2.5K/mo |

**2026 refresh**: 10% lower entry tiers (AI agents reduce delivery cost).

## Cadence (v0.2.0)

| Time | What |
|------|------|
| Fri 18:00 PYT | finance-controller weekly close |
| Daily | accounting-automation |
| Weekly | tax-receipt-tracker, procurement-tracker, compliance-monitor |
| Daily 02:00 | db-snapshot |
| Quarterly | budget review, compliance audit |

## State schema (`state/finance.json`)

```json
{
  "last_run": null,
  "runway_months": null,
  "mrr_usd": 240,
  "burn_usd_monthly": 500,
  "deals_open": [],
  "deals_signed_this_week": [],
  "compliance_flags": [],
  "renewals_due_30d": []
}
```

## Escalation triggers

- Spend > $500 unauthorized → escalate
- Runway < 3 months → emergency brief
- Compliance flag severity "high" → page immediately
- New vendor > $50/mo not on approved list → Ivan + Kiki joint approval
- **NEW**: EU client contract attempt → HARD-STOP, surface to Compliance Officer

## Cash-flow model (per Phase 7)

- Current: $240/mo MRR, $400-600/mo burn
- After Phase 7: ~$600/mo burn
- **Break-even**: Month 2-3 with 1 deal closed
- **Trigger to reduce tool spend**: if MRR < $400/mo for 60 days

## FX exposure

- Gs/USD historical: ~15% depreciation 2025-2026
- Recommendation: avoid 12-month USD commitments; prefer monthly billing

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Playbook: `/opt/data/agents-v2/playbooks/04-finance-legal.md`
- Agent spec: `/opt/data/agents-v2/agents/finance-controller/PROMPT.md`
- Tool stack: `/opt/data/agents/research/tool-stack-decisions.md`
- Hostinger compliance: `/opt/data/scratchpad/wa-bridge-rewrite/`

---

## CHANGELOG

- v0.2.0 (2026-08-14): added 14 sub-roles, 5 sub-agents (incl. compliance-monitor), EU client hard-stop, Compliance Officer named role, Pricing refresh, Cash-flow model, FX exposure, Cross-references.
- v0.1.0 (2026-08-13): initial ratification.
