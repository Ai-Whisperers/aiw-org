# DEMIURGE-093 Progress

- 2026-09-02: Audited 4 bulk-frontmatter scripts (add-max-output-tokens, fix-parent-spec, add-cluster-field, repair-prompts-after-cluster-add).
- 2026-09-02: Found 1 buggy script (add-max-output-tokens.py) which had the body-destruction defect.
- 2026-09-02: DEMIURGE-092 fixes that script (extract_frontmatter now 4-tuple, process_file writes body).
- 2026-09-02: Audited the other 3 scripts: all preserve body via different mechanisms (regex sub on raw content, explicit rest preservation, regex sub for remediation).
- 2026-09-02: Wrote docs/scripts/SIBLING-SCRIPT-AUDIT.md with the per-script findings, the audit method, and a process recommendation for future scripts.
