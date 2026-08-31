# 04 — Finance & Legal Playbook

> Department charter + roles + agents + tooling + SOPs for Finance & Legal.
> **Last updated**: 2026-08-14

---

## Finance & Legal — Department Charter

**Mission**: Track every dollar, every contract, every compliance flag. Finance & Legal makes sure Ivan knows the company's financial and legal position without opening a spreadsheet.

**Head**: Ivan
**Sub-functions**: Compliance (Tier 2 named role), Procurement (Tier 2)

---

## Roles (14 roles)

| # | Role | Tier | Status |
|---|------|------|--------|
| 2.1 | CFO/Controller | 🟢 T1 | Ivan |
| 2.2 | Accountant | 🟡 T2 | external contractor |
| 2.3 | Bookkeeper | 🟢 T1 | sub-agent: finance-controller |
| 2.4 | AP Specialist | 🟡 T2 | sub-agent |
| 2.5 | AR Specialist | 🟡 T2 | sub-agent |
| 2.6 | Procurement Officer | 🟢 T1 | Ivan (manual) + sub-agent |
| 2.7 | Legal Counsel | 🟢 T1 | external contractor (retainer) |
| 2.8 | Compliance Officer | 🟢 T1 | NAMED ROLE — Ivan wearing the hat (per D3) |
| 2.9 | Tax Specialist | 🟢 T1 | external accountant (annual) |
| 2.10 | Contract Drafter | 🟢 T1 | sub-agent |
| 2.11 | Payroll Specialist | 🔴 T4 | deferred (no FTEs) |
| 2.12 | Treasurer | 🟠 T3 | deferred ($100K+ cash trigger) |
| 2.13 | FP&A Analyst | 🟡 T2 | sub-agent |
| 2.14 | Pricing Analyst | 🟢 T1 | Ivan + sub-agent |

---

## Sub-agents (Tier 2)

| Agent | Cadence | Mission |
|-------|---------|---------|
| `finance-controller` | Fri 18:00 PYT | Weekly close, runway, contracts |
| `accounting-automation` | Daily | Categorizes expenses, generates invoices |
| `tax-receipt-tracker` | Weekly | Tracks receipts for tax filing |
| `procurement-tracker` | Weekly | Vendor evaluation, renewal management |
| `compliance-monitor` | Weekly | Compliance program monitoring |

---

## Tooling

### CFO/Controller (Ivan)
- **Bookkeeping**: Wave (free tier) or GnuCash (OSS)
- **Invoicing**: Invoice Ninja (OSS) — alt for FreshBooks
- **Banking**: Bank APIs (per Paraguay banks: Sudameris, Continental, GNB)
- **FX tracking**: Manual + cron rate refresh

### Legal Counsel
- **Contracts**: Pandoc + Markdown templates
- **E-signature**: Documenso (OSS)
- **Trademark monitoring**: trademark-compliance-scrub skill

### Compliance Officer (Ivan wearing hat)
- **Trademark**: trademark-scrub.sh on every public artifact
- **Privacy**: Manual review of any EU-adjacent content
- **EU AI Act**: Hard-stop on EU clients until named officer filled

### Tax Specialist (external)
- **Annual filing**: SET/DNIT (Paraguay tax authority)
- **IRP**: Personal income tax on domestic-source income only
- **Foreign income**: Tax-free under Paraguay law

---

## Compliance HARD rules (per `02-finance-legal.md` lines 64-70)

**Banned** (case-insensitive, mechanical):
`texto mensajeria empresarial canal de texto web canal de texto red social principal objetivo red social de fotos red social de fotos canal de mensajeria gafas de realidad virtual pasarela de pagos secundaria pasarela de pagos buscador principal correo electronico plataforma de video plataforma de videos cortos red social red social canal de comunicacion canal de comunicacion suite ofimatica suite ofimatica dispositivo personal almacenamiento en la nube tienda en linea infraestructura-en-la-nube- proveedor de IA asistente de IA generativa proveedor de IA modelo de IA`

**Carve-outs**: bare functional terms ("messaging bridge", "linked device"); upstream OSS names; Hostinger incident quote; existing package names.

**Reason**: Hostinger suspended `srv1396188.hstgr.cloud` 2026-Q1 over `mensajeconnect.paragu-ai.com` flagged as phishing impersonation.

**Enforcement**: `trademark-scrub.sh` runs on every artifact before publish.

---

## EU client hard-stop (per D3)

> **No EU client contracts accepted until Compliance Officer role is filled by a named person (not Ivan alone).**

Trigger to promote Compliance Officer to standalone dept: first EU client OR $50K MRR.

---

## Paraguay tax facts

- **IRP** (Personal Income Tax): Only domestic-source income is taxed
- **Foreign income**: Tax-free
- **IVA** (VAT): 10% on goods/services
- **RUC**: Tax ID for businesses (required for invoicing)

---

## SOPs

### Weekly
- Fri 18:00 PYT: finance-controller (weekly close)
- Weekly: tax-receipt-tracker, procurement-tracker, compliance-monitor

### Daily
- Daily: accounting-automation (expense categorization, invoice generation)

### Monthly
- Quarterly: budget review
- Monthly: bank reconciliation (manual)

### Annually
- Tax filing (external accountant)
- Trademark portfolio renewal
- License renewals

---

## Hard stops (Finance dept)

| Action | Authority |
|--------|-----------|
| Send a proposal (after scope approval) | Ivan |
| Sign a contract | Ivan only |
| Re-issue an invoice | Finance agent (logged, Ivan notified) |
| Renew a domain < $100/yr | Finance agent (logged) |
| Renew a domain > $100/yr | Ivan |
| New vendor onboarding | Ivan + Kiki |
| Trademark compliance scrub | Finance agent (automated) |

---

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

---

## Pricing benchmarks (per Session 1 — Rubicón EAS deal)

| Tier | Dental (Gs.) | Legal multiplier | Legal (USD) |
|------|--------------|------------------|-------------|
| Quick-Win | 500K setup + 150K/mo | ~3x | 1.5K setup + 550/mo |
| Standard | 1.2M setup + 400K/mo | ~3x | 2K setup + 1.3K/mo |
| Premium | 2.5M setup + 900K/mo | ~3x | 4.5K setup + 2.5K/mo |
| Enterprise | — | bespoke | 9K setup + 2.5K/mo |

---

## Skills stack

- `paraguai-proposal-pricing` — pricing templates + multipliers
- `trademark-compliance-scrub` — public artifact compliance
- `prospect-dossier-pii-sanitization` — PII handling

---

## Cash-flow model (per Phase 7 task 7.4)

- Current: $240/mo MRR, $400-600/mo burn
- After Phase 7: +$200/mo new tools = $600-800/mo burn
- Runway at current: many months
- Runway after Phase 7: 3-4 months if MRR doesn't grow
- **Trigger to reduce tool spend**: if MRR < $400/mo for 60 days

---

## FX exposure (per Phase 7 task 7.5)

- Gs/USD historical: ~15% depreciation 2025-2026
- New SaaS contracts in USD: priced at spot rate, no hedge
- **Recommendation**: avoid 12-month USD commitments; prefer monthly billing

---

## Escalation triggers

- Spend > $500 unauthorized → escalate
- Runway < 3 months → emergency brief
- Compliance flag severity "high" → page immediately
- New vendor > $50/mo not on approved list → Ivan + Kiki joint approval

---

## See also

- `/opt/data/agents/departments/02-finance-legal.md` (canonical charter)
- `/opt/data/agents-v2/agents/finance-controller/PROMPT.md` (agent spec)
- `/opt/data/build/rubicon-eas/marketing/ometz-reference/` (pricing benchmarks)
- `/opt/data/scratchpad/wa-bridge-rewrite/` (Hostinger compliance reply draft)
