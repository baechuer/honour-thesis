#!/usr/bin/env python3
"""Fail-closed reconciliation controller for one or more Phase-5 packets.

This controller is deliberately transport/reconciliation only.  It validates
packet identity and complete A/B coverage, keeps disagreements sealed, and
never opens a target/token join unless every semantic decision is reconciled.
It does not read historical outcomes, retrieval output, embeddings, or
provider results.  A missing return is a BLOCK, never an implicit rejection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

DECISIONS = {
    "FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR",
    "ACCEPT", "REJECT", "PASS", "FAIL", "BLOCK", "BLOCKED_OR_UNCLEAR",
}
BATCH_ADEQUACY_DECISIONS = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}
DECISION_KEYS = ("adequacy", "decision", "disposition", "outcome", "relation_decision", "cue_decision")
ID_KEYS = ("packet_id", "blind_packet_id", "batch_id", "item_id", "candidate_token")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("packets", "items", "batches", "records", "assessments"):
            if isinstance(value.get(key), list):
                return value[key]
    raise ValueError(f"Expected JSON object-list: {path}")


def pick(path: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        candidate = path / name
        if candidate.is_file():
            return candidate
    return None


def identity(row: dict[str, Any]) -> str | None:
    for key in ID_KEYS:
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def decision(row: dict[str, Any]) -> str | None:
    for key in DECISION_KEYS:
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def packet_sha(row: dict[str, Any]) -> str | None:
    for key in ("packet_sha256", "packet_input_sha256", "batch_input_sha256", "input_sha256"):
        value = row.get(key)
        if isinstance(value, str):
            return value
    return None


def method_gate(row: dict[str, Any]) -> str:
    """Apply only the declared post-join gate, never infer a label."""
    if row.get("positive_tail") is True or row.get("tail_outcome") in {"PARTIALLY_ADEQUATE", "FULLY_ACCEPTABLE"}:
        return "METHOD_GATE_OPEN_POSITIVE_TAIL"
    if row.get("quality_issue") is True or row.get("unresolved_quality_issue") is True:
        return "BLOCK_UNRESOLVED_QUALITY_OR_TAIL_ISSUE"
    values = row.get("acceptable_set_source_sha256", row.get("acceptable_set", []))
    if not isinstance(values, list):
        return "BLOCK_ACCEPTABLE_SET_UNAVAILABLE"
    if len(values) == 1:
        return "STRICT_FINAL_CANDIDATE"
    if len(values) > 1:
        return "ACCEPTABLE_MULTI"
    return "BLOCK_NO_ACCEPTABLE_SOURCE"


def run_phase5_batch(args: argparse.Namespace, main_path: Path, tail_path: Path) -> int:
    """Reconcile the actual K=6 Batch packet shape (one row per candidate)."""
    out = args.out.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing output: {out}")
    main = read_rows(main_path); tail = read_rows(tail_path)
    allocation_path = main_path.parent / "batch_group_allocation.jsonl"
    if not allocation_path.is_file():
        raise SystemExit("Missing batch_group_allocation.jsonl")
    allocation_rows = read_rows(allocation_path)
    allocation = {r.get("packet_id"): r for r in allocation_rows}
    allocation_by_prompt = {r.get("prompt_sha256"): r for r in allocation_rows}
    packets = [("main", row) for row in main] + [("tail", row) for row in tail]
    expected: dict[tuple[str, str], dict[str, Any]] = {}
    errors: list[str] = []
    for kind, packet in packets:
        pid = packet.get("packet_id")
        candidates = packet.get("candidates")
        if not isinstance(pid, str) or not isinstance(candidates, list):
            errors.append(f"packet:invalid:{pid}"); continue
        group = allocation.get(pid) or allocation_by_prompt.get(packet.get("prompt_sha256"))
        if not isinstance(group, dict) or not isinstance(group.get("batch_group_id"), str):
            errors.append(f"packet:missing_batch_group_id:{pid}")
        for candidate in candidates:
            token = candidate.get("candidate_token") if isinstance(candidate, dict) else None
            if not isinstance(token, str) or not token:
                errors.append(f"packet:missing_candidate_token:{pid}"); continue
            key = (pid, token)
            if key in expected: errors.append(f"packet:duplicate_assessment:{pid}:{token}")
            else: expected[key] = {"packet_id": pid, "candidate_token": token, "packet_kind": kind, "batch_group_id": group.get("batch_group_id") if group else None, "packet": packet, "candidate": candidate}
    collection_sha = hashlib.sha256(main_path.read_bytes() + tail_path.read_bytes()).hexdigest()
    returns: dict[str, list[dict[str, Any]]] = {}
    for role, path in (("A", args.reviewer_a), ("B", args.reviewer_b)):
        if path is None or not path.is_file():
            errors.append(f"{role}:missing_return_file")
            returns[role] = []; continue
        rows = read_rows(path); returns[role] = rows; seen: set[tuple[str, str]] = set()
        for row in rows:
            pid, token = row.get("packet_id"), row.get("candidate_token")
            key = (pid, token)
            if key not in expected: errors.append(f"{role}:unexpected_assessment:{pid}:{token}"); continue
            if key in seen: errors.append(f"{role}:duplicate_assessment:{pid}:{token}"); continue
            seen.add(key)
            expected_row = expected[key]
            if row.get("batch_group_id") != expected_row["batch_group_id"]:
                errors.append(f"{role}:batch_group_id_mismatch:{pid}:{token}")
            if row.get("adequacy_decision") not in BATCH_ADEQUACY_DECISIONS:
                errors.append(f"{role}:missing_or_invalid_adequacy_decision:{pid}:{token}")
            if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
                errors.append(f"{role}:missing_rationale:{pid}:{token}")
            anchors = row.get("source_anchors", row.get("anchors"))
            if not isinstance(anchors, list) or not anchors:
                errors.append(f"{role}:missing_anchors:{pid}:{token}")
            expected_tail = expected_row["packet_kind"] == "TAIL_CHALLENGE"
            if row.get("tail_flag") is not expected_tail:
                errors.append(f"{role}:tail_flag_mismatch:{pid}:{token}")
            supplied = row.get("input_packet_sha256") or row.get("packet_collection_sha256")
            if supplied != collection_sha:
                errors.append(f"{role}:input_packet_sha256_mismatch:{pid}:{token}")
        errors.extend(f"{role}:missing_assessment:{pid}:{token}" for pid, token in sorted(set(expected) - seen))
        if len(rows) != len(expected): errors.append(f"{role}:coverage_count:{len(rows)}_of_{len(expected)}")
    by_role = {role: {(r.get("packet_id"), r.get("candidate_token")): r for r in rows} for role, rows in returns.items()}
    disagreements: list[dict[str, Any]] = []; reconciled: list[dict[str, Any]] = []
    if not errors:
        for key in sorted(expected):
            a, b = by_role["A"][key], by_role["B"][key]
            da, db = a["adequacy_decision"], b["adequacy_decision"]
            base = {"packet_id": key[0], "candidate_token": key[1], "reviewer_a_decision": da, "reviewer_b_decision": db}
            if da == db and da not in {"UNCLEAR", "BLOCKED_OR_UNCLEAR"}:
                reconciled.append({**base, "reconciliation": "EXACT_AB_AGREEMENT"})
            else:
                disagreements.append({**base, "reconciliation": "SEALED_COORDINATOR_REQUIRED", "packet_evidence": {"packet_id": key[0], "candidate_token": key[1], "packet_kind": expected[key]["packet_kind"], "prompt": expected[key]["packet"]["prompt"], "candidate": expected[key]["candidate"]}})
    coord_rows: list[dict[str, Any]] = []
    for path in args.coordinator:
        if path.is_file(): coord_rows.extend(read_rows(path))
        else: errors.append(f"coordinator:missing_file:{path}")
    coord_by_key = {(r.get("packet_id"), r.get("candidate_token")): r for r in coord_rows}
    required_coord = {(r["packet_id"], r["candidate_token"]) for r in disagreements}
    if not errors:
        errors.extend(f"coordinator:unexpected_assessment:{p}:{t}" for p, t in sorted(set(coord_by_key) - required_coord))
        for item in disagreements:
            key = (item["packet_id"], item["candidate_token"]); row = coord_by_key.get(key)
            if row is None: errors.append(f"coordinator:missing_assessment:{key[0]}:{key[1]}"); continue
            dc = row.get("adequacy_decision")
            if row.get("batch_group_id") != expected[item["packet_id"], item["candidate_token"]]["batch_group_id"]:
                errors.append(f"coordinator:batch_group_id_mismatch:{key[0]}:{key[1]}")
            if dc not in BATCH_ADEQUACY_DECISIONS or dc == "UNCLEAR":
                errors.append(f"coordinator:unresolved_assessment:{key[0]}:{key[1]}")
            else: reconciled.append({"packet_id": key[0], "candidate_token": key[1], "coordinator_decision": dc, "reconciliation": "SEALED_COORDINATOR_RESOLVED"})
    out.mkdir(parents=True)
    (out / "sealed_disagreements.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in disagreements), encoding="utf-8")
    (out / "reconciled_assessments.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in reconciled), encoding="utf-8")
    missing = [{"role": role, "packet_id": pid, "candidate_token": token, "reason": "RETURN_NOT_PRESENT"} for role in ("A", "B") for pid, token in sorted(set(expected) - {(r.get("packet_id"), r.get("candidate_token")) for r in returns[role]})]
    (out / "missing_return_staging.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in missing), encoding="utf-8")
    status = "PASS_BATCH_RECONCILED_NO_TARGET_JOIN" if not errors else "BLOCK_PHASE5_BATCH_RECONCILIATION"
    summary = {"status": status, "batch_mode": True, "packet_files": {"main": str(main_path), "tail": str(tail_path)}, "packet_collection_sha256": collection_sha, "counts": {"expected_assessments": len(expected), "reviewer_a_returns": len(returns["A"]), "reviewer_b_returns": len(returns["B"]), "missing_returns": len(missing), "sealed_disagreements": len(disagreements), "reconciled": len(reconciled)}, "validation_errors": errors, "target_join_performed": False, "k": 6, "retrieval_or_embedding_executed": False, "labels_or_results_read": False}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True)); return 0 if not errors else 2


def validate_return(row: dict[str, Any], expected: dict[str, Any], role: str) -> list[str]:
    errors: list[str] = []
    if identity(row) != identity(expected):
        errors.append(f"{role}:identity_mismatch")
    expected_sha = packet_sha(expected)
    actual_sha = packet_sha(row)
    if not expected_sha:
        errors.append(f"packet:missing_packet_sha:{identity(expected)}")
    elif actual_sha != expected_sha:
        errors.append(f"{role}:packet_sha_mismatch:{identity(row)}")
    value = decision(row)
    if value not in DECISIONS:
        errors.append(f"{role}:missing_or_invalid_decision:{identity(row)}")
    if not any(isinstance(row.get(k), str) and row[k].strip() for k in ("rationale", "reason", "source_anchor", "source_anchors")):
        errors.append(f"{role}:missing_rationale_or_anchor:{identity(row)}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packet-dir", type=Path, required=True)
    ap.add_argument("--reviewer-a", type=Path)
    ap.add_argument("--reviewer-b", type=Path)
    ap.add_argument("--coordinator", type=Path, action="append", default=[])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--target-map", type=Path, help="Optional post-reconciliation-only join map")
    args = ap.parse_args()
    packet_dir = args.packet_dir.resolve(); out = args.out.resolve()
    main_packet = packet_dir / "main_blind_review_packets.jsonl"
    tail_packet = packet_dir / "tail_blind_review_packets.jsonl"
    if main_packet.is_file() and tail_packet.is_file():
        return run_phase5_batch(args, main_packet, tail_packet)
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing output: {out}")
    packet_path = pick(packet_dir, ("packet_manifest.jsonl", "prompt_group_batch_manifest.jsonl", "batch_manifest.jsonl", "packets.jsonl"))
    if packet_path is None:
        raise SystemExit("Missing packet manifest (packet_manifest.jsonl or prompt_group_batch_manifest.jsonl)")
    packets = read_rows(packet_path)
    errors: list[str] = []
    pids = [identity(row) for row in packets]
    if not packets or any(value is None for value in pids) or len(set(pids)) != len(pids):
        errors.append("packet:empty_or_duplicate_or_missing_identity")
    packet_by_id = {identity(row): row for row in packets if identity(row)}
    returns: dict[str, list[dict[str, Any]]] = {}
    for role, path in (("A", args.reviewer_a), ("B", args.reviewer_b)):
        if path is None or not path.is_file():
            errors.append(f"{role}:missing_return_file")
            returns[role] = []
            continue
        rows = read_rows(path); returns[role] = rows
        seen: set[str] = set()
        for row in rows:
            rid = identity(row)
            if rid not in packet_by_id: errors.append(f"{role}:unexpected_identity:{rid}")
            elif rid in seen: errors.append(f"{role}:duplicate_identity:{rid}")
            else: seen.add(rid); errors.extend(validate_return(row, packet_by_id[rid], role))
        missing = sorted(set(packet_by_id) - seen)
        errors.extend(f"{role}:missing_identity:{value}" for value in missing)
        if len(rows) != len(packet_by_id): errors.append(f"{role}:coverage_count:{len(rows)}_of_{len(packet_by_id)}")
    by_role = {role: {identity(row): row for row in rows if identity(row)} for role, rows in returns.items()}
    disagreements: list[dict[str, Any]] = []
    reconciled: list[dict[str, Any]] = []
    if not errors:
        for pid in sorted(packet_by_id):
            a, b = by_role["A"][pid], by_role["B"][pid]
            da, db = decision(a), decision(b)
            if da == db and da not in {"UNCLEAR", "BLOCKED_OR_UNCLEAR"}:
                reconciled.append({"packet_id": pid, "decision": da, "reconciliation": "EXACT_AB_AGREEMENT"})
            else:
                disagreements.append({"packet_id": pid, "reviewer_a_decision": da, "reviewer_b_decision": db, "reconciliation": "SEALED_COORDINATOR_REQUIRED"})
    coord_rows = []
    for path in args.coordinator:
        if path.is_file(): coord_rows.extend(read_rows(path))
        else: errors.append(f"coordinator:missing_file:{path}")
    coord_by_id = {identity(row): row for row in coord_rows if identity(row)}
    if not errors:
        errors.extend(f"coordinator:unexpected_identity:{value}" for value in sorted(set(coord_by_id) - set(disagreements[i]["packet_id"] for i in range(len(disagreements)))))
    if not errors and disagreements:
        for item in disagreements:
            row = coord_by_id.get(item["packet_id"])
            if row is None:
                errors.append(f"coordinator:missing_identity:{item['packet_id']}")
                continue
            dc = decision(row)
            if dc is None or dc in {"UNCLEAR", "BLOCKED_OR_UNCLEAR"}:
                errors.append(f"coordinator:unresolved:{item['packet_id']}")
            else:
                reconciled.append({"packet_id": item["packet_id"], "decision": dc, "reconciliation": "SEALED_COORDINATOR_RESOLVED"})
    if not errors and len(reconciled) != len(packet_by_id):
        errors.append("reconciliation:incomplete_coverage")
    out.mkdir(parents=True)
    sealed = out / "sealed_disagreements.jsonl"
    sealed.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in disagreements), encoding="utf-8")
    (out / "reconciled_decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in reconciled), encoding="utf-8")
    missing = []
    for role in ("A", "B"):
        seen = {identity(row) for row in returns[role] if identity(row)}
        missing.extend({"role": role, "packet_id": pid, "reason": "RETURN_NOT_PRESENT"} for pid in sorted(set(packet_by_id) - seen))
    (out / "missing_return_staging.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in missing), encoding="utf-8")
    joined = False
    if args.target_map and not errors:
        target_rows = read_rows(args.target_map)
        target_by_id = {identity(row): row for row in target_rows if identity(row)}
        if set(target_by_id) != set(packet_by_id): errors.append("target_join:exact_coverage_required")
        else:
            # Deliberately performed after all A/B/coordinator decisions are closed.
            joined_rows = []
            for row in reconciled:
                joined_row = {**row, **target_by_id[row["packet_id"]]}
                joined_row["method_gate"] = method_gate(joined_row)
                joined_rows.append(joined_row)
            (out / "post_reconciliation_target_join.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in joined_rows), encoding="utf-8")
            joined = True
    status = "PASS_RECONCILED_NO_TARGET_JOIN" if not errors and not joined else "PASS_RECONCILED_TARGET_JOINED" if not errors else "BLOCK_PHASE5_RECONCILIATION"
    summary = {"status": status, "packet_manifest": str(packet_path), "packet_manifest_sha256": digest(packet_path), "counts": {"packets": len(packets), "reviewer_a_returns": len(returns["A"]), "reviewer_b_returns": len(returns["B"]), "missing_returns": len(missing), "sealed_disagreements": len(disagreements), "reconciled": len(reconciled)}, "validation_errors": errors, "target_join_performed": joined, "k": 6, "retrieval_or_embedding_executed": False, "labels_or_results_read": False, "claim_boundary": "No final library, acceptable-set, strict-gold, retrieval, or experiment conclusion is emitted by this controller."}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
