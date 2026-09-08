#!/usr/bin/env python3
"""Build or replay the sanitised V7 synthetic provider-connectivity receipt.

The two provider calls described here were already completed under explicit
synthetic-only authorisation.  This builder never reads a credential, opens a
benchmark payload, or contacts a provider.  It only binds the supplied
sanitised observations to the frozen local request contracts and preflight.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_provider_connectivity_receipt_2026_09_09_v1"
)

INPUT_BINDINGS = {
    "zero_inference_preflight_report": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_runtime_preflight_2026_09_09_v1/integrity_report.json",
        "sha256": "93e047af9e92ead168b53a1b47b17ff5839b36ee3f900d47e5254e2694214279",
    },
    "zero_inference_runtime_inventory": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_runtime_preflight_2026_09_09_v1/runtime_inventory.json",
        "sha256": "3bc874eaa23ed699c71ee7007039374868cb65ab69ce05823b67ea3a5b955b54",
    },
    "qwen_embedding_contract_source": {
        "path": "skill_benchmark/scripts/run_rq2b_qwen.py",
        "sha256": "ad9016cf14c20c3935c84482d9c9499be3e86f0272a6105a7ab3fa2238a7c05f",
    },
    "qwen_reranker_contract_source": {
        "path": "skill_benchmark/scripts/rq2b_qwen_reranker.py",
        "sha256": "d7f83d25076dbec12750d8c7dad687b69545f335bddf7a1889bc9f3a5a598f7a",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _validate_bindings() -> None:
    for name, binding in INPUT_BINDINGS.items():
        path = ROOT / binding["path"]
        require(path.is_file(), f"Missing connectivity-receipt binding: {name}")
        require(sha256_file(path) == binding["sha256"], f"Connectivity-receipt binding hash drift: {name}")


def receipt() -> dict[str, Any]:
    _validate_bindings()
    value = {
        "schema_version": "rq2b-v7-b36-c6-provider-connectivity-receipt-v1",
        "status": "PASS_SANITISED_SYNTHETIC_CONNECTIVITY_RECEIPT_NOT_SCIENTIFIC_EXECUTION",
        "recorded_date": "2026-09-09",
        "evidence_origin": "USER_AUTHORISED_SYNTHETIC_ONLY_CONNECTIVITY_SMOKES_REPORTED_BY_EXECUTOR",
        "bindings": INPUT_BINDINGS,
        "provider_calls": {
            "total": 2,
            "embedding": {
                "status": "PASS_CONNECTIVITY",
                "endpoint": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings",
                "model": "text-embedding-v4",
                "calls": 1,
                "synthetic_texts": 1,
                "embedding_dimensions": 1024,
                "usage": {"prompt_tokens": 11, "total_tokens": 11},
            },
            "reranker": {
                "status": "PASS_CONNECTIVITY",
                "endpoint": "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
                "model": "qwen3-rerank",
                "calls": 1,
                "synthetic_queries": 1,
                "synthetic_documents": 2,
                "scores": [0.7933007406217729, 0.44544158349861485],
                "usage": {"total_tokens": 60},
            },
        },
        "transfer_boundary": {
            "benchmark_prompts_transferred": 0,
            "benchmark_queries_transferred": 0,
            "benchmark_source_documents_transferred": 0,
            "benchmark_candidate_texts_transferred": 0,
            "synthetic_embedding_texts_transferred": 1,
            "synthetic_reranker_queries_transferred": 1,
            "synthetic_reranker_documents_transferred": 2,
        },
        "credential_boundary": {
            "environment_variable_name": "DASHSCOPE_API_KEY",
            "credential_value_recorded": False,
            "authorization_header_recorded": False,
            "dotenv_scanned_by_this_builder": False,
        },
        "sanitisation": {
            "raw_request_text_recorded": False,
            "raw_provider_response_recorded": False,
            "credentials_or_headers_recorded": False,
            "retained_fields": ["endpoint", "model", "call/input counts", "dimensions", "usage counts", "synthetic reranker scores", "status"],
        },
        "boundary": {
            "scientific_result": False,
            "benchmark_result": False,
            "execution_authorisation": False,
            "provider_contract_validation_only": True,
            "may_not_be_used_to_claim_full_matrix_readiness_or_performance": True,
            "zero_inference_preflight_rewritten": False,
            "builder_network_calls": 0,
        },
    }
    validate_receipt(value)
    return value


def validate_receipt(value: dict[str, Any]) -> None:
    require(value.get("schema_version") == "rq2b-v7-b36-c6-provider-connectivity-receipt-v1", "Connectivity receipt schema drift")
    require(value.get("bindings") == INPUT_BINDINGS, "Connectivity receipt input binding drift")
    calls = value.get("provider_calls", {})
    require(calls.get("total") == 2, "Connectivity receipt call-total drift")
    embedding = calls.get("embedding", {})
    require(embedding.get("calls") == 1 and embedding.get("synthetic_texts") == 1, "Embedding connectivity scope drift")
    require(embedding.get("model") == "text-embedding-v4" and embedding.get("embedding_dimensions") == 1024, "Embedding connectivity contract drift")
    require(embedding.get("endpoint") == "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings", "Embedding endpoint drift")
    require(embedding.get("usage") == {"prompt_tokens": 11, "total_tokens": 11}, "Embedding usage drift")
    reranker = calls.get("reranker", {})
    require(reranker.get("calls") == 1 and reranker.get("synthetic_queries") == 1 and reranker.get("synthetic_documents") == 2, "Reranker connectivity scope drift")
    require(reranker.get("model") == "qwen3-rerank", "Reranker connectivity model drift")
    require(reranker.get("endpoint") == "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank", "Reranker endpoint drift")
    scores = reranker.get("scores")
    require(isinstance(scores, list) and len(scores) == 2, "Reranker connectivity score coverage drift")
    require(all(isinstance(score, (int, float)) and math.isfinite(float(score)) for score in scores), "Reranker connectivity score is non-finite")
    require(reranker.get("usage") == {"total_tokens": 60}, "Reranker usage drift")
    transfer = value.get("transfer_boundary", {})
    require(all(transfer.get(key) == 0 for key in (
        "benchmark_prompts_transferred",
        "benchmark_queries_transferred",
        "benchmark_source_documents_transferred",
        "benchmark_candidate_texts_transferred",
    )), "Connectivity receipt contains benchmark transfer")
    credential = value.get("credential_boundary", {})
    require(credential.get("environment_variable_name") == "DASHSCOPE_API_KEY", "Credential variable-name drift")
    require(credential.get("credential_value_recorded") is False and credential.get("authorization_header_recorded") is False, "Connectivity receipt retained credential material")
    sanitisation = value.get("sanitisation", {})
    require(all(sanitisation.get(key) is False for key in ("raw_request_text_recorded", "raw_provider_response_recorded", "credentials_or_headers_recorded")), "Connectivity receipt retained a forbidden raw field")
    boundary = value.get("boundary", {})
    require(boundary.get("scientific_result") is False and boundary.get("benchmark_result") is False, "Connectivity receipt misclassified as a result")
    require(boundary.get("execution_authorisation") is False and boundary.get("builder_network_calls") == 0, "Connectivity receipt misclassified as execution authorisation")
    require(boundary.get("zero_inference_preflight_rewritten") is False, "Connectivity receipt claims to rewrite zero-inference preflight")


def markdown_bytes(value: dict[str, Any]) -> bytes:
    embedding = value["provider_calls"]["embedding"]
    reranker = value["provider_calls"]["reranker"]
    text = f"""# V7 B36+C6 sanitised provider-connectivity receipt v1

Status: `PASS_SANITISED_SYNTHETIC_CONNECTIVITY_RECEIPT_NOT_SCIENTIFIC_EXECUTION`.

Under explicit synthetic-only authorisation, two connectivity calls were completed:

- DashScope `text-embedding-v4`: one synthetic text, {embedding['embedding_dimensions']} dimensions, 11 prompt/total tokens.
- DashScope `qwen3-rerank`: one synthetic query and two synthetic documents, total tokens 60, scores `{reranker['scores']}`.

Transferred benchmark prompts, benchmark queries, benchmark source documents and benchmark candidate texts: **zero**. The synthetic input text, raw request/response, credential value and authorisation header are not retained. Only the credential variable name `DASHSCOPE_API_KEY` is recorded.

This receipt establishes endpoint/model connectivity for the two frozen request contracts. It is not a scientific or benchmark result, does not establish full-matrix readiness, does not authorise another call, and does not modify the zero-inference runtime preflight.

## Bound evidence

- Zero-inference preflight report SHA-256: `{value['bindings']['zero_inference_preflight_report']['sha256']}`
- Qwen embedding contract script SHA-256: `{value['bindings']['qwen_embedding_contract_source']['sha256']}`
- Qwen reranker contract script SHA-256: `{value['bindings']['qwen_reranker_contract_source']['sha256']}`

## Exact zero-network replay

```sh
python3 -B skill_benchmark/scripts/verify_rq2b_v7_first_matrix_provider_connectivity_receipt.py
python3 -B skill_benchmark/scripts/test_rq2b_v7_first_matrix_provider_connectivity_receipt.py
git diff --check
```

These replay commands validate the sanitised receipt and its local bindings. They make no provider call and read no key.
"""
    return text.encode("utf-8")


def artifacts() -> dict[str, bytes]:
    value = receipt()
    return {
        "connectivity_receipt.json": json_bytes(value),
        "connectivity_receipt.md": markdown_bytes(value),
    }


def build() -> None:
    outputs = artifacts()
    require(not PACKAGE.exists(), f"Refusing to overwrite existing package: {PACKAGE}")
    PACKAGE.mkdir(parents=True, exist_ok=False)
    for name, data in outputs.items():
        with (PACKAGE / name).open("xb") as handle:
            handle.write(data)


def verify() -> dict[str, Any]:
    outputs = artifacts()
    require(PACKAGE.is_dir(), f"Missing connectivity receipt package: {PACKAGE}")
    require({path.name for path in PACKAGE.iterdir() if path.is_file()} == set(outputs), "Connectivity receipt package file-set drift")
    for name, expected in outputs.items():
        require((PACKAGE / name).read_bytes() == expected, f"Connectivity receipt replay mismatch: {name}")
    return {
        "status": "PASS_SANITISED_SYNTHETIC_CONNECTIVITY_RECEIPT_REPLAY",
        "package": str(PACKAGE.relative_to(ROOT)),
        "files": {name: sha256_file(PACKAGE / name) for name in sorted(outputs)},
        "provider_calls_replayed": 0,
        "credential_values_read": 0,
        "benchmark_texts_read": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.build:
        build()
        output = {"status": "PASS_CONNECTIVITY_RECEIPT_CREATED", "package": str(PACKAGE.relative_to(ROOT))}
    else:
        output = verify()
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
