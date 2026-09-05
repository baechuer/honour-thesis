#!/usr/bin/env python3
"""Frozen grouped inference primitives for the RQ2b primary contrasts."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any, Iterable

from rq2b_common import require


BOOTSTRAP_SEED = 2026080201
SIGN_FLIP_SEED = 2026080202
BOOTSTRAP_RESAMPLES = 10_000
SIGN_FLIP_DRAWS = 100_000
NONINFERIORITY_MARGIN = -0.03
STATISTICS_VERSION = "rq2b-grouped-inference-v1"


def arithmetic_mean(values: Iterable[float]) -> float:
    materialized = list(values)
    require(bool(materialized), "Cannot average an empty sequence")
    return sum(materialized) / len(materialized)


def percentile_linear(values: list[float], probability: float) -> float:
    require(bool(values), "Cannot compute an empty percentile")
    require(0.0 <= probability <= 1.0, "Percentile probability is outside [0, 1]")
    ordered = sorted(float(value) for value in values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def group_values(rows: list[dict[str, Any]]) -> dict[str, list[float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        group = str(row.get("group") or "")
        require(bool(group), "Paired inference row has no group")
        value = float(row["difference"])
        require(math.isfinite(value), "Paired inference difference is non-finite")
        grouped[group].append(value)
    require(bool(grouped), "Paired inference has no groups")
    return dict(grouped)


def prompt_weighted_estimate(grouped: dict[str, list[float]]) -> float:
    return arithmetic_mean(value for values in grouped.values() for value in values)


def equal_group_estimate(grouped: dict[str, list[float]]) -> float:
    return arithmetic_mean(arithmetic_mean(values) for values in grouped.values())


def grouped_percentile_bootstrap(
    rows: list[dict[str, Any]],
    *,
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> dict[str, Any]:
    require(resamples > 0, "Bootstrap resamples must be positive")
    grouped = group_values(rows)
    groups = sorted(grouped)
    generator = random.Random(seed)
    draws: list[float] = []
    for _ in range(resamples):
        sampled_groups = [generator.choice(groups) for _ in groups]
        sampled_values = [
            value
            for group in sampled_groups
            for value in grouped[group]
        ]
        draws.append(arithmetic_mean(sampled_values))
    return {
        "estimate": prompt_weighted_estimate(grouped),
        "equal_group_sensitivity": equal_group_estimate(grouped),
        "two_sided_95": [
            percentile_linear(draws, 0.025),
            percentile_linear(draws, 0.975),
        ],
        "one_sided_95_lower": percentile_linear(draws, 0.05),
        "resamples": resamples,
        "seed": seed,
        "groups": len(groups),
        "prompts": sum(len(values) for values in grouped.values()),
        "percentile_method": "linear_interpolation_at_(n-1)*p",
    }


def grouped_sign_flip(
    rows: list[dict[str, Any]],
    *,
    tail: str,
    draws: int = SIGN_FLIP_DRAWS,
    seed: int = SIGN_FLIP_SEED,
) -> dict[str, Any]:
    require(tail in {"positive_one_sided", "absolute_two_sided"}, "Unknown sign-flip tail")
    require(draws > 0, "Sign-flip draws must be positive")
    grouped = group_values(rows)
    groups = sorted(grouped)
    observed = prompt_weighted_estimate(grouped)
    generator = random.Random(seed)
    extreme = 0
    for _ in range(draws):
        signed_values: list[float] = []
        for group in groups:
            sign = 1.0 if generator.getrandbits(1) else -1.0
            signed_values.extend(sign * value for value in grouped[group])
        statistic = arithmetic_mean(signed_values)
        if tail == "positive_one_sided":
            extreme += statistic >= observed
        else:
            extreme += abs(statistic) >= abs(observed)
    return {
        "observed": observed,
        "tail": tail,
        "draws": draws,
        "seed": seed,
        "extreme_draws": extreme,
        "p_value": (1.0 + extreme) / (draws + 1.0),
        "groups": len(groups),
        "prompts": sum(len(values) for values in grouped.values()),
    }


def holm_adjust(p_values: dict[str, float]) -> dict[str, dict[str, Any]]:
    require(bool(p_values), "Holm family is empty")
    ordered = sorted(p_values.items(), key=lambda item: (float(item[1]), item[0]))
    family_size = len(ordered)
    adjusted_running = 0.0
    output: dict[str, dict[str, Any]] = {}
    for index, (hypothesis, raw) in enumerate(ordered):
        raw = float(raw)
        require(0.0 <= raw <= 1.0, f"Invalid p-value for {hypothesis}")
        adjusted_running = max(adjusted_running, min(1.0, raw * (family_size - index)))
        output[hypothesis] = {
            "raw_p_value": raw,
            "holm_adjusted_p_value": adjusted_running,
            "holm_reject_at_0_05": adjusted_running <= 0.05,
            "holm_family_size": family_size,
            "holm_order": index + 1,
        }
    return output


def self_test() -> dict[str, Any]:
    rows = [
        {"group": "a", "difference": 1.0},
        {"group": "a", "difference": 0.0},
        {"group": "b", "difference": 1.0},
        {"group": "c", "difference": -1.0},
    ]
    bootstrap_a = grouped_percentile_bootstrap(rows, resamples=200, seed=17)
    bootstrap_b = grouped_percentile_bootstrap(rows, resamples=200, seed=17)
    require(bootstrap_a == bootstrap_b, "Grouped bootstrap is not deterministic")
    positive = grouped_sign_flip(rows, tail="positive_one_sided", draws=500, seed=19)
    two_sided = grouped_sign_flip(rows, tail="absolute_two_sided", draws=500, seed=19)
    require(0.0 < positive["p_value"] <= 1.0, "Positive sign-flip p-value is invalid")
    require(0.0 < two_sided["p_value"] <= 1.0, "Two-sided sign-flip p-value is invalid")
    holm = holm_adjust({"P2-C": 0.01, "P2-P": 0.02, "P3-C": 0.5})
    require(holm["P2-C"]["holm_adjusted_p_value"] == 0.03, "Holm self-test failed")
    return {
        "state": "synthetic_inference_only",
        "bootstrap_deterministic": True,
        "positive_p_value": positive["p_value"],
        "two_sided_p_value": two_sided["p_value"],
        "holm": holm,
    }
