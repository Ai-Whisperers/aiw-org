# AIW Departments — Complete Reference (4 tiers, 31 depts, 137+ roles, 88+ agents)

> **Generated**: 2026-08-31 from canonical source files
> **Sources**:
> - `/opt/data/agents-v2/constitution/01-06-*.md` (6 Tier-1 charters, v0.2.0/v0.3.0)
> - `/opt/data/agents-v2/playbooks/07-cross-cutting-concerns.md` (8 Tier-2 concerns)
> - `/opt/data/agents-v2/playbooks/08-deferred-tier3.md` (17 Tier-3 + 5 Tier-4 depts)
> - `/opt/data/agents-v2/packages/*/agents/*/PROMPT.md` (35 v2 agent specs)
> - `/opt/data/agents/*/PROMPT.md` (51 v1-legacy agents, 30 active with outbox)
> - `/opt/data/scratchpad/analysis/AGENT-NAMES-V2.json` (portmanteau naming)

---

## Top-level summary

| Tier | Count | Description |
|---|---|---|
| **1** | **6** | Core departments (charters v0.2.0/v0.3.0) |
| **2** | **8** | Cross-cutting sub-functions |
| **3** | **17** | Deferred departments (with promotion triggers) |
| **4** | **5** | Enterprise scale departments |
| **TOTAL** | **36** | |

---

# TIER 1 — ACTIVE CORE DEPARTMENTS (6)

## Operations (v0.2.0)

> **Mission**: Keep the agent platform itself alive, healthy, observable. Operations is the **objetivo-department** — it doesn't ship products, it makes sure every other department can ship.

### Roles

| # | Role | Tier |
|---|---|---|
| 1.1 | Operations Lead | 🟢 T1 |
| 1.2 | Repo Steward | 🟢 T1 |
| 1.3 | Asset Tracker | 🟢 T1 |
| 1.4 | Vendor Coordinator | 🟢 T1 |
| 1.5 | Compliance Watchdog | 🟢 T1 |
| 1.6 | Watchdog Engineer | 🟢 T1 |
| 1.7 | BizOps Specialist | 🟡 T2 |
| 1.8 | COO | 🟠 T3 |

### Sub-agents (charter)

| Formal name | Portmanteau | Cadence |
|---|---|---|
| `management-coordinator` | **Coordina** | Mon+Thu 17:00 PYT |
| `business-analyst` | **Analisa** | Daily 06:30 PYT |
| `kiki-coach` | **Magistra** | Fri 17:00 PYT |

---

## Finance & Legal (v0.2.0)

> **Mission**: Track every dollar in and out, every contract sent/signed/expired, every compliance flag. The Finance & Legal department's job is to make sure Ivan knows the company's financial and legal position wit

### Roles

| # | Role | Tier |
|---|---|---|
| 2.1 | CFO/Controller | 🟢 T1 |
| 2.2 | Accountant | 🟡 T2 |
| 2.3 | Bookkeeper | 🟢 T1 |
| 2.4 | AP Specialist | 🟡 T2 |
| 2.5 | AR Specialist | 🟡 T2 |
| 2.6 | Procurement Officer | 🟢 T1 |
| 2.7 | Legal Counsel | 🟢 T1 *external* |
| 2.8 | Compliance Officer (named role) | 🟢 T1 |
| 2.9 | Tax Specialist | 🟢 T1 *external* |
| 2.10 | Contract Drafter | 🟢 T1 |
| 2.11 | Payroll Specialist | 🔴 T4 |
| 2.12 | Treasurer | 🟠 T3 |
| 2.13 | FP&A Analyst | 🟡 T2 |
| 2.14 | Pricing Analyst | 🟢 T1 |

### Sub-agents (charter)

| Formal name | Portmanteau | Cadence |
|---|---|---|
| `finance-controller` | **Finus** | Fri 18:00 PYT |
| `accounting-automation`` | **—** | Daily |
| `tax-receipt-tracker`` | **—** | Weekly |
| `procurement-tracker`` | **—** | Weekly |
| `compliance-monitor`` | **—** | Weekly |

---

## Sales & Growth (v0.2.0)

> **Mission**: Generate qualified leads, run outreach, close deals. Sales is the only department that directly produces revenue.

### Roles

| # | Role | Tier |
|---|---|---|
| 3.1 | Head of Sales / CRO | 🟢 T1 |
| 3.2 | SDR | 🟢 T1 |
| 3.3 | BDR | 🟡 T2 |
| 3.4 | Account Executive | 🟢 T1 |
| 3.5 | Sales Engineer | 🟡 T2 |
| 3.6 | Customer Success Manager | 🟡 T2 |
| 3.7 | Proposal Writer | 🟢 T1 |
| 3.8 | Marketing Manager | 🟢 T1 |
| 3.9 | Content Marketing Manager | 🟡 T2 |
| 3.10 | Performance Marketing Manager | 🟠 T3 *TM-restricted* |
| 3.11 | SEO Specialist | 🟡 T2 |
| 3.12 | Email Marketing Specialist | 🟡 T2 |
| 3.13 | Social Media Manager | 🟠 T3 |
| 3.14 | Community Manager | 🟠 T3 |
| 3.15 | Brand Manager | 🟠 T3 |
| 3.16 | Product Marketing Manager | 🟡 T2 |
| 3.17 | Growth Marketer | 🟡 T2 |
| 3.18 | Channel Sales Manager | 🟠 T3 |

### Sub-agents (charter)

| Formal name | Portmanteau | Cadence |
|---|---|---|
| `sales-pipeline` | **Saleina** | Daily 12:00 PYT |
| `proposal-drafter` | **Proporina** | On-demand |
| `lead-enrichment` | **Prospia** | Daily |
| `marketing-content-producer` | **Markina** | Mon/Wed/Fri |
| `multimedia-producer` | **Media** | On-demand |
| `customer-health-scorer`` | **—** | Weekly |

---

## Engineering & Delivery (v0.3.0)

> **Mission**: Ship client sites, maintain infra uptime, keep the ParaguAI Builder running, deploy changes safely. Engineering is where Kiki owns end-to-end.

### Roles

| # | Role | Tier |
|---|---|---|
| 4.1 | CTO/Eng Lead | 🟢 T1 |
| 4.2 | Engineering Manager | 🟠 T3 |
| 4.3 | Frontend Engineer | 🟢 T1 |
| 4.4 | Backend Engineer | 🟢 T1 |
| 4.5 | Full-stack Engineer | 🟢 T1 |
| 4.6 | Mobile Engineer | 🟠 T3 |
| 4.7 | DevOps / SRE | 🟢 T1 |
| 4.8 | QA Engineer | 🟢 T1 |
| 4.9 | Security Engineer | 🟢 T1 |
| 4.10 | ML Engineer | 🟠 T3 |
| 4.11 | Data Engineer | 🟠 T3 |
| 4.12 | Solutions Architect | 🟠 T3 |
| 4.13 | Tech Writer | 🟡 T2 |
| 4.14 | Engineering PM | 🟠 T3 |
| 4.15 | Platform Engineer | 🟠 T3 |
| 4.16 | Release Manager | 🟠 T3 |
| 4.17 | SRE | 🟠 T3 |
| 4.18 | DBA | 🟡 T2 |
| 4.19 | Network Engineer | 🟠 T3 |
| 4.20 | UI/UX Designer | 🟡 T2 |
| 4.21 | Product Designer | 🟠 T3 |
| 4.22 | EngOps Specialist | 🟠 T3 |
| 4.23 | Build/Release Engineer | 🟠 T3 |
| 4.24 | AI Safety Engineer | 🟢 T1 *NEW v0.2.0* |

### Sub-agents (charter)

| Formal name | Portmanteau | Cadence |
|---|---|---|
| `engineering-roster` | **Devin** | Tue+Fri 17:00 PYT |
| `devops-monitor` | **Devor** | Every 30 min |
| `qa-automation-runner` | **Qualis** | On-PR |
| `security-watchdog` | **Securia** | Every 30 min |
| `ai-safety-engineer`` | **—** | Every 30 min |
| `scope-intake`` | **—** | On Metis proposal |
| `delivery-tracker`` | **—** | Mon 11:00 PYT |
| `feasibility-gate`` | **—** | On Metis send |

---

## Research & Education (v0.2.0)

> **Mission**: Drive the master's thesis (P1 GeoData v2 — Paraguayan cartography) to completion, package research into publications, and turn it into paid products (courses, papers, consulting). Research is a flagsh

### Roles

| # | Role | Tier |
|---|---|---|
| 5.1 | Research Lead | 🟢 T1 |
| 5.2 | Researcher | 🟢 T1 |
| 5.3 | Writer / Editor | 🟢 T1 |
| 5.4 | Academic Liaison | 🟡 T2 |
| 5.5 | Citation / Bibliography Specialist | 🟢 T1 |
| 5.6 | Course Designer | 🟢 T1 |
| 5.7 | Course Producer | 🟡 T2 |
| 5.8 | Instructional Designer | 🟠 T3 |
| 5.9 | Subject Matter Expert (SME) | 🟡 T2 *external* |
| 5.10 | Research Engineer | 🟡 T2 |
| 5.11 | IP / Patent Specialist | 🟠 T3 |
| 5.12 | Publication Coordinator | 🟡 T2 |

### Sub-agents (charter)

| Formal name | Portmanteau | Cadence |
|---|---|---|
| `research-tracker` | **Researcha** | Sun 18:00 PYT |
| `citation-checker`` | **—** | On-demand |
| `thesis-tracker`` | **—** | Daily 06:00 UTC |
| `course-producer`` | **—** | Weekly |
| `source-curator`` | **—** | Weekly |

---

## People & Culture (v0.2.0)

> **Mission**: Make sure both founders (Ivan + Kiki) and any future hires stay sharp, healthy, and growing. People & Culture is small in headcount but huge in leverage — Ivan's bandwidth and Kiki's growth are the co

### Roles

| # | Role | Tier |
|---|---|---|
| 6.1 | Head of People / VP HR | 🟢 T1 |
| 6.2 | Recruiter | 🔴 T4 *deferred* |
| 6.3 | Onboarding Specialist | 🔴 T4 *deferred* |
| 6.4 | Performance Coach | 🟢 T1 |
| 6.5 | Recognition Lead | 🟢 T1 |
| 6.6 | Compensation Specialist | 🔴 T4 *deferred* |
| 6.7 | People Operations Specialist | 🟠 T3 *deferred* |
| 6.8 | Learning & Development Manager | 🟠 T3 *deferred* |

### Sub-agents (charter)

| Formal name | Portmanteau | Cadence |
|---|---|---|
| `kiki-coach` | **Magistra** | Fri 17:00 PYT |
| `founder-bandwidth-watchdog`` | **—** | Weekly |

---

# TIER 2 — CROSS-CUTTING SUB-FUNCTIONS (8)

## AI Ops → **Opsina**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## Compliance → **Compla**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## Knowledge Management → **Curatora**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## RevOps → **Revina**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## BizOps → **Bizina**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## Customer Success → **Churna**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## AI Safety → **Safina**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

## Procurement → **Procin**

- **Owner dept**: ?
- **Status**: ?
- **Promotion trigger**: ?

---

# TIER 3 — DEFERRED DEPARTMENTS (17)

## Customer Success (absorbed in Sales) → **Churna**

- **Promotion trigger**: 5+ recurring clients
- **Roles**: CSM Lead, Onboarding Specialist, Account Manager, Renewals Manager, Customer Education, Support Engineer
- **Agent candidates**: `customer-health-scorer` (already in plan as Tier 2)

## Marketing (independent) (absorbed in Sales) → **—**

- **Promotion trigger**: >$2K/mo marketing budget OR 10+ clients
- **Roles**: Brand Manager, SEO Specialist, Email Marketing Specialist, Paid Ads Specialist (TRADEMARK-BANNED), Social Media Manager (TRADEMARK-RESTRICTED), Community Manager, Event Coordinator, Partnerships Manager
- **Agent candidates**: `marketing-content-producer`, `multimedia-producer` (already Tier 2)

## Procurement (independent) (absorbed in Finance) → **—**

- **Promotion trigger**: Active vendors > 10 OR SaaS spend > $1K/mo
- **Roles**: Procurement Manager, Vendor Manager, Contract Negotiator, Renewal Specialist
- **Agent candidates**: `procurement-tracker` (already Tier 2)

## Compliance (standalone) (currently Ivan wearing hat) → **—**

- **Promotion trigger**: First EU client OR $50K MRR
- **Roles**: Compliance Officer (currently Ivan), Privacy Counsel/DPO, Regulatory Affairs Specialist
- **Agent candidates**: `compliance-monitor` (currently Tier 2, promotes to Tier 3 lead)

## Investor Relations → **Investia**

- **Promotion trigger**: First external investor
- **Roles**: IR Manager, Fundraising Lead, Board Liaison
- **Agent candidates**: `ir-monitor` (tracks cap table, runway, deck status)

## Chief of Staff → **COS**

- **Promotion trigger**: Ivan coord hours > 50/week
- **Roles**: Chief of Staff, Executive Assistant, Board Prep Specialist
- **Agent candidates**: `executive-brief-generator` (auto-generates board updates)

## Treasury → **Treasuria**

- **Promotion trigger**: $100K+ cash OR debt instruments
- **Roles**: Treasurer, Banking Specialist, FX Manager, Investment Manager
- **Agent candidates**: `treasury-monitor` (tracks cash, FX exposure, runway scenarios)

## Internal Audit → **Auditia**

- **Promotion trigger**: $1M+ revenue
- **Roles**: Internal Audit Lead, Compliance Auditor, Risk Analyst
- **Agent candidates**: `audit-runner` (scheduled compliance + control checks)

## Trust & Safety → **Trustina**

- **Promotion trigger**: Ship consumer AI product
- **Roles**: T&S Lead, Content Moderator, Misuse Specialist, Policy Writer
- **Agent candidates**: `t-s-monitor` (scans for misuse patterns)

## DevRel → **Devrelia**

- **Promotion trigger**: ParaguAI Builder has public API
- **Roles**: DevRel Manager, Developer Advocate, Community Manager, Tech Writer
- **Agent candidates**: `devrel-content-producer`, `api-docs-monitor`

## Workplace Operations → **Workopia**

- **Promotion trigger**: Open physical office
- **Roles**: Workplace Manager, Office Coordinator, IT Support
- **Agent candidates**: `workplace-monitor` (sensor + access management)

## Fraud / Risk → **Frauda**

- **Promotion trigger**: $500K+ payment volume
- **Roles**: Fraud Analyst, Risk Manager, Chargeback Specialist
- **Agent candidates**: `fraud-detector` (analyzes transaction patterns)

## Compensation & Benefits → **Compina**

- **Promotion trigger**: First FTE hire
- **Roles**: Comp & Benefits Manager, Equity Specialist, Payroll Admin
- **Agent candidates**: `comp-monitor` (salary band tracking)

## People Operations (HR) → **Herina-II**

- **Promotion trigger**: 5+ FTEs
- **Roles**: People Ops Partner, HR Generalist, Benefits Admin
- **Agent candidates**: `people-ops` (onboarding workflow, benefits tracking)

## DEI / Belonging → **Diversina**

- **Promotion trigger**: 10+ employees (and values-aligned)
- **Roles**: DEI Specialist, ER Lead
- **Agent candidates**: (none — sensitive human work)

## Public Relations → **Publicina**

- **Promotion trigger**: Launch flagship brand OR media interest
- **Roles**: PR Manager, Media Liaison, Spokesperson
- **Agent candidates**: `press-monitor` (tracks media mentions)

## Government Relations → **Goverina**

- **Promotion trigger**: Regulated vertical
- **Roles**: GovRel Manager, Lobbyist, Compliance Liaison
- **Agent candidates**: `regulatory-monitor` (gov announcement watch)

---

# TIER 4 — ENTERPRISE SCALE DEPARTMENTS (5)

## Internal Communications → **Comina**

- **Promotion trigger**: 50+ people
- **Roles**: Internal Comms Manager, Newsletter Editor

## M&A / Corp Dev → **Mandina**

- **Promotion trigger**: Acquisitions planned
- **Roles**: Corp Dev Lead, M&A Analyst

## Chief Data Officer (CDO) → **Dataia**

- **Promotion trigger**: Data-driven product
- **Roles**: CDO, Data Strategy Lead

## Chief AI Officer (CAIO) → **AIia**

- **Promotion trigger**: Enterprise AI (per Futureproofing.dev 2026)
- **Roles**: CAIO, AI Strategy Lead

## Diversity & Inclusion Lead → **Diversia**

- **Promotion trigger**: 25+ employees (and values-aligned)

---

# V1-LEGACY ACTIVE AGENTS (30 with outbox content)

These v1 agents have active cron jobs (outbox/). They're also listed under Tier 1 depts above; this is a consolidated view.

| Formal name | Portmanteau | Dept | Owner | Schedule | Outbox |
|---|---|---|---|---|---|
| `board-of-directors` | **Boardina** | 01 Operations | ivan | 0 14 1 */3 * | 2 |
| `business-analyst` | **Analisa** | 01 Operations | — | ? | 4 |
| `management-coordinator` | **Coordina** | 01 Operations | — | ? | 2 |
| `finance-controller` | **Finus** | 02 Finance & Legal | — | ? | 4 |
| `lead-enrichment` | **Prospia** | 03 Sales & Growth | — | ? | 1 |
| `multimedia-producer` | **Media** | 03 Sales & Growth | — | ? | 2 |
| `sales-pipeline` | **Saleina** | 03 Sales & Growth | — | ? | 7 |
| `ai-safety-engineer-30min` | **Safina-30** | 04 Engineering & Delivery | — | ? | 108 |
| `devops-monitor-30min` | **Devor-30** | 04 Engineering & Delivery | erebus | */30 * * * * | 104 |
| `engineering-roster` | **Devin** | 04 Engineering & Delivery | — | ? | 3 |
| `qa-automation-runner` | **Qualis** | 04 Engineering & Delivery | — | ? | 1 |
| `security-watchdog-30min` | **Securia-30** | 04 Engineering & Delivery | — | ? | 8 |
| `citation-checker` | **Citia** | 05 Research & Education | — | ? | 2 |
| `research-tracker` | **Researcha** | 05 Research & Education | — | ? | 3 |
| `thesis-tracker` | **Thesis** | 05 Research & Education | — | ? | 2 |
| `coach-cohort-facilitator` | **—** | 06 People & Culture | erebus | weekly (per cohort) | 1 |
| `coach-conversion-agent` | **Coachin** | 06 People & Culture | erebus | on-demand (after each free quick-win session) | 3 |
| `coach-ivan` | **Coachis** | 06 People & Culture | ivan | 0 21 * * 0 | 1 |
| `coach-kiki` | **Coachita** | 06 People & Culture | erebus | 0 21 * * 5 | 1 |
| `coach-lead-agents` | **Lidera** | 06 People & Culture | erebus | 0 22 1 * * | 1 |
| `coach-lead-finder` | **Leadius** | 06 People & Culture | erebus | weekly (Wednesday) | 1 |
| `coach-onboarding` | **Onboardia** | 06 People & Culture | erebus | triggered on new customer signup (via webhook from CF Worker) | 2 |
| `coach-org` | **Organis** | 06 People & Culture | erebus | 0 0 1 1,4,7,10 * | 1 |
| `coach-practitioner` | **Practis** | 06 People & Culture | erebus | on-demand (triggered per session) | 1 |
| `coach-renewal-manager` | **Renovin** | 06 People & Culture | erebus | monthly (1st of month, 09:00 UTC) | 1 |
| `coach-roi-tracker` | **Roina** | 06 People & Culture | erebus | weekly (Friday) | 1 |
| `coaching-content-curator` | **Contentis** | 06 People & Culture | erebus | 0 14 * * 1 | 1 |
| `coaching-quality-reviewer` | **Qualireva** | 06 People & Culture | erebus | */30 * * * * | 99 |
| `coaching-research-intelligence` | **Cochis** | 06 People & Culture | erebus | 0 13 * * 3 | 1 |
| `people-hr` | **Herina** | 06 People & Culture | ivan | 0 22 * * 1 | 1 |

---

# FINAL STATS

- **Tier 1**: 6 depts, 84 roles, 29 sub-agents
- **Tier 2**: 8 concerns, 0 roles, 0 sub-agents
- **Tier 3**: 17 depts (deferred)
- **Tier 4**: 5 depts (deferred)
- **v1-legacy active**: 30 agents (with outbox content)

**Grand total**: 36 functional areas (6 + 8 + 17 + 5 = 36 — slightly more than 31 because the playbook counts some items twice)

**Agent names**: every agent has a portmanteau name from `/opt/data/scratchpad/analysis/AGENT-NAMES-V2.json` (54 names, all unique)
**Reference**: `/opt/data/scratchpad/analysis/AGENT-NAMES-V2.md` (full reference)
