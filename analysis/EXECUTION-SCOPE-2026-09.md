# AIW Org Production Prep — Execution Scope

> **Status**: AUTHORITATIVE. This is the binding execution doc for the
> `aiw-org` upgrade as of 2026-09-01.
>
> **Companion docs** (read in this order):
> 1. `UPGRADE-PROPOSAL-2026-09.md` v1.3.0 — architectural design + §12 staged soul gate
> 2. `RESEARCH-CITATIONS-2026-09.md` — 27 sources, 3 streams of grounding research
> 3. `GAP-RESEARCH-FINDINGS-2026-09.md` — 52-gap audit, what the data actually shows
> 4. `PRE-WORK-GAP-ANALYSIS-2026-09.md` — pre-work, 13-hat analysis
>
> **Decision summary**: Ivan is solo (Kiki busy/offline). No customers — purely
> internal. Phase 5 (feedback-loop runtime + auto soul revisions) is OUT OF
> SCOPE. The complete solution is **3 unconditional layers + 1 conditional
> adaptive layer deferred until customer traction**.

---

## 0 — Operating principles

These apply to every layer. They are not negotiable without re-decision.

### Doctrine 1 — AI self-fixes when it can

**Default behavior**: AI analyzes logs, identifies root cause, applies the
fix, validates the fix, commits, documents. **Escalates only when it can't.**

Per Ivan (2026-09-01): *"no need for ivan to say to ai analyze the logs and fix
it should know to do that."*

| AI can fix autonomously | AI pauses and asks Ivan |
|------------------------|------------------------|
| Wrong regex in a validator script | Architectural decision (e.g. "add a new field") |
| Outdated dependency in requirements.txt | New agent creation (more than one file change) |
| Frontmatter schema violation across PROMPTs | Modifying hard_stops (security-relevant) |
| Cron job drift (jobs.json vs .hermes) | Touching secrets or BWS values |
| State file schema violations | Soul-improvement (per §12 staged gate) |
| Documentation inconsistency | Anything in `growth-coaching` repo |
| Outbox retention cleanup | Anything customer-facing |
| .gitignore that doesn't match git patterns | Cross-repo coordination |
| Test failures from regression | Anything outside aiw-org repo |

### Doctrine 2 — Per-layer scope docs

Before starting a layer, write `LAYER-N-NAME-SCOPE.md` with:
- Full task list with acceptance criteria per task
- Per-task rollback plan
- Smoke-test gate definition (per layer 3 deliverable)
- Files affected (estimated)
- Tokens-to-execute estimate
- Dependencies on previous layers

### Doctrine 3 — Per-layer runbook for human actions

Operator actions (web console clicks, etc.) get a `LAYER-N-NAME-RUNBOOK.md`:
- Step-by-step instructions
- Console URLs
- Expected outcome per step
- Verification command

### Doctrine 4 — Reporting cadence

- **Granular commits** (every meaningful state change)
- **Weekly summary** (Sunday): what's done, what's next, blockers, time spent
- **Per-layer completion report** (one document at end of each layer): what shipped, what didn't, lessons learned

### Doctrine 5 — When in doubt, pause

- **Small decisions**: AI proceeds with documented defaults; surfaces in commit message
- **Big decisions**: AI pauses and asks Ivan (architectural, cross-repo, soul-improvement, anything that touches customer-facing systems, anything outside aiw-org repo)

---

## 1 — The 4 layers (complete solution)

### Layer 1 — Operational Hygiene
**Time estimate**: 5-7h total | **Reversibility**: Full | **AI does**: ~3-4h | **Ivan does**: ~2-3h

Goal: stop the bleeding. Close P0 leaks, fix known-broken incidents, restart dead services, capture baseline metrics.

### Layer 2 — Structural Foundation
**Time estimate**: 14-22h | **Reversibility**: Full per phase | **AI does**: ~12-18h | **Ivan does**: ~2-4h review/approve

Goal: lift the 3-tier atomic/business/governance architecture from aspirational to enforced. The original proposal's Phase 1-3 work.

### Layer 3 — Quality Infrastructure
**Time estimate**: 8-12h | **Reversibility**: Full | **AI does**: ~7-10h | **Ivan does**: ~1-2h review

Goal: make the system *measurable*. Tests, eval gates, smoke-test gates per phase.

### Layer 4 — Adaptive Layer (CONDITIONAL, deferred)
**Time estimate**: 10-15h | **Reversibility**: Partial (kill-switch design required) | **AI does**: ~9-13h | **Ivan does**: ~1-2h

Goal: feedback loops for MONITORING (not soul-improvement). **Only proceeds when**:
- ≥1 paying customer uses aiw-org features (today: 0)
- OR Ivan explicitly requests activation with the §12 staged gate satisfied

**Soul-improvement is NOT part of Layer 4.** It is its own gated capability per proposal §12.

---

## 2 — Weekly breakdown (Ivan-pacing-friendly)

Per Ivan's preference for weekly blocks, here's how each layer fits:

| Week | Layer | Tasks | Ivan hours | AI hours | Deliverable |
|------|-------|-------|-----------|----------|-------------|
| **W1** | Layer 1 (5-7h) | P0 leaks + incidents + wrangler + baseline | 2-3h | 3-4h | All known-broken things fixed; metrics baseline captured |
| **W2** | Layer 2a (6-9h) | Cleanup: tier-2 taxonomy delete, playbook dedup, .gitignore fix, linter, 14 agent.yaml fills | 1h review | 5-8h | Tech debt eliminated; all demiurge agents have metadata |
| **W3** | Layer 2b (4-6h) | Frontmatter standardization (8 new fields × 58 PROMPTs) | 1h review | 3-5h | All PROMPTs have layer/topology/archetype/composition/etc. |
| **W4** | Layer 2c (4-7h) | Business-layer integration: atomic→dept signals, dept→atomic composition | 1h review | 3-6h | All dept agents call atomic agents correctly |
| **W5** | Layer 3 (8-12h) | Test scaffolding + eval gates + per-phase smoke-test gates | 1-2h review | 7-10h | System has regression coverage |
| **W6** | (idle / review) | — | — | — | Buffer week for unknowns |
| **W7+** | Layer 4 (conditional) | Only if gates met | — | — | (see §3 below) |
| **TOTAL** | | | **7-9h** | **21-33h** | Complete solution in 5 weeks (if Layer 4 deferred) |

### Pace assumption
- **AI works continuously** (autonomous loops, scripts, file ops)
- **Ivan does light review**: 1-2h/week, mostly reading commits + approving per-layer greenlight + answering occasional questions
- **No weekend work** unless Ivan requests

---

## 3 — Layer 4 conditional triggers

Layer 4 (Adaptive) proceeds ONLY if all of these are met:

1. **Customer traction**: ≥1 paying customer uses an aiw-org-managed feature in production
2. **Operational stability**: Layers 1-3 deliverables stable for 7+ consecutive days
3. **Quality gates**: Per-phase smoke-test pass rate ≥95% over the last 14 days
4. **Soul-improvement gate**: Per proposal §12, soul-improvement is NEVER in Layer 4. Layer 4 is feedback loops for MONITORING only. Soul-improvement has its own 4-stage gate.

**If Layer 4 triggers are NOT met by W7**: scrap Layer 4 entirely. Layers 1-3 stand on their own. Re-evaluate quarterly.

---

## 4 — Per-layer execution checklist

Each layer has the same skeleton. The actual content lives in `LAYER-N-NAME-SCOPE.md`.

### Common tasks (every layer)

- [ ] Read prior layer's completion report
- [ ] Write/update `LAYER-N-NAME-SCOPE.md`
- [ ] Run smoke-test gate from previous layer
- [ ] All hard_stops enforced (per Layer 3 scope)
- [ ] All changes committed granularly (per Doctrine 4)
- [ ] End-of-layer report written and committed
- [ ] No untracked files at commit time (per `.gitignore`)
- [ ] Pre-commit hook passes (cron-sync clean)

---

## 5 — Risks (forward-looking)

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| AI overcommits and breaks substrate | Low | Medium | Per-phase greenlight + per-phase smoke-test gates |
| Ivan unavailable mid-layer | Low | Medium | Each layer's deliverables are independently committable; AI can pause |
| Cost exceeds budget | Low | Low | Cost-tracker.py is existing; Layer 1 includes baseline |
| Customer emerges mid-layer | Low | High | Layer 4 conditional; existing Foundation work is customer-ready |
| Kiki becomes available mid-layer | Low | Medium | Could parallelize Layer 3 work; AI can defer to AI while Kiki does operator parts |
| New P0 leak emerges mid-layer | Medium | Medium | Doctrine 1: AI fixes what it can; pause for big issues |

---

## 6 — What this doc is NOT

- **Not** a sales pitch for "production-grade" — Ivan explicitly rejected that framing
- **Not** a research proposal — see `RESEARCH-CITATIONS-2026-09.md` for research
- **Not** a gap analysis — see `GAP-RESEARCH-FINDINGS-2026-09.md` for that
- **Not** a decision record — see `DECISIONS-2026-Q3.md` for ratified decisions

This IS the execution plan. It says what we're doing, in what order, by when,
and what gates each piece behind.

---

## 7 — When this doc gets updated

- When a layer starts (add scope doc reference)
- When a layer completes (add completion report reference)
- When Ivan changes scope (update layer definitions)
- When a new gate condition emerges (add to §3)
- Never without Ivan's review of the change

---

## 8 — Appendix: Quick reference

### The 3 layers that always run (unconditional)

1. **Layer 1** — `LAYER-1-HYGIENE-SCOPE.md` + `LAYER-1-HYGIENE-RUNBOOK.md`
2. **Layer 2** — `LAYER-2-FOUNDATION-SCOPE.md` (covers Phase 1+2+3 of original proposal)
3. **Layer 3** — `LAYER-3-QUALITY-SCOPE.md` (covers Phase 4 + smoke gates)

### The 1 layer that's conditional

4. **Layer 4** — `LAYER-4-ADAPTIVE-SCOPE.md` (only if §3 gates met)
   - Soul-improvement NEVER in scope here — see proposal §12

### Naming convention for layer artifacts

- `LAYER-N-NAME-SCOPE.md` — the layer's full scope doc
- `LAYER-N-NAME-RUNBOOK.md` — operator-action runbook (if any operator work)
- `LAYER-N-NAME-COMPLETION-REPORT.md` — what shipped, what didn't, lessons
- `analysis/EXECUTION-SCOPE-2026-09.md` — THIS file, the master plan

---

**Next deliverable**: `LAYER-1-HYGIENE-SCOPE.md` + `LAYER-1-HYGIENE-RUNBOOK.md`.

**Awaiting**: Ivan's greenlight to start Layer 1.