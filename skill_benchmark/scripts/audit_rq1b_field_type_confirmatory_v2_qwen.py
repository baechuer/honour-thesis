#!/usr/bin/env python3
"""Validate a completed RQ1b v2 Qwen embedding run locally."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import FIELDS
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze
from run_rq1b_field_type_confirmatory_v2_bm25 import CONDITIONS, FIELD_CONDITIONS, load_strict_families


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--payload-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--authorisation", type=Path, required=True)
    args = parser.parse_args()

    verify_freeze(args.root)
    payload_path = args.payload_dir / "payload.json"
    payload = json.loads(payload_path.read_text())
    authorisation = json.loads(args.authorisation.read_text())
    manifest = json.loads((args.output_dir / "manifest.json").read_text())
    summary = json.loads((args.output_dir / "summary.json").read_text())
    rows = [json.loads(line) for line in (args.output_dir / "rows.jsonl").read_text().splitlines() if line]

    if manifest.get("status") != "RQ1B_FIELD_TYPE_V2_QWEN_RUN_EXTERNAL_RESULT":
        raise ValueError("unexpected Qwen manifest status")
    if manifest.get("payload_sha256") != sha256_file(payload_path):
        raise ValueError("payload hash mismatch")
    if manifest.get("authorisation_sha256") != sha256_file(args.authorisation):
        raise ValueError("authorisation hash mismatch")
    for artifact in ("rows.jsonl", "summary.json"):
        if manifest.get("artifacts", {}).get(artifact) != sha256_file(args.output_dir / artifact):
            raise ValueError(f"artifact hash mismatch: {artifact}")
    execution = manifest.get("execution", {})
    if execution.get("request_attempts") != execution.get("successful_calls"):
        raise ValueError("a failed or retried Qwen request is present")
    if execution.get("request_attempts", 0) > authorisation["maximum_request_attempts"]:
        raise ValueError("request ceiling exceeded")
    if execution.get("successful_calls", 0) > authorisation["maximum_successful_calls"]:
        raise ValueError("successful-call ceiling exceeded")
    if execution.get("cache_misses", 0) > authorisation["maximum_new_texts"]:
        raise ValueError("new-text ceiling exceeded")
    receipts = sorted((args.output_dir / "requests").glob("*_receipt.json"))
    attempts = sorted((args.output_dir / "requests").glob("*_attempt.json"))
    failures = sorted((args.output_dir / "requests").glob("*_failure.json"))
    if len(receipts) != execution.get("successful_calls") or len(attempts) != execution.get("request_attempts") or failures:
        raise ValueError("request receipt integrity failure")
    if any(json.loads(path.read_text()).get("automatic_retry") is not False for path in attempts):
        raise ValueError("automatic retry flag invalid")

    families, eligible = load_strict_families(args.root)
    expected = {(family["routing_family_id"], variant, condition) for family in families for variant in ("direct", "paraphrase") for condition in CONDITIONS}
    actual = {(row.get("routing_family_id"), row.get("prompt_variant"), row.get("condition")) for row in rows}
    if actual != expected or len(rows) != len(expected) or len(rows) != payload["counts"]["expected_score_rows"]:
        raise ValueError(f"row coverage mismatch: expected {len(expected)}, found {len(rows)}")
    for row in rows:
        ranking = row.get("ranking")
        if row.get("retriever") != "qwen-text-embedding-v4" or not isinstance(ranking, list) or len(ranking) != row.get("candidate_count"):
            raise ValueError("Qwen row schema mismatch")
        labels = [item.get("label") for item in ranking]
        scores = [item.get("score") for item in ranking]
        if labels != sorted(labels, key=lambda label: (-scores[labels.index(label)], label)):
            raise ValueError("ranking order/tie break mismatch")
        if labels[row["gold_rank"] - 1] != row["gold_label"] or row["winner_label"] != labels[0]:
            raise ValueError("gold-rank or winner binding mismatch")
    fields = summary.get("fields")
    if not isinstance(fields, dict) or set(fields) != set(FIELDS):
        raise ValueError("summary field coverage mismatch")
    for field in FIELDS:
        block = fields[field]
        if block.get("condition") != FIELD_CONDITIONS[field] or block.get("routing_family_count") != len(eligible[field]):
            raise ValueError(f"summary eligibility drift: {field}")
        if block.get("prompt_pair_count") != len(eligible[field]) * 2:
            raise ValueError(f"summary prompt count drift: {field}")
    print(json.dumps({"valid": True, "rows": len(rows), "strict_families": len(families), "field_counts": {field: len(ids) for field, ids in eligible.items()}, "request_attempts": execution["request_attempts"], "successful_calls": execution["successful_calls"], "cache_misses": execution["cache_misses"]}, sort_keys=True))


if __name__ == "__main__":
    main()
