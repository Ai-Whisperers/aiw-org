#!/usr/bin/env python3
"""Auto-generated tests for self-running-check-v2.py"""
import subprocess
import sys
import py_compile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts/self-running-check-v2.py"


class SelfRunningCheckV2Tests(unittest.TestCase):
    def test_help(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                           capture_output=True, text=True, timeout=10)
        self.assertIn(r.returncode, (0, 2), f"--help failed: {r.returncode}")
    
    def test_compile(self):
        py_compile.compile(str(SCRIPT), doraise=True)
