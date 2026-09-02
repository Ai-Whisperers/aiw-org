#!/usr/bin/env python3
"""Build 7 missing Research dept agents in one batch.

Built Phase 7 R6 (gap-closing execution).

Creates PROMPT.md + PROMPT-monitor.md for each:
  5.4  Academic Liaison (T2)
  5.9  Subject Matter Expert (SME) (T2)
  5.10 Research Engineer (T2)
  5.11 IP / Patent Specialist (T3)
  5.12 Publication Coordinator (T2)
  5.13 Research Associate (T2)
  5.8  Instructional Designer (T3)

Idempotent — skips if dir already exists.
"""

import sys
from pathlib import Path

# --- AIW_ROOT path bootstrap (DEMIURGE-098) ---
import sys as _sys_bootstrap_098
from pathlib import Path as _Path_bootstrap_098
_PY_PATHS_ROOT = _Path_bootstrap_098(__file__).resolve().parent.parent
if str(_PY_PATHS_ROOT) not in _sys_bootstrap_098.path:
    _sys_bootstrap_098.path.insert(0, str(_PY_PATHS_ROOT))
from _paths import AGENTS, AIW_ROOT
# --- end bootstrap ---


REPO = AGENTS
RESEARCH_DIR = REPO / "05-research-education"

# Each agent: (name, version, archetype, cluster, hard_stops, mission, composition, transfer_targets, monitor_cadence)
AGENTS = [
    {
        "name": "academic-liaison",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "enable",
        "hard_stops": [
            ("submit_paper", "ivan+kiki"),
            ("withdraw_submission", "ivan+kiki"),
            ("respond_to_reviewer", "ivan"),
            ("accept_review_decision", "ivan+kiki"),
        ],
        "mission": "Bridge between research outputs (thesis chapters, papers) and academic venues (journals, conferences). Own the submission pipeline: venue matching, submission prep, reviewer-response coordination, acceptance tracking. Activates when first paper is queued for submission.",
        "composition": ["thoth-literature-scanner", "peitho-language-quality", "mnemosyne-document-archivist"],
        "transfer_targets": ["05-research-education/research-tracker", "05-research-education/thesis-tracker"],
        "monitor_cadence": "weekly",
    },
    {
        "name": "subject-matter-expert",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "enable",
        "hard_stops": [
            ("publish_external", "ivan+kiki"),
            ("sign_contract", "ivan+kiki"),
            ("accept_payment", "ivan"),
            ("share_pii", "ivan+kiki"),
        ],
        "mission": "Coordinate contracted Subject Matter Experts (SMEs) for course modules and thesis chapters. Maintain bench of available experts per domain (geography, AI coaching, regulatory). Manage SME scoping, contracting, payment, IP rights. Activates when 5+ course modules need external expertise or thesis requires domain expert review.",
        "composition": ["thoth-literature-scanner", "calliope-content-producer"],
        "transfer_targets": ["05-research-education/course-producer", "05-research-education/research-tracker"],
        "monitor_cadence": "monthly",
    },
    {
        "name": "research-engineer",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "build",
        "hard_stops": [
            ("deploy_prod", "ivan"),
            ("modify_eval_golden", "ivan+kiki"),
            ("disable_eval_gate", "ivan+kiki"),
        ],
        "mission": "Build the tooling that research needs: eval harnesses, data pipelines, measurement scripts, statistical models. Own the eval-trending.json computation, citation-coverage-enforcer orchestration, thesis-to-product conversion metrics. Activates when thesis graduates to product or eval coverage needs scaling.",
        "composition": ["thoth-literature-scanner", "mnemosyne-document-archivist", "eval-gate-runner"],
        "transfer_targets": ["05-research-education/research-tracker", "05-research-education/citation-coverage-enforcer"],
        "monitor_cadence": "weekly",
    },
    {
        "name": "ip-patent-specialist",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "enable",
        "hard_stops": [
            ("file_patent", "ivan+kiki"),
            ("sign_ip_assignment", "ivan+kiki"),
            ("publish_ip_disclosure", "ivan+kiki"),
        ],
        "mission": "Own IP/patent/trademark portfolio: filings, renewals, assignments, infringement monitoring. Coordinates with external IP counsel. Activates on first patent trigger or IP disclosure event. Triggers: novel thesis finding with commercial potential, third-party infringement claim.",
        "composition": ["compliance-monitor", "thoth-literature-scanner"],
        "transfer_targets": ["02-finance-legal/legal-counsel", "05-research-education/research-tracker"],
        "monitor_cadence": "monthly",
    },
    {
        "name": "publication-coordinator",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "enable",
        "hard_stops": [
            ("submit_paper", "ivan+kiki"),
            ("withdraw_submission", "ivan+kiki"),
            ("publish_preprint", "ivan"),
            ("set_embargo", "ivan+kiki"),
        ],
        "mission": "End-to-end publication pipeline coordinator: preprint server submissions, journal submissions, conference submissions, embargo management, status tracking, venue matcher. Activates on first submission event. Companion to academic-liaison (this agent owns the system; liaison owns the relationships).",
        "composition": ["thoth-literature-scanner", "mnemosyne-document-archivist"],
        "transfer_targets": ["05-research-education/academic-liaison", "05-research-education/research-tracker"],
        "monitor_cadence": "weekly",
    },
    {
        "name": "research-associate",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "enable",
        "hard_stops": [
            ("write_state", "none"),
            ("read_state", "none"),
            ("publish_external", "ivan+kiki"),
        ],
        "mission": "Support experiments and operational research tasks per MIT career ladder pattern: data collection, experiment execution, lab-notebook maintenance, sample preparation, field-work logistics. Activates when research execution volume exceeds solo-Researcher capacity. Lower-risk than Researcher (5.2); can be hired as FTE before Researcher.",
        "composition": ["thoth-literature-scanner", "hephaestus-document-miner"],
        "transfer_targets": ["05-research-education/research-tracker", "05-research-education/research-engineer"],
        "monitor_cadence": "weekly",
    },
    {
        "name": "instructional-designer",
        "version": "0.1.0",
        "archetype": "specialist",
        "cluster": "enable",
        "hard_stops": [
            ("publish_module", "ivan+kiki"),
            ("modify_curriculum", "ivan+kiki"),
            ("assess_learner", "ivan"),
        ],
        "mission": "Apply pedagogical frameworks (ADDIE, Bloom's taxonomy, constructivism) to course module design. Produce learning objectives, assessments, scaffolds per module. Activates when course scales past 2 modules/week or pedagogical rigor is demanded by clients. Currently T3 deferred — activates with course growth.",
        "composition": ["calliope-content-producer", "orpheus-recordings-agent", "peitho-language-quality"],
        "transfer_targets": ["05-research-education/course-producer", "05-research-education/subject-matter-expert"],
        "monitor_cadence": "monthly",
    },
]


def frontmatter(agent):
    composition_yaml = "\n".join(f"  - {c}" for c in agent["composition"])
    transfer_yaml = "\n".join(f"  - {t}" for t in agent["transfer_targets"])
    hard_stops_yaml = "\n".join(
        f"  - action: {a}\n    require_approval: true\n    approved_human: '{h}'"
        for a, h in agent["hard_stops"]
    )
    return f"""---
name: {agent['name']}
version: {agent['version']}
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: {agent['cluster']}
archetype: {agent['archetype']}
time_scale: {agent['monitor_cadence']}
composition:
{composition_yaml}
transfer_targets:
{transfer_yaml}
---

# {agent['name'].replace('-', ' ').title()} — Research Dept

You are **{agent['name'].replace('-', ' ').title()}**, a specialist in the Research dept.

## Mission

{agent['mission']}

## Inputs

1. State files: `state/research.json`, `state/citation-coverage.json`,
   `state/editorial-calendar.json`
2. Demiurge atomics: {", ".join(agent['composition'])}
3. Cron schedules per `jobs.json`

## Output contract

- Update relevant state file per `schemas/*.schema.json`
- Write brief to `outbox/YYYY-MM-DD.md` per cadence
- Cross-link to upstream/downstream agents via `transfer_targets`

## Hard stops

```yaml
hard_stops:
{hard_stops_yaml}
```

## What this agent does NOT do

- Does NOT modify state files outside the `research.*` schema
- Does NOT bypass hard-stops; all require explicit human approval per
  the approved_human field above
- Does NOT publish externally without Ivan (+ Kiki for high-impact)

## Cadence

**{agent['monitor_cadence']}** — write brief + update state.

## Cross-references

- Charter: `departments/05-research-education.md`
- Methodology: `research/DEPT-RESEARCH-METHODOLOGY.md`
- Peer review: `research/peer-review-process.md`
- Citation discipline: `research/citation-coverage-audit-2026.md`

---

**Built**: 2026-09-01 (Phase 7 R6)
**Status**: Tier-2/3 deferred per ROLES-INVENTORY; activates on trigger.
"""


def monitor_md(agent):
    return f"""# Monitor — {agent['name']}

> Auto-generated monitor wrapper. Phase 7 R6.

## What this monitor checks

Every {agent['monitor_cadence']}:

1. State file updated within last cycle
2. No hard_stop violations in last run
3. transfer_targets: at least one downstream agent contacted
4. Brief written to `outbox/` (if cadence != daily)

## Health indicators

- ✅ Green: state file fresh + brief written + no violations
- 🟡 Yellow: state file stale (2x cadence period)
- 🔴 Red: hard_stop violation OR state missing

## Build info

- Built: Phase 7 R6 (2026-09-01)
- Owner: ai-ops-coordinator
- Topology: stream-aligned
- Cluster: {agent['cluster']}
"""


def build_agent(agent):
    agent_dir = RESEARCH_DIR / agent["name"]
    if agent_dir.exists():
        print(f"  SKIP {agent['name']} (exists)")
        return False

    agent_dir.mkdir(parents=True)
    (agent_dir / "PROMPT.md").write_text(frontmatter(agent))
    (agent_dir / "PROMPT-monitor.md").write_text(monitor_md(agent))
    print(f"  BUILT {agent['name']}/")
    return True


def main():
    built = skipped = 0
    for agent in AGENTS:
        if build_agent(agent):
            built += 1
        else:
            skipped += 1
    print(f"\n{built} built, {skipped} skipped")


if __name__ == "__main__":
    main()