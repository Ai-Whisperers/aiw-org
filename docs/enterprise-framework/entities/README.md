# AIW Enterprise Entity Catalog

> **Status:** `proposed` — AIW-04 pending approval.
> **Scope:** Type definitions and example schemas only — no runtime objects, agents, or departments.
> **Metamodel:** All entities conform to the [Entity envelope](../METAMODEL.md).
> **Terminology:** Authoritative definitions in [TERMS.md](../../terminology/TERMS.md).

---

## Purpose

Catalogue business entity types missing from AIW's agent-centric domain model. Entity definitions do **not** imply the corresponding function is active in AIW — they enable consistent modeling when those functions are introduced.

---

## Domains

| # | Domain | File | Entity count |
|---|--------|------|--------------|
| 1 | Organization | *(DEMIURGE — see below)* | 8 |
| 2 | Value and market | [value-market.md](value-market.md) | 10 |
| 3 | Work and behavior | [work.md](work.md) | 11 |
| 4 | Information and data | [information-data.md](information-data.md) | 12 |
| 5 | Technology | [technology.md](technology.md) | 10 |
| 6 | Governance | [governance.md](governance.md) | 13 |

**Coverage matrix:** [ENTITY-COVERAGE.md](../ENTITY-COVERAGE.md)

---

## Domain 1: Organization

Organization entities are defined in the DEMIURGE model and reconciled with the metamodel. This catalog references them; it does not redefine them.

| Entity | Definition status | Schema path | Owner | Standard basis | AIW instances |
|--------|-------------------|-------------|-------|----------------|---------------|
| Agent | defined | [agent-soul.md](../../demiurge/schemas/agent-soul.md) | AI Ops | DEMIURGE | yes |
| Soul | defined (sub-component) | [agent-soul.md](../../demiurge/schemas/agent-soul.md) | AI Ops | DEMIURGE | yes |
| Role | defined | [role-department.md](../../demiurge/schemas/role-department.md) | AI Ops | RACI | yes |
| Department | defined | [role-department.md](../../demiurge/schemas/role-department.md) | AI Ops | Org design | yes |
| Cadence | defined | [feedback-kpi-cadence.md](../../demiurge/schemas/feedback-kpi-cadence.md) | AI Ops | DEMIURGE | yes |
| KPI | defined | [feedback-kpi-cadence.md](../../demiurge/schemas/feedback-kpi-cadence.md) | Dept owners | DEMIURGE | partial |
| Relationship | defined | [METAMODEL.md](../METAMODEL.md) | Framework | DEMIURGE | yes |
| StandardAlignment | defined | [METAMODEL.md](../METAMODEL.md) | Framework | ISO/RACI | partial |

---

## Domain 2: Value and market

| Entity | Definition status | Schema path | Owner | Standard basis | AIW instances |
|--------|-------------------|-------------|-------|----------------|---------------|
| Customer | defined | [value-market.md](value-market.md) | Sales / PO | CRM | no |
| CustomerSegment | defined | [value-market.md](value-market.md) | Marketing | Segmentation | partial |
| Need | defined | [value-market.md](value-market.md) | Product | Jobs-to-be-done | no |
| ValueProposition | defined | [value-market.md](value-market.md) | Product | Lean canvas | partial |
| Product | defined | [value-market.md](value-market.md) | Product Owner | Product mgmt | partial |
| Service | defined | [value-market.md](value-market.md) | Product Owner | ITIL service | partial |
| Offering | defined | [value-market.md](value-market.md) | Sales | Commercial | no |
| Contract | defined | [value-market.md](value-market.md) | Legal / Finance | Contract law | no |
| Supplier | defined | [value-market.md](value-market.md) | Finance | Vendor mgmt | partial |
| Partner | defined | [value-market.md](value-market.md) | BD | Partnership | no |

---

## Domain 3: Work and behavior

| Entity | Definition status | Schema path | Owner | Standard basis | AIW instances |
|--------|-------------------|-------------|-------|----------------|---------------|
| Capability | defined | [work.md](work.md) | Strategy | BizBOK | partial |
| ValueStream | defined | [work.md](work.md) | Operations | Lean | no |
| Process | defined | [work.md](work.md) | Operations | BPMN | partial |
| Subprocess | defined | [work.md](work.md) | Operations | BPMN | no |
| Activity | defined | [work.md](work.md) | Operations | BPMN | no |
| Workflow | defined | [work.md](work.md) | AI Ops | DEMIURGE | partial |
| Procedure | defined | [work.md](work.md) | Compliance | SOP | partial |
| Task | defined | [work.md](work.md) | Dept owners | Work mgmt | yes (artifact) |
| Decision | defined | [work.md](work.md) | Leadership | RACI | yes (artifact) |
| Approval | defined | [work.md](work.md) | Governance | RACI | partial |
| Event | defined | [work.md](work.md) | AI Ops | Event-driven | partial |

---

## Domain 4: Information and data

| Entity | Definition status | Schema path | Owner | Standard basis | AIW instances |
|--------|-------------------|-------------|-------|----------------|---------------|
| InformationDomain | defined | [information-data.md](information-data.md) | Data steward | DAMA | no |
| DataDomain | defined | [information-data.md](information-data.md) | Data steward | DAMA | no |
| DataAsset | defined | [information-data.md](information-data.md) | Data steward | DAMA | partial |
| Dataset | defined | [information-data.md](information-data.md) | Data steward | DAMA | partial |
| RecordType | defined | [information-data.md](information-data.md) | Engineering | Schema design | partial |
| DataElement | defined | [information-data.md](information-data.md) | Data steward | DAMA | no |
| Document | defined | [information-data.md](information-data.md) | Knowledge | DEMIURGE | yes |
| Artifact | defined | [artifacts.md](../../demiurge/schemas/artifacts.md) | Dept owners | DEMIURGE | yes |
| Source | defined | [source-catalog.md](../../demiurge/schemas/source-catalog.md) | Research | DEMIURGE | yes |
| Signal | defined | [signal-channel.md](../../demiurge/schemas/signal-channel.md) | AI Ops | DEMIURGE | yes |
| Event | defined | [work.md](work.md) / [information-data.md](information-data.md) | AI Ops | Event-driven | partial |
| Metric | defined | [information-data.md](information-data.md) | Dept owners | KPI framework | partial |

---

## Domain 5: Technology

| Entity | Definition status | Schema path | Owner | Standard basis | AIW instances |
|--------|-------------------|-------------|-------|----------------|---------------|
| Application | defined | [technology.md](technology.md) | Engineering | TOGAF | partial |
| System | defined | [technology.md](technology.md) | Platform | TOGAF | yes |
| Component | defined | [technology.md](technology.md) | Engineering | C4 model | partial |
| Tool | defined | [technology.md](technology.md) | AI Ops | DEMIURGE | yes |
| API | defined | [technology.md](technology.md) | Engineering | OpenAPI | partial |
| Interface | defined | [technology.md](technology.md) | Engineering | Integration | partial |
| Channel | defined | [signal-channel.md](../../demiurge/schemas/signal-channel.md) | AI Ops | DEMIURGE | yes |
| DataStore | defined | [technology.md](technology.md) | Platform | DAMA | yes |
| InfrastructureNode | defined | [technology.md](technology.md) | Platform | Infra | partial |
| Deployment | defined | [technology.md](technology.md) | Platform | CI/CD | partial |

---

## Domain 6: Governance

| Entity | Definition status | Schema path | Owner | Standard basis | AIW instances |
|--------|-------------------|-------------|-------|----------------|---------------|
| Goal | defined | [governance.md](governance.md) | Leadership | OKR | partial |
| Requirement | defined | [governance.md](governance.md) | Product / Eng | Requirements eng | partial |
| Principle | defined | [governance.md](governance.md) | Architecture | ADR | partial |
| Policy | defined | [governance.md](governance.md) | Compliance | ISO 27001 | partial |
| Standard | defined | [governance.md](governance.md) | Framework | ISO / internal | partial |
| Risk | defined | [governance.md](governance.md) | Risk owner | ISO 31000 | no |
| Control | defined | [governance.md](governance.md) | Compliance | COSO | partial |
| Obligation | defined | [governance.md](governance.md) | Legal | Regulatory | no |
| Classification | defined | [governance.md](governance.md) | Security | Data classification | partial |
| KPI | defined | [feedback-kpi-cadence.md](../../demiurge/schemas/feedback-kpi-cadence.md) | Dept owners | DEMIURGE | partial |
| SLO | defined | [governance.md](governance.md) | Platform | SRE | no |
| Owner | defined | [governance.md](governance.md) | Governance | RACI | yes |
| Steward | defined | [governance.md](governance.md) | Data / Knowledge | DAMA | partial |

---

## Out of scope (v0.1)

The following are intentionally **not** catalogued in v0.1:

- Individual employee roles (10,000-scale job titles) — use Capability + Role references instead
- Legal entities, physical assets, facilities, vehicles
- Financial instruments (invoices, payments, ledger entries)
- Every conceivable regulatory filing type

Gaps are tracked in [ENTITY-COVERAGE.md](../ENTITY-COVERAGE.md) with `validation_state: out_of_scope`.

---

## Related documents

| Document | Relationship |
|----------|--------------|
| [METAMODEL.md](../METAMODEL.md) | Entity envelope and Relationship model |
| [GOVERNANCE.md](../GOVERNANCE.md) | Lifecycle states for catalog entries |
| [ENTITY-COVERAGE.md](../ENTITY-COVERAGE.md) | Full coverage matrix |
| [domain-model.md](../../demiurge/domain-model.md) | DEMIURGE object graph |
