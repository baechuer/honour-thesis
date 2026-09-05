#!/usr/bin/env python3
"""Run the frozen RQ1b v2 local BM25 field-availability experiment.

The runner reads only the ledger-defined strict-preserved families and the
eight immutable candidate-synchronous card conditions. It intentionally writes
outside the frozen input root and makes no network call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import shutil
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq1b_field_type_confirmatory_v2_common import (
    DISPLAY_NAMES,
    FIELDS,
    canonical_entries,
    composition_rows,
    label_for_skill,
    load_object,
    routing_family_rows,
)
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze


RUNNER_VERSION = "rq1b-field-type-v2-bm25-v1"
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
FIELD_CONDITIONS = dict(zip(FIELDS, CONDITIONS[1:], strict=True))
K1 = 1.5
B = 0.75
TOKEN_RE = re.compile(r"[a-z0-9]+")


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(value: str) -> list[str]:
    return TOKEN_RE.findall(value.lower())


class BM25:
    def __init__(self, labels: list[str], documents: list[str]) -> None:
        if len(labels) != len(documents) or not labels or len(set(labels)) != len(labels):
            raise ValueError("invalid BM25 candidate set")
        self.labels = labels
        self.doc_tokens = [tokens(document) for document in documents]
        self.lengths = [len(row) for row in self.doc_tokens]
        self.average_length = statistics.mean(self.lengths) or 1.0
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for index, row in enumerate(self.doc_tokens):
            for term, count in Counter(row).items():
                self.postings[term].append((index, count))
        self.idf = {
            term: math.log(1.0 + (len(labels) - len(posting) + 0.5) / (len(posting) + 0.5))
            for term, posting in self.postings.items()
        }

    def rank(self, query: str) -> list[tuple[str, float]]:
        scores = [0.0] * len(self.labels)
        for term, query_count in Counter(tokens(query)).items():
            for index, frequency in self.postings.get(term, []):
                length = self.lengths[index] or 1
                denominator = frequency + K1 * (1.0 - B + B * length / self.average_length)
                scores[index] += query_count * self.idf[term] * frequency * (K1 + 1.0) / denominator
        return sorted(zip(self.labels, scores, strict=True), key=lambda item: (-item[1], item[0]))


def render_card(card: dict[str, str]) -> str:
    return "\n\n".join(f"{DISPLAY_NAMES[field]}:\n{card[field]}" for field in FIELDS)


def load_condition(root: Path, composition_id: str, condition: str, entry: dict[str, Any]) -> list[dict[str, Any]]:
    path = root / "conditions" / composition_id / f"{condition}.json"
    payload = load_object(path)
    if (
        payload.get("status") != "RQ1B_FIELD_TYPE_ABLATION_V2_CONDITION_NOT_A_RESULT"
        or payload.get("composition_id") != composition_id
        or payload.get("condition") != condition
        or digest(payload) != entry["condition_sha256"][condition]
    ):
        raise ValueError(f"condition binding invalid: {composition_id}/{condition}")
    cards = payload.get("cards")
    if not isinstance(cards, list) or len(cards) not in {3, 4}:
        raise ValueError(f"condition cards invalid: {composition_id}/{condition}")
    labels = [card.get("label") for card in cards if isinstance(card, dict)]
    if len(labels) != len(cards) or len(set(labels)) != len(labels):
        raise ValueError(f"condition labels invalid: {composition_id}/{condition}")
    for card in cards:
        slots = card.get("slots")
        if not isinstance(slots, dict) or set(slots) != set(FIELDS) or any(not isinstance(slots[field], str) for field in FIELDS):
            raise ValueError(f"condition slots invalid: {composition_id}/{condition}/{card.get('label')}")
    return cards


def load_strict_families(root: Path) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    eligibility = load_object(root / "audits" / "field_eligibility_ledger.json")
    families = routing_family_rows(root)
    compositions = composition_rows(root)
    entries = canonical_entries(root)
    strict: list[dict[str, Any]] = []
    field_eligible: dict[str, set[str]] = {field: set() for field in FIELDS}
    for row in eligibility.get("families", []):
        family_id = row.get("routing_family_id")
        if not isinstance(family_id, str):
            raise ValueError("eligibility family id missing")
        if row.get("full_card_preservation_state") != "FULL_CARD_PRESERVATION_PASS":
            continue
        family = families.get(family_id)
        if family is None or row.get("composition_id") != family.get("composition_id"):
            raise ValueError(f"eligibility/family binding invalid: {family_id}")
        composition_id = family["composition_id"]
        entry = entries.get(composition_id)
        if not isinstance(entry, dict) or entry.get("status") != "MATERIALISED_FROM_FROZEN_CANONICAL_CARD":
            raise ValueError(f"strict family has non-materialised composition: {family_id}")
        gold_label = label_for_skill(compositions[composition_id], family["strict_gold_skill_id"])
        if row.get("sealed_gold_label") != gold_label:
            raise ValueError(f"sealed gold binding invalid: {family_id}")
        prompt_by_variant = {item["prompt_variant"]: item["prompt"] for item in family["prompt_lineage"]}
        strict.append(
            {
                "routing_family_id": family_id,
                "composition_id": composition_id,
                "gold_label": gold_label,
                "prompts": prompt_by_variant,
            }
        )
        for field_row in row.get("field_rows", []):
            field = field_row.get("field")
            if field in field_eligible and field_row.get("scoring_eligible_after_preservation") is True:
                field_eligible[field].add(family_id)
    strict.sort(key=lambda item: item["routing_family_id"])
    if len(strict) != 87:
        raise ValueError(f"strict family count drift: {len(strict)}")
    expected = {
        "use_condition": 79,
        "input_precondition": 82,
        "output_artifact": 86,
        "workflow_procedure": 85,
        "success_verification": 78,
        "boundary_not_for": 79,
        "dependency_resource": 77,
    }
    observed = {field: len(ids) for field, ids in field_eligible.items()}
    if observed != expected:
        raise ValueError(f"field eligibility drift: {observed}")
    return strict, field_eligible


def metric_for_ranking(ranking: list[tuple[str, float]], gold_label: str) -> dict[str, Any]:
    labels = [label for label, _ in ranking]
    gold_rank = labels.index(gold_label) + 1
    scores = dict(ranking)
    best_wrong = max(score for label, score in ranking if label != gold_label)
    return {
        "gold_rank": gold_rank,
        "hit_at_1": int(gold_rank == 1),
        "mrr": 1.0 / gold_rank,
        "gold_score": scores[gold_label],
        "best_wrong_score": best_wrong,
        "gold_minus_best_wrong_margin": scores[gold_label] - best_wrong,
        "winner_label": labels[0],
        "ranking": [{"label": label, "score": score} for label, score in ranking],
    }


def percentile(values: list[float], level: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty bootstrap distribution")
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * level)))
    return ordered[index]


def bootstrap_mean(values_by_composition: dict[str, float], seed: int) -> dict[str, Any]:
    ids = sorted(values_by_composition)
    values = [values_by_composition[item] for item in ids]
    generator = random.Random(seed)
    samples = [statistics.mean(generator.choice(values) for _ in values) for _ in range(5000)]
    return {
        "composition_count": len(values),
        "mean": statistics.mean(values),
        "bootstrap_replicates": 5000,
        "bootstrap_seed": seed,
        "ci95": [percentile(samples, 0.025), percentile(samples, 0.975)],
    }


def summarize(rows: list[dict[str, Any]], eligible: dict[str, set[str]]) -> dict[str, Any]:
    by_key = {(row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    fields: dict[str, Any] = {}
    for position, field in enumerate(FIELDS, start=1):
        condition = FIELD_CONDITIONS[field]
        pairs = []
        for family_id in sorted(eligible[field]):
            for variant in ("direct", "paraphrase"):
                full = by_key[(family_id, variant, "FULL")]
                masked = by_key[(family_id, variant, condition)]
                pairs.append({"family_id": family_id, "composition_id": full["composition_id"], "full": full, "masked": masked})
        def average(path: str) -> float:
            return statistics.mean(pair["full"][path] for pair in pairs)
        def masked_average(path: str) -> float:
            return statistics.mean(pair["masked"][path] for pair in pairs)
        composition_values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for pair in pairs:
            full, masked = pair["full"], pair["masked"]
            composition_values[pair["composition_id"]]["top1"].append(full["hit_at_1"] - masked["hit_at_1"])
            composition_values[pair["composition_id"]]["mrr"].append(full["mrr"] - masked["mrr"])
            composition_values[pair["composition_id"]]["margin"].append(
                full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"]
            )
        aggregated = {
            metric: {composition: statistics.mean(values[metric]) for composition, values in composition_values.items()}
            for metric in ("top1", "mrr", "margin")
        }
        winners = Counter(pair["masked"]["winner_label"] for pair in pairs)
        fields[field] = {
            "condition": condition,
            "routing_family_count": len(eligible[field]),
            "prompt_pair_count": len(pairs),
            "full": {
                "top1": average("hit_at_1"),
                "mrr": average("mrr"),
                "mean_gold_rank": average("gold_rank"),
                "mean_margin": average("gold_minus_best_wrong_margin"),
            },
            "masked": {
                "top1": masked_average("hit_at_1"),
                "mrr": masked_average("mrr"),
                "mean_gold_rank": masked_average("gold_rank"),
                "mean_margin": masked_average("gold_minus_best_wrong_margin"),
            },
            "full_correct_to_masked_wrong_rate": statistics.mean(
                pair["full"]["hit_at_1"] == 1 and pair["masked"]["hit_at_1"] == 0 for pair in pairs
            ),
            "masked_winner_counts": dict(sorted(winners.items())),
            "composition_bootstrap_full_minus_mask": {
                "top1": bootstrap_mean(aggregated["top1"], 20260829 + position),
                "mrr": bootstrap_mean(aggregated["mrr"], 20260929 + position),
                "margin": bootstrap_mean(aggregated["margin"], 20261029 + position),
            },
        }
    return {
        "status": "RQ1B_FIELD_TYPE_V2_BM25_SUMMARY_LOCAL_RESULT",
        "retriever": "bm25",
        "analysis_unit": "routing family prompts retained; field effects are composition-aggregated for bootstrap",
        "fields": fields,
    }


def run(root: Path, output_dir: Path) -> dict[str, Any]:
    verify_freeze(root)
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite output directory: {output_dir}")
    families, eligible = load_strict_families(root)
    entries = canonical_entries(root)
    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for family in families:
        composition_id = family["composition_id"]
        entry = entries[composition_id]
        labels_by_condition: dict[str, set[str]] = {}
        for condition in CONDITIONS:
            cards = load_condition(root, composition_id, condition, entry)
            labels = [card["label"] for card in cards]
            labels_by_condition[condition] = set(labels)
            index = BM25(labels, [render_card(card["slots"]) for card in cards])
            for variant, prompt in family["prompts"].items():
                begun = time.perf_counter()
                ranking = index.rank(prompt)
                measures = metric_for_ranking(ranking, family["gold_label"])
                rows.append(
                    {
                        "status": "RQ1B_FIELD_TYPE_V2_BM25_ROW_LOCAL_RESULT",
                        "routing_family_id": family["routing_family_id"],
                        "composition_id": composition_id,
                        "prompt_variant": variant,
                        "condition": condition,
                        "gold_label": family["gold_label"],
                        "candidate_count": len(labels),
                        "query_seconds": time.perf_counter() - begun,
                        **measures,
                    }
                )
        if len(set(map(frozenset, labels_by_condition.values()))) != 1:
            raise ValueError(f"candidate membership drift across conditions: {composition_id}")
    expected_rows = len(families) * 2 * len(CONDITIONS)
    if len(rows) != expected_rows or len({(row['routing_family_id'], row['prompt_variant'], row['condition']) for row in rows}) != expected_rows:
        raise ValueError("BM25 output row coverage invalid")
    summary = summarize(rows, eligible)
    provenance = {
        "status": "RQ1B_FIELD_TYPE_V2_BM25_LOCAL_RUN_MANIFEST",
        "runner_version": RUNNER_VERSION,
        "network_calls": 0,
        "texts_transmitted": 0,
        "thesis_results_written": False,
        "root": str(root),
        "inputs": {
            relative: sha256_file(root / relative)
            for relative in (
                "condition_materialisation_freeze_amendment_2026-08-29.json",
                "canonicalisation_ledger.json",
                "routing_family_manifest_private.json",
                "audits/field_eligibility_ledger.json",
            )
        },
        "configuration": {
            "scope": "per-composition candidate set only",
            "tokenizer": "lowercase_[a-z0-9]+",
            "k1": K1,
            "b": B,
            "tie_break": "candidate_label_ascending",
            "conditions": list(CONDITIONS),
        },
        "counts": {
            "strict_routing_families": len(families),
            "prompt_variants": len(families) * 2,
            "condition_rows": len(rows),
        },
        "timing": {"wall_seconds": time.perf_counter() - started, "query_seconds": sum(row["query_seconds"] for row in rows)},
    }
    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        (staging / "rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
        (staging / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        provenance["artifacts"] = {
            "rows.jsonl": sha256_file(staging / "rows.jsonl"),
            "summary.json": sha256_file(staging / "summary.json"),
        }
        (staging / "manifest.json").write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
        staging.replace(output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return provenance


def self_test() -> None:
    ranking = BM25(["A", "B", "C"], ["parse scanned pdf with ocr", "extract native pdf text", "render pdf pages"]).rank("OCR scanned PDF")
    if ranking[0][0] != "A":
        raise ValueError("BM25 synthetic OCR test failed")
    if metric_for_ranking(ranking, "A")["gold_rank"] != 1:
        raise ValueError("BM25 rank metrics self-test failed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print(json.dumps({"status": "pass_synthetic_no_scientific_result", "network_calls": 0}, sort_keys=True))
        return
    if args.output_dir is None:
        raise ValueError("--output-dir is required unless --self-test is used")
    output_dir = args.output_dir if args.output_dir.is_absolute() else Path.cwd() / args.output_dir
    print(json.dumps(run(args.root, output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
