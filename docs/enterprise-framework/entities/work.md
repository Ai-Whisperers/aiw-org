# Work and Behavior Entities

> **Domain:** 3 — Work and behavior
> **Status:** `proposed`
> **Terms:** [capability](../../terminology/TERMS.md), [process](../../terminology/TERMS.md)

Entities describing what the organization can do, how work flows, and how outcomes are produced.

---

## Core distinctions

| Entity | One-line definition | Question answered |
|--------|---------------------|-------------------|
| **Capability** | Organizational **ability** to achieve an outcome | What can we do? |
| **Process** | Repeatable work producing a defined **outcome** | How do we consistently deliver? |
| **Workflow** | Ordered **coordination** of activities for a process or case | How are steps sequenced for this instance? |
| **Procedure** | **Prescribed method** — step-by-step instructions | What exact steps must be followed? |
| **Task** | One **owned unit** of work with a clear completion criterion | Who does what by when? |

**Rule:** Capability ≠ Process ≠ Workflow. A capability may be realized by multiple processes; a process may be executed via many workflow instances; a procedure documents how within a process.

---

## Entity definitions

### Capability

Organizational ability to achieve an outcome. Stable over time; realized by processes, roles, and systems.

```yaml
Capability:
  entity_type: Capability
  outcome_description: string
  maturity_level: initial | developing | defined | managed | optimizing
  process_ids: string[]
  owner_role_id: string
```

### ValueStream

End-to-end flow of activities delivering value to a customer — from demand to outcome. Spans multiple processes and capabilities.

**Distinct from:** Process (bounded repeatable unit within a stream).

```yaml
ValueStream:
  entity_type: ValueStream
  customer_facing: boolean
  stage_ids: string[]
  capability_ids: string[]
```

### Process

Repeatable work that transforms inputs into outputs and produces a defined outcome. Has trigger, activities, roles, and measures.

```yaml
Process:
  entity_type: Process
  trigger: string
  inputs: string[]
  outputs: string[]
  outcome: string
  subprocess_ids: string[]
  capability_ids: string[]
  owner_role_id: string
```

### Subprocess

A bounded part of a parent process with its own inputs, outputs, and owner. Decomposition unit for complex processes.

```yaml
Subprocess:
  entity_type: Subprocess
  parent_process_id: string
  inputs: string[]
  outputs: string[]
```

### Activity

A single unit of work within a process or subprocess — atomic step, not independently owned across processes.

**Distinct from:** Task (owned work item with assignee and due date).

```yaml
Activity:
  entity_type: Activity
  process_id: string
  sequence_order: integer
  role_id: string | null
  estimated_duration: iso8601_duration | null
```

### Workflow

Ordered coordination of activities for a process or case instance. May be automated (agent routing) or manual.

```yaml
Workflow:
  entity_type: Workflow
  process_id: string
  activity_sequence: string[]
  automation_level: manual | assisted | automated
  trigger_event: string | null
```

### Procedure

Prescribed method — documented step-by-step instructions operators must follow. Often compliance-driven.

**Distinct from:** Process (outcome-oriented); Workflow (coordination pattern).

```yaml
Procedure:
  entity_type: Procedure
  process_id: string
  steps: string[]
  compliance_refs: string[]
  review_cadence: iso8601_duration
```

### Task

One owned unit of work with a clear completion criterion, assignee, and optional due date.

**Note:** DEMIURGE defines `task` as an [Artifact type](../../demiurge/schemas/artifacts.md) for operational work items. This entity type is the **work-management** abstraction; artifact tasks are runtime instances conforming to both schemas where applicable.

```yaml
Task:
  entity_type: Task
  assignee_id: string
  process_id: string | null
  due_at: iso8601 | null
  completion_criteria: string
  status: open | in_progress | blocked | done | cancelled
```

### Decision

A recorded choice with rationale, alternatives considered, and authority. May gate process progression.

**Note:** DEMIURGE `decision` artifact type is the operational instance. This entity type is the governed work concept.

```yaml
Decision:
  entity_type: Decision
  decision_maker_id: string
  rationale: string
  alternatives_considered: string[]
  evidence_refs: string[]
```

### Approval

A formal authorization granting permission to proceed — lifecycle transition, spend, release, or policy exception.

**Distinct from:** Decision (choice among options); Approval is binary authorize/deny.

```yaml
Approval:
  entity_type: Approval
  approver_id: string
  subject_id: string
  subject_type: string
  outcome: approved | denied | deferred
  authority_ref: string | null
```

### Event

Something that happened at a point in time — may trigger processes, workflows, or signals. Work-domain events are business occurrences; see [information-data.md](information-data.md) for data-domain event overlap.

```yaml
Event:
  entity_type: Event
  event_type: string
  occurred_at: iso8601
  source_id: string | null
  payload_ref: string | null
  triggers_process_ids: string[]
```

---

## Relationships (examples)

| Source | Type | Target | Meaning |
|--------|------|--------|---------|
| Capability | `realizes` | ValueStream stage | Capability enables stream stage |
| Process | `implements` | Capability | Process exercises capability |
| Workflow | `depends_on` | Process | Workflow executes process pattern |
| Task | `assigned_to` | Agent | Work allocated to actor |
| Approval | `approves` | Process transition | Gate before proceeding |
| Event | `triggers` | Workflow | Event starts coordination |

---

## AIW instances (v0.1)

| Entity | Instance status | Notes |
|--------|-----------------|-------|
| Task | yes | Artifact type in operational memory |
| Decision | yes | Artifact type in decisions/ |
| Workflow | partial | Agent routing, signal flows implicit |
| Procedure | partial | AGENTS.md, rules, prompts as informal procedures |
| Process, Capability, ValueStream | partial | Documented informally; not governed catalog |

---

## Related documents

- [value-market.md](value-market.md) — Product and Service
- [information-data.md](information-data.md) — Artifact and Signal mapping
- [METAMODEL.md](../METAMODEL.md) — Relationship vocabulary
