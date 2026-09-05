#!/usr/bin/env python3
"""Validate the frozen V3 blinded QA outputs and write its single pass/fail decision."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new


VERSION_ID = "rq2b-i3c-v3-2026-08-18"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
QA_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa_calibrated_v1"
MANIFEST = f"{QA_ROOT}/manifest.json"
RECEIPT = f"{QA_ROOT}/manual_qa_completion_approval_receipt.json"
EXPECTED_PACKET_SHA256 = "1990b6a46b27e16c539ac131814ad64b63eed34fbdc89695422ee47d71fa6bcb"
FIELD_KEYS = {
    "use_conditions", "input_preconditions", "output_artifacts", "workflow_steps",
    "success_criteria", "constraints_boundaries", "dependencies_resources",
}
ERROR_CODES = {
    "evidence_not_exact", "benchmark_scaffold_leakage", "wrong_operational_field",
    "missing_selection_critical_content", "generic_or_misleading_selector_span", "other",
}
COMPLETED_KEYS = {
    "review_id", "review_status", "critical_error", "major_error", "major_error_fields",
    "error_codes", "reviewer_notes", "reviewer_id",
}


def require_approved(root: Path) -> tuple[Path, dict[str, Any]]:
    manifest_path = root / MANIFEST
    receipt = read_json(root / RECEIPT)
    manifest = read_json(manifest_path)
    require(sha256_file(manifest_path) == EXPECTED_PACKET_SHA256, "frozen V3 QA packet hash drift")
    require(receipt["state"] == "explicitly_approved_for_v3_calibrated_manual_qa_once", "manual QA is not approved")
    require(receipt["approved_packet"]["sha256"] == EXPECTED_PACKET_SHA256, "approval receipt does not bind this packet")
    require(manifest["state"] == "frozen_calibration_pending_manual_qa_authorisation", "unexpected V3 QA state")
    require(manifest["manual_qa_completion_authorized"] is False, "packet itself must remain immutable and pre-review")
    return root / QA_ROOT, manifest


def validate_row(row: dict[str, Any], expected_id: str, reviewer_id: str) -> None:
    require(set(row) == COMPLETED_KEYS, f"review schema mismatch: {expected_id}")
    require(row["review_id"] == expected_id and row["review_status"] == "completed", f"review identity/status mismatch: {expected_id}")
    require(row["reviewer_id"] == reviewer_id, f"reviewer identity mismatch: {expected_id}")
    require(isinstance(row["critical_error"], bool) and isinstance(row["major_error"], bool), f"review booleans invalid: {expected_id}")
    require(isinstance(row["major_error_fields"], list) and len(row["major_error_fields"]) == len(set(row["major_error_fields"])) and set(row["major_error_fields"]).issubset(FIELD_KEYS), f"major fields invalid: {expected_id}")
    require(isinstance(row["error_codes"], list) and len(row["error_codes"]) == len(set(row["error_codes"])) and set(row["error_codes"]).issubset(ERROR_CODES), f"error codes invalid: {expected_id}")
    require(bool(row["major_error_fields"]) == row["major_error"], f"major field flag mismatch: {expected_id}")
    require((row["critical_error"] or row["major_error"]) == bool(row["error_codes"]), f"error-code flag mismatch: {expected_id}")
    require(isinstance(row["reviewer_notes"], str) and len(row["reviewer_notes"]) <= 4000, f"review notes invalid: {expected_id}")


def calibration_status(root: Path, qa_root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    answer_ref = manifest["artifacts"]["calibration_answer_key_do_not_give_reviewer"]
    answers = read_jsonl(root / answer_ref["path"])
    answer_ids = [row["review_id"] for row in answers]
    require(len(answers) == manifest["calibration_size"] == 8 and len(answer_ids) == len(set(answer_ids)), "calibration answer key mismatch")
    answer_by_id = {row["review_id"]: row for row in answers}
    slots: list[dict[str, Any]] = []
    for batch in manifest["batches"]:
        index = batch["batch_index"]
        reviewer_id = f"rq2b-v3-i3c-calibrated-slot-{index:03d}"
        path = qa_root / "calibration_outputs" / f"calibration_{index:03d}_completed.jsonl"
        require(path.is_file(), f"missing calibration output: batch {index}")
        rows = read_jsonl(path)
        require([row.get("review_id") for row in rows] == answer_ids, f"calibration ordering mismatch: batch {index}")
        for row in rows:
            validate_row(row, row["review_id"], reviewer_id)
            expected = answer_by_id[row["review_id"]]
            for key in ("critical_error", "major_error", "major_error_fields", "error_codes"):
                require(row[key] == expected[key], f"calibration mismatch batch {index}: {row['review_id']}:{key}")
        slots.append({"batch_index": index, "reviewer_id": reviewer_id, "output_path": relative(path, root), "output_sha256": sha256_file(path), "state": "passed"})
    return {"all_passed": True, "slots": slots}


def finalize(root: Path) -> dict[str, Any]:
    qa_root, manifest = require_approved(root)
    calibration = calibration_status(root, qa_root, manifest)
    combined: list[dict[str, Any]] = []
    for batch in manifest["batches"]:
        index = batch["batch_index"]
        input_path = root / batch["input_path"]
        require(input_path.is_file() and sha256_file(input_path) == batch["input_sha256"], f"batch input drift: {index}")
        reviewer_id = f"rq2b-v3-i3c-calibrated-slot-{index:03d}"
        output_path = qa_root / "review_batches" / "outputs" / f"review_batch_{index:03d}_completed.jsonl"
        require(output_path.is_file(), f"missing review output: batch {index}")
        rows = read_jsonl(output_path)
        require(len(rows) == batch["expected_rows"] and [row.get("review_id") for row in rows] == batch["review_ids"], f"review order/count mismatch: batch {index}")
        for row in rows:
            validate_row(row, row["review_id"], reviewer_id)
        combined.extend(rows)
    reviewer_ref = manifest["artifacts"]["blinded_reviewer_packet"]
    reviewer_rows = read_jsonl(root / reviewer_ref["path"])
    require([row["review_id"] for row in combined] == [row["review_id"] for row in reviewer_rows], "reviewed IDs differ from frozen packet")
    completed_path = qa_root / "review_form_completed.jsonl"
    decision_path = qa_root / "manual_qa_decision.json"
    checkpoint_path = qa_root / "manual_qa_completion_checkpoint.json"
    require(not completed_path.exists() and not decision_path.exists() and not checkpoint_path.exists(), "refusing to overwrite V3 QA decision")
    write_jsonl_new(completed_path, combined)
    critical = sum(int(row["critical_error"]) for row in combined)
    major = sum(int(row["major_error"]) for row in combined)
    by_field: Counter[str] = Counter(field for row in combined for field in row["major_error_fields"])
    by_code: Counter[str] = Counter(code for row in combined for code in row["error_codes"])
    passed = critical == 0 and major <= 6
    decision = {
        "schema_version": "rq2b-i3c-v3-calibrated-qa-decision-v1",
        "version_id": VERSION_ID,
        "state": "manual_qa_passed_retrieval_still_requires_separate_authorisation" if passed else "manual_qa_failed_retrieval_blocked",
        "retrieval_ready": passed,
        "qa_manifest": {"path": relative(root / MANIFEST, root), "sha256": EXPECTED_PACKET_SHA256},
        "approval_receipt": {"path": relative(root / RECEIPT, root), "sha256": sha256_file(root / RECEIPT)},
        "calibration": calibration,
        "completed_review_form": {"path": relative(completed_path, root), "sha256": sha256_file(completed_path), "rows": len(combined)},
        "acceptance": {
            "critical_error_rows": critical,
            "major_error_rows": major,
            "major_error_rate": major / len(combined),
            "threshold": {"critical_error_rows": 0, "maximum_major_error_rows": 6},
            "major_error_rows_by_field_descriptive_only": dict(sorted(by_field.items())),
            "error_codes": dict(sorted(by_code.items())),
        },
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "next_gate": "separate B1L local BM25 execution authorisation" if passed else "stop; report the source-grounded QA failure without automatic re-review",
    }
    write_json_new(decision_path, decision)
    checkpoint = {
        "schema_version": "rq2b-i3c-v3-calibrated-qa-completion-checkpoint-v1",
        "version_id": VERSION_ID,
        "state": decision["state"],
        "decision": {"path": relative(decision_path, root), "sha256": sha256_file(decision_path)},
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
    }
    write_json_new(checkpoint_path, checkpoint)
    return decision


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(finalize(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
