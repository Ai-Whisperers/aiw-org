# Document Classifier

> DEMIURGE-078 — `document-intelligence/classifier`

```yaml
id: di-classifier
agent_id: themis-document-classifier
implementation: demiurge/agents/themis-document-classifier/
department: knowledge-mgmt
status: active
role: Assign all standard document attributes to every ingested document.
```

## Role

Reads an incoming document and populates `DocumentEnvelope.derived` (and validates `given` attributes). Urgency is sometimes only determinable by reading content — the Classifier must handle `given.urgency: unknown` and emit confidence scores.

## Inputs

- Raw document or text extract (`body`, optional `storage_uri`)
- Optional `given.audience`, `given.urgency` from creator
- Vocabulary from `docs/terminology/TERMS.md` (DEMIURGE-077)

## Outputs

- Populated `DocumentEnvelope` with `derived` block
- `classifier_model`, `classifier_run_id`, `classified_at`

## Prior art

- **Dublin Core** — `dc_type` mapping on envelope
- **Schema.org `CreativeWork`** — document type taxonomy reference
- **LLM structured extraction** — OpenAI/Anthropic tool calling for typed attribute output

## Manual analog

None. No general document classifier exists today; agents receive unfiltered content or humans route manually.

## Dependencies

- **DEMIURGE-077** — authoritative terms for `document_type`, `formality`, `tone`, `routing_tags`
- **document.md** — envelope schema
- Downstream: Router, Archivist, Miner consume Classifier output

## Phase 3 notes

- Structured output schema must match `DocumentEnvelope.derived`
- Low-confidence fields trigger Router hold or human review per policy
