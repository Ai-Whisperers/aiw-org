# Schema: Agent + Soul + Skill + Tool

> DEMIURGE-001
> **Metamodel:** Field mappings to the common Entity envelope — [METAMODEL.md](../../enterprise-framework/METAMODEL.md).

## Agent

The AI entity doing work. Has a memorable **name**, not just a role ID.

```yaml
Agent:
  id: string              # kebab-case, e.g. hera-marketing-lead
  name: string            # memorable, e.g. "Hera"
  display_name: string    # "Hera — Head of Marketing"
  soul: Soul              # ref by id
  roles: Role[]           # one agent may hold multiple roles
  memory: Memory          # ref by agent id
  skills: Skill[]         # Hermes skills
  tools: Tool[]           # MCPs, scripts, APIs
  cadence: Cadence        # when this agent acts
  git_repo: string        # https://github.com/Ai-Whisperers/aiw-agent-<id>
  status: enum            # draft | active | paused | deprecated
  departments: string[]   # dept ids this agent serves
```

### Agent naming rules

- `id`: `{name-lowercase}-{primary-role}` e.g. `hera-marketing-lead`
- `name`: single mythological or memorable name, human-assigned
- One name per agent; role changes do not require rename

### Entity envelope mapping (Agent)

| Entity field | Agent field | Notes |
|--------------|-------------|-------|
| `id` | `id` | Stable; never encodes current role |
| `entity_type` | `"Agent"` | Fixed type discriminator |
| `schema_version` | — | Schema file version when formalized |
| `name` | `name` | Memorable agent name |
| `definition` | — | Derived from soul archetype + roles |
| `purpose` | — | Dept/role mission statement |
| `lifecycle.status` | `status` | Maps: draft, active, paused→suspended, deprecated→retired |
| `governance.owner_id` | — | Typically dept lead or human owner |
| `evidence_refs` | — | Eval gate results, ADR refs |
| `created_at` / `updated_at` | — | Operational timestamps |

### Relationship mapping (Agent)

Agent participates in these governed relationships (see [METAMODEL.md](../../enterprise-framework/METAMODEL.md)):

| Relationship | Direction | Target | Cardinality | Denormalized field |
|--------------|-----------|--------|-------------|-------------------|
| `holds` | Agent → Role | Role id | many_to_many | `roles[]` |
| `belongs_to` | Agent → Department | Department id | many_to_many | `departments[]` |
| `performs` | Cadence → Role | Role id | many_to_many | via `cadence` |
| `has` | Agent → Soul | Soul id | one_to_one | `soul` |
| `has` | Agent → Memory | Memory id | one_to_one | `memory` |

**Role changes:** Retire the `holds` Relationship, create a new one, update `roles[]`. Do not change Agent `id` or Soul `id`.

## Soul

Immutable identity kernel (Hermes concept). Separate from operational memory.

```yaml
Soul:
  id: string              # matches agent id
  archetype: enum         # Strategist | Builder | Watchdog | Curator | Connector | Analyst | Coach
  values: string[]        # behavioral constitution (3-7 items)
  hard_stops: HardStop[]  # actions requiring approval
  prompt_ref: string      # path to PROMPT.md
  primary_model: string   # e.g. openrouter/anthropic/claude-sonnet-4
  fallback_model: string  # e.g. litellm/primary
  version: semver         # bumped when character evolves (not for memory)
  created_at: iso8601
  updated_at: iso8601
```

Soul is a **versioned sub-component** of Agent (proposed — see [METAMODEL.md](../../enterprise-framework/METAMODEL.md) open questions). Maps partially to Entity envelope via parent Agent; `Soul.version` tracks identity evolution independently of operational memory.

### Entity envelope mapping (Soul)

| Entity field | Soul field | Notes |
|--------------|------------|-------|
| `id` | `id` | Matches parent Agent id (1:1) |
| `entity_type` | `"Soul"` | Sub-component, not standalone org instance |
| `schema_version` | `version` | Semver; bumped on character evolution |
| `lifecycle.status` | — | Governed via parent Agent lifecycle |
| `updated_at` | `updated_at` | Last soul revision timestamp |

### HardStop (embedded in Soul)

```yaml
HardStop:
  action: string          # e.g. send_external_message, merge_pr
  require_approval: boolean
  approved_human: string  # ivan | kiki | board
  rate_limit_per_run: int # optional
```

### Archetypes

| Archetype | Typical roles |
|-----------|---------------|
| Strategist | Dept leads, board, product discovery |
| Builder | Engineering, content production |
| Watchdog | Security, compliance, health monitor |
| Curator | Research, source curation, literature scanner |
| Connector | Sales, community, routing |
| Analyst | RevOps, finance, KPI monitor |
| Coach | Coaching, people, onboarding |

## Skill

Hermes skill reference.

```yaml
Skill:
  id: string
  name: string
  path: string            # skill file or repo path
  version: string
  required: boolean
```

## Tool

External capability (MCP, script, API).

```yaml
Tool:
  id: string
  name: string
  type: enum              # mcp | script | api | webhook
  endpoint: string        # URL or path
  credentials_ref: string # BWS secret id, never inline
  scopes: string[]
```

## JSON Schema fragment (Agent)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Agent",
  "type": "object",
  "required": ["id", "name", "soul", "git_repo", "status"],
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
    "name": { "type": "string", "minLength": 2, "maxLength": 32 },
    "display_name": { "type": "string" },
    "soul": { "$ref": "#/$defs/Soul" },
    "roles": { "type": "array", "items": { "type": "string" } },
    "git_repo": { "type": "string", "format": "uri" },
    "status": { "enum": ["draft", "active", "paused", "deprecated"] }
  }
}
```

## Validation checklist

- [ ] Every active agent has a Soul with prompt_ref pointing to existing PROMPT.md
- [ ] hard_stops YAML parses and passes ai-safety scan
- [ ] git_repo is set before status → active
- [ ] name is unique across the org instance
