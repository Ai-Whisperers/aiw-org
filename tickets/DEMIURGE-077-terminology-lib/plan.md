# DEMIURGE-077: Terminology Library v1 — authoritative vocabulary

**Sprint**: Phase 1 — Identify + Stabilize
**Size**: 90m
**Owner**: AI + Ivan review
**Output**: `docs/terminology/TERMS.md`

## Objective

Create the single authoritative source for every term used across the AI Whisperers system. All agents, rules, prompts, schemas, and tickets defer to this file for definitions. No local redefinitions. No implicit meanings.

This is a living document — terms are added here first, then used elsewhere.

## Why this matters

Every system that grows without a vocabulary authority develops dialect drift. "Signal" means one thing in `revenue-signals.yaml` and something slightly different in a ticket plan. "Notification" and "alert" get used interchangeably. This accumulates into agent misrouting, schema conflicts, and onboarding confusion.

## Scope — term categories to cover in v1

### 1. Org structure
- department, sub-department, functional area
- tier (T1/T2/T3/T4) — what each tier means operationally
- status: active, skeleton, prototype, deferred, archived
- activation trigger

### 2. Agent model
- agent, soul, archetype, lead agent, sub-agent
- router, monitor, scanner, coach, decorator, finder, researcher
- prototype vs active vs deferred agent

### 3. Communication & information types
- signal, notification, alert, request, inform, escalation, acknowledgment, broadcast
- urgency tier: P0 (immediate), P1 (same-day), P2 (weekly), P3 (async)
- formality level: formal, semi-formal, informal
- tone: directive, advisory, informational, confirmatory
- directionality: inbound, outbound, internal, cross-dept, org-wide

### 4. Documents & knowledge
- document, artifact, spec, plan, report, transcript, research, synthesis
- nugget — a valuable piece of information embedded in a document, may be left intentionally
- source, citation, catalog, bibliography
- derived attribute vs given attribute (document classification)

### 5. Operational
- cadence, heartbeat, cron, eval gate, hard stop, quorum, SLA
- soul improvement, soul version, reflection

### 6. Roles
- role, function, responsibility
- Tier coding per ROLES-INVENTORY.md

## Format per term

```yaml
term: signal
category: communication
definition: >
  A discrete, typed event emitted by a department or agent to indicate a state
  change or trigger a downstream action. Signals are machine-processable and
  routed by the router agent.
not_to_be_confused_with:
  notification: "Sent to inform a human. Not intended to trigger agent logic."
  alert: "High-urgency signal requiring immediate response. Subset of signal."
properties:
  - type (required)
  - urgency_tier (default: P2)
  - routing_tags
  - payload_schema
used_in:
  - "departments/*/signals.yaml"
  - "demiurge/router/revenue-signals.yaml"
```

## Process

1. Grep all existing `.yaml`, `.md` files for terms that are used but not defined
2. List every term in `department-taxonomy-v1.md`, `ROLES-INVENTORY.md`, `demiurge/schemas/`
3. List every communication-related term in `signals.yaml` files
4. Write definitions in YAML-in-Markdown format
5. Cross-reference terms that overlap or could be confused
6. Ivan reviews for correctness in his domain (communication + information types)

## Acceptance criteria

- [x] `docs/terminology/TERMS.md` created
- [x] Minimum 40 terms defined across all 6 categories
- [x] Every term has: definition, category, `not_to_be_confused_with` (where relevant), `used_in`
- [x] No circular definitions
- [x] Document header states: "This file is authoritative. Add here first, use elsewhere second."
- [x] DEMIURGE-078 (document intelligence) can reference this as its vocabulary source
