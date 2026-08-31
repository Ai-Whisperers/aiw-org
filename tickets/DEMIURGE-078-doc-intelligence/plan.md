# DEMIURGE-078: Document Intelligence System — classifier, attributes, routing, mining, quality, recordings

**Sprint**: Phase 1 — Identify + Stabilize (design) / Phase 3 — Meta-Agent Framework (build)
**Size**: 120m (design) + implementation per sub-agent
**Owner**: AI + Ivan (communication layer)
**Depends on**: DEMIURGE-077 (vocabulary must exist before classifiers can classify)

## Objective

Design and skeleton the Document Intelligence System — the layer that processes every document in the org to determine what it is, who it's for, how urgent it is, what it contains, and where it goes. Currently this is done manually or not at all.

## The core problem

Every document entering or created within the org has implicit attributes:
- **Who is it for?** (this agent, this dept, broadcast, human only)
- **How urgent is it?** (sometimes you must read it to know)
- **What type is it?** (plan, report, signal, transcript, research, spec, etc.)
- **What's in it?** (decisions, action items, references, nuggets)
- **What quality is it?** (language quality, terminology compliance, completeness)

Without a classification layer, agents receive everything and filter nothing. With it, each agent only sees what's relevant to it.

## Sub-agents in this system

### 1. Document Classifier
**What it does**: Reads an incoming document and assigns all standard attributes.

Attributes it assigns:
```yaml
document_type: plan | report | signal | transcript | research | spec | communication | recording
urgency: P0 | P1 | P2 | P3
audience:
  - agent-id or dept-id or role or broadcast or human-only
formality: formal | semi-formal | informal
tone: directive | advisory | informational | confirmatory
routing_tags: [list]
derived:
  has_action_items: bool
  has_decisions: bool
  has_nuggets: bool     # valuable embedded info, sometimes intentional
  requires_human: bool
```

**Note**: Urgency is sometimes only determinable by reading content — the classifier must handle the "unknown until read" case.

### 2. Document Router
**What it does**: Takes the classifier's output and delivers the document to the right agents/depts.

Rules:
- Routes based on `audience` + `routing_tags`
- P0/P1 urgency triggers immediate delivery + acknowledgment required
- P2/P3 goes to scheduled queue
- `requires_human` routes to human-readable output (WhatsApp, email)

### 3. Document Cataloger / Archivist
**What it does**: Maintains the master index of all documents with their classified attributes.

**The Archivist** is the agent holding this role. Not just storage — active cataloging:
- Tags documents by topic, source, date, type, dept
- Maintains relationships between documents (this plan → these tickets → these outputs)
- Enables retrieval: "what decisions were made about X?" or "what did we say about Y?"

**Nuggets**: Documents contain embedded valuable information — sometimes deliberately placed, sometimes incidental. The Archivist flags these for the Miner.

### 4. Document Miner
**What it does**: Extracts structured assets from documents.

Assets it mines:
- Action items → create tickets or signals
- Decisions → log to decision register
- References / citations → forward to Thoth (literature scanner)
- Nuggets → flag to relevant dept or agent
- New terminology → flag to DEMIURGE-077 terms registry

The "nuggets left on purpose" use case: if Ivan writes a document and deliberately embeds a strategic insight, the Miner surfaces it to the right agent without Ivan having to manually route it.

### 5. Language Quality Agent
**What it does**: Spell check + more. Specifically:

- Spelling and grammar (basic)
- Tone consistency with stated audience/formality
- Terminology compliance — is the document using terms as defined in DEMIURGE-077?
- Clarity score (readability for the target audience)
- Completeness check (does a plan have all required sections?)

**Not a blocker** — quality issues produce a quality report, not a rejection. Unless the document is a formal external communication (then P1 quality gate).

### 6. Recordings Agent
**What it does**: Handles audio/video recordings (meetings, voice notes, interviews).

Pipeline:
1. Receive recording (file or stream link)
2. Transcribe → structured transcript
3. Run Classifier on transcript → assign all document attributes
4. Run Miner on transcript → extract decisions, action items, nuggets
5. Route structured outputs to appropriate agents/depts
6. Archive original + transcript + extracted assets

**Existing analog**: `CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md` was manually created from a meeting transcript. Recordings Agent automates this entirely.

## Department placement

All 6 sub-agents live under **Knowledge Management** dept as a sub-system called `document-intelligence`.

```
knowledge-mgmt/
└── document-intelligence/
    ├── classifier/
    ├── router/
    ├── archivist/
    ├── miner/
    ├── language-quality/
    └── recordings/
```

## Phase 1 deliverable (this ticket)

Design only — no implementation yet:
1. Document attribute schema (YAML)
2. Sub-agent list with roles defined
3. Department placement confirmed
4. Dependency map (077 → 078 → all other depts)

## Phase 3 deliverable (implementation)

One sub-agent per session, starting with:
1. Classifier (enables everything else)
2. Archivist (enables retrieval)
3. Miner (enables nugget surfacing)
4. Router (enables automated delivery)
5. Language Quality
6. Recordings

## Acceptance criteria (Phase 1 / design)

- [ ] Document attribute schema defined in `docs/demiurge/schemas/document.md`
- [ ] All 6 sub-agents listed in `departments/knowledge-mgmt/document-intelligence/` skeleton
- [ ] Dependency on DEMIURGE-077 documented (classifier needs vocabulary)
- [ ] Existing manual analog identified for each sub-agent (what human/process currently does this job)
- [ ] `TERMS.md` (DEMIURGE-077) updated with document intelligence vocabulary
