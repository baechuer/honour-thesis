#!/usr/bin/env python3
"""Audit composition-keyed RQ1b v2 inputs locally before card construction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    public = json.loads((root / "source_card_builder_manifest.json").read_text())
    private_compositions = json.loads((root / "composition_manifest_private.json").read_text())
    private_families = json.loads((root / "routing_family_manifest_private.json").read_text())
    private_by_id = {row.get("composition_id"): row for row in private_compositions}
    failures, compositions = [], []
    seen_compositions = set()
    for row in public:
        composition_id = row.get("composition_id")
        family_failures = []
        private = private_by_id.get(composition_id)
        if private is None:
            family_failures.append("private_composition_missing")
            private = {}
        if composition_id in seen_compositions:
            family_failures.append("duplicate_composition_id")
        seen_compositions.add(composition_id)
        packet = json.loads((root / composition_id / "field_card_builder_packet.json").read_text())
        candidates, private_candidates = packet.get("candidates", []), private.get("private_candidates", [])
        if len(candidates) not in {3, 4} or len(candidates) != len(private_candidates):
            family_failures.append("candidate_cardinality_mismatch")
        by_label = {candidate.get("label"): candidate for candidate in private_candidates}
        for candidate in candidates:
            label, expected_sha = candidate.get("label"), candidate.get("source_sha256")
            copy_path = root / composition_id / candidate.get("text_path", "")
            private_candidate = by_label.get(label)
            if private_candidate is None:
                family_failures.append(f"private_candidate_missing:{label}")
            elif expected_sha != private_candidate.get("source_sha256"):
                family_failures.append(f"private_source_hash_mismatch:{label}")
            if not copy_path.is_file() or sha256(copy_path) != expected_sha:
                family_failures.append(f"copied_source_hash_mismatch:{label}")
        failures.extend(f"{composition_id}:{failure}" for failure in family_failures)
        compositions.append({"composition_id": composition_id, "valid": not family_failures, "failures": family_failures})
    family_rows = []
    seen_families = set()
    for row in private_families:
        routing_family_id, composition_id, gold = row.get("routing_family_id"), row.get("composition_id"), row.get("strict_gold_skill_id")
        row_failures = []
        if routing_family_id in seen_families:
            row_failures.append("duplicate_routing_family_id")
        seen_families.add(routing_family_id)
        composition = private_by_id.get(composition_id, {})
        skills = {candidate.get("skill_id") for candidate in composition.get("private_candidates", [])}
        if gold not in skills:
            row_failures.append("strict_gold_not_in_composition")
        variants = {item.get("prompt_variant") for item in row.get("prompt_lineage", [])}
        if variants != {"direct", "paraphrase"}:
            row_failures.append("direct_paraphrase_pair_missing")
        failures.extend(f"{routing_family_id}:{failure}" for failure in row_failures)
        family_rows.append({"routing_family_id": routing_family_id, "composition_id": composition_id, "valid": not row_failures, "failures": row_failures})
    payload = {"status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_V2_INPUT_INTEGRITY_AUDIT_NOT_A_RESULT", "valid": not failures, "composition_count": len(compositions), "routing_family_count": len(family_rows), "compositions": compositions, "routing_families": family_rows, "failures": failures, "exclusions": ["No card decision, selector, embedding, retrieval, score, metric, API call, or result is created."]}
    output = root / "audits" / "confirmatory_v2_input_integrity_audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"composition_count": len(compositions), "routing_family_count": len(family_rows), "valid": payload["valid"]}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
