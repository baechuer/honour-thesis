#!/usr/bin/env python3
"""Verify the six RQ1b field-type pilot inputs without scoring them."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pilot_root
    public_rows = json.loads((root / "source_card_builder_manifest.json").read_text())
    private_rows = json.loads((root / "pilot_input_manifest_private.json").read_text())
    private_by_id = {item["pilot_id"]: item for item in private_rows}
    failures = []
    families = []
    for public in public_rows:
        pilot_id = public.get("pilot_id")
        private = private_by_id.get(pilot_id)
        family_failures = []
        if private is None:
            family_failures.append("private_lineage_missing")
            private = {}
        packet_path = root / pilot_id / "field_card_builder_packet.json"
        try:
            packet = json.loads(packet_path.read_text())
        except Exception as error:
            packet = {"candidates": []}
            family_failures.append(f"packet_load_error:{error}")
        candidates = packet.get("candidates", [])
        private_candidates = private.get("private_candidates", [])
        if len(candidates) not in {3, 4} or len(candidates) != len(private_candidates):
            family_failures.append("candidate_cardinality_mismatch")
        by_label = {item.get("label"): item for item in private_candidates}
        for candidate in candidates:
            label = candidate.get("label")
            private_candidate = by_label.get(label)
            copied = root / pilot_id / candidate.get("text_path", "")
            if private_candidate is None:
                family_failures.append(f"private_candidate_missing:{label}")
                continue
            if not copied.is_file() or sha256(copied) != candidate.get("source_sha256"):
                family_failures.append(f"copied_source_hash_mismatch:{label}")
            if candidate.get("source_sha256") != private_candidate.get("source_sha256"):
                family_failures.append(f"private_source_hash_mismatch:{label}")
        skills = {item.get("skill_id") for item in private_candidates}
        if private.get("strict_gold_skill_id") not in skills:
            family_failures.append("strict_gold_not_in_candidates")
        variants = {item.get("prompt_variant") for item in private.get("prompt_lineage", [])}
        if variants != {"direct", "paraphrase"}:
            family_failures.append("direct_paraphrase_pair_missing")
        failures.extend(f"{pilot_id}:{failure}" for failure in family_failures)
        families.append({"pilot_id": pilot_id, "valid": not family_failures, "failures": family_failures})
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_PILOT_INPUT_INTEGRITY_AUDIT_NOT_A_RESULT",
        "valid": not failures,
        "family_count": len(families),
        "families": families,
        "failures": failures,
        "exclusions": [
            "No card decision, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    output = root / "audits" / "pilot_input_integrity_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"family_count": len(families), "valid": payload["valid"]}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
