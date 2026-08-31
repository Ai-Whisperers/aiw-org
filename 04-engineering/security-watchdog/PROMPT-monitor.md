# security-watchdog-monitor — Watchdog for Security Watchdog

> Watchdog for security-watchdog. Surfaces compliance breaches, missing scans, secrets leaks. Read-only.

## Purpose

Watch `/opt/data/agents/state/engineering.json` (security incidents, audit findings, secret-rotation status) and `(real file, no schema — read raw from /opt/data/agents/state/coord.json:compliance_breaches[])` if present. Lead agent is `security-watchdog`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/engineering.json` | `engineering.schema.json` |
| `/opt/data/agents/state/coord.json` | `coord.schema.json` (compliance decisions) |

## Metrics watched

1. `engineering.security_audit_findings[]` — open security audit findings
2. `engineering.secret_rotations_overdue` — secrets past rotation window
3. `engineering.last_security_scan` — last full security scan timestamp
4. `engineering.last_secret_audit` — last secrets audit timestamp
5. `engineering.incidents_72h` filtered by `tag=security` — security-tagged incidents
6. `coord.compliance_breaches[]` — compliance breach log

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `secret_rotations_overdue` | `> 0` | **HIGH** |
| `secret_rotations_overdue` | `> 3` | **CRITICAL** |
| `security_audit_findings[]` | any CRITICAL severity finding | **CRITICAL** |
| `security_audit_findings[]` | length > 5 | **HIGH** |
| `security_audit_findings[]` | any finding age > 30 days unresolved | **HIGH** |
| `last_security_scan` | stale > 7 days | **MEDIUM** |
| `last_security_scan` | stale > 14 days | **HIGH** |
| `last_secret_audit` | stale > 30 days | **HIGH** |
| `incidents_72h` (tag=security) | any P0 | **CRITICAL** |
| `incidents_72h` (tag=security) | length > 2 | **HIGH** |
| `compliance_breaches[]` | length > 0 | **CRITICAL** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/security-watchdog/monitor-notes/YYYY-MM-DD.md` (do NOT mutate any state file — schemas are `additionalProperties: false`).

## Run procedure

1. Read state files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py engineering coord`. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *` — daily 09:00 PYT. Alias: `aiw-security-watchdog-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-rotate secrets.
- DO NOT auto-remediate findings — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 3).

