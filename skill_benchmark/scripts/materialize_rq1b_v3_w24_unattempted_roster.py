#!/usr/bin/env python3
"""Materialise only never-attempted W24 URLs for a separate one-shot capture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incident-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for number, line in enumerate(args.incident_manifest.read_text(encoding="utf-8").splitlines(), start=1):
        if not line:
            continue
        value = json.loads(line)
        draft = value.get("draft")
        if value.get("status") != "RQ1B_V3_W24_CAPTURE_NOT_ATTEMPTED_AFTER_CONCURRENCY_INCIDENT" or not isinstance(draft, dict):
            raise SystemExit(f"invalid_incident_row:{number}")
        url = draft.get("raw_artifact_url")
        if not isinstance(url, str) or not url or url in seen:
            raise SystemExit(f"invalid_or_duplicate_url:{number}")
        seen.add(url)
        records.append(draft)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    print(json.dumps({"status": "RQ1B_V3_W24_NEVER_ATTEMPTED_ROSTER_MATERIALISED_NOT_A_CLUSTER", "record_count": len(records)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
