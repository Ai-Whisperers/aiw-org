# AI Whisperers — Internal Org Layer (`aiw-org`)

> **This repo is the internal AI Whisperers organization layer.**
> It contains the people, departments, agents, and tooling that run AIW day-to-day.
> It is **not** the customer-facing coaching product — that lives in
> [`Ai-Whisperers/growth-coaching`](https://github.com/Ai-Whisperers/growth-coaching).

---

## What this repo is — at a glance (2026-09-01 snapshot)

| | Count | Where to find |
|---|---:|---|
| Tier-1 charter departments | 7 (6 + board) | `01..06-*/`, `board-of-directors/` |
| Atomic DEMIURGE agents | 24 | `demiurge/agents/` |
| Sub-agents (Tier-2/Tier-3) | 49 | `<dept>/<agent>/PROMPT.md` |
| PROMPT.md files (all agents) | **63** | every agent dir |
| PROMPT-monitor.md files (wiring + thresholds) | **35** | every monitored agent dir |
| Cron jobs (heartbeat) | **131** | `/opt/data/.hermes/cron/jobs.json` |
| KPI stacks (per dept) | 7 | `demiurge/kpi/*-stack.yaml` |
| Signal routes (per dept) | 7 | `demiurge/signals/*.yaml` |
| State files (live + versioned) | ~50 | `state/`, `/opt/data/state/` |
| Research catalogs (per dept) | 7 | `research/dept-research/{01..06,board}-research-areas.md` |
| Research areas documented | **52** | (per `DEPT-RESEARCH-METHODOLOGY.md`) |
| Research areas executed (Phase 8) | **30** | `engineering/`, `operations/`, `sales/`, `finance/`, `research/`, `board/` |
| Tests | **72** | `tests/` (incl. new `test_eval_aggregate.py`) |
| Scripts (production) | 36 | `scripts/` |
| Smoke gate | 100% pass, 9s | `scripts/smoke-test.sh all` |
| Lint | 63/63 pass | `scripts/lint-prompts.py` |

**Active phases**: 5 (setup parity), 6 (execution gaps), 7 (per-dept research), 8 (executing 30 research areas). See `analysis/PHASE-*-FEEDBACK.md`.

---

## What is NOT in this repo

| Concern | Repo | Why |
|---|---|---|
| GROW coaching product for paying customers | `Ai-Whisperers/growth-coaching` | Different audience (customers), different lifecycle (releases), different access control |
| The `packages/coaching/` distributable package | `Ai-Whisperers/growth-coaching` | Product code, not org code |
| DEMIURGE research / source catalog | `Ai-Whisperers/growth-coaching` | Framework + research belongs with the product that uses it |
| Customer data | (not in repo at all — runs at runtime in `/opt/data/state/`) | PII must never leak into the org-as-code artifact |

---

## Quick links

- **[OPERATIONS.md](OPERATIONS.md)** — how the whole org works end-to-end (read first if new)
- **[department-index.md](department-index.md)** — per-department overview (agents, monitors, research, KPIs)
- **[ON-CALL.md](ON-CALL.md)** — who/what to do when things break
- **[REVIEW-2026-Q4.md](REVIEW-2026-Q4.md)** — current quarter review + Phase 26 candidates
- **[ORG-AGENTS.md](ORG-AGENTS.md)** — full 47-agent handoff matrix + 9 schemas + producer→consumer
- **[departments/](departments/)** — 6 Tier-1 dept charters
- **[analysis/](analysis/)** — phase feedback docs + L1-L4 hygiene + naming catalogs
- **[research/](research/)** — research areas + methodology + cross-dept research catalogs
- **[research/dept-research/](research/dept-research/)** — 7 per-dept research catalogs (52 areas)
- **[dept-monitors/](dept-monitors/)** — 35 PROMPT-monitor.md patterns + INDEX
- **[demiurge/](demiurge/)** — DEMIURGE agent framework (24 souls) + KPI stacks + signals
- **[schemas/](schemas/)** — 9 agent-state schemas (additionalProperties: false enforced)
- **[state/](state/)** — LIVE runtime state (mirrored from `/opt/data/state/`)
- **[patterns/](patterns/)** — hard-stop-wrapper, idempotency, trademark-scrub
- **[playbooks/](playbooks/)** — 00-INDEX + 8 dept playbooks + ROADMAP
- **[scripts/](scripts/)** — 36 production scripts (cron-sync, eval-gate, smoke-test, …)
- **[tests/](tests/)** — 32 test files (72 tests)
- **[tickets/](tickets/)** — 81 DEMIURGE ticket artifacts

---

## The 6 Tier-1 departments (one-line each)

| Dept | Charter | Lead agent | Sub-agents |
|---|---|---|---|
| **Operations** | Obs/automation/process excellence | `management-coordinator` | 9 (bizops, ai-ops, compliance, founder-bandwidth, source-curator, okr, procurement, + 2 cadence variants) |
| **Finance & Legal** | Compliance, funding, runway | `finance-controller` | 5 (business-analyst, accounting, funding, tax-receipts, + 1 cadence variant) |
| **Sales & Growth** | Revenue, pipeline, proposals | `sales-pipeline` | 6 (lead-enrichment, proposal-drafter, revops, marketing, multimedia, + 3 cadence variants) |
| **Engineering** | Code, infra, safety, quality | `engineering-roster` | 13 (ai-safety, devops, qa, security, chaos, drift, eval-gate, delivery, + 4 cadence variants) |
| **Research & Education** | Knowledge, thesis, courses | `research-tracker` | 3 (citation-checker, course-producer, thesis-tracker) |
| **People & Culture** | Founder health, first-FTE prep | `people-hr` | 0 (kiki-coach lives in sister repo `coach-agents`) |
| **Board of Directors** | Cross-dept governance | `board-of-directors` | 0 (governance, not a charter dept) |

**For details per dept**: see [department-index.md](department-index.md).

---

## How to add a new agent

1. **Pick a name** — see `analysis/AGENT-NAMES-V2.md` (DEMIURGE: Greek myth; heritage: portmanteau)
2. **Pick a department** — see `analysis/DEPT-AGENTS-ROLES-COMPLETE.md`
3. **Create the directory**:
   ```
   /opt/data/agents/<dept>/<agent-name>/
   ├── PROMPT.md          ← 12-section template
   ├── PROMPT-monitor.md  ← if monitored (PROMPT-monitor.md template)
   └── outbox/            ← mkdir + .gitkeep (output sink)
   ```
4. **Add a cron job** to `/opt/data/.hermes/cron/jobs.json` (use any `aiw-<existing-agent>` as template)
5. **Update catalogs** — `analysis/DEPT-AGENTS-ROLES-COMPLETE.md` + relevant `demiurge/kpi/` + `demiurge/signals/`
6. **Verify** — `bash /opt/data/scripts/cron-sync.sh && /opt/data/.venv/bin/python3 scripts/lint-prompts.py && ./scripts/smoke-test.sh all`
7. **Commit + push** — pre-commit hook validates cron drift

---

## Repo naming history

| Period | Repo name | Purpose |
|---|---|---|
| 2026-08-31 earlier | `Ai-Whisperers/agent-infra` | Original name (general "infra") |
| 2026-08-31 now | **`Ai-Whisperers/aiw-org`** | Renamed to signal "internal AIW org layer" — not the coaching product |

Old URLs auto-redirect to the new name.

---

## Sister repo

[`Ai-Whisperers/growth-coaching`](https://github.com/Ai-Whisperers/growth-coaching) — the **customer-facing coaching product**. It contains:
- 6 distributable packages (coaching, finance, sales, operations, engineering, research)
- DEMIURGE framework + research catalog
- Constitution charters + research archives

The two repos share:
- Cron sync infrastructure (`/opt/data/cron/jobs.json` is the canonical mirror)
- BWS secret store (`/opt/data/.hermes/bws-secrets-cache.tsv`)
- Bitwarden-backed credentials
- The same Hermes runtime + state schema design

---

## See also

- **[OPERATIONS.md](OPERATIONS.md)** — the operational runbook (read this to understand how the org works)
- **[department-index.md](department-index.md)** — per-department pointer file
- **[ON-CALL.md](ON-CALL.md)** — what to do when X breaks
- **[ORG-AGENTS.md](ORG-AGENTS.md)** — full 47-agent handoff matrix
- **[dept-monitors/INDEX.md](dept-monitors/INDEX.md)** — 35 monitor pattern inventory
- **[analysis/PHASE-5-COMPLETION-REPORT.md](analysis/PHASE-5-COMPLETION-REPORT.md)** — setup parity 100%
- **[analysis/PHASE-6-REFINEMENT-FEEDBACK.md](analysis/PHASE-6-REFINEMENT-FEEDBACK.md)** — execution gap fixes
- **[analysis/PHASE-7-RESEARCH-FEEDBACK.md](analysis/PHASE-7-RESEARCH-FEEDBACK.md)** — 52 research areas
- **[analysis/PHASE-8-FEEDBACK.md](analysis/PHASE-8-FEEDBACK.md)** — 30 research areas executed
- **[research/DEPT-RESEARCH-METHODOLOGY.md](research/DEPT-RESEARCH-METHODOLOGY.md)** — the 7-question pattern
