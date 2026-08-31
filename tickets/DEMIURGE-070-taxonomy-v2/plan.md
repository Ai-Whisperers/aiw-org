# DEMIURGE-070: Update department taxonomy — add missing depts + fix status drift

**Sprint**: Phase 1 — Identify + Stabilize
**Size**: 45m
**Owner**: AI

## Objective

Bring `docs/demiurge/department-taxonomy-v1.md` to v2 as the single authoritative list of all departments. Add 7 New departments identified in the 2026-08-28 gap analysis. Promote 6 Partial stubs. Fix status drift for `ai-safety` and `operations`.

## Changes

### Add to Tier 2 (activate at lower trigger than Tier 3):
- `executive-office` — CEO office, board mgmt, CoS
- `it-enterprise` — internal IT, helpdesk, enterprise SaaS stack
- `business-development` — strategic partnerships, channels, alliances
- `cybersecurity` — InfoSec, traditional security ops (separate from ai-safety)
- `design-creative` — UX, brand design, content design
- `corporate-communications` — PR, media, internal comms

### Add to Tier 3 (on trigger):
- `pmo` — Program Management Office (trigger: >8 active depts)
- `field-services` — Professional Services / Implementation (trigger: first enterprise client)
- `data-science` — standalone Data Science (trigger: data volume justifies dedicated team)
- `customer-experience` — CX design, VoC, NPS (trigger: 10+ recurring clients)

### Fix status:
- `operations`: change "active" → "skeleton" (no `departments/` folder exists yet)
- `ai-safety`: change "active (partial)" → "skeleton" (same reason)

### Restore from org-original (were in original-20, dropped without record):
- `multimedia` — add back as Tier 2 skeleton (agent `multimedia-producer.md` already exists)
- `board` — add as special governance node (not a standard dept — note the distinction)

### Promote partial stub (6th of 6):
- `product-management` — Tier 3 skeleton (trigger: >3 parallel roadmap tracks; separate from Product Discovery)

## Acceptance criteria

- [x] `department-taxonomy-v1.md` contains all departments with accurate status
- [x] No department has status "active" without a corresponding `departments/<id>/` folder
- [x] New departments have at least: id, name, status=skeleton, activation trigger
- [x] File renamed to `department-taxonomy-v2.md` or version bump noted in header
