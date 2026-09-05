#!/usr/bin/env python3
"""Locally merge the approved RQ2b v1.2 I3C extraction and stop at manual QA.

This consumes only the approved, source-only v1.2 extraction artifacts.  It
performs no network access, retrieval, reranking, or thesis-result writing.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import canonical_extraction, representation_row, summarize
from rq2b_common import (
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    serialize_i3_flat,
    serialize_i3c,
    sha256_file,
    write_json_new,
    write_jsonl_new,
)


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
EXTRACTION_ROOT = f"{RELATIVE_ROOT}/i3c_extraction"
PACKET = f"{RELATIVE_ROOT}/i3c_source_assignment_approval_packet.json"
RECEIPT = f"{RELATIVE_ROOT}/i3c_source_assignment_approval_receipt.json"
MERGED_ROOT = f"{RELATIVE_ROOT}/i3c_merged"
CHECKPOINT = f"{RELATIVE_ROOT}/i3c_extraction_completion_checkpoint.json"
APPROVED_PACKET_SHA256 = "472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe"
MERGER_VERSION = "rq2b-v12-i3c-local-merger-v1"


def verify_authorisation(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Bind the merge to the exact packet and its explicit local-only receipt."""
    packet_path = root / PACKET
    receipt_path = root / RECEIPT
    extraction_manifest_path = root / EXTRACTION_ROOT / "manifest.json"
    require(packet_path.is_file() and receipt_path.is_file(), "v1.2 I3C approval artifacts are missing")
    require(sha256_file(packet_path) == APPROVED_PACKET_SHA256, "v1.2 I3C packet hash mismatch")
    packet = read_json(packet_path)
    receipt = read_json(receipt_path)
    extraction_manifest = read_json(extraction_manifest_path)
    require(packet["schema_version"] == "rq2b-v12-i3c-source-assignment-approval-packet-v1", "v1.2 packet schema mismatch")
    require(packet["version_id"] == VERSION_ID and len(packet["chunks"]) == 57, "v1.2 packet inventory mismatch")
    require(receipt["schema_version"] == "rq2b-v12-i3c-source-assignment-approval-receipt-v1", "v1.2 receipt schema mismatch")
    require(receipt["state"] == "explicitly_approved_for_v12_i3c_source_assignment_once", "v1.2 receipt state mismatch")
    require(receipt["approved_packet"]["sha256"] == APPROVED_PACKET_SHA256, "v1.2 receipt packet mismatch")
    require(extraction_manifest["version_id"] == VERSION_ID, "v1.2 extraction manifest version mismatch")
    require(extraction_manifest["counts"]["input_rows"] == 2433, "v1.2 input row count mismatch")
    require(extraction_manifest["network_calls"] == extraction_manifest["external_api_calls"] == 0, "v1.2 extraction crossed network boundary")
    return packet, receipt, extraction_manifest


def merge(root: Path) -> dict[str, Any]:
    packet, receipt, extraction_manifest = verify_authorisation(root)
    merged_root = root / MERGED_ROOT
    staging_root = merged_root.with_name(".i3c_merged.staging")
    checkpoint_path = root / CHECKPOINT
    require(not merged_root.exists(), f"Refusing to overwrite merged I3C: {merged_root}")
    require(not staging_root.exists(), f"Stale merge staging directory: {staging_root}")
    require(not checkpoint_path.exists(), f"Refusing to overwrite v1.2 checkpoint: {checkpoint_path}")

    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    worker_outputs: list[dict[str, Any]] = []
    canonicalization_seconds = fielded_seconds = flat_seconds = 0.0

    for chunk in packet["chunks"]:
        input_path = root / chunk["input_path"]
        output_path = root / chunk["expected_output_path"]
        require(input_path.is_file() and output_path.is_file(), f"Missing v1.2 I3C chunk: {chunk['chunk_index']}")
        require(sha256_file(input_path) == chunk["planned_input_sha256"], f"Input hash drift: {chunk['chunk_index']}")
        inputs, outputs = read_jsonl(input_path), read_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["row_count"], f"Chunk row count mismatch: {chunk['chunk_index']}")
        worker_outputs.append({"chunk_index": chunk["chunk_index"], "path": relative(output_path, root), "sha256": sha256_file(output_path), "rows": len(outputs)})
        for input_row, output_row in zip(inputs, outputs, strict=True):
            started = time.perf_counter()
            canonical, retained, _ = canonical_extraction(input_row, output_row)
            canonicalization_seconds += time.perf_counter() - started
            canonical["merger_version"] = MERGER_VERSION
            started = time.perf_counter()
            fielded = serialize_i3c(input_row["name"], input_row["description"], retained)
            fielded_seconds += time.perf_counter() - started
            started = time.perf_counter()
            flat = serialize_i3_flat(input_row["name"], input_row["description"], retained)
            flat_seconds += time.perf_counter() - started
            canonical_rows.append(canonical)
            fielded_rows.append(representation_row(canonical, "i3c-fielded-evidence", fielded))
            flat_rows.append(representation_row(canonical, "i3-flat-evidence", flat))

    require(len(canonical_rows) == 2433, "Merged v1.2 I3C row count mismatch")
    require([row["source_row_index"] for row in canonical_rows] == list(range(2433)), "Merged v1.2 row-index drift")
    require(len({row["skill_id"] for row in canonical_rows}) == 2433, "Merged v1.2 skill-ID duplicate")
    summary = summarize(canonical_rows, fielded_rows, flat_rows)
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "v1.2 merge automatic gate failure")

    staging_root.mkdir(parents=True, exist_ok=False)
    artifact_paths = {
        "canonical_extractions": staging_root / "canonical_extractions.jsonl",
        "i3c-fielded-evidence": staging_root / "i3c-fielded-evidence.jsonl",
        "i3-flat-evidence": staging_root / "i3-flat-evidence.jsonl",
    }
    write_jsonl_new(artifact_paths["canonical_extractions"], canonical_rows)
    write_jsonl_new(artifact_paths["i3c-fielded-evidence"], fielded_rows)
    write_jsonl_new(artifact_paths["i3-flat-evidence"], flat_rows)
    manifest = {
        "schema_version": "rq2b-v12-i3c-merge-manifest-v1",
        "version_id": VERSION_ID,
        "state": "automatic_gates_passed_manual_qa_pending",
        "merger_version": MERGER_VERSION,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "source_assignment_packet": {"path": PACKET, "sha256": APPROVED_PACKET_SHA256},
        "source_assignment_receipt": {"path": RECEIPT, "sha256": sha256_file(root / RECEIPT)},
        "extraction_manifest": {"path": f"{EXTRACTION_ROOT}/manifest.json", "sha256": sha256_file(root / EXTRACTION_ROOT / "manifest.json")},
        "worker_outputs": worker_outputs,
        "timing": {"canonicalization_seconds": canonicalization_seconds, "i3c_serialization_seconds": fielded_seconds, "i3flat_serialization_seconds": flat_seconds},
        "summary": summary,
        "artifacts": {key: {"path": relative(merged_root / path.name, root), "sha256": sha256_file(path), "rows": len(canonical_rows)} for key, path in artifact_paths.items()},
        "manual_qa": {"required": True, "state": "pending", "review_rows": 120, "completion_authorized": False},
        "retrieval_authorized": False,
    }
    write_json_new(staging_root / "manifest.json", manifest)
    staging_root.replace(merged_root)
    checkpoint = {
        "schema_version": "rq2b-v12-i3c-extraction-completion-checkpoint-v1",
        "version_id": VERSION_ID,
        "state": "automatic_gates_passed_manual_qa_packet_not_yet_built",
        "merged_manifest": {"path": relative(merged_root / "manifest.json", root), "sha256": sha256_file(merged_root / "manifest.json")},
        "rows": 2433,
        "chunks": 57,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "manual_qa_completion_authorized": False,
        "thesis_result_writing": False,
    }
    write_json_new(checkpoint_path, checkpoint)
    return checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(merge(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
