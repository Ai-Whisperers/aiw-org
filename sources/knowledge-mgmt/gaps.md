# Knowledge Management — Literature Gap Analysis

> DEMIURGE-081

## In literature, missing or weak in our model

| Gap | Literature says | Action |
|-----|-----------------|--------|
| Dublin Core full element set | DCMI: 15 core elements + refinements for rich metadata | Extend `document.md` envelope with optional DC elements beyond current seed |
| PROV-O lineage chain | W3C PROV-O: wasDerivedFrom, wasGeneratedBy for audit trail | Wire Mnemosyne archival records to PROV-O-compatible provenance fields |
| SKOS concept schemes | W3C SKOS: broader/narrower/related for controlled vocabularies | Link `TERMS.md` to SKOS concept scheme; Thoth expands catalog with SKOS refs |
| Confidence on derived attributes | DIS design: classifier inference must carry confidence | Enforced in `document-classified` payload; verify Peitho gate respects low-confidence |
| routing_tags ↔ audience mirror | catalog.yaml insight #2: audience values must appear in routing_tags | Validate Themis classifier output against dispatch rule match convention |
| Citation handoff pipeline | Hephaestus→Thoth citation flow requires explicit signal | `citation-extracted` signal wired in DEMIURGE-081 |

## In our model, well covered (catalog seed)

| Capability | Source | Benchmark alignment |
|------------|--------|---------------------|
| Dublin Core basics | km-dublin-core | DCMI 15-element model — partial (seed only) |
| Provenance ontology | km-prov-o | W3C PROV-O — referenced, not fully implemented |
| Controlled vocabulary | km-skos | W3C SKOS — TERMS.md exists, SKOS mapping pending |
| Urgency tiers | km-itil-urgency | ITIL P0–P3 — wired in classifier + dispatch |
| Internal terminology | km-terms-md | AI Whisperers TERMS.md — active registry |

## Legacy → DEMIURGE migration gaps

| Legacy pattern | Missing DEMIURGE structure | DEMIURGE-081 action |
|----------------|---------------------------|---------------------|
| Hephaestus citation forward (PROMPT prose) | No signal type, no Thoth subscription | `citation-extracted` signal + PROMPT update |
| Operations audience routing | No dispatch rule for `routing_tags: [operations]` | `route-document-audience-operations` rule |
| Thoth catalog maintenance | `maintained_by: mnemosyne-document-archivist` (wrong agent) | Fixed to `thoth-literature-scanner` |
| Echo community scan | knowledge-mgmt excluded from Echo departments | Added to `echo-community-scanner/agent.yaml` |

## AI-native document intelligence benchmark

Sourced from W3C standards and practitioner KM playbooks:

| Practice | Benchmark | AI Whisperers today |
|----------|-----------|---------------------|
| Metadata schema | Dublin Core minimum + domain extensions | Seed catalog — partial |
| Provenance tracking | PROV-O for all derived attributes | Design intent documented — not runtime |
| Controlled vocabulary | SKOS concept scheme with versioning | TERMS.md — flat list, no SKOS |
| Quality gate before route | Assess before dispatch (Peitho→Pheme) | Wired — aligned |
| Citation expansion | Miner extracts → literature scanner expands catalog | Signal wired in DEMIURGE-081 |
| Community signal intake | Echo scans practitioner communities per dept | community-signals.md created |

## Recommended additions (skeleton)

```yaml
- id: skos-vocabulary-curator
  tier: mid
  trigger: TERMS.md exceeds 50 entries
- id: provenance-auditor
  tier: senior
  trigger: first compliance audit requiring lineage proof
```

## Next scan

Quarterly or when a new W3C recommendation affects document.md schema.
