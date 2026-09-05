# AIW Enterprise Entity Coverage Matrix

> **Status:** `proposed` — AIW-04
> **Purpose:** Track definition, schema, standard mapping, instances, ownership, and approval state for every catalogued entity type.
> **Catalog:** [entities/README.md](entities/README.md)

---

## Column definitions

| Column | Values |
|--------|--------|
| **definition present** | `yes` — non-circular definition in catalog; `partial` — referenced only; `no` — gap |
| **schema present** | `yes` — YAML example or DEMIURGE schema; `partial` — informal only; `no` — none |
| **standard mapping** | Primary external or internal standard basis |
| **AIW instances** | `yes` — operational instances exist; `partial` — implicit/informal; `no` — type only |
| **owner** | Responsible role or domain |
| **approval state** | `proposed` \| `approved` \| `out_of_scope` |
| **validation state** | `not_started` \| `peer_reviewed` \| `gate_pending` \| `validated` |

---

## Organization domain (DEMIURGE)

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| Agent | yes | yes | DEMIURGE | yes | AI Ops | proposed | gate_pending |
| Soul | yes | yes | DEMIURGE | yes | AI Ops | proposed | gate_pending |
| Role | yes | yes | RACI | yes | AI Ops | proposed | gate_pending |
| Department | yes | yes | Org design | yes | AI Ops | proposed | gate_pending |
| Cadence | yes | yes | DEMIURGE | yes | AI Ops | proposed | gate_pending |
| KPI | yes | yes | DEMIURGE | partial | Dept owners | proposed | not_started |
| Relationship | yes | yes | METAMODEL | yes | Framework | proposed | peer_reviewed |
| StandardAlignment | yes | yes | ISO/RACI | partial | Framework | proposed | not_started |

---

## Value and market domain

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| Customer | yes | yes | CRM | no | Sales / PO | proposed | not_started |
| CustomerSegment | yes | yes | Segmentation | partial | Marketing | proposed | not_started |
| Need | yes | yes | Jobs-to-be-done | no | Product | proposed | not_started |
| ValueProposition | yes | yes | Lean canvas | partial | Product | proposed | not_started |
| Product | yes | yes | Product mgmt | partial | Product Owner | proposed | not_started |
| Service | yes | yes | ITIL service | partial | Product Owner | proposed | not_started |
| Offering | yes | yes | Commercial | no | Sales | proposed | not_started |
| Contract | yes | yes | Contract law | no | Legal / Finance | proposed | not_started |
| Supplier | yes | yes | Vendor mgmt | partial | Finance | proposed | not_started |
| Partner | yes | yes | Partnership | no | BD | proposed | not_started |

---

## Work and behavior domain

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| Capability | yes | yes | BizBOK | partial | Strategy | proposed | not_started |
| ValueStream | yes | yes | Lean | no | Operations | proposed | not_started |
| Process | yes | yes | BPMN | partial | Operations | proposed | not_started |
| Subprocess | yes | yes | BPMN | no | Operations | proposed | not_started |
| Activity | yes | yes | BPMN | no | Operations | proposed | not_started |
| Workflow | yes | yes | DEMIURGE | partial | AI Ops | proposed | not_started |
| Procedure | yes | yes | SOP | partial | Compliance | proposed | not_started |
| Task | yes | yes | Work mgmt | yes | Dept owners | proposed | peer_reviewed |
| Decision | yes | yes | RACI | yes | Leadership | proposed | peer_reviewed |
| Approval | yes | yes | RACI | partial | Governance | proposed | not_started |
| Event | yes | yes | Event-driven | partial | AI Ops | proposed | not_started |

---

## Information and data domain

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| InformationDomain | yes | yes | DAMA | no | Data steward | proposed | not_started |
| DataDomain | yes | yes | DAMA | no | Data steward | proposed | not_started |
| DataAsset | yes | yes | DAMA | partial | Data steward | proposed | not_started |
| Dataset | yes | yes | DAMA | partial | Data steward | proposed | not_started |
| RecordType | yes | yes | Schema design | partial | Engineering | proposed | not_started |
| DataElement | yes | yes | DAMA | no | Data steward | proposed | not_started |
| Document | yes | yes | DEMIURGE | yes | Knowledge | proposed | gate_pending |
| Artifact | yes | yes | DEMIURGE | yes | Dept owners | proposed | gate_pending |
| Source | yes | yes | DEMIURGE | yes | Research | proposed | gate_pending |
| Signal | yes | yes | DEMIURGE | yes | AI Ops | proposed | gate_pending |
| Event | yes | yes | Event-driven | partial | AI Ops | proposed | not_started |
| Metric | yes | yes | KPI framework | partial | Dept owners | proposed | not_started |

---

## Technology domain

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| Application | yes | yes | TOGAF | partial | Engineering | proposed | not_started |
| System | yes | yes | TOGAF | yes | Platform | proposed | not_started |
| Component | yes | yes | C4 model | partial | Engineering | proposed | not_started |
| Tool | yes | yes | DEMIURGE | yes | AI Ops | proposed | not_started |
| API | yes | yes | OpenAPI | partial | Engineering | proposed | not_started |
| Interface | yes | yes | Integration | partial | Engineering | proposed | not_started |
| Channel | yes | yes | DEMIURGE | yes | AI Ops | proposed | gate_pending |
| DataStore | yes | yes | DAMA | yes | Platform | proposed | not_started |
| InfrastructureNode | yes | yes | Infra | partial | Platform | proposed | not_started |
| Deployment | yes | yes | CI/CD | partial | Platform | proposed | not_started |

---

## Governance domain

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| Goal | yes | yes | OKR | partial | Leadership | proposed | not_started |
| Requirement | yes | yes | Requirements eng | partial | Product / Eng | proposed | not_started |
| Principle | yes | yes | ADR | partial | Architecture | proposed | not_started |
| Policy | yes | yes | ISO 27001 | partial | Compliance | proposed | not_started |
| Standard | yes | yes | ISO / internal | partial | Framework | proposed | not_started |
| Risk | yes | yes | ISO 31000 | no | Risk owner | proposed | not_started |
| Control | yes | yes | COSO | partial | Compliance | proposed | not_started |
| Obligation | yes | yes | Regulatory | no | Legal | proposed | not_started |
| Classification | yes | yes | Data classification | partial | Security | proposed | not_started |
| KPI | yes | yes | DEMIURGE | partial | Dept owners | proposed | gate_pending |
| SLO | yes | yes | SRE | no | Platform | proposed | not_started |
| Owner | yes | yes | RACI | yes | Governance | proposed | not_started |
| Steward | yes | yes | DAMA | partial | Data / Knowledge | proposed | not_started |

---

## Out of scope (v0.1)

| Entity type | Definition present | Schema present | Standard mapping | AIW instances | Owner | Approval state | Validation state |
|-------------|-------------------|----------------|------------------|---------------|-------|----------------|------------------|
| Employee role (job title catalog) | no | no | HR taxonomy | no | HR | out_of_scope | not_started |
| Legal entity | no | no | Corporate law | no | Legal | out_of_scope | not_started |
| Physical asset | no | no | Asset mgmt | no | Operations | out_of_scope | not_started |
| Financial instrument | no | no | Accounting | no | Finance | out_of_scope | not_started |

---

## Summary

| Domain | Entity count | Definitions complete | Schemas complete | AIW instances (yes/partial) |
|--------|--------------|---------------------|------------------|----------------------------|
| Organization | 8 | 8 | 8 | 7 / 1 |
| Value and market | 10 | 10 | 10 | 0 / 4 |
| Work and behavior | 11 | 11 | 11 | 2 / 5 |
| Information and data | 12 | 12 | 12 | 5 / 5 |
| Technology | 10 | 10 | 10 | 4 / 6 |
| Governance | 13 | 13 | 13 | 1 / 9 |
| **Total catalogued** | **64** | **64** | **64** | **19 / 30** |
| Out of scope | 4 | — | — | — |

---

## Next validation steps

1. Peer review entity distinctions (Capability vs Process vs Workflow vs Procedure vs Task).
2. Ivan sign-off on TERMS.md enterprise entity entries (DEMIURGE-077 gate).
3. Add AIW-04 row to [APPROVALS.md](APPROVALS.md) when gate file is created.
4. Reconcile Task entity with DEMIURGE artifact `task` type — document mapping in work.md (done).

---

## Related documents

- [entities/README.md](entities/README.md) — catalog index
- [METAMODEL.md](METAMODEL.md) — Entity envelope
- [TERMS.md](../terminology/TERMS.md) — authoritative terms
