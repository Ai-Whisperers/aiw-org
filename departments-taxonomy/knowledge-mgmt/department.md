# Knowledge Management Department

> DEMIURGE-078

```yaml
id: knowledge-mgmt
name: Knowledge Management
tier: 2
status: active
mission: Classify, route, catalog, and extract value from every document in the org so agents receive only what is relevant.
head_agent: mnemosyne-document-archivist
router_id: pheme-document-router
source_catalog_id: catalog-knowledge-mgmt
```

## Sub-system: document-intelligence

All six agents below live under `document-intelligence/`. See [`docs/demiurge/schemas/document.md`](../../docs/demiurge/schemas/document.md) for the document envelope schema.

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| di-classifier | Document Classifier | themis-document-classifier | active |
| di-router | Document Router | pheme-document-router | active |
| di-archivist | Document Cataloger / Archivist | mnemosyne-document-archivist | active |
| di-miner | Document Miner | hephaestus-document-miner | active |
| di-language-quality | Language Quality Agent | peitho-language-quality | active |
| di-recordings | Recordings Agent | orpheus-recordings-agent | active |

## Inbound signals

| id | from | SLA |
|----|------|-----|
| document-ingest | org-wide | PT1H |
| recording-upload | human, any dept | PT4H |
| terminology-update | DEMIURGE-077 | PT24H |

See [signals.yaml](signals.yaml).

## Outbound signals

| id | to | SLA |
|----|------|-----|
| document-routed | target agent/dept | per derived.urgency |
| action-item-extracted | owning dept | PT24H |
| decision-logged | relevant depts | PT24H |
| nugget-surfaced | target agent/dept | PT48H |
| quality-report | author / human-only | PT72H |

## Router config

- Document dispatch: `demiurge/router/document-dispatch-rules.yaml`
- Document timing: `demiurge/router/document-timing-rules.yaml`
- Revenue signals (handoff): `demiurge/router/dispatch-rules.yaml` via `hermes-router-revenue`

## Dependencies

- **DEMIURGE-077** — vocabulary for classification and terminology compliance (`docs/terminology/TERMS.md`)
- **DEMIURGE-072** — reconcile with Hermes profiles when Ivan shares active profiles
