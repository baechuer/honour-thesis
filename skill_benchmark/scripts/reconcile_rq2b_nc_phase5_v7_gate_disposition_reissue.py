#!/usr/bin/env python3
"""Mechanically pair V7 gate reissues with their retained valid counterpart lanes."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_gate_disposition_reissue_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-gate-disposition-reissue-2026-09-08-v1"
VERIFY = WORKSPACE / "skill_benchmark" / "scripts" / "verify_rq2b_nc_phase5_v7_gate_disposition_reissue.py"
VERIFY_MODULE = VERIFY
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
U0527_A_PATH = "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase5-v7-machine-b-microbatch-008-reissue-001-2026-09-07-v1/returns/reviewer_A/RQ2B-P4-V7-U0527.json"
U0527_A_COMMIT = "8024e1c9728d83dbe10a820662e9d24b64c7caa4"
U0527_A_SHA256 = "2fae5f7a8f5472e115a2a39171683ca13393819b41e56cba9db345dfafaebb5a"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_pair_reconciliation_2026_09_08_v1"


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


def git_blob(commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"], cwd=WORKSPACE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise ValueError(f"missing source blob {commit}:{relative_path}: {result.stderr.decode('utf-8')}")
    return result.stdout


def load_verifier() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_v7_gate_reissue_verifier", VERIFY_MODULE)
    if spec is None or spec.loader is None:
        raise ValueError("unable to load gate-reissue verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite frozen pair-reconciliation package: {OUTPUT}")
    verification_run = subprocess.run(
        [sys.executable, str(VERIFY), "--dispatch", str(DISPATCH), "--return-root", str(RETURN_ROOT)],
        cwd=WORKSPACE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if verification_run.returncode:
        raise ValueError(f"fresh reissue return validation failed: {verification_run.stdout}\n{verification_run.stderr}")
    verification = json.loads(verification_run.stdout)
    if verification["status"] != "PASS_V7_GATE_REISSUE_RETURNS_COMPLETE":
        raise ValueError(f"fresh reissue returns incomplete: {verification['status']}")
    verifier = load_verifier()
    expected, allowed_top, assessment_fields, adequacy_values = verifier.load_expected(DISPATCH)

    integration_rows = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    retained_by_batch: dict[str, dict[str, Any]] = {}
    for row in integration_rows:
        if row["batch_id"] in {"RQ2B-P4-V7-U0979", "RQ2B-P4-V7-U1068", "RQ2B-P4-V7-U1078"} and row["reviewer_lane"] == "A":
            retained_by_batch[row["batch_id"]] = row
    if set(retained_by_batch) != {"RQ2B-P4-V7-U0979", "RQ2B-P4-V7-U1068", "RQ2B-P4-V7-U1078"}:
        raise ValueError("retained machine-A lane scope drift")

    pairs: dict[str, tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = {}
    # U0527 uses the already-valid R001 A reissue; U1157 uses both fresh lanes.
    u0527_a_bytes = git_blob(U0527_A_COMMIT, U0527_A_PATH)
    if sha_bytes(u0527_a_bytes) != U0527_A_SHA256:
        raise ValueError("U0527 retained reissue-A hash drift")
    u0527_a = json.loads(u0527_a_bytes)
    u0527_row = expected[("B", "RQ2B-P4-V7-U0527")]
    problem = verifier.validate_return(u0527_a, "A", u0527_row, allowed_top, assessment_fields, adequacy_values)
    if problem:
        raise ValueError(f"U0527 retained A validation drift: {problem}")
    u0527_b_path = RETURN_ROOT / "reviewer_B" / "RQ2B-P4-V7-U0527.json"
    pairs["RQ2B-P4-V7-U0527"] = (u0527_a, json.loads(u0527_b_path.read_text()), {
        "A": {"return_path": U0527_A_PATH, "source_commit": U0527_A_COMMIT, "return_sha256": U0527_A_SHA256, "selection": "VALIDATED_REISSUE_001_A_RETAINED"},
        "B": {"return_path": str(u0527_b_path.relative_to(WORKSPACE)), "source_commit": None, "return_sha256": sha_path(u0527_b_path), "selection": "FRESH_USER_APPROVED_GATE_REISSUE"},
    })
    for batch_id, ledger in retained_by_batch.items():
        raw = git_blob(ledger["source_commit"], ledger["source_return_path"])
        if sha_bytes(raw) != ledger["source_return_sha256"]:
            raise ValueError(f"retained source return hash drift: {batch_id}")
        retained_a = json.loads(raw)
        b_row = expected[("B", batch_id)]
        problem = verifier.validate_return(retained_a, "A", b_row, allowed_top, assessment_fields, adequacy_values)
        if problem:
            raise ValueError(f"retained A validation drift: {batch_id}: {problem}")
        fresh_b_path = RETURN_ROOT / "reviewer_B" / f"{batch_id}.json"
        pairs[batch_id] = (retained_a, json.loads(fresh_b_path.read_text()), {
            "A": {"return_path": ledger["source_return_path"], "source_commit": ledger["source_commit"], "return_sha256": ledger["source_return_sha256"], "selection": "VALIDATED_CANONICAL_A_RETAINED"},
            "B": {"return_path": str(fresh_b_path.relative_to(WORKSPACE)), "source_commit": None, "return_sha256": sha_path(fresh_b_path), "selection": "FRESH_USER_APPROVED_GATE_REISSUE"},
        })
    fresh_a_path = RETURN_ROOT / "reviewer_A" / "RQ2B-P4-V7-U1157.json"
    fresh_b_path = RETURN_ROOT / "reviewer_B" / "RQ2B-P4-V7-U1157.json"
    pairs["RQ2B-P4-V7-U1157"] = (json.loads(fresh_a_path.read_text()), json.loads(fresh_b_path.read_text()), {
        "A": {"return_path": str(fresh_a_path.relative_to(WORKSPACE)), "source_commit": None, "return_sha256": sha_path(fresh_a_path), "selection": "FRESH_USER_APPROVED_GATE_REISSUE"},
        "B": {"return_path": str(fresh_b_path.relative_to(WORKSPACE)), "source_commit": None, "return_sha256": sha_path(fresh_b_path), "selection": "FRESH_USER_APPROVED_GATE_REISSUE"},
    })
    if set(pairs) != {"RQ2B-P4-V7-U0527", "RQ2B-P4-V7-U0979", "RQ2B-P4-V7-U1068", "RQ2B-P4-V7-U1078", "RQ2B-P4-V7-U1157"}:
        raise ValueError("pair reconciliation scope drift")

    group_rows: list[dict[str, Any]] = []
    coordinator_rows: list[dict[str, Any]] = []
    exact_counts: Counter[str] = Counter()
    for batch_id in sorted(pairs):
        returned_a, returned_b, lineage = pairs[batch_id]
        a_by_token = {row["candidate_token"]: row["adequacy"] for row in returned_a["assessments"]}
        b_by_token = {row["candidate_token"]: row["adequacy"] for row in returned_b["assessments"]}
        if set(a_by_token) != set(b_by_token) or len(a_by_token) != 8:
            raise ValueError(f"assessment partition drift: {batch_id}")
        dispositions: list[dict[str, Any]] = []
        blocked = False
        for token in sorted(a_by_token):
            a, b = a_by_token[token], b_by_token[token]
            if a == b and a != "UNCLEAR":
                dispositions.append({"candidate_token": token, "final_adequacy": a, "decision_route": "EXACT_RETAINED_FRESH_INDEPENDENT_AGREEMENT"})
                exact_counts[a] += 1
            else:
                blocked = True
                coordinator_rows.append({
                    "batch_id": batch_id,
                    "blind_packet_id": expected[("B", batch_id)]["blind_packet_id"],
                    "candidate_token": token,
                    "reviewer_A_return_sha256": lineage["A"]["return_sha256"],
                    "reviewer_B_return_sha256": lineage["B"]["return_sha256"],
                    "route": "REQUIRES_FRESH_PROMPT_BOUND_SEALED_COORDINATOR",
                })
                dispositions.append({"candidate_token": token, "decision_route": "PENDING_SEALED_COORDINATOR"})
        group_rows.append({
            "batch_id": batch_id,
            "blind_packet_id": expected[("B", batch_id)]["blind_packet_id"],
            "selected_return_lineage": lineage,
            "candidate_dispositions": dispositions,
            "group_reconciliation_state": "PENDING_SEALED_COORDINATOR" if blocked else "TARGET_BLIND_REISSUE_PAIR_RECONCILED_PENDING_MASTER_SOP_READINESS",
        })
    OUTPUT.mkdir(parents=True)
    write_jsonl(OUTPUT / "target_blind_gate_reissue_pair_reconciliation.jsonl", group_rows)
    write_jsonl(OUTPUT / "sealed_coordinator_queue.jsonl", coordinator_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_gate_reissue_pair_reconciliation_v1",
        "status": "PASS_TARGET_BLIND_GATE_REISSUE_PAIR_RECONCILIATION_PENDING_SEALED_COORDINATOR" if coordinator_rows else "PASS_TARGET_BLIND_GATE_REISSUE_PAIR_RECONCILIATION_PENDING_MASTER_SOP_READINESS",
        "claim_boundary": "Target-blind mechanical pairing only; no target join, acceptable set, library update, retrieval result, metric, thesis result, or K change.",
        "counts": {
            "reissued_prompt_groups": len(group_rows),
            "candidate_assessments": 8 * len(group_rows),
            "exact_independent_agreements": sum(exact_counts.values()),
            "exact_adequacy_counts": dict(sorted(exact_counts.items())),
            "sealed_coordinator_candidates": len(coordinator_rows),
            "groups_pending_sealed_coordinator": sum(row["group_reconciliation_state"] == "PENDING_SEALED_COORDINATOR" for row in group_rows),
        },
        "bound_inputs": {
            "user_approved_reissue_dispatch": str(DISPATCH.relative_to(WORKSPACE)),
            "user_approved_reissue_dispatch_integrity_sha256": sha_path(DISPATCH / "integrity_report.json"),
            "fresh_return_validation": verification,
            "historical_integration_ledger": str((INTEGRATION / "integration_intake_ledger.jsonl").relative_to(WORKSPACE)),
            "historical_integration_ledger_sha256": sha_path(INTEGRATION / "integration_intake_ledger.jsonl"),
        },
        "u0323_disposition": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE_BY_USER_APPROVAL_2026-09-08",
        "stop_boundary": "Any queued candidate requires a fresh prompt-bound sealed coordinator. After coordinator closure, every V7 record must be reconciled or explicitly excluded, then a master-SOP readiness verifier must pass before target join or acceptable-set/library update.",
    }
    write_json(OUTPUT / "integrity_report.json", report)
    (OUTPUT / "integrity_report.md").write_text(
        "# V7 gate reissue pair reconciliation\n\n"
        f"- Reissued prompt groups: {len(group_rows)}\n"
        f"- Exact A/B candidate agreements: {sum(exact_counts.values())}\n"
        f"- Candidates requiring sealed coordinator: {len(coordinator_rows)}\n\n"
        "This package only pairs validated target-blind returns and preserves their selected raw lineage. `U0323` remains explicitly deferred/excluded from V7 closure. No target join, acceptable set, library update, or metric is produced.\n",
        encoding="utf-8",
    )
    (OUTPUT / "README.md").write_text(
        "# V7 gate reissue pair reconciliation\n\n"
        "Reproduce with:\n\n```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_gate_disposition_reissue.py\npython3 skill_benchmark/scripts/reconcile_rq2b_nc_phase5_v7_gate_disposition_reissue.py\n```\n\n"
        "The reconciler reads only validated target-blind returns and bound raw lineage. Exact non-unclear A/B agreement is mechanically reconciled; all disagreement or `UNCLEAR` is written to the sealed coordinator queue.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
