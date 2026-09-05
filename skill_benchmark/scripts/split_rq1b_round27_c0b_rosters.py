#!/usr/bin/env python3
"""Create disjoint, source-only Round 27 C0B reviewer rosters.

Each roster contains only protocol-independent membership, provenance, and the
packet-original path. It deliberately omits C0A envelopes and risks, prompts,
labels, and all prior review or result material.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--packet-manifest", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--max-proposals-per-roster", type=int, default=3)
    args = parser.parse_args()
    if args.max_proposals_per_roster <= 0:
        raise SystemExit("max_proposals_per_roster_must_be_positive")

    packets: dict[str, dict[str, dict[str, Any]]] = {}
    for packet in read_jsonl(args.packet_manifest):
        proposal_id, skill_id = str(packet.get("proposal_id", "")), str(packet.get("skill_id", ""))
        if not proposal_id or not skill_id or skill_id in packets.setdefault(proposal_id, {}):
            raise SystemExit("invalid_or_duplicate_packet_identity")
        packets[proposal_id][skill_id] = packet

    failures: list[str] = []
    rows: list[dict[str, Any]] = []
    seen_candidates: set[str] = set()
    for proposal in sorted(read_jsonl(args.queue), key=lambda row: str(row.get("proposal_id", ""))):
        proposal_id = str(proposal.get("proposal_id", ""))
        candidate_ids = [str(item.get("skill_id", "")) for item in proposal.get("candidates", [])]
        if not proposal_id or len(candidate_ids) not in (3, 4) or len(set(candidate_ids)) != len(candidate_ids):
            failures.append(f"invalid_queue_proposal:{proposal_id}")
            continue
        if set(candidate_ids) != set(packets.get(proposal_id, {})):
            failures.append(f"packet_alignment:{proposal_id}")
            continue
        overlap = sorted(set(candidate_ids) & seen_candidates)
        if overlap:
            failures.append(f"candidate_reuse:{proposal_id}:{','.join(overlap)}")
            continue
        rows.append({
            "c0b_roster_status": "C0B_SOURCE_REVIEW_ROSTER_NOT_A_CLUSTER_OR_RESULT",
            "proposal_id": proposal_id,
            "candidate_skill_ids": candidate_ids,
            "candidates": [
                {
                    "skill_id": skill_id,
                    "origin": packets[proposal_id][skill_id]["origin"],
                    "pinned_commit": packets[proposal_id][skill_id]["pinned_commit"],
                    "source_repository_path": packets[proposal_id][skill_id]["source_repository_path"],
                    "source_sha256": packets[proposal_id][skill_id]["source_sha256"],
                    "packet_original_path": packets[proposal_id][skill_id]["packet_original_path"],
                }
                for skill_id in candidate_ids
            ],
            "exclusions": [
                "No C0A envelope or risk is supplied to the reviewer.",
                "No prompt, gold label, acceptable set, retrieval input, model call, metric, or result exists.",
            ],
        })
        seen_candidates.update(candidate_ids)

    rosters = [rows[index:index + args.max_proposals_per_roster] for index in range(0, len(rows), args.max_proposals_per_roster)]
    args.output_directory.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    for index, roster in enumerate(rosters, 1):
        output = args.output_directory / f"c0b_round27_group_{index:02d}_source_roster_2026-08-28.jsonl"
        output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in roster), encoding="utf-8")
        outputs.append(str(output))
    summary = {
        "status": "C0B_ROUND27_ROSTERS_READY_SOURCE_ONLY_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0B_ROUND27_ROSTERS_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "queue_proposal_count": len(rows),
        "roster_count": len(rosters),
        "roster_sizes": [len(roster) for roster in rosters],
        "candidate_count": len(seen_candidates),
        "outputs": outputs,
        "failures": failures,
        "exclusions": [
            "C0B reviewers receive only protocol, candidate membership/provenance, and exact packet originals.",
            "No C0B decision, prompt, label, acceptable set, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "queue_proposal_count", "roster_count", "candidate_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
