#!/usr/bin/env python3
"""Audit the calibrated v1.2 I3C QA failure without changing corpus rows."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
QA_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa_calibrated_v6"
FIELDS = (
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "dependencies_resources",
    "constraints_boundaries",
    "success_criteria",
)


def build(root: Path) -> dict[str, Any]:
    qa_root = root / QA_ROOT
    decision_path = qa_root / "manual_qa_decision.json"
    reviewer_path = qa_root / "blinded_reviewer_packet.jsonl"
    completed_path = qa_root / "review_form_completed.jsonl"
    merged_path = root / RELATIVE_ROOT / "i3c_merged" / "canonical_extractions.jsonl"
    source_manifest_path = root / RELATIVE_ROOT / "source_manifest.jsonl"
    for path in (decision_path, reviewer_path, completed_path, merged_path, source_manifest_path):
        require(path.is_file(), f"required calibrated QA audit input is missing: {path}")
    decision = read_json(decision_path)
    require(decision["state"] == "manual_qa_failed_retrieval_blocked", "this audit requires the failed calibrated QA decision")
    reviewer_rows = {row["review_id"]: row for row in read_jsonl(reviewer_path)}
    reviews = read_jsonl(completed_path)
    sources = read_jsonl(source_manifest_path)
    canonical = read_jsonl(merged_path)
    require(len(sources) == len(canonical) == 2433, "v1.2 corpus row count mismatch")

    critical_rows = [row for row in reviews if row["critical_error"]]
    critical_evidence_checks: list[dict[str, Any]] = []
    for review in critical_rows:
        packet = reviewer_rows[review["review_id"]]
        exact_evidence = all(
            item["evidence"] in packet["source_text"]
            for items in packet["extracted_fields"].values()
            for item in items
        )
        nonliteral_parser_text = [
            {"field": field, "item_id": item["id"], "text": item["text"], "evidence": item["evidence"]}
            for field, items in packet["extracted_fields"].items()
            for item in items
            if item["text"] not in packet["source_text"] and item["evidence"] in packet["source_text"]
        ]
        critical_evidence_checks.append(
            {
                "review_id": review["review_id"],
                "reported_codes": review["error_codes"],
                "all_bound_evidence_exact_source_substrings": exact_evidence,
                "nonliteral_parser_text_items": nonliteral_parser_text,
            }
        )

    empty_rows = [
        {"source": source, "canonical": extraction}
        for source, extraction in zip(sources, canonical, strict=True)
        if not any(extraction["fields"][field] for field in FIELDS)
    ]
    description_patterns = {
        "use_when": r"\buse when\b",
        "open": r"\bopen\b",
        "build": r"\bbuild\b",
        "analyze": r"\banaly[sz]e\b",
        "create": r"\bcreate\b",
        "calculate": r"\bcalculate\b",
        "implement": r"\bimplement\b",
    }
    field_empty_audit = {
        "all_fields_empty_rows": len(empty_rows),
        "by_source_policy": dict(Counter(row["source"]["source_policy"] for row in empty_rows)),
        "with_nonempty_native_description": sum(bool(row["source"]["source_description"].strip()) for row in empty_rows),
        "native_description_pattern_counts": {
            name: sum(bool(re.search(pattern, row["source"]["source_description"], re.IGNORECASE)) for row in empty_rows)
            for name, pattern in description_patterns.items()
        },
        "examples": [
            {
                "skill_id": row["source"]["skill_id"],
                "source_policy": row["source"]["source_policy"],
                "source_description": row["source"]["source_description"],
                "qa_warnings": row["canonical"]["qa_warnings"],
            }
            for row in empty_rows[:20]
        ],
    }
    major_rows = [row for row in reviews if row["major_error"]]
    report = {
        "schema_version": "rq2b-v12-calibrated-qa-failure-audit-v1",
        "version_id": VERSION_ID,
        "state": "qa_failed_correction_preflight_required",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "bound_inputs": {
            "calibrated_decision": {"path": relative(decision_path, root), "sha256": sha256_file(decision_path)},
            "completed_reviews": {"path": relative(completed_path, root), "sha256": sha256_file(completed_path), "rows": len(reviews)},
            "reviewer_packet": {"path": relative(reviewer_path, root), "sha256": sha256_file(reviewer_path), "rows": len(reviewer_rows)},
            "canonical_extractions": {"path": relative(merged_path, root), "sha256": sha256_file(merged_path), "rows": len(canonical)},
            "source_manifest": {"path": relative(source_manifest_path, root), "sha256": sha256_file(source_manifest_path), "rows": len(sources)},
        },
        "calibrated_decision": decision["acceptance"],
        "critical_error_interpretation": {
            "reported_rows": len(critical_rows),
            "all_rows_keep_exact_evidence_substrings": all(row["all_bound_evidence_exact_source_substrings"] for row in critical_evidence_checks),
            "finding": "The four reviewed critical reports concern non-selector-visible parser text. Bound evidence strings remain exact source substrings; this is a reviewer-packet/rubric visibility defect, not a literal-evidence automatic-gate failure.",
            "rows": critical_evidence_checks,
        },
        "major_error_interpretation": {
            "reported_rows": len(major_rows),
            "codes": dict(Counter(code for row in major_rows for code in row["error_codes"])),
            "finding": "Major findings remain actionable: fieldless source-native descriptions prevent canonical I3 operational organization, and a sampled output-artifact selection retained a generic span while omitting the distinctive deliverable.",
        },
        "fieldless_public_description_audit": field_empty_audit,
        "required_next_gate": [
            "freeze a corrected reviewer packet that explicitly distinguishes non-selector-visible parser text from exact evidence",
            "freeze a source-grounded V3 extraction policy that records selector-useful native descriptions canonically even when their duplicate span is omitted from selector serialization",
            "obtain a new explicit approval before assigning source text for V3 re-extraction",
            "run automatic gates and a fresh calibrated blind QA; do not selectively repair reviewed rows",
        ],
        "retrieval_ready": False,
    }
    output_path = qa_root / "failure_audit.json"
    require(not output_path.exists(), "refusing to overwrite calibrated QA failure audit")
    write_json_new(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(build(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
