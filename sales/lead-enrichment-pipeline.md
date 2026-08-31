# Lead Enrichment Pipeline — Atomic Agents + CRM Integration

> **Phase 8 Area #22** | Sales & Growth dept | Owner: cadmus-lead-enrichment + sales-pipeline
> **Date**: 2026-09-01
> **Status**: Design (no live pipeline; pending Worker fix for inbound)

---

## Current state

Atomic agents exist:
- `cadmus-lead-enrichment` (demiurge/agents/) — adds contact info from public sources
- `clio-customer-signal-collector` (demiurge/agents/) — collects buying signals

**No CRM** currently. Lead data lives in `state/coaching-customers.json` and `state/customers.json`.

---

## CRM options (<100 leads)

| Option | Free tier | Pricing at scale | Integration | Verdict |
|--------|-----------|------------------|-------------|---------|
| **Airtable** | 1,200 records/base | $20/mo per user | API + Zapier | ✅ Best for our scale |
| **HubSpot Free CRM** | 1M contacts | $20/mo per user (paid) | API + Zapier | OK but bloated |
| **Notion DB** | Unlimited | Free | API | Free but limited querying |
| **Self-hosted (postgres)** | Unlimited | Hosting cost | Direct | Overkill for <100 leads |

**Recommendation**: **Airtable Free** until we hit 200+ leads, then upgrade.

---

## Pipeline design

### Stage 1: Formspree submission (post-Worker-fix)

```
Prospect fills form
  → Formspree captures
  → Zapier forwards to Airtable (new row)
  → sales-pipeline agent triggers (cron: every 30min)
  → cadmus-lead-enrichment enriches (add company info, LinkedIn, etc.)
  → Row updated with enrichment
```

### Stage 2: Manual outreach

```
Sales rep picks lead from Airtable
  → Logs outreach attempt (state/conversion-attempts.json)
  → If reply: schedules discovery call
  → clio-customer-signal-collector adds buying signals
```

### Stage 3: Qualified → Discovery

```
Discovery call scheduled (calendar invite)
  → After call: update Airtable with gap analysis (Gap Selling)
  → If qualified: trigger proposal-drafter agent
```

### Stage 4: Proposal → Close

```
Proposal sent (from metis-proposal-drafter)
  → Track open + response
  → If accepted: contract → onboarding
  → If rejected: log loss reason (for archaeology)
```

---

## Airtable schema (initial)

| Field | Type | Notes |
|-------|------|-------|
| `id` | Auto | UUID |
| `name` | Text | |
| `company` | Text | |
| `email` | Email | |
| `phone` | Phone | WhatsApp preferred |
| `vertical` | Select | legal / coaching / retail / saas / other |
| `source` | Select | form / outbound / referral |
| `stage` | Select | new / contacted / discovery / proposal / closed-won / closed-lost |
| `gap_analysis_current` | Long text | (Gap Selling) |
| `gap_analysis_future` | Long text | |
| `gap_analysis_gap` | Long text | |
| `next_action` | Text | |
| `next_action_date` | Date | |
| `created_at` | Created time | |
| `last_updated` | Last modified time | |

---

## What to do now

1. **Worker fix** (Phase 8 #19 decision): use Formspree
2. **Create Airtable base**: `/opt/data/sales/leads-pipeline` (mirrored to Airtable)
3. **Test end-to-end** with 1 prospect (after Worker fix)
4. **Document the integration** in `sales/airtable-integration.md`

---

**Cross-references**:
- `demiurge/agents/cadmus-lead-enrichment/PROMPT.md`
- `demiurge/agents/clio-customer-signal-collector/PROMPT.md`
- `state/coaching-customers.json`
- `state/conversion-attempts.json`
- `analysis/PHASE-7-dept-research/03-sales-growth-research-areas.md` Area #8

