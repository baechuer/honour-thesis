#!/usr/bin/env python3
"""Materialise non-pilot RQ1b field-type ablation inputs from the C6 roster.

This is a local, hash-verified lineage reconstruction only. It builds anonymous
source-card packets for paired strict C6 families and deliberately excludes the
six field-type validation-pilot compositions. It does not create cards, masks,
selector inputs, embeddings, retrieval scores, metrics, API requests, or
scientific results.
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
DEFAULT_PILOT = ROOT / "working/field_type_ablation_pilot_2026-08-28/pilot_input_manifest_private.json"
DEFAULT_OUTPUT = ROOT / "working/field_type_ablation_confirmatory_2026-08-28"
FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
EXPECTED_P0_COUNTS = {"rows": 408, "families": 209, "compositions": 76}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def family_key(composition: list[str], gold: str) -> tuple[tuple[str, ...], str]:
    return tuple(sorted(composition)), gold


def packet_schema(labels: list[str]) -> dict:
    return {
        label: {
            field: {"status": "EVIDENCE or NOT_STATED", "quotes": []}
            for field in FIELDS
        }
        for label in labels
    }


def pilot_keys(path: Path) -> set[tuple[tuple[str, ...], str]]:
    rows = json.loads(path.read_text())
    if not isinstance(rows, list):
        raise ValueError("pilot private manifest must be a JSON array")
    keys = set()
    for row in rows:
        candidates = row.get("private_candidates")
        gold = row.get("strict_gold_skill_id")
        if not isinstance(candidates, list) or not isinstance(gold, str):
            raise ValueError("malformed pilot private row")
        composition = []
        for candidate in candidates:
            skill_id = candidate.get("skill_id")
            source_sha = candidate.get("source_sha256")
            if not isinstance(skill_id, str) or not isinstance(source_sha, str):
                raise ValueError("malformed pilot candidate")
            composition.append(f"{skill_id}:{source_sha}")
        keys.add(family_key(composition, gold))
    return keys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--pilot-private", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {args.output}")

    roster = json.loads(args.roster.read_text())
    if roster.get("status") != "P0_MASTER_ROSTER_PRECHECK_PASS_NOT_A_RESULT":
        raise ValueError("P0 roster status is not the frozen precheck pass")
    if roster.get("counts") != EXPECTED_P0_COUNTS:
        raise ValueError(f"P0 count mismatch: {roster.get('counts')}")
    rows = roster.get("rows")
    if not isinstance(rows, list) or len(rows) != EXPECTED_P0_COUNTS["rows"]:
        raise ValueError("malformed P0 roster rows")

    pilot_exclusions = pilot_keys(args.pilot_private)
    grouped: dict[tuple[tuple[str, ...], str], list[dict]] = defaultdict(list)
    for row in rows:
        composition = row.get("candidate_composition_key")
        gold = row.get("strict_gold_skill_id")
        candidates = row.get("candidates")
        if not isinstance(composition, list) or not isinstance(gold, str) or not isinstance(candidates, list):
            raise ValueError("malformed P0 row")
        if len(candidates) not in {3, 4}:
            raise ValueError("P0 candidate cardinality outside 3-4")
        grouped[family_key(composition, gold)].append(row)

    decisions = []
    retained: list[tuple[tuple[tuple[str, ...], str], list[dict]]] = []
    for key, group_rows in sorted(grouped.items()):
        variants = {item.get("prompt_variant") for item in group_rows}
        candidate_lists = {tuple(item.get("candidate_composition_key", [])) for item in group_rows}
        if len(candidate_lists) != 1:
            raise ValueError(f"candidate composition drift in group: {key}")
        if key in pilot_exclusions:
            status = "EXCLUDED_PILOT_COMPOSITION_AND_GOLD"
        elif variants != {"direct", "paraphrase"} or len(group_rows) != 2:
            status = "EXCLUDED_MISSING_EXACT_DIRECT_PARAPHRASE_PAIR"
        else:
            status = "RETAINED_PAIRED_NONPILOT"
            retained.append((key, group_rows))
        decisions.append(
            {
                "family_key": {"candidate_composition_key": list(key[0]), "strict_gold_skill_id": key[1]},
                "row_count": len(group_rows),
                "prompt_variants": sorted(variants),
                "status": status,
            }
        )

    args.output.mkdir(parents=True)
    public_manifest = []
    private_manifest = []
    for index, (key, group_rows) in enumerate(retained, start=1):
        family_id = f"CFTA-{index:03d}"
        by_variant = {row["prompt_variant"]: row for row in group_rows}
        base = by_variant["direct"]
        candidates = sorted(
            base["candidates"],
            key=lambda item: f"{item['skill_id']}:{item['source_sha256']}",
        )
        family_dir = args.output / family_id
        source_dir = family_dir / "sources"
        source_dir.mkdir(parents=True)
        public_candidates = []
        private_candidates = []
        for ordinal, candidate in enumerate(candidates):
            label = f"Candidate {chr(ord('A') + ordinal)}"
            source = Path(candidate["canonical_source"]["packet_original_path"])
            expected_sha = candidate["source_sha256"]
            if source.name != "SKILL.original.md" or not source.is_file():
                raise ValueError(f"source original missing for {family_id}: {source}")
            if sha256(source) != expected_sha:
                raise ValueError(f"source hash mismatch for {family_id}: {source}")
            copy_path = source_dir / f"{label.replace(' ', '_')}.md"
            shutil.copyfile(source, copy_path)
            if sha256(copy_path) != expected_sha:
                raise ValueError(f"copied hash mismatch for {family_id}: {copy_path}")
            public_candidates.append({"label": label, "source_sha256": expected_sha, "text_path": f"sources/{copy_path.name}"})
            private_candidates.append(
                {
                    "label": label,
                    "skill_id": candidate["skill_id"],
                    "source_sha256": expected_sha,
                    "canonical_source": candidate["canonical_source"],
                    "lineage_matches": candidate["lineage_matches"],
                }
            )

        labels = [item["label"] for item in public_candidates]
        packet = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_SOURCE_CARD_BUILDER_PACKET_NOT_A_RESULT",
            "family_id": family_id,
            "instructions": [
                "Use only this packet and its anonymous source copies.",
                "Do not inspect other workspace files, prompts, strict-gold labels, provenance, previous cards, masks, selectors, or results.",
                "Do not use web, external APIs, embeddings, retrieval, or select a winner.",
                "Return one card for every candidate and all seven fields.",
                "Every EVIDENCE quote must be an exact contiguous source-body substring.",
                "Use NOT_STATED only when that source body contains no evidence for the field.",
                "Do not quote YAML frontmatter, document titles, repository names, IDs, URLs, provenance, or markdown heading lines.",
                "Do not paraphrase, concatenate non-contiguous snippets, add a summary, or infer a missing fact.",
                "Return only the required JSON object.",
            ],
            "field_order": list(FIELDS),
            "field_record_schema": {"status": "EVIDENCE or NOT_STATED", "quotes": ["exact contiguous source-body excerpt; non-empty only for EVIDENCE"]},
            "required_response_schema": {"family_id": family_id, "cards": packet_schema(labels)},
            "candidates": public_candidates,
        }
        write_json(family_dir / "field_card_builder_packet.json", packet)
        public_manifest.append(
            {
                "family_id": family_id,
                "candidate_count": len(labels),
                "builder_packet": str(family_dir / "field_card_builder_packet.json"),
                "status": "READY_FOR_TWO_INDEPENDENT_SOURCE_ONLY_CARD_BUILDERS",
            }
        )
        private_manifest.append(
            {
                "family_id": family_id,
                "roster_family_key": {"candidate_composition_key": list(key[0]), "strict_gold_skill_id": key[1]},
                "strict_gold_skill_id": key[1],
                "prompt_lineage": [
                    {
                        "prompt_variant": variant,
                        "prompt": by_variant[variant]["prompt"],
                        "round": by_variant[variant]["round"],
                        "proposal_id": by_variant[variant]["proposal_id"],
                        "c6_manifest": by_variant[variant]["c6_manifest"],
                        "c6_manifest_sha256": by_variant[variant]["c6_manifest_sha256"],
                        "c6_manifest_line": by_variant[variant]["c6_manifest_line"],
                        "c2_lineage": by_variant[variant]["c2_lineage"],
                    }
                    for variant in ("direct", "paraphrase")
                ],
                "private_candidates": private_candidates,
            }
        )

    write_json(args.output / "source_card_builder_manifest.json", public_manifest)
    write_json(args.output / "confirmatory_input_manifest_private.json", private_manifest)
    write_json(args.output / "exclusion_ledger.json", {"status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_INPUT_EXCLUSIONS_NOT_A_RESULT", "decisions": decisions})
    counts = {
        "p0_rows": len(rows),
        "p0_family_groups": len(grouped),
        "pilot_excluded_groups": sum(item["status"] == "EXCLUDED_PILOT_COMPOSITION_AND_GOLD" for item in decisions),
        "unpaired_or_variant_excluded_groups": sum(item["status"] == "EXCLUDED_MISSING_EXACT_DIRECT_PARAPHRASE_PAIR" for item in decisions),
        "retained_nonpilot_paired_families": len(retained),
        "retained_prompts": len(retained) * 2,
    }
    write_json(
        args.output / "summary.json",
        {
            "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_INPUT_MATERIALISED_NOT_A_RESULT",
            "counts": counts,
            "field_order": list(FIELDS),
            "scope": "local anonymous hash-verified sources only",
            "exclusions": [
                "Pilot composition-plus-gold families are excluded from confirmatory effect estimates.",
                "Groups without exactly one direct and one paraphrase prompt are excluded.",
                "No card, mask, selector input, embedding, retrieval score, metric, API call, or result exists.",
            ],
        },
    )
    print(json.dumps({"output": str(args.output), **counts}, sort_keys=True))


if __name__ == "__main__":
    main()
