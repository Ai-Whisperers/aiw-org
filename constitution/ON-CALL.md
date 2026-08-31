# ON-CALL.md

> On-call rotation. Documented per Session 1 cheatsheet + Gap-audit P2 #11.
> **Last updated**: 2026-08-14

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

- `/opt/data/agents/departments/01-operations.md` (Operations dept spec)
- `/opt/data/agents/REVIEW-2026-Q4.md` (90-day review includes on-call metrics)
- `/opt/data/agents-v2/FAILURE-MODES.md` (failure modes that trigger on-call)
