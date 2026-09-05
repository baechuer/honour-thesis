#!/usr/bin/env python3
"""Materialise the outcome-blind 23,450-source RQ2 K-calibration packets.

The script is deliberately a queue/packet materialiser.  It reads no adequacy
outcome and writes no cluster, label, representation, selector, or metric.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK_ROOT = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK_ROOT / "rq2b_naturalistic_confusability"
BASE_PROTOCOL = NC_ROOT / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_PROTOCOL_2026-08-31.json"
CALIBRATION_PROTOCOL = NC_ROOT / "review/USER_AUTHORIZED_BACKGROUND_CORPUS_K_CALIBRATION_PROTOCOL_2026-09-03.md"
EXTENDED_DIR = NC_ROOT / "manifests/background_corpus_extended_union_23450_2026-09-03"
PROFILES = EXTENDED_DIR / "navigation_profiles.jsonl"
POPULATION = EXTENDED_DIR / "candidate_population.jsonl"
PARENT_DELTA = EXTENDED_DIR / "parent_non_gold_delta_source_hashes.jsonl"
PARENT_PROMPTS = BENCHMARK_ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
NC_PROMPTS = NC_ROOT / "manifests/curation_closed_checkpoint_2026-08-31/curation_eligible_prompts.jsonl"
OUTPUT_DIR = NC_ROOT / "manifests/background_corpus_k_calibration_2026-09-03"
PARTITION_OUT = OUTPUT_DIR / "calibration_prompt_partition.jsonl"
QUEUE_OUT = OUTPUT_DIR / "calibration_queues_internal.jsonl"
PAIR_REGISTER_OUT = OUTPUT_DIR / "calibration_pair_register_internal.jsonl"
REVIEWER_A_OUT = OUTPUT_DIR / "reviewer_a_packet.jsonl"
REVIEWER_B_OUT = OUTPUT_DIR / "reviewer_b_packet.jsonl"
TERM_STATS_OUT = OUTPUT_DIR / "lane_term_statistics.json"
SUMMARY_OUT = OUTPUT_DIR / "summary.json"

EXPECTED_EXTENDED = 23450
EXPECTED_PARENT_DELTA = 21019
EXPECTED_PARENT_PROMPTS = 381
EXPECTED_NC_PROMPTS = 125
CALIBRATION_PARENT_PER_STRATUM = 18
CALIBRATION_NC_CLUSTERS = 36
K_VALUES = (8, 12, 16)
K_MAX = 16
REVIEWER_PAIR_BUDGET = 4500
MICRO_IDF = 1_000_000
RESIDUAL_ROLE_ORDER = [
    "UNADJUDICATED_PROVENANCE_BOUND_BACKGROUND_CANDIDATE",
    "RQ2B_NC_REVIEWED_SOURCE_CANDIDATE",
    "RQ2B_NC_RQ1_REVIEWED_NEW_SOURCE_CANDIDATE",
    "RQ1_NEW_PUBLIC_SOURCE_CANDIDATE",
    "PARENT_V3_CANONICAL_SOURCE",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def hash_key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_terms(text: str, token_re: re.Pattern[str], stopwords: set[str]) -> tuple[set[str], set[str]]:
    normalised = unicodedata.normalize("NFKC", text).lower()
    tokens = [
        token for token in token_re.findall(normalised)
        if token not in stopwords and len(token) > 1
    ]
    return set(tokens), {f"{left}::{right}" for left, right in zip(tokens, tokens[1:])}


def integer_idf(document_count: int, document_frequency: int) -> int:
    return round((math.log((document_count + 1) / (document_frequency + 1)) + 1) * MICRO_IDF)


def ranked_channel(scores: dict[str, tuple[int, ...]]) -> list[tuple[tuple[int, ...], str]]:
    return sorted(
        [(score, source_hash) for source_hash, score in scores.items()],
        key=lambda item: tuple(-value for value in item[0]) + (item[1],),
    )


def top_k_with_positive_ties(
    ranked: list[tuple[tuple[int, ...], str]], k: int
) -> tuple[list[tuple[tuple[int, ...], str]], bool]:
    positive = [item for item in ranked if any(value > 0 for value in item[0])]
    if len(positive) <= k:
        return positive, False
    cutoff = positive[k - 1][0]
    selected = [item for item in positive if item[0] >= cutoff]
    return selected, len(selected) > k


def anchor_gate_score(
    shared_anchors: set[str],
    *,
    operation_terms: set[str],
    exclusive_artifact_terms: set[str],
    artifact_terms_before_exclusion: set[str],
    classes_by_term: dict[str, set[str]],
    idf: dict[str, int],
) -> tuple[int, ...]:
    shared_operations = shared_anchors & operation_terms
    shared_artifacts = shared_anchors & exclusive_artifact_terms
    if not shared_operations or not shared_artifacts:
        return (0, 0, 0)
    classes = {
        class_name for term in shared_anchors
        for class_name in classes_by_term.get(term, set())
    }
    return (
        len(classes),
        sum(idf.get(term, MICRO_IDF) for term in shared_anchors),
        len(shared_anchors),
    )


def self_checks() -> None:
    ranked = ranked_channel({"b": (2, 1), "a": (2, 1), "c": (1, 9)})
    assert ranked == [((2, 1), "a"), ((2, 1), "b"), ((1, 9), "c")]
    selected, overflow = top_k_with_positive_ties(ranked, 1)
    assert selected == [((2, 1), "a"), ((2, 1), "b")] and overflow
    selected, overflow = top_k_with_positive_ties([((0, 0), "a")], 4)
    assert selected == [] and not overflow
    assert anchor_gate_score(
        {"review", "report"},
        operation_terms={"review"},
        exclusive_artifact_terms={"report"},
        artifact_terms_before_exclusion={"report"},
        classes_by_term={"review": {"operation"}, "report": {"evidence_artifact"}},
        idf={"review": 2, "report": 5},
    ) == (2, 7, 2)


def select_partition(parent_rows: list[dict[str, Any]], nc_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_selected: set[str] = set()
    for stratum in ("controlled", "public_gold"):
        rows = [row for row in parent_rows if row["stratum"] == stratum]
        selected = sorted(
            rows,
            key=lambda row: hash_key(f"E23KCAL-v1:{stratum}:{row['prompt_sha256']}"),
        )[:CALIBRATION_PARENT_PER_STRATUM]
        if len(selected) != CALIBRATION_PARENT_PER_STRATUM:
            raise SystemExit(f"Cannot select {CALIBRATION_PARENT_PER_STRATUM} parent prompts in {stratum}")
        parent_selected.update(str(row["prompt_id"]) for row in selected)

    by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in nc_rows:
        by_cluster[str(row["cluster_id"])].append(row)
    if len(by_cluster) != 54:
        raise SystemExit("NC calibration requires the fixed 54-cluster checkpoint")
    selected_clusters = sorted(
        by_cluster,
        key=lambda cluster: hash_key(f"E23KCAL-v1:cluster:{cluster}"),
    )[:CALIBRATION_NC_CLUSTERS]
    nc_selected: set[str] = set()
    for cluster in selected_clusters:
        row = min(
            by_cluster[cluster],
            key=lambda item: hash_key(f"E23KCAL-v1:prompt:{text_sha256(str(item['prompt']))}"),
        )
        nc_selected.add(str(row["prompt_id"]))

    partition: list[dict[str, Any]] = []
    for row in parent_rows:
        partition.append({
            "lane_id": "A_PARENT_EXTENDED_NON_GOLD_DELTA",
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "partition": "CALIBRATION_DEVELOPMENT" if row["prompt_id"] in parent_selected else "HELD_OUT_MAIN_COVERAGE",
            "reporting_stratum": row["stratum"],
            "reporting_group": row["group"],
            "selection_key": hash_key(f"E23KCAL-v1:{row['stratum']}:{row['prompt_sha256']}"),
        })
    for row in nc_rows:
        prompt_hash = text_sha256(str(row["prompt"]))
        partition.append({
            "lane_id": "B_NC_EXTENDED_FULL_UNION",
            "prompt_id": row["prompt_id"],
            "prompt_sha256": prompt_hash,
            "partition": "CALIBRATION_DEVELOPMENT" if row["prompt_id"] in nc_selected else "HELD_OUT_MAIN_COVERAGE",
            "reporting_stratum": "nc_extension",
            "reporting_group": row["cluster_id"],
            "selection_key": hash_key(f"E23KCAL-v1:prompt:{prompt_hash}"),
        })
    partition.sort(key=lambda row: (row["lane_id"], row["prompt_id"]))
    if sum(row["partition"] == "CALIBRATION_DEVELOPMENT" for row in partition) != 72:
        raise SystemExit("Calibration partition must contain exactly 72 prompts")
    if sum(row["partition"] == "HELD_OUT_MAIN_COVERAGE" for row in partition) != 434:
        raise SystemExit("Held-out partition must contain exactly 434 prompts")
    return partition


def add_queue_item(
    queue: dict[str, dict[str, Any]], source_hash: str, reason: str,
    score: tuple[int, ...] | None = None,
) -> None:
    item = queue.setdefault(source_hash, {
        "canonical_source_sha256": source_hash,
        "discovery_reasons": [],
        "channel_scores": {},
        "tail": False,
        "local_roster_forced": False,
        "selected_at_k": {str(k): False for k in K_VALUES},
    })
    if reason not in item["discovery_reasons"]:
        item["discovery_reasons"].append(reason)
    if score is not None:
        item["channel_scores"][reason] = list(score)


def main() -> int:
    self_checks()
    required = [BASE_PROTOCOL, CALIBRATION_PROTOCOL, PROFILES, POPULATION, PARENT_DELTA, PARENT_PROMPTS, NC_PROMPTS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    protocol = json.loads(BASE_PROTOCOL.read_text(encoding="utf-8"))
    calibration_text = CALIBRATION_PROTOCOL.read_text(encoding="utf-8")
    for required_text in ("K in {8, 12, 16}", "K_max = 16", "4,500", "36 parent prompts", "36 NC prompts"):
        if required_text not in calibration_text:
            raise SystemExit(f"Calibration protocol lacks fixed rule: {required_text}")
    token_re = re.compile(protocol["normaliser"]["token_pattern"])
    stopwords = set(protocol["normaliser"]["stopwords"])
    if set(protocol["provider_product_tokens_excluded_from_relevance_text"]) != {"anthropic", "chatgpt", "claude", "codex", "gemini", "openai"}:
        raise SystemExit("Frozen provider exclusion set changed")

    profiles = read_jsonl(PROFILES)
    population = read_jsonl(POPULATION)
    parent_delta = read_jsonl(PARENT_DELTA)
    parent_rows = read_jsonl(PARENT_PROMPTS)
    nc_rows = read_jsonl(NC_PROMPTS)
    profile_by_hash = {str(row["canonical_source_sha256"]): row for row in profiles}
    population_hashes = {str(row["canonical_source_sha256"]) for row in population}
    parent_delta_hashes = {str(row["canonical_source_sha256"]) for row in parent_delta}
    if len(profiles) != len(profile_by_hash) != len(population_hashes) != EXPECTED_EXTENDED:
        raise SystemExit("Extended profile/population binding is not 23,450 unique sources")
    if set(profile_by_hash) != population_hashes:
        raise SystemExit("Profile and population source sets differ")
    if len(parent_delta) != len(parent_delta_hashes) != EXPECTED_PARENT_DELTA or not parent_delta_hashes <= population_hashes:
        raise SystemExit("Parent alternative lane is not the fixed 21,019-source delta")
    if len(parent_rows) != EXPECTED_PARENT_PROMPTS or len(nc_rows) != EXPECTED_NC_PROMPTS:
        raise SystemExit("Prompt checkpoint count changed")

    partition = select_partition(parent_rows, nc_rows)
    partition_by_key = {(row["lane_id"], row["prompt_id"]): row for row in partition}
    source_terms: dict[str, dict[str, set[str]]] = {}
    for source_hash, profile in profile_by_hash.items():
        name_u, name_b = make_terms(str(profile["relevance_source_name"]), token_re, stopwords)
        desc_u, desc_b = make_terms(str(profile["relevance_source_description"]), token_re, stopwords)
        head_u, head_b = make_terms(str(profile["relevance_heading_profile"]), token_re, stopwords)
        source_terms[source_hash] = {
            "name_u": name_u, "name_b": name_b, "desc_u": desc_u, "desc_b": desc_b,
            "head_u": head_u, "head_b": head_b,
            "all": name_u | name_b | desc_u | desc_b | head_u | head_b,
        }

    classes_by_term: dict[str, set[str]] = defaultdict(set)
    for class_name, terms in protocol["anchor_classes"].items():
        for term in terms:
            classes_by_term[term].add(class_name)
    all_anchor_terms = set(classes_by_term)
    operation_terms = set(protocol["anchor_classes"]["operation"])
    a_protocol = protocol["channels"]["A_ARTIFACT_PROCESS_ANCHORS"]
    artifact_terms_before_exclusion = {
        term for class_name in a_protocol["exclusive_artifact_classes"]
        for term in protocol["anchor_classes"][class_name]
    }
    exclusive_artifact_terms = artifact_terms_before_exclusion - operation_terms - set(a_protocol["operation_family_excluded_from_artifact"])

    lane_inputs = {
        "A_PARENT_EXTENDED_NON_GOLD_DELTA": {
            "candidate_hashes": sorted(parent_delta_hashes),
            "prompts": [{
                "prompt_id": row["prompt_id"], "prompt": row["prompt"], "prompt_sha256": row["prompt_sha256"],
                "reporting_stratum": row["stratum"], "reporting_group": row["group"], "forced_roster": [],
            } for row in parent_rows],
        },
        "B_NC_EXTENDED_FULL_UNION": {
            "candidate_hashes": sorted(population_hashes),
            "prompts": [{
                "prompt_id": row["prompt_id"], "prompt": row["prompt"], "prompt_sha256": text_sha256(str(row["prompt"])),
                "reporting_stratum": "nc_extension", "reporting_group": row["cluster_id"],
                "forced_roster": sorted(set(str(value) for value in row["candidate_source_sha256"])),
            } for row in nc_rows],
        },
    }

    internal_queues: list[dict[str, Any]] = []
    pair_register: list[dict[str, Any]] = []
    lane_term_stats: dict[str, Any] = {}
    for lane_id, lane in lane_inputs.items():
        candidates = lane["candidate_hashes"]
        df: Counter[str] = Counter()
        for source_hash in candidates:
            df.update(source_terms[source_hash]["all"])
        idf = {term: integer_idf(len(candidates), count) for term, count in df.items()}
        lane_term_stats[lane_id] = {
            "candidate_count": len(candidates),
            "document_frequency": dict(sorted(df.items())),
            "integer_micro_idf": dict(sorted(idf.items())),
        }
        for prompt in sorted(lane["prompts"], key=lambda row: row["prompt_id"]):
            if partition_by_key[(lane_id, prompt["prompt_id"])]["partition"] != "CALIBRATION_DEVELOPMENT":
                continue
            query_u, query_b = make_terms(str(prompt["prompt"]), token_re, stopwords)
            query_all = query_u | query_b
            n_scores: dict[str, tuple[int, ...]] = {}
            h_scores: dict[str, tuple[int, ...]] = {}
            a_scores: dict[str, tuple[int, ...]] = {}
            for source_hash in candidates:
                terms = source_terms[source_hash]
                n_weights: dict[str, int] = {}
                for term in terms["desc_u"]:
                    n_weights[term] = max(n_weights.get(term, 0), 1)
                for term in terms["name_u"]:
                    n_weights[term] = max(n_weights.get(term, 0), 2)
                for term in terms["desc_b"]:
                    n_weights[term] = max(n_weights.get(term, 0), 2)
                for term in terms["name_b"]:
                    n_weights[term] = max(n_weights.get(term, 0), 4)
                shared_n = query_all & set(n_weights)
                n_scores[source_hash] = (sum(idf.get(term, MICRO_IDF) * n_weights[term] for term in shared_n), len(shared_n))
                shared_h_b = query_b & terms["head_b"]
                shared_h_u = query_u & terms["head_u"]
                shared_h = shared_h_b if shared_h_b else shared_h_u
                h_scores[source_hash] = (
                    2 if shared_h_b else (1 if shared_h_u else 0),
                    max((idf.get(term, MICRO_IDF) for term in shared_h), default=0),
                    sum(idf.get(term, MICRO_IDF) for term in shared_h), len(shared_h),
                )
                a_scores[source_hash] = anchor_gate_score(
                    query_all & terms["all"] & all_anchor_terms,
                    operation_terms=operation_terms,
                    exclusive_artifact_terms=exclusive_artifact_terms,
                    artifact_terms_before_exclusion=artifact_terms_before_exclusion,
                    classes_by_term=classes_by_term,
                    idf=idf,
                )
            rankings = {
                "N_NAME_DESCRIPTION": ranked_channel(n_scores),
                "H_HEADINGS": ranked_channel(h_scores),
                "A_ARTIFACT_PROCESS_ANCHORS": ranked_channel(a_scores),
            }
            queue: dict[str, dict[str, Any]] = {}
            channel_diagnostics: dict[str, Any] = {}
            selected_by_k: dict[int, set[str]] = {k: set() for k in K_VALUES}
            for channel, ranked in rankings.items():
                for k in K_VALUES:
                    selected, overflow = top_k_with_positive_ties(ranked, k)
                    channel_diagnostics.setdefault(channel, {})[str(k)] = {
                        "selected_count": len(selected), "positive_tie_overflow": overflow,
                        "cutoff_score": list(selected[-1][0]) if selected else None,
                    }
                    for score, source_hash in selected:
                        selected_by_k[k].add(source_hash)
                        if k == K_MAX:
                            add_queue_item(queue, source_hash, channel, score)
            for source_hash in prompt["forced_roster"]:
                if source_hash not in candidates:
                    raise SystemExit(f"Forced NC roster source missing from lane: {source_hash}")
                for k in K_VALUES:
                    selected_by_k[k].add(source_hash)
                add_queue_item(queue, source_hash, "FORCED_NC_LOCAL_ROSTER")
                queue[source_hash]["local_roster_forced"] = True
            for k in K_VALUES:
                for source_hash in selected_by_k[k]:
                    if source_hash not in queue:
                        raise SystemExit("Smaller-K selection absent from K=16 queue")
                    queue[source_hash]["selected_at_k"][str(k)] = True
            phrase_tail = next(
                (source_hash for score, source_hash in rankings["H_HEADINGS"]
                 if any(value > 0 for value in score) and source_hash not in queue),
                None,
            )
            if phrase_tail:
                add_queue_item(queue, phrase_tail, "TAIL_PHRASE")
                queue[phrase_tail]["tail"] = True
            residual = [source_hash for source_hash in candidates if source_hash not in queue]
            residual_tail = None
            if residual:
                represented = {profile_by_hash[source_hash]["final_intake_role"] for source_hash in queue}
                chosen_pool: list[str] = []
                for role in RESIDUAL_ROLE_ORDER:
                    if role in represented:
                        continue
                    chosen_pool = [source_hash for source_hash in residual if profile_by_hash[source_hash]["final_intake_role"] == role]
                    if chosen_pool:
                        break
                if not chosen_pool:
                    chosen_pool = residual
                residual_tail = min(
                    chosen_pool,
                    key=lambda source_hash: hash_key(f"{prompt['prompt_sha256']}:{source_hash}"),
                )
                add_queue_item(queue, residual_tail, "TAIL_RESIDUAL")
                queue[residual_tail]["tail"] = True
            items = []
            for source_hash in sorted(queue):
                item = queue[source_hash]
                profile = profile_by_hash[source_hash]
                item["discovery_reasons"].sort()
                item["candidate_alias_ids"] = profile["candidate_alias_ids"]
                item["final_intake_role"] = profile["final_intake_role"]
                item["review_priority"] = "TAIL_FIRST" if item["tail"] else "MAIN_POOL"
                items.append(item)
                pair_id = hash_key(f"E23KCAL-v1:pair:{lane_id}:{prompt['prompt_sha256']}:{source_hash}")
                pair_register.append({
                    "calibration_pair_id": pair_id,
                    "lane_id": lane_id,
                    "prompt_id": prompt["prompt_id"],
                    "prompt_sha256": prompt["prompt_sha256"],
                    "canonical_source_sha256": source_hash,
                    "source_paths": profile["source_paths"],
                    "final_intake_role": profile["final_intake_role"],
                    "discovery_reasons": item["discovery_reasons"],
                    "channel_scores": item["channel_scores"],
                    "selected_at_k": item["selected_at_k"],
                    "tail": item["tail"],
                    "local_roster_forced": item["local_roster_forced"],
                    "review_status": "PENDING_INDEPENDENT_SOURCE_VISIBLE_A_B_ADJUDICATION",
                })
            internal_queues.append({
                "lane_id": lane_id,
                "prompt_id": prompt["prompt_id"],
                "prompt": prompt["prompt"],
                "prompt_sha256": prompt["prompt_sha256"],
                "reporting_stratum": prompt["reporting_stratum"],
                "reporting_group": prompt["reporting_group"],
                "candidate_universe_count": len(candidates),
                "channel_diagnostics": channel_diagnostics,
                "phrase_tail_source_sha256": phrase_tail,
                "residual_tail_source_sha256": residual_tail,
                "queue_count": len(items),
                "queue": items,
                "status": "OUTCOME_BLIND_K_CALIBRATION_QUEUE_PENDING_INDEPENDENT_A_B_REVIEW",
            })

    internal_queues.sort(key=lambda row: (row["lane_id"], row["prompt_id"]))
    pair_register.sort(key=lambda row: (row["lane_id"], row["prompt_id"], row["canonical_source_sha256"]))
    if len(internal_queues) != 72 or len(pair_register) != len({row["calibration_pair_id"] for row in pair_register}):
        raise SystemExit("Calibration queue uniqueness/count invariant failed")
    if len(pair_register) > REVIEWER_PAIR_BUDGET:
        raise SystemExit(f"K_SELECTION_HOLD: packet count {len(pair_register)} exceeds {REVIEWER_PAIR_BUDGET}")

    for pair in pair_register:
        pair["reviewer_item_ids"] = {
            reviewer: hash_key(f"E23KCAL-v1:reviewer-{reviewer}:{pair['calibration_pair_id']}")
            for reviewer in ("A", "B")
        }

    prompt_by_key = {
        (row["lane_id"], row["prompt_id"]): row["prompt"]
        for row in internal_queues
    }
    reviewer_packets: dict[str, list[dict[str, Any]]] = {"A": [], "B": []}
    for pair in pair_register:
        prompt = prompt_by_key[(pair["lane_id"], pair["prompt_id"])]
        for reviewer in reviewer_packets:
            item_id = pair["reviewer_item_ids"][reviewer]
            reviewer_packets[reviewer].append({
                "review_item_id": item_id,
                "prompt": prompt,
                "source_paths": pair["source_paths"],
                "source_sha256": pair["canonical_source_sha256"],
                "instructions": (
                    "Assess this byte-bound source against this prompt using the established adequacy rubric. "
                    "Do not infer an intended benchmark target; record one source-visible disposition and evidence."
                ),
                "required_dispositions": ["FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "NOT_ADEQUATE", "UNCLEAR"],
                "status": "PENDING_INDEPENDENT_REVIEW",
            })
    for reviewer, rows in reviewer_packets.items():
        rows.sort(key=lambda row: hash_key(f"E23KCAL-v1:reviewer-order-{reviewer}:{row['review_item_id']}"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(PARTITION_OUT, partition)
    write_jsonl(QUEUE_OUT, internal_queues)
    write_jsonl(PAIR_REGISTER_OUT, pair_register)
    write_jsonl(REVIEWER_A_OUT, reviewer_packets["A"])
    write_jsonl(REVIEWER_B_OUT, reviewer_packets["B"])
    TERM_STATS_OUT.write_text(json.dumps(lane_term_stats, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    pairs_by_lane = Counter(row["lane_id"] for row in pair_register)
    summary = {
        "status": "PASS_OUTCOME_BLIND_23450_SOURCE_K_CALIBRATION_PACKET_PENDING_A_B_REVIEW",
        "bound_inputs": {str(path.relative_to(BENCHMARK_ROOT)): sha256_file(path) for path in required},
        "counts": {
            "calibration_prompts": len(internal_queues),
            "calibration_parent_prompts": sum(row["lane_id"] == "A_PARENT_EXTENDED_NON_GOLD_DELTA" for row in internal_queues),
            "calibration_nc_prompts": sum(row["lane_id"] == "B_NC_EXTENDED_FULL_UNION" for row in internal_queues),
            "held_out_main_coverage_prompts": 434,
            "unique_source_visible_pairs_per_reviewer": len(pair_register),
            "pairs_by_lane": dict(sorted(pairs_by_lane.items())),
            "tail_pairs": sum(row["tail"] for row in pair_register),
            "forced_nc_local_roster_pairs": sum(row["local_roster_forced"] for row in pair_register),
            "reviewer_budget": REVIEWER_PAIR_BUDGET,
            "reviewer_budget_remaining": REVIEWER_PAIR_BUDGET - len(pair_register),
        },
        "k_grid": list(K_VALUES),
        "k_max": K_MAX,
        "selection_rule": "Smallest K in {8,12,16} with zero reconciled post-K positives in both calibration lanes; otherwise K_SELECTION_HOLD.",
        "outcome_blind_firewall": {
            "source_fields_read_for_relevance": ["relevance_source_name", "relevance_source_description", "relevance_heading_profile"],
            "prompt_fields_read_for_relevance": ["prompt"],
            "not_read_for_relevance": protocol["forbidden_relevance_fields"],
            "nc_forced_roster_after_ranking_only": True,
            "reviewer_packets_hide": ["lane_id", "prompt_id", "historical_target", "cluster_local_label", "rank", "rank_band", "selection_reason", "K_membership"],
        },
        "outputs": {path.name: sha256_file(path) for path in [PARTITION_OUT, QUEUE_OUT, PAIR_REGISTER_OUT, REVIEWER_A_OUT, REVIEWER_B_OUT, TERM_STATS_OUT]},
        "claim_boundary": [
            "This output contains no reviewer outcome and therefore does not select K.",
            "The 20,356 background sources remain unadjudicated outside prompt-source pairs reviewed under this protocol.",
            "Calibration outcomes can select K but cannot be pooled into the held-out final coverage conclusion.",
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
