# Document Router

> DEMIURGE-078 — `document-intelligence/router`

```yaml
id: di-router
agent_id: pheme-document-router
implementation: demiurge/agents/pheme-document-router/
department: knowledge-mgmt
status: active
role: Deliver classified documents to the right agents and departments based on audience and urgency.
```

## Role

Takes Classifier output and routes the document envelope (and optional body) to recipients. P0/P1 triggers immediate delivery and acknowledgment; P2/P3 uses scheduled queue. `requires_human: true` routes to human-readable channels (WhatsApp, email).

## Inputs

- Classified `DocumentEnvelope` from Classifier
- Routing rules (dept signal config, agent subscriptions)

## Outputs

- Delivery records per recipient
- Signals or queue entries per `derived.urgency`
- Dead-letter queue entries when audience cannot be resolved

## Prior art

- **ITIL P0–P3** — urgency tiers (aligned with org signal vocabulary)
- **Content-based routing** — Apache Camel / ESB pattern: route on `audience` + `routing_tags`
- **Priority queues** — RabbitMQ/Kafka: separate queues by urgency tier

## Manual analog

Ivan's manual distribution — deciding who needs to see what and when.

## Dependencies

- **Classifier** — must run first
- **signal-channel.md** — may emit Signal artifacts for urgent cross-dept delivery
- **Hermes router** (DEMIURGE-072) — reconcile before Phase 3 if profiles overlap

## Phase 3 notes

- Unresolved `derived.audience` → dead-letter queue + alert
- P0/P1: ack required within SLA or escalate
