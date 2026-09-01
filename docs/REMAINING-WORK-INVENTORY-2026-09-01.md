# Remaining-Work Inventory — 2026-09-01

> **One-page snapshot of open items after Phase 9 R1-R5.**
> Designed for the operator (Ivan) to triage at session-start.
> All askable items require explicit one-word operator authorization.

---

## Critical (Open — Operator-Gated)

| Item | Why it matters | Asks |
|------|---------------|------|
| R2: Sales pipeline dead (0 leads, Worker 404) | $0 → $5K+ MRR lever | ADR-0004 deferred until engineering stable |
| R10: Burn rate > runway (no clients) | Will trigger Tier-3 review if not addressed | Tier-3 trigger: 5+ clients |
| R11: Ivan bandwidth | Single point of failure | Hiring (Tier-3 deferred) |

## Low-Risk (Open — Auto-Mitigated)

| Risk | Status | Auto-mitigation |
|------|--------|-----------------|
| R1 (hard-stops wrapper unenforced) | ACCEPTED per ADR-0004 | Pre-commit guards + human-in-loop on destructive ops |
| R3 (Sunday cron pile-up) | MITIGATED | Spread crons + cost-optimize overlap detector |
| R4 (eval aggregate unknown) | MITIGATED | aiw-eval-aggregate-nightly cron |
| R5 (LLM prompt injection) | MITIGATED | 16/16 schemas strict (additionalProperties: false) |
| R6 (Cloudflare Worker outage) | DEFERRED until engineering stable | Formspree fallback planned |
| R7 (trademark incident) | MITIGATED | aiw-trademark-scan-cron wired weekly |
| R8 (LiteLLM outage) | TESTED | chaos-runner scenario 3 |
| R9 (Bitwarden compromise) | MITIGATED | cron-secret-sentinel daily scan |
| R12 (cron-error-watchdog false neg) | MITIGATED | Manual trigger test passed 2026-09-01 |

## Deferred (per ADR-0004)

- DEMIURGE-082: portmanteau migration → DEFERRED
- Formspree lead form migration → DEFERRED
- Start-Up Chile application → DEFERRED
- Open-source framework → DEFERRED
- Tier-3 hiring / people research → DEFERRED

## What is NOT blocked on operator

- Daily crons (token-ledger, chaos-runner, sentinel, watchdog, etc.) — all running
- Schema hardening — 16/16 strict
- Cost optimization — 19 overlaps detected
- Eval gate enforcement — policy loaded + enforced
- Parent-spec loader — 47 PROMPT.md validated, 0 missing
- Tier-C2 boundary (aiw-org ↔ growth-coaching) — defined via schema
- Tier-C5 (curator-evolver + homunculus) — running weekly

## What IS blocked on operator (Tier-2 / Tier-3)

- R2 sales funnel revival (4h, DEFERRED until engineering stable)
- R10 5+ clients (Tier-3 trigger, currently 0)
- R11 hiring (2 weeks, Tier-3 deferred)
- 6 DEMIURGE tickets already APPROVED 2026-09-01 R5

## How to use this inventory

1. **Run this session**: zero P0 items open. All 5 mitigations shipped.
2. **Operator asks only**: R2, R10, R11 — and the 4 ADR-0004 deferrals.
3. **Next session suggestion**: If R2 unlocked, do Tier-3 funnel revival pass.
4. **If not**: stay operational; this is the production state.

---

**Maintainer**: AIW org automated
**Last update**: 2026-09-01 22:00 UTC (auto)
**Source**: `board/risk-register-2026.md`, `tickets/DEMIURGE-*/`, `/opt/data/.hermes/cron/jobs.json`
