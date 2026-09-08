#!/usr/bin/env python3
"""Build or replay the zero-inference V7 B36+C6 runtime preflight.

This script inventories a specific local Python environment, exact ignored
model snapshots, provider request contracts, and operator-supplied smoke
dispositions.  It never loads a model, reads a dotenv file, contacts a
provider, opens benchmark labels/results, or authorises scientific execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import sys
from importlib import metadata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_runtime_preflight_2026_09_09_v1"
)
VENV_RELATIVE = ".venv-rq2b-v7"
SCHEMA_VERSION = "rq2b-v7-b36-c6-runtime-preflight-v1"
CPU_AUDIT_NAMESPACE = "rq2b-v7-b36-c6-runtime-cpu-audit-v1"
CPU_AUDIT_PER_REPRESENTATION = 8
REPRESENTATIONS = ("I1-discovery", "I2-original", "I3C-fielded", "I3-flat")


EXPECTED_ENVIRONMENT = {
    "implementation": "CPython",
    "machine": "arm64",
    "platform": "macOS-26.5.2-arm64-arm-64bit-Mach-O",
    "python": "3.13.2",
}

EXPECTED_PACKAGES = {
    "accelerate": "1.10.1",
    "certifi": "2026.7.22",
    "charset-normalizer": "3.5.1",
    "filelock": "3.32.5",
    "fsspec": "2026.7.0",
    "hf-xet": "1.6.0",
    "huggingface-hub": "0.36.0",
    "idna": "3.19",
    "jinja2": "3.1.6",
    "markupsafe": "3.0.3",
    "mpmath": "1.3.0",
    "networkx": "3.6.1",
    "numpy": "2.3.3",
    "packaging": "26.3",
    "psutil": "7.2.2",
    "pyyaml": "6.0.3",
    "regex": "2026.9.3",
    "requests": "2.34.2",
    "safetensors": "0.6.2",
    "setuptools": "84.0.0",
    "sympy": "1.14.0",
    "tokenizers": "0.22.2",
    "torch": "2.8.0",
    "tqdm": "4.70.0",
    "transformers": "4.56.2",
    "typing-extensions": "4.16.0",
    "urllib3": "2.7.0",
}

INPUT_BINDINGS = {
    "v7_core_conditions": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl",
        "sha256": "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
        "bytes": 17961,
    },
    "v7_bridge_conditions": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/fixed_candidate_bridge_conditions.jsonl",
        "sha256": "d659ff98a5a2534478f68ab44794e4df7d89b23eb3a44a2fbf335cdca42366f7",
        "bytes": 3072,
    },
    "v7_preparation_readiness": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/readiness_report.json",
        "sha256": "55f666bc3daa96f3e37f7209761b4a0c06eb7aaf14484db0a4b7d6aea94725e0",
        "bytes": 2430,
    },
    "embedding_lineage_constants": {
        "path": "skill_benchmark/scripts/rq2bv1_v3_skillrouter_primary_constants.py",
        "sha256": "b925260ffd80fd0e619aeb8b997adb3a7b53e31cf13d618b1a2623b627436926",
    },
    "embedding_lineage_runner": {
        "path": "skill_benchmark/scripts/run_rq2bv1_v3_skillrouter_primary.py",
        "sha256": "f335f9fe9da9fed3802cf5ce4991e3a75cbf5d80824b34467935d69af99b4e7b",
    },
    "reranker_lineage_runner": {
        "path": "skill_benchmark/scripts/hf_rq2bv1_v3_b2_skillrouter_reranker_job.py",
        "sha256": "3517a1c1c8a375285b98a08da5ebf38184aa518fd1908606d7e7a4f5cd84c4a2",
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

MODEL_SNAPSHOTS = {
    "skillrouter_embedding": {
        "repository": "pipizhao/SkillRouter-Embedding-0.6B",
        "revision": "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558",
        "snapshot_path": "skill_benchmark/cache/huggingface/SkillRouter-Embedding-0.6B-c03c9bcee9fc",
        "files": {
            "added_tokens.json": "c0284b582e14987fbd3d5a2cb2bd139084371ed9acbae488829a1c900833c680",
            "config.json": "02b34f6be10ee6a35304e32b67ac37be4b2b04e327efff49a689136b0913a0e8",
            "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
            "model.safetensors": "cbab45b8a3c786b8c23aedb24fb22aff74d0e9b62a52369a3090c37f26b00360",
            "special_tokens_map.json": "76862e765266b85aa9459767e33cbaf13970f327a0e88d1c65846c2ddd3a1ecd",
            "tokenizer.json": "def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a",
            "tokenizer_config.json": "7f33cbb21bae9b2ed4a7396d68f9f10d6280d75332d04911cd6c5a0967bd10c9",
            "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
        },
    },
    "skillrouter_reranker": {
        "repository": "pipizhao/SkillRouter-Reranker-0.6B",
        "revision": "78986e1142d12857cfd85b8005e62902cd42d858",
        "snapshot_path": "skill_benchmark/cache/huggingface/SkillRouter-Reranker-0.6B-78986e1142d1",
        "files": {
            "added_tokens.json": "c0284b582e14987fbd3d5a2cb2bd139084371ed9acbae488829a1c900833c680",
            "config.json": "17f3b5063350823bfda01f740ac14b9d1cd9cb80c738cbe0d9939c4988ac6b39",
            "generation_config.json": "b015f739ce02d6f51f0fbd1fbd6bfd22436983139cfb51514c86fa1ffe5dfef5",
            "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
            "model.safetensors": "34064850b1b512168309481a9cebe4ecaf55d0821bf22608f657b40033ed36d7",
            "special_tokens_map.json": "76862e765266b85aa9459767e33cbaf13970f327a0e88d1c65846c2ddd3a1ecd",
            "tokenizer.json": "ab19c66299579df20542864f9e27b79898ca05f35acc97fd9259aee385a07d4a",
            "tokenizer_config.json": "7f33cbb21bae9b2ed4a7396d68f9f10d6280d75332d04911cd6c5a0967bd10c9",
            "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
        },
    },
}

SMOKE_CASES = [
    {
        "case_id": "embedding-default-sdpa-mps-float32-heterogeneous-left-padding",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "float32",
        "batch_shape": "heterogeneous_token_lengths_with_left_padding",
        "output_finite": False,
        "disposition": "INVALID_NON_FINITE",
    },
    {
        "case_id": "embedding-default-sdpa-mps-float16-heterogeneous-left-padding",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "float16",
        "batch_shape": "heterogeneous_token_lengths_with_left_padding",
        "output_finite": False,
        "disposition": "INVALID_NON_FINITE",
    },
    {
        "case_id": "embedding-default-sdpa-mps-float32-single-unpadded",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "float32",
        "batch_shape": "single_row_unpadded",
        "output_finite": True,
        "dimensions": 1024,
        "disposition": "VALID_SMOKE",
    },
    {
        "case_id": "reranker-default-sdpa-mps-float32-single-unpadded",
        "component": "SkillRouter-Reranker-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "float32",
        "batch_shape": "single_row_unpadded",
        "output_finite": True,
        "scores": [-0.06677818],
        "disposition": "VALID_SMOKE",
    },
    {
        "case_id": "embedding-default-sdpa-mps-float32-exact-length-batch16",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "float32",
        "batch_shape": "16_identical_exact_token_length_rows_no_padding",
        "output_finite": True,
        "dimensions": 1024,
        "scores": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "score_semantics": "cosine_against_first_identical_row",
        "disposition": "VALID_DIAGNOSTIC_SMOKE",
    },
    {
        "case_id": "reranker-default-sdpa-mps-float32-exact-length-batch16",
        "component": "SkillRouter-Reranker-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "float32",
        "batch_shape": "16_identical_exact_token_length_rows_no_padding",
        "output_finite": True,
        "scores": [-0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124, -0.0667858124],
        "forward_seconds": 0.232,
        "disposition": "VALID_DIAGNOSTIC_SMOKE",
    },
    {
        "case_id": "embedding-default-sdpa-mps-bfloat16-exact-length-batch16",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "bfloat16",
        "batch_shape": "16_identical_exact_token_length_rows_no_padding",
        "output_finite": True,
        "dimensions": 1024,
        "scores": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "score_semantics": "cosine_against_first_identical_row",
        "disposition": "VALID_PRIMARY_RUNTIME_SMOKE",
    },
    {
        "case_id": "reranker-default-sdpa-mps-bfloat16-short-unpadded",
        "component": "SkillRouter-Reranker-0.6B",
        "device": "mps",
        "attention_implementation": "default_sdpa",
        "dtype": "bfloat16",
        "batch_shape": "16_short_exact_token_length_rows_no_padding",
        "output_finite": True,
        "score_observations": {
            "relevant_yes_minus_no": 0.0,
            "irrelevant_yes_minus_no_approximate": -5.25
        },
        "disposition": "VALID_PRIMARY_RUNTIME_SMOKE_WITH_NUMERICAL_TIE_LIMITATION",
    },
    {
        "case_id": "embedding-eager-mps-float32",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "mps",
        "attention_implementation": "eager",
        "dtype": "float32",
        "output_finite": True,
        "dimensions": 1024,
        "scores": [0.7236307263, 0.1343006194],
        "disposition": "VALID_SMOKE",
    },
    {
        "case_id": "embedding-eager-cpu-float32",
        "component": "SkillRouter-Embedding-0.6B",
        "device": "cpu",
        "attention_implementation": "eager",
        "dtype": "float32",
        "output_finite": True,
        "dimensions": 1024,
        "scores": [0.7236300707, 0.1343012303],
        "disposition": "VALID_CPU_REFERENCE_SMOKE",
    },
    {
        "case_id": "reranker-eager-mps-float32",
        "component": "SkillRouter-Reranker-0.6B",
        "device": "mps",
        "attention_implementation": "eager",
        "dtype": "float32",
        "output_finite": True,
        "scores": [-0.0667819977, -5.2218322754],
        "disposition": "VALID_SMOKE",
    },
    {
        "case_id": "reranker-eager-cpu-float32",
        "component": "SkillRouter-Reranker-0.6B",
        "device": "cpu",
        "attention_implementation": "eager",
        "dtype": "float32",
        "output_finite": True,
        "scores": [-0.0667953491, -5.2218294144],
        "disposition": "VALID_CPU_REFERENCE_SMOKE",
    },
]

LONG_SEQUENCE_PROBES = [
    {
        "case_id": "embedding-mps-default-sdpa-float32-30000-single-unpadded",
        "input_tokens": 30000,
        "dtype": "float32",
        "output_finite": False,
        "disposition": "INVALID_HARD_MEMORY_FAILURE",
        "failure": "Invalid buffer size 53.64 GiB",
    },
    {
        "case_id": "embedding-mps-default-sdpa-float32-4096-single-unpadded",
        "input_tokens": 4096,
        "dtype": "float32",
        "output_finite": True,
        "forward_seconds": 78.83,
        "disposition": "VALID_BUT_NOT_PRIMARY_RUNTIME",
    },
    {
        "case_id": "embedding-mps-default-sdpa-bfloat16-4096-single-unpadded",
        "input_tokens": 4096,
        "dtype": "bfloat16",
        "output_finite": True,
        "forward_seconds_range": [2.81, 3.88],
        "disposition": "VALID_PRIMARY_RUNTIME_PROBE",
    },
    {
        "case_id": "embedding-mps-default-sdpa-bfloat16-7500-single-unpadded",
        "input_tokens": 7500,
        "dtype": "bfloat16",
        "output_finite": True,
        "forward_seconds": 10.65,
        "disposition": "VALID_PROPOSED_WINDOW_CEILING_PROBE",
    },
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def canonical_package_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def observed_packages() -> dict[str, str]:
    observed: dict[str, str] = {}
    for distribution in metadata.distributions():
        raw_name = distribution.metadata.get("Name")
        require(bool(raw_name), "Installed distribution lacks a Name field")
        name = canonical_package_name(str(raw_name))
        require(name not in observed, f"Duplicate installed distribution: {name}")
        observed[name] = distribution.version
    return dict(sorted(observed.items()))


def validate_finite_scores(values: list[float], *, expected_length: int | None = None) -> None:
    require(isinstance(values, list) and bool(values), "Model score output is empty")
    if expected_length is not None:
        require(len(values) == expected_length, "Model score output length drift")
    require(all(isinstance(value, (int, float)) and math.isfinite(float(value)) for value in values), "Model score output is non-finite")


def select_cpu_audit_ids(stable_ids: list[str], *, component: str, representation: str, count: int = CPU_AUDIT_PER_REPRESENTATION) -> list[str]:
    require(representation in REPRESENTATIONS, "Unknown CPU-audit representation")
    require(len(stable_ids) == len(set(stable_ids)), "CPU-audit stable IDs are not unique")
    require(count > 0, "CPU-audit count must be positive")
    return sorted(
        stable_ids,
        key=lambda stable_id: (
            hashlib.sha256(f"{CPU_AUDIT_NAMESPACE}|{component}|{representation}|{stable_id}".encode()).hexdigest(),
            stable_id,
        ),
    )[: min(count, len(stable_ids))]


def _check_bindings() -> None:
    for name, binding in INPUT_BINDINGS.items():
        path = ROOT / binding["path"]
        require(path.is_file(), f"Missing input binding {name}: {path}")
        require(sha256_file(path) == binding["sha256"], f"Input binding hash drift: {name}")
        if "bytes" in binding:
            require(path.stat().st_size == binding["bytes"], f"Input binding byte-size drift: {name}")
    for name, snapshot in MODEL_SNAPSHOTS.items():
        root = ROOT / snapshot["snapshot_path"]
        require(root.is_dir(), f"Missing ignored model snapshot: {name}")
        for filename, expected_sha in snapshot["files"].items():
            path = root / filename
            require(path.is_file(), f"Missing pinned model file: {name}/{filename}")
            require(sha256_file(path) == expected_sha, f"Pinned model file hash drift: {name}/{filename}")


def _environment_inventory() -> dict[str, Any]:
    require(Path(sys.prefix).resolve() == (ROOT / VENV_RELATIVE).resolve(), f"Run with {VENV_RELATIVE}/bin/python")
    environment = {
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "platform": platform.platform(),
        "python": platform.python_version(),
    }
    require(environment == EXPECTED_ENVIRONMENT, "Python/platform inventory drift")
    packages = observed_packages()
    require(packages == EXPECTED_PACKAGES, "Installed package inventory drift")
    import torch

    require(torch.__version__ == EXPECTED_PACKAGES["torch"], "Imported torch version drift")
    return {
        **environment,
        "venv_path": VENV_RELATIVE,
        "packages": packages,
        "torch_backend": {
            "mps_built": bool(torch.backends.mps.is_built()),
            "mps_available_in_verifier_process": bool(torch.backends.mps.is_available()),
        },
    }


def _smoke_evidence() -> dict[str, Any]:
    for row in SMOKE_CASES:
        if row["output_finite"] and "scores" in row:
            validate_finite_scores(row["scores"])
    by_id = {row["case_id"]: row for row in SMOKE_CASES}
    embedding_mps = by_id["embedding-eager-mps-float32"]["scores"]
    embedding_cpu = by_id["embedding-eager-cpu-float32"]["scores"]
    reranker_mps = by_id["reranker-eager-mps-float32"]["scores"]
    reranker_cpu = by_id["reranker-eager-cpu-float32"]["scores"]
    embedding_delta = max(abs(a - b) for a, b in zip(embedding_mps, embedding_cpu, strict=True))
    reranker_delta = max(abs(a - b) for a, b in zip(reranker_mps, reranker_cpu, strict=True))
    require(abs(embedding_delta - 0.0000006556) < 1e-12, "Embedding smoke delta drift")
    require(abs(reranker_delta - 0.0000133514) < 1e-12, "Reranker smoke delta drift")
    return {
        "evidence_status": "OPERATOR_VERIFIED_SMOKE_SUMMARY_RECORDED_NOT_REEXECUTED_BY_BUILDER",
        "cases": SMOKE_CASES,
        "cross_device_max_absolute_score_delta": {
            "SkillRouter-Embedding-0.6B": embedding_delta,
            "SkillRouter-Reranker-0.6B": reranker_delta,
        },
        "interpretation": "Default SDPA is valid for short unpadded exact-token-length batches. Only heterogeneous left-padded default-attention batches are invalid. MPS bfloat16 is primary; MPS/CPU float32 and eager results are diagnostic/sensitivity evidence. The bfloat16 reranker can quantise a relevant yes-minus-no score to zero, creating a numerical/tie limitation that must be reported.",
    }


def runtime_inventory() -> dict[str, Any]:
    _check_bindings()
    environment = _environment_inventory()
    dashscope_present = bool(os.environ.get("DASHSCOPE_API_KEY"))
    blockers = []
    if not environment["torch_backend"]["mps_available_in_verifier_process"]:
        blockers.append("MPS_UNAVAILABLE_IN_CURRENT_VERIFIER_PROCESS")
    if not dashscope_present:
        blockers.append("DASHSCOPE_API_KEY_ABSENT_FROM_CURRENT_PROCESS")
    blockers.extend([
        "PROSPECTIVE_LOSSLESS_7500_TOKEN_256_OVERLAP_MAX_WINDOW_ADAPTATION_PENDING_APPROVAL",
        "I3C_AND_I3_FLAT_TOKEN_LENGTH_AUDITS_PENDING",
    ])
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS_ZERO_INFERENCE_RUNTIME_INVENTORY_EXECUTION_NOT_AUTHORISED",
        "scope": {
            "benchmark": "RQ2b-NC V7 frozen library",
            "matrix": "B36+C6",
            "core_configurations": 36,
            "fixed_candidate_bridge_configurations": 6,
            "prompt_count": 1077,
            "representations": list(REPRESENTATIONS),
            "runtime_rerank_k": 20,
            "audit_main_k": 6,
            "v7_input_bindings": INPUT_BINDINGS,
        },
        "environment": environment,
        "local_models": {
            **MODEL_SNAPSHOTS,
            "shared_policy": {
                "local_files_only": True,
                "trust_remote_code": False,
                "downloaded_snapshots_are_ignored_runtime_inputs": True,
            },
            "embedding_contract": {
                "architecture": "AutoModel/Qwen3Model",
                "dimensions": 1024,
                "maximum_model_tokens": 32768,
                "padding_side": "left",
                "pooling": "last_non_padding_token",
                "normalisation": "l2",
                "document_query_score": "cosine",
                "query_instruction": "Instruct: Given a task description, retrieve the most relevant skill document that would help an agent complete the task\nQuery:",
            },
            "reranker_contract": {
                "architecture": "AutoModelForCausalLM/Qwen3ForCausalLM",
                "maximum_pair_tokens": 2048,
                "padding_side": "left",
                "pair_score": "final_token_yes_logit_minus_no_logit",
                "instruction": "Given a task description, judge whether the skill document is relevant and useful for completing the task",
            },
            "reuse_boundary": "V3 constants, tokenizer/model semantics and pinned revisions are reusable lineage. V3 CUDA/bfloat16 runners and their old 2,433-skill/381-prompt payload assumptions are not V7 scientific runners.",
        },
        "dashscope_contracts": {
            "credential": {
                "environment_variable": "DASHSCOPE_API_KEY",
                "present_in_current_process": dashscope_present,
                "presence_only_check": True,
                "secret_value_serialised": False,
                "dotenv_files_scanned": False,
            },
            "embedding": {
                "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
                "endpoint": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings",
                "model": "text-embedding-v4",
                "dimensions": 1024,
                "encoding_format": "float",
                "maximum_batch_texts": 10,
                "request_shape": {"model": "string", "input": "array[string]", "dimensions": "integer", "encoding_format": "float"},
                "response_gate": "exact request coverage, 1024 dimensions, every coordinate finite",
            },
            "reranker": {
                "endpoint": "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
                "model": "qwen3-rerank",
                "request_shape": {"model": "string", "input": {"query": "string", "documents": "array[string]"}, "parameters": {"return_documents": False, "top_n": "requested document count", "instruct": "frozen instruction"}},
                "response_gate": "one unique index per requested document, exact coverage, every relevance_score finite",
            },
        },
        "scientific_runtime_contract": {
            "device": "mps",
            "attention_implementation": "default_sdpa",
            "dtype": "bfloat16",
            "batching": {
                "maximum_batch_size": 16,
                "bucket_key": "exact_model_input_token_length",
                "padding_allowed": False,
                "heterogeneous_token_length_batch_allowed": False,
            },
            "eager_attention_disposition": "diagnostic_and_traceable_fallback_only_not_primary; any fallback requires an explicit runtime amendment and may not be silent",
            "forbidden_fallbacks": ["heterogeneous left-padded batches", "float16", "silent float32 substitution", "silent eager-attention substitution", "silent CPU fallback", "non-finite persistence or ranking"],
            "fail_closed_output_gate": {
                "before_cache_write": True,
                "before_score_persistence": True,
                "before_ranking": True,
                "embedding_dimensions": 1024,
                "all_model_outputs_finite": True,
                "on_failure": "abort current shard/condition without result write; preserve attempt evidence",
            },
            "cpu_audit_spot_check": {
                "required_before_scientific_finalisation": True,
                "selection_namespace": CPU_AUDIT_NAMESPACE,
                "selection": "for each local model and representation, take the 8 stable IDs with lexicographically smallest SHA-256(namespace|component|representation|stable_id), or all when fewer",
                "per_model_per_representation": CPU_AUDIT_PER_REPRESENTATION,
                "maximum_units_per_model": CPU_AUDIT_PER_REPRESENTATION * len(REPRESENTATIONS),
                "cpu_runtime": {"device": "cpu", "attention_implementation": "eager", "dtype": "float32"},
                "comparison": "record same scalar pair score, absolute delta, rank/tie changes and output finiteness; embedding uses cosine, reranker uses yes-minus-no logit",
                "equivalence_threshold": None,
                "interpretation": "Sensitivity analysis, not a device-equivalence gate. Disclose bfloat16 quantisation/ties and any rank changes; do not select a runtime post hoc from results.",
                "on_nonfinite_output": "invalidate local-model scientific run pending diagnosis; do not silently substitute CPU results",
            },
            "reranker_numerical_limitation": {
                "observed": "a short relevant example's bfloat16 yes-minus-no score quantised to 0 while an irrelevant example was approximately -5.25",
                "required_reporting": ["exact score ties", "deterministic tie breaks", "CPU-fp32 spot sensitivity"],
                "tie_break_contract_pending_runner_seal": "preserve persisted candidate order, then stable candidate ID; do not add random jitter",
            },
        },
        "source_token_length_audit": {
            "evidence_status": "OPERATOR_VERIFIED_TOKEN_AUDIT_SUMMARY_RECORDED_NOT_REPLAYED_BY_BUILDER",
            "I1-discovery": {"maximum_tokens": 419, "over_7500": 0, "over_16000": 0, "over_32768": 0},
            "I2-original": {"maximum_tokens": 56648, "over_7500": 28, "over_16000": 4, "over_32768": 1},
            "I3C-fielded": {"status": "PENDING_TOKEN_AUDIT"},
            "I3-flat": {"status": "PENDING_TOKEN_AUDIT"},
            "skillrouter_embedding_max_position_embeddings": 32768,
            "prospective_hardware_adaptation": {
                "status": "PROPOSED_NOT_APPROVED_HARD_GATE",
                "applies_only_to_documents_over_tokens": 7500,
                "known_I2_documents_in_scope": 28,
                "window_tokens": 7500,
                "overlap_tokens": 256,
                "document_score_aggregation": "maximum_window_score",
                "lossless_full_text_coverage_required": True,
                "classification": "pipeline_hardware_adaptation_not_a_change_to_source_representation",
                "forbidden": ["silent truncation", "source exclusion", "representation substitution", "post-hoc threshold choice"],
                "gate": "Audit I3C/I3-flat lengths and prospectively approve/seal this adaptation before any affected SkillRouter execution.",
            },
        },
        "smoke_evidence": _smoke_evidence(),
        "long_sequence_runtime_probes": {
            "evidence_status": "OPERATOR_VERIFIED_PROBE_SUMMARY_RECORDED_NOT_REEXECUTED_BY_BUILDER",
            "cases": LONG_SEQUENCE_PROBES,
            "interpretation": "MPS float32 is impractical and fails hard at 30k. MPS bfloat16 was finite at 4,096 and 7,500 tokens; the 7,500 ceiling remains a proposed hardware adaptation, not an approved method change.",
        },
        "current_execution_disposition": {
            "execution_authorised": False,
            "retrieval_or_reranking_performed_by_this_package": False,
            "provider_calls_performed_by_this_package": 0,
            "model_forward_passes_performed_by_this_package": 0,
            "labels_or_results_read": False,
            "current_process_blockers": blockers,
            "required_next_artifact": "a separate hash-bound V7 scientific runner/authorisation package that enforces this contract",
        },
    }


def readme_bytes(inventory: dict[str, Any]) -> bytes:
    key_present = str(inventory["dashscope_contracts"]["credential"]["present_in_current_process"]).lower()
    mps_available = str(inventory["environment"]["torch_backend"]["mps_available_in_verifier_process"]).lower()
    text = f"""# V7 B36+C6 runtime preflight v1

Status: `PASS_ZERO_INFERENCE_RUNTIME_INVENTORY_EXECUTION_NOT_AUTHORISED`.

This package binds the V7 36-condition core matrix plus six fixed-candidate bridges to one exact local Python environment, two pinned local SkillRouter snapshots, the two DashScope request contracts, and the supplied verified smoke dispositions. It is a runtime inventory and fail-closed execution contract, not a retrieval/reranking runner or an authorisation receipt.

## Frozen scientific local runtime

- device: `mps`
- attention implementation: default SDPA
- dtype: `bfloat16`
- batching: exact input-token-length buckets only, no padding, maximum batch size 16
- SkillRouter embedding output: exactly 1,024 finite coordinates before caching or scoring
- SkillRouter reranker output: finite yes-logit-minus-no-logit score before persistence or ranking
- no heterogeneous left-padded batch, float16, silent fp32/eager substitution or silent CPU fallback
- deterministic CPU eager/fp32 sensitivity spot-check: eight lowest hash-bound stable IDs per representation and local model; record score deltas and rank/tie changes without treating CPU as a silent substitute

The corrected smoke evidence localises the default-attention failure to heterogeneous left-padded batches. Default-SDPA MPS bfloat16 is finite for short exact-token-length unpadded batches; embedding identical-row cosine was 1.0. The short reranker probe was finite, but its relevant yes-minus-no score quantised to 0 while the irrelevant example was about -5.25. That is a numerical/tie limitation, so exact ties and CPU-fp32 sensitivity must be reported. Eager and fp32 results remain diagnostic/reference evidence, not the primary setting. The builder records these supplied dispositions but deliberately does not rerun a model.

The supplied token audit records I1 max 419 tokens and I2 max 56,648 tokens. I2 has 28 sources above 7,500, four above 16,000 and one above the embedding model's 32,768-position limit; I3C and I3-flat still need the same audit. A 30k fp32 probe failed with `Invalid buffer size 53.64 GiB`; fp32 at 4,096 was finite but took 78.83 seconds, while bfloat16 was finite at 4,096 (2.81--3.88 seconds) and 7,500 (10.65 seconds).

The suggested 7,500-token/256-overlap/max-window approach for only over-threshold documents is recorded as `PROPOSED_NOT_APPROVED_HARD_GATE`. It must preserve every token and be classified as a pipeline hardware adaptation. It cannot be silently truncated, excluded, substituted or executed until the remaining length audit and prospective amendment are approved and sealed.

## Current-process observations

- `DASHSCOPE_API_KEY` present: `{key_present}` (boolean only; no value is serialised and no dotenv is scanned)
- PyTorch MPS built: `true`
- PyTorch MPS available in this verifier process: `{mps_available}`

These observations do not override the smoke evidence. Any absent credential or unavailable MPS backend blocks execution in that process; it does not license a fallback. A later execution attempt must reissue or extend the preflight if the bound environment changes.

## Exact replay

From the repository root:

```sh
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/verify_rq2b_v7_first_matrix_runtime_preflight.py
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_first_matrix_runtime_preflight.py
git diff --check
```

The replay hashes only named tracked inputs and named ignored snapshot files. It does not read `.env`, model tensors, benchmark labels, acceptable sets or result files. It makes zero network calls and zero model forward passes.

## Boundary

The pinned V3 SkillRouter constants and model semantics are lineage inputs only. Existing V3 hosted CUDA/bfloat16 runners embed old 2,433-skill/381-prompt payload assumptions and are not valid V7 B36+C6 runners. Likewise, this package freezes provider endpoints and payload/response gates but does not authorise DashScope use. A separate V7 payload, runner and explicit execution receipt remain required.
"""
    return text.encode("utf-8")


def build_artifacts() -> dict[str, bytes]:
    inventory = runtime_inventory()
    inventory_data = json_bytes(inventory)
    readme_data = readme_bytes(inventory)
    tooling_paths = {
        "builder": Path(__file__).resolve(),
        "verifier": ROOT / "skill_benchmark/scripts/verify_rq2b_v7_first_matrix_runtime_preflight.py",
        "tests": ROOT / "skill_benchmark/scripts/test_rq2b_v7_first_matrix_runtime_preflight.py",
    }
    for name, path in tooling_paths.items():
        require(path.is_file(), f"Missing runtime preflight {name}: {path}")
    report = {
        "schema_version": "rq2b-v7-b36-c6-runtime-preflight-integrity-v1",
        "status": "PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY",
        "counts": {
            "core_configurations": 36,
            "bridge_configurations": 6,
            "installed_packages": len(EXPECTED_PACKAGES),
            "local_model_snapshots": len(MODEL_SNAPSHOTS),
            "pinned_model_files": sum(len(value["files"]) for value in MODEL_SNAPSHOTS.values()),
            "smoke_cases": len(SMOKE_CASES),
            "long_sequence_probes": len(LONG_SEQUENCE_PROBES),
        },
        "checks": {
            "v7_matrix_bindings": True,
            "python_platform_exact": True,
            "package_inventory_exact": True,
            "model_revisions_and_file_hashes": True,
            "provider_contracts_bound": True,
            "credential_recorded_as_boolean_only": True,
            "scientific_runtime_mps_default_sdpa_bfloat16_exact_length_unpadded": True,
            "nonfinite_output_fail_closed": True,
            "deterministic_cpu_audit_spot_check": True,
            "prospective_lossless_7500_256_max_window_adaptation_gate_recorded_not_approved": True,
            "remaining_representation_token_audits_recorded": True,
            "zero_network": True,
            "zero_model_forward": True,
            "labels_and_results_unread": True,
            "execution_authorised": False,
        },
        "artifacts": {
            "runtime_inventory.json": {"sha256": sha256_bytes(inventory_data), "bytes": len(inventory_data)},
            "README.md": {"sha256": sha256_bytes(readme_data), "bytes": len(readme_data)},
        },
        "tooling": {
            name: {"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path)}
            for name, path in sorted(tooling_paths.items())
        },
        "current_process_blockers": inventory["current_execution_disposition"]["current_process_blockers"],
        "scope_boundary": "Integrity PASS means inventory replay only. It is not scientific execution readiness or permission.",
    }
    report_data = json_bytes(report)
    report_md = f"""# V7 B36+C6 runtime preflight integrity

Status: `PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY`.

- V7 matrix: 36 core + 6 fixed-candidate bridge configurations
- Python packages: {len(EXPECTED_PACKAGES)} exact distributions
- SkillRouter snapshots: 2 exact revisions, {sum(len(value['files']) for value in MODEL_SNAPSHOTS.values())} pinned runtime files
- Smoke evidence: {len(SMOKE_CASES)} supplied verified cases; no case rerun by this builder
- Primary local runtime: MPS bfloat16, default SDPA, exact-token-length unpadded buckets, batch at most 16
- Long-sequence probes: {len(LONG_SEQUENCE_PROBES)} supplied observations; none rerun by this builder
- Adaptation gate: 7,500-token/256-overlap/max-window is proposed, not approved; I3C/I3-flat length audits remain pending
- Network calls: 0
- Model forward passes: 0
- Labels/results read: false
- Execution authorised: false
- Current-process blockers: {', '.join(report['current_process_blockers']) if report['current_process_blockers'] else 'none observed'}

Artifact hashes:

- `runtime_inventory.json`: `{report['artifacts']['runtime_inventory.json']['sha256']}`
- `README.md`: `{report['artifacts']['README.md']['sha256']}`

Tooling hashes:

- builder: `{report['tooling']['builder']['sha256']}`
- verifier: `{report['tooling']['verifier']['sha256']}`
- tests: `{report['tooling']['tests']['sha256']}`

This PASS validates only deterministic inventory, hashes and contracts. A separate V7 runner and explicit execution authorisation are still required.
""".encode("utf-8")
    return {
        "runtime_inventory.json": inventory_data,
        "README.md": readme_data,
        "integrity_report.json": report_data,
        "integrity_report.md": report_md,
    }


def build() -> None:
    outputs = build_artifacts()
    require(not PACKAGE.exists(), f"Refusing to overwrite existing package: {PACKAGE}")
    PACKAGE.mkdir(parents=True, exist_ok=False)
    for name, data in outputs.items():
        path = PACKAGE / name
        with path.open("xb") as handle:
            handle.write(data)


def verify() -> dict[str, Any]:
    outputs = build_artifacts()
    require(PACKAGE.is_dir(), f"Missing runtime preflight package: {PACKAGE}")
    require({path.name for path in PACKAGE.iterdir() if path.is_file()} == set(outputs), "Runtime preflight package file-set drift")
    for name, expected in outputs.items():
        require((PACKAGE / name).read_bytes() == expected, f"Runtime preflight replay mismatch: {name}")
    return {
        "status": "PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY",
        "package": str(PACKAGE.relative_to(ROOT)),
        "files": {name: sha256_bytes(data) for name, data in sorted(outputs.items())},
        "network_calls": 0,
        "model_forward_passes": 0,
        "labels_or_results_read": False,
        "execution_authorised": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.build:
        build()
        result = {"status": "PASS_RUNTIME_PREFLIGHT_CREATED", "package": str(PACKAGE.relative_to(ROOT))}
    else:
        result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
