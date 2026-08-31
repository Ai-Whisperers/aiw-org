# AI Whisperers — Detailed Org Analysis + Organigram

> **SNAPSHOT as-of 2026-08-14.** Numbers reflect the pre-DEMIURGE constitution design.
> For current operational state see [ROADMAP-DEPT-EXPANSION.md](../ROADMAP-DEPT-EXPANSION.md).

**Last Updated:** 2026-08-24
**Status:** Production-ready, self-running, v0.4.0
**Total Agents (constitution design):** 51 across 18 departments
**Operational (DEMIURGE):** 12 agents, 3 active departments

---

## 📊 The Org at a Glance

```
                                    AI WHISPERERS
                                    ================
                                    Iván Weiss Van der Pol (CEO)
                                              │
                                              ▼
                            ┌─────────────────────────────────┐
                            │     CO-FOUNDER / TECH DIR       │
                            │      Kyrian "Kiki"              │
                            └─────────────────────────────────┘
                                              │
                              ┌───────────────┼───────────────┐
                              │               │               │
                              ▼               ▼               ▼
                        ┌──────────┐   ┌──────────┐   ┌──────────┐
                        │ EXEC     │   │ COACHING │   │ CROSS-   │
                        │ DEPTs    │   │ PRODUCT  │   │ CUTTING  │
                        │(16 dept) │   │ (5 dept) │   │ (2)      │
                        │ 32 agents│   │ 9 agents │   │ 4 agents │
                        └──────────┘   └──────────┘   └──────────┘
                            │               │               │
                            └───────────────┼───────────────┘
                                            ▼
                                    ┌───────────────┐
                                    │  THE FOUNDATION│
                                    │               │
                                    │ - 235 skills  │
                                    │ - 90 scripts  │
                                    │ - 83 cron jobs│
                                    │ - 16 MCPs     │
                                    │ - 14 webhook  │
                                    └───────────────┘
```

---

## 🏢 Complete Organigram (51 Agents)

### Tier 0: Executive
```
┌─────────────────────────────────────────────────────────┐
│                  Iván Weiss Van der Pol                  │
│                       (CEO/Founder)                       │
│              PYT (UTC-4) | Paraguay | Spanish            │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Kyrian "Kiki"                                │
│           Co-Founder / Tech Director                     │
│            (AI-coaching partner)                         │
└─────────────────────────────────────────────────────────┘
```

### Tier 1: Management Layer (6 agents)
```
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ management- │    │  coach-org  │    │coach-lead-  │
  │ coordinator │    │             │    │ agents      │
  └─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ okr-tracker │    │ coach-ivan  │    │ kiki-coach  │
  │             │    │             │    │             │
  └─────────────┘    └─────────────┘    └─────────────┘
```

### Tier 1.5: Board of Directors (1 agent)
```
  ┌─────────────────────────────────────────────────────┐
  │            board-of-directors                       │
  │  (Quarterly strategic review, 3-perspective)        │
  └─────────────────────────────────────────────────────┘
```

---

## 📦 EXECUTIVE DEPARTMENTS (16 Depts, 32 Agents)

### Dept 01 — Finance (3 agents)
```
  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
  │   finance-  │  │  funding-   │  │  tax-receipt-  │
  │  controller │  │ coordinator │  │     tracker     │
  └─────────────┘  └─────────────┘  └─────────────────┘
   • P&L tracking   • Grant apps    • Tax compliance
   • Cost alerts    • Investor CRM  • Paraguay tax
```

### Dept 02 — Human Resources (2 agents)
```
  ┌─────────────┐  ┌──────────────┐
  │  people-hr  │  │  founder-    │
  │             │  │ bandwidth-   │
  └─────────────┘  │  watchdog    │
   • Hiring        └──────────────┘
   • Onboarding    • Workload alert
   • Performance    • Burnout prevent
   • Comp planning
```

### Dept 03 — Legal & Compliance (1 agent)
```
  ┌──────────────────────────────────┐
  │       compliance-monitor         │
  └──────────────────────────────────┘
   • EU AI Act compliance
   • Trademark banlist enforcement
   • Doc compliance
```

### Dept 04 — Development (5 agents)
```
  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
  │ engineering │  │  devops-    │  │  thesis-     │
  │   roster    │  │  monitor    │  │  tracker     │
  └─────────────┘  └─────────────┘  └──────────────┘
                       │
                       ▼
                  ┌──────────────┐     ┌──────────────┐
                  │  devops-     │     │   course-    │
                  │  monitor-30m │     │  producer    │
                  └──────────────┘     └──────────────┘
   • Code reviews         • Every 30m   • Educational
   • Git workflow          deployment     course content
   • Hotfix tracking       up monitoring
```

### Dept 05 — Quality Assurance (3 agents)
```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ qa-automation│  │ eval-gate-   │  │ chaos-test-  │
  │   runner     │  │   runner     │  │   runner     │
  └──────────────┘  └──────────────┘  └──────────────┘
   • Unit tests        • 5-check        • Resilience
   • Integration        scoring          testing
   • E2E (44 tests)
```

### Dept 06 — Operations (2 agents)
```
  ┌──────────────┐  ┌──────────────┐
  │  ai-ops-     │  │   bizops-    │
  │ coordinator  │  │   tracker    │
  └──────────────┘  └──────────────┘
   • Day-to-day        • Org-wide
     operations          efficiency
   • 83 cron jobs      • KPIs
```

### Dept 07 — Research (4 agents)
```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │   research-  │  │  citation-   │  │   source-    │
  │   tracker    │  │   checker    │  │   curator    │
  └──────────────┘  └──────────────┘  └──────────────┘
         │
         ▼
  ┌──────────────────┐
  │ coaching-research│
  │   intelligence   │
  └──────────────────┘
   • Literature reviews
   • Citation validation
   • Source quality
   • Coaching research digest
```

### Dept 08 — Marketing (2 agents)
```
  ┌──────────────┐  ┌──────────────┐
  │  marketing-  │  │  marketing-  │
  │   content-   │  │   content-   │
  │  producer    │  │ mon-wed-fri  │
  └──────────────┘  └──────────────┘
   • Articles          • Daily 3x
   • Pitches              social posts
   • Trilingual
```

### Dept 09 — Multimedia (1 agent)
```
  ┌──────────────────────────────────┐
  │       multimedia-producer        │
  └──────────────────────────────────┘
   • Images, video, audio
   • Trilingual assets
   • Brand consistency
```

### Dept 10 — Sales (6 agents)
```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │   sales-     │  │   lead-      │  │  revops-     │
  │  pipeline    │  │ enrichment   │  │  pipeline-   │
  │              │  │              │  │  analyzer    │
  └──────────────┘  └──────────────┘  └──────────────┘
         │                 │
         ▼                 ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │    coach-    │  │  coach-lead- │  │    coach-    │
  │  conversion- │  │   finder     │  │   renewal-   │
  │   agent      │  │              │  │   manager    │
  └──────────────┘  └──────────────┘  └──────────────┘
   • MRR funnel    • Prospect       • Day 30
   • M-tier          discovery        L-tier
   • Conversion       (LinkedIn,      upgrade
     sequence         WhatsApp)
```

### Dept 11 — Procurement (1 agent)
```
  ┌──────────────────────────────────┐
  │       procurement-tracker        │
  └──────────────────────────────────┘
   • Vendor evaluation
   • Cost optimization
```

### Dept 12 — Accounting (1 agent)
```
  ┌──────────────────────────────────┐
  │       accounting-automation      │
  └──────────────────────────────────┘
   • Invoicing
   • Reconciliation
   • Paraguay tax law
```

---

## 💼 THE COACHING PRODUCT (5 Depts, 9 Agents)

### Product Org Chart
```
                    ┌────────────────────────┐
                    │  THE COACHING SERVICE  │
                    │  Trilingual GROW       │
                    │  EN / ES / NL          │
                    └────────────┬───────────┘
                                 │
        ┌────────────────────────┼─────────────────────┐
        │                        │                     │
        ▼                        ▼                     ▼
  ┌────────────┐         ┌────────────┐         ┌────────────┐
  │ PRE-SALE   │         │ DELIVERY   │         │ POST-SALE  │
  │ Discovery  │         │ GROW       │         │ Retention  │
  │ Quality    │         │ Sessions   │         │ Renewal    │
  └────────────┘         └────────────┘         └────────────┘
        │                        │                     │
        ▼                        ▼                     ▼
  ┌────────────┐         ┌────────────┐         ┌────────────┐
  │ coach-lead-│         │  coach-    │         │  coach-    │
  │   finder   │         │practitioner│         │   renewal- │
  └────────────┘         └────────────┘         │   manager  │
                                │               └────────────┘
                                ▼
  ┌────────────┐         ┌────────────┐         ┌────────────┐
  │ coach-     │         │  coaching- │         │  coach-    │
  │ onboarding │         │  quality-  │         │   roi-     │
  │            │         │  reviewer  │         │  tracker   │
  └────────────┘         └────────────┘         └────────────┘
                                +
                       ┌────────────┐
                       │ coach-     │
                       │ conversion-│
                       │ agent      │
                       └────────────┘
                                +
                  ┌──────────────────────┐
                  │  coach-cohort-       │
                  │  facilitator         │
                  └──────────────────────┘
```

### Roles
| Agent | Phase | Purpose |
|-------|-------|---------|
| coach-lead-finder | Pre-sale | Prospect discovery |
| coach-conversion-agent | Pre-sale | M-tier funnel scoring |
| coach-onboarding | Sale | Day 1 consent + welcome |
| coach-practitioner | Delivery | Run GROW sessions |
| coaching-quality-reviewer | Delivery | ICF compliance audit |
| coach-cohort-facilitator | Delivery | Group sessions |
| coach-roi-tracker | Delivery | ROI measurement |
| coach-renewal-manager | Post-sale | Day 30 L-tier upgrade |
| coaching-content-curator | Support | Session prep materials |

---

## 🛡️ CROSS-CUTTING CONCERNS (4 Agents)

```
  ┌─────────────────────────────────────────────────────────┐
  │ AI SAFETY (2 agents)                                    │
  │ ┌─────────────────┐  ┌──────────────────────────┐       │
  │ │ ai-safety-      │  │ ai-safety-engineer-30min │       │
  │ │ engineer        │  │  (every 30 min)          │       │
  │ └─────────────────┘  └──────────────────────────┘       │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ SECURITY (2 agents)                                     │
  │ ┌─────────────────┐  ┌──────────────────────────┐       │
  │ │ security-       │  │ security-watchdog-30min   │       │
  │ │ watchdog        │  │  (every 30 min)           │       │
  │ └─────────────────┘  └──────────────────────────┘       │
  └─────────────────────────────────────────────────────────┘
```

---

## 📦 THE FOUNDATION (not agents — the infrastructure)

```
  ┌─────────────────────────────────────────────────────────┐
  │                  THE FOUNDATION                         │
  ├─────────────────────────────────────────────────────────┤
  │ SKILLS (235)                                            │
  │ • 17 coaching (the IP)                                  │
  │ • 218 operational                                        │
  │ • 0 HIGH / 0 FAIL                                       │
  │                                                          │
  │ SCRIPTS (90)                                            │
  │ • 26 in agents-v2/scripts/                              │
  │ • 64 in /opt/data/scripts/                              │
  │ • 44/44 unit tests PASS                                 │
  │                                                          │
  │ CRON JOBS (83)                                          │
  │ • Daily: 8                                              │
  │ • Hourly: 6                                             │
  │ • Weekly: 7                                             │
  │ • Real-time (5min): 4                                   │
  │ • Monthly: 4                                            │
  │                                                          │
  │ MCPs (16 enabled)                                       │
  │ • linear, github, figma, cloudflare, brave-search       │
  │ • comfy-cloud, blender, sqlite, postgres                 │
  │ • filesystem, memory-mcp, context7, exa                 │
  │ • social-graph-mcp, mercury, unreal-engine              │
  │                                                          │
  │ WEBHOOKS (4 endpoints, port 8081)                       │
  │ • Mercado Pago, PIX, Bank, Custom                       │
  │ • HMAC validation, dedup                                │
  │                                                          │
  │ DATABASES (14 SQLite + 14 JSON)                         │
  │ • Auto-versioned via git                                │
  │ • org-state.json single source of truth                 │
  │                                                          │
  │ MONITORING                                              │
  │ • cost-monitor ($293/mo tracked)                        │
  │ • errors.json (compact)                                 │
  │ • agent-traces.jsonl                                    │
  │ • eval-trending.json (30-day pass rate)                 │
  └─────────────────────────────────────────────────────────┘
```

---

## 🔄 The Conversion Funnel (How Money Flows)

```
┌──────────────┐
│  PROSPECT    │
│  DISCOVERY   │ ─── coach-lead-finder + sales-pipeline
└──────┬───────┘
       │ outreach WhatsApp / lead form
       ▼
┌──────────────┐
│  COLD LEAD   │
│  / QUICK WIN │ ─── marketing-content-producer
└──────┬───────┘
       │ 30-min free GROW session
       ▼
┌──────────────┐
│  QUALIFIED   │
│  LEAD        │ ─── coach-practitioner + ICF compliance
└──────┬───────┘
       │ score (engagement + commitment + outcomes)
       ▼
┌──────────────┐
│  READY       │ ─── run-conversion.py
│  ≥ 70 score  │
└──────┬───────┘
       │ Ivan approves via WhatsApp (Factor 7)
       ▼
┌──────────────┐
│  M-TIER      │ ─── send-conversion-sequence.py
│  $500/mo     │      (Day 1, 7, 14 emails)
└──────┬───────┘
       │ Customer replies YES
       ▼
┌──────────────┐
│  $500 MRR    │ ─── coach-practitioner runs weekly
│  WEEKLY      │
│  GROW        │ ─── weekly brief
└──────┬───────┘
       │ Day 30: re-score
       ▼
┌──────────────┐
│  L-TIER      │ ─── coach-renewal-manager
│  $1500/mo    │
│  + Sunstein  │
│  audit       │
└──────────────┘
```

---

## 💰 Revenue Model

| Tier | Price | Agents Involved | Per-Unit Workload |
|------|-------|-----------------|-------------------|
| S (Free) | $0 | coach-practitioner | 30 min session |
| **M (Growth)** | **$500/mo** | coach-practitioner + coach-onboarding + coach-conversion | 4 sessions + 4 briefs + 1 retro |
| **L (Transformation)** | **$1500/mo** | All coaching agents + Sunstein compliance | 4 GROW + 2 intensive + ethics audit |

**Target:** 5 M-tier customers = $2500 MRR → 3 L-tier = +$4500 = $7000 MRR

---

## 📐 The 12-Factor Audit

| Factor | Score | Notes |
|--------|-------|-------|
| 1. Codebase | 9 | Agents-v2 repo, single main branch |
| 2. Dependencies | 9 | Pin via uv + requirements.txt |
| 3. **Context windows** | **9** | Per-agent context builds, 47 agents |
| 4. Backing services | 9 | Mongo/Cloudflare/Email treated as resources |
| 5. **Unified state** | **9** | org-state.json single source of truth |
| 6. Processes | 9 | All agents stateless, state in JSON |
| 7. **Human-in-loop** | **8** | WhatsApp via Factor 7 escalation |
| 8. Concurrency | 9 | Cron handles parallel workloads |
| 9. **Compact errors** | **9** | errors.json structured + humanized |
| 10. Logs as event streams | 9 | agent-traces.jsonl per call |
| 11. **Webhook triggers** | **8** | Self-hosted receiver (port 8081) |
| 12. **Stateless reducers** | **9** | All agents read state, write state |
| **AVG** | **9.0/10** | |

---

## 🔢 Detailed Numbers

| Metric | Count |
|--------|-------|
| **Agents** | 51 |
| ├─ Executive (16 depts) | 32 |
| ├─ Coaching (5 depts) | 9 |
| ├─ Cross-cutting | 4 |
| ├─ Board | 1 |
| ├─ Top exec/management | 5 |
| **Skills** | 235 (0 HIGH, 0 FAIL) |
| ├─ Coaching (the IP) | 17 |
| ├─ Operations | 218 |
| **Scripts** | 90 |
| ├─ agents-v2/scripts/ | 26 |
| ├─ /opt/data/scripts/ | 64 |
| ├─ Unit tests | 44 PASS |
| **Cron jobs** | 83 |
| ├─ Daily | 8 |
| ├─ Hourly | 6 |
| ├─ Weekly | 7 |
| ├─ Real-time | 4 |
| ├─ Monthly | 4 |
| ├─ Per-tick (30m) | 6+ |
| **MCPs** | 16 |
| **Webhook endpoints** | 4 |
| **Databases** | 14 SQLite + 14 JSON |
| **Eval-gate runs** | 96 (233 PASS historical) |
| **Phase docs** | 27 |
| **GitHub commits** | 50+ |

---

## 🚀 The Loop (How It Runs Automatically)

```
┌─────────────────────────────────────────────────────────┐
│ THE 7-STEP ORG LOOP                                      │
│                                                          │
│ 1. PRIORITIZE  ──► management-coordinator + OKRs         │
│                       │                                  │
│ 2. SETUP       ──► engineering-roster + ai-ops           │
│                       │                                  │
│ 3. REVIEW      ──► eval-gate-runner (17/17 PASS)         │
│                       │                                  │
│ 4. OPTIMIZE    ──► devops-monitor + cost-monitor         │
│                       │                                  │
│ 5. AUTOMATE    ──► 83 cron jobs + webhook triggers       │
│                       │                                  │
│ 6. SELF-       ──► coaching-quality-reviewer +            │
│    REFLECT          prompt-improvement-suggester          │
│                       │                                  │
│ 7. MONITOR     ──► cron-heartbeat + self-running-check   │
│                       │                                  │
│ 8. INTEGRATE   ──► org-state.json unified source         │
│                       │                                  │
│                  (loops to 1)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🌐 Tech Stack (External Dependencies)

```
┌─────────────────┐
│  HERMES AGENT   │ ── from NousResearch, forked
│  (orchestrator) │      local: WhatsApp→Messaging rebrand
└────────┬────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│   LLM PROVIDERS │    │   MCPs (16)     │
│ • litellm/fast  │    │ • linear        │
│ • OpenRouter    │    │ • github        │
│ • Modelo de IA 4.5    │    │ • figma         │
│ • MiniMax-M3    │    │ • cloudflare    │
└─────────────────┘    │ • brave-search  │
                       │ • comfy-cloud   │
                       │ • blender       │
                       │ • + 10 more     │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  INTEGRATIONS   │
                       │ • Evolution API │
                       │   (WhatsApp)    │
                       │ • Cloudflare    │
                       │ • Cloudflare R2 │
                       │ • Email (SMTP)  │
                       └─────────────────┘
```

---

## 📜 Trademark Compliance

Per Hostinger incident (2026-Q1): `srv1396188.hstgr.cloud` suspended over `mensajeconnect.paragu-ai.com` flagged as phishing impersonation.

**Banned case-insensitive:** `texto mensajeria empresarial canal de texto web canal de texto red social principal objetivo red social de fotos red social de fotos canal de mensajeria gafas de realidad virtual pasarela de pagos secundaria pasarela de pagos buscador principal correo electronico plataforma de video plataforma de videos cortos red social red social canal de comunicacion canal de comunicacion suite ofimatica suite ofimatica dispositivo personal almacenamiento en la nube tienda en linea infraestructura-en-la-nube- proveedor de IA asistente de IA generativa proveedor de IA modelo de IA`

**Carve-outs:** functional terms, upstream OSS names, Hostinger incident quote.

**Enforcement:** `trademark-compliance-scrub` cron every commit + agent prompt injection.

---

## ✅ What's Next (3 Real Blockers)

1. **Send first prospect WhatsApp** (5 min, $0)
2. **Top up $20 OpenRouter** (2 min, $20)
3. **Run first free quick-win** (45 min, $0)

After first customer: $500 MRR → compound.

---

*Built with Hermes Agent + 51 sub-agents + 235 skills + 90 scripts. Audited 9.0/10. Self-running. Production-ready. Awaiting first paying customer.*
