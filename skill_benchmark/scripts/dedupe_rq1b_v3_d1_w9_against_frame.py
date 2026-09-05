#!/usr/bin/env python3
"""Hash-deduplicate a versioned RQ1b V3 source intake against source frames."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_SUCCESS = "RQ1B_V3_D1_W9_DOWNLOAD_SUCCESS_NOT_A_CLUSTER"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_row_not_object:{path}:{number}")
            rows.append(value)
    return rows


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retrieval-manifest", type=Path, required=True)
    parser.add_argument("--frozen-source-manifest", type=Path, action="append", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--expected-retrieval-status", default=DEFAULT_SUCCESS)
    parser.add_argument("--status-prefix", default="RQ1B_V3_D1_W9")
    return parser.parse_args()


def source_hash(row: dict[str, Any]) -> str:
    canonical = row.get("canonical")
    if isinstance(canonical, dict) and canonical.get("source_sha256"):
        return str(canonical["source_sha256"])
    return str(row.get("sha256") or row.get("source_sha256") or "")


def source_id(row: dict[str, Any]) -> str | None:
    return row.get("source_id") or row.get("amendment_source_id")


def main() -> int:
    args = parse_args()
    frozen_rows = [row for path in args.frozen_source_manifest for row in read_jsonl(path)]
    frozen_by_hash = {source_hash(row): row for row in frozen_rows}
    if not frozen_by_hash or "" in frozen_by_hash:
        raise SystemExit("invalid_frozen_source_manifest")
    retrieved = read_jsonl(args.retrieval_manifest)
    successful_retrievals = [
        row for row in retrieved if row.get("status") == args.expected_retrieval_status
    ]
    non_successful_retrievals = [
        row for row in retrieved if row.get("status") != args.expected_retrieval_status
    ]
    if not successful_retrievals:
        raise SystemExit("retrieval_manifest_has_no_success_rows")

    novel: list[dict[str, Any]] = []
    existing: list[dict[str, Any]] = []
    seen_new_by_hash: dict[str, dict[str, Any]] = {}
    failures: list[str] = []
    for row in successful_retrievals:
        raw_path = Path(str(row.get("local_raw_path", "")))
        claimed_hash = str(row.get("source_sha256", ""))
        if not raw_path.is_file() or digest(raw_path) != claimed_hash:
            failures.append(f"retrieved_byte_hash_mismatch:{row.get('raw_artifact_url')}")
            continue
        if claimed_hash in frozen_by_hash:
            existing.append({
                "status": f"{args.status_prefix}_ALREADY_IN_FROZEN_FRAME_NOT_A_CLUSTER",
                "raw_artifact_url": row.get("raw_artifact_url"),
                "repository_ref": row.get("repository_ref"),
                "artifact_path": row.get("artifact_path"),
                "source_sha256": claimed_hash,
                "existing_source_id": source_id(frozen_by_hash[claimed_hash]),
            })
            continue
        if claimed_hash in seen_new_by_hash:
            canonical = seen_new_by_hash[claimed_hash]
            existing.append({
                "status": f"{args.status_prefix}_WITHIN_WAVE_BYTE_ALIAS_NOT_A_CLUSTER",
                "raw_artifact_url": row.get("raw_artifact_url"),
                "repository_ref": row.get("repository_ref"),
                "artifact_path": row.get("artifact_path"),
                "source_sha256": claimed_hash,
                "canonical_provisional_source_id": canonical["provisional_source_id"],
                "canonical_raw_artifact_url": canonical["raw_artifact_url"],
            })
            continue
        novel_row = {
            "status": f"{args.status_prefix}_NOVEL_RETRIEVED_PUBLIC_ORIGINAL_AWAITING_SOURCE_FRAME_AMENDMENT",
            "provisional_source_id": f"{args.status_prefix.replace('_D1_', '-')}-INTAKE-{len(novel) + 1:04d}",
            "lane": row.get("lane"),
            "origin_url": row.get("origin_url"),
            "repository_ref": row.get("repository_ref"),
            "artifact_path": row.get("artifact_path"),
            "raw_artifact_url": row.get("raw_artifact_url"),
            "source_sha256": claimed_hash,
            "byte_count": row.get("byte_count"),
            "local_raw_path": row.get("local_raw_path"),
        }
        seen_new_by_hash[claimed_hash] = novel_row
        novel.append(novel_row)

    output_root = args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "novel_retrieved_sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in novel), encoding="utf-8")
    (output_root / "already_frozen_aliases.jsonl").write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in existing), encoding="utf-8")
    report = {
        "status": f"{args.status_prefix}_DEDUP_{'PASS' if not failures else 'FAIL'}_NOT_A_CLUSTER",
        "retrieval_record_count": len(retrieved),
        "retrieved_success_count": len(successful_retrievals),
        "non_successful_retrieval_count": len(non_successful_retrievals),
        "non_successful_retrieval_status_counts": {
            status: sum(item.get("status") == status for item in non_successful_retrievals)
            for status in sorted({str(item.get("status")) for item in non_successful_retrievals})
        },
        "novel_byte_distinct_source_count": len(novel),
        "already_frozen_byte_duplicate_count": sum(
            item["status"] == f"{args.status_prefix}_ALREADY_IN_FROZEN_FRAME_NOT_A_CLUSTER"
            for item in existing
        ),
        "within_wave_byte_alias_count": sum(
            item["status"] == f"{args.status_prefix}_WITHIN_WAVE_BYTE_ALIAS_NOT_A_CLUSTER"
            for item in existing
        ),
        "failures": failures,
        "boundary": "Byte-level source deduplication only. Non-successful retrieval records remain retained and are not retried or deduplicated. Exact byte aliases against frozen sources and within the current wave are retained in the alias ledger; each novel byte-distinct source is frozen at most once. Novel successful records await a separate source-frame amendment and have no D1/C1 eligibility, cluster, prompt, label, selector, metric, or result status.",
    }
    (output_root / "dedup_report.json").write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
