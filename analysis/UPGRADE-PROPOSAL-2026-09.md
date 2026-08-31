# AIW Org Upgrade Proposal — 2026-09

> **Status**: DRAFT v1.3.0, awaiting Ivan's approval for Layer 1 greenlight.
> **Date**: 2026-09-01
> **Scope**: `aiw-org` repo. **Excludes** `coach/` (moved to `growth-coaching` repo) and all sister repos.
> **Method**: Local diagnostic + literature grounded in
> `research/org-design-literature.md` + DEMIURGE architecture docs + `analysis/`
> catalog + **comprehensive web research** across 27 sources in 3 streams
> (classic canon + SMB frameworks + AI researchers). See
> `analysis/RESEARCH-CITATIONS-2026-09.md` for primary sources.
>
> **v1.3.0 changes**: Reframed from "production-grade" to "production prep."
> Phases 1-4 now organized as 4 sequential layers (operational hygiene →
> structural foundation → quality infrastructure → conditional adaptive layer).
> Phase 5 (feedback-loop runtime) is now **out of scope** until customer
> traction emerges + Ivan's staged soul-improvement gate (§12) is satisfied.
> Authoritative execution doc: `EXECUTION-SCOPE-2026-09.md`.

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
| **Risk** | **HIGH** — this is the moment the org goes from "designed" to "running." If a loop misfires, could spam Ivan. Recommend **shadow mode for 7 days** before activating Ivan notifications (extended from initial 48h estimate after research pass — Brown + Silver both emphasize interactions matter more than components, so observing the *interactions* between feedback loops needs longer than the components alone). |
| **Greenlight** | Need your go. **Recommend starting in shadow mode (log only, no notifications) for 7 days before activating full loop.** |

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

### 6.3 Research findings (10/10 surveyed, top-relevant)

> **Full citations + extracted patterns**: see
> `analysis/RESEARCH-CITATIONS-2026-09.md` for primary sources, direct quotes, and
> per-researcher application tables. This section is the **mapping back** to the
> upgrade phases.

Researchers surveyed (in this order):
**Karpathy, Sutton, Yao, Schaul, Andreas, LeCun, Bengio, Silver, Brown, Christiano**.
Top 10 focused on multi-agent / orchestration / eval relevance per Ivan's "(b)" choice.
The full original list of 20 + 10 additional researchers deferred (see §10 Appendix:
acknowledged gaps).

### 6.3.1 Eight cross-cutting patterns synthesized

After reviewing all 27 sources across 3 streams (classic canon + SMB frameworks + AI researchers), **8 patterns** emerge that map to specific phases of this upgrade:

| # | Pattern | Sources | Maps to phase |
|---|---------|---------|---------------|
| 1 | **Atomic composition**: small primitives compose into larger capabilities | Andreas (NMN), Yao (ReAct/CoALA), Christiano (IDA), **Team Topologies (Platform/Stream-aligned)**, **Mintzberg (adhocracy)** | **Phase 3** — `composition:` + `topology:` block |
| 2 | **Search + learning**: agents both explore options AND improve from outcomes | Sutton (Bitter Lesson), Silver (AlphaZero/MuZero), Karpathy (Software 2.0/3.0), **Grove (Manager Output Equation)**, **EOS (Traction)** | **Phase 5** — feedback loop runtime |
| 3 | **Hierarchical abstraction**: agents at different levels manipulate different kinds of representations | Bengio (System 2), LeCun (H-JEPA), **Precup (Options / Time scales)**, **Larson (3 systems)**, **Mintzberg (Fly)** | **Phase 3** — `layer:` frontmatter |
| 4 | **Embedded oversight**: agents operating on themselves / each other need explicit human gates | Schaul (Agent Foundations), Christiano (Alignment via Amplification), Brown (Strategic Interactions), **Leike (Scalable Oversight)**, **Hadfield-Menell (CIRL)** | **Phase 5** — preserves Ivan approval in soul-improvement |
| 5 | **Reflection & revision**: agents should record what went wrong and adapt | Yao (Reflexion, CoALA), Karpathy (LLM Wiki), Sutton (learn-by-search), **Hinton (Forward-Forward negative pass)**, **Olah (Mechanistic Interpretability)** | **Phase 5** — outbox + state + soul-improvement |
| 6 | **Professional + Adhocratic hybrid**: org is professional at dept layer (experts with autonomy), adhocratic at atomic layer (innovation engine) | **Mintzberg (Professional/Adhocracy)**, **Team Topologies**, **Christensen (Autonomous org)** | **Phase 1** — preserve; document explicitly |
| 7 | **Multi-time-scale operation**: every org runs at multiple time scales simultaneously | **Precup (Options)**, **Grove (cadence)**, **Shape Up (6-week cycles)**, **AIW cron grid**, **Larson (eng/ops/infra)** | **Phase 3** — document in cadence-map |
| 8 | **Right People in Right Seats**: agents have explicit competence boundaries; escalate outside them | **Wickman (EOS People)**, **Collins (First Who)**, **Grove (TRM)**, **Hadfield-Menell (CIRL)** | **Phase 3** — `composition:` block + `archetype:` field |

### 6.3.2 Pattern-by-pattern application

#### Pattern 1 — Atomic composition (Phase 3)

> Andreas: "Modular architectures support compositional adaptation: a system can
> compose modules to address a task, decompose a composition when its parts no
> longer fit."
>
> Yao (CoALA): agents have a memory, an action space, a decision-making process —
> and the action space IS the composition of available modules.
>
> Christiano (IDA): amplification via task decomposition is the alignment-preserving
> way to build powerful agents.

**Applied as**: Phase 3's `composition:` block in dept PROMPT frontmatter. Every
dept agent declares which atomic agents it composes. This makes the composition
explicit, testable, and versionable.

#### Pattern 2 — Search + learning (Phase 5)

> Sutton (Bitter Lesson): "general methods that leverage computation are ultimately
> the most effective... search and learning are the two most important classes of
> techniques for utilizing massive amounts of computation."
>
> Silver (AlphaZero/MuZero): combine tree search with self-play learning — neither
> alone is enough.
>
> Karpathy (Software 2.0): "specify some goal... write a rough skeleton of the code...
> use the computational resources at our disposal to search this space for a program
> that works."

**Applied as**: Phase 5's `feedback-loop-runner.py` runs every 15 min. The runner
is the "search" — it explores which feedback loops should fire based on current KPI
values. The state files + outbox accumulation is the "learning" — agents improve
across runs. Neither alone produces a self-improving org.

#### Pattern 3 — Hierarchical abstraction (Phase 3)

> Bengio (System 2): "System 2 requirements will put pressure on representation
> learning to discover the kind of high-level concepts which humans manipulate with
> conscious thought."
>
> LeCun (H-JEPA): "configurable predictive world model, behavior driven through
> intrinsic motivation, and hierarchical joint embedding architectures trained with
> self-supervised learning."

**Applied as**: Phase 3 adds `layer: atomic | business | governance` to PROMPT
frontmatter. Each agent declares its abstraction level. Atomic agents manipulate
atomic concepts (signals, KPIs, individual files). Business agents manipulate dept
concepts (leads, deals, invoices). Governance agents manipulate org concepts
(decisions, escalations, constitution).

#### Pattern 4 — Embedded oversight (Phase 5)

> Schaul (Agent Foundations): "agents are part of the world they reason about"
> — embedded agency requires explicit handling of self-reference.
>
> Christiano (IDA alignment): "the amplified agent stays aligned because each
> distillation step is overseen."
>
> Brown (Pluribus): success in multi-agent systems comes from getting the
> interactions right, not just individual agent quality.

**Applied as**: Phase 5 preserves the `human:ivan` approval gate in soul-improvement.
The feedback-loop runner can SUGGEST soul revisions, but cannot apply them. This is
the explicit acknowledgment that AIW agents modifying each other (and themselves)
require human oversight — Brown + Schaul + Christiano all point to this.

#### Pattern 5 — Reflection & revision (Phase 5)

> Yao (Reflexion): agents reflect verbally on their failures and store reflections
> in memory, improving on subsequent attempts.
>
> Yao (CoALA): agents have explicit memory layers including episodic reflection.
>
> Karpathy (LLM Wiki): "schema is always the system prompt and the user message
> carries the current wiki content plus whatever the operation needs."

**Applied as**: Phase 5's feedback loop captures each firing event in
`state/feedback_loop_runs.jsonl` — the org's episodic reflection memory. Phase 3
extends PROMPT template with a "lessons learned" section. Combined: every AIW
agent has a structured place to reflect + a memory layer that persists across runs.

#### Pattern 6 — Professional + Adhocratic hybrid (Phase 1, document only)

> Mintzberg (1979): 5 organizational configurations — Entrepreneurial, Machine
> Bureaucracy, Professional, Divisional, Adhocracy. AI-native companies will trend
> toward Adhocracy.
>
> Team Topologies (2019): stream-aligned teams (business-flow-aligned) vs platform
> teams (infrastructure-as-a-product). The split is exactly our dept/atomic split.
>
> Christensen (1997): disruptive orgs must be autonomous to avoid being judged by
> incumbent metrics.

**Applied as**: Phase 1 explicitly documents in `ORG-AGENTS.md` that AIW is a
**Professional configuration at the dept layer** (experts with autonomy, standardized
inputs/outputs) and an **Adhocratic / Platform configuration at the atomic layer**
(project-based, multidisciplinary). This validates the architecture as the
literature-consistent answer, not a workaround. **Phase 1 also adds a
`topology:` field to agent.yaml** per Team Topologies:
`stream-aligned | platform | enabling | complicated-subsystem`.

**Per-dept mapping to Mintzberg configurations**:

| Dept | Mintzberg config | Team Topologies equivalent |
|------|------------------|----------------------------|
| 01-operations | Professional + Machine (mixed) | Stream-aligned + Platform |
| 02-finance-legal | Machine Bureaucracy (compliance rules) | Complicated Subsystem |
| 03-sales-growth | Professional + Adhocratic | Stream-aligned (revenue stream) |
| 04-engineering | Adhocratic | Stream-aligned + Platform |
| 05-research-education | Adhocratic | Enabling + Complicated Subsystem |
| 06-people-culture | Professional | Stream-aligned |

#### Pattern 7 — Multi-time-scale operation (Phase 3, document)

> Precup/Sutton/Singh (1999) — Options framework: temporally extended actions
> over multiple time scales.
>
> Grove (1983) — Manager output = sum across activities at different cadences.
>
> Shape Up (2019) — 6-week cycles + daily standups + quarterly planning.
>
> AIW's cron grid already has 5min/15min/30min/daily/weekly/monthly/quarterly.

**Applied as**: Phase 3 adds an explicit time-scale hierarchy section to
`ORG-AGENTS.md`. This makes the implicit options framework visible and lets us
audit it. **Adds `time_scale:` field to PROMPT frontmatter** per agent:
`seconds | minutes | hours | days | weeks | months | quarters`. Documents the
cron-vs-options correspondence:

| Cron | Time scale | Option equivalent |
|------|-----------|------------------|
| `health.sh` every 5min | seconds | "system heartbeat option" |
| `heartbeat-alerts-15min` | minutes | "near-real-time monitoring" |
| `daily-brief` 06:00 | days | "morning intelligence option" |
| `engineering-roster` Tue/Fri | days | "weekly velocity review" |
| `finance-controller` Fri | weeks | "weekly cash position" |
| `board-of-directors` quarterly | quarters | "strategic review option" |

#### Pattern 8 — Right People in Right Seats (Phase 3)

> Wickman (EOS) — "Right People in the Right Seats" — every position needs someone
> who understands the vision and has the ability.
>
> Collins — "First Who Then What" — get the right people on the bus *before* deciding
> where to drive it.
>
> Grove — Task-Relevant Maturity (TRM) — same person has high TRM for familiar work,
> low TRM for new responsibilities.
>
> Hadfield-Menell (CIRL) — agents don't fully know Ivan's true reward function; they
> must learn it via feedback.

**Applied as**: Phase 3's `composition:` block (Pattern 1) is the "right seat"
declaration. **Phase 3 also adds `archetype:` field to PROMPT frontmatter** per
Larson (Pattern 6 + 8): `team-lead | architect | solver | right-hand | specialist`.
Combined with `topology:` (Pattern 6) and `composition:` (Pattern 1), every agent
declares its archetype, its position in the org topology, and which atomic agents
it calls. This is the operational realization of "right people in right seats."

### 6.3.3 What the research DELTA'd in the original proposal

Two design decisions **changed** after the v1 research pass:

1. **Phase 3 PROMPT frontmatter** now includes `layer:` (atomic/business/governance)
   field — added per LeCun + Bengio's hierarchical-abstraction pattern. Was not in
   the original proposal.

2. **Phase 5 shadow-mode period** extended from 48h to 7 days for the new
   feedback-loop-runner. Reasoning: Brown + Silver both emphasize that the
   interactions matter more than the components, and the current proposal had only
   48h of shadow-mode observation — too short to observe the *interactions*
   between feedback loops. Updated in §4 Phase 5.

One design decision **rejected**:

3. **Standing pull permission for secrets**: I had wanted to build a credential-
   loader workflow mid-upgrade. The research pass doesn't change this — per Schaul
   (embedded agency) and Christiano (amplification needs oversight), a bot pulling
   vault items on its own initiative is exactly the kind of agent-modifying-itself
   pattern that needs a human gate. **The loader workflow is out of scope for this
   upgrade; if it gets built, it gets its own design + review.**

Five design decisions **added** after the v2 comprehensive research pass:

4. **`topology:` field** (Phase 3 PROMPT frontmatter) — `stream-aligned | platform
   | enabling | complicated-subsystem`. Per Team Topologies' 4-team-type model.
   Maps AIW's dept layer to stream-aligned + the DEMIURGE atomic layer to platform.
   Per Pattern 6.

5. **`archetype:` field** (Phase 3 PROMPT frontmatter) — `team-lead | architect |
   solver | right-hand | specialist`. Per Will Larson's staff-eng archetypes.
   Identifies what KIND of agent each is, not just what it does. Per Pattern 8.

6. **`intent_mismatch:` field** in feedback loop runs (Phase 5). Per Hadfield-Menell's
   CIRL — distinguishes formal KPI breach from informal Ivan-dislikes-this. Per
   Pattern 4.

7. **Spec-gaming tests in Phase 4** — at least one test per agent asserting "you
   cannot game your KPI by [known gaming pattern]." Per Anca Dragan's reward
   hacking research. Dragan's audit table is in the citations file (§C5).

8. **Time-scale hierarchy documented** in `ORG-AGENTS.md` §cadence-map (Phase 3).
   Adds `time_scale:` field to PROMPT frontmatter (`seconds | minutes | hours |
   days | weeks | months | quarters`). Maps cron schedules to Precup's Options
   framework. Per Pattern 7.

**Updated PROMPT frontmatter schema** (Phase 3, additive only):

```yaml
---
name: <agent-id>
version: <semver>
schedule: <cron>
owner: <human>
parent_spec: <path/to/charter>
state_db: <path>
fallback_model: <model>

# NEW v1 (research)
layer: atomic | business | governance      # Pattern 3 — LeCun/Bengio

# NEW v2 (comprehensive)
topology: stream-aligned | platform | enabling | complicated-subsystem   # Pattern 6 — Team Topologies
archetype: team-lead | architect | solver | right-hand | specialist     # Pattern 8 — Larson
time_scale: seconds | minutes | hours | days | weeks | months | quarters   # Pattern 7 — Precup

# NEW v2 (per agent type)
composition: [<atomic-agent-id>, ...]       # Pattern 1 — Andreas/Christiano
negative_examples: ["do NOT ..."]           # Pattern 5 — Hinton
transfer_targets: [<agent-id>, ...]         # Pattern 4 — Singh

hard_stops:
  - action: <verb>
    require_approval: bool
    approved_human: <who>
---
```

**Total DELTAs**: **8 design additions** (2 from v1 + 5 from v2 + 1 negative
from §6.3.3 secret-loader) + **2 design changes** (shadow mode 48h→7d;
heritage agent migration now explicitly DEMIURGE-082). None of these are
breaking changes to existing PROMPT files — they are all additive fields
with sensible defaults.

### 6.3.4 Citations file

The full citations + per-researcher application tables live at
`analysis/RESEARCH-CITATIONS-2026-09.md`. URL index:

- Karpathy: https://karpathy.medium.com/software-2-0-a64152b37c35
- Sutton: http://www.incompleteideas.net/IncIdeas/BitterLesson.html
- Yao: https://arxiv.org/abs/2210.03629 + https://ysymyth.github.io/
- Schaul: https://arxiv.org/pdf/1811.07871
- Andreas: https://arxiv.org/html/1511.02799v4
- LeCun: https://openreview.net/pdf?id=BZ5a1r-kVsf
- Bengio: https://neurips.cc/virtual/2019/invited-talk/15488
- Silver: https://www.youtube.com/watch?v=uPUEq8d73JI
- Brown: https://www.science.org/doi/10.1126/science.aay2400
- Christiano: https://arxiv.org/pdf/1810.08575.pdf

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

## 10 — Appendix: Research summary

### What changed since draft v1.0.0

**v1.0.0** of this proposal was drafted with Firecrawl disabled, citing only the
local literature synthesis (`research/org-design-literature.md`, 318 lines,
covering classic management literature — Drucker, Grove, Bossidy, Collins,
Mintzberg, Peters, Blank).

**v1.1.0** (this revision) folds in web-grounded primary sources for the 10
researchers Ivan selected: **Karpathy, Sutton, Yao, Schaul, Andreas, LeCun,
Bengio, Silver, Brown, Christiano**. Full citations + extracted patterns +
per-researcher application tables live at `analysis/RESEARCH-CITATIONS-2026-09.md`.
Mapping back to upgrade phases is in §6.3.

### What's still missing (acknowledged gaps)

**10 additional researchers** were in the original §6.3 list but deferred per
Ivan's "(b) Top 10 only" choice. They remain available via the same Firecrawl
path if a future revision needs them:

- Doina Precup — options framework, temporal abstraction
- Satinder Singh — transfer learning for agents, MDP formalisms
- Michael Littman — RL foundations, communication in agents
- Geoffrey Hinton — capsule networks, forward-forward, routing intuitions
- Dylan Hadfield-Menell — cooperative AI, principal-agent problems for AI
- Anca Dragan — value alignment, specification gaming
- Jan Leike / Shane Legg — DeepMind safety, scalable oversight
- Dario Amodei / Chris Olah — mechanistic interpretability, agent accountability
- François Chollet — ARC, measure of intelligence, program synthesis
- Vinod Narayanan (placeholder; intended to refer to institutional economics
  literature for AI org design — confirm researcher name in v1.2 if pursued)

---

## 11 — Appendix: What you should decide now

Three things only:

1. **Approve this proposal in principle** (or push back on the phasing/architecture).
2. **Greenlight Phase 1** (cleanup only, 30 min, zero risk) — or specify a different starting phase.
3. **Decide on Firecrawl** — when can web research happen? If you can flip it on now,
   I do §6.3 in parallel with Phase 1.

Everything else waits for per-phase greenlight.

---

## 12 — Staged soul-improvement gate (added in v1.3.0)

**Phase 5 (feedback-loop runtime + auto soul revisions) is explicitly OUT OF SCOPE
for this upgrade.** The Layer 4 (Adaptive) work in `EXECUTION-SCOPE-2026-09.md`
covers feedback loops for *monitoring and alerting* only — never for *soul
modification*. Soul-improvement is a separate, gated capability that requires
its own decision tree, which is formalized here.

### Why this gate exists

Soul-improvement lets agents modify their own `PROMPT.md`. This is the
highest-blast-radius capability in any agent system. Per the Phase5 risks in
§4 and Pattern 4 in §6.3 (Schaul's embedded agency, Christiano's amplification
needs oversight), auto-modification without human-in-the-loop is a category of
risk that justifies a dedicated gate.

### Per-Ivan directive (2026-09-01)

Ivan's explicit rule: *"we can improve the soul but only once we know we should
do it and it will be fine and a test edit of a soul works and is stable and
efficient not all souls at once and not the main soul we use first."*

Translated into a 4-stage gate:

| Stage | Gate | Duration | What we test | Exit criteria |
|-------|------|----------|--------------|---------------|
| **1. Test edit on a non-main soul** | `soul-improvement-test-harness.py` runs against a sandbox agent (NOT in `demiurge/agents/`, NOT in `departments/`). Edit a copy, observe behavior change, verify rollback works. | 1 week | Soul-edit mechanics work; rollback is clean; no PROMPT.md corruption outside sandbox | Test harness passes 100% of cases; rollback verified by hash diff |
| **2. Apply to ONE non-main soul, observe** | Pick the lowest-stakes demiurge agent (e.g. `orpheus-recordings-agent` — audio transcription, no customer-facing output). Enable soul-improvement in shadow mode (writes proposals, never modifies). After 7 days, review proposal quality. | 1 week | Real-world soul-improvement suggestions are sensible | 0 corrupt proposals; ≥80% of proposals make semantic sense to a human reviewer |
| **3. Graduated rollout to MORE non-main souls** | Enable soul-improvement in active mode for `orpheus` + 2-3 other low-stakes agents. Each gets 7-day observation. | 2-3 weeks | Active soul revisions improve agent behavior without breaking it | KPI movement ≥+5% on each agent; 0 regressions; ≤1 Ivan review/week per agent |
| **4. Main souls only after proof** | Only enable soul-improvement for primary dept agents (`management-coordinator`, `engineering-roster`, etc) AFTER ≥3 stages-3 agents are running smoothly AND ≥1 paying customer uses aiw-org features in production. | 2-4 weeks | Main agents don't break; customer experience unaffected | Customer-facing KPIs stable; 0 critical incidents attributable to soul-improvement |

**Critical rule**: at no stage is soul-improvement enabled for the "main soul
we use first" — meaning the agents that handle customer-facing work, the
constitution, or the feedback loops themselves.

### Per-stage rollback

| Stage | Rollback command | Time-to-rollback |
|-------|------------------|-------------------|
| 1 | `git revert <commit>` | <5 min |
| 2 | Disable soul-improvement in Argus PROMPT | <30 min |
| 3 | Per-agent disable via new `soul_improvement_enabled: false` flag | <5 min per agent |
| 4 | Org-wide kill-switch: `hermes cron disable aiw-soul-improver` (new cron job, defined in Layer 4) | <1 min |

### What this gate does NOT cover

- Phase 1-4 of the upgrade (cleanup, atomic-layer completion, business-layer integration, tests) — these proceed unconditionally
- Layer 4 (Adaptive) from the execution scope — feedback loops for MONITORING, not for soul editing
- The "AI self-fixes" doctrine from the EXECUTION-SCOPE — soul-improvement is NOT self-fixing; it requires the staged gate above

### What triggers re-evaluation of the gate

If any of these happen, the gate re-opens from Stage 1:
- A new AI model release that makes soul-improvement qualitatively safer (e.g. built-in constitutional AI with formal verification)
- A formal verification framework for soul changes becomes available
- An external security audit concludes soul-improvement is safe under certain conditions
- Ivan explicitly requests re-evaluation

---

**Document version**: 1.3.0 — 2026-09-01 (4-layer framing, Phase5 deferred, §12 staged soul gate)
**Author**: Hermes (Ivan's session)
**Status**: AWAITING REVIEW (Layer 1 greenlight pending)
**Next review**: After Ivan's feedback on §3, §4, §7, §11, §12
**Companions**:
- `analysis/RESEARCH-CITATIONS-2026-09.md` (27 sources, 3 streams)
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (52-gap audit)
- `analysis/EXECUTION-SCOPE-2026-09.md` (authoritative execution doc — Layer 1-4 scope)