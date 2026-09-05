#!/usr/bin/env python3
"""Locally finish a completed RQ1b v2.1 Qwen run from persisted receipts and cache only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from prepare_rq1b_joint_field_mask_v21 import CONDITIONS, load_joint_condition, load_joint_scope
from run_rq1b_field_type_confirmatory_v2_bm25 import metric_for_ranking
from run_rq1b_field_type_confirmatory_v2_qwen import cache_load, cosine
from run_rq1b_joint_field_mask_v21_bm25 import summarize


FINALIZER_VERSION = "rq1b-joint-field-mask-v21-qwen-cache-finalizer-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt_execution(output_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    request_dir = output_dir / "requests"
    attempts = sorted(request_dir.glob("*_attempt.json"))
    receipts = sorted(request_dir.glob("*_receipt.json"))
    failures = sorted(request_dir.glob("*_failure.json"))
    expected_calls = payload["counts"]["maximum_request_attempts_no_retry"]
    if len(attempts) != expected_calls or len(receipts) != expected_calls or failures:
        raise ValueError("cannot finalise: Qwen receipt set is incomplete or failed")
    attempt_rows = [json.loads(path.read_text()) for path in attempts]
    receipt_rows = [json.loads(path.read_text()) for path in receipts]
    if any(row.get("automatic_retry") is not False for row in attempt_rows):
        raise ValueError("cannot finalise: automatic retry evidence present")
    if any(row.get("state") != "success" for row in receipt_rows):
        raise ValueError("cannot finalise: unsuccessful receipt")
    receipt_ids = [identifier for row in receipt_rows for identifier in row.get("text_ids", [])]
    document_ids = {
        row["text_id"]
        for row in payload["text_inventory"]
        if any(role["kind"] == "document" for role in row["roles"])
    }
    # The preflight establishes that only 402 document cards were cache misses; queries were already cached.
    if (
        not set(receipt_ids).issubset(document_ids)
        or len(receipt_ids) != payload["counts"]["new_document_texts"]["texts"]
        or len(set(receipt_ids)) != len(receipt_ids)
    ):
        raise ValueError("cannot finalise: receipt text IDs do not match the authorised new document-card payload")
    usage: dict[str, int] = {}
    for receipt in receipt_rows:
        for key, value in (receipt.get("provider_usage") or {}).items():
            if isinstance(value, int):
                usage[key] = usage.get(key, 0) + value
    return {
        "cache_hits": payload["counts"]["cache_hits"]["texts"],
        "cache_misses": payload["counts"]["cache_misses"]["texts"],
        "request_attempts": len(attempts),
        "successful_calls": len(receipts),
        "provider_usage": usage,
        "recovered_from_completed_receipts": True,
    }


def run(payload_dir: Path, cache_root: Path, output_dir: Path, authorisation: Path) -> dict[str, Any]:
    payload_path = payload_dir / "payload.json"
    payload = json.loads(payload_path.read_text())
    auth = json.loads(authorisation.read_text())
    if payload.get("status") != "RQ1B_JOINT_FIELD_MASK_V21_QWEN_PAYLOAD_LOCAL_PREFLIGHT_NOT_EXECUTED":
        raise ValueError("unexpected payload status")
    if any((output_dir / name).exists() for name in ("rows.jsonl", "summary.json", "manifest.json")):
        raise ValueError("refusing to overwrite an existing Qwen result")
    if auth.get("payload_sha256") != sha256_file(payload_path):
        raise ValueError("authorisation/payload binding drift")
    execution = receipt_execution(output_dir, payload)
    joint_root = Path(payload["joint_root"])
    if payload.get("joint_freeze_sha256") != sha256_file(joint_root / "joint_mask_freeze.json"):
        raise ValueError("joint freeze binding drift")
    freeze, _, families, eligible = load_joint_scope(joint_root)
    inventory = {row["text_id"]: row for row in payload["text_inventory"]}
    vectors: dict[str, list[float]] = {}
    for identifier, row in inventory.items():
        vector = cache_load(cache_root, row)
        if vector is None:
            raise ValueError(f"missing cached vector: {identifier}")
        vectors[identifier] = vector
    documents = {
        (row["composition_id"], row["condition"], row["candidate_label"]): row["text_id"]
        for row in payload["documents"]
    }
    queries = {(row["routing_family_id"], row["prompt_variant"]): row["text_id"] for row in payload["queries"]}
    rows: list[dict[str, Any]] = []
    for family in families:
        for variant in ("direct", "paraphrase"):
            query_vector = vectors[queries[(family["routing_family_id"], variant)]]
            for condition in CONDITIONS:
                cards = load_joint_condition(joint_root, freeze, family["composition_id"], condition)
                ranking = sorted(
                    ((card["label"], cosine(query_vector, vectors[documents[(family["composition_id"], condition, card["label"])]])) for card in cards),
                    key=lambda item: (-item[1], item[0]),
                )
                rows.append({
                    "status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_ROW_EXTERNAL_RESULT",
                    "retriever": "qwen-text-embedding-v4",
                    "routing_family_id": family["routing_family_id"],
                    "composition_id": family["composition_id"],
                    "prompt_variant": variant,
                    "condition": condition,
                    "gold_label": family["gold_label"],
                    "candidate_count": len(cards),
                    "query_seconds": None,
                    **metric_for_ranking(ranking, family["gold_label"]),
                })
    if len(rows) != payload["counts"]["expected_score_rows"]:
        raise ValueError("score-row coverage mismatch")
    summary = summarize(rows, eligible)
    rows_path, summary_path, manifest_path = (output_dir / "rows.jsonl", output_dir / "summary.json", output_dir / "manifest.json")
    rows_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    manifest = {
        "status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_RUN_EXTERNAL_RESULT",
        "runner_version": FINALIZER_VERSION,
        "payload_sha256": sha256_file(payload_path),
        "authorisation_sha256": sha256_file(authorisation),
        "execution": execution,
        "artifacts": {"rows.jsonl": sha256_file(rows_path), "summary.json": sha256_file(summary_path)},
        "thesis_results_written": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload-dir", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--authorisation", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.payload_dir, args.cache_root, args.output_dir, args.authorisation), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
