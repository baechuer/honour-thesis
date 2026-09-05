#!/usr/bin/env python3
"""Build composition-keyed RQ1b field-type confirmatory inputs locally.

Cards are a property of a candidate composition, not of a prompt/gold family.
This materialiser therefore makes one anonymous hash-verified source packet per
composition and a separate sealed evaluation-family manifest. It does not
create cards, masks, selector inputs, embeddings, scores, metrics, API calls,
or results.
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
DEFAULT_OUTPUT = ROOT / "working/field_type_ablation_confirmatory_v2_2026-08-28"
EXPECTED_P0_COUNTS = {"rows": 408, "families": 209, "compositions": 76}
FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def family_key(composition: list[str], gold: str) -> tuple[tuple[str, ...], str]:
    return tuple(sorted(composition)), gold


def packet_schema(labels: list[str]) -> dict:
    return {
        label: {field: {"status": "EVIDENCE or NOT_STATED", "quotes": []} for field in FIELDS}
        for label in labels
    }


def load_pilot_family_keys(path: Path) -> set[tuple[tuple[str, ...], str]]:
    rows = json.loads(path.read_text())
    if not isinstance(rows, list):
        raise ValueError("pilot private manifest must be a JSON array")
    keys = set()
    for row in rows:
        candidates = row.get("private_candidates")
        gold = row.get("strict_gold_skill_id")
        if not isinstance(candidates, list) or not isinstance(gold, str):
            raise ValueError("malformed pilot private row")
        parts = []
        for candidate in candidates:
            skill_id, source_sha = candidate.get("skill_id"), candidate.get("source_sha256")
            if not isinstance(skill_id, str) or not isinstance(source_sha, str):
                raise ValueError("malformed pilot candidate")
            parts.append(f"{skill_id}:{source_sha}")
        keys.add(family_key(parts, gold))
    return keys


def candidate_identity(candidate: dict) -> str:
    return f"{candidate['skill_id']}:{candidate['source_sha256']}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--pilot-private", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {args.output}")

    roster = json.loads(args.roster.read_text())
    if roster.get("status") != "P0_MASTER_ROSTER_PRECHECK_PASS_NOT_A_RESULT" or roster.get("counts") != EXPECTED_P0_COUNTS:
        raise ValueError("frozen P0 roster status/counts do not match")
    rows = roster.get("rows")
    if not isinstance(rows, list) or len(rows) != EXPECTED_P0_COUNTS["rows"]:
        raise ValueError("malformed P0 rows")
    pilot_exclusions = load_pilot_family_keys(args.pilot_private)

    routing_groups: dict[tuple[tuple[str, ...], str], list[dict]] = defaultdict(list)
    for row in rows:
        composition, gold, candidates = row.get("candidate_composition_key"), row.get("strict_gold_skill_id"), row.get("candidates")
        if not isinstance(composition, list) or not isinstance(gold, str) or not isinstance(candidates, list) or len(candidates) not in {3, 4}:
            raise ValueError("malformed P0 candidate or family row")
        if tuple(sorted(candidate_identity(candidate) for candidate in candidates)) != tuple(sorted(composition)):
            raise ValueError("candidate composition identity mismatch")
        routing_groups[family_key(composition, gold)].append(row)

    decisions = []
    retained_families: list[tuple[tuple[tuple[str, ...], str], list[dict]]] = []
    for key, group_rows in sorted(routing_groups.items()):
        variants = {row.get("prompt_variant") for row in group_rows}
        if key in pilot_exclusions:
            status = "EXCLUDED_PILOT_ROUTING_FAMILY"
        elif variants != {"direct", "paraphrase"} or len(group_rows) != 2:
            status = "EXCLUDED_MISSING_EXACT_DIRECT_PARAPHRASE_PAIR"
        else:
            status = "RETAINED_PAIRED_NONPILOT_ROUTING_FAMILY"
            retained_families.append((key, group_rows))
        decisions.append({"routing_family_key": {"candidate_composition_key": list(key[0]), "strict_gold_skill_id": key[1]}, "row_count": len(group_rows), "prompt_variants": sorted(variants), "status": status})

    by_composition: dict[tuple[str, ...], list[tuple[tuple[tuple[str, ...], str], list[dict]]]] = defaultdict(list)
    for family in retained_families:
        by_composition[family[0][0]].append(family)
    args.output.mkdir(parents=True)
    composition_ids = {composition: f"CFTC-{index:03d}" for index, composition in enumerate(sorted(by_composition), start=1)}
    public_compositions = []
    private_compositions = []
    for composition in sorted(by_composition):
        composition_id = composition_ids[composition]
        members = by_composition[composition]
        representative = sorted(members[0][1], key=lambda row: (row["round"], row["c6_manifest"], row["c6_manifest_line"]))[0]
        candidates = sorted(representative["candidates"], key=candidate_identity)
        if tuple(candidate_identity(candidate) for candidate in candidates) != composition:
            raise ValueError(f"representative composition mismatch: {composition_id}")
        source_dir = args.output / composition_id / "sources"
        source_dir.mkdir(parents=True)
        public_candidates, private_candidates = [], []
        for ordinal, candidate in enumerate(candidates):
            label = f"Candidate {chr(ord('A') + ordinal)}"
            source = Path(candidate["canonical_source"]["packet_original_path"])
            expected_sha = candidate["source_sha256"]
            if source.name != "SKILL.original.md" or not source.is_file() or sha256(source) != expected_sha:
                raise ValueError(f"unverified source for {composition_id}: {source}")
            copied = source_dir / f"{label.replace(' ', '_')}.md"
            shutil.copyfile(source, copied)
            if sha256(copied) != expected_sha:
                raise ValueError(f"copy hash mismatch: {copied}")
            public_candidates.append({"label": label, "source_sha256": expected_sha, "text_path": f"sources/{copied.name}"})
            private_candidates.append({"label": label, "skill_id": candidate["skill_id"], "source_sha256": expected_sha, "canonical_source": candidate["canonical_source"], "lineage_matches": candidate["lineage_matches"]})
        labels = [candidate["label"] for candidate in public_candidates]
        packet = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_V2_SOURCE_CARD_BUILDER_PACKET_NOT_A_RESULT",
            "composition_id": composition_id,
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
            "required_response_schema": {"composition_id": composition_id, "cards": packet_schema(labels)},
            "candidates": public_candidates,
        }
        write_json(args.output / composition_id / "field_card_builder_packet.json", packet)
        public_compositions.append({"composition_id": composition_id, "candidate_count": len(labels), "builder_packet": str(args.output / composition_id / "field_card_builder_packet.json"), "status": "READY_FOR_TWO_INDEPENDENT_SOURCE_ONLY_CARD_BUILDERS"})
        private_compositions.append({"composition_id": composition_id, "candidate_composition_key": list(composition), "private_candidates": private_candidates})

    private_families = []
    for index, (key, group_rows) in enumerate(sorted(retained_families), start=1):
        by_variant = {row["prompt_variant"]: row for row in group_rows}
        private_families.append({
            "routing_family_id": f"CFTF-{index:03d}",
            "composition_id": composition_ids[key[0]],
            "strict_gold_skill_id": key[1],
            "prompt_lineage": [
                {"prompt_variant": variant, "prompt": by_variant[variant]["prompt"], "round": by_variant[variant]["round"], "proposal_id": by_variant[variant]["proposal_id"], "c6_manifest": by_variant[variant]["c6_manifest"], "c6_manifest_sha256": by_variant[variant]["c6_manifest_sha256"], "c6_manifest_line": by_variant[variant]["c6_manifest_line"], "c2_lineage": by_variant[variant]["c2_lineage"]}
                for variant in ("direct", "paraphrase")
            ],
        })

    write_json(args.output / "source_card_builder_manifest.json", public_compositions)
    write_json(args.output / "composition_manifest_private.json", private_compositions)
    write_json(args.output / "routing_family_manifest_private.json", private_families)
    write_json(args.output / "exclusion_ledger.json", {"status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_V2_INPUT_EXCLUSIONS_NOT_A_RESULT", "decisions": decisions})
    counts = {"p0_rows": len(rows), "p0_routing_groups": len(routing_groups), "p0_candidate_compositions": len({key[0] for key in routing_groups}), "pilot_excluded_routing_families": sum(row["status"] == "EXCLUDED_PILOT_ROUTING_FAMILY" for row in decisions), "unpaired_or_variant_excluded_routing_families": sum(row["status"] == "EXCLUDED_MISSING_EXACT_DIRECT_PARAPHRASE_PAIR" for row in decisions), "retained_routing_families": len(private_families), "retained_prompts": len(private_families) * 2, "retained_candidate_compositions": len(private_compositions)}
    write_json(args.output / "summary.json", {"status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_V2_INPUT_MATERIALISED_NOT_A_RESULT", "counts": counts, "field_order": list(FIELDS), "scope": "local anonymous hash-verified composition source packets and sealed routing-family lineage only", "exclusions": ["Pilot routing families are excluded from confirmatory effects.", "Groups without exactly one direct and one paraphrase prompt are excluded.", "No card, mask, selector input, embedding, retrieval score, metric, API call, or result exists."]})
    print(json.dumps({"output": str(args.output), **counts}, sort_keys=True))


if __name__ == "__main__":
    main()
