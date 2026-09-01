"""test_research_education.py — Tests for research-education scripts.

Phase 9 R3 / Tier C3. Validates the 3 new research-education scripts
plus the bus integration.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path("/opt/data/agents")
VENV = Path("/opt/data/.venv") / "bin" / "python3"


def test_dedupe_runs():
    """dedupe-research-corpus.py runs without crash."""
    r = subprocess.run(
        [str(VENV), str(REPO / "scripts" / "dedupe-research-corpus.py")],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0
    assert "Scanned" in r.stdout


def test_research_bus_post_and_list():
    """research-request-bus.py can post + list."""
    # Post
    r = subprocess.run(
        [str(VENV), str(REPO / "scripts" / "research-request-bus.py"),
         "post", "--from", "test-dept", "--topic", "test topic", "--priority", "P2"],
        capture_output=True, text=True, timeout=5,
    )
    assert r.returncode == 0
    # List
    r2 = subprocess.run(
        [str(VENV), str(REPO / "scripts" / "research-request-bus.py"), "list"],
        capture_output=True, text=True, timeout=5,
    )
    assert r2.returncode == 0


def test_research_bus_fulfill():
    """research-request-bus.py can mark requests fulfilled."""
    # Post first
    r = subprocess.run(
        [str(VENV), str(REPO / "scripts" / "research-request-bus.py"),
         "post", "--from", "test-dept-2", "--topic", "fulfillable topic", "--priority", "P1"],
        capture_output=True, text=True, timeout=5,
    )
    # Extract the request ID from output
    import re
    m = re.search(r"Request (\w+) posted", r.stdout)
    if m:
        req_id = m.group(1)
        # Fulfill
        r2 = subprocess.run(
            [str(VENV), str(REPO / "scripts" / "research-request-bus.py"),
             "fulfill", "--id", req_id, "--response", "/tmp/test-response.md"],
            capture_output=True, text=True, timeout=5,
        )
        assert r2.returncode == 0
        assert "fulfilled" in r2.stdout


def test_knowledge_synthesizer_runs():
    """knowledge-synthesizer.py runs and produces output."""
    r = subprocess.run(
        [str(VENV), str(REPO / "scripts" / "knowledge-synthesizer.py")],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0
    assert "Wrote" in r.stdout
    # Verify file was created
    synth_files = list((REPO / "research").glob("WEEKLY-SYNTHESIS-*.md"))
    assert len(synth_files) >= 1


def test_methodology_version_log_exists():
    """The methodology version log file exists."""
    log = REPO / "research" / "dept-research" / "METHODOLOGY-VERSION-LOG.md"
    assert log.exists()
    content = log.read_text()
    assert "v1.1" in content
    assert "v1.0" in content


def test_gap_closure_doc_exists():
    """The gap closure summary doc exists."""
    doc = REPO / "research" / "dept-research" / "05-research-education-gap-closure-2026-09.md"
    assert doc.exists()
    content = doc.read_text()
    assert "8 dept gaps" in content.lower() or "Gap Closure Summary" in content


def test_9_new_research_crons_wired():
    """9 research-education cron entries should be wired."""
    cron_path = Path("/opt/data/.hermes/cron/jobs.json")
    with cron_path.open() as f:
        jobs = json.load(f)
    research_crons = [j for j in jobs["jobs"] if any(
        keyword in j["name"] for keyword in [
            "academic-liaison", "research-associate", "research-engineer",
            "research-tracker", "citation-checker", "course-producer",
            "instructional-designer", "ip-patent", "publication-coordinator",
            "literature-scan", "knowledge-synthesizer"
        ]
    )]
    assert len(research_crons) >= 9