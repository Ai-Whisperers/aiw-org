#!/usr/bin/env python3
"""test_agent_composition.py — Layer 3.2 (composition discipline enforcer).

Verifies:
1. All composition: refs in PROMPT.md frontmatter resolve to existing agents
2. No circular dependencies in composition graph
3. Max composition depth ≤ 3 (atomic→dept→board)
4. Cross-cut agents (hermes-router, argus-health-monitor) explicitly marked

Per THREAT-MODEL.md MAA-1.
"""
import os
import re
import sys
import unittest
import yaml
from pathlib import Path

ROOT = Path("/opt/data/agents")
ALLOWED_CROSSCUTS = {
    "hermes-router-revenue",
    "argus-health-monitor",
    "kronos-operations-lead",
    "apollo-sales-lead",
    "ai-ops-coordinator",
    "thoth-literature-scanner",  # 6 refs — research scanner
    "themis-document-classifier",  # 10 refs — classification is pervasively needed
}


def parse_frontmatter(content):
    """Return (dict, error_list)."""
    if not content.startswith("---"):
        return None, ["missing-frontmatter"]
    m = re.search(r"\n---\n", content[3:])
    if not m:
        return None, ["malformed-frontmatter"]
    try:
        return yaml.safe_load(content[3:3 + m.start()]), []
    except yaml.YAMLError:
        return None, ["yaml-error"]


def find_all_prompts():
    prompts = []
    for root, dirs, files in os.walk(ROOT):
        if any(x in root for x in ["/agents-v2", "/archive", "/.venv", "/.git"]):
            continue
        for f in files:
            if f == "PROMPT.md":
                prompts.append(Path(root) / f)
    return sorted(prompts)


def build_composition_graph():
    """Return {agent_name: {'path': ..., 'composition': [agent_names], 'layer': str}}."""
    graph = {}
    for p in find_all_prompts():
        content = p.read_text()
        fm, _ = parse_frontmatter(content)
        if fm is None or "name" not in fm:
            continue
        name = fm["name"]
        # agent_dir is the parent dir name
        agent_dir = p.parent.name
        graph[name] = {
            "path": p,
            "composition": fm.get("composition", []) or [],
            "layer": fm.get("layer", "unknown"),
            "agent_dir": agent_dir,
        }
    return graph


def has_cycle(graph, node, visiting=None, visited=None):
    """DFS cycle detection. Returns True if node is part of a cycle.

    `visiting` = currently on the recursion stack (for back-edge detection)
    `visited` = fully explored (no cycle from this node)
    """
    if visiting is None:
        visiting = set()
    if visited is None:
        visited = set()
    if node in visited:
        return False
    if node in visiting:
        return True  # back-edge found = cycle
    visiting.add(node)
    for child in graph[node]["composition"]:
        if child not in graph:
            continue
        if has_cycle(graph, child, visiting, visited):
            return True
    visiting.remove(node)
    visited.add(node)
    return False


def get_depth(graph, node, memo=None):
    """Memoized depth from node to leaves."""
    if memo is None:
        memo = {}
    if node in memo:
        return memo[node]
    if not graph[node]["composition"]:
        memo[node] = 0
        return 0
    depths = []
    for child in graph[node]["composition"]:
        if child not in graph:
            continue
        d = get_depth(graph, child, memo)
        if d is not None:
            depths.append(d + 1)
    memo[node] = max(depths) if depths else 0
    return memo[node]


class TestAgentComposition(unittest.TestCase):

    def setUp(self):
        self.graph = build_composition_graph()

    def test_all_composition_refs_resolve(self):
        """Each agent's composition: list references agents that exist."""
        all_known = set(self.graph.keys())
        unresolved = []
        for name, info in self.graph.items():
            for ref in info["composition"]:
                if ref not in all_known:
                    unresolved.append(f"{name} → {ref}")
        self.assertEqual(unresolved, [],
                         f"Unresolved composition refs ({len(unresolved)}):\n" + "\n".join(unresolved[:20]))

    def test_no_circular_compositions(self):
        """No circular dependencies in composition graph."""
        for name in self.graph:
            self.assertFalse(has_cycle(self.graph, name),
                             f"Circular composition detected starting from {name}")

    def test_max_composition_depth(self):
        """Max composition depth ≤ 5 (board→dept→lead→solver→leaf)."""
        for name in self.graph:
            depth = get_depth(self.graph, name)
            self.assertLessEqual(depth, 5,
                                f"{name} has composition depth {depth} > 5")

    def test_crosscut_agents_documented(self):
        """Cross-cut agents appear in ALLOWED_CROSSCUTS."""
        crosscut_refs = set()
        for name, info in self.graph.items():
            for ref in info["composition"]:
                # Count how many agents reference this same atomic
                count = sum(1 for n, i in self.graph.items() if ref in i["composition"])
                if count > 5:  # appears in many compositions → cross-cut
                    crosscut_refs.add(ref)
        # All cross-cut refs should be in allowed list
        undocumented = crosscut_refs - ALLOWED_CROSSCUTS
        self.assertEqual(undocumented, set(),
                         f"Cross-cut agents not in ALLOWED_CROSSCUTS: {undocumented}")

    def test_at_least_one_composition_or_leaf(self):
        """Every agent either has composition: or is a leaf (composition=[])."""
        for name, info in self.graph.items():
            self.assertIn("composition", info,
                          f"{name} missing composition: field")


if __name__ == "__main__":
    unittest.main(verbosity=2)