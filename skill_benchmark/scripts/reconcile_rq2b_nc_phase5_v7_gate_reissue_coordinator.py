#!/usr/bin/env python3
"""Apply validated sealed coordinator decisions to V7 gate-reissue pair records."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
PAIR = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_pair_reconciliation_2026_09_08_v1"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_sealed_coordinator_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-gate-reissue-sealed-coordinator-2026-09-08-v1" / "gate_reissue_coordinator"
VERIFY = WORKSPACE / "skill_benchmark" / "scripts" / "verify_rq2b_nc_phase5_v7_gate_reissue_coordinator.py"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_final_reconciliation_2026_09_08_v1"

DECISION_TO_ADEQUACY = {
    "CONFIRMED_FULLY_ACCEPTABLE": "FULLY_ACCEPTABLE",
    "CONFIRMED_PARTIALLY_ADEQUATE": "PARTIALLY_ADEQUATE",
    "CONFIRMED_INADEQUATE": "INADEQUATE",
    "CONFIRMED_UNCLEAR": "UNCLEAR",
    "REOPEN_PACKET": "REOPEN_PACKET",
}


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite frozen final gate-reissue reconciliation: {OUTPUT}")
    run = subprocess.run(
        [sys.executable, str(VERIFY), "--dispatch", str(DISPATCH), "--return-root", str(RETURN_ROOT)],
        cwd=WORKSPACE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if run.returncode:
        raise ValueError(f"coordinator validation failed: {run.stdout}\n{run.stderr}")
    validation = json.loads(run.stdout)
    if validation["status"] != "PASS_V7_GATE_REISSUE_COORDINATOR_RETURNS_COMPLETE":
        raise ValueError(f"coordinator returns incomplete: {validation['status']}")
    admin = load_jsonl(DISPATCH / "sealed_admin_assignment_ledger.jsonl")
    queue_by_key = {(row["batch_id"], row["candidate_token"]): row for row in admin}
    if len(queue_by_key) != 9:
        raise ValueError("coordinator admin ledger identity drift")
    coordinator = {
        row["coordinator_dispatch_id"]: json.loads((RETURN_ROOT / f"{row['coordinator_dispatch_id']}.json").read_text())
        for row in admin
    }
    if len(coordinator) != 9:
        raise ValueError("coordinator return identity drift")
    pairs = load_jsonl(PAIR / "target_blind_gate_reissue_pair_reconciliation.jsonl")
    if len(pairs) != 5 or len({row["batch_id"] for row in pairs}) != 5:
        raise ValueError("gate pair scope drift")
    group_rows: list[dict[str, Any]] = []
    final_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    blocked_groups = 0
    for group in sorted(pairs, key=lambda row: row["batch_id"]):
        final_dispositions: list[dict[str, Any]] = []
        blocked = False
        for disposition in group["candidate_dispositions"]:
            token = disposition["candidate_token"]
            if disposition["decision_route"] == "EXACT_RETAINED_FRESH_INDEPENDENT_AGREEMENT":
                final = disposition["final_adequacy"]
                route = disposition["decision_route"]
                evidence: dict[str, Any] = {}
            elif disposition["decision_route"] == "PENDING_SEALED_COORDINATOR":
                assignment = queue_by_key.get((group["batch_id"], token))
                if assignment is None:
                    raise ValueError(f"missing coordinator assignment: {group['batch_id']}/{token}")
                returned = coordinator[assignment["coordinator_dispatch_id"]]
                decision = returned["coordinator_decision"]
                if decision not in DECISION_TO_ADEQUACY:
                    raise ValueError(f"unsupported coordinator decision: {decision}")
                final = DECISION_TO_ADEQUACY[decision]
                route = "FRESH_PROMPT_BOUND_SEALED_COORDINATOR"
                evidence = {
                    "coordinator_dispatch_id": assignment["coordinator_dispatch_id"],
                    "coordinator_return_sha256": sha_path(RETURN_ROOT / f"{assignment['coordinator_dispatch_id']}.json"),
                }
            else:
                raise ValueError(f"unknown pair disposition route: {disposition['decision_route']}")
            if final in {"UNCLEAR", "REOPEN_PACKET"}:
                blocked = True
            final_dispositions.append({"candidate_token": token, "final_adequacy": final, "decision_route": route, **evidence})
            final_counts[final] += 1
            route_counts[route] += 1
        if blocked:
            blocked_groups += 1
        group_rows.append({
            "batch_id": group["batch_id"],
            "blind_packet_id": group["blind_packet_id"],
            "selected_return_lineage": group["selected_return_lineage"],
            "candidate_dispositions": final_dispositions,
            "group_reconciliation_state": "BLOCKED_BY_UNCLEAR_OR_REOPEN" if blocked else "TARGET_BLIND_GATE_REISSUE_RECONCILED_PENDING_GLOBAL_MASTER_SOP_READINESS",
        })
    if sum(len(row["candidate_dispositions"]) for row in group_rows) != 40:
        raise ValueError("final gate-reissue candidate cardinality drift")
    OUTPUT.mkdir(parents=True)
    write_jsonl(OUTPUT / "target_blind_gate_reissue_final_reconciliation.jsonl", group_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_gate_reissue_final_reconciliation_v1",
        "status": "PASS_TARGET_BLIND_GATE_REISSUE_RECONCILIATION_PENDING_GLOBAL_MASTER_SOP_READINESS" if not blocked_groups else "PASS_TARGET_BLIND_GATE_REISSUE_RECONCILIATION_WITH_BLOCKERS",
        "claim_boundary": "Target-blind mechanical reconciliation only; no target join, acceptable set, library update, retrieval result, metric, thesis result, or K change.",
        "counts": {
            "reconciled_gate_reissue_groups": len(group_rows),
            "candidate_dispositions": 40,
            "final_adequacy_counts": dict(sorted(final_counts.items())),
            "decision_route_counts": dict(sorted(route_counts.items())),
            "blocked_groups": blocked_groups,
        },
        "bound_inputs": {
            "pair_reconciliation_integrity": str((PAIR / "integrity_report.json").relative_to(WORKSPACE)),
            "pair_reconciliation_integrity_sha256": sha_path(PAIR / "integrity_report.json"),
            "coordinator_dispatch_integrity": str((DISPATCH / "integrity_report.json").relative_to(WORKSPACE)),
            "coordinator_dispatch_integrity_sha256": sha_path(DISPATCH / "integrity_report.json"),
            "coordinator_return_validation": validation,
        },
        "u0323_disposition": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE_BY_USER_APPROVAL_2026-09-08",
        "stop_boundary": "This resolves only the five approved reissue groups. Combine it with the 228 direct and 832 earlier prompt-bound reconciliations, plus the U0323 exclusion, in a global master-SOP readiness replay before target join or acceptable-set/library update.",
    }
    write_json(OUTPUT / "integrity_report.json", report)
    (OUTPUT / "integrity_report.md").write_text(
        "# V7 gate-reissue final reconciliation\n\n"
        f"- Reconciled reissue groups: {len(group_rows)}\n"
        f"- Candidate dispositions: 40\n"
        f"- Groups blocked by coordinator unclear/reopen: {blocked_groups}\n\n"
        "This package is target-blind evidence only. `U0323` is explicitly deferred/excluded from V7 closure. A global master-SOP readiness replay remains mandatory before any target join or acceptable-set/library update.\n",
        encoding="utf-8",
    )
    (OUTPUT / "README.md").write_text(
        "# V7 gate-reissue final reconciliation\n\n"
        "Reproduce with:\n\n```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_gate_reissue_coordinator.py\npython3 skill_benchmark/scripts/reconcile_rq2b_nc_phase5_v7_gate_reissue_coordinator.py\n```\n\n"
        "Exact pair agreements and validated coordinator decisions are combined without a target join. No library conclusion is created here.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
