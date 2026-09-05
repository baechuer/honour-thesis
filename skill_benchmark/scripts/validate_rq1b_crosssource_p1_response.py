#!/usr/bin/env python3
"""Validate literal source evidence in a blind RQ1b P1 mapper response."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CARRIERS = {
    "title_heading",
    "description",
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
    "example",
    "resource_reference",
}
CLASSIFICATIONS = {
    "differential_target_field",
    "shared_non_target",
    "inseparable_structural_cue",
}


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_rq1b_crosssource_p1_response.py RESPONSE.json")
    response_path = Path(sys.argv[1])
    family_dir = response_path.parents[2] / response_path.stem
    packet = json.loads((family_dir / "p1_evidence_mapping_packet.json").read_text())
    response = json.loads(response_path.read_text())
    failures = []
    if response.get("family_id") != packet.get("family_id"):
        failures.append("family_id_mismatch")
    if response.get("locked_primary_field") != packet.get("locked_primary_field"):
        failures.append("locked_primary_field_mismatch")
    candidate_text = {
        candidate["label"]: (family_dir / candidate["text_path"]).read_text()
        for candidate in packet["candidates"]
    }
    maps = response.get("candidate_maps")
    if not isinstance(maps, dict):
        failures.append("candidate_maps_missing")
        maps = {}
    if set(maps) != set(candidate_text):
        failures.append("candidate_map_labels_mismatch")
    for label, entries in maps.items():
        if label not in candidate_text:
            continue
        if not isinstance(entries, list):
            failures.append(f"entries_not_list:{label}")
            continue
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                failures.append(f"entry_not_object:{label}:{index}")
                continue
            quote = entry.get("quote")
            if not isinstance(quote, str) or quote not in candidate_text[label]:
                failures.append(f"quote_not_exact:{label}:{index}")
            if entry.get("carrier") not in CARRIERS:
                failures.append(f"invalid_carrier:{label}:{index}")
            if entry.get("classification") not in CLASSIFICATIONS:
                failures.append(f"invalid_classification:{label}:{index}")
            if entry.get("classification") == "differential_target_field" and not isinstance(entry.get("replacement"), (str, type(None))):
                failures.append(f"replacement_invalid:{label}:{index}")
    if failures:
        print(json.dumps({"status": "P1_RESPONSE_EVIDENCE_FAIL", "failures": failures}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"family_id": packet["family_id"], "status": "P1_RESPONSE_EVIDENCE_PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
