#!/usr/bin/env python3
"""Validate sealed coordinator returns and freeze the finding docket."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from build_rq2b_v7_phase8_quality_coordinator_dispatch import (
    COORDINATOR_RETURN_SCHEMA,
    OUTPUT as DISPATCH,
    ROOT,
    build as build_dispatch,
    verify as verify_dispatch,
)
from reconcile_rq2b_v7_phase8_quality_reviews import (
    OUTPUT as REVIEW_RECONCILIATION,
    assignment_rows as review_assignment_rows,
    build as build_review_reconciliation,
    verify as verify_review_reconciliation,
)


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_coordinator_reconciliation_2026_09_09_v1"
)
RETURN_KEYS = {
    "schema_version", "packet_id", "packet_sha256", "gate",
    "decision", "source_anchors", "rationale",
}
FINDING_DECISIONS = {
    "AVOIDABLE_IDENTITY_CUE",
    "SPLIT_LEAKAGE",
    "TRANSFORMED_DUPLICATE",
    "TRANSFORMED_COPY",
    "ALIAS_OR_FORK",
    "BLOCKED_OR_UNCLEAR",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(
        (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        for value in values
    )


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def validate_return(assignment: dict[str, Any], returned: dict[str, Any]) -> None:
    require(set(returned) == RETURN_KEYS, f"coordinator return key drift: {assignment['packet_id']}")
    require(returned["schema_version"] == COORDINATOR_RETURN_SCHEMA, f"coordinator schema drift: {assignment['packet_id']}")
    for field in ("packet_id", "packet_sha256", "gate"):
        require(returned[field] == assignment[field], f"coordinator binding drift: {assignment['packet_id']} {field}")
    require(returned["decision"] in assignment["allowed_decisions"], f"coordinator decision drift: {assignment['packet_id']}")
    require(
        isinstance(returned["source_anchors"], list)
        and bool(returned["source_anchors"])
        and all(isinstance(value, str) and value.strip() for value in returned["source_anchors"]),
        f"coordinator source anchors drift: {assignment['packet_id']}",
    )
    require(isinstance(returned["rationale"], str) and returned["rationale"].strip(), f"empty coordinator rationale: {assignment['packet_id']}")


def build() -> dict[str, bytes]:
    verify_dispatch()
    verify_review_reconciliation()
    dispatch_payloads = build_dispatch()
    review_payloads = build_review_reconciliation()
    coordinator_returns: dict[str, dict[str, Any]] = {}
    return_bindings = []
    for group in (1, 2, 3):
        assignments = rows(dispatch_payloads[f"coordinator_group_{group}_packet.jsonl"])
        path = ROOT / DISPATCH / "returns" / f"coordinator_group_{group}_return.jsonl"
        require(path.is_file(), f"missing coordinator return: group {group}")
        data = path.read_bytes()
        returned = rows(data)
        require(len(returned) == len(assignments), f"coordinator return count drift: group {group}")
        for assignment, result in zip(assignments, returned, strict=True):
            validate_return(assignment, result)
            require(result["packet_id"] not in coordinator_returns, f"duplicate coordinator return: {result['packet_id']}")
            coordinator_returns[result["packet_id"]] = result
        return_bindings.append({
            "coordinator_group": group,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha(data),
            "rows": len(returned),
        })
    require(len(coordinator_returns) == 109, "coordinator return coverage drift")

    final_rows: list[dict[str, Any]] = []
    for direct in rows(review_payloads["direct_reconciliation.jsonl"]):
        final_rows.append({
            "schema_version": "rq2b-v7-phase8-quality-final-packet-decision-v1",
            "packet_id": direct["packet_id"],
            "packet_sha256": direct["packet_sha256"],
            "gate": direct["gate"],
            "decision": direct["decision"],
            "decision_source": "EXACT_TWO_REVIEWER_NON_UNCLEAR_AGREEMENT",
            "evidence": direct,
        })
    coordinator_packets = {row["packet_id"]: row for row in rows(review_payloads["sealed_coordinator_packets.jsonl"])}
    require(set(coordinator_packets) == set(coordinator_returns), "coordinator packet/return union drift")
    for packet_id, returned in coordinator_returns.items():
        packet = coordinator_packets[packet_id]
        final_rows.append({
            "schema_version": "rq2b-v7-phase8-quality-final-packet-decision-v1",
            "packet_id": packet_id,
            "packet_sha256": packet["packet_sha256"],
            "gate": packet["gate"],
            "decision": returned["decision"],
            "decision_source": "SEALED_COORDINATOR",
            "evidence": {"coordinator_return": returned, "reviewer_returns": packet["reviewer_returns"]},
        })
    final_rows.sort(key=lambda row: row["packet_id"])
    require(len(final_rows) == 241 and len({row["packet_id"] for row in final_rows}) == 241, "final quality packet coverage drift")
    original_assignments, _ = review_assignment_rows()
    original_packet_by_id = {row["packet"]["packet_id"]: row["packet"] for row in original_assignments}
    require(len(original_packet_by_id) == 241, "original quality packet coverage drift")
    findings = []
    for row in final_rows:
        if row["decision"] in FINDING_DECISIONS:
            findings.append({
                "schema_version": "rq2b-v7-phase8-quality-finding-disposition-docket-v1",
                "packet_id": row["packet_id"],
                "packet_sha256": row["packet_sha256"],
                "gate": row["gate"],
                "decision": row["decision"],
                "required_disposition": (
                    "FRESH_REVIEW_OR_EXCLUDE"
                    if row["decision"] == "BLOCKED_OR_UNCLEAR"
                    else "BIND_EXISTING_DEPENDENCY_OR_EXCLUSION_OR_PROSPECTIVE_REMEDIATION"
                ),
                "sealed_packet": original_packet_by_id[row["packet_id"]],
                "decision_evidence": row["evidence"],
                "status": "PENDING",
            })
    final_data = rows_bytes(final_rows)
    finding_data = rows_bytes(findings)
    report = {
        "schema_version": "rq2b-v7-phase8-quality-coordinator-reconciliation-report-v1",
        "state": "BLOCKED_PENDING_FINDING_DISPOSITION_AND_QUALITY_CLOSURE" if findings else "BLOCKED_PENDING_QUALITY_CLOSURE",
        "formal_execution_ready": False,
        "counts": {
            "final_packet_decisions": len(final_rows),
            "direct_decisions": 132,
            "coordinator_decisions": 109,
            "finding_docket": len(findings),
            "decisions": dict(sorted(Counter(row["decision"] for row in final_rows).items())),
            "findings_by_gate": dict(sorted(Counter(row["gate"] for row in findings).items())),
        },
        "assertions": {
            "coordinator_dispatch_replayed": True,
            "one_valid_coordinator_return_per_assigned_packet": True,
            "direct_and_coordinator_union_is_241": True,
            "all_adverse_or_unclear_decisions_enter_docket": True,
            "no_quality_pass_emitted": True,
        },
        "bindings": {
            "review_reconciliation_integrity_sha256": sha(review_payloads["integrity_report.json"]),
            "coordinator_dispatch_integrity_sha256": sha(dispatch_payloads["integrity_report.json"]),
            "coordinator_returns": return_bindings,
            "final_quality_decisions_sha256": sha(final_data),
            "finding_disposition_docket_sha256": sha(finding_data),
            "reconciler_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "boundary": "This package preserves adverse findings and creates no quality PASS, input promotion, selector run, target join, or metric.",
    }
    return {
        "final_quality_decisions.jsonl": final_data,
        "finding_disposition_docket.jsonl": finding_data,
        "integrity_report.json": json_bytes(report),
        "README.md": (
            "# V7 Phase-8 quality coordinator reconciliation\n\n"
            "This package validates one sealed coordinator return for each of the 109 disagreement/unclear packets, "
            "combines them with 132 direct two-reviewer agreements, and routes every adverse or still-unclear "
            "decision into a separate finding-disposition docket. It does not create a quality PASS or experiment "
            "authority.\n"
        ).encode(),
    }


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "quality coordinator reconciliation missing")
    expected = build()
    require({path.name for path in root.iterdir() if path.is_file()} == set(expected), "quality coordinator reconciliation file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"quality coordinator reconciliation artifact drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_PHASE8_QUALITY_COORDINATOR_RECONCILIATION_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite quality coordinator reconciliation")
        payloads = build()
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale quality coordinator reconciliation staging directory")
        staging.mkdir(parents=True)
        for name, data in payloads.items():
            (staging / name).write_bytes(data)
        staging.rename(output)
        status = "PASS_V7_PHASE8_QUALITY_COORDINATOR_RECONCILIATION_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
