# AIW Enterprise Framework — Governance

> **Purpose:** Define lifecycle states, authority, and change rules for framework artifacts (models, standards, terminology, review gates).
> **Scope:** Documentation and schema governance only — no runtime approval queues.
> **Canonical index:** [APPROVALS.md](APPROVALS.md)

---

## Lifecycle states

Every governed artifact carries a `lifecycle` value. States are mutually exclusive at a point in time.

| State | Meaning |
|-------|---------|
| `draft` | Work in progress; not ready for human review. |
| `proposed` | Ready for human review; checklist or gate file exists but sign-off is incomplete. |
| `approved` | Human authority has signed off on a **specific commit** and **schema version**. |
| `implemented` | Approved design is reflected in code, config, or operational artifacts. Requires evidence links. |
| `enforced` | Automated checks or runtime behavior depend on the approved artifact. Requires evidence links. |
| `superseded` | Replaced by a newer approved version; retained for history. |
| `retired` | No longer in use; not a source of truth. |

**Critical distinctions:**

- `approved` ≠ `implemented` — approval is a human gate on a document snapshot.
- `implemented` ≠ `enforced` — implementation may exist without automated or runtime dependency.
- Agents must not describe an artifact as `locked`, `complete`, or `approved` while its review gate remains open.

---

## Approval binding

Approval applies to:

1. **`approved_commit`** — the exact git commit hash reviewers examined.
2. **`schema_version`** — semantic version of the schema or document set under review.

If content changes after approval without a new gate, the artifact reverts to `proposed` until re-approved.

---

## Allowed transitions

| From | To | Authorized by | Requirement |
|------|-----|---------------|-------------|
| — | `draft` | Author (human or agent) | Initial creation |
| `draft` | `proposed` | Author | Review gate file created or updated |
| `proposed` | `approved` | Named reviewers in gate | Sign-off row completed; `approved_commit` set |
| `approved` | `implemented` | Implementer + evidence | Link to PR, deploy, or config showing adoption |
| `implemented` | `enforced` | Platform owner | Link to validator, cron, or runtime check |
| `approved` | `superseded` | Reviewers of successor gate | `supersedes` / `superseded_by` link |
| any | `retired` | Human authority (Ivan, John, or delegated owner) | Dated note in gate or ADR |

Retroactive approval of old gates requires an explicit human decision documented in the gate sign-off — agents must not infer it.

---

## Status block (YAML)

Attach this block (or equivalent front-matter) to governed artifacts:

```yaml
framework_status:
  lifecycle: proposed
  schema_version: 0.1.0
  approved_commit: null
  approvers: [human:ivan, human:john]
  evidence_refs: []
  supersedes: null
  reviewed_at: null
  next_review_at: null
```

| Field | Description |
|-------|-------------|
| `lifecycle` | One of the states above |
| `schema_version` | Semver of the governed schema or document set |
| `approved_commit` | Git SHA at approval; `null` until signed |
| `approvers` | Roles or humans who may sign the gate |
| `evidence_refs` | Paths or URLs proving `implemented` / `enforced` |
| `supersedes` | Prior gate or schema id this artifact replaces |
| `reviewed_at` | ISO date of last human review |
| `next_review_at` | Scheduled re-review; optional |

---

## Framework change rules

### 1. Terminology-first

New or changed domain terms are added to [`docs/terminology/TERMS.md`](../terminology/TERMS.md) **before** use in schemas, prompts, rules, or tickets. No local redefinitions.

### 2. ADR for breaking model changes

An ADR in [`docs/adr/`](../adr/) is required for breaking changes to:

- Core entities (Agent, Department, Signal, Soul, etc.)
- Relationships in the domain model
- Closed enumerations used by runtime routing or validation

Non-breaking additions (new optional fields, new terms) follow terminology-first only.

### 3. Migration notes

When an **approved** schema version changes, include migration notes in the gate file or ADR: what changed, what consumers must update, and whether old artifacts are `superseded` or `retired`.

### 4. Human authority changes

Changes to who may approve, sign, or enforce framework artifacts require a **dated review gate** (new or updated row in [APPROVALS.md](APPROVALS.md)) — not a silent edit.

### 5. AI-generated approval is not evidence

Summaries, checklists marked complete, or "approved" language produced by an AI agent are **not** evidence of human approval. Only completed sign-off rows, named dates, and `approved_commit` values count.

---

## Related documents

| Document | Role |
|----------|------|
| [APPROVALS.md](APPROVALS.md) | Canonical index of all review gates |
| [TERMS.md](../terminology/TERMS.md) | Authoritative vocabulary |
| [docs/adr/](../adr/) | Architectural decisions |
| [docs/demiurge/](../demiurge/) | DEMIURGE domain model and schemas |

**Last updated:** 2026-09-05 (ef-01-governance)
