# Tracker — DEMIURGE-081

## Phase 1 — Cluster A: Dept attribution

- [x] Fix `sources/knowledge-mgmt/catalog.yaml` — `maintained_by: thoth-literature-scanner`
- [x] Add `knowledge-mgmt` to `thoth-literature-scanner/agent.yaml` departments
- [x] Add `knowledge-mgmt` to `echo-community-scanner/agent.yaml` departments
- [x] Verify Thoth/Echo rows in `departments/knowledge-mgmt/cadences.md` — no action needed (scheduled agents use agent.yaml cron)

## Phase 2 — Cluster B: Source catalog infrastructure

- [x] Create `sources/knowledge-mgmt/community-signals.md`
- [x] Create `sources/knowledge-mgmt/gaps.md`

## Phase 3 — Cluster C: Citation handoff + dispatch rules

- [x] Verify Operations lead agent id (`demiurge/agents/` listing) — `kronos-operations-lead`
- [x] Add `citation-extracted` signal to `departments/knowledge-mgmt/signals.yaml`
- [x] Add `route-document-audience-operations` rule to `demiurge/router/document-dispatch-rules.yaml`
- [x] Update `hephaestus-document-miner/PROMPT.md` citation output row → `citation-extracted` signal

## Phase 4 — Validation

- [x] All acceptance criteria in plan.md checked
- [x] No new signals.yaml entries break existing signal routing
- [x] Thoth/Echo agent.yaml depts consistent across cadences.md
