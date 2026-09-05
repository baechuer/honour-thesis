#!/usr/bin/env python3
"""Freeze six blinded local-review batches for the RQ2b v1.2 I3C QA packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
QA_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa"
BATCH_ROOT = f"{QA_ROOT}/review_batches"
BATCH_MANIFEST = f"{BATCH_ROOT}/manifest.json"
QA_SAMPLE_SIZE = 120
BATCH_COUNT = 6
BATCH_SIZE = 20


def verify_packet(root: Path) -> dict[str, Any]:
    packet_path = root / QA_ROOT / "manifest.json"
    require(packet_path.is_file(), "v1.2 I3C QA packet is missing")
    packet = read_json(packet_path)
    require(packet["version_id"] == VERSION_ID and packet["state"] == "blinded_review_pending", "v1.2 I3C QA packet state mismatch")
    require(packet["sample_size"] == QA_SAMPLE_SIZE, "v1.2 I3C QA sample size mismatch")
    require(packet["network_calls"] == packet["external_api_calls"] == 0, "v1.2 QA packet crossed external boundary")
    require(packet["manual_qa_completion_authorized"] is False, "QA packet must remain uncompleted before receipt")
    reviewer = packet["artifacts"]["blinded_reviewer_packet"]
    reviewer_path = root / reviewer["path"]
    require(sha256_file(reviewer_path) == reviewer["sha256"], "v1.2 reviewer packet hash drift")
    rows = read_jsonl(reviewer_path)
    require(len(rows) == QA_SAMPLE_SIZE, "v1.2 reviewer packet row count mismatch")
    return packet


def build(root: Path) -> dict[str, Any]:
    packet = verify_packet(root)
    reviewer_ref = packet["artifacts"]["blinded_reviewer_packet"]
    reviewer_rows = read_jsonl(root / reviewer_ref["path"])
    batch_root = root / BATCH_ROOT
    staging = batch_root.with_name(".review_batches.staging")
    require(not batch_root.exists() and not staging.exists(), "refusing to overwrite or mix v1.2 I3C QA batches")
    input_root = staging / "inputs"
    output_root = staging / "outputs"
    input_root.mkdir(parents=True, exist_ok=False)
    output_root.mkdir(parents=True, exist_ok=False)
    batches: list[dict[str, Any]] = []
    for batch_index in range(BATCH_COUNT):
        start = batch_index * BATCH_SIZE
        rows = reviewer_rows[start : start + BATCH_SIZE]
        require(len(rows) == BATCH_SIZE, "v1.2 I3C QA batch row count drift")
        input_path = input_root / f"review_batch_{batch_index:03d}_input.jsonl"
        output_path = output_root / f"review_batch_{batch_index:03d}_completed.jsonl"
        write_jsonl_new(input_path, rows)
        batches.append(
            {
                "batch_index": batch_index,
                "input_path": relative(batch_root / "inputs" / input_path.name, root),
                "input_sha256": sha256_file(input_path),
                "output_path": relative(batch_root / "outputs" / output_path.name, root),
                "expected_rows": BATCH_SIZE,
                "review_ids": [row["review_id"] for row in rows],
            }
        )
    manifest = {
        "schema_version": "rq2b-v12-i3c-manual-qa-batches-v1",
        "version_id": VERSION_ID,
        "state": "blind_review_batches_frozen_pending_completion_receipt",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "qa_packet_manifest": {"path": relative(root / QA_ROOT / "manifest.json", root), "sha256": sha256_file(root / QA_ROOT / "manifest.json")},
        "blinded_reviewer_packet": reviewer_ref,
        "reviewer_visibility": {
            "only_assigned_input_batch": True,
            "sampling_key_prohibited": True,
            "prompt_gold_alternatives_role_stratum_cluster_retrieval_prohibited": True,
        },
        "review_contract": {
            "purpose": "source-to-I3C extraction fidelity only",
            "critical_error": ["unsupported content", "identity-breaking content", "benchmark-scaffold leakage", "evidence not present in source"],
            "major_error": ["material missing content", "material unsupported or misclassified field", "misleading selector-visible span"],
            "error_codes": ["unsupported_content", "identity_mismatch", "evidence_not_exact", "evidence_not_meaningful", "missing_material_field", "misclassified_field", "misleading_selector_span", "benchmark_scaffold_leakage", "other"],
            "do_not_repair_or_rewrite": True,
            "complete_every_assigned_row": True,
            "mark_false_when_no_error": True,
            "completed_row_keys": ["review_id", "review_status", "critical_error", "major_error", "major_error_fields", "error_codes", "reviewer_notes", "reviewer_id"],
        },
        "batches": batches,
        "manual_qa_completion_authorized": False,
        "retrieval_authorized": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(batch_root)
    return verify(root, allow_completed_outputs=False)


def verify(root: Path, *, allow_completed_outputs: bool) -> dict[str, Any]:
    packet = verify_packet(root)
    manifest_path = root / BATCH_MANIFEST
    require(manifest_path.is_file(), "v1.2 I3C QA batch manifest is missing")
    manifest = read_json(manifest_path)
    require(manifest["version_id"] == VERSION_ID and manifest["state"] == "blind_review_batches_frozen_pending_completion_receipt", "v1.2 batch state mismatch")
    require(manifest["network_calls"] == manifest["external_api_calls"] == 0, "v1.2 QA batches crossed external boundary")
    require(manifest["scientific_retrieval_or_reranking"] is False and manifest["thesis_result_writing"] is False, "v1.2 QA batches crossed science boundary")
    require(manifest["manual_qa_completion_authorized"] is False and manifest["retrieval_authorized"] is False, "v1.2 batch approval boundary drift")
    expected_packet = {"path": relative(root / QA_ROOT / "manifest.json", root), "sha256": sha256_file(root / QA_ROOT / "manifest.json")}
    require(manifest["qa_packet_manifest"] == expected_packet, "v1.2 QA packet binding drift")
    batches = manifest["batches"]
    require(len(batches) == BATCH_COUNT, "v1.2 QA batch count mismatch")
    actual_review_ids: list[str] = []
    for expected_index, batch in enumerate(batches):
        require(batch["batch_index"] == expected_index and batch["expected_rows"] == BATCH_SIZE, "v1.2 QA batch indexing mismatch")
        input_path = root / batch["input_path"]
        output_path = root / batch["output_path"]
        rows = read_jsonl(input_path)
        require(sha256_file(input_path) == batch["input_sha256"], "v1.2 QA input hash drift")
        require(len(rows) == BATCH_SIZE and [row["review_id"] for row in rows] == batch["review_ids"], "v1.2 QA input identity mismatch")
        if not allow_completed_outputs:
            require(not output_path.exists(), "v1.2 QA output unexpectedly exists")
        actual_review_ids.extend(batch["review_ids"])
    require(len(actual_review_ids) == QA_SAMPLE_SIZE and len(set(actual_review_ids)) == QA_SAMPLE_SIZE, "v1.2 QA global review identity mismatch")
    require(set(actual_review_ids) == {row["review_id"] for row in read_jsonl(root / packet["artifacts"]["blinded_reviewer_packet"]["path"])}, "v1.2 QA batch coverage mismatch")
    return {"state": manifest["state"], "batches": BATCH_COUNT, "rows_per_batch": BATCH_SIZE, "network_calls": 0, "external_api_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    result = verify(root, allow_completed_outputs=False) if args.verify_only else build(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
