# PHASE-8-COMPLETE.md

> Phase 8 finished. Constitution + 6 dept specs + deferred docs all at v0.2.0.

---

## Phase 8 — DONE ✅

**Goal**: Constitution v0.2.0 + 6 dept specs + deferred docs.

### Files modified

- `/opt/data/agents/departments/01-operations.md` (v0.1.0 → v0.2.0)
- `/opt/data/agents/departments/02-finance-legal.md` (v0.1.0 → v0.2.0)
- `/opt/data/agents/departments/03-sales-growth.md` (v0.1.0 → v0.2.0)
- `/opt/data/agents/departments/04-engineering-delivery.md` (v0.1.0 → v0.2.0)
- `/opt/data/agents/departments/05-research-education.md` (v0.1.0 → v0.2.0)
- `/opt/data/agents/departments/06-people-culture.md` (v0.1.0 → v0.2.0)
- `/opt/data/agents/departments/ORG-AGENTS.md` (v0.1.0 → v0.2.0, with Appendices A-G)

### Files added

- `/opt/data/agents/DEFERRED-ROLES.md` (Tier 2/3/4 roles with triggers)
- `/opt/data/agents/DEFERRED-AGENTS.md` (deferred agent candidates)
- `/opt/data/agents/ON-CALL.md` (Ivan primary, Kiki backup)
- `/opt/data/agents/REVIEW-2026-Q4.md` (30/60/90-day checklist)
- `/opt/data/agents-v2/BURNOUT-SIGNAL-SPEC.md` (founder-bandwidth-watchdog spec)

### Backup

- `/opt/data/agents/departments/archive/ORG-AGENTS-v0.1.0-2026-08-13.md` (pre-bump)

### Verification

- All 7 dept specs include: Sub-roles, Sub-agents, Tooling/SOPs, Escalation triggers, Storage, Cross-references, CHANGELOG
- Constitution includes: Appendices A-G (cross-cutting, deferred, storage, patterns, decisions, rituals, on-call)
- DEFERRED-ROLES: covers Tier 2/3/4 roles
- DEFERRED-AGENTS: covers Tier 3 agent candidates

### Phase 9 — READY TO START

**Goal**: Operational disciplines + self-running milestone.

### Tasks queued

- 9A: Model fallbacks (verify all 7 lead agents have fallback_model field)
- 9A: Secret-leak-check.sh (pre-commit hook)
- 9B: Security review (7-agent side-effect audit)
- 9B: Load test (7 agents firing simultaneously)
- 9B: Chaos test scenarios (3 from FAILURE-MODES.md)
- 9C: Self-running milestone definition + check

### Expected effort

20-30 turns, 2-3 sessions.

---

**Document path**: `/opt/data/agents-v2/PHASE-8-COMPLETE.md`
**Status**: Phase 8 COMPLETE
**Next phase**: Phase 9 (operational disciplines)
**Last updated**: 2026-08-14
