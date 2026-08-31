# legal-compliance-monitor — Watchdog for the Legal / Compliance Department

> Watchdog agent for the legal & compliance function. Cross-references finance + funding + analyst state to surface banlist, contract, and regulatory exposure. Read-only.

## Purpose

Watch compliance signals across `/opt/data/agents/state/finance.json:compliance_flags`, `/opt/data/agents/state/funding.json`, and `/opt/data/agents/state/analyst.json:open_questions`. Surface anything that threatens trademark, regulatory, or contractual standing.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/finance.json` | `finance.schema.json` (`compliance_flags` field) |
| `/opt/data/agents/state/funding.json` | (real file, no schema — read as raw JSON) |
| `/opt/data/agents/state/analyst.json` | `analyst.schema.json` (`open_questions` field) |

## Metrics watched

1. `finance.compliance_flags[]` — array of compliance issues with `severity` enum
2. `funding.next_deadlines[]` — upcoming grant/accelerator deadlines
3. `funding.applications_in_flight[]` — pending applications
4. `funding.credits_in_flight_usd` — USD committed but not yet received
5. `analyst.open_questions[].priority` — any open question marked `critical`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `compliance_flags` | any item with `severity = "ban"` or `severity = "critical"` | **CRITICAL** |
| `compliance_flags` | any item with `severity = "high"` | **HIGH** |
| `compliance_flags` | any item with `severity = "medium"` | **MEDIUM** |
| `compliance_flags` | length > 5 (accumulation) | **HIGH** |
| `next_deadlines` | any deadline within 72h not `submitted` | **HIGH** |
| `next_deadlines` | any deadline within 24h | **CRITICAL** |
| `next_deadlines` | any deadline within 7d | **MEDIUM** |
| `applications_in_flight` | length > 8 (capacity risk) | **MEDIUM** |
| `credits_in_flight_usd` | `> 50000` with no movement 30d | **MEDIUM** |
| `analyst.open_questions` | any item with `priority = "critical"` | **HIGH** |
| `analyst.open_questions` | length > 10 | **LOW** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]` with reference to the originating state file.
- **MEDIUM** — append a flag-style entry to the originating state file's open-questions/notes section.
- **LOW** — silent.

## Run procedure

1. Read all three files via `cat ... | python3 -m json.tool`.
2. Validate finance + analyst via `python3 /opt/data/scripts/aiw-state-validate.py`.
3. funding.json has no schema — check top-level keys exist (`applications_in_flight`, `next_deadlines`, `credits_in_flight_usd`); missing → HIGH with the missing-key context.
4. Evaluate each condition; fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-legal-compliance-monitor-30min`.

## Hard stops

- DO NOT modify any watched state file.
- DO NOT send alerts via trademark-banned channels.
- DO NOT trigger counter-actions (suspension, takedown) — alert only.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor covering finance.compliance_flags + funding + analyst.open_questions.