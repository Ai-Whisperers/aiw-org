# AIW Enterprise Framework — Standards Registry

> **Status:** `proposed` — AIW-03 pending approval.
> **Scope:** Documentation design only — no conformance test automation in this ticket.
> **Governance:** [GOVERNANCE.md](GOVERNANCE.md) · [APPROVALS.md](APPROVALS.md) · [METAMODEL.md](METAMODEL.md)

---

## Purpose

Maintain a **controlled registry** of external standards, frameworks, and reference models that AIW follows, profiles, adapts, or intentionally rejects.

Standards remain **external references**. This repository stores:

- identifiers and versions,
- official source URLs,
- scope of use within AIW,
- conformance level,
- documented deviations,
- owners and review dates.

**Do not copy** copyrighted or licensed standard text (ISO, APQC, TOGAF, ArchiMate body content, etc.) into this repository. Store mappings and AIW-specific profiles only.

---

## StandardAlignment schema

Defined in [METAMODEL.md](METAMODEL.md#standardalignment-embedded). Embedded on Entity envelopes via `standard_alignments[]` and as standalone records in the catalog.

| Field | Role |
|-------|------|
| `standard_id` | Stable catalog key |
| `title` | Human-readable standard name |
| `issuing_body` | Maintainer or standards body |
| `version` | Pinned or cited edition |
| `source_url` | Official issuer URL |
| `scope` | Clauses, controls, or AIW profile areas in use |
| `conformance` | Posture toward the standard (see below) |
| `mapped_entities` | Entity types or schema ids that use this standard |
| `deviation_reason` | Required when `conformance` is `adapted` or `profiled` with material gaps |
| `decision_ref` | ADR, ticket, or approval record authorizing use |
| `owner_id` | Maintainer accountable for alignment accuracy |
| `reviewed_at` | Last human review of version and posture |

### Conformance levels

| Level | Meaning | External claim allowed |
|-------|---------|------------------------|
| `exact` | Implements the cited edition without material deviation | Yes — only with documented conformance evidence |
| `profiled` | Subset or extension of the standard with documented profile | Partial — describe profile, not full standard compliance |
| `adapted` | Material deviation for AIW context; rationale required | No — describe adaptation, not compliance |
| `inspired` | Conceptual alignment only; not a conformance claim | No |
| `not_applicable` | Referenced for context; not adopted | No |

**Rule:** Do not claim ITIL, ISO, APQC, ArchiMate, or similar **conformance** without a conformance test and approver sign-off. `inspired` and `adapted` are not compliance claims.

---

## Catalog

Authoritative entries: [standards/catalog.yaml](standards/catalog.yaml).

Each entry must include `issuing_body`, `version`, `source_url`, `conformance`, `owner_id`, and `scope`.

---

## Deviation governance

AIW may deviate from an external standard only when at least one documented reason applies:

1. **AI-agent execution** — human-oriented process or artifact shape does not fit agent runtime.
2. **Disproportionate complexity** — full adoption cost exceeds benefit at current scale.
3. **Licensing or usage constraints** — reproduction or implementation restricted.
4. **Inapplicable scale** — standard targets enterprise scale or domain AIW does not operate in.

### Requirements for material deviations

When `conformance` is `adapted` or `profiled` with material gaps:

1. Set `deviation_reason` to a specific rationale (not generic).
2. Assign `owner_id` accountable for the deviation.
3. Record `decision_ref` pointing to an ADR in `docs/adr/` or an approved ticket.
4. Set `reviewed_at` on each review cycle.

**"AIW-specific" alone is not a sufficient deviation reason.** State what constraint the standard imposes and why the chosen deviation is necessary.

### Periodic review

When a referenced standard publishes a new edition:

1. Owner reviews whether `version`, `scope`, and `conformance` remain accurate.
2. Update `reviewed_at` and catalog entry; bump `decision_ref` or ADR if posture changes.
3. Do not silently drift — unresolved version pins are governance debt.

---

## Licensing and source quality

1. Use **official issuer URLs** in `source_url`.
2. Quote no more than necessary for identification.
3. Store **AIW mappings and profiles**, not protected standard body content.
4. Record access or review date via `reviewed_at`; add license notes in catalog `scope` or ADR when usage is restricted (e.g. APQC, ISO store terms).

### Verification commands

```bash
git diff --check
git grep -n "conformance:" -- docs/enterprise-framework/standards/catalog.yaml
git grep -n "iso.org\|omg.org\|w3.org\|apqc.org\|opengroup.org" -- docs/enterprise-framework
```

---

## Related documents

| Document | Relationship |
|----------|--------------|
| [METAMODEL.md](METAMODEL.md) | Entity envelope and embedded `StandardAlignment` |
| [standards/catalog.yaml](standards/catalog.yaml) | Governed catalog entries |
| [document.md](../demiurge/schemas/document.md) | Document envelope standard mappings |
| [source-catalog.md](../demiurge/schemas/source-catalog.md) | Source type `standard` references |
| [TERMS.md](../terminology/TERMS.md) | `standard_alignment`, `conformance`, `deviation` definitions |
