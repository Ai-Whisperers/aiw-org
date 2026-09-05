# Schema: Role + Department

> DEMIURGE-003
> **Metamodel:** Field mappings to the common Entity envelope — [METAMODEL.md](../../enterprise-framework/METAMODEL.md).

## Role

A function/responsibility within a department. Multiple agents can share a role; one agent can hold multiple roles.

```yaml
Role:
  id: string                # e.g. marketing-head-of-content
  title: string             # "Head of Content"
  department_id: string
  tier: enum                # lead | senior | mid | junior | deferred
  responsibilities: string[]
  kpis: string[]            # KPI ids
  source_basis: string[]    # Source ids grounding this role
  skills_required: string[]
  tools_required: string[]
  cadence_hint: string      # e.g. "Mon/Wed/Fri 09:00 PYT"
  status: enum              # active | skeleton | deferred
  agent_assignments: string[]  # agent ids currently holding this role
```

### Entity envelope mapping (Role)

| Entity field | Role field | Notes |
|--------------|------------|-------|
| `id` | `id` | Catalog entry at `reference_model_item` layer |
| `entity_type` | `"Role"` | Fixed type discriminator |
| `name` | `title` | Human-readable role title |
| `definition` | `responsibilities[]` | Concatenated or primary responsibility |
| `purpose` | — | Derived from department mission + responsibilities |
| `lifecycle.status` | `status` | Maps: active, skeleton→draft, deferred |
| `governance.accountable_id` | — | Typically dept head or human owner |
| `evidence_refs` | `source_basis[]` | Source ids grounding this role |

### Relationship mapping (Role)

| Relationship | Direction | Target | Cardinality | Denormalized field |
|--------------|-----------|--------|-------------|-------------------|
| `belongs_to` | Role → Department | `department_id` | many_to_one | `department_id` |
| `holds` (inverse) | Agent → Role | Agent id | many_to_many | `agent_assignments[]` |

**Agent↔Role many-to-many:** Multiple agents may hold the same role; one agent may hold multiple roles. Governed `holds` Relationships are source of truth; `agent_assignments[]` and `Agent.roles[]` are denormalized convenience fields.

## Department

A functional area of the company. Mimics a real large-org department.

```yaml
Department:
  id: string                # kebab-case, e.g. marketing
  name: string              # "Marketing"
  tier: int                 # 1 core | 2 cross-cutting | 3 deferred | 4 enterprise
  parent_dept_id: string    # optional, for sub-departments
  mission: string           # one sentence
  head_human: string        # ivan | kiki | agent:<id>
  roles: string[]           # Role ids
  agents: string[]          # Agent ids assigned to this dept
  source_catalog_id: string # SourceCatalog id
  in_signals: SignalType[]  # what this dept receives
  out_signals: SignalType[] # what this dept emits
  kpis: string[]
  channels: string[]        # Channel ids
  router_id: string         # Router agent managing this dept's signals
  status: enum              # skeleton | active | deferred
  promotion_trigger: string # for Tier 3, when to activate fully
```

### Entity envelope mapping (Department)

| Entity field | Department field | Notes |
|--------------|------------------|-------|
| `id` | `id` | Org unit at `organization_instance` layer |
| `entity_type` | `"Department"` | Fixed type discriminator |
| `name` | `name` | Department display name |
| `definition` | `mission` | One-sentence mission statement |
| `purpose` | `mission` | Same as definition for departments |
| `lifecycle.status` | `status` | Maps: skeleton→draft, active, deferred |
| `governance.accountable_id` | `head_human` | ivan, kiki, or agent:id |
| `governance.owner_id` | `head_human` | Dept lead accountability |

### Relationship mapping (Department)

| Relationship | Direction | Target | Cardinality | Denormalized field |
|--------------|-----------|--------|-------------|-------------------|
| `contains` | Department → Role | Role id | one_to_many | `roles[]` |
| `belongs_to` (inverse) | Role → Department | Department id | many_to_one | Role.`department_id` |
| `belongs_to` | Agent → Department | Agent id | many_to_many | `agents[]` |

**Agent↔Department many-to-many:** One agent may serve multiple departments; one department has multiple agents. Governed `belongs_to` Relationships are source of truth; `agents[]` and `Agent.departments[]` are denormalized.

## SignalType (department-level contract)

Defines what a department emits or expects, not a single message instance.

```yaml
SignalType:
  id: string                # e.g. marketing-content-ready
  name: string
  direction: enum           # in | out
  payload_schema: string    # JSON Schema ref or inline
  default_priority: enum    # normal | urgent | critical
  default_quorum: string    # Quorum id or null
  sla_reaction: duration    # e.g. PT2H
  routing_tags: string[]
```

## Tier definitions

| Tier | Meaning | Example |
|------|---------|---------|
| 1 | Core canonical dept | Sales, Marketing, Engineering |
| 2 | Cross-cutting | AI Ops, RevOps, Compliance |
| 3 | Deferred until trigger | Customer Success (5+ clients) |
| 4 | Enterprise scale | Investor Relations at scale |

## Skeleton department

A department with `status: skeleton` has:

- Mission + role inventory defined
- Source catalog stub
- No active agents yet
- Ready for focused build session

Priority build order: Marketing → Product Discovery → Sales (revenue path).

## JSON example (Department)

```json
{
  "id": "marketing",
  "name": "Marketing",
  "tier": 1,
  "mission": "Generate demand, nurture audience, feed Sales with qualified attention.",
  "head_human": "agent:hera-marketing-lead",
  "roles": ["marketing-lead", "marketing-content-producer", "marketing-community-monitor"],
  "status": "active",
  "in_signals": ["sales-pipeline-feedback", "product-discovery-insight"],
  "out_signals": ["marketing-content-ready", "marketing-campaign-brief"]
}
```
