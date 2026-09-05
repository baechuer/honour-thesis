#!/usr/bin/env python3
"""Build, but do not complete, the blinded calibrated V3 I3C QA packet.

Reviewer-visible field entries contain only literal selector ``evidence``. The
internal parser-normalised ``text`` is intentionally omitted, so it cannot be
mistaken for selector-visible content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new, write_text_new


VERSION_ID = "rq2b-i3c-v3-2026-08-18"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
V12_ROOT = "skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16"
V3_PACKET = f"{RELATIVE_ROOT}/source_assignment_approval_packet_sealed.json"
V3_RECEIPT = f"{RELATIVE_ROOT}/source_assignment_approval_receipt.json"
FINALISATION_PACKET = f"{RELATIVE_ROOT}/finalisation_approval_packet.json"
FINALISATION_RECEIPT = f"{RELATIVE_ROOT}/finalisation_approval_receipt.json"
MERGED_ROOT = f"{RELATIVE_ROOT}/i3c_merged_final"
CHUNK_MANIFEST = f"{RELATIVE_ROOT}/i3c_extraction/manifest.json"
SOURCE_MANIFEST = f"{V12_ROOT}/source_manifest.jsonl"
DEFAULT_QA_DIRECTORY = "i3c_manual_qa_calibrated_v1"
QA_SAMPLE_SIZE = 120
PINNED_ROOT_COVERAGE_CHUNK = 49
CALIBRATION_SIZE = 8
BATCH_SIZE = 20
FIELD_KEYS = (
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "success_criteria",
    "constraints_boundaries",
    "dependencies_resources",
)
REVIEWER_ALLOWED_KEYS = {
    "review_id",
    "source_text",
    "native_selector_metadata",
    "extracted_selector_evidence",
    "field_warnings",
    "qa_warnings",
}
FORBIDDEN_REVIEWER_KEY_TOKENS = (
    "prompt", "gold", "alternative", "role", "stratum", "group", "retrieval",
    "skill_id", "source_path", "source_row_index", "source_sha256",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def empty_fields() -> dict[str, list[dict[str, str]]]:
    return {field: [] for field in FIELD_KEYS}


def visible_item(item_id: str, evidence: str) -> dict[str, str]:
    return {"id": item_id, "evidence": evidence, "evidence_status": "explicit"}


def reviewer_items(items: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {"id": str(item["id"]), "evidence": str(item["evidence"]), "evidence_status": str(item["evidence_status"])}
        for item in items
    ]


def fixture(review_id: str, source_text: str, fields: dict[str, list[dict[str, str]]], name: str, description: str = "") -> dict[str, Any]:
    return {
        "review_id": review_id,
        "source_text": source_text,
        "native_selector_metadata": {"name": name, "description": description},
        "extracted_selector_evidence": fields,
        "field_warnings": {},
        "qa_warnings": [],
    }


def calibration_fixtures() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Eight exact-match fixtures: two clean, three major, two critical, one metadata duplicate."""
    visible: list[dict[str, Any]] = []
    answers: list[dict[str, Any]] = []

    fields = empty_fields()
    source = "# Native PDF Extractor\n\nUse when the input is a born-digital PDF with selectable text.\n\nOutput: a UTF-8 plain-text file.\n"
    fields["use_conditions"] = [visible_item("use_1", "Use when the input is a born-digital PDF with selectable text.")]
    fields["output_artifacts"] = [visible_item("output_1", "Output: a UTF-8 plain-text file.")]
    visible.append(fixture("calibration-001", source, fields, "Native PDF Extractor"))
    answers.append({"review_id": "calibration-001", "critical_error": False, "major_error": False, "major_error_fields": [], "error_codes": []})

    fields = empty_fields()
    source = "# Archive Manifest Builder\n\nInput: a directory of signed release files.\n\nOutput: a SHA-256 manifest in JSON.\n"
    fields["input_preconditions"] = [visible_item("input_1", "Input: a directory of signed release files.")]
    fields["output_artifacts"] = [visible_item("output_1", "Output: a SHA-256 manifest in JSON.")]
    visible.append(fixture("calibration-002", source, fields, "Archive Manifest Builder"))
    answers.append({"review_id": "calibration-002", "critical_error": False, "major_error": False, "major_error_fields": [], "error_codes": []})

    fields = empty_fields()
    source = "# DOCX Citation Normalizer\n\nUse only when the supplied document is a DOCX manuscript.\n\nProcedure: normalise citation punctuation without changing prose.\n"
    fields["workflow_steps"] = [visible_item("workflow_1", "Procedure: normalise citation punctuation without changing prose.")]
    visible.append(fixture("calibration-003", source, fields, "DOCX Citation Normalizer"))
    answers.append({"review_id": "calibration-003", "critical_error": False, "major_error": True, "major_error_fields": ["use_conditions"], "error_codes": ["missing_selection_critical_content"]})

    fields = empty_fields()
    source = "# Protobuf Compatibility Checker\n\nInput: a .proto schema and a baseline descriptor.\n\nOutput: a compatibility report.\n"
    fields["output_artifacts"] = [visible_item("output_1", "Input: a .proto schema and a baseline descriptor."), visible_item("output_2", "Output: a compatibility report.")]
    visible.append(fixture("calibration-004", source, fields, "Protobuf Compatibility Checker"))
    answers.append({"review_id": "calibration-004", "critical_error": False, "major_error": True, "major_error_fields": ["output_artifacts"], "error_codes": ["wrong_operational_field"]})

    fields = empty_fields()
    source = "# JSON Audit Exporter\n\nOutput: an NDJSON audit export.\n"
    fields["output_artifacts"] = [visible_item("output_1", "Output: a CSV audit export.")]
    visible.append(fixture("calibration-005", source, fields, "JSON Audit Exporter"))
    answers.append({"review_id": "calibration-005", "critical_error": True, "major_error": False, "major_error_fields": [], "error_codes": ["evidence_not_exact"]})

    fields = empty_fields()
    source = "# Medical Triage Labeler\n\nUse when assigning a severity label to an adverse-event report.\n\nThis skill must not contain benchmark routing scaffold or gold-label instructions.\n"
    fields["use_conditions"] = [visible_item("use_1", "benchmark routing scaffold or gold-label instructions")]
    visible.append(fixture("calibration-006", source, fields, "Medical Triage Labeler"))
    answers.append({"review_id": "calibration-006", "critical_error": True, "major_error": False, "major_error_fields": [], "error_codes": ["benchmark_scaffold_leakage"]})

    fields = empty_fields()
    source = "---\nname: JSON Manifest Writer\ndescription: Generates a JSON release manifest.\n---\n\n# JSON Manifest Writer\n\nOutput: Generates a JSON release manifest.\n"
    visible.append(fixture("calibration-007", source, fields, "JSON Manifest Writer", "Generates a JSON release manifest."))
    answers.append({"review_id": "calibration-007", "critical_error": False, "major_error": False, "major_error_fields": [], "error_codes": []})

    fields = empty_fields()
    source = "# Payment Dispute Router\n\nGeneral note: The user needs help.\n\nUse when reconciling customer payment disputes against settlement records.\n"
    fields["use_conditions"] = [visible_item("use_1", "The user needs help.")]
    visible.append(fixture("calibration-008", source, fields, "Payment Dispute Router"))
    answers.append({"review_id": "calibration-008", "critical_error": False, "major_error": True, "major_error_fields": ["use_conditions"], "error_codes": ["generic_or_misleading_selector_span"]})
    return visible, answers


GUIDANCE = """# RQ2b V3 Calibrated I3C Blinded Extraction-Fidelity QA

## Scope and blinding

Judge only whether the anonymous source document was faithfully represented by
the visible selector evidence. Do not assess prompt fit, gold labels,
alternatives, routing accuracy, rankings, or benchmark strata. Use only the
assigned calibration/batch input, this guidance, and the assigned output path.
Do not use network or APIs.

`native_selector_metadata` and literal evidence under
`extracted_selector_evidence` are selector-visible. Internal parser-normalised
`text` is deliberately absent and is not part of the selector. Do not infer an
error from its absence or from parser whitespace normalisation.

## Errors

**Critical**: visible evidence is not an exact source substring, or benchmark
or routing scaffold appears in the extraction.

**Major**, only if it materially changes selection meaning:

1. `wrong_operational_field`: evidence is assigned to a contradictory field.
2. `missing_selection_critical_content`: an explicit distinctive condition,
input, output, procedure, boundary, dependency, or success rule is absent from
both native metadata and every extracted selector-evidence field.
3. `generic_or_misleading_selector_span`: retained evidence is generic or
misleading and replaces, obscures, or contradicts a distinctive source claim.

Do not mark a major error for reasonable field overlap, non-distinctive
examples/substeps, formatting, an empty source-absent field, or exact material
already carried by native metadata. For an invalid-evidence critical error, do
not also report a major error for that same item.

Write one completed JSON object per record with `review_id`, `review_status`,
`critical_error`, `major_error`, `major_error_fields`, `error_codes`,
`reviewer_notes`, and `reviewer_id`. Notes must quote the exact source phrase
and reason for any error; otherwise give a short confirmation.
"""


def verify_authorised_ready(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    packet = read_json(root / V3_PACKET)
    receipt = read_json(root / V3_RECEIPT)
    finalisation_packet = read_json(root / FINALISATION_PACKET)
    finalisation_receipt = read_json(root / FINALISATION_RECEIPT)
    merged = read_json(root / MERGED_ROOT / "manifest.json")
    require(receipt["state"] == "explicitly_approved_for_v3_i3c_source_assignment_once", "V3 source assignment is not approved")
    require(finalisation_receipt["state"] == "explicitly_approved_for_v3_finalisation_once", "V3 finalisation is not approved")
    require(sha256_file(root / V3_PACKET) == receipt["approved_packet"]["sha256"], "V3 packet hash drift")
    require(sha256_file(root / FINALISATION_PACKET) == finalisation_receipt["approved_packet"]["sha256"], "V3 finalisation packet hash drift")
    require("build but not complete a fresh calibrated blinded extraction-fidelity QA packet after automatic gates pass" in packet["authorises_if_approved"], "V3 approval does not authorise QA packet construction")
    require(merged["state"] == "automatic_gates_passed_manual_qa_pending", "final I3C merge is not ready")
    require(merged["root_coverage"]["fieldless_nonempty_public_description_rows"] == 0, "root coverage is not clean")
    require(merged["root_coverage"]["fieldless_public_description_contains_use_when_rows"] == 0, "use-when coverage is not clean")
    require(merged["network_calls"] == merged["external_api_calls"] == 0, "local-only boundary was crossed")
    require(merged["manual_qa"]["completion_authorized"] is False and merged["retrieval_authorized"] is False, "downstream execution must remain unapproved")
    canonical_ref = merged["artifacts"]["canonical_extractions"]
    canonical_path = root / canonical_ref["path"]
    require(sha256_file(canonical_path) == canonical_ref["sha256"], "canonical extraction hash drift")
    sources_path = root / SOURCE_MANIFEST
    require(sha256_file(sources_path) == packet["source_corpus"]["source_manifest"]["sha256"], "source manifest hash drift")
    sources = read_jsonl(sources_path)
    canonical = read_jsonl(canonical_path)
    require(len(sources) == len(canonical) == 2433, "V3 QA population is not 2,433 rows")
    return merged, sources, canonical, read_json(root / CHUNK_MANIFEST)


def build_metadata(sources: list[dict[str, Any]], canonical: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    by_length = sorted(range(len(sources)), key=lambda i: (sources[i]["source_utf8_bytes"], sources[i]["skill_id"]))
    length_bucket = {index: "short" if rank < len(by_length) // 4 else "median" if rank < 3 * len(by_length) // 4 else "long" for rank, index in enumerate(by_length)}
    by_density = sorted(range(len(canonical)), key=lambda i: (len(canonical[i]["retained_selector_spans"]), canonical[i]["skill_id"]))
    density_bucket = {index: "sparse" if rank < len(by_density) // 3 else "dense" if rank >= 2 * len(by_density) // 3 else "medium" for rank, index in enumerate(by_density)}
    metadata: dict[int, dict[str, Any]] = {}
    for index, (source, extraction) in enumerate(zip(sources, canonical, strict=True)):
        require(source["source_row_index"] == extraction["source_row_index"] == index, f"source-row mismatch: {index}")
        require(source["skill_id"] == extraction["skill_id"] and source["source_sha256"] == extraction["source_sha256"], f"source identity mismatch: {index}")
        metadata[index] = {
            "source_policy": str(source["source_policy"]),
            "family": str(source["family"]),
            "length_bucket": length_bucket[index],
            "density_bucket": density_bucket[index],
            "present_fields": sorted(field for field in FIELD_KEYS if extraction["fields"][field]),
        }
    return metadata


def features(values: dict[str, Any]) -> set[tuple[str, str]]:
    return {("source_policy", values["source_policy"]), ("length_bucket", values["length_bucket"]), ("density_bucket", values["density_bucket"]), *(("field", field) for field in values["present_fields"])}


def select_rows(metadata: dict[int, dict[str, Any]], chunk_manifest: dict[str, Any]) -> tuple[list[int], set[int]]:
    chunk = next((item for item in chunk_manifest["chunks"] if item["chunk_index"] == PINNED_ROOT_COVERAGE_CHUNK), None)
    require(chunk is not None, "root-coverage replacement chunk is absent")
    pinned = set(range(chunk["first_source_row_index"], chunk["last_source_row_index"] + 1))
    require(len(pinned) == chunk["row_count"] == 32 and len(pinned) < QA_SAMPLE_SIZE, "pinned chunk shape drift")
    selected = sorted(pinned)
    selected_set = set(selected)
    uncovered = set().union(*(features(values) for values in metadata.values()))
    for index in selected:
        uncovered.difference_update(features(metadata[index]))
    generator = random.Random(2026081801)
    candidates = list(metadata)
    generator.shuffle(candidates)
    while uncovered:
        available = [index for index in candidates if index not in selected_set]
        best = max(available, key=lambda index: (len(features(metadata[index]) & uncovered), -index))
        require(bool(features(metadata[best]) & uncovered), f"uncovered QA features: {sorted(uncovered)}")
        selected.append(best)
        selected_set.add(best)
        uncovered.difference_update(features(metadata[best]))
    strata: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for index, values in metadata.items():
        strata[(values["source_policy"], values["length_bucket"], values["density_bucket"])].append(index)
    for values in strata.values():
        generator.shuffle(values)
    keys = sorted(strata)
    cursor = 0
    while len(selected) < QA_SAMPLE_SIZE:
        key = keys[cursor % len(keys)]
        cursor += 1
        available = [index for index in strata[key] if index not in selected_set]
        if not available:
            require(any(index not in selected_set for values in strata.values() for index in values), "QA sampling exhausted")
            continue
        selected.append(available[-1])
        selected_set.add(available[-1])
    require(len(selected) == QA_SAMPLE_SIZE and len(selected_set) == QA_SAMPLE_SIZE, "QA selection mismatch")
    return selected, pinned


def validate_reviewer_rows(rows: list[dict[str, Any]]) -> None:
    require(len(rows) == QA_SAMPLE_SIZE and len({row["review_id"] for row in rows}) == QA_SAMPLE_SIZE, "reviewer packet identity mismatch")
    for row in rows:
        require(set(row) == REVIEWER_ALLOWED_KEYS, f"unexpected reviewer keys: {set(row) - REVIEWER_ALLOWED_KEYS}")
        require(not any(token in key.lower() for key in row for token in FORBIDDEN_REVIEWER_KEY_TOKENS), f"reviewer leakage key: {row['review_id']}")
        require(set(row["extracted_selector_evidence"]) == set(FIELD_KEYS), f"field keys mismatch: {row['review_id']}")
        for items in row["extracted_selector_evidence"].values():
            for item in items:
                require(set(item) == {"id", "evidence", "evidence_status"}, f"parser text leaked: {row['review_id']}")
                require(item["evidence"] in row["source_text"], f"evidence drift: {row['review_id']}")


def build(root: Path, qa_directory: str = DEFAULT_QA_DIRECTORY) -> dict[str, Any]:
    require(qa_directory == DEFAULT_QA_DIRECTORY, "invalid V3 QA directory")
    _, sources, canonical, chunk_manifest = verify_authorised_ready(root)
    metadata = build_metadata(sources, canonical)
    selected, pinned = select_rows(metadata, chunk_manifest)
    qa_root = root / RELATIVE_ROOT / qa_directory
    staging = qa_root.with_name(f".{qa_root.name}.staging")
    require(not qa_root.exists() and not staging.exists(), "refusing to overwrite V3 QA packet")

    reviewer_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    for sample_index, source_index in enumerate(selected, start=1):
        source = sources[source_index]
        extraction = canonical[source_index]
        source_bytes = (root / source["source_path"]).read_bytes()
        require(sha256_bytes(source_bytes) == source["source_sha256"], f"source byte drift: {source_index}")
        review_id = f"rq2b-v3-i3c-qa-{sample_index:03d}"
        reviewer_rows.append({
            "review_id": review_id,
            "source_text": source_bytes.decode("utf-8"),
            "native_selector_metadata": {"name": extraction["name"], "description": extraction["description"]},
            "extracted_selector_evidence": {field: reviewer_items(extraction["fields"][field]) for field in FIELD_KEYS},
            "field_warnings": extraction["field_warnings"],
            "qa_warnings": extraction["qa_warnings"],
        })
        key_rows.append({"review_id": review_id, "source_row_index": source_index, "skill_id": source["skill_id"], "source_path": source["source_path"], "source_sha256": source["source_sha256"], "pinned_root_coverage_chunk": source_index in pinned, **metadata[source_index]})
    validate_reviewer_rows(reviewer_rows)
    fixtures, answers = calibration_fixtures()
    require(len(fixtures) == len(answers) == CALIBRATION_SIZE, "calibration fixture shape mismatch")

    staging.mkdir(parents=True, exist_ok=False)
    reviewer_path = staging / "blinded_reviewer_packet.jsonl"
    key_path = staging / "sampling_key_do_not_give_reviewer.jsonl"
    fixtures_path = staging / "calibration_input.jsonl"
    answers_path = staging / "calibration_answer_key_do_not_give_reviewer.jsonl"
    guidance_path = staging / "reviewer_guidance.md"
    batch_root = staging / "review_batches" / "inputs"
    batch_root.mkdir(parents=True, exist_ok=False)
    write_jsonl_new(reviewer_path, reviewer_rows)
    write_jsonl_new(key_path, key_rows)
    write_jsonl_new(fixtures_path, fixtures)
    write_jsonl_new(answers_path, answers)
    write_text_new(guidance_path, GUIDANCE)
    batches: list[dict[str, Any]] = []
    for batch_index in range(QA_SAMPLE_SIZE // BATCH_SIZE):
        rows = reviewer_rows[batch_index * BATCH_SIZE : (batch_index + 1) * BATCH_SIZE]
        input_path = batch_root / f"review_batch_{batch_index:03d}_input.jsonl"
        write_jsonl_new(input_path, rows)
        batches.append({"batch_index": batch_index, "input_path": relative(qa_root / "review_batches" / "inputs" / input_path.name, root), "input_sha256": sha256_file(input_path), "expected_rows": BATCH_SIZE, "review_ids": [row["review_id"] for row in rows], "reviewer_assignment": "unassigned; manual QA completion is not authorised"})
    protocol = {
        "schema_version": "rq2b-i3c-v3-calibrated-qa-protocol-v1",
        "version_id": VERSION_ID,
        "purpose": "blinded source-to-selector-evidence extraction fidelity only",
        "population": "120 pairs: all 32 repaired root-coverage chunk rows plus 88 deterministic coverage/stratified rows",
        "calibration": {"fixtures": CALIBRATION_SIZE, "pass_rule": "all eight severity, field, and code decisions must match before batch assignment"},
        "acceptance_rule": {"critical_error_rows": 0, "maximum_major_error_rows": 6, "maximum_major_error_rate": 0.05},
        "selector_visibility_rule": "score only native metadata and literal evidence; parser-normalised text is not selector-visible and is hidden",
        "network_calls": 0,
        "external_api_calls": 0,
        "manual_qa_completion_authorized": False,
        "retrieval_or_reranking": False,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "protocol.json", protocol)
    manifest = {
        "schema_version": "rq2b-i3c-v3-calibrated-qa-packet-v1",
        "version_id": VERSION_ID,
        "state": "frozen_calibration_pending_manual_qa_authorisation",
        "sample_size": QA_SAMPLE_SIZE,
        "pinned_root_coverage_rows": len(pinned),
        "stratified_rows": QA_SAMPLE_SIZE - len(pinned),
        "calibration_size": CALIBRATION_SIZE,
        "batch_count": len(batches),
        "batch_size": BATCH_SIZE,
        "network_calls": 0,
        "external_api_calls": 0,
        "manual_qa_completion_authorized": False,
        "retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "bound_final_merge_manifest": {"path": relative(root / MERGED_ROOT / "manifest.json", root), "sha256": sha256_file(root / MERGED_ROOT / "manifest.json")},
        "artifacts": {
            "protocol": {"path": relative(qa_root / "protocol.json", root), "sha256": sha256_file(staging / "protocol.json")},
            "reviewer_guidance": {"path": relative(qa_root / guidance_path.name, root), "sha256": sha256_file(guidance_path)},
            "blinded_reviewer_packet": {"path": relative(qa_root / reviewer_path.name, root), "sha256": sha256_file(reviewer_path), "rows": QA_SAMPLE_SIZE},
            "sampling_key_do_not_give_reviewer": {"path": relative(qa_root / key_path.name, root), "sha256": sha256_file(key_path), "rows": QA_SAMPLE_SIZE},
            "calibration_input": {"path": relative(qa_root / fixtures_path.name, root), "sha256": sha256_file(fixtures_path), "rows": CALIBRATION_SIZE},
            "calibration_answer_key_do_not_give_reviewer": {"path": relative(qa_root / answers_path.name, root), "sha256": sha256_file(answers_path), "rows": CALIBRATION_SIZE},
        },
        "batches": batches,
    }
    write_json_new(staging / "manifest.json", manifest)
    checkpoint = {
        "schema_version": "rq2b-i3c-v3-calibrated-qa-packet-checkpoint-v1",
        "version_id": VERSION_ID,
        "state": "calibrated_blinded_qa_packet_built_manual_qa_not_authorized",
        "packet_manifest": {"path": relative(qa_root / "manifest.json", root), "sha256": sha256_file(staging / "manifest.json")},
        "network_calls": 0,
        "external_api_calls": 0,
        "manual_qa_completion_authorized": False,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "qa_packet_checkpoint.json", checkpoint)
    staging.rename(qa_root)
    return checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--qa-directory", default=DEFAULT_QA_DIRECTORY)
    args = parser.parse_args()
    print(json.dumps(build(args.root.resolve(), args.qa_directory), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
