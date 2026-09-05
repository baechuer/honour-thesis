#!/usr/bin/env python3
"""Build target-blinded packets for a structured RQ1 re-review batch.

The batch review file must contain source-only dispositions and the private
authoring file one prompt per promoted candidate.  Intended targets and skill
IDs are omitted from packets.  No label or admission is produced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, required=True, choices=range(2, 1000))
    args = parser.parse_args()
    batch = args.batch
    token = f"{batch:03d}"
    decisions_path = BASE / f"review/rq1_frozen_cluster_re_review_batch_{token}_2026-08-31.jsonl"
    authors_path = BASE / f"prompts/rq1_frozen_cluster_reauthored_batch_{token}_private_2026-08-31.jsonl"
    packets_path = BASE / f"review/rq1_frozen_cluster_reauthored_batch_{token}_target_blinded_packets_2026-08-31.jsonl"
    summary_path = BASE / f"review/rq1_frozen_cluster_reauthored_batch_{token}_packet_summary_2026-08-31.json"
    if not decisions_path.is_file() or not authors_path.is_file():
        raise SystemExit(f"Missing batch inputs: {decisions_path}, {authors_path}")

    decisions = read_jsonl(decisions_path)
    authors = read_jsonl(authors_path)
    expected_decisions = 19 if batch == 4 else 20
    if len(decisions) != expected_decisions:
        raise SystemExit(f"Expected {expected_decisions} source-only decisions, found {len(decisions)}")
    promoted = {
        str(row["review_queue_id"]): row
        for row in decisions
        if row["disposition"] in {"PROMOTE", "PROMOTE_TO_RQ2_PROMPT_AUTHORING"}
    }
    expected_prompts = sum(int(row["candidate_cardinality"]) for row in promoted.values())
    if len(authors) != expected_prompts:
        raise SystemExit(f"Expected {expected_prompts} prompts for {len(promoted)} clusters, found {len(authors)}")

    rosters: dict[str, list[dict[str, str]]] = {}
    for queue_id, decision in promoted.items():
        roster: list[dict[str, str]] = []
        for boundary in decision["necessary_candidate_boundaries"]:
            evidence = boundary["source_evidence"]
            source_path = Path(str(evidence["source_path"]))
            if not source_path.is_file() or sha256_file(source_path) != str(evidence["source_sha256"]):
                raise SystemExit(f"Source replay failed: {source_path}")
            roster.append({"source_path": str(source_path), "source_sha256": str(evidence["source_sha256"])})
        if len(roster) != int(decision["candidate_cardinality"]):
            raise SystemExit(f"Candidate cardinality mismatch: {queue_id}")
        rosters[queue_id] = roster

    packet_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, author in enumerate(authors):
        prompt_id = str(author["prompt_id"])
        queue_id = str(author["review_queue_id"])
        if prompt_id in seen or queue_id not in promoted:
            raise SystemExit(f"Duplicate prompt or non-promoted queue: {prompt_id}/{queue_id}")
        seen.add(prompt_id)
        roster = list(rosters[queue_id])
        intended = str(author["author_intended_candidate_source_sha256"])
        if intended not in {row["source_sha256"] for row in roster}:
            raise SystemExit(f"Private author target absent from roster: {prompt_id}")
        rotation = (index + int(promoted[queue_id]["review_order"])) % len(roster)
        rotated = roster[rotation:] + roster[:rotation]
        packet_rows.append({
            "packet_id": f"RQ2B-NC-TARGET-BLIND-{prompt_id}",
            "prompt_id": prompt_id,
            "review_queue_id": queue_id,
            "parent_rq1_cluster_id": author["parent_rq1_cluster_id"],
            "family_id": author.get("family_id"),
            "prompt": author["prompt"],
            "candidates": [
                {"alias": chr(ord("A") + alias_index), **row}
                for alias_index, row in enumerate(rotated)
            ],
            "reviewer_instruction": (
                "Read each preserved source independently. The author target is withheld. Classify every "
                "candidate as fully_adequate, partially_adequate, inadequate, or unclear; identify "
                "necessary-versus-gratuitous cueing, source-description echo, hierarchy, subsumption, "
                "workflow composition, and multi-acceptable risk. Do not infer or request the intended "
                "target. Do not consult any RQ1 prompt, gold/acceptable label, cluster card, field card, "
                "selector output, or metric."
            ),
            "status": "TARGET_BLINDED_REVIEW_INPUT_NOT_A_LABEL_OR_RESULT",
        })

    write_jsonl(packets_path, packet_rows)
    summary = {
        "status": f"PASS_RQ1_REVIEW_BATCH_{token}_PACKETISATION_NOT_A_LABEL_OR_ADMISSION",
        "source_only_decision_count": len(decisions),
        "promoted_cluster_count": len(promoted),
        "target_blinded_packet_count": len(packet_rows),
        "candidate_judgment_slot_count": sum(len(row["candidates"]) for row in packet_rows),
        "input_sha256": {
            str(decisions_path.relative_to(ROOT)): sha256_file(decisions_path),
            str(authors_path.relative_to(ROOT)): sha256_file(authors_path),
        },
        "artifacts": {str(packets_path.relative_to(ROOT)): sha256_file(packets_path)},
        "claim_boundary": [
            "The packet withholds each author-intended target but exposes full candidate source identities.",
            "This is target-blinded, candidate-identity-visible model-assisted curation input.",
            "No RQ1 prompt or label is transferred and no prompt, cluster, or gold label is admitted."
        ],
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
