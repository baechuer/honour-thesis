#!/usr/bin/env python3
"""Aggregate six completed blind QA batches for RQ2b v1.2 I3C."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from prepare_rq2b_v12_i3c_qa_batches import BATCH_MANIFEST, BATCH_SIZE, QA_ROOT, VERSION_ID, verify as verify_batches
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new


RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
RECEIPT = f"{QA_ROOT}/manual_qa_completion_approval_receipt.json"
QA_SAMPLE_SIZE = 120
FIELD_KEYS = {"use_conditions", "input_preconditions", "output_artifacts", "workflow_steps", "success_criteria", "constraints_boundaries", "dependencies_resources"}
COMPLETED_KEYS = {"review_id", "review_status", "critical_error", "major_error", "major_error_fields", "error_codes", "reviewer_notes", "reviewer_id"}
ERROR_CODES = {"unsupported_content", "identity_mismatch", "evidence_not_exact", "evidence_not_meaningful", "missing_material_field", "misclassified_field", "misleading_selector_span", "benchmark_scaffold_leakage", "other"}


def validate_row(row: dict[str, Any], expected: dict[str, Any]) -> None:
    review_id = expected["review_id"]
    require(set(row) == COMPLETED_KEYS and row["review_id"] == review_id, f"v1.2 QA row schema/identity mismatch: {review_id}")
    require(row["review_status"] == "completed", f"v1.2 QA row is not completed: {review_id}")
    require(isinstance(row["critical_error"], bool) and isinstance(row["major_error"], bool), f"v1.2 QA error booleans incomplete: {review_id}")
    require(isinstance(row["reviewer_id"], str) and row["reviewer_id"].strip() and len(row["reviewer_id"]) <= 200, f"v1.2 QA reviewer identity invalid: {review_id}")
    require(isinstance(row["reviewer_notes"], str) and len(row["reviewer_notes"]) <= 4000, f"v1.2 QA notes invalid: {review_id}")
    require(isinstance(row["error_codes"], list) and len(row["error_codes"]) == len(set(row["error_codes"])) and set(row["error_codes"]).issubset(ERROR_CODES), f"v1.2 QA error codes invalid: {review_id}")
    fields = row["major_error_fields"]
    require(isinstance(fields, list) and len(fields) == len(set(fields)) and set(fields).issubset(FIELD_KEYS), f"v1.2 QA major fields invalid: {review_id}")
    require(bool(fields) == row["major_error"], f"v1.2 QA major field attribution mismatch: {review_id}")
    require((row["critical_error"] or row["major_error"]) == bool(row["error_codes"]), f"v1.2 QA error-code attribution mismatch: {review_id}")


def decision(reviews: list[dict[str, Any]], key_rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(len(reviews) == len(key_rows) == QA_SAMPLE_SIZE, "v1.2 QA requires exactly 120 reviewed rows")
    key_by_id = {row["review_id"]: row for row in key_rows}
    require(len(key_by_id) == QA_SAMPLE_SIZE and [row["review_id"] for row in reviews] == [row["review_id"] for row in key_rows], "v1.2 QA final ordering differs from sampling key")
    critical = major_rows = 0
    reviewers: Counter[str] = Counter()
    reviewed_by_field: Counter[str] = Counter()
    major_by_field: Counter[str] = Counter()
    for row in reviews:
        validate_row(row, key_by_id[row["review_id"]])
        critical += int(row["critical_error"])
        major_rows += int(row["major_error"])
        reviewers[row["reviewer_id"]] += 1
        for field in key_by_id[row["review_id"]]["present_fields"]:
            reviewed_by_field[field] += 1
        for field in row["major_error_fields"]:
            major_by_field[field] += 1
    row_rate = major_rows / QA_SAMPLE_SIZE
    # A reviewer may correctly attribute a missing-field error to a field that
    # has no extracted item. Therefore extracted-field coverage is not a valid
    # denominator for a field-attribution rate. The v1.2 packet also does not
    # bind an acceptance threshold, so this function reports raw QA evidence
    # only; a later frozen protocol must interpret it.
    return {
        "critical_errors": critical,
        "major_error_rows": major_rows,
        "major_error_row_rate": row_rate,
        "reviewed_rows_by_extracted_field": dict(reviewed_by_field),
        "major_error_rows_attributed_by_field": dict(major_by_field),
        "major_error_attribution_rate_by_field_total_sample": {
            field: major_by_field[field] / QA_SAMPLE_SIZE for field in sorted(major_by_field)
        },
        "reviewer_row_counts": dict(reviewers),
        "acceptance_decision": "not_computable_without_a_frozen_v12_rubric_and_threshold",
    }


def finalize(root: Path) -> dict[str, Any]:
    verify_batches(root, allow_completed_outputs=True)
    qa_root = root / QA_ROOT
    receipt_path = root / RECEIPT
    batch_manifest_path = root / BATCH_MANIFEST
    require(receipt_path.is_file(), "v1.2 manual-QA completion receipt is missing")
    receipt = read_json(receipt_path)
    require(receipt["state"] == "explicitly_approved_for_v12_i3c_manual_qa_once", "v1.2 manual QA is not approved")
    require(receipt["qa_packet_manifest"] == {"path": relative(qa_root / "manifest.json", root), "sha256": sha256_file(qa_root / "manifest.json")}, "v1.2 QA receipt packet binding drift")
    require(receipt["batch_manifest"] == {"path": relative(batch_manifest_path, root), "sha256": sha256_file(batch_manifest_path)}, "v1.2 QA receipt batch binding drift")
    packet = read_json(qa_root / "manifest.json")
    key_ref = packet["artifacts"]["sampling_key_do_not_give_reviewer"]
    key_rows = read_jsonl(root / key_ref["path"])
    require(sha256_file(root / key_ref["path"]) == key_ref["sha256"], "v1.2 sampling key drift")
    batches = read_json(batch_manifest_path)["batches"]
    combined: list[dict[str, Any]] = []
    for batch in batches:
        output_path = root / batch["output_path"]
        require(output_path.is_file(), f"v1.2 QA output missing: {batch['batch_index']}")
        rows = read_jsonl(output_path)
        require(len(rows) == BATCH_SIZE and [row.get("review_id") for row in rows] == batch["review_ids"], f"v1.2 QA batch output identity mismatch: {batch['batch_index']}")
        expected_reviewer = f"codex-v12-i3c-qa-batch-{batch['batch_index']:03d}"
        require(all(row.get("reviewer_id") == expected_reviewer for row in rows), f"v1.2 QA reviewer identity mismatch: {batch['batch_index']}")
        combined.extend(rows)
    completed_path = qa_root / "review_form_completed.jsonl"
    decision_path = qa_root / "manual_qa_decision.json"
    require(not completed_path.exists() and not decision_path.exists(), "refusing to overwrite v1.2 QA finalization")
    write_jsonl_new(completed_path, combined)
    result = decision(combined, key_rows)
    report = {
        "schema_version": "rq2b-v12-i3c-manual-qa-decision-v1",
        "version_id": VERSION_ID,
        "state": "manual_qa_reviews_complete_acceptance_criterion_not_bound",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "qa_packet_manifest": {"path": relative(qa_root / "manifest.json", root), "sha256": sha256_file(qa_root / "manifest.json")},
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
