# Profile Skills Inventory — 2026-09-03

> **Review of the 43 skills available in `/opt/data/profiles/ivan/skills/`**
> vs what was claimed in HANDOFF-PHASE-8.md ("drop unused from 126").

## Headline

- **Actual count**: 43 skills installed (not 126).
- **Profile config**: `enabled_toolsets` / `enabled_skills` field is NOT set.
  Hermes default behavior: all installed skills are loaded.
- **No per-skill cost**: skills load into context, not billed per skill.
- **Real impact**: context bloat, latency. NOT a $-savings target.

## Categories (43 total)

| Category | Count | Examples |
|---|---:|---|
| AIW-internal workflow | ~10 | aiw-local-first-app-tests, aiw-phased-execution, aiw-repo-hardening |
| Meta / productivity | ~8 | commit-before-preamble, verification-before-completion, plan, requesting-code-review |
| Software-development | ~6 | test-driven-development, subagent-driven-development, systematic-debugging |
| Domain-specific | ~5 | mcp-builder, drawio-skill, dispatching-parallel-agents, autonomous-ai-agents |
| Finance | ~3 | excel-author, pptx-author, 3-statement-model |
| Creative | ~3 | architecture-diagram, ascii-art, sketch |
| Email/Messaging | ~3 | himalaya, mcp-builder |
| Git/GitHub | ~3 | git-lfs-overtracking-recovery, github-pr-workflow, github-code-review |
| Other (productivity, docs) | ~2 | nano-pdf, ocr-and-documents |

## Recommendation

**Skip optimization**. The handoff's "drop unused from 126 → ~$1-5/mo savings" framing was based on a wrong count (126 vs 43). Skills don't have a per-load cost.

If profile-skill context bloat is a real concern, the right metric is **per-session latency / context-window pressure**, not spend. That requires per-session tracing which is out of scope for an autonomous session.

**Decision**: leave skills as-is. Move to Track D.

Refs: HANDOFF-PHASE-8.md `## MED` #2, `/opt/data/profiles/ivan/config.yaml`.
