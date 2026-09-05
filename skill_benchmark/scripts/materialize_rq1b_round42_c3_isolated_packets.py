#!/usr/bin/env python3
"""Materialise disjoint Round 42 C3 semantic-cue review packets.

The packets expose a C2 prompt, its construction target, and only the exact
candidate original-artifact paths needed to inspect possible source-specific
cueing. They deliberately exclude C4 reviews, C5 strata, and all retrieval
inputs/results.
"""

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--c1", type=Path, required=True)
    parser.add_argument("--source-pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--slice-count", type=int, default=6)
    parser.add_argument(
        "--round-label",
        default="round42",
        help="Audit-round label used only in generated packet filenames.",
    )
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    if args.slice_count < 1:
        raise SystemExit("invalid_slice_count")
    source_by_id = {str(row["skill_id"]): row for row in read_jsonl(args.source_pool)}
    c1_by_proposal = {
        str(row["proposal_id"]): row
        for row in read_jsonl(args.c1)
        if row.get("c1_status") == "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT"
    }
    packets: list[dict[str, Any]] = []
    for row in sorted(read_jsonl(args.prompts), key=lambda value: (str(value["proposal_id"]), str(value["intended_candidate_skill_id"]), str(value["variant"]))):
        proposal_id = str(row["proposal_id"])
        c1 = c1_by_proposal.get(proposal_id)
        if c1 is None:
            raise SystemExit(f"missing_c1:{proposal_id}")
        candidates: list[dict[str, str]] = []
        for skill_id in c1["candidate_skill_ids"]:
            source = source_by_id.get(str(skill_id))
            if source is None:
                raise SystemExit(f"missing_source:{proposal_id}:{skill_id}")
            original_path = Path(str(source["local_original_path"]))
            if not original_path.is_file():
                raise SystemExit(f"missing_original:{proposal_id}:{skill_id}:{original_path}")
            candidates.append({
                "skill_id": str(skill_id),
                "source_sha256": str(source["source_sha256"]),
                "local_original_path": str(original_path),
            })
        packets.append({
            "c3_packet_status": "C3_MANUAL_SEMANTIC_CUE_PACKET_NOT_A_LABEL_OR_RESULT",
            "proposal_id": proposal_id,
            "intended_candidate_skill_id": str(row["intended_candidate_skill_id"]),
            "variant": str(row["variant"]),
            "prompt": str(row["prompt"]),
            "candidate_originals": candidates,
            "instructions": [
                "Assess semantic source-cue risk only; do not assess adequacy, gold labels, or retrieval performance.",
                "A bounded ordinary operational constraint is allowed. A copied title, distinctive source phrase, unique named workflow, or unusual output specification is a cue risk.",
                "Return one disposition: C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT or C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT.",
            ],
            "exclusions": ["No label, selection review, retrieval input, model result, metric, or frozen benchmark state is present."],
        })
    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, packet in enumerate(packets):
        buckets[index % args.slice_count].append(packet)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, Any]] = []
    for index in range(args.slice_count):
        number = index + 1
        path = args.output_dir / f"c3_{args.round_label}_manual_slice_{number:02d}_2026-08-28.jsonl"
        write_jsonl(path, buckets[index])
        manifest_rows.append({"slice": number, "packet_count": len(buckets[index]), "path": str(path)})
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({
        "status": "C3_MANUAL_PACKET_MATERIALISATION_NOT_A_LABEL_OR_RESULT",
        "prompt_packet_count": len(packets),
        "slice_count": args.slice_count,
        "slices": manifest_rows,
        "exclusions": ["No C3 judgment, label, selection review, retrieval input, model result, metric, or frozen benchmark state was created."],
    }, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"prompt_packet_count": len(packets), "slice_count": args.slice_count}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
