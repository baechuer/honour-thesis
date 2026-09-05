#!/usr/bin/env python3
"""Freeze byte-distinct public originals as an additive source-frame amendment.

This is a provenance operation only.  It deliberately makes no statement about
skill quality, D1/C1 eligibility, cluster membership, prompt fitness, labels,
or retrieval results.  The original 2026-08-29 source frame is read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


BOUNDARY = (
    "Additive versioned source-frame amendment only. Every record is a "
    "byte-distinct publicly retrieved original whose local bytes were rehashed. "
    "Admission here is not D1/C1 eligibility, a cluster, a prompt, a label, a "
    "selector condition, a metric, or a scientific result."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--novel-manifest", type=Path, required=True)
    parser.add_argument("--frozen-source-manifest", type=Path, action="append", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--source-id-prefix", default="RQ1B-V3-W9-SRC")
    parser.add_argument("--status-prefix", default="RQ1B_V3_D1_W9")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_hash(row: dict) -> str:
    canonical = row.get("canonical")
    if isinstance(canonical, dict) and canonical.get("source_sha256"):
        return str(canonical["source_sha256"])
    return str(row.get("sha256") or row.get("source_sha256") or "")


def main() -> int:
    args = parse_args()
    novel = read_jsonl(args.novel_manifest)
    frozen = [row for path in args.frozen_source_manifest for row in read_jsonl(path)]
    frozen_hashes = {source_hash(row) for row in frozen}
    if "" in frozen_hashes:
        raise SystemExit("invalid_frozen_source_manifest")

    failures: list[dict] = []
    accepted: list[dict] = []
    seen_hashes: set[str] = set()
    source_urls: Counter[str] = Counter()

    for index, row in enumerate(novel, start=1):
        local_path = Path(row["local_raw_path"])
        expected_hash = row["source_sha256"]
        actual_hash = sha256_file(local_path) if local_path.is_file() else None
        source_urls[row["raw_artifact_url"]] += 1

        problems: list[str] = []
        if actual_hash is None:
            problems.append("missing_local_raw_artifact")
        elif actual_hash != expected_hash:
            problems.append("local_byte_hash_mismatch")
        if expected_hash in frozen_hashes:
            problems.append("duplicate_of_frozen_frame")
        if expected_hash in seen_hashes:
            problems.append("duplicate_within_w9_novel_manifest")
        if problems:
            failures.append(
                {
                    "provisional_source_id": row.get("provisional_source_id"),
                    "source_sha256": expected_hash,
                    "problems": problems,
                }
            )
            continue

        seen_hashes.add(expected_hash)
        accepted.append(
            {
                "amendment_source_id": f"{args.source_id_prefix}-{index:04d}",
                "byte_count": row["byte_count"],
                "canonical": {
                    "artifact_path": row["artifact_path"],
                    "local_raw_path": row["local_raw_path"],
                    "raw_artifact_url": row["raw_artifact_url"],
                    "repository_ref": row["repository_ref"],
                    "source_sha256": expected_hash,
                },
                # W9 records used `lane`; later intake waves preserve the
                # same provenance under the less ambiguous `intake_lane`.
                "intake_lane": row.get("intake_lane") or row["lane"],
                "origin_url": row["origin_url"],
                "provisional_source_id": row["provisional_source_id"],
                "source_status": f"{args.status_prefix}_PUBLIC_ORIGINAL_BYTE_DISTINCT_SOURCE_FRAME_AMENDMENT_ONLY",
            }
        )

    duplicate_urls = sorted(url for url, count in source_urls.items() if count > 1)
    if duplicate_urls:
        failures.append({"problems": ["duplicate_raw_artifact_url"], "urls": duplicate_urls})

    args.output_root.mkdir(parents=True, exist_ok=True)
    amendment_path = args.output_root / "canonical_sources_amendment.jsonl"
    with amendment_path.open("w", encoding="utf-8") as handle:
        for row in accepted:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    report = {
        "boundary": BOUNDARY,
        "frozen_source_frame_record_count": len(frozen),
        "input_novel_manifest_record_count": len(novel),
        "accepted_amendment_source_count": len(accepted),
        "failure_count": len(failures),
        "failures": failures,
        "status": (
            f"{args.status_prefix}_SOURCE_FRAME_AMENDMENT_FREEZE_PASS_NOT_A_CLUSTER"
            if not failures
            else f"{args.status_prefix}_SOURCE_FRAME_AMENDMENT_FREEZE_FAIL_NOT_A_CLUSTER"
        ),
    }
    write_json(args.output_root / "source_frame_amendment_report.json", report)
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
