#!/usr/bin/env python3
"""Materialise prompt-free C1 source-evidence review packets from C0 advances."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


VERSION = "rq1b-v3-c1-source-evidence-materialiser-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c0-wave-dir", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=3)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError(f"refusing to overwrite C1 review wave: {args.output_dir}")

    selected = []
    parent_ledgers = []
    for wave_dir in args.c0_wave_dir:
        ledger_path = wave_dir / "c0_review_final_ledger.jsonl"
        roster_path = wave_dir / "c0_review_roster.jsonl"
        if not ledger_path.exists() or not roster_path.exists():
            raise ValueError(f"missing final C0 ledger or roster: {wave_dir}")
        parent_ledgers.append({"path": str(ledger_path), "sha256": sha256_file(ledger_path)})
        roster = {row["c0_review_id"]: row for row in read_jsonl(roster_path)}
        for decision in read_jsonl(ledger_path):
            if decision["final_c0_outcome"] != "ADVANCE_C1_SOURCE_EVIDENCE":
                continue
            parent = roster.get(decision["c0_review_id"])
            if parent is None:
                raise ValueError(f"C0 final record has no roster binding: {decision['c0_review_id']}")
            selected.append({"decision": decision, "parent": parent})

    selected.sort(key=lambda item: item["decision"]["c0_review_id"])
    source_ids = [member["source_id"] for item in selected for member in item["parent"]["members"]]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("C1 source reuse across C0 advances requires explicit separate handling")

    staging = args.output_dir.parent / f".{args.output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        packets = []
        for index, item in enumerate(selected, start=1):
            parent = item["parent"]
            decision = item["decision"]
            packets.append(
                {
                    "c1_review_id": f"RQ1B-V3-C1-W1-{index:03d}",
                    "parent_c0_review_id": decision["c0_review_id"],
                    "lexical_draft_id": decision["lexical_draft_id"],
                    "members": parent["members"],
                    "candidate_count": 3,
                    "review_scope": "SOURCE_ONLY_C1_EVIDENCE_CARD",
                    "review_status": "UNREVIEWED_SOURCE_ONLY",
                    "claim_boundary": "This packet contains no prompt, intended winner, gold label, acceptable set, representation, selector output, or metric. A C1 pass is only permission for later prompt construction.",
                    "allowed_outcomes": [
                        "ADVANCE_C2_PROMPT_CONSTRUCTION",
                        "REJECT_SOURCE_BINDING",
                        "REJECT_ABSENT_OPERATIONAL_CHAIN",
                        "REJECT_NO_COMMON_ENVELOPE",
                        "REJECT_NONPARALLEL_OR_COMPONENT",
                        "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
                        "NEEDS_PARENT_REVIEW",
                    ],
                    "required_card_elements": [
                        "common envelope evidence for all members",
                        "literal input or trigger span for every member",
                        "literal operation span for every member",
                        "literal output span for every member",
                        "literal boundary/prerequisite/dependency span when stated, otherwise NOT STATED",
                        "peer-role rationale with no invented prompt",
                    ],
                }
            )
        (staging / "c1_review_roster.jsonl").write_text("".join(json.dumps(packet, sort_keys=True) + "\n" for packet in packets))
        for start in range(0, len(packets), args.batch_size):
            batch = packets[start : start + args.batch_size]
            (staging / f"batch_{start // args.batch_size + 1:02d}.json").write_text(
                json.dumps({
                    "review_scope": "SOURCE_ONLY_C1_EVIDENCE_CARD",
                    "instructions": "Read only the listed original source artifacts. Do not inspect or invent prompts, labels, gold answers, acceptable sets, representations, selector outputs, scores, or online information. Return one allowed outcome and literal source spans for every required card element.",
                    "items": batch,
                }, indent=2, sort_keys=True) + "\n"
            )
        manifest = {
            "status": "RQ1B_V3_C1_SOURCE_EVIDENCE_WAVE_MATERIALISED_LOCAL_ONLY",
            "version": VERSION,
            "parent_ledgers": parent_ledgers,
            "packets": len(packets),
            "sources": len(source_ids),
            "batches": (len(packets) + args.batch_size - 1) // args.batch_size,
            "batch_size": args.batch_size,
            "network_calls": 0,
            "texts_transmitted": 0,
            "claim_boundary": "C1 materialisation is source-only evidence construction. It is not prompt construction, gold adjudication, semantic validation, field-effect evidence, or retrieval.",
            "artifacts": {"c1_review_roster.jsonl": sha256_file(staging / "c1_review_roster.jsonl")},
        }
        (staging / "c1_review_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(args.output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
