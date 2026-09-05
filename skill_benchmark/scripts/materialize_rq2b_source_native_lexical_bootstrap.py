#!/usr/bin/env python3
"""Materialise a native-description lexical-only cluster-discovery batch.

Uses exact source-native descriptions from the frozen corpus.  Output is a
source-reading queue only: no source card, full-source judgement, cluster,
prompt, label, acceptable set, selector or metric is generated here.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS_DIR = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04"
CORPUS = CORPUS_DIR / "source_native_description_corpus.jsonl"
OUTPUT_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04"

TOP_NEIGHBOURS = 12
BATCH_FAMILIES = 25
K1 = 1.2
B = 0.75
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}")
STOPWORDS = {
    "about", "after", "also", "and", "are", "as", "at", "be", "by", "can", "do", "for", "from", "how", "if", "in", "into", "is", "it", "its", "of", "on", "or", "that", "the", "their", "then", "this", "to", "use", "used", "using", "when", "with", "you", "your",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS]


def rank_neighbours(
    index: int,
    term_counts: list[Counter[str]],
    document_lengths: list[int],
    postings: dict[str, list[tuple[int, int]]],
    idf: dict[str, float],
    average_length: float,
    source_hashes: list[str],
    description_hashes: list[str],
) -> list[tuple[int, float]]:
    scores: defaultdict[int, float] = defaultdict(float)
    for term in term_counts[index]:
        for candidate, frequency in postings[term]:
            if candidate == index or description_hashes[candidate] == description_hashes[index]:
                continue
            denominator = frequency + K1 * (1.0 - B + B * document_lengths[candidate] / average_length)
            scores[candidate] += idf[term] * frequency * (K1 + 1.0) / denominator
    ranked = [(candidate, score) for candidate, score in scores.items() if score > 0.0]
    return sorted(ranked, key=lambda item: (-item[1], source_hashes[item[0]]))[:TOP_NEIGHBOURS]


def main() -> int:
    if not PROTOCOL.is_file() or not CORPUS.is_file():
        raise SystemExit("Missing protocol or native-description corpus")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")
    source_rows_all = [row for row in read_jsonl(CORPUS) if row.get("index_eligibility") is True]
    if len(source_rows_all) != 23_431:
        raise SystemExit("Expected the 23,431-source indexable native-description corpus")
    lexical_excluded = [row for row in source_rows_all if not tokens(str(row["native_description"]))]
    source_rows = [row for row in source_rows_all if tokens(str(row["native_description"]))]
    if not source_rows:
        raise SystemExit("No native descriptions have usable lexical terms")
    source_rows.sort(key=lambda row: str(row["canonical_source_sha256"]))
    source_hashes = [str(row["canonical_source_sha256"]) for row in source_rows]
    description_hashes = [str(row["native_description_sha256"]) for row in source_rows]
    term_counts = [Counter(tokens(str(row["native_description"]))) for row in source_rows]
    document_lengths = [sum(counts.values()) for counts in term_counts]
    average_length = sum(document_lengths) / len(document_lengths)
    postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for index, counts in enumerate(term_counts):
        for term, frequency in counts.items():
            postings[term].append((index, frequency))
    document_count = len(source_rows)
    idf = {term: math.log(1.0 + (document_count - len(rows) + 0.5) / (len(rows) + 0.5)) for term, rows in postings.items()}

    ranks: dict[int, list[tuple[int, float]]] = {}
    ranking_rows: list[dict[str, Any]] = []
    for index in range(document_count):
        ranked = rank_neighbours(index, term_counts, document_lengths, postings, idf, average_length, source_hashes, description_hashes)
        ranks[index] = ranked
        for rank, (candidate, score) in enumerate(ranked, start=1):
            ranking_rows.append({
                "record_type": "native_description_lexical_neighbour",
                "seed_source_sha256": source_hashes[index],
                "neighbour_source_sha256": source_hashes[candidate],
                "rank": rank,
                "bm25_score": score,
                "discovery_route": "LEXICAL_ONLY_BOOTSTRAP_EXACT_NATIVE_DESCRIPTION",
                "claim_boundary": "Source-reading prioritisation only; not semantic ground truth or a cluster result.",
            })
    rank_lookup = {(index, candidate): rank for index, ranked in ranks.items() for rank, (candidate, _score) in enumerate(ranked, start=1)}
    mutual: dict[int, set[int]] = defaultdict(set)
    for (left, right), _rank in rank_lookup.items():
        if (right, left) in rank_lookup:
            mutual[left].add(right)

    family_rows: list[dict[str, Any]] = []
    observed: set[tuple[int, int, int]] = set()
    for left in range(document_count):
        for middle, right in combinations(sorted(mutual[left]), 2):
            members = tuple(sorted((left, middle, right)))
            if members in observed:
                continue
            observed.add(members)
            if middle not in mutual[right]:
                continue
            if len({description_hashes[item] for item in members}) != 3:
                continue
            directional_ranks = [rank_lookup[(first, second)] for first in members for second in members if first != second]
            if len(directional_ranks) != 6:
                raise SystemExit("Mutual triangle lacks all directional ranks")
            score = sum(1.0 / (60.0 + rank) for rank in directional_ranks)
            member_hashes = [source_hashes[item] for item in members]
            family_id = "SN-LEX-" + hashlib.sha256("|".join(member_hashes).encode("utf-8")).hexdigest()[:16]
            family_rows.append({
                "record_type": "source_native_confusable_family_hypothesis",
                "family_id": family_id,
                "member_source_sha256": member_hashes,
                "member_source_paths": [source_rows[item]["source_paths"] for item in members],
                "member_native_description_sha256": [description_hashes[item] for item in members],
                "mutual_directional_ranks": directional_ranks,
                "reciprocal_link_count": 3,
                "rank_fusion_score": score,
                "discovery_route": "LEXICAL_ONLY_BOOTSTRAP_EXACT_NATIVE_DESCRIPTION",
                "review_state": "UNREVIEWED_FULL_SOURCE",
                "claim_boundary": "Hypothesis only; complete original sources must establish envelope, independence and contrast.",
            })
    family_rows.sort(key=lambda row: (-row["reciprocal_link_count"], -row["rank_fusion_score"], row["member_source_sha256"]))
    batch_rows: list[dict[str, Any]] = []
    used_members: set[str] = set()
    for row in family_rows:
        members = set(row["member_source_sha256"])
        if members & used_members:
            continue
        batch_rows.append({**row, "batch_id": "SN-LEX-B001", "batch_rank": len(batch_rows) + 1})
        used_members.update(members)
        if len(batch_rows) == BATCH_FAMILIES:
            break

    OUTPUT_DIR.mkdir(parents=True)
    ranking_path = OUTPUT_DIR / "native_description_lexical_top12.jsonl"
    hypotheses_path = OUTPUT_DIR / "all_mutual_triangle_hypotheses.jsonl"
    batch_path = OUTPUT_DIR / "batch_001_full_source_review_queue_internal.jsonl"
    write_jsonl(ranking_path, ranking_rows)
    write_jsonl(hypotheses_path, family_rows)
    write_jsonl(batch_path, batch_rows)
    summary = {
        "status": "PASS_SOURCE_NATIVE_LEXICAL_ONLY_BOOTSTRAP_UNREVIEWED_FAMILY_HYPOTHESES",
        "protocol": relative(PROTOCOL),
        "bound_inputs": {relative(CORPUS): sha256_file(CORPUS)},
        "parameters": {"top_neighbours": TOP_NEIGHBOURS, "batch_families": BATCH_FAMILIES, "bm25_k1": K1, "bm25_b": B, "stopwords": sorted(STOPWORDS)},
        "counts": {"literal_replay_sources": len(source_rows_all), "lexical_indexable_sources": len(source_rows), "lexical_excluded_zero_term_sources": len(lexical_excluded), "directed_top12_edges": len(ranking_rows), "mutual_triangles": len(family_rows), "batch_001_families": len(batch_rows), "batch_001_sources": len(used_members)},
        "outputs": {"native_description_lexical_top12.jsonl": sha256_file(ranking_path), "all_mutual_triangle_hypotheses.jsonl": sha256_file(hypotheses_path), "batch_001_full_source_review_queue_internal.jsonl": sha256_file(batch_path)},
        "dense_status": "NOT_EXECUTED_NO_PROVIDER_CREDENTIAL_IN_PROCESS_ENVIRONMENT_NO_PROVIDER_CONTACT",
        "claim_boundary": "Lexical-only source-reading queue; no full-source approval, cluster, prompt, label, admission, selector or metric has occurred.",
    }
    write_json(OUTPUT_DIR / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
