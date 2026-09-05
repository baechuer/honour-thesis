#!/usr/bin/env python3
"""Merge an approved RQ2b I3C V3 extraction without running retrieval."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import canonical_extraction, representation_row, summarize
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, serialize_i3_flat, serialize_i3c, sha256_file, write_json_new, write_jsonl_new


V3_VERSION_ID = "rq2b-i3c-v3-2026-08-18"
V3_ROOT = f"skill_benchmark/rq2b_full_library/{V3_VERSION_ID}"
PACKET = f"{V3_ROOT}/source_assignment_approval_packet_sealed.json"
RECEIPT = f"{V3_ROOT}/source_assignment_approval_receipt.json"
EXTRACTION_ROOT = f"{V3_ROOT}/i3c_extraction"
MERGED_ROOT = f"{V3_ROOT}/i3c_merged"
CHECKPOINT = f"{V3_ROOT}/i3c_extraction_completion_checkpoint.json"
MERGER_VERSION = "rq2b-i3c-v3-local-merger-v1"


def verify_approval(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    packet_path = root / PACKET
    receipt_path = root / RECEIPT
    extraction_path = root / EXTRACTION_ROOT / "manifest.json"
    require(packet_path.is_file() and receipt_path.is_file() and extraction_path.is_file(), "V3 approval or extraction manifest missing")
    packet, receipt, extraction = read_json(packet_path), read_json(receipt_path), read_json(extraction_path)
    require(packet["schema_version"] == "rq2b-i3c-v3-source-assignment-approval-packet-v1", "V3 packet schema mismatch")
    require(receipt.get("state") == "explicitly_approved_for_v3_i3c_source_assignment_once", "V3 receipt is not approved")
    require(receipt.get("approved_packet", {}).get("sha256") == sha256_file(packet_path), "V3 receipt packet mismatch")
    require(extraction["version_id"] == V3_VERSION_ID and extraction["counts"]["input_rows"] == 2433, "V3 input manifest mismatch")
    require(extraction["network_calls"] == extraction["external_api_calls"] == 0, "V3 extraction crossed network boundary")
    return packet, receipt


def merge(root: Path) -> dict[str, Any]:
    packet, receipt = verify_approval(root)
    merged_root = root / MERGED_ROOT
    staging = merged_root.with_name(".i3c_merged.staging")
    checkpoint = root / CHECKPOINT
    require(not merged_root.exists() and not staging.exists() and not checkpoint.exists(), "Refusing to overwrite V3 merge artifacts")
    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    worker_outputs: list[dict[str, Any]] = []
    timing = {"canonicalization_seconds": 0.0, "i3c_serialization_seconds": 0.0, "i3flat_serialization_seconds": 0.0}
    for chunk in packet["chunks"]:
        input_path, output_path = root / chunk["input_path"], root / chunk["expected_output_path"]
        require(input_path.is_file() and output_path.is_file(), f"Missing V3 chunk {chunk['chunk_index']}")
        require(sha256_file(input_path) == chunk["planned_input_sha256"], f"V3 input hash drift: {chunk['chunk_index']}")
        inputs, outputs = read_jsonl(input_path), read_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["row_count"], f"V3 row count mismatch: {chunk['chunk_index']}")
        worker_outputs.append({"chunk_index": chunk["chunk_index"], "path": relative(output_path, root), "sha256": sha256_file(output_path), "rows": len(outputs)})
        for input_row, output_row in zip(inputs, outputs, strict=True):
            started = time.perf_counter(); canonical, retained, _ = canonical_extraction(input_row, output_row); timing["canonicalization_seconds"] += time.perf_counter() - started
            canonical["merger_version"] = MERGER_VERSION
            started = time.perf_counter(); fielded = serialize_i3c(input_row["name"], input_row["description"], retained); timing["i3c_serialization_seconds"] += time.perf_counter() - started
            started = time.perf_counter(); flat = serialize_i3_flat(input_row["name"], input_row["description"], retained); timing["i3flat_serialization_seconds"] += time.perf_counter() - started
            canonical_rows.append(canonical); fielded_rows.append(representation_row(canonical, "i3c-fielded-evidence", fielded)); flat_rows.append(representation_row(canonical, "i3-flat-evidence", flat))
    require(len(canonical_rows) == 2433 and [row["source_row_index"] for row in canonical_rows] == list(range(2433)), "V3 canonical identity drift")
    require(len({row["skill_id"] for row in canonical_rows}) == 2433, "V3 duplicate skill ID")
    summary = summarize(canonical_rows, fielded_rows, flat_rows)
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "V3 automatic merge failure")
    staging.mkdir(parents=True, exist_ok=False)
    paths = {"canonical_extractions": staging / "canonical_extractions.jsonl", "i3c-fielded-evidence": staging / "i3c-fielded-evidence.jsonl", "i3-flat-evidence": staging / "i3-flat-evidence.jsonl"}
    for key, path in paths.items(): write_jsonl_new(path, canonical_rows if key == "canonical_extractions" else fielded_rows if key == "i3c-fielded-evidence" else flat_rows)
    manifest = {"schema_version": "rq2b-i3c-v3-merge-manifest-v1", "version_id": V3_VERSION_ID, "state": "automatic_gates_passed_manual_qa_pending", "merger_version": MERGER_VERSION, "network_calls": 0, "external_api_calls": 0, "scientific_retrieval_or_reranking": False, "thesis_result_writing": False, "source_assignment_packet": {"path": PACKET, "sha256": sha256_file(root / PACKET)}, "source_assignment_receipt": {"path": RECEIPT, "sha256": sha256_file(root / RECEIPT)}, "extraction_manifest": {"path": f"{EXTRACTION_ROOT}/manifest.json", "sha256": sha256_file(root / EXTRACTION_ROOT / "manifest.json")}, "worker_outputs": worker_outputs, "timing": timing, "summary": summary, "artifacts": {key: {"path": relative(merged_root / path.name, root), "sha256": sha256_file(path), "rows": len(canonical_rows)} for key, path in paths.items()}, "manual_qa": {"required": True, "state": "pending", "review_rows": 120, "completion_authorized": False}, "retrieval_authorized": False}
    write_json_new(staging / "manifest.json", manifest); staging.replace(merged_root)
    checkpoint_value = {"schema_version": "rq2b-i3c-v3-extraction-completion-checkpoint-v1", "version_id": V3_VERSION_ID, "state": "automatic_gates_passed_manual_qa_packet_not_yet_built", "merged_manifest": {"path": relative(merged_root / "manifest.json", root), "sha256": sha256_file(merged_root / "manifest.json")}, "rows": 2433, "chunks": 57, "network_calls": 0, "external_api_calls": 0, "scientific_retrieval_or_reranking": False, "manual_qa_completion_authorized": False, "thesis_result_writing": False}
    write_json_new(checkpoint, checkpoint_value)
    return checkpoint_value


def main() -> int:
    print(json.dumps(merge(repo_root()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
