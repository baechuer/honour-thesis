#!/usr/bin/env python3
"""Freeze the calibrated, blinded RQ2b v1.2 I3C extraction-fidelity re-review.

This package deliberately reuses the original 120 anonymous source/extraction
pairs but creates a separate review identity, rubric, calibration fixtures,
batch manifest and completion receipt.  It never changes the raw QA attempt.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import (
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    write_json_new,
    write_jsonl_new,
    write_text_new,
)


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
PARENT_QA_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa"
DEFAULT_QA_DIRECTORY = "i3c_manual_qa_calibrated_v2"
QA_SAMPLE_SIZE = 120
BATCH_COUNT = 6
BATCH_SIZE = 20
CALIBRATION_SIZE = 8
FIELD_KEYS = (
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "dependencies_resources",
    "constraints_boundaries",
    "success_criteria",
)


def empty_fields() -> dict[str, list[dict[str, str]]]:
    return {field: [] for field in FIELD_KEYS}


def item(item_id: str, text: str) -> dict[str, str]:
    return {
        "id": item_id,
        "text": text,
        "evidence": text,
        "evidence_status": "explicit",
    }


def fixture(
    review_id: str,
    source_text: str,
    fields: dict[str, list[dict[str, str]]],
    retained: list[dict[str, str]],
    omitted: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return {
        "review_id": review_id,
        "source_text": source_text,
        "extracted_fields": fields,
        "retained_selector_spans": retained,
        "omitted_selector_spans": omitted or [],
        "field_warnings": {},
        "qa_warnings": [],
    }


def calibration_fixtures() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return reviewer-visible fixtures and the local-only expected decisions."""
    visible: list[dict[str, Any]] = []
    answers: list[dict[str, Any]] = []

    fields = empty_fields()
    text = "# Native PDF Extractor\n\nUse when the input is a born-digital PDF with selectable text.\n\nOutput: a UTF-8 plain-text file.\n"
    fields["use_conditions"] = [item("use_1", "Use when the input is a born-digital PDF with selectable text.")]
    fields["output_artifacts"] = [item("output_1", "Output: a UTF-8 plain-text file.")]
    visible.append(fixture("calibration-001", text, fields, fields["use_conditions"] + fields["output_artifacts"]))
    answers.append({"review_id": "calibration-001", "critical_error": False, "major_error": False, "major_error_fields": [], "error_codes": []})

    fields = empty_fields()
    text = "# Archive Manifest Builder\n\nInput: a directory of signed release files.\n\nOutput: a SHA-256 manifest in JSON.\n"
    fields["input_preconditions"] = [item("input_1", "Input: a directory of signed release files.")]
    fields["output_artifacts"] = [item("output_1", "Output: a SHA-256 manifest in JSON.")]
    visible.append(fixture("calibration-002", text, fields, fields["input_preconditions"] + fields["output_artifacts"]))
    answers.append({"review_id": "calibration-002", "critical_error": False, "major_error": False, "major_error_fields": [], "error_codes": []})

    fields = empty_fields()
    text = "# DOCX Citation Normalizer\n\nUse only when the supplied document is a DOCX manuscript.\n\nProcedure: normalise citation punctuation without changing prose.\n"
    fields["workflow_steps"] = [item("workflow_1", "Procedure: normalise citation punctuation without changing prose.")]
    visible.append(fixture("calibration-003", text, fields, fields["workflow_steps"]))
    answers.append({"review_id": "calibration-003", "critical_error": False, "major_error": True, "major_error_fields": ["use_conditions"], "error_codes": ["missing_selection_critical_content"]})

    fields = empty_fields()
    text = "# Protobuf Compatibility Checker\n\nInput: a .proto schema and a baseline descriptor.\n\nOutput: a compatibility report.\n"
    misplaced = item("output_1", "Input: a .proto schema and a baseline descriptor.")
    fields["output_artifacts"] = [misplaced]
    fields["output_artifacts"].append(item("output_2", "Output: a compatibility report."))
    visible.append(fixture("calibration-004", text, fields, fields["output_artifacts"]))
    answers.append({"review_id": "calibration-004", "critical_error": False, "major_error": True, "major_error_fields": ["output_artifacts"], "error_codes": ["wrong_operational_field"]})

    fields = empty_fields()
    text = "# JSON Audit Exporter\n\nOutput: an NDJSON audit export.\n"
    unsupported = {"id": "output_1", "text": "Output: a CSV audit export.", "evidence": "Output: a CSV audit export.", "evidence_status": "explicit"}
    fields["output_artifacts"] = [unsupported]
    visible.append(fixture("calibration-005", text, fields, [unsupported]))
    answers.append({"review_id": "calibration-005", "critical_error": True, "major_error": False, "major_error_fields": [], "error_codes": ["evidence_not_exact"]})

    fields = empty_fields()
    text = "# Medical Triage Labeler\n\nUse when assigning a severity label to an adverse-event report.\n\nThis skill must not contain benchmark routing scaffold or gold-label instructions.\n"
    scaffold = item("use_1", "benchmark routing scaffold or gold-label instructions")
    fields["use_conditions"] = [scaffold]
    visible.append(fixture("calibration-006", text, fields, [scaffold]))
    answers.append({"review_id": "calibration-006", "critical_error": True, "major_error": False, "major_error_fields": [], "error_codes": ["benchmark_scaffold_leakage"]})

    fields = empty_fields()
    text = "---\nname: JSON Manifest Writer\ndescription: Generates a JSON release manifest.\n---\n\n# JSON Manifest Writer\n\nOutput: Generates a JSON release manifest.\n"
    duplicate = item("output_1", "Generates a JSON release manifest.")
    fields["output_artifacts"] = [duplicate]
    omitted = [{"field_key": "output_artifacts", "item_id": "output_1", "evidence": duplicate["evidence"], "omission_reason": "exact_duplicate_of_source_native_description"}]
    visible.append(fixture("calibration-007", text, fields, [], omitted))
    answers.append({"review_id": "calibration-007", "critical_error": False, "major_error": False, "major_error_fields": [], "error_codes": []})

    fields = empty_fields()
    text = "# Payment Dispute Router\n\nGeneral note: The user needs help.\n\nUse when reconciling customer payment disputes against settlement records.\n"
    generic = item("use_1", "The user needs help.")
    fields["use_conditions"] = [generic]
    visible.append(fixture("calibration-008", text, fields, [generic]))
    answers.append({"review_id": "calibration-008", "critical_error": False, "major_error": True, "major_error_fields": ["use_conditions"], "error_codes": ["generic_or_misleading_selector_span"]})

    return visible, answers


GUIDANCE = """# RQ2b v1.2 Calibrated I3C Blinded Extraction-Fidelity QA

## Scope and blinding

Judge only whether this anonymous source document was faithfully converted into
the supplied operational-field extraction and selector-visible evidence spans.
Do not assess prompt fit, gold labels, nearest alternatives, routing accuracy,
rankings, benchmark strata, or whether you personally would rewrite the skill.
Do not read any other QA directory, sampling key, prompt manifest, prior review,
retrieval output, or result file. Use only the assigned calibration/batch input,
this guidance, and your assigned output path. Do not use network or APIs.

## What counts as an error

**Critical**: an extracted item or selector-visible evidence claims text that is
not an exact source substring, or visible benchmark/routing scaffold leaks into
the extraction. Critical means the evidence-grounding boundary itself is broken.

**Major**: only one of the following, and only if it can materially alter the
operational selection meaning of this skill:

1. `wrong_operational_field`: an evidence span is put in an operational field
   that contradicts its role (for example, a required input is represented as
   an output).
2. `missing_selection_critical_content`: an explicit, distinctive operational
   condition, input, output, procedure, boundary, dependency, or success rule
   is absent from every extracted field. Do not require every example, detail,
   or sentence: flag only a missing claim whose absence changes what the skill
   is for or when it should be selected.
3. `generic_or_misleading_selector_span`: a retained span is generic or
   misleading in a way that substitutes for, obscures, or contradicts an
   explicit distinguishing source claim.

Do **not** call these errors: reasonable overlap between neighbouring fields;
absence of a non-distinctive example/substep; short evidence; formatting; an
empty field when the source provides no distinctive content; or a field item
omitted from `retained_selector_spans` because it exactly duplicates the native
name/description (that native metadata remains selector-visible separately).

When one retained generic span replaces a single explicit distinguishing claim,
use `generic_or_misleading_selector_span` only. Do not add
`missing_selection_critical_content` for that same replacement; reserve the
missing-content code for a distinctive claim with no related retained field
item at all.

When an item has a critical evidence or scaffold failure, record the critical
failure only. Do not also add a major error merely because the same invalid item
fails to capture a legitimate source claim.

For every record, write exactly one completed JSON object using this schema:
`review_id`, `review_status`, `critical_error`, `major_error`,
`major_error_fields`, `error_codes`, `reviewer_notes`, `reviewer_id`.

Set `review_status` to `completed`. `major_error_fields` must be empty iff
`major_error` is false. Use only the error codes listed above plus
`evidence_not_exact`, `benchmark_scaffold_leakage`, or `other` for a genuinely
different protocol-breaking case. If no error meets these definitions, use
false/false with empty lists. Notes must state the exact source phrase and
reason when an error is marked; otherwise write a short confirmation.
"""


def verify_parent(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parent_root = root / PARENT_QA_ROOT
    manifest_path = parent_root / "manifest.json"
    audit_path = parent_root / "manual_qa_integrity_audit.json"
    require(manifest_path.is_file() and audit_path.is_file(), "raw v1.2 QA evidence is incomplete")
    manifest = read_json(manifest_path)
    audit = read_json(audit_path)
    require(manifest["version_id"] == VERSION_ID, "parent QA version mismatch")
    require(audit["state"] == "manual_qa_reviews_complete_gate_inconclusive_reviewer_calibration_required", "parent QA audit state mismatch")
    reviewer_ref = manifest["artifacts"]["blinded_reviewer_packet"]
    reviewer_path = root / reviewer_ref["path"]
    require(sha256_file(reviewer_path) == reviewer_ref["sha256"], "parent blinded reviewer packet hash drift")
    rows = read_jsonl(reviewer_path)
    require(len(rows) == QA_SAMPLE_SIZE, "parent QA sample size mismatch")
    return manifest, rows


def build(root: Path, *, qa_directory: str = DEFAULT_QA_DIRECTORY) -> dict[str, Any]:
    parent_manifest, parent_rows = verify_parent(root)
    require(qa_directory.startswith("i3c_manual_qa_calibrated_") and "/" not in qa_directory, "invalid calibrated QA directory")
    qa_root = root / RELATIVE_ROOT / qa_directory
    staging = qa_root.with_name(f".{qa_root.name}.staging")
    require(not qa_root.exists() and not staging.exists(), "refusing to overwrite calibrated QA package")
    fixtures, answer_key = calibration_fixtures()
    require(len(fixtures) == len(answer_key) == CALIBRATION_SIZE, "calibration size mismatch")

    reviewer_rows: list[dict[str, Any]] = []
    for index, parent in enumerate(parent_rows, start=1):
        reviewer_rows.append({**parent, "review_id": f"rq2b-v12-i3c-calibrated-qa-{index:03d}"})

    staging.mkdir(parents=True, exist_ok=False)
    batch_inputs = staging / "review_batches" / "inputs"
    batch_outputs = staging / "review_batches" / "outputs"
    calibration_outputs = staging / "calibration_outputs"
    batch_inputs.mkdir(parents=True, exist_ok=False)
    batch_outputs.mkdir(parents=True, exist_ok=False)
    calibration_outputs.mkdir(parents=True, exist_ok=False)
    reviewer_packet = staging / "blinded_reviewer_packet.jsonl"
    calibration_input = staging / "calibration_input.jsonl"
    calibration_key = staging / "calibration_answer_key_do_not_give_reviewer.jsonl"
    guidance = staging / "reviewer_guidance.md"
    write_jsonl_new(reviewer_packet, reviewer_rows)
    write_jsonl_new(calibration_input, fixtures)
    write_jsonl_new(calibration_key, answer_key)
    write_text_new(guidance, GUIDANCE)

    batches: list[dict[str, Any]] = []
    for batch_index in range(BATCH_COUNT):
        rows = reviewer_rows[batch_index * BATCH_SIZE : (batch_index + 1) * BATCH_SIZE]
        input_path = batch_inputs / f"review_batch_{batch_index:03d}_input.jsonl"
        write_jsonl_new(input_path, rows)
        slot = f"codex-v12-i3c-calibrated-v2-slot-{batch_index:03d}"
        primary_calibration = qa_root / "calibration_outputs" / f"calibration_{batch_index:03d}_primary_completed.jsonl"
        replacement_calibration = qa_root / "calibration_outputs" / f"calibration_{batch_index:03d}_replacement_completed.jsonl"
        batches.append(
            {
                "batch_index": batch_index,
                "reviewer_id": slot,
                "calibration_attempt_paths": [
                    relative(primary_calibration, root),
                    relative(replacement_calibration, root),
                ],
                "input_path": relative(qa_root / "review_batches" / "inputs" / input_path.name, root),
                "input_sha256": sha256_file(input_path),
                "output_path": relative(qa_root / "review_batches" / "outputs" / f"review_batch_{batch_index:03d}_completed.jsonl", root),
                "expected_rows": BATCH_SIZE,
                "review_ids": [row["review_id"] for row in rows],
            }
        )

    source_packet = parent_manifest["artifacts"]["blinded_reviewer_packet"]
    protocol = {
        "schema_version": "rq2b-v12-i3c-calibrated-qa-protocol-v2",
        "version_id": VERSION_ID,
        "purpose": "blinded source-to-I3C extraction fidelity only",
        "population": "the 120 frozen anonymous source/extraction pairs from the raw v1.2 attempt; no resampling and no raw-review visibility",
        "calibration": {"fixtures": CALIBRATION_SIZE, "pass_rule": "all 8 expected severity, field, and code decisions match before a reviewer receives its batch", "maximum_independent_replacement_attempts_per_slot": 1, "failed_calibration_outputs": "preserved and never overwritten"},
        "acceptance_rule": {"critical_error_rows": 0, "maximum_major_error_rows": 6, "maximum_major_error_rate": 0.05, "field_level_threshold": "none; field attribution is descriptive because field counts are sparse"},
        "major_error_definition": ["wrong operational field that changes selection meaning", "missing explicit distinctive operational content that changes selection meaning", "generic or misleading retained selector span that substitutes for, obscures, or contradicts a distinctive source claim"],
        "not_major": ["missing non-distinctive examples/substeps", "reasonable field overlap", "short formatting", "empty source-absent fields", "items omitted only because exact duplicates of source-native name/description"],
        "bound_parent_packet": source_packet,
        "parent_integrity_audit": {"path": relative(root / PARENT_QA_ROOT / "manual_qa_integrity_audit.json", root), "sha256": sha256_file(root / PARENT_QA_ROOT / "manual_qa_integrity_audit.json")},
        "network_calls": 0,
        "external_api_calls": 0,
        "retrieval_or_reranking": False,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "protocol.json", protocol)
    receipt = {
        "schema_version": "rq2b-v12-i3c-calibrated-qa-approval-receipt-v1",
        "version_id": VERSION_ID,
        "state": "explicitly_authorized_local_calibrated_re_review_once",
        "user_authorization": "freeze the QA protocol, re-review, then run the first-version experiment",
        "authorization_date": "2026-08-18",
        "scope": ["freeze this local calibrated QA package", "use at most six local Codex reviewers with no network/API", "complete calibration then one disjoint 20-row batch per passing reviewer", "after and only after a valid QA pass, run the first local BM25 B1L matrix subject to its separate local preflight"],
        "does_not_authorize": ["external text transmission", "paid embedding or reranker calls", "hosted SkillRouter", "thesis LaTeX/PDF result integration"],
        "network_calls": 0,
        "external_api_calls": 0,
    }
    write_json_new(staging / "approval_receipt.json", receipt)
    manifest = {
        "schema_version": "rq2b-v12-i3c-calibrated-qa-package-v2",
        "version_id": VERSION_ID,
        "state": "frozen_calibration_pending",
        "sample_size": QA_SAMPLE_SIZE,
        "batch_count": BATCH_COUNT,
        "batch_size": BATCH_SIZE,
        "calibration_size": CALIBRATION_SIZE,
        "maximum_independent_replacement_attempts_per_slot": 1,
        "network_calls": 0,
        "external_api_calls": 0,
        "retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "artifacts": {
            "protocol": {"path": relative(qa_root / "protocol.json", root), "sha256": sha256_file(staging / "protocol.json")},
            "approval_receipt": {"path": relative(qa_root / "approval_receipt.json", root), "sha256": sha256_file(staging / "approval_receipt.json")},
            "reviewer_guidance": {"path": relative(qa_root / "reviewer_guidance.md", root), "sha256": sha256_file(guidance)},
            "blinded_reviewer_packet": {"path": relative(qa_root / "blinded_reviewer_packet.jsonl", root), "sha256": sha256_file(reviewer_packet), "rows": QA_SAMPLE_SIZE},
            "calibration_input": {"path": relative(qa_root / "calibration_input.jsonl", root), "sha256": sha256_file(calibration_input), "rows": CALIBRATION_SIZE},
            "calibration_answer_key_do_not_give_reviewer": {"path": relative(qa_root / "calibration_answer_key_do_not_give_reviewer.jsonl", root), "sha256": sha256_file(calibration_key), "rows": CALIBRATION_SIZE},
        },
        "batches": batches,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(qa_root)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--qa-directory", default=DEFAULT_QA_DIRECTORY)
    args = parser.parse_args()
    print(json.dumps(build(args.root.resolve(), qa_directory=args.qa_directory), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
