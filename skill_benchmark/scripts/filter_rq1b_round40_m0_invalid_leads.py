#!/usr/bin/env python3
"""Quarantine malformed Round 40 M0 navigation leads before canonical intake."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED = {
    "repository_url",
    "source_repository_path",
    "skill_locator_url",
    "skill_title_or_name",
    "capability_summary",
    "discovery_domain",
    "discovery_rationale",
}


def read_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise SystemExit(f"non_object_json:{path}:{line_number}")
        rows.append((line_number, value))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--clean-directory", type=Path, required=True)
    parser.add_argument("--quarantine", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    clean_outputs: list[str] = []
    quarantined: list[dict[str, Any]] = []
    clean_count = 0
    for input_path in args.input:
        clean_rows: list[dict[str, Any]] = []
        for line_number, row in read_jsonl(input_path):
            missing = sorted(key for key in REQUIRED if not str(row.get(key, "")).strip())
            if missing:
                quarantined.append({
                    "m0_quarantine_status": "M0_MALFORMED_NAVIGATION_LEAD_NON_ADMISSION_NOT_A_CLUSTER_OR_RESULT",
                    "source_input_path": str(input_path),
                    "source_line_number": line_number,
                    "reason": f"missing_required_fields:{','.join(missing)}",
                    "original_row": row,
                    "exclusions": [
                        "The lead is not repaired, pinned, fetched, or admitted.",
                        "No source body, candidate composition, prompt, label, retrieval input, model call, metric, or result exists.",
                    ],
                })
                continue
            clean_rows.append(row)
        output_path = args.clean_directory / input_path.name
        write_jsonl(output_path, clean_rows)
        clean_outputs.append(str(output_path))
        clean_count += len(clean_rows)

    write_jsonl(args.quarantine, quarantined)
    summary = {
        "status": "M0_ROUND40_MALFORMED_LEADS_QUARANTINED_NOT_A_CLUSTER_OR_RESULT",
        "input_file_count": len(args.input),
        "clean_lead_count": clean_count,
        "quarantined_lead_count": len(quarantined),
        "clean_outputs": clean_outputs,
        "quarantine": str(args.quarantine),
        "exclusions": [
            "Quarantine is a local format gate only; it does not validate source existence or body content.",
            "Quarantined leads are not repaired or passed into M0 canonicalisation.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "clean_lead_count", "quarantined_lead_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
