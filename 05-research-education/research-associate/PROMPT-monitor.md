# Monitor — research-associate

> Auto-generated monitor wrapper. Phase 7 R6.

## What this monitor checks

Every weekly:

1. State file updated within last cycle
2. No hard_stop violations in last run
3. transfer_targets: at least one downstream agent contacted
4. Brief written to `outbox/` (if cadence != daily)

## Health indicators

- ✅ Green: state file fresh + brief written + no violations
- 🟡 Yellow: state file stale (2x cadence period)
- 🔴 Red: hard_stop violation OR state missing

## Build info

- Built: Phase 7 R6 (2026-09-01)
- Owner: ai-ops-coordinator
- Topology: stream-aligned
- Cluster: enable
