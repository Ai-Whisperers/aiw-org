# AIW Enterprise Framework — Core Entity Metamodel

> **Status:** `proposed` — AIW-02 pending approval.
> **Scope:** Documentation design only — no loaders or validators in this ticket.
> **Extends:** [DEMIURGE domain model](../demiurge/domain-model.md) — does not replace it.
> **Governance:** [GOVERNANCE.md](GOVERNANCE.md) · [APPROVALS.md](APPROVALS.md) · [TERMS.md](../terminology/TERMS.md)

---

## Purpose

Define a reusable **entity envelope** and **relationship model** that separates:

- type definitions from catalog entries,
- organization-specific instances from runtime deployments,
- and governed relationships from ad-hoc field references.

Every DEMIURGE object (Agent, Role, Department, Signal, etc.) conforms to the common Entity envelope; type-specific schemas add only their own properties.

---

## Modeling layers

Four layers exist. Each layer answers a different question. **Counts at different layers must never be combined.**

| Layer | Question answered | Example |
|-------|-------------------|---------|
| `concept_definition` | What is this type of thing? | The abstract concept **Role** |
| `reference_model_item` | What governed catalog entry defines it? | AIW catalog entry **product-owner** |
| `organization_instance` | Who or what holds it in this org? | Agent **hera-marketing-lead** holds product-owner |
| `runtime_deployment` | How is it executed right now? | Hermes cron assignment `hera-mon-wed-fri-09:00-pyt` |

### Layer rule

When reporting metrics (role count, agent count, deployment count), always state the layer. Mixing layers produces invalid totals.

**Invalid:** "We have 3 roles and 5 agents, so 8 things."
**Valid:** "We have 12 `reference_model_item` roles in the catalog, 8 `organization_instance` role assignments, and 5 active `runtime_deployment` cadence slots."

### Worked example: Role → product-owner → Hera → cron assignment

```yaml
# Layer 1: concept_definition
concept: Role
definition: "A function or responsibility within a department."

# Layer 2: reference_model_item
Role:
  id: product-owner
  title: "Product Owner"
  department_id: product-discovery
  layer: reference_model_item

# Layer 3: organization_instance
Agent:
  id: hera-marketing-lead
  name: Hera
  layer: organization_instance
Relationship:
  id: rel-hera-holds-product-owner
  relationship_type: holds
  source_id: hera-marketing-lead
  target_id: product-owner
  cardinality: many_to_many
  layer: organization_instance

# Layer 4: runtime_deployment
Cadence:
  id: hera-product-owner-cadence
  agent_id: hera-marketing-lead
  schedule: "Mon/Wed/Fri 09:00 PYT"
  layer: runtime_deployment
Relationship:
  id: rel-hera-cadence-performs-product-owner
  relationship_type: performs
  source_id: hera-product-owner-cadence
  target_id: product-owner
  layer: runtime_deployment
```

---

## Common Entity envelope

All governed entities share this baseline. Type-specific schemas extend it; they do not redefine identity, lifecycle, or governance fields under different names.

```yaml
Entity:
  id: string                    # stable identifier; never encodes current role
  entity_type: string           # e.g. Agent, Role, Department, Signal
  schema_version: semver        # version of the type-specific schema
  name: string                  # human-readable label
  definition: string            # what this entity is
  purpose: string               # why this entity exists in the org
  lifecycle:
    status: draft | proposed | approved | active | suspended | superseded | retired
    valid_from: iso8601
    valid_until: iso8601 | null
  governance:
    owner_id: string            # who maintains the definition
    accountable_id: string      # who is answerable for outcomes
    approver_ids: string[]      # who may approve lifecycle transitions
    review_cadence: iso8601_duration
  standard_alignments: StandardAlignment[]
  evidence_refs: string[]       # links to ADRs, tickets, eval results
  tags: string[]
  created_at: iso8601
  updated_at: iso8601
```

### StandardAlignment (embedded)

```yaml
StandardAlignment:
  standard_id: string           # e.g. ISO-27001, RACI, ITIL
  clause_ref: string            # specific section or control
  alignment_status: aligned | partial | gap | not_applicable
  evidence_ref: string | null
```

### Lifecycle states

Aligned with [GOVERNANCE.md](GOVERNANCE.md). Entity `lifecycle.status` uses the same vocabulary as framework artifacts.

| State | Meaning for entities |
|-------|----------------------|
| `draft` | Defined locally; not ready for review |
| `proposed` | Ready for human review |
| `approved` | Signed off on a specific commit and schema version |
| `active` | In operational use |
| `suspended` | Temporarily inactive; identity preserved |
| `superseded` | Replaced by a newer version |
| `retired` | No longer in use |

---

## First-class relationships

Relationships are governed objects — not implicit array fields. When governance, evidence, or lifecycle must attach to a link between two entities, model it as a `Relationship`.

```yaml
Relationship:
  id: string
  relationship_type: string     # from governed vocabulary below
  source_id: string             # entity id at source end
  target_id: string             # entity id at target end
  direction: directed | undirected
  cardinality: one_to_one | one_to_many | many_to_one | many_to_many
  lifecycle_status: proposed | approved | active | retired
  authority_ref: string | null  # RACI authority or approval ticket
  evidence_refs: string[]
  valid_from: iso8601 | null
  valid_until: iso8601 | null
  metadata: object              # type-specific qualifiers (cadence, tier, etc.)
```

### Governed relationship vocabulary

| Type | Typical use | Example |
|------|-------------|---------|
| `contains` | Parent owns child structurally | Department contains Role |
| `belongs_to` | Child membership in parent | Role belongs_to Department |
| `holds` | Actor carries a role or responsibility | Agent holds Role |
| `assigned_to` | Work or duty allocated to actor | Task assigned_to Agent |
| `performs` | Runtime execution of a function | Cadence performs Role |
| `owns` | Accountability for an outcome | Agent owns KPI |
| `accountable_for` | RACI accountable party | Human accountable_for Role |
| `consulted_by` | RACI consulted party | Agent consulted_by on Decision |
| `informs` | RACI informed party | Department informs Board |
| `produces` | Creates an artifact | Agent produces Artifact |
| `consumes` | Reads or uses an artifact | Agent consumes Source |
| `controls` | Enforces a policy or gate | Router controls Signal delivery |
| `checks` | Validates against criteria | Eval gate checks Soul change |
| `challenges` | Adversarial review | Watchdog challenges Deployment |
| `approves` | Grants lifecycle transition | Human approves Role activation |
| `escalates_to` | Routes on failure or SLA breach | Signal escalates_to Lead Agent |
| `implements` | Realizes a design artifact | Agent implements Technical Feature |
| `realizes` | Connects instance to definition | organization_instance realizes reference_model_item |
| `supports` | Assists without holding accountability | Agent supports human Role holder |
| `depends_on` | Ordering or availability constraint | Department depends_on Source Catalog |
| `supersedes` | Replaces a prior version | Role v2 supersedes Role v1 |

**Rule:** Do not turn every relationship into an entity. Use the Relationship envelope when governance, evidence, lifecycle, or cardinality must be tracked independently of the endpoints.

---

## DEMIURGE alignment

The metamodel extends the existing DEMIURGE object graph. Mapping tables in schema files show how current fields map to the Entity envelope and Relationship types.

### Key many-to-many relationships (explicit)

| Source | Relationship | Target | Cardinality |
|--------|--------------|--------|-------------|
| Agent | `holds` | Role | many_to_many |
| Agent | `belongs_to` | Department | many_to_many |
| Role | `belongs_to` | Department | many_to_one |
| Agent | `performs` | Role (via Cadence) | many_to_many |

Inline array fields (`Agent.roles[]`, `Role.agent_assignments[]`, `Department.agents[]`) remain as convenience denormalizations. The Relationship records are the governed source of truth when lifecycle or evidence must attach.

### Role changes without identity changes

Agent `id` is stable across role changes. When an agent moves from one role to another:

1. Retire the `holds` Relationship (`lifecycle_status: retired`, `valid_until` set).
2. Create a new `holds` Relationship to the new Role.
3. Update denormalized arrays (`roles[]`, `agent_assignments[]`) for query convenience.
4. Do **not** rename the Agent `id` or Soul `id`.

---

## Examples

### 1. Agent holding roles from Engineering and Research

```yaml
Agent:
  id: thoth-research-analyst
  name: Thoth
  entity_type: Agent
  layer: organization_instance

Relationships:
  - id: rel-thoth-holds-eng-reviewer
    relationship_type: holds
    source_id: thoth-research-analyst
    target_id: engineering-code-reviewer
    cardinality: many_to_many
    lifecycle_status: active

  - id: rel-thoth-holds-research-curator
    relationship_type: holds
    source_id: thoth-research-analyst
    target_id: research-literature-curator
    cardinality: many_to_many
    lifecycle_status: active
```

One agent, two roles, two departments. Count at `organization_instance` layer: 2 role assignments, 1 agent.

### 2. Product Owner held by a human and supported by an agent

```yaml
# Human holds accountability
Relationship:
  id: rel-ivan-accountable-product-owner
  relationship_type: accountable_for
  source_id: human:ivan
  target_id: product-owner
  lifecycle_status: active

# Agent supports without replacing human accountability
Relationship:
  id: rel-hera-supports-product-owner
  relationship_type: supports
  source_id: hera-marketing-lead
  target_id: product-owner
  lifecycle_status: active
  metadata:
    scope: "backlog grooming, stakeholder summaries"
```

### 3. Two agents sharing reviewer role at different cadences

```yaml
Role:
  id: engineering-code-reviewer
  layer: reference_model_item

Relationships:
  - id: rel-thoth-holds-reviewer
    relationship_type: holds
    source_id: thoth-research-analyst
    target_id: engineering-code-reviewer
    cardinality: many_to_many

  - id: rel-atlas-holds-reviewer
    relationship_type: holds
    source_id: atlas-engineering-lead
    target_id: engineering-code-reviewer
    cardinality: many_to_many

# Runtime deployments differ
Cadence:
  id: thoth-reviewer-cadence
  schedule: "Mon/Fri 10:00 PYT"
Relationship:
  id: rel-thoth-cadence-performs-reviewer
  relationship_type: performs
  source_id: thoth-reviewer-cadence
  target_id: engineering-code-reviewer

Cadence:
  id: atlas-reviewer-cadence
  schedule: "Tue/Thu 14:00 PYT"
Relationship:
  id: rel-atlas-cadence-performs-reviewer
  relationship_type: performs
  source_id: atlas-reviewer-cadence
  target_id: engineering-code-reviewer
```

Same role (`reference_model_item` count: 1). Two agents (`organization_instance` count: 2 assignments). Two cadences (`runtime_deployment` count: 2).

### 4. Anti-example: equating agent, role, and department (forbidden)

```yaml
# FORBIDDEN — do not model this way
Agent:
  id: marketing-department-head-of-content   # encodes department + role in identity
  department: marketing                      # collapses dept into agent
  role: head-of-content                      # collapses role into agent
  # No Relationship records; no layer separation
```

**Why forbidden:**

- Identity changes when role or department changes — violates stable `id` rule.
- Cannot count roles, agents, or departments at any layer.
- Cannot attach governance or evidence to assignments independently.
- Prevents many-to-many (one agent across departments, multiple agents per role).

**Correct approach:** Separate Agent entity, Role `reference_model_item`, Department entity, and governed `holds` / `belongs_to` Relationships at `organization_instance` layer.

---

## Open questions

Documented as stubs — not blockers for this ticket.

### Soul: Entity or sub-component?

**Current position (proposed):** Soul is a **versioned sub-component** of Agent, not a standalone Entity at `organization_instance` layer. Soul has its own `version` semver and revision process, but shares Agent `id`. Rationale: Soul is always 1:1 with Agent; splitting would duplicate identity governance.

**Alternative:** Soul as separate Entity with `realizes` Relationship to Agent. Revisit if Soul must be shared across agents or audited independently.

### Runtime cron jobs: Deployment, Cadence, or both?

**Current position (proposed):** Hermes cron registration maps to **Cadence** at `runtime_deployment` layer. A Cadence `performs` one or more Roles. "Deployment" is used informally for the active cron slot, not as a separate entity type in v1.

**Alternative:** Introduce `Deployment` as a distinct Entity wrapping Cadence + environment binding. Revisit when multi-environment runtime (staging vs production) needs separate governance.

---

## Related documents

| Document | Relationship |
|----------|--------------|
| [domain-model.md](../demiurge/domain-model.md) | DEMIURGE object graph this metamodel extends |
| [agent-soul.md](../demiurge/schemas/agent-soul.md) | Agent/Soul field mapping to Entity envelope |
| [role-department.md](../demiurge/schemas/role-department.md) | Role/Department field mapping to Entity envelope |
| [TERMS.md](../terminology/TERMS.md) | Authoritative term definitions including relationship types |
| [GOVERNANCE.md](GOVERNANCE.md) | Lifecycle states and approval binding |
