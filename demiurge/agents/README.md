# DEMIURGE agents index

| id | name | dept | repo |
|----|------|------|------|
| thoth-literature-scanner | Thoth | cross | aiw-agent-thoth-literature-scanner |
| echo-community-scanner | Echo | cross | aiw-agent-echo-community-scanner |
| hera-marketing-lead | Hera | marketing | aiw-agent-hera-marketing-lead |
| calliope-content-producer | Calliope | marketing | aiw-agent-calliope-content-producer |
| iris-community-monitor | Iris | marketing | aiw-agent-iris-community-monitor |
| apollo-sales-lead | Apollo | sales | aiw-agent-apollo-sales-lead |
| cadmus-lead-enrichment | Cadmus | sales | aiw-agent-cadmus-lead-enrichment |
| metis-proposal-drafter | Metis | sales | aiw-agent-metis-proposal-drafter |
| athena-product-discovery-lead | Athena | product-discovery | aiw-agent-athena-product-discovery-lead |
| clio-customer-signal-collector | Clio | product-discovery | aiw-agent-clio-customer-signal-collector |
| kronos-operations-lead | Kronos | operations | aiw-agent-kronos-operations-lead |
| management-coordinator | Mgmt Coordinator | operations | aiw-agent-management-coordinator |
| business-analyst | Business Analyst | operations | aiw-agent-business-analyst |
| bizops-tracker | BizOps Tracker | operations | aiw-agent-bizops-tracker |
| ai-ops-coordinator | AI Ops Coordinator | ai-ops | aiw-agent-ai-ops-coordinator |
| compliance-monitor | Compliance Monitor | compliance | aiw-agent-compliance-monitor |
| hermes-router-revenue | Hermes | router | aiw-agent-hermes-router-revenue |
| argus-health-monitor | Argus | monitor | aiw-agent-argus-health-monitor |
| themis-document-classifier | Themis | knowledge-mgmt | aiw-agent-themis-document-classifier |
| mnemosyne-document-archivist | Mnemosyne | knowledge-mgmt | aiw-agent-mnemosyne-document-archivist |
| hephaestus-document-miner | Hephaestus | knowledge-mgmt | aiw-agent-hephaestus-document-miner |
| pheme-document-router | Pheme | knowledge-mgmt | aiw-agent-pheme-document-router |
| peitho-language-quality | Peitho | knowledge-mgmt | aiw-agent-peitho-language-quality |
| orpheus-recordings-agent | Orpheus | knowledge-mgmt | aiw-agent-orpheus-recordings-agent |

Souls: `demiurge/agents/<id>/PROMPT.md`  
Manifests: `repo-manifest.yaml` (GitHub org `Ai-Whisperers`)

Document Intelligence pipeline: Orpheus → Themis → (Mnemosyne, Hephaestus, Peitho) → quality-assessed → Pheme
