# AIW Org Upgrade Proposal — 2026-09

> **Status**: DRAFT, awaiting Ivan's approval per phase.
> **Date**: 2026-09-01
> **Scope**: `aiw-org` repo. **Excludes** `coach/` (moved to `growth-coaching` repo) and all sister repos.
> **Method**: Local diagnostic of repo state + literature grounded in existing
> `research/org-design-literature.md` + DEMIURGE architecture docs + `analysis/`
> catalog. Web research on AI researchers (Karpathy/Sutton/Yao/Schaul/Andreas/etc.)
> **deferred pending Firecrawl enablement** — see §10 Appendix.

---

## TL;DR — what we are proposing

Treat `aiw-org` as a production platform. Lift DEMIURGE's architectural patterns
(atomicity, router, KPI, feedback loops, naming canon) into the dept layer.
Collapse the 3-taxonomy mess (6 Tier-1 + 8 Tier-2 skeleton + DEMIURGE side-layer)
into ONE coherent architecture with three clean layers:

| Layer | Purpose | Currently | Target |
|-------|---------|-----------|--------|
| **Atomic** | Reusable primitives (DEMIURGE agents) | 24 agents, partial infra | 24 agents, full infra wired |
| **Business** | Department functions (6 depts) | 6 depts × 34 PROMPTs, gaps | 6 depts × ~7 PROMPTs each, fully integrated |
| **Governance** | Constitution, monitors, eval gates | Mostly there, under-wired | Production-grade with feedback loops |

**5 phases, reversible, each with rollback plan. No big-bang rewrite.**

---

## 1 — Current state (diagnostic)

### 1.1 Inventory at a glance

| Asset | Count | Status |
|-------|-------|--------|
| Departments (Tier-1) | 6 | ✓ Ratified v0.3.0 |
| Departments (Tier-2 / v2 taxonomy) | 8 | ✗ Skeleton only — `department.md` + `cadences.md` + `signals.yaml`, no agents underneath |
| DEMIURGE agents | 24 | ✓ Have PROMPT.md; ⚠ only 10 have `agent.yaml`+`repo-manifest.yaml` |
| DEMIURGE router rules | 5 yaml files | ✓ Substantive content (dispatch, timing, document, signals) |
| DEMIURGE KPI | 1 yaml (revenue-stack) | ⚠ Covers 3 depts (marketing/sales/PD); no ops/finance/eng/research/people KPIs |
| DEMIURGE feedback loops | 4 loops + soul-improvement workflow | ✓ Defined; ⚠ no runtime evidence of firing |
| Dept agents with PROMPT.md | 34 | ⚠ Mix of frontmatter styles; some empty |
| Dept agents with PROMPT-monitor.md | 15 | ✓ Most leads covered |
| Schema files | 9 | ✓ JSON Schema draft-07 with `additionalProperties: false` |
| Tickets | 79 DEMIURGE + 3 misc | 49 COMPLETED, 6 ACTIVE, 1 COMPLETE, 22 planned/pending |
| Patterns | 9 | ✓ (idempotency, hard-stops, sqlite-schema, trademark-scrub, etc.) |
| Playbooks | 13 | ✓ |
| Scripts | 47 (across subdirs) | ⚠ Some deprecated (`coach-onboarding-poller.py`), some orphan |
| Tests | 22 pytest | ⚠ Coverage uneven (state/db heavily tested, eval lightly) |
| State JSON files | 11 live + history/ + snapshots/ | ⚠ Many `pre-sqlite.bak` files left in place; cleanup needed |

### 1.2 The 3-taxonomy problem

The repo has THREE different "department taxonomies" living simultaneously:

1. **`departments/`** (Tier-1, 6 depts) — `01-operations.md` through `06-people-culture.md`,
   plus `ORG-AGENTS.md` v0.3.0 as operating constitution. **This is the ratified one.**
2. **`departments-taxonomy/`** (Tier-2, 8 depts) — `ai-ops`, `ai-org-platform`, `compliance`,
   `knowledge-mgmt`, `marketing`, `operations`, `product-discovery`, `sales`.
   **Each has only `department.md` + `cadences.md` + `signals.yaml`** — no agents, no PROMPTs.
3. **DEMIURGE priority depts** (3 depts) — `marketing`, `sales`, `product-discovery`.
   These are the "revenue stack" departments with full agent swarms (Hera/Apollo/Athena).

**The three don't cleanly map.** DEMIURGE's 3 priority depts overlap with Tier-1's
03-sales-growth and partially with Tier-2's marketing/sales/product-discovery.
Tier-2's other 5 depts (ai-ops, ai-org-platform, compliance, knowledge-mgmt, operations)
have no Tier-1 or DEMIURGE counterparts.

### 1.3 What's actually working well

- **DEMIURGE router is real**. `dispatch-rules.yaml`, `document-dispatch-rules.yaml`,
  `timing-rules.yaml`, `document-timing-rules.yaml`, `revenue-signals.yaml` —
  these are production-grade patterns with P0–P3 ITIL-aligned SLAs.
- **Soul-improvement workflow is well-designed**. Argus → suggestion file → Ivan
  approval → PROMPT.md version bump → episodic log. Just no evidence it's run.
- **16-monitor matrix in `dept-monitors/INDEX.md`** is a strong design intent,
  even though only 15 PROMPT-monitor.md files exist.
- **KPI definitions** for the 3 revenue-stack depts are precise (formulas, targets, units, feedback_loop).
- **Pattern catalog** (`patterns/`) covers idempotency, hard-stops, SQLite schema,
  trademark scrubbing — exactly the "production hygiene" primitives a multi-agent
  org needs.
- **Existing literature synthesis** (`research/org-design-literature.md`, 318 lines)
  already maps the 4 invariants of org design (decision rights, boundaries, cadence,
  specialization) to specific agents and files in this repo.

### 1.4 What's broken or missing

| # | Gap | Severity | Impact |
|---|-----|----------|--------|
| 1 | Tier-2 taxonomy (`departments-taxonomy/`) is 8 skeleton depts with no agents | **HIGH** | Confusing — looks like a parallel org that's empty |
| 2 | DEMIURGE KPIs only cover 3 depts (mkt/sales/PD); ops/finance/eng/research/people have none | **HIGH** | 3 of 6 departments have no measurable health |
| 3 | 23 heritage agents in `agents-prompts/` awaiting migration to `demiurge/agents/` (DEMIURGE-082 pending) | **HIGH** | Two name systems in parallel; can't apply canonical soul-improvement |
| 4 | Feedback loops defined but no runtime signal that they fire (no logs, no test coverage) | **HIGH** | Soul-improvement is theoretical, not operational |
| 5 | State files have `pre-sqlite.bak` left in place; migration incomplete | **MED** | Confusion about which file is source of truth |
| 6 | Scripts dir has deprecated/orphan files (`coach-onboarding-poller.py`, `eval-gate-runner.sh` + `scripts/eval/aiw-eval-gate-runner.sh` — duplicate) | **MED** | Two cron jobs doing same thing, or dead code |
| 7 | DEMIURGE naming convention (`NAMING-CONVENTION-ANALYSIS.md`, `AGENT-NAMES-V2.md`) only ~50% applied to dept layer | **MED** | Greek-myth canon inconsistent |
| 8 | No `tests/` for: router dispatch, KPI computation, feedback-loop firing, dept-monitor thresholds | **HIGH** | Critical infra has no regression tests |
| 9 | `docs/demiurge/` exists but `docs/` root has overlap (e.g. `ORGANIGRAM-AND-DETAILED-ANALYSIS.md` vs `analysis/ORGANIGRAM.md`) | **LOW** | Doc drift, not blocking |
| 10 | 4 P0 secret leaks OPEN (per `REMAINING-TASKS-AND-WISHLIST.md`) — outside upgrade scope but block production hardening | **P0** | Operator action only |

### 1.5 DEMIURGE patterns that are NOT lifted to dept layer (yet)

The user specifically asked: lift all Demiurge architectural patterns to dept layer.
Status:

| DEMIURGE pattern | Defined in demiurge/ | Adopted by dept layer? |
|------------------|----------------------|------------------------|
| Atomic agents (one job each) | ✓ 24 agents | ⚠ Partial — dept agents mix granular and composite roles |
| YAML metadata (`agent.yaml`) | ✓ 10/24 agents have it | ✗ Dept layer uses frontmatter, no `agent.yaml` |
| Naming canon (Greek myth) | ✓ Enforced | ✗ Dept layer uses portmanteau (`ai-ops-coordinator` not `Kronos`) |
| Router dispatch rules | ✓ 5 yaml files | ✗ Dept layer relies on cron + chat handoffs |
| Timing SLAs (PT2H, P7D, etc.) | ✓ ITIL-aligned | ✗ Dept layer has cron schedules but no SLA definitions |
| Quorum requirements | ✓ Defined in router | ✗ Dept layer has no quorum semantics |
| KPI definitions with formulas | ✓ revenue-stack.yaml | ⚠ Only 3 depts covered |
| Feedback loops (trigger→action→owner) | ✓ 4 loops defined | ✗ Dept layer has none |
| Soul-improvement workflow | ✓ soul-improvement.yaml | ✗ Dept layer has no soul versioning |
| Source-grounding (literature+community) | ✓ `sources/*/catalog.yaml` | ✗ Dept layer has no `sources/` per dept |
| Signal-typed inter-agent comms | ✓ `signal-channel` schema | ✗ Dept layer uses string-keyed state files |
| Memory layers (episodic git + community + operational sqlite) | ✓ Schema defined | ⚠ Operational sqlite exists; episodic git exists; community NOT used |
| Human approval gates | ✓ DEMIURGE-008/015/033/041/047 | ⚠ Dept layer has hard_stops in frontmatter, no formal gate tickets |
| Repo-manifest per agent | ✓ Per-agent git repo | ✗ Dept agents have no separate git repos |

---

## 2 — Target architecture (one diagram)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GOVERNANCE LAYER                              │
│  constitution/      departments/ORG-AGENTS.md v0.4.0            │
│  departments/       (6 depts, ratified)                          │
│  analysis/          (catalog docs, kept in sync)                 │
│  playbooks/         (13 playbooks, references dept + atomic)     │
│  state/             (live runtime, one file per dept)            │
│  state/snapshots/   (6h snapshots, 90-day retention)              │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ escalation / hard_stops / gate decisions
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS LAYER (6 depts)                      │
│  01-operations     02-finance-legal     03-sales-growth         │
│  04-engineering    05-research-edu      06-people-culture        │
│                                                                  │
│  Each dept:                                                      │
│  ├── department.md        (charter, owns, doesn't own)          │
│  ├── cadences.md         (cron schedule grid)                    │
│  ├── signals.yaml        (input/output signal types)             │
│  ├── kpis.yaml           (NEW — measurable health, feedback)     │
│  ├── feedback-loops/     (NEW — monitor→source→soul)             │
│  ├── sources/            (NEW — literature+community grounding)  │
│  ├── lead-agent/         (PROMPT.md + agent.yaml + monitor)      │
│  └── sub-agent-N/        (PROMPT.md + agent.yaml)                │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ composed-of (dept agents call atomic agents)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    ATOMIC LAYER (DEMIURGE)                       │
│  demiurge/agents/    (24 named agents, all have agent.yaml)     │
│  demiurge/router/    (5 yaml: dispatch, timing, signals)        │
│  demiurge/kpi/       (per-dept KPI yaml, all 6 depts)           │
│  demiurge/feedback-loops/  (4 loops + soul-improvement)          │
│  demiurge/sources/   (literature+community catalogs)            │
│  demiurge/memory/    (episodic+community+operational layers)    │
│                                                                  │
│  Pattern: dept agents COMPOSE atomic agents; atomic agents are   │
│  never bypassed for "revenue-stack" work (mkt/sales/PD).        │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ signals in / events out
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                          │
│  scripts/  (cron jobs, health, eval, cost-cap, snapshot)        │
│  schemas/  (9 agent-state JSON schemas, draft-07)                │
│  patterns/ (9 reusable: idempotency, hard-stops, sqlite)        │
│  tests/    (pytest, 30+ tests covering router, kpi, feedback)   │
│  tickets/  (DEMIURGE + Phase + ad-hoc — single workflow)        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 The key architectural commitment

**Atomic ≠ Business.** A dept agent that needs to score leads does not implement
lead scoring itself — it calls `cadmus-lead-enrichment` (atomic). A dept agent that
needs to draft a proposal does not write copy itself — it calls `metis-proposal-drafter`
(atomic) and `calliope-content-producer` (atomic). This is the **DEMIURGE composition
discipline** and it must be enforced.

**Why this matters**: it gives you independent testability, independent KPI tracking,
and independent versioning for each piece. When `cadmus-lead-enrichment`'s soul gets
revised, only Apollo (the dept agent that calls it) needs to re-validate, not every
dept agent that does lead work.

### 2.2 The "delete Tier-2 taxonomy" decision

After Phase 1, `departments-taxonomy/` will be **deleted** (with migration of any
unique content into `departments/`). The 8-dept v2 taxonomy was a v2 design that
was never executed. Keeping skeleton depts with no agents is worse than deleting
them — it implies an org structure that doesn't exist.

If you ever need a v3 taxonomy, you write it cleanly from the v0.4.0 architecture,
not from skeleton directories that are out of sync with reality.

---

## 3 — Migration plan

### 3.1 Files / directories affected

| Path | Action | Reason |
|------|--------|--------|
| `departments-taxonomy/` | **DELETE** (after content migration) | Skeleton depts with no agents, never activated |
| `departments/` | KEEP + EXTEND | Ratified v0.3.0 operating constitution |
| `departments/ORG-AGENTS.md` | UPDATE to v0.4.0 | Reflect atomic-composition, signal-typed comms, dept KPIs |
| `demiurge/agents/` | KEEP + COMPLETE | Add `agent.yaml` to remaining 14 agents (currently 10/24 have it) |
| `demiurge/kpi/` | EXTEND | Add ops, finance, engineering, research, people KPIs (currently only mkt/sales/PD) |
| `demiurge/feedback-loops/` | EXTEND | Add dept-specific loops; keep existing 4 |
| `departments/<N>/kpis.yaml` | CREATE (×6) | Per-dept KPIs with formulas, targets, feedback_loop |
| `departments/<N>/feedback-loops/` | CREATE (×6) | Dept-specific loops |
| `departments/<N>/sources/` | CREATE (×6, optional) | Literature+community grounding per dept |
| `state/*.pre-sqlite.bak` | DELETE (after migration verified) | Migration leftovers |
| `scripts/coach-onboarding-poller.py` | MOVE to `growth-coaching` or DELETE | Coaching scope, not org layer |
| `scripts/eval-gate-runner.sh` (root) | DELETE | Duplicate of `scripts/eval/aiw-eval-gate-runner.sh` |
| `scripts/deprecation/` | KEEP | Useful pattern for retiring agents/scripts |
| `agents-prompts/` (legacy) | MIGRATE to `demiurge/agents/` (DEMIURGE-082) | One canonical location for agent souls |
| `docs/ORGANIGRAM-AND-DETAILED-ANALYSIS.md` | DELETE | Duplicates `analysis/ORGANIGRAM.md` |
| `dept-monitors/INDEX.md` | UPDATE | Sync with new 16-monitor matrix reflecting atomic-layer additions |
| `analysis/UPGRADE-PROPOSAL-2026-09.md` | KEEP (this doc) | Reference for the rollout |
| `tests/` | EXTEND | Add router dispatch tests, KPI computation tests, feedback-loop firing tests |

### 3.2 New files to create

```
departments/01-operations/
├── kpis.yaml                         (NEW — operations health metrics)
├── feedback-loops/ops-monitor-loops.yaml   (NEW)
└── sources/operations/              (NEW — if content exists from research)

[repeat for 02-finance-legal, 03-sales-growth, 04-engineering, 05-research-education, 06-people-culture]

demiurge/agents/<id>/agent.yaml      (CREATE for the 14 missing)
demiurge/kpi/{operations,finance,engineering,research,people}.yaml   (NEW)
demiurge/feedback-loops/finance-monitor-loops.yaml          (NEW)
demiurge/feedback-loops/engineering-monitor-loops.yaml      (NEW)
demiurge/feedback-loops/research-monitor-loops.yaml         (NEW)

tests/test_router_dispatch.py          (NEW)
tests/test_kpi_computation.py          (NEW)
tests/test_feedback_loop_firing.py     (NEW)
tests/test_dept_monitor_thresholds.py  (NEW)

analysis/ARCHITECTURE-DIAGRAM-2026-09.md   (NEW — visual target architecture)
```

### 3.3 What does NOT change (preserved invariants)

- **Decision rights matrix** in `ORG-AGENTS.md` (USD thresholds, hard stops) — preserved
- **16-monitor matrix** in `dept-monitors/INDEX.md` — preserved (just updated)
- **9 schema files** — preserved (extended, not replaced)
- **9 patterns** — preserved (extended, not replaced)
- **13 playbooks** — preserved (cross-referenced, not rewritten)
- **Cron schedule grid** in `ORCHESTRATION.md` — preserved (no cadence changes)
- **Founder HITL gates** (Ivan + Kiki) — preserved (hard_stops unchanged)
- **`scripts/observability/prompt-improvement-suggester.py`** — preserved as the soul-improvement runner
- **`scripts/state-snapshot.sh`, `scripts/db-snapshot.py`, `scripts/cron-heartbeat.sh`** — preserved as is

---

## 4 — Phased rollout (reversible, no big-bang)

Each phase has: scope, deliverables, success criteria, rollback, time estimate.

### Phase 1 — **Diagnostic lock-in + taxonomy cleanup** (no code yet)

| Aspect | Detail |
|--------|--------|
| **Scope** | Migrate any unique content from `departments-taxonomy/` into `departments/`; delete `departments-taxonomy/`; delete duplicate `docs/ORGANIGRAM-AND-DETAILED-ANALYSIS.md` |
| **Deliverables** | One commit: `chore(cleanup): remove tier-2 skeleton taxonomy` |
| **Success** | `find . -name "department.md"` returns only the 6 Tier-1 dept files; `analysis/REMAINING-TASKS-AND-WISHLIST.md` updated to remove "Tier-2 taxonomy v2" item |
| **Rollback** | `git revert` |
| **Time** | 30 min |
| **Risk** | **LOW** — pure cleanup, no behavior change |
| **Greenlight** | Need your go. Will not start without it. |

### Phase 2 — **Atomic layer completion** (DEMIURGE infrastructure)

| Aspect | Detail |
|--------|--------|
| **Scope** | (a) Add `agent.yaml` to 14 DEMIURGE agents that lack it. (b) Add per-dept KPIs for the 3 currently-uncovered depts (ops/finance/eng/research/people). (c) Add feedback loops for those depts. (d) Wire runtime evidence: each feedback loop gets a `last_fired_at` field in its yaml, updated by the soul-improvement workflow |
| **Deliverables** | 14 new `agent.yaml` files, 5 new `kpi/*.yaml` files, 3 new feedback-loop yamls, 1 new `soul-improvement.yaml` extension |
| **Success** | `find demiurge/agents -name agent.yaml | wc -l` returns 24 (not 10). `find demiurge/kpi -name '*.yaml'` returns 6 (not 1). `scripts/observability/prompt-improvement-suggester.py --validate` passes |
| **Rollback** | `git revert` (additive, no destructive changes) |
| **Time** | 2–3 hours |
| **Risk** | **LOW** — additive only |
| **Greenlight** | Need your go. |

### Phase 3 — **Business layer integration** (dept layer mirrors atomic)

| Aspect | Detail |
|--------|--------|
| **Scope** | (a) For each of 6 depts: create `kpis.yaml`, `feedback-loops/*.yaml`, link to atomic-layer KPIs. (b) Migrate 23 heritage agents from `agents-prompts/` to canonical locations (DEMIURGE-082). (c) Apply naming canon where missing (rename or alias map). (d) Add frontmatter `composition:` block to dept PROMPTs that declare which atomic agents they call. (e) Update `departments/ORG-AGENTS.md` to v0.4.0 with composition discipline |
| **Deliverables** | 6 × `kpis.yaml`, 6 × `feedback-loops/*.yaml`, 23 migrated agents, ~30 PROMPT frontmatter additions, 1 constitution bump |
| **Success** | `find departments -name "kpis.yaml" | wc -l` returns 6. `grep -l "composition:" departments/*/PROMPT.md | wc -l` returns ≥ 30. `tests/test_agent_composition.py` passes (new test). |
| **Rollback** | `git revert` (mostly additive) |
| **Time** | 4–6 hours |
| **Risk** | **MEDIUM** — PROMPT frontmatter changes affect agent behavior; need to validate each agent runs cleanly after change |
| **Greenlight** | Need your go. Per-dept checkpoint after each dept completes. |

### Phase 4 — **Test coverage + CI**

| Aspect | Detail |
|--------|--------|
| **Scope** | (a) Add 4 new test files: router dispatch, KPI computation, feedback-loop firing, dept-monitor thresholds. (b) Add a `tests/integration/` for end-to-end signal routing (mock cron, mock state files). (c) Wire `pytest` into pre-commit or a `make test` target. (d) Add CI workflow (GitHub Actions YAML) that runs `pytest` + `scripts/self-running-check-v2.py` on every PR |
| **Deliverables** | 4+ new test files, GitHub Actions workflow, `Makefile` (or equivalent), updated `scripts/run_tests.sh` |
| **Success** | `pytest tests/` runs in <30s with ≥ 30 tests passing. CI green on the PR that lands this phase. `scripts/self-running-check-v2.py --deep` returns 0 |
| **Rollback** | `git revert` (additive) |
| **Time** | 3–4 hours |
| **Risk** | **MEDIUM** — depends on existing tests being stable; CI config is platform-specific |
| **Greenlight** | Need your go. |

### Phase 5 — **Feedback loop runtime wiring** (the "make it real" phase)

| Aspect | Detail |
|--------|--------|
| **Scope** | (a) Add a cron job `aiw-feedback-loop-runner-15min` that evaluates feedback-loop triggers every 15 min. (b) Add `feedback_loop_runs.jsonl` log to capture every firing. (c) Hook the soul-improvement workflow into Argus's actual daily run (Argus already runs; this connects it to soul-improvement.yaml). (d) Add a `kpi-org-health-score` computation that aggregates per-dept KPIs into one number (already defined in `revenue-stack.yaml`; just wire runtime). |
| **Deliverables** | 1 new script (`scripts/feedback-loop-runner.py`), 1 new cron job, 1 new log file convention, 1 new KPI aggregator |
| **Success** | After 24h of runtime, `feedback_loop_runs.jsonl` has ≥ 90 entries (15min × 24 × estimated loop firings). At least 1 soul-improvement suggestion has been auto-generated (even if Ivan doesn't approve it). `kpi-org-health-score` shows up in `state/coord.json` |
| **Rollback** | `git revert` + remove cron entry |
| **Time** | 4–6 hours |
| **Risk** | **HIGH** — this is the moment the org goes from "designed" to "running." If a loop misfires, could spam Ivan. Recommend shadow-run for 48h before activating Ivan notifications. |
| **Greenlight** | Need your go. **Recommend starting in shadow mode (log only, no notifications) for 48h before activating full loop.** |

---

## 5 — Per-area upgrade tasks (the work, by area)

### 5.1 State (`/state/`)

| Task | Phase | Notes |
|------|-------|-------|
| Delete `*.pre-sqlite.bak` after migration verified | 1 | Pure cleanup |
| Add `state/kpis/<dept>.json` mirror of per-dept kpis.yaml (runtime values) | 2, 3 | Bridges yaml-defined KPIs to runtime values |
| Add `state/feedback_loop_runs.jsonl` | 5 | Append-only log |
| Add `state/org_health.json` (org-level KPI aggregator) | 5 | Surfaces `kpi-org-health-score` |
| Add `state/snapshots/INDEX.md` pointing to most recent per-dept snapshot | 2 | Discoverability |

### 5.2 Cron + scripts (`/scripts/`)

| Task | Phase | Notes |
|------|-------|-------|
| Delete duplicate `scripts/eval-gate-runner.sh` (root); canonical is `scripts/eval/aiw-eval-gate-runner.sh` | 1 | Pure cleanup |
| Move/deprecate `scripts/coach-onboarding-poller.py` (coaching scope) | 1 | Out of scope; document why |
| Add `scripts/feedback-loop-runner.py` | 5 | New, the loop runner |
| Add `scripts/dept-monitor-thresholds.py` (refactor of the 15 PROMPT-monitor logic into shared lib) | 4 | DRY |
| Update `scripts/cron-sync.sh` to include new cron jobs | 5 | One-time update |

### 5.3 Monitors (`/dept-monitors/`, plus per-agent `PROMPT-monitor.md`)

| Task | Phase | Notes |
|------|-------|-------|
| Update `dept-monitors/INDEX.md` master matrix to add 8 more monitors for atomic-layer agents that need watching (Argus, Hermes-router, Thoth, Echo, Clio, Cadmus, Metis, Mnemosyne) | 2, 3 | Brings monitor count from 16 → 24 |
| Add `PROMPT-monitor.md` for the 19 dept agents that lack one (currently 15/34) | 3 | Per `dept-monitors/INDEX.md` spec |
| Refactor monitor threshold logic into shared lib (used by both dept and atomic monitors) | 4 | DRY, testable |

### 5.4 PROMPTs (per-agent)

| Task | Phase | Notes |
|------|-------|-------|
| Standardize frontmatter across all 34+24 = 58 PROMPTs (single yaml schema, agent_id, version, schedule, owner, parent_spec, hard_stops, composition:) | 3 | Mechanical, but every file changes |
| Apply naming canon: portmanteau names get a `soul_name` field linking to Greek-myth canonical (e.g. `ai-ops-coordinator` → soul: `Kronos`) | 2, 3 | Non-breaking, additive |
| Add `composition:` block to dept PROMPTs that declares atomic agents called | 3 | Enforces composition discipline |
| Migrate heritage agents from `agents-prompts/` to canonical | 3 | DEMIURGE-082 |

### 5.5 Tests (`/tests/`)

| Task | Phase | Notes |
|------|-------|-------|
| Add `test_router_dispatch.py` — verifies `demiurge/router/dispatch-rules.yaml` is well-formed and matches expected signal types | 4 | |
| Add `test_kpi_computation.py` — verifies formulas in `demiurge/kpi/*.yaml` are syntactically evaluable (Python `eval` with safe globals) | 4 | |
| Add `test_feedback_loop_firing.py` — verifies trigger conditions are syntactically valid (yaml + expression parse) | 4 | |
| Add `test_dept_monitor_thresholds.py` — verifies 16 monitor specs have valid thresholds against schemas | 4 | |
| Add `test_agent_composition.py` — verifies every dept PROMPT declaring `composition:` references an existing atomic agent | 4 | Enforces composition discipline at test-time |

### 5.6 Tickets (`/tickets/`)

| Task | Phase | Notes |
|------|-------|-------|
| Create new tickets for each phase's work (one ticket per phase, with sub-tasks) | 1–5 | Single workflow, easier to track |
| Close out the 6 ACTIVE review-gate tickets (DEMIURGE-008, -015, -033, -041, -047, -054) when their phases land | 2, 3, 5 | These are review gates, not blockers |
| DEMIURGE-082 (legacy agents migration) → Phase 3 | 3 | Already a ticket |

### 5.7 Documentation (`/docs/`, `/analysis/`)

| Task | Phase | Notes |
|------|-------|-------|
| Bump `ORG-AGENTS.md` to v0.4.0 | 3 | Reflects atomic-composition discipline |
| Bump `ORCHESTRATION.md` to v0.3.0 | 3 | Reflects feedback loop runtime |
| Update `analysis/ORGANIGRAM.md` to reflect target architecture | 1 | Visual sync |
| Create `analysis/ARCHITECTURE-DIAGRAM-2026-09.md` (the diagram in §2) | 1 | Living doc |
| Update `analysis/REMAINING-TASKS-AND-WISHLIST.md` to remove completed items after each phase | 1–5 | Living doc |
| Add `analysis/FEEDBACK-LOOP-RUNTIME.md` explaining when each loop fires and what its output looks like | 5 | Operational docs |

---

## 6 — Mapping design decisions to research

> **Note**: web research on AI researchers (Karpathy/Sutton/Yao/Schaul/Andreas/etc.)
> is **deferred** until Firecrawl is enabled. Below I cite the local literature
> synthesis + DEMIURGE architecture docs that already encode the relevant patterns.
> When Firecrawl is up, this section gets expanded with primary citations.

### 6.1 The 4 invariants (from `research/org-design-literature.md`)

These are already mapped in the existing local synthesis. They drive every design
decision in this proposal:

| Invariant | Source | Applied in this proposal |
|-----------|--------|--------------------------|
| **Decision rights are explicit** | Drucker (1954), Grove (1983) | Hard stops in PROMPT frontmatter; USD thresholds in `ORG-AGENTS.md` §decision-rights (preserved); human approval gates at DEMIURGE-008/015/033/041/047 (preserved); Phase 3 adds `composition:` declarations (extending decision rights to inter-agent calls) |
| **Boundaries are exclusive** | Mintzberg (1979), Bossidy (2002) | Atomic ≠ Business composition discipline (§2.1); per-dept "owns/doesn't own" sections (preserved); Phase 3 deletes Tier-2 taxonomy to eliminate ambiguity; each dept has one canonical location |
| **Cadence beats heroics** | Grove (1983), Collins (2001) | 92 cron jobs (preserved); no cadence changes in any phase; Phase 5 adds `aiw-feedback-loop-runner-15min` as the new cadence |
| **Specialization beats generalization** | Mintzberg (1979), Organimi SMB playbook | 6 specialist depts (preserved); DEMIURGE's atomic-agent discipline = one job per agent (extended in §2.1) |

### 6.2 Patterns lifted from DEMIURGE architecture

| Pattern | DEMIURGE source | Applied in this proposal |
|---------|-----------------|--------------------------|
| **Atomic agent** (one job, composable) | `demiurge/agents/<id>/` (24 instances) | Phase 3 enforces via `composition:` frontmatter + `tests/test_agent_composition.py` |
| **Router with typed signals** | `demiurge/router/dispatch-rules.yaml`, `revenue-signals.yaml` | Phase 3 extends dept layer to declare which signals it consumes/emits |
| **Timing SLAs (ITIL P0-P3)** | `demiurge/router/document-timing-rules.yaml` | Phase 3 adds per-dept SLA definitions; Phase 5 wires `feedback-loop-runner.py` to honor SLAs |
| **KPI with formulas + feedback_loop** | `demiurge/kpi/revenue-stack.yaml` | Phase 2 extends to all 6 depts; Phase 3 mirrors at dept level |
| **Feedback loop (trigger→action→owner)** | `demiurge/feedback-loops/README.md` (4 loops) | Phase 3 adds dept-specific loops; Phase 5 wires runtime |
| **Soul-improvement with human gate** | `demiurge/feedback-loops/soul-improvement.yaml` | Phase 5 hooks into Argus's daily run; preserves Ivan approval requirement |
| **Source-grounding (lit + community)** | `sources/marketing/`, `sources/sales/`, `sources/product-discovery/` | Phase 3 creates `departments/<N>/sources/` (optional, only if content exists) |
| **Memory layers (episodic + community + operational)** | `docs/demiurge/domain-model.md` Memory Layer 2/2.5/3 | Phase 3 ensures all dept agents have operational sqlite (already do); episodic git (already do per-agent repos); community layer (not used, deferred) |

### 6.3 Research questions for Firecrawl (when enabled)

When web research is unblocked, I will pull primary sources on:

1. **Andrej Karpathy** — software 2.0 thesis, nanoGPT, agent design intuitions
2. **Richard Sutton** — "Reward is enough" (Bitter Lesson), RL foundational
3. **Shunyu Yao** — ReAct, Reflexion, Tree of Thoughts, language agents
4. **Tom Schaul** — agent foundations, environment design, intrinsically motivated agents
5. **Jacob Andreas** — composition in language models, neural module networks
6. **Vinod Narayanan** — institutional/organizational economics for AI agents (?)
7. **Satinder Singh** — transfer learning for agents, MDP formalisms
8. **Doina Precup** — options framework, temporal abstraction
9. **Michael Littman** — RL foundations, communication in agents
10. **Yoshua Bengio** — system 2 reasoning, consciousness priors for agents
11. **Yann LeCun** — JEPA, world models, energy-based agents
12. **Geoffrey Hinton** — capsule networks, forward-forward, routing intuitions
13. **David Silver / Julian Schrittwieser** — AlphaZero, MuZero, search + learning
14. **Noam Brown** — poker, multi-agent equilibrium, Libratus/Pluribus
15. **Dylan Hadfield-Menell** — cooperative AI, principal-agent problems for AI
16. **Anca Dragan** — value alignment, specification gaming
17. **Paul Christiano** — amplification, debate, IDA
18. **Jan Leike / Shane Legg** — DeepMind safety, scalable oversight
19. **Dario Amodei / Chris Olah** — mechanistic interpretability, agent accountability
20. **François Chollet** — ARC, measure of intelligence, program synthesis

These citations will be folded into this section before final proposal signoff.

---

## 7 — Risk analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| P0 secret leaks remain open during upgrade | HIGH | None on upgrade, but platform can't go "production" with leaks | Parallel track (you closing P0s, me upgrading); don't claim "production" until P0s closed |
| PROMPT frontmatter standardization breaks agents | MED | Agents fail to load / cron fires fail | Phase 3 is incremental, one dept at a time, with per-dept checkpoint + smoke test (`scripts/self-running-check-v2.py`) |
| Feedback loop misfires (Phase 5) | MED | Spam Ivan, false positives | Phase 5 starts in **shadow mode** (log only, no notifications) for 48h before activation |
| Deleting Tier-2 taxonomy loses content | LOW | Confusion, lost work | Phase 1 first audits all 8 dept files for unique content; only delete after migration |
| Heritage agent migration breaks state files | LOW | Agents can't read old state | Phase 3 includes a one-time backfill script: `agents-prompts/<id>/state.json` → `demiurge/agents/<id>/state.json` |
| Test additions don't catch the right regressions | MED | False confidence in CI | Phase 4 includes manual smoke tests of each new test file |
| Cron collision from new `feedback-loop-runner-15min` | LOW | Cron contention, missed jobs | Verify against `scripts/grid.sh` before adding |

---

## 8 — Rollback plan (per phase)

| Phase | Rollback command | Time to rollback |
|-------|------------------|------------------|
| 1 | `git revert <phase-1-commit>` | 1 min |
| 2 | `git revert <phase-2-commit>` (all additive, safe) | 1 min |
| 3 | `git revert <phase-3-commit>` (frontmatter changes reversible; check per-dept) | 5–15 min, depends on how many commits |
| 4 | `git revert <phase-4-commit>` + delete CI workflow file | 2 min |
| 5 | `git revert <phase-5-commit>` + `hermes cron remove aiw-feedback-loop-runner-15min` + delete `state/feedback_loop_runs.jsonl` | 5 min |

---

## 9 — Success criteria (post-rollout)

After all 5 phases complete and run for 7 days, the org should hit:

| Criterion | How to measure | Target |
|-----------|----------------|--------|
| All 24 DEMIURGE agents have `agent.yaml` | `find demiurge/agents -name agent.yaml | wc -l` | 24 |
| All 6 depts have `kpis.yaml` | `find departments -name kpis.yaml | wc -l` | 6 |
| All dept PROMPTs declare `composition:` | `grep -l "composition:" departments/*/PROMPT.md | wc -l` | ≥ 30 |
| Feedback loop log has entries | `wc -l state/feedback_loop_runs.jsonl` | ≥ 90 (15min × 24h × fires) |
| Org health score surfaces in state | `jq .org_health_score state/coord.json` | non-null |
| Test suite passes | `pytest tests/` | 0 failures |
| Self-running check passes | `scripts/self-running-check-v2.py` | exit 0 |
| No `*.pre-sqlite.bak` leftovers | `find state -name "*.bak"` | 0 |
| Tier-2 taxonomy deleted | `ls departments-taxonomy/` | "No such file" |
| Heritage agents migrated | `ls agents-prompts/` | empty or DELETED |

---

## 10 — Appendix: Research limitations

### What's missing from this proposal

**Web research on 20-30 AI researchers** (Karpathy, Sutton, Yao, Schaul, Andreas,
Narayanan, LeCun, Bengio, Hinton, Silver, Schrittwieser, Brown, Precup, Littman,
Hadfield-Menell, Dragan, Christiano, Leike/Legg, Amodei/Olah, Chollet, etc.)
is **deferred pending Firecrawl enablement**.

The local literature synthesis (`research/org-design-literature.md`, 318 lines)
covers classic management literature (Drucker, Grove, Bossidy, Collins, Mintzberg,
Peters, Blank) but not the AI-researcher-side literature on multi-agent design.

Once Firecrawl is configured, I will:

1. Run `web_search` for each of the ~20 researchers with their agent/multi-agent
   /orchestration/eval work.
2. Fold citations into §6.3 of this doc.
3. Add a §6.4 "Cross-validation: AIW design vs published patterns" that maps our
   choices to specific papers/blog posts.
4. Re-submit the proposal for final signoff.

**No code will be touched in any phase until you greenlight that phase.**

---

## 11 — Appendix: What you should decide now

Three things only:

1. **Approve this proposal in principle** (or push back on the phasing/architecture).
2. **Greenlight Phase 1** (cleanup only, 30 min, zero risk) — or specify a different starting phase.
3. **Decide on Firecrawl** — when can web research happen? If you can flip it on now,
   I do §6.3 in parallel with Phase 1.

Everything else waits for per-phase greenlight.

---

**Document version**: 1.0.0 — 2026-09-01
**Author**: Hermes (Ivan's session)
**Status**: AWAITING REVIEW
**Next review**: After Ivan's feedback on §3, §4, §7, and §11