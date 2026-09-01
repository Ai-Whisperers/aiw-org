# Phase 36 — More Multilingual + Cron Auto-Fix Apply + Wrapper Enhancement + Audit

> **Date**: 2026-09-01
> **Trigger**: Ivan "all defaults ok" (a a b b a)
> **Status**: 5/5 in progress

---

## Plan

| # | Decision | Scope | Effort |
|---|---|---|---:|
| **Q1a** | Multilingual KO/VI/ID/HI | 4 new languages + red-team scenarios | ~3h |
| **Q2a** | Cron auto-fix apply all | Apply the 6 stagger candidates from Phase 35 R1 | ~30min |
| **Q3b** | Wrapper wildcard with sensitive_action list | Basic: `*` allows all, but specific actions in `sensitive_actions` list still require approval | ~2h |
| **Q4b** | Multilingual red-team iteration | 2 more edge cases (false positive traps + mixed-language) | ~2h |
| **Q5a** | Full audit + bug-hunt on Phase 31-35 | Run audit-fresh + targeted bug-hunt on changed paths | ~1h |

Total: ~8.5h focused eng+devops+AI-safety work.

---

## Cross-references

- `analysis/PHASE-35-FEEDBACK.md` — prior phase
- `scripts/cron-autofix.py` — Phase 35 R1 (will be applied in R2)
- `patterns/hard-stop-wrapper.py` — Phase 35 R3 (will extend in R3)
- `state/cost-optimization-report.md` — 6 candidates for R2
