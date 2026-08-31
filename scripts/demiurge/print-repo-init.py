#!/usr/bin/env python3
"""Print git init commands for DEMIURGE agent repos from repo-manifest.yaml files."""

from __future__ import annotations

from pathlib import Path

import yaml


def main() -> None:
    root = Path(__file__).resolve().parents[2] / "demiurge" / "agents"
    for agent_dir in sorted(root.iterdir()):
        if not agent_dir.is_dir():
            continue
        manifest = agent_dir / "repo-manifest.yaml"
        if not manifest.exists():
            continue
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        repo = data.get("repo", agent_dir.name)
        remote = data.get("remote", f"https://github.com/Ai-Whisperers/{repo}")
        print(f"# {agent_dir.name}")
        print(f"gh repo create Ai-Whisperers/{repo} --private --source . --remote origin")
        print(f"git remote add origin {remote}  # if creating locally")
        print()


if __name__ == "__main__":
    main()
