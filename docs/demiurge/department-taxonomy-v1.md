# Department Taxonomy v2

> DEMIURGE-011 — seeds agents-v2 functional area taxonomy
> DEMIURGE-070 — add missing depts, fix status drift, restore original-20 entries

## Tier 1 — Core (7)

| id | name | status | priority |
|----|------|--------|----------|
| operations | Operations | **active** | — |
| finance-legal | Finance & Legal | skeleton | — |
| sales | Sales | **active** | P0 |
| engineering | Engineering & Delivery | skeleton | — |
| research | Research & Education | skeleton | — |
| people | People & Culture | skeleton | — |
| ai-org-platform | AI Org Platform | skeleton | — |

## Tier 1 sub — Revenue (priority build)

| id | name | status | priority |
|----|------|--------|----------|
| marketing | Marketing | **active** | P0 |
| product-discovery | Product Discovery | **active** | P0 |

## Tier 2 — Cross-cutting (15)

| id | name | status |
|----|------|--------|
| ai-ops | AI Ops | skeleton |
| bizops | BizOps | skeleton |
| compliance | Compliance | skeleton |
| revops | RevOps | skeleton |
| knowledge-mgmt | Knowledge Management | active |
| customer-success | Customer Success | skeleton |
| ai-safety | AI Safety | skeleton |
| procurement | Procurement | skeleton |
| executive-office | Executive Office | skeleton |
| it-enterprise | IT Enterprise | skeleton |
| business-development | Business Development | skeleton |
| cybersecurity | Cybersecurity | skeleton |
| design-creative | Design & Creative | skeleton |
| corporate-communications | Corporate Communications | skeleton |
| multimedia | Multimedia | skeleton |

### Tier 2 activation triggers (DEMIURGE-070 additions)

| id | activation trigger |
|----|-------------------|
| executive-office | >5 active depts need CEO-office coordination |
| it-enterprise | first internal IT hire or >10 enterprise SaaS tools |
| business-development | first strategic partnership or channel deal |
| cybersecurity | handling regulated/sensitive data or first security audit |
| design-creative | first design hire or brand/UX deliverable at scale |
| corporate-communications | first PR launch or sustained media relations |
| multimedia | first video/audio production beyond ad-hoc assets |

`executive-office` (Tier 2) is the CEO-office department shell; `chief-of-staff` (Tier 3) is the promoted dedicated CoS role when coordination load exceeds >50 hrs/week — not duplicate entries.

## Tier 3 — Deferred (17)

| id | name | promotion trigger |
|----|------|-------------------|
| marketing-independent | Marketing (standalone dept) | >$2K/mo marketing budget |
| cs-standalone | Customer Success | 5+ recurring clients |
| compliance-standalone | Compliance | first EU client |
| knowledge-standalone | Knowledge Mgmt | >100 source files |
| ai-governance | AI Governance | >15 agents |
| investor-relations | Investor Relations | first external investor |
| chief-of-staff | Chief of Staff | >50 hrs coord/week |
| devrel | Developer Relations | public API launch |
| workplace | Workplace / Facilities | physical office |
| fraud-risk | Fraud & Risk | $500K+ payment volume |
| compensation | Compensation & Benefits | first FTE |
| people-ops | People Operations | 5+ FTEs |
| pmo | Program Management Office | >8 active depts |
| field-services | Field Services | first enterprise client |
| data-science | Data Science | data volume justifies dedicated team |
| customer-experience | Customer Experience | 10+ recurring clients |
| product-management | Product Management | >3 parallel roadmap tracks |

## Governance — non-dept node

Not a standard department. Oversight and quarterly review; agent `board-of-directors` exists.

| id | name | status |
|----|------|--------|
| board | Board of Directors | skeleton |

## Tier 4 — Enterprise (4)

Documented in constitution; not in scope at current scale.

## Build order (Ivan directive + DEMIURGE)

1. **Marketing** — demand generation
2. **Product Discovery** — what to build/sell
3. **Sales** — revenue capture
4. Operations + AI Ops (management spine)
5. Engineering
6. Finance + Compliance
7. Research + Knowledge
8. People
9. Tier 3 on trigger

## Skeleton definition

`skeleton` = mission + role inventory + source catalog stub + signal types defined; no active agents until focused session.

## Parent/child

```
sales-growth (playbook)
├── marketing (sub-dept at Tier 1, promotes Tier 3)
├── sales
└── revops (Tier 2)
```
