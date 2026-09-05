#!/usr/bin/env python3
"""Materialise the frozen outcome-blind pooled alternative-discovery queues."""

from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK_ROOT = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK_ROOT / "rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_PROTOCOL_2026-08-31.json"
K6_OVERRIDE = NC_ROOT / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_V3_K6_B_OVERRIDE_2026-08-31.json"
PROFILES = NC_ROOT / "manifests/whole_library_navigation_profiles_prefreeze_2026-08-31/navigation_profiles.jsonl"
UNION = NC_ROOT / "manifests/current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
DELTA = NC_ROOT / "manifests/parent_v3_delta_candidate_inventory_current_pre_freeze_2026-08-31/new_to_parent_v3_candidates.jsonl"
PARENT_IDENTITIES = BENCHMARK_ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
PARENT_PROMPTS = BENCHMARK_ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
NC_PROMPTS = NC_ROOT / "manifests/curation_closed_checkpoint_2026-08-31/curation_eligible_prompts.jsonl"
OUTPUT_DIR = NC_ROOT / "manifests/whole_library_pooled_discovery_queue_v3_k6_b_2026-08-31"
QUEUE_OUT = OUTPUT_DIR / "prompt_discovery_queues.jsonl"
PAIR_OUT = OUTPUT_DIR / "source_visible_review_pairs.jsonl"
ANCHOR_GATE_OUT = OUTPUT_DIR / "anchor_gate_accounting.jsonl"
TERM_STATS_OUT = OUTPUT_DIR / "lane_term_statistics.json"
SUMMARY_OUT = OUTPUT_DIR / "summary.json"
MICRO_IDF = 1_000_000


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def make_terms(text: str, token_re: re.Pattern[str], stopwords: set[str]) -> tuple[set[str], set[str]]:
    normalised = unicodedata.normalize("NFKC", text).lower()
    tokens = [
        token
        for token in token_re.findall(normalised)
        if token not in stopwords and len(token) > 1
    ]
    unigrams = set(tokens)
    bigrams = {f"{left}::{right}" for left, right in zip(tokens, tokens[1:])}
    return unigrams, bigrams


def integer_idf(document_count: int, document_frequency: int) -> int:
    return round((math.log((document_count + 1) / (document_frequency + 1)) + 1) * MICRO_IDF)


def top_k_with_positive_ties(
    ranked: list[tuple[tuple[int, ...], str]], k: int
) -> tuple[list[tuple[tuple[int, ...], str]], bool]:
    positive = [item for item in ranked if any(value > 0 for value in item[0])]
    if len(positive) <= k:
        return positive, False
    cutoff = positive[k - 1][0]
    included = [item for item in positive if item[0] >= cutoff]
    return included, len(included) > k


def ranked_channel(
    scores: dict[str, tuple[int, ...]],
) -> list[tuple[tuple[int, ...], str]]:
    score_hash_pairs = [(score, source_hash) for source_hash, score in scores.items()]
    return sorted(
        score_hash_pairs,
        key=lambda item: tuple([-value for value in item[0]]) + (item[1],),
    )


def add_queue_reason(
    queue: dict[str, dict],
    source_hash: str,
    *,
    reason: str,
    score: tuple[int, ...] | None = None,
) -> None:
    item = queue.setdefault(
        source_hash,
        {
            "canonical_source_sha256": source_hash,
            "discovery_reasons": [],
            "channel_scores": {},
            "tail": False,
            "local_roster_forced": False,
        },
    )
    if reason not in item["discovery_reasons"]:
        item["discovery_reasons"].append(reason)
    if score is not None:
        item["channel_scores"][reason] = list(score)


def anchor_gate_score(
    shared_anchors: set[str],
    *,
    operation_terms: set[str],
    exclusive_artifact_terms: set[str],
    artifact_terms_before_exclusion: set[str],
    classes_by_term: dict[str, set[str]],
    idf: dict[str, int],
) -> tuple[tuple[int, ...], str, list[str], list[str], list[str]]:
    shared_operations = shared_anchors & operation_terms
    shared_artifacts = shared_anchors & exclusive_artifact_terms
    if not shared_operations:
        disposition = "NO_SHARED_OPERATION"
    elif not shared_artifacts:
        disposition = (
            "DUAL_CLASS_OR_FAMILY_ONLY"
            if shared_anchors & artifact_terms_before_exclusion
            else "NO_SHARED_EXCLUSIVE_ARTIFACT"
        )
    else:
        disposition = "A_GATE_PASS"

    if disposition != "A_GATE_PASS":
        return (0, 0, 0), disposition, sorted(shared_operations), [], []

    classes = sorted(
        {
            class_name
            for term in shared_anchors
            for class_name in classes_by_term.get(term, set())
        }
    )
    return (
        len(classes),
        sum(idf.get(term, MICRO_IDF) for term in shared_anchors),
        len(shared_anchors),
    ), disposition, sorted(shared_operations), sorted(shared_artifacts), classes


def self_checks() -> None:
    ranked = ranked_channel({"b": (2, 1), "a": (2, 1), "c": (1, 9)})
    assert ranked == [((2, 1), "a"), ((2, 1), "b"), ((1, 9), "c")]
    selected, overflow = top_k_with_positive_ties(ranked, 1)
    assert selected == [((2, 1), "a"), ((2, 1), "b")]
    assert overflow
    selected, overflow = top_k_with_positive_ties([((0, 0), "a")], 4)
    assert selected == [] and not overflow
    gate_kwargs = {
        "operation_terms": {"review", "test", "tests"},
        "exclusive_artifact_terms": {"report", "api"},
        "artifact_terms_before_exclusion": {"report", "api", "test", "tests"},
        "classes_by_term": {
            "review": {"operation"},
            "test": {"operation", "software_artifact"},
            "tests": {"operation", "software_artifact"},
            "report": {"evidence_artifact"},
            "api": {"software_artifact"},
        },
        "idf": {"review": 2, "test": 3, "tests": 3, "report": 5, "api": 7},
    }
    assert anchor_gate_score({"review"}, **gate_kwargs)[1] == "NO_SHARED_EXCLUSIVE_ARTIFACT"
    assert anchor_gate_score({"report"}, **gate_kwargs)[1] == "NO_SHARED_OPERATION"
    assert anchor_gate_score({"test"}, **gate_kwargs)[1] == "DUAL_CLASS_OR_FAMILY_ONLY"
    passed = anchor_gate_score({"review", "report"}, **gate_kwargs)
    assert passed[1] == "A_GATE_PASS" and passed[0] == (2, 7, 2)


def main() -> None:
    self_checks()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["status"] == "FROZEN_AFTER_V1_PREFREEZE_REPAIR_BEFORE_V2_QUEUE_MATERIALISATION"
    override = json.loads(K6_OVERRIDE.read_text(encoding="utf-8"))
    assert override["status"] in {
        "FROZEN_AFTER_CONFIRMED_B_LANE_TAIL_TRIGGER_BEFORE_V3_QUEUE_MATERIALISATION",
        "FROZEN_AFTER_CONFIRMED_A_LANE_TAIL_TRIGGER_BEFORE_V4_QUEUE_MATERIALISATION",
    }
    assert override["base_protocol_sha256"] == sha256(PROTOCOL)
    trigger_evidence_path = BENCHMARK_ROOT / override["trigger_evidence"]["path"]
    assert override["trigger_evidence"]["sha256"] == sha256(trigger_evidence_path)
    token_re = re.compile(protocol["normaliser"]["token_pattern"])
    stopwords = set(protocol["normaliser"]["stopwords"])
    classes_by_anchor_term: dict[str, set[str]] = defaultdict(set)
    for class_name, terms in protocol["anchor_classes"].items():
        for term in terms:
            classes_by_anchor_term[term].add(class_name)
    all_anchor_terms = set(classes_by_anchor_term)
    operation_terms = set(protocol["anchor_classes"]["operation"])
    a_protocol = protocol["channels"]["A_ARTIFACT_PROCESS_ANCHORS"]
    artifact_terms_before_exclusion = {
        term
        for class_name in a_protocol["exclusive_artifact_classes"]
        for term in protocol["anchor_classes"][class_name]
    }
    excluded_artifact_family = set(a_protocol["operation_family_excluded_from_artifact"])
    exclusive_artifact_terms = artifact_terms_before_exclusion - operation_terms - excluded_artifact_family
    assert not (exclusive_artifact_terms & operation_terms)

    profiles = read_jsonl(PROFILES)
    profile_by_hash = {row["canonical_source_sha256"]: row for row in profiles}
    union_rows = read_jsonl(UNION)
    union_hashes = {row["canonical_source_sha256"] for row in union_rows}
    delta_rows = read_jsonl(DELTA)
    delta_hashes = {row["canonical_source_sha256"] for row in delta_rows}
    parent_identity_rows = read_jsonl(PARENT_IDENTITIES)
    parent_hashes = {row["source_sha256"] for row in parent_identity_rows}
    parent_prompt_rows = read_jsonl(PARENT_PROMPTS)
    nc_prompt_rows = read_jsonl(NC_PROMPTS)

    assert len(profiles) == len(profile_by_hash) == len(union_hashes) == 3094
    assert set(profile_by_hash) == union_hashes
    assert len(delta_hashes) == 663
    assert len(parent_hashes) == 2431
    assert not (delta_hashes & parent_hashes)
    assert delta_hashes | parent_hashes == union_hashes
    assert len(parent_prompt_rows) == 381
    assert len(nc_prompt_rows) == 125

    source_terms: dict[str, dict[str, set[str]]] = {}
    for source_hash, profile in profile_by_hash.items():
        name_u, name_b = make_terms(profile["relevance_source_name"], token_re, stopwords)
        desc_u, desc_b = make_terms(profile["relevance_source_description"], token_re, stopwords)
        head_u, head_b = make_terms(profile["relevance_heading_profile"], token_re, stopwords)
        source_terms[source_hash] = {
            "name_u": name_u,
            "name_b": name_b,
            "desc_u": desc_u,
            "desc_b": desc_b,
            "head_u": head_u,
            "head_b": head_b,
            "all": name_u | name_b | desc_u | desc_b | head_u | head_b,
        }

    lane_inputs = {
        "A_PARENT_DELTA": {
            "candidates": sorted(delta_hashes),
            "prompts": [
                {
                    "prompt_id": row["prompt_id"],
                    "prompt": row["prompt"],
                    "prompt_sha256": row["prompt_sha256"],
                    "reporting_stratum": row["stratum"],
                    "reporting_group": row["group"],
                    "forced_roster": [],
                }
                for row in parent_prompt_rows
            ],
        },
        "B_NC_FULL_UNION": {
            "candidates": sorted(union_hashes),
            "prompts": [
                {
                    "prompt_id": row["prompt_id"],
                    "prompt": row["prompt"],
                    "prompt_sha256": text_sha256(row["prompt"]),
                    "reporting_stratum": "nc_extension",
                    "reporting_group": row["cluster_id"],
                    "forced_roster": sorted(set(row["candidate_source_sha256"])),
                }
                for row in nc_prompt_rows
            ],
        },
    }

    all_queue_rows: list[dict] = []
    all_pair_rows: list[dict] = []
    all_anchor_gate_rows: list[dict] = []
    term_statistics: dict[str, dict] = {}
    diagnostic_counts: Counter[str] = Counter()
    lane_pair_counts: Counter[str] = Counter()

    for lane_id, lane in lane_inputs.items():
        candidate_hashes = lane["candidates"]
        candidate_count = len(candidate_hashes)
        expected = protocol["lanes"][lane_id]
        assert len(lane["prompts"]) == expected["prompt_count"]
        assert candidate_count == expected["candidate_count"]

        df: Counter[str] = Counter()
        for source_hash in candidate_hashes:
            df.update(source_terms[source_hash]["all"])
        idf = {term: integer_idf(candidate_count, count) for term, count in df.items()}
        term_statistics[lane_id] = {
            "candidate_count": candidate_count,
            "document_frequency": dict(sorted(df.items())),
            "integer_micro_idf": dict(sorted(idf.items())),
        }

        for prompt in sorted(lane["prompts"], key=lambda row: row["prompt_id"]):
            assert prompt["prompt_sha256"] == text_sha256(prompt["prompt"])
            query_u, query_b = make_terms(prompt["prompt"], token_re, stopwords)
            query_all = query_u | query_b
            n_scores: dict[str, tuple[int, ...]] = {}
            h_scores: dict[str, tuple[int, ...]] = {}
            a_scores: dict[str, tuple[int, ...]] = {}
            a_gate_evidence: dict[str, dict] = {}
            a_gate_counts: Counter[str] = Counter()

            for source_hash in candidate_hashes:
                terms = source_terms[source_hash]
                n_weight: dict[str, int] = {}
                for term in terms["desc_u"]:
                    n_weight[term] = max(n_weight.get(term, 0), 1)
                for term in terms["name_u"]:
                    n_weight[term] = max(n_weight.get(term, 0), 2)
                for term in terms["desc_b"]:
                    n_weight[term] = max(n_weight.get(term, 0), 2)
                for term in terms["name_b"]:
                    n_weight[term] = max(n_weight.get(term, 0), 4)
                shared_n = query_all & set(n_weight)
                n_score = sum(idf.get(term, MICRO_IDF) * n_weight[term] for term in shared_n)
                n_scores[source_hash] = (n_score, len(shared_n))

                shared_h_b = query_b & terms["head_b"]
                shared_h_u = query_u & terms["head_u"]
                shared_h = shared_h_b if shared_h_b else shared_h_u
                h_scores[source_hash] = (
                    2 if shared_h_b else (1 if shared_h_u else 0),
                    max((idf.get(term, MICRO_IDF) for term in shared_h), default=0),
                    sum(idf.get(term, MICRO_IDF) for term in shared_h),
                    len(shared_h),
                )

                shared_anchors = query_all & terms["all"] & all_anchor_terms
                a_score, gate_disposition, shared_o, shared_x, anchor_classes = anchor_gate_score(
                    shared_anchors,
                    operation_terms=operation_terms,
                    exclusive_artifact_terms=exclusive_artifact_terms,
                    artifact_terms_before_exclusion=artifact_terms_before_exclusion,
                    classes_by_term=classes_by_anchor_term,
                    idf=idf,
                )
                a_scores[source_hash] = a_score
                a_gate_counts[gate_disposition] += 1
                if gate_disposition == "A_GATE_PASS":
                    a_gate_evidence[source_hash] = {
                        "canonical_source_sha256": source_hash,
                        "shared_operation_terms": shared_o,
                        "shared_exclusive_artifact_terms": shared_x,
                        "shared_anchor_classes": anchor_classes,
                        "rank_score": list(a_score),
                    }

            channel_rankings = {
                "N_NAME_DESCRIPTION": ranked_channel(n_scores),
                "H_HEADINGS": ranked_channel(h_scores),
                "A_ARTIFACT_PROCESS_ANCHORS": ranked_channel(a_scores),
            }
            queue: dict[str, dict] = {}
            channel_diagnostics: dict[str, dict] = {}
            for channel_name, ranked in channel_rankings.items():
                k = int(
                    override["channel_k_by_lane"][lane_id].get(
                        channel_name, protocol["channels"][channel_name]["k"]
                    )
                )
                selected, overflow = top_k_with_positive_ties(ranked, k)
                channel_diagnostics[channel_name] = {
                    "selected_count": len(selected),
                    "positive_tie_overflow": overflow,
                    "cutoff_score": list(selected[-1][0]) if selected else None,
                }
                if not selected:
                    diagnostic_counts[f"{lane_id}:EMPTY:{channel_name}"] += 1
                if overflow:
                    diagnostic_counts[f"{lane_id}:TIE_OVERFLOW:{channel_name}"] += 1
                for score, source_hash in selected:
                    add_queue_reason(queue, source_hash, reason=channel_name, score=score)

            selected_a_hashes = {
                source_hash
                for _, source_hash in top_k_with_positive_ties(
                    channel_rankings["A_ARTIFACT_PROCESS_ANCHORS"],
                    int(
                        override["channel_k_by_lane"][lane_id].get(
                            "A_ARTIFACT_PROCESS_ANCHORS",
                            protocol["channels"]["A_ARTIFACT_PROCESS_ANCHORS"]["k"],
                        )
                    ),
                )[0]
            }
            for source_hash, evidence in a_gate_evidence.items():
                evidence["selected_by_a_channel"] = source_hash in selected_a_hashes
            assert sum(a_gate_counts.values()) == candidate_count
            assert a_gate_counts["A_GATE_PASS"] == len(a_gate_evidence)
            all_anchor_gate_rows.append(
                {
                    "lane_id": lane_id,
                    "prompt_id": prompt["prompt_id"],
                    "prompt_sha256": prompt["prompt_sha256"],
                    "candidate_universe_count": candidate_count,
                    "gate_disposition_counts": dict(sorted(a_gate_counts.items())),
                    "eligible_candidate_evidence": [
                        a_gate_evidence[source_hash] for source_hash in sorted(a_gate_evidence)
                    ],
                    "protocol_version": protocol["protocol_version"],
                }
            )

            for source_hash in prompt["forced_roster"]:
                assert source_hash in candidate_hashes
                add_queue_reason(queue, source_hash, reason="FORCED_NC_LOCAL_ROSTER")
                queue[source_hash]["local_roster_forced"] = True

            phrase_tail_hash = None
            for score, source_hash in channel_rankings["H_HEADINGS"]:
                if any(value > 0 for value in score) and source_hash not in queue:
                    phrase_tail_hash = source_hash
                    break
            if phrase_tail_hash:
                add_queue_reason(queue, phrase_tail_hash, reason="TAIL_PHRASE")
                queue[phrase_tail_hash]["tail"] = True
            else:
                diagnostic_counts[f"{lane_id}:NO_PHRASE_TAIL"] += 1

            residual = [source_hash for source_hash in candidate_hashes if source_hash not in queue]
            residual_tail_hash = None
            if residual:
                represented_roles = {
                    profile_by_hash[source_hash]["final_intake_role"] for source_hash in queue
                }
                role_order = protocol["tail_challenge"]["role_order"]
                chosen_pool: list[str] = []
                for role in role_order:
                    if role in represented_roles:
                        continue
                    chosen_pool = [
                        source_hash
                        for source_hash in residual
                        if profile_by_hash[source_hash]["final_intake_role"] == role
                    ]
                    if chosen_pool:
                        break
                if not chosen_pool:
                    chosen_pool = residual
                residual_tail_hash = min(
                    chosen_pool,
                    key=lambda source_hash: hashlib.sha256(
                        f"{prompt['prompt_sha256']}:{source_hash}".encode("utf-8")
                    ).hexdigest(),
                )
                add_queue_reason(queue, residual_tail_hash, reason="TAIL_RESIDUAL")
                queue[residual_tail_hash]["tail"] = True
            else:
                diagnostic_counts[f"{lane_id}:NO_RESIDUAL_TAIL"] += 1

            queue_items = []
            for source_hash in sorted(queue):
                item = queue[source_hash]
                profile = profile_by_hash[source_hash]
                item["candidate_alias_ids"] = profile["candidate_alias_ids"]
                item["final_intake_role"] = profile["final_intake_role"]
                item["review_priority"] = "TAIL_FIRST" if item["tail"] else "MAIN_POOL"
                item["discovery_reasons"].sort()
                queue_items.append(item)
                all_pair_rows.append(
                    {
                        "lane_id": lane_id,
                        "prompt_id": prompt["prompt_id"],
                        "prompt_sha256": prompt["prompt_sha256"],
                        "canonical_source_sha256": source_hash,
                        "candidate_alias_ids": profile["candidate_alias_ids"],
                        "final_intake_role": profile["final_intake_role"],
                        "discovery_reasons": item["discovery_reasons"],
                        "channel_scores": item["channel_scores"],
                        "tail": item["tail"],
                        "local_roster_forced": item["local_roster_forced"],
                        "review_status": "PENDING_SOURCE_VISIBLE_ADJUDICATION",
                    }
                )

            lane_pair_counts[lane_id] += len(queue_items)
            all_queue_rows.append(
                {
                    "lane_id": lane_id,
                    "prompt_id": prompt["prompt_id"],
                    "prompt": prompt["prompt"],
                    "prompt_sha256": prompt["prompt_sha256"],
                    "reporting_stratum": prompt["reporting_stratum"],
                    "reporting_group": prompt["reporting_group"],
                    "candidate_universe_count": candidate_count,
                    "channel_diagnostics": channel_diagnostics,
                    "phrase_tail_source_sha256": phrase_tail_hash,
                    "residual_tail_source_sha256": residual_tail_hash,
                    "queue_count": len(queue_items),
                    "queue": queue_items,
                    "status": "OUTCOME_BLIND_DISCOVERY_QUEUE_PENDING_SOURCE_VISIBLE_ADJUDICATION",
                }
            )

    all_queue_rows.sort(key=lambda row: (row["lane_id"], row["prompt_id"]))
    all_pair_rows.sort(
        key=lambda row: (row["lane_id"], row["prompt_id"], row["canonical_source_sha256"])
    )
    all_anchor_gate_rows.sort(key=lambda row: (row["lane_id"], row["prompt_id"]))
    assert len(all_queue_rows) == 506
    assert len(all_pair_rows) == len(
        {
            (row["lane_id"], row["prompt_id"], row["canonical_source_sha256"])
            for row in all_pair_rows
        }
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(QUEUE_OUT, all_queue_rows)
    write_jsonl(PAIR_OUT, all_pair_rows)
    write_jsonl(ANCHOR_GATE_OUT, all_anchor_gate_rows)
    TERM_STATS_OUT.write_text(
        json.dumps(term_statistics, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    queue_counts = [row["queue_count"] for row in all_queue_rows]
    summary = {
        "status": "PASS_OUTCOME_BLIND_POOLED_DISCOVERY_QUEUE_NOT_A_LABEL_METRIC_OR_SELECTOR_RESULT",
        "bound_inputs": {
            str(PROTOCOL.relative_to(BENCHMARK_ROOT)): sha256(PROTOCOL),
            str(K6_OVERRIDE.relative_to(BENCHMARK_ROOT)): sha256(K6_OVERRIDE),
            str(PROFILES.relative_to(BENCHMARK_ROOT)): sha256(PROFILES),
            str(UNION.relative_to(BENCHMARK_ROOT)): sha256(UNION),
            str(DELTA.relative_to(BENCHMARK_ROOT)): sha256(DELTA),
            str(PARENT_IDENTITIES.relative_to(BENCHMARK_ROOT)): sha256(PARENT_IDENTITIES),
            str(PARENT_PROMPTS.relative_to(BENCHMARK_ROOT)): sha256(PARENT_PROMPTS),
            str(NC_PROMPTS.relative_to(BENCHMARK_ROOT)): sha256(NC_PROMPTS),
        },
        "counts": {
            "prompt_queues": len(all_queue_rows),
            "source_visible_review_pairs": len(all_pair_rows),
            "pairs_by_lane": dict(sorted(lane_pair_counts.items())),
            "minimum_queue_size": min(queue_counts),
            "maximum_queue_size": max(queue_counts),
            "mean_queue_size": sum(queue_counts) / len(queue_counts),
            "tail_pairs": sum(row["tail"] for row in all_pair_rows),
            "forced_nc_local_roster_pairs": sum(
                row["local_roster_forced"] for row in all_pair_rows
            ),
            "anchor_gate_tested_pairs": sum(
                row["candidate_universe_count"] for row in all_anchor_gate_rows
            ),
            "anchor_gate_eligible_pairs": sum(
                row["gate_disposition_counts"].get("A_GATE_PASS", 0)
                for row in all_anchor_gate_rows
            ),
            "diagnostics": dict(sorted(diagnostic_counts.items())),
        },
        "channel_k_by_lane": override["channel_k_by_lane"],
        "tail_trigger_override": {
            "affected_lanes": override.get("affected_lanes") or [override["affected_lane"]],
            "trigger_evidence_path": override["trigger_evidence"]["path"],
            "trigger_evidence_sha256": sha256(trigger_evidence_path),
        },
        "outputs": {
            QUEUE_OUT.name: sha256(QUEUE_OUT),
            PAIR_OUT.name: sha256(PAIR_OUT),
            ANCHOR_GATE_OUT.name: sha256(ANCHOR_GATE_OUT),
            TERM_STATS_OUT.name: sha256(TERM_STATS_OUT),
        },
        "outcome_blind_firewall": {
            "parent_fields_read_for_relevance": ["prompt_id", "prompt", "prompt_sha256"],
            "nc_fields_read_for_relevance": ["prompt_id", "prompt"],
            "nc_nonranking_forced_roster_field": "candidate_source_sha256",
            "source_fields_read_for_relevance": [
                "relevance_source_name",
                "relevance_source_description",
                "relevance_heading_profile"
            ],
            "not_read_for_relevance": protocol["forbidden_relevance_fields"],
        },
        "claim_boundary": [
            "Every in-scope candidate was screened by all frozen applicable channels.",
            "Only pooled and tail candidates are queued for source-visible adjudication.",
            "Unqueued sources receive no negative label; this is not exhaustive whole-library relevance annotation.",
            "No historical selector output, adequacy result, acceptable set, gold identity, metric, embedding or reranker is used or produced."
        ]
    }
    SUMMARY_OUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
