# DEMIURGE Domain Model

> **Status:** `proposed` — DEMIURGE-008 pending approval ([REVIEW-domain-model.md](REVIEW-domain-model.md)).
> Every agent, department, and signal is an instance of these objects.
> **Metamodel:** Common entity envelope and relationship model — [METAMODEL.md](../enterprise-framework/METAMODEL.md).

## Object graph

```mermaid
erDiagram
    Agent ||--|| Soul : has
    Agent ||--|| Memory : has
    Agent }o--o{ Role : holds
    Agent }o--o{ Skill : uses
    Agent }o--o{ Tool : uses
    Agent ||--o| Cadence : runs_on
    Role }o--|| Department : belongs_to
    Department }o--o{ Source : grounded_in
    Department }o--o{ KPI : measures
    Signal }o--|| Agent : sent_by
    Signal }o--o{ Agent : recipients
    Signal }o--o| Quorum : may_require
    Channel }o--o{ Agent : members
    Channel ||--o| Router : managed_by
    Router }o--o{ Department : routes_for
    FeedbackLoop }o--|| KPI : triggered_by
    SourceCatalog }o--o{ Source : contains
    Agent }o--o{ Artifact : creates
    MessageBoard }o--o{ Artifact : contains
    CommunityMemory }o--o{ CommunityMemoryEntry : contains
    Agent }o--o{ CommunityMemory : reads_writes
    Channel ||--o| MessageBoard : surfaces
    Artifact }o--o| Signal : referenced_by
```

## Governed relationships (explicit)

The ER diagram above shows cardinality. The following table names the governed `relationship_type` from [METAMODEL.md](../enterprise-framework/METAMODEL.md). Inline schema fields are denormalized convenience; Relationship records are source of truth when lifecycle or evidence must attach.

| Source | relationship_type | Target | Cardinality | Schema reference |
|--------|-------------------|--------|-------------|------------------|
| Agent | `has` | Soul | one_to_one | [agent-soul.md](schemas/agent-soul.md) |
| Agent | `has` | Memory | one_to_one | [memory.md](schemas/memory.md) |
| Agent | `holds` | Role | many_to_many | `Agent.roles[]` ↔ `Role.agent_assignments[]` |
| Agent | `belongs_to` | Department | many_to_many | `Agent.departments[]` ↔ `Department.agents[]` |
| Agent | `uses` | Skill | many_to_many | `Agent.skills[]` |
| Agent | `uses` | Tool | many_to_many | `Agent.tools[]` |
| Agent | `runs_on` | Cadence | one_to_one | `Agent.cadence` |
| Cadence | `performs` | Role | many_to_many | runtime_deployment layer |
| Role | `belongs_to` | Department | many_to_one | `Role.department_id` |
| Department | `contains` | Role | one_to_many | `Department.roles[]` |
| Department | `grounded_in` | Source | many_to_many | Source catalog |
| Department | `measures` | KPI | many_to_many | Dept KPIs |
| Agent | `creates` | Artifact | many_to_many | Episodic memory |
| Signal | `sent_by` | Agent | many_to_one | Signal sender |
| Signal | `assigned_to` | Agent | many_to_many | Signal recipients |

### Agent ↔ Role many-to-many

- Multiple agents may hold the same role (e.g. two code reviewers).
- One agent may hold roles in multiple departments (e.g. Engineering reviewer + Research curator).
- Agent `id` does not encode role; role changes retire/create `holds` Relationships without renaming the agent.

### Agent ↔ Department many-to-many

- One agent may serve multiple departments via `belongs_to` Relationships.
- `Department.agents[]` and `Agent.departments[]` are denormalized mirrors.

## Hermes alignment

| DEMIURGE concept | Hermes / runtime concept |
|----------------|--------------------------|
| Soul | Immutable agent identity kernel (PROMPT.md + hard_stops YAML) |
| Memory Layer 2 Episodic | Git repo per agent: notes, findings, lessons, boards/ |
| Memory Layer 2.5 Community | Shared git repos: `aiw-community-*` — practices, norms, Echo signals |
| Memory Layer 3 Operational | SQLite: tasks, todos, escalations, idempotency |
| Cadence | Hermes cron job registration |
| Signal | Inter-agent message routed by Router |
| Router | Dedicated Hermes instance or cron workflow |

## Design principles

1. **Soul is not memory** — identity is versioned separately from operational state.
2. **Git-backed memory is operational** — episodic history, not the soul.
3. **Agents have names** — memorable names (e.g. Hera, Thoth) plus role IDs.
4. **Roles are fungible** — multiple agents per role; one agent across departments.
5. **Signals are typed** — direct, group, dept_broadcast, cross_dept.
6. **Router enforces delivery** — right agents, on time, quorum met.
7. **Sources ground departments** — literature + community, quality-rated 1–5.
8. **Feedback loops are first-class** — monitor → source → soul → agent.
9. **Artifacts are first-class** — notes, tasks, todos, boards, thoughts, findings, learnings; agents read/write them across memory layers.

## Schema files

See `schemas/` for field-level definitions and JSON Schema fragments.

| Schema | Objects |
|--------|---------|
| [artifacts.md](schemas/artifacts.md) | Artifact, MessageBoard, Task, Todo, Thought, Finding, Learning |
