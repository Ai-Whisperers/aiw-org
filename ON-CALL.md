# ON-CALL.md

> On-call rotation. Documented per Session 1 cheatsheet + Gap-audit P2 #11.
> **Last updated**: 2026-09-01 (Phase 8 — refreshed after funnel revival + health dashboard work)
>
> **Pair with**: [OPERATIONS.md](OPERATIONS.md) (how the org works), [ON-CALL-QUICK-REF](#quick-ref-when-x-breaks) below

---

## Current rotation

| Role | Person | Backup |
|------|--------|--------|
| Primary on-call | **Ivan** | Kiki |
| Backup on-call | **Kiki** | Ivan |

## Cycle

- **Monthly rotation** (theoretical)
- In practice at 2 people: both are always on call
- Cycle applies when we hire (3+ people)

## Scope of on-call

- **Production site down** > 5 min
- **Cron jobs in error state** for > 24 hours
- **State corruption** (state validator alerts)
- **Cost cap breach** (per-agent > $1/day or total > $10/day)
- **Hard-stop wrapper blocked action** with potential customer impact
- **Security incident** (credential leak, exploit attempt)
- **Burnout signal** (founder-bandwidth-watchdog alert)

## Not on-call scope

- **Routine brief delivery** (agents handle)
- **Tuning idempotency windows** (background optimization)
- **Adding new sub-agents** (planned work)
- **Documentation updates** (background)

## Escalation timing

| Severity | Response time |
|----------|---------------|
| Critical (prod down, security incident) | < 15 min |
| High (cost cap breach, hard-stop blocked action) | < 1 hour |
| Medium (cron job error > 24h) | < 4 hours |
| Low (backup stale, drift detection) | < 24 hours |

## Communication

- **Critical/High**: Direct ping (Telegram or WhatsApp)
- **Medium**: Email + next brief
- **Low**: Logged in `state/<dept>.json`, surfaced in next brief

## Post-incident

For Critical/High:
1. **Document** in `state/<dept>.json` `incidents` table
2. **Root cause analysis** within 48 hours
3. **Mitigation plan** within 1 week
4. **Cross-dept brief** if applicable (e.g., incident in Engineering surfaces in Operations)

## Future: when we hire

- **3 people**: 3-way rotation, weekly cycles
- **5 people**: Add 2 dedicated ops (5-way rotation, primary + backup always)
- **10 people**: Add a proper on-call team, separate from engineering

## Cross-references

- `/opt/data/agents/OPERATIONS.md` — how the org works (read first)
- `/opt/data/agents/department-index.md` — per-dept agent/monitor/research map
- `/opt/data/agents/departments/01-operations.md` — Operations dept spec
- `/opt/data/agents/REVIEW-2026-Q4.md` — 90-day review includes on-call metrics
- `/opt/data/agents/board/risk-register-2026.md` — 12 risks ranked
- `/opt/data/agents/operations/health-dashboard.md` — per-dept health scores
- `/opt/data/agents/operations/cron-error-patterns-30d.md` — current cron-error snapshot
- `/opt/data/agents/analysis/GAP-RESEARCH-FINDINGS-2026-09.md` — Phase 1 L1 audit findings

---

## Quick-ref: when X breaks

| Symptom | Likely cause | First action |
|---|---|---|
| Sales funnel empty | Worker 404 / form backend down | `sales/funnel-revival-2026.md` — recommend Formspree |
| Cron errors > 5 | Sunday-evening token-plan | Spread crons; check `cron-error-watchdog.json` |
| Hard-stops blocked | LLM tried destructive action | Check `patterns/hard-stop-wrapper.py`; review action log |
| Eval aggregate < 0.5 | Eval system not populating `by_agent` | `python3 scripts/eval-aggregate-pass-rate.py`; investigate |
| Drift alerts flood | Threshold too sensitive | `operations/monitor-threshold-calibration-2026.md` |
| Health score < 60 | Per-dept issue | `operations/health-dashboard.md` |
| Ivan bandwidth red | Founder overload | `01-operations/founder-bandwidth-watchdog/` triggers |
| Hard-stops never invoked | Wrapper exists but 0/49 agents call it | `operations/hard-stops-enforcement-audit.md` — needs Kiki |
| Trademark incident | Hostinger-like | `compliance-monitor` + trademark-scan-cron |
| SECURITY: credential leak | Bitwarden vault compromised | Rotate via BWS immediately; check `state/webhook-log.json` |
| SECURITY: prompt injection | Adversarial input | ai-safety-engineer + state-write-disciple catches (if invoked) |
| Lua: `minimax-plan` unknown | Config drift | Edit cron definition to use current provider |
| Lint fails | New PROMPT.md missing frontmatter | `scripts/lint-prompts.py --fix` |
| Smoke gate fails | Layer regression | `scripts/smoke-test.sh all` — read which layer broke |

---

## Phase 8 alerts (priorities for the next 7 days)

1. **🔴 URGENT — Sales pipeline revival decision** — Ivan picks Formspree (1-2h) vs Worker revival (8-16h). See `sales/funnel-revival-2026.md`.
2. **🔴 HIGH — Hard-stops enforcement decision** — Kiki reviews `operations/hard-stops-enforcement-audit.md`. 16h to implement.
3. **🟡 MEDIUM — Sunday-evening cron spread** — 2h work, ai-ops-coordinator.
4. **🟡 MEDIUM — Provider name fix** — `aiw-people-hr-weekly` cron has `minimax-plan` (wrong). Trivial fix.
5. **🟢 LOW — Eval aggregate cron wiring** — `scripts/eval-aggregate-pass-rate.py` should run nightly. 4h work.
