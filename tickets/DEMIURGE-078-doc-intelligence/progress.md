# Progress — DEMIURGE-078

**Status**: done (phase-3)
**Phase**: Phase 1 (design) + Phase 3 (agent souls + dept wiring) complete

## Phase 1 acceptance criteria

- [x] `docs/demiurge/schemas/document.md` created with full schema (`schema_version`, `dc_type`, confidence on derived fields)
- [x] Prior art documented in schema (Dublin Core mapping, ITIL tiers, SKOS reference)
- [x] `departments/knowledge-mgmt/document-intelligence/` with 6 `agent.md` skeletons, each with named prior art
- [x] Dependency on DEMIURGE-077 documented in schema and Classifier skeleton
- [x] Manual analog identified in each `agent.md`
- [x] Document-intelligence terms added to DEMIURGE-077 context
- [x] `progress.md` updated

## Phase 3 acceptance criteria

- [x] Six agent souls in `demiurge/agents/` (Themis, Mnemosyne, Hephaestus, Pheme, Peitho, Orpheus)
- [x] Each agent: `agent.yaml`, `PROMPT.md`, `repo-manifest.yaml`
- [x] `departments/knowledge-mgmt/signals.yaml` and `cadences.md`
- [x] `demiurge/router/document-dispatch-rules.yaml` and `document-timing-rules.yaml`
- [x] `departments/knowledge-mgmt/department.md` wired (active, head_agent, router_id)
- [x] `demiurge/agents/README.md` updated
- [x] Sub-system `agent.md` files reference live `agent_id`

## Agent mapping

| Role | agent_id | Myth name |
|------|----------|-----------|
| Classifier | themis-document-classifier | Themis |
| Archivist | mnemosyne-document-archivist | Mnemosyne |
| Miner | hephaestus-document-miner | Hephaestus |
| Router | pheme-document-router | Pheme |
| Language Quality | peitho-language-quality | Peitho |
| Recordings | orpheus-recordings-agent | Orpheus |

## Legacy agents migration map (DEMIURGE-082)

| Legacy file | Overlap | Disposition |
|---|---|---|
| `agents-prompts/citation-checker.md` | Hephaestus citation extraction (incoming) | Retained — outgoing pre-publication validation; not superseded |
| `agents-prompts/source-curator.md` | Mnemosyne catalog health | Retained for `source-materials/` filesystem sweep; DI pipeline takes over after ingest |
| `agents-prompts/research-tracker.md` | Hephaestus/Mnemosyne process research docs | Pointer added — route docs via `document-ingest`; agent itself not replaced |

## Pipeline

```
recording-upload → Orpheus → transcript-ready → Themis → document-classified
  → parallel: Mnemosyne, Hephaestus, Peitho → Pheme → targets / Hermes handoff
```

## Remaining (runtime, not repo design)

- [ ] Create GitHub repos via `scripts/demiurge/print-repo-init.py` for each agent
- [ ] Register Hermes cron jobs per `cadences.md`
- [ ] Reconcile with Ivan's Hermes profiles (DEMIURGE-072) when shared
- [ ] RAG dual-index for Archivist when catalog volume warrants
- [ ] Whisper/pyannote runtime integration in `aiw-agent-orpheus-recordings-agent` repo

## Review findings addressed (2026-08-29)

- [x] Mermaid pipeline diagram corrected (Classifier → Language Quality → Router)
- [x] Derived field attribution documented (Peitho vs Themis)
- [x] Dispatch rules: removed circular P0/P1 → Pheme; route to final agents with urgency tiers
- [x] Dispatch match on `routing_tags` only (audience copied by Classifier)
- [x] Peitho/Pheme coordination via `quality-assessed` signal + `quality-gate-cleared`
- [x] Hermes handoff via cross_dept signal (removed unsupported `type: router`)
- [x] Taxonomy `knowledge-mgmt` → active; `sources/knowledge-mgmt/catalog.yaml` created
- [x] `tickets/INDEX.md` synced to completed

## Notes from session (2026-08-29)

- Ivan indicated some document intelligence capabilities may already be partially built in Hermes profiles
- Check Ivan's active profiles (DEMIURGE-072) before runtime deployment
- Recordings agent is the highest-value immediate win (replaces manual transcription sessions)
