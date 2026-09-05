#!/usr/bin/env python3
"""Materialise isolated, high-risk-only C3 rewrite packets for Round 42."""

from __future__ import annotations

import argparse
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--c3-review", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--slice-count", type=int, default=4)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    if args.slice_count < 1:
        raise SystemExit("invalid_slice_count")

    prompts_by_key = {key(row): row for row in read_jsonl(args.prompts)}
    selected: list[dict[str, Any]] = []
    for review in read_jsonl(args.c3_review):
        if review.get("residual_cue_risk") != "high":
            continue
        row_key = key(review)
        prompt = prompts_by_key.get(row_key)
        if prompt is None:
            raise SystemExit(f"missing_prompt:{row_key}")
        selected.append({
            "c3_high_risk_rewrite_packet_status": "C3_HIGH_RISK_REWRITE_PACKET_NOT_A_LABEL_OR_RESULT",
            "proposal_id": row_key[0],
            "intended_candidate_skill_id": row_key[1],
            "variant": row_key[2],
            "old_prompt": str(prompt["prompt"]),
            "c3_rationale": str(review["rationale"]),
            "instructions": [
                "Rewrite source-cue risk only; do not assess adequacy, labels, selection, or retrieval.",
                "The new prompt must be one ordinary user sentence with one high-level task/object and at most one broad operational constraint.",
                "Remove time windows, named workflows, multi-step sequences, specialised interface combinations, fixed paths, parameter bundles, output formats, and source-specific examples.",
            ],
            "exclusions": ["No candidate originals, labels, selection review, retrieval input, result, metric, or C4+ material is included."],
        })
    selected.sort(key=key)
    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(selected):
        buckets[index % args.slice_count].append(row)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    slices: list[dict[str, Any]] = []
    for index in range(args.slice_count):
        number = index + 1
        path = args.output_dir / f"c3_round42_high_risk_rewrite_slice_{number:02d}_2026-08-28.jsonl"
        write_jsonl(path, buckets[index])
        slices.append({"slice": number, "packet_count": len(buckets[index]), "path": str(path)})
    manifest = {
        "status": "C3_ROUND42_HIGH_RISK_REWRITE_PACKETS_MATERIALISED_NOT_A_LABEL_OR_RESULT",
        "high_risk_prompt_count": len(selected),
        "slices": slices,
        "exclusions": ["These are prompt-rewrite inputs only; no adequacy, label, retrieval, metric, or frozen-cluster decision was made."],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"high_risk_prompt_count": len(selected), "slice_count": len(slices), "status": manifest["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
