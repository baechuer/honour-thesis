#!/usr/bin/env python3
"""Reconcile a validated Phase-4 unified blind batch without opening joins or targets."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v4-unified-8candidate-blind-delivery"
BATCH_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-unified-target-blind-batches-2026-09-05"
RETURN_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-unified-independent-returns-2026-09-05"
OUT = NC_ROOT / "review/RQ2B-NC-phase4-unified-reconciliation-2026-09-05"
ALLOWED = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("reviewer_output_sha256", None)
    return hashlib.sha256(json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def load_checked_return(batch_id: str, reviewer: str, manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    batch_path = BATCH_ROOT / f"reviewer_{reviewer}" / f"{batch_id}.json"
    return_path = RETURN_ROOT / f"reviewer_{reviewer}" / f"{batch_id}.json"
    if not batch_path.is_file() or not return_path.is_file():
        raise SystemExit(f"Missing frozen batch or independent return for reviewer {reviewer}")
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    returned = json.loads(return_path.read_text(encoding="utf-8"))
    packet = batch.get("packet")
    if not isinstance(packet, dict) or returned.get("reviewer_blind_id") != reviewer or returned.get("batch_id") != batch_id or returned.get("blind_packet_id") != manifest["blind_packet_id"] or returned.get("batch_input_sha256") != batch.get("batch_input_sha256") or returned.get("reviewer_instruction_sha256") != manifest["reviewer_instruction_sha256"] or returned.get("reviewer_output_sha256") != canonical_sha(returned):
        raise SystemExit(f"Independent return binding drift for reviewer {reviewer}")
    assessments = returned.get("assessments")
    tokens = {candidate["candidate_token"] for candidate in packet.get("candidates", [])}
    if not isinstance(assessments, list) or len(tokens) != 8 or len(assessments) != 8 or {item.get("candidate_token") for item in assessments} != tokens or any(item.get("adequacy") not in ALLOWED or not isinstance(item.get("source_anchor"), str) or not item["source_anchor"].strip() or not isinstance(item.get("rationale"), str) or not item["rationale"].strip() for item in assessments):
        raise SystemExit(f"Independent return content drift for reviewer {reviewer}")
    return batch, returned


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    target = out / args.batch_id
    if target.exists():
        raise SystemExit(f"Refusing to overwrite reconciliation: {target}")
    summary = json.loads((EXECUTION / "summary.json").read_text(encoding="utf-8"))
    if summary.get("status") != "PASS_PHASE4_UNIFIED_BLIND_REVIEW_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS":
        raise SystemExit("Unified execution state drift")
    for name, expected in summary["outputs"].items():
        path = EXECUTION / name
        if not path.is_file() or sha(path) != expected:
            raise SystemExit(f"Execution-freeze hash drift: {name}")
    manifest = next((json.loads(line) for line in (EXECUTION / "unified_prompt_group_batch_manifest.jsonl").read_text(encoding="utf-8").splitlines() if line and json.loads(line)["batch_id"] == args.batch_id), None)
    if manifest is None:
        raise SystemExit("Unknown frozen unified batch")
    batch_a, return_a = load_checked_return(args.batch_id, "A", manifest)
    batch_b, return_b = load_checked_return(args.batch_id, "B", manifest)
    if batch_a["packet"] != batch_b["packet"]:
        raise SystemExit("Reviewer packet-rendering mismatch")
    by_a = {item["candidate_token"]: item for item in return_a["assessments"]}
    by_b = {item["candidate_token"]: item for item in return_b["assessments"]}
    source_by_token = {item["candidate_token"]: item["source_full_skill"] for item in batch_a["packet"]["candidates"]}
    agreements, coordinator_packets = [], []
    for token in sorted(by_a):
        decision_a, decision_b = by_a[token]["adequacy"], by_b[token]["adequacy"]
        if decision_a == decision_b and decision_a != "UNCLEAR":
            disposition = "EXACT_AGREEMENT_RETAINED"
        else:
            disposition = "COORDINATOR_REQUIRED"
            coordinator_packets.append({"blind_packet_id": manifest["blind_packet_id"], "candidate_token": token, "reviewer_A_assessment": by_a[token], "reviewer_B_assessment": by_b[token], "fresh_source_visible_skill": source_by_token[token], "coordinator_instruction": "Resolve only the A/B adequacy disagreement or UNCLEAR trigger using this fresh source-visible rendering and the frozen rubric. Do not inspect targets, main/tail role, allocation, rank, path, provenance, historical/local reference or retrieval outcome."})
        agreements.append({"candidate_token": token, "reviewer_A_adequacy": decision_a, "reviewer_B_adequacy": decision_b, "reconciliation_disposition": disposition})
    target.mkdir(parents=True)
    (target / "reconciliation_ledger.json").write_text(json.dumps({"batch_id": args.batch_id, "blind_packet_id": manifest["blind_packet_id"], "reviewer_A_return_sha256": sha(RETURN_ROOT / "reviewer_A" / f"{args.batch_id}.json"), "reviewer_B_return_sha256": sha(RETURN_ROOT / "reviewer_B" / f"{args.batch_id}.json"), "candidate_reconciliations": agreements, "status": "PENDING_SEALED_COORDINATOR_FOR_DISAGREEMENTS_OR_UNCLEAR" if coordinator_packets else "PASS_EXACT_INDEPENDENT_AGREEMENT_PENDING_LIBRARY_LEVEL_CLOSURE"}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (target / "sealed_coordinator_packets.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for packet in coordinator_packets:
            handle.write(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n")
    result = {"batch_id": args.batch_id, "exact_agreements": sum(row["reconciliation_disposition"] == "EXACT_AGREEMENT_RETAINED" for row in agreements), "coordinator_packets": len(coordinator_packets), "status": "PASS_RECONCILIATION_MATERIALISED_PENDING_COORDINATOR" if coordinator_packets else "PASS_EXACT_AGREEMENT_PENDING_LIBRARY_LEVEL_CLOSURE"}
    (target / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
