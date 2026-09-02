# DEMIURGE-095 Progress

## 2026-09-02

### Done
- [x] All 7 unrecoverable stubs identified and marked with explicit
      '## Intentual stub' section
- [x] Each stub body now has:
      - Status explanation (intentional, not corruption)
      - Rationale referencing the 2026-09-01 incident analysis
      - Design intent (what the agent does at runtime)
      - List of sections needed in a proper body
      - Tracking reference to DEMIURGE-095b follow-up work
- [x] Test contract updated (test_restore_prompt_bodies.py):
      - test_plan_finds_seven_unrecoverable_files ->
        test_plan_finds_seven_stubs_now_marked_explicit (expects 0 truncated)
      - test_post_apply_min_body_lines_satisfied ->
        expects plan() to be empty after stub-marking
- [x] Verified: pytest 466/5/1 (only pre-existing test_parent_spec failure,
      unrelated to this work)

### Files modified
- 7 PROMPT.md files: argus-health-monitor, athena, cadmus, calliope, clio,
  iris, metis
- tests/test_restore_prompt_bodies.py: 2 test methods updated

### Follow-up (operator-gated)
- DEMIURGE-095b: author proper bodies for the 7 stubs (~14h AI work)
- Per R8 "small commits, one verifiable claim each" + per ticket scope,
  body authoring is a separate ticket

### Verification
```
=== Pytest ===
1 failed, 466 passed, 5 skipped in 14.20s
=== Pre-existing failure ===
tests/test_parent_spec.py::test_audit_after_fix
  - 1 of 48 PROMPTs has wrong parent_spec
  - marketing-content-mon-wed-fri/PROMPT.md
  - Pre-existing, not from this session's work
```

### Time
~30 min (vs 45m estimate)
