# DEMIURGE-081: Complete knowledge-mgmt wiring — Thoth/Echo dept coverage, source infra, citation handoff, dispatch rules

**Sprint**: Phase 3 — Meta-Agent Framework (follow-up)
**Size**: 90m
**Owner**: AI
**Depends on**: DEMIURGE-078 (done), DEMIURGE-079 (pending — pattern reference)

## Objective

Close five wiring gaps that prevent the Document Intelligence System from functioning correctly with the rest of the agent ecosystem. All findings surfaced by gap analysis against DEMIURGE-078.

The gaps fall into three clusters:

**Cluster A — Thoth/Echo dept attribution (Critical + High)**
- `sources/knowledge-mgmt/catalog.yaml` declares `maintained_by: mnemosyne-document-archivist`, which is wrong. Mnemosyne maintains the document index (`catalog/index.yaml`); Thoth maintains all `sources/*/catalog.yaml` files consistently across every other dept. This must be fixed to avoid routing catalog-maintenance work to the wrong agent.
- `thoth-literature-scanner/agent.yaml` does not include `knowledge-mgmt` in its departments list, so Thoth won't receive knowledge-mgmt dept context and won't expand the literature catalog.
- `echo-community-scanner/agent.yaml` likewise excludes `knowledge-mgmt` — no community signals will be written for the dept.

**Cluster B — Source catalog infrastructure (High)**
- `sources/knowledge-mgmt/` is missing `community-signals.md` and `gaps.md`. Every other active dept source folder has both. The knowledge-mgmt dept source infrastructure must match the standard pattern.

**Cluster C — Citation handoff signal + dispatch rules (High × 2)**
- `hephaestus-document-miner/PROMPT.md` states citations are forwarded to `thoth-literature-scanner`, but no signal type, routing_tag, or subscription is defined for this handoff. Thoth has no inbound subscription from the DI system.
- `demiurge/router/document-dispatch-rules.yaml` has no rule for `routing_tags: [operations]`, leaving documents tagged for Operations in the dead-letter queue.

## Inputs

- `demiurge/agents/thoth-literature-scanner/agent.yaml`
- `demiurge/agents/echo-community-scanner/agent.yaml`
- `sources/knowledge-mgmt/catalog.yaml`
- `sources/marketing/community-signals.md` — format reference for new community-signals file
- `sources/operations/gaps.md` — format reference for new gaps file
- `departments/knowledge-mgmt/signals.yaml`
- `demiurge/router/document-dispatch-rules.yaml`
- `demiurge/agents/hephaestus-document-miner/PROMPT.md`
- `demiurge/agents/kronos-operations-lead/agent.yaml` — dispatch target for operations (verify id)
- Reference: `sources/marketing/catalog.yaml` — Thoth dept pattern
- Reference: `departments/knowledge-mgmt/department.md` — dept wiring model

## Output

```
demiurge/agents/
└── thoth-literature-scanner/
    └── agent.yaml                    # +knowledge-mgmt in departments
└── echo-community-scanner/
    └── agent.yaml                    # +knowledge-mgmt in departments

sources/knowledge-mgmt/
├── catalog.yaml                      # maintained_by: thoth-literature-scanner
├── community-signals.md              # NEW — monitored communities for KM practices
└── gaps.md                           # NEW — literature gaps vs DIS standards

departments/knowledge-mgmt/
└── signals.yaml                      # +citation-extracted signal definition

demiurge/router/
└── document-dispatch-rules.yaml      # +route-document-audience-operations rule

demiurge/agents/hephaestus-document-miner/
└── PROMPT.md                         # citation handoff: reference citation-extracted signal
```

## Complexity Assessment

**Track**: Complex Implementation

**Rationale**: 7 files across 5 directories. Each change is small but they compose into a coherent wiring story that must be consistent end-to-end (signal emitter → signal definition → signal subscriber → dispatch rule). Creating the two new source files requires content judgment (not just metadata edits).

## Acceptance criteria

### Cluster A — Thoth/Echo dept attribution

- [ ] `sources/knowledge-mgmt/catalog.yaml` — `maintained_by` changed to `thoth-literature-scanner`
- [ ] `demiurge/agents/thoth-literature-scanner/agent.yaml` — `knowledge-mgmt` added to `departments`
- [ ] `demiurge/agents/echo-community-scanner/agent.yaml` — `knowledge-mgmt` added to `departments`

### Cluster B — Source catalog infrastructure

- [ ] `sources/knowledge-mgmt/community-signals.md` created with monitored communities relevant to document intelligence and knowledge management practices
- [ ] `sources/knowledge-mgmt/gaps.md` created with gap analysis against DIS standards (Dublin Core, W3C PROV-O, SKOS), cross-referenced to `sources/knowledge-mgmt/catalog.yaml`

### Cluster C — Citation handoff + dispatch rules

- [ ] `departments/knowledge-mgmt/signals.yaml` — `citation-extracted` signal added: direction `internal`, sender `hephaestus-document-miner`, subscriber `thoth-literature-scanner`, routing_tag `[citation, literature]`
- [ ] `demiurge/router/document-dispatch-rules.yaml` — rule `route-document-audience-operations` added for `routing_tags: [operations]` → kronos-operations-lead
- [ ] `demiurge/agents/hephaestus-document-miner/PROMPT.md` — citation output row updated to reference `citation-extracted` signal type

## Risks

- Operations lead agent ID may differ from `kronos-operations-lead` — verify before writing dispatch rule.
- `citation-extracted` signal name must be checked against existing signal naming conventions in `signals.yaml` before publishing.
- Echo's `community-signals.md` scan targets for knowledge-mgmt should reference practitioner communities for KM/document-intelligence topics, not the same sources as marketing/sales.
