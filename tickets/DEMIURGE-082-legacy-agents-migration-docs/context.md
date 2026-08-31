# Context — DEMIURGE-082

**Status**: pending
**Focus**: Add migration annotations to legacy agents-prompts files

## Current state

Three `agents-prompts/` files exist without any indication they are superseded or partially replaced by DEMIURGE-078 DI agents:

- `citation-checker.md` — Erebus checks citations before external publication. The DI system's Hephaestus now owns citation extraction from all ingested documents. The boundary is unclear: is Erebus still relevant for pre-publication checks, or fully replaced?
- `source-curator.md` — Erebus runs weekly freshness sweeps on `source-materials/`. Mnemosyne now archives and manages document indices. Again, boundary unclear.
- `research-tracker.md` — Erebus provides weekly research visibility. Research documents (theses, publications) are the exact input class for the DI pipeline, but the file has no pointer.

No developer picking up these files would know the DI system now handles overlapping work.

## Components

- `agents-prompts/citation-checker.md` — prepend or append migration status note
- `agents-prompts/source-curator.md` — prepend or append migration status note
- `agents-prompts/research-tracker.md` — add DI pointer note
- `tickets/DEMIURGE-078-doc-intelligence/progress.md` — append migration map summary

## Immediate next steps

1. Read all three legacy files to understand current scope
2. Read Hephaestus and Mnemosyne PROMPT.md to confirm coverage
3. Write migration status blocks — be precise about what's superseded vs complementary
4. Append to DEMIURGE-078 progress.md
