# Technology Entities

> **Domain:** 5 — Technology
> **Status:** `proposed`
> **Terms:** [system](../../terminology/TERMS.md), [agent](../../terminology/TERMS.md)

Entities describing software, infrastructure, interfaces, and deployments that agents and humans use to operate.

---

## Agent vs Tool vs Application vs System

| Entity | Definition | Example |
|--------|------------|---------|
| **Agent** | AI worker with soul, roles, memory, cadence | Hera, Thoth |
| **Tool** | Utility an agent **invokes** for a specific function | Web search, file read, MCP server |
| **Application** | Deployable software unit providing interfaces | Hermes CLI, LiteLLM proxy |
| **System** | Bounded collection delivering a business/technical function | Hermes orchestration stack |

**Critical rule:**

- An **Agent may use** a Tool — via skills, MCP, or scripts.
- An **Agent is not** automatically a Tool or Application.
- An Agent is an organization_instance actor; Tool and Application are technology entities.
- Do not model agents as tools in the technology catalog unless documenting a specific tool interface an agent exposes to others.

```yaml
# CORRECT
Relationship:
  relationship_type: consumes
  source_id: hera-marketing-lead    # Agent
  target_id: tool:web-search        # Tool

# FORBIDDEN — collapses agent into technology
Tool:
  id: hera-marketing-lead           # Agent id used as Tool
  entity_type: Tool
```

---

## Entity definitions

### Application

A deployable software unit — binary, container, or service — with defined interfaces and lifecycle.

```yaml
Application:
  entity_type: Application
  runtime: python | node | go | container | other
  version: semver
  system_id: string
  interface_ids: string[]
```

### System

A bounded collection of applications, components, infrastructure, and interfaces delivering a function.

```yaml
System:
  entity_type: System
  purpose: string
  application_ids: string[]
  component_ids: string[]
  infrastructure_node_ids: string[]
  owner_role_id: string
```

### Component

A modular part within an application or system — library, module, microservice, plugin.

```yaml
Component:
  entity_type: Component
  parent_id: string
  component_type: library | module | microservice | plugin
  version: semver
```

### Tool

A utility invoked by agents or humans for a specific function. Narrower scope than Application.

```yaml
Tool:
  entity_type: Tool
  tool_type: mcp | skill | script | api_client | cli
  invocation_method: string
  agent_skill_ref: string | null
```

### API

A defined programmatic interface — endpoints, operations, schemas. May be internal or external.

```yaml
API:
  entity_type: API
  api_type: rest | graphql | grpc | webhook | other
  specification_ref: string
  version: semver
  interface_id: string
```

### Interface

A connection point between systems, applications, or actors — abstracts protocol and data contract.

```yaml
Interface:
  entity_type: Interface
  protocol: string
  data_format: json | yaml | protobuf | other
  api_id: string | null
```

### Channel

A delivery path for signals and messages. **Canonical schema:** [signal-channel.md](../../demiurge/schemas/signal-channel.md).

**Distinct from:** Interface (technical contract); Channel is operational routing (WhatsApp, email, in-app).

```yaml
Channel:
  entity_type: Channel
  channel_type: whatsapp | email | slack | in_app | webhook | other
  signal_type_ids: string[]
```

### DataStore

A persistent storage system — database, object store, file system, vault.

```yaml
DataStore:
  entity_type: DataStore
  store_type: sqlite | postgres | git | s3 | vault | other
  data_asset_ids: string[]
  classification: string
```

### InfrastructureNode

A compute, network, or hosting resource — VM, container host, CDN edge, DNS zone.

```yaml
InfrastructureNode:
  entity_type: InfrastructureNode
  node_type: vm | container_host | serverless | network | other
  environment: development | staging | production
  system_ids: string[]
```

### Deployment

An installed instance of an application or system in an environment — binds version to infrastructure.

**Note:** METAMODEL uses `runtime_deployment` for cadence/cron execution. This entity is the **technology deployment** (software install); cadence is operational execution.

```yaml
Deployment:
  entity_type: Deployment
  application_id: string
  infrastructure_node_id: string
  environment: development | staging | production
  deployed_at: iso8601
  version: semver
```

---

## Relationships (examples)

| Source | Type | Target | Meaning |
|--------|------|--------|---------|
| Agent | `consumes` | Tool | Agent invokes tool |
| Application | `depends_on` | Component | App composed of components |
| System | `contains` | Application | System groups applications |
| Deployment | `implements` | Application | Deployed instance of app |
| API | `supports` | Interface | API realizes interface |
| DataStore | `supports` | DataAsset | Storage holds governed data |

---

## AIW instances (v0.1)

| Entity | Instance status | Notes |
|--------|-----------------|-------|
| System | yes | Hermes, LiteLLM, git repos |
| Tool | yes | MCP servers, Hermes skills |
| Channel | yes | WhatsApp, webhook, in-app |
| DataStore | yes | SQLite, git, BWS vault |
| Application, Component | partial | Scripts, agents repos |
| API, Interface | partial | Webhooks, MCP protocols |
| InfrastructureNode, Deployment | partial | Host environment implicit |

---

## Related documents

- [agent-soul.md](../../demiurge/schemas/agent-soul.md) — Agent model
- [signal-channel.md](../../demiurge/schemas/signal-channel.md) — Channel
- [information-data.md](information-data.md) — DataAsset
- [METAMODEL.md](../METAMODEL.md) — runtime_deployment vs Deployment
