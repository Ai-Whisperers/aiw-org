---

name: pheme-document-router
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: minutes
composition:
  - themis-document-classifier
transfer_targets:
  - hephaestus-document-miner
  - mnemosyne-document-archivist
max_output_tokens: 800

---

