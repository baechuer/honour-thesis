#!/usr/bin/env python3
"""Materialize one anonymous P0.5 blind field-coding batch from the P0 roster.

This is local curation only. It reads the immutable P0 roster, copies exact
hash-verified original artifacts into anonymous per-family packets, and keeps
gold/provenance only in a private lineage manifest. It creates no mask,
selector score, embedding, external transfer, or metric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark")
DEFAULT_ROSTER = ROOT / "working/masked_execution/p0_master_roster_2026-08-28.json"
DEFAULT_PILOT = ROOT / "working/masked_execution/p05_field_coding_round01_2026-08-28/private_lineage_manifest.json"
FIELD_CODES = [
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
    "MULTI_FIELD_OR_NONCODEABLE",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def family_key(row: dict) -> str:
    payload = {
        "candidate_composition_key": row["candidate_composition_key"],
        "strict_gold_skill_id": row["strict_gold_skill_id"],
    }
    return hashlib.sha256(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()).hexdigest()


def pilot_exclusions(path: Path) -> set[tuple[tuple[str, ...], str]]:
    if not path.is_file():
        raise ValueError(f"pilot private manifest missing: {path}")
    records = json.loads(path.read_text())
    if not isinstance(records, list):
        raise ValueError(f"pilot private manifest is not a list: {path}")
    excluded = set()
    for record in records:
        candidate_ids = record.get("candidate_skill_ids")
        strict_gold = record.get("strict_gold_skill_id")
        if not isinstance(candidate_ids, list) or not isinstance(strict_gold, str):
            raise ValueError(f"malformed pilot private record: {record!r}")
        excluded.add((tuple(sorted(candidate_ids)), strict_gold))
    return excluded


def grouped_families(roster: dict) -> list[dict]:
    if roster.get("status") != "P0_MASTER_ROSTER_PRECHECK_PASS_NOT_A_RESULT":
        raise ValueError("roster status is not the required P0 precheck pass")
    expected = {"rows": 408, "families": 209, "compositions": 76}
    if roster.get("counts") != expected:
        raise ValueError(f"unexpected P0 roster counts: {roster.get('counts')}")

    grouped: dict[tuple[tuple[str, ...], str], list[dict]] = defaultdict(list)
    for row in roster.get("rows", []):
        required = {
            "candidate_composition_key",
            "strict_gold_skill_id",
            "prompt_variant",
            "prompt",
            "candidates",
            "proposal_id",
            "c2_lineage",
        }
        if not required.issubset(row):
            raise ValueError(f"incomplete P0 roster row: {row!r}")
        key = (tuple(row["candidate_composition_key"]), row["strict_gold_skill_id"])
        grouped[key].append(row)

    if len(grouped) != expected["families"]:
        raise ValueError(f"P0 family grouping mismatch: {len(grouped)}")

    families = []
    for key, rows in grouped.items():
        variants = [row["prompt_variant"] for row in rows]
        if len(set(variants)) != len(variants):
            raise ValueError(f"duplicate prompt variant in P0 family: {key}")
        candidate_signatures = {
            tuple((candidate["skill_id"], candidate["source_sha256"]) for candidate in row["candidates"])
            for row in rows
        }
        if len(candidate_signatures) != 1:
            raise ValueError(f"candidate lineage drift within P0 family: {key}")
        proposals = {row["proposal_id"] for row in rows}
        if len(proposals) != 1:
            raise ValueError(f"proposal lineage drift within P0 family: {key}")
        families.append(
            {
                "family_key": family_key(rows[0]),
                "candidate_skill_ids": tuple(sorted(candidate["skill_id"] for candidate in rows[0]["candidates"])),
                "strict_gold_skill_id": rows[0]["strict_gold_skill_id"],
                "rows": sorted(rows, key=lambda item: item["prompt_variant"]),
            }
        )
    return sorted(families, key=lambda item: item["family_key"])


def validate_source(candidate: dict) -> Path:
    canonical = candidate.get("canonical_source", {})
    source_path = Path(canonical.get("packet_original_path", ""))
    expected_sha = candidate.get("source_sha256")
    if not source_path.is_file() or source_path.name != "SKILL.original.md":
        raise ValueError(f"missing canonical original source: {source_path}")
    actual_sha = sha256(source_path)
    if actual_sha != expected_sha:
        raise ValueError(f"canonical source hash mismatch: {source_path}")
    return source_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-index", type=int, required=True, help="1-based batch index after pilot exclusions")
    parser.add_argument("--batch-size", type=int, default=6)
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--pilot-private-manifest", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.batch_index < 1 or not 1 <= args.batch_size <= 6:
        raise SystemExit("batch-index must be positive and batch-size must be in 1..6")

    roster = json.loads(args.roster.read_text())
    excluded = pilot_exclusions(args.pilot_private_manifest)
    remaining = [
        family
        for family in grouped_families(roster)
        if (family["candidate_skill_ids"], family["strict_gold_skill_id"]) not in excluded
    ]
    if len(remaining) != 205:
        raise ValueError(f"expected 205 remaining P0.5 families after four pilot exclusions, got {len(remaining)}")
    start = (args.batch_index - 1) * args.batch_size
    selected = remaining[start : start + args.batch_size]
    if not selected:
        raise SystemExit("requested P0.5 batch is empty")

    output = args.output or ROOT / "working/masked_execution" / f"p05_field_coding_batch{args.batch_index:02d}_2026-08-28"
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing batch directory: {output}")
    output.mkdir(parents=True)

    public_records = []
    private_records = []
    for position, family in enumerate(selected, start=1):
        family_id = f"P05B{args.batch_index:02d}-{position:03d}"
        family_dir = output / family_id
        family_dir.mkdir()
        source_candidates = sorted(
            family["rows"][0]["candidates"],
            key=lambda item: (item["source_sha256"], item["skill_id"]),
        )
        agent_candidates = []
        private_candidates = []
        for label, candidate in zip(("Candidate A", "Candidate B", "Candidate C", "Candidate D"), source_candidates):
            source_path = validate_source(candidate)
            destination = family_dir / f"{label.replace(' ', '_')}.md"
            shutil.copyfile(source_path, destination)
            if sha256(destination) != candidate["source_sha256"]:
                raise ValueError(f"copy hash mismatch for {family_id}:{candidate['skill_id']}")
            agent_candidates.append(
                {"label": label, "sha256": candidate["source_sha256"], "text_path": destination.name}
            )
            private_candidates.append(
                {
                    "label": label,
                    "skill_id": candidate["skill_id"],
                    "source_sha256": candidate["source_sha256"],
                    "canonical_source": candidate["canonical_source"],
                    "all_verified_lineage_matches": candidate["lineage_matches"],
                }
            )

        packet = {
            "packet_status": "P05_BLIND_FIELD_CONTRAST_CODING_INPUT_NOT_A_RESULT",
            "family_id": family_id,
            "instructions": [
                "Use only this packet and the listed anonymous candidate text files.",
                "Do not use online search, external APIs, retrieval, embeddings, or other workspace files.",
                "Do not infer or declare a gold label; code the operational field required by each prompt.",
                "Choose exactly one code per prompt: " + ", ".join(FIELD_CODES) + ".",
                "Quote exact prompt clauses and exact candidate evidence substrings for every asserted field value.",
                "In candidate_evidence, include only labels present in this packet and omit labels with no quoted evidence.",
                "If a single field cannot be cleanly isolated, fail closed with MULTI_FIELD_OR_NONCODEABLE.",
                "Return exactly one JSON object: {\"family_id\": <family id>, \"per_prompt\": [{\"variant\": <packet variant>, \"code\": <one allowed code>, \"prompt_clauses\": [<exact prompt substring>], \"candidate_evidence\": {<present candidate label>: [<exact candidate substring>]}, \"reason\": <brief rationale>}]}.",
                "Use the key per_prompt exactly; do not use prompt_codings, prompt_clause, field_code, or operational_requirement. Return one per_prompt object for every packet prompt variant.",
            ],
            "prompts": [{"variant": row["prompt_variant"], "text": row["prompt"]} for row in family["rows"]],
            "candidates": agent_candidates,
        }
        write_json(family_dir / "field_coding_packet.json", packet)
        public_records.append(
            {
                "family_id": family_id,
                "family_key": family["family_key"],
                "candidate_count": len(agent_candidates),
                "prompt_variants": [row["prompt_variant"] for row in family["rows"]],
                "packet_path": str(family_dir / "field_coding_packet.json"),
                "status": "P05_READY_FOR_TWO_INDEPENDENT_BLIND_CODERS_NOT_A_RESULT",
            }
        )
        private_records.append(
            {
                "family_id": family_id,
                "family_key": family["family_key"],
                "proposal_id": family["rows"][0]["proposal_id"],
                "strict_gold_skill_id": family["strict_gold_skill_id"],
                "candidate_skill_ids": list(family["candidate_skill_ids"]),
                "prompt_lineage": [
                    {
                        "prompt_variant": row["prompt_variant"],
                        "prompt": row["prompt"],
                        "c2_lineage": row["c2_lineage"],
                        "c6_manifest": row["c6_manifest"],
                        "c6_manifest_sha256": row["c6_manifest_sha256"],
                        "c6_manifest_line": row["c6_manifest_line"],
                    }
                    for row in family["rows"]
                ],
                "private_candidates": private_candidates,
                "agent_packet_path": str(family_dir / "field_coding_packet.json"),
            }
        )

    write_json(output / "agent_packet_manifest.json", public_records)
    write_json(output / "private_lineage_manifest.json", private_records)
    write_json(
        output / "summary.json",
        {
            "status": "P05_BATCH_PACKET_BUILD_COMPLETE_NOT_A_RESULT",
            "scope": "local anonymous P0.5 field-coding packet materialization only",
            "batch_index": args.batch_index,
            "batch_size": len(selected),
            "remaining_after_pilot_exclusions": len(remaining),
            "pilot_exclusion_count": len(excluded),
            "roster": str(args.roster),
            "roster_status": roster["status"],
            "exclusions": [
                "No mask was created.",
                "No selector, embedding, retrieval, API call, metric, or label was created.",
            ],
        },
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "batch_index": args.batch_index,
                "packet_count": len(public_records),
                "remaining_after_pilot_exclusions": len(remaining),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
