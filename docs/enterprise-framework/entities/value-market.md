# Value and Market Entities

> **Domain:** 2 — Value and market
> **Status:** `proposed`
> **Terms:** [customer](../../terminology/TERMS.md), [product](../../terminology/TERMS.md), [service](../../terminology/TERMS.md)

External-facing entities describing who AIW serves, what problems are solved, and how value is packaged and exchanged.

---

## Entity definitions

### Customer

An external party that receives value — individual, team, or organization. May hold contracts and consume products or services.

**Distinct from:** Partner (collaborates without necessarily paying); internal Agent or Department.

```yaml
Customer:
  entity_type: Customer
  customer_type: individual | team | organization
  segment_ids: string[]
  contact_refs: string[]
  contract_ids: string[]
  lifecycle_stage: prospect | active | churned | archived
```

### CustomerSegment

A group of customers sharing characteristics, needs, or buying behavior. Used for targeting and positioning.

**Distinct from:** Customer (a segment is a classification, not a party).

```yaml
CustomerSegment:
  entity_type: CustomerSegment
  criteria: string[]
  geographic_scope: string | null
  icp_ref: string | null
```

### Need

A problem, job-to-be-done, or outcome a customer seeks. Needs drive value propositions and product design.

**Distinct from:** Requirement (internal specification); ValueProposition (our response to a need).

```yaml
Need:
  entity_type: Need
  description: string
  segment_ids: string[]
  priority: high | medium | low
  evidence_refs: string[]
```

### ValueProposition

A statement of how AIW creates value for a segment — problems solved, benefits delivered, differentiators.

**Distinct from:** Product (concrete offering); Need (customer-side problem).

```yaml
ValueProposition:
  entity_type: ValueProposition
  segment_ids: string[]
  problems_addressed: string[]
  benefits: string[]
  differentiators: string[]
  product_ids: string[]
```

### Product

A packaged offering solving defined customer problems for target segments. See minimum schema below.

**Distinct from:** Service (component of delivery); Offering (commercial wrapper).

```yaml
Product:
  entity_type: Product
  target_segments: string[]
  problems: string[]
  value_propositions: string[]
  included_services: string[]
  exclusions: string[]
  lifecycle_stage: discovery | pilot | active | sunset
  product_owner_role_id: string
  acceptance_policy_ref: string
  commercial_terms_ref: string | null
```

### Service

A discrete capability or deliverable provided to customers — consulting, automation, content, support.

**Distinct from:** Capability (internal ability); Product (market-facing package).

```yaml
Service:
  entity_type: Service
  service_type: consulting | automation | content | support | other
  inputs: string[]
  outputs: string[]
  quality_criteria: string[]
  product_ids: string[]
```

### Offering

A commercial wrapper — SKU, bundle, tier, or pricing package — that references products, services, and contract terms.

**Distinct from:** Product (what is delivered); Contract (legal agreement).

```yaml
Offering:
  entity_type: Offering
  product_ids: string[]
  service_ids: string[]
  pricing_model: fixed | subscription | usage | custom
  contract_template_ref: string | null
```

### Contract

A legal or commercial agreement governing delivery, payment, and obligations between AIW and a customer or partner.

**Distinct from:** Offering (commercial structure); Obligation (governance entity).

```yaml
Contract:
  entity_type: Contract
  party_ids: string[]
  offering_id: string | null
  effective_from: iso8601
  effective_until: iso8601 | null
  terms_ref: string
```

### Supplier

An external party providing goods or services to AIW — vendors, contractors, infrastructure providers.

**Distinct from:** Partner (strategic collaboration); Customer (receives value from AIW).

```yaml
Supplier:
  entity_type: Supplier
  supplier_type: vendor | contractor | infrastructure | other
  service_scope: string[]
  contract_ids: string[]
```

### Partner

An external party collaborating with AIW for mutual benefit — co-marketing, integration, referral, joint delivery.

**Distinct from:** Customer (may not pay); Supplier (provides to AIW operationally).

```yaml
Partner:
  entity_type: Partner
  partnership_type: co_marketing | integration | referral | joint_delivery | other
  mutual_obligations_ref: string | null
```

---

## Relationships (examples)

| Source | Type | Target | Meaning |
|--------|------|--------|---------|
| Product | `realizes` | ValueProposition | Product delivers on proposition |
| Product | `contains` | Service | Product bundles services |
| Customer | `belongs_to` | CustomerSegment | Customer classified in segment |
| Contract | `depends_on` | Offering | Contract references commercial terms |
| Need | `informs` | ValueProposition | Customer need shapes positioning |

---

## AIW instances (v0.1)

| Entity | Instance status | Notes |
|--------|-----------------|-------|
| Product | partial | Coaching, agent templates referenced informally; no governed catalog |
| Service | partial | Consulting and automation services implicit |
| CustomerSegment | partial | LATAM/PY ICP in research; not formalized as entities |
| Customer, Offering, Contract, Partner | no | Not modeled as first-class entities yet |

Entity definitions exist; operational activation is separate.

---

## Related documents

- [README.md](README.md) — catalog index
- [work.md](work.md) — Capability and Process
- [governance.md](governance.md) — Policy and Obligation
