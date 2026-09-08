#!/usr/bin/env python3
"""Mechanically reconcile completed V7 V2 sealed-coordinator returns.

This creates an opaque, target-blind collection ledger only.  It does not join
targets, finalise a prompt group, derive an acceptable set, or update a library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_2026_09_08_v2"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-sealed-coordinator-returns-2026-09-08-v2"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_sealed_coordinator_collection_reconciliation_2026_09_08_v1"
VERIFY = WORKSPACE / "skill_benchmark" / "scripts" / "verify_rq2b_nc_phase5_v7_sealed_coordinator_returns.py"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dispatch", type=Path, default=DISPATCH)
    parser.add_argument("--return-root", type=Path, default=RETURN_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    dispatch, return_root, output = args.dispatch.resolve(), args.return_root.resolve(), args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen reconciliation package: {output}")

    verified = subprocess.run(
        [sys.executable, str(VERIFY), "--dispatch", str(dispatch), "--return-root", str(return_root)],
        cwd=WORKSPACE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if verified.returncode:
        raise ValueError(f"coordinator return validation failed: {verified.stdout}\n{verified.stderr}")
    verification = json.loads(verified.stdout)
    if verification["status"] != "PASS_V7_SEALED_COORDINATOR_RETURNS_COMPLETE":
        raise ValueError(f"coordinator return collection is incomplete: {verification['status']}")

    admin = load_jsonl(dispatch / "sealed_admin_assignment_ledger.jsonl")
    if len(admin) != 2291 or len({row["coordinator_dispatch_id"] for row in admin}) != 2291:
        raise ValueError("admin dispatch ledger identity/cardinality drift")
    outcomes: list[dict[str, Any]] = []
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    decision_counts: Counter[str] = Counter()
    owner_decision_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in sorted(admin, key=lambda item: item["coordinator_dispatch_id"]):
        owner = row["owner_coordinator"]
        path = return_root / owner / f"{row['coordinator_dispatch_id']}.json"
        returned = json.loads(path.read_text(encoding="utf-8"))
        decision = returned["coordinator_decision"]
        decision_counts[decision] += 1
        owner_decision_counts[owner][decision] += 1
        state = "BLOCKED_REOPEN_PACKET" if decision == "REOPEN_PACKET" else "RESOLVED_CANDIDATE_PENDING_GROUP_RECONCILIATION"
        opaque = {
            "coordinator_dispatch_id": row["coordinator_dispatch_id"],
            "batch_id": row["batch_id"],
            "blind_packet_id": row["blind_packet_id"],
            "candidate_token": row["candidate_token"],
            "owner_coordinator": owner,
            "coordinator_decision": decision,
            "coordinator_return_sha256": sha_path(path),
            "candidate_collection_state": state,
        }
        outcomes.append(opaque)
        by_group[row["batch_id"]].append(opaque)
    if len(by_group) != 832:
        raise ValueError(f"expected 832 coordinator prompt groups, got {len(by_group)}")

    group_rows: list[dict[str, Any]] = []
    for batch_id, rows in sorted(by_group.items()):
        reopens = sum(row["coordinator_decision"] == "REOPEN_PACKET" for row in rows)
        group_rows.append({
            "batch_id": batch_id,
            "blind_packet_id": rows[0]["blind_packet_id"],
            "coordinator_candidate_packets": len(rows),
            "reopen_candidate_packets": reopens,
            "group_collection_state": "BLOCKED_REOPEN_PACKET" if reopens else "CANDIDATE_RESOLUTIONS_PENDING_GROUP_RECONCILIATION",
        })
    blocked_groups = sum(row["group_collection_state"] == "BLOCKED_REOPEN_PACKET" for row in group_rows)
    owner_counts = {owner: dict(sorted(counts.items())) for owner, counts in sorted(owner_decision_counts.items())}
    all_reopen_owners = [owner for owner, counts in owner_decision_counts.items() if counts and set(counts) == {"REOPEN_PACKET"}]
    summary = {
        "schema_version": "rq2b_nc_phase5_v7_sealed_coordinator_collection_reconciliation_v1",
        "status": "PASS_MECHANICAL_COLLECTION_BLOCKED_PENDING_METHOD_GATE" if blocked_groups else "PASS_MECHANICAL_COLLECTION_PENDING_GROUP_RECONCILIATION",
        "claim_boundary": "Target-blind mechanical collection only; no target join, group finalisation, acceptable-set decision, retrieval result, metric, or library update.",
        "bound_inputs": {
            "dispatch_path": str(dispatch.relative_to(WORKSPACE)),
            "dispatch_integrity_report_sha256": sha_path(dispatch / "integrity_report.json"),
            "coordinator_return_schema_sha256": sha_path(dispatch / "coordinator_return_schema.json"),
            "return_root": str(return_root.relative_to(WORKSPACE)),
            "return_validation": verification,
        },
        "counts": {
            "coordinator_candidate_packets": len(outcomes),
            "coordinator_prompt_groups": len(group_rows),
            "decision_counts": dict(sorted(decision_counts.items())),
            "prompt_groups_blocked_by_reopen": blocked_groups,
            "candidate_packets_reopened": decision_counts["REOPEN_PACKET"],
            "owner_decision_counts": owner_counts,
        },
        "method_gate": {
            "required": bool(blocked_groups),
            "reason": "REOPEN_PACKET prevents library-level closure under the frozen protocol. An owner-level all-REOPEN concentration is recorded as a calibration/decidability signal, not silently converted to a substantive adequacy result.",
            "all_reopen_owner_lanes": sorted(all_reopen_owners),
            "permitted_next_actions": ["prospective protocol amendment and new review", "explicit defer or exclude with limitation"],
            "prohibited_actions": ["target join", "acceptable-set creation", "library update", "silent decision substitution", "K change"],
        },
    }
    output.mkdir(parents=True)
    write_jsonl(output / "sealed_coordinator_candidate_collection_state.jsonl", outcomes)
    write_jsonl(output / "sealed_coordinator_group_collection_state.jsonl", group_rows)
    write_json(output / "integrity_report.json", summary)
    (output / "integrity_report.md").write_text(
        "# V7 sealed coordinator collection reconciliation\n\n"
        f"- Candidate-level coordinator returns validated: {len(outcomes)}\n"
        f"- Coordinator prompt groups: {len(group_rows)}\n"
        f"- Reopened candidate packets: {decision_counts['REOPEN_PACKET']}\n"
        f"- Prompt groups with at least one reopen: {blocked_groups}\n\n"
        "This is a target-blind mechanical collection ledger, not a finalisation or acceptable-set artifact. `REOPEN_PACKET` is a method gate under the frozen protocol.\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# V7 sealed coordinator collection reconciliation\n\n"
        "Reproduce with:\n\n"
        "```sh\n"
        "python3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_sealed_coordinator_returns.py\n"
        "python3 skill_benchmark/scripts/reconcile_rq2b_nc_phase5_v7_sealed_coordinator_collection.py\n"
        "```\n\n"
        "The second command refuses to overwrite this frozen package. It validates every return first, then writes only opaque collection states. It does not perform a target join, finalise a group, create acceptable sets, or update the library.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": summary["status"], "output": str(output), "counts": summary["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
