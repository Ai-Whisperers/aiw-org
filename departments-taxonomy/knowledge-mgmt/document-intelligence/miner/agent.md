# Document Miner

> DEMIURGE-078 — `document-intelligence/miner`

```yaml
id: di-miner
agent_id: hephaestus-document-miner
implementation: demiurge/agents/hephaestus-document-miner/
department: knowledge-mgmt
status: active
role: Extract structured assets from documents — action items, decisions, references, nuggets, new terminology.
```

## Role

Mines documents for durable value. Action items may become tickets or signals; decisions log to a decision register; references forward to Thoth (literature scanner); nuggets surface to relevant dept or agent; unknown terms flag to DEMIURGE-077 terms registry.

Intentional nuggets: if a author embeds strategic insight deliberately, Miner surfaces it without manual routing.

## Inputs

- Classified `DocumentEnvelope` with `body`
- `derived.has_action_items`, `has_decisions`, `has_nuggets` hints from Classifier

## Outputs

- `ActionItem`, `Decision`, `Nugget` records (see document.md)
- Signals to owning depts
- Terminology candidates for DEMIURGE-077

## Prior art

- **Information extraction** — NER + relation extraction (established NLP)
- **DACI framework** — decision records with driver/approver/contributor/informed roles
- **Information foraging** (Pirolli & Card, 1999) — "nugget" as valuable embedded information

## Manual analog

Manual extraction of action items and decisions from meeting notes and long documents.

## Dependencies

- **Classifier** — content flags and document_type
- **DEMIURGE-077** — new term proposals
- **thoth-literature-scanner** — citation/reference handoff (narrow domain today)

## Phase 3 notes

- Confidence thresholds per asset type before auto-creating tickets
- Decisions require minimum fields per DACI-inspired schema in document.md
