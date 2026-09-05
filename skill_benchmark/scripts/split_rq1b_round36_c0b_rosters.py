#!/usr/bin/env python3
"""Create disjoint Round 36 source-only C0B rosters from exact packets."""

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
    if args.max_proposals_per_roster < 1:
        raise SystemExit("invalid_max_proposals_per_roster")
    packets: dict[str, dict[str, dict[str, Any]]] = {}
    for packet in read_jsonl(args.packet_manifest):
        proposal_id, skill_id = str(packet.get("proposal_id", "")), str(packet.get("skill_id", ""))
        if not proposal_id or not skill_id or skill_id in packets.setdefault(proposal_id, {}):
            raise SystemExit("invalid_or_duplicate_packet_identity")
        packets[proposal_id][skill_id] = packet
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for proposal in sorted(read_jsonl(args.queue), key=lambda row: str(row.get("proposal_id", ""))):
        proposal_id = str(proposal.get("proposal_id", ""))
        candidates = [str(item.get("skill_id", "")) for item in proposal.get("candidates", [])]
        if not proposal_id or len(candidates) not in (3, 4) or len(candidates) != len(set(candidates)) or set(candidates) != set(packets.get(proposal_id, {})):
            failures.append(f"proposal_packet_alignment:{proposal_id}")
            continue
        overlap = sorted(set(candidates) & seen)
        if overlap:
            failures.append(f"candidate_reuse:{proposal_id}:{','.join(overlap)}")
            continue
        rows.append({"c0b_roster_status": "C0B_SOURCE_REVIEW_ROSTER_NOT_A_CLUSTER_OR_RESULT", "proposal_id": proposal_id, "candidate_skill_ids": candidates, "candidates": [{"skill_id": skill_id, "origin": packets[proposal_id][skill_id]["origin"], "pinned_commit": packets[proposal_id][skill_id]["pinned_commit"], "source_repository_path": packets[proposal_id][skill_id]["source_repository_path"], "source_sha256": packets[proposal_id][skill_id]["source_sha256"], "packet_original_path": packets[proposal_id][skill_id]["packet_original_path"]} for skill_id in candidates], "exclusions": ["No C0A envelope/risk, prompt, gold label, acceptable set, retrieval input, model call, metric, or result is supplied."]})
        seen.update(candidates)
    rosters = [rows[index:index + args.max_proposals_per_roster] for index in range(0, len(rows), args.max_proposals_per_roster)]
    args.output_directory.mkdir(parents=True, exist_ok=True)
    outputs = []
    for index, roster in enumerate(rosters, 1):
        output = args.output_directory / f"c0b_round36_group_{index:02d}_source_roster_2026-08-28.jsonl"
        output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in roster), encoding="utf-8")
        outputs.append(str(output))
    summary = {"status": "C0B_ROUND36_ROSTERS_READY_SOURCE_ONLY_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0B_ROUND36_ROSTERS_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT", "queue_proposal_count": len(rows), "roster_count": len(rosters), "roster_sizes": [len(roster) for roster in rosters], "candidate_count": len(seen), "outputs": outputs, "failures": failures, "exclusions": ["C0B reviewers receive only protocol, candidate membership/provenance, and exact packet originals.", "No C0B decision, prompt, label, acceptable set, retrieval input, model call, metric, or result was created."]}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "queue_proposal_count", "roster_count", "candidate_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
