# Phase 35 — Cron Auto-Fix + Multilingual + Whitelist + Diagnostics

> **Date**: 2026-09-01
> **Trigger**: Ivan "all defaults ok" (a a b a a) — Cron auto-fix, 4 multilingual langs, basic whitelist per-action, failed cron diagnosis, full bug-hunt
> **Status**: 5/5 in progress

---

## Plan

| # | Decision | Scope | Effort |
|---|---|---|---:|
| **Q1a** | Cron auto-fix script | Resume+stagger from cost findings (auto, with dry-run) | ~2h |
| **Q2a** | Multilingual RU/CN/JP/AR | 4 new languages + 4 red-team scenarios | ~3h |
| **Q3b** | Wrapper per-action require_approval in whitelist mode | Basic support (mark certain actions as "approval needed" within whitelist) | ~2h |
| **Q4a** | Failed cron diagnosis tool | Auto-investigate cron failures (token plan vs code bug) | ~1h |
| **Q5a** | Bug-hunt sweep on Phase 30-34 work | Full audit of all changed paths + regressions | ~1h |

Total: ~9h focused eng+devops work.

---

## Cross-references

- `analysis/PHASE-34-FEEDBACK.md` — prior phase
- `state/cost-optimization-report.md` — source for Q1
- `scripts/red-team-scenarios.py` — multilingual template
- `patterns/hard-stop-wrapper.py` — Phase 33 R1 whitelist mode
- `state/cron-error-watchdog.json` — source for Q4
