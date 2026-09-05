#!/usr/bin/env python3
"""Audit C1 integrity and composition for C0B cross-source source drafts.

This local-only audit rechecks source hashes, origin diversity, candidate hash
uniqueness, and candidate reuse. It does not create prompts, labels,
acceptable sets, retrieval inputs, models calls, metrics, or benchmark results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


PASS = "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, action="append", required=True)
    parser.add_argument("--queue", type=Path, action="append", required=True)
    parser.add_argument(
        "--reserved-candidate-manifest",
        type=Path,
        action="append",
        default=[],
        help="C6-frozen candidate manifests whose ids may not be reused.",
    )
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    draft_ids: set[str] = set()
    for path in args.ledger:
        for row in read_jsonl(path):
            if row.get("c0b_status", row.get("status")) == PASS:
                draft_ids.add(str(row["proposal_id"]))

    queue_by_id: dict[str, dict[str, Any]] = {}
    for path in args.queue:
        for row in read_jsonl(path):
            proposal_id = str(row.get("proposal_id", ""))
            if proposal_id in queue_by_id:
                raise SystemExit(f"duplicate_queue_proposal:{proposal_id}")
            queue_by_id[proposal_id] = row

    missing = sorted(draft_ids - set(queue_by_id))
    failures: list[str] = [f"missing_queue_proposal:{proposal_id}" for proposal_id in missing]
    records: list[dict[str, Any]] = []
    candidate_use: Counter[str] = Counter()
    reserved_candidates: set[str] = set()
    for path in args.reserved_candidate_manifest:
        for row in read_jsonl(path):
            reserved_candidates.update(
                str(skill_id) for skill_id in row.get("candidate_skill_ids", [])
            )

    for proposal_id in sorted(draft_ids):
        proposal = queue_by_id.get(proposal_id)
        if proposal is None:
            continue
        candidates = proposal.get("candidates", [])
        candidate_failures: list[str] = []
        origins = {str(candidate.get("origin")) for candidate in candidates if candidate.get("origin")}
        hashes = [str(candidate.get("source_sha256")) for candidate in candidates]
        for candidate in candidates:
            skill_id = str(candidate.get("skill_id", ""))
            candidate_use[skill_id] += 1
            if skill_id in reserved_candidates:
                candidate_failures.append(f"candidate_reuse_frozen:{skill_id}")
            source = Path(str(candidate.get("local_original_path", "")))
            expected = str(candidate.get("source_sha256", ""))
            if not skill_id or not expected or not source.is_file():
                candidate_failures.append(f"missing_source:{skill_id}")
            elif sha256(source) != expected:
                candidate_failures.append(f"source_hash_drift:{skill_id}")
        if not 3 <= len(candidates) <= 4:
            candidate_failures.append(f"candidate_count:{len(candidates)}")
        if len(origins) < 2:
            candidate_failures.append(f"origin_count:{len(origins)}")
        if len(set(hashes)) != len(hashes):
            candidate_failures.append("duplicate_candidate_source_hash")
        status = "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT" if not candidate_failures else "C1_INTEGRITY_FAIL_NOT_A_CLUSTER_OR_RESULT"
        failures.extend(f"{proposal_id}:{failure}" for failure in candidate_failures)
        records.append(
            {
                "c1_status": status,
                "proposal_id": proposal_id,
                "candidate_count": len(candidates),
                "origin_count": len(origins),
                "candidate_skill_ids": [candidate.get("skill_id") for candidate in candidates],
                "candidate_source_sha256": hashes,
                "integrity_failures": candidate_failures,
                "exclusions": [
                    "No prompt, label, acceptable set, retrieval input, model call, metric, or benchmark cluster was created.",
                ],
            }
        )

    duplicate_uses = sorted(skill_id for skill_id, count in candidate_use.items() if count > 1)
    if duplicate_uses:
        failures.extend(f"candidate_reuse:{skill_id}" for skill_id in duplicate_uses)
        for record in records:
            reused = sorted(set(record["candidate_skill_ids"]) & set(duplicate_uses))
            if reused:
                record["integrity_failures"].extend(f"candidate_reuse:{skill_id}" for skill_id in reused)
                record["c1_status"] = "C1_INTEGRITY_FAIL_NOT_A_CLUSTER_OR_RESULT"

    records.sort(key=lambda row: row["proposal_id"])
    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    args.output_jsonl.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    summary = {
        "status": "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT" if not failures else "C1_INTEGRITY_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "draft_count": len(draft_ids),
        "c1_pass_count": sum(record["c1_status"] == "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT" for record in records),
        "candidate_reuse": duplicate_uses,
        "reserved_candidate_count": len(reserved_candidates),
        "failures": failures,
        "exclusions": [
            "C1 integrity does not establish prompt quality, strict singleton validity, an acceptable set, a frozen cluster, or empirical performance.",
        ],
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "draft_count", "c1_pass_count", "candidate_reuse", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
