#!/usr/bin/env python3
"""Summarise RQ1b confirmatory source-card construction without scoring.

The report applies the frozen B1-then-B2 literal-valid rule and explicitly
retains invalid/pending builder records. It never constructs a card or a mask.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def audit_valid(root: Path, family_id: str, reviewer: str) -> bool | None:
    path = root / "audits" / f"{family_id}_{reviewer}_literal_audit.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text()).get("valid") is True
    except Exception:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    manifest = json.loads((root / "source_card_builder_manifest.json").read_text())
    families = []
    for item in manifest:
        family_id = item["family_id"]
        b1 = audit_valid(root, family_id, "b1")
        b2 = audit_valid(root, family_id, "b2")
        if b1 is True:
            status = "READY_CANONICAL_B1"
        elif b2 is True:
            status = "READY_CANONICAL_B2"
        elif b1 is False and b2 is False:
            status = "NO_LITERAL_VALID_CARD_RETAIN_FAILURE_RECORDS"
        else:
            status = "PENDING_TWO_INDEPENDENT_LITERAL_AUDITS"
        families.append({"family_id": family_id, "b1_literal_valid": b1, "b2_literal_valid": b2, "status": status})
    counts = {}
    for row in families:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_CARD_CONSTRUCTION_PROGRESS_NOT_A_RESULT",
        "canonical_rule": "B1 if literal-valid, otherwise B2 if literal-valid, otherwise no card",
        "counts": counts,
        "families": families,
        "exclusions": ["No card, mask, prompt, gold label, selector, embedding, retrieval score, metric, API call, or result is created."],
    }
    output = root / "audits" / "card_construction_progress.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"counts": counts, "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
