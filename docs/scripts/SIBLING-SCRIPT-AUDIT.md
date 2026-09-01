# Sibling bulk-frontmatter script audit

> **Audit date**: 2026-09-02
> **Trigger**: DEMIURGE-093 (per Phase Kernel brief WS-1 item 5)
> **Prompt**: "Audit the sibling scripts (`fix-parent-spec.py`,
> `add-cluster-field.py`, and any other bulk-frontmatter tool) for the
> same defect."

## The defect in question

`scripts/add-max-output-tokens.py::process_file()` wrote
`prefix + new_fm + suffix` to disk, but never captured or wrote the body.
This silently destroyed 72 of 76 PROMPT.md bodies at commit `fffd7c4`.

The bug class: **bulk-frontmatter scripts that read the file, mutate
only the YAML, and write back without preserving everything else**.

## Audited scripts

### 1. `scripts/add-max-output-tokens.py` — BUG, FIXED in DEMIURGE-092

- Original 3-tuple return: `(prefix, fm_text, suffix)` — body discarded
- Fixed 4-tuple return: `(prefix, fm_text, suffix, body)`
- `process_file()` now writes all 4 fields
- Status: **fixed**, tests added, regression test un-skipped

### 2. `scripts/fix-parent-spec.py` — OK (body-safe)

```python
# From the script's actual logic:
new_content = update_parent_spec(content, expected)
p.write_text(new_content)
```

`update_parent_spec()` is a regex-based substitute within the frontmatter
itself. It does NOT touch the body. **Verified by inspection** that the
content regex targets only the frontmatter block (via `^parent_spec:`
MULTILINE), and `content` is the full file passed unchanged.

- Status: **safe**, no changes needed

### 3. `scripts/add-cluster-field.py` — OK (body-safe, explicit comment)

```python
# From the actual script (lines around `add_cluster_field`):
end = text.find("---", 3)
frontmatter = text[3:end]
rest = text[end:]  # everything from the closing --- onward
```

The script **explicitly preserves** `rest = text[end:]` (the body) and
includes it in the reconstructed file as `new_text = "---" + new_
frontmatter + rest`. **Verified by inspection** that body is preserved.

- Status: **safe**, no changes needed. Code already followed the correct
  pattern (which DEMIURGE-092's fix is now adopting for
  add-max-output-tokens.py).

### 4. `scripts/repair-prompts-after-cluster-add.py` — OK (remediation)

This is a remediation script that repairs the separate newline bug in
add-cluster-field.py (lost newline before closing `---`). It is itself
body-safe because it uses regex sub on the raw content without
reconstructing from parts. **Verified by inspection**.

- Status: **safe**, no changes needed

## Summary

Of 4 bulk-prompt scripts in repo:
- 1 had the body-destruction bug: `add-max-output-tokens.py` (FIXED per DEMIURGE-092)
- 3 are body-safe by design or by explicit handling: the others

## Process recommendation

For future bulk-prompt scripts (DEMIURGE-103 kernel extraction, future
saskia work):
- Use the 4-tuple signature: `(prefix, fm_text, suffix, body)`
- Write all 4 fields on disk
- Add a regression test that asserts lossless round-trip
- Per R2 from the Phase Kernel brief: any bulk edit to PROMPT.md must
  assert body preservation and print a line-count diff before committing

## Audit sign-off

- Date: 2026-09-02
- Audited by: AI session running the Phase Kernel brief execution
- Method: code reading of each script + verification of preservation
  semantics at the regex level
- Verification: DEMIURGE-092 closing the source bug
