#!/usr/bin/env python3
"""Harmonise four complete V3 strict triads with RQ1b V2's frozen format.

This local tool never modifies V2, rebuilds cards, scores a selector, or sends
text externally. It imports only V3 C4A canonical cards already bound by C4B,
C5 and C6, and retains incomplete V3 parents in a quarantine ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
V2 = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28"
V3 = REPO / "skill_benchmark/rq1b_v3_public_source_frame"
DEFAULT_OUT = REPO / "skill_benchmark/rq1b_final_public_corpus_v1/v2_v3_complete_triad_extension_2026-08-30"
FIELDS = (
    "use_condition", "input_precondition", "output_artifact",
    "workflow_procedure", "success_verification", "boundary_not_for",
    "dependency_resource",
)
CONDITIONS = {
    "FULL": None, "MASK_USE": "use_condition", "MASK_INPUT": "input_precondition",
    "MASK_OUTPUT": "output_artifact", "MASK_WORKFLOW": "workflow_procedure",
    "MASK_SUCCESS": "success_verification", "MASK_BOUNDARY": "boundary_not_for",
    "MASK_DEPENDENCY": "dependency_resource",
}
MARKER = "[FIELD WITHHELD IN THIS REPRESENTATION]"

COMPLETE = (
    {
        "extension_id": "CFTX-V3-001", "source_composition_id": "RQ1B-V3-D1-W4-001",
        "card": V3 / "c4a_v1_2_execution_2026-08-30/conformance_proposals/C4A-RQ1B-V3-D1-W4-001.json",
        "card_audit": V3 / "c4a_v1_2_execution_2026-08-30/canonical_card_audits/C4A-RQ1B-V3-D1-W4-001.json",
        "consensus": V3 / "c4b_blind_review_wave_001_v2_2026-08-30/c4b_consensus_audit_r1.json",
        "c5_key": V3 / "c4b_blind_review_wave_001_v2_2026-08-30/private_key/c5_sealed_target_key.jsonl",
        "c6": V3 / "c4b_blind_review_wave_001_v2_2026-08-30/c6_freeze/c6_frozen_strict_cases.jsonl",
        "c2": V3 / "c2_prompt_construction_wave_001_2026-08-29/c2_draft_ledger_r1.jsonl",
    },
    {
        "extension_id": "CFTX-V3-002", "source_composition_id": "RQ1B-V3-W29-D1-UI-DOMAIN-001",
        "card": V3 / "c4a_field_card_wave_029_2026-08-30/conformance_proposals/C4A-RQ1B-V3-W29-D1-UI-DOMAIN-001.json",
        "card_audit": V3 / "c4a_field_card_wave_029_2026-08-30/canonical_audits/C4A-RQ1B-V3-W29-D1-UI-DOMAIN-001_audit.json",
        "consensus": V3 / "c4b_blind_review_wave_029_2026-08-30/c4b_consensus_audit_amended.json",
        "c5_key": V3 / "c4b_blind_review_wave_029_2026-08-30/private_key/c5_sealed_target_key.jsonl",
        "c6": V3 / "c4b_blind_review_wave_029_2026-08-30/c6_freeze/c6_frozen_strict_cases.jsonl",
        "c2": V3 / "c2_prompt_construction_wave_029_2026-08-30/c2_draft_ledger_c3r1_validated.jsonl",
    },
    {
        "extension_id": "CFTX-V3-003", "source_composition_id": "RQ1B-V3-W32-D1-PRIOR-ART-SURVEY-001",
        "card": V3 / "d1_directed_discovery_wave_032_2026-08-30/c4a_field_card_wave_032_2026-08-30/canonical_cards/C4A-RQ1B-V3-W32-D1-PRIOR-ART-SURVEY-001.json",
        "card_audit": V3 / "d1_directed_discovery_wave_032_2026-08-30/c4a_field_card_wave_032_2026-08-30/canonical_cards/C4A-RQ1B-V3-W32-D1-PRIOR-ART-SURVEY-001_audit.json",
        "consensus": V3 / "d1_directed_discovery_wave_032_2026-08-30/c4b_blind_adequacy_wave_032_2026-08-30/C4B_CONSENSUS_AUDIT_R1.json",
        "c5_key": V3 / "d1_directed_discovery_wave_032_2026-08-30/c4b_blind_adequacy_wave_032_2026-08-30/private_key/c5_sealed_target_key.jsonl",
        "c6": V3 / "d1_directed_discovery_wave_032_2026-08-30/c6_strict_freeze_wave_032_2026-08-30/c6_frozen_strict_cases.jsonl",
        "c2": V3 / "d1_directed_discovery_wave_032_2026-08-30/c2_prompt_construction_wave_032_2026-08-30/c2_draft_ledger_c3r1.jsonl",
    },
    {
        "extension_id": "CFTX-V3-004", "source_composition_id": "RQ1B-V3-W33-D1-PATHWAY-INPUT-001",
        "card": V3 / "d1_directed_discovery_wave_033_2026-08-30/c4a_field_card_wave_033_2026-08-30/canonical_cards/C4A-RQ1B-V3-W33-D1-PATHWAY-INPUT-001_r1.json",
        "card_audit": V3 / "d1_directed_discovery_wave_033_2026-08-30/c4a_field_card_wave_033_2026-08-30/canonical_cards/C4A-RQ1B-V3-W33-D1-PATHWAY-INPUT-001_r1_audit.json",
        "consensus": V3 / "d1_directed_discovery_wave_033_2026-08-30/c4b_blind_adequacy_wave_033_2026-08-30/C4B_CONSENSUS_AUDIT.json",
        "c5_key": V3 / "d1_directed_discovery_wave_033_2026-08-30/c4b_blind_adequacy_wave_033_2026-08-30/private_key/c5_sealed_target_key.jsonl",
        "c6": V3 / "d1_directed_discovery_wave_033_2026-08-30/c6_strict_freeze_wave_033_2026-08-30/c6_frozen_strict_cases.jsonl",
        "c2": V3 / "d1_directed_discovery_wave_033_2026-08-30/c2_prompt_construction_wave_033_2026-08-30/c2_draft_ledger.jsonl",
    },
)
PARTIAL_QUARANTINE = (
    {"source_composition_id": "RQ1B-V3-D1-W4-002", "strict_case_count": 4, "expected_complete_case_count": 6},
    {"source_composition_id": "RQ1B-V3-D1-W4-003", "strict_case_count": 4, "expected_complete_case_count": 6},
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"JSONL object rows required: {path}")
    return rows


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def render(cell: dict[str, Any]) -> str:
    return "NOT_STATED" if cell["status"] == "NOT_STATED" else "\n\n".join(cell["quotes"])


def validate_cards(cards: Any, context: str) -> dict[str, dict[str, dict[str, Any]]]:
    if not isinstance(cards, dict) or len(cards) != 3:
        raise ValueError(f"{context}: exactly three cards required")
    for label, card in cards.items():
        if not isinstance(label, str) or not isinstance(card, dict) or tuple(card) != FIELDS:
            raise ValueError(f"{context}: incompatible card fields for {label}")
        for field in FIELDS:
            cell = card[field]
            if not isinstance(cell, dict) or set(cell) != {"status", "quotes"}:
                raise ValueError(f"{context}: bad schema for {label}/{field}")
            if cell["status"] not in {"EVIDENCE", "NOT_STATED"} or not isinstance(cell["quotes"], list):
                raise ValueError(f"{context}: bad cell for {label}/{field}")
            if (cell["status"] == "EVIDENCE" and not cell["quotes"]) or (cell["status"] == "NOT_STATED" and cell["quotes"]):
                raise ValueError(f"{context}: evidence-status mismatch for {label}/{field}")
    return cards


def immutable_json(path: Path, value: object, check: bool) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            raise ValueError(f"non-identical or missing integration artifact: {relative(path)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ValueError(f"refusing to overwrite non-identical frozen artifact: {relative(path)}")
    path.write_text(text, encoding="utf-8")


def resolve(config: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    card_payload = read_json(config["card"])
    cards = validate_cards(card_payload.get("cards"), config["extension_id"])
    card_audit, consensus = read_json(config["card_audit"]), read_json(config["consensus"])
    if not str(card_audit.get("status", "")).endswith("PASS") or "PASS" not in str(consensus.get("status", "")):
        raise ValueError(f"{config['extension_id']}: C4A/C4B gate failure")
    c6 = [row for row in read_jsonl(config["c6"]) if row.get("composition_id") == config["source_composition_id"]]
    if len(c6) != 6 or {row.get("prompt_variant") for row in c6} != {"direct", "paraphrase"}:
        raise ValueError(f"{config['extension_id']}: incomplete C6 coverage")
    if any(row.get("status") != "RQ1B_V3_C6_FROZEN_STRICT_CASE_WITH_CUE_STRATUM_NOT_A_RETRIEVAL_RESULT" for row in c6):
        raise ValueError(f"{config['extension_id']}: unfrozen C6 case")
    if {row.get("canonical_card_sha256") for row in c6} != {sha_file(config["card"])}:
        raise ValueError(f"{config['extension_id']}: card hash binding failure")
    if {row.get("canonical_card_audit_sha256") for row in c6} != {sha_file(config["card_audit"])}:
        raise ValueError(f"{config['extension_id']}: audit hash binding failure")
    if {row.get("c4b_consensus_sha256") for row in c6} != {sha_file(config["consensus"])}:
        raise ValueError(f"{config['extension_id']}: consensus hash binding failure")

    c2_by_packet = {
        row["c2_packet_id"]: row for row in read_jsonl(config["c2"])
        if isinstance(row.get("c2_packet_id"), str) and isinstance(row.get("prompt_text"), str) and row["prompt_text"].strip()
    }
    c5_by_packet = {
        row["c2_packet_id"]: row for row in read_jsonl(config["c5_key"])
        if isinstance(row.get("c2_packet_id"), str)
    }
    label_to_source: dict[str, tuple[str, str]] = {}
    cases = []
    for row in sorted(c6, key=lambda item: item["case_id"]):
        packet = row["c2_packet_id"]
        c2, c5 = c2_by_packet.get(packet), c5_by_packet.get(packet)
        if c2 is None or c5 is None or sha_text(c2["prompt_text"]) != row["prompt_sha256"]:
            raise ValueError(f"{config['extension_id']}: missing or unbound C2 prompt {packet}")
        if c2.get("variant") != row["prompt_variant"] or c2.get("sealed_target_source_id") != row["strict_gold_source_id"]:
            raise ValueError(f"{config['extension_id']}: C2 target/variant mismatch {packet}")
        mapping = {
            item["canonical_card_label"]: (item["source_id"], item["source_sha256"])
            for item in c5.get("canonical_card_to_source", [])
        }
        if set(mapping) != set(cards) or mapping.get(row["selected_canonical_card"], (None,))[0] != row["strict_gold_source_id"]:
            raise ValueError(f"{config['extension_id']}: C5 card-to-gold mismatch {packet}")
        if sorted(value[1] for value in mapping.values()) != sorted(item["source_sha256"] for item in row["candidate_source_hashes"]):
            raise ValueError(f"{config['extension_id']}: C5 source hash mismatch {packet}")
        if label_to_source and label_to_source != mapping:
            raise ValueError(f"{config['extension_id']}: candidate mapping drift")
        label_to_source = mapping
        cases.append({
            "case_id": row["case_id"], "c2_packet_id": packet, "prompt": c2["prompt_text"],
            "prompt_sha256": row["prompt_sha256"], "prompt_variant": row["prompt_variant"],
            "strict_gold_skill_id": row["strict_gold_source_id"], "strict_gold_card": row["selected_canonical_card"],
            "residual_cue_risk": row["residual_cue_risk"],
        })
    by_gold: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        by_gold[case["strict_gold_skill_id"]].append(case)
    if len(by_gold) != 3 or any({case["prompt_variant"] for case in group} != {"direct", "paraphrase"} for group in by_gold.values()):
        raise ValueError(f"{config['extension_id']}: target-by-variant symmetry failure")
    provenance = {
        "v3_canonical_card_path": relative(config["card"]), "v3_canonical_card_sha256": sha_file(config["card"]),
        "v3_card_audit_path": relative(config["card_audit"]), "v3_card_audit_sha256": sha_file(config["card_audit"]),
        "v3_c4b_consensus_path": relative(config["consensus"]), "v3_c4b_consensus_sha256": sha_file(config["consensus"]),
        "v3_c5_key_path": relative(config["c5_key"]), "v3_c6_path": relative(config["c6"]),
        "v3_c2_final_prompt_path": relative(config["c2"]),
    }
    return ({
        "composition_id": config["extension_id"], "source_composition_id": config["source_composition_id"],
        "candidate_count": 3, "candidate_source_sha256": sorted(value[1] for value in label_to_source.values()),
        "private_candidates": [{"label": label, "skill_id": value[0], "source_sha256": value[1]} for label, value in sorted(label_to_source.items())],
        "provenance": provenance,
    }, cases, {"cards": cards, "provenance": provenance})


def build(output: Path, check: bool) -> dict[str, Any]:
    freeze = read_json(V2 / "condition_materialisation_freeze_amendment_2026-08-29.json")
    if len(freeze.get("canonical_card_file_sha256", {})) != 48:
        raise ValueError("native V2 active-composition contract drift")
    compositions, families, audit_rows = [], [], []
    for config in COMPLETE:
        composition, cases, imported = resolve(config)
        compositions.append(composition)
        canonical = {
            "status": "RQ1B_V2_PLUS_V3_IMPORTED_CANONICAL_SOURCE_CARD_NOT_A_RESULT",
            "composition_id": composition["composition_id"], "source_composition_id": composition["source_composition_id"],
            "field_order": list(FIELDS), "canonical_builder": "V3_C4A_IMPORTED_AFTER_LOCAL_COMPATIBILITY_AUDIT",
            "provenance": imported["provenance"], "cards": imported["cards"],
        }
        immutable_json(output / "canonical_cards" / f"{composition['composition_id']}.json", canonical, check)
        for condition, withheld in CONDITIONS.items():
            payload = {
                "status": "RQ1B_V2_PLUS_V3_IMPORTED_CONDITION_NOT_A_RESULT",
                "composition_id": composition["composition_id"], "source_composition_id": composition["source_composition_id"],
                "condition": condition, "withheld_field": withheld, "marker": MARKER if withheld else None,
                "field_order": list(FIELDS),
                "cards": [{"label": label, "slots": {field: MARKER if field == withheld else render(imported["cards"][label][field]) for field in FIELDS}} for label in sorted(imported["cards"])],
            }
            immutable_json(output / "conditions" / composition["composition_id"] / f"{condition}.json", payload, check)
        by_gold: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for case in cases:
            by_gold[case["strict_gold_skill_id"]].append(case)
        for index, (gold, group) in enumerate(sorted(by_gold.items()), start=1):
            ordered = sorted(group, key=lambda row: row["prompt_variant"])
            families.append({
                "routing_family_id": f"{composition['composition_id']}-F{index}", "composition_id": composition["composition_id"],
                "source_composition_id": composition["source_composition_id"], "strict_gold_skill_id": gold,
                "strict_gold_card": ordered[0]["strict_gold_card"], "prompt_lineage": ordered,
            })
        audit_rows.append({
            "extension_composition_id": composition["composition_id"], "source_composition_id": composition["source_composition_id"],
            "status": "COMPATIBLE_COMPLETE_TRIAD", "candidate_count": 3, "strict_case_count": 6,
            "routing_family_count": 3, "prompt_count": 6, "all_card_fields": list(FIELDS),
            "all_c6_prompt_hashes_resolved": True, "all_c5_target_maps_verified": True,
            "all_c4a_and_c4b_gates_passed": True, "provenance": imported["provenance"],
        })
    if len(compositions) != 4 or len(families) != 12:
        raise ValueError("extension count drift")
    quarantine = {
        "status": "RQ1B_V2_PLUS_V3_PARTIAL_V3_COMPOSITIONS_QUARANTINED_NOT_A_RESULT",
        "rule": "A parent must have all three strict target-by-direct/paraphrase pairs before it enters the symmetric field-ablation matrix.",
        "rows": [{**row, "reason": "two target/variant cases are absent; do not materialise an asymmetric composition"} for row in PARTIAL_QUARANTINE],
    }
    audit = {
        "status": "RQ1B_V2_PLUS_V3_COMPLETE_TRIAD_COMPATIBILITY_AUDIT_PASS_NOT_A_SELECTOR_RESULT",
        "field_order": list(FIELDS), "condition_order": list(CONDITIONS), "complete_triads": audit_rows,
        "partial_triads_quarantined": quarantine["rows"],
        "claim_boundary": "Schema and lineage compatibility only; no selector score, embedding, retrieval metric, field-effect estimate or thesis result.",
    }
    combined = {
        "status": "RQ1B_V2_PLUS_V3_HARMONISED_FUTURE_SELECTOR_MANIFEST_NOT_A_RESULT",
        "native_v2": {"root": relative(V2), "active_candidate_compositions": 48, "strict_preserved_routing_families": 87, "strict_prompts": 174, "conditions_per_composition": 8},
        "imported_v3_complete_triads": {"root": relative(output), "candidate_compositions": 4, "strict_preserved_routing_families": 12, "strict_prompts": 24, "conditions_per_composition": 8},
        "prospective_harmonised_matrix": {"candidate_compositions": 52, "strict_preserved_routing_families": 99, "strict_prompts": 198, "conditions": list(CONDITIONS), "selector_rows_per_retriever": 1584},
        "pooling_rule": "Do not overwrite or relabel completed native V2 results. A later selector run must report native V2, imported V3 and a harmonised combined estimate separately.",
    }
    artifacts = {
        "extension_composition_manifest_private.json": {"status": "RQ1B_V2_PLUS_V3_EXTENSION_COMPOSITIONS_NOT_A_RESULT", "rows": compositions},
        "extension_routing_family_manifest_private.json": {"status": "RQ1B_V2_PLUS_V3_EXTENSION_FAMILIES_NOT_A_RESULT", "rows": families},
        "partial_v3_quarantine_ledger.json": quarantine, "compatibility_audit.json": audit, "combined_matrix_manifest.json": combined,
    }
    for name, payload in artifacts.items():
        immutable_json(output / name, payload, check)
    return combined


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    summary = build(args.output, args.check)
    print(json.dumps({"status": "PASS", "mode": "check" if args.check else "write", "prospective_harmonised_matrix": summary["prospective_harmonised_matrix"]}, sort_keys=True))


if __name__ == "__main__":
    main()
