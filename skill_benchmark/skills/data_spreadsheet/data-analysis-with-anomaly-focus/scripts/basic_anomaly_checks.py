#!/usr/bin/env python3
"""Basic anomaly checks for simple numeric sequences."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Check simple numeric series for anomalous recent values.")
    parser.add_argument("input", nargs="?", help="Optional input file; reads stdin if omitted.")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    values = load_values(text)
    if len(values) < 3:
        print(json.dumps({"error": "Need at least three numeric values"}, indent=2))
        return 1

    baseline = values[:-1]
    recent = values[-1]
    mean = statistics.mean(baseline)
    stdev = statistics.pstdev(baseline) if len(baseline) > 1 else 0.0

    z_score = None if stdev == 0 else (recent - mean) / stdev
    direction = "high" if recent > mean else "low" if recent < mean else "flat"
    severe = abs(z_score) >= 2 if z_score is not None else False

    result = {
        "baseline_mean": mean,
        "recent_value": recent,
        "direction_vs_baseline": direction,
        "z_score": z_score,
        "looks_anomalous": severe or abs(recent - mean) > abs(mean) * 0.25 if mean != 0 else severe,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
