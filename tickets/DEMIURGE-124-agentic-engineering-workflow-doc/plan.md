# DEMIURGE-124: agentic-engineering-workflow-doc

**Sprint**: Phase Kernel
**Size**: 1h
**Owner**: AI

## Objective

Ship `docs/AGENTIC-ENGINEERING-WORKFLOW.md` (~2 pages):
- What AIW's agentic engineering workflow IS (the loop)
- Roles: operator, AI, demiurge, agents
- Sprint lifecycle: ticket → commit → PR → merge → review
- Cron layer: how the AIW fleet runs without operator input
- Kernel extraction interface: how the workflow interfaces with the
  instance-zero → kernel abstraction
- Pointers to existing detailed docs (no duplication)

## Acceptance criteria

- [ ] docs/AGENTIC-ENGINEERING-WORKFLOW.md (~2 pages, 4-6KB)
- [ ] Cites real artifacts (curator-evolver, instinct YAML format, sprint
      output, recent master commits)
- [ ] No duplication of AGENTS.md / OPERATIONS.md / ORCHESTRATION.md
      (this is a READ-FIRST pointer document)
- [ ] pytest + lint still pass (no code changes, only doc)

## Verification

- File exists, content reflects actual AIW state (not generic)
- File references ≥ 3 existing shipped artifacts (commits, scripts, docs)
- File is < 8KB (would otherwise be doing OPERATIONS.md's job)
