#!/usr/bin/env python3
"""Quarantine duplicate W24 capture attempts without rewriting the raw manifest."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise SystemExit(f"jsonl_row_not_object:{path}:{number}")
            rows.append(value)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--raw-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    draft_rows = read_jsonl(args.draft)
    raw_rows = read_jsonl(args.raw_manifest)
    draft_by_url = {str(row.get("raw_artifact_url", "")): row for row in draft_rows}
    if "" in draft_by_url or len(draft_by_url) != len(draft_rows):
        raise SystemExit("invalid_or_duplicate_draft_urls")

    by_url: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for line_number, row in enumerate(raw_rows, start=1):
        url = str(row.get("raw_artifact_url", ""))
        by_url[url].append({"raw_manifest_line": line_number, **row})

    clean: list[dict[str, Any]] = []
    duplicate_quarantine: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for url, draft_row in draft_by_url.items():
        attempts = by_url.get(url, [])
        if not attempts:
            missing.append({"raw_artifact_url": url, "draft": draft_row, "status": "RQ1B_V3_W24_CAPTURE_NOT_ATTEMPTED_AFTER_CONCURRENCY_INCIDENT"})
        elif len(attempts) == 1:
            clean.append(attempts[0])
        else:
            unique_statuses = sorted({str(item.get("status", "")) for item in attempts})
            unique_hashes = sorted({str(item.get("source_sha256", "")) for item in attempts if item.get("source_sha256")})
            duplicate_quarantine.append(
                {
                    "raw_artifact_url": url,
                    "attempt_count": len(attempts),
                    "attempt_line_numbers": [item["raw_manifest_line"] for item in attempts],
                    "unique_statuses": unique_statuses,
                    "unique_success_sha256": unique_hashes,
                    "attempts": attempts,
                    "status": "RQ1B_V3_W24_CAPTURE_DUPLICATE_ATTEMPTS_QUARANTINED_NOT_ELIGIBLE_FOR_SOURCE_ADMISSION",
                }
            )

    out_of_roster = [
        {"raw_manifest_line": line_number, **row, "status": "RQ1B_V3_W24_CAPTURE_OUT_OF_ROSTER_QUARANTINED"}
        for line_number, row in enumerate(raw_rows, start=1)
        if str(row.get("raw_artifact_url", "")) not in draft_by_url
    ]
    clean_urls = {str(row.get("raw_artifact_url", "")) for row in clean}
    if clean_urls & {row["raw_artifact_url"] for row in duplicate_quarantine}:
        raise SystemExit("clean_duplicate_overlap")

    write_jsonl(args.output_root / "single_attempt_manifest.jsonl", clean)
    write_jsonl(args.output_root / "duplicate_attempt_url_quarantine.jsonl", duplicate_quarantine)
    write_jsonl(args.output_root / "not_attempted_url_quarantine.jsonl", missing)
    write_jsonl(args.output_root / "out_of_roster_quarantine.jsonl", out_of_roster)
    summary = {
        "status": "RQ1B_V3_W24_CAPTURE_CONCURRENCY_INCIDENT_AUDITED_NOT_A_SOURCE_OR_CLUSTER",
        "raw_manifest_path": str(args.raw_manifest),
        "draft_url_count": len(draft_rows),
        "raw_manifest_line_count": len(raw_rows),
        "single_attempt_url_count": len(clean),
        "duplicate_attempt_url_count": len(duplicate_quarantine),
        "not_attempted_url_count": len(missing),
        "out_of_roster_manifest_line_count": len(out_of_roster),
        "duplicate_attempt_histogram": dict(sorted(Counter(row["attempt_count"] for row in duplicate_quarantine).items())),
        "boundary": [
            "The original manifest and raw artifacts are preserved unchanged for audit.",
            "Only URLs with exactly one retained raw-manifest record may be considered in a subsequent source-only deduplication stage.",
            "Duplicate-attempt and unattempted URLs are quarantined, not silently repaired or used as source admission evidence.",
            "This is execution-integrity accounting only, not a source-quality, D1/C1, cluster, prompt, label, selector, metric or retrieval result.",
        ],
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "audit_report.json").write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
