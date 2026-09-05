#!/usr/bin/env python3
"""Re-materialise Round 42 C3 packets after a prompt-only rewrite, fail closed."""

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
    parser.add_argument("--prior-packet", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    prompts = read_jsonl(args.prompts)
    prompt_by_key = {key(row): row for row in prompts}
    if len(prompt_by_key) != len(prompts):
        raise SystemExit("duplicate_prompt_identity")
    prior = [row for path in args.prior_packet for row in read_jsonl(path)]
    prior_by_key = {key(row): row for row in prior}
    if len(prior_by_key) != len(prior) or set(prior_by_key) != set(prompt_by_key):
        raise SystemExit("prior_packet_identity_mismatch")

    packets: list[dict[str, Any]] = []
    for row_key in sorted(prompt_by_key):
        packet = dict(prior_by_key[row_key])
        packet["prompt"] = str(prompt_by_key[row_key]["prompt"])
        packet["c3_packet_status"] = "C3_MANUAL_SEMANTIC_RECHECK_PACKET_NOT_A_LABEL_OR_RESULT"
        for candidate in packet.get("candidate_originals", []):
            source = Path(str(candidate.get("local_original_path", "")))
            if not source.is_file() or sha256(source) != str(candidate.get("source_sha256", "")):
                raise SystemExit(f"candidate_source_changed_or_missing:{row_key}:{candidate.get('skill_id')}")
        packets.append(packet)

    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, packet in enumerate(packets):
        buckets[index % len(args.prior_packet)].append(packet)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    slices: list[dict[str, Any]] = []
    for index in range(len(args.prior_packet)):
        number = index + 1
        path = args.output_dir / f"c3_round42_recheck_slice_{number:02d}_2026-08-28.jsonl"
        write_jsonl(path, buckets[index])
        slices.append({"slice": number, "packet_count": len(buckets[index]), "path": str(path), "sha256": sha256(path)})
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "status": "C3_ROUND42_RECHECK_PACKETS_MATERIALISED_NOT_A_LABEL_OR_RESULT",
        "prompt_packet_count": len(packets),
        "prior_packet_count": len(args.prior_packet),
        "slices": slices,
        "invariants": [
            "Only the prompt text was refreshed from the declared prompt-only rewrite output.",
            "Candidate identities, original artifact paths, and source hashes were preserved and byte-verified.",
            "No adequacy, label, retrieval input, model result, metric, or frozen benchmark state was created.",
        ],
    }
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"prompt_packet_count": len(packets), "slice_count": len(slices), "status": manifest["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
