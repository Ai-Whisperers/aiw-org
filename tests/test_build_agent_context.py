#!/usr/bin/env python3
"""Auto-generated tests for build-agent-context.py"""
import subprocess
import sys
import py_compile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts/context/build-agent-context.py"


class BuildAgentContextTests(unittest.TestCase):
    def test_help(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                           capture_output=True, text=True, timeout=10)
        self.assertIn(r.returncode, (0, 2), f"--help failed: {r.returncode}")
    
    def test_compile(self):
        py_compile.compile(str(SCRIPT), doraise=True)
