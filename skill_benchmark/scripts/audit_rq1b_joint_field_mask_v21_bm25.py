#!/usr/bin/env python3
"""Audit completed local RQ1b v2.1 joint-mask BM25 output."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from prepare_rq1b_joint_field_mask_v21 import CONDITIONS, GROUPS, load_joint_scope


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    _, _, families, eligible = load_joint_scope(args.root)
    manifest = json.loads((args.output_dir / "manifest.json").read_text())
    summary = json.loads((args.output_dir / "summary.json").read_text())
    rows = [json.loads(line) for line in (args.output_dir / "rows.jsonl").read_text().splitlines() if line]
    if manifest.get("status") != "RQ1B_JOINT_FIELD_MASK_V21_BM25_LOCAL_RUN_MANIFEST" or manifest.get("network_calls") != 0 or manifest.get("texts_transmitted") != 0:
        raise ValueError("joint BM25 manifest scope mismatch")
    for artifact in ("rows.jsonl", "summary.json"):
        if manifest.get("artifacts", {}).get(artifact) != sha256_file(args.output_dir / artifact):
            raise ValueError(f"joint BM25 artifact hash mismatch: {artifact}")
    expected = {(family["routing_family_id"], variant, condition) for family in families for variant in ("direct", "paraphrase") for condition in CONDITIONS}
    actual = {(row.get("routing_family_id"), row.get("prompt_variant"), row.get("condition")) for row in rows}
    if actual != expected or len(rows) != len(expected):
        raise ValueError("joint BM25 row coverage mismatch")
    for row in rows:
        ranking = row.get("ranking")
        if not isinstance(ranking, list) or len(ranking) != row.get("candidate_count"):
            raise ValueError("joint BM25 ranking schema mismatch")
        labels = [item.get("label") for item in ranking]
        scores = [item.get("score") for item in ranking]
        if labels != sorted(labels, key=lambda label: (-scores[labels.index(label)], label)):
            raise ValueError("joint BM25 ranking order mismatch")
        if labels[row["gold_rank"] - 1] != row["gold_label"] or labels[0] != row["winner_label"]:
            raise ValueError("joint BM25 gold/winner binding mismatch")
    groups = summary.get("groups")
    if not isinstance(groups, dict) or set(groups) != set(GROUPS):
        raise ValueError("joint BM25 summary group coverage mismatch")
    for condition, fields in GROUPS.items():
        block = groups[condition]
        if block.get("withheld_fields") != list(fields) or block.get("routing_family_count") != len(eligible[condition]):
            raise ValueError(f"joint eligibility drift: {condition}")
        if block.get("prompt_pair_count") != len(eligible[condition]) * 2:
            raise ValueError(f"joint prompt denominator drift: {condition}")
    print(json.dumps({"valid": True, "rows": len(rows), "strict_families": len(families), "group_eligible_families": {condition: len(ids) for condition, ids in eligible.items()}, "network_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
