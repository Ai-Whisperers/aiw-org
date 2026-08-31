#!/usr/bin/env python3
"""Create epic/DEMIURGE and per-ticket commits on feature/DEMIURGE-NNN branches."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EPIC_BRANCH = "epic/DEMIURGE"

# ticket_id -> list of paths relative to repo root (files or dirs)
COMMITS: list[tuple[str, str, list[str]]] = [
    ("001", "DEMIURGE-001: define Agent and Soul schemas", [
        "docs/demiurge/schemas/agent-soul.md",
        "tickets/DEMIURGE-001",
    ]),
    ("002", "DEMIURGE-002: define Memory layers and artifact schemas", [
        "docs/demiurge/schemas/memory.md",
        "docs/demiurge/schemas/artifacts.md",
        "docs/demiurge/schemas/community-memory.md",
        "tickets/DEMIURGE-002",
    ]),
    ("003", "DEMIURGE-003: define Role and Department schemas", [
        "docs/demiurge/schemas/role-department.md",
        "tickets/DEMIURGE-003",
    ]),
    ("004", "DEMIURGE-004: define Signal and Channel schemas", [
        "docs/demiurge/schemas/signal-channel.md",
        "tickets/DEMIURGE-004",
    ]),
    ("005", "DEMIURGE-005: define Router and Quorum schemas", [
        "docs/demiurge/schemas/router-quorum.md",
        "tickets/DEMIURGE-005",
    ]),
    ("006", "DEMIURGE-006: define Source and SourceCatalog schemas", [
        "docs/demiurge/schemas/source-catalog.md",
        "tickets/DEMIURGE-006",
    ]),
    ("007", "DEMIURGE-007: define FeedbackLoop KPI and Cadence schemas", [
        "docs/demiurge/schemas/feedback-kpi-cadence.md",
        "docs/demiurge/domain-model.md",
        "tickets/DEMIURGE-007",
    ]),
    ("008", "DEMIURGE-008: domain model review gate", [
        "docs/demiurge/REVIEW-domain-model.md",
        "tickets/DEMIURGE-008",
    ]),
    ("009", "DEMIURGE-009: DEMIURGE architecture and folder structure", [
        "docs/demiurge/architecture.md",
        "docs/demiurge/README.md",
        "demiurge/README.md",
        "community/README.md",
        "tickets/DEMIURGE-009",
    ]),
    ("010", "DEMIURGE-010: tickets folder and conventions", [
        "tickets/README.md",
        "tickets/INDEX.md",
        "scripts/demiurge/generate-tickets.py",
        "tickets/DEMIURGE-010",
    ]),
    ("011", "DEMIURGE-011: department taxonomy v1", [
        "docs/demiurge/department-taxonomy-v1.md",
        "tickets/DEMIURGE-011",
    ]),
    ("012", "DEMIURGE-012: agent naming conventions", [
        "docs/demiurge/naming-conventions.md",
        "tickets/DEMIURGE-012",
    ]),
    ("013", "DEMIURGE-013: Router agent design spec", [
        "docs/demiurge/router-design.md",
        "tickets/DEMIURGE-013",
    ]),
    ("014", "DEMIURGE-014: formalize DEMIURGE feature list", [
        "docs/demiurge/feature-list.md",
        "tickets/DEMIURGE-014",
    ]),
    ("015", "DEMIURGE-015: Sprint 1 review gate", [
        "docs/demiurge/REVIEW-sprint-1.md",
        "docs/demiurge/SPRINT-0-COMPLETE.md",
        "docs/demiurge/SPRINT-1-COMPLETE.md",
        "tickets/DEMIURGE-015",
    ]),
    ("016", "DEMIURGE-016: Marketing source research seed", [
        "sources/marketing/catalog.yaml",
        "tickets/DEMIURGE-016",
    ]),
    ("017", "DEMIURGE-017: Sales source research seed", [
        "sources/sales/catalog.yaml",
        "tickets/DEMIURGE-017",
    ]),
    ("018", "DEMIURGE-018: Product Discovery source research seed", [
        "sources/product-discovery/catalog.yaml",
        "tickets/DEMIURGE-018",
    ]),
    ("019", "DEMIURGE-019: Marketing source catalog", [
        "tickets/DEMIURGE-019",
    ]),
    ("020", "DEMIURGE-020: Sales source catalog", [
        "tickets/DEMIURGE-020",
    ]),
    ("021", "DEMIURGE-021: Product Discovery source catalog", [
        "tickets/DEMIURGE-021",
    ]),
    ("022", "DEMIURGE-022: Thoth literature scanner soul", [
        "demiurge/agents/thoth-literature-scanner",
        "tickets/DEMIURGE-022",
    ]),
    ("023", "DEMIURGE-023: Echo community scanner soul", [
        "demiurge/agents/echo-community-scanner",
        "tickets/DEMIURGE-023",
    ]),
    ("024", "DEMIURGE-024: Marketing literature gap analysis", [
        "sources/marketing/gaps.md",
        "sources/marketing/community-signals.md",
        "tickets/DEMIURGE-024",
    ]),
    ("025", "DEMIURGE-025: Sales and PD gap analysis", [
        "sources/sales/gaps.md",
        "sources/sales/community-signals.md",
        "sources/product-discovery/gaps.md",
        "sources/product-discovery/community-signals.md",
        "tickets/DEMIURGE-025",
    ]),
    ("026", "DEMIURGE-026: Marketing role inventory", [
        "departments/marketing/department.md",
        "tickets/DEMIURGE-026",
    ]),
    ("027", "DEMIURGE-027: Hera marketing lead soul", [
        "demiurge/agents/hera-marketing-lead",
        "tickets/DEMIURGE-027",
    ]),
    ("028", "DEMIURGE-028: Calliope content producer soul", [
        "demiurge/agents/calliope-content-producer",
        "tickets/DEMIURGE-028",
    ]),
    ("029", "DEMIURGE-029: Iris community monitor soul", [
        "demiurge/agents/iris-community-monitor",
        "tickets/DEMIURGE-029",
    ]),
    ("030", "DEMIURGE-030: Marketing agent repo manifests", [
        "tickets/DEMIURGE-030",
    ]),
    ("031", "DEMIURGE-031: Marketing cadences and router wiring", [
        "departments/marketing/cadences.md",
        "departments/marketing/signals.yaml",
        "tickets/DEMIURGE-031",
    ]),
    ("032", "DEMIURGE-032: Marketing to Sales outbound signals", [
        "demiurge/router/revenue-signals.yaml",
        "tickets/DEMIURGE-032",
    ]),
    ("033", "DEMIURGE-033: Marketing dept activation review", [
        "departments/marketing/REVIEW.md",
        "docs/demiurge/REVIEW-departments.md",
        "tickets/DEMIURGE-033",
    ]),
    ("034", "DEMIURGE-034: Sales role inventory", [
        "departments/sales/department.md",
        "tickets/DEMIURGE-034",
    ]),
    ("035", "DEMIURGE-035: Apollo sales lead soul", [
        "demiurge/agents/apollo-sales-lead",
        "tickets/DEMIURGE-035",
    ]),
    ("036", "DEMIURGE-036: Cadmus lead enrichment soul", [
        "demiurge/agents/cadmus-lead-enrichment",
        "tickets/DEMIURGE-036",
    ]),
    ("037", "DEMIURGE-037: Metis proposal drafter soul", [
        "demiurge/agents/metis-proposal-drafter",
        "tickets/DEMIURGE-037",
    ]),
    ("038", "DEMIURGE-038: Sales agent repo manifests", [
        "tickets/DEMIURGE-038",
    ]),
    ("039", "DEMIURGE-039: Sales cadences and router wiring", [
        "departments/sales/cadences.md",
        "departments/sales/signals.yaml",
        "demiurge/router/dispatch-rules.yaml",
        "tickets/DEMIURGE-039",
    ]),
    ("040", "DEMIURGE-040: Sales to Marketing feedback signal", [
        "tickets/DEMIURGE-040",
    ]),
    ("041", "DEMIURGE-041: Sales dept activation review", [
        "departments/sales/REVIEW.md",
        "tickets/DEMIURGE-041",
    ]),
    ("042", "DEMIURGE-042: Product Discovery role inventory", [
        "departments/product-discovery/department.md",
        "tickets/DEMIURGE-042",
    ]),
    ("043", "DEMIURGE-043: Athena product discovery lead soul", [
        "demiurge/agents/athena-product-discovery-lead",
        "tickets/DEMIURGE-043",
    ]),
    ("044", "DEMIURGE-044: Clio customer signal collector soul", [
        "demiurge/agents/clio-customer-signal-collector",
        "tickets/DEMIURGE-044",
    ]),
    ("045", "DEMIURGE-045: PD cadences and router wiring", [
        "departments/product-discovery/cadences.md",
        "departments/product-discovery/signals.yaml",
        "demiurge/router/timing-rules.yaml",
        "scripts/demiurge/print-repo-init.py",
        "tickets/DEMIURGE-045",
    ]),
    ("046", "DEMIURGE-046: three-way revenue stack signal map", [
        "tickets/DEMIURGE-046",
    ]),
    ("047", "DEMIURGE-047: Product Discovery activation review", [
        "departments/product-discovery/REVIEW.md",
        "tickets/DEMIURGE-047",
    ]),
    ("048", "DEMIURGE-048: KPI schema for revenue stack", [
        "demiurge/kpi/revenue-stack.yaml",
        "docs/demiurge/kpi-schema-revenue.md",
        "tickets/DEMIURGE-048",
    ]),
    ("049", "DEMIURGE-049: Argus health monitor soul", [
        "demiurge/agents/argus-health-monitor",
        "tickets/DEMIURGE-049",
    ]),
    ("050", "DEMIURGE-050: monitor to source catalog feedback loop", [
        "demiurge/feedback-loops/README.md",
        "tickets/DEMIURGE-050",
    ]),
    ("051", "DEMIURGE-051: monitor to soul improvement loop", [
        "demiurge/feedback-loops/soul-improvement.yaml",
        "tickets/DEMIURGE-051",
    ]),
    ("052", "DEMIURGE-052: Router and Quorum test cases", [
        "docs/demiurge/router-test-cases.md",
        "tickets/DEMIURGE-052",
    ]),
    ("053", "DEMIURGE-053: self-running milestone criteria", [
        "docs/demiurge/self-running-milestone.md",
        "tickets/DEMIURGE-053",
    ]),
    ("054", "DEMIURGE-054: observation window definition", [
        "tickets/DEMIURGE-054",
    ]),
    ("055", "DEMIURGE-055: Sprint 6 complete and handoff", [
        "docs/demiurge/SPRINT-2-5-COMPLETE.md",
        "docs/demiurge/SPRINT-6-COMPLETE.md",
        "demiurge/agents/README.md",
        "demiurge/agents/hermes-router-revenue",
        "tickets/DEMIURGE-055",
    ]),
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=REPO,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def paths_exist(paths: list[str]) -> list[str]:
    existing: list[str] = []
    for p in paths:
        full = REPO / p
        if full.exists():
            existing.append(p)
        else:
            print(f"WARN missing path skipped: {p}")
    return existing


def main() -> None:
    run(["git", "checkout", "main"])
    run(["git", "checkout", "-b", EPIC_BRANCH])

    for ticket_id, message, paths in COMMITS:
        branch = f"feature/DEMIURGE-{ticket_id}"
        existing = paths_exist(paths)
        if not existing:
            print(f"SKIP {ticket_id}: no files")
            continue

        run(["git", "checkout", EPIC_BRANCH])
        run(["git", "checkout", "-b", branch])

        for path in existing:
            run(["git", "add", path])

        run(["git", "commit", "-m", message])
        run(["git", "checkout", EPIC_BRANCH])
        run(["git", "merge", "--no-ff", branch, "-m", f"Merge {branch} into {EPIC_BRANCH}"])

    status = run(["git", "status", "--short"], check=False)
    print(status.stdout)
    if status.stdout.strip():
        print("WARNING: uncommitted files remain (see above)")

    run(["git", "log", "--oneline", "-12"], check=False)
    print(f"\nDone. Epic branch: {EPIC_BRANCH}")


if __name__ == "__main__":
    main()
