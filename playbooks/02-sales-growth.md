# 02 — Sales & Growth Playbook

> Department charter + roles + agents + tooling + SOPs for Sales & Growth.
> **Last updated**: 2026-08-14

---

## Sales & Growth — Department Charter

**Mission**: Generate qualified leads, run outreach, close deals. Sales is the only department that directly produces revenue.

**Head**: Ivan
**Sub-functions**: Marketing (sub at Tier 1, promotes to own dept at Tier 3)

---

## Roles (18 roles)

| # | Role | Tier | Status |
|---|------|------|--------|
| 3.1 | Head of Sales / CRO | 🟢 T1 | Ivan |
| 3.2 | SDR (Sales Development Rep) | 🟢 T1 | sub-agent (deferred outbound per D2) |
| 3.3 | BDR (Business Development Rep) | 🟡 T2 | deferred |
| 3.4 | Account Executive (AE) | 🟢 T1 | Ivan (closing) |
| 3.5 | Sales Engineer | 🟡 T2 | deferred |
| 3.6 | Customer Success Manager (CSM) | 🟡 T2 | Tier 3 dept promotion |
| 3.7 | Proposal Writer | 🟢 T1 | sub-agent: proposal-drafter |
| 3.8 | Marketing Manager | 🟢 T1 | Ivan + content-producer |
| 3.9 | Content Marketing Manager | 🟡 T2 | sub-agent |
| 3.10 | Performance Marketing Manager | 🟠 T3 | TRADEMARK-RESTRICTED |
| 3.11 | SEO Specialist | 🟡 T2 | sub-agent |
| 3.12 | Email Marketing Specialist | 🟡 T2 | sub-agent |
| 3.13 | Social Media Manager | 🟠 T3 | TRADEMARK-RESTRICTED on some |
| 3.14 | Community Manager | 🟠 T3 | deferred |
| 3.15 | Brand Manager | 🟠 T3 | deferred |
| 3.16 | Product Marketing Manager | 🟡 T2 | sub-agent |
| 3.17 | Growth Marketer | 🟡 T2 | sub-agent |
| 3.18 | Channel Sales Manager | 🟠 T3 | deferred |

---

## Sub-agents (Tier 2)

| Agent | Cadence | Mission |
|-------|---------|---------|
| `sales-pipeline` | Daily 12:00 PYT | Inbound triage, ICP scoring |
| `proposal-drafter` | On-demand | Drafts proposals after discovery call |
| `lead-enrichment` | Daily | Adds intent signals, scores leads |
| `marketing-content-producer` | Mon/Wed/Fri | Blog posts, social |
| `multimedia-producer` | On-demand | Video, graphics, podcast |
| `customer-health-scorer` | Tier 3 | Proactive churn detection |

---

## Tooling

### Head of Sales (Ivan)
- **CRM**: EspoCRM (OSS) — self-hosted
- **Email tracking**: Mailscale (OSS alt for Yesware)
- **Calendar**: Buscador principal Calendar via API
- **Docs**: Obsidian + Markdown

### SDR / AE
- **Email sequences**: Mautic (OSS) — alt for Outreach.io
- **LinkedIn automation**: Banned (trademark)
- **Dialer**: Aircall (premium) or browser-based

### Proposal Writer
- **Templates**: Pandoc + Markdown → PDF (OSS)
- **E-signature**: Documenso (OSS) — alt for DocuSign
- **Pricing refs**: `paraguai-proposal-pricing` skill

### Marketing Manager
- **Content**: WordPress + Gutenberg (OSS) or Hugo static
- **SEO**: Ahrefs (premium) or SerpBear (OSS)
- **Email**: Listmonk (OSS) or Mailchimp (premium)
- **Analytics**: Plausible (OSS) or GA4 (free)

### Content Producer
- **Writing**: Obsidian + Markdown
- **Images**: Canva (freemium) or FOSS Krita
- **Multimedia**: DaVinci Resolve (OSS) or Final Cut Pro (premium)

---

## SOPs

### Daily
- 12:00 PYT: sales-pipeline cron (lead triage)
- Daily: lead-enrichment (overnight data refresh)

### Weekly
- Mon/Wed/Fri: marketing-content-producer
- Friday 16:00 PYT: pipeline summary (handoff to finance-controller)

### On-demand
- proposal-drafter (triggered after discovery call booked)
- multimedia-producer (triggered after content draft approved)

### Monthly
- Quarterly: ICP validation (every 90 days per analysis B3 SA-1)

---

## ICP validation (per analysis B3 SA-1)

**3 ICPs** in `marketing-strategy/playbook.md`:
1. Solo entrepreneur ($500-5K budget)
2. SME ops manager ($10K-100K budget)
3. Corporate innovation lead ($100K-500K+ budget)

**Validation trigger**: 30 days of lead data
**Refresh cadence**: annually

---

## Conversion funnel targets (per analysis B3 SA-2)

| Stage | Target |
|-------|--------|
| leads → calls | > 40% |
| calls → proposals | > 60% |
| proposals → signed | > 30% |
| Pipeline coverage | 3x quarterly target |

---

## Hard stops (Sales dept)

| Action | Authority |
|--------|-----------|
| Send cold outreach draft | Sales agent (Ivan approves within 24h) |
| Reply to inbound lead | Sales agent (logged) |
| Book discovery call | Sales agent (logs to calendar) |
| Send proposal < $1K | Ivan pre-approves scope, Sales sends |
| Send proposal $1K-5K | Ivan reads proposal before send |
| Send proposal > $5K | Ivan + Kiki together |
| Discount > 15% off list | Ivan only |
| New outreach channel | Ivan + Kiki together |

---

## Test deal: richar-ruiz (per analysis B3 SA-4)

The named deal in `/opt/data/richar-ruiz-outreach/`. Use as canary for entire pipeline:
- Track conversion metrics specifically
- Surface in every sales-pipeline brief until signed
- Use to validate ICP scoring algorithm

---

## State schema (`state/sales.json`)

```json
{
  "last_run": null,
  "leads_in_flight": [
    {"name": "...", "icp": "SME", "stage": "qualified", "value_usd": 1500, "next_action": "...", "blocker": null}
  ],
  "funnel_30d": {
    "leads": 0,
    "calls_booked": 0,
    "proposals_sent": 0,
    "contracts_signed": 0
  },
  "outreach_queue_today": [],
  "stalled_deals": []
}
```

---

## Inbound-first principle (per D2)

Outbound sequencing DEFERRED until:
- 20+ inbound leads/week sustained 4 weeks
- THEN add outbound agent

**Why**: 2026 evidence (ToolDirectory) shows inbound-first outperforms outbound. Plus our trademark banlist blocks Plataforma de Redes/Plataforma de videos cortos/paid acquisition.

---

## Trademark compliance (hard rule)

- **Banned**: Plataforma de Redes, Plataforma de videos cortos, Red social, Canal de comunicacion, Canal de comunicacion (per trademark-compliance-scrub)
- **Allowed for content**: WordPress, Hugo, Mailchimp (alt), Ahrefs (alt)
- **Required for every external artifact**: trademark-scrub.sh

---

## Escalation triggers

- New lead ICP match > 80% AND value > $5K → page Ivan
- Proposal out > 14d no reply → suggest follow-up
- Any complaint/refund → Ivan direct (no agent reply)
- Negative social signal → same-day alert

---

## See also

- `/opt/data/agents/departments/03-sales-growth.md` (canonical charter)
- `/opt/data/agents-v2/agents/sales-pipeline/PROMPT.md` (agent spec)
- `/opt/data/b2b-cold-outreach-pitch/` (skill)
- `/opt/data/paraguai-proposal-pricing/` (skill)
