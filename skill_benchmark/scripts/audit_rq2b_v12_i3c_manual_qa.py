#!/usr/bin/env python3
"""Audit v1.2 blinded I3C QA completion without reinterpreting reviews.

This is a methodological integrity check. It preserves every completed review,
performs no semantic re-review, and cannot make the corpus retrieval-ready.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
QA_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa"
AUDIT_PATH = f"{QA_ROOT}/manual_qa_integrity_audit.json"
QA_SAMPLE_SIZE = 120


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row[key]) for row in rows))


def audit(root: Path) -> dict[str, Any]:
    qa_root = root / QA_ROOT
    output_path = root / AUDIT_PATH
    require(not output_path.exists(), f"refusing to overwrite v1.2 QA integrity audit: {output_path}")
    packet_path = qa_root / "manifest.json"
    decision_path = qa_root / "manual_qa_decision.json"
    completed_path = qa_root / "review_form_completed.jsonl"
    key_path = qa_root / "sampling_key_do_not_give_reviewer.jsonl"
    batch_path = qa_root / "review_batches" / "manifest.json"
    packet, prior_decision, batches = read_json(packet_path), read_json(decision_path), read_json(batch_path)
    reviews, key_rows = read_jsonl(completed_path), read_jsonl(key_path)
    require(len(reviews) == len(key_rows) == QA_SAMPLE_SIZE, "v1.2 QA review/key row count mismatch")
    key_by_id = {row["review_id"]: row for row in key_rows}
    require(len(key_by_id) == QA_SAMPLE_SIZE and [row["review_id"] for row in reviews] == [row["review_id"] for row in key_rows], "v1.2 QA review/key alignment mismatch")
    require(len({row["reviewer_id"] for row in reviews}) == 6, "v1.2 QA reviewer count mismatch")

    rows_by_reviewer: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for review in reviews:
        joined = dict(key_by_id[review["review_id"]])
        joined.update({"reviewer_id": review["reviewer_id"], "major_error": review["major_error"], "critical_error": review["critical_error"]})
        rows_by_reviewer[review["reviewer_id"]].append(joined)
    batch_profiles = []
    for reviewer_id, rows in sorted(rows_by_reviewer.items()):
        require(len(rows) == 20, f"v1.2 QA reviewer batch size mismatch: {reviewer_id}")
        batch_profiles.append(
            {
                "reviewer_id": reviewer_id,
                "rows": len(rows),
                "critical_errors": sum(bool(row["critical_error"]) for row in rows),
                "major_error_rows": sum(bool(row["major_error"]) for row in rows),
                "major_error_row_rate": sum(bool(row["major_error"]) for row in rows) / len(rows),
                "cohorts": count_by(rows, "cohort"),
                "source_policies": count_by(rows, "source_policy"),
            }
        )
    major_counts = [profile["major_error_rows"] for profile in batch_profiles]
    raw_error_codes = Counter(code for row in reviews for code in row["error_codes"])
    raw_fields = Counter(field for row in reviews for field in row["major_error_fields"])
    prior_metrics = prior_decision["decision"]
    result = {
        "schema_version": "rq2b-v12-i3c-manual-qa-integrity-audit-v1",
        "version_id": VERSION_ID,
        "state": "manual_qa_reviews_complete_gate_inconclusive_reviewer_calibration_required",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "retrieval_authorized": False,
        "review_binding": {
            "qa_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
            "completed_review_form": {"path": relative(completed_path, root), "sha256": sha256_file(completed_path), "rows": len(reviews)},
            "batch_manifest": {"path": relative(batch_path, root), "sha256": sha256_file(batch_path)},
            "raw_decision": {"path": relative(decision_path, root), "sha256": sha256_file(decision_path)},
        },
        "structural_checks": {
            "review_rows": len(reviews),
            "key_rows": len(key_rows),
            "review_ids_identity_aligned": True,
            "completed_rows": sum(row["review_status"] == "completed" for row in reviews),
            "reviewer_batches": len(batch_profiles),
        },
        "raw_review_observations": {
            "critical_errors": sum(bool(row["critical_error"]) for row in reviews),
            "major_error_rows": sum(bool(row["major_error"]) for row in reviews),
            "major_error_row_rate": sum(bool(row["major_error"]) for row in reviews) / len(reviews),
            "error_codes": dict(raw_error_codes),
            "major_field_attributions": dict(raw_fields),
            "batch_profiles": batch_profiles,
            "batch_major_error_range": {"minimum": min(major_counts), "maximum": max(major_counts)},
        },
        "methodological_findings": [
            "The packet and receipt did not bind a v1.2 acceptance threshold; the raw finalizer inherited an unbound 5% threshold.",
            "The packet defined a major error as material missing content but did not bind a coverage rule for when a concise selector-oriented extraction becomes materially incomplete.",
            "Each sampled row was reviewed once. The six 20-row reviewer batches range from zero to sixteen major-error rows, so reviewer-policy variation cannot be separated from extraction quality.",
            "The raw finalizer divided missing-field attributions by extracted-field coverage, producing invalid field rates above one. Its raw forms remain preserved, but that field-rate interpretation is superseded.",
            "Batch 003 and batch 004 have the same cohort profile (9 background-scale, 6 main-evaluated, 5 other) and the same source-policy profile (16 authored, 4 public-original), yet report 0 versus 15 major rows. This does not prove either batch wrong, but demonstrates that source-mix counts alone do not explain the disparity.",
        ],
        "interpretation": "The completed raw reviews are evidence for rubric calibration, not a valid corpus pass or corpus-wide rejection decision. The corpus is not retrieval-ready. A new, frozen QA rubric and an explicitly approved calibrated re-review are required before the extraction gate can support a retrieval decision.",
        "selective_sample_only_repairs_allowed": False,
    }
    write_json_new(output_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(audit(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
