# ADR Index — AIW Org Architecture Decision Records

> **One ADR per architectural decision.** Each must justify its choice with alternatives + consequences.
> Use `0000-template.md` for new entries. Save as `NNNN-<short-slug>.md`.

---

## Index

| # | Title | Date | Status | Deciders |
|---|---|---|---|---|
| [0001](0001-adopt-agents-md-methodology-layer.md) | Adopt AGENTS.md methodology layer for AIW org | 2026-09-01 | Accepted | Ivan + Hermes session `20260901_134405_00cab4` |
| [0002](0002-instinct-integration-plan.md) | Instinct integration plan for AIW org (curator-evolver + homunculus pattern) | 2026-09-01 | Accepted | Ivan + Hermes session `20260901_134405_00cab4` |
| [0003](0003-handoff-boundary-integrity.md) | Adopt "Handoff Boundary Integrity" rule from Boundary Metadata Collapse research (arXiv 2026) | 2026-09-01 | Accepted | Ivan + Hermes session `20260901_134405_00cab4` |
| [0004](0004-tier-2-decisions-batch-2026-09-01.md) | Tier-2 Decision Batch (8 calls: taxonomy / naming / merge / R1 / Formspree / Start-Up Chile / open-source / public-repo) | 2026-09-01 | Accepted | Ivan + Hermes session `20260901_175348_46e9b0` |
| [0005](0005-libsodium-blob-disposition.md) | Disposition of libsodium secretbox blob `a1d64864-77f9-4e6a-8d6e-b4a90137189a` (quarantine / delete / commit-encrypted) | 2026-09-03 | **Proposed — awaiting Ivan** | Ivan (operator-gated) |

---

## Conventions

- **Filename:** `NNNN-<short-slug>.md` — number is monotonic, never reused even if ADR is deleted
- **Status lifecycle:** Proposed → Accepted → (Deprecated | Superseded)
- **One decision per ADR** — if you find yourself writing "and also...", split into two ADRs
- **Update existing ADR** if a decision is refined — don't supersede unless the decision itself changes
- **Search ADRs before deciding** — duplicates are bad; the index is the table of contents

---

## How to read this index

- New agents: scan the index first to understand why AIW is shaped the way it is
- Reviewers: cross-reference ADRs against PR descriptions
- Auditors: ADRs are the canonical answer to "why did we do X instead of Y?"

---

**Maintainer:** AIW org
**Last updated:** 2026-09-03
