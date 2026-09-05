#!/usr/bin/env python3
"""Run the local-only RQ1b E1 T5 hash and no-reuse audit.

This script freezes only packets that already have a recorded strict T4
singleton consensus. It never re-evaluates prompts, source structure, or
reviewer decisions, and makes no retrieval/model/network call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t0-t1", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t0_t1_pair_audit.jsonl")
    parser.add_argument("--t4", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t4_blinded_singleton_ledger.jsonl")
    parser.add_argument("--source-inventory", type=Path, default=ROOT / "manifest/source_inventory.jsonl")
    parser.add_argument("--output", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t5_freeze_audit_2026-08-26.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parent_rows = {str(row["cluster_id"]): row for row in read_jsonl(args.t0_t1)}
    source_rows = {str(row["skill_id"]): row for row in read_jsonl(args.source_inventory)}
    t4_rows = read_jsonl(args.t4)
    frozen_ids = {skill_id for row in parent_rows.values() for skill_id in row["candidate_skill_ids"]}

    packet_records: list[dict[str, Any]] = []
    all_triads: Counter[str] = Counter()
    all_thirds: Counter[str] = Counter()
    for t4 in t4_rows:
        parent = parent_rows.get(str(t4["parent_pair_cluster_id"]))
        triad_ids = [str(value) for value in t4["candidate_skill_ids"]]
        parent_ids = [str(value) for value in parent["candidate_skill_ids"]] if parent else []
        third_ids = sorted(set(triad_ids) - set(parent_ids))
        source_records: dict[str, Any] = {}
        hash_failures: list[str] = []
        for skill_id in triad_ids:
            record = source_rows.get(skill_id)
            if not record:
                hash_failures.append(f"source_inventory_missing:{skill_id}")
                continue
            source_path = Path(str(record["source_path"]))
            if not source_path.is_file():
                hash_failures.append(f"source_file_missing:{skill_id}")
                continue
            actual = sha256(source_path)
            if actual != str(record["source_sha256"]):
                hash_failures.append(f"source_hash_mismatch:{skill_id}")
            source_records[skill_id] = {
                "source_path": str(source_path),
                "expected_sha256": str(record["source_sha256"]),
                "actual_sha256": actual,
            }
        parent_subset_ok = bool(parent) and set(parent_ids).issubset(triad_ids)
        one_third_ok = len(third_ids) == 1
        third_unfrozen_ok = one_third_ok and third_ids[0] not in frozen_ids
        all_triads.update(triad_ids)
        all_thirds.update(third_ids)
        packet_records.append(
            {
                "cluster_id": t4["cluster_id"],
                "parent_pair_cluster_id": t4["parent_pair_cluster_id"],
                "candidate_skill_ids": triad_ids,
                "derived_third_candidate_ids": third_ids,
                "parent_pair_subset_ok": parent_subset_ok,
                "exactly_one_new_third_ok": one_third_ok,
                "third_not_in_frozen_parent_corpus_ok": third_unfrozen_ok,
                "source_hash_records": source_records,
                "source_hash_failures": hash_failures,
                "cue_risk_retained": t4["cue_risk"],
            }
        )

    triad_reuse = {skill_id: count for skill_id, count in all_triads.items() if count > 1}
    third_reuse = {skill_id: count for skill_id, count in all_thirds.items() if count > 1}
    for record in packet_records:
        per_packet_reuse = [skill_id for skill_id in record["candidate_skill_ids"] if skill_id in triad_reuse]
        checks_pass = (
            record["parent_pair_subset_ok"]
            and record["exactly_one_new_third_ok"]
            and record["third_not_in_frozen_parent_corpus_ok"]
            and not record["source_hash_failures"]
            and not per_packet_reuse
            and not any(skill_id in third_reuse for skill_id in record["derived_third_candidate_ids"])
        )
        record["cross_packet_candidate_reuse"] = per_packet_reuse
        record["t5_result"] = "PASS" if checks_pass else "FAIL"

    pass_count = sum(record["t5_result"] == "PASS" for record in packet_records)
    report = {
        "status": "T5_COMPLETE_LOCAL_HASH_AND_NO_REUSE_AUDIT_NOT_A_RETRIEVAL_RESULT",
        "t4_consensus_packet_count": len(t4_rows),
        "t5_pass_count": pass_count,
        "t5_fail_count": len(t4_rows) - pass_count,
        "cross_packet_candidate_reuse": triad_reuse,
        "cross_packet_third_candidate_reuse": third_reuse,
        "packets": packet_records,
        "freeze_status_if_all_pass": "VALID_TRIADIC_EXTENSION_ORIGINAL_ONLY",
        "strict_yield_interpretation": "The resulting count is a strict public-triad feasibility yield, not a whole-library routing result or a causal field effect.",
        "boundary": "Local hash/no-reuse audit only. It does not replace T2/T3/T4, assess semantic fidelity, or create selector/embedding/retrieval/thesis results.",
    }
    if len(t4_rows) != 6:
        raise SystemExit(f"Expected six T4 consensus packets, found {len(t4_rows)}")
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in report if key != "packets"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
