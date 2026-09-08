#!/usr/bin/env python3
"""Deterministic zero-model tests for the V7 runtime preflight contract."""

from __future__ import annotations

import json
import math

from build_rq2b_v7_first_matrix_runtime_preflight import (
    LONG_SEQUENCE_PROBES,
    REPRESENTATIONS,
    SMOKE_CASES,
    require,
    select_cpu_audit_ids,
    validate_finite_scores,
    verify,
)


def expect_failure(function, *args, **kwargs) -> None:
    try:
        function(*args, **kwargs)
    except RuntimeError:
        return
    raise RuntimeError(f"Expected fail-closed rejection from {function.__name__}")


def main() -> int:
    validate_finite_scores([0.0, -1.0, 1.0], expected_length=3)
    expect_failure(validate_finite_scores, [0.0, math.nan])
    expect_failure(validate_finite_scores, [math.inf])
    expect_failure(validate_finite_scores, [0.0], expected_length=2)

    stable_ids = ["unit-c", "unit-a", "unit-d", "unit-b"]
    first = select_cpu_audit_ids(stable_ids, component="embedding", representation=REPRESENTATIONS[0], count=2)
    second = select_cpu_audit_ids(list(reversed(stable_ids)), component="embedding", representation=REPRESENTATIONS[0], count=2)
    require(first == second and len(first) == 2, "CPU-audit selection is not order-independent and deterministic")
    require(len(select_cpu_audit_ids(["only"], component="reranker", representation=REPRESENTATIONS[1], count=8)) == 1, "CPU-audit short population rule drift")

    by_id = {row["case_id"]: row for row in SMOKE_CASES}
    require(by_id["embedding-default-sdpa-mps-float32-heterogeneous-left-padding"]["disposition"] == "INVALID_NON_FINITE", "Heterogeneous padding smoke must fail closed")
    require(by_id["embedding-default-sdpa-mps-float32-single-unpadded"]["output_finite"] is True, "Unpadded default-SDPA embedding smoke drift")
    primary_embedding = by_id["embedding-default-sdpa-mps-bfloat16-exact-length-batch16"]["scores"]
    primary_reranker = by_id["reranker-default-sdpa-mps-bfloat16-short-unpadded"]
    validate_finite_scores(primary_embedding, expected_length=16)
    require(set(primary_embedding) == {1.0}, "Primary bfloat16 embedding identical-row cosine smoke drift")
    require(primary_reranker["batch_shape"] == "16_short_exact_token_length_rows_no_padding", "Primary bfloat16 reranker batch contract drift")
    require(primary_reranker["score_observations"]["relevant_yes_minus_no"] == 0.0, "Primary bfloat16 reranker quantisation evidence drift")
    validate_finite_scores(list(primary_reranker["score_observations"].values()), expected_length=2)

    embedding_delta = max(abs(a - b) for a, b in zip(by_id["embedding-eager-mps-float32"]["scores"], by_id["embedding-eager-cpu-float32"]["scores"], strict=True))
    reranker_delta = max(abs(a - b) for a, b in zip(by_id["reranker-eager-mps-float32"]["scores"], by_id["reranker-eager-cpu-float32"]["scores"], strict=True))
    require(abs(embedding_delta - 0.0000006556) < 1e-12 and abs(reranker_delta - 0.0000133514) < 1e-12, "Recorded fp32 diagnostic delta drift")

    probes = {row["case_id"]: row for row in LONG_SEQUENCE_PROBES}
    require(probes["embedding-mps-default-sdpa-float32-30000-single-unpadded"]["disposition"] == "INVALID_HARD_MEMORY_FAILURE", "30k fp32 hard-failure evidence drift")
    require(probes["embedding-mps-default-sdpa-bfloat16-7500-single-unpadded"]["output_finite"] is True, "7,500-token bfloat16 probe drift")

    replay = verify()
    print(json.dumps({
        "status": "PASS_ZERO_MODEL_RUNTIME_PREFLIGHT_TESTS",
        "finite_gate_rejections": 3,
        "deterministic_cpu_selection": True,
        "primary_exact_length_batch16_smokes": 2,
        "long_sequence_probes_checked": len(LONG_SEQUENCE_PROBES),
        "package_replay": replay["status"],
        "network_calls": 0,
        "model_forward_passes": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
