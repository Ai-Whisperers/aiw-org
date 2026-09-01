# Engineering Dept — Gap Audit

> **Built 2026-09-01** — Phase 7 R6 (gap audit, companion to Research dept upgrade).
>
> **Doctrine**: LATAM-focused, no compliance theater. Engineering gaps evaluated
> against actual AIW deployment state (2 people, $240 MRR, 131 cron jobs, 12
> wired sub-agents, L1-L3 stable).
>
> **Methodology**: Direct inventory from `docs/ROLES-INVENTORY.md` +
> `ls 04-engineering/` + PROMPT.md frontmatter cluster field.

---

## Summary

**Engineering dept coverage**: **12/24 fully wired**, **3/24 partial**, **9/24 deferred**.

| Status | Count | % |
|---|---|---|
| ✅ Fully wired (T1 roles + critical T3) | 12 | 50% |
| 🟡 Partial (T2/T3 roles with thin coverage) | 3 | 12.5% |
| 💤 Deferred (rightly not activated at current scale) | 9 | 37.5% |

**Cluster distribution** (Run/Build/Enable per Phase 7 R5):
- **run**: 7 (devops-monitor + 30min, security-watchdog + 30min, ai-safety + 30min, chaos-test-runner, drift-detector, eval-gate-runner)
- **build**: 6 (engineering-roster, qa-automation-runner + on-pr, security-auditor, security-watchdog + 30min)
- **enable**: 1 (delivery-tracker)
- **unset**: 0 (all 14 agents now have cluster field)

---

## 24-Role Coverage Matrix

| # | Role | Tier | Status | Wired via |
|---|---|---|---|---|
| 4.1 | CTO/VP Engineering | 🟢 T1 | ✅ | Kiki (sole, human) |
| 4.2 | Engineering Manager | 🟠 T3 | 💤 Deferred | (5+ engs trigger) |
| 4.3 | Frontend Engineer | 🟢 T1 | ✅ | Kiki (consolidated) |
| 4.4 | Backend Engineer | 🟢 T1 | ✅ | Kiki (consolidated) |
| 4.5 | Full-stack Engineer | 🟢 T1 | ✅ | Kiki (consolidated) |
| 4.6 | Mobile Engineer | 🟠 T3 | 💤 Deferred | (no mobile products) |
| 4.7 | DevOps / SRE | 🟢 T1 | ✅ | `devops-monitor` + 30min |
| 4.8 | QA Engineer | 🟢 T1 | ✅ | `qa-automation-runner` + `qa-automation-on-pr` |
| 4.9 | Security Engineer | 🟢 T1 | ✅ | `security-watchdog` + 30min, `security-auditor` |
| 4.10 | ML Engineer | 🟠 T3 | 💤 Deferred | (no model training) |
| 4.11 | Data Engineer | 🟠 T3 | 💤 Deferred | (small data, < 100GB) |
| 4.12 | Solutions Architect | 🟠 T3 | ✅ | `architect-agent` (Phase 3 NEW) |
| 4.13 | Tech Writer | 🟡 T2 | 💤 Deferred | (Ivan writes docs today) |
| 4.14 | Engineering PM | 🟠 T3 | ✅ | `scope-intake`, `delivery-tracker` |
| 4.15 | Platform Engineer | 🟠 T3 | 🟡 Partial | implicit in `devops-monitor` |
| 4.16 | Release Manager | 🟠 T3 | ✅ | `engineering-roster` (deploy gate) |
| 4.17 | SRE | 🟠 T3 | ✅ | `chaos-test-runner` (Phase 5 NEW) |
| 4.18 | DBA | 🟡 T2 | 🟡 Partial | `devops-monitor` (backup verification) |
| 4.19 | Network Engineer | 🟠 T3 | 💤 Deferred | (Traefik + CF handle today) |
| 4.20 | UI/UX Designer | 🟡 T2 | 💤 Deferred | (Kiki handles, no formal design) |
| 4.21 | Product Designer | 🟠 T3 | 💤 Deferred | (no product surfaces to design) |
| 4.22 | Build / Release Engineer | 🟠 T3 | 🟡 Partial | CI handles, no dedicated agent |
| 4.23 | Embedded Systems Engineer | 🔴 T4 | 💤 Deferred | (T4 enterprise trigger) |
| 4.24 | AI Safety Engineer | 🟢 T1 | ✅ | `ai-safety-engineer` + 30min |

---

## Cluster Coverage (Run/Build/Enable)

| Cluster | Agents | Gap |
|---|---|---|
| **Run** (always-on monitors) | 7 | Good — all critical monitors wired |
| **Build** (shipping agents) | 6 | Good — all deploys/PRs covered |
| **Enable** (gates + scopes) | **1** | **GAP** — only `delivery-tracker`; missing delivery-orchestration |

---

## Cross-Cutting Demiurge Atomics

Only **2 atomics** explicitly reference engineering dept:
- `compliance-monitor` (security/compliance overlap)
- `argus-health-monitor` (health check overlap)

**Gap**: Engineering agents don't transfer_outputs to/from many atomics. The pattern `composition:` lists 1-2 atomics per agent — low integration density.

---

## Critical Gaps (prioritized)

### P1 — Activate now (gates current work)

| Gap | Cost | Trigger | Why now |
|---|---|---|---|
| **4.22 Build/Release Engineer** (T3) | 1 agent PROMPT + 1 script | NOW | CI pipeline has no agent; rollout/deploy gates rely on Kiki manually. Add `release-pipeline-agent` that owns the deploy-state machine. |
| **4.15 Platform Engineer** (T3) | 1 agent PROMPT | NOW | `devops-monitor` is overloaded; need separation of concerns between platform (infra) vs ops (monitoring). |

### P2 — Build soon (active gaps with clear ROI)

| Gap | Cost | Trigger |
|---|---|---|
| **4.18 DBA** (T2) | 1 agent PROMPT + 1 SQLite backup-verify script | When Postgres/SQLite > 5 DBs |
| **4.13 Tech Writer** (T2) | 1 agent PROMPT + 1 doc-style-guide | When docs > 50 files (currently 30) |

### P3 — Defer (correctly per doctrine)

| Gap | Trigger |
|---|---|
| **4.2 Engineering Manager** | 5+ engineers on team |
| **4.6 Mobile Engineer** | Mobile product launches |
| **4.10 ML Engineer** | Model training pipeline starts |
| **4.11 Data Engineer** | Data warehouse > 1TB |
| **4.19 Network Engineer** | Multi-region deploy |
| **4.20 UI/UX Designer** | >3 design surfaces |
| **4.21 Product Designer** | Product launch |
| **4.23 Embedded Systems** | T4 enterprise trigger |

---

## Build Order (Recommended)

| # | Agent | Effort | Impact |
|---|---|---|---|
| 1 | `release-pipeline-agent` (4.22) | 4h | Closes 4.22 partial → wired |
| 2 | `platform-engineer-agent` (4.15) | 4h | Closes 4.15 partial → wired; devops-monitor unloads |
| 3 | `dba-agent` (4.18) | 4h | Closes 4.18 partial → wired; SQLite backups verified daily |
| 4 | `tech-writer-agent` (4.13) | 6h | Closes 4.13 deferred → wired; auto-generates runbooks |

**Total**: 4 agents, ~18h work, 4/24 → wired (so12 → 16 of 24, i.e. 67%).

---

## What This Audit Does NOT Recommend

Per doctrine (no compliance theater, LATAM-focused):

- ❌ **SOC2 / ISO 27001** preparation — irrelevant at $240 MRR / 2 people
- ❌ **Staff Engineer / Principal Engineer tracks** — we have 1 engineer (Kiki)
- ❌ **Engineering Manager tracks** — flat org until 5+ engs
- ❌ **Multi-region Network Engineer** — Traefik + CF handles today
- ❌ **Embedded Systems** — T4 trigger, irrelevant for AIW

---

## Cross-Reference

- Research dept audit: see `04-05-implementation-plan.md` + v2 catalog
- Phase 7 R5 audit: see `04-05-phase7r5-execution-log.md`
- Cluster classification: Run/Build/Enable per `04-05-compiled-findings.md` §3

---

**Document path**: `/opt/data/agents/research/dept-research/04-engineering-gap-audit.md`
**Last updated**: 2026-09-01
**Status**: Audit complete, recommendations pending Ivan approval

---

## Sources & Standards

The audit framework and gap taxonomy draws on:

- **Drucker, P. (1974), *Management: Tasks, Responsibilities, Practices*** — the original functions-of-the-manager frame.
- **Laloux, F. (2014), *Reinventing Organizations*** — evolutionary-Teal self-management model. ISBN 978-0-9839241-1-8.
- **Gallup, *State of the Global Workplace Report*** (2024 ed.) — engagement vs performance benchmarks. <https://www.gallup.com/workplace>
- **Sunstein, C. (2013), *Simpler: The Future of Government*** — informed-consent + sludge-reduction framework for ops. ISBN 978-1-4813-0100-9.
- **HBR (2021), *The Leader as Coach* (Gormley & van Nieuwerburgh)**, *Harvard Business Review*, Nov-Dec 2021.
- **Susskind & Susskind (2015), *The Future of the Professions*** — expertise vs automation displacement framework.