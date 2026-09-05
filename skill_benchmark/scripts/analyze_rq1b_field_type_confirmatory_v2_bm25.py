#!/usr/bin/env python3
"""Produce residual-stratified local analysis for a completed RQ1b v2 BM25 run."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq1b_field_type_confirmatory_v2_common import FIELDS, load_list
from run_rq1b_field_type_confirmatory_v2_bm25 import FIELD_CONDITIONS, bootstrap_mean, load_strict_families


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def residual_labels(root: Path) -> dict[tuple[str, str, str], str]:
    packet_by_composition = {
        row["composition_id"]: row["packet_id"]
        for row in load_list(root / "residual_packet_private_map.json")
    }
    labels: dict[tuple[str, str, str], str] = {}
    for composition_id, packet_id in packet_by_composition.items():
        payload = json.loads((root / "residual_ledger_opaque" / f"{packet_id}.json").read_text())
        if payload.get("packet_id") != packet_id:
            raise ValueError(f"residual packet binding invalid: {composition_id}")
        for row in payload.get("rows", []):
            candidate, field, label = row.get("candidate"), row.get("field"), row.get("residual_label")
            if field not in FIELDS or label not in {"none", "partial", "substantial", "disagreed"}:
                raise ValueError(f"residual row invalid: {packet_id}")
            key = (composition_id, candidate, field)
            if key in labels:
                raise ValueError(f"duplicate residual row: {key}")
            labels[key] = label
    return labels


def block(pairs: list[dict[str, Any]], seed: int) -> dict[str, Any]:
    if not pairs:
        return {"routing_family_count": 0, "prompt_pair_count": 0, "composition_count": 0}
    family_ids = {pair["family_id"] for pair in pairs}
    per_composition: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    transitions = Counter()
    winner_changes = Counter()
    for pair in pairs:
        full, masked = pair["full"], pair["masked"]
        transitions[f"{full['hit_at_1']}_to_{masked['hit_at_1']}"] += 1
        if full["winner_label"] != masked["winner_label"]:
            winner_changes[f"{full['winner_label']}->{masked['winner_label']}"] += 1
        for metric, value in {
            "top1": full["hit_at_1"] - masked["hit_at_1"],
            "mrr": full["mrr"] - masked["mrr"],
            "margin": full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"],
        }.items():
            per_composition[pair["composition_id"]][metric].append(value)
    aggregate = {
        metric: {composition: sum(values[metric]) / len(values[metric]) for composition, values in per_composition.items()}
        for metric in ("top1", "mrr", "margin")
    }
    return {
        "routing_family_count": len(family_ids),
        "prompt_pair_count": len(pairs),
        "composition_count": len(per_composition),
        "top1_full_minus_mask": bootstrap_mean(aggregate["top1"], seed),
        "mrr_full_minus_mask": bootstrap_mean(aggregate["mrr"], seed + 1000),
        "margin_full_minus_mask": bootstrap_mean(aggregate["margin"], seed + 2000),
        "top1_transition_counts": dict(sorted(transitions.items())),
        "winner_change_count": sum(winner_changes.values()),
        "winner_change_pairs": dict(winner_changes.most_common()),
    }


def markdown(analysis: dict[str, Any], selector_label: str) -> str:
    lines = [f"# RQ1b v2 {selector_label} Failure And Residual-Stratum Analysis", "", f"This is a completed {selector_label} result analysis. It does not create a thesis claim.", "", "| Field | Families | Prompts | FULL-MASK Top-1 (95% cluster CI) | FULL-MASK MRR (95% cluster CI) | FULL-correct to masked-wrong | Low-residual families |", "|---|---:|---:|---:|---:|---:|---:|"]
    for field, value in analysis["fields"].items():
        all_block = value["all_eligible"]
        low = value["none_or_partial"]
        top1 = all_block["top1_full_minus_mask"]
        mrr = all_block["mrr_full_minus_mask"]
        loss = all_block["top1_transition_counts"].get("1_to_0", 0)
        lines.append(
            f"| {field} | {all_block['routing_family_count']} | {all_block['prompt_pair_count']} | "
            f"{top1['mean']:.3f} [{top1['ci95'][0]:.3f}, {top1['ci95'][1]:.3f}] | "
            f"{mrr['mean']:.3f} [{mrr['ci95'][0]:.3f}, {mrr['ci95'][1]:.3f}] | "
            f"{loss}/{all_block['prompt_pair_count']} | {low['routing_family_count']} |"
        )
    lines.extend(["", "Positive differences mean the full card outperformed the corresponding all-candidate mask. The low-residual stratum retains only gold-field labels with residual `none` or `partial`; it is descriptive because public cards naturally repeat information across slots.", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--selector-label", default="BM25")
    args = parser.parse_args()
    rows_path = args.output_dir / "rows.jsonl"
    rows = [json.loads(line) for line in rows_path.read_text().splitlines() if line]
    by_key = {(row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    families, eligible = load_strict_families(args.root)
    residual = residual_labels(args.root)
    family_by_id = {family["routing_family_id"]: family for family in families}
    result: dict[str, Any] = {
        "status": f"RQ1B_FIELD_TYPE_V2_{args.selector_label.upper().replace(' ', '_')}_FAILURE_AND_RESIDUAL_ANALYSIS_LOCAL_RESULT",
        "scope": "post-score descriptive analysis; no new selector execution",
        "rows_sha256": sha256_file(rows_path),
        "fields": {},
    }
    for offset, field in enumerate(FIELDS, start=1):
        condition = FIELD_CONDITIONS[field]
        pairs, low_residual_pairs, labels = [], [], Counter()
        for family_id in sorted(eligible[field]):
            family = family_by_id[family_id]
            label = residual[(family["composition_id"], family["gold_label"], field)]
            labels[label] += 1
            for variant in ("direct", "paraphrase"):
                pair = {
                    "family_id": family_id,
                    "composition_id": family["composition_id"],
                    "full": by_key[(family_id, variant, "FULL")],
                    "masked": by_key[(family_id, variant, condition)],
                }
                pairs.append(pair)
                if label in {"none", "partial"}:
                    low_residual_pairs.append(pair)
        result["fields"][field] = {
            "condition": condition,
            "gold_residual_label_counts": dict(sorted(labels.items())),
            "all_eligible": block(pairs, 20262000 + offset),
            "none_or_partial": block(low_residual_pairs, 20263000 + offset),
        }
    (args.output_dir / "failure_and_residual_analysis.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (args.output_dir / "failure_and_residual_analysis.md").write_text(markdown(result, args.selector_label))
    print(json.dumps({"valid": True, "fields": {field: value["all_eligible"]["routing_family_count"] for field, value in result["fields"].items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
