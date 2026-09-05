#!/usr/bin/env python3
"""Materialise the local RQ1b-S source-grounded field-card validation pilot.

The script copies only hash-verified frozen original sources into anonymous
builder packets. It creates no field card, mask, selector input, embedding,
retrieval, external transfer, score, metric, or thesis result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark")
DEFAULT_OUTPUT = ROOT / "working/field_card_pilot_2026-08-28"
PILOT_FAMILIES = (
    {
        "pilot_id": "FCP-001",
        "p05_family_id": "P05B08-001",
        "p05_private_manifest": ROOT / "working/masked_execution/p05_field_coding_batch08_2026-08-28/private_lineage_manifest.json",
        "locked_field": "use_condition",
    },
    {
        "pilot_id": "FCP-002",
        "p05_family_id": "P05B08-003",
        "p05_private_manifest": ROOT / "working/masked_execution/p05_field_coding_batch08_2026-08-28/private_lineage_manifest.json",
        "locked_field": "input_precondition",
    },
    {
        "pilot_id": "FCP-003",
        "p05_family_id": "P05B08-005",
        "p05_private_manifest": ROOT / "working/masked_execution/p05_field_coding_batch08_2026-08-28/private_lineage_manifest.json",
        "locked_field": "output_artifact",
    },
    {
        "pilot_id": "FCP-004",
        "p05_family_id": "P05B03-005",
        "p05_private_manifest": ROOT / "working/masked_execution/p05_field_coding_batch03_2026-08-28/private_lineage_manifest.json",
        "locked_field": "workflow_procedure",
    },
    {
        "pilot_id": "FCP-005",
        "p05_family_id": "P05B09-006",
        "p05_private_manifest": ROOT / "working/masked_execution/p05_field_coding_batch09_2026-08-28/private_lineage_manifest.json",
        "locked_field": "boundary_not_for",
    },
    {
        "pilot_id": "FCP-006",
        "p05_family_id": "P05B10-006",
        "p05_private_manifest": ROOT / "working/masked_execution/p05_field_coding_batch10_2026-08-28/private_lineage_manifest.json",
        "locked_field": "dependency_resource",
    },
)
FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def load_private_record(spec: dict) -> dict:
    records = json.loads(spec["p05_private_manifest"].read_text())
    matches = [record for record in records if record.get("family_id") == spec["p05_family_id"]]
    if len(matches) != 1:
        raise ValueError(f"expected one P0.5 private record for {spec['p05_family_id']}, got {len(matches)}")
    record = matches[0]
    candidates = record.get("private_candidates")
    if not isinstance(candidates, list) or len(candidates) not in (3, 4):
        raise ValueError(f"invalid candidate set in {spec['p05_family_id']}")
    if record.get("strict_gold_skill_id") not in {item.get("skill_id") for item in candidates}:
        raise ValueError(f"strict gold is outside candidate set: {spec['p05_family_id']}")
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing pilot directory: {output}")

    output.mkdir(parents=True)
    public_manifest = []
    private_manifest = []
    for spec in PILOT_FAMILIES:
        record = load_private_record(spec)
        family_dir = output / spec["pilot_id"]
        source_dir = family_dir / "sources"
        source_dir.mkdir(parents=True)

        public_candidates = []
        private_candidates = []
        for candidate in sorted(record["private_candidates"], key=lambda item: item["label"]):
            label = candidate["label"]
            source = Path(candidate["canonical_source"]["packet_original_path"])
            expected_sha = candidate["source_sha256"]
            if not source.is_file() or source.name != "SKILL.original.md":
                raise ValueError(f"missing source: {source}")
            if sha256(source) != expected_sha:
                raise ValueError(f"source hash mismatch: {source}")
            destination = source_dir / f"{label.replace(' ', '_')}.md"
            shutil.copyfile(source, destination)
            if sha256(destination) != expected_sha:
                raise ValueError(f"copy hash mismatch: {destination}")
            public_candidates.append(
                {"label": label, "source_sha256": expected_sha, "text_path": f"sources/{destination.name}"}
            )
            private_candidates.append(
                {
                    "label": label,
                    "skill_id": candidate["skill_id"],
                    "source_sha256": expected_sha,
                    "canonical_source": candidate["canonical_source"],
                    "all_verified_lineage_matches": candidate["all_verified_lineage_matches"],
                }
            )

        packet = {
            "status": "RQ1B_S_FIELD_CARD_BUILDER_PACKET_NOT_A_RESULT",
            "pilot_id": spec["pilot_id"],
            "instructions": [
                "Work only from this packet and its anonymous source copies.",
                "Do not inspect other workspace files, prompts, strict-gold labels, provenance, previous reviews, masks, selectors, or results.",
                "Do not use web, external APIs, embeddings, or retrieval.",
                "Do not select a winner or infer a user request.",
                "Build exactly one card record for every listed candidate and all seven fields.",
                "A field with evidence uses one or more exact contiguous excerpts from the candidate source body.",
                "Use NOT_STATED only when source body has no evidence for that field. Do not infer a missing fact.",
                "Do not quote YAML frontmatter, a document title, repository name, skill ID, URL, provenance text, or markdown heading line.",
                "Do not paraphrase, concatenate non-contiguous text, add a summary, or create a task envelope.",
                "Return only the required JSON object to the required response path.",
            ],
            "field_order": list(FIELDS),
            "field_record_schema": {
                "status": "EVIDENCE or NOT_STATED",
                "quotes": ["exact contiguous source excerpt; one or more only when status is EVIDENCE"],
            },
            "required_response_schema": {
                "pilot_id": spec["pilot_id"],
                "cards": {
                    "Candidate A": {
                        "use_condition": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                        "input_precondition": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                        "output_artifact": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                        "workflow_procedure": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                        "boundary_not_for": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                        "dependency_resource": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                        "success_verification": {"status": "EVIDENCE or NOT_STATED", "quotes": []},
                    }
                },
            },
            "candidates": public_candidates,
        }
        write_json(family_dir / "field_card_builder_packet.json", packet)

        public_manifest.append(
            {
                "pilot_id": spec["pilot_id"],
                "locked_field": spec["locked_field"],
                "candidate_count": len(public_candidates),
                "builder_packet": str(family_dir / "field_card_builder_packet.json"),
                "status": "READY_FOR_BLIND_SOURCE_GROUNDED_CARD_BUILDING_NOT_A_RESULT",
            }
        )
        private_manifest.append(
            {
                "pilot_id": spec["pilot_id"],
                "source_p05_family_id": spec["p05_family_id"],
                "locked_field": spec["locked_field"],
                "strict_gold_skill_id": record["strict_gold_skill_id"],
                "prompt_lineage": record["prompt_lineage"],
                "private_candidates": private_candidates,
            }
        )

    write_json(output / "builder_packet_manifest.json", public_manifest)
    write_json(output / "private_lineage_manifest.json", private_manifest)
    write_json(
        output / "summary.json",
        {
            "status": "RQ1B_S_FIELD_CARD_PILOT_PACKET_MATERIALISED_NOT_A_RESULT",
            "scope": "local hash-verified anonymous source packets only",
            "pilot_count": len(PILOT_FAMILIES),
            "fields": [spec["locked_field"] for spec in PILOT_FAMILIES],
            "exclusions": [
                "No source text was changed.",
                "No field card, target neutralisation, sham neutralisation, or selector input was created.",
                "No embedding, retrieval, API call, score, metric, or thesis result exists.",
            ],
        },
    )
    print(json.dumps({"output": str(output), "pilot_count": len(PILOT_FAMILIES)}, sort_keys=True))


if __name__ == "__main__":
    main()
