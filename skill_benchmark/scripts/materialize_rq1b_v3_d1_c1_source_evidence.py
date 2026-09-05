#!/usr/bin/env python3
"""Materialise prompt-free C1 source-evidence packets from D1 drafts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


VERSION = "rq1b-v3-d1-c1-source-evidence-materialiser-v1"
BOUNDARY = "C1 materialisation is source-only evidence construction. It is not prompt construction, gold adjudication, semantic validation, field-effect evidence, or retrieval."


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--d1-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument(
        "--wave-label",
        default="W1",
        help="Stable C1 wave token, for example W1 or W2 (default: W1).",
    )
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError(f"refusing to overwrite C1 review wave: {args.output_dir}")
    drafts = [json.loads(line) for line in args.d1_manifest.read_text().splitlines() if line.strip()]
    if not drafts:
        raise ValueError("D1 manifest is empty")
    staging = args.output_dir.parent / f".{args.output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        packets = []
        for index, draft in enumerate(drafts, start=1):
            members = draft["members"]
            if len(members) not in {3, 4} or len({member["source_id"] for member in members}) != len(members):
                raise ValueError(f"invalid D1 member set: {draft['d1_draft_id']}")
            packets.append({
                "c1_review_id": f"RQ1B-V3-D1-C1-{args.wave_label}-{index:03d}",
                "parent_d1_draft_id": draft["d1_draft_id"],
                "discovery_lane": draft["discovery_lane"],
                "members": [{key: member[key] for key in ("source_id", "sha256", "origin_key", "relative_path", "absolute_path", "title")} for member in members],
                "candidate_count": len(members),
                "review_scope": "SOURCE_ONLY_C1_EVIDENCE_CARD",
                "review_status": "UNREVIEWED_SOURCE_ONLY",
                "claim_boundary": "This packet contains no prompt, intended winner, gold label, acceptable set, representation, selector output, or metric. A C1 pass is only permission for later prompt construction.",
                "allowed_outcomes": ["ADVANCE_C2_PROMPT_CONSTRUCTION", "REJECT_SOURCE_BINDING", "REJECT_ABSENT_OPERATIONAL_CHAIN", "REJECT_NO_COMMON_ENVELOPE", "REJECT_NONPARALLEL_OR_COMPONENT", "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "NEEDS_PARENT_REVIEW"],
                "required_card_elements": ["common envelope evidence for all members", "literal input or trigger span for every member", "literal operation span for every member", "literal output span for every member", "literal boundary/prerequisite/dependency span when stated, otherwise NOT STATED", "peer-route rationale with no invented prompt"],
            })
        (staging / "c1_review_roster.jsonl").write_text("".join(json.dumps(packet, sort_keys=True) + "\n" for packet in packets))
        for start in range(0, len(packets), args.batch_size):
            (staging / f"batch_{start // args.batch_size + 1:02d}.json").write_text(json.dumps({
                "review_scope": "SOURCE_ONLY_C1_EVIDENCE_CARD",
                "instructions": "Read only the listed original source artifacts. Do not inspect or invent prompts, labels, gold answers, acceptable sets, representations, selector outputs, scores, or online information. Return one allowed outcome and literal source spans for every required card element.",
                "items": packets[start : start + args.batch_size],
            }, indent=2, sort_keys=True) + "\n")
        manifest = {"status": "RQ1B_V3_D1_C1_SOURCE_EVIDENCE_WAVE_MATERIALISED_LOCAL_ONLY", "version": VERSION, "wave_label": args.wave_label, "parent_d1_manifest_sha256": sha256_file(args.d1_manifest), "packets": len(packets), "sources": sum(len(packet["members"]) for packet in packets), "batches": (len(packets) + args.batch_size - 1) // args.batch_size, "batch_size": args.batch_size, "network_calls": 0, "texts_transmitted": 0, "claim_boundary": BOUNDARY, "artifacts": {"c1_review_roster.jsonl": sha256_file(staging / "c1_review_roster.jsonl")}}
        (staging / "c1_review_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(args.output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
