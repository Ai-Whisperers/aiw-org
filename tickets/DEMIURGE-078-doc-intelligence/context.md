# Context — DEMIURGE-078

Raised in 2026-08-28/29 planning session.

Key insight from session:
- Every document has attributes — derived (by classifier) or given (by creator)
- Urgency is sometimes only knowable by reading the content → classifier must handle ambiguity
- Documents contain "nuggets" — valuable embedded info, sometimes left deliberately
- The Archivist role was conceptually known but never formalized in the repo
- Meeting recordings are currently transcribed manually (see CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md)
- Language quality is more than spell check — it includes terminology compliance (DEMIURGE-077)

Ivan owns the communication layer (formality, tone, urgency, information types) — DEMIURGE-078 must align with Ivan's communication taxonomy.

Existing agents that partially do this job:
- `thoth-literature-scanner` — mines literature sources (narrow domain)
- `echo-community-scanner` — mines community signals (narrow domain)
- `citation-checker` — legacy, validates citations
- `argus-health-monitor` — reads KPI signals (not documents)

None of these is a general document classifier or archivist.

Existing documents created from recordings (manual):
- `docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md`
- Various research synthesis docs

The Recordings Agent automates what currently requires a human transcription + synthesis session.
