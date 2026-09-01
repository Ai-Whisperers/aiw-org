---

name: themis-document-classifier
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: minutes
transfer_targets:
  - hephaestus-document-miner
  - mnemosyne-document-archivist
max_output_tokens: 800

---

