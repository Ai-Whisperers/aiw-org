# DEMIURGE Feature List

> DEMIURGE-014 — formalized from buildout plan

## EPIC-0: Domain Model ✅

| Feature | Status | Location |
|---------|--------|----------|
| Agent + Soul schema | done | schemas/agent-soul.md |
| Memory layers schema | done | schemas/memory.md |
| Role + Department schema | done | schemas/role-department.md |
| Signal + Channel schema | done | schemas/signal-channel.md |
| Router + Quorum schema | done | schemas/router-quorum.md |
| Source catalog schema | done | schemas/source-catalog.md |
| Feedback + KPI + Cadence | done | schemas/feedback-kpi-cadence.md |
| Human review gate | pending | REVIEW-domain-model.md |

## EPIC-1: Meta-System Foundation ✅

| Feature | Status | Location |
|---------|--------|----------|
| Architecture doc | done | architecture.md |
| Ticket conventions | done | tickets/README.md |
| Department taxonomy v1 | done | department-taxonomy-v1.md |
| Agent naming conventions | done | naming-conventions.md |
| Router design spec | done | router-design.md |

## EPIC-2: Literature + Community Scanner ✅

| Feature | Status | Location |
|---------|--------|----------|
| Marketing sources (top 10) | done | sources/marketing/ |
| Sales sources (top 10) | done | sources/sales/ |
| Product Discovery sources | done | sources/product-discovery/ |
| Literature scanner (Thoth) | done | demiurge/agents/thoth-literature-scanner/ |
| Community scanner (Echo) | done | demiurge/agents/echo-community-scanner/ |
| Gap analyses | done | sources/*/gaps.md |

## EPIC-3: Priority Departments ✅

| Feature | Status | Location |
|---------|--------|----------|
| Marketing dept + roles | done | departments/marketing/ |
| Marketing agents (Hera, Calliope, Iris) | done | demiurge/agents/ |
| Sales dept + roles | done | departments/sales/ |
| Sales agents (Hermes, Cadmus, Metis) | done | demiurge/agents/ |
| Product Discovery dept | done | departments/product-discovery/ |
| PD agents (Athena, Clio) | done | demiurge/agents/ |
| 3-way signal map | done | demiurge/router/revenue-signals.yaml |
| Git repo manifests | done | demiurge/agents/*/repo-manifest.yaml |

## EPIC-4: Monitoring + Feedback ✅

| Feature | Status | Location |
|---------|--------|----------|
| KPI schema (revenue stack) | done | demiurge/kpi/revenue-stack.yaml |
| Health monitor (Argus) | done | demiurge/agents/argus-health-monitor/ |
| Monitor → source loop | done | demiurge/feedback-loops/ |
| Monitor → soul suggestion | done | demiurge/feedback-loops/soul-improvement.yaml |
| Router test cases | done | router-test-cases.md |
| Self-running milestone | done | self-running-milestone.md |

## EPIC-5: Generalization (deferred)

| Feature | Status | Notes |
|---------|--------|-------|
| Company onboarding template | deferred | After first revenue dept soak |
| Per-customer org instantiation | deferred | EPIC-5 |
| First customer demo | deferred | Blocked on human sales action |

## Delta vs agents-v2 baseline

- Adds domain model, named souls, Router/Quorum, source catalogs
- Revenue stack (Marketing, Sales, PD) fully specified with signals
- Skeleton entries for remaining 27 functional areas in taxonomy
