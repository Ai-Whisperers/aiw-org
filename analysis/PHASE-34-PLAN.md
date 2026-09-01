# Phase 34 — Cost Optimization Cleanup

> **Date**: 2026-09-01
> **Trigger**: Ivan "all defaults ok" (b b a a a) — Resume only crons, stagger top 5, investigate 6 failing, wrapper edge case, multilingual 3 langs
> **Status**: 5/5 in progress

---

## Plan

| # | Decision | Scope | Effort |
|---|---|---|---:|
| **Q1b** | Resume 19 disabled crons (no remove) | Toggle `enabled=true` for paused/cancelled crons | ~2h |
| **Q2b** | Stagger top 5 overlapping schedules | Move crons by 1-15 minutes to avoid burst | ~1h |
| **Q3a** | Investigate 6 failing crons | Diagnose + fix or flag | ~2h |
| **Q4a** | Wrapper edge case test | whitelist + hard_stops combined behavior | ~1h |
| **Q5a** | Multilingual patterns (French/German/Portuguese) | More red-team coverage | ~2h |

Total: ~8h focused eng+devops work, all within scope pivot.

---

## Cross-references

- `analysis/PHASE-33-FEEDBACK.md` — prior phase
- `state/cost-optimization-report.md` — 19 disabled + 17 overlapping + 6 failing
- `patterns/hard-stop-wrapper.py` — whitelist mode (Phase 33 R1)
- `scripts/red-team-scenarios.py` — multilingual scenarios
