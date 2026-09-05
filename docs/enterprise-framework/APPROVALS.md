# AIW Enterprise Framework — Approval Index

> **Purpose:** Single review surface for every framework gate. Link to gate files; do not duplicate checklists here.
> **Governance:** [GOVERNANCE.md](GOVERNANCE.md)
> **Rule:** Never invent approval evidence. Empty sign-off = `proposed`, not `approved`.

---

## DEMIURGE review gates

| ID | Subject | Gate file | Reviewers | Lifecycle | Blocks | `approved_commit` | Next action |
|----|---------|-----------|-----------|-----------|--------|-------------------|-------------|
| DEMIURGE-008 | Domain model + core schemas | [REVIEW-domain-model.md](../demiurge/REVIEW-domain-model.md) | Ivan, John | `proposed` | Sprint 1+ domain work | — | Complete checklist and sign-off; or supersede with new gate |
| DEMIURGE-015 | Sprint 1 architecture bundle | [REVIEW-sprint-1.md](../demiurge/REVIEW-sprint-1.md) | Ivan, John | `proposed` | Taxonomy/naming/router alignment claims | — | Complete checklist and sign-off; resolve taxonomy v1/v2 label |
| DEMIURGE-077 | Terminology library v1 | [TERMS.md](../terminology/TERMS.md) · [ticket](../../tickets/DEMIURGE-077-terminology-lib/plan.md) | AI + Ivan | `proposed` | DEMIURGE-078, 080 (vocabulary-dependent) | — | Ivan review of communication/priority terms; formal gate sign-off |

### DEMIURGE-008 artifacts (via gate file)

- [domain-model.md](../demiurge/domain-model.md)
- [schemas/agent-soul.md](../demiurge/schemas/agent-soul.md)
- [schemas/memory.md](../demiurge/schemas/memory.md)
- [schemas/role-department.md](../demiurge/schemas/role-department.md)
- [schemas/signal-channel.md](../demiurge/schemas/signal-channel.md)
- [schemas/router-quorum.md](../demiurge/schemas/router-quorum.md)
- [schemas/source-catalog.md](../demiurge/schemas/source-catalog.md)
- [schemas/feedback-kpi-cadence.md](../demiurge/schemas/feedback-kpi-cadence.md)

### DEMIURGE-015 artifacts (via gate file)

- [architecture.md](../demiurge/architecture.md)
- [department-taxonomy-v1.md](../demiurge/department-taxonomy-v1.md) (internal version: v2 — see file header)
- [naming-conventions.md](../demiurge/naming-conventions.md)
- [router-design.md](../demiurge/router-design.md)
- [feature-list.md](../demiurge/feature-list.md)

---

## Blocked human review gate

| ID | Subject | Gate file | Reviewers | Lifecycle | Blocks | `approved_commit` | Next action |
|----|---------|-----------|-----------|-----------|--------|-------------------|-------------|
| DEMIURGE-068 | LATAM + PY market research human validation | [latam-py-market-REVIEW-GATE.md](../../research/latam-py-market-REVIEW-GATE.md) | Ivan, John, Kiki | `proposed` | Promoting `community/*/language/` to `active`; ICP/market claims | — | Ivan/John complete checklist; no AI sign-off |

**Ticket:** [DEMIURGE-068/plan.md](../../tickets/DEMIURGE-068/plan.md)

---

## Department design decisions (DD)

Locked decisions (DD-01–DD-10) are recorded in [meetings/department-design/DECISIONS.md](../../meetings/department-design/DECISIONS.md). Open items require a dated session — not agent resolution.

| ID | Subject | Source | Reviewers | Lifecycle | Blocks | `approved_commit` | Next action |
|----|---------|--------|-----------|-----------|--------|-------------------|-------------|
| DD-O1 | Human product owner | DECISIONS.md | Ivan, Kiki | `draft` | PO naming, product list | — | Close in dated meeting |
| DD-O2 | PO: Athena expansion vs new agent | DECISIONS.md | Ivan | `draft` | Agent roster design | — | Close in dated meeting |
| DD-O3 | Written product list (in/out, audience) | DECISIONS.md | PO (once named) | `draft` | Sales promise boundaries | — | PO produces list after DD-O1 |
| DD-O4 | Freelancer content: Drive vs Hermes | DECISIONS.md | Kiki | `draft` | Content ops tooling | — | Close in dated meeting |
| DD-O5 | Reopen D1 funnel before Q1 2027? | DECISIONS.md | Ivan | `draft` | Funnel work | — | Default: no (per DD-08) |
| DD-O6 | Token-plan / credits for failing crons | DECISIONS.md | Kiki, Ivan | `draft` | Cron reliability | — | Close in dated meeting |
| DD-O7 | GitHub PAT rotation after `195e055` | DECISIONS.md | Ivan | `draft` | Credential hygiene | — | Human GitHub task; confirm in meeting |

---

## Review target commits

Gates that specify `review_target_commit` pin the snapshot under review:

| Gate | `review_target_commit` |
|------|------------------------|
| DEMIURGE-008 | `4b74290981e60b04fed044e420a93442bb0766ac` |
| DEMIURGE-015 | `4b74290981e60b04fed044e420a93442bb0766ac` |

Re-review required if artifacts change after this commit without a new approval.

---

**Last updated:** 2026-09-05 (ef-01-governance)
