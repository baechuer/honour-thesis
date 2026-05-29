#!/usr/bin/env python3
"""Scan a spreadsheet for likely drivers of margin deterioration."""

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
    parser = argparse.ArgumentParser(description="Find the strongest drivers of margin deterioration.")
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

    candidates: list[dict[str, object]] = []
    for segment, segment_rows in by_segment.items():
        segment_rows.sort(key=lambda row: row["week"])
        first = segment_rows[0]
        last = segment_rows[-1]
        first_gp = _gross_profit(first)
        last_gp = _gross_profit(last)
        first_conv = _as_float(first.get("conversion_rate", "")) or 0.0
        last_conv = _as_float(last.get("conversion_rate", "")) or 0.0
        first_returns = _as_float(first.get("returns", "")) or 0.0
        last_returns = _as_float(last.get("returns", "")) or 0.0
        first_margin = _as_float(first.get("gross_margin_pct", "")) or 0.0
        last_margin = _as_float(last.get("gross_margin_pct", "")) or 0.0

        missing_margin = any(_as_float(r.get("gross_margin_pct", "")) is None for r in segment_rows)
        missing_cost = any(_as_float(r.get("cost", "")) is None for r in segment_rows)

        candidates.append(
            {
                "segment": segment,
                "gross_profit_delta": None if first_gp is None or last_gp is None else round(last_gp - first_gp, 2),
                "margin_pct_delta": round(last_margin - first_margin, 2),
                "conversion_delta": round(last_conv - first_conv, 3),
                "returns_delta": round(last_returns - first_returns, 2),
                "missing_margin_data": missing_margin,
                "missing_cost_data": missing_cost,
                "latest_note": last.get("notes", ""),
            }
        )

    ranked = sorted(
        candidates,
        key=lambda item: (
            item["gross_profit_delta"] if item["gross_profit_delta"] is not None else 10**12,
            item["margin_pct_delta"],
            item["conversion_delta"],
            -item["returns_delta"],
        ),
    )

    result = {
        "leading_drivers": ranked[:4],
        "data_quality_confounders": [
            item for item in ranked if item["missing_margin_data"] or item["missing_cost_data"]
        ][:3],
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
