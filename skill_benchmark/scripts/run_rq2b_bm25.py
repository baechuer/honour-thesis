#!/usr/bin/env python3
"""Run the frozen global-corpus RQ2b BM25 candidate generator."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    lexical_tokens,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    verify_i3c_retrieval_ready,
    version_root,
    write_json_new,
    write_jsonl_new,
)


RUNNER_VERSION = "rq2b-global-bm25-runner-v1"
K1 = 1.5
B = 0.75
TOP_PERSISTED = 100


class GlobalBM25:
    def __init__(self, skill_ids: list[str], documents: list[str]) -> None:
        require(len(skill_ids) == len(documents) and bool(skill_ids), "BM25 corpus is empty or misaligned")
        require(len(skill_ids) == len(set(skill_ids)), "BM25 skill IDs are not unique")
        self.skill_ids = skill_ids
        self.document_tokens = [lexical_tokens(document) for document in documents]
        self.document_lengths = [len(tokens) for tokens in self.document_tokens]
        self.average_document_length = statistics.mean(self.document_lengths) or 1.0
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for document_index, tokens in enumerate(self.document_tokens):
            for term, frequency in Counter(tokens).items():
                self.postings[term].append((document_index, frequency))
        self.document_count = len(documents)
        self.idf = {
            term: math.log(
                1.0
                + (
                    self.document_count
                    - len(posting)
                    + 0.5
                )
                / (len(posting) + 0.5)
            )
            for term, posting in self.postings.items()
        }

    def score(self, query: str) -> list[float]:
        scores = [0.0] * self.document_count
        query_counts = Counter(lexical_tokens(query))
        for term, query_frequency in query_counts.items():
            postings = self.postings.get(term)
            if not postings:
                continue
            idf = self.idf[term]
            for document_index, frequency in postings:
                document_length = self.document_lengths[document_index] or 1
                denominator = frequency + K1 * (
                    1.0 - B + B * document_length / self.average_document_length
                )
                scores[document_index] += query_frequency * idf * (
                    frequency * (K1 + 1.0)
                ) / denominator
        return scores

    def rank(self, query: str) -> list[tuple[str, float]]:
        scores = self.score(query)
        return sorted(
            zip(self.skill_ids, scores, strict=True),
            key=lambda item: (-float(item[1]), item[0]),
        )

    def persisted_index(self) -> dict[str, Any]:
        return {
            "schema_version": "rq2b-bm25-index-v1",
            "runner_version": RUNNER_VERSION,
            "tokenizer": "lowercase_[a-z0-9]+",
            "query_term_frequency": "multiplicative",
            "k1": K1,
            "b": B,
            "document_count": self.document_count,
            "average_document_length": self.average_document_length,
            "skill_ids": self.skill_ids,
            "document_lengths": self.document_lengths,
            "postings": {
                term: [[document_index, frequency] for document_index, frequency in posting]
                for term, posting in sorted(self.postings.items())
            },
            "idf": dict(sorted(self.idf.items())),
        }

    @classmethod
    def from_persisted(cls, payload: dict[str, Any]) -> "GlobalBM25":
        require(payload.get("schema_version") == "rq2b-bm25-index-v1", "Persisted BM25 schema mismatch")
        require(payload.get("runner_version") == RUNNER_VERSION, "Persisted BM25 runner mismatch")
        require(payload.get("tokenizer") == "lowercase_[a-z0-9]+", "Persisted BM25 tokenizer mismatch")
        require(float(payload.get("k1")) == K1 and float(payload.get("b")) == B, "Persisted BM25 parameter mismatch")
        instance = cls.__new__(cls)
        instance.skill_ids = [str(value) for value in payload["skill_ids"]]
        instance.document_lengths = [int(value) for value in payload["document_lengths"]]
        instance.average_document_length = float(payload["average_document_length"])
        instance.document_count = int(payload["document_count"])
        require(instance.document_count == len(instance.skill_ids) == len(instance.document_lengths), "Persisted BM25 document alignment mismatch")
        require(len(instance.skill_ids) == len(set(instance.skill_ids)), "Persisted BM25 skill IDs are not unique")
        instance.postings = {
            term: [(int(index), int(frequency)) for index, frequency in rows]
            for term, rows in payload["postings"].items()
        }
        instance.idf = {term: float(value) for term, value in payload["idf"].items()}
        require(set(instance.postings) == set(instance.idf), "Persisted BM25 term inventory mismatch")
        instance.document_tokens = []
        return instance


def annotate_unresolved_public_equivalents(
    prompts: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_by_id = {row["skill_id"]: row for row in sources}
    require(len(source_by_id) == len(sources), "Source identities are not unique")
    public_ids_by_name: dict[str, set[str]] = defaultdict(set)
    for source in sources:
        if source["source_policy"] == "public_original":
            public_ids_by_name[source["source_name"]].add(source["skill_id"])
    annotated: list[dict[str, Any]] = []
    for prompt in prompts:
        valid_names = {
            source_by_id[skill_id]["source_name"]
            for skill_id in prompt["valid_skills"]
        }
        unresolved = {
            skill_id
            for name in valid_names
            for skill_id in public_ids_by_name.get(name, set())
        }
        unresolved.difference_update(prompt["valid_skills"])
        unresolved.difference_update(prompt["closest_alternatives"])
        annotated.append(
            {
                **prompt,
                "unresolved_public_equivalents": sorted(unresolved),
            }
        )
    return annotated


def candidate_class(skill_id: str, prompt: dict[str, Any]) -> str:
    if skill_id in prompt["valid_skills"]:
        return "valid"
    if skill_id in prompt["closest_alternatives"]:
        return "annotated_near_neighbour"
    if skill_id in prompt.get("unresolved_public_equivalents", []):
        return "unresolved_public_equivalent"
    return "background_unrelated"


def rank_row(
    prompt: dict[str, Any],
    ranking: list[tuple[str, float]],
    *,
    representation: str,
    query_seconds: float,
    retriever: str = "bm25",
    runner_version: str = RUNNER_VERSION,
    aggregation: str | None = None,
) -> dict[str, Any]:
    rank_by_skill = {skill_id: index for index, (skill_id, _) in enumerate(ranking, start=1)}
    strict_rank = rank_by_skill[prompt["gold_skill"]]
    acceptable_rank = min(rank_by_skill[skill_id] for skill_id in prompt["valid_skills"])
    top = ranking[:TOP_PERSISTED]
    top_rows = [
        {
            "rank": index,
            "skill_id": skill_id,
            "score": float(score),
            "destination_class": candidate_class(skill_id, prompt),
        }
        for index, (skill_id, score) in enumerate(top, start=1)
    ]
    return {
        "schema_version": "rq2b-b1-result-row-v1",
        "version_id": VERSION_ID,
        "runner_version": runner_version,
        "retriever": retriever,
        "representation": representation,
        **({"aggregation": aggregation} if aggregation is not None else {}),
        "prompt_id": prompt["prompt_id"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "prompt_sha256": prompt["prompt_sha256"],
        "gold_skill": prompt["gold_skill"],
        "valid_skills": prompt["valid_skills"],
        "strict_gold_rank": strict_rank,
        "acceptable_gold_rank": acceptable_rank,
        "strict_hit_at_1": int(strict_rank == 1),
        "acceptable_hit_at_1": int(acceptable_rank == 1),
        "strict_recall_at_5": int(strict_rank <= 5),
        "acceptable_recall_at_5": int(acceptable_rank <= 5),
        "strict_recall_at_20": int(strict_rank <= 20),
        "acceptable_recall_at_20": int(acceptable_rank <= 20),
        "strict_recall_at_50": int(strict_rank <= 50),
        "acceptable_recall_at_50": int(acceptable_rank <= 50),
        "strict_recall_at_100": int(strict_rank <= 100),
        "acceptable_recall_at_100": int(acceptable_rank <= 100),
        "strict_reciprocal_rank": 1.0 / strict_rank,
        "acceptable_reciprocal_rank": 1.0 / acceptable_rank,
        "top_5_skill_ids": [skill_id for skill_id, _ in ranking[:5]],
        "top_20_skill_ids": [skill_id for skill_id, _ in ranking[:20]],
        "top_50_skill_ids": [skill_id for skill_id, _ in ranking[:50]],
        "top_100": top_rows,
        "query_seconds": query_seconds,
    }


def load_representation(root: Path, name: str) -> tuple[Path, list[dict[str, Any]]]:
    frozen_root = version_root(root)
    if name in {"i1-discovery", "i2-original"}:
        manifest = read_json(frozen_root / "representations" / "manifest.json")
    else:
        manifest = read_json(frozen_root / "i3c_merged" / "manifest.json")
        verify_i3c_retrieval_ready(root)
    artifact = manifest["artifacts"].get(name)
    require(artifact is not None, f"Representation is not available: {name}")
    path = root / artifact["path"]
    require(sha256_file(path) == artifact["sha256"], f"Representation hash drift: {name}")
    rows = read_jsonl(path)
    require(len(rows) == 2433, f"Representation row count mismatch: {name}")
    return path, rows


def run(root: Path, representation: str, output_dir: Path, run_id: str) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    verify_i3c_retrieval_ready(root)
    require(not output_dir.exists(), f"Refusing to overwrite BM25 run: {output_dir}")
    representation_path, representation_rows = load_representation(root, representation)
    prompts_path = version_root(root) / "prompt_manifest.jsonl"
    prompts = annotate_unresolved_public_equivalents(
        read_jsonl(prompts_path),
        read_jsonl(version_root(root) / "source_manifest.jsonl"),
    )
    started = time.perf_counter()
    index = GlobalBM25(
        [row["skill_id"] for row in representation_rows],
        [row["selector_text"] for row in representation_rows],
    )
    build_seconds = time.perf_counter() - started
    result_rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query_started = time.perf_counter()
        ranking = index.rank(prompt["prompt"])
        query_seconds = time.perf_counter() - query_started
        result_rows.append(
            rank_row(
                prompt,
                ranking,
                representation=representation,
                query_seconds=query_seconds,
            )
        )

    staging = output_dir.parent / f".{output_dir.name}.staging"
    require(not staging.exists(), f"Stale BM25 run staging directory: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    index_path = staging / "index.json"
    rows_path = staging / "rows.jsonl"
    write_json_new(index_path, index.persisted_index())
    write_jsonl_new(rows_path, result_rows)
    manifest = {
        "schema_version": "rq2b-bm25-run-manifest-v1",
        "version_id": VERSION_ID,
        "state": "complete_scientific_b1_local",
        "run_id": run_id,
        "runner_version": RUNNER_VERSION,
        "network_calls": 0,
        "retriever": "bm25",
        "representation": representation,
        "configuration": {
            "tokenizer": "lowercase_[a-z0-9]+",
            "query_term_frequency": "multiplicative",
            "k1": K1,
            "b": B,
            "corpus_documents": len(representation_rows),
            "persisted_top_k": TOP_PERSISTED,
            "tie_break": "skill_id_ascending",
        },
        "inputs": {
            "representation_path": relative(representation_path, root),
            "representation_sha256": sha256_file(representation_path),
            "prompt_manifest_path": relative(prompts_path, root),
            "prompt_manifest_sha256": sha256_file(prompts_path),
        },
        "counts": {
            "documents": len(representation_rows),
            "prompts": len(prompts),
            "rows": len(result_rows),
        },
        "timing": {
            "index_build_seconds": build_seconds,
            "query_total_seconds": sum(row["query_seconds"] for row in result_rows),
        },
        "artifacts": {
            "index": {
                "path": relative(output_dir / index_path.name, root),
                "sha256": sha256_file(index_path),
                "utf8_bytes": index_path.stat().st_size,
            },
            "rows": {
                "path": relative(output_dir / rows_path.name, root),
                "sha256": sha256_file(rows_path),
                "utf8_bytes": rows_path.stat().st_size,
                "rows": len(result_rows),
            },
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_dir)
    return manifest


def self_test() -> dict[str, Any]:
    skill_ids = ["alpha", "beta", "gamma"]
    documents = [
        "name: alpha\ndescription: parse scanned PDF using OCR",
        "name: beta\ndescription: extract native PDF text",
        "name: gamma\ndescription: render PDF pages as images",
    ]
    index = GlobalBM25(skill_ids, documents)
    direct = index.rank("OCR a scanned PDF")
    native = index.rank("extract native PDF text")
    require(direct[0][0] == "alpha", "BM25 direct self-test failed")
    require(native[0][0] == "beta", "BM25 native self-test failed")
    require(len(index.persisted_index()["postings"]) > 0, "BM25 index persistence failed")
    restored = GlobalBM25.from_persisted(index.persisted_index())
    require(restored.rank("OCR a scanned PDF") == direct, "BM25 persisted-index round-trip failed")
    annotated = annotate_unresolved_public_equivalents(
        [
            {
                "prompt_id": "p1",
                "valid_skills": ["authored"],
                "closest_alternatives": [],
            }
        ],
        [
            {
                "skill_id": "authored",
                "source_name": "Same capability",
                "source_policy": "authored_skill",
            },
            {
                "skill_id": "public-copy",
                "source_name": "Same capability",
                "source_policy": "public_original",
            },
        ],
    )
    require(
        candidate_class("public-copy", annotated[0]) == "unresolved_public_equivalent",
        "BM25 unresolved-public-equivalent self-test failed",
    )
    return {
        "state": "synthetic_no_scientific_result",
        "documents": 3,
        "direct_top1": direct[0][0],
        "native_top1": native[0][0],
        "network_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--representation", choices=("i1-discovery", "i2-original", "i3c-fielded-evidence", "i3-flat-evidence"))
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.execute, "Scientific BM25 execution requires --execute")
        require(args.representation is not None, "--representation is required")
        require(args.run_id is not None, "--run-id is required")
        require(args.output_dir is not None, "--output-dir is required")
        root = args.root.resolve()
        output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        result = run(root, args.representation, output_dir, args.run_id)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
