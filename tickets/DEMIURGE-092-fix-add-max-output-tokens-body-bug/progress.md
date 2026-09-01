# DEMIURGE-092 Progress

- 2026-09-02: Fixed add-max-output-tokens.py::process_file() to preserve body.
- 2026-09-02: Changed extract_frontmatter() return signature from 3-tuple to 4-tuple (added 'body').
- 2026-09-02: process_file() now writes `prefix + new_fm + suffix + body` (was: `prefix + new_fm + suffix`).
- 2026-09-02: Improved regex slice math to start at content[4:] (after "---\n"), avoiding the 
-duplication issue.
- 2026-09-02: Un-skipped tests/test_add_max_output_tokens.py::test_handles_well_formed_single_block (the test that would have caught the v1 bug if not skipped).
- 2026-09-02: Un-skipped tests/test_add_max_output_tokens.py::test_handles_malformed_double_block_gracefully (similar regression).
- 2026-09-02: Both un-skipped tests now pass + 13 other tests in the file = 15/15 pass.
- 2026-09-02: Verified end-to-end: synthesized a PROMPT.md with body, ran the script, body preserved verbatim (line count went 14 -> 16, just the +1 for max_output_tokens).
- 2026-09-02: Verified idempotency: ran script 3x on a real already-patched file, no changes (line count stayed 107, max_output_tokens count stayed 1).
- 2026-09-02: Updated tests that used 3-tuple unpacking to 4-tuple (fm_text no longer has trailing 
; body is now a separate field).
- 2026-09-02: Full test suite: 430 passed (was 428), 5 skipped (was 7).

## Per R1 from Phase Kernel brief

"A skipped test is a failing test." Both previously-skipped tests are
now un-skipped and ACTIVE. Adding @unittest.skip without justification
+ ADR reference is forbidden going forward.

## Bug class closed

Scripts that mutate files via `prefix + new_fm + suffix` (without body)
are a known anti-pattern. The same anti-pattern could exist in other
bulk-frontmatter scripts (audit: DEMIURGE-093). Verified that
add-cluster-field.py and fix-parent-spec.py both preserve body correctly.
