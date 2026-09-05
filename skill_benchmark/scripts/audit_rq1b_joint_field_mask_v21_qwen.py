#!/usr/bin/env python3
"""Audit a completed RQ1b v2.1 joint-mask Qwen run locally."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from prepare_rq1b_joint_field_mask_v21 import CONDITIONS, GROUPS, load_joint_scope


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--joint-root", type=Path, required=True)
    parser.add_argument("--payload-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--authorisation", type=Path, required=True)
    args = parser.parse_args()
    _, _, families, eligible = load_joint_scope(args.joint_root)
    payload_path = args.payload_dir / "payload.json"
    payload = json.loads(payload_path.read_text())
    authorisation = json.loads(args.authorisation.read_text())
    manifest = json.loads((args.output_dir / "manifest.json").read_text())
    summary = json.loads((args.output_dir / "summary.json").read_text())
    rows = [json.loads(line) for line in (args.output_dir / "rows.jsonl").read_text().splitlines() if line]
    if manifest.get("status") != "RQ1B_JOINT_FIELD_MASK_V21_QWEN_RUN_EXTERNAL_RESULT":
        raise ValueError("unexpected joint Qwen manifest status")
    if manifest.get("payload_sha256") != sha256_file(payload_path) or manifest.get("authorisation_sha256") != sha256_file(args.authorisation):
        raise ValueError("joint Qwen provenance hash mismatch")
    for artifact in ("rows.jsonl", "summary.json"):
        if manifest.get("artifacts", {}).get(artifact) != sha256_file(args.output_dir / artifact):
            raise ValueError(f"joint Qwen artifact hash mismatch: {artifact}")
    execution = manifest.get("execution", {})
    if execution.get("request_attempts") != execution.get("successful_calls"):
        raise ValueError("failed or retried Qwen request present")
    for key in ("maximum_request_attempts", "maximum_successful_calls"):
        if execution.get("request_attempts" if key == "maximum_request_attempts" else "successful_calls", 0) > authorisation[key]:
            raise ValueError(f"joint Qwen {key} exceeded")
    if execution.get("cache_misses", 0) > authorisation["maximum_new_texts"]:
        raise ValueError("joint Qwen new-text ceiling exceeded")
    receipts = sorted((args.output_dir / "requests").glob("*_receipt.json"))
    attempts = sorted((args.output_dir / "requests").glob("*_attempt.json"))
    failures = sorted((args.output_dir / "requests").glob("*_failure.json"))
    if len(receipts) != execution.get("successful_calls") or len(attempts) != execution.get("request_attempts") or failures:
        raise ValueError("joint Qwen receipt integrity failure")
    if any(json.loads(path.read_text()).get("automatic_retry") is not False for path in attempts):
        raise ValueError("joint Qwen automatic retry violation")
    expected = {(family["routing_family_id"], variant, condition) for family in families for variant in ("direct", "paraphrase") for condition in CONDITIONS}
    actual = {(row.get("routing_family_id"), row.get("prompt_variant"), row.get("condition")) for row in rows}
    if actual != expected or len(rows) != len(expected) or len(rows) != payload["counts"]["expected_score_rows"]:
        raise ValueError("joint Qwen row coverage mismatch")
    for row in rows:
        ranking = row.get("ranking")
        if row.get("retriever") != "qwen-text-embedding-v4" or not isinstance(ranking, list) or len(ranking) != row.get("candidate_count"):
            raise ValueError("joint Qwen row schema mismatch")
        labels = [item.get("label") for item in ranking]
        scores = [item.get("score") for item in ranking]
        if labels != sorted(labels, key=lambda label: (-scores[labels.index(label)], label)) or labels[row["gold_rank"] - 1] != row["gold_label"] or labels[0] != row["winner_label"]:
            raise ValueError("joint Qwen ranking binding mismatch")
    groups = summary.get("groups")
    if not isinstance(groups, dict) or set(groups) != set(GROUPS):
        raise ValueError("joint Qwen summary group coverage mismatch")
    for condition, fields in GROUPS.items():
        block = groups[condition]
        if block.get("withheld_fields") != list(fields) or block.get("routing_family_count") != len(eligible[condition]) or block.get("prompt_pair_count") != len(eligible[condition]) * 2:
            raise ValueError(f"joint Qwen eligibility drift: {condition}")
    print(json.dumps({"valid": True, "rows": len(rows), "request_attempts": execution["request_attempts"], "successful_calls": execution["successful_calls"], "cache_misses": execution["cache_misses"], "group_eligible_families": {condition: len(ids) for condition, ids in eligible.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
