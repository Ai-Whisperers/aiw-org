# Doc Drift Audit — Phase 9 R3 (2026-09-01)

> **Scope**: DEMIURGE-071 + audit Section 4 §1 "Ground truth vs. documented claims"
> **Status**: 6 drift items identified, 4 resolved in this commit, 2 deferred to next session.

---

## Drift table

| # | Doc | Claim | Actual | Status |
|---|---|---|---|---|
| D1 | README.md | "24 Atomic DEMIURGE agents" | 28 | ✅ Fixed |
| D2 | README.md | "49 Sub-agents (Tier-2/Tier-3)" | 35 | ✅ Fixed |
| D3 | README.md | "35 PROMPT-monitor.md files" | 63 | ✅ Fixed |
| D4 | README.md | "131 Cron jobs" | 167 | ✅ Fixed |
| D5 | README.md | "~50 State files" | 86+ | ✅ Fixed |
| D6 | README.md | "72 Tests" | 278 | ✅ Fixed |
| D7 | README.md | "36 Scripts" | 96 | ✅ Fixed |
| D8 | README.md | "100% pass, 9s" | ~3s | ✅ Fixed |
| D9 | README.md | "Phases 5-8 active" | Phase 9 R-series | ✅ Fixed |
| D10 | README.md | "47-agent handoff matrix" | 63-agent | ✅ Fixed |
| D11 | README.md | "9 schemas" | 13 | ✅ Fixed |
| D12 | README.md | "9 schemas" | 13 | ✅ Fixed (duplicate) |
| D13 | OPERATIONS.md | "49 agents" | 63 | ✅ Fixed |
| D14 | OPERATIONS.md | "35 PROMPT-monitor.md" | 63 | ✅ Fixed |
| D15 | OPERATIONS.md | "131 cron jobs" | 167 | ✅ Fixed |
| D16 | OPERATIONS.md | "32 test files, 72 tests" | 38 test files, 278 tests | ✅ Fixed |
| D17 | ORCHESTRATION.md | "10 cron jobs, 3 agents" | 167 jobs, 63 agents | ⚠️ DEFERRED — file dated 2026-08-13, full rewrite needed |
| D18 | department-index.md | (not yet audited) | — | ⚠️ DEFERRED |

---

## Method

1. Read README.md, OPERATIONS.md sections referencing counts
2. Cross-reference against actual filesystem state:
   - `find . -name "PROMPT.md" -not -path "./.git/*" | wc -l`
   - `find . -name "PROMPT-monitor.md" -not -path "./.git/*" | wc -l`
   - `jq '.jobs | length' /opt/data/.hermes/cron/jobs.json`
   - `find tests -name "test_*.py" | wc -l` + `python3 -m pytest --collect-only -q | wc -l`
   - `find . -path "./schemas/*.json" | wc -l`
   - `ls scripts/*.py scripts/*.sh | wc -l`

---

## Verification

- All ✅ items committed in `aiw-org: Phase 9 R3 - Tier-A1 close-out`
- Pre-commit chain (cron-guard + secret-leak + trademark-scrub + citation-coverage) passes
- Canonical gate: 278/278 tests pass

---

## Deferred to Phase 9 R4

- **ORCHESTRATION.md full rewrite** (~30m) — file describes pre-Phase-8 state, needs complete rewrite
- **department-index.md audit** (~1h) — not yet checked
- **state-snapshot.md / FAILURE-MODES.md / COMPLETE-EXPLANATION.md** — secondary drift items

---

## Drift prevention

Recommended for future: add a `scripts/audit-doc-drift.py` script that reads the README/OPERATIONS metrics and verifies against filesystem, run as part of nightly cron. Estimated effort: 2h.

This is wishlist item W-NEW-9 from the plan.