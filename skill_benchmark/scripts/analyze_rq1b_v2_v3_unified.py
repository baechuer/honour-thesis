#!/usr/bin/env python3
"""Produce the single final RQ1b V2+V3 field-removal experiment summary.

This is a local-only finaliser.  It treats the verified V2 and V3 rows as one
frozen 46-scored-composition, 99-family, 198-prompt experiment drawn from 52
frozen composition artifacts.  Source strata remain
in every row for provenance and heterogeneity audits, but are not separate
scientific estimators.  Paired field effects use composition-level bootstrap
resampling so direct/paraphrase variants and several routing families from one
candidate composition do not inflate the effective sample size.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30")
OUTPUT = Path("skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30")
CONDITIONS = (
    "FULL",
    "MASK_USE",
    "MASK_INPUT",
    "MASK_OUTPUT",
    "MASK_WORKFLOW",
    "MASK_SUCCESS",
    "MASK_BOUNDARY",
    "MASK_DEPENDENCY",
)
FIELDS = (
    ("use_condition", "MASK_USE"),
    ("input_precondition", "MASK_INPUT"),
    ("output_artifact", "MASK_OUTPUT"),
    ("workflow_procedure", "MASK_WORKFLOW"),
    ("success_verification", "MASK_SUCCESS"),
    ("boundary_not_for", "MASK_BOUNDARY"),
    ("dependency_resource", "MASK_DEPENDENCY"),
)
METHODS = ("bm25", "qwen")
EXPECTED = {"frozen_composition_artifacts": 52, "scored_compositions": 46, "families": 99, "prompts": 198, "rows": 1584}


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def percentile(values: list[float], level: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * level)))
    return ordered[index]


def bootstrap(values: dict[str, float], seed: int) -> dict[str, Any]:
    ids = sorted(values)
    sample_values = [values[item] for item in ids]
    generator = random.Random(seed)
    distribution = [statistics.mean(generator.choice(sample_values) for _ in sample_values) for _ in range(5000)]
    return {
        "composition_count": len(sample_values),
        "mean": statistics.mean(sample_values),
        "bootstrap_replicates": 5000,
        "bootstrap_seed": seed,
        "ci95": [percentile(distribution, 0.025), percentile(distribution, 0.975)],
    }


def condition_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_condition[row["condition"]].append(row)
    result: dict[str, dict[str, float | int]] = {}
    for condition in CONDITIONS:
        values = by_condition[condition]
        result[condition] = {
            "prompt_count": len(values),
            "top1": statistics.mean(row["hit_at_1"] for row in values),
            "mrr": statistics.mean(row["mrr"] for row in values),
            "mean_gold_rank": statistics.mean(row["gold_rank"] for row in values),
            "mean_gold_minus_best_wrong_margin": statistics.mean(row["gold_minus_best_wrong_margin"] for row in values),
        }
    return result


def field_effects(rows: list[dict[str, Any]], method_offset: int) -> dict[str, Any]:
    by_key = {(row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    effects: dict[str, Any] = {}
    for position, (field, condition) in enumerate(FIELDS, start=1):
        paired = []
        for family_id, variant, current in sorted(by_key):
            if current != "FULL":
                continue
            full = by_key[(family_id, variant, "FULL")]
            masked = by_key[(family_id, variant, condition)]
            paired.append((full, masked))
        composition_values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for full, masked in paired:
            values = composition_values[full["composition_id"]]
            values["top1"].append(full["hit_at_1"] - masked["hit_at_1"])
            values["mrr"].append(full["mrr"] - masked["mrr"])
            values["margin"].append(full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"])
        composition_means = {
            metric: {composition: statistics.mean(metric_values[metric]) for composition, metric_values in composition_values.items()}
            for metric in ("top1", "mrr", "margin")
        }
        effects[field] = {
            "condition": condition,
            "routing_family_count": len({full["routing_family_id"] for full, _ in paired}),
            "prompt_pair_count": len(paired),
            "full_correct_to_masked_wrong_rate": statistics.mean(
                full["hit_at_1"] == 1 and masked["hit_at_1"] == 0 for full, masked in paired
            ),
            "composition_bootstrap_full_minus_mask": {
                "top1": bootstrap(composition_means["top1"], 20300830 + method_offset + position),
                "mrr": bootstrap(composition_means["mrr"], 20310830 + method_offset + position),
                "margin": bootstrap(composition_means["margin"], 20320830 + method_offset + position),
            },
        }
    return effects


def validate(rows: list[dict[str, Any]], method: str) -> None:
    keys = {(row["routing_family_id"], row["prompt_variant"], row["condition"]) for row in rows}
    if len(rows) != EXPECTED["rows"] or len(keys) != EXPECTED["rows"]:
        raise ValueError(f"{method}: expected {EXPECTED['rows']} unique rows, received {len(rows)} / {len(keys)}")
    families = {row["routing_family_id"] for row in rows}
    compositions = {row["composition_id"] for row in rows}
    prompts = {(row["routing_family_id"], row["prompt_variant"]) for row in rows}
    if len(families) != EXPECTED["families"] or len(compositions) != EXPECTED["scored_compositions"] or len(prompts) != EXPECTED["prompts"]:
        raise ValueError(f"{method}: matrix cardinality mismatch")
    for family_id, variant in prompts:
        present = {row["condition"] for row in rows if row["routing_family_id"] == family_id and row["prompt_variant"] == variant}
        if present != set(CONDITIONS):
            raise ValueError(f"{method}: incomplete condition coverage for {family_id}/{variant}")
    strata = Counter(row.get("integration_stratum") for row in rows)
    if strata != Counter({"native_v2_reused": 1392, "imported_v3_new": 192}):
        raise ValueError(f"{method}: unexpected provenance strata: {strata}")


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# RQ1b V2+V3 Unified Final Result",
        "",
        "This is one frozen field-removal experiment: 46 scored candidate compositions drawn from 52 frozen composition artifacts, 99 strict routing families, 198 prompt instances and eight candidate-synchronous conditions. V2/V3 remain provenance tags only, not separate experimental denominators.",
        "",
        "## Full-Card Results",
        "",
        "| Retriever | Top-1 | MRR | Mean gold rank | Mean native margin |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for method in METHODS:
        values = result["retrievers"][method]["condition_metrics"]["FULL"]
        lines.append(f"| {method} | {values['top1']:.4f} | {values['mrr']:.4f} | {values['mean_gold_rank']:.4f} | {values['mean_gold_minus_best_wrong_margin']:.4f} |")
    lines += ["", "## Paired Field-Removal Effects", "", "Positive values mean that the complete card outperformed the candidate-synchronous field-masked card. Intervals are 5,000-replicate, composition-level paired bootstrap intervals.", ""]
    for method in METHODS:
        lines += [f"### {method}", "", "| Field removed | Full-minus-mask Top-1 (95% CI) | Full-minus-mask MRR (95% CI) | Full-correct to masked-wrong |", "| --- | ---: | ---: | ---: |"]
        for field, _ in FIELDS:
            value = result["retrievers"][method]["field_effects"][field]
            top1 = value["composition_bootstrap_full_minus_mask"]["top1"]
            mrr = value["composition_bootstrap_full_minus_mask"]["mrr"]
            lines.append(f"| {field} | {top1['mean']:.4f} [{top1['ci95'][0]:.4f}, {top1['ci95'][1]:.4f}] | {mrr['mean']:.4f} [{mrr['ci95'][0]:.4f}, {mrr['ci95'][1]:.4f}] | {value['full_correct_to_masked_wrong_rate']:.4f} |")
        lines.append("")
    lines += [
        "## Boundary",
        "",
        "The unified estimator tests candidate-synchronous removal of one field from all competing cards. It supports empirical comparisons of field availability in this frozen public-artifact corpus; it does not establish that a field is universally necessary, independent of all other card content, or causal outside these 46 scored compositions.",
        "",
    ]
    return "\n".join(lines)


def build() -> dict[str, Any]:
    retrievers: dict[str, Any] = {}
    for offset, method in enumerate(METHODS, start=1):
        rows = read_rows(ROOT / method / "combined_rows.jsonl")
        validate(rows, method)
        retrievers[method] = {
            "row_count": len(rows),
            "condition_metrics": condition_summary(rows),
            "field_effects": field_effects(rows, offset * 100),
        }
    return {
        "status": "RQ1B_V2_V3_UNIFIED_FINAL_LOCAL_ANALYSIS",
        "analysis_unit": "one frozen 46-scored-composition / 99-family / 198-prompt experiment drawn from 52 frozen composition artifacts; field effects use composition-level paired bootstrap",
        "provenance_note": "V2/V3 source tags are retained for integrity/heterogeneity audit only and are not separate main estimators.",
        "matrix": {**EXPECTED, "conditions": list(CONDITIONS)},
        "retrievers": retrievers,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.run == args.check:
        parser.error("choose exactly one of --run or --check")
    result = build()
    if args.check:
        saved = json.loads((OUTPUT / "summary.json").read_text())
        if saved != result:
            raise ValueError("saved unified analysis differs from recomputed analysis")
        print(json.dumps({"status": "PASS", "matrix": result["matrix"]}, sort_keys=True))
        return
    if OUTPUT.exists():
        raise ValueError(f"refusing to overwrite existing output: {OUTPUT}")
    OUTPUT.mkdir(parents=True)
    (OUTPUT / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (OUTPUT / "SUMMARY.md").write_text(render_markdown(result))
    print(json.dumps({"status": result["status"], "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
