# Tracker — DEMIURGE-080

## Phase 1 — Critical routing fixes (est. 30m)

- [x] `pd/signals.yaml`: add `routing_tags: [campaign, brief]` to `marketing-campaign-brief` inbound
- [x] `pd/signals.yaml`: add `routing_tags: [customer-voice]` to `customer-signal-raw`
- [x] `sales/signals.yaml`: update `marketing-content-ready` inbound tags to `[content, pipeline]`
- [x] `marketing/signals.yaml`, `sales/signals.yaml`, `pd/signals.yaml`: sync `sales-pipeline-feedback`
  tags to union `[pipeline, win-loss, customer-voice]`

## Phase 2 — Schema extension (est. 30m)

- [x] `signal-channel.md`: add `## SignalType` section (type-registry schema, distinct from Signal instance)
- [x] `signal-channel.md`: add `## QuorumDefinition` section
- [x] `signal-channel.md`: add `kpi` to type enum or document as operations-internal extension
- [x] `signal-channel.md`: update validation checklist

## Phase 3 — Field normalization (est. 60m)

- [x] All signals.yaml: rename `quorum:` → `quorum_required:`
- [x] `marketing/signals.yaml`: rename `payload_schema:` → `payload:`
- [x] All signals.yaml: `sender`/`recipients` shorthand documented in schema (Decision 4B/5B — no YAML expansion)
- [x] All signals.yaml: add `priority: normal` to signal type definitions missing it
      (note: pending DEMIURGE-077 Ivan review for P0-P3 alignment)
- [x] `pd/signals.yaml`: `customer-signal-raw` already `type: direct` (pre-satisfied)

## Done

- 2026-08-29: All phases complete. Routing tags synced; schema extended; fields normalized.
