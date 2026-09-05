#!/usr/bin/env python3
"""Create the final RQ1b metric ledger from frozen local selector rows.

The ledger reports every routing metric needed to interpret the result: absolute
FULL/masked performance, raw paired prompt deltas, composition-level paired
bootstrap deltas, score margins, rank changes and Top-1 transition counts.
The V2+V3 single-field matrix is the primary experiment.  The older V2-only
three-group masks remain a separately labelled supporting analysis because V3
was not materialised under those three conditions.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark/outputs")
PRIMARY = ROOT / "field_type_ablation_confirmatory_v2_v3_extension_2026-08-30"
JOINT_FREEZE = Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_joint_mask_v21_2026-08-29/joint_mask_freeze.json")
GROUPS = {
    "task_specification": ("MASK_TASK_SPECIFICATION", ("use_condition", "input_precondition", "output_artifact")),
    "execution_verification": ("MASK_EXECUTION_VERIFICATION", ("workflow_procedure", "success_verification")),
    "applicability_capability": ("MASK_APPLICABILITY_CAPABILITY", ("boundary_not_for", "dependency_resource")),
}
FIELDS = {
    "use_condition": "MASK_USE",
    "input_precondition": "MASK_INPUT",
    "output_artifact": "MASK_OUTPUT",
    "workflow_procedure": "MASK_WORKFLOW",
    "success_verification": "MASK_SUCCESS",
    "boundary_not_for": "MASK_BOUNDARY",
    "dependency_resource": "MASK_DEPENDENCY",
}
OUTPUT = ROOT / "field_type_ablation_final_result_ledger_2026-08-30"
METHODS = ("bm25", "qwen")


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def percentile(values: list[float], level: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * level)))
    return ordered[index]


def bootstrap(values: dict[str, float], seed: int) -> dict[str, Any]:
    ids = sorted(values)
    source = [values[item] for item in ids]
    generator = random.Random(seed)
    samples = [statistics.mean(generator.choice(source) for _ in source) for _ in range(5000)]
    return {
        "composition_count": len(source),
        "mean": statistics.mean(source),
        "bootstrap_replicates": 5000,
        "bootstrap_seed": seed,
        "ci95": [percentile(samples, 0.025), percentile(samples, 0.975)],
    }


def metric_mean(rows: list[dict[str, Any]], name: str) -> float:
    return statistics.mean(row[name] for row in rows)


def paired_metrics(rows: list[dict[str, Any]], condition: str, seed: int, eligible_family_ids: set[str] | None = None) -> dict[str, Any]:
    by_key = {(r["routing_family_id"], r["prompt_variant"], r["condition"]): r for r in rows}
    prompt_pairs = []
    for family_id, variant, state in sorted(by_key):
        if state != "FULL" or (eligible_family_ids is not None and family_id not in eligible_family_ids):
            continue
        full = by_key[(family_id, variant, "FULL")]
        masked = by_key[(family_id, variant, condition)]
        prompt_pairs.append((full, masked))
    if not prompt_pairs:
        raise ValueError(f"empty comparison: {condition}")
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    transitions = Counter()
    for full, masked in prompt_pairs:
        values = grouped[full["composition_id"]]
        values["top1"].append(full["hit_at_1"] - masked["hit_at_1"])
        values["mrr"].append(full["mrr"] - masked["mrr"])
        values["margin"].append(full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"])
        values["rank_worsening"].append(masked["gold_rank"] - full["gold_rank"])
        transitions[f"{full['hit_at_1']}_to_{masked['hit_at_1']}"] += 1
    composition_means = {
        metric: {composition: statistics.mean(value[metric]) for composition, value in grouped.items()}
        for metric in ("top1", "mrr", "margin", "rank_worsening")
    }
    full_rows = [full for full, _ in prompt_pairs]
    masked_rows = [masked for _, masked in prompt_pairs]
    return {
        "condition": condition,
        "composition_count": len(grouped),
        "routing_family_count": len({full["routing_family_id"] for full, _ in prompt_pairs}),
        "prompt_pair_count": len(prompt_pairs),
        "absolute_prompt_metrics": {
            "full": {
                "top1": metric_mean(full_rows, "hit_at_1"),
                "mrr": metric_mean(full_rows, "mrr"),
                "mean_gold_rank": metric_mean(full_rows, "gold_rank"),
                "mean_margin": metric_mean(full_rows, "gold_minus_best_wrong_margin"),
            },
            "masked": {
                "top1": metric_mean(masked_rows, "hit_at_1"),
                "mrr": metric_mean(masked_rows, "mrr"),
                "mean_gold_rank": metric_mean(masked_rows, "gold_rank"),
                "mean_margin": metric_mean(masked_rows, "gold_minus_best_wrong_margin"),
            },
        },
        "raw_prompt_full_minus_mask": {
            "top1": metric_mean(full_rows, "hit_at_1") - metric_mean(masked_rows, "hit_at_1"),
            "mrr": metric_mean(full_rows, "mrr") - metric_mean(masked_rows, "mrr"),
            "margin": metric_mean(full_rows, "gold_minus_best_wrong_margin") - metric_mean(masked_rows, "gold_minus_best_wrong_margin"),
            "rank_worsening": metric_mean(masked_rows, "gold_rank") - metric_mean(full_rows, "gold_rank"),
        },
        "composition_bootstrap_full_minus_mask": {
            "top1": bootstrap(composition_means["top1"], seed + 1),
            "mrr": bootstrap(composition_means["mrr"], seed + 2),
            "margin": bootstrap(composition_means["margin"], seed + 3),
            "rank_worsening": bootstrap(composition_means["rank_worsening"], seed + 4),
        },
        "transition_counts": dict(sorted(transitions.items())),
        "full_correct_to_masked_wrong_rate": transitions["1_to_0"] / len(prompt_pairs),
        "full_wrong_to_masked_correct_rate": transitions["0_to_1"] / len(prompt_pairs),
    }


def validate_primary(rows: list[dict[str, Any]]) -> None:
    keys = {(r["routing_family_id"], r["prompt_variant"], r["condition"]) for r in rows}
    if len(rows) != 1584 or len(keys) != 1584:
        raise ValueError("primary unified row coverage invalid")
    if len({r["composition_id"] for r in rows}) != 46 or len({r["routing_family_id"] for r in rows}) != 99:
        raise ValueError("primary unified denominator invalid")
    if Counter(r.get("integration_stratum") for r in rows) != Counter({"native_v2_reused": 1392, "imported_v3_new": 192}):
        raise ValueError("primary provenance coverage invalid")


def build() -> dict[str, Any]:
    primary: dict[str, Any] = {}
    joint_groups: dict[str, Any] = {}
    joint_freeze = json.loads(JOINT_FREEZE.read_text())
    eligible = {condition: set(ids) for condition, ids in joint_freeze["group_eligible_routing_family_ids"].items()}
    for method_index, method in enumerate(METHODS, start=1):
        rows = read_rows(PRIMARY / method / "combined_rows.jsonl")
        validate_primary(rows)
        primary[method] = {
            "full_card": paired_metrics(rows, "FULL", 20400000 + method_index * 1000),
            "single_field_masks": {
                field: paired_metrics(rows, condition, 20410000 + method_index * 1000 + position)
                for position, (field, condition) in enumerate(FIELDS.items(), start=1)
            },
        }
        group_rows = read_rows(ROOT / f"field_type_joint_mask_v21_{method}_2026-08-29" / "rows.jsonl")
        joint_groups[method] = {
            "scope": "V2-only supporting analysis; group eligibility intersections differ by group and V3 was not scored under these three masks.",
            "groups": {
                group: {
                    "withheld_fields": list(fields),
                    "eligible_family_ids": sorted(eligible[condition]),
                    **paired_metrics(group_rows, condition, 20420000 + method_index * 1000 + position, eligible[condition]),
                }
                for position, (group, (condition, fields)) in enumerate(GROUPS.items(), start=1)
            },
        }
    return {
        "status": "RQ1B_FINAL_RESULT_LEDGER_LOCAL_ONLY",
        "primary_experiment": {
            "definition": "one V2+V3 candidate-synchronous single-field-removal experiment",
            "frozen_composition_artifacts": 52,
            "scored_compositions": 46,
            "strict_routing_families": 99,
            "prompt_instances": 198,
            "conditions": ["FULL", *FIELDS.values()],
            "row_count_per_retriever": 1584,
        },
        "primary_single_field": primary,
        "v2_joint_group_supporting_analysis": joint_groups,
        "claim_boundary": "Point estimates, raw transitions and margin changes are reported in full. Composition-level bootstrap CIs determine whether the field-removal accuracy evidence is stable at the composition unit.",
    }


def ci(metric: dict[str, Any]) -> str:
    return f"{metric['mean']:.4f} [{metric['ci95'][0]:.4f}, {metric['ci95'][1]:.4f}]"


def render_section(lines: list[str], title: str, values: dict[str, Any]) -> None:
    lines.extend([f"## {title}", ""])
    for method in METHODS:
        lines.extend([f"### {method}", "", "| Removal | Prompt pairs | FULL -> masked Top-1 | Raw dTop-1 | Composition dTop-1 (95% CI) | Raw dMRR | Composition dMRR (95% CI) | Raw dMargin | Composition dMargin (95% CI) | 1->0 / 0->1 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"])
        for label, value in values[method].items():
            absolute = value["absolute_prompt_metrics"]
            raw = value["raw_prompt_full_minus_mask"]
            boot = value["composition_bootstrap_full_minus_mask"]
            transitions = value["transition_counts"]
            lines.append(
                f"| {label} | {value['prompt_pair_count']} | {absolute['full']['top1']:.4f} -> {absolute['masked']['top1']:.4f} | {raw['top1']:.4f} | {ci(boot['top1'])} | {raw['mrr']:.4f} | {ci(boot['mrr'])} | {raw['margin']:.4f} | {ci(boot['margin'])} | {transitions.get('1_to_0', 0)} / {transitions.get('0_to_1', 0)} |"
            )
        lines.append("")


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# RQ1b Final Result Ledger",
        "",
        "## Primary Experiment",
        "",
        "One V2+V3 candidate-synchronous single-field-removal experiment: 46 scored compositions drawn from 52 frozen artifacts, 99 strict routing families, 198 prompt instances, eight conditions and 1,584 rows per retriever. Positive deltas always mean `FULL - MASK`, except rank worsening, where positive means the masked card gives the gold a worse rank.",
        "",
    ]
    full_values = {}
    for method in METHODS:
        value = result["primary_single_field"][method]["full_card"]["absolute_prompt_metrics"]["full"]
        full_values[method] = value
    lines.extend(["| Retriever | FULL Top-1 | FULL MRR | Mean gold rank | Mean native margin |", "| --- | ---: | ---: | ---: | ---: |"])
    for method, value in full_values.items():
        lines.append(f"| {method} | {value['top1']:.4f} | {value['mrr']:.4f} | {value['mean_gold_rank']:.4f} | {value['mean_margin']:.4f} |")
    lines.append("")
    render_section(lines, "Primary Single-Field Results", {method: result["primary_single_field"][method]["single_field_masks"] for method in METHODS})
    supporting = {}
    for method in METHODS:
        supporting[method] = result["v2_joint_group_supporting_analysis"][method]["groups"]
    render_section(lines, "V2-Only Joint-Group Supporting Results", supporting)
    lines.extend([
        "## Conclusion",
        "",
        "The complete card is the strongest observed condition for both retrievers. In the primary single-field experiment, every Top-1 and MRR composition-bootstrap interval crosses zero; individual field removal therefore has no stable corpus-wide accuracy effect at the composition unit. The V2-only joint groups all show raw Top-1 degradation when removed, and several margin intervals are positive, which is consistent with distributed/redundant routing evidence across fields. This supports a bounded conclusion: natural public skills carry routing-relevant information in combinations of fields, but this experiment does not identify a universally decisive individual field.",
        "",
    ])
    return "\n".join(lines)


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
            raise ValueError("saved ledger differs from recomputed result")
        print(json.dumps({"status": "PASS", "primary": result["primary_experiment"]}, sort_keys=True))
        return
    if OUTPUT.exists():
        raise ValueError(f"refusing to overwrite output: {OUTPUT}")
    OUTPUT.mkdir(parents=True)
    (OUTPUT / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (OUTPUT / "SUMMARY.md").write_text(render_markdown(result))
    print(json.dumps({"status": result["status"], "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
