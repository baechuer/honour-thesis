#!/usr/bin/env python3
"""Materialise the final, local-only manifest for E1 T5-passing packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t2", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t2_source_screening.jsonl")
    parser.add_argument("--t3", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t3_strict_ledger.jsonl")
    parser.add_argument("--t4", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t4_blinded_singleton_ledger.jsonl")
    parser.add_argument("--t5", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t5_freeze_audit_2026-08-26.json")
    parser.add_argument("--output", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t5_frozen_manifest_2026-08-26.jsonl")
    parser.add_argument("--certificate", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t5_freeze_certificate_2026-08-26.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    t2_rows = read_jsonl(args.t2)
    t3_rows = {str(row["cluster_id"]): row for row in read_jsonl(args.t3)}
    t4_rows = {str(row["cluster_id"]): row for row in read_jsonl(args.t4)}
    t5 = json.loads(args.t5.read_text(encoding="utf-8"))
    if t5["t5_fail_count"] or t5["t5_pass_count"] != 6:
        raise SystemExit("T5 did not establish six clean packets; refusing to freeze.")

    frozen: list[dict[str, Any]] = []
    for packet in sorted(t5["packets"], key=lambda item: str(item["cluster_id"])):
        if packet["t5_result"] != "PASS":
            continue
        cluster_id = str(packet["cluster_id"])
        candidate_ids = set(packet["candidate_skill_ids"])
        matching_t2 = [
            row for row in t2_rows
            if set(row.get("candidate_skill_ids", [])) == candidate_ids
            and row["e1_status"] in {
                "T2_SOURCE_BACKED_TRIAD_DRAFT_NOT_A_VALID_CLUSTER",
                "T2_SOURCE_BACKED_ALTERNATE_TRIAD_DRAFT_NOT_A_VALID_CLUSTER",
            }
        ]
        t3 = t3_rows.get(cluster_id)
        t4 = t4_rows.get(cluster_id)
        if len(matching_t2) != 1 or not t3 or not t4:
            raise SystemExit(f"Missing exact gate evidence for {cluster_id}")
        if t3["e1_status"] != "T3_PASS_STRICT_SINGLETON_PENDING_BLINDED_T4":
            raise SystemExit(f"T3 is not a strict pass for {cluster_id}")
        if t4["e1_status"] != "T4_MODEL_ASSISTED_BLINDED_SINGLETON_CONSENSUS_PENDING_T5":
            raise SystemExit(f"T4 is not a consensus packet for {cluster_id}")
        frozen.append(
            {
                "e1_status": "VALID_TRIADIC_EXTENSION_ORIGINAL_ONLY",
                "cluster_id": cluster_id,
                "parent_pair_cluster_id": packet["parent_pair_cluster_id"],
                "candidate_skill_ids": packet["candidate_skill_ids"],
                "third_candidate_skill_id": packet["derived_third_candidate_ids"][0],
                "source_hash_records": packet["source_hash_records"],
                "t2_evidence_locator": {
                    "parent_pair_cluster_id": matching_t2[0]["parent_pair_cluster_id"],
                    "candidate_skill_ids": matching_t2[0]["candidate_skill_ids"],
                    "e1_status": matching_t2[0]["e1_status"],
                    "source_screen_card": matching_t2[0].get("source_screen_card"),
                    "screen_id_if_present": matching_t2[0].get("screen_id"),
                },
                "t3_status": t3["e1_status"],
                "t4_status": t4["e1_status"],
                "t4_per_prompt_singleton_skill_id": t4["per_prompt_singleton_skill_id"],
                "cue_risk_retained": t4["cue_risk"],
                "t5_status": "PASS_HASH_AND_NO_REUSE",
                "boundary": "Strict natural-original triadic-extension curation record. It is not a human-annotation result, causal field test, semantic-fidelity validation, selector result, embedding result, retrieval result, or thesis result.",
            }
        )
    if len(frozen) != 6:
        raise SystemExit(f"Expected six frozen packets, materialised {len(frozen)}")
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True, allow_nan=False) + "\n" for row in frozen), encoding="utf-8")
    certificate = {
        "status": "E1_STRICT_PUBLIC_TRIAD_FEASIBILITY_AUDIT_COMPLETE",
        "frozen_strict_triad_count": len(frozen),
        "targeted_frozen_parent_pair_count": 74,
        "standalone_robustness_threshold": 30,
        "threshold_reached": False,
        "interpretation": "Six strict natural-original triads survive T0-T5. The completed E1 pass is a feasibility audit, not a standalone multi-neighbour robustness stratum and not a basis for a universal public-routing claim.",
        "no_wave_003_fill_rule": "Do not enlarge this result by relaxing singleton gold or inserting workflow components. Any Wave 003 public-source discovery must be separately designed and frozen.",
        "inputs": {"t2": str(args.t2), "t3": str(args.t3), "t4": str(args.t4), "t5": str(args.t5)},
        "output": str(args.output),
        "boundary": "Local curation completion only; no retrieval, external transfer, model, selector, reranker, or thesis result was produced.",
    }
    args.certificate.write_text(json.dumps(certificate, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
