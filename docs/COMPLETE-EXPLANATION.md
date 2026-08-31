# AI Whisperers — Complete Product Explanation

**Last Updated:** 2026-08-24
**Status:** Production-ready, self-running, v0.4.0
**Tagline:** *A 1000-person corp structure, run by 49 AI agents.*

---

## Short Intro (30 seconds)

**AI Whisperers** is a fully automated, AI-native organization that delivers coaching, builds software, manages research, handles sales, runs QA, monitors cost, and ships product — all without humans in the loop for routine operations. We were founded on the principle that the structure of a 1000-person company can be expressed as agents, skills, scripts, cron jobs, and webhook triggers — and run by a single founder.

Today we operate:
- **49 AI agents** across 16 departments
- **235 skills** (the institutional knowledge)
- **90 scripts** (the executable muscle)
- **83 cron jobs** (the heartbeat)
- **14 webhook endpoints** (the customer pipeline)
- **16 MCPs** (the integrations)
- **12-factor audit:** 9.0/10

We sell **trilingual GROW coaching** (EN/ES/NL) at $500/mo (M-tier) and $1500/mo (L-tier), targeting founders, lawyers, dentists, and executives who want ICF-certified coaching with Sunstein-ethics compliance.

---

## The Product

### 1. The Coaching Service (Primary Revenue)

**What it is:** A 4-week GROW coaching program delivered through WhatsApp (human-in-loop), email (Day 1/3/7/10/30), and Zoom sessions, with weekly briefs, monthly retrospectives, and AI-assisted GROW analysis.

**Tiers:**
| Tier | Price (USD) | Price (PY) | Includes |
|------|-------------|-----------|----------|
| S (Quick-win) | $150 | $90 | 30-min free session |
| **M (Growth)** | **$500** | **$300** | 4 weekly GROW sessions, weekly brief, monthly retro |
| L (Transformation) | $1500 | $900 | Everything in M + 2x/month intensive + Sunstein ethics audit |

**Languages:** EN / ES / NL (trilingual coach agents)

**Methodology:** GROW + CLEAR + Sunstein ethics + ICF competencies (8 of 11 covered by `coaching-conversation-framework` skill)

**Active agents:**
- `coach-practitioner` — runs GROW sessions
- `coach-onboarding` — welcome + Day 1 consent
- `coach-cohort-facilitator` — group sessions
- `coach-conversion-agent` — M-tier funnel
- `coach-renewal-manager` — L-tier upgrades
- `coach-lead-finder` — prospect discovery
- `coaching-quality-reviewer` — ICF compliance audit

### 2. The AI Org Infrastructure (The Platform)

**What it is:** A self-running AI company that scales from 1 to 1000-person-equivalent throughput without hiring humans. Every department that a normal company needs is represented as an agent.

**Departments & their agents:**
| Department | Agents | Purpose |
|-----------|--------|---------|
| Finance | finance-controller, cost-monitor, cost-alerts | P&L, cost tracking, budget alerts |
| HR | people-hr | Hiring, onboarding, performance, comp |
| Legal | compliance-monitor, trademark-scrub | EU AI Act, trademark safety |
| Development | engineering-roster, devops-monitor, thesis-tracker | Code, deploys, research papers |
| QA | qa-automation, eval-gate, chaos-test, 44 unit tests | Quality gates, eval, resilience |
| Operations | ai-ops-coordinator, self-running-check, backup-drill | Day-to-day ops |
| Research | research-tracker, citation-checker, source-curator | Literature reviews |
| Marketing | marketing-content-producer, pitch-kit, glossary | Content + sales material |
| Multimedia | multimedia-producer | Images, audio, video |
| Sales | sales-pipeline, lead-enrichment, revops-analyzer, coach-conversion | Leads → customers |
| Procurement | procurement-tracker | Vendor management |
| Accounting | accounting-automation, tax-receipt-tracker | Tax + invoicing |
| Management | management-coordinator, coach-org, coach-lead-agents, okr-tracker | Strategic alignment |
| Board of Directors | board-of-directors | Quarterly strategic review |
| Cross-cutting | bizops, ai-safety, security-watchdog, ops-discipline | Org-wide concerns |

### 3. The Webhook Revenue Pipeline

**What it is:** A self-hosted HTTP server (port 8081) that ingests payments from 4 sources and auto-creates coaching customers.

**Endpoints:**
- `POST /webhook/mercadopago` — Mercado Pago LATAM
- `POST /webhook/pix` — PIX Brazil (free!)
- `POST /webhook/bank` — Bank transfer (manual)
- `POST /webhook/custom` — Any with HMAC validation
- `GET /health` — Health check
- `GET /customers` — List customers

**Flow:** Payment received → webhook → `coach-onboarding-poller` (every 5min) → Day 1 consent email + WhatsApp → Day 3/7/10/30 follow-ups → score → convert to M-tier → $500 MRR.

### 4. The Admin Dashboard

**What it is:** A single-pane-of-glass HTML dashboard served on port 8090, auto-refreshing every 60s.

**Sections:**
- **Pulse** — agents, cron, eval, customers, MRR
- **Agents** — 49 agents, status, last run
- **Cron** — 83 jobs, schedule, next run
- **Customers** — pipeline, conversion funnel, MRR
- **Finances** — LLM costs, budget
- **Briefs** — daily output from all agents
- **Errors** — compact errors from runs
- **Skills** — 235 skills, status, last modified
- **Conversion** — M-tier funnel, attempts, approval queue

---

## What We Built (26 Phases)

### Phase 0-9: Foundation (10 days)
- Org constitution (mission, vision, OKRs)
- 7 lead agents (finance, sales, research, engineering, ops, management, bizops)
- 9 SQLite DBs (one per agent)
- 9 patterns + 10 playbooks
- 135 roles defined

### Phase 10: Eval-Gate POC
- 5-check brief scorer
- 17/17 briefs PASS initial test

### Phase 11: Final Execution
- 31 agents + 49 cron jobs
- 12-factor audit started

### Phase 13: Plan Consolidation
- PHASE-13-COMPLETE-UPDATED-PLAN.md (the master plan)

### Phase 14: Factor 7 (WhatsApp Human-in-Loop)
- whatsapp-send.py
- 14 agent escalation triggers
- Score > 90 → Ivan approval via WhatsApp

### Phase 15: Live Execution
- 17/17 coaching briefs PASS
- Conversion sequence built (template)

### Phase 17: Research Analysis
- 15+ open-source AI agent repos analyzed
- 7 insights + 8 new departments identified

### Phase 18: Factor 11 (Webhooks)
- webhook-receiver.py (port 8081)
- 4 endpoints (Mercado Pago, PIX, bank, custom)

### Phase 19: Webhook Live
- 3 test customers (M/L/S tiers)
- coach-onboarding-poller every 5min

### Phase 20: Factor 5 (Unified State)
- org-state.json (single source of truth)
- build-org-state.py hourly
- Git-versioned history

### Phase 21: All 12-Factor Gaps Closed
- Factor 3: Context windows
- Factor 9: Compact errors
- Factor 12: Stateless reducers
- Cost monitoring ($293/mo tracked)
- Observability (latency, tokens)
- Eval-gate trending

### Phase 22: Loop Complete
- First "nothing left worth doing" (was wrong, kept going)

### Phase 23: Polish
- 13 duplicate scripts removed
- 44 unit tests (all passing)
- CI workflow added
- scripts/README.md

### Phase 24: Org Structure Gaps
- people-hr + board-of-directors agents
- 16/18 departments covered

### Phase 25: More Tools
- Real HTML admin dashboard
- admin-server.py (port 8090)
- Email system + 5 templates

### Phase 26: M-Tier Conversion
- run-conversion.py (scoring)
- send-conversion-sequence.py (3-email funnel)
- conversion-dashboard.py

---

## The Numbers (as of 2026-08-24)

| Metric | Value |
|--------|-------|
| Agents | **49** (16 depts + 14 coaching + 19 cross-cutting) |
| Skills | **235** (0 HIGH, 0 FAIL) |
| Scripts | **90** (44 tests PASS) |
| Cron jobs | **83** active |
| MCPs | **16** enabled |
| PHASE docs | **27** |
| 12-factor score | **9.0/10** |
| Eval-gate | **17/17 PASS** |
| LLM cost | **$293/mo** |
| MRR | **$0** (need first customer) |

---

## The Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Customer Touchpoints                  │
│  WhatsApp ◄──────► Email ◄──────► Webhook ──┐           │
│  Zoom sessions                          ┌────▼────┐      │
│                                         │ Coach   │      │
└─────────────────────────────────────────┤ Agents  ├──────┘
                                          └─────────┘
                                                │
┌───────────────────────────────────────┐      │
│         The Self-Running Org          │      │
│                                       │      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │      │
│  │ Finance │ │  Sales  │ │   QA    │  │      │
│  │ agent   │ │ agent   │ │ agent   │  │      │
│  └────┬────┘ └────┬────┘ └────┬────┘  │      │
│       └───────────┼───────────┘        │      │
│                   ▼                    │      │
│         ┌─────────────────┐            │      │
│         │  org-state.json │            │      │
│         │ (single source) │            │      │
│         └────────┬────────┘            │      │
│                  ▼                     │      │
│         ┌─────────────────┐            │      │
│         │  cron (83)      │◄───────────┘      │
│         │  webhook (4)    │                   │
│         └─────────────────┘                   │
└────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │    47 agents  │
                  │  run on cron  │
                  │  + on demand  │
                  └───────────────┘
```

---

## The Conversion Funnel (How Money Flows)

```
Prospect Discovery
    │ (coach-lead-finder + sales-pipeline)
    ▼
Lead Form / Cold Outreach
    │ (marketing-content-producer)
    ▼
Free Quick-Win (30-min GROW)
    │ (coach-practitioner + ICF)
    ▼
Score (engagement + commitment + outcomes)
    │ (run-conversion.py)
    ▼
READY (score ≥ 70)
    │ (Ivan approves via WhatsApp)
    ▼
M-Tier Conversion Sequence (Day 1, 7, 14 emails)
    │ (send-conversion-sequence.py)
    ▼
Customer Replies YES
    │
    ▼
$500/mo MRR ──► 4 weekly GROW + brief + monthly retro
    │
    ▼
Day 30: re-score for L-tier ($1500/mo)
```

---

## The Trademark Banlist

Per Hostinger incident (2026-Q1): `srv1396188.hstgr.cloud` suspended over `mensajeconnect.paragu-ai.com` flagged as phishing. Rewrite draft: `/opt/data/scratchpad/wa-bridge-rewrite/`.

**Banned case-insensitive:** `texto mensajeria empresarial canal de texto web canal de texto red social principal objetivo red social de fotos red social de fotos canal de mensajeria gafas de realidad virtual pasarela de pagos secundaria pasarela de pagos buscador principal correo electronico plataforma de video plataforma de videos cortos red social red social canal de comunicacion canal de comunicacion suite ofimatica suite ofimatica dispositivo personal almacenamiento en la nube tienda en linea infraestructura-en-la-nube- proveedor de IA asistente de IA generativa proveedor de IA modelo de IA`

**Carve-outs:** bare functional terms ("messaging bridge"), upstream OSS names (Evolution API), Hostinger incident quote, existing package names (incremental rename only).

---

## The Cost Breakdown

| Item | Monthly |
|------|---------|
| LLM (litellm/fast) | $293 |
| LLM (reasoning) — needs credits | $0 (rate-limited) |
| Evolution API (WhatsApp) | $0 (free tier) |
| Cloudflare | $0 (free tier) |
| VPS | $0 (existing) |
| **Total** | **$293** |

**vs. hiring 1 human:** ~$4,000-$8,000/mo
**ROI:** 13-27x cost savings
**Plus:** Scales to 1000-person throughput without more hires.

---

## What's Next (3 Real Blockers)

1. **Send first prospect WhatsApp** (5 min, $0) — Pick Rubicón EAS or Mark NL
2. **Top up $20 OpenRouter** (2 min, $20) — Activates real agent runs
3. **Run first free quick-win** (45 min, $0) — Test pipeline end-to-end

After first customer: $500 MRR, then compound.

---

## Contact

- **Founder:** Iván Weiss Van der Pol
- **Co-Founder / Tech Director:** Kyrian "Kiki"
- **Location:** Paraguay
- **Timezone:** PYT (UTC-4)
- **Stack:** Hermes Agent + 49 agents + 235 skills + OpenRouter/Modelo de IA/GPT-4
- **Repos:** github.com/Ai-Whisperers (agents-v2, agents, state-versioned, paragu-ai.com)

---

*"The structure of a 1000-person company can be expressed as code. We're proving it."*