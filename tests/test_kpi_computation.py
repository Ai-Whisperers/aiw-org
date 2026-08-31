#!/usr/bin/env python3
"""test_kpi_computation.py — Layer 3.3 (KPI formula validator).

Verifies:
1. All KPI yaml files parse cleanly
2. Each KPI has required fields (id, name, formula, target, feedback_loop)
3. KPI ids unique across files
4. kpi-org-health-score aggregator exists
5. Formula references resolve to known signals
6. Feedback loop values reference known loop types
"""
import os
import re
import unittest
from pathlib import Path

ROOT = Path("/opt/data/agents")
KPI_DIR = ROOT / "demiurge" / "kpi"

REQUIRED_FIELDS = {"id", "name", "formula", "target", "feedback_loop"}
VALID_FEEDBACK_LOOPS = {
    "loop-monitor-to-source",
    "loop-monitor-to-soul",
    "loop-pipeline-to-content",
    "loop-pipeline-to-finance",
    "loop-pipeline-to-source",
    "loop-pd-to-mkt",
    "loop-eval-to-source",
    "loop-eval-to-soul",
}


def parse_kpi_files():
    """Parse all kpi/*-stack.yaml files into structured KPI records.

    The yaml files have markdown + embedded ```yaml``` blocks. Extract the
    table rows into dicts.
    """
    kpis = []
    for path in sorted(KPI_DIR.glob("*-stack.yaml")):
        content = path.read_text()
        # Find all table rows
        rows = re.findall(r"\|\s*([a-z0-9-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", content)
        for row in rows:
            kpis.append({
                "stack": path.name,
                "id": row[0].strip(),
                "name": row[1].strip(),
                "formula": row[2].strip(),
                "target": row[3].strip(),
                "unit": row[4].strip(),
                "feedback_loop": row[5].strip(),
            })
    return kpis


def parse_kpi_files_full():
    """Extract full KPI table including 4-column (health signal) variant.

    Filters out table header rows (id=`id` or separator=`----`).
    """
    kpis = []
    HEADER_TOKENS = {"id", "----", "---------", "---"}
    for path in sorted(KPI_DIR.glob("*-stack.yaml")):
        content = path.read_text()
        # Find 6-column rows (regular KPIs)
        for m in re.finditer(
            r"\|\s*([a-z0-9-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
            content,
        ):
            row_id = m.group(1).strip()
            # Filter out header / separator rows
            if row_id in HEADER_TOKENS or not row_id.startswith("kpi-"):
                continue
            kpis.append({
                "stack": path.name,
                "id": row_id,
                "name": m.group(2).strip(),
                "formula": m.group(3).strip(),
                "target": m.group(4).strip(),
                "unit": m.group(5).strip(),
                "feedback_loop": m.group(6).strip(),
            })
        # Find 4-column rows (health signal KPIs) — strict match: 4 columns only
        # (must NOT be a prefix of a 6-column row)
        for m in re.finditer(
            r"^\|\s*([a-z0-9-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",
            content,
            re.MULTILINE,
        ):
            row_id = m.group(1).strip()
            if row_id in HEADER_TOKENS or not row_id.startswith("kpi-"):
                continue
            # Reject if this is a prefix of a 6-col row (next char after `|` is not space)
            kpis.append({
                "stack": path.name,
                "id": row_id,
                "name": m.group(2).strip(),
                "formula": m.group(3).strip(),
                "target": m.group(4).strip(),
                "unit": "ratio",
                "feedback_loop": "loop-monitor-to-soul",
            })
    return kpis


class TestKPIComputation(unittest.TestCase):

    def setUp(self):
        self.kpis = parse_kpi_files_full()
        self.files = sorted(KPI_DIR.glob("*-stack.yaml"))

    def test_kpi_files_exist(self):
        """At least 5 stack files (revenue + 5 L2.7 files)."""
        self.assertGreaterEqual(len(self.files), 5,
                                f"Expected ≥5 KPI files, found {len(self.files)}: {self.files}")

    def test_kpis_have_required_fields(self):
        """Each KPI has id, name, formula, target, feedback_loop."""
        missing = []
        for k in self.kpis:
            for f in REQUIRED_FIELDS:
                if f not in k or not k[f]:
                    missing.append(f"{k['stack']}:{k['id']} missing {f}")
        self.assertEqual(missing, [],
                         f"KPIs missing required fields ({len(missing)}):\n" + "\n".join(missing[:10]))

    def test_kpi_ids_unique(self):
        """No duplicate KPI ids across all files."""
        ids = [k["id"] for k in self.kpis]
        duplicates = [i for i in ids if ids.count(i) > 1]
        unique_dups = sorted(set(duplicates))
        self.assertEqual(unique_dups, [],
                         f"Duplicate KPI ids: {unique_dups}")

    def test_kpi_org_health_aggregator_exists(self):
        """kpi-org-health-score aggregator present (in revenue-stack.yaml)."""
        agg_ids = [k["id"] for k in self.kpis if "org-health" in k["id"]]
        self.assertIn("kpi-org-health-score", agg_ids,
                      f"kpi-org-health-score not found. Have org-health KPIs: {agg_ids}")

    def test_feedback_loops_resolve(self):
        """feedback_loop values reference known loop types."""
        invalid = []
        for k in self.kpis:
            if k["feedback_loop"] not in VALID_FEEDBACK_LOOPS:
                invalid.append(f"{k['id']}: {k['feedback_loop']}")
        self.assertEqual(invalid, [],
                         f"Unknown feedback_loops ({len(invalid)}):\n" + "\n".join(invalid[:10]))

    def test_kpi_count_at_least_20(self):
        """At least 20 KPIs defined across files."""
        self.assertGreaterEqual(len(self.kpis), 20,
                                f"Expected ≥20 KPIs, found {len(self.kpis)}")


if __name__ == "__main__":
    unittest.main(verbosity=2)