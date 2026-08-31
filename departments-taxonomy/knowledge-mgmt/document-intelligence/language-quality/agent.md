# Language Quality Agent

> DEMIURGE-078 — `document-intelligence/language-quality`

```yaml
id: di-language-quality
agent_id: peitho-language-quality
implementation: demiurge/agents/peitho-language-quality/
department: knowledge-mgmt
status: active
role: Assess spelling, grammar, tone, terminology compliance, clarity, and completeness; produce quality reports, not blockers (except formal external comms).
```

## Role

Spell check and beyond: tone consistency with stated audience/formality; terminology compliance against DEMIURGE-077; clarity score for target audience; completeness check (e.g. plan has required sections). Quality issues produce a report — not rejection — unless document is formal external communication (then P1 quality gate).

## Inputs

- Document `body` and `derived.formality`, `derived.audience`
- `docs/terminology/TERMS.md` (DEMIURGE-077)

## Outputs

- `language_quality_score`, `terminology_compliance_score` on envelope (or quality sidecar)
- Quality report artifact for author
- Optional P1 gate flag for formal external communications

## Prior art

- **Flesch-Kincaid** — readability scoring
- **LanguageTool** — open-source grammar/spelling
- **SKOS** (W3C) — controlled vocabulary / terminology compliance model
- **Vale** — prose linting and style rules

## Manual analog

Manual review before sending important documents; ad hoc spell check.

## Dependencies

- **DEMIURGE-077** — terminology definitions for compliance scoring
- **Classifier** — formality, tone, document_type for rule selection
- May run in parallel with or after Classifier depending on pipeline design (Phase 3)

## Phase 3 notes

- Formal external `communication` type → enforce P1 gate on failure
- Scores normalized 0.0–1.0 on `DocumentEnvelope.derived`
