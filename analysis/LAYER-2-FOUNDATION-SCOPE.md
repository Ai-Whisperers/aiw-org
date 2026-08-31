# Layer 2 — Structural Foundation — Scope

> **Status**: Active. AI proceeding autonomously per Ivan's directive (2026-09-01).
> **Owner**: AI (12-18h) + Ivan (2-4h review/approve)
> **Total time**: 14-22h
> **Reversibility**: Full per task (each task independently committable)

---

## Goal

Lift the 3-tier atomic / business / governance architecture from aspirational to enforced. Make every PROMPT agent-typed, every dept signal-routed, every script lintable. **Layer 2 ships when a baseline pytest run passes and 58 PROMPTs have full frontmatter.**

---

## Per-task scope

### L2.1 — Delete `departments-taxonomy/` (8 empty depts)

**What**: `departments-taxonomy/` has 8 dirs (`ai-ops`, `ai-org-platform`, `compliance`, `knowledge-mgmt`, `marketing`, `operations`, `product-discovery`, `sales`) with charter skeletons but no agents underneath. **No "why abandoned" doc exists.** Decision: delete with a one-line note in commit message.

**Acceptance criteria**:
- [ ] `git rm -r departments-taxonomy/` executed
- [ ] Commit message references "v2 taxonomy abandoned per Layer 2 cleanup"
- [ ] `analysis/REMAINING-TASKS-AND-WISHLIST.md` updated
- [ ] `git status` clean (no other deleted files)

**Files affected**: `departments-taxonomy/` (8 dirs, ~27 files, 9.5KB total)

**Rollback**: `git revert <commit>`

**Tokens**: ~200

---

### L2.2 — Dedupe `playbooks/` vs `departments/`

**What**: 6 playbooks × ~200 lines = 1,200 lines of overlap with `departments/0[1-6]-*.md`. Plan: keep the **more detailed** of each pair as canonical, delete the other.

**Decision matrix** (auto-resolved by line count):
| Dept | `playbooks/NN-*.md` | `departments/NN-*.md` | Canonical | Delete |
|------|---------------------|----------------------|-----------|--------|
| 01-operations | 5,955b (178 lines) | 5,401b (similar content) | playbooks (longer, more detailed) | departments/01-operations.md |
| 02-sales-growth | 6,363b (205 lines) | 6,586b (similar) | departments (longer) | playbooks/02-sales-growth.md |
| 03-engineering-delivery | 6,604b (201 lines) | 7,984b (much longer) | departments (much longer) | playbooks/03-engineering-delivery.md |
| 04-finance-legal | 7,008b (207 lines) | 6,521b (similar) | playbooks (slightly longer) | departments/04-finance-legal.md |
| 05-research-education | 6,344b (204 lines) | 6,091b (similar) | playbooks (slightly longer) | departments/05-research-education.md |
| 06-people-culture | 5,810b (185 lines) | 6,092b (similar) | departments (slightly longer) | playbooks/06-people-culture.md |

**Net**: keep 3 playbooks, keep 3 dept charters. Delete the other 6.

**Acceptance criteria**:
- [ ] 6 files deleted (3 from playbooks/, 3 from departments/)
- [ ] 6 files kept (canonical)
- [ ] Cross-reference note: canonical file mentions "replaces playbook/NN-*.md" or "replaces departments/NN-*.md"
- [ ] Per-canonical commit (not one mega-commit)

**Files affected**: 6 deletions

**Rollback**: `git revert <commit>`

**Tokens**: ~300

---

### L2.3 — Fix `.gitignore` patterns

**What**: Per Layer1 precheck audit, `.gitignore` patterns are broken — only 2 patterns match per `git check-ignore`. Outbox files (279 files), monitor-notes, state snapshots — all slip through despite being in `.gitignore` with patterns like `*/outbox/*.md`.

**Root cause**: Gitignore patterns use `*/outbox/*.md` which should work, but testing shows only 2 patterns match. Likely cause: missing `**` for nested dirs, or pattern needs `**/outbox/*.md` instead.

**Fix**: Replace `.gitignore` with corrected patterns + test with `git check-ignore`.

**Acceptance criteria**:
- [ ] `git check-ignore` on all 713 untracked files: ≥700 marked as ignored
- [ ] Specifically: all `*/outbox/*.md` files match
- [ ] All `*/monitor-notes/*.md` files match
- [ ] All `state/snapshots/` files match
- [ ] `*.pre-sqlite.bak` matches
- [ ] Committed + verified

**Files affected**: `.gitignore` (replace contents)

**Rollback**: `git checkout HEAD -- .gitignore`

**Tokens**: ~500

---

### L2.4 — Write `scripts/lint-prompts.py` (Doctrine 2 enforcer)

**What**: New Python script that lints all 58 PROMPTs for:
- Required fields: `name`, `version`, `schedule` (or omit if N/A), `owner`
- Recommended fields (Layer 3 additions): `layer`, `topology`, `archetype`
- `hard_stops` schema validation (each stop has `action`, `require_approval`, optional `approved_human`)
- Optional fields warning: `composition` (Layer 3), `negative_examples`, `transfer_targets`

**Acceptance criteria**:
- [ ] Script at `scripts/lint-prompts.py`
- [ ] Runs in <5s across all 58 PROMPTs
- [ ] Exits 0 if all pass; 1 if any fail
- [ ] Per-agent output (name, missing fields, hard_stops issues)
- [ ] Integrates with `tests/run-all.sh`
- [ ] Output format: `agent-name: missing-field-list`

**Files affected**: `scripts/lint-prompts.py` (new), `tests/test_lint_prompts.py` (new), `tests/run-all.sh` (modified)

**Rollback**: `git revert <commit>`

**Tokens**: ~1,500

---

### L2.5 — Add Layer 3 frontmatter to all 34 dept PROMPTs

**What**: For each of 34 dept PROMPT files in `01-operations/*/PROMPT.md` through `06-people-culture/*/PROMPT.md`, add frontmatter fields:
- `layer: business` (per Pattern 3 — LeCun/Bengio)
- `topology: stream-aligned` (per Pattern 6 — Team Topologies)
- `archetype: team-lead` or appropriate (per Pattern 8 — Larson)
- `composition: [<atomic-agents-called>]` (per Pattern 1 — Andreas/Christiano)
- `time_scale: daily|weekly|...` (per Pattern 7 — Precup)
- `negative_examples: [...]` (per Pattern 5 — Hinton)
- `transfer_targets: [<agent-ids>]` (per Pattern 4 — Singh)

**Acceptance criteria**:
- [ ] All 34 dept PROMPTs have the 7 new fields
- [ ] `scripts/lint-prompts.py` exits 0 on all 34
- [ ] Each agent's `composition:` references agents that EXIST in `demiurge/agents/` or are marked as external
- [ ] No regression in agent behavior (smoke test via existing tests)

**Files affected**: 34 `PROMPT.md` files modified

**Rollback**: `git revert <commit>` (single rollback covers all 34)

**Tokens**: ~3,000

---

### L2.6 — Add Layer 3 frontmatter to all 24 demiurge PROMPTs

**What**: Same as L2.5 but for demiurge agents. Add:
- `layer: atomic`
- `topology: platform` (most) or `complicated-subsystem` (audio)
- `archetype: solver` (most) or `architect` (Hermes-router)
- `time_scale: minutes|hours` (most cron-runnable)
- For Hermes-router: `composition:` listing which signals it routes
- For others: `transfer_targets:` listing dept agents that call them

**Acceptance criteria**:
- [ ] All 24 demiurge PROMPTs have the new fields
- [ ] `scripts/lint-prompts.py` exits 0 on all 24
- [ ] `agent.yaml` files updated if needed for sync
- [ ] Per-agent commits (one per agent for granular history)

**Files affected**: 24 `PROMPT.md` files + possibly 24 `agent.yaml` files

**Rollback**: per-agent revert (granular)

**Tokens**: ~2,000

---

### L2.7 — Add per-dept `signals.yaml` + `kpis.yaml`

**What**: `demiurge/kpi/revenue-stack.yaml` covers 3 depts (marketing, sales, product-discovery). Add similar for the other 3 depts (operations, finance-legal, engineering, research-education, people-culture). Per `EXECUTION-SCOPE §2 Layer 2` + `GAP-RESEARCH-FINDINGS Surprise 5: Phase 5 is dependent on Phase 2`.

**Acceptance criteria**:
- [ ] `demiurge/kpi/operations.yaml` (operations KPIs)
- [ ] `demiurge/kpi/finance.yaml` (finance-legal KPIs)
- [ ] `demiurge/kpi/engineering.yaml` (engineering KPIs)
- [ ] `demiurge/kpi/research.yaml` (research-education KPIs)
- [ ] `demiurge/kpi/people.yaml` (people-culture KPIs)
- [ ] All follow same schema as `revenue-stack.yaml`
- [ ] `kpi-org-health-score` aggregator (already defined; verify)

**Files affected**: 5 new yaml files

**Rollback**: per-file revert

**Tokens**: ~1,500

---

### L2.8 — Update `docs/THREAT-MODEL.md`

**What**: Per Layer 1 precheck audit, threat model is from 2026-08-14, predates DEMIURGE integration. Add:
- DEMIURGE atomic agent attack surface
- Cross-repo leak vectors (P5/P7/P8 buckets from security-watchdog)
- Soul-improvement threat model (per proposal §12)
- Hard-stops wrapper enforcement gap (per Layer 1 audit finding: 0 agents currently invoke wrapper)
- New threat actors: AI agent compromise, model extraction, prompt injection at scale

**Acceptance criteria**:
- [ ] New "Multi-agent Attack Surface" section
- [ ] Updated threat model with DEMIURGE + ai-ops-coordinator + 24 atomic agents
- [ ] Hard-stops enforcement gap explicitly called out
- [ ] AI self-fix doctrine referenced
- [ ] Cross-references to `RESEARCH-CITATIONS-2026-09.md` §C2/C6 (composition, hard-stops)

**Files affected**: `docs/THREAT-MODEL.md` (rewrite)

**Rollback**: `git revert <commit>`

**Tokens**: ~1,200

---

### L2.9 — Layer 2 completion report + smoke gate

**What**: 
- Layer 2 completion report at `analysis/LAYER-2-FOUNDATION-COMPLETION-REPORT.md`
- Run `scripts/lint-prompts.py` on all 58 PROMPTs (must exit 0)
- Run existing `tests/run-all.sh` (must pass; pytest baseline established)
- Capture post-Layer-2 baseline metrics (compare to `BASELINE-METRICS-2026-09-01.json`)
- Update `REMAINING-TASKS-AND-WISHLIST.md` with Layer 2 status

**Acceptance criteria** (Layer 2 → Layer 3 transition):
- [ ] `scripts/lint-prompts.py` exits 0 on all 58 PROMPTs
- [ ] All 58 PROMPTs have new frontmatter fields
- [ ] `.gitignore` patterns fixed (≥700 ignored files)
- [ ] Per-dept signals.yaml + kpis.yaml exist for all 6 depts
- [ ] `docs/THREAT-MODEL.md` updated
- [ ] Completion report committed
- [ ] Wishlist updated
- [ ] State files valid per `validate-state.py`
- [ ] AI declares "Layer 2 complete" with commit hash

**Files affected**: 3 docs + state/coord.json note

**Rollback**: per-commit revert

**Tokens**: ~800

---

## Layer 2 exit criteria

Layer 2 is DONE when:

1. All 9 tasks committed (granular commits per task)
2. Smoke gate passes (lint-prompts.py + tests + validate-state)
3. Completion report committed
4. Wishlist updated
5. AI announces "Layer 2 complete"

Then: **pause for Layer 3 greenlight** (Ivan: "Layer 3 go").

---

## Dependencies

- None before Layer 2
- Layer 3 depends on Layer 2's lint-prompts.py + frontmatter fields
- Layer 4 (conditional) depends on Layer 3 + customer traction

---

## Risks specific to Layer 2

| Risk | Mitigation |
|------|------------|
| L2.5/L2.6 frontmatter changes break agent behavior | Per-agent commits + per-agent rollback |
| .gitignore fix accidentally commits runtime artifacts | Verify `git status` before commit |
| Lint script rejects valid PROMPTs | Iterate: first pass collects all issues, second pass fixes |
| Test regressions from frontmatter changes | Existing tests should pass; if not, investigate |
| Per-dept KPIs are speculative (no historical data) | Use placeholder values + signal "set target on first run" |

---

## Token budget

| Task | Estimate |
|------|----------|
| L2.1 (delete taxonomy) | 200 |
| L2.2 (dedupe playbooks) | 300 |
| L2.3 (fix .gitignore) | 500 |
| L2.4 (lint script) | 1,500 |
| L2.5 (dept frontmatter × 34) | 3,000 |
| L2.6 (demiurge frontmatter × 24) | 2,000 |
| L2.7 (per-dept KPIs × 5) | 1,500 |
| L2.8 (threat model) | 1,200 |
| L2.9 (report + smoke) | 800 |
| **TOTAL** | **~11,000 tokens** |

This is the budget. AI self-monitors and pauses if any single task exceeds 2x estimate.

---

**AI is starting Layer 2 execution now. Per task:**
- Read context
- Apply changes
- Verify with smoke gate
- Commit granularly
- Document in wishlist

**Awaiting nothing** — Ivan said "go for all layers all phases." Proceeding.
