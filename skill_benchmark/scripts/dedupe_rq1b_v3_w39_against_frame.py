#!/usr/bin/env python3
"""Byte-deduplicate Wave 038 one-shot captures against the complete local frame."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SUCCESS = "RQ1B_V3_W39_M3_CAPTURE_PASS_NOT_ADMITTED"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_hash_and_id(row: dict) -> tuple[str, str]:
    canonical = row.get("canonical")
    if isinstance(canonical, dict) and isinstance(canonical.get("source_sha256"), str):
        return canonical["source_sha256"], str(row.get("amendment_source_id") or row.get("source_id") or "UNKNOWN")
    return str(row.get("sha256") or ""), str(row.get("source_id") or row.get("amendment_source_id") or "UNKNOWN")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-manifest", type=Path, required=True)
    parser.add_argument("--base-frame", type=Path, required=True)
    parser.add_argument("--amendment-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    frozen_paths = [args.base_frame] + sorted(args.amendment_root.glob("d1_source_intake_wave_*/source_frame_amendment/canonical_sources_amendment.jsonl"))
    frozen = {}
    for manifest in frozen_paths:
        for row in read_jsonl(manifest):
            digest, source_id = frozen_hash_and_id(row)
            if not digest:
                raise SystemExit(f"invalid_frozen_hash:{manifest}")
            frozen.setdefault(digest, source_id)
    captured = read_jsonl(args.capture_manifest)
    if not captured:
        raise SystemExit("empty_capture_manifest")
    output_root = args.output_root
    if output_root.exists():
        raise SystemExit("refusing_to_overwrite_dedup_output")
    output_root.mkdir(parents=True)
    capture_root = args.capture_manifest.parent
    novel, aliases, seen = [], [], {}
    failures = []
    for row in captured:
        if row.get("status") != SUCCESS:
            continue
        raw_path = capture_root / str(row.get("relative_capture_path", ""))
        digest = str(row.get("sha256", ""))
        if not raw_path.is_file() or sha256_file(raw_path) != digest:
            failures.append(f"capture_hash_mismatch:{row.get('capture_id')}")
            continue
        if digest in frozen:
            aliases.append({"status": "RQ1B_V3_W39_ALREADY_FROZEN_BYTE_ALIAS_NOT_A_CLUSTER", "capture_id": row["capture_id"], "source_sha256": digest, "existing_source_id": frozen[digest], "root": row["root"], "repository_path": row["repository_path"]})
        elif digest in seen:
            aliases.append({"status": "RQ1B_V3_W39_WITHIN_WAVE_BYTE_ALIAS_NOT_A_CLUSTER", "capture_id": row["capture_id"], "source_sha256": digest, "canonical_provisional_source_id": seen[digest]["provisional_source_id"], "root": row["root"], "repository_path": row["repository_path"]})
        else:
            item = {"status": "RQ1B_V3_W39_NOVEL_RETRIEVED_PUBLIC_ORIGINAL_AWAITING_SOURCE_FRAME_AMENDMENT", "provisional_source_id": f"RQ1B-V3-W39-INTAKE-{len(novel) + 1:04d}", "capture_id": row["capture_id"], "intake_lane": row["domain"], "origin_url": row["root"], "repository_ref": f"{row['root'].removeprefix('https://github.com/')}@{row['commit_sha']}", "artifact_path": row["repository_path"], "raw_artifact_url": row["raw_url"], "source_sha256": digest, "byte_count": row["byte_count"], "local_raw_path": raw_path.as_posix()}
            novel.append(item)
            seen[digest] = item
    non_success = [row for row in captured if row.get("status") != SUCCESS]
    (output_root / "novel_retrieved_sources.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in novel), encoding="utf-8")
    (output_root / "already_frozen_aliases.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in aliases), encoding="utf-8")
    report = {"status": "RQ1B_V3_W39_DEDUP_PASS_NOT_A_CLUSTER" if not failures else "RQ1B_V3_W39_DEDUP_FAIL_NOT_A_CLUSTER", "retrieval_record_count": len(captured), "retrieved_success_count": len(captured) - len(non_success), "non_successful_retrieval_count": len(non_success), "novel_byte_distinct_source_count": len(novel), "already_frozen_byte_duplicate_count": sum(row["status"] == "RQ1B_V3_W39_ALREADY_FROZEN_BYTE_ALIAS_NOT_A_CLUSTER" for row in aliases), "within_wave_byte_alias_count": sum(row["status"] == "RQ1B_V3_W39_WITHIN_WAVE_BYTE_ALIAS_NOT_A_CLUSTER" for row in aliases), "frozen_manifest_count": len(frozen_paths), "frozen_hash_count": len(frozen), "failures": failures, "network_calls": 0, "claim_boundary": "Byte-level source deduplication only. Novel sources await a separate source-frame amendment and have no triage, cluster, prompt, label, selector, metric or result status."}
    (output_root / "dedup_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("novel_byte_distinct_source_count", "already_frozen_byte_duplicate_count", "within_wave_byte_alias_count", "frozen_manifest_count")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
