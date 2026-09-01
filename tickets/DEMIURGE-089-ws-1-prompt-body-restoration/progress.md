# DEMIURGE-089 Progress

- Commit 320ffdc shipped (amended twice) 2026-09-02: fix(prompts): restore 65 PROMPT.md bodies + incident report (WS-1 close-out)
- Bug class identified: extract_frontmatter() never captured body; new script correctly locates closing --- via offset 3+idx+4+nl+1, then captures suffix body from idx
- BEFORE: 4/76 prompts had body >= 20 lines (recovery needed 72 files)
- AFTER: 69/76 prompts have body >= 20 lines (65 restored, 7 unrecoverable stubs remain)
- Live host synced: 4/76 -> 69/76 (matches repo)
- Initial commit 5df06d6 only had script+tests+report; amended to 320ffdc with the 65 PROMPT.md changes (caught via R9-style review of git show --stat)
- 7 unrecoverable: argus-health-monitor, athena-product-discovery-lead, cadmus-lead-enrichment, calliope-content-producer, clio-customer-signal-collector, iris-community-monitor, metis-proposal-drafter (per brief item 3, these were never longer than 9-18 lines in any commit -- intentional stubs, not damage)
- analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md contains full postmortem per brief item 8
