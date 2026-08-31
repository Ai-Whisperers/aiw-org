# Pre-Execution Audit — All 4 Layers

> **Purpose**: Catch blockers for ALL4 layers before execution starts. Same
> approach as the Layer1 preflight, extended to Layers 2-4 + cross-layer.
>
> **Outcome**: Net assessment + remaining questions for Ivan before Layer1
> autonomous work can begin.

---

## TL;DR

| Layer | Status | Blockers before greenlight |
|-------|--------|---------------------------|
| **Layer 1** | Ready for operator parts (A+B+C); autonomous parts blocked | Tasks1.2-1.4 file locations unknown + pytest not installed |
| **Layer 2** | Ready except for runtime config | `.gitignore` patterns broken (already known); need to fix permissions on `demiurge/` for AI to write |
| **Layer 3** | Blocked on tooling | pytest not installed; coverage tools not installed |
| **Layer 4** | Blocked by design | Customer traction gate NOT met (rubicon-eas archived, $240 MRR) — exactly as planned |
| **Cross-layer** | Several decisions needed | See §6 |

---

## 1 — Layer 1 audit (covered in PRE-LAYER-1-PREFLIGHT-AUDIT-2026-09.md, summary here)

- 5 P0 secret leaks (operator parts): proceedable now via runbook
- LiteLLM topup (operator): proceedable
- Wrangler restart (operator decision + AI exec): proceedable after Ivan's choice
- Tasks 1.2-1.4 (validator/MCP fixes): **BLOCKED** — code not in aiw-org, file locations needed
- Task 1.7 (baseline metrics): proceedable (read-only on state files)
- Task 1.10 (smoke gate): **BLOCKED on pytest install**

---

## 2 — Layer 2 audit (Structural Foundation)

### What's ready
- `departments-taxonomy/` exists with 8 dirs + 27 files (charter skeletons); safe to remove in Layer 2.1
- Playbooks vs dept charters duplication: 6 playbooks × 200 lines each = ~1,200 lines of overlap. Dedup target clear.
- 34 dept PROMPTs need frontmatter standardization. Field coverage survey:
  - `hard_stops`: 34/34 (100%) — already universal
  - `name`, `version`, `owner`: 26/34 (76%) — 8 PROMPTs missing basic metadata
  - `schedule`: 24/34 (71%) — 10 PROMPTs missing schedule
  - `fallback_model`: 19/34 (56%) — half missing
  - `parent_spec`: 11/34 (32%) — most missing
  - `git_repo`, `state_db`: 8/34 (24%) — most missing
- 24 demiurge agents: ALL have `agent.yaml` (gap analysis said 10/24; **this audit shows 24/24 — the file was added between the gap analysis and now**)
- BWS cache: fresh (54 min old)
- Git remote + token: working (verified last commit)

### What's blocked
- **`.gitignore` patterns broken** (already known — only 2 patterns match per `git check-ignore`). Layer 2.4 fix is required.
- **`demiurge/` dir permissions** — needs verification AI can write to it. Tests show write access to `/opt/data/agents/` yes, but specific subdirs may need explicit chmod. **Verify at Layer 2 start.**
- **Outbox bloat**: 279 outbox .md files, 1.8 MB. Not in scope (gitignored), but Layer 2 should verify the .gitignore fix prevents re-tracking.

### Estimated scope (from EXECUTION-SCOPE §2)
- W2: Cleanup (1-2h)
- W3: Atomic-layer completion (2-3h, but agent.yaml gap already closed)
- W4: Business-layer integration (4-6h, mostly frontmatter + composition block)
- **Total Layer 2**: ~7-11h AI time

---

## 3 — Layer 3 audit (Quality Infrastructure)

### What's ready
- `scripts/validate-state.py` exists (3302b) — JSON schema validator for state files
- `scripts/eval-gate.py` exists (5023b) — eval gate runner
- `tests/` has 22 test files
- `jsonschema` module available (v4.26.0)
- `run-all.sh` exists, uses `unittest discover` (not pytest)

### What's blocked

| Item | Status | Resolution |
|------|--------|------------|
| **pytest** | NOT installed | Need Ivan's go to `pip install pytest` |
| **coverage** | NOT installed | Need Ivan's go to `pip install coverage pytest-cov` |
| **Existing test suite** | Last run time unknown | Need baseline run before Layer 3 starts |
| **`run-all.sh` uses unittest not pytest** | Working as-is | Can run today; pytest integration is Layer 3 enhancement |
| **Pre-existing test coverage %** | Unknown | Need baseline measurement before Layer 3 |

### Questions for Ivan
- (a) `pip install pytest pytest-cov` — safe, ~60 sec — get your go
- (b) Use unittest (current) and skip pytest — works today but slower
- (c) Different approach

### Estimated scope (from EXECUTION-SCOPE §2)
- W5: Tests + eval gates + smoke-test gates (8-12h)
- **Total Layer 3**: 7-10h AI time

---

## 4 — Layer 4 audit (Adaptive, CONDITIONAL)

### Trigger gates per EXECUTION-SCOPE §3

| Gate | Current status | Met? |
|------|---------------|------|
| ≥1 paying customer uses aiw-org-managed feature | rubicon-eas archived 2026-08-28; no replacement | ❌ |
| Layers 1-3 stable for 7+ consecutive days | Not yet started | ❌ |
| Per-phase smoke-test pass rate ≥95% over 14 days | Not measured | ❌ |
| Operator P0 leak queue empty | Not closed (operator task) | ❌ |

**Verdict**: Layer 4 gate NOT met. **This is the correct design** — Ivan explicitly chose "complete solution but adaptive capability only after traction."

### Soul-improvement staged gate (per proposal §12)

- Stage 1 (test harness) requires building a sandbox agent
- Stages 2-4 require active customers
- **All 4 stages are conditional** — same as Layer 4

### What this means

**Layer 4 is essentially a no-op until Ivan has a customer + stable layers.** This is intentional. The current prep work is making Layers 1-3 ready so that when the gate conditions trigger, Layer 4 can proceed.

### Estimated scope (from EXECUTION-SCOPE §2)
- Layer 4: 10-15h IF gates met
- Current path: do NOT plan Layer 4 yet. Re-evaluate quarterly.

---

## 5 — Cross-layer audit

### Q1 — Is the dev environment sustainable?

- `/opt/data/agents/` writable: **YES**
- `/opt/data/` writable: **YES**
- Disk free: **143 GB** (plenty for 37-56h of work)
- BWS cache: fresh (54 min old)
- Git remote + GH PAT: working (last commit `4c40957` pushed successfully)

**Verdict**: Environment is stable. AI can work continuously.

### Q2 — Cron jobs drift

Last 3 commits all show cron-sync drift was caught + resolved automatically by the pre-commit hook. Pattern is: cron-sync before commit, hook passes. **Operational discipline is good.**

**Verdict**: OK. AI must continue running `bash /opt/data/scripts/cron-sync.sh` before every commit (per Doctrine 2 in EXECUTION-SCOPE).

### Q3 — Sister repos in scope?

`agents-v2` exists (37 PROMPTs, 83 DEMIURGE tickets, **the customer-facing product** per Gap Research Findings).

Per Doctrine 5 ("pause on cross-repo coordination"), Layer 1-3 should NOT touch `agents-v2`. Layer 4 (if it triggers) needs explicit cross-repo permission.

**Question**: Is `agents-v2` EXPLICITLY out of scope for Layers 1-3? (Yes per current EXECUTION-SCOPE, just confirming.)

### Q4 — docs/ inventory

16 markdown files in `docs/`. Some are from 2026-08-14, some updated more recently. **No Layer 1-3 task touches docs/** unless Layer 3 adds testing docs. Carry-forward.

**Notable**: `docs/THREAT-MODEL.md` is from 2026-08-14, predates DEMIURGE. **Layer 2 should update it.** Adding to Layer 2 scope.

### Q5 — Open PRs

5 open PRs in dependent repos. None in aiw-org itself:
- 1 in paraguai-platform (deploy pipeline, not stale)
- 4 trademark-scrub PRs, all 15 days stale

**Verdict**: Out of aiw-org scope. No blocker.

### Q6 — Operator notification path

In-session: chat (current). **Cross-session**: unclear. If Ivan closes this chat and AI starts autonomous work, AI will not be able to reach Ivan until he opens a new session.

**Question**: Does AI work **only** when Ivan is in session? Or does AI work offline and Ivan reviews on next session?

Per Doctrine 1 (AI self-fixes) and Doctrine 5 (pause on big), AI CAN work autonomously when only small decisions are needed. AI PAUSES on big decisions. **When in doubt, pause.**

**Recommendation**: AI proceeds with autonomous work in-session. **Between sessions, AI commits small fixes and waits for next session to surface them.** This is implicit in "Doctrine 1: AI self-fixes when it can" — the self-fix happens in real-time; the reporting happens on next contact.

### Q7 — Are the 4 layer scope docs in place?

| Doc | Status |
|-----|--------|
| `LAYER-1-HYGIENE-SCOPE.md` | ✅ written |
| `LAYER-2-FOUNDATION-SCOPE.md` | ❌ **NOT written** (referenced in EXECUTION-SCOPE §8 but not created yet) |
| `LAYER-3-QUALITY-SCOPE.md` | ❌ **NOT written** |
| `LAYER-4-ADAPTIVE-SCOPE.md` | ❌ **NOT written** |

**Per EXECUTION-SCOPE Doctrine 2**: each layer scope doc is written **before** the layer starts. So:
- Before Layer 1 starts: scope doc done ✅
- Before Layer 2 starts: scope doc needed
- Before Layer 3 starts: scope doc needed
- Before Layer 4 starts: scope doc needed

**AI will write these as we reach each layer.** No blocker.

---

## 6 — Open questions for Ivan

These are the remaining decisions before Layer1 autonomous execution can begin:

### Q1 — Validator file location (Tasks1.2, 1.3)
- (a) point me at path in aiw-org
- (b) grant agents-v2 access
- (c) grant work/research-repos access
- (d) tell me where
- (e) incidents are stale — mark closed

### Q2 — MCP file location (Task1.4)
Same options as Q1.

### Q3 — pytest for Layer1 smoke gate (Task1.10) + Layer3
- (a) `pip install pytest pytest-cov` (60 sec, safe)
- (b) use unittest (current state), skip pytest
- (c) different approach

### Q4 — `.env` files in adjacent paths
- (a) audit + report (Layer 1)
- (b) fix `.gitignore` only (carry to Layer 2)
- (c) ignore

### Q5 — `fix_requirements.py` at `/opt/data/fix_requirements.py`
- (a) out of scope, ignore
- (b) tracked somewhere — tell me where
- (c) delete

### Q6 — Cross-session autonomous work
- (a) AI works only when Ivan is in session; commits small fixes; surfaces on next session
- (b) AI works offline; Ivan reviews async when convenient
- (c) AI pauses any task when session ends; resumes on next

### Q7 — Layer 2 scope doc format preference
- (a) Same template as Layer 1 (10 tasks + acceptance criteria + per-task rollback + token budgets)
- (b) Different template (Layer 2 is bigger; maybe a different structure)
- (c) I'll choose based on what fits Layer 2

---

## 7 — Net readiness assessment

### What's procedable today (with no further answers)

| Work | Time | Notes |
|------|------|-------|
| Operator work Batch A (P0 leaks) | 75 min | Runbook ready |
| Operator work Batch B (LiteLLM) | 5 min | Runbook ready |
| Operator work Batch C (wrangler decision) | 5 min + 30 min AI exec | Runbook ready |
| Task 1.7 (baseline metrics) | 60 min | Read-only state files |
| Task 1.8 (wishlist update) | 15 min | AI self-fix |
| Layer 2 audit (read-only) | 30 min | Verify the 27 demiurge agent.yamls work, etc. |

### What's blocked until answers

| Work | Blocked by |
|------|-----------|
| Tasks1.2-1.4 (validator/MCP fixes) | Q1, Q2 (file locations) |
| Task 1.10 (smoke gate) | Q3 (pytest) |
| `.env` audit | Q4 |
| Layer 2 autonomous work | Need Ivan's greenlight after Layer 1 done |
| Layer 3 autonomous work | Q3 (pytest install) + Layer 2 done |
| Layer 4 | Customer traction gate |

### Token cost of "more prep / more research"

| More research | Token cost | Value |
|---------------|-----------|-------|
| Audit the sister repo `agents-v2/` for code that touches aiw-org | ~1K tokens | Could surface cross-repo dependencies |
| Audit `.env` files for actual secrets (per Q4) | ~500 tokens | Could find real P0 secrets I missed |
| Audit `tests/` for what's actually passing/failing | ~500 tokens | Sets baseline for Layer 3 |
| Research: which research repos are LIVE vs ARCHIVED | ~1K tokens | Could surface ~10 more dead-code references |
| Research: what do other "AI-native" companies (Linear, Notion) actually do for org structure | ~3K tokens | Already covered in RESEARCH-CITATIONS; low additional value |
| Research: soul-improvement formal verification methods | ~2K tokens | Already in §12 staged rollout; deeper research is for v2 |

**Recommended additional research**: only the first 3 (env audit + tests audit + sister-repo deps). Low token cost, high operational value for Layer 1-3 execution.

---

## 8 — My recommendation

1. **Answer Q1-Q5** (file locations + pytest + .env scope + fix_requirements) — blocks Layer1 autonomous parts
2. **Answer Q6** (cross-session behavior) — blocks effective long-running AI work
3. **Let me run the 3 recommended additional research items** (env audit, tests audit, sister-repo deps) — ~2K tokens, ~10 min
4. **Then greenlight Layer 1** — operator work + autonomous parts (subject to answers)

OR

1. **Greenlight just operator work now** — Ivan starts Batch A + B in 90 min uninterrupted
2. **AI does the 3 additional research items in parallel** — surface findings
3. **AI waits for Ivan's answers on Q1-Q6** — Doctrine 5
5. **Then proceed with autonomous Layer 1 parts**

---

**Awaiting Ivan's call on Q1-Q6 + which option (1 or 2 above) for sequencing.**