#!/usr/bin/env python3
"""Materialise exact, checksum-verified Round 39 C0B source packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c0a", type=Path, required=True)
    parser.add_argument("--source-pool", type=Path, required=True)
    parser.add_argument("--packet-directory", type=Path, required=True)
    parser.add_argument("--queue-output", type=Path, required=True)
    parser.add_argument("--packet-manifest", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    pool = {str(row["skill_id"]): row for row in read_jsonl(args.source_pool)}
    proposals = read_jsonl(args.c0a)
    packet_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    seen_candidates: set[str] = set()
    args.packet_directory.mkdir(parents=True, exist_ok=True)

    for proposal in proposals:
        proposal_id = str(proposal.get("proposal_id", ""))
        candidate_ids = [str(value) for value in proposal.get("candidate_skill_ids", [])]
        if not proposal_id or len(candidate_ids) not in (3, 4) or len(set(candidate_ids)) != len(candidate_ids):
            failures.append(f"invalid_proposal:{proposal_id}")
            continue
        unknown = [skill_id for skill_id in candidate_ids if skill_id not in pool]
        reused = sorted(set(candidate_ids) & seen_candidates)
        if unknown or reused:
            failures.extend(f"unknown_candidate:{proposal_id}:{skill_id}" for skill_id in unknown)
            failures.extend(f"candidate_reuse:{proposal_id}:{skill_id}" for skill_id in reused)
            continue
        candidates: list[dict[str, Any]] = []
        for skill_id in candidate_ids:
            source = pool[skill_id]
            original = Path(str(source["local_original_path"])).resolve()
            expected_hash = str(source["source_sha256"])
            if not original.is_file() or sha256(original) != expected_hash:
                failures.append(f"source_hash_or_presence_failure:{proposal_id}:{skill_id}")
                continue
            packet_path = args.packet_directory / skill_id / "SKILL.original.md"
            packet_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, packet_path)
            if sha256(packet_path) != expected_hash:
                failures.append(f"packet_copy_hash_failure:{proposal_id}:{skill_id}")
                continue
            candidate = {
                "skill_id": skill_id,
                "origin": source["origin"],
                "repository_url": source["repository_url"],
                "pinned_commit": source["pinned_commit"],
                "source_repository_path": source["source_repository_path"],
                "source_sha256": expected_hash,
                "local_original_path": str(original),
                "license": source["license"],
                "license_status": source["license_status"],
                "packet_original_path": str(packet_path.resolve()),
            }
            candidates.append(candidate)
            packet_rows.append({
                "packet_status": "C0B_EXACT_PINNED_SOURCE_COPY_NOT_A_CLUSTER_OR_RESULT",
                "proposal_id": proposal_id,
                **candidate,
                "exclusions": [
                    "This packet is an immutable source copy for C0B only.",
                    "No prompt, label, acceptable set, retrieval input, model call, metric, or result exists.",
                ],
            })
        if len(candidates) != len(candidate_ids):
            continue
        if len({str(candidate["origin"]) for candidate in candidates}) != len(candidates):
            failures.append(f"candidate_origins_not_unique:{proposal_id}")
            continue
        seen_candidates.update(candidate_ids)
        queue_rows.append({
            "c0b_queue_status": "C0B_QUEUE_SOURCE_SCREEN_ONLY_NOT_A_CLUSTER_OR_RESULT",
            "proposal_id": proposal_id,
            "candidates": candidates,
            "exclusions": [
                "No C0A envelope or C0A risk is transferred to a C0B roster.",
                "No prompt, label, acceptable set, retrieval input, model call, metric, or result exists.",
            ],
        })

    packet_rows.sort(key=lambda row: (str(row["proposal_id"]), str(row["skill_id"])))
    queue_rows.sort(key=lambda row: str(row["proposal_id"]))
    write_jsonl(args.packet_manifest, packet_rows)
    write_jsonl(args.queue_output, queue_rows)
    summary = {
        "status": "C0B_SOURCE_PACKET_PASS_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0B_SOURCE_PACKET_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "proposal_count": len(queue_rows),
        "source_copy_count": len(packet_rows),
        "unique_skill_count": len({str(row["skill_id"]) for row in packet_rows}),
        "failures": failures,
        "exclusions": [
            "No source text was edited; packet copies were SHA-256 verified.",
            "No prompt, label, acceptable set, retrieval input, model call, metric, or benchmark cluster was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "proposal_count": summary["proposal_count"],
        "source_copy_count": summary["source_copy_count"],
        "unique_skill_count": summary["unique_skill_count"],
        "failure_count": len(failures),
    }, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
