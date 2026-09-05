#!/usr/bin/env python3
"""Run the separately approved local-only V3 B1L strict BM25 matrix.

The default modes are a synthetic self-test and a no-ranking preflight.  The
``--execute`` mode is fail-closed: it requires a later exact user approval
receipt bound to the B1L packet created by the preparation script.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from prepare_rq2b_i3c_v3_b1l_preflight import (
    EXECUTION_PACKET_NAME,
    PREFLIGHT_CHECKPOINT_NAME,
    PREFLIGHT_REPORT_NAME,
    PREFLIGHT_ROOT,
    PREFLIGHT_VERSION,
    REPRESENTATIONS,
    STRICT_PROMPT_SCHEMA,
    validate_representation_rows,
    validate_strict_prompts,
)
from rq2b_common import (
    lexical_tokens,
    read_json,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    write_json_new,
    write_jsonl_new,
)
from rq2b_v11_execution_contract import B1_SCHEMA, validate_b1_row
from verify_rq2b_i3c_v3_automatic_freeze import SOURCE_MANIFEST, VERSION_ID
from verify_rq2b_i3c_v3_automatic_freeze import verify_full as verify_v3_automatic_integrity


RUNNER_VERSION = "rq2b-i3c-v3-b1l-strict-bm25-runner-v1"
K1 = 1.5
B = 0.75
PERSISTED_K = 100
EXECUTION_RECEIPT = f"{PREFLIGHT_ROOT}/b1l_execution_approval_receipt.json"
RUN_ROOT = f"{PREFLIGHT_ROOT}/b1l_local_bm25_run"


class GlobalBM25:
    def __init__(self, skill_ids: list[str], documents: list[str]) -> None:
        require(len(skill_ids) == len(documents) == 2433, "BM25 candidate size must be 2,433")
        require(len(skill_ids) == len(set(skill_ids)), "BM25 skill IDs must be unique")
        self.skill_ids = skill_ids
        self.document_tokens = [lexical_tokens(document) for document in documents]
        self.document_lengths = [len(tokens) for tokens in self.document_tokens]
        self.average_document_length = sum(self.document_lengths) / len(self.document_lengths)
        require(self.average_document_length > 0.0, "BM25 candidate documents are all empty")
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for document_index, tokens in enumerate(self.document_tokens):
            for token, frequency in Counter(tokens).items():
                self.postings[token].append((document_index, frequency))
        self.document_count = len(documents)
        self.idf = {
            token: math.log(1.0 + (self.document_count - len(posting) + 0.5) / (len(posting) + 0.5))
            for token, posting in self.postings.items()
        }

    def rank(self, query: str) -> list[tuple[str, float]]:
        scores = [0.0] * self.document_count
        for token, query_frequency in Counter(lexical_tokens(query)).items():
            posting = self.postings.get(token)
            if posting is None:
                continue
            idf = self.idf[token]
            for document_index, frequency in posting:
                document_length = self.document_lengths[document_index] or 1
                denominator = frequency + K1 * (1.0 - B + B * document_length / self.average_document_length)
                scores[document_index] += query_frequency * idf * (frequency * (K1 + 1.0)) / denominator
        return sorted(zip(self.skill_ids, scores, strict=True), key=lambda item: (-float(item[1]), item[0]))

    def persisted_index(self) -> dict[str, Any]:
        return {
            "schema_version": "rq2b-i3c-v3-bm25-index-v1",
            "runner_version": RUNNER_VERSION,
            "tokenizer": "lowercase_[a-z0-9]+",
            "k1": K1,
            "b": B,
            "document_count": self.document_count,
            "average_document_length": self.average_document_length,
            "skill_ids": self.skill_ids,
            "document_lengths": self.document_lengths,
            "postings": {token: [[index, frequency] for index, frequency in posting] for token, posting in sorted(self.postings.items())},
            "idf": dict(sorted(self.idf.items())),
        }

    @classmethod
    def from_persisted(cls, payload: dict[str, Any]) -> "GlobalBM25":
        require(payload.get("schema_version") == "rq2b-i3c-v3-bm25-index-v1", "persisted BM25 schema mismatch")
        require(payload.get("runner_version") == RUNNER_VERSION, "persisted BM25 runner mismatch")
        require(payload.get("tokenizer") == "lowercase_[a-z0-9]+", "persisted BM25 tokenizer mismatch")
        require(float(payload.get("k1")) == K1 and float(payload.get("b")) == B, "persisted BM25 hyperparameter mismatch")
        instance = cls.__new__(cls)
        instance.skill_ids = [str(value) for value in payload["skill_ids"]]
        instance.document_lengths = [int(value) for value in payload["document_lengths"]]
        instance.average_document_length = float(payload["average_document_length"])
        instance.document_count = int(payload["document_count"])
        require(instance.document_count == len(instance.skill_ids) == len(instance.document_lengths) == 2433, "persisted BM25 identity mismatch")
        require(len(instance.skill_ids) == len(set(instance.skill_ids)), "persisted BM25 duplicate IDs")
        instance.postings = {token: [(int(index), int(frequency)) for index, frequency in posting] for token, posting in payload["postings"].items()}
        instance.idf = {token: float(value) for token, value in payload["idf"].items()}
        require(set(instance.postings) == set(instance.idf), "persisted BM25 token inventory mismatch")
        instance.document_tokens = []
        return instance


def b1_row(prompt: dict[str, Any], ranking: list[tuple[str, float]], *, representation: str, query_seconds: float, index_seconds: float, selector_tokens: int) -> dict[str, Any]:
    rank_by_id = {skill_id: index for index, (skill_id, _) in enumerate(ranking, start=1)}
    strict_rank = rank_by_id[prompt["gold_skill"]]
    top100 = ranking[:PERSISTED_K]
    return {
        "schema_version": B1_SCHEMA,
        "version_id": "rq2b-full-library-v1.1-2026-08-15",
        "runner_version": RUNNER_VERSION,
        "retriever": "bm25",
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
        "top_5_skill_ids": [skill_id for skill_id, _ in ranking[:5]],
        "top_20_skill_ids": [skill_id for skill_id, _ in ranking[:20]],
        "top_50_skill_ids": [skill_id for skill_id, _ in ranking[:50]],
        "top_100": [{"rank": index, "skill_id": skill_id, "score": float(score)} for index, (skill_id, score) in enumerate(top100, start=1)],
        "query_seconds": query_seconds,
        "selector_visible_tokens": selector_tokens,
        "one_time_document_embedding_or_index_seconds": index_seconds,
    }


def verify_preflight(root: Path) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    automatic_report = verify_v3_automatic_integrity(root)
    require(automatic_report.get("state") == "automatic_integrity_verification_passed", "V3 automatic integrity replay failed")
    preflight_root = root / PREFLIGHT_ROOT
    checkpoint = read_json(preflight_root / PREFLIGHT_CHECKPOINT_NAME)
    require(checkpoint.get("state") == "b1l_preflight_frozen_execution_approval_required", "B1L preflight is not frozen")
    report_path = root / checkpoint["report"]["path"]
    require(sha256_file(report_path) == checkpoint["report"]["sha256"], "B1L preflight report hash drift")
    report = read_json(report_path)
    require(report.get("state") == "b1l_preflight_verified_no_scoring", "B1L preflight state mismatch")
    require(report.get("candidate_library_skills") == 2433 and report.get("b1l_expected_result_rows") == 1524, "B1L preflight population mismatch")
    frozen_report = root / report["automatic_freeze"]["report"]["path"]
    require(sha256_file(frozen_report) == report["automatic_freeze"]["report"]["sha256"], "automatic freeze report drift")
    packet_path = root / checkpoint["execution_approval_packet"]["path"]
    require(sha256_file(packet_path) == checkpoint["execution_approval_packet"]["sha256"], "B1L execution packet hash drift")
    packet = read_json(packet_path)
    require(packet.get("state") == "awaiting_explicit_user_approval_b1l_local_bm25_only", "B1L execution packet state mismatch")
    require(packet.get("preflight_report") == checkpoint["report"], "B1L packet/report binding mismatch")
    expected_script_path = relative(Path(__file__).resolve(), root)
    require(packet.get("execution_script", {}).get("path") == expected_script_path, "B1L execution script path mismatch")
    require(packet.get("execution_script", {}).get("sha256") == sha256_file(Path(__file__).resolve()), "B1L execution script hash drift")
    prompt_artifact = report["strict_scored_prompts"]
    prompt_path = root / prompt_artifact["path"]
    require(sha256_file(prompt_path) == prompt_artifact["sha256"], "B1L strict prompt artifact hash drift")
    prompts = []
    for raw in prompt_path.read_text(encoding="utf-8").splitlines():
        require(bool(raw), "blank strict prompt JSONL line")
        parsed = json.loads(raw)
        require(isinstance(parsed, dict), "strict prompt row is not an object")
        prompts.append(parsed)
    sources = []
    for raw in (root / SOURCE_MANIFEST).read_text(encoding="utf-8").splitlines():
        require(bool(raw), "blank source JSONL line")
        sources.append(json.loads(raw))
    candidate_ids = {row["skill_id"] for row in sources}
    validate_strict_prompts(prompts, candidate_ids)
    representations: dict[str, list[dict[str, Any]]] = {}
    for representation in REPRESENTATIONS:
        artifact = report["representations"][representation]
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], f"B1L representation hash drift: {representation}")
        rows = []
        for raw in path.read_text(encoding="utf-8").splitlines():
            require(bool(raw), f"blank {representation} JSONL line")
            rows.append(json.loads(raw))
        validate_representation_rows(
            root=root,
            sources=sources,
            rows=rows,
            representation=representation,
            require_exact_source=representation == "i2-original",
            require_v3_evidence_alignment=representation in {"i3c-fielded-evidence", "i3-flat-evidence"},
        )
        representations[representation] = rows
    return report, representations, prompts


def verify_execution_receipt(root: Path) -> dict[str, Any]:
    packet_path = root / PREFLIGHT_ROOT / EXECUTION_PACKET_NAME
    receipt_path = root / EXECUTION_RECEIPT
    require(receipt_path.is_file(), "B1L execution is not approved: exact receipt is absent")
    receipt = read_json(receipt_path)
    require(receipt.get("state") == "explicitly_approved_for_v3_b1l_local_bm25_once", "B1L execution receipt state mismatch")
    require(receipt.get("approved_packet", {}).get("path") == relative(packet_path, root), "B1L receipt packet path mismatch")
    require(receipt.get("approved_packet", {}).get("sha256") == sha256_file(packet_path), "B1L receipt packet hash mismatch")
    return receipt


def execute(root: Path) -> dict[str, Any]:
    verify_execution_receipt(root)
    report, representations, prompts = verify_preflight(root)
    output_root = root / RUN_ROOT
    staging_root = output_root.with_name(".b1l_local_bm25_run.staging")
    require(not output_root.exists() and not staging_root.exists(), "refusing to overwrite B1L BM25 run")
    staging_root.mkdir(parents=True, exist_ok=False)
    all_rows: list[dict[str, Any]] = []
    index_artifacts: dict[str, dict[str, Any]] = {}
    warm_verification: dict[str, dict[str, Any]] = {}
    for representation, documents in representations.items():
        build_started = time.perf_counter()
        index = GlobalBM25([row["skill_id"] for row in documents], [row["selector_text"] for row in documents])
        index_seconds = time.perf_counter() - build_started
        selector_tokens = sum(int(row["selector_visible_counts"]["lexical_tokens"]) for row in documents)
        index_path = staging_root / f"{representation}.bm25-index.json"
        write_json_new(index_path, index.persisted_index())
        index_artifacts[representation] = {"path": relative(output_root / index_path.name, root), "sha256": sha256_file(index_path), "build_seconds": index_seconds, "selector_visible_tokens": selector_tokens}
        condition_rows: list[dict[str, Any]] = []
        for prompt in prompts:
            query_started = time.perf_counter()
            ranking = index.rank(prompt["prompt"])
            row = b1_row(prompt, ranking, representation=representation, query_seconds=time.perf_counter() - query_started, index_seconds=index_seconds, selector_tokens=selector_tokens)
            validate_b1_row(row, prompt, f"{representation}:{prompt['prompt_id']}")
            all_rows.append(row)
            condition_rows.append(row)
        warm_index = GlobalBM25.from_persisted(read_json(index_path))
        warm_started = time.perf_counter()
        for prompt, row in zip(prompts, condition_rows, strict=True):
            warm_ranking = warm_index.rank(prompt["prompt"])
            require(
                [skill_id for skill_id, _ in warm_ranking[:PERSISTED_K]]
                == [entry["skill_id"] for entry in row["top_100"]],
                f"warm BM25 Top-100 mismatch: {representation}:{prompt['prompt_id']}",
            )
        warm_verification[representation] = {
            "persisted_index_sha256": sha256_file(index_path),
            "verified_prompts": len(prompts),
            "warm_query_seconds": time.perf_counter() - warm_started,
        }
    require(len(all_rows) == report["b1l_expected_result_rows"] == 1524, "B1L result matrix count mismatch")
    results_path = staging_root / "b1l_strict_results.jsonl"
    write_jsonl_new(results_path, all_rows)
    summary_rows: list[dict[str, Any]] = []
    for representation in REPRESENTATIONS:
        for stratum in ("controlled", "public_gold"):
            rows = [row for row in all_rows if row["representation"] == representation and row["stratum"] == stratum]
            require(bool(rows), f"missing B1L condition: {representation}/{stratum}")
            summary_rows.append({
                "retriever": "bm25",
                "representation": representation,
                "stratum": stratum,
                "prompts": len(rows),
                "strict_hit_at_1": sum(row["strict_hit_at_1"] for row in rows) / len(rows),
                "strict_recall_at_20": sum(row["strict_recall_at_20"] for row in rows) / len(rows),
                "strict_mrr_at_10": sum(float(row["strict_mrr_at_10"]) for row in rows) / len(rows),
            })
    summary = {
        "schema_version": "rq2b-i3c-v3-b1l-bm25-run-summary-v1",
        "version_id": VERSION_ID,
        "state": "local_b1l_bm25_completed_pending_warm_verification_and_user_result_review",
        "b1l_preflight": {
            "path": relative(root / PREFLIGHT_ROOT / PREFLIGHT_REPORT_NAME, root),
            "sha256": sha256_file(root / PREFLIGHT_ROOT / PREFLIGHT_REPORT_NAME),
            "strict_endpoint_contract": report["strict_endpoint_contract"],
        },
        "results": {"path": relative(output_root / results_path.name, root), "sha256": sha256_file(results_path), "rows": len(all_rows)},
        "indexes": index_artifacts,
        "warm_verification": warm_verification,
        "strict_summary": summary_rows,
        "network_calls": 0,
        "external_api_calls": 0,
        "thesis_result_writing": False,
    }
    write_json_new(staging_root / "b1l_bm25_run_summary.json", summary)
    staging_root.rename(output_root)
    return summary


def self_test() -> dict[str, Any]:
    skill_ids = [f"skill-{index:04d}" for index in range(2433)]
    documents = ["alpha alpha" if skill_id == "skill-0000" else "beta" for skill_id in skill_ids]
    index = GlobalBM25(skill_ids, documents)
    prompt = {
        "schema_version": STRICT_PROMPT_SCHEMA,
        "prompt_id": "synthetic",
        "prompt": "alpha",
        "prompt_sha256": sha256_text("alpha"),
        "stratum": "controlled",
        "group": "synthetic",
        "gold_skill": "skill-0000",
    }
    row = b1_row(prompt, index.rank(prompt["prompt"]), representation="i1-discovery", query_seconds=0.0, index_seconds=0.0, selector_tokens=2434)
    validate_b1_row(row, prompt, "synthetic")
    tampered = {**row, "top_5_skill_ids": list(reversed(row["top_5_skill_ids"]))}
    try:
        validate_b1_row(tampered, prompt, "tampered")
    except ValueError:
        rejected = "ranking_prefix_tamper"
    else:
        raise AssertionError("B1L self-test did not reject prefix tamper")
    return {"schema_version": "rq2b-i3c-v3-b1l-bm25-self-test-v1", "state": "self_test_passed", "rejected_case": rejected, "network_calls": 0, "scientific_retrieval_or_reranking": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    require(sum((args.self_test, args.preflight, args.execute)) == 1, "choose exactly one mode")
    root = args.root.resolve()
    if args.self_test:
        result = self_test()
    elif args.preflight:
        report, representations, prompts = verify_preflight(root)
        result = {"state": "preflight_passed_no_scoring", "representations": sorted(representations), "strict_prompts": len(prompts), "expected_result_rows": report["b1l_expected_result_rows"], "network_calls": 0}
    else:
        result = execute(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
