#!/usr/bin/env python3
"""Audit a completed local RQ1b v2 BM25 run without modifying it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import FIELDS
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze
from run_rq1b_field_type_confirmatory_v2_bm25 import CONDITIONS, FIELD_CONDITIONS, load_strict_families


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root, output = args.root, args.output_dir
    verify_freeze(root)
    manifest = json.loads((output / "manifest.json").read_text())
    summary = json.loads((output / "summary.json").read_text())
    rows = [json.loads(line) for line in (output / "rows.jsonl").read_text().splitlines() if line]
    if manifest.get("network_calls") != 0 or manifest.get("texts_transmitted") != 0:
        raise ValueError("local BM25 manifest claims external activity")
    if manifest.get("artifacts", {}).get("rows.jsonl") != sha256_file(output / "rows.jsonl"):
        raise ValueError("rows hash mismatch")
    if manifest.get("artifacts", {}).get("summary.json") != sha256_file(output / "summary.json"):
        raise ValueError("summary hash mismatch")
    families, eligible = load_strict_families(root)
    expected = {(family["routing_family_id"], variant, condition) for family in families for variant in ("direct", "paraphrase") for condition in CONDITIONS}
    actual = {(row.get("routing_family_id"), row.get("prompt_variant"), row.get("condition")) for row in rows}
    if actual != expected or len(rows) != len(expected):
        raise ValueError(f"row coverage mismatch: expected {len(expected)}, found {len(rows)}")
    for row in rows:
        ranking = row.get("ranking")
        if not isinstance(ranking, list) or len(ranking) != row.get("candidate_count"):
            raise ValueError("ranking schema mismatch")
        labels = [item.get("label") for item in ranking]
        scores = [item.get("score") for item in ranking]
        if labels != sorted(labels, key=lambda label: (-scores[labels.index(label)], label)):
            raise ValueError("ranking order/tie break mismatch")
        if labels[row["gold_rank"] - 1] != row["gold_label"] or row["winner_label"] != labels[0]:
            raise ValueError("gold rank or winner binding mismatch")
    fields = summary.get("fields")
    if not isinstance(fields, dict) or set(fields) != set(FIELDS):
        raise ValueError("summary field coverage mismatch")
    for field in FIELDS:
        block = fields[field]
        if block.get("condition") != FIELD_CONDITIONS[field] or block.get("routing_family_count") != len(eligible[field]):
            raise ValueError(f"summary eligibility drift: {field}")
        if block.get("prompt_pair_count") != len(eligible[field]) * 2:
            raise ValueError(f"summary prompt count drift: {field}")
    print(json.dumps({"valid": True, "rows": len(rows), "strict_families": len(families), "field_counts": {field: len(ids) for field, ids in eligible.items()}, "network_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
