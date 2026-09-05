#!/usr/bin/env python3
"""Run a zero-network, no-score smoke over the frozen RQ2b chunk policies."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from audit_rq2b_token_limits import BODY_FORMAT, INSTRUCTION, PREFIX, SUFFIX
from rq2b_chunking import CHUNKER_VERSION, exact_text_chunks, tokenizer_ids
from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    version_root,
    write_json_new,
)


def load_tokenizer(snapshot: str, expected_sha256: str) -> Any:
    from transformers import AutoTokenizer

    path = Path(snapshot)
    tokenizer_json = path / "tokenizer.json"
    require(tokenizer_json.exists(), f"Cached tokenizer missing: {tokenizer_json}")
    require(sha256_file(tokenizer_json) == expected_sha256, f"Tokenizer hash drift: {tokenizer_json}")
    return AutoTokenizer.from_pretrained(path, local_files_only=True)


def run(root: Path) -> dict[str, Any]:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    verify_frozen_manifest(root)
    frozen_root = version_root(root)
    representation_manifest = read_json(frozen_root / "representations" / "manifest.json")
    i2_path = root / representation_manifest["artifacts"]["i2-original"]["path"]
    i2_rows = read_jsonl(i2_path)
    prompts = read_jsonl(frozen_root / "prompt_manifest.jsonl")
    token_audit_path = root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"
    token_audit = read_json(token_audit_path)
    qwen = token_audit["qwen"]
    skillrouter = token_audit["skillrouter"]
    qwen_tokenizer = load_tokenizer(
        qwen["local_proxy_tokenizer_snapshot"],
        qwen["local_proxy_tokenizer_sha256"],
    )
    reranker_tokenizer = load_tokenizer(
        skillrouter["tokenizer_snapshot"],
        skillrouter["tokenizer_sha256"],
    )

    qwen_chunk_rows: list[dict[str, Any]] = []
    for row in i2_rows:
        chunks = exact_text_chunks(
            qwen_tokenizer,
            row["selector_text"],
            maximum_tokens=int(qwen["proposed_chunk_tokens"]),
            overlap_tokens=int(qwen["proposed_overlap_tokens"]),
        )
        qwen_chunk_rows.append(
            {
                "skill_id": row["skill_id"],
                "source_sha256": row["source_sha256"],
                "chunk_count": len(chunks),
                "maximum_chunk_tokens": max(chunk.token_count for chunk in chunks),
                "all_chunks_exact_substrings": True,
                "lossless_character_reconstruction": True,
                "chunk_metadata": [
                    {
                        key: value
                        for key, value in chunk.to_dict().items()
                        if key != "text"
                    }
                    for chunk in chunks
                ],
            }
        )

    overhead_by_prompt = {
        row["prompt_id"]: row
        for row in token_audit["prompt_overhead_rows"]
    }
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    minimum_budget_row = min(
        token_audit["prompt_overhead_rows"],
        key=lambda row: int(row["document_window_budget"]),
    )
    minimum_prompt = prompt_by_id[minimum_budget_row["prompt_id"]]
    longest_documents = sorted(
        i2_rows,
        key=lambda row: row["selector_visible_counts"]["utf8_bytes"],
        reverse=True,
    )[:5]
    reranker_rows: list[dict[str, Any]] = []
    for row in longest_documents:
        budget = int(overhead_by_prompt[minimum_prompt["prompt_id"]]["document_window_budget"])
        chunks = exact_text_chunks(
            reranker_tokenizer,
            row["selector_text"],
            maximum_tokens=budget,
            overlap_tokens=int(skillrouter["overlap_tokens"]),
        )
        pair_counts: list[int] = []
        for chunk in chunks:
            body = BODY_FORMAT.format(
                instruction=INSTRUCTION,
                query=minimum_prompt["prompt"],
                document=chunk.text,
            )
            pair_tokens = len(tokenizer_ids(reranker_tokenizer, PREFIX + body + SUFFIX))
            require(pair_tokens <= int(skillrouter["maximum_pair_tokens"]), "Reranker pair exceeds 2,048 tokens")
            pair_counts.append(pair_tokens)
        reranker_rows.append(
            {
                "skill_id": row["skill_id"],
                "prompt_id": minimum_prompt["prompt_id"],
                "document_budget": budget,
                "window_count": len(chunks),
                "maximum_pair_tokens": max(pair_counts),
                "all_windows_exact_substrings": True,
            }
        )

    report = {
        "schema_version": "rq2b-chunking-smoke-v1",
        "version_id": VERSION_ID,
        "state": "zero_network_no_score_smoke",
        "chunker_version": CHUNKER_VERSION,
        "network_calls": 0,
        "scientific_scores": 0,
        "qwen": {
            "documents_checked": len(qwen_chunk_rows),
            "total_chunks": sum(row["chunk_count"] for row in qwen_chunk_rows),
            "multi_chunk_documents": sum(row["chunk_count"] > 1 for row in qwen_chunk_rows),
            "maximum_chunk_tokens": max(row["maximum_chunk_tokens"] for row in qwen_chunk_rows),
            "chunk_tokens_ceiling": qwen["proposed_chunk_tokens"],
            "overlap_tokens": qwen["proposed_overlap_tokens"],
            "rows": qwen_chunk_rows,
        },
        "skillrouter": {
            "documents_checked": len(reranker_rows),
            "minimum_budget_prompt": minimum_prompt["prompt_id"],
            "maximum_pair_tokens_observed": max(row["maximum_pair_tokens"] for row in reranker_rows),
            "pair_tokens_ceiling": skillrouter["maximum_pair_tokens"],
            "rows": reranker_rows,
        },
        "inputs": {
            "i2_path": relative(i2_path, root),
            "i2_sha256": sha256_file(i2_path),
            "token_audit_path": relative(token_audit_path, root),
            "token_audit_sha256": sha256_file(token_audit_path),
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    output_path = version_root(root) / "smoke" / "chunking_smoke.json"
    report = run(root)
    if args.verify_only:
        require(output_path.exists(), f"Chunking smoke report missing: {output_path}")
        require(read_json(output_path) == report, "Chunking smoke report drift")
    else:
        write_json_new(output_path, report)
    print(
        json.dumps(
            {
                "state": report["state"],
                "network_calls": report["network_calls"],
                "scientific_scores": report["scientific_scores"],
                "qwen_documents_checked": report["qwen"]["documents_checked"],
                "qwen_total_chunks": report["qwen"]["total_chunks"],
                "qwen_multi_chunk_documents": report["qwen"]["multi_chunk_documents"],
                "qwen_maximum_chunk_tokens": report["qwen"]["maximum_chunk_tokens"],
                "skillrouter_maximum_pair_tokens_observed": report["skillrouter"]["maximum_pair_tokens_observed"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
