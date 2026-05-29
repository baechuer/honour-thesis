#!/usr/bin/env python3
"""Summarize channel spreadsheet movement across first and last observed weeks."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


def _as_float(value: str) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _segment_key(row: dict[str, str]) -> str:
    return f"{row['channel']} | {row['device']} | {row['region']}"


def _gross_profit(row: dict[str, str]) -> float | None:
    revenue = _as_float(row.get("revenue", ""))
    cost = _as_float(row.get("cost", ""))
    margin_pct = _as_float(row.get("gross_margin_pct", ""))
    if revenue is not None and margin_pct is not None:
        return revenue * (margin_pct / 100.0)
    if revenue is not None and cost is not None:
        return revenue - cost
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize overall movement in a spreadsheet fixture.")
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
    weeks = sorted({row["week"] for row in rows})
    for row in rows:
        by_segment[_segment_key(row)].append(row)

    segment_changes: list[dict[str, object]] = []
    missing_data_segments: list[str] = []
    for segment, segment_rows in by_segment.items():
        segment_rows.sort(key=lambda row: row["week"])
        first = segment_rows[0]
        last = segment_rows[-1]

        first_revenue = _as_float(first.get("revenue", "")) or 0.0
        last_revenue = _as_float(last.get("revenue", "")) or 0.0
        first_conv = _as_float(first.get("conversion_rate", "")) or 0.0
        last_conv = _as_float(last.get("conversion_rate", "")) or 0.0
        first_returns = _as_float(first.get("returns", "")) or 0.0
        last_returns = _as_float(last.get("returns", "")) or 0.0
        first_gp = _gross_profit(first)
        last_gp = _gross_profit(last)

        if any(_as_float(r.get("cost", "")) is None or _as_float(r.get("gross_margin_pct", "")) is None for r in segment_rows):
            missing_data_segments.append(segment)

        segment_changes.append(
            {
                "segment": segment,
                "revenue_change": round(last_revenue - first_revenue, 2),
                "conversion_change": round(last_conv - first_conv, 3),
                "returns_change": round(last_returns - first_returns, 2),
                "gross_profit_change": None if first_gp is None or last_gp is None else round(last_gp - first_gp, 2),
                "latest_note": last.get("notes", ""),
            }
        )

    def _sort_value(item: dict[str, object], key: str) -> float:
        value = item.get(key)
        return float(value) if isinstance(value, (int, float)) else -10**18

    result = {
        "weeks": weeks,
        "segment_count": len(by_segment),
        "strongest_revenue_growth": sorted(segment_changes, key=lambda item: _sort_value(item, "revenue_change"), reverse=True)[:3],
        "sharpest_conversion_drop": sorted(segment_changes, key=lambda item: _sort_value(item, "conversion_change"))[:3],
        "largest_gross_profit_drop": sorted(segment_changes, key=lambda item: _sort_value(item, "gross_profit_change"))[:3],
        "segments_with_missing_margin_data": sorted(set(missing_data_segments)),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
