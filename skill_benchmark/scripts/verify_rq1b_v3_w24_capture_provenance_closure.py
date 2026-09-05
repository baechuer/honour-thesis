#!/usr/bin/env python3
"""Independently prove the Wave 024 clean-capture URL-set closure."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line:
            item = json.loads(line)
            if not isinstance(item, dict):
                raise SystemExit(f"jsonl_row_not_object:{path}:{number}")
            rows.append(item)
    return rows


def url(record: dict[str, Any]) -> str:
    value = record.get("raw_artifact_url")
    if not isinstance(value, str) or not value:
        raise ValueError("missing_raw_artifact_url")
    return value


def source_bytes_ok(record: dict[str, Any]) -> bool:
    local = record.get("local_raw_path")
    claimed = record.get("source_sha256")
    if not isinstance(local, str) or not isinstance(claimed, str):
        return False
    path = Path(local)
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == claimed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--incident-raw-manifest", type=Path, required=True)
    parser.add_argument("--incident-single-attempt", type=Path, required=True)
    parser.add_argument("--incident-never-attempted", type=Path, required=True)
    parser.add_argument("--separate-one-shot-manifest", type=Path, required=True)
    parser.add_argument("--clean-merged-manifest", type=Path, required=True)
    parser.add_argument("--expected-status", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    draft = read_jsonl(args.draft)
    incident_raw = read_jsonl(args.incident_raw_manifest)
    incident_single = read_jsonl(args.incident_single_attempt)
    incident_never = read_jsonl(args.incident_never_attempted)
    one_shot = read_jsonl(args.separate_one_shot_manifest)
    merged = read_jsonl(args.clean_merged_manifest)

    failures: list[str] = []
    draft_urls = [url(row) for row in draft]
    if len(set(draft_urls)) != len(draft_urls):
        failures.append("draft_duplicate_urls")
    draft_set = set(draft_urls)

    raw_urls = [url(row) for row in incident_raw]
    raw_counts = Counter(raw_urls)
    if set(raw_counts) - draft_set:
        failures.append("incident_raw_out_of_roster_url")
    singleton_set = {item for item, count in raw_counts.items() if count == 1}
    duplicate_set = {item for item, count in raw_counts.items() if count > 1}
    never_set = draft_set - set(raw_counts)

    provided_single_urls = [url(row) for row in incident_single]
    if len(set(provided_single_urls)) != len(provided_single_urls):
        failures.append("provided_single_duplicate_urls")
    if set(provided_single_urls) != singleton_set:
        failures.append("provided_single_set_mismatch")

    provided_never_urls: list[str] = []
    for row in incident_never:
        draft_row = row.get("draft")
        if not isinstance(draft_row, dict):
            failures.append("provided_never_missing_draft")
            continue
        provided_never_urls.append(url(draft_row))
    if len(set(provided_never_urls)) != len(provided_never_urls):
        failures.append("provided_never_duplicate_urls")
    if set(provided_never_urls) != never_set:
        failures.append("provided_never_set_mismatch")

    one_shot_urls = [url(row) for row in one_shot]
    if len(set(one_shot_urls)) != len(one_shot_urls):
        failures.append("one_shot_duplicate_urls")
    if set(one_shot_urls) != never_set:
        failures.append("one_shot_set_mismatch")
    if any(row.get("status") != args.expected_status for row in one_shot):
        failures.append("one_shot_unexpected_status")

    merged_urls = [url(row) for row in merged]
    if len(set(merged_urls)) != len(merged_urls):
        failures.append("merged_duplicate_urls")
    expected_clean = singleton_set | never_set
    if set(merged_urls) != expected_clean:
        failures.append("merged_set_mismatch")
    if any(row.get("status") != args.expected_status for row in merged):
        failures.append("merged_unexpected_status")
    bad_hash_urls = sorted(url(row) for row in merged if not source_bytes_ok(row))
    if bad_hash_urls:
        failures.append("merged_local_hash_mismatch")

    report = {
        "status": "RQ1B_V3_W24_CAPTURE_PROVENANCE_CLOSURE_" + ("PASS" if not failures else "FAIL") + "_NOT_A_SOURCE_OR_CLUSTER",
        "draft_url_count": len(draft_set),
        "incident_raw_manifest_line_count": len(incident_raw),
        "incident_singleton_url_count": len(singleton_set),
        "incident_duplicate_url_count": len(duplicate_set),
        "incident_never_attempted_url_count": len(never_set),
        "separate_one_shot_url_count": len(set(one_shot_urls)),
        "merged_clean_url_count": len(set(merged_urls)),
        "clean_source_hash_verified_count": len(merged) - len(bad_hash_urls),
        "bad_hash_urls": bad_hash_urls,
        "failures": failures,
        "set_relationship": "merged = incident_exactly_once UNION incident_never_attempted_then_separate_exactly_once; incident_duplicate URLs are excluded",
        "boundary": [
            "This verifies capture provenance and local source bytes only.",
            "It does not establish source quality, source-frame admission quality, D1/C1 eligibility, a cluster, prompt, label, selector, metric or retrieval result.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
