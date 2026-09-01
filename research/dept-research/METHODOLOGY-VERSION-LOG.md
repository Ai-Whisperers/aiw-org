# Research Methodology Version Log

> **Started:** 2026-09-01
> **Maintainer:** research-engineer

## Versions

### v1.1 (Phase 9 R3 / 2026-09-01)
- Citation-coverage-enforcer schema now applies to all research outputs
- Knowledge synthesizer produces weekly synthesis docs (WEEKLY-SYNTHESIS-{ISO-WEEK}.md)
- Cross-dept research request bus: `scripts/research-request-bus.py`
- Dedupe script: `scripts/dedupe-research-corpus.py`

### v1.0 (Phase 8 R5 / 2026-08-25)
- Literature scan cron: weekly Tuesday 08:00 UTC
- Source-materials-scorer: tier-1/tier-2/tier-3 source authority
- Citation coverage threshold: ≥1 inline citation per file

## Active Methodology Decisions

- Each research file MUST have ≥1 inline citation (citation-coverage-enforcer)
- Tier-1 sources: peer-reviewed journals, primary research
- Tier-2 sources: industry reports, established journalism
- Tier-3 sources: blog posts, social media (use sparingly, flag with citation)
- Synthesis cadence: weekly (Sunday 23:00 UTC)
- Cross-dept requests: signal queue at /opt/data/state/research-requests.ndjson

## Outstanding Methodology Questions

- Q1: Should tier-3 sources be allowed in synthesis docs? Currently allowed but flagged.
- Q2: When does a research file "graduate" from research/ to canon/? (Not yet defined)
- Q3: How do we handle conflicting sources? (Currently picks most recent)
