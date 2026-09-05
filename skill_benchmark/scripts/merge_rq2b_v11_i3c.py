#!/usr/bin/env python3
"""Merge the approved RQ2b v1.1 I3C extraction and verify its local ledger.

The source chunks remain owned by the frozen v1 parent corpus.  This utility
writes only v1.1-derived artifacts, checks the authorised worker-event ledger,
and stops at the manual-QA boundary.  It does not run retrieval or contact any
external service.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import canonical_extraction, summarize as legacy_summarize
from rq2b_common import (
    FIELD_SPECS,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    selector_counts,
    serialize_i3_flat,
    serialize_i3c,
    sha256_file,
    sha256_text,
    write_json_new,
    write_jsonl_new,
)
from rq2b_v11_contract import RELATIVE_ROOT, VERSION_ID, verify as verify_v11_contract


MERGER_VERSION = "rq2b-v11-i3c-local-merger-v1"
PARENT_VERSION = "rq2b-full-library-v1-2026-08-02"
PARENT_ROOT = f"skill_benchmark/rq2b_full_library/{PARENT_VERSION}"
V11_ROOT = RELATIVE_ROOT
PACKET_RELATIVE = f"{V11_ROOT}/b1r_v11_authorisation_packet.json"
RECEIPT_RELATIVE = f"{V11_ROOT}/b1r_v11_approval_receipt.json"
EVENT_RELATIVE = f"{PARENT_ROOT}/i3c_extraction/worker_events.jsonl"
MERGE_RELATIVE = f"{V11_ROOT}/i3c_merged"
LEDGER_RELATIVE = f"{V11_ROOT}/i3c_extraction_execution_ledger.json"
PARENT_MANIFEST_RELATIVE = f"{PARENT_ROOT}/i3c_extraction/manifest.json"

APPROVED_PACKET_SHA256 = "fedb297afda625784225761b77c949d46c49d5df113f3e7f1df3b04b2648871f"
APPROVED_SCOPE_SHA256 = "b9a3dfc3ff95479403f6a21564aee62322e9296e0e950659d5955a8e42544cfc"
EVENT_KEYS = {
    "attempt_index",
    "automatic_retry",
    "chunk_index",
    "completed_at_epoch_seconds",
    "external_api_calls",
    "failure_reason",
    "input_path",
    "input_sha256",
    "network_calls",
    "output_path",
    "output_rows",
    "output_sha256",
    "schema_version",
    "started_at_epoch_seconds",
    "status",
    "version_id",
    "worker_id",
}


def verify_authorisation(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Verify the exact B1R approval, not merely a similarly named packet."""
    verify_v11_contract(root)
    packet_path = root / PACKET_RELATIVE
    receipt_path = root / RECEIPT_RELATIVE
    require(packet_path.is_file(), f"v1.1 B1R packet missing: {packet_path}")
    require(receipt_path.is_file(), f"v1.1 B1R receipt missing: {receipt_path}")
    require(sha256_file(packet_path) == APPROVED_PACKET_SHA256, "B1R packet hash is not the approved packet")
    packet = read_json(packet_path)
    receipt = read_json(receipt_path)
    require(packet.get("schema_version") == "rq2b-v11-b1r-authorisation-packet-v1", "B1R packet schema mismatch")
    require(packet.get("version_id") == VERSION_ID, "B1R packet version mismatch")
    require(packet.get("scope_sha256") == APPROVED_SCOPE_SHA256, "B1R packet scope mismatch")
    require(packet.get("state") == "awaiting_explicit_v11_b1r_source_transfer_approval", "B1R packet state mismatch")
    require(packet.get("external_texts_transmitted") == 0, "B1R packet records external transfer")
    require(receipt == {
        "authorised_by": "Jacky Zhang",
        "authorised_on": "2026-08-15",
        "authorised_source_transfer": True,
        "explicit_user_statement": "ok开始吧; this is interpreted in the immediately preceding B1R context as approval to begin only the recapitulated 2,433-skill, 57-chunk, max-six-worker local Codex I3C extraction scope.",
        "internet_or_external_api_authorised": False,
        "packet_sha256": APPROVED_PACKET_SHA256,
        "schema_version": "rq2b-v11-b1r-approval-receipt-v1",
        "scope_sha256": APPROVED_SCOPE_SHA256,
        "scientific_scoring_authorised": False,
        "state": "explicitly_approved_for_v11_b1r_once",
        "thesis_result_writing_authorised": False,
        "worker_model": "Codex subagent inherited model; low reasoning effort",
    }, "B1R approval receipt mismatch")
    return packet, receipt


def validate_events(root: Path, packet: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Recompute the B1R worker controls against the finished local outputs."""
    event_path = root / EVENT_RELATIVE
    require(event_path.is_file(), f"I3C worker-event ledger missing: {event_path}")
    events = read_jsonl(event_path)
    chunks = {int(chunk["chunk_index"]): chunk for chunk in packet["chunks"]}
    require(len(chunks) == 57, "B1R chunk inventory mismatch")
    source_text_bytes: dict[int, int] = {}
    for chunk_index, chunk in chunks.items():
        rows = read_jsonl(root / chunk["input_path"])
        require(len(rows) == chunk["row_count"], "I3C input row count drift")
        source_text_bytes[chunk_index] = sum(len(row["text"].encode("utf-8")) for row in rows)
    require(
        sum(source_text_bytes.values()) == packet["scope"]["source_utf8_bytes"],
        "B1R source-text byte total drift",
    )
    grouped: dict[int, list[dict[str, Any]]] = {}
    worker_ids: set[str] = set()
    for event in events:
        require(set(event) == EVENT_KEYS, "I3C worker-event key mismatch")
        require(event["schema_version"] == "rq2b-i3c-worker-event-v1", "I3C worker-event schema mismatch")
        require(event["version_id"] == VERSION_ID, "I3C worker-event version mismatch")
        chunk_index = event["chunk_index"]
        require(isinstance(chunk_index, int) and chunk_index in chunks, "Unknown I3C worker-event chunk")
        require(isinstance(event["attempt_index"], int) and event["attempt_index"] >= 1, "Invalid I3C attempt")
        require(isinstance(event["worker_id"], str) and event["worker_id"] and event["worker_id"] not in worker_ids, "Worker ID reused")
        worker_ids.add(event["worker_id"])
        require(event["status"] in {"completed", "failed"}, "Invalid I3C event status")
        require(event["network_calls"] == event["external_api_calls"] == 0, "I3C worker used external access")
        require(event["automatic_retry"] is False, "I3C automatic retry recorded")
        started = float(event["started_at_epoch_seconds"])
        ended = float(event["completed_at_epoch_seconds"])
        require(math.isfinite(started) and math.isfinite(ended) and ended >= started, "Invalid worker timing")
        chunk = chunks[chunk_index]
        require(event["input_path"] == chunk["input_path"], "Worker-event input path mismatch")
        require(event["input_sha256"] == chunk["input_sha256"], "Worker-event input hash mismatch")
        if event["status"] == "completed":
            require(event["failure_reason"] is None, "Completed worker event has a failure reason")
            require(event["output_path"] == chunk["expected_output_path"], "Worker-event output path mismatch")
            output_path = root / event["output_path"]
            require(output_path.is_file(), f"Completed output is missing: {output_path}")
            require(sha256_file(output_path) == event["output_sha256"], "Worker-event output hash drift")
            require(event["output_rows"] == chunk["row_count"] == len(read_jsonl(output_path)), "Worker-event output row mismatch")
        else:
            require(isinstance(event["failure_reason"], str) and event["failure_reason"], "Failed worker lacks a reason")
            require(event["output_path"] is None and event["output_sha256"] is None and event["output_rows"] == 0, "Failed worker claims a canonical output")
        grouped.setdefault(chunk_index, []).append(event)

    require(set(grouped) == set(chunks), "I3C worker-event coverage mismatch")
    final_events: list[dict[str, Any]] = []
    for chunk_index, attempt_events in grouped.items():
        ordered = sorted(attempt_events, key=lambda row: row["attempt_index"])
        require([row["attempt_index"] for row in ordered] == list(range(1, len(ordered) + 1)), "Non-contiguous attempt indexes")
        require(all(row["status"] == "failed" for row in ordered[:-1]), "Work continued after a completed event")
        require(ordered[-1]["status"] == "completed", "Chunk has no final completed event")
        for previous, current in zip(ordered, ordered[1:], strict=False):
            require(current["started_at_epoch_seconds"] >= previous["completed_at_epoch_seconds"], "Replacement overlapped prior worker")
        final_events.append(ordered[-1])
    active: list[dict[str, Any]] = []
    peak = 0
    for event in sorted(events, key=lambda row: (row["started_at_epoch_seconds"], row["completed_at_epoch_seconds"], row["chunk_index"], row["attempt_index"])):
        active = [row for row in active if row["completed_at_epoch_seconds"] > event["started_at_epoch_seconds"]]
        active.append(event)
        peak = max(peak, len(active))
    scope = packet["scope"]
    require(peak <= scope["maximum_active_workers"] == 6, "I3C active-worker ceiling exceeded")
    require(len(events) <= scope["maximum_total_assignment_attempts"], "I3C assignment ceiling exceeded")
    failed = [event for event in events if event["status"] == "failed"]
    require(len(failed) <= scope["maximum_replacement_assignments"], "I3C replacement ceiling exceeded")
    summary = {
        "assignments": len(events),
        "completed_chunks": len(final_events),
        "failed_attempts": len(failed),
        "unique_workers": len(worker_ids),
        "maximum_active_workers_allowed": scope["maximum_active_workers"],
        "maximum_active_workers_observed": peak,
        "new_worker_per_assignment_enforced": True,
        "replacement_nonoverlap_enforced": True,
        "worker_seconds_sum": sum(event["completed_at_epoch_seconds"] - event["started_at_epoch_seconds"] for event in events),
        "orchestrator_wall_seconds": max(event["completed_at_epoch_seconds"] for event in events) - min(event["started_at_epoch_seconds"] for event in events),
        "assigned_source_rows": sum(chunks[event["chunk_index"]]["row_count"] for event in events),
        "assigned_source_utf8_bytes": sum(source_text_bytes[event["chunk_index"]] for event in events),
        "assigned_input_artifact_utf8_bytes": sum(chunks[event["chunk_index"]]["utf8_bytes"] for event in events),
        "assigned_qwen_proxy_tokens": sum(chunks[event["chunk_index"]]["qwen_proxy_tokens"] for event in events),
    }
    require(summary["assigned_source_rows"] <= scope["maximum_assigned_source_rows"], "I3C assigned-row ceiling exceeded")
    require(summary["assigned_source_utf8_bytes"] <= scope["maximum_assigned_source_utf8_bytes"], "I3C assigned-byte ceiling exceeded")
    require(summary["assigned_qwen_proxy_tokens"] <= scope["maximum_assigned_qwen_proxy_tokens"], "I3C assigned-token ceiling exceeded")
    return events, summary


def representation_row(canonical: dict[str, Any], representation: str, selector_text: str) -> dict[str, Any]:
    return {
        "schema_version": "rq2b-representation-row-v1",
        "serializer_version": MERGER_VERSION,
        "representation": representation,
        "source_row_index": canonical["source_row_index"],
        "skill_id": canonical["skill_id"],
        "family": canonical["family"],
        "source_path": canonical["source"],
        "source_sha256": canonical["source_sha256"],
        "selector_text": selector_text,
        "selector_text_sha256": sha256_text(selector_text),
        "selector_visible_counts": selector_counts(selector_text),
        "selector_evidence_spans": [
            {
                "field_key": span["field_key"],
                "field_label": span["field_label"],
                "item_id": span["item_id"],
                "source_position": span["source_position"],
                "selector_evidence": span["selector_evidence"],
            }
            for span in canonical["retained_selector_spans"]
        ],
    }


def merge(root: Path) -> dict[str, Any]:
    packet, _ = verify_authorisation(root)
    events, execution_summary = validate_events(root, packet)
    parent_manifest_path = root / PARENT_MANIFEST_RELATIVE
    parent_manifest = read_json(parent_manifest_path)
    require(parent_manifest.get("counts", {}).get("input_rows") == 2433, "Parent I3C source count mismatch")
    require(len(packet["chunks"]) == len(parent_manifest.get("chunks", [])) == 57, "Parent/v1.1 chunk count mismatch")
    for packet_chunk, parent_chunk in zip(packet["chunks"], parent_manifest["chunks"], strict=True):
        require(packet_chunk["chunk_index"] == parent_chunk["chunk_index"], "Parent/v1.1 chunk index mismatch")
        for key in ("input_path", "input_sha256", "expected_output_path", "row_count"):
            require(packet_chunk[key] == parent_chunk[key], f"Parent/v1.1 chunk {key} mismatch")

    output_root = root / MERGE_RELATIVE
    ledger_path = root / LEDGER_RELATIVE
    staging_root = output_root.with_name(".i3c_merged.staging")
    require(not output_root.exists(), f"Refusing to overwrite merged I3C: {output_root}")
    require(not ledger_path.exists(), f"Refusing to overwrite I3C ledger: {ledger_path}")
    require(not staging_root.exists(), f"Stale merged-I3C staging root: {staging_root}")

    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    output_hashes: list[dict[str, Any]] = []
    canonicalization_seconds = 0.0
    fielded_serialization_seconds = 0.0
    flat_serialization_seconds = 0.0
    for chunk in packet["chunks"]:
        input_path = root / chunk["input_path"]
        output_path = root / chunk["expected_output_path"]
        require(sha256_file(input_path) == chunk["input_sha256"], "Input chunk hash drift")
        inputs = read_jsonl(input_path)
        outputs = read_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["row_count"], "I3C chunk row mismatch")
        output_hashes.append({"path": relative(output_path, root), "sha256": sha256_file(output_path), "rows": len(outputs)})
        for input_row, output_row in zip(inputs, outputs, strict=True):
            started = time.perf_counter()
            canonical, retained, _ = canonical_extraction(input_row, output_row)
            canonicalization_seconds += time.perf_counter() - started
            canonical["merger_version"] = MERGER_VERSION
            started = time.perf_counter()
            fielded = serialize_i3c(input_row["name"], input_row["description"], retained)
            fielded_serialization_seconds += time.perf_counter() - started
            started = time.perf_counter()
            flat = serialize_i3_flat(input_row["name"], input_row["description"], retained)
            flat_serialization_seconds += time.perf_counter() - started
            canonical_rows.append(canonical)
            fielded_rows.append(representation_row(canonical, "i3c-fielded-evidence", fielded))
            flat_rows.append(representation_row(canonical, "i3-flat-evidence", flat))

    require(len(canonical_rows) == 2433, "Merged I3C must contain exactly 2,433 rows")
    require([row["source_row_index"] for row in canonical_rows] == list(range(2433)), "Merged source indices are not contiguous")
    require(len({row["skill_id"] for row in canonical_rows}) == 2433, "Merged skill IDs are not unique")
    summary = legacy_summarize(canonical_rows, fielded_rows, flat_rows)
    require(summary["rows"] == 2433, "Merged summary row count mismatch")
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "Automatic gate failure")

    staging_root.mkdir(parents=True, exist_ok=False)
    artifacts = {
        "canonical_extractions": staging_root / "canonical_extractions.jsonl",
        "i3c-fielded-evidence": staging_root / "i3c-fielded-evidence.jsonl",
        "i3-flat-evidence": staging_root / "i3-flat-evidence.jsonl",
    }
    write_jsonl_new(artifacts["canonical_extractions"], canonical_rows)
    write_jsonl_new(artifacts["i3c-fielded-evidence"], fielded_rows)
    write_jsonl_new(artifacts["i3-flat-evidence"], flat_rows)
    merge_manifest = {
        "schema_version": "rq2b-v11-i3c-merge-manifest-v1",
        "version_id": VERSION_ID,
        "source_corpus_parent_version": PARENT_VERSION,
        "state": "automatic_gates_passed_manual_qa_pending",
        "merger_version": MERGER_VERSION,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "b1r_authorisation_packet": {"path": PACKET_RELATIVE, "sha256": sha256_file(root / PACKET_RELATIVE), "scope_sha256": APPROVED_SCOPE_SHA256},
        "b1r_approval_receipt": {"path": RECEIPT_RELATIVE, "sha256": sha256_file(root / RECEIPT_RELATIVE)},
        "parent_i3c_source_manifest": {"path": PARENT_MANIFEST_RELATIVE, "sha256": sha256_file(parent_manifest_path)},
        "worker_events": {"path": EVENT_RELATIVE, "sha256": sha256_file(root / EVENT_RELATIVE), "rows": len(events)},
        "worker_outputs": output_hashes,
        "timing": {
            "canonicalization_seconds": canonicalization_seconds,
            "i3c_serialization_seconds": fielded_serialization_seconds,
            "i3flat_serialization_seconds": flat_serialization_seconds,
        },
        "summary": summary,
        "artifacts": {
            name: {"path": relative(output_root / path.name, root), "sha256": sha256_file(path), "rows": len(canonical_rows)}
            for name, path in artifacts.items()
        },
        "manual_qa": {"required": True, "state": "pending", "review_rows": None},
        "retrieval_authorized": False,
    }
    write_json_new(staging_root / "manifest.json", merge_manifest)
    staging_root.replace(output_root)

    ledger = {
        "schema_version": "rq2b-v11-i3c-execution-ledger-v1",
        "version_id": VERSION_ID,
        "source_corpus_parent_version": PARENT_VERSION,
        "state": "complete_all_chunks_automatic_gates_passed_manual_qa_pending",
        "network_calls": 0,
        "external_api_calls": 0,
        "automatic_retries": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "unique_source_rows": 2433,
        "input_qwen_proxy_tokens": packet["scope"]["local_qwen_proxy_tokens"],
        "unique_source_utf8_bytes": packet["scope"]["source_utf8_bytes"],
        "execution_summary": execution_summary,
        "worker_events": {"path": EVENT_RELATIVE, "sha256": sha256_file(root / EVENT_RELATIVE), "rows": len(events)},
        "merge_manifest": {"path": relative(output_root / "manifest.json", root), "sha256": sha256_file(output_root / "manifest.json")},
        "b1r_authorisation_packet": {"path": PACKET_RELATIVE, "sha256": sha256_file(root / PACKET_RELATIVE), "scope_sha256": APPROVED_SCOPE_SHA256},
        "b1r_approval_receipt": {"path": RECEIPT_RELATIVE, "sha256": sha256_file(root / RECEIPT_RELATIVE)},
    }
    write_json_new(ledger_path, ledger)
    return verify(root)


def verify(root: Path) -> dict[str, Any]:
    packet, _ = verify_authorisation(root)
    events, execution_summary = validate_events(root, packet)
    output_root = root / MERGE_RELATIVE
    ledger_path = root / LEDGER_RELATIVE
    manifest_path = output_root / "manifest.json"
    require(manifest_path.is_file() and ledger_path.is_file(), "v1.1 merged I3C or ledger is missing")
    manifest = read_json(manifest_path)
    require(manifest.get("schema_version") == "rq2b-v11-i3c-merge-manifest-v1", "v1.1 merge schema mismatch")
    require(manifest.get("version_id") == VERSION_ID and manifest.get("source_corpus_parent_version") == PARENT_VERSION, "v1.1 merge identity mismatch")
    require(manifest.get("state") == "automatic_gates_passed_manual_qa_pending", "v1.1 merge state mismatch")
    require(manifest.get("network_calls") == manifest.get("external_api_calls") == 0, "v1.1 merge records external access")
    require(manifest.get("scientific_retrieval_or_reranking") is False and manifest.get("thesis_result_writing") is False, "v1.1 merge crossed boundary")
    require(manifest.get("manual_qa") == {"required": True, "state": "pending", "review_rows": None}, "v1.1 manual QA boundary mismatch")
    require(manifest.get("retrieval_authorized") is False, "v1.1 merge authorizes retrieval")
    summary = manifest["summary"]
    require(summary["rows"] == 2433, "v1.1 merged rows mismatch")
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "v1.1 automatic gate failure")
    artifacts = manifest.get("artifacts", {})
    require(set(artifacts) == {"canonical_extractions", "i3c-fielded-evidence", "i3-flat-evidence"}, "v1.1 merged artifacts mismatch")
    for artifact in artifacts.values():
        path = root / artifact["path"]
        require(path.is_file() and sha256_file(path) == artifact["sha256"], "v1.1 merged artifact hash drift")
        require(len(read_jsonl(path)) == artifact["rows"] == 2433, "v1.1 merged artifact row drift")
    canonical = read_jsonl(root / artifacts["canonical_extractions"]["path"])
    require([row["source_row_index"] for row in canonical] == list(range(2433)), "v1.1 canonical index drift")
    require(len({row["skill_id"] for row in canonical}) == 2433, "v1.1 canonical skill-ID drift")
    ledger = read_json(ledger_path)
    require(ledger.get("schema_version") == "rq2b-v11-i3c-execution-ledger-v1", "v1.1 ledger schema mismatch")
    require(ledger.get("state") == "complete_all_chunks_automatic_gates_passed_manual_qa_pending", "v1.1 ledger state mismatch")
    require(ledger.get("execution_summary") == execution_summary, "v1.1 ledger execution summary drift")
    require(ledger.get("worker_events") == {"path": EVENT_RELATIVE, "sha256": sha256_file(root / EVENT_RELATIVE), "rows": len(events)}, "v1.1 worker event binding drift")
    require(ledger.get("merge_manifest") == {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)}, "v1.1 merge binding drift")
    return {
        "state": "complete_all_chunks_automatic_gates_passed_manual_qa_pending",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "rows": 2433,
        "chunks": 57,
        "assignments": execution_summary["assignments"],
        "failed_attempts": execution_summary["failed_attempts"],
        "maximum_active_workers_observed": execution_summary["maximum_active_workers_observed"],
        "merge_manifest": relative(manifest_path, root),
        "execution_ledger": relative(ledger_path, root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    result = verify(root) if args.verify_only else merge(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
