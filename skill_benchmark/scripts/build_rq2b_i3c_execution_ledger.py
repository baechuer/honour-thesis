#!/usr/bin/env python3
"""Build the audited RQ2b I3C worker-execution ledger after extraction."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from build_rq2b_i3c_transfer_packet import verify as verify_i3c_packet
from rq2b_common import (
    B1R_MAXIMUM_ACTIVE_WORKERS,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_b1s_implementation_seal,
    verify_b1r_execution_authorised,
    version_root,
    write_json_new,
)


EVENT_KEYS = {
    "schema_version",
    "version_id",
    "chunk_index",
    "attempt_index",
    "worker_id",
    "status",
    "started_at_epoch_seconds",
    "completed_at_epoch_seconds",
    "network_calls",
    "external_api_calls",
    "automatic_retry",
    "input_path",
    "input_sha256",
    "output_path",
    "output_sha256",
    "output_rows",
    "failure_reason",
}


def validate_events(
    packet: dict[str, Any],
    events: list[dict[str, Any]],
    *,
    root: Path | None = None,
    maximum_active_workers: int = 6,
) -> dict[str, Any]:
    require(
        isinstance(maximum_active_workers, int)
        and not isinstance(maximum_active_workers, bool)
        and maximum_active_workers >= 1,
        "Invalid I3C active-worker ceiling",
    )
    chunks = {int(row["chunk_index"]): row for row in packet["chunks"]}
    require(len(chunks) == packet["counts"]["chunks"], "I3C packet chunk IDs are not unique")
    grouped: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        require(set(event) == EVENT_KEYS, "I3C worker-event key mismatch")
        require(event["schema_version"] == "rq2b-i3c-worker-event-v1", "I3C worker-event schema mismatch")
        require(event["version_id"] == VERSION_ID, "I3C worker-event version mismatch")
        chunk_index = event["chunk_index"]
        require(isinstance(chunk_index, int) and chunk_index in chunks, "Unknown I3C worker-event chunk")
        require(isinstance(event["attempt_index"], int) and event["attempt_index"] >= 1, "Invalid I3C attempt index")
        require(isinstance(event["worker_id"], str) and bool(event["worker_id"]), "Invalid I3C worker ID")
        require(event["status"] in {"completed", "failed"}, "Invalid I3C worker-event status")
        require(event["network_calls"] == event["external_api_calls"] == 0, "I3C worker event used prohibited external access")
        require(event["automatic_retry"] is False, "I3C worker event records an automatic retry")
        started = float(event["started_at_epoch_seconds"])
        completed = float(event["completed_at_epoch_seconds"])
        require(math.isfinite(started) and math.isfinite(completed) and completed >= started, "Invalid I3C worker timing")
        chunk = chunks[chunk_index]
        require(event["input_path"] == chunk["input_path"], "I3C worker-event input path mismatch")
        require(event["input_sha256"] == chunk["input_sha256"], "I3C worker-event input hash mismatch")
        if event["status"] == "completed":
            require(event["failure_reason"] is None, "Completed I3C worker event has a failure reason")
            require(event["output_path"] == chunk["expected_output_path"], "I3C worker-event output path mismatch")
            require(isinstance(event["output_sha256"], str) and bool(event["output_sha256"]), "Completed I3C event lacks output hash")
            require(event["output_rows"] == chunk["row_count"], "Completed I3C event row-count mismatch")
            if root is not None:
                output_path = root / event["output_path"]
                require(output_path.is_file(), f"I3C worker output missing: {output_path}")
                require(sha256_file(output_path) == event["output_sha256"], "I3C worker-event output hash drift")
                require(len(read_jsonl(output_path)) == event["output_rows"], "I3C worker-event output parse/row mismatch")
        else:
            require(isinstance(event["failure_reason"], str) and bool(event["failure_reason"]), "Failed I3C event lacks a failure reason")
            require(event["output_path"] is None, "Failed I3C event must not claim a canonical output")
            require(event["output_sha256"] is None, "Failed I3C event must not claim an output hash")
            require(event["output_rows"] == 0, "Failed I3C event must record zero accepted rows")
        grouped.setdefault(chunk_index, []).append(event)

    require(set(grouped) == set(chunks), "I3C worker-event chunk coverage mismatch")
    worker_ids = [row["worker_id"] for row in events]
    require(
        len(worker_ids) == len(set(worker_ids)),
        "Each explicit I3C assignment must use a newly spawned worker ID",
    )
    completed_events: list[dict[str, Any]] = []
    for chunk_index, chunk_events in grouped.items():
        ordered = sorted(chunk_events, key=lambda row: row["attempt_index"])
        require(
            [row["attempt_index"] for row in ordered] == list(range(1, len(ordered) + 1)),
            f"I3C attempt indices are not contiguous: {chunk_index}",
        )
        require(all(row["status"] == "failed" for row in ordered[:-1]), f"I3C chunk has work after completion: {chunk_index}")
        require(ordered[-1]["status"] == "completed", f"I3C chunk lacks a final completed attempt: {chunk_index}")
        for previous, current in zip(ordered, ordered[1:], strict=False):
            require(
                float(current["started_at_epoch_seconds"])
                >= float(previous["completed_at_epoch_seconds"]),
                f"I3C replacement began before the previous worker closed: {chunk_index}",
            )
        completed_events.append(ordered[-1])

    active: list[dict[str, Any]] = []
    maximum_observed_workers = 0
    for event in sorted(
        events,
        key=lambda row: (
            float(row["started_at_epoch_seconds"]),
            float(row["completed_at_epoch_seconds"]),
            int(row["chunk_index"]),
            int(row["attempt_index"]),
        ),
    ):
        started = float(event["started_at_epoch_seconds"])
        active = [
            row
            for row in active
            if float(row["completed_at_epoch_seconds"]) > started
        ]
        require(
            all(row["chunk_index"] != event["chunk_index"] for row in active),
            f"Duplicate active I3C chunk assignment: {event['chunk_index']}",
        )
        require(
            all(row["worker_id"] != event["worker_id"] for row in active),
            f"I3C worker has overlapping active assignments: {event['worker_id']}",
        )
        active.append(event)
        maximum_observed_workers = max(maximum_observed_workers, len(active))
        require(
            maximum_observed_workers <= maximum_active_workers,
            "I3C active-worker ceiling exceeded",
        )

    timings = [
        float(row["completed_at_epoch_seconds"]) - float(row["started_at_epoch_seconds"])
        for row in events
    ]
    return {
        "assignments": len(events),
        "completed_chunks": len(completed_events),
        "failed_attempts": sum(row["status"] == "failed" for row in events),
        "unique_workers": len({row["worker_id"] for row in events}),
        "maximum_active_workers_allowed": maximum_active_workers,
        "maximum_active_workers_observed": maximum_observed_workers,
        "new_worker_per_assignment_enforced": True,
        "replacement_nonoverlap_enforced": True,
        "worker_seconds_sum": sum(timings),
        "orchestrator_wall_seconds": max(float(row["completed_at_epoch_seconds"]) for row in events)
        - min(float(row["started_at_epoch_seconds"]) for row in events),
        "assigned_source_rows": sum(chunks[row["chunk_index"]]["row_count"] for row in events),
        "assigned_source_utf8_bytes": sum(chunks[row["chunk_index"]]["utf8_bytes"] for row in events),
        "assigned_qwen_proxy_tokens": sum(chunks[row["chunk_index"]]["qwen_proxy_tokens"] for row in events),
    }


def build(root: Path, event_path: Path) -> dict[str, Any]:
    verify_b1s_implementation_seal(root)
    b1r = verify_b1r_execution_authorised(root)
    packet = verify_i3c_packet(root)
    frozen_root = version_root(root)
    merge_manifest_path = frozen_root / "i3c_merged" / "manifest.json"
    require(merge_manifest_path.is_file(), "I3C merge manifest is missing")
    merge_manifest = read_json(merge_manifest_path)
    require(merge_manifest.get("state") == "automatic_gates_passed_manual_qa_pending", "I3C automatic gates have not passed")
    require(
        merge_manifest.get("packet_manifest_sha256") == sha256_file(frozen_root / "i3c_extraction" / "manifest.json"),
        "I3C merge does not bind the current packet",
    )
    expected_event_path = root / b1r["worker_event_ledger"]["path"]
    require(
        event_path.resolve() == expected_event_path.resolve(),
        "I3C worker-event input is not the B1R-authorised canonical ledger path",
    )
    events = read_jsonl(event_path)
    summary = validate_events(
        packet,
        events,
        root=root,
        maximum_active_workers=B1R_MAXIMUM_ACTIVE_WORKERS,
    )
    require(summary["assignments"] <= b1r["scope"]["maximum_total_assignment_attempts"], "I3C assignment ceiling exceeded")
    require(summary["failed_attempts"] <= b1r["scope"]["maximum_replacement_assignments"], "I3C replacement ceiling exceeded")
    require(summary["assigned_source_rows"] <= b1r["scope"]["maximum_assigned_source_rows"], "I3C assigned-row ceiling exceeded")
    require(summary["assigned_source_utf8_bytes"] <= b1r["scope"]["maximum_assigned_source_utf8_bytes"], "I3C assigned-byte ceiling exceeded")
    require(summary["assigned_qwen_proxy_tokens"] <= b1r["scope"]["maximum_assigned_qwen_proxy_tokens"], "I3C assigned-token ceiling exceeded")
    completed_hashes = {
        row["output_path"]: row["output_sha256"]
        for row in events
        if row["status"] == "completed"
    }
    require(
        completed_hashes
        == {row["path"]: row["sha256"] for row in merge_manifest["worker_outputs"]},
        "I3C worker events do not match the automatic-gate merge inputs",
    )
    output_path = frozen_root / "i3c_extraction_execution_ledger.json"
    require(not output_path.exists(), f"Refusing to overwrite I3C execution ledger: {output_path}")
    report = {
        "schema_version": "rq2b-i3c-execution-ledger-v1",
        "version_id": VERSION_ID,
        "state": "complete_all_chunks_automatic_gates_passed",
        "network_calls": 0,
        "external_api_calls": 0,
        "automatic_retries": 0,
        "input_qwen_proxy_tokens": packet["counts"]["total_qwen_proxy_tokens"],
        "unique_source_rows": packet["counts"]["input_rows"],
        "unique_source_utf8_bytes": packet["counts"]["total_source_utf8_bytes"],
        "execution_summary": summary,
        "worker_events": {
            "path": relative(event_path, root),
            "sha256": sha256_file(event_path),
            "rows": len(events),
        },
        "packet_manifest": {
            "path": relative(frozen_root / "i3c_extraction" / "manifest.json", root),
            "sha256": sha256_file(frozen_root / "i3c_extraction" / "manifest.json"),
        },
        "merge_manifest": {
            "path": relative(merge_manifest_path, root),
            "sha256": sha256_file(merge_manifest_path),
        },
        "b1r_authorisation_packet": {
            "path": relative(frozen_root / "b1r_authorisation_packet.json", root),
            "sha256": sha256_file(frozen_root / "b1r_authorisation_packet.json"),
            "scope_sha256": b1r["scope_sha256"],
        },
        "b1r_approval_receipt": {
            "path": relative(frozen_root / "b1r_approval_receipt.json", root),
            "sha256": sha256_file(frozen_root / "b1r_approval_receipt.json"),
        },
    }
    write_json_new(output_path, report)
    return verify(root)


def verify(root: Path) -> dict[str, Any]:
    """Recompute the complete extraction audit before I3C can enter retrieval."""
    frozen_root = version_root(root)
    ledger_path = frozen_root / "i3c_extraction_execution_ledger.json"
    require(ledger_path.is_file(), f"I3C execution ledger is missing: {ledger_path}")
    verify_b1s_implementation_seal(root)
    b1r = verify_b1r_execution_authorised(root)
    packet = verify_i3c_packet(root)
    merge_manifest_path = frozen_root / "i3c_merged" / "manifest.json"
    packet_manifest_path = frozen_root / "i3c_extraction" / "manifest.json"
    b1r_packet_path = frozen_root / "b1r_authorisation_packet.json"
    b1r_receipt_path = frozen_root / "b1r_approval_receipt.json"
    event_path = root / b1r["worker_event_ledger"]["path"]

    for label, path in (
        ("execution ledger", ledger_path),
        ("worker events", event_path),
        ("merge manifest", merge_manifest_path),
        ("packet manifest", packet_manifest_path),
        ("B1R authorisation packet", b1r_packet_path),
        ("B1R approval receipt", b1r_receipt_path),
    ):
        require(path.is_file(), f"I3C {label} is missing: {path}")

    report = read_json(ledger_path)
    require(
        set(report)
        == {
            "schema_version",
            "version_id",
            "state",
            "network_calls",
            "external_api_calls",
            "automatic_retries",
            "input_qwen_proxy_tokens",
            "unique_source_rows",
            "unique_source_utf8_bytes",
            "execution_summary",
            "worker_events",
            "packet_manifest",
            "merge_manifest",
            "b1r_authorisation_packet",
            "b1r_approval_receipt",
        },
        "I3C execution-ledger key mismatch",
    )
    require(report["schema_version"] == "rq2b-i3c-execution-ledger-v1", "I3C execution-ledger schema mismatch")
    require(report["version_id"] == VERSION_ID, "I3C execution-ledger version mismatch")
    require(report["state"] == "complete_all_chunks_automatic_gates_passed", "I3C execution ledger is incomplete")
    require(report["network_calls"] == report["external_api_calls"] == 0, "I3C execution ledger records external access")
    require(report["automatic_retries"] == 0, "I3C execution ledger records automatic retries")

    merge_manifest = read_json(merge_manifest_path)
    require(
        merge_manifest.get("state") == "automatic_gates_passed_manual_qa_pending",
        "I3C automatic gates have not passed",
    )
    require(
        merge_manifest.get("packet_manifest_sha256") == sha256_file(packet_manifest_path),
        "I3C merge does not bind the current packet",
    )
    events = read_jsonl(event_path)
    summary = validate_events(
        packet,
        events,
        root=root,
        maximum_active_workers=B1R_MAXIMUM_ACTIVE_WORKERS,
    )
    require(summary == report["execution_summary"], "I3C execution-ledger summary is not reproducible")
    require(summary["assignments"] <= b1r["scope"]["maximum_total_assignment_attempts"], "I3C assignment ceiling exceeded")
    require(summary["failed_attempts"] <= b1r["scope"]["maximum_replacement_assignments"], "I3C replacement ceiling exceeded")
    require(summary["assigned_source_rows"] <= b1r["scope"]["maximum_assigned_source_rows"], "I3C assigned-row ceiling exceeded")
    require(summary["assigned_source_utf8_bytes"] <= b1r["scope"]["maximum_assigned_source_utf8_bytes"], "I3C assigned-byte ceiling exceeded")
    require(summary["assigned_qwen_proxy_tokens"] <= b1r["scope"]["maximum_assigned_qwen_proxy_tokens"], "I3C assigned-token ceiling exceeded")
    require(summary["maximum_active_workers_allowed"] == B1R_MAXIMUM_ACTIVE_WORKERS, "I3C active-worker ceiling drift")
    require(report["input_qwen_proxy_tokens"] == packet["counts"]["total_qwen_proxy_tokens"], "I3C input-token total drift")
    require(report["unique_source_rows"] == packet["counts"]["input_rows"], "I3C unique-row total drift")
    require(report["unique_source_utf8_bytes"] == packet["counts"]["total_source_utf8_bytes"], "I3C unique-byte total drift")

    require(
        report["worker_events"]
        == {
            "path": relative(event_path, root),
            "sha256": sha256_file(event_path),
            "rows": len(events),
        },
        "I3C execution ledger does not bind the current worker events",
    )
    require(
        report["packet_manifest"]
        == {
            "path": relative(packet_manifest_path, root),
            "sha256": sha256_file(packet_manifest_path),
        },
        "I3C execution ledger does not bind the current extraction packet",
    )
    require(
        report["merge_manifest"]
        == {
            "path": relative(merge_manifest_path, root),
            "sha256": sha256_file(merge_manifest_path),
        },
        "I3C execution ledger does not bind the current merge manifest",
    )
    require(
        report["b1r_authorisation_packet"]
        == {
            "path": relative(b1r_packet_path, root),
            "sha256": sha256_file(b1r_packet_path),
            "scope_sha256": b1r["scope_sha256"],
        },
        "I3C execution ledger does not bind the current B1R packet",
    )
    require(
        report["b1r_approval_receipt"]
        == {
            "path": relative(b1r_receipt_path, root),
            "sha256": sha256_file(b1r_receipt_path),
        },
        "I3C execution ledger does not bind the current B1R approval receipt",
    )
    completed_hashes = {
        row["output_path"]: row["output_sha256"]
        for row in events
        if row["status"] == "completed"
    }
    require(
        completed_hashes
        == {row["path"]: row["sha256"] for row in merge_manifest["worker_outputs"]},
        "I3C worker events do not match the automatic-gate merge inputs",
    )
    return report


def self_test() -> dict[str, Any]:
    packet = {
        "counts": {"chunks": 1},
        "chunks": [
            {
                "chunk_index": 0,
                "input_path": "input.jsonl",
                "input_sha256": "a" * 64,
                "expected_output_path": "output.jsonl",
                "row_count": 2,
                "utf8_bytes": 100,
                "qwen_proxy_tokens": 25,
            }
        ],
    }
    base = {
        "schema_version": "rq2b-i3c-worker-event-v1",
        "version_id": VERSION_ID,
        "chunk_index": 0,
        "worker_id": "worker-1",
        "network_calls": 0,
        "external_api_calls": 0,
        "automatic_retry": False,
        "input_path": "input.jsonl",
        "input_sha256": "a" * 64,
    }
    failed = {
        **base,
        "attempt_index": 1,
        "status": "failed",
        "started_at_epoch_seconds": 1.0,
        "completed_at_epoch_seconds": 2.0,
        "output_path": None,
        "output_sha256": None,
        "output_rows": 0,
        "failure_reason": "synthetic failure",
    }
    completed = {
        **base,
        "worker_id": "worker-2",
        "attempt_index": 2,
        "status": "completed",
        "started_at_epoch_seconds": 2.0,
        "completed_at_epoch_seconds": 5.0,
        "output_path": "output.jsonl",
        "output_sha256": "b" * 64,
        "output_rows": 2,
        "failure_reason": None,
    }
    summary = validate_events(packet, [failed, completed])
    require(summary["failed_attempts"] == 1 and summary["completed_chunks"] == 1, "I3C execution-ledger retry self-test failed")
    require(summary["assigned_source_rows"] == 4, "I3C execution-ledger repeated-transfer accounting failed")

    overlapping_replacement = json.loads(json.dumps([failed, completed]))
    overlapping_replacement[1]["started_at_epoch_seconds"] = 1.5
    overlap_rejected = False
    try:
        validate_events(packet, overlapping_replacement)
    except ValueError:
        overlap_rejected = True
    require(overlap_rejected, "I3C overlapping-replacement self-test failed")

    reused_worker = json.loads(json.dumps([failed, completed]))
    reused_worker[1]["worker_id"] = reused_worker[0]["worker_id"]
    reused_worker_rejected = False
    try:
        validate_events(packet, reused_worker)
    except ValueError:
        reused_worker_rejected = True
    require(reused_worker_rejected, "I3C reused-worker self-test failed")

    concurrent_packet = {
        "counts": {"chunks": 7},
        "chunks": [
            {
                "chunk_index": index,
                "input_path": f"input-{index}.jsonl",
                "input_sha256": f"{index + 1:064x}",
                "expected_output_path": f"output-{index}.jsonl",
                "row_count": 1,
                "utf8_bytes": 10,
                "qwen_proxy_tokens": 3,
            }
            for index in range(7)
        ],
    }
    concurrent_events = [
        {
            **base,
            "chunk_index": index,
            "attempt_index": 1,
            "worker_id": f"worker-{index}",
            "status": "completed",
            "started_at_epoch_seconds": 1.0,
            "completed_at_epoch_seconds": 3.0,
            "input_path": f"input-{index}.jsonl",
            "input_sha256": f"{index + 1:064x}",
            "output_path": f"output-{index}.jsonl",
            "output_sha256": f"{index + 101:064x}",
            "output_rows": 1,
            "failure_reason": None,
        }
        for index in range(7)
    ]
    concurrency_rejected = False
    try:
        validate_events(concurrent_packet, concurrent_events, maximum_active_workers=6)
    except ValueError:
        concurrency_rejected = True
    require(concurrency_rejected, "I3C worker-concurrency self-test failed")
    return {
        "state": "synthetic_execution_ledger_only",
        "failed_attempts": summary["failed_attempts"],
        "completed_chunks": summary["completed_chunks"],
        "repeated_transfer_accounted": True,
        "overlapping_replacement_rejected": overlap_rejected,
        "reused_worker_rejected": reused_worker_rejected,
        "seven_concurrent_workers_rejected": concurrency_rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--worker-events", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.worker_events is not None, "--worker-events is required")
        root = args.root.resolve()
        event_path = args.worker_events if args.worker_events.is_absolute() else root / args.worker_events
        result = build(root, event_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
