#!/usr/bin/env python3
"""Apply the pre-specified non-scoring RQ1b pilot gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pilot_root
    integrity = load_object(root / "audits" / "pilot_input_integrity_audit.json")
    canonical = load_object(root / "canonicalisation_ledger.json")
    mask_summary = load_object(root / "audits" / "mask_mechanics_audit_summary.json")
    eligibility = load_object(root / "audits" / "field_eligibility_ledger.json")
    residual = load_object(root / "audits" / "residual_redundancy_ledger.json")
    eligibility_by_id = {item["pilot_id"]: item for item in eligibility["families"]}
    residual_rows_by_id = {}
    for row in residual["eligible_gold_field_rows"]:
        residual_rows_by_id.setdefault(row["pilot_id"], []).append(row)
    mask_by_id = {item["pilot_id"]: item for item in mask_summary["families"]}
    private_rows = json.loads((root / "pilot_input_manifest_private.json").read_text())
    decisions = []
    for entry in canonical["families"]:
        pilot_id = entry["pilot_id"]
        checks = {
            "literal_card": entry.get("status") == "MATERIALISED_FROM_LITERAL_VALID_CARD",
            "mask_mechanics": bool(mask_by_id.get(pilot_id, {}).get("valid")),
            "full_card_preservation": False,
            "eligibility_complete": False,
            "residual_complete": False,
        }
        if checks["literal_card"]:
            card_audit = load_object(root / "audits" / f"{pilot_id}_{entry['canonical_builder']}_literal_audit.json")
            checks["literal_card"] = bool(card_audit.get("valid"))
            preservation_files = list((root / "audits").glob(f"{pilot_id}_*_vs_*_full_card_preservation.json"))
            checks["full_card_preservation"] = len(preservation_files) == 1 and load_object(preservation_files[0]).get("status") == "RQ1B_FIELD_TYPE_ABLATION_FULL_CARD_PRESERVATION_PASS_NOT_A_SELECTOR_RESULT"
            expected_fields = [row["field"] for row in eligibility_by_id.get(pilot_id, {}).get("field_rows", []) if row["eligible"]]
            actual_fields = [row["field"] for row in residual_rows_by_id.get(pilot_id, [])]
            checks["eligibility_complete"] = len(eligibility_by_id.get(pilot_id, {}).get("field_rows", [])) == 7
            checks["residual_complete"] = residual.get("review_audits_complete") is True and sorted(actual_fields) == sorted(expected_fields)
        decisions.append({"pilot_id": pilot_id, "checks": checks, "passes_all_applicable_gates": all(checks.values())})

    card_or_mask_failures = [
        item["pilot_id"] for item in decisions
        if item["checks"]["literal_card"] and (not item["checks"]["mask_mechanics"] or not item["checks"]["full_card_preservation"])
    ]
    passed_families = sum(item["passes_all_applicable_gates"] for item in decisions)
    passed = bool(integrity.get("valid")) and passed_families >= 4 and len(card_or_mask_failures) <= 1
    payload = {
        "status": (
            "RQ1B_FIELD_TYPE_ABLATION_PILOT_PASS_READY_FOR_NONPILOT_CARD_CONSTRUCTION_NOT_A_RESULT"
            if passed
            else "RQ1B_FIELD_TYPE_ABLATION_PILOT_FAIL_STOP_BEFORE_SCORING_NOT_A_RESULT"
        ),
        "input_integrity_valid": integrity.get("valid") is True,
        "pilot_family_count": len(decisions),
        "families_passing_all_applicable_gates": passed_families,
        "card_or_mask_failure_families": card_or_mask_failures,
        "families": decisions,
        "exclusions": [
            "No BM25, embedding, retrieval score, metric, external API call, or thesis result is created by this gate.",
        ],
    }
    output = root / "audits" / "pilot_gate_decision.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": passed, "passed_families": passed_families, "output": str(output)}, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
