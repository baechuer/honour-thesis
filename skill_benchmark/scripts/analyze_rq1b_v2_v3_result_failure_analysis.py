#!/usr/bin/env python3
"""Create a local-only RQ1b V2+V3 result synthesis and failure ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq1b_field_type_confirmatory_v2_common import canonical_entries
from run_rq1b_field_type_confirmatory_v2_bm25 import load_condition, load_strict_families
from run_rq1b_v2_v3_complete_triad_extension import load_extension


REPO = Path(__file__).resolve().parents[2]
OUTPUT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30"
V2_ROOT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28"
PRIMARY_ROOT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30"
JOINT_ROOT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30"
VERSION = "rq1b-v2-v3-result-failure-analysis-v1"
DESCRIPTIVE_REVIEW_FILE = "descriptive_case_review.json"
DESCRIPTIVE_REVIEW_STATUS = "RQ1B_V2_V3_LOCAL_DESCRIPTIVE_CASE_REVIEW"

METHODS = ("bm25", "qwen")
PRIMARY_FIELDS = {
    "use_condition": "MASK_USE",
    "input_precondition": "MASK_INPUT",
    "output_artifact": "MASK_OUTPUT",
    "workflow_procedure": "MASK_WORKFLOW",
    "success_verification": "MASK_SUCCESS",
    "boundary_not_for": "MASK_BOUNDARY",
    "dependency_resource": "MASK_DEPENDENCY",
}
JOINT_GROUPS = {
    "task_specification": ("MASK_TASK_SPECIFICATION", ("use_condition", "input_precondition", "output_artifact")),
    "execution_verification": ("MASK_EXECUTION_VERIFICATION", ("workflow_procedure", "success_verification")),
    "applicability_capability": ("MASK_APPLICABILITY_CAPABILITY", ("boundary_not_for", "dependency_resource")),
}
EXPECTED_PRIMARY_MANIFEST = {
    "bm25": "RQ1B_V2_V3_EXTENSION_BM25_LOCAL_RUN_MANIFEST",
    "qwen": "RQ1B_V2_V3_EXTENSION_QWEN_EXTERNAL_RUN_MANIFEST",
}
EXPECTED_JOINT_MANIFEST = {
    "bm25": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_BM25_LOCAL_RUN_MANIFEST",
    "qwen": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_EXTERNAL_RUN_MANIFEST",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"JSONL row invalid: {path}")
    return rows


def verify_result(root: Path, expected_status: str, row_file: str, expected_rows: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = read_json(root / "manifest.json")
    if manifest.get("status") != expected_status:
        raise ValueError(f"result status drift: {root}")
    for name in (row_file, "summary.json"):
        if manifest.get("artifacts", {}).get(name) != sha256_file(root / name):
            raise ValueError(f"result hash drift: {root}/{name}")
    rows = read_jsonl(root / row_file)
    if len(rows) != expected_rows:
        raise ValueError(f"result row count drift: {root}")
    return rows, {
        "root": root.relative_to(REPO).as_posix(),
        "manifest_sha256": sha256_file(root / "manifest.json"),
        f"{row_file}_sha256": sha256_file(root / row_file),
        "row_count": len(rows),
    }


def load_case_context() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, dict[str, str]]], dict[str, Any]]:
    v2_families, _ = load_strict_families(V2_ROOT)
    v2_family_map = {family["routing_family_id"]: family for family in v2_families}
    v2_entries = canonical_entries(V2_ROOT)
    cards: dict[str, dict[str, dict[str, str]]] = {}
    for composition_id in sorted({family["composition_id"] for family in v2_families}):
        entry = v2_entries[composition_id]
        cards[composition_id] = {card["label"]: card["slots"] for card in load_condition(V2_ROOT, composition_id, "FULL", entry)}

    v3_cards, v3_families, v3_audit = load_extension()
    v3_family_map = {
        family["routing_family_id"]: {
            "routing_family_id": family["routing_family_id"],
            "composition_id": family["composition_id"],
            "prompts": {variant: item["prompt"] for variant, item in family["prompts"].items()},
            "gold_label": family["gold_label"],
        }
        for family in v3_families
    }
    for family in v3_families:
        composition_id = family["composition_id"]
        cards[composition_id] = {card["label"]: card["slots"] for card in v3_cards[f"{composition_id}/FULL"]}

    families = v2_family_map | v3_family_map
    if len(v2_family_map) != 87 or len(v3_family_map) != 12 or len(families) != 99 or len(cards) != 46:
        raise ValueError("case-context denominator drift")
    for family in families.values():
        if set(family["prompts"]) != {"direct", "paraphrase"}:
            raise ValueError(f"prompt variant drift: {family['routing_family_id']}")
        if family["gold_label"] not in cards[family["composition_id"]]:
            raise ValueError(f"gold/card binding drift: {family['routing_family_id']}")
    return families, cards, {"v2_root": V2_ROOT.relative_to(REPO).as_posix(), "v2_canonicalisation_ledger_sha256": sha256_file(V2_ROOT / "canonicalisation_ledger.json"), "v3_extension_audit": v3_audit}


def transition(full: dict[str, Any], masked: dict[str, Any]) -> str:
    key = (full["hit_at_1"], masked["hit_at_1"])
    return {(1, 0): "routing_regression", (0, 1): "mask_recovery", (1, 1): "stable_correct", (0, 0): "stable_wrong"}[key]


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: row[key] for key in ("hit_at_1", "mrr", "gold_rank", "gold_score", "best_wrong_score", "gold_minus_best_wrong_margin", "winner_label", "ranking")}


def pair_rows(rows: list[dict[str, Any]], families: dict[str, dict[str, Any]], cards: dict[str, dict[str, dict[str, str]]], *, stratum: str, analysis_map: dict[str, tuple[str, tuple[str, ...]]]) -> list[dict[str, Any]]:
    by_key = {(row["analysis_group"] if stratum == "joint_group_supporting" else "primary", row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    if len(by_key) != len(rows):
        raise ValueError(f"duplicate source row keys: {stratum}")
    records = []
    for analysis_id, (mask_condition, withheld_fields) in analysis_map.items():
        analysis_rows = [row for row in rows if (row.get("analysis_group") if stratum == "joint_group_supporting" else "primary") == (mask_condition if stratum == "joint_group_supporting" else "primary")]
        family_variants = {(row["routing_family_id"], row["prompt_variant"]) for row in analysis_rows if row["condition"] == "FULL"}
        for family_id, variant in sorted(family_variants):
            full = by_key[(mask_condition if stratum == "joint_group_supporting" else "primary", family_id, variant, "FULL")]
            masked = by_key[(mask_condition if stratum == "joint_group_supporting" else "primary", family_id, variant, mask_condition)]
            family = families.get(family_id)
            if family is None or family["composition_id"] != full["composition_id"] or family["gold_label"] != full["gold_label"]:
                raise ValueError(f"family context drift: {stratum}/{family_id}")
            records.append({
                "analysis_stratum": stratum,
                "analysis_id": analysis_id,
                "mask_condition": mask_condition,
                "withheld_fields": list(withheld_fields),
                "retriever": full.get("retriever", "bm25"),
                "routing_family_id": family_id,
                "composition_id": full["composition_id"],
                "integration_stratum": full.get("integration_stratum"),
                "prompt_variant": variant,
                "prompt": family["prompts"][variant],
                "gold_label": full["gold_label"],
                "candidate_count": full["candidate_count"],
                "transition": transition(full, masked),
                "delta": {
                    "top1": full["hit_at_1"] - masked["hit_at_1"],
                    "mrr": full["mrr"] - masked["mrr"],
                    "margin": full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"],
                    "gold_rank_worsening": masked["gold_rank"] - full["gold_rank"],
                },
                "full": compact_row(full),
                "masked": compact_row(masked),
                "winner_changed": full["winner_label"] != masked["winner_label"],
                "card_reference": {"composition_id": full["composition_id"], "full_card_source": "frozen_card_map"},
            })
    return records


def summarise(records: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["analysis_stratum"], record["analysis_id"], record["retriever"])].append(record)
    summary: dict[str, Any] = {}
    for (stratum, analysis_id, retriever), values in sorted(grouped.items()):
        transitions = Counter(record["transition"] for record in values)
        summary.setdefault(stratum, {}).setdefault(analysis_id, {})[retriever] = {
            "prompt_pair_count": len(values),
            "composition_count": len({record["composition_id"] for record in values}),
            "routing_family_count": len({record["routing_family_id"] for record in values}),
            "transition_counts": dict(sorted(transitions.items())),
            "transition_rates": {name: count / len(values) for name, count in sorted(transitions.items())},
            "mean_delta": {metric: statistics.mean(record["delta"][metric] for record in values) for metric in ("top1", "mrr", "margin", "gold_rank_worsening")},
            "stable_correct_margin_weakened_count": sum(record["transition"] == "stable_correct" and record["delta"]["margin"] > 0 for record in values),
            "winner_changed_count": sum(record["winner_changed"] for record in values),
        }
    return summary


def enrich(record: dict[str, Any], cards: dict[str, dict[str, dict[str, str]]]) -> dict[str, Any]:
    return {**record, "candidate_cards_full": cards[record["composition_id"]]}


def audit_queues(records: list[dict[str, Any]], cards: dict[str, dict[str, dict[str, str]]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    pairs: dict[tuple[str, str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for record in records:
        pairs[(record["analysis_stratum"], record["analysis_id"], record["routing_family_id"], record["prompt_variant"])][record["retriever"]] = record
    if any(set(value) != set(METHODS) for value in pairs.values()):
        raise ValueError("cross-retriever pairing drift")
    concordant_regressions, concordant_recoveries, discordant_regressions, stable_margin = [], [], [], []
    agreement = Counter()
    for _, views in sorted(pairs.items()):
        bm25, qwen = views["bm25"], views["qwen"]
        classes = (bm25["transition"], qwen["transition"])
        agreement[f"{classes[0]}__{classes[1]}"] += 1
        case = {
            "analysis_stratum": bm25["analysis_stratum"],
            "analysis_id": bm25["analysis_id"],
            "routing_family_id": bm25["routing_family_id"],
            "composition_id": bm25["composition_id"],
            "prompt_variant": bm25["prompt_variant"],
            "prompt": bm25["prompt"],
            "gold_label": bm25["gold_label"],
            "withheld_fields": bm25["withheld_fields"],
            "retriever_views": {"bm25": bm25, "qwen": qwen},
            "candidate_cards_full": cards[bm25["composition_id"]],
        }
        if classes == ("routing_regression", "routing_regression"):
            concordant_regressions.append(case)
        elif classes == ("mask_recovery", "mask_recovery"):
            concordant_recoveries.append(case)
        elif "routing_regression" in classes:
            discordant_regressions.append(case)
        elif "stable_correct" in classes and max(bm25["delta"]["margin"], qwen["delta"]["margin"]) > 0:
            stable_margin.append(case)

    priority = lambda case: (-max(view["delta"]["margin"] for view in case["retriever_views"].values()), case["analysis_stratum"], case["analysis_id"], case["routing_family_id"], case["prompt_variant"])
    queues = {
        "cross_retriever_concordant_regressions": sorted(concordant_regressions, key=priority),
        "cross_retriever_concordant_recoveries": sorted(concordant_recoveries, key=priority),
        "retriever_discordant_regressions_cap24": sorted(discordant_regressions, key=priority)[:24],
        "large_margin_stable_correct_cap24": sorted(stable_margin, key=priority)[:24],
    }
    return queues, {"paired_prompt_units": len(pairs), "transition_agreement_counts": dict(sorted(agreement.items())), "uncapped_discordant_regression_count": len(discordant_regressions), "uncapped_stable_margin_count": len(stable_margin)}


def render(summary: dict[str, Any], agreement: dict[str, Any]) -> str:
    lines = [
        "# RQ1b V2+V3 Result Synthesis and Failure Analysis",
        "",
        "This local-only package preserves the primary single-field and supporting joint-field strata separately. A `routing_regression` is only `FULL` Top-1 correct to mask Top-1 wrong. A `mask_recovery` is retained as a counterexample; a stable Top-1 with a positive margin delta is an ordering-fragility observation, not a routing failure.",
        "",
    ]
    for stratum, analyses in summary.items():
        lines.extend([f"## {stratum}", "", "| Analysis | Retriever | Pairs | Regressions | Recoveries | Stable correct | Stable wrong | Mean dMargin | Mean rank worsening |", "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"])
        for analysis_id, by_method in analyses.items():
            for method, value in by_method.items():
                counts = value["transition_counts"]
                lines.append(f"| {analysis_id} | {method} | {value['prompt_pair_count']} | {counts.get('routing_regression', 0)} | {counts.get('mask_recovery', 0)} | {counts.get('stable_correct', 0)} | {counts.get('stable_wrong', 0)} | {value['mean_delta']['margin']:.4f} | {value['mean_delta']['gold_rank_worsening']:.4f} |")
        lines.append("")
    lines.extend(["## Cross-Retriever Agreement", "", f"There are {agreement['paired_prompt_units']} prompt-level pair units. Transition agreement is reported as `bm25__qwen`.", "", "| Transition pair | Count |", "| --- | ---: |"])
    for key, value in agreement["transition_agreement_counts"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Interpretation Boundary", "", "The queues identify results needing explanatory review. They do not change strict labels, and they do not establish an independent causal effect of a masked field or group outside this frozen corpus.", ""])
    return "\n".join(lines)


def run(output: Path = OUTPUT) -> dict[str, Any]:
    if output.exists():
        raise ValueError(f"refusing to overwrite analysis output: {output}")
    families, cards, context_provenance = load_case_context()
    primary_records, joint_records, source_artifacts = [], [], {}
    for method in METHODS:
        rows, provenance = verify_result(PRIMARY_ROOT / method, EXPECTED_PRIMARY_MANIFEST[method], "combined_rows.jsonl", 1584)
        source_artifacts[f"primary_{method}"] = provenance
        primary_records.extend([{**record, "retriever": method} for record in pair_rows(rows, families, cards, stratum="primary_single_field", analysis_map={field: (condition, (field,)) for field, condition in PRIMARY_FIELDS.items()})])
        joint_rows, provenance = verify_result(JOINT_ROOT / method, EXPECTED_JOINT_MANIFEST[method], "combined_group_rows.jsonl", 1024)
        source_artifacts[f"joint_{method}"] = provenance
        joint_records.extend([{**record, "retriever": method} for record in pair_rows(joint_rows, families, cards, stratum="joint_group_supporting", analysis_map=JOINT_GROUPS)])
    records = primary_records + joint_records
    if len(primary_records) != 2772 or len(joint_records) != 1024 or len(records) != 3796:
        raise ValueError(f"pair-ledger count drift: primary={len(primary_records)} joint={len(joint_records)}")
    summary = summarise(records)
    queues, agreement = audit_queues(records, cards)
    report = {
        "status": "RQ1B_V2_V3_RESULT_FAILURE_ANALYSIS_LOCAL_ONLY",
        "version": VERSION,
        "claim_boundary": [
            "Primary single-field and supporting joint-field strata are reported separately.",
            "A routing regression is a frozen strict-gold FULL 1-to-mask 0 transition; recoveries remain counterexamples.",
            "This package explains observed outcomes but does not modify scientific inputs or establish universal field causality.",
        ],
        "counts": {"primary_pair_records": len(primary_records), "joint_pair_records": len(joint_records), "all_pair_records": len(records), "audit_queue_counts": {name: len(values) for name, values in queues.items()}},
        "source_artifacts": source_artifacts,
        "context_provenance": context_provenance,
        "summary": summary,
        "cross_retriever_agreement": agreement,
    }
    files = {
        "pair_ledger.jsonl": "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        "audit_queues.json": json.dumps(queues, indent=2, sort_keys=True) + "\n",
        "summary.json": json.dumps(report, indent=2, sort_keys=True) + "\n",
        "SUMMARY.md": render(summary, agreement),
    }
    manifest = {"status": "RQ1B_V2_V3_RESULT_FAILURE_ANALYSIS_LOCAL_ONLY_MANIFEST", "version": VERSION, "network_calls": 0, "texts_transmitted": 0, "thesis_results_written": False, "source_artifacts": source_artifacts, "artifacts": {name: hashlib.sha256(content.encode("utf-8")).hexdigest() for name, content in files.items()}}
    files["manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    staging = output.parent / f".{output.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        for name, content in files.items():
            (staging / name).write_text(content, encoding="utf-8")
        staging.replace(output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def check(output: Path = OUTPUT) -> dict[str, Any]:
    manifest = read_json(output / "manifest.json")
    if manifest.get("status") != "RQ1B_V2_V3_RESULT_FAILURE_ANALYSIS_LOCAL_ONLY_MANIFEST" or manifest.get("version") != VERSION:
        raise ValueError("analysis manifest state drift")
    for name, expected in manifest.get("artifacts", {}).items():
        if sha256_file(output / name) != expected:
            raise ValueError(f"analysis artifact hash drift: {name}")
    rows = read_jsonl(output / "pair_ledger.jsonl")
    if len(rows) != 3796 or len({(row["analysis_stratum"], row["analysis_id"], row["retriever"], row["routing_family_id"], row["prompt_variant"]) for row in rows}) != 3796:
        raise ValueError("analysis pair ledger coverage drift")
    for key, source in manifest["source_artifacts"].items():
        root = REPO / source["root"]
        if sha256_file(root / "manifest.json") != source["manifest_sha256"]:
            raise ValueError(f"source manifest drift: {key}")
    review = read_json(output / DESCRIPTIVE_REVIEW_FILE)
    if review.get("status") != DESCRIPTIVE_REVIEW_STATUS:
        raise ValueError("descriptive review status drift")
    scope = review.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("descriptive review scope missing")
    for filename, key in (("audit_queues.json", "audit_queues_sha256"), ("pair_ledger.jsonl", "pair_ledger_sha256")):
        if scope.get(key) != sha256_file(output / filename):
            raise ValueError(f"descriptive review source hash drift: {filename}")
    queues = read_json(output / "audit_queues.json")
    expected_cases: dict[str, str] = {}
    for transition, queue_name in (("routing_regression", "cross_retriever_concordant_regressions"), ("mask_recovery", "cross_retriever_concordant_recoveries")):
        cases = queues.get(queue_name)
        if not isinstance(cases, list):
            raise ValueError(f"review queue missing: {queue_name}")
        for case in cases:
            key = "/".join((case["analysis_stratum"], case["analysis_id"], case["routing_family_id"], case["prompt_variant"]))
            if key in expected_cases:
                raise ValueError(f"duplicate review queue key: {key}")
            expected_cases[key] = transition
    reviewed_cases = review.get("cases")
    if not isinstance(reviewed_cases, list) or len(reviewed_cases) != len(expected_cases):
        raise ValueError("descriptive review count drift")
    allowed = set(review.get("allowed_labels", []))
    actual_cases: dict[str, str] = {}
    for case in reviewed_cases:
        key, transition_name, labels = case.get("case_key"), case.get("transition"), case.get("labels")
        if not isinstance(key, str) or key in actual_cases or expected_cases.get(key) != transition_name:
            raise ValueError(f"descriptive review case binding drift: {key}")
        if not isinstance(labels, list) or not labels or not all(isinstance(label, str) and label in allowed for label in labels):
            raise ValueError(f"descriptive review label drift: {key}")
        actual_cases[key] = transition_name
    if actual_cases != expected_cases:
        raise ValueError("descriptive review coverage drift")
    return {
        "status": "PASS",
        "pair_records": len(rows),
        "descriptive_review_cases": len(actual_cases),
        "descriptive_review_transitions": dict(sorted(Counter(actual_cases.values()).items())),
        "network_calls": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.run == args.check:
        parser.error("choose exactly one of --run or --check")
    print(json.dumps(run() if args.run else check(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
