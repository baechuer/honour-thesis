#!/usr/bin/env python3
"""Create immutable final V3 I3C artifacts after a hash-bound repair approval."""

from __future__ import annotations

import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import canonical_extraction, representation_row, summarize
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, serialize_i3_flat, serialize_i3c, sha256_file, write_json_new, write_jsonl_new


VERSION_ID = "rq2b-i3c-v3-2026-08-18"
V3_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
V12_ROOT = "skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16"
PACKET = f"{V3_ROOT}/finalisation_approval_packet.json"
RECEIPT = f"{V3_ROOT}/finalisation_approval_receipt.json"
SOURCE_MANIFEST = f"{V12_ROOT}/source_manifest.jsonl"
MERGED_ROOT = f"{V3_ROOT}/i3c_merged_final"
CHECKPOINT = f"{V3_ROOT}/i3c_finalisation_completion_checkpoint.json"
MERGER_VERSION = "rq2b-i3c-v3-final-local-merger-v1"


def verify(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    packet_path, receipt_path = root / PACKET, root / RECEIPT
    require(packet_path.is_file() and receipt_path.is_file(), "V3 finalisation approval is missing")
    packet, receipt = read_json(packet_path), read_json(receipt_path)
    require(packet["state"] == "awaiting_explicit_finalisation_approval", "unexpected finalisation packet state")
    require(receipt.get("state") == "explicitly_approved_for_v3_finalisation_once", "V3 finalisation is not approved")
    require(receipt.get("approved_packet", {}).get("sha256") == sha256_file(packet_path), "finalisation receipt packet mismatch")
    require(packet["implementation"]["merger_sha256"] == sha256_file(Path(__file__)), "final merger implementation drift")
    require(len(packet["worker_outputs"]) == 57, "finalisation worker inventory mismatch")
    return packet, receipt


def root_coverage(root: Path, canonical_rows: list[dict[str, Any]]) -> dict[str, Any]:
    sources = read_jsonl(root / SOURCE_MANIFEST)
    source_by_id = {row["skill_id"]: row for row in sources}
    fieldless: list[str] = []
    use_when_fieldless: list[str] = []
    for row in canonical_rows:
        source = source_by_id[row["skill_id"]]
        description = str(source.get("source_description") or "").strip()
        if source["source_policy"] == "public_original" and description and not any(row["fields"].values()):
            fieldless.append(row["skill_id"])
            if "use when" in description.lower():
                use_when_fieldless.append(row["skill_id"])
    public_descriptions = [row for row in sources if row["source_policy"] == "public_original" and str(row.get("source_description") or "").strip()]
    public_use_when = [row for row in public_descriptions if "use when" in str(row["source_description"]).lower()]
    return {
        "public_original_nonempty_description_rows": len(public_descriptions),
        "public_original_description_contains_use_when_rows": len(public_use_when),
        "fieldless_nonempty_public_description_rows": len(fieldless),
        "fieldless_public_description_contains_use_when_rows": len(use_when_fieldless),
        "fieldless_skill_ids": fieldless,
    }


def source_duplicate_groups(root: Path) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in read_jsonl(root / SOURCE_MANIFEST):
        groups[row["source_sha256"]].append(row["skill_id"])
    return [{"source_sha256": digest, "skill_ids": sorted(ids)} for digest, ids in sorted(groups.items()) if len(ids) > 1]


def merge(root: Path) -> dict[str, Any]:
    packet, _ = verify(root)
    merged_root, checkpoint = root / MERGED_ROOT, root / CHECKPOINT
    staging = merged_root.with_name(".i3c_merged_final.staging")
    require(not merged_root.exists() and not checkpoint.exists() and not staging.exists(), "refusing to overwrite V3 final artifacts")
    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    timings = {"canonicalization_seconds": 0.0, "i3c_serialization_seconds": 0.0, "i3flat_serialization_seconds": 0.0}
    for chunk in packet["worker_outputs"]:
        input_path, output_path = root / chunk["input_path"], root / chunk["output_path"]
        require(sha256_file(input_path) == chunk["input_sha256"], f"final input hash drift: {chunk['chunk_index']}")
        require(sha256_file(output_path) == chunk["output_sha256"], f"final output hash drift: {chunk['chunk_index']}")
        inputs, outputs = read_jsonl(input_path), read_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["rows"], f"final worker row count mismatch: {chunk['chunk_index']}")
        for input_row, output_row in zip(inputs, outputs, strict=True):
            started = time.perf_counter()
            canonical, retained, _ = canonical_extraction(input_row, output_row)
            timings["canonicalization_seconds"] += time.perf_counter() - started
            canonical["merger_version"] = MERGER_VERSION
            started = time.perf_counter()
            fielded = serialize_i3c(input_row["name"], input_row["description"], retained)
            timings["i3c_serialization_seconds"] += time.perf_counter() - started
            started = time.perf_counter()
            flat = serialize_i3_flat(input_row["name"], input_row["description"], retained)
            timings["i3flat_serialization_seconds"] += time.perf_counter() - started
            canonical_rows.append(canonical)
            fielded_rows.append(representation_row(canonical, "i3c-fielded-evidence", fielded))
            flat_rows.append(representation_row(canonical, "i3-flat-evidence", flat))
    require(len(canonical_rows) == 2433 and [row["source_row_index"] for row in canonical_rows] == list(range(2433)), "final canonical order drift")
    require(len({row["skill_id"] for row in canonical_rows}) == 2433, "final duplicate skill ID")
    summary = summarize(canonical_rows, fielded_rows, flat_rows)
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "final automatic merge failure")
    coverage = root_coverage(root, canonical_rows)
    require(coverage["fieldless_nonempty_public_description_rows"] == 0, "final root coverage failure")
    require(coverage["fieldless_public_description_contains_use_when_rows"] == 0, "final use-when root coverage failure")
    staging.mkdir(parents=True, exist_ok=False)
    paths = {"canonical_extractions": staging / "canonical_extractions.jsonl", "i3c-fielded-evidence": staging / "i3c-fielded-evidence.jsonl", "i3-flat-evidence": staging / "i3-flat-evidence.jsonl"}
    for key, path in paths.items():
        write_jsonl_new(path, canonical_rows if key == "canonical_extractions" else fielded_rows if key == "i3c-fielded-evidence" else flat_rows)
    write_json_new(staging / "root_coverage_report.json", coverage)
    manifest = {
        "schema_version": "rq2b-i3c-v3-final-merge-manifest-v1",
        "version_id": VERSION_ID,
        "state": "automatic_gates_passed_manual_qa_pending",
        "merger_version": MERGER_VERSION,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "finalisation_packet": {"path": PACKET, "sha256": sha256_file(root / PACKET)},
        "finalisation_receipt": {"path": RECEIPT, "sha256": sha256_file(root / RECEIPT)},
        "summary": summary,
        "root_coverage": coverage,
        "exact_source_duplicate_groups": source_duplicate_groups(root),
        "artifacts": {key: {"path": relative(merged_root / path.name, root), "sha256": sha256_file(path), "rows": len(canonical_rows)} for key, path in paths.items()},
        "root_coverage_report": {"path": relative(merged_root / "root_coverage_report.json", root), "sha256": sha256_file(staging / "root_coverage_report.json")},
        "manual_qa": {"required": True, "state": "pending", "review_rows": 120, "completion_authorized": False},
        "retrieval_authorized": False,
        "timing": timings,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(merged_root)
    checkpoint_value = {
        "schema_version": "rq2b-i3c-v3-finalisation-checkpoint-v1",
        "version_id": VERSION_ID,
        "state": "automatic_gates_passed_calibrated_qa_packet_not_yet_built",
        "merged_manifest": {"path": relative(merged_root / "manifest.json", root), "sha256": sha256_file(merged_root / "manifest.json")},
        "rows": 2433,
        "chunks": 57,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "manual_qa_completion_authorized": False,
        "thesis_result_writing": False,
    }
    write_json_new(checkpoint, checkpoint_value)
    return checkpoint_value


def main() -> int:
    print(json.dumps(merge(repo_root()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
