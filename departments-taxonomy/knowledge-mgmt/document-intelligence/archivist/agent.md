# Document Cataloger / Archivist

> DEMIURGE-078 — `document-intelligence/archivist`

```yaml
id: di-archivist
agent_id: mnemosyne-document-archivist
implementation: demiurge/agents/mnemosyne-document-archivist/
department: knowledge-mgmt
status: active
role: Maintain the master index of all documents with classified attributes and relationships.
```

## Role

Active cataloging — not passive storage. Tags documents by topic, source, date, type, department; maintains relationships (plan → tickets → outputs); enables retrieval ("what decisions were made about X?"). Flags `has_nuggets` documents for Miner follow-up.

## Inputs

- Classified `DocumentEnvelope`
- Miner outputs (optional links: action items, decisions, nuggets)

## Outputs

- Catalog index entries (metadata + refs)
- Relationship graph edges between documents and artifacts
- Retrieval API / query surface for agents (Phase 3)

## Prior art

- **RAG dual-index** — BM25 keyword + vector embeddings (LlamaIndex/Haystack document store pattern)
- **W3C PROV-O** — provenance and lineage (`source_id`, recording → transcript)

## Manual analog

None. No org-wide document catalog or archivist role exists today.

## Dependencies

- **Classifier** — attributes required for indexing facets
- **document.md** — envelope schema
- **artifacts.md** — links to artifact records where applicable

## Phase 3 notes

- Dual-index target: keyword + semantic search
- Retention and visibility follow `Artifact.visibility` patterns where linked
