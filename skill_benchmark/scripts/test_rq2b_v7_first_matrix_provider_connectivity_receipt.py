#!/usr/bin/env python3
"""Zero-network tests for the sanitised V7 provider-connectivity receipt."""

from __future__ import annotations

import copy
import json
import math

from build_rq2b_v7_first_matrix_provider_connectivity_receipt import receipt, validate_receipt, verify


def expect_failure(value: dict) -> None:
    try:
        validate_receipt(value)
    except RuntimeError:
        return
    raise RuntimeError("Expected sanitised connectivity receipt rejection")


def main() -> int:
    value = receipt()
    validate_receipt(value)

    leaked_benchmark = copy.deepcopy(value)
    leaked_benchmark["transfer_boundary"]["benchmark_queries_transferred"] = 1
    expect_failure(leaked_benchmark)

    nonfinite = copy.deepcopy(value)
    nonfinite["provider_calls"]["reranker"]["scores"][0] = math.nan
    expect_failure(nonfinite)

    authorised = copy.deepcopy(value)
    authorised["boundary"]["execution_authorisation"] = True
    expect_failure(authorised)

    endpoint_drift = copy.deepcopy(value)
    endpoint_drift["provider_calls"]["embedding"]["endpoint"] = "https://example.invalid/embeddings"
    expect_failure(endpoint_drift)

    replay = verify()
    print(json.dumps({
        "status": "PASS_SANITISED_CONNECTIVITY_RECEIPT_TESTS",
        "fail_closed_rejections": 4,
        "receipt_replay": replay["status"],
        "provider_calls_replayed": 0,
        "credential_values_read": 0,
        "benchmark_texts_read": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
