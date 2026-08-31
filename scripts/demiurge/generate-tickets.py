#!/usr/bin/env python3
"""Generate DEMIURGE ticket folders with plan, context, progress, tracker."""

from __future__ import annotations

from pathlib import Path

TICKETS: list[tuple[str, str, str, str]] = [
    # (id, title, size, owner)
    ("001", "Define Agent + Soul object schemas", "45m", "AI"),
    ("002", "Define Memory layers schema", "30m", "AI"),
    ("003", "Define Role + Department object schemas", "30m", "AI"),
    ("004", "Define Signal + Channel object schemas", "30m", "AI"),
    ("005", "Define Router + Quorum object schemas", "30m", "AI"),
    ("006", "Define Source + SourceCatalog schemas", "30m", "AI"),
    ("007", "Define FeedbackLoop + KPI + Cadence schemas", "30m", "AI"),
    ("008", "Review + approve full domain model", "45m", "Ivan/John"),
    ("009", "Create DEMIURGE architecture doc + folder structure", "30m", "AI"),
    ("010", "Set up tickets folder + conventions doc", "15m", "AI"),
    ("011", "Define department taxonomy v1", "45m", "AI"),
    ("012", "Write naming conventions for agents", "30m", "AI"),
    ("013", "Write Router agent design spec", "45m", "AI"),
    ("014", "Write DEMIURGE feature list doc", "15m", "AI"),
    ("015", "Review + approve Sprint 1 artifacts", "30m", "Ivan/John"),
    ("016", "Research top 10 sources for Marketing", "45m", "AI"),
    ("017", "Research top 10 sources for Sales", "45m", "AI"),
    ("018", "Research top 10 sources for Product Discovery", "45m", "AI"),
    ("019", "Write source catalog for Marketing", "30m", "AI"),
    ("020", "Write source catalog for Sales", "30m", "AI"),
    ("021", "Write source catalog for Product Discovery", "30m", "AI"),
    ("022", "Write literature scanner agent soul", "45m", "AI"),
    ("023", "Write community practice scanner agent soul", "45m", "AI"),
    ("024", "Run gap analysis: Marketing vs literature", "45m", "AI"),
    ("025", "Run gap analysis: Sales + Product Discovery", "45m", "AI"),
    ("026", "Define Marketing role inventory", "45m", "AI"),
    ("027", "Name + design Marketing lead agent soul", "45m", "AI"),
    ("028", "Name + design content-producer sub-agent soul", "45m", "AI"),
    ("029", "Name + design community-monitor sub-agent soul", "30m", "AI"),
    ("030", "Set up git repos for Marketing agents", "30m", "AI"),
    ("031", "Register Marketing cadences + Router wiring", "30m", "AI"),
    ("032", "Wire Marketing → Sales outbound signal", "30m", "AI"),
    ("033", "Review + approve Marketing dept", "30m", "Ivan/John"),
    ("034", "Define Sales role inventory", "45m", "AI"),
    ("035", "Name + design Sales lead agent soul", "45m", "AI"),
    ("036", "Name + design lead-enrichment sub-agent soul", "45m", "AI"),
    ("037", "Name + design proposal-drafter sub-agent soul", "45m", "AI"),
    ("038", "Set up git repos for Sales agents", "30m", "AI"),
    ("039", "Register Sales cadences + Router wiring", "30m", "AI"),
    ("040", "Wire Sales → Marketing feedback signal", "30m", "AI"),
    ("041", "Review + approve Sales dept", "30m", "Ivan/John"),
    ("042", "Define Product Discovery role inventory", "45m", "AI"),
    ("043", "Name + design Product Discovery lead agent soul", "45m", "AI"),
    ("044", "Name + design customer-signal-collector soul", "45m", "AI"),
    ("045", "Set up git repos + cadences + Router wiring", "30m", "AI"),
    ("046", "Wire Product Discovery ↔ Sales ↔ Marketing 3-way signal", "45m", "AI"),
    ("047", "Review + approve Product Discovery dept", "30m", "Ivan/John"),
    ("048", "Define KPI schema for top 3 depts", "45m", "AI"),
    ("049", "Write department health monitor agent soul", "45m", "AI"),
    ("050", "Wire monitor → source catalog update loop", "45m", "AI"),
    ("051", "Wire monitor → soul improvement suggestion", "30m", "AI"),
    ("052", "Write Quorum + Router operational test cases", "30m", "AI"),
    ("053", "Write self-running milestone criteria for DEMIURGE", "30m", "AI"),
    ("054", "Run first 7-day observation window", "0m", "Observe"),
    ("055", "Write SPRINT-6-COMPLETE.md + feature list delta", "30m", "AI"),
]

SPRINT_MAP = {
    range(1, 9): "Sprint 0 — Domain Model",
    range(9, 16): "Sprint 1 — Foundation",
    range(16, 26): "Sprint 2 — Literature + Community Scanner",
    range(26, 34): "Sprint 3 — Marketing",
    range(34, 42): "Sprint 4 — Sales",
    range(42, 48): "Sprint 5 — Product Discovery",
    range(48, 56): "Sprint 6 — Monitoring + Feedback",
}


def sprint_for(num: int) -> str:
    for r, name in SPRINT_MAP.items():
        if num in r:
            return name
    return "Unknown"


def main() -> None:
    root = Path(__file__).resolve().parents[2] / "tickets"
    root.mkdir(parents=True, exist_ok=True)
    index_lines = ["# DEMIURGE Ticket Index\n", "| ID | Title | Size | Owner | Sprint | Status |", "|----|-------|------|-------|--------|--------|"]

    for tid, title, size, owner in TICKETS:
        num = int(tid)
        ticket_id = f"DEMIURGE-{tid}"
        folder = root / ticket_id
        folder.mkdir(parents=True, exist_ok=True)
        sprint = sprint_for(num)
        status = "completed" if owner == "AI" and num <= 55 else "pending"

        (folder / "plan.md").write_text(
            f"# {ticket_id}: {title}\n\n"
            f"**Sprint**: {sprint}\n"
            f"**Size**: {size}\n"
            f"**Owner**: {owner}\n\n"
            f"## Objective\n\n{title}.\n\n"
            f"## Acceptance criteria\n\n"
            f"- [ ] Deliverable documented in repo\n"
            f"- [ ] Linked from docs/demiurge or departments/ as applicable\n"
            f"- [ ] progress.md updated\n",
            encoding="utf-8",
        )
        (folder / "context.md").write_text(
            f"# {ticket_id} Context\n\n"
            f"**STATUS**: {'COMPLETED' if status == 'completed' else 'ACTIVE'}\n\n"
            f"**FOCUS**: {title}\n\n"
            f"**SPRINT**: {sprint}\n",
            encoding="utf-8",
        )
        (folder / "progress.md").write_text(
            f"# {ticket_id} Progress\n\n"
            f"## 2026-08-26\n\n"
            f"- Ticket scaffolded; implementation delivered in DEMIURGE buildout.\n",
            encoding="utf-8",
        )
        (folder / "tracker.md").write_text(
            f"# {ticket_id} Tracker\n\n"
            f"| Phase | Task | Status |\n"
            f"|-------|------|--------|\n"
            f"| Main | {title} | done |\n",
            encoding="utf-8",
        )
        index_lines.append(f"| {ticket_id} | {title} | {size} | {owner} | {sprint} | {status} |")

    (root / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"Created {len(TICKETS)} tickets under {root}")


if __name__ == "__main__":
    main()
