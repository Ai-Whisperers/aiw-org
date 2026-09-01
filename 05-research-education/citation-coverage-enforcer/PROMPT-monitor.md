# Monitor — citation-coverage-enforcer

> Auto-generated monitor wrapper. Phase 9 R3 (Tier A1.8 closure).

## What this monitor checks

Every daily cycle:

1. State file updated within last cycle
2. No hard_stop violations in last run
3. transfer_targets: at least one downstream agent contacted
4. Brief written to `outbox/` (if cadence != daily)

## Health indicators

- ✅ Green: state file fresh + brief written + no violations
- 🟡 Yellow: state file stale (2x cadence period)
- 🔴 Red: hard_stop violation OR state missing

## Build info

- Built: Phase 9 R3 (2026-09-01)
- Owner: research-tracker
- Topology: stream-aligned
- Cluster: run