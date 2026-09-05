#!/usr/bin/env python3
"""Audit one source-only RQ1b v2 surface-cue repair builder response."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    FIELDS,
    card_surface_cue_violations,
    load_object,
    sha256_file,
    write_json,
)


NO_SAFE_ALTERNATIVE = "NO_SAFE_ALTERNATIVE"


def cue_free(candidate: str, field: str, quotes: list[str]) -> bool:
    cards = {candidate: {field: {"status": "EVIDENCE", "quotes": quotes}}}
    # Fill the other slots only because the shared checker expects a full card.
    for name in FIELDS:
        cards[candidate].setdefault(name, {"status": "NOT_STATED", "quotes": []})
    return not card_surface_cue_violations(cards)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--composition-id", required=True)
    parser.add_argument("--builder", required=True)
    args = parser.parse_args()
    root = args.root
    packet = load_object(root / "surface_cue_repair_packets" / f"{args.composition_id}.json")
    response_path = root / "surface_cue_repair_responses" / args.builder / f"{args.composition_id}.json"
    failures, safe_updates, unresolved = [], [], []
    expected = {
        (row.get("candidate"), row.get("field"))
        for row in packet.get("targets", [])
        if isinstance(row, dict)
    }
    if packet.get("composition_id") != args.composition_id or not expected or len(expected) != len(packet.get("targets", [])):
        failures.append("repair_packet_target_schema_invalid")
    try:
        response = load_object(response_path)
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("composition_id") != args.composition_id:
        failures.append("composition_id_mismatch")
    rows = response.get("replacements") if isinstance(response.get("replacements"), list) else []
    seen = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"replacement_not_object:{index}")
            continue
        key = (row.get("candidate"), row.get("field"))
        if key not in expected:
            failures.append(f"unknown_repair_target:{index}")
        if key in seen:
            failures.append(f"duplicate_repair_target:{index}")
        seen.add(key)
        replacement = row.get("replacement")
        if replacement == NO_SAFE_ALTERNATIVE or replacement == [NO_SAFE_ALTERNATIVE]:
            unresolved.append({"candidate": key[0], "field": key[1], "reason": row.get("reason")})
        elif not isinstance(replacement, list) or not replacement or any(not isinstance(quote, str) or not quote for quote in replacement):
            failures.append(f"invalid_replacement_value:{index}")
        else:
            source_path = root / args.composition_id / "sources" / f"{str(key[0]).replace(' ', '_')}.md"
            if not source_path.is_file():
                failures.append(f"anonymous_source_missing:{index}")
            else:
                source_text = source_path.read_text()
                for quote_index, quote in enumerate(replacement):
                    if quote not in source_text:
                        failures.append(f"replacement_not_exact_source_substring:{index}:{quote_index}")
                if not cue_free(key[0], key[1], replacement):
                    failures.append(f"replacement_contains_surface_cue:{index}")
                safe_updates.append({"candidate": key[0], "field": key[1], "quotes": replacement})
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            failures.append(f"invalid_reason:{index}")
    if seen != expected:
        failures.append("repair_target_set_mismatch")
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_SOURCE_ONLY_SURFACE_CUE_REPAIR_AUDIT_NOT_A_RESULT",
        "composition_id": args.composition_id,
        "builder": args.builder,
        "response_sha256": sha256_file(response_path) if response_path.is_file() else None,
        "schema_and_literal_valid": not failures,
        "complete_literal_safe_repair": not failures and not unresolved and len(safe_updates) == len(expected),
        "failures": failures,
        "unresolved": unresolved,
        "safe_updates": safe_updates,
        "exclusions": [
            "No prompt, gold label, provenance, mask, selector, embedding, retrieval, score, metric, API call, or result is used or produced.",
        ],
    }
    write_json(root / "audits" / f"{args.composition_id}_{args.builder}_surface_cue_repair_audit.json", payload)
    print({"composition_id": args.composition_id, "builder": args.builder, "complete_literal_safe_repair": payload["complete_literal_safe_repair"]})
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
