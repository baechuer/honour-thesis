#!/usr/bin/env python3
"""Materialise the local RQ1b public field-type ablation validation pilot.

This script only reconstructs six frozen strict public families into anonymous,
hash-verified source packets. It intentionally omits the historical
primary-field locks. It creates no field cards, mask conditions, selector
inputs, embeddings, retrieval scores, metrics, or external transfers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark")
DEFAULT_OUTPUT = ROOT / "working/field_type_ablation_pilot_2026-08-28"
PILOT_FAMILIES = (
    ("FTA-001", "P05B08-001", ROOT / "working/masked_execution/p05_field_coding_batch08_2026-08-28/private_lineage_manifest.json"),
    ("FTA-002", "P05B08-003", ROOT / "working/masked_execution/p05_field_coding_batch08_2026-08-28/private_lineage_manifest.json"),
    ("FTA-003", "P05B08-005", ROOT / "working/masked_execution/p05_field_coding_batch08_2026-08-28/private_lineage_manifest.json"),
    ("FTA-004", "P05B03-005", ROOT / "working/masked_execution/p05_field_coding_batch03_2026-08-28/private_lineage_manifest.json"),
    ("FTA-005", "P05B09-006", ROOT / "working/masked_execution/p05_field_coding_batch09_2026-08-28/private_lineage_manifest.json"),
    ("FTA-006", "P05B10-006", ROOT / "working/masked_execution/p05_field_coding_batch10_2026-08-28/private_lineage_manifest.json"),
)
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
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def load_private_family(family_id: str, private_manifest: Path) -> dict:
    records = json.loads(private_manifest.read_text())
    matches = [item for item in records if item.get("family_id") == family_id]
    if len(matches) != 1:
        raise ValueError(f"expected one private family for {family_id}, found {len(matches)}")
    record = matches[0]
    candidates = record.get("private_candidates")
    if not isinstance(candidates, list) or len(candidates) not in (3, 4):
        raise ValueError(f"invalid candidate cardinality for {family_id}")
    gold = record.get("strict_gold_skill_id")
    if gold not in {candidate.get("skill_id") for candidate in candidates}:
        raise ValueError(f"strict gold missing from {family_id}")
    prompt_variants = {item.get("prompt_variant") for item in record.get("prompt_lineage", [])}
    if prompt_variants != {"direct", "paraphrase"}:
        raise ValueError(f"missing direct/paraphrase pair for {family_id}: {prompt_variants}")
    return record


def packet_schema(labels: list[str]) -> dict:
    return {
        label: {
            field: {"status": "EVIDENCE or NOT_STATED", "quotes": []}
            for field in FIELDS
        }
        for label in labels
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {output}")

    output.mkdir(parents=True)
    public_manifest = []
    private_manifest = []
    for pilot_id, family_id, lineage_path in PILOT_FAMILIES:
        record = load_private_family(family_id, lineage_path)
        pilot_dir = output / pilot_id
        source_dir = pilot_dir / "sources"
        source_dir.mkdir(parents=True)

        public_candidates = []
        private_candidates = []
        for candidate in sorted(record["private_candidates"], key=lambda item: item["label"]):
            label = candidate["label"]
            source = Path(candidate["canonical_source"]["packet_original_path"])
            expected_sha = candidate["source_sha256"]
            if source.name != "SKILL.original.md" or not source.is_file():
                raise ValueError(f"missing canonical original for {pilot_id}: {source}")
            if sha256(source) != expected_sha:
                raise ValueError(f"source hash mismatch for {pilot_id}: {source}")
            copy_path = source_dir / f"{label.replace(' ', '_')}.md"
            shutil.copyfile(source, copy_path)
            if sha256(copy_path) != expected_sha:
                raise ValueError(f"copy hash mismatch for {pilot_id}: {copy_path}")
            public_candidates.append(
                {"label": label, "source_sha256": expected_sha, "text_path": f"sources/{copy_path.name}"}
            )
            private_candidates.append(
                {
                    "label": label,
                    "skill_id": candidate["skill_id"],
                    "source_sha256": expected_sha,
                    "canonical_source": candidate["canonical_source"],
                }
            )

        labels = [item["label"] for item in public_candidates]
        packet = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_SOURCE_CARD_BUILDER_PACKET_NOT_A_RESULT",
            "pilot_id": pilot_id,
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
            "field_record_schema": {
                "status": "EVIDENCE or NOT_STATED",
                "quotes": ["exact contiguous source-body excerpt; non-empty only for EVIDENCE"],
            },
            "required_response_schema": {"pilot_id": pilot_id, "cards": packet_schema(labels)},
            "candidates": public_candidates,
        }
        write_json(pilot_dir / "field_card_builder_packet.json", packet)
        public_manifest.append(
            {
                "pilot_id": pilot_id,
                "source_family_id": family_id,
                "candidate_count": len(labels),
                "builder_packet": str(pilot_dir / "field_card_builder_packet.json"),
                "status": "READY_FOR_TWO_INDEPENDENT_SOURCE_ONLY_CARD_BUILDERS",
            }
        )
        private_manifest.append(
            {
                "pilot_id": pilot_id,
                "source_family_id": family_id,
                "strict_gold_skill_id": record["strict_gold_skill_id"],
                "prompt_lineage": record["prompt_lineage"],
                "private_candidates": private_candidates,
            }
        )

    write_json(output / "source_card_builder_manifest.json", public_manifest)
    write_json(output / "pilot_input_manifest_private.json", private_manifest)
    write_json(
        output / "summary.json",
        {
            "status": "RQ1B_FIELD_TYPE_ABLATION_PILOT_INPUT_MATERIALISED_NOT_A_RESULT",
            "pilot_count": len(PILOT_FAMILIES),
            "field_order": list(FIELDS),
            "scope": "local anonymous hash-verified sources only",
            "exclusions": [
                "No primary-field label is included.",
                "No card, mask, selector input, embedding, retrieval, score, metric, or thesis result exists.",
                "No external service or API call occurred.",
            ],
        },
    )
    print(json.dumps({"output": str(output), "pilot_count": len(PILOT_FAMILIES)}, sort_keys=True))


if __name__ == "__main__":
    main()
