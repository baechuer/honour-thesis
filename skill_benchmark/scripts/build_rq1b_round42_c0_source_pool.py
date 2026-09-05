#!/usr/bin/env python3
"""Expose Round 42 M1-verified sources as C0 navigation metadata only."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED_STATUS = "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for line_number, source in enumerate(read_jsonl(args.inventory), start=1):
        if source.get("source_admission_status") != EXPECTED_STATUS:
            failures.append(f"unexpected_admission_status:{line_number}:{source.get('skill_id')}")
            continue
        required = ("skill_id", "origin", "source_sha256", "local_original_path", "pinned_commit", "source_repository_path")
        missing = [field for field in required if not source.get(field)]
        original = Path(str(source.get("local_original_path", "")))
        if not original.is_absolute():
            original = (Path.cwd() / original).resolve()
        if missing:
            failures.append(f"missing_required:{line_number}:{','.join(missing)}")
            continue
        if not original.is_file():
            failures.append(f"missing_original:{line_number}:{source['skill_id']}")
            continue
        if sha256(original) != str(source["source_sha256"]):
            failures.append(f"source_hash_drift:{line_number}:{source['skill_id']}")
            continue
        rows.append({
            "c0_pool_status": "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT",
            "source_admission_status": source["source_admission_status"],
            "skill_id": source["skill_id"],
            "origin": source["origin"],
            "repository_url": source.get("repository_url"),
            "pinned_commit": source["pinned_commit"],
            "license": source.get("license"),
            "license_status": source.get("license_status"),
            "source_repository_path": source["source_repository_path"],
            "source_url": source.get("source_url"),
            "source_sha256": source["source_sha256"],
            "source_bytes": source.get("source_bytes"),
            "local_original_path": str(original),
            "source_name": source.get("frontmatter_name"),
            "source_description_preview": source.get("frontmatter_description"),
            "source_heading_preview": None,
            "source_inventory": str(args.inventory),
            "m1_source_position": source.get("m1_source_position"),
            "stage_directory": source.get("stage_directory"),
            "exclusions": [
                "The C0 pool provides source navigation metadata only and has no original source-body text.",
                "No candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
            ],
        })

    rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C0_ROUND42_SOURCE_POOL_READY_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0_ROUND42_SOURCE_POOL_FAIL_OR_INCOMPLETE",
        "input_inventory": str(args.inventory),
        "source_record_count": len(rows),
        "origin_count": len({str(row["origin"]) for row in rows}),
        "origins": dict(sorted(Counter(str(row["origin"]) for row in rows).items())),
        "integrity_failures": failures,
        "exclusions": [
            "The pool provides source-provided navigation metadata only and has no source-body text.",
            "No candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "source_record_count", "origin_count", "integrity_failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
