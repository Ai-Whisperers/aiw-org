# RoleAssignment Entity

> **Domain:** 1 — Organization (assignment instance)
> **Layer:** `organization_instance`
> **Status:** `proposed` — AIW-05 pending approval.
> **Metamodel:** Conforms to the [Entity envelope](../METAMODEL.md).
> **Terms:** [role_assignment](../../terminology/TERMS.md), [role](../../terminology/TERMS.md), [agent](../../terminology/TERMS.md)

A **RoleAssignment** is a time-bound, governed record linking an actor (human, agent, or team) to a Role. It is the source of truth for who holds what authority, in which department context, and for how long.

**Rule:** `Agent.roles[]` and `Role.agent_assignments[]` are convenience denormalizations. When scope, authority, effective dates, conflict rules, or human accountability must be tracked, use RoleAssignment records.

---

## Schema

```yaml
RoleAssignment:
  id: string                    # e.g. ra-devin-holds-engineering-roster
  role_id: string               # reference_model_item Role id
  actor_id: string              # human:<id> | agent id | team:<id>
  actor_type: human | agent | team
  department_context_ids: string[]  # depts where this assignment applies
  scope: string                 # free-text or structured scope qualifier
  authority_level: advise | propose | decide | approve | execute | audit
  accountable_human_id: string  # REQUIRED — human answerable for outcomes
  effective_from: iso8601
  effective_until: iso8601 | null
  status: proposed | active | suspended | retired
  conflict_rules: string[]      # ids or inline rules for SoD collisions
```

### Field semantics

| Field | Required | Notes |
|-------|----------|-------|
| `role_id` | yes | Points to a `reference_model_item` Role catalog entry |
| `actor_id` | yes | Stable actor identifier; does not change when role scope narrows |
| `actor_type` | yes | Distinguishes human accountability chain from agent execution |
| `department_context_ids` | yes (may be empty) | Empty = org-wide; non-empty = cross-dept or scoped assignment |
| `scope` | yes | Describes what subset of the role this assignment covers |
| `authority_level` | yes | Highest authority this assignment grants in the given scope |
| `accountable_human_id` | yes | Human who remains answerable even when `actor_type: agent` |
| `effective_from` / `effective_until` | yes / optional | Assignment is invalid outside this window |
| `status` | yes | Lifecycle independent of Role catalog status |
| `conflict_rules` | optional | References SoD rules in [CONTROLS.md](../CONTROLS.md) |

### Authority levels

| Level | Meaning |
|-------|---------|
| `advise` | May recommend; cannot commit org resources |
| `propose` | May draft decisions or artifacts for approval |
| `decide` | May commit within delegated scope |
| `approve` | May grant lifecycle transitions or external actions |
| `execute` | May run operational work (default for most agents) |
| `audit` | May review evidence; must not also execute the same case when SoD requires separation |

---

## Entity envelope mapping

| Entity field | RoleAssignment field | Notes |
|--------------|----------------------|-------|
| `id` | `id` | Stable assignment record id |
| `entity_type` | `"RoleAssignment"` | Fixed type discriminator |
| `schema_version` | — | Schema file version when formalized |
| `name` | derived | e.g. `{actor_id} → {role_id}` |
| `definition` | `scope` | What this assignment covers |
| `purpose` | — | Why this actor holds this role in this context |
| `lifecycle.status` | `status` | proposed → active → suspended/retired |
| `lifecycle.valid_from` | `effective_from` | Assignment start |
| `lifecycle.valid_until` | `effective_until` | Assignment end; null = open-ended |
| `governance.accountable_id` | `accountable_human_id` | **Always human** |
| `governance.owner_id` | — | Typically dept lead or role owner |
| `evidence_refs` | — | Approval tickets, ADR refs for activation |

---

## Relationship to `holds`

Each active RoleAssignment materializes one governed `holds` Relationship between actor and Role (see [METAMODEL.md](../METAMODEL.md)):

```yaml
Relationship:
  id: rel-devin-holds-engineering-roster
  relationship_type: holds
  source_id: devin-engineering-roster      # actor_id when actor_type: agent
  target_id: engineering-roster            # role_id
  cardinality: many_to_many
  lifecycle_status: active
  valid_from: "2026-08-28T00:00:00Z"
  valid_until: null
  metadata:
    role_assignment_id: ra-devin-holds-engineering-roster
    authority_level: execute
    department_context_ids: [engineering]
```

**Role changes:** Retire the RoleAssignment (`status: retired`, `effective_until` set) and its `holds` Relationship. Create a new RoleAssignment for the new role. Do **not** rename `actor_id`.

---

## Human accountability rule

**Mandatory:** Every RoleAssignment MUST include `accountable_human_id`.

When an agent holds a role:

1. The agent performs operational work (`actor_type: agent`, `authority_level: execute` or lower unless explicitly delegated).
2. A human remains answerable for outcomes (`accountable_human_id`).
3. Agent assignment does **not** transfer legal, financial, or board-level accountability to the agent.

```yaml
# CORRECT — agent executes, human accountable
RoleAssignment:
  id: ra-hera-supports-product-owner
  role_id: product-owner
  actor_id: hera-marketing-lead
  actor_type: agent
  authority_level: propose
  accountable_human_id: human:ivan
  status: active

# FORBIDDEN — missing accountable human
RoleAssignment:
  id: ra-agent-only-owner
  role_id: finance-controller
  actor_id: finus-finance-controller
  actor_type: agent
  accountable_human_id: null   # INVALID
```

---

## Cross-department assignments

One actor may hold the same or different roles across multiple departments. Model each scope as a separate RoleAssignment (or one assignment with multiple `department_context_ids` when scope is identical).

```yaml
RoleAssignment:
  id: ra-thoth-reviewer-eng
  role_id: engineering-code-reviewer
  actor_id: thoth-research-analyst
  actor_type: agent
  department_context_ids: [engineering]
  scope: "PR review for engineering repos"
  authority_level: audit
  accountable_human_id: human:ivan
  effective_from: "2026-09-01T00:00:00Z"
  status: active

RoleAssignment:
  id: ra-thoth-curator-research
  role_id: research-literature-curator
  actor_id: thoth-research-analyst
  actor_type: agent
  department_context_ids: [research-education]
  scope: "Literature scan and source curation"
  authority_level: execute
  accountable_human_id: human:ivan
  effective_from: "2026-09-01T00:00:00Z"
  status: active
```

Count at `organization_instance` layer: **2 assignments**, **1 agent**.

---

## Conflict rules

When two active RoleAssignments collide on the same actor, scope, or controlled process, apply these rules in order:

1. **Explicit `conflict_rules` on the assignment** — if listed, evaluate named SoD rules from [CONTROLS.md](../CONTROLS.md) first.
2. **`independence_requirement: separate_agent`** — the same `actor_id` cannot hold both primary and counteracting roles for the same `controlled_process_id` in the same case.
3. **`independence_requirement: human`** — at least one side of the control pair must be `actor_type: human` with `authority_level: approve`.
4. **Authority precedence** — if two assignments grant conflicting `authority_level` in the same scope, the lower precedence assignment is suspended until the conflict is resolved; do not merge authority silently.
5. **Temporal overlap** — two active assignments to the same `role_id` + `actor_id` + overlapping `department_context_ids` + overlapping effective dates require explicit `conflict_rules` documentation or one assignment must be retired.

**Disagreement outcome:** Conflicts produce an **escalation artifact** (ticket, signal, or approval record) — not an infinite agent-to-agent debate loop.

---

## Examples

### Agent holds role; human accountable

```yaml
RoleAssignment:
  id: ra-devin-holds-engineering-roster
  role_id: engineering-roster
  actor_id: devin-engineering-roster
  actor_type: agent
  department_context_ids: [engineering]
  scope: "Engineering delivery and roster coordination"
  authority_level: execute
  accountable_human_id: human:ivan
  effective_from: "2026-08-28T00:00:00Z"
  effective_until: null
  status: active
  conflict_rules:
    - sod-separate-agent-for-safety-review
```

### Human holds role; agent supports (no duplicate accountability)

```yaml
RoleAssignment:
  id: ra-ivan-accountable-product-owner
  role_id: product-owner
  actor_id: human:ivan
  actor_type: human
  department_context_ids: [product-discovery]
  scope: "Backlog ownership and prioritization"
  authority_level: decide
  accountable_human_id: human:ivan
  effective_from: "2026-01-01T00:00:00Z"
  status: active
```

---

## Related documents

| Document | Relationship |
|----------|--------------|
| [METAMODEL.md](../METAMODEL.md) | Entity envelope, `holds` relationship vocabulary |
| [role-department.md](../../demiurge/schemas/role-department.md) | Role catalog schema; `agent_assignments[]` convenience field |
| [agent-soul.md](../../demiurge/schemas/agent-soul.md) | Agent schema; `roles[]` convenience field |
| [CONTROLS.md](../CONTROLS.md) | Counteracting controls and separation-of-duty rules |
| [CONTROL-MAP.md](../CONTROL-MAP.md) | AIW control pair inventory |
