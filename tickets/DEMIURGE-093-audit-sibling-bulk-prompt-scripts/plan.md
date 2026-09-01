# DEMIURGE-093: audit-sibling-bulk-prompt-scripts

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

For each bulk-prompt script in scripts/, audit for the body-preservation bug. Document finding per script. Fix any that have the bug in the same patch.

## Acceptance criteria

- [ ] scripts/fix-parent-spec.py audit completed
- [ ] scripts/add-cluster-field.py audit completed
- [ ] Any other bulk-frontmatter script (per find) audit completed
- [ ] Each script: per-file audit docs/scripts/SIBLING-SCRIPT-AUDIT.md + fix if buggy

## Deliverables (paths)

- `docs/scripts/SIBLING-SCRIPT-AUDIT.md`

## Verification

```bash
# See progress.md for verification output (once started)
```
