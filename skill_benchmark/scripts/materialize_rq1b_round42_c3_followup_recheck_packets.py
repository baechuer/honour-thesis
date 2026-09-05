#!/usr/bin/env python3
"""Materialise only freshly rewritten Round 42 C3 follow-up review packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--rewrites", type=Path, required=True)
    parser.add_argument("--prior-packet", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--slice-count", type=int, default=4)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    if args.slice_count < 1:
        raise SystemExit("invalid_slice_count")

    prompts_by_key = {key(row): row for row in read_jsonl(args.prompts)}
    selected_keys = {key(row) for row in read_jsonl(args.rewrites)}
    prior_rows = [row for path in args.prior_packet for row in read_jsonl(path)]
    prior_by_key = {key(row): row for row in prior_rows}
    if len(prior_by_key) != len(prior_rows) or not selected_keys <= set(prior_by_key) or not selected_keys <= set(prompts_by_key):
        raise SystemExit("followup_identity_mismatch")

    packets: list[dict[str, Any]] = []
    for row_key in sorted(selected_keys):
        packet = dict(prior_by_key[row_key])
        packet["prompt"] = str(prompts_by_key[row_key]["prompt"])
        packet["c3_packet_status"] = "C3_MANUAL_SEMANTIC_FOLLOWUP_RECHECK_PACKET_NOT_A_LABEL_OR_RESULT"
        for candidate in packet.get("candidate_originals", []):
            source = Path(str(candidate.get("local_original_path", "")))
            if not source.is_file() or sha256(source) != str(candidate.get("source_sha256", "")):
                raise SystemExit(f"candidate_source_changed_or_missing:{row_key}:{candidate.get('skill_id')}")
        packets.append(packet)

    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, packet in enumerate(packets):
        buckets[index % args.slice_count].append(packet)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    slices: list[dict[str, Any]] = []
    for index in range(args.slice_count):
        number = index + 1
        path = args.output_dir / f"c3_round42_followup_recheck_slice_{number:02d}_2026-08-28.jsonl"
        write_jsonl(path, buckets[index])
        slices.append({"slice": number, "packet_count": len(buckets[index]), "path": str(path), "sha256": sha256(path)})
    manifest = {
        "status": "C3_ROUND42_FOLLOWUP_RECHECK_PACKETS_MATERIALISED_NOT_A_LABEL_OR_RESULT",
        "prompt_packet_count": len(packets),
        "slices": slices,
        "invariants": [
            "Only high-risk prompt identities rewritten after the prior C3 review are included.",
            "Candidate identities, original artifact paths, and source hashes were preserved and byte-verified.",
            "No adequacy, label, retrieval, metric, or frozen benchmark state was created.",
        ],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"prompt_packet_count": len(packets), "slice_count": len(slices), "status": manifest["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
