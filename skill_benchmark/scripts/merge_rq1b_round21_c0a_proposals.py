#!/usr/bin/env python3
"""Merge and structurally validate Round 21 C0A navigation proposals.

C0A is a source-navigation sort. This checker deliberately validates only
proposal mechanics against the frozen source-only pool; it does not inspect
original bodies, score semantic similarity, decide peerhood, or form a valid
cluster. C0B remains the full-source structural gate.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_POOL_STATUS = "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT"
PROPOSAL_STATUS = "C0A_PROPOSAL_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-pool", type=Path, required=True)
    parser.add_argument("--proposal-input", action="append", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pool_rows = read_jsonl(args.source_pool.resolve())
    pool = {
        str(row["skill_id"]): row
        for row in pool_rows
        if row.get("c0_pool_status") == SOURCE_POOL_STATUS
    }
    if not pool:
        raise SystemExit("No valid source-only pool rows")

    accepted: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []
    proposal_ids: set[str] = set()
    candidate_owner: dict[str, str] = {}
    for input_path in args.proposal_input:
        resolved = input_path.resolve()
        for line_number, proposal in enumerate(read_jsonl(resolved), 1):
            errors: list[str] = []
            proposal_id = str(proposal.get("proposal_id", ""))
            candidate_ids = proposal.get("candidate_skill_ids")
            if proposal.get("status") != PROPOSAL_STATUS:
                errors.append("unexpected_status")
            if proposal.get("candidate_source_evidence") or proposal.get("candidate_local_original_paths"):
                errors.append("c0a_source_body_overflow")
            if not proposal_id:
                errors.append("missing_proposal_id")
            elif proposal_id in proposal_ids:
                errors.append("duplicate_proposal_id")
            if not isinstance(candidate_ids, list) or len(candidate_ids) not in (3, 4):
                errors.append("candidate_count_not_3_or_4")
                candidate_ids = []
            elif len({str(value) for value in candidate_ids}) != len(candidate_ids):
                errors.append("duplicate_candidate_id")
            unknown = [str(value) for value in candidate_ids if str(value) not in pool]
            if unknown:
                errors.append("unknown_candidate_id")
            origins = {
                str(pool[str(value)]["origin"])
                for value in candidate_ids
                if str(value) in pool
            }
            if len(origins) != len(candidate_ids):
                errors.append("origins_not_unique_per_candidate")
            reported_origins = proposal.get("candidate_origins")
            if isinstance(reported_origins, list) and set(str(value) for value in reported_origins) != origins:
                errors.append("reported_origin_mismatch")
            contexts = [
                {
                    "skill_id": str(value),
                    "source_name": pool[str(value)].get("source_name"),
                    "source_description_preview": pool[str(value)].get("source_description_preview"),
                    "source_heading_preview": pool[str(value)].get("source_heading_preview"),
                    "status": "TENTATIVE_NAVIGATION_METADATA_ONLY",
                }
                for value in candidate_ids
                if str(value) in pool
            ]
            if len(contexts) != len(candidate_ids):
                errors.append("cannot_materialize_navigation_context")
            if not isinstance(proposal.get("tentative_shared_envelope"), str) or not proposal["tentative_shared_envelope"].strip():
                errors.append("missing_shared_envelope")
            risks = proposal.get("c0b_risks")
            if isinstance(risks, dict):
                risks = [str(value) for value in risks.values() if str(value).strip()]
            if not isinstance(risks, list) or not risks:
                errors.append("missing_c0b_risks")
                risks = []
            reused = [str(value) for value in candidate_ids if candidate_owner.get(str(value)) not in (None, proposal_id)]
            if reused:
                errors.append("candidate_reused_across_proposals")
            record = {
                "proposal_id": proposal_id,
                "status": PROPOSAL_STATUS,
                "candidate_skill_ids": [str(value) for value in candidate_ids],
                "origin_count": len(origins),
                "candidate_origins": [str(pool[str(value)]["origin"]) for value in candidate_ids if str(value) in pool],
                "tentative_shared_envelope": proposal.get("tentative_shared_envelope"),
                "operational_contexts": contexts,
                "c0b_risks": risks,
                "source_pool_path": str(args.source_pool),
                "c0a_structural_validation": "C0A_STRUCTURALLY_VALID_NOT_A_CLUSTER_OR_RESULT" if not errors else "C0A_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT",
                "c0a_structural_errors": errors,
                "proposal_source_file": str(resolved),
                "proposal_source_line": line_number,
            }
            if errors:
                rejects.append(record)
            else:
                proposal_ids.add(proposal_id)
                for skill_id in candidate_ids:
                    candidate_owner[str(skill_id)] = proposal_id
                accepted.append(record)

    accepted.sort(key=lambda row: str(row["proposal_id"]))
    rejects.sort(key=lambda row: (str(row.get("proposal_source_file")), int(row.get("proposal_source_line", 0))))
    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    args.output_jsonl.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in accepted),
        encoding="utf-8",
    )
    summary = {
        "status": "C0A_ROUND21_MERGED_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT",
        "source_pool_count": len(pool),
        "input_file_count": len(args.proposal_input),
        "structurally_valid_proposal_count": len(accepted),
        "structurally_rejected_proposal_count": len(rejects),
        "structural_reject_reasons": dict(sorted(Counter(error for row in rejects for error in row["c0a_structural_errors"]).items())),
        "rejected_proposals": rejects,
        "exclusions": [
            "Validation does not inspect source bodies or determine whether candidates are operational peers.",
            "No prompt, label, acceptable set, retrieval score, model call, or empirical result was created.",
            "Only C0B may use literal source evidence to retain a source-backed draft.",
        ],
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "structurally_valid_proposal_count", "structurally_rejected_proposal_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
