#!/usr/bin/env python3
"""Build a blind P1 source-evidence mapping packet from a locked P0.5 family.

The resulting packet contains only anonymous candidate copies, source hashes,
and a coordinator-supplied field contrast. It deliberately excludes prompts,
gold labels, provenance, C4/C5 records, and prior mapper output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p05-root", type=Path, required=True)
    parser.add_argument("--family-id", required=True)
    parser.add_argument("--field", required=True)
    parser.add_argument("--contrast", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    source_dir = args.p05_root / args.family_id
    source_packet = json.loads((source_dir / "field_coding_packet.json").read_text())
    output_dir = args.output_root / args.family_id.replace("P05", "P1")
    if output_dir.exists():
        raise SystemExit(f"Refusing to overwrite packet: {output_dir}")
    output_dir.mkdir(parents=True)

    candidates = []
    for candidate in source_packet["candidates"]:
        source = source_dir / candidate["text_path"]
        expected_sha = candidate["sha256"]
        if not source.is_file() or sha256(source) != expected_sha:
            raise SystemExit(f"source hash mismatch: {candidate['label']}")
        destination = output_dir / candidate["text_path"]
        shutil.copyfile(source, destination)
        if sha256(destination) != expected_sha:
            raise SystemExit(f"copy hash mismatch: {candidate['label']}")
        candidates.append(
            {
                "label": candidate["label"],
                "text_path": candidate["text_path"],
                "sha256": expected_sha,
            }
        )

    packet = {
        "packet_status": "P1_BLIND_EVIDENCE_MAPPING_INPUT_NOT_A_RESULT",
        "family_id": output_dir.name,
        "locked_primary_field": args.field,
        "locked_field_value_contrast": args.contrast,
        "instructions": [
            "Use only this packet and the listed anonymous candidate text files.",
            "Do not read prompts, gold labels, provenance, C4/C5 records, masks, prior maps, scores, or results.",
            "Enumerate every exact source span that directly states, operationalises, negates, presupposes, or verifies the locked field value.",
            "For each span, classify the carrier as title_heading, description, use_condition, input_precondition, output_artifact, workflow_procedure, boundary_not_for, dependency_resource, success_verification, example, or resource_reference.",
            "Classify each span as differential_target_field, shared_non_target, or inseparable_structural_cue; propose a neutral local replacement only for differential_target_field.",
            "Every evidence quote must be a literal contiguous substring from its anonymous candidate text. Do not paraphrase or normalise punctuation.",
            "Before finalising, the reviewer may run the local literal-evidence validator on its own response and these packet copies; that preflight does not approve a map or expose any excluded information.",
            "Do not infer a gold candidate or predict a retrieval outcome.",
        ],
        "candidates": candidates,
    }
    write_json(output_dir / "p1_evidence_mapping_packet.json", packet)
    write_json(
        output_dir / "packet_integrity.json",
        {
            "status": "P1_PACKET_HASH_PASS_NOT_A_RESULT",
            "family_id": output_dir.name,
            "candidate_count": len(candidates),
            "candidate_hashes": {candidate["label"]: candidate["sha256"] for candidate in candidates},
            "exclusions": ["No prompts copied.", "No gold label copied.", "No mask created.", "No retrieval, embedding, API call, score, or metric created."],
        },
    )
    print(json.dumps({"output": str(output_dir), "candidate_count": len(candidates)}, sort_keys=True))


if __name__ == "__main__":
    main()
