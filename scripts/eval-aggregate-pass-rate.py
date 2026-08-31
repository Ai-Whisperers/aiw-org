#!/usr/bin/env python3
"""Compute aggregate eval-gate pass_rate from /opt/data/state/eval-per-agent.json.

Built as Phase 8 Area #10 (engineering research catalog).
Output: writes /opt/data/state/eval-trending.json (initial values) and stdout summary.

Schema of eval-per-agent.json:

    {
      "version": "1.0.0",
      "total": <int>,
      "passed": <int>,
      "failed": <int>,
      "by_agent": {
        "<agent-name>": {
          "pass_rate": <0-1>,
          "last_eval_at": "<ISO timestamp>",
          "consecutive_failures": <int>,
          "eval_count": <int>
        },
        ...
      }
    }

Output schema (eval-trending.json):
    {
      "computed_at": "<ISO timestamp>",
      "agent_count": <int>,
      "aggregate_pass_rate": <float 0-1>,
      "passing_agents": <int>,  # pass_rate >= 0.95
      "warning_agents": <int>,  # 0.5 <= pass_rate < 0.95
      "failing_agents": <int>,  # pass_rate < 0.5
      "longest_streak": {"agent": str, "consecutive_failures": int},
      "per_agent": {<agent>: {"pass_rate": float, "trend_7d": float}, ...},
      "alert": null | str  # null if no alerts; otherwise HIGH/CRITICAL signal
    }
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

DEFAULT_EVAL_FILE = Path("/opt/data/state/eval-per-agent.json")
DEFAULT_OUTPUT_FILE = Path("/opt/data/state/eval-trending.json")
WARNING_THRESHOLD = 0.95  # KPI target
FAILURE_THRESHOLD = 0.5


def compute_aggregate(eval_file=None):
    """Compute aggregate eval pass_rate.

    Args:
        eval_file: Path to eval-per-agent.json (defaults to /opt/data/state/).

    Returns: dict with the aggregate metrics (see schema above).
    """
    if eval_file is None:
        eval_file = DEFAULT_EVAL_FILE
    eval_file = Path(eval_file)

    if not eval_file.exists():
        print(f"ERROR: {eval_file} not found", file=sys.stderr)
        sys.exit(1)

    with eval_file.open() as f:
        raw = json.load(f)

    # Schema: eval-per-agent.json has top-level summary + "by_agent" map
    # We compute against by_agent (the per-agent breakdown)
    agents = {}
    total_pass = 0.0
    total_count = 0
    passing = 0
    warning = 0
    failing = 0
    longest_streak = {"agent": None, "consecutive_failures": 0}

    # Iterate by_agent if present, otherwise iterate raw directly (backward compat)
    agent_data = raw.get("by_agent") if "by_agent" in raw else raw
    if not isinstance(agent_data, dict):
        agent_data = {}

    for agent_name, data in agent_data.items():
        if not isinstance(data, dict):
            continue
        pass_rate = data.get("pass_rate", 0.0)
        eval_count = data.get("eval_count", data.get("n", 1))
        consecutive = data.get("consecutive_failures", 0)

        # Weighted by eval_count so agents with more evals count more
        total_pass += pass_rate * eval_count
        total_count += eval_count

        if pass_rate >= WARNING_THRESHOLD:
            passing += 1
        elif pass_rate >= FAILURE_THRESHOLD:
            warning += 1
        else:
            failing += 1

        if consecutive > longest_streak["consecutive_failures"]:
            longest_streak = {
                "agent": agent_name,
                "consecutive_failures": consecutive,
            }

        agents[agent_name] = {
            "pass_rate": pass_rate,
            "consecutive_failures": consecutive,
            "last_eval_at": data.get("last_eval_at"),
        }

    aggregate = total_pass / total_count if total_count > 0 else 0.0

    # Determine alert level
    alert = None
    if aggregate < FAILURE_THRESHOLD and total_count > 0:
        alert = "CRITICAL: aggregate pass_rate below 0.5"
    elif aggregate < WARNING_THRESHOLD and total_count > 0:
        alert = "HIGH: aggregate pass_rate below 0.95 target"
    elif longest_streak["consecutive_failures"] >= 5:
        alert = f"HIGH: {longest_streak['agent']} has {longest_streak['consecutive_failures']} consecutive failures"

    output = {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "agent_count": len(agents),
        "aggregate_pass_rate": round(aggregate, 4),
        "passing_agents": passing,
        "warning_agents": warning,
        "failing_agents": failing,
        "longest_streak": longest_streak,
        "per_agent": agents,
        "alert": alert,
    }

    return output


def write_output(result, output_file=None):
    """Write result to output_file."""
    if output_file is None:
        output_file = DEFAULT_OUTPUT_FILE
    output_file = Path(output_file)
    with output_file.open("w") as f:
        json.dump(result, f, indent=2)
    return output_file


def main():
    result = compute_aggregate()
    output_file = write_output(result)

    # Stdout summary
    print(f"=== Eval Aggregate Pass Rate ===")
    print(f"Computed at: {result['computed_at']}")
    print(f"Agent count: {result['agent_count']}")
    print(f"Aggregate pass_rate: {result['aggregate_pass_rate']:.2%}")
    print(f"  Passing (>=95%): {result['passing_agents']}")
    print(f"  Warning (50-95%): {result['warning_agents']}")
    print(f"  Failing (<50%): {result['failing_agents']}")
    print(f"Longest streak: {result['longest_streak']['agent']} ({result['longest_streak']['consecutive_failures']} failures)")
    print(f"Alert: {result['alert'] or 'none'}")
    print(f"Written: {output_file}")


if __name__ == "__main__":
    main()
