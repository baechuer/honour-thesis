#!/usr/bin/env python3
"""Simple recent-window trend checks for spreadsheet-like data.

Reads numeric values from stdin or a file and reports direction, percent change,
and whether the most recent step suggests acceleration, flattening, or reversal.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path


NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def load_values(text: str) -> list[float]:
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [float(x) for x in parsed]
    except Exception:
        pass

    values: list[float] = []
    for line in text.splitlines():
        matches = NUMBER_RE.findall(line)
        if matches:
            values.append(float(matches[-1]))
    return values


def pct_change(start: float, end: float) -> float | None:
    if start == 0:
        return None
    return (end - start) / abs(start) * 100.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute simple trend direction and momentum checks.")
    parser.add_argument("input", nargs="?", help="Optional file path; reads stdin if omitted.")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    values = load_values(text)
    if len(values) < 2:
        print(json.dumps({"error": "Need at least two numeric values"}, indent=2))
        return 1

    deltas = [b - a for a, b in zip(values, values[1:])]
    recent_delta = deltas[-1]
    prior_delta = deltas[-2] if len(deltas) >= 2 else None

    if recent_delta > 0:
        direction = "up"
    elif recent_delta < 0:
        direction = "down"
    else:
        direction = "flat"

    momentum = "unclear"
    if prior_delta is not None:
        if abs(recent_delta) > abs(prior_delta):
            momentum = "accelerating"
        elif abs(recent_delta) < abs(prior_delta):
            momentum = "flattening"
        else:
            momentum = "steady"
        if recent_delta == 0 and prior_delta != 0:
            momentum = "stalling"
        elif recent_delta * prior_delta < 0:
            momentum = "reversing"

    result = {
        "values": values,
        "direction": direction,
        "start_to_end_percent_change": pct_change(values[0], values[-1]),
        "recent_delta": recent_delta,
        "momentum": momentum,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
