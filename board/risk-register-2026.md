# Risk Register 2026-Q3 (AI Whisperers @ $240 MRR)

> **Phase 8 Area #28** | Board of Directors | Owner: board-of-directors + ai-safety-engineer + Ivan
> **Date**: 2026-09-01
> **Status**: Initial register; refresh quarterly

---

## Scoring method

- **Likelihood** (1=rare, 5=almost certain)
- **Impact** (1=minor, 5=critical)
- **Risk score** = Likelihood × Impact

| Score band | Tier |
|------------|------|
| 1-5 | 🟢 LOW |
| 6-12 | 🟡 MEDIUM |
| 13-19 | 🟠 HIGH |
| 20-25 | 🔴 CRITICAL |

---

## Top 12 risks at $240 MRR

| # | Risk | Likelihood | Impact | Score | Tier | Mitigation | Owner |
|---|------|-----------|--------|-------|------|------------|-------|
| R1 | Hard-stops wrapper unenforced (LLM can violate declarations) | 4 | 5 | **20** | 🔴 | **ACCEPTED 2026-09-01** (ADR-0004) — wrapper invocation deferred; declarations remain advisory. Mitigated by pre-commit secret-leak + trademark-scrub guards + human-in-loop for destructive ops | Ivan (decision), ai-safety-engineer (monitor) |
| R2 | Sales pipeline dead (0 leads, Worker 404) | 5 | 4 | **20** | 🔴 | Phase 8 #19: funnel revival | sales-pipeline |
| R3 | Token-plan exhaustion on Sunday-evening weekly stack | 4 | 3 | **12** | 🟡 | Spread crons (Phase 8 #3) | ai-ops-coordinator |
| R4 | Eval aggregate pass_rate unknown | 4 | 3 | **12** | 🟡 | Run eval-aggregate-pass-rate.py nightly | ai-safety-engineer |
| R5 | LLM prompt injection (state-file mutation) | 3 | 5 | **15** | 🟠 | additionalProperties: false (P1 pattern) | engineering-roster |
| R6 | Cloudflare Worker outage (rubicon-eas-lead) | 3 | 4 | **12** | 🟡 | Move form to Formspree/Typeform (Phase 8 #19) | sales-pipeline |
| R7 | Trademark incident (Hostinger-like) | 2 | 5 | **10** | 🟡 | trademark-compliance-scrub cron | ai-safety-engineer |
| R8 | LiteLLM provider outage (no failover tested) | 3 | 4 | **12** | 🟡 | chaos-test-runner scenario #3 | chaos-test-runner |
| R9 | Bitwarden credential compromise | 2 | 5 | **10** | 🟡 | Encrypted storage + cron secret rotation | ai-safety-engineer |
| R10 | Burn rate > runway (no clients) | 3 | 5 | **15** | 🟠 | Tier-3 trigger: 5+ clients | Ivan |
| R11 | Ivan bandwidth bottleneck (single point of failure) | 5 | 4 | **20** | 🔴 | People research area: bandwidth audit | Ivan |
| R12 | Phase-25 cron-error-watchdog false negatives | 3 | 3 | **9** | 🟡 | Manual trigger test (Phase 8 #1) | ai-ops-coordinator |

---

## Tier-2 decisions ratified 2026-09-01 (ADR-0004)

| Decision | Status | Owner |
|----------|--------|-------|
| Delete Tier-2 `departments-taxonomy/` | Already gone (effective) | n/a |
| Portmanteau naming canonical (Greek → portmanteau migration) | Migration in progress (DEMIURGE-082) | ai-ops-coordinator |
| Keep `aiw-org` and `growth-coaching` separate | Active; coaching = future product department | Ivan |
| R1 hard-stops: ACCEPT risk | See row above; row updated | ai-safety-engineer |
| Formspree lead form | DEFERRED until engineering tier stable | sales-pipeline |
| Start-Up Chile application | DEFERRED until engineering tier stable | Ivan |
| Open-source the framework | DEFERRED until engineering tier stable | Ivan |
| Keep public repo (deliberate) | Active; threat model acknowledges external exposure | ai-safety-engineer |

---

## 3 critical risks needing board attention

1. **R2: Sales pipeline dead** — No revenue. Trivial to fix (Worker fix or replacement). **DEFERRED** per ADR-0004 until engineering tier stable.
2. **R11: Ivan bandwidth** — Single point of failure. Mitigated by hiring (Tier-3 deferred).
3. **R1: Hard-stops wrapper** — **ACCEPTED 2026-09-01 per ADR-0004**. Mitigated by pre-commit guards (Phase 9) + human-in-loop on destructive ops. Reassess if/when budget allows 8-16h enforcement work.

---

## 5 high-priority mitigations

| Mitigation | Owner | Effort | ETA |
|------------|-------|--------|-----|
| Invoke hard-stops wrapper (R1) | Kiki | 16h | 2026-09-15 |
| Fix sales funnel (R2) | sales-pipeline | 4h | 2026-09-08 |
| Spread Sunday-evening crons (R3) | ai-ops-coordinator | 2h | 2026-09-08 |
| Run eval-aggregate nightly (R4) | ai-safety-engineer | 4h | 2026-09-15 |
| People-area bandwidth audit (R11) | Ivan | 2 weeks | 2026-09-15 |

---

**Cross-references**:
- `docs/THREAT-MODEL.md`
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md`
- `analysis/PHASE-7-dept-research/board-of-directors-research-areas.md` Area #3
- `analysis/PHASE-8-EXECUTION-PLAN.md`

