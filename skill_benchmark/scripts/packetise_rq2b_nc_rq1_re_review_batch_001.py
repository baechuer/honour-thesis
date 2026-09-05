#!/usr/bin/env python3
"""Build target-blinded review packets for RQ1 re-review batch 001.

The inputs are a source-only cluster disposition ledger and private prompt
authoring rows.  Intended targets and candidate skill IDs are omitted from the
review packets.  No cluster, prompt, or label is admitted by this script.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "rq2b_naturalistic_confusability/review/rq1_frozen_cluster_re_review_batch_001_2026-08-31.jsonl"
AUTHORS = ROOT / "rq2b_naturalistic_confusability/prompts/rq1_frozen_cluster_reauthored_batch_001_private_2026-08-31.jsonl"
PACKETS = ROOT / "rq2b_naturalistic_confusability/review/rq1_frozen_cluster_reauthored_batch_001_target_blinded_packets_2026-08-31.jsonl"
SUMMARY = ROOT / "rq2b_naturalistic_confusability/review/rq1_frozen_cluster_reauthored_batch_001_packet_summary_2026-08-31.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    decisions = read_jsonl(DECISIONS)
    authors = read_jsonl(AUTHORS)
    if len(decisions) != 20:
        raise SystemExit(f"Expected 20 review decisions, found {len(decisions)}")
    promoted = {
        row["review_queue_id"]: row
        for row in decisions
        if row["disposition"] == "PROMOTE_TO_RQ2_PROMPT_AUTHORING"
    }
    if len(promoted) != 10 or len(authors) != 20:
        raise SystemExit(f"Expected 10 promoted clusters and 20 prompts, found {len(promoted)}/{len(authors)}")

    source_rosters: dict[str, list[dict[str, str]]] = {}
    for queue_id, decision in promoted.items():
        roster: list[dict[str, str]] = []
        for item in decision["necessary_candidate_boundaries"]:
            evidence = item["source_evidence"]
            source_path = Path(evidence["source_path"])
            if not source_path.is_file():
                raise SystemExit(f"Missing source: {source_path}")
            if sha256_file(source_path) != evidence["source_sha256"]:
                raise SystemExit(f"Source hash mismatch: {source_path}")
            roster.append({
                "source_sha256": evidence["source_sha256"],
                "source_path": evidence["source_path"],
            })
        if len({row["source_sha256"] for row in roster}) != len(roster):
            raise SystemExit(f"Duplicate source within {queue_id}")
        source_rosters[queue_id] = roster

    packet_rows: list[dict[str, Any]] = []
    seen_prompt_ids: set[str] = set()
    for prompt_index, author in enumerate(authors):
        prompt_id = author["prompt_id"]
        queue_id = author["review_queue_id"]
        if prompt_id in seen_prompt_ids:
            raise SystemExit(f"Duplicate prompt ID: {prompt_id}")
        seen_prompt_ids.add(prompt_id)
        if queue_id not in promoted:
            raise SystemExit(f"Author prompt refers to non-promoted queue: {queue_id}")
        roster = list(source_rosters[queue_id])
        intended = author["author_intended_candidate_source_sha256"]
        if intended not in {row["source_sha256"] for row in roster}:
            raise SystemExit(f"Intended source absent from {queue_id}: {intended}")
        rotation = (prompt_index + int(promoted[queue_id]["review_order"])) % len(roster)
        rotated = roster[rotation:] + roster[:rotation]
        packet_rows.append({
            "packet_id": f"RQ2B-NC-TARGET-BLIND-{prompt_id}",
            "prompt_id": prompt_id,
            "review_queue_id": queue_id,
            "parent_rq1_cluster_id": author["parent_rq1_cluster_id"],
            "family_id": author["family_id"],
            "prompt": author["prompt"],
            "candidates": [
                {
                    "alias": chr(ord("A") + alias_index),
                    "source_sha256": item["source_sha256"],
                    "source_path": item["source_path"],
                }
                for alias_index, item in enumerate(rotated)
            ],
            "reviewer_instruction": (
                "Read each preserved source independently. The author target is withheld. Classify every "
                "candidate as fully_adequate, partially_adequate, inadequate, or unclear; identify "
                "necessary-versus-gratuitous cueing, hierarchy, subsumption, workflow composition, and "
                "multi-acceptable risk. Do not infer or request the intended target. Do not consult any "
                "RQ1 prompt, gold/acceptable label, cluster card, field card, selector output, or metric."
            ),
            "status": "TARGET_BLINDED_REVIEW_INPUT_NOT_A_LABEL_OR_RESULT",
        })

    write_jsonl(PACKETS, packet_rows)
    summary = {
        "status": "PASS_RQ1_REVIEW_BATCH_001_PACKETISATION_NOT_A_LABEL_OR_ADMISSION",
        "source_only_decision_count": len(decisions),
        "promoted_cluster_count": len(promoted),
        "target_blinded_packet_count": len(packet_rows),
        "candidate_judgment_slot_count": sum(len(row["candidates"]) for row in packet_rows),
        "input_sha256": {
            str(DECISIONS.relative_to(ROOT)): sha256_file(DECISIONS),
            str(AUTHORS.relative_to(ROOT)): sha256_file(AUTHORS),
        },
        "artifacts": {str(PACKETS.relative_to(ROOT)): sha256_file(PACKETS)},
        "claim_boundary": [
            "The packet withholds each author-intended candidate but exposes complete candidate source identities.",
            "This is target-blinded, not candidate-identity-blinded, model-assisted curation input.",
            "No RQ1 prompt or label is transferred and no prompt, cluster, or gold label is admitted.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
