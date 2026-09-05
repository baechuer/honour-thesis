#!/usr/bin/env python3
"""Run the prospective RQ1b v2.1 joint field-set mask experiment locally."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from prepare_rq1b_joint_field_mask_v21 import CONDITIONS, GROUPS, load_joint_condition, load_joint_scope
from run_rq1b_field_type_confirmatory_v2_bm25 import BM25, bootstrap_mean, metric_for_ranking, render_card


RUNNER_VERSION = "rq1b-joint-field-mask-v21-bm25-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(rows: list[dict[str, Any]], eligible: dict[str, set[str]]) -> dict[str, Any]:
    by_key = {(row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    groups: dict[str, Any] = {}
    for position, condition in enumerate(GROUPS, start=1):
        pairs = []
        for family_id in sorted(eligible[condition]):
            for variant in ("direct", "paraphrase"):
                full = by_key[(family_id, variant, "FULL")]
                masked = by_key[(family_id, variant, condition)]
                pairs.append({"family_id": family_id, "composition_id": full["composition_id"], "full": full, "masked": masked})
        if not pairs:
            raise ValueError(f"empty eligible pair set: {condition}")
        by_composition: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        transitions = Counter()
        for pair in pairs:
            full, masked = pair["full"], pair["masked"]
            transitions[f"{full['hit_at_1']}_to_{masked['hit_at_1']}"] += 1
            for metric, value in {
                "top1": full["hit_at_1"] - masked["hit_at_1"],
                "mrr": full["mrr"] - masked["mrr"],
                "margin": full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"],
            }.items():
                by_composition[pair["composition_id"]][metric].append(value)
        aggregate = {
            metric: {composition: statistics.mean(values[metric]) for composition, values in by_composition.items()}
            for metric in ("top1", "mrr", "margin")
        }
        groups[condition] = {
            "withheld_fields": list(GROUPS[condition]),
            "routing_family_count": len(eligible[condition]),
            "prompt_pair_count": len(pairs),
            "full": {
                "top1": statistics.mean(pair["full"]["hit_at_1"] for pair in pairs),
                "mrr": statistics.mean(pair["full"]["mrr"] for pair in pairs),
                "mean_gold_rank": statistics.mean(pair["full"]["gold_rank"] for pair in pairs),
                "mean_margin": statistics.mean(pair["full"]["gold_minus_best_wrong_margin"] for pair in pairs),
            },
            "masked": {
                "top1": statistics.mean(pair["masked"]["hit_at_1"] for pair in pairs),
                "mrr": statistics.mean(pair["masked"]["mrr"] for pair in pairs),
                "mean_gold_rank": statistics.mean(pair["masked"]["gold_rank"] for pair in pairs),
                "mean_margin": statistics.mean(pair["masked"]["gold_minus_best_wrong_margin"] for pair in pairs),
            },
            "full_correct_to_masked_wrong_rate": statistics.mean(
                pair["full"]["hit_at_1"] == 1 and pair["masked"]["hit_at_1"] == 0 for pair in pairs
            ),
            "transition_counts": dict(sorted(transitions.items())),
            "composition_bootstrap_full_minus_mask": {
                "top1": bootstrap_mean(aggregate["top1"], 20260860 + position),
                "mrr": bootstrap_mean(aggregate["mrr"], 20260960 + position),
                "margin": bootstrap_mean(aggregate["margin"], 20261060 + position),
            },
        }
    return {
        "status": "RQ1B_JOINT_FIELD_MASK_V21_BM25_SUMMARY_LOCAL_RESULT",
        "retriever": "bm25",
        "analysis_unit": "routing-family prompt outcomes retained; inference aggregates direct/paraphrase outcomes within candidate composition",
        "groups": groups,
    }


def run(root: Path, output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite output directory: {output_dir}")
    freeze, source_root, families, eligible = load_joint_scope(root)
    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for family in families:
        labels_by_condition: dict[str, set[str]] = {}
        for condition in CONDITIONS:
            cards = load_joint_condition(root, freeze, family["composition_id"], condition)
            labels = [card["label"] for card in cards]
            labels_by_condition[condition] = set(labels)
            index = BM25(labels, [render_card(card["slots"]) for card in cards])
            for variant, prompt in family["prompts"].items():
                begun = time.perf_counter()
                ranking = index.rank(prompt)
                rows.append(
                    {
                        "status": "RQ1B_JOINT_FIELD_MASK_V21_BM25_ROW_LOCAL_RESULT",
                        "routing_family_id": family["routing_family_id"],
                        "composition_id": family["composition_id"],
                        "prompt_variant": variant,
                        "condition": condition,
                        "gold_label": family["gold_label"],
                        "candidate_count": len(labels),
                        "query_seconds": time.perf_counter() - begun,
                        **metric_for_ranking(ranking, family["gold_label"]),
                    }
                )
        if len(set(map(frozenset, labels_by_condition.values()))) != 1:
            raise ValueError(f"candidate membership drift: {family['composition_id']}")
    expected_rows = len(families) * 2 * len(CONDITIONS)
    if len(rows) != expected_rows or len({(row["routing_family_id"], row["prompt_variant"], row["condition"]) for row in rows}) != expected_rows:
        raise ValueError("joint BM25 row coverage mismatch")
    summary = summarize(rows, eligible)
    manifest = {
        "status": "RQ1B_JOINT_FIELD_MASK_V21_BM25_LOCAL_RUN_MANIFEST",
        "runner_version": RUNNER_VERSION,
        "network_calls": 0,
        "texts_transmitted": 0,
        "thesis_results_written": False,
        "joint_root": str(root),
        "source_v2_root": str(source_root),
        "inputs": {"joint_mask_freeze.json": sha256_file(root / "joint_mask_freeze.json")},
        "configuration": {
            "scope": "per-composition candidate set only",
            "conditions": list(CONDITIONS),
            "groups": {condition: list(fields) for condition, fields in GROUPS.items()},
            "tie_break": "candidate_label_ascending",
        },
        "counts": {"strict_routing_families": len(families), "prompt_variants": len(families) * 2, "condition_rows": len(rows)},
        "timing": {"wall_seconds": time.perf_counter() - started, "query_seconds": sum(row["query_seconds"] for row in rows)},
    }
    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        (staging / "rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
        (staging / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        manifest["artifacts"] = {"rows.jsonl": sha256_file(staging / "rows.jsonl"), "summary.json": sha256_file(staging / "summary.json")}
        (staging / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
