# AI Whisperers — Internal Org Layer (`aiw-org`)

> **This repo is the internal AI Whisperers organization layer.**
> It contains the people, departments, agents, and tooling that run AIW day-to-day.
> It is **not** the customer-facing coaching product — that lives in
> [`Ai-Whisperers/growth-coaching`](https://github.com/Ai-Whisperers/growth-coaching).

---

## What this repo is

The internal AIW organization, defined as code:

- **6 Tier-1 departments** — Operations, Finance & Legal, Sales & Growth, Engineering & Development, Research & Education, People & Culture
- **47 agents** (T1 leads + T2 sub + T3 cross-cutting + T4 monitoring + T5 coaching)
- **92 cron jobs** (the heartbeat of the org)
- **24 DEMIURGE agents** (Greek-mythology-named canonical layer)
- **113 KB of state** (org-state.json + 8 dept state files + eval-per-agent.json + cron-error-watchdog.json + 30+ historical snapshots)
- **13 scripts** in `scripts/` (cron-heartbeat, health-check, state-validate, kiki-coach-prep, etc.)
- **16 dept-monitor patterns** (one per agent)
- **Catalog docs** — full dept/role/agent inventory at `analysis/DEPT-AGENTS-ROLES-COMPLETE.md` and `analysis/ORGANIGRAM.md`

---

## Repo naming history

| Period | Repo name | Purpose |
|---|---|---|
| 2026-08-31 earlier | `Ai-Whisperers/agent-infra` | Original name (general "infra") |
| 2026-08-31 now | **`Ai-Whisperers/aiw-org`** | Renamed to signal "internal AIW org layer" — not the coaching product |

Old URLs auto-redirect to the new name.

---

## What is NOT in this repo

| Concern | Repo | Why |
|---|---|---|
| GROW coaching product for paying customers | `Ai-Whisperers/growth-coaching` | Different audience (customers), different lifecycle (releases), different access control |
| The `packages/coaching/` distributable package | `Ai-Whisperers/growth-coaching` | Product code, not org code |
| DEMIURGE research / source catalog | `Ai-Whisperers/growth-coaching` | Framework + research belongs with the product that uses it |
| Customer data | (not in repo at all — runs at runtime in `/opt/data/state/`) | PII must never leak into the org-as-code artifact |

---

## Layout

```
aiw-org/
├── README.md                              ← you are here
├── analysis/                              ← catalog docs (DEPT-AGENTS-ROLES-COMPLETE, ORGANIGRAM, naming)
│   ├── DEPT-AGENTS-ROLES-COMPLETE.md
│   ├── ORGANIGRAM.md
│   ├── AGENT-NAMES-V2.md
│   ├── NAMING-CONVENTION-ANALYSIS.md
│   ├── AGENT-HUMAN-NAMES.md
│   ├── DEPT-AGENTS-PUN-NAMES.md
│   ├── REMAINING-TASKS-AND-WISHLIST.md
│   └── README.md
├── departments/                           ← 6 Tier-1 dept charters
│   ├── 01-operations.md
│   ├── 02-finance-legal.md
│   ├── 03-sales-growth.md
│   ├── 04-engineering-delivery.md
│   ├── 05-research-education.md
│   └── 06-people-culture.md
├── coach/                                 ← internal coaching product (14 agents)
│   ├── README.md
│   ├── kiki-coach/                        ← charter + curriculum + lessons (Ivan's actual coaching)
│   ├── coach-ivan/                        ← self-coaching cron agent
│   ├── coach-kiki/                        ← self-coaching cron agent for Kiki
│   ├── coach-lead-agents/                 ← coaches lead agents on GROW
│   ├── coach-lead-finder/                 ← lead-finding coaching
│   ├── coach-onboarding/                  ← customer/FTE onboarding
│   ├── coach-cohort-facilitator/          ← (planned)
│   ├── coach-conversion-agent/            ← (planned)
│   ├── coach-practitioner/                ← (planned)
│   ├── coach-renewal-manager/             ← renewal coaching
│   ├── coach-roi-tracker/                 ← ROI coaching
│   ├── coach-org/                         ← quarterly org coaching
│   ├── coaching-content-curator/          ← coaching content calendar
│   ├── coaching-quality-reviewer/         ← every-30-min quality review
│   └── coaching-research-intelligence/    ← coaching research signals
├── <agent-name>/                          ← the other 33 production agents at root
│   ├── PROMPT.md
│   ├── outbox/                            ← historical briefs
│   └── PROMPT-monitor.md                  ← (some agents)
├── dept-monitors/                         ← 16 PROMPT-monitor.md patterns + INDEX.md
├── scripts/                               ← infra scripts (state-validate, cron-heartbeat, etc.)
├── schemas/                               ← 9 agent-state schemas
├── state/                                 ← LIVE runtime state (coord.json, finance.json, ...)
└── research/                              ← research materials used by org agents
```

---

## Sister repo

[`Ai-Whisperers/growth-coaching`](https://github.com/Ai-Whisperers/growth-coaching) — the **customer-facing coaching product**. It contains:
- 6 distributable packages (coaching, finance, sales, operations, engineering, research)
- DEMIURGE framework + research catalog
- Constitution charters + research archives

The two repos are **sister projects** that share:
- Cron sync infrastructure (`/opt/data/cron/jobs.json` is the canonical mirror)
- BWS secret store (`/opt/data/.hermes/bws-secrets-cache.tsv`)
- Bitwarden-backed credentials
- The same Hermes runtime + state schema design

---

## How to add a new agent

1. **Pick a name** — see `analysis/NAMING-CONVENTION-ANALYSIS.md` for the rule (DEMIURGE agents use Greek mythology, heritage agents use portmanteau)
2. **Pick a department** — see `analysis/DEPT-AGENTS-ROLES-COMPLETE.md` for the canonical role catalog
3. **Create the directory**:
   ```
   /opt/data/agents/<agent-name>/
   ├── PROMPT.md          ← 12-section template (see coach/coach-ivan/PROMPT.md for example)
   └── outbox/            ← mkdir + .gitkeep
   ```
4. **Add a cron job** to `/opt/data/cron/jobs.json` (use any `aiw-<existing-agent>` as template)
5. **Update the catalogs** — `analysis/DEPT-AGENTS-ROLES-COMPLETE.md` and `analysis/ORGANIGRAM.md`
6. **Commit + push** — the cron-guard pre-commit hook + cron-sync cron pick it up

---

## See also

- [ORG-AGENTS.md](ORG-AGENTS.md) — full handoff matrix (47 agents, 9 schemas, producer→consumer)
- [departments/](departments/) — 6 Tier-1 dept charters
- [analysis/](analysis/) — catalogs + naming + wishlist
- [coach/README.md](coach/README.md) — internal coaching product details
- [`Ai-Whisperers/growth-coaching`](https://github.com/Ai-Whisperers/growth-coaching) — sister repo