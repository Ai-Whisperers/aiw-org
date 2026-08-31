# Knowledge Management cadences (Hermes cron registration)

> DEMIURGE-078

| hermes_cron_id | agent | schedule | PYT | type |
|----------------|-------|----------|-----|------|
| demiurge-themis-classifier | themis-document-classifier | on_signal | — | document-ingest, transcript-ready |
| demiurge-mnemosyne-archivist | mnemosyne-document-archivist | on_signal | — | document-classified |
| demiurge-hephaestus-miner | hephaestus-document-miner | on_signal | — | document-classified |
| demiurge-peitho-quality | peitho-language-quality | on_signal | — | document-classified |
| demiurge-pheme-router | pheme-document-router | */5 6-22 * * * | every 5m 06:00–22:00 | queue drain + on_signal |
| demiurge-orpheus-recordings | orpheus-recordings-agent | on_signal | — | recording-upload |

Register via `hermes cron add` when runtime available. Mirror to `cron-jobs-snapshot` on commit.

Pipeline order on ingest: **Orpheus** (if recording) → **Themis** → parallel **Mnemosyne**, **Hephaestus**, **Peitho** → **Peitho emits quality-assessed** → **Pheme**.
