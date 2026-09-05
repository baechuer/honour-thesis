#!/usr/bin/env python3
"""Build a hash-verified, read-only C0B source packet from a C0A worklist.

The packet copies exact public originals into one local audit directory so a
source-screen reviewer receives only the protocol and assigned source files.
It does not assess semantic similarity, create prompts or labels, or produce
benchmark clusters or empirical results.
"""

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--packet-manifest", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queue = read_jsonl(args.queue)
    if not queue:
        raise SystemExit("empty_queue")

    output_root = args.output_root.resolve()
    rows: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    failures: list[str] = []

    for proposal in queue:
        proposal_id = str(proposal.get("proposal_id", ""))
        if not proposal_id:
            failures.append("missing_proposal_id")
            continue
        for candidate in proposal.get("candidates", []):
            skill_id = str(candidate.get("skill_id", ""))
            expected_hash = str(candidate.get("source_sha256", ""))
            source = Path(str(candidate.get("local_original_path", "")))
            if not skill_id or not expected_hash or not source.is_file():
                failures.append(f"missing_source:{proposal_id}:{skill_id}")
                continue
            if sha256(source) != expected_hash:
                failures.append(f"source_hash_drift:{proposal_id}:{skill_id}")
                continue
            previous = seen.get(skill_id)
            if previous is not None and previous != expected_hash:
                failures.append(f"skill_id_hash_collision:{skill_id}")
                continue
            seen[skill_id] = expected_hash
            destination = output_root / skill_id / "SKILL.original.md"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            if sha256(destination) != expected_hash:
                failures.append(f"packet_copy_hash_drift:{proposal_id}:{skill_id}")
                continue
            rows.append(
                {
                    "packet_status": "C0B_EXACT_SOURCE_PACKET_NOT_A_CLUSTER_OR_RESULT",
                    "proposal_id": proposal_id,
                    "skill_id": skill_id,
                    "origin": candidate.get("origin"),
                    "repository_url": candidate.get("repository_url"),
                    "pinned_commit": candidate.get("pinned_commit"),
                    "license": candidate.get("license"),
                    "license_status": candidate.get(
                        "license_status", "DECLARED_REPOSITORY_LICENSE"
                    ),
                    "source_repository_path": candidate.get("source_repository_path"),
                    "source_sha256": expected_hash,
                    "packet_original_path": str(destination),
                }
            )

    rows.sort(key=lambda row: (row["proposal_id"], row["skill_id"]))
    args.packet_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.packet_manifest.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8"
    )
    summary = {
        "status": "C0B_SOURCE_PACKET_PASS_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0B_SOURCE_PACKET_FAIL_OR_INCOMPLETE",
        "proposal_count": len(queue),
        "source_copy_count": len(rows),
        "unique_skill_count": len(seen),
        "failures": failures,
        "exclusions": [
            "No source text was edited; packet copies were SHA-256 verified.",
            "No prompt, label, acceptable set, retrieval input, model call, metric, or benchmark cluster was created.",
        ],
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "source_copy_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
