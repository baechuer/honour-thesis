#!/usr/bin/env python3
"""Validate calibrated blinded QA and issue the only v1.2 retrieval-readiness decision."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
DEFAULT_QA_DIRECTORY = "i3c_manual_qa_calibrated_v2"
FIELD_KEYS = {"use_conditions", "input_preconditions", "output_artifacts", "workflow_steps", "dependencies_resources", "constraints_boundaries", "success_criteria"}
COMPLETED_KEYS = {"review_id", "review_status", "critical_error", "major_error", "major_error_fields", "error_codes", "reviewer_notes", "reviewer_id"}
ERROR_CODES = {"evidence_not_exact", "benchmark_scaffold_leakage", "wrong_operational_field", "missing_selection_critical_content", "generic_or_misleading_selector_span", "other"}


def validate_row(row: dict[str, Any], expected_id: str, reviewer_id: str) -> None:
    require(set(row) == COMPLETED_KEYS, f"review schema mismatch: {expected_id}")
    require(row["review_id"] == expected_id and row["review_status"] == "completed", f"review identity/status mismatch: {expected_id}")
    require(row["reviewer_id"] == reviewer_id, f"reviewer identity mismatch: {expected_id}")
    require(isinstance(row["critical_error"], bool) and isinstance(row["major_error"], bool), f"review booleans missing: {expected_id}")
    require(isinstance(row["major_error_fields"], list) and len(row["major_error_fields"]) == len(set(row["major_error_fields"])) and set(row["major_error_fields"]).issubset(FIELD_KEYS), f"review field attribution invalid: {expected_id}")
    require(isinstance(row["error_codes"], list) and len(row["error_codes"]) == len(set(row["error_codes"])) and set(row["error_codes"]).issubset(ERROR_CODES), f"review error codes invalid: {expected_id}")
    require(bool(row["major_error_fields"]) == row["major_error"], f"major field attribution mismatch: {expected_id}")
    require((row["critical_error"] or row["major_error"]) == bool(row["error_codes"]), f"error code attribution mismatch: {expected_id}")
    require(isinstance(row["reviewer_notes"], str) and len(row["reviewer_notes"]) <= 4000, f"review notes invalid: {expected_id}")


def load_manifest(root: Path, qa_directory: str) -> tuple[Path, dict[str, Any]]:
    require(qa_directory.startswith("i3c_manual_qa_calibrated_") and "/" not in qa_directory, "invalid calibrated QA directory")
    qa_root = root / RELATIVE_ROOT / qa_directory
    manifest_path = qa_root / "manifest.json"
    require(manifest_path.is_file(), "calibrated QA manifest is missing")
    manifest = read_json(manifest_path)
    require(manifest["version_id"] == VERSION_ID and manifest["state"] == "frozen_calibration_pending", "calibrated QA manifest state mismatch")
    for ref in manifest["artifacts"].values():
        path = root / ref["path"]
        require(path.is_file() and sha256_file(path) == ref["sha256"], f"calibrated QA artifact drift: {ref['path']}")
    return qa_root, manifest


def calibration_status(root: Path, qa_directory: str = DEFAULT_QA_DIRECTORY) -> dict[str, Any]:
    qa_root, manifest = load_manifest(root, qa_directory)
    answers = read_jsonl(root / manifest["artifacts"]["calibration_answer_key_do_not_give_reviewer"]["path"])
    by_id = {row["review_id"]: row for row in answers}
    require(len(by_id) == len(answers) == manifest["calibration_size"], "calibration answer key mismatch")
    slots: list[dict[str, Any]] = []
    for batch in manifest["batches"]:
        attempts: list[dict[str, Any]] = []
        for attempt_path in batch.get("calibration_attempt_paths", []):
            output = root / attempt_path
            if not output.is_file():
                attempts.append({"path": attempt_path, "state": "missing"})
                continue
            rows = read_jsonl(output)
            matched = True
            reason = ""
            try:
                require(len(rows) == len(answers), "calibration row count mismatch")
                require([row.get("review_id") for row in rows] == [row["review_id"] for row in answers], "calibration ordering mismatch")
                for row in rows:
                    validate_row(row, row["review_id"], batch["reviewer_id"])
                    expected = by_id[row["review_id"]]
                    for key in ("critical_error", "major_error", "major_error_fields", "error_codes"):
                        require(row[key] == expected[key], f"calibration mismatch {row['review_id']}:{key}")
            except (AssertionError, ValueError, KeyError) as exc:
                matched = False
                reason = str(exc)
            attempts.append({"path": attempt_path, "state": "passed" if matched else "failed", "reason": reason, "output_sha256": sha256_file(output)})
        passing = next((attempt for attempt in attempts if attempt["state"] == "passed"), None)
        slots.append({"batch_index": batch["batch_index"], "reviewer_id": batch["reviewer_id"], "state": "passed" if passing else ("failed" if any(attempt["state"] == "failed" for attempt in attempts) else "missing"), "accepted_attempt": passing, "attempts": attempts})
    return {"all_passed": len(slots) == len(manifest["batches"]) and all(slot["state"] == "passed" for slot in slots), "slots": slots}


def finalize(root: Path, qa_directory: str = DEFAULT_QA_DIRECTORY) -> dict[str, Any]:
    qa_root, manifest = load_manifest(root, qa_directory)
    calibration = calibration_status(root, qa_directory)
    require(calibration["all_passed"], "calibration has not passed for every reviewer slot")
    reviewer_packet = read_jsonl(root / manifest["artifacts"]["blinded_reviewer_packet"]["path"])
    expected_ids = [row["review_id"] for row in reviewer_packet]
    require(len(expected_ids) == len(set(expected_ids)) == manifest["sample_size"], "review packet identity mismatch")
    combined: list[dict[str, Any]] = []
    for batch in manifest["batches"]:
        output = root / batch["output_path"]
        require(output.is_file(), f"review output missing: batch {batch['batch_index']}")
        rows = read_jsonl(output)
        require(len(rows) == batch["expected_rows"] and [row.get("review_id") for row in rows] == batch["review_ids"], f"review output order mismatch: batch {batch['batch_index']}")
        for row in rows:
            validate_row(row, row["review_id"], batch["reviewer_id"])
        combined.extend(rows)
    require([row["review_id"] for row in combined] == expected_ids, "completed review order differs from frozen packet")
    completed_path = qa_root / "review_form_completed.jsonl"
    decision_path = qa_root / "manual_qa_decision.json"
    require(not completed_path.exists() and not decision_path.exists(), "refusing to overwrite calibrated QA decision")
    write_jsonl_new(completed_path, combined)
    critical = sum(int(row["critical_error"]) for row in combined)
    major = sum(int(row["major_error"]) for row in combined)
    by_field: Counter[str] = Counter(field for row in combined for field in row["major_error_fields"])
    by_code: Counter[str] = Counter(code for row in combined for code in row["error_codes"])
    review_pass = critical == 0 and major <= 6
    report = {
        "schema_version": "rq2b-v12-i3c-calibrated-qa-decision-v2",
        "version_id": VERSION_ID,
        "state": "manual_qa_passed_retrieval_ready" if review_pass else "manual_qa_failed_retrieval_blocked",
        "retrieval_ready": review_pass,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "qa_manifest": {"path": relative(qa_root / "manifest.json", root), "sha256": sha256_file(qa_root / "manifest.json")},
        "protocol": manifest["artifacts"]["protocol"],
        "approval_receipt": manifest["artifacts"]["approval_receipt"],
        "calibration": calibration,
        "completed_review_form": {"path": relative(completed_path, root), "sha256": sha256_file(completed_path), "rows": len(combined)},
        "acceptance": {"critical_error_rows": critical, "major_error_rows": major, "major_error_rate": major / len(combined), "threshold": {"critical_error_rows": 0, "maximum_major_error_rows": 6}, "major_error_rows_by_field_descriptive_only": dict(sorted(by_field.items())), "error_codes": dict(sorted(by_code.items()))},
        "next_gate": "B1L local BM25 preflight and bound execution" if review_pass else "corpus correction and fresh source-grounded extraction/QA version",
        "selective_sample_only_repairs_allowed": False,
    }
    write_json_new(decision_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--check-calibration", action="store_true")
    parser.add_argument("--qa-directory", default=DEFAULT_QA_DIRECTORY)
    args = parser.parse_args()
    result = calibration_status(args.root.resolve(), args.qa_directory) if args.check_calibration else finalize(args.root.resolve(), args.qa_directory)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
