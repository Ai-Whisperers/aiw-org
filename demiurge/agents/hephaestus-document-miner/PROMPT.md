---

name: hephaestus-document-miner
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: minutes
composition:
  - pheme-document-router
  - themis-document-classifier
max_output_tokens: 800

---

