#!/usr/bin/env python3
"""Freeze six blind local-review batches for the RQ2b v1.1 I3C QA packet.

The builder copies only 20 blinded reviewer rows into each batch. It never
opens the sampling key during batch creation, never makes a network call, and
does not run retrieval, embeddings, reranking, or scientific scoring.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new
from rq2b_v11_contract import RELATIVE_ROOT, VERSION_ID
from build_rq2b_v11_i3c_qa_packet import QA_ROOT, QA_SAMPLE_SIZE, verify as verify_qa_packet


BATCH_COUNT = 6
BATCH_SIZE = 20
BATCH_ROOT = f"{QA_ROOT}/review_batches"
BATCH_MANIFEST = f"{BATCH_ROOT}/manifest.json"


def build(root: Path) -> dict[str, Any]:
    verify_qa_packet(root)
    qa_root = root / QA_ROOT
    packet_manifest_path = qa_root / "manifest.json"
    packet = read_json(packet_manifest_path)
    reviewer_ref = packet["artifacts"]["blinded_reviewer_packet"]
    reviewer_path = root / reviewer_ref["path"]
    reviewer_rows = read_jsonl(reviewer_path)
    require(len(reviewer_rows) == QA_SAMPLE_SIZE == BATCH_COUNT * BATCH_SIZE, "I3C QA batch sizing mismatch")
    require(sha256_file(reviewer_path) == reviewer_ref["sha256"], "I3C QA reviewer packet hash drift")

    batch_root = root / BATCH_ROOT
    staging = batch_root.with_name(".review_batches.staging")
    require(not batch_root.exists() and not staging.exists(), "Refusing to overwrite or mix I3C QA batches")
    input_root = staging / "inputs"
    output_root = staging / "outputs"
    input_root.mkdir(parents=True, exist_ok=False)
    output_root.mkdir(parents=True, exist_ok=False)
    batches: list[dict[str, Any]] = []
    for batch_index in range(BATCH_COUNT):
        start = batch_index * BATCH_SIZE
        rows = reviewer_rows[start : start + BATCH_SIZE]
        require(len(rows) == BATCH_SIZE, "I3C QA batch row count drift")
        input_path = input_root / f"review_batch_{batch_index:03d}_input.jsonl"
        output_path = output_root / f"review_batch_{batch_index:03d}_completed.jsonl"
        write_jsonl_new(input_path, rows)
        batches.append({
            "batch_index": batch_index,
            "input_path": relative(batch_root / "inputs" / input_path.name, root),
            "input_sha256": sha256_file(input_path),
            "output_path": relative(batch_root / "outputs" / output_path.name, root),
            "expected_rows": BATCH_SIZE,
            "sample_index_start": start,
            "sample_index_end": start + BATCH_SIZE - 1,
            "review_ids": [row["review_id"] for row in rows],
        })
    manifest = {
        "schema_version": "rq2b-v11-i3c-manual-qa-batches-v1",
        "version_id": VERSION_ID,
        "state": "blind_review_batches_pending",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "qa_packet_manifest": {
            "path": relative(packet_manifest_path, root),
            "sha256": sha256_file(packet_manifest_path),
        },
        "blinded_reviewer_packet": reviewer_ref,
        "reviewer_visibility": {
            "only_assigned_input_batch": True,
            "sampling_key_prohibited": True,
            "prompt_gold_stratum_role_prohibited": True,
        },
        "review_contract": {
            "critical_error": [
                "identity mismatch",
                "benchmark-role leakage",
                "non-substring selector text",
                "unsupported evidence",
            ],
            "major_error": [
                "selector-visible span assigned to the wrong operational field",
                "generic or non-routing selector span likely to alter retrieval",
            ],
            "do_not_repair": True,
            "complete_every_assigned_row": True,
            "mark_false_when_no_error": True,
            "completed_row_keys": [
                "sample_index", "review_id", "critical_error", "major_error",
                "major_error_fields", "error_codes", "reviewer_notes", "reviewer_id",
            ],
        },
        "batches": batches,
        "manual_qa_completion_authorized": False,
        "retrieval_authorized": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(batch_root)
    return verify(root)


def verify(root: Path, *, allow_completed_outputs: bool = False) -> dict[str, Any]:
    verify_qa_packet(root)
    manifest_path = root / BATCH_MANIFEST
    require(manifest_path.is_file(), "I3C QA batch manifest is missing")
    manifest = read_json(manifest_path)
    require(manifest.get("schema_version") == "rq2b-v11-i3c-manual-qa-batches-v1", "I3C QA batch schema mismatch")
    require(manifest.get("version_id") == VERSION_ID and manifest.get("state") == "blind_review_batches_pending", "I3C QA batch state mismatch")
    require(manifest.get("network_calls") == manifest.get("external_api_calls") == 0, "I3C QA batches record external access")
    require(manifest.get("scientific_retrieval_or_reranking") is False, "I3C QA batches crossed retrieval boundary")
    require(manifest.get("manual_qa_completion_authorized") is False and manifest.get("retrieval_authorized") is False, "I3C QA batch authorization boundary drift")
    qa_manifest_path = root / QA_ROOT / "manifest.json"
    expected_binding = {"path": relative(qa_manifest_path, root), "sha256": sha256_file(qa_manifest_path)}
    require(manifest.get("qa_packet_manifest") == expected_binding, "I3C QA batch packet binding drift")
    batches = manifest.get("batches")
    require(isinstance(batches, list) and len(batches) == BATCH_COUNT, "I3C QA batch count mismatch")
    expected_indices = list(range(QA_SAMPLE_SIZE))
    actual_indices: list[int] = []
    review_ids: list[str] = []
    for expected_batch_index, batch in enumerate(batches):
        require(batch.get("batch_index") == expected_batch_index, "I3C QA batch ordering mismatch")
        rows = read_jsonl(root / batch["input_path"])
        require(len(rows) == batch["expected_rows"] == BATCH_SIZE, "I3C QA batch input count mismatch")
        require(sha256_file(root / batch["input_path"]) == batch["input_sha256"], "I3C QA batch input hash drift")
        if not allow_completed_outputs:
            require(not (root / batch["output_path"]).exists(), "I3C QA batch output unexpectedly exists")
        actual_indices.extend(row["sample_index"] for row in rows)
        review_ids.extend(row["review_id"] for row in rows)
        require([row["review_id"] for row in rows] == batch["review_ids"], "I3C QA batch review identity mismatch")
    require(actual_indices == expected_indices and len(set(review_ids)) == QA_SAMPLE_SIZE, "I3C QA batch global identity mismatch")
    return {"state": "blind_review_batches_pending", "batches": BATCH_COUNT, "rows_per_batch": BATCH_SIZE, "network_calls": 0, "external_api_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    print(json.dumps(verify(root) if args.verify_only else build(root), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
