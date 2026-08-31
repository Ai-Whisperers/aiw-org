# Context — DEMIURGE-077

Identified in 2026-08-28 planning session as a gap across all layers of the system.

Related files (terms currently used without authoritative definition):
- `docs/demiurge/department-taxonomy-v1.md` — uses tier, status, skeleton, active
- `demiurge/schemas/` — defines signal, agent, soul, role, department schemas
- `departments/*/signals.yaml` — uses signal types, urgency, routing_tags
- `ROLES-INVENTORY.md` — uses tier coding, role vs function
- `demiurge/router/revenue-signals.yaml` — uses signal, routing, dispatch

Ivan owns the communication + information type vocabulary (formality, tone, urgency, information types).
AI can draft the org structure + agent model vocabulary.

This document feeds DEMIURGE-078 (document intelligence) — classifiers need vocabulary to classify against.

## document-intelligence-terms (from DEMIURGE-078)

Terms to define in `TERMS.md` for Document Intelligence System (Phase 1 scope contribution):

| term | category | notes |
|------|----------|-------|
| document envelope | documents & knowledge | Wrapper around raw content: identity, given + derived attributes (`docs/demiurge/schemas/document.md`) |
| document_type | documents & knowledge | Org-specific type: plan, report, signal, transcript, research, spec, communication, recording |
| given attribute | documents & knowledge | Set by creator at ingest; may be empty or `unknown` |
| derived attribute | documents & knowledge | Set by Document Classifier; includes confidence scores |
| nugget | documents & knowledge | Valuable embedded information; may be intentional (information foraging) |
| routing_tag | communication | Dispatch hint for Document Router; aligns with signal `routing_tags` |
| language quality score | documents & knowledge | Normalized 0.0–1.0; Flesch-Kincaid inspired readability |
| terminology compliance | documents & knowledge | Normalized 0.0–1.0; SKOS-inspired check vs TERMS.md |
| recordings pipeline | documents & knowledge | ASR → transcript envelope → classify → mine → route → archive |
| information extraction | documents & knowledge | NER + relation extraction; Miner output types (action item, decision, nugget) |

Schema reference: `docs/demiurge/schemas/document.md` (DEMIURGE-078). Add definitions here first; Classifier and Language Quality agents defer to TERMS.md.
