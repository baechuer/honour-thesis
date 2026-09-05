#!/usr/bin/env python3
"""Materialize anonymous, exact-byte P0.5 field-coding packets for Round 42.

This is a local curation builder. It creates no mask, selector score, embedding,
external transfer, or metric. Agent-facing packets omit proposal IDs, source
provenance, and strict-gold labels; the private manifest retains the lineage.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark")
MANIFEST = ROOT / "manifest"
OUTPUT = ROOT / "working/masked_execution/p05_field_coding_round01_2026-08-28"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    c6_rows = read_jsonl(MANIFEST / "c6_round42_frozen_primary_2026-08-28.jsonl")
    c2_rows = read_jsonl(MANIFEST / "c2_round42_drafts_after_c3_final_rewrite_2026-08-28.jsonl")
    c1_rows = read_jsonl(MANIFEST / "c1_round42_integrity_2026-08-28.jsonl")
    source_rows = read_jsonl(MANIFEST / "c0b_round42_source_packet_manifest_2026-08-28.jsonl")

    source_by_skill = {row["skill_id"]: row for row in source_rows}
    c1_by_proposal = {row["proposal_id"]: row for row in c1_rows}
    strict_families: dict[tuple[str, tuple[str, ...], str], dict] = {}
    for row in c6_rows:
        key = (
            row["proposal_id"],
            tuple(sorted(row["candidate_skill_ids"])),
            row["strict_gold_skill_id"],
        )
        strict_families[key] = row

    if OUTPUT.exists():
        raise SystemExit(f"Refusing to overwrite existing packet directory: {OUTPUT}")
    OUTPUT.mkdir(parents=True)

    private_records = []
    public_records = []
    failures = []
    for position, ((proposal_id, candidate_ids, strict_gold), c6_row) in enumerate(
        sorted(strict_families.items()), start=1
    ):
        c1_row = c1_by_proposal.get(proposal_id)
        if c1_row is None or tuple(sorted(c1_row["candidate_skill_ids"])) != candidate_ids:
            failures.append({"proposal_id": proposal_id, "reason": "C1_LINEAGE_MISMATCH"})
            continue

        prompts = [
            row
            for row in c2_rows
            if row["proposal_id"] == proposal_id and row["intended_candidate_skill_id"] == strict_gold
        ]
        prompts.sort(key=lambda row: row["variant"])
        if not prompts or len({row["variant"] for row in prompts}) != len(prompts):
            failures.append({"proposal_id": proposal_id, "reason": "PROMPT_FAMILY_MISSING_OR_DUPLICATE"})
            continue

        ordered_candidates = sorted(candidate_ids, key=lambda skill_id: source_by_skill[skill_id]["source_sha256"])
        family_id = f"P05R01-{position:03d}"
        family_dir = OUTPUT / family_id
        family_dir.mkdir()
        agent_candidates = []
        private_candidates = []
        for label, skill_id in zip(("Candidate A", "Candidate B", "Candidate C", "Candidate D"), ordered_candidates):
            source = source_by_skill.get(skill_id)
            if source is None:
                failures.append({"proposal_id": proposal_id, "reason": f"SOURCE_PACKET_MISSING:{skill_id}"})
                break
            original = Path(source["packet_original_path"])
            expected_sha = source["source_sha256"]
            if not original.is_file() or sha256(original) != expected_sha:
                failures.append({"proposal_id": proposal_id, "reason": f"SOURCE_HASH_MISMATCH:{skill_id}"})
                break
            destination = family_dir / f"{label.replace(' ', '_')}.md"
            shutil.copyfile(original, destination)
            if sha256(destination) != expected_sha:
                failures.append({"proposal_id": proposal_id, "reason": f"COPY_HASH_MISMATCH:{skill_id}"})
                break
            agent_candidates.append(
                {
                    "label": label,
                    "sha256": expected_sha,
                    "text_path": destination.name,
                }
            )
            private_candidates.append(
                {
                    "label": label,
                    "skill_id": skill_id,
                    "source_path": str(original),
                    "sha256": expected_sha,
                }
            )
        else:
            packet = {
                "packet_status": "P05_BLIND_FIELD_CONTRAST_CODING_INPUT_NOT_A_RESULT",
                "family_id": family_id,
                "instructions": [
                    "Use only this packet and the listed anonymous candidate text files.",
                    "Do not use online search, external APIs, retrieval, embeddings, or other workspace files.",
                    "Do not infer or declare a gold label; code the operational field required by each prompt.",
                    "Choose exactly one code per prompt: use_condition, input_precondition, output_artifact, workflow_procedure, boundary_not_for, dependency_resource, success_verification, or MULTI_FIELD_OR_NONCODEABLE.",
                    "Quote exact prompt clauses and exact candidate evidence substrings for every asserted field value.",
                    "If a single field cannot be cleanly isolated, fail closed with MULTI_FIELD_OR_NONCODEABLE.",
                ],
                "prompts": [{"variant": row["variant"], "text": row["prompt"]} for row in prompts],
                "candidates": agent_candidates,
            }
            write_json(family_dir / "field_coding_packet.json", packet)
            private_records.append(
                {
                    "family_id": family_id,
                    "proposal_id": proposal_id,
                    "strict_gold_skill_id": strict_gold,
                    "candidate_skill_ids": list(candidate_ids),
                    "candidate_source_sha256": c6_row["candidate_source_sha256"],
                    "review_packet_ids": [
                        row["review_packet_id"]
                        for row in c6_rows
                        if row["proposal_id"] == proposal_id and row["strict_gold_skill_id"] == strict_gold
                    ],
                    "prompt_variants": [row["variant"] for row in prompts],
                    "private_candidates": private_candidates,
                    "agent_packet_path": str(family_dir / "field_coding_packet.json"),
                }
            )
            public_records.append(
                {
                    "family_id": family_id,
                    "candidate_count": len(agent_candidates),
                    "prompt_variants": [row["variant"] for row in prompts],
                    "packet_path": str(family_dir / "field_coding_packet.json"),
                    "status": "P05_READY_FOR_TWO_INDEPENDENT_BLIND_CODERS_NOT_A_RESULT",
                }
            )
            continue

        shutil.rmtree(family_dir, ignore_errors=True)

    write_json(OUTPUT / "private_lineage_manifest.json", private_records)
    write_json(OUTPUT / "agent_packet_manifest.json", public_records)
    write_json(
        OUTPUT / "summary.json",
        {
            "status": "P05_ROUND01_PACKET_BUILD_COMPLETE_NOT_A_RESULT",
            "source_round": "Round 42 C6",
            "strict_family_count": len(strict_families),
            "packet_count": len(public_records),
            "failure_count": len(failures),
            "failures": failures,
            "exclusions": [
                "No mask was created.",
                "No selector, embedding, retrieval, API call, metric, or label was created.",
            ],
        },
    )
    if failures:
        raise SystemExit(f"Packet build failed: {failures}")
    print(json.dumps({"packet_count": len(public_records), "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
