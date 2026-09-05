#!/usr/bin/env python3
"""Offline token-limit audit for the prefreeze RQ2b protocol.

This script loads only already-cached tokenizers and local benchmark text. It
does not call Hugging Face, DashScope, or any other network service.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "skill_benchmark" / "outputs" / "rq2b" / "preflight"
SOURCE_INVENTORY = PREFLIGHT / "source_inventory.jsonl"
PROMPT_INVENTORY = PREFLIGHT / "prompt_inventory.jsonl"
OUTPUT_JSON = PREFLIGHT / "token_limit_audit.json"
OUTPUT_MD = PREFLIGHT / "token_limit_audit.md"

QWEN_PROXY_MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
QWEN_PROXY_REVISION = "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
QWEN_PROVIDER_LIMIT = 8192
QWEN_CHUNK_TOKENS = 7500
QWEN_OVERLAP_TOKENS = 256

SKILLROUTER_MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
SKILLROUTER_REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
SKILLROUTER_MAX_TOKENS = 2048
SKILLROUTER_OVERLAP_TOKENS = 128
SKILLROUTER_SAFETY_TOKENS = 16

INSTRUCTION = (
    "Given a task description, judge whether the skill document "
    "is relevant and useful for completing the task"
)
BODY_FORMAT = "<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {document}"
PREFIX = (
    "<|im_start|>system\nJudge whether the Document meets the requirements "
    "based on the Query and the Instruct provided. Note that the answer can "
    'only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
)
SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def prompt_contract_sha256() -> str:
    payload = {
        "version": "skillrouter-reranker-prompt-v1",
        "prefix": PREFIX,
        "instruction": INSTRUCTION,
        "body_format": BODY_FORMAT,
        "suffix": SUFFIX,
    }
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return sha256_text(canonical)


def percentile(values: list[int], fraction: float) -> int:
    ordered = sorted(values)
    index = min(len(ordered) - 1, int((len(ordered) - 1) * fraction))
    return ordered[index]


def window_count(token_count: int, window: int, overlap: int) -> int:
    if token_count <= window:
        return 1
    stride = window - overlap
    return 1 + math.ceil((token_count - window) / stride)


def tokenizer_snapshot(model: str, revision: str) -> Path:
    slug = "models--" + model.replace("/", "--")
    return Path.home() / ".cache" / "huggingface" / "hub" / slug / "snapshots" / revision


def load_local_tokenizer(model: str, revision: str):
    from transformers import AutoTokenizer

    snapshot = tokenizer_snapshot(model, revision)
    tokenizer_file = snapshot / "tokenizer.json"
    if not tokenizer_file.exists():
        raise FileNotFoundError(f"missing cached tokenizer: {tokenizer_file}")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    return tokenizer, snapshot, sha256_bytes(tokenizer_file.read_bytes())


def prompt_text(row: dict[str, Any]) -> str:
    source = ROOT / row["source_path"]
    data = json.loads(source.read_text(encoding="utf-8"))
    text = str(data[row["source_row_index"]]["prompt"])
    if sha256_text(text) != row["prompt_sha256"]:
        raise ValueError(f"prompt hash mismatch: {row['prompt_id']}")
    return text


def main() -> None:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

    sources = read_jsonl(SOURCE_INVENTORY)
    prompts = read_jsonl(PROMPT_INVENTORY)
    qwen_tokenizer, qwen_snapshot, qwen_tokenizer_sha = load_local_tokenizer(
        QWEN_PROXY_MODEL, QWEN_PROXY_REVISION
    )
    reranker_tokenizer, reranker_snapshot, reranker_tokenizer_sha = load_local_tokenizer(
        SKILLROUTER_MODEL, SKILLROUTER_REVISION
    )

    source_rows: list[dict[str, Any]] = []
    for row in sources:
        text = (ROOT / row["source_path"]).read_text(encoding="utf-8")
        qwen_tokens = len(qwen_tokenizer.encode(text, add_special_tokens=False))
        reranker_tokens = len(reranker_tokenizer.encode(text, add_special_tokens=False))
        source_rows.append(
            {
                "skill_id": row["skill_id"],
                "qwen_proxy_tokens": qwen_tokens,
                "qwen_window_count": window_count(
                    qwen_tokens, QWEN_CHUNK_TOKENS, QWEN_OVERLAP_TOKENS
                ),
                "reranker_document_tokens": reranker_tokens,
            }
        )

    overhead_rows: list[dict[str, Any]] = []
    for row in prompts:
        query = prompt_text(row)
        empty_document_prompt = (
            f"<Instruct>: {INSTRUCTION}\n\n<Query>: {query}\n\n<Document>: "
        )
        overhead = len(
            reranker_tokenizer.encode(
                PREFIX + empty_document_prompt + SUFFIX,
                add_special_tokens=False,
            )
        )
        budget = SKILLROUTER_MAX_TOKENS - overhead - SKILLROUTER_SAFETY_TOKENS
        if budget <= SKILLROUTER_OVERLAP_TOKENS:
            raise ValueError(f"non-positive reranker document budget: {row['prompt_id']}")
        overhead_rows.append(
            {
                "prompt_id": row["prompt_id"],
                "prompt_sha256": row["prompt_sha256"],
                "empty_document_pair_tokens": overhead,
                "document_window_budget": budget,
            }
        )

    qwen_counts = [row["qwen_proxy_tokens"] for row in source_rows]
    reranker_counts = [row["reranker_document_tokens"] for row in source_rows]
    overheads = [row["empty_document_pair_tokens"] for row in overhead_rows]
    budgets = [row["document_window_budget"] for row in overhead_rows]
    report = {
        "schema_version": "rq2b-prefreeze-token-limit-audit-v1",
        "state": "prefreeze_audit_only_not_protocol_not_result",
        "network_calls": 0,
        "qwen": {
            "provider_model": "text-embedding-v4",
            "provider_documented_per_text_limit": QWEN_PROVIDER_LIMIT,
            "provider_documentation": "https://www.alibabacloud.com/help/en/model-studio/embedding",
            "provider_documentation_checked_date": "2026-08-02",
            "local_proxy_tokenizer_model": QWEN_PROXY_MODEL,
            "local_proxy_tokenizer_revision": QWEN_PROXY_REVISION,
            "local_proxy_tokenizer_snapshot": str(qwen_snapshot),
            "local_proxy_tokenizer_sha256": qwen_tokenizer_sha,
            "proposed_chunk_tokens": QWEN_CHUNK_TOKENS,
            "proposed_overlap_tokens": QWEN_OVERLAP_TOKENS,
            "source_p50_tokens": percentile(qwen_counts, 0.50),
            "source_p95_tokens": percentile(qwen_counts, 0.95),
            "source_p99_tokens": percentile(qwen_counts, 0.99),
            "source_max_tokens": max(qwen_counts),
            "sources_over_provider_limit": sum(n > QWEN_PROVIDER_LIMIT for n in qwen_counts),
            "sources_requiring_proposed_chunking": sum(
                n > QWEN_CHUNK_TOKENS for n in qwen_counts
            ),
            "total_document_windows": sum(row["qwen_window_count"] for row in source_rows),
        },
        "skillrouter": {
            "model": SKILLROUTER_MODEL,
            "revision": SKILLROUTER_REVISION,
            "tokenizer_snapshot": str(reranker_snapshot),
            "tokenizer_sha256": reranker_tokenizer_sha,
            "prompt_contract_sha256": prompt_contract_sha256(),
            "maximum_pair_tokens": SKILLROUTER_MAX_TOKENS,
            "overlap_tokens": SKILLROUTER_OVERLAP_TOKENS,
            "safety_tokens": SKILLROUTER_SAFETY_TOKENS,
            "source_p50_document_tokens": percentile(reranker_counts, 0.50),
            "source_p95_document_tokens": percentile(reranker_counts, 0.95),
            "source_p99_document_tokens": percentile(reranker_counts, 0.99),
            "source_max_document_tokens": max(reranker_counts),
            "minimum_document_window_budget": min(budgets),
            "maximum_document_window_budget": max(budgets),
            "maximum_empty_document_pair_tokens": max(overheads),
            "minimum_empty_document_pair_tokens": min(overheads),
        },
        "source_rows": source_rows,
        "prompt_overhead_rows": overhead_rows,
    }
    OUTPUT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# RQ2b Prefreeze Token-Limit Audit",
        "",
        "This is a zero-network audit, not a frozen protocol and not a scientific result.",
        "",
        "## Qwen",
        "",
        f"- Official per-text limit: {QWEN_PROVIDER_LIMIT} tokens",
        f"- Local proxy-tokenizer maximum: {max(qwen_counts)} tokens",
        f"- Sources over the official limit: {sum(n > QWEN_PROVIDER_LIMIT for n in qwen_counts)}",
        f"- Proposed 7,500-token chunking affects: {sum(n > QWEN_CHUNK_TOKENS for n in qwen_counts)} sources",
        f"- Proposed total document windows: {sum(row['qwen_window_count'] for row in source_rows)}",
        "",
        "## SkillRouter",
        "",
        f"- Frozen total pair limit: {SKILLROUTER_MAX_TOKENS} tokens",
        f"- Query-specific document budget range: {min(budgets)}-{max(budgets)} tokens",
        f"- Maximum source document length: {max(reranker_counts)} tokens",
        f"- Window overlap: {SKILLROUTER_OVERLAP_TOKENS} tokens",
        "",
    ]
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "network_calls": 0,
                "qwen_sources_chunked": report["qwen"]["sources_requiring_proposed_chunking"],
                "qwen_source_max_tokens": report["qwen"]["source_max_tokens"],
                "skillrouter_min_document_budget": report["skillrouter"]["minimum_document_window_budget"],
                "skillrouter_source_max_tokens": report["skillrouter"]["source_max_document_tokens"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
