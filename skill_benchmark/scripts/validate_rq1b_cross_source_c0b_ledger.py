#!/usr/bin/env python3
"""Validate a C0B cross-source ledger against its exact-source packet manifests.

This local-only guard checks JSONL shape, proposal/candidate identity alignment,
and that every quoted evidence substring is literal source text in the matching
packet original. It does not make prompts, labels, retrieval inputs, model calls,
metrics, or benchmark clusters.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_STATUSES = {
    "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT",
    "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise SystemExit(f"json_parse_error:{path}:{line_number}:{error.msg}") from error
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--packet-manifest", type=Path, action="append", required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    packet_by_proposal: dict[str, dict[str, dict[str, Any]]] = {}
    failures: list[str] = []
    for packet_manifest in args.packet_manifest:
        for packet in read_jsonl(packet_manifest):
            proposal_id = str(packet.get("proposal_id", ""))
            skill_id = str(packet.get("skill_id", ""))
            if not proposal_id or not skill_id:
                failures.append(f"packet_identity_missing:{packet_manifest}")
                continue
            proposal_packets = packet_by_proposal.setdefault(proposal_id, {})
            if skill_id in proposal_packets:
                failures.append(f"duplicate_packet_candidate:{proposal_id}:{skill_id}")
            proposal_packets[skill_id] = packet

    rows = read_jsonl(args.ledger)
    seen_proposals: set[str] = set()
    exact_evidence_count = 0
    statuses: dict[str, int] = {status: 0 for status in VALID_STATUSES}
    for row in rows:
        proposal_id = str(row.get("proposal_id", ""))
        if not proposal_id or proposal_id in seen_proposals:
            failures.append(f"duplicate_or_missing_proposal:{proposal_id or '<missing>'}")
            continue
        seen_proposals.add(proposal_id)
        status = row.get("c0b_status")
        if status not in VALID_STATUSES:
            failures.append(f"invalid_status:{proposal_id}:{status}")
        else:
            statuses[status] += 1
        candidates = [str(value) for value in row.get("candidate_skill_ids", [])]
        evidence_rows = row.get("candidate_evidence", [])
        packet_candidates = packet_by_proposal.get(proposal_id, {})
        if set(candidates) != set(packet_candidates):
            failures.append(f"candidate_alignment:{proposal_id}")
        if {str(item.get("skill_id", "")) for item in evidence_rows} != set(candidates):
            failures.append(f"evidence_identity_alignment:{proposal_id}")
        for item in evidence_rows:
            skill_id = str(item.get("skill_id", ""))
            packet = packet_candidates.get(skill_id)
            if packet is None:
                continue
            original = Path(str(packet.get("packet_original_path", "")))
            if not original.is_file():
                failures.append(f"packet_original_missing:{proposal_id}:{skill_id}")
                continue
            source = original.read_text(encoding="utf-8")
            substrings = item.get("evidence_substrings", [])
            if not substrings:
                failures.append(f"evidence_missing:{proposal_id}:{skill_id}")
            for index, substring in enumerate(substrings):
                if not isinstance(substring, str) or not substring:
                    failures.append(f"invalid_evidence:{proposal_id}:{skill_id}:{index}")
                elif substring not in source:
                    failures.append(f"nonliteral_evidence:{proposal_id}:{skill_id}:{index}")
                else:
                    exact_evidence_count += 1

    unexpected_packets = sorted(set(packet_by_proposal) - seen_proposals)
    failures.extend(f"unrepresented_packet_proposal:{proposal_id}" for proposal_id in unexpected_packets)
    summary = {
        "status": "C0B_LEDGER_VALID_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0B_LEDGER_INVALID_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "ledger_rows": len(rows),
        "source_backed_drafts": statuses["C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT"],
        "structural_rejects": statuses["C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT"],
        "exact_evidence_substrings": exact_evidence_count,
        "exact_evidence_substrings_verified": exact_evidence_count if not failures else 0,
        "failures": failures,
        "exclusions": [
            "No prompt, label, acceptable set, retrieval input, model call, metric, or benchmark cluster was created."
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
