#!/usr/bin/env python3
"""Freeze eligible RQ1b cross-source primary prompt packets after C1--C5.

The script validates local curation facts only. It does not retrieve, embed,
rerank, contact an external service, or produce an empirical metric.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


STRICT = "C5_PRIMARY_STRICT_SINGLETON_GOLD_NOT_FROZEN_NOT_A_RESULT"
EXPLORATORY = "C5_EXPLORATORY_ACCEPTABLE_SET_NOT_A_GOLD_OR_RESULT"
UNRESOLVED = "C5_UNRESOLVED_C4_DISAGREEMENT_NOT_A_GOLD_OR_RESULT"
C3_SAFE_DISPOSITIONS = {
    "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT",
    "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c5", type=Path, required=True)
    parser.add_argument("--c4-key", type=Path, required=True)
    parser.add_argument("--c1", type=Path, action="append", required=True)
    parser.add_argument("--c3-audit", type=Path, required=True)
    parser.add_argument("--c3-manual", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    c3 = read_json(args.c3_audit)
    if c3.get("status") != "C3_LITERAL_CUE_AUDIT_COMPLETE_NOT_A_LABEL_OR_RESULT":
        raise SystemExit(f"unexpected_c3_status:{c3.get('status')}")
    c1_by_proposal: dict[str, dict[str, Any]] = {}
    for path in args.c1:
        for row in read_jsonl(path):
            proposal_id = str(row.get("proposal_id", ""))
            if proposal_id in c1_by_proposal:
                raise SystemExit(f"duplicate_c1_proposal:{proposal_id}")
            c1_by_proposal[proposal_id] = row
    key_by_packet = {str(row["review_packet_id"]): row for row in read_jsonl(args.c4_key)}
    c3_manual = {(str(row.get("proposal_id")), str(row.get("intended_candidate_skill_id")), str(row.get("variant"))): row for row in read_jsonl(args.c3_manual)}
    c5_rows = read_jsonl(args.c5)

    owner_by_candidate: dict[str, str] = {}
    frozen: list[dict[str, Any]] = []
    failures: list[str] = []
    proposals: set[str] = set()
    for row in c5_rows:
        if row.get("c5_status") != STRICT:
            continue
        packet_id = str(row["review_packet_id"])
        key = key_by_packet.get(packet_id)
        if key is None:
            failures.append(f"missing_c4_key:{packet_id}")
            continue
        proposal_id = str(row.get("proposal_id"))
        c1 = c1_by_proposal.get(proposal_id)
        if c1 is None or c1.get("c1_status") != "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT":
            failures.append(f"missing_c1_pass:{proposal_id}")
            continue
        cards = key.get("card_key", [])
        candidate_ids = [str(card.get("skill_id")) for card in cards]
        hashes = [str(card.get("source_sha256")) for card in cards]
        if set(candidate_ids) != set(map(str, c1.get("candidate_skill_ids", []))):
            failures.append(f"candidate_set_mismatch:{packet_id}")
            continue
        if set(hashes) != set(map(str, c1.get("candidate_source_sha256", []))):
            failures.append(f"hash_set_mismatch:{packet_id}")
            continue
        for candidate_id in candidate_ids:
            prior = owner_by_candidate.setdefault(candidate_id, proposal_id)
            if prior != proposal_id:
                failures.append(f"cross_proposal_candidate_reuse:{candidate_id}:{prior}:{proposal_id}")
        target = str(row.get("strict_gold_skill_id"))
        if target != str(key.get("intended_candidate_skill_id_sealed")):
            failures.append(f"c5_key_target_mismatch:{packet_id}")
            continue
        manual = c3_manual.get((proposal_id, target, str(key.get("prompt_variant"))))
        if manual is None:
            failures.append(f"missing_c3_manual_disposition:{packet_id}")
            continue
        # A reworded record has passed the final literal C3 audit; it retains the
        # rewrite history rather than being relabelled as originally allowed.
        if manual.get("c3_disposition") not in C3_SAFE_DISPOSITIONS:
            failures.append(f"invalid_c3_manual_disposition:{packet_id}:{manual.get('c3_disposition')}")
            continue
        frozen.append({
            "c6_status": "C6_FROZEN_PRIMARY_STRICT_PACKET_NOT_A_RETRIEVAL_OR_RESULT",
            "review_packet_id": packet_id,
            "proposal_id": proposal_id,
            "prompt_variant": key.get("prompt_variant"),
            "strict_gold_skill_id": target,
            "candidate_skill_ids": candidate_ids,
            "candidate_source_sha256": hashes,
            "origin_count": c1.get("origin_count"),
            "c3_status": c3.get("status"),
            "c3_manual_disposition": manual.get("c3_disposition"),
            "residual_cue_risk": manual.get("residual_cue_risk"),
            "c4_c5_chain": "two_model_assisted_blind_reviewers_exact_singleton_agreement_then_sealed_target_check",
            "exclusions": ["not a retrieval input", "not a model result", "not a metric", "not downstream task success"],
        })
        proposals.add(proposal_id)

    summary = {
        "status": "C6_FREEZE_PASS_NOT_A_RETRIEVAL_OR_RESULT" if not failures else "C6_FREEZE_FAILED_NOT_A_RESULT",
        "frozen_primary_prompt_packet_count": len(frozen),
        "frozen_candidate_composition_count": len(proposals),
        "exploratory_acceptable_set_prompt_count": sum(row.get("c5_status") == EXPLORATORY for row in c5_rows),
        "unresolved_c5_disagreement_prompt_count": sum(row.get("c5_status") == UNRESOLVED for row in c5_rows),
        "unexpected_nonprimary_c5_prompt_count": sum(row.get("c5_status") not in {STRICT, EXPLORATORY, UNRESOLVED} for row in c5_rows),
        "failures": sorted(set(failures)),
        "exclusions": ["A frozen packet is a curation artefact. No retrieval or representation result has been run."],
    }
    write_jsonl(args.output, frozen)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
