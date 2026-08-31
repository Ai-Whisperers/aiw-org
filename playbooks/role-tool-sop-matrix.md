# Role × Tool × SOP Matrix

> Pivot table: rows = roles across all 30 functional areas, columns = tool tier + SOP cadence.
> **Last updated**: 2026-08-14

---

## Reading guide

This matrix is the master reference for: "what does each role use, and how often does it do what?"

For brevity, only Tier 1 and Tier 2 roles are listed in detail. Tier 3/4 deferred roles are aggregated.

---

## Operations dept

| Role | Default tool | OSS alt | Premium | Daily | Weekly | Monthly |
|------|--------------|---------|---------|-------|--------|---------|
| Operations Lead | Telegram + WhatsApp | Matrix (OSS) | Canal de comunicacion (banned) | review alerts | review OKRs | review budget |
| Repo Steward | `gh` CLI | Gitea | GitHub Enterprise | scan for stale | archive idle | quarterly sweep |
| Asset Tracker | JSON inventory | Snipe-IT | Jamf | log changes | reconcile | full audit |
| Vendor Coordinator | Spreadsheet + email | FreeScout | Vendr | — | review renewals | vendor review |
| Compliance Watchdog | trademark-scrub.sh | OPA | Vanta | scrub every artifact | weekly check | annual audit |
| Watchdog Engineer | Bash + cron | Healthchecks.io | Datadog | monitor health | review alerts | monthly review |
| BizOps Specialist | Spreadsheet + dashboards | Metabase | Looker | — | OKR tracking | exec brief |

---

## Finance & Legal dept

| Role | Default tool | OSS alt | Premium | Daily | Weekly | Monthly |
|------|--------------|---------|---------|-------|--------|---------|
| CFO/Controller | (manual) | (manual) | (manual) | review brief | approve contracts | monthly close |
| Accountant | Wave (free) | GnuCash | QuickBooks | categorize | reconcile | monthly close |
| Bookkeeper | sub-agent | — | — | (auto) | weekly close | annual |
| AP Specialist | sub-agent | — | — | (auto) | process invoices | monthly |
| AR Specialist | sub-agent | — | — | (auto) | chase payments | monthly |
| Procurement Officer | procurement-tracker | — | Vendr | — | review renewals | vendor review |
| Legal Counsel | (external retainer) | — | — | — | (on-demand) | (on-demand) |
| Compliance Officer | trademark-scrub | OPA | Vanta | scrub | weekly check | annual audit |
| Tax Specialist | (external annual) | — | — | — | — | annual filing |
| Contract Drafter | Pandoc templates | — | DocuSign | — | (on-demand) | — |
| FP&A Analyst | sub-agent + spreadsheet | — | Cube | — | unit econ | forecast |
| Pricing Analyst | sub-agent + pricing-skill | — | — | (on-demand) | — | — |

---

## Sales & Growth dept

| Role | Default tool | OSS alt | Premium | Daily | Weekly | Monthly |
|------|--------------|---------|---------|-------|--------|---------|
| Head of Sales | EspoCRM | SuiteCRM | Salesforce (banned) | review pipeline | forecast | quarterly review |
| SDR | Mautic (sequences) | Mautic | Outreach (banned) | outreach queue | (auto) | — |
| AE | EspoCRM + calendar | SuiteCRM | Salesforce (banned) | close deals | pipeline review | forecast |
| Proposal Writer | proposal-drafter + Pandoc | — | — | (on-demand) | — | — |
| Marketing Manager | WordPress + Plausible | Hugo | HubSpot (banned) | review content | content calendar | campaign review |
| Content Producer | Obsidian + Markdown | Hugo | — | draft posts | publish | — |
| SEO Specialist | SerpBear | SerpBear | Ahrefs | — | keyword research | monthly audit |
| Email Marketing | Listmonk | Listmonk | Mailchimp | — | send campaign | list cleanup |
| Customer Success Manager | FreeScout | FreeScout | Zendesk (banned) | respond to tickets | QBR prep | quarterly |
| Channel Sales Manager | Spreadsheet | — | PartnerStack | — | — | — |

---

## Engineering & Delivery dept

| Role | Default tool | OSS alt | Premium | Daily | Weekly | Monthly |
|------|--------------|---------|---------|-------|--------|---------|
| CTO/Eng Lead | Cursor + GH | VSCode | Cursor Pro | code review | sprint review | capacity plan |
| Frontend Engineer | Next.js + Tailwind | — | — | code | PR review | — |
| Backend Engineer | Node/Python + Postgres | — | — | code | PR review | — |
| Full-stack Engineer | (consolidated) | — | — | code | PR review | — |
| DevOps / SRE | Docker Swarm + Traefik | — | — | monitor | deploy | — |
| QA Engineer | Vitest + Playwright | — | — | run tests | review coverage | — |
| Security Engineer | security-watchdog + OWASP | — | Snyk | scan | review vulns | patch Tuesday |
| Tech Writer | Obsidian + Markdown | Docusaurus | — | — | doc review | — |
| AI Safety Engineer | ai-safety-engineer + OWASP | — | — | check agents | chaos test | threat model |
| Database Admin | sqlite-admin + postgres | — | — | (on-trigger) | review | — |

---

## Research & Education dept

| Role | Default tool | OSS alt | Premium | Daily | Weekly | Monthly |
|------|--------------|---------|---------|-------|--------|---------|
| Research Lead | Obsidian + Zotero | — | — | (manual) | thesis review | — |
| Researcher | Python + pandas | — | — | (thesis work) | thesis review | — |
| Writer / Editor | Obsidian + Markdown | — | — | draft | edit | — |
| Citation Specialist | Zotero + citation-checker | Manubot | — | (on-publish) | — | — |
| Course Designer | Obsidian + Marp | — | — | design | review | — |
| Course Producer | course-producer + Pandoc | — | — | — | produce | — |
| Research Engineer | Python + Jupyter | — | — | (on-demand) | — | — |
| Publication Coordinator | Pandoc + arxiv | — | — | (on-demand) | track submissions | — |
| Source Curator | source-curator | — | — | — | freshness sweep | triage |

---

## People & Culture dept

| Role | Default tool | OSS alt | Premium | Daily | Weekly | Monthly |
|------|--------------|---------|---------|-------|--------|---------|
| Head of People | (manual) | — | — | — | check-in | — |
| Performance Coach | kiki-coach | — | — | — | lesson | — |
| Recognition Lead | LinkedIn + Notes | — | — | (on-milestone) | — | — |

---

## Cross-cutting Tier 2 (8 functions)

| Function | Default tool | OSS alt | Premium | Cadence |
|----------|--------------|---------|---------|---------|
| AI Ops | Bash + cron + eval | — | Datadog | daily + on-event |
| Compliance | trademark-scrub + manual | OPA | Vanta | on-every-artifact |
| Knowledge Mgmt | Markdown + source-curator | — | — | weekly sweep |
| RevOps | EspoCRM + Metabase | — | Looker | daily pipeline |
| BizOps | Dashboards + OKRs | Metabase | — | weekly |
| Customer Success | FreeScout | FreeScout | — | daily tickets |
| AI Safety | hard-stop-wrapper + chaos | — | — | 30 min + weekly |
| Procurement | procurement-tracker | — | Vendr | weekly renewals |

---

## Tool tier legend

| Tier | Cost | When to use |
|------|------|-------------|
| **Default** | Free / included | Day 1 |
| **OSS alt** | Free + self-host | When default is insufficient |
| **Premium** | $$/mo | Only when scale demands |

---

## Trademark-restricted tools (BANNED)

Per `02-finance-legal.md` lines 64-70:
- Canal de comunicacion → Matrix (OSS)
- Canal de comunicacion → Matrix (OSS)
- Salesforce → EspoCRM (OSS)
- Plataforma de Redes → (no replacement, banned entirely)
- Plataforma de videos cortos → (no replacement, banned entirely)
- Red social/X → (no replacement)
- Pasarela de pagos/Pasarela de pagos secundaria → (use Paraguay bank rails)
- Buscador principal Workspace → (use Proton/Nextcloud)
- Plataforma de video → PeerTube (OSS) when needed
- Suite ofimatica → LibreOffice (OSS)
- AWS → Cloudflare R2 + Hostinger VPS
- Asistente de IA generativa/Proveedor de IA/Modelo de IA → use local models + litellm

---

## Cadence summary

| Cadence | Count of activities |
|---------|---------------------|
| Continuous (every 5-30 min) | 6 (watchdogs + monitors) |
| Daily | ~15 (agent runs + automation) |
| Weekly | ~25 (agent runs + meetings) |
| Monthly | ~10 (reviews) |
| Quarterly | ~5 (business reviews) |

---

## Cost roll-up (defaults only)

| Category | Monthly USD |
|----------|-------------|
| Hosting (Hostinger VPS) | ~$30 |
| Cloudflare (R2 + Workers) | ~$10 |
| GitHub (free tier) | $0 |
| LLM API (litellm primary) | ~$50 |
| Domain + DNS | ~$5 |
| Compliance (trademark-scrub, etc.) | $0 |
| Observability (cron + bash) | $0 |
| **Total estimated burn** | **~$95** |

Within $400-600/mo budget with margin.

---

## See also

- `/opt/data/agents-v2/playbooks/00-INDEX.md` (master cross-dept)
- `/opt/data/agents-v2/playbooks/01-06` (per-dept playbooks)
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` (cost section)
- `/opt/data/agents-v2/DECISIONS-2026-Q3.md` D1 (cost cap $1/agent/day)
