#!/usr/bin/env python3
"""Validate one P1/P2 evidence map and emit local audit data only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CARRIERS = {
    "title_heading", "description", "use_condition", "input_precondition",
    "output_artifact", "workflow_procedure", "boundary_not_for",
    "dependency_resource", "success_verification", "example", "resource_reference",
}
CLASSIFICATIONS = {
    "differential_target_field", "shared_non_target", "inseparable_structural_cue",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--family-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()

    family_dir = args.root / args.family_id
    packet = json.loads((family_dir / "p1_evidence_mapping_packet.json").read_text())
    response_path = args.root / "reviews" / args.reviewer / f"{args.family_id}.json"
    failures = []
    records = []
    try:
        response = json.loads(response_path.read_text())
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("family_id") != packet.get("family_id"):
        failures.append("family_id_mismatch")
    if response.get("locked_primary_field") != packet.get("locked_primary_field"):
        failures.append("locked_primary_field_mismatch")
    candidate_text = {
        item["label"]: (family_dir / item["text_path"]).read_text() for item in packet["candidates"]
    }
    maps = response.get("candidate_maps")
    if not isinstance(maps, dict) or set(maps) != set(candidate_text):
        failures.append("candidate_map_labels_mismatch")
        maps = maps if isinstance(maps, dict) else {}
    for label in candidate_text:
        entries = maps.get(label)
        if not isinstance(entries, list):
            failures.append(f"entries_not_list:{label}")
            continue
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                failures.append(f"entry_not_object:{label}:{index}")
                continue
            quote = entry.get("quote")
            if not isinstance(quote, str) or not quote or quote not in candidate_text[label]:
                failures.append(f"quote_not_exact:{label}:{index}")
            if entry.get("carrier") not in CARRIERS:
                failures.append(f"invalid_carrier:{label}:{index}")
            if entry.get("classification") not in CLASSIFICATIONS:
                failures.append(f"invalid_classification:{label}:{index}")
            if entry.get("classification") == "differential_target_field" and not isinstance(entry.get("replacement"), (str, type(None))):
                failures.append(f"replacement_invalid:{label}:{index}")
            records.append(
                {
                    "candidate": label,
                    "quote": quote,
                    "carrier": entry.get("carrier"),
                    "classification": entry.get("classification"),
                    "replacement": entry.get("replacement"),
                }
            )
    payload = {
        "status": "P1_P2_LITERAL_EVIDENCE_AUDIT_NOT_A_UNION_DECISION_OR_RESULT",
        "family_id": args.family_id,
        "reviewer": args.reviewer,
        "valid": not failures,
        "failures": failures,
        "entry_count": len(records),
        "records": records,
        "exclusions": [
            "No P1/P2 union decision is made by this audit.",
            "No mask, selector, embedding, retrieval, API call, metric, or result exists.",
        ],
    }
    output = args.root / "audits" / f"{args.family_id}_{args.reviewer}_audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "valid": payload["valid"], "entry_count": len(records)}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
