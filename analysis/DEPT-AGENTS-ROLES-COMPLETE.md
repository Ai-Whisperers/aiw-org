# AIW Agent Roster — DEMIURGE is Source of Truth

> **Last updated**: 2026-08-31 (after DEMIURGE branch audit)
> **Source of truth**: `github.com/Ai-Whisperers/growth-coaching` branch `epic/DEMIURGE`
> **Canonical reference**: `demiurge/agents/README.md` (24 DEMIURGE agents) + constitution charters (heritage agents)

## Naming convention

Every DEMIURGE agent has a **single Greek-mythology name** (Apollo, Hera, Thoth, etc.).
These names ARE the agent identity — there is no second portmanteau name, no Spanish-surname variant, no human-name alias.
Heritage agents (from the v0.2.0/v0.3.0 constitution) keep their formal names until they migrate to DEMIURGE.

**Rule**: One name per agent. No duplicates. No aliases. If you find two names for one agent, that's a bug to fix.

---

# DEMIURGE Agents — Active (24)

These agents have full PROMPT.md, agent.yaml, and repo-manifest.yaml in the DEMIURGE branch.
Each runs as a standalone repo under `Ai-Whisperers/aiw-agent-<id>`.

## Marketing

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Calliope** | `calliope-content-producer` | 0 10 * * 1,3,5 | ivan | You are **Calliope**, muse of content. You produce blog posts, social drafts, and email copy from Hera's briefs. |
| **Hera** | `hera-marketing-lead` | 0 9 * * 1,3,5 | ivan | You are **Hera**, strategist of demand. You own marketing direction, campaign briefs, and the bridge from Product Discovery insights to Sale |
| **Iris** | `iris-community-monitor` | 0 11 * * 2,4 | ivan | You are **Iris**, rainbow bridge to the audience. You monitor community channels and surface engagement opportunities to Hera. |

## Sales

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Apollo** | `apollo-sales-lead` | 0 12 * * * | ivan | You are **Apollo**, bringer of clarity in the pipeline. You triage inbound leads, run discovery (SPIN/MEDDIC), and coordinate Cadmus and Met |
| **Cadmus** | `cadmus-lead-enrichment` | manual | ivan | You enrich inbound leads with ICP scoring and intent signals. Route summary to Apollo within same signal batch. |
| **Metis** | `metis-proposal-drafter` | manual | ivan | You draft proposals after discovery. Human approval required before send. |

## Product Discovery

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Athena** | `athena-product-discovery-lead` | 0 8 * * 1 | ivan | You synthesize customer evidence into validated insights. Continuous discovery per Torres/Mom Test. |
| **Clio** | `clio-customer-signal-collector` | 0 7 * * 1-5 | ivan | Collect raw customer signals from sessions, support, win/loss notes. Emit `customer-signal-raw` to Athena. |

## Operations

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **BizOps Tracker** | `bizops-tracker` | 0 17 * * 0 | ivan | You are **Erebus**, AI Whisperers' BizOps tracker. You track cross-functional metrics, OKRs, and executive decision support. |
| **Business Analyst** | `business-analyst` | 30 6 * * * | ivan | You are **Erebus**, AI Whisperers' business analyst. You produce a single one-page brief per day so Ivan can answer in 30 seconds: **"Are we |
| **Kronos** | `kronos-operations-lead` | 0 7 * * 1-5 | ivan | You are **Kronos**, keeper of operational order. You own OKR tracking, incident triage, cross-dept coordination, vendor hygiene, and cost co |
| **Mgmt Coordinator** | `management-coordinator` | 0 17 * * 1,4 | ivan | You are **Erebus**, AI Whisperers' ops coordinator. Twice a week you surface what's open, what's blocked, and what Ivan or Kyrian should pic |

## AI Ops

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **AI Ops Coordinator** | `ai-ops-coordinator` | 0 9 * * * | kiki | You are **Erebus**, AI Whisperers' AI Ops coordinator. You monitor the agent layer itself — eval gates, hard stops, drift detection, golden  |

## Compliance

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Compliance Monitor** | `compliance-monitor` | 0 8 * * 1 | ivan | You are **Erebus**, AI Whisperers' compliance monitor. You watch for regulatory changes (EU AI Act, GDPR, LGPD), trademark issues, and PII h |

## Router

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Hermes** | `hermes-router-revenue` | */15 6-22 * * * | ivan | You route signals across Marketing, Sales, Product Discovery, and Operations. Enforce dispatch rules, timing SLAs, and quorum. |

## Monitor

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Argus** | `argus-health-monitor` | 0 */6 * * * | ivan | You watch KPIs and agent cadences for the revenue stack. Fire feedback loops when thresholds breach. |

## Knowledge Management

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Hephaestus** | `hephaestus-document-miner` | on_signal | ivan | You are **Hephaestus**, forger of structured value from raw material. You extract action items, decisions, nuggets, references, and terminol |
| **Mnemosyne** | `mnemosyne-document-archivist` | on_signal | ivan | You are **Mnemosyne**, mother of memory. You maintain the org's document catalog — not passive storage, but active indexing, tagging, and re |
| **Orpheus** | `orpheus-recordings-agent` | on_signal | ivan | You are **Orpheus**, master of voice and song. You ingest audio/video recordings, transcribe them, and hand structured transcripts into the  |
| **Peitho** | `peitho-language-quality` | on_signal | ivan | You are **Peitho**, goddess of persuasion and eloquence. You assess document quality — spelling, grammar, tone, terminology compliance, clar |
| **Pheme** | `pheme-document-router` | */5 6-22 * * * | ivan | You are **Pheme**, voice of rumour and fame. You deliver classified documents and mined assets to the right agents and departments — replaci |
| **Themis** | `themis-document-classifier` | on_signal | ivan | You are **Themis**, goddess of divine order. You read every ingested document and assign structured attributes so downstream agents route, c |

## Cross-cutting (knowledge discovery)

| Name | ID | Schedule | Owner | Mission |
|---|---|---|---|---|
| **Echo** | `echo-community-scanner` | 0 7 * * 3  # Wed 07:00 PYT | ivan | You are **Echo**, listener of the swarm. You scan practitioner communities for emerging tactics, anti-patterns, and language shifts. |
| **Thoth** | `thoth-literature-scanner` | 0 6 * * 1  # Mon 06:00 PYT | ivan | You are **Thoth**, curator of knowledge. You scan authoritative literature and update department source catalogs with quality-rated entries  |

---

# Heritage Agents — Awaiting DEMIURGE Migration (~23)

These agents exist in the constitution (`agents-v2/constitution/01-06-*.md`) and the legacy `agents/` repo.
They use the portmanteau naming framework (Saleina, Devin, Finus, etc.) for now.
**Migration path**: when a dept gets built to DEMIURGE standard, these get renamed to Greek-mythology names.

| Department | Formal name | Portmanteau | Mission |
|---|---|---|---|

### Engineering & Delivery

| engineering-roster | **Devin** | Twice-weekly visibility into production health + Kiki's bandwidth |
| devops-monitor | **Devor** | Detect infrastructure anomalies. Surface to engineering-roster. |
| qa-automation-runner | **Qualis** | Run all tests on every PR. Comment results. Block merge if coverage drops. |
| security-watchdog | **Securia** | Detect security threats before they become incidents. |
| ai-safety-engineer | **Safina** | Prevent Kiro-class incidents |
| scope-intake | **Scopia** | Scope before contract signed |
| delivery-tracker | **Deliva** | Make Kiki's bandwidth visible to sales before commitments |
| feasibility-gate | **Gatina** | Stop the org from overpromising |
| chaos-test-runner | **Chaosia** | Weekly chaos testing |

### Finance & Legal

| finance-controller | **Finus** | Weekly end-of-week close |
| accounting-automation | **Bokina** | Daily expense categorization |
| tax-receipt-tracker | **Taxina** | Weekly receipt capture |
| procurement-tracker | **Procin** | Weekly vendor renewal alerts |

### Research & Education

| research-tracker | **Researcha** | Weekly thesis + publications visibility |
| thesis-tracker | **Thesis** | Advance thesis by 1 task/day |
| citation-checker | **Citia** | Zero hallucinated citations |
| course-producer | **Coursia** | 1 module/week |
| okr-tracker | **Metrika** | Weekly OKR progress |
| funding-coordinator | **Fundina** | 15+ funding apps by Nov 12 |
| source-curator | **Curatora** | Source-material freshness sweep |

### People & Culture

| kiki-coach | **Magistra** | Deliver one concrete skill per week |
| founder-bandwidth-watchdog | **Vigilis** | Burnout detection |

---

# Tier 2 Cross-cutting Concerns (8)

These touch every department as sub-functions of existing Tier-1 depts. Promote to standalone when triggers fire.

| Concern | Portmanteau | Owner dept | Status | Promotion trigger |
|---|---|---|---|---|
| AI Ops | **Opsina** | Engineering (Kiki) | T1 active | Always |
| Compliance | **Compla** | Finance (Ivan wearing hat) | T1 vacant | First EU client OR $50K MRR |
| Knowledge Management | **Curatora** | Research | T2 next | >100 source-material files OR 2nd knowledge-heavy vertical |
| RevOps | **Revina** | Sales | T2 next | 5+ closed deals/quarter |
| BizOps | **Bizina** | Operations | T2 next | When OKRs formalized |
| Customer Success | **Churna** | Sales | T3 deferred | 5+ clients |
| AI Safety | **Safina** | Engineering | T1 active | Already promoted (heritage) |
| Procurement | **Procin** | Finance | T2 next | Vendor count > 10 |

---

# Tier 3 — Deferred Departments (17)

| Department | Portmanteau | Promotion trigger |
|---|---|---|
| Customer Success | **Churna** | 5+ recurring clients |
| Marketing (independent) | **Markina-II** | >$2K/mo marketing budget OR 10+ clients |
| Procurement (independent) | **Procin** | Active vendors > 10 OR SaaS spend > $1K/mo |
| Compliance (standalone) | **Compla** | First EU client OR $50K MRR (HARD-STOP) |
| Investor Relations | **Investia** | First external investor |
| Chief of Staff | **COS** | Ivan coord hours > 50/week |
| Treasury | **Treasuria** | $100K+ cash OR debt instruments |
| Internal Audit | **Auditia** | $1M+ revenue |
| Trust & Safety | **Trustina** | Ship consumer AI product |
| DevRel | **Devrelia** | ParaguAI Builder has public API |
| Workplace Operations | **Workopia** | Open physical office |
| Fraud / Risk | **Frauda** | $500K+ payment volume |
| Compensation & Benefits | **Compina** | 10+ employees |
| People Operations (HR) | **Herina-II** | First FTE hire |
| DEI / Belonging | **Diversina** | 10+ employees |
| Public Relations | **Publicina** | Launch flagship brand |
| Government Relations | **Goverina** | Regulated vertical |

# Tier 4 — Enterprise Scale (5)

| Department | Portmanteau | Promotion trigger |
|---|---|---|
| Internal Communications | **Comina** | 50+ people |
| M&A / Corp Dev | **Mandina** | Acquisitions planned |
| Chief Data Officer (CDO) | **Dataia** | Data-driven product |
| Chief AI Officer (CAIO) | **AIia** | Enterprise AI |
| Diversity & Inclusion Lead | **Diversia** | 25+ employees |

---

# Final Stats

- **DEMIURGE active**: 24 agents (canonical, Greek-mythology names)
- **Heritage agents**: 23 agents (constitution v0.2.0/v0.3.0, portmanteau names)
- **Total shipped**: 47 agents
- **Tier 2 cross-cutting**: 8 concerns
- **Tier 3 deferred**: 17 depts
- **Tier 4 enterprise**: 5 depts
- **Total functional areas**: 31 + 8 Tier 2 = **39**
- **Total roles**: 84 (Tier 1) + 36 (Tier 2) + 17 (Tier 3) + 5 (Tier 4) = **142**

## Demotions and replacements (cleanup)

**DEMIURGE replaces**: the portmanteau framework (`/opt/data/scratchpad/analysis/AGENT-NAMES-V2.md`) for the 24 agents that have DEMIURGE equivalents. The portmanteau framework stays as the **legacy naming layer** for heritage agents awaiting migration.

**Examples of replacements** (DEMIURGE → portmanteau legacy):

| DEMIURGE (canonical) | Portmanteau (legacy) | Function |
|---|---|---|
| **Apollo** | Saleina | sales-pipeline (lead) |
| **Cadmus** | Prospia | lead-enrichment |
| **Metis** | Proporina | proposal-drafter |
| **Hera** | Markina | marketing lead |
| **Calliope** | Contentis | content producer |
| **Iris** | (none) | community monitor |
| **Athena** | (none) | product discovery lead |
| **Clio** | (none) | customer signal collector |
| **Kronos** | (none) | operations lead |
| **Thoth** | (none) | literature scanner |
| **Echo** | (none) | community scanner |
| **Hermes** | (none) | revenue router |
| **Argus** | (none) | health monitor |
| **Themis** | (none) | document classifier |
| **Mnemosyne** | (none) | document archivist |
| **Hephaestus** | (none) | document miner |
| **Pheme** | (none) | document router |
| **Peitho** | (none) | language quality |
| **Orpheus** | (none) | recordings |
| **Kronos** (replacement) | Coordina | operations coordinator |

Heritage agents that don't have DEMIURGE replacements yet:

| Portmanteau | Formal | Function |
|---|---|---|
| Devin | engineering-roster | Engineering lead |
| Devor | devops-monitor | DevOps |
| Qualis | qa-automation-runner | QA |
| Securia | security-watchdog | Security |
| Safina | ai-safety-engineer | AI Safety |
| Scopia | scope-intake | Scope intake |
| Deliva | delivery-tracker | Delivery tracking |
| Gatina | feasibility-gate | Feasibility gate |
| Chaosia | chaos-test-runner | Chaos testing |
| Finus | finance-controller | Finance lead |
| Bokina | accounting-automation | Accounting |
| Taxina | tax-receipt-tracker | Tax |
| Procin | procurement-tracker | Procurement |
| Magistra | kiki-coach | Coaching |
| Vigilis | founder-bandwidth-watchdog | Burnout detection |
| Researcha | research-tracker | Research lead |
| Thesis | thesis-tracker | Thesis |
| Citia | citation-checker | Citations |
| Coursia | course-producer | Courses |
| Metrika | okr-tracker | OKRs |
| Fundina | funding-coordinator | Funding |
| Curatora | source-curator | Sources |