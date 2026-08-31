#!/usr/bin/env python3
"""test_dept_monitor_thresholds.py — Layer 3.4 (16-monitor spec validator).

Verifies the 16-monitor spec at dept-monitors/INDEX.md:
1. INDEX file exists
2. Master matrix has exactly 16 monitors
3. Each monitor entry has required fields (dept, folder, files, metrics, cron, alias)
4. Cron expressions are valid
5. Aliases unique across monitors
6. Threshold rules section present (CRITICAL/HIGH/MEDIUM/LOW)
"""
import os
import re
import unittest
from pathlib import Path

ROOT = Path("/opt/data/agents")
INDEX_PATH = ROOT / "dept-monitors" / "INDEX.md"


def parse_master_matrix(content):
    """Extract 16-monitor table rows from INDEX.md."""
    monitors = []
    in_matrix = False
    for line in content.split("\n"):
        if "## Master matrix" in line:
            in_matrix = True
            continue
        if in_matrix:
            # End at next heading
            if line.startswith("## "):
                break
            # Skip non-table rows
            if not line.strip().startswith("|"):
                continue
            # Skip header + separator
            if "|" not in line[1:]:
                continue
            if re.match(r"\|\s*#\s*\|", line):  # | # | Dept | Folder | ...
                continue
            if re.match(r"\|\s*-+", line):
                continue
            # Parse row
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 7:
                monitors.append({
                    "num": int(parts[0]),
                    "dept": parts[1],
                    "folder": parts[2],
                    "files": parts[3],
                    "metrics": parts[4],
                    "cron": parts[5],
                    "alias": parts[6],
                })
    return monitors


def has_threshold_rules(content):
    """Check Threshold rules section with CRITICAL/HIGH/MEDIUM/LOW ladder."""
    if "## Threshold rules" not in content:
        return False
    section = content.split("## Threshold rules")[1].split("## ")[0]
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if f"**{sev}**" not in section:
            return False
    return True


class TestDeptMonitorThresholds(unittest.TestCase):

    def setUp(self):
        self.assertTrue(INDEX_PATH.exists(),
                        f"INDEX.md not found at {INDEX_PATH}")
        self.content = INDEX_PATH.read_text()
        self.monitors = parse_master_matrix(self.content)

    def test_index_exists(self):
        """dept-monitors/INDEX.md exists."""
        self.assertTrue(INDEX_PATH.exists())

    def test_16_monitors_in_master_matrix(self):
        """Exactly 16 monitors listed."""
        self.assertEqual(len(self.monitors), 16,
                         f"Expected 16 monitors, found {len(self.monitors)}: {[m['dept'] for m in self.monitors]}")

    def test_each_monitor_has_required_fields(self):
        """Each monitor entry has dept, folder, files, metrics, cron, alias."""
        missing = []
        for m in self.monitors:
            for f in ("dept", "folder", "files", "metrics", "cron", "alias"):
                if not m.get(f):
                    missing.append(f"monitor #{m.get('num', '?')} missing {f}")
        self.assertEqual(missing, [],
                         f"Monitors with missing fields ({len(missing)}):\n" + "\n".join(missing[:5]))

    def test_aliases_unique(self):
        """Monitor aliases unique."""
        aliases = [m["alias"] for m in self.monitors]
        dups = sorted(set(a for a in aliases if aliases.count(a) > 1))
        self.assertEqual(dups, [],
                         f"Duplicate monitor aliases: {dups}")

    def test_cron_expressions_basic_valid(self):
        """Each monitor's cron is a 5-field expression."""
        invalid = []
        for m in self.monitors:
            cron = m["cron"]
            # Should be 5 space-separated fields
            fields = cron.split()
            if len(fields) != 5:
                invalid.append(f"#{m['num']}: {cron}")
        self.assertEqual(invalid, [],
                         f"Invalid cron expressions: {invalid}")

    def test_threshold_rules_section_present(self):
        """Threshold rules section with CRITICAL/HIGH/MEDIUM/LOW ladder."""
        self.assertTrue(has_threshold_rules(self.content),
                        "Threshold rules section missing or incomplete")

    def test_state_write_discipline_section_present(self):
        """State-file write discipline section present."""
        self.assertIn("## State-file write discipline", self.content,
                      "State-file write discipline section missing")


if __name__ == "__main__":
    unittest.main(verbosity=2)