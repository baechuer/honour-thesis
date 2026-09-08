#!/usr/bin/env python3
"""Freeze user-approved V7 gate dispositions and five target-blind reissues."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
V7_MANIFEST = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery" / "unified_prompt_group_batch_manifest.jsonl"
V7_RETURN_SCHEMA = V7_MANIFEST.parent / "unified_independent_reviewer_return_schema.json"
V7_HANDOFF = WORKSPACE / "skill_benchmark" / "scripts" / "materialize_rq2b_nc_phase5_v7_parallel_handoff_2026_09_06.py"
GATE_READINESS = NC / "manifests" / "rq2b_nc_phase5_v7_gate_docket_readiness_2026_09_08_v1"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_gate_disposition_reissue_2026_09_08_v1"

REISSUE_LANES = {
    "RQ2B-P4-V7-U0527": ["B"],
    "RQ2B-P4-V7-U0979": ["B"],
    "RQ2B-P4-V7-U1068": ["B"],
    "RQ2B-P4-V7-U1078": ["B"],
    "RQ2B-P4-V7-U1157": ["A", "B"],
}


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_v7_handoff() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_v7_gate_reissue_handoff", V7_HANDOFF)
    if spec is None or spec.loader is None:
        raise ValueError("unable to load frozen V7 handoff helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite frozen V7 gate-reissue package: {OUTPUT}")
    readiness = json.loads((GATE_READINESS / "integrity_report.json").read_text(encoding="utf-8"))
    if readiness["status"] != "PASS_TARGET_BLIND_GATE_DOCKET_EVIDENCE_CONSOLIDATED_PENDING_USER_METHOD_DECISION":
        raise ValueError("gate-readiness status drift")
    gate_rows = {row["batch_id"]: row for row in load_jsonl(GATE_READINESS / "target_blind_gate_docket_reconciliation.jsonl")}
    if set(gate_rows) != {"RQ2B-P4-V7-U0323", *REISSUE_LANES}:
        raise ValueError("gate-readiness scope drift")

    handoff = load_v7_handoff()
    protocol, manifests, _, _ = handoff.verified_inputs()
    _, main_by_id, tail_by_id = protocol.verify_audit()
    instruction, _, return_schema, _ = protocol.reviewer_instruction_and_schema()
    if canonical_sha(return_schema) != canonical_sha(json.loads(V7_RETURN_SCHEMA.read_text(encoding="utf-8"))):
        raise ValueError("V7 return-schema drift")
    manifests_by_id = {row["batch_id"]: row for row in manifests}

    admin_rows = [{
        "batch_id": "RQ2B-P4-V7-U0323",
        "blind_packet_id": gate_rows["RQ2B-P4-V7-U0323"]["blind_packet_id"],
        "disposition": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE",
        "disposition_authority": "USER_APPROVED_2026-09-08",
        "reason": "SUBSTANTIVE_CONSTRUCT_METHOD_GATE; same-packet A+B reissue is not a mechanical repair.",
        "target_join_permitted": False,
    }]
    reviewer_rows: dict[str, list[dict[str, Any]]] = {"A": [], "B": []}
    for batch_id in sorted(REISSUE_LANES):
        manifest = manifests_by_id.get(batch_id)
        if manifest is None:
            raise ValueError(f"missing V7 manifest: {batch_id}")
        packet = handoff.packet_for_manifest(protocol, manifest, main_by_id, tail_by_id, instruction)
        packet_sha = canonical_sha(packet)
        if len(packet["candidates"]) != 8 or set(packet) != protocol.PACKET_FIELDS:
            raise ValueError(f"V7 packet cardinality/schema drift: {batch_id}")
        admin_rows.append({
            "batch_id": batch_id,
            "blind_packet_id": manifest["blind_packet_id"],
            "disposition": "USER_APPROVED_TRACEABLE_TARGET_BLIND_REISSUE_PENDING_RETURN",
            "disposition_authority": "USER_APPROVED_2026-09-08",
            "historical_gate_reason": gate_rows[batch_id]["historical_gate_reason"],
            "reissue_lanes": REISSUE_LANES[batch_id],
            "source_manifest_sha256": sha_path(V7_MANIFEST),
            "packet_input_sha256": packet_sha,
            "sealed_main_packet_sha256": manifest["sealed_main_packet"]["packet_sha256"],
            "sealed_tail_packet_sha256s": [row["packet_sha256"] for row in manifest["sealed_tail_packets"]],
            "target_join_permitted": False,
        })
        for lane in REISSUE_LANES[batch_id]:
            reviewer_rows[lane].append({
                "schema_version": "rq2b_nc_phase5_v7_gate_reissue_reviewer_input_v1",
                "reissue_dispatch_id": f"V7-GR-{lane}-{batch_id.rsplit('-', 1)[-1]}",
                "reviewer_blind_id": lane,
                "batch_id": batch_id,
                "blind_packet_id": manifest["blind_packet_id"],
                "packet_input_sha256": packet_sha,
                "protocol_instruction_sha256": manifest["reviewer_instruction_sha256"],
                "sealed_target_blind_packet": packet,
                "blindness_notice": "Read only this packet and the copied frozen return schema. It has no target identity, gold label, retrieval result, prior return, reconciliation decision, or main/tail role.",
            })
    if len(reviewer_rows["A"]) != 1 or len(reviewer_rows["B"]) != 5:
        raise ValueError("approved reissue lane allocation drift")
    if len({row["batch_id"] for row in reviewer_rows["A"]} | {row["batch_id"] for row in reviewer_rows["B"]}) != 5:
        raise ValueError("approved reissue group scope drift")

    OUTPUT.mkdir(parents=True)
    write_jsonl(OUTPUT / "sealed_admin_disposition_and_reissue_ledger.jsonl", admin_rows)
    write_jsonl(OUTPUT / "reviewer_A_reissue_manifest.jsonl", reviewer_rows["A"])
    write_jsonl(OUTPUT / "reviewer_B_reissue_manifest.jsonl", reviewer_rows["B"])
    write_json(OUTPUT / "reviewer_return_schema.json", return_schema)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_gate_disposition_reissue_v1",
        "status": "PASS_USER_APPROVED_V7_GATE_DISPOSITION_AND_REISSUE_DISPATCH_READY",
        "claim_boundary": "Dispatch preparation only; no return, target join, acceptable set, library update, retrieval result, metric, thesis result, or K change is produced.",
        "user_approved_disposition": {
            "U0323": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE",
            "remaining_five_gate_groups": "TRACEABLE_TARGET_BLIND_REISSUE",
        },
        "counts": {
            "deferred_excluded_groups": 1,
            "reissue_prompt_groups": 5,
            "reviewer_A_reissue_groups": len(reviewer_rows["A"]),
            "reviewer_B_reissue_groups": len(reviewer_rows["B"]),
            "total_reissue_returns_required": len(reviewer_rows["A"]) + len(reviewer_rows["B"]),
            "candidate_assessments_required": 8 * (len(reviewer_rows["A"]) + len(reviewer_rows["B"])),
        },
        "bound_inputs": {
            "v7_unified_manifest": str(V7_MANIFEST.relative_to(WORKSPACE)),
            "v7_unified_manifest_sha256": sha_path(V7_MANIFEST),
            "v7_return_schema": str(V7_RETURN_SCHEMA.relative_to(WORKSPACE)),
            "v7_return_schema_sha256": sha_path(V7_RETURN_SCHEMA),
            "v7_handoff_helper": str(V7_HANDOFF.relative_to(WORKSPACE)),
            "v7_handoff_helper_sha256": sha_path(V7_HANDOFF),
            "gate_readiness_integrity": str((GATE_READINESS / "integrity_report.json").relative_to(WORKSPACE)),
            "gate_readiness_integrity_sha256": sha_path(GATE_READINESS / "integrity_report.json"),
        },
        "validations": {
            "u0323_not_reissued": all(row.get("batch_id") != "RQ2B-P4-V7-U0323" for rows in reviewer_rows.values() for row in rows),
            "all_reissue_packets_have_eight_candidates": all(len(row["sealed_target_blind_packet"]["candidates"]) == 8 for rows in reviewer_rows.values() for row in rows),
            "all_reissue_groups_have_two_v7_tail_hashes": all(len(row["sealed_tail_packet_sha256s"]) == 2 for row in admin_rows if "sealed_tail_packet_sha256s" in row),
            "only_user_approved_gate_groups_issued": {row["batch_id"] for rows in reviewer_rows.values() for row in rows} == set(REISSUE_LANES),
        },
        "stop_boundary": "Returns must validate, then be mechanically reconciled with the retained valid counterpart(s). No target join or acceptable-set/library update is allowed before all selected reissue groups are finalised or explicitly excluded and a new master-SOP readiness verification passes.",
    }
    if not all(report["validations"].values()):
        raise ValueError("reissue-dispatch integrity failure")
    write_json(OUTPUT / "integrity_report.json", report)
    (OUTPUT / "integrity_report.md").write_text(
        "# User-approved V7 gate disposition and reissue readiness\n\n"
        "- `U0323`: deferred/excluded from the V7 frozen-library closure.\n"
        "- Reissue groups: 5, each retaining its complete eight-candidate V7 packet (six main plus two tails).\n"
        "- Fresh reviewer returns required: 1 A-lane and 5 B-lane.\n\n"
        "The lane manifests are reviewer-facing and target-blind. The administrative ledger is not reviewer input. No reviewer may inspect it, any retained raw return, target identity, retrieval outcome, main/tail role, or peer lane.\n",
        encoding="utf-8",
    )
    (OUTPUT / "README.md").write_text(
        "# V7 gate disposition and traceable reissue\n\n"
        "This frozen package records the user-approved V7 disposition: `U0323` is deferred/excluded from V7 closure; the other five gate groups are reissued against unchanged complete V7 packets. It does not alter K=6, tails, candidates, prompts, targets, or source material.\n\n"
        "A reviewer may read only their own manifest and `reviewer_return_schema.json`. Each row has exactly eight source-visible candidates and must yield one strict-schema return under the configured return directory. The administrative ledger must remain sealed from reviewers.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
