#!/usr/bin/env python3
"""Freeze a three-way sealed coordinator dispatch for Phase-8 quality reviews."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable

from reconcile_rq2b_v7_phase8_quality_reviews import (
    COORDINATOR_RETURN_SCHEMA,
    OUTPUT as RECONCILIATION,
    ROOT,
    build as build_reconciliation,
    verify as verify_reconciliation,
)


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_coordinator_dispatch_2026_09_09_v1"
)
ASSIGNMENT_SCHEMA = "rq2b-v7-phase8-quality-coordinator-assignment-v1"
FORBIDDEN_KEY_FRAGMENTS = (
    "target_skill", "gold_label", "gold_set", "acceptable_set",
    "retrieval_result", "rerank_result", "metric_value",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(
        (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        for value in values
    )


def rows(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def scan_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if any(fragment in lowered for fragment in FORBIDDEN_KEY_FRAGMENTS):
                findings.append(f"{path}.{key}")
            findings.extend(scan_forbidden_keys(nested, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            findings.extend(scan_forbidden_keys(nested, f"{path}[{index}]"))
    return findings


def build() -> dict[str, bytes]:
    verify_reconciliation()
    reconciliation_payloads = build_reconciliation()
    coordinator_data = reconciliation_payloads["sealed_coordinator_packets.jsonl"]
    packets = rows(coordinator_data)
    require(len(packets) == 109, "quality coordinator scope drift")
    require(len({row["packet_id"] for row in packets}) == len(packets), "duplicate coordinator packet ID")
    require(not scan_forbidden_keys(packets), "coordinator packet contains prohibited outcome/label key")
    ordered = sorted(packets, key=lambda row: (hashlib.sha256(row["packet_id"].encode()).hexdigest(), row["packet_id"]))
    sizes = (37, 36, 36)
    assigned: dict[int, list[dict[str, Any]]] = {1: [], 2: [], 3: []}
    cursor = 0
    for group, size in enumerate(sizes, 1):
        for packet in ordered[cursor: cursor + size]:
            assigned[group].append({
                "schema_version": ASSIGNMENT_SCHEMA,
                "coordinator_group": group,
                "coordinator_slot": 1,
                "source_reconciliation_sha256": sha(coordinator_data),
                "packet_id": packet["packet_id"],
                "packet_sha256": packet["packet_sha256"],
                "gate": packet["gate"],
                "allowed_decisions": packet["allowed_decisions"],
                "sealed_packet": packet,
                "required_return": {
                    "schema_version": COORDINATOR_RETURN_SCHEMA,
                    "packet_id": packet["packet_id"],
                    "packet_sha256": packet["packet_sha256"],
                    "gate": packet["gate"],
                    "decision": "PENDING",
                    "source_anchors": [],
                    "rationale": "",
                },
                "boundary": "Use only this assignment row. Do not inspect labels, acceptable sets, retrieval/reranking outputs, metrics, other coordinator returns, or files outside this sealed package.",
            })
        cursor += size
    require(cursor == len(ordered), "coordinator assignment cursor drift")
    unions = [set(row["packet_id"] for row in assigned[group]) for group in (1, 2, 3)]
    require(not (unions[0] & unions[1] or unions[0] & unions[2] or unions[1] & unions[2]), "coordinator assignments overlap")
    require(set.union(*unions) == {row["packet_id"] for row in packets}, "coordinator assignment coverage drift")
    payloads: dict[str, bytes] = {}
    for group in (1, 2, 3):
        payloads[f"coordinator_group_{group}_packet.jsonl"] = rows_bytes(assigned[group])
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "packet_id", "packet_sha256", "gate", "decision", "source_anchors", "rationale"],
        "properties": {
            "schema_version": {"const": COORDINATOR_RETURN_SCHEMA},
            "packet_id": {"type": "string", "pattern": r"^P8-(?:SPLIT-MIXED|PRREL|CUE|SRCREL)-[0-9]{3,}$"},
            "packet_sha256": {"type": "string", "pattern": r"^[0-9a-f]{64}$"},
            "gate": {"enum": ["split", "semantic_near_copy", "cue", "source_relation"]},
            "decision": {"type": "string", "minLength": 1},
            "source_anchors": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
            "rationale": {"type": "string", "minLength": 1},
        },
    }
    payloads["coordinator_return_schema.json"] = json_bytes(schema)
    group_hashes = {str(group): sha(payloads[f"coordinator_group_{group}_packet.jsonl"]) for group in (1, 2, 3)}
    report = {
        "schema_version": "rq2b-v7-phase8-quality-coordinator-dispatch-report-v1",
        "state": "PASS_SEALED_COORDINATOR_DISPATCH_PENDING_RETURNS",
        "formal_execution_ready": False,
        "counts": {"coordinator_packets": 109, "group_1": 37, "group_2": 36, "group_3": 36},
        "assertions": {
            "reconciliation_replayed": True,
            "deterministic_sha256_packet_id_order": True,
            "complete_coverage": True,
            "pairwise_disjoint": True,
            "target_gold_acceptable_set_retrieval_metric_keys_absent": True,
            "one_sealed_coordinator_decision_per_packet_required": True,
            "no_quality_pass_emitted": True,
        },
        "bindings": {
            "reconciliation_integrity_sha256": sha(reconciliation_payloads["integrity_report.json"]),
            "sealed_coordinator_packets_sha256": sha(coordinator_data),
            "coordinator_group_packet_sha256": group_hashes,
            "return_schema_sha256": sha(payloads["coordinator_return_schema.json"]),
            "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "boundary": "Coordinator decisions remain target-blind quality evidence. They neither repair adverse findings nor create a quality PASS or experiment authority.",
    }
    payloads["integrity_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 Phase-8 sealed quality coordinator dispatch\n\n"
        "The 109 disagreement/unclear packets from the immutable two-review reconciliation are split "
        "deterministically across three fresh coordinators (37/36/36). A coordinator may read only its "
        "assigned packet file, this README, and the return schema. It must choose one listed allowed decision, "
        "cite visible packet anchors, and give a specific rationale. Do not inspect benchmark labels, acceptable "
        "sets, retrieval/reranking outputs, metrics, or another coordinator's return.\n\n"
        "Write exactly one return row per assignment row, in order, to "
        "`returns/coordinator_group_N_return.jsonl`. No return creates a quality PASS; adverse findings still need "
        "a separate traceable disposition.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_coordinator_dispatch.py --verify`.\n"
    ).encode()
    return payloads


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "quality coordinator dispatch missing")
    expected = build()
    actual = {path.name for path in root.iterdir() if path.is_file()}
    require(actual == set(expected), "quality coordinator dispatch file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"quality coordinator dispatch artifact drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_PHASE8_QUALITY_COORDINATOR_DISPATCH_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite quality coordinator dispatch")
        payloads = build()
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale quality coordinator staging directory")
        staging.mkdir(parents=True)
        for name, data in payloads.items():
            (staging / name).write_bytes(data)
        (staging / "returns").mkdir()
        staging.rename(output)
        status = "PASS_V7_PHASE8_QUALITY_COORDINATOR_DISPATCH_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
