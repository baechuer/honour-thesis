#!/usr/bin/env python3
"""Aggregate six completed blind I3C QA batches for RQ2b v1.1.

This is a local QA gate only. A QA pass establishes no retrieval result and
does not authorise BM25, embedding, reranking, external calls, or thesis edits.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import FIELD_SPECS, read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new
from rq2b_v11_contract import RELATIVE_ROOT, VERSION_ID
from build_rq2b_v11_i3c_qa_packet import QA_ROOT, QA_SAMPLE_SIZE, verify as verify_qa_packet
from prepare_rq2b_v11_i3c_qa_batches import BATCH_MANIFEST, BATCH_SIZE, verify as verify_batches


COMPLETED_KEYS = {"sample_index", "review_id", "critical_error", "major_error", "major_error_fields", "error_codes", "reviewer_notes", "reviewer_id"}
FIELD_KEYS = tuple(field for field, _ in FIELD_SPECS)
MAJOR_ERROR_THRESHOLD = 0.05
APPROVAL_RECEIPT = f"{QA_ROOT}/manual_qa_completion_approval_receipt.json"


def validate_review_row(row: dict[str, Any], expected: dict[str, Any], key_row: dict[str, Any]) -> None:
    review_id = expected["review_id"]
    require(set(row) == COMPLETED_KEYS, f"I3C QA completed row keys mismatch: {review_id}")
    require(row.get("sample_index") == expected["sample_index"] and row.get("review_id") == review_id, f"I3C QA row identity mismatch: {review_id}")
    require(isinstance(row["critical_error"], bool) and isinstance(row["major_error"], bool), f"I3C QA error booleans incomplete: {review_id}")
    require(isinstance(row["reviewer_id"], str) and bool(row["reviewer_id"].strip()) and len(row["reviewer_id"]) <= 200, f"I3C QA reviewer ID invalid: {review_id}")
    require(isinstance(row["reviewer_notes"], str) and len(row["reviewer_notes"]) <= 4000, f"I3C QA notes invalid: {review_id}")
    codes = row["error_codes"]
    require(isinstance(codes, list) and len(codes) == len(set(codes)) and all(isinstance(code, str) and bool(code.strip()) and len(code) <= 100 for code in codes), f"I3C QA error codes invalid: {review_id}")
    fields = row["major_error_fields"]
    require(isinstance(fields, list) and len(fields) == len(set(fields)) and set(fields).issubset(FIELD_KEYS), f"I3C QA major fields invalid: {review_id}")
    if row["major_error"]:
        require(bool(fields), f"I3C QA major error lacks field attribution: {review_id}")
    else:
        require(not fields, f"I3C QA non-major error includes field attribution: {review_id}")
    require(set(fields).issubset(set(key_row["present_fields"])), f"I3C QA major field was not present in sample: {review_id}")


def decide(reviews: list[dict[str, Any]], key_rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(len(reviews) == len(key_rows) == QA_SAMPLE_SIZE, "I3C QA requires exactly 120 reviews and key rows")
    keys = {row["review_id"]: row for row in key_rows}
    require(len(keys) == QA_SAMPLE_SIZE, "I3C QA sampling keys not unique")
    require([row["review_id"] for row in reviews] == [row["review_id"] for row in key_rows], "I3C QA final ordering differs from sampling key")
    critical = 0
    major_rows = 0
    reviewers = Counter()
    reviewed_by_field = Counter()
    major_by_field = Counter()
    for row in reviews:
        key = keys[row["review_id"]]
        validate_review_row(row, {"sample_index": key["sample_index"], "review_id": key["review_id"]}, key)
        critical += int(row["critical_error"])
        major_rows += int(row["major_error"])
        reviewers[row["reviewer_id"]] += 1
        for field in key["present_fields"]:
            reviewed_by_field[field] += 1
        for field in row["major_error_fields"]:
            major_by_field[field] += 1
    row_rate = major_rows / QA_SAMPLE_SIZE
    field_rates = {field: major_by_field[field] / reviewed_by_field[field] for field in FIELD_KEYS if reviewed_by_field[field]}
    passed = critical == 0 and row_rate <= MAJOR_ERROR_THRESHOLD and all(rate <= MAJOR_ERROR_THRESHOLD for rate in field_rates.values())
    return {
        "critical_errors": critical,
        "major_error_rows": major_rows,
        "major_error_row_rate": row_rate,
        "major_error_threshold": MAJOR_ERROR_THRESHOLD,
        "reviewed_rows_by_field": dict(reviewed_by_field),
        "major_errors_by_field": dict(major_by_field),
        "major_error_rate_by_field": field_rates,
        "reviewer_row_counts": dict(reviewers),
        "passed": passed,
    }


def finalize(root: Path) -> dict[str, Any]:
    verify_qa_packet(root)
    verify_batches(root, allow_completed_outputs=True)
    qa_root = root / QA_ROOT
    qa_manifest_path = qa_root / "manifest.json"
    batch_manifest_path = root / BATCH_MANIFEST
    receipt_path = root / APPROVAL_RECEIPT
    require(receipt_path.is_file(), "I3C QA completion approval receipt is missing")
    receipt = read_json(receipt_path)
    require(receipt.get("state") == "explicitly_approved_for_v11_i3c_manual_qa_once", "I3C QA completion is not approved")
    require(receipt.get("qa_packet_manifest") == {"path": relative(qa_manifest_path, root), "sha256": sha256_file(qa_manifest_path)}, "I3C QA receipt packet binding drift")
    require(receipt.get("batch_manifest") == {"path": relative(batch_manifest_path, root), "sha256": sha256_file(batch_manifest_path)}, "I3C QA receipt batch binding drift")
    batch_manifest = read_json(batch_manifest_path)
    qa_packet = read_json(qa_manifest_path)
    key_ref = qa_packet["artifacts"]["sampling_key"]
    key_rows = read_jsonl(root / key_ref["path"])
    require(sha256_file(root / key_ref["path"]) == key_ref["sha256"], "I3C QA sampling key drift")
    combined: list[dict[str, Any]] = []
    for batch in batch_manifest["batches"]:
        output_path = root / batch["output_path"]
        require(output_path.is_file(), f"I3C QA output is missing: {batch['batch_index']}")
        rows = read_jsonl(output_path)
        require(len(rows) == BATCH_SIZE, f"I3C QA output row count mismatch: {batch['batch_index']}")
        expected_ids = batch["review_ids"]
        require([row.get("review_id") for row in rows] == expected_ids, f"I3C QA output identity mismatch: {batch['batch_index']}")
        expected_reviewer_id = f"codex-independent-qa-batch-{batch['batch_index']:03d}"
        require(
            all(row.get("reviewer_id") == expected_reviewer_id for row in rows),
            f"I3C QA reviewer identity mismatch: {batch['batch_index']}",
        )
        combined.extend(rows)
    completed_path = qa_root / "review_form_completed.jsonl"
    decision_path = qa_root / "manual_qa_decision.json"
    require(not completed_path.exists() and not decision_path.exists(), "Refusing to overwrite I3C QA finalization")
    write_jsonl_new(completed_path, combined)
    result = decide(combined, key_rows)
    report = {
        "schema_version": "rq2b-v11-i3c-manual-qa-decision-v1",
        "version_id": VERSION_ID,
        "state": "manual_qa_passed_retrieval_not_yet_authorised" if result["passed"] else "manual_qa_rejected_corpus_wide_correction_required",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "qa_packet_manifest": {"path": relative(qa_manifest_path, root), "sha256": sha256_file(qa_manifest_path)},
        "batch_manifest": {"path": relative(batch_manifest_path, root), "sha256": sha256_file(batch_manifest_path)},
        "manual_qa_completion_receipt": {"path": relative(receipt_path, root), "sha256": sha256_file(receipt_path)},
        "completed_review_form": {"path": relative(completed_path, root), "sha256": sha256_file(completed_path), "rows": len(combined)},
        "decision": result,
        "retrieval_authorized": False,
        "selective_sample_only_repairs_allowed": False,
    }
    write_json_new(decision_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(finalize(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
