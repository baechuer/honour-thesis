#!/usr/bin/env python3
"""Repair only V7 coordinator-packet dispatch without reopening its independent review.

The V7-C2 output is fail-closed: it freezes and rechecks the repair runtime,
the V7 delivery, and both already-validated reviewer returns.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
PROTOCOL_PATH = BENCHMARK / "scripts/rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
RETURN_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
OUT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-coordinator-packet-repair-v2-2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def protocol() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_v7_protocol", PROTOCOL_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load V7 protocol implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if module.EXECUTION != EXECUTION or module.RETURN_ROOT != RETURN_ROOT:
        raise ValueError("Coordinator repair is not bound to the frozen V7 protocol")
    return module


def expected_bound_paths(batch_id: str) -> set[str]:
    return {
        str(Path(__file__).resolve().relative_to(WORKSPACE)),
        str(PROTOCOL_PATH.relative_to(WORKSPACE)),
        str((EXECUTION / "summary.json").relative_to(WORKSPACE)),
        str((RETURN_ROOT / "reviewer_A" / f"{batch_id}.json").relative_to(WORKSPACE)),
        str((RETURN_ROOT / "reviewer_B" / f"{batch_id}.json").relative_to(WORKSPACE)),
    }


def materialise(batch_id: str, output_dir: Path) -> None:
    out = output_dir.resolve() / batch_id
    if out.exists():
        raise ValueError(f"Refusing to overwrite V7 coordinator repair: {out}")
    p = protocol()
    p.verify_execution()
    _, return_a, path_a = p.load_validated_return(batch_id, "A")
    _, return_b, path_b = p.load_validated_return(batch_id, "B")
    by_a = {item["candidate_token"]: item for item in return_a["assessments"]}
    by_b = {item["candidate_token"]: item for item in return_b["assessments"]}
    packets: list[dict[str, Any]] = []
    for token in sorted(by_a):
        if by_a[token]["adequacy"] != by_b[token]["adequacy"] or "UNCLEAR" in {by_a[token]["adequacy"], by_b[token]["adequacy"]}:
            bindings, packet, _ = p.coordinator_context(batch_id, token)
            packets.append({"packet_sha256": canonical_sha(packet), "bindings": bindings, "packet": packet})
    if not packets:
        raise ValueError("No V7 coordinator-eligible packets for this batch")
    out.mkdir(parents=True)
    packets_path = out / "strict_sealed_coordinator_packets.jsonl"
    write_jsonl(packets_path, packets)
    summary = {
        "status": "PASS_V7_COORDINATOR_PACKET_REPAIR_V2_PENDING_FRESH_COORDINATOR_RETURNS",
        "batch_id": batch_id,
        "claim_boundary": "This repairs coordinator-packet dispatch only. It uses already-validated independent returns, preserves their target-blind source-only boundary, and makes no final candidate or library disposition.",
        "reason": "The original V7 reconciliation renderer omitted reviewer-return SHA bindings from coordinator-visible packets. This V7-C2 repair rebuilds every eligible packet from the V7 protocol's independently validated return loader, includes the exact bindings required by the frozen coordinator schema, and fail-closed verifies its entire bound-input ledger.",
        "bound_inputs": {
            str(Path(__file__).resolve().relative_to(WORKSPACE)): sha(Path(__file__).resolve()),
            str(PROTOCOL_PATH.relative_to(WORKSPACE)): sha(PROTOCOL_PATH),
            str((EXECUTION / "summary.json").relative_to(WORKSPACE)): sha(EXECUTION / "summary.json"),
            str(path_a.relative_to(WORKSPACE)): sha(path_a),
            str(path_b.relative_to(WORKSPACE)): sha(path_b),
        },
        "outputs": {packets_path.name: sha(packets_path)},
        "coordinator_packets": len(packets),
    }
    write_json(out / "summary.json", summary)
    print(json.dumps({"batch_id": batch_id, "coordinator_packets": len(packets), "output": str(out), "status": summary["status"]}, sort_keys=True))


def verify(batch_id: str, output_dir: Path) -> None:
    out = output_dir.resolve() / batch_id
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    if summary.get("status") != "PASS_V7_COORDINATOR_PACKET_REPAIR_V2_PENDING_FRESH_COORDINATOR_RETURNS":
        raise ValueError("V7 coordinator-repair status drift")
    if set(summary.get("bound_inputs", {})) != expected_bound_paths(batch_id):
        raise ValueError("V7 coordinator-repair bound-input keyset drift")
    for relative, expected in summary["bound_inputs"].items():
        path = (WORKSPACE / relative).resolve()
        if not path.is_relative_to(WORKSPACE) or not path.is_file() or sha(path) != expected:
            raise ValueError(f"V7 coordinator-repair bound-input drift: {relative}")
    packet_path = out / "strict_sealed_coordinator_packets.jsonl"
    if set(summary.get("outputs", {})) != {packet_path.name} or sha(packet_path) != summary["outputs"][packet_path.name]:
        raise ValueError("V7 coordinator-repair output hash drift")
    p = protocol()
    rows = [json.loads(line) for line in packet_path.read_text(encoding="utf-8").splitlines() if line]
    if len(rows) != summary["coordinator_packets"]:
        raise ValueError("V7 coordinator-repair cardinality drift")
    for row in rows:
        token = row["bindings"]["candidate_token"]
        bindings, packet, _ = p.coordinator_context(batch_id, token)
        if row != {"packet_sha256": canonical_sha(packet), "bindings": bindings, "packet": packet}:
            raise ValueError("V7 coordinator-repair packet content binding drift")
    print(json.dumps({"batch_id": batch_id, "coordinator_packets": len(rows), "status": "PASS_V7_COORDINATOR_PACKET_REPAIR_VERIFIED"}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("materialise")
    make.add_argument("--batch-id", required=True)
    make.add_argument("--output-dir", type=Path, default=OUT)
    check = sub.add_parser("verify")
    check.add_argument("--batch-id", required=True)
    check.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    try:
        if args.command == "materialise":
            materialise(args.batch_id, args.output_dir)
        else:
            verify(args.batch_id, args.output_dir)
    except ValueError as exc:
        raise SystemExit(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
