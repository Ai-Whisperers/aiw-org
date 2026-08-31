# DEMIURGE-082: Document legacy agents-prompts → DI migration mapping

**Sprint**: Phase 3 — Meta-Agent Framework (follow-up)
**Size**: 30m
**Owner**: AI
**Depends on**: DEMIURGE-078 (done)

## Objective

Add migration annotations to three `agents-prompts/` files that partially overlap with DEMIURGE-078 DI agents, and create a compact legacy↔DI bridge note in the DEMIURGE-078 ticket. Without this, future work may unknowingly maintain or expand superseded prompts instead of the canonical DI agents.

Gap analysis surfaced these files as "partially overlapping but not annotated":

| Legacy file | Overlaps with | Risk |
|---|---|---|
| `agents-prompts/citation-checker.md` | `hephaestus-document-miner` citation extraction | Duplicate citation work; unclear ownership |
| `agents-prompts/source-curator.md` | `mnemosyne-document-archivist` freshness/naming | Duplicate freshness sweeps; competing writes |
| `agents-prompts/research-tracker.md` | `hephaestus-document-miner` research output extraction | Unclear if research docs enter the DI pipeline |

`research-tracker.md` is lower risk (complementary, not directly replaced) but benefits from a pointer.

## Inputs

- `agents-prompts/citation-checker.md`
- `agents-prompts/source-curator.md`
- `agents-prompts/research-tracker.md`
- `tickets/DEMIURGE-078-doc-intelligence/progress.md` — append migration note
- `demiurge/agents/hephaestus-document-miner/PROMPT.md` — citation/extraction owner reference
- `demiurge/agents/mnemosyne-document-archivist/PROMPT.md` — archival/freshness owner reference

## Output

```
agents-prompts/
├── citation-checker.md          # + migration header: superseded by hephaestus-document-miner
├── source-curator.md            # + migration header: superseded by mnemosyne-document-archivist
└── research-tracker.md          # + doc note: research docs enter DI via document-ingest signal

tickets/DEMIURGE-078-doc-intelligence/
└── progress.md                  # + migration map note appended
```

## Complexity Assessment

**Track**: Simple Fix

**Rationale**: Annotation-only. No behavioral changes, no new agents, no signal wiring. Append a short YAML/markdown header to 3 files and one progress.md append.

## Acceptance criteria

- [ ] `agents-prompts/citation-checker.md` has a `## Migration Status` note: "Superseded by `hephaestus-document-miner` (DEMIURGE-078). Use DI pipeline for citation extraction."
- [ ] `agents-prompts/source-curator.md` has a `## Migration Status` note: "Superseded by `mnemosyne-document-archivist` (DEMIURGE-078). Freshness sweeps are now part of the Archivist cadence."
- [ ] `agents-prompts/research-tracker.md` has a note directing research document outputs to the `document-ingest` signal for DI pipeline processing.
- [ ] `tickets/DEMIURGE-078-doc-intelligence/progress.md` has an appended entry naming all three legacy files and their DI successors.

## Risks

Low. Documentation-only change; no functional impact.
