#!/usr/bin/env python3
"""prompt-improvement-suggester.py - Suggest PROMPT.md changes based on eval-gate trends.

For each agent with low pass rate:
- Read latest brief
- Read PROMPT.md
- Suggest specific changes

Writes suggestions to /opt/data/state/prompt-improvements.md
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

STATE_DIR = Path("/opt/data/state")
AGENTS_DIR = Path("/opt/data/agents")
OUTPUT = STATE_DIR / "prompt-improvements.md"

THRESHOLD_PASS_RATE = 70.0  # Below this = needs improvement


def analyze_agent(agent_name: str, recent_briefs: list) -> dict:
    """Analyze an agent's recent briefs and suggest improvements."""
    agent_dir = AGENTS_DIR / agent_name
    prompt_path = agent_dir / "PROMPT.md"
    
    if not prompt_path.exists():
        return {"error": "no PROMPT"}
    
    prompt_text = prompt_path.read_text()
    
    issues = []
    suggestions = []
    
    # Issue 1: brief length
    if recent_briefs:
        avg_size = sum(b.get("size_bytes", 0) for b in recent_briefs) / len(recent_briefs)
        if avg_size < 200:
            issues.append(f"Briefs averaging {avg_size:.0f} bytes (too short)")
            suggestions.append("Add 'Length: 300-700 words' to Hard constraints")
    
    # Issue 2: missing sections in PROMPT
    if "## Hard constraints" not in prompt_text:
        issues.append("Missing 'Hard constraints' section")
        suggestions.append("Add Hard constraints with length/format/delivery rules")
    
    if "## Class" not in prompt_text and "## Mission" not in prompt_text:
        issues.append("Missing Class/Mission sections")
        suggestions.append("Add Class (OPERATIONAL/CONTENT) and Mission sections")
    
    if "## Inputs" not in prompt_text and "## Outputs" not in prompt_text:
        issues.append("Missing contract sections")
        suggestions.append("Add Inputs (Contract) and Outputs (Contract) sections")
    
    # Issue 3: trademark violations
    banned = ["proveedor de IA", "modelo de IA", "proveedor de IA", "asistente de IA generativa", "gpt-4", "texto", "whatsapp", "canal de texto"]
    for brief in recent_briefs:
        try:
            text = (STATE_DIR / brief["path"]).read_text()
            for b in banned:
                if b.lower() in text.lower():
                    issues.append(f"Banned trademark in brief: {b}")
                    suggestions.append(f"Remove '{b}' from brief")
                    break
        except:
            pass
    
    # Issue 4: missing skill references
    if "skill stack" not in prompt_text.lower() and "## Skill" not in prompt_text:
        issues.append("No skill stack section")
        suggestions.append("Add '## Skill stack' with required skills")
    
    return {
        "agent": agent_name,
        "issues": issues,
        "suggestions": suggestions,
        "brief_count": len(recent_briefs),
    }


def main():
    # Read recent briefs from org-state
    org = json.loads((STATE_DIR / "org-state.json").read_text())
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=30)
    
    analyses = []
    for agent_name, agent_data in org.get("agents", {}).items():
        briefs = agent_data.get("briefs", [])
        # Filter to last 30 days
        recent = []
        for b in briefs:
            try:
                date = datetime.strptime(b["date"], "%Y-%m-%d").date()
                if date >= cutoff:
                    recent.append(b)
            except:
                pass
        
        if not recent:
            continue
        
        result = analyze_agent(agent_name, recent)
        if result.get("issues"):
            analyses.append(result)
    
    # Sort by number of issues
    analyses.sort(key=lambda a: -len(a.get("issues", [])))
    
    # Write report
    out = "# Prompt Improvement Suggestions\n\n"
    out += f"_Generated: {datetime.now(timezone.utc).isoformat()}_\n\n"
    out += f"Total agents with issues: {len(analyses)}\n\n"
    
    for analysis in analyses[:30]:
        out += f"## {analysis['agent']}\n\n"
        out += f"_Briefs in last 30 days: {analysis['brief_count']}_\n\n"
        out += "### Issues\n\n"
        for issue in analysis["issues"]:
            out += f"- {issue}\n"
        out += "\n### Suggested Fixes\n\n"
        for sug in analysis["suggestions"]:
            out += f"- {sug}\n"
        out += "\n---\n\n"
    
    OUTPUT.write_text(out)
    print(f"Found {len(analyses)} agents with issues")
    print(f"Report: {OUTPUT}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

