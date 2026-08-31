# Agent Naming Conventions

> DEMIURGE-012

## Rules

1. **One memorable name per agent** — mythological or archetypal (Greek, Roman, Egyptian, etc.)
2. **`id`** = `{name-lowercase}-{role-slug}` e.g. `hera-marketing-lead`
3. **`display_name`** = `{Name} — {Role Title}` e.g. `Hera — Head of Marketing`
4. Name persists across role changes; update `roles[]` not `name`
5. Router agent for revenue stack: **Hermes** (messenger god) — distinct from Sales lead naming

## Archetype → name pool

| Archetype | Example names | Use for |
|-----------|---------------|---------|
| Strategist | Athena, Odin, Solomon | Leads, product discovery |
| Builder | Vulcan, Hephaestus, Ptah | Engineering, content |
| Watchdog | Argus, Cerberus, Anubis | Security, health monitor |
| Curator | Thoth, Clio, Saraswati | Research, literature scanner |
| Connector | Hermes, Iris, Mercury | Sales, routing, community |
| Analyst | Metis, Janus, Themis | Enrichment, RevOps |
| Coach | Chiron, Sophia | People, coaching |

## Revenue stack assignments

| Agent | Name | Role | Archetype |
|-------|------|------|-----------|
| marketing-lead | Hera | Head of Marketing | Strategist |
| content-producer | Calliope | Content Producer | Builder |
| community-monitor | Iris | Community Monitor | Connector |
| sales-lead | Apollo | Head of Sales | Connector |
| lead-enrichment | Cadmus | Lead Enrichment | Analyst |
| proposal-drafter | Metis | Proposal Drafter | Analyst |
| product-discovery-lead | Athena | Head of Product Discovery | Strategist |
| customer-signal-collector | Clio | Customer Signal Collector | Curator |
| literature-scanner | Thoth | Literature Scanner | Curator |
| community-scanner | Echo | Community Scanner | Curator |
| health-monitor | Argus | Department Health Monitor | Watchdog |
| router | Hermes | Signal Router | Connector |

> **Note**: Sales lead uses Apollo (light/truth/oracles) to avoid collision with Router Hermes.

## Operations stack assignments

| Agent | Name | Role | Archetype |
|-------|------|------|-----------|
| ops-lead | Kronos | Head of Operations | Strategist |

> **Note**: Kronos (time/order) is the Operations dept lead; inbound ops signals route via Hermes (DEMIURGE-076).

## Knowledge Management (document-intelligence) assignments

| Agent | Name | Role | Archetype |
|-------|------|------|-----------|
| document-classifier | Themis | Document Classifier | Analyst |
| document-archivist | Mnemosyne | Document Archivist | Curator |
| document-miner | Hephaestus | Document Miner | Builder |
| document-router | Pheme | Document Router | Connector |
| language-quality | Peitho | Language Quality | Analyst |
| recordings | Orpheus | Recordings Agent | Builder |

> **Note**: Pheme routes document envelopes; Hermes routes inter-dept revenue and operations signals. Handoff via cross-dept signals when mined assets target revenue stack.

## Git repo naming

```
github.com/Ai-Whisperers/aiw-agent-{agent-id}
```

Example: `aiw-agent-hera-marketing-lead`

## Soul version bumps

Increment `Soul.version` patch when:
- hard_stops change
- values[] change
- prompt_ref major rewrite

Increment minor when archetype or primary mission changes (requires review ticket).
