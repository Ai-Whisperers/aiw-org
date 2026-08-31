# DEMIURGE-080: Signal Schema Normalization and Routing Tag Correctness

**Sprint**: Phase 2 — Reference Dept (Operations) / Phase 1 follow-up
**Size**: 120m
**Owner**: AI
**Depends on**: DEMIURGE-077 (for final vocabulary decisions on `priority`, `urgency`, `directionality`)

## Objective

Fix two critical dead dispatch routes and normalize all signal type definitions across
`marketing`, `sales`, `product-discovery` (and `operations`) to match the authoritative schema
in `docs/demiurge/schemas/signal-channel.md`. Extend the schema to cover `SignalType`
definitions and `QuorumDefinition` — both patterns are in use but have no formal schema.

## Why this matters

- Two dispatch rules currently **never match** their intended signals (routing is broken at runtime).
- DEMIURGE-077 (Terminology Library) and DEMIURGE-078 (Document Intelligence) both depend on a
  consistent, complete signal schema. The vocabulary library defines terms; this ticket fixes
  the structural mismatches that would invalidate any classifier or router built on top.
- The schema in `signal-channel.md` models a runtime Signal **instance**, not a signal **type
  definition**. Every `signals.yaml` file is a type registry, not a runtime store — this
  distinction is missing and causes all field-level mismatches.

## Scope

Files modified:
- `departments/marketing/signals.yaml`
- `departments/sales/signals.yaml`
- `departments/product-discovery/signals.yaml`
- `departments/operations/signals.yaml` (field normalization only)
- `demiurge/router/dispatch-rules.yaml` (routing tag fix for `route-customer-signal`)
- `docs/demiurge/schemas/signal-channel.md` (schema extension)

## Acceptance Criteria

### Critical routing fixes
- [ ] `marketing-campaign-brief` inbound in `pd/signals.yaml` has `routing_tags: [campaign, brief]`
- [ ] `customer-signal-raw` in `pd/signals.yaml` has `routing_tags: [customer-voice]` (or
  `route-customer-signal` dispatch rule updated to match the actual tag — see Decision 1)
- [ ] `marketing-content-ready` routing_tags consistent: both marketing (out) and sales (in) use
  `[content, pipeline]`
- [ ] `sales-pipeline-feedback` routing_tags consistent across marketing (in), sales (out),
  pd (in): agree on a canonical tag set (see Decision 2)

### Schema extension
- [ ] `signal-channel.md` has a `## SignalType` section defining the type-definition schema
  (separate from the runtime `Signal` instance schema)
- [ ] `signal-channel.md` has a `## QuorumDefinition` section documenting the structure in use
  (`required_count`, `required_agents`, `time_window`, `fallback`, `fallback_target`, `on_met`)
- [ ] `signal-channel.md` validation checklist updated to include SignalType rules

### Field normalization
- [ ] Field `quorum` → `quorum_required` in all signals.yaml files (or schema updated to
  canonicalize `quorum`) — see Decision 3
- [ ] Field `payload_schema` in `marketing/signals.yaml` renamed to `payload` and aligned with
  schema payload conventions
- [ ] Field `sender: <dept>` normalized to `sender_id` (agent) + `sender_dept_id` (dept) per
  schema, or schema updated to accept `sender: <dept_id>` as dept-level shorthand — see Decision 4
- [ ] Field `recipients` changed from bare string list `[sales]` to typed objects
  `[{type: department, id: sales}]` across all files, or schema updated with a `recipients`
  shorthand section
- [ ] `priority: normal` added to all signal type definitions that omit it (with note that
  `priority` defaults are pending DEMIURGE-077 Ivan review for P0–P3 mapping)
- [ ] `type: internal` in `pd/signals.yaml:customer-signal-raw` replaced with a valid enum value
  (`direct` is the natural choice for agent-to-agent internal signals)

### Type enum coverage
- [ ] `signal-channel.md` type enum updated to include `kpi` if that type is retained in
  `operations/signals.yaml`, or `operations/signals.yaml` updated to use a valid type

## Decisions Required (before or during implementation)

| # | Decision | Options | Owner |
|---|---|---|---|
| 1 | `customer-signal-raw` routing tag | A) Add `[customer-voice]` to signal OR B) Change dispatch rule tag to match signal | AI |
| 2 | `sales-pipeline-feedback` canonical tags | A) `[pipeline, win-loss]` (marketing view) OR B) `[win-loss, customer-voice]` (pd view) OR C) `[pipeline, win-loss, customer-voice]` (union) | AI (no Ivan input required) |
| 3 | `quorum` vs `quorum_required` | A) Rename field to `quorum_required` in all YAMLs OR B) Update schema to use `quorum` | AI |
| 4 | `sender` shorthand | A) Expand to `sender_id` + `sender_dept_id` (schema-conformant) OR B) Keep `sender: <dept>` and document as dept-level shorthand in schema | AI |
| 5 | `recipients` shorthand | A) Expand to typed objects OR B) Add shorthand section to schema | AI |
| 6 | `type: kpi` in operations | A) Add `kpi` to schema enum OR B) Change to `cross_dept`/`internal` | AI |

All decisions are stylistic normalization choices with no external dependency — AI can resolve at implementation time using consistency-first heuristic.

## Implementation Approach

### Phase 1 — Critical routing fixes (30m)
Fix the two dead dispatch routes first; these are operational and block correct routing.

1. `pd/signals.yaml`: add `routing_tags: [campaign, brief]` to `marketing-campaign-brief` inbound
2. `pd/signals.yaml`: add `routing_tags: [customer-voice]` to `customer-signal-raw` (Decision 1A)
3. Sync `marketing-content-ready` tags: update `sales/signals.yaml` inbound to `[content, pipeline]`
4. Sync `sales-pipeline-feedback` tags: adopt `[pipeline, win-loss, customer-voice]` union
   across all three departments (Decision 2C — most inclusive, no information loss)

### Phase 2 — Schema extension (30m)
Add missing schema sections to `signal-channel.md`.

1. Add `## SignalType` section (the type-registry schema)
2. Add `## QuorumDefinition` section (documenting existing practice)
3. Add `kpi` to type enum OR document as operations-internal type
4. Update validation checklist

### Phase 3 — Field normalization (60m)
Apply field decisions across all signals.yaml files.

1. Rename `quorum` → `quorum_required` across all 4 files (Decision 3A — schema-conformant)
2. Rename `payload_schema` → `payload` in marketing/signals.yaml
3. Normalize `sender` to `sender_id` + `sender_dept_id` (Decision 4A — schema-conformant)
4. Normalize `recipients` to typed objects (Decision 5A — schema-conformant)
5. Add `priority: normal` to all signal type definitions missing it
6. Change `type: internal` → `type: direct` in `customer-signal-raw`

## Risks

- DEMIURGE-077 is pending Ivan review for urgency/priority vocabulary. The `priority` field
  normalization in this ticket uses `normal` as default — may need update once Ivan confirms
  the P0–P3 mapping. Mark `priority` entries with a comment noting pending review.
- `operations/signals.yaml` was created by DEMIURGE-075 and uses the same `quorum` pattern.
  Including it in field normalization keeps consistency but touches a recently completed ticket's
  output.

## Questions

- Should `signal-channel.md` be renamed/versioned (v2) to reflect the schema additions, or
  just updated in place? (Recommend: update in place, bump internal schema_version if defined.)
