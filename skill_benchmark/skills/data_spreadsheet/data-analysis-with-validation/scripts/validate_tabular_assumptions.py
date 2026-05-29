#!/usr/bin/env python3
"""Simple tabular validation checks.

Input JSON format:
{
  "rows": [{"id": 1, "value": 10}, {"id": 1, "value": null}],
  "key": "id",
  "required": ["id", "value"]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check simple tabular assumptions.")
    parser.add_argument("input", nargs="?", help="Optional JSON file path; reads stdin if omitted.")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    payload = json.loads(text)
    rows = payload.get("rows", [])
    key = payload.get("key")
    required = payload.get("required", [])

    missing_counts = {field: 0 for field in required}
    for row in rows:
        for field in required:
            if row.get(field) in (None, ""):
                missing_counts[field] += 1

    duplicates = []
    if key:
        counts = Counter(row.get(key) for row in rows if row.get(key) not in (None, ""))
        duplicates = [value for value, count in counts.items() if count > 1]

    result = {
        "row_count": len(rows),
        "missing_counts": missing_counts,
        "duplicate_keys": duplicates,
        "looks_clean": not duplicates and all(count == 0 for count in missing_counts.values()),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
