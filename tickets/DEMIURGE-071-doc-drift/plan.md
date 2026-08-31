# DEMIURGE-071: Fix doc-impl drift — README counts, ORGANIGRAM, ai-safety/operations status

**Sprint**: Phase 1 — Identify + Stabilize
**Size**: 30m
**Owner**: AI

## Objective

Fix three concrete doc-impl mismatches identified in gap analysis. No new features — corrections only.

## Changes

### 1. `README.md` (root)
- Update "16 deptos" → actual count from updated taxonomy
- Update agent count to reflect DEMIURGE active (12) vs legacy total
- Add note distinguishing "active DEMIURGE agents" from "constitution agents"

### 2. `docs/ORGANIGRAM-AND-DETAILED-ANALYSIS.md`
- Update "51 agentes, 18 deptos" header claim
- Mark document as "as-of 2026-08-14 — see ROADMAP-DEPT-EXPANSION.md for current state"

### 3. `docs/demiurge/department-taxonomy-v1.md` (if not handled by DEMIURGE-070)
- Ensure no department has status=active without a `departments/` folder

## Acceptance criteria

- [ ] README agent/dept counts reflect reality (± 2 is acceptable, must not be off by 10+)
- [ ] ORGANIGRAM doc has a staleness notice at the top
- [ ] Zero departments in taxonomy claiming "active" without corresponding folder
