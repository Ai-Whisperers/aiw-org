# DEMIURGE-092: fix-add-max-output-tokens-body-bug

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Fix scripts/add-max-output-tokens.py::extract_frontmatter() to capture and return the body. Un-skip tests/test_add_max_output_tokens.py::test_handles_well_formed_single_block in same commit.

## Acceptance criteria

- [ ] add-max-output-tokens.py: extract_frontmatter returns (prefix, fm_text, suffix, body) -- body captured
- [ ] process_file: writes prefix + new_fm + suffix + body -- body preserved
- [ ] tests/test_add_max_output_tokens.py::test_handles_well_formed_single_block un-skipped, asserts body survives
- [ ] R2 from brief: 'bulk edit to PROMPT.md must assert body preservation and print a line-count diff'

## Deliverables (paths)

- `scripts/add-max-output-tokens.py`
- `tests/test_add_max_output_tokens.py`

## Verification

```bash
# See progress.md for verification output (once started)
```
