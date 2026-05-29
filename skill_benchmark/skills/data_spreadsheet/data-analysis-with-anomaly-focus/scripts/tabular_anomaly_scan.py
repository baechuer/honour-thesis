#!/usr/bin/env python3
"""Scan tabular weekly data for concentrated anomalies by segment."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


METRICS = ("orders", "returns", "conversion_rate", "gross_margin_pct")
PROBLEM_DIRECTIONS = {
    "orders": "down",
    "returns": "up",
    "conversion_rate": "down",
    "gross_margin_pct": "down",
}


def _as_float(value: str) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _segment_key(row: dict[str, str]) -> str:
    return f"{row['channel']} | {row['device']} | {row['region']}"


def _score_recent(metric: str, values: list[float]) -> tuple[float | None, bool]:
    if len(values) < 3:
        return None, False
    baseline = values[:-1]
    recent = values[-1]
    mean = statistics.mean(baseline)
    stdev = statistics.pstdev(baseline) if len(baseline) > 1 else 0.0
    z_score = None if stdev == 0 else (recent - mean) / stdev
    delta = recent - mean
    pct_gap = abs(delta) / abs(mean) if mean else 0.0
    direction = PROBLEM_DIRECTIONS[metric]
    problem_side = (delta < 0) if direction == "down" else (delta > 0)
    strong_enough = abs(z_score) >= 1.75 if z_score is not None else pct_gap >= 0.2
    flag = problem_side and strong_enough and pct_gap >= 0.12
    return z_score, flag


def main() -> int:
    parser = argparse.ArgumentParser(description="Find tabular anomalies in a CSV.")
    parser.add_argument("input", nargs="?", help="CSV file path; reads stdin if omitted.")
    args = parser.parse_args()

    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    rows = list(csv.DictReader(text.splitlines()))
    if not rows:
        print(json.dumps({"error": "No CSV rows found"}, indent=2))
        return 1

    by_segment: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_segment[_segment_key(row)].append(row)

    anomalies: list[dict[str, object]] = []
    for segment, segment_rows in by_segment.items():
        segment_rows.sort(key=lambda row: row["week"])
        latest = segment_rows[-1]
        for metric in METRICS:
            values = [_as_float(row.get(metric, "")) for row in segment_rows]
            clean_values = [value for value in values if value is not None]
            if len(clean_values) < 3:
                continue
            z_score, flag = _score_recent(metric, clean_values)
            if not flag:
                continue
            anomalies.append(
                {
                    "segment": segment,
                    "metric": metric,
                    "latest_week": latest["week"],
                    "latest_value": clean_values[-1],
                    "z_score": None if z_score is None else round(z_score, 2),
                    "latest_note": latest.get("notes", ""),
                }
            )
        for metric in ("cost", "gross_margin_pct"):
            if _as_float(latest.get(metric, "")) is None:
                anomalies.append(
                    {
                        "segment": segment,
                        "metric": metric,
                        "latest_week": latest["week"],
                        "latest_value": None,
                        "z_score": None,
                        "latest_note": latest.get("notes", ""),
                    }
                )

    print(json.dumps({"anomalies": anomalies}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
