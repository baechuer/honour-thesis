#!/usr/bin/env python3
"""Compare two blind v2 FULL-card reviews with the sealed strict label."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    composition_rows,
    label_for_skill,
    load_list,
    load_object,
    opaque_packet_id,
    routing_family_rows,
    sha256_file,
    write_json,
)
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--routing-family-id", required=True)
    parser.add_argument("--first-reviewer", required=True)
    parser.add_argument("--second-reviewer", required=True)
    args = parser.parse_args()
    root = args.root
    verify_freeze(root)
    if args.first_reviewer == args.second_reviewer:
        raise ValueError("two distinct reviewers required")
    family = routing_family_rows(root).get(args.routing_family_id)
    if family is None:
        raise ValueError("private routing family missing")
    composition = composition_rows(root).get(family["composition_id"])
    if composition is None:
        raise ValueError("private composition missing")
    gold_label = label_for_skill(composition, family["strict_gold_skill_id"])
    private_map = {item.get("routing_family_id"): item for item in load_list(root / "selection_packet_private_map.json")}
    mapping = private_map.get(args.routing_family_id)
    if not isinstance(mapping, dict):
        raise ValueError("private selection packet map missing family")
    packet_id = mapping.get("packet_id")
    if mapping.get("composition_id") != family["composition_id"] or not isinstance(packet_id, str):
        raise ValueError("private selection packet map mismatch")
    packet_path = root / "selection_packets_opaque" / f"{packet_id}.json"
    packet_sha256 = sha256_file(packet_path)
    if mapping.get("packet_sha256") != packet_sha256:
        raise ValueError("selection packet hash mismatch")
    expected_packet_id = opaque_packet_id("sfp", args.routing_family_id, mapping.get("canonical_card_sha256", ""))
    if packet_id != expected_packet_id:
        raise ValueError("opaque selection packet ID mismatch")
    first_audit = load_object(root / "audits" / f"{packet_id}_{args.first_reviewer}_selection_review_audit.json")
    second_audit = load_object(root / "audits" / f"{packet_id}_{args.second_reviewer}_selection_review_audit.json")
    first = load_object(root / "selection_reviews_opaque" / args.first_reviewer / f"{packet_id}.json")
    second = load_object(root / "selection_reviews_opaque" / args.second_reviewer / f"{packet_id}.json")
    audit_hashes, response_hashes = {}, {}
    for reviewer, audit, response in ((args.first_reviewer, first_audit, first), (args.second_reviewer, second_audit, second)):
        audit_path = root / "audits" / f"{packet_id}_{reviewer}_selection_review_audit.json"
        response_path = root / "selection_reviews_opaque" / reviewer / f"{packet_id}.json"
        audit_hashes[reviewer] = sha256_file(audit_path)
        response_hashes[reviewer] = sha256_file(response_path)
        if (
            audit.get("packet_id") != packet_id
            or audit.get("reviewer") != reviewer
            or audit.get("packet_sha256") != packet_sha256
            or audit.get("response_sha256") != response_hashes[reviewer]
            or not audit.get("valid")
        ):
            raise ValueError(f"invalid selection audit binding: {reviewer}")
        if response.get("packet_id") != packet_id:
            raise ValueError(f"selection response packet binding mismatch: {reviewer}")
    first_rows = {row.get("variant"): row for row in first.get("per_prompt", []) if isinstance(row, dict)}
    second_rows = {row.get("variant"): row for row in second.get("per_prompt", []) if isinstance(row, dict)}
    rows = []
    for prompt in sorted(family["prompt_lineage"], key=lambda item: item["prompt_variant"]):
        variant = prompt["prompt_variant"]
        first_row, second_row = first_rows.get(variant, {}), second_rows.get(variant, {})
        first_set = first_row.get("fully_adequate_candidates", [])
        second_set = second_row.get("fully_adequate_candidates", [])
        passed = (
            first_row.get("adequacy_outcome") == "SINGLETON"
            and second_row.get("adequacy_outcome") == "SINGLETON"
            and first_set == [gold_label]
            and second_set == [gold_label]
        )
        rows.append(
            {
                "variant": variant,
                "sealed_gold_label": gold_label,
                "first_adequacy_outcome": first_row.get("adequacy_outcome"),
                "first_fully_adequate_candidates": first_set,
                "second_adequacy_outcome": second_row.get("adequacy_outcome"),
                "second_fully_adequate_candidates": second_set,
                "strict_singleton_preserved": passed,
            }
        )
    reviews_valid = True
    passed = reviews_valid and all(row["strict_singleton_preserved"] for row in rows)
    payload = {
        "status": (
            "RQ1B_FIELD_TYPE_V2_FULL_CARD_PRESERVATION_PASS_NOT_A_SELECTOR_RESULT"
            if passed
            else "RQ1B_FIELD_TYPE_V2_FULL_CARD_PRESERVATION_FAIL_NOT_A_SELECTOR_RESULT"
        ),
        "routing_family_id": args.routing_family_id,
        "composition_id": family["composition_id"],
        "packet_id": packet_id,
        "packet_sha256": packet_sha256,
        "sealed_gold_label": gold_label,
        "first_reviewer": args.first_reviewer,
        "second_reviewer": args.second_reviewer,
        "both_reviews_schema_valid": reviews_valid,
        "first_audit_sha256": audit_hashes[args.first_reviewer],
        "second_audit_sha256": audit_hashes[args.second_reviewer],
        "first_response_sha256": response_hashes[args.first_reviewer],
        "second_response_sha256": response_hashes[args.second_reviewer],
        "variant_rows": rows,
        "strict_singleton_preserved": passed,
        "exclusions": [
            "No field attribution, masked-field effect, selector, embedding, retrieval, score, metric, API call, or result exists.",
        ],
    }
    output = root / "preservation_ledger" / f"{args.routing_family_id}.json"
    write_json(output, payload)
    print({"routing_family_id": args.routing_family_id, "strict_singleton_preserved": passed, "output": str(output)})


if __name__ == "__main__":
    main()
