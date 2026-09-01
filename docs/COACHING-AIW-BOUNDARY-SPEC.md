# Coaching-AIW Boundary Spec — Phase 9 R3 / Tier C6

> **Date:** 2026-09-01
> **Status:** ADR-0004 #3 (ratified): keep aiw-org ↔ growth-coaching separate
> **Scope:** state-sync architecture between two repos

---

## Context

Per ADR-0004 decision D3, the coaching product (currently planned as
`growth-coaching` repo) will remain **separate** from the aiw-org
repo. The two systems interact through a defined state boundary.

This document captures the boundary spec so that when the
growth-coaching repo is built, both sides agree on the protocol.

---

## Boundary Architecture

```
┌─────────────────────┐                    ┌──────────────────────┐
│      aiw-org        │                    │   growth-coaching    │
│                     │                    │                      │
│  /opt/data/agents   │   boundary file    │  /opt/data/          │
│                     │   (read-only on    │  growth-coaching     │
│  - 63 agents        │    both sides)     │                      │
│  - 182 cron jobs    │                    │  - coaching agents   │
│  - state/* files    │                    │  - customer data     │
│                     │                    │  - state/* files     │
└──────────┬──────────┘                    └──────────┬───────────┘
           │                                          │
           └──────────────┬───────────────────────────┘
                          ▼
                  ┌───────────────┐
                  │   boundary/   │  ← SHARED STATE
                  │               │
                  │ - coaches.ndjson
                  │ - sessions.ndjson
                  │ - signals.ndjson
                  │ - config.yaml
                  └───────────────┘
```

The shared boundary lives at `/opt/data/boundary/` and is **append-only**
NDJSON files. Both repos read but neither writes unilaterally — all
writes happen through scripts that emit schema-validated records.

---

## Boundary Files

| File | Schema | Write Side | Read Side | Notes |
|---|---|---|---|---|
| `coaches.ndjson` | coach_id, name, status, license, last_active | growth-coaching | aiw-org | Coach profiles |
| `sessions.ndjson` | session_id, coach_id, customer_id, started_at, ended_at, summary | growth-coaching | aiw-org | Session log |
| `signals.ndjson` | signal_type, source, target, payload, timestamp | both | both | Cross-system signals |
| `config.yaml` | version, schema_versions, sync_intervals | both (manually) | both | Boundary config |

---

## Sync Protocol

### aiw-org → growth-coaching
When aiw-org detects a coaching-related signal (e.g., a coach engaged
with the org), it appends to `signals.ndjson` with `signal_type`:
- `coach_engagement`
- `coach_performance_alert`
- `customer_lifecycle_event`

### growth-coaching → aiw-org
When growth-coaching captures a session outcome or coach behavior, it
appends to:
- `sessions.ndjson` (sessions)
- `signals.ndjson` (alerts, escalations)

### Polling Cadence
- aiw-org reads `signals.ndjson` every 15 min (cron `aiw-boundary-sync-15min`)
- growth-coaching reads `signals.ndjson` every 15 min (its own cron)

---

## Schema Validation

Every record written to `boundary/*.ndjson` MUST pass
`scripts/boundary-validate.py --file <path>` before being committed.

Validation rules:
- All required fields present
- All enum fields use canonical values
- Timestamps in ISO-8601 UTC
- IDs are UUIDv4 or domain-prefixed slugs

---

## Status (Phase 9 R3)

- ✅ Boundary spec drafted
- ⏳ `/opt/data/boundary/` directory creation pending
- ⏳ `boundary-validate.py` implementation pending
- ⏳ First sync run pending (requires growth-coaching repo to exist)
- ⏳ `aiw-boundary-sync-15min` cron wiring pending

---

## Deferred (not in Phase 9 R3)

- Full growth-coaching repo creation (~19h of work)
- Customer onboarding flow (~8h)
- Coach-coordinator agent (will live in growth-coaching)

---

## References

- ADR-0004 #3: keep aiw-org ↔ growth-coaching separate
- research/coaching-continuation-plan.md (589 lines)
- research/org-upgrade-coaching-context.md (431 lines)
- research/coaching-agents-implementation.md (existing agent design)