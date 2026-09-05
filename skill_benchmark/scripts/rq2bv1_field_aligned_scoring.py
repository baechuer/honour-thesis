#!/usr/bin/env python3
"""Zero-network scoring contract for B1E-FQ field-aligned retrieval."""

from __future__ import annotations

import argparse
import math
from typing import Any

from rq2b_common import require
# B1E-FQ V2.1 is the only consumer of this scorer.  Its field keys are the
# grounded parser's singular query-side names, which map explicitly to the
# plural candidate-side I3C field names in the E2E runner.
from rq2bv1_query_field_parser_v2 import FIELD_ORDER


SCORER_VERSION = "rq2bv1-v3-b1e-fq-field-aligned-scorer-v1"


def cosine(left: list[float], right: list[float]) -> float:
    require(len(left) == len(right) and len(left) > 0, "Field vectors have incompatible dimensions")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    require(left_norm > 0.0 and right_norm > 0.0, "Field vector has zero norm")
    return sum(a * b for a, b in zip(left, right, strict=True)) / (left_norm * right_norm)


def normalized_equal_weights(active_fields: tuple[str, ...] | list[str]) -> dict[str, float]:
    unique = tuple(active_fields)
    require(bool(unique) and len(set(unique)) == len(unique), "Active fields must be unique and non-empty")
    require(all(field in FIELD_ORDER for field in unique), "Active fields drift from parser contract")
    return {field: 1.0 / len(unique) for field in unique}


def score_candidate(
    query_vectors: dict[str, list[float]],
    candidate_vectors: dict[str, list[float]],
    active_fields: tuple[str, ...] | list[str],
    *,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Score only field-to-same-field comparisons; no cross-field top-k exists."""
    active = tuple(active_fields)
    chosen_weights = weights or normalized_equal_weights(active)
    require(set(chosen_weights) == set(active), "Weights must cover exactly the active fields")
    require(all(value >= 0.0 and math.isfinite(value) for value in chosen_weights.values()), "Weights must be finite and non-negative")
    total_weight = sum(chosen_weights.values())
    require(abs(total_weight - 1.0) <= 1e-12, "Weights must sum to one")

    components: dict[str, float] = {}
    for field in active:
        require(field in query_vectors and field in candidate_vectors, f"Missing aligned field vector: {field}")
        components[field] = cosine(query_vectors[field], candidate_vectors[field])
    return {
        "scorer_version": SCORER_VERSION,
        "aggregation": "normalized_equal_weight_field_aligned_cosine",
        "active_fields": list(active),
        "weights": {field: chosen_weights[field] for field in active},
        "component_scores": components,
        "score": sum(chosen_weights[field] * components[field] for field in active),
    }


def self_test() -> dict[str, Any]:
    query = {"input_precondition": [1.0, 0.0], "output_artifact": [0.0, 1.0]}
    active = ("input_precondition", "output_artifact")
    aligned = score_candidate(query, {"input_precondition": [1.0, 0.0], "output_artifact": [0.0, 1.0]}, active)
    wrong_output = score_candidate(query, {"input_precondition": [1.0, 0.0], "output_artifact": [-1.0, 0.0]}, active)
    unrelated_peak = score_candidate(
        query,
        {
            "input_precondition": [0.0, 1.0],
            "output_artifact": [-1.0, 0.0],
            "workflow_procedure": [1.0, 0.0],
        },
        active,
    )
    require(abs(float(aligned["score"]) - 1.0) <= 1e-12, "Aligned score self-test failed")
    require(float(aligned["score"]) > float(wrong_output["score"]), "Aligned score did not prefer matching output")
    require(float(unrelated_peak["score"]) < float(aligned["score"]), "Unrelated candidate field affected aligned scoring")
    require("workflow_procedure" not in unrelated_peak["component_scores"], "Inactive field leaked into aligned score")
    return {
        "schema_version": "rq2bv1-v3-b1e-fq-field-aligned-scorer-self-test-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the B1E-FQ field-aligned scorer contract.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.self_test, "Only --self-test is implemented")
    print(self_test())


if __name__ == "__main__":
    main()
