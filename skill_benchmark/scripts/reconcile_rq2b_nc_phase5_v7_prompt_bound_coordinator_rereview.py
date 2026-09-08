#!/usr/bin/env python3
"""Create target-blind group reconciliation from prompt-bound coordinator re-review.

This is a mechanical, opaque consolidation of valid A/B exact agreements and
valid prompt-bound coordinator decisions. It never opens a target join or
creates an acceptable set, retrieval result, metric, or library update.
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
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-2026-09-08-v1"
INVALID_ARCHIVE = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-invalid-attempt-2026-09-08-v1" / "coordinator_3"
VERIFY = WORKSPACE / "skill_benchmark" / "scripts" / "verify_rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview.py"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_reconciliation_2026_09_08_v1"


DECISION_TO_ADEQUACY = {
    "CONFIRMED_FULLY_ACCEPTABLE": "FULLY_ACCEPTABLE",
    "CONFIRMED_PARTIALLY_ADEQUATE": "PARTIALLY_ADEQUATE",
    "CONFIRMED_INADEQUATE": "INADEQUATE",
    "CONFIRMED_UNCLEAR": "UNCLEAR",
    "REOPEN_PACKET": "REOPEN_PACKET",
}


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def git_blobs(revision: str, paths: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(paths))
    process = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=WORKSPACE,
        input=("\n".join(f"{revision}:{path}" for path in unique) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        raise ValueError(process.stderr.decode("utf-8"))
    result: dict[str, bytes] = {}
    cursor = 0
    for path in unique:
        end = process.stdout.index(b"\n", cursor)
        header = process.stdout[cursor:end].decode("utf-8").split()
        cursor = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"missing/unexpected source blob: {revision}:{path}")
        size = int(header[2])
        result[path] = process.stdout[cursor:cursor + size]
        cursor += size
        if process.stdout[cursor:cursor + 1] != b"\n":
            raise ValueError(f"truncated source blob: {revision}:{path}")
        cursor += 1
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dispatch", type=Path, default=DISPATCH)
    parser.add_argument("--return-root", type=Path, default=RETURN_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    dispatch, return_root, output = args.dispatch.resolve(), args.return_root.resolve(), args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen reconciliation package: {output}")

    verification_run = subprocess.run(
        [sys.executable, str(VERIFY), "--dispatch", str(dispatch), "--return-root", str(return_root)],
        cwd=WORKSPACE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if verification_run.returncode:
        raise ValueError(f"prompt-bound return validation failed: {verification_run.stdout}\n{verification_run.stderr}")
    verification = json.loads(verification_run.stdout)
    if verification["status"] != "PASS_V7_PROMPT_BOUND_COORDINATOR_REREVIEW_RETURNS_COMPLETE":
        raise ValueError(f"incomplete prompt-bound returns: {verification['status']}")

    admin_rows = load_jsonl(dispatch / "sealed_admin_assignment_ledger.jsonl")
    if len(admin_rows) != 2291 or len({row["coordinator_dispatch_id"] for row in admin_rows}) != 2291:
        raise ValueError("prompt-bound admin ledger identity/cardinality drift")
    coordinator_by_group_token: dict[tuple[str, str], dict[str, Any]] = {}
    candidate_collection_rows: list[dict[str, Any]] = []
    coordinator_decision_counts: Counter[str] = Counter()
    for row in admin_rows:
        path = return_root / row["owner_coordinator"] / f"{row['coordinator_dispatch_id']}.json"
        returned = json.loads(path.read_text(encoding="utf-8"))
        decision = returned["coordinator_decision"]
        if decision not in DECISION_TO_ADEQUACY:
            raise ValueError(f"unsupported coordinator decision: {decision}")
        key = (row["batch_id"], row["candidate_token"])
        if key in coordinator_by_group_token:
            raise ValueError("coordinator candidate identity overlap")
        opaque = {
            "batch_id": row["batch_id"],
            "blind_packet_id": row["blind_packet_id"],
            "candidate_token": row["candidate_token"],
            "coordinator_dispatch_id": row["coordinator_dispatch_id"],
            "owner_coordinator": row["owner_coordinator"],
            "coordinator_decision": decision,
            "resolved_adequacy": DECISION_TO_ADEQUACY[decision],
            "coordinator_return_sha256": sha_path(path),
            "candidate_collection_state": "BLOCKED" if decision in {"CONFIRMED_UNCLEAR", "REOPEN_PACKET"} else "RESOLVED",
        }
        coordinator_by_group_token[key] = opaque
        candidate_collection_rows.append(opaque)
        coordinator_decision_counts[decision] += 1

    ledger = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    selected = [row for row in ledger if row["group_route"] == "SEALED_COORDINATOR_ELIGIBLE"]
    by_group: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        if not row["active_return_selected"]:
            raise ValueError(f"inactive original return in re-review scope: {row['batch_id']}")
        by_group[row["batch_id"]][row["reviewer_lane"]] = row
    if len(by_group) != 832 or any(set(lanes) != {"A", "B"} for lanes in by_group.values()):
        raise ValueError("re-review group scope drift")
    blobs_by_commit: dict[str, dict[str, bytes]] = {}
    for commit in sorted({row["source_commit"] for row in selected}):
        blobs_by_commit[commit] = git_blobs(commit, [row["source_return_path"] for row in selected if row["source_commit"] == commit])

    group_rows: list[dict[str, Any]] = []
    final_adequacy_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    for batch_id in sorted(by_group):
        pair = by_group[batch_id]
        original_returns: dict[str, dict[str, Any]] = {}
        for lane, row in pair.items():
            raw = blobs_by_commit[row["source_commit"]][row["source_return_path"]]
            if sha_bytes(raw) != row["source_return_sha256"]:
                raise ValueError(f"original source return hash drift: {batch_id}/{lane}")
            original_returns[lane] = json.loads(raw)
        assessment_a = {item["candidate_token"]: item["adequacy"] for item in original_returns["A"]["assessments"]}
        assessment_b = {item["candidate_token"]: item["adequacy"] for item in original_returns["B"]["assessments"]}
        if set(assessment_a) != set(assessment_b) or len(assessment_a) != 8:
            raise ValueError(f"original assessment partition drift: {batch_id}")
        dispositions: list[dict[str, Any]] = []
        blocked = False
        for token in sorted(assessment_a):
            a, b = assessment_a[token], assessment_b[token]
            if a == b and a != "UNCLEAR":
                final, route = a, "EXACT_INDEPENDENT_AGREEMENT"
                evidence = {}
            else:
                coordinator = coordinator_by_group_token.get((batch_id, token))
                if coordinator is None:
                    raise ValueError(f"missing prompt-bound coordinator return: {batch_id}/{token}")
                final, route = coordinator["resolved_adequacy"], "PROMPT_BOUND_COORDINATOR_REREVIEW"
                evidence = {
                    "coordinator_dispatch_id": coordinator["coordinator_dispatch_id"],
                    "coordinator_return_sha256": coordinator["coordinator_return_sha256"],
                }
            if final in {"UNCLEAR", "REOPEN_PACKET"}:
                blocked = True
            dispositions.append({"candidate_token": token, "final_adequacy": final, "decision_route": route, **evidence})
            final_adequacy_counts[final] += 1
            route_counts[route] += 1
        group_rows.append({
            "batch_id": batch_id,
            "blind_packet_id": pair["A"]["blind_packet_id"],
            "candidate_dispositions": dispositions,
            "group_reconciliation_state": "BLOCKED_BY_UNCLEAR_OR_REOPEN" if blocked else "TARGET_BLIND_GROUP_RECONCILED_PENDING_GATE_DOCKET",
        })
    if len(group_rows) != 832 or sum(len(row["candidate_dispositions"]) for row in group_rows) != 6656:
        raise ValueError("group reconciliation cardinality drift")
    blocked_groups = sum(row["group_reconciliation_state"] != "TARGET_BLIND_GROUP_RECONCILED_PENDING_GATE_DOCKET" for row in group_rows)
    invalid_archive_count = len(list(INVALID_ARCHIVE.glob("*.json"))) if INVALID_ARCHIVE.is_dir() else 0
    output.mkdir(parents=True)
    candidate_collection_rows.sort(key=lambda row: row["coordinator_dispatch_id"])
    write_jsonl(output / "prompt_bound_coordinator_candidate_collection.jsonl", candidate_collection_rows)
    write_jsonl(output / "target_blind_group_reconciliation.jsonl", group_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_reconciliation_v1",
        "status": "PASS_TARGET_BLIND_GROUP_RECONCILIATION_PENDING_GATE_DOCKET" if not blocked_groups else "PASS_TARGET_BLIND_GROUP_RECONCILIATION_WITH_BLOCKERS",
        "claim_boundary": "Target-blind mechanical reconciliation only; no target join, acceptable-set decision, library update, retrieval result, metric, or thesis result update.",
        "bound_inputs": {
            "prompt_bound_dispatch": str(dispatch.relative_to(WORKSPACE)),
            "prompt_bound_dispatch_integrity_sha256": sha_path(dispatch / "integrity_report.json"),
            "prompt_bound_return_schema_sha256": sha_path(dispatch / "coordinator_return_schema.json"),
            "prompt_bound_return_validation": verification,
            "original_integration_ledger": str(INTEGRATION.relative_to(WORKSPACE) / "integration_intake_ledger.jsonl"),
            "original_integration_ledger_sha256": sha_path(INTEGRATION / "integration_intake_ledger.jsonl"),
        },
        "counts": {
            "rereview_prompt_groups": 832,
            "total_candidate_dispositions": 6656,
            "coordinator_candidate_dispositions": len(candidate_collection_rows),
            "coordinator_decision_counts": dict(sorted(coordinator_decision_counts.items())),
            "final_adequacy_counts": dict(sorted(final_adequacy_counts.items())),
            "decision_route_counts": dict(sorted(route_counts.items())),
            "blocked_prompt_groups": blocked_groups,
        },
        "historical_invalid_attempt": {
            "path": str(INVALID_ARCHIVE.relative_to(WORKSPACE)),
            "raw_return_count": invalid_archive_count,
            "status": "PRESERVED_UNSELECTED_SCHEMA_INVALID",
            "selection_rule": "No return in this archive is read or selected by this reconciliation.",
        },
        "remaining_gate_boundary": {
            "historical_gate_docket_groups_not_in_rereview_scope": 6,
            "required_before_target_join_or_library_closure": ["explicit disposition of every historical gate-docket record", "master-SOP readiness review"],
            "prohibited_now": ["target join", "acceptable-set creation", "library update", "retrieval or metrics", "K change"],
        },
    }
    write_json(output / "integrity_report.json", report)
    (output / "integrity_report.md").write_text(
        "# Prompt-bound coordinator re-review reconciliation\n\n"
        f"- Reconciled target-blind prompt groups: {len(group_rows)}\n"
        f"- Candidate dispositions: 6,656\n"
        f"- Prompt-bound coordinator dispositions: {len(candidate_collection_rows)}\n"
        f"- Groups blocked by a new unclear/reopen: {blocked_groups}\n\n"
        "This package combines only validated, target-blind evidence. It is not an acceptable set or a final library. The six historical gate-docket groups remain outside the re-review scope and must be explicitly disposed before any target join.\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# RQ2b-NC target-blind prompt-bound reconciliation\n\n"
        "Reproduce with:\n\n"
        "```sh\n"
        "python3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview.py\n"
        "python3 skill_benchmark/scripts/reconcile_rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview.py\n"
        "```\n\n"
        "The reconciliation refuses to run unless all 2,291 prompt-bound returns validate. It then combines only exact A/B agreements and valid prompt-bound coordinator decisions using opaque packet IDs. It does not open a target join or derive acceptable-set/library outcomes.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(output), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
