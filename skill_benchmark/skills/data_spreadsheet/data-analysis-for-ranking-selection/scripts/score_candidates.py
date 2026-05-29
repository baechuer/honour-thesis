#!/usr/bin/env python3
"""Weighted candidate scoring helper.

Input JSON format:
{
  "weights": {"criterion_a": 0.5, "criterion_b": 0.5},
  "rows": [
    {"name": "A", "criterion_a": 10, "criterion_b": 8},
    {"name": "B", "criterion_a": 7, "criterion_b": 9}
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply weighted scoring to candidate rows.")
    parser.add_argument("input", nargs="?", help="Optional JSON file path; reads stdin if omitted.")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    payload = json.loads(text)

    weights = payload.get("weights", {})
    rows = payload.get("rows", [])
    scored = []
    for row in rows:
        score = 0.0
        contributions = {}
        for key, weight in weights.items():
            value = float(row.get(key, 0.0))
            contrib = value * float(weight)
            contributions[key] = contrib
            score += contrib
        scored.append(
            {
                "name": row.get("name"),
                "score": score,
                "contributions": contributions,
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    print(json.dumps({"ranking": scored}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
