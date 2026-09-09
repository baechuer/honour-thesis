#!/usr/bin/env python3
"""Validate two independent quality returns and freeze direct/coordinator queues."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from build_rq2b_v7_phase8_quality_review_dispatch import (
    OUTPUT as DISPATCH,
    RETURN_SCHEMA,
    ROOT,
    build as build_dispatch,
    verify as verify_dispatch,
)
from validate_rq2b_v7_phase8_quality_return_schema_v2 import (
    V2_PACKAGE as QUALITY_SCHEMA_AMENDMENT,
    V2_SCHEMA_PATH as QUALITY_RETURN_SCHEMA_V2,
    validate_files as validate_return_files_v2,
)


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_review_reconciliation_2026_09_09_v1"
)
RETURN_KEYS = {
    "schema_version", "packet_id", "packet_sha256", "reviewer_group",
    "reviewer_slot", "gate", "decision", "source_anchors", "rationale",
}
COORDINATOR_RETURN_SCHEMA = "rq2b-v7-phase8-quality-coordinator-return-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def rows_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(value) for value in values)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        require(bool(raw), f"blank JSONL row: {path}:{line_number}")
        value = json.loads(raw)
        require(isinstance(value, dict), f"non-object JSONL row: {path}:{line_number}")
        values.append(value)
    return values


def assignment_rows() -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    payloads = build_dispatch()
    rows: list[dict[str, Any]] = []
    for name, data in payloads.items():
        if name.endswith("_packet.jsonl"):
            rows.extend(read_jsonl_bytes(data))
    return rows, payloads


def read_jsonl_bytes(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def validate_return(assignment: dict[str, Any], returned: dict[str, Any]) -> None:
    require(set(returned) == RETURN_KEYS, f"quality return key drift: {assignment['packet']['packet_id']}")
    require(returned["schema_version"] == RETURN_SCHEMA, "quality return schema drift")
    expected = {
        "packet_id": assignment["packet"]["packet_id"],
        "packet_sha256": assignment["packet_sha256"],
        "reviewer_group": assignment["reviewer_group"],
        "reviewer_slot": assignment["reviewer_slot"],
        "gate": assignment["gate"],
    }
    for key, value in expected.items():
        require(returned[key] == value, f"quality return binding drift: {expected['packet_id']} {key}")
    require(returned["decision"] in assignment["allowed_decisions"], f"quality return decision drift: {expected['packet_id']}")
    require(isinstance(returned["rationale"], str) and returned["rationale"].strip(), f"empty quality rationale: {expected['packet_id']}")
    require(isinstance(returned["source_anchors"], list) and all(isinstance(value, str) and value.strip() for value in returned["source_anchors"]), f"quality source anchors drift: {expected['packet_id']}")


def build() -> dict[str, bytes]:
    verify_dispatch()
    assignments, dispatch_payloads = assignment_rows()
    require(len(assignments) == 482, "quality assignment coverage drift")
    dispatch_root = ROOT / DISPATCH
    expected_by_slot: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for assignment in assignments:
        expected_by_slot[(assignment["reviewer_group"], assignment["reviewer_slot"])].append(assignment)

    returns_by_packet: dict[str, list[dict[str, Any]]] = defaultdict(list)
    return_bindings = []
    for (group, slot), expected in sorted(expected_by_slot.items()):
        path = dispatch_root / "returns" / f"reviewer_group_{group}_slot_{slot:03d}_return.jsonl"
        require(path.is_file(), f"missing quality return: {group}:{slot:03d}")
        packet_path = dispatch_root / f"reviewer_group_{group}_slot_{slot:03d}_packet.jsonl"
        schema_receipt = validate_return_files_v2(packet_path, path)
        require(schema_receipt["status"] == "SCHEMA_ENVELOPE_VALID", f"quality schema-v2 replay failed: {group}:{slot:03d}")
        data = path.read_bytes()
        returned = read_jsonl_bytes(data)
        require(len(returned) == len(expected), f"quality return count drift: {group}:{slot:03d}")
        expected_by_id = {row["packet"]["packet_id"]: row for row in expected}
        require(len(expected_by_id) == len(expected), f"duplicate assignment packet: {group}:{slot:03d}")
        require({row.get("packet_id") for row in returned} == set(expected_by_id), f"quality return coverage drift: {group}:{slot:03d}")
        for row in returned:
            assignment = expected_by_id[row["packet_id"]]
            validate_return(assignment, row)
            returns_by_packet[row["packet_id"]].append(row)
        return_bindings.append({
            "reviewer_group": group,
            "reviewer_slot": slot,
            "path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(data).hexdigest(),
            "rows": len(returned),
            "schema_v2_status": schema_receipt["status"],
        })

    require(len(returns_by_packet) == 241, "quality returned packet coverage drift")
    require(all(len(rows) == 2 and len({row["reviewer_group"] for row in rows}) == 2 for rows in returns_by_packet.values()), "quality independent-review cardinality drift")
    assignment_by_packet = {}
    for assignment in assignments:
        assignment_by_packet.setdefault(assignment["packet"]["packet_id"], assignment)

    direct = []
    coordinator = []
    decision_counts: Counter[str] = Counter()
    gate_counts: Counter[str] = Counter()
    for packet_id in sorted(assignment_by_packet):
        assignment = assignment_by_packet[packet_id]
        reviews = sorted(returns_by_packet[packet_id], key=lambda row: row["reviewer_group"])
        decisions = {row["decision"] for row in reviews}
        if len(decisions) == 1 and "BLOCKED_OR_UNCLEAR" not in decisions:
            decision = next(iter(decisions))
            decision_counts[decision] += 1
            gate_counts[assignment["gate"]] += 1
            direct.append({
                "schema_version": "rq2b-v7-phase8-quality-direct-reconciliation-v1",
                "packet_id": packet_id,
                "packet_sha256": assignment["packet_sha256"],
                "gate": assignment["gate"],
                "decision": decision,
                "reviewer_groups": [row["reviewer_group"] for row in reviews],
                "reviews": reviews,
            })
        else:
            coordinator.append({
                "schema_version": "rq2b-v7-phase8-quality-sealed-coordinator-packet-v1",
                "packet_id": packet_id,
                "packet_sha256": assignment["packet_sha256"],
                "gate": assignment["gate"],
                "allowed_decisions": assignment["allowed_decisions"],
                "packet": assignment["packet"],
                "reviewer_returns": reviews,
                "required_return": {
                    "schema_version": COORDINATOR_RETURN_SCHEMA,
                    "packet_id": packet_id,
                    "packet_sha256": assignment["packet_sha256"],
                    "gate": assignment["gate"],
                    "decision": "PENDING",
                    "source_anchors": [],
                    "rationale": "",
                },
                "review_boundary": "Sealed target-blind coordination. Use only this packet; do not access labels, acceptable sets, retrieval outputs, results, or metrics.",
            })

    direct_data = rows_bytes(direct)
    coordinator_data = rows_bytes(coordinator)
    report = {
        "schema_version": "rq2b-v7-phase8-quality-review-reconciliation-report-v1",
        "state": "BLOCKED_PENDING_SEALED_COORDINATOR_AND_FINDING_DISPOSITION" if coordinator else "BLOCKED_PENDING_FINDING_DISPOSITION_AND_QUALITY_CLOSURE",
        "formal_execution_ready": False,
        "counts": {
            "unique_packets": 241,
            "review_returns": 482,
            "direct_reconciliations": len(direct),
            "coordinator_packets": len(coordinator),
            "direct_by_gate": dict(sorted(gate_counts.items())),
            "direct_decisions": dict(sorted(decision_counts.items())),
        },
        "assertions": {
            "two_distinct_target_blind_returns_per_packet": True,
            "packet_hashes_replayed": True,
            "all_decisions_within_packet_contract": True,
            "only_exact_non_unclear_agreements_direct": True,
            "prospective_schema_envelope_amendment_replayed": True,
            "all_returns_have_nonempty_source_anchors": True,
            "no_quality_pass_emitted": True,
        },
        "bindings": {
            "dispatch_integrity_sha256": hashlib.sha256(dispatch_payloads["integrity_report.json"]).hexdigest(),
            "quality_return_schema_v2_sha256": file_sha256(QUALITY_RETURN_SCHEMA_V2),
            "quality_return_schema_amendment_receipt_sha256": file_sha256(QUALITY_SCHEMA_AMENDMENT / "amendment_receipt.json"),
            "review_returns": return_bindings,
            "direct_reconciliation_sha256": hashlib.sha256(direct_data).hexdigest(),
            "coordinator_packets_sha256": hashlib.sha256(coordinator_data).hexdigest(),
            "reconciler_sha256": file_sha256(Path(__file__)),
        },
        "boundary": "This reconciliation creates no quality PASS and no experiment authority. Coordinator and any adverse finding disposition remain required.",
    }
    return {
        "direct_reconciliation.jsonl": direct_data,
        "sealed_coordinator_packets.jsonl": coordinator_data,
        "integrity_report.json": json_bytes(report),
        "README.md": (
            "# V7 Phase-8 quality review reconciliation v1\n\n"
            "This package validates two independent target-blind returns per quality packet. Exact non-unclear agreements enter the direct ledger; disagreements and unclear decisions enter the sealed coordinator queue. No quality PASS or experiment authority is created here.\n"
        ).encode(),
    }


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "quality reconciliation missing")
    expected = build()
    require({path.name for path in root.iterdir() if path.is_file()} == set(expected), "quality reconciliation file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"quality reconciliation artifact drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_PHASE8_QUALITY_RECONCILIATION_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite quality reconciliation")
        expected = build()
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale reconciliation staging directory")
        staging.mkdir(parents=True)
        for name, data in expected.items():
            (staging / name).write_bytes(data)
        staging.rename(output)
        status = "PASS_V7_PHASE8_QUALITY_RECONCILIATION_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
