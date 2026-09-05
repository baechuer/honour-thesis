#!/usr/bin/env python3
"""Enrich source-agnostic RQ1b C0A proposals into a read-only C0B queue.

This copies provenance records from the admitted source pool. It does not read
candidate bodies, assess semantic fitness, draft prompts, create labels, or
produce a benchmark result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c0a", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pool = {str(row["skill_id"]): row for row in read_jsonl(args.pool)}
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    seen_candidates: dict[str, str] = {}
    for proposal in read_jsonl(args.c0a):
        if proposal.get("status") != "C0A_PROPOSAL_NOT_A_CLUSTER_OR_RESULT":
            continue
        proposal_id = str(proposal["proposal_id"])
        candidate_ids = [str(value) for value in proposal.get("candidate_skill_ids", [])]
        if not 3 <= len(candidate_ids) <= 4 or len(set(candidate_ids)) != len(candidate_ids):
            failures.append(f"candidate_count_or_duplicate:{proposal_id}")
            continue
        candidates: list[dict[str, Any]] = []
        for skill_id in candidate_ids:
            source = pool.get(skill_id)
            if source is None:
                failures.append(f"missing_pool_skill:{proposal_id}:{skill_id}")
                continue
            prior = seen_candidates.setdefault(skill_id, proposal_id)
            if prior != proposal_id:
                failures.append(f"proposal_candidate_reuse:{skill_id}:{prior}:{proposal_id}")
            candidates.append({
                "skill_id": skill_id,
                "origin": source["origin"],
                "repository_url": source["repository_url"],
                "pinned_commit": source["pinned_commit"],
                "source_repository_path": source["source_repository_path"],
                "local_original_path": source["local_original_path"],
                "source_sha256": source["source_sha256"],
                "license": source["license"],
                "license_status": source.get(
                    "license_status", "DECLARED_REPOSITORY_LICENSE"
                ),
            })
        if len(candidates) != len(candidate_ids):
            continue
        if len({candidate["origin"] for candidate in candidates}) < 2:
            failures.append(f"insufficient_origin_count:{proposal_id}")
            continue
        rows.append({
            "c0b_queue_status": "C0B_QUEUE_SOURCE_SCREEN_ONLY_NOT_A_CLUSTER_OR_RESULT",
            "proposal_id": proposal_id,
            "domain": proposal.get("domain"),
            "tentative_shared_envelope": proposal.get("tentative_shared_envelope"),
            "operational_contexts": proposal.get("operational_contexts"),
            "c0b_risks": proposal.get("c0b_risks"),
            "c0a_curation_basis": proposal.get("curation_basis"),
            "candidates": candidates,
            "exclusions": ["no source-content claim", "no prompt", "no label", "no acceptable set", "no retrieval/model result"],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True) + "\n" for row in rows), encoding="utf-8")
    print(json.dumps({"queue_count": len(rows), "failures": failures, "status": "C0B_QUEUE_PASS_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0B_QUEUE_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT"}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
