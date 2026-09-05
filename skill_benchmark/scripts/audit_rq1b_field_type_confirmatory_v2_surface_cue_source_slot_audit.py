#!/usr/bin/env python3
"""Validate one independent source-only same-slot audit of B1/B2 repairs."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import load_object, sha256_file, write_json


NO_SAFE_ALTERNATIVE = "NO_SAFE_ALTERNATIVE"


def builder_replacements(
    root: Path,
    composition_id: str,
    builder: str,
    expected: set[tuple[str, str]],
) -> tuple[dict[tuple[str, str], list[str] | None], str]:
    path = root / "surface_cue_repair_responses" / builder / f"{composition_id}.json"
    response = load_object(path)
    if response.get("composition_id") != composition_id:
        raise ValueError(f"repair response composition mismatch: {builder}")
    rows = response.get("replacements")
    if not isinstance(rows, list):
        raise ValueError(f"repair response replacements missing: {builder}")
    values = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"repair response row invalid: {builder}")
        key = (row.get("candidate"), row.get("field"))
        value = row.get("replacement")
        if key not in expected or key in values:
            raise ValueError(f"repair response target invalid: {builder}")
        if value == NO_SAFE_ALTERNATIVE or value == [NO_SAFE_ALTERNATIVE]:
            values[key] = None
        elif isinstance(value, list) and value and all(isinstance(quote, str) and quote for quote in value):
            values[key] = value
        else:
            raise ValueError(f"repair response replacement invalid: {builder}")
    if set(values) != expected:
        raise ValueError(f"repair response target set mismatch: {builder}")
    return values, sha256_file(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--composition-id", required=True)
    args = parser.parse_args()
    root = args.root
    packet = load_object(root / "surface_cue_repair_packets" / f"{args.composition_id}.json")
    expected = {
        (item.get("candidate"), item.get("field"))
        for item in packet.get("targets", [])
        if isinstance(item, dict)
    }
    response_path = root / "surface_cue_repair_source_slot_audits" / f"{args.composition_id}.json"
    failures = []
    try:
        response = load_object(response_path)
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("composition_id") != args.composition_id:
        failures.append("composition_id_mismatch")
    builder_rows = response.get("builders") if isinstance(response.get("builders"), list) else []
    by_builder = {}
    for item in builder_rows:
        if not isinstance(item, dict) or item.get("builder") not in {"b1", "b2"} or item.get("builder") in by_builder:
            failures.append("invalid_or_duplicate_builder_row")
            continue
        by_builder[item["builder"]] = item
    if set(by_builder) != {"b1", "b2"}:
        failures.append("builder_set_mismatch")
    decisions, repair_hashes = {}, {}
    builder_failures = {"b1": [], "b2": []}
    for builder in ("b1", "b2"):
        try:
            replacements, repair_hashes[builder] = builder_replacements(root, args.composition_id, builder, expected)
        except Exception as error:
            replacements, repair_hashes[builder] = {}, None
            builder_failures[builder].append(f"repair_response_binding_invalid:{error}")
        item = by_builder.get(builder, {})
        rows = item.get("per_target") if isinstance(item.get("per_target"), list) else []
        seen = set()
        all_preserved = True
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                builder_failures[builder].append(f"target_row_invalid:{index}")
                continue
            key = (row.get("candidate"), row.get("field"))
            if key not in expected or key in seen:
                builder_failures[builder].append(f"target_binding_invalid:{index}")
            seen.add(key)
            preserved = row.get("same_slot_preserved")
            if not isinstance(preserved, bool):
                builder_failures[builder].append(f"same_slot_preserved_invalid:{index}")
                preserved = False
            if not isinstance(row.get("reason"), str) or not row["reason"].strip():
                builder_failures[builder].append(f"reason_invalid:{index}")
            if preserved:
                source_path = root / args.composition_id / "sources" / f"{str(key[0]).replace(' ', '_')}.md"
                basis = row.get("field_role_basis")
                if not isinstance(basis, list) or not basis or any(not isinstance(quote, str) or not quote or quote not in source_path.read_text() for quote in basis):
                    builder_failures[builder].append(f"field_role_basis_not_exact_source:{index}")
                replacement = replacements.get(key)
                if not replacement or not any(quote in candidate_quote for quote in basis for candidate_quote in replacement):
                    builder_failures[builder].append(f"field_role_basis_not_bound_to_builder_replacement:{index}")
                all_preserved = all_preserved and True
            else:
                all_preserved = False
        if seen != expected:
            builder_failures[builder].append("target_set_mismatch")
        decisions[builder] = all_preserved and seen == expected and not builder_failures[builder]
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_SOURCE_ONLY_REPAIR_SLOT_AUDIT_NOT_A_RESULT",
        "composition_id": args.composition_id,
        "response_sha256": sha256_file(response_path) if response_path.is_file() else None,
        "b1_repair_response_sha256": repair_hashes.get("b1"),
        "b2_repair_response_sha256": repair_hashes.get("b2"),
        "valid": not failures,
        "builder_valid": {builder: not issues for builder, issues in builder_failures.items()},
        "builder_slot_preserved": decisions,
        "builder_validation_failures": builder_failures,
        "failures": failures,
        "exclusions": [
            "No prompt, gold label, provenance, mask, selector, embedding, retrieval, score, metric, API call, or result is used or produced.",
        ],
    }
    write_json(root / "audits" / f"{args.composition_id}_surface_cue_source_slot_audit.json", payload)
    print({"composition_id": args.composition_id, "valid": payload["valid"], "builder_slot_preserved": decisions})
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
