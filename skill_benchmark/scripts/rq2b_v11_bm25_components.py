#!/usr/bin/env python3
"""Local strict-only BM25 primitives for a future sealed RQ2b v1.1 runner.

The module intentionally exposes no scientific-corpus CLI.  It provides the
deterministic lexical index and strict B1 row serializer that a later sealed
runner may call after the I3C and stage-authorisation gates pass.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import lexical_tokens, repo_root, require, write_json_new
from rq2b_v11_execution_contract import B1_SCHEMA, PERSISTED_K, validate_b1_row


RUNNER_VERSION = "rq2b-v11-bm25-components-v1"
K1 = 1.5
B = 0.75


class GlobalBM25:
    """Deterministic global BM25 with a stable skill-ID tie-break."""

    def __init__(self, skill_ids: list[str], documents: list[str]) -> None:
        require(len(skill_ids) == len(documents) and bool(skill_ids), "BM25 corpus is empty or misaligned")
        require(len(skill_ids) == len(set(skill_ids)), "BM25 skill IDs are not unique")
        self.skill_ids = skill_ids
        self.document_tokens = [lexical_tokens(document) for document in documents]
        self.document_lengths = [len(tokens) for tokens in self.document_tokens]
        self.average_document_length = statistics.mean(self.document_lengths) or 1.0
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for index, tokens in enumerate(self.document_tokens):
            for term, frequency in Counter(tokens).items():
                self.postings[term].append((index, frequency))
        self.document_count = len(documents)
        self.idf = {
            term: math.log(1.0 + (self.document_count - len(posting) + 0.5) / (len(posting) + 0.5))
            for term, posting in self.postings.items()
        }

    def rank(self, query: str) -> list[tuple[str, float]]:
        scores = [0.0] * self.document_count
        for term, query_frequency in Counter(lexical_tokens(query)).items():
            for index, frequency in self.postings.get(term, []):
                length = self.document_lengths[index] or 1
                denominator = frequency + K1 * (1.0 - B + B * length / self.average_document_length)
                scores[index] += query_frequency * self.idf[term] * frequency * (K1 + 1.0) / denominator
        return sorted(zip(self.skill_ids, scores, strict=True), key=lambda row: (-float(row[1]), row[0]))


def build_b1_row(
    *,
    prompt: dict[str, Any],
    ranking: list[tuple[str, float]],
    representation: str,
    query_seconds: float,
    retriever: str = "bm25",
    runner_version: str = RUNNER_VERSION,
) -> dict[str, Any]:
    require(len(ranking) >= PERSISTED_K, "B1 ranking does not contain the persisted top-100")
    skill_ids = [skill_id for skill_id, _ in ranking]
    require(len(skill_ids) == len(set(skill_ids)), "B1 ranking has duplicate skill IDs")
    require(prompt["gold_skill"] in skill_ids, "B1 strict gold is not in the complete ranking")
    strict_rank = skill_ids.index(prompt["gold_skill"]) + 1
    top = ranking[:PERSISTED_K]
    row = {
        "schema_version": B1_SCHEMA,
        "version_id": "rq2b-full-library-v1.1-2026-08-15",
        "runner_version": runner_version,
        "retriever": retriever,
        "representation": representation,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": strict_rank,
        "strict_hit_at_1": int(strict_rank == 1),
        "strict_recall_at_5": int(strict_rank <= 5),
        "strict_recall_at_20": int(strict_rank <= 20),
        "strict_recall_at_50": int(strict_rank <= 50),
        "strict_recall_at_100": int(strict_rank <= 100),
        "strict_mrr_at_10": 0.0 if strict_rank > 10 else 1.0 / strict_rank,
        "top_5_skill_ids": skill_ids[:5],
        "top_20_skill_ids": skill_ids[:20],
        "top_50_skill_ids": skill_ids[:50],
        "top_100": [
            {"rank": index, "skill_id": skill_id, "score": float(score)}
            for index, (skill_id, score) in enumerate(top, start=1)
        ],
        "query_seconds": float(query_seconds),
    }
    validate_b1_row(row, prompt, f"{retriever}/{representation}/{prompt['prompt_id']}")
    return row


def self_test() -> dict[str, Any]:
    ids = ["alpha", "beta", "gamma"]
    index = GlobalBM25(
        ids,
        [
            "parse scanned PDF pages with OCR",
            "extract native PDF text from digital pages",
            "render PDF pages into images",
        ],
    )
    ocr = index.rank("OCR a scanned PDF")
    native = index.rank("extract native PDF text")
    require(ocr[0][0] == "alpha", "BM25 OCR synthetic ranking mismatch")
    require(native[0][0] == "beta", "BM25 native synthetic ranking mismatch")

    prompt = {
        "prompt_id": "synthetic-prompt",
        "prompt_sha256": "synthetic-sha",
        "stratum": "controlled",
        "group": "synthetic-group",
        "gold_skill": "gold",
    }
    ranking = [("alternate", 2.0), ("gold", 1.0)] + [
        (f"background-{index:03d}", 0.0) for index in range(98)
    ]
    row = build_b1_row(
        prompt=prompt,
        ranking=ranking,
        representation="i1-discovery",
        query_seconds=0.0,
    )
    require(row["strict_gold_rank"] == 2 and row["strict_mrr_at_10"] == 0.5, "B1 strict metric synthesis failed")
    require("valid_skills" not in row and all("acceptable" not in key for key in row), "B1 serializer emitted legacy fields")
    return {
        "state": "pass_synthetic_zero_network_no_scientific_result",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "ocr_top1": ocr[0][0],
        "native_top1": native[0][0],
        "strict_gold_rank": row["strict_gold_rank"],
        "legacy_acceptable_fields_emitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    require(args.self_test, "This component module only exposes --self-test")
    report = self_test()
    if args.record is not None:
        output = args.record if args.record.is_absolute() else repo_root() / args.record
        write_json_new(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
