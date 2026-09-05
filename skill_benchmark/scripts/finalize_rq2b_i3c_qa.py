#!/usr/bin/env python3
"""Finalize a completed blinded I3C QA form without mutating frozen outputs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import (
    FIELD_SPECS,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    version_root,
    write_json_new,
)


MAJOR_ERROR_THRESHOLD = 0.05
FIELD_KEYS = tuple(field for field, _ in FIELD_SPECS)
COMPLETED_REVIEW_KEYS = {
    "sample_index",
    "review_id",
    "critical_error",
    "major_error",
    "major_error_fields",
    "error_codes",
    "reviewer_notes",
    "reviewer_id",
}


def decision(
    reviews: list[dict[str, Any]],
    key_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    require(len(reviews) == len(key_rows) == 120, "I3C QA requires exactly 120 reviewed rows")
    key_by_id = {row["review_id"]: row for row in key_rows}
    require(len(key_by_id) == 120, "I3C QA sampling keys are not unique")
    review_ids = [row.get("review_id") for row in reviews]
    require(len(set(review_ids)) == 120, "I3C QA completed review IDs are not unique")
    require(set(review_ids) == set(key_by_id), "I3C QA completed review set differs from the sampling key")
    critical = 0
    major_rows = 0
    reviewed_by_field = Counter()
    major_by_field = Counter()
    reviewers = Counter()
    for review in reviews:
        require(
            set(review) == COMPLETED_REVIEW_KEYS,
            "I3C QA completed review key mismatch",
        )
        review_id = review["review_id"]
        require(review_id in key_by_id, f"Unknown I3C QA review ID: {review_id}")
        require(
            isinstance(review["sample_index"], int)
            and not isinstance(review["sample_index"], bool)
            and review["sample_index"] == key_by_id[review_id]["sample_index"],
            f"I3C QA sample index mismatch: {review_id}",
        )
        require(isinstance(review.get("critical_error"), bool), f"Incomplete critical_error: {review_id}")
        require(isinstance(review.get("major_error"), bool), f"Incomplete major_error: {review_id}")
        reviewer_id = review["reviewer_id"]
        require(
            isinstance(reviewer_id, str)
            and bool(reviewer_id.strip())
            and len(reviewer_id) <= 200,
            f"Missing or invalid reviewer ID: {review_id}",
        )
        reviewer_notes = review["reviewer_notes"]
        require(
            isinstance(reviewer_notes, str) and len(reviewer_notes) <= 4000,
            f"Invalid reviewer notes: {review_id}",
        )
        error_codes = review["error_codes"]
        require(
            isinstance(error_codes, list)
            and len(error_codes) == len(set(error_codes))
            and all(
                isinstance(code, str)
                and bool(code.strip())
                and len(code) <= 100
                for code in error_codes
            ),
            f"Invalid I3C QA error codes: {review_id}",
        )
        critical += int(review["critical_error"])
        major_rows += int(review["major_error"])
        reviewers[reviewer_id] += 1
        present_fields = key_by_id[review_id]["present_fields"]
        for field in present_fields:
            reviewed_by_field[field] += 1
        major_fields = review["major_error_fields"]
        require(
            isinstance(major_fields, list)
            and len(major_fields) == len(set(major_fields))
            and set(major_fields).issubset(FIELD_KEYS),
            f"Unknown or duplicate major-error field: {review_id}",
        )
        if review["major_error"]:
            require(bool(major_fields), f"Major error has no field attribution: {review_id}")
        else:
            require(not major_fields, f"Non-major review has major-error fields: {review_id}")
        for field in major_fields:
            major_by_field[field] += 1
    row_rate = major_rows / len(reviews)
    field_rates = {
        field: major_by_field[field] / reviewed_by_field[field]
        for field in FIELD_KEYS
        if reviewed_by_field[field]
    }
    passed = (
        critical == 0
        and row_rate <= MAJOR_ERROR_THRESHOLD
        and all(rate <= MAJOR_ERROR_THRESHOLD for rate in field_rates.values())
    )
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


def finalize(root: Path, completed_form: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    qa_root = version_root(root) / "i3c_manual_qa"
    packet_manifest_path = qa_root / "manifest.json"
    packet = read_json(packet_manifest_path)
    require(packet.get("state") == "blinded_review_pending", "I3C QA packet state mismatch")
    key_path = root / packet["artifacts"]["sampling_key"]["path"]
    require(sha256_file(key_path) == packet["artifacts"]["sampling_key"]["sha256"], "I3C QA sampling key drift")
    reviews = read_jsonl(completed_form)
    key_rows = read_jsonl(key_path)
    result = decision(reviews, key_rows)
    output_path = qa_root / "manual_qa_decision.json"
    report = {
        "schema_version": "rq2b-i3c-manual-qa-decision-v1",
        "version_id": VERSION_ID,
        "state": (
            "manual_qa_passed_retrieval_ready"
            if result["passed"]
            else "manual_qa_rejected_corpus_wide_correction_required"
        ),
        "network_calls": 0,
        "packet_manifest": {
            "path": relative(packet_manifest_path, root),
            "sha256": sha256_file(packet_manifest_path),
        },
        "completed_review_form": {
            "path": relative(completed_form, root),
            "sha256": sha256_file(completed_form),
            "rows": len(reviews),
        },
        "decision": result,
        "retrieval_ready": result["passed"],
        "selective_sample_only_repairs_allowed": False,
    }
    write_json_new(output_path, report)
    return report


def self_test() -> dict[str, Any]:
    keys = [
        {
            "sample_index": index,
            "review_id": f"r{index}",
            "present_fields": [FIELD_KEYS[index % len(FIELD_KEYS)]],
        }
        for index in range(120)
    ]
    reviews = [
        {
            "sample_index": index,
            "review_id": f"r{index}",
            "critical_error": False,
            "major_error": False,
            "major_error_fields": [],
            "error_codes": [],
            "reviewer_notes": "",
            "reviewer_id": "synthetic-reviewer",
        }
        for index in range(120)
    ]
    passed = decision(reviews, keys)
    require(passed["passed"] is True, "I3C QA passing self-test failed")
    rejected_reviews = json.loads(json.dumps(reviews))
    rejected_reviews[0]["critical_error"] = True
    rejected = decision(rejected_reviews, keys)
    require(rejected["passed"] is False, "I3C QA critical-error self-test failed")
    duplicate_reviews = json.loads(json.dumps(reviews))
    duplicate_reviews[-1]["review_id"] = duplicate_reviews[0]["review_id"]
    duplicate_rejected = False
    try:
        decision(duplicate_reviews, keys)
    except ValueError:
        duplicate_rejected = True
    require(duplicate_rejected, "I3C QA duplicate-review self-test failed")
    extra_metadata_reviews = json.loads(json.dumps(reviews))
    extra_metadata_reviews[0]["gold_skill"] = "prohibited"
    extra_metadata_rejected = False
    try:
        decision(extra_metadata_reviews, keys)
    except ValueError:
        extra_metadata_rejected = True
    require(extra_metadata_rejected, "I3C QA extra-metadata self-test failed")
    return {
        "state": "synthetic_qa_decision_only",
        "pass_case": passed["passed"],
        "critical_reject_case": not rejected["passed"],
        "duplicate_review_rejected": duplicate_rejected,
        "extra_metadata_rejected": extra_metadata_rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--completed-form", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.completed_form is not None, "--completed-form is required")
        root = args.root.resolve()
        form = args.completed_form if args.completed_form.is_absolute() else root / args.completed_form
        result = finalize(root, form)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
