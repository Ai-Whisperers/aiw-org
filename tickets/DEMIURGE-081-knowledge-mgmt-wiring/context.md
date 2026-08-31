# Context — DEMIURGE-081

**Status**: done
**Focus**: Five wiring gaps across knowledge-mgmt ecosystem

## Current state

DEMIURGE-078 Phase 1 (design) and Phase 3 (agent souls + dept wiring) are marked done. All six DI agent.yaml and PROMPT.md files exist. However, the following gaps prevent correct operation:

1. **catalog.yaml wrong owner** — `sources/knowledge-mgmt/catalog.yaml` says `maintained_by: mnemosyne-document-archivist`. Thoth maintains all `sources/*/catalog.yaml` per its PROMPT.md (`inputs: sources/*/catalog.yaml`). Mnemosyne maintains `catalog/index.yaml` (the document index). This is a naming collision that will silently route work to the wrong agent.

2. **Thoth excluded from knowledge-mgmt** — `thoth-literature-scanner/agent.yaml` lists `marketing, sales, product-discovery` but not `knowledge-mgmt`. The literature catalog for the dept won't expand.

3. **Echo excluded from knowledge-mgmt** — same pattern as Thoth; no community signals will flow.

4. **Missing community-signals.md and gaps.md** — every other active dept under `sources/` has both. The knowledge-mgmt folder only has `catalog.yaml`.

5. **Hephaestus→Thoth citation handoff undefined** — PROMPT says "forward citations to Thoth" with no signal name, no signals.yaml entry, no Thoth subscription. The handoff is a dead letter.

6. **Operations routing missing** — `document-dispatch-rules.yaml` has rules for marketing, sales, product-discovery, and a catch-all for human-only. Documents tagged `operations` have no route and end up in the dead-letter queue.

## Components

| File | Change |
|---|---|
| `sources/knowledge-mgmt/catalog.yaml` | Fix maintained_by |
| `demiurge/agents/thoth-literature-scanner/agent.yaml` | Add knowledge-mgmt dept |
| `demiurge/agents/echo-community-scanner/agent.yaml` | Add knowledge-mgmt dept |
| `sources/knowledge-mgmt/community-signals.md` | CREATE |
| `sources/knowledge-mgmt/gaps.md` | CREATE |
| `departments/knowledge-mgmt/signals.yaml` | Add citation-extracted |
| `demiurge/router/document-dispatch-rules.yaml` | Add operations rule |
| `demiurge/agents/hephaestus-document-miner/PROMPT.md` | Reference citation-extracted signal |

## Dependencies

- DEMIURGE-079 — provides Operations lead agent id (Kronos). Verify id before writing dispatch rule. Can proceed with clusters A and B while pending.

## Integration points

- `departments/knowledge-mgmt/cadences.md` — Thoth and Echo cadences already include knowledge-mgmt in dept column? Verify when working on Cluster A.
- `departments/knowledge-mgmt/department.md` — lists Thoth and Echo as associated agents? Verify.

## Immediate next steps

1. Verify Operations lead agent id in `demiurge/agents/` (pattern: `*-operations-lead*` or `kronos*`)
2. Verify Thoth/Echo cadences.md for knowledge-mgmt inclusion
3. Fix Cluster A (catalog.yaml, Thoth agent.yaml, Echo agent.yaml) — fastest
4. Create Cluster B (community-signals.md, gaps.md)
5. Implement Cluster C (signal definition, dispatch rule, PROMPT update)
