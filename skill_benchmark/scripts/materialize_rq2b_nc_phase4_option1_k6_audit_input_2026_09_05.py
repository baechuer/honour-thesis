#!/usr/bin/env python3
"""Materialise the prospectively frozen, outcome-blind Phase-4 K=6 audit input.

This is a candidate-proposal and blind-packet construction step only.  It does
not read adequacy labels, historical gold, targets, retrieval/reranking output,
provider output, or metrics; nor does it make any final benchmark claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
BASE_NAVIGATION_PROTOCOL = NC_ROOT / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_PROTOCOL_2026-08-31.json"
AMENDMENT = NC_ROOT / "review/RQ2B_NC_PHASE4_OPTION1_LEGACY_AMENDMENT_2026-09-05.json"
PHASE3 = NC_ROOT / "manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
PROFILES = NC_ROOT / "manifests/rq2b_nc_phase4_navigation_profiles_2026-09-05"
PARENT_IDENTITIES = BENCHMARK / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
OUT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"

MICRO_IDF = 1_000_000
TOKEN_SALT = "rq2b-nc-phase4-audit-input-token-v1"
EXPECTED_AMENDMENT_STATUS = "USER_APPROVED_PHASE4_OPTION1_LEGACY_2LOCAL_K6_AND_NESTED_PATH_FALLBACK"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def make_terms(text: str, token_re: re.Pattern[str], stopwords: set[str]) -> tuple[set[str], set[str]]:
    tokens = [token for token in token_re.findall(unicodedata.normalize("NFKC", text).lower()) if token not in stopwords and len(token) > 1]
    return set(tokens), {f"{left}::{right}" for left, right in zip(tokens, tokens[1:])}


def integer_idf(document_count: int, document_frequency: int) -> int:
    return round((math.log((document_count + 1) / (document_frequency + 1)) + 1) * MICRO_IDF)


def ranked_channel(scores: dict[str, tuple[int, ...]]) -> list[tuple[tuple[int, ...], str]]:
    return sorted(((score, source) for source, score in scores.items()), key=lambda item: tuple(-value for value in item[0]) + (item[1],))


def positive(score: tuple[int, ...]) -> bool:
    return any(value > 0 for value in score)


def take_unused(ranking: list[tuple[tuple[int, ...], str]], taken: set[str]) -> dict[str, Any] | None:
    for rank_position, (score, source) in enumerate(ranking, start=1):
        if source not in taken:
            return {
                "canonical_source_sha256": source,
                "rank_position": rank_position,
                "score": list(score),
                "zero_score_coverage_fallback": not positive(score),
            }
    return None


def anchor_gate_score(shared_anchors: set[str], *, operation_terms: set[str], exclusive_artifact_terms: set[str], artifact_terms_before_exclusion: set[str], classes_by_term: dict[str, set[str]], idf: dict[str, int]) -> tuple[int, ...]:
    shared_operations = shared_anchors & operation_terms
    shared_artifacts = shared_anchors & exclusive_artifact_terms
    if not shared_operations or not shared_artifacts:
        return (0, 0, 0)
    classes = {class_name for term in shared_anchors for class_name in classes_by_term.get(term, set())}
    return (len(classes), sum(idf.get(term, MICRO_IDF) for term in shared_anchors), len(shared_anchors))


def cluster_id(row: dict[str, Any]) -> str:
    value = row.get("audit_cluster_id", row.get("cluster_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit("NC cluster without a stable identifier")
    return value


def prompt_id(row: dict[str, Any]) -> str:
    value = row.get("audit_prompt_id", row.get("prompt_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit("Prompt without a stable identifier")
    return value


def prompt_cluster_id(row: dict[str, Any]) -> str:
    value = row.get("audit_cluster_id", row.get("cluster_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit("NC prompt without a stable cluster identifier")
    return value


def source_role(union_row: dict[str, Any]) -> str:
    historical = union_row.get("historical_base_candidate")
    if isinstance(historical, dict) and isinstance(historical.get("final_intake_role"), str):
        return historical["final_intake_role"]
    return "RQ2B_NC_SOURCE_NATIVE_CANDIDATE"


def opaque_token(prompt_sha256: str, source: str) -> str:
    return "C-" + hashlib.sha256(f"{TOKEN_SALT}\0{prompt_sha256}\0{source}".encode("utf-8")).hexdigest()[:16].upper()


def packet_id(kind: str, prompt_sha256: str, ordinal: int = 0) -> str:
    return "P-" + hashlib.sha256(f"rq2b-nc-phase4-packet-v1\0{kind}\0{prompt_sha256}\0{ordinal}".encode("utf-8")).hexdigest()[:18].upper()


def source_text(path_row: dict[str, Any], source: str, cache: dict[str, str]) -> str:
    if source not in cache:
        stored = path_row["selected_workspace_relative_path"]
        path = WORKSPACE / stored
        if not path.is_file() or sha(path) != source:
            raise SystemExit(f"Source packet byte replay drift: {source}")
        cache[source] = path.read_text(encoding="utf-8-sig")
    return cache[source]


def parser_regression_checks() -> None:
    ranking = ranked_channel({"b": (2, 1), "a": (2, 1), "c": (0, 0)})
    assert ranking == [((2, 1), "a"), ((2, 1), "b"), ((0, 0), "c")]
    assert take_unused(ranking, {"a", "b"}) == {"canonical_source_sha256": "c", "rank_position": 3, "score": [0, 0], "zero_score_coverage_fallback": True}
    assert opaque_token("a" * 64, "b" * 64) == opaque_token("a" * 64, "b" * 64)
    assert opaque_token("a" * 64, "b" * 64) != opaque_token("a" * 64, "c" * 64)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite audit input: {out}")
    parser_regression_checks()

    inputs = {
        "controlling_sop": SOP,
        "base_navigation_fields": BASE_NAVIGATION_PROTOCOL,
        "user_approved_amendment": AMENDMENT,
        "phase3_summary": PHASE3 / "summary.json",
        "candidate_source_union": PHASE3 / "candidate_source_union_for_phase4.jsonl",
        "parent_prompts": PHASE3 / "parent_prompt_manifest_for_phase5.jsonl",
        "nc_clusters": PHASE3 / "nc_cluster_manifest_for_phase4.jsonl",
        "nc_prompts": PHASE3 / "nc_prompt_manifest_for_phase4.jsonl",
        "parent_v3_identities": PARENT_IDENTITIES,
        "navigation_profiles": PROFILES / "navigation_profiles.jsonl",
        "source_path_resolution_ledger": PROFILES / "source_path_resolution_ledger.jsonl",
        "navigation_profile_summary": PROFILES / "summary.json",
    }
    for path in inputs.values():
        if not path.is_file():
            raise SystemExit(f"Missing audit-input dependency: {path}")
    amendment = json.loads(AMENDMENT.read_text(encoding="utf-8"))
    if amendment.get("status") != EXPECTED_AMENDMENT_STATUS:
        raise SystemExit("Phase-4 amendment status drift")
    if amendment.get("main_pool_rule", {}).get("all_prompts_exactly_six_source_unique_candidates") is not True:
        raise SystemExit("Amendment does not bind exact K=6")
    phase3_summary = json.loads(inputs["phase3_summary"].read_text(encoding="utf-8"))
    if phase3_summary.get("status") != "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE":
        raise SystemExit("Phase-3 closure state drift")
    profile_summary = json.loads(inputs["navigation_profile_summary"].read_text(encoding="utf-8"))
    if profile_summary.get("status") != "PASS_SOURCE_NATIVE_NAVIGATION_PROFILE_MATERIALISATION_OUTCOME_BLIND_ONLY":
        raise SystemExit("Navigation-profile state drift")

    base = json.loads(BASE_NAVIGATION_PROTOCOL.read_text(encoding="utf-8"))
    token_re = re.compile(base["normaliser"]["token_pattern"])
    stopwords = set(base["normaliser"]["stopwords"])
    if set(base["provider_product_tokens_excluded_from_relevance_text"]) != {"anthropic", "chatgpt", "claude", "codex", "gemini", "openai"}:
        raise SystemExit("Provider-token exclusion configuration drift")
    classes_by_term: dict[str, set[str]] = defaultdict(set)
    for class_name, terms in base["anchor_classes"].items():
        for term in terms:
            classes_by_term[term].add(class_name)
    all_anchor_terms = set(classes_by_term)
    operation_terms = set(base["anchor_classes"]["operation"])
    a_config = base["channels"]["A_ARTIFACT_PROCESS_ANCHORS"]
    artifact_terms_before_exclusion = {term for class_name in a_config["exclusive_artifact_classes"] for term in base["anchor_classes"][class_name]}
    exclusive_artifact_terms = artifact_terms_before_exclusion - operation_terms - set(a_config["operation_family_excluded_from_artifact"])

    union = read_jsonl(inputs["candidate_source_union"])
    union_by_source = {row.get("canonical_source_sha256"): row for row in union}
    profiles = read_jsonl(inputs["navigation_profiles"])
    profile_by_source = {row.get("canonical_source_sha256"): row for row in profiles}
    paths = read_jsonl(inputs["source_path_resolution_ledger"])
    path_by_source = {row.get("canonical_source_sha256"): row for row in paths}
    if len(union) != len(union_by_source) or len(union_by_source) != 3813 or set(profile_by_source) != set(union_by_source) or set(path_by_source) != set(union_by_source):
        raise SystemExit("Frozen candidate/profile/path identity binding drift")
    parent_identity_rows = read_jsonl(inputs["parent_v3_identities"])
    parent_sources = {row.get("source_sha256") for row in parent_identity_rows}
    if len(parent_sources) != 2431 or not parent_sources.issubset(union_by_source):
        raise SystemExit("Parent V3 identity binding drift")
    parent_delta = sorted(set(union_by_source) - parent_sources)
    if len(parent_delta) != 1382:
        raise SystemExit("Parent delta source count drift")
    parent_prompts = read_jsonl(inputs["parent_prompts"])
    nc_clusters = read_jsonl(inputs["nc_clusters"])
    nc_prompts = read_jsonl(inputs["nc_prompts"])
    cluster_by_id = {cluster_id(row): row for row in nc_clusters}
    if len(parent_prompts) != 381 or len({prompt_id(row) for row in parent_prompts}) != 381 or len(cluster_by_id) != 49 or len(nc_prompts) != 147 or len({prompt_id(row) for row in nc_prompts}) != 147:
        raise SystemExit("Prompt/cluster cardinality drift")

    source_terms: dict[str, dict[str, Any]] = {}
    for source, profile in profile_by_source.items():
        name_u, name_b = make_terms(str(profile["relevance_source_name"]), token_re, stopwords)
        desc_u, desc_b = make_terms(str(profile["relevance_source_description"]), token_re, stopwords)
        head_u, head_b = make_terms(str(profile["relevance_heading_profile"]), token_re, stopwords)
        n_weight: dict[str, int] = {}
        for term in desc_u:
            n_weight[term] = max(n_weight.get(term, 0), 1)
        for term in name_u:
            n_weight[term] = max(n_weight.get(term, 0), 2)
        for term in desc_b:
            n_weight[term] = max(n_weight.get(term, 0), 2)
        for term in name_b:
            n_weight[term] = max(n_weight.get(term, 0), 4)
        source_terms[source] = {"name_u": name_u, "desc_u": desc_u, "head_u": head_u, "head_b": head_b, "n_weight": n_weight, "all": name_u | name_b | desc_u | desc_b | head_u | head_b}

    lane_specs: list[dict[str, Any]] = []
    for row in parent_prompts:
        prompt = row.get("prompt")
        if not isinstance(prompt, str):
            raise SystemExit("Parent prompt text missing")
        lane_specs.append({"lane_id": "A_PARENT_DELTA", "prompt_id": prompt_id(row), "prompt": prompt, "prompt_sha256": text_sha(prompt), "reporting_stratum": row.get("stratum", "UNSPECIFIED"), "reporting_group": row.get("group", "UNSPECIFIED"), "candidate_hashes": parent_delta, "local_roster": [], "main_slots": ["N_1", "N_2", "H_1", "H_2", "A_1", "A_2"]})
    for row in nc_prompts:
        prompt = row.get("prompt")
        cluster = cluster_by_id.get(prompt_cluster_id(row))
        if not isinstance(prompt, str) or cluster is None:
            raise SystemExit("NC prompt binding missing")
        local = sorted(cluster.get("candidate_source_sha256", []))
        if len(local) not in {2, 3} or len(local) != len(set(local)) or not set(local).issubset(union_by_source):
            raise SystemExit(f"NC local roster drift: {prompt_id(row)}")
        if len(local) == 3:
            slots, reporting_stratum = ["LOCAL_1", "LOCAL_2", "LOCAL_3", "N_EXTERNAL", "H_EXTERNAL", "A_EXTERNAL"], "source_native_three_member"
        else:
            slots, reporting_stratum = ["LOCAL_1", "LOCAL_2", "N_EXTERNAL_1", "N_EXTERNAL_2", "H_EXTERNAL", "A_EXTERNAL"], "legacy_2member_checkpoint"
        lane_specs.append({"lane_id": "B_NC_FULL_UNION", "prompt_id": prompt_id(row), "prompt": prompt, "prompt_sha256": text_sha(prompt), "reporting_stratum": reporting_stratum, "reporting_group": prompt_cluster_id(row), "candidate_hashes": sorted(union_by_source), "local_roster": local, "main_slots": slots})
    if len(lane_specs) != 528:
        raise SystemExit("Audit prompt population drift")

    # N/H/A navigation scores are generated from only prompt text and the three
    # relevance-safe source fields.  Origin data is consulted later solely for
    # deterministic tail coverage, never for score computation.
    idf_by_lane: dict[str, dict[str, int]] = {}
    for lane_id, candidates in (("A_PARENT_DELTA", parent_delta), ("B_NC_FULL_UNION", sorted(union_by_source))):
        df: Counter[str] = Counter()
        for source in candidates:
            df.update(source_terms[source]["all"])
        idf_by_lane[lane_id] = {term: integer_idf(len(candidates), frequency) for term, frequency in df.items()}

    queue_rows: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    token_rows: list[dict[str, Any]] = []
    main_packets: list[dict[str, Any]] = []
    tail_packets: list[dict[str, Any]] = []
    source_cache: dict[str, str] = {}
    lane_pair_counts: Counter[str] = Counter()
    zero_fallback_count = 0
    tail_counts: Counter[str] = Counter()
    role_order = ["RQ2B_NC_SOURCE_NATIVE_CANDIDATE", "RQ2B_NC_REVIEWED_SOURCE_CANDIDATE", "RQ2B_NC_RQ1_REVIEWED_NEW_SOURCE_CANDIDATE", "RQ1_NEW_PUBLIC_SOURCE_CANDIDATE", "PARENT_V3_CANONICAL_SOURCE"]

    for spec in sorted(lane_specs, key=lambda item: (item["lane_id"], item["prompt_id"])):
        candidates = spec["candidate_hashes"]
        local_roster = spec["local_roster"]
        query_u, query_b = make_terms(spec["prompt"], token_re, stopwords)
        query_all = query_u | query_b
        idf = idf_by_lane[spec["lane_id"]]
        n_scores: dict[str, tuple[int, ...]] = {}
        h_scores: dict[str, tuple[int, ...]] = {}
        a_scores: dict[str, tuple[int, ...]] = {}
        for source in candidates:
            terms = source_terms[source]
            shared_n = query_all & set(terms["n_weight"])
            n_scores[source] = (sum(idf.get(term, MICRO_IDF) * terms["n_weight"][term] for term in shared_n), len(shared_n))
            shared_h_b = query_b & terms["head_b"]
            shared_h_u = query_u & terms["head_u"]
            shared_h = shared_h_b if shared_h_b else shared_h_u
            h_scores[source] = (2 if shared_h_b else (1 if shared_h_u else 0), max((idf.get(term, MICRO_IDF) for term in shared_h), default=0), sum(idf.get(term, MICRO_IDF) for term in shared_h), len(shared_h))
            shared_anchors = query_all & terms["all"] & all_anchor_terms
            a_scores[source] = anchor_gate_score(shared_anchors, operation_terms=operation_terms, exclusive_artifact_terms=exclusive_artifact_terms, artifact_terms_before_exclusion=artifact_terms_before_exclusion, classes_by_term=classes_by_term, idf=idf)
        rankings = {"N": ranked_channel(n_scores), "H": ranked_channel(h_scores), "A": ranked_channel(a_scores)}

        main: list[dict[str, Any]] = []
        taken: set[str] = set()
        for index, source in enumerate(local_roster, start=1):
            taken.add(source)
            main.append({"slot": f"LOCAL_{index}", "canonical_source_sha256": source, "selection_channel": "LOCAL_FROZEN_ROSTER", "rank_position": None, "score": None, "zero_score_coverage_fallback": False})
        for slot in spec["main_slots"][len(local_roster) :]:
            channel = "N" if slot.startswith("N_") else ("H" if slot.startswith("H_") else "A")
            chosen = take_unused(rankings[channel], taken)
            if chosen is None:
                raise SystemExit(f"K=6 allocation cannot fill {spec['prompt_id']}/{slot}")
            taken.add(chosen["canonical_source_sha256"])
            main.append({"slot": slot, "selection_channel": channel, **chosen})
            zero_fallback_count += int(chosen["zero_score_coverage_fallback"])
        if len(main) != 6 or len({item["canonical_source_sha256"] for item in main}) != 6 or [item["slot"] for item in main] != spec["main_slots"]:
            raise SystemExit(f"Exact K=6 allocation invariant failed: {spec['prompt_id']}")

        tails: list[dict[str, Any]] = []
        phrase = next(({"tail_kind": "PHRASE_H_POSITIVE", "selection_channel": "H", "canonical_source_sha256": source, "rank_position": rank, "score": list(score), "zero_score_coverage_fallback": False} for rank, (score, source) in enumerate(rankings["H"], start=1) if positive(score) and source not in taken), None)
        if phrase is not None:
            tails.append(phrase)
            taken.add(phrase["canonical_source_sha256"])
            tail_counts["phrase"] += 1
        residual = [source for source in candidates if source not in taken]
        if residual:
            represented = {source_role(union_by_source[item["canonical_source_sha256"]]) for item in main}
            pool: list[str] = []
            for role in role_order:
                if role not in represented:
                    pool = [source for source in residual if source_role(union_by_source[source]) == role]
                    if pool:
                        break
            pool = pool or residual
            source = min(pool, key=lambda value: hashlib.sha256(f"{spec['prompt_sha256']}:{value}".encode("utf-8")).hexdigest())
            tails.append({"tail_kind": "RESIDUAL_ROLE_BALANCED", "selection_channel": "RESIDUAL", "canonical_source_sha256": source, "rank_position": None, "score": None, "zero_score_coverage_fallback": False})
            tail_counts["residual"] += 1
        if len(tails) > 2 or {item["canonical_source_sha256"] for item in tails} & {item["canonical_source_sha256"] for item in main} or len({item["canonical_source_sha256"] for item in tails}) != len(tails):
            raise SystemExit(f"Tail disjointness invariant failed: {spec['prompt_id']}")

        all_selected = main + tails
        tokens = {item["canonical_source_sha256"]: opaque_token(spec["prompt_sha256"], item["canonical_source_sha256"]) for item in all_selected}
        if len(tokens) != len(all_selected) or len(set(tokens.values())) != len(tokens):
            raise SystemExit(f"Opaque-token collision: {spec['prompt_id']}")
        main_packet_candidates = []
        for item in main:
            source = item["canonical_source_sha256"]
            token = tokens[source]
            main_packet_candidates.append({"candidate_token": token, "source_full_skill": source_text(path_by_source[source], source, source_cache)})
            pair_rows.append({"lane_id": spec["lane_id"], "prompt_id": spec["prompt_id"], "prompt_sha256": spec["prompt_sha256"], "candidate_token": token, "canonical_source_sha256": source, "packet_kind": "K6_MAIN", "allocation_slot": item["slot"], "selection_channel": item["selection_channel"], "rank_position": item["rank_position"], "channel_score": item["score"], "zero_score_coverage_fallback": item["zero_score_coverage_fallback"], "review_status": "PENDING_TWO_INDEPENDENT_TARGET_BLIND_REVIEWS"})
            token_rows.append({"packet_kind": "K6_MAIN", "packet_id": packet_id("K6_MAIN", spec["prompt_sha256"]), "prompt_id": spec["prompt_id"], "candidate_token": token, "canonical_source_sha256": source, "join_status": "SEALED_UNTIL_BLIND_RETURNS_CLOSE"})
        # The allocation ledger is sealed separately.  Reviewers receive the
        # same six candidates in token order, which is independent of N/H/A
        # rank, local-roster position and main-slot allocation.
        main_packet_candidates.sort(key=lambda item: item["candidate_token"])
        main_packets.append({"packet_id": packet_id("K6_MAIN", spec["prompt_sha256"]), "packet_kind": "K6_MAIN", "prompt": spec["prompt"], "prompt_sha256": spec["prompt_sha256"], "candidates": main_packet_candidates, "review_instruction": "Judge each source-visible candidate against the prompt using the frozen adequacy rubric. Candidate-token order is opaque and carries no target, rank or suitability information. Report FULLY_ACCEPTABLE, PARTIALLY_ADEQUATE, INADEQUATE or UNCLEAR with source-grounded rationale."})
        for ordinal, item in enumerate(tails, start=1):
            source = item["canonical_source_sha256"]
            token = tokens[source]
            tail_id = packet_id("TAIL", spec["prompt_sha256"], ordinal)
            tail_packets.append({"packet_id": tail_id, "packet_kind": "TAIL_CHALLENGE", "prompt": spec["prompt"], "prompt_sha256": spec["prompt_sha256"], "candidates": [{"candidate_token": token, "source_full_skill": source_text(path_by_source[source], source, source_cache)}], "review_instruction": "Judge this source-visible candidate against the prompt using the frozen adequacy rubric. Report FULLY_ACCEPTABLE, PARTIALLY_ADEQUATE, INADEQUATE or UNCLEAR with source-grounded rationale."})
            pair_rows.append({"lane_id": spec["lane_id"], "prompt_id": spec["prompt_id"], "prompt_sha256": spec["prompt_sha256"], "candidate_token": token, "canonical_source_sha256": source, "packet_kind": "TAIL_CHALLENGE", "tail_kind": item["tail_kind"], "selection_channel": item["selection_channel"], "rank_position": item["rank_position"], "channel_score": item["score"], "zero_score_coverage_fallback": False, "review_status": "PENDING_TWO_INDEPENDENT_TARGET_BLIND_REVIEWS"})
            token_rows.append({"packet_kind": "TAIL_CHALLENGE", "packet_id": tail_id, "prompt_id": spec["prompt_id"], "candidate_token": token, "canonical_source_sha256": source, "join_status": "SEALED_UNTIL_BLIND_RETURNS_CLOSE"})
        lane_pair_counts[spec["lane_id"]] += len(all_selected)
        queue_rows.append({"lane_id": spec["lane_id"], "prompt_id": spec["prompt_id"], "prompt": spec["prompt"], "prompt_sha256": spec["prompt_sha256"], "reporting_stratum": spec["reporting_stratum"], "reporting_group": spec["reporting_group"], "candidate_universe_count": len(candidates), "main_pool_exact_k": 6, "main_allocation": main, "tail_allocation": tails, "status": "OUTCOME_BLIND_K6_AUDIT_INPUT_PENDING_TARGET_BLIND_REVIEW"})

    queue_rows.sort(key=lambda row: (row["lane_id"], row["prompt_id"]))
    pair_rows.sort(key=lambda row: (row["lane_id"], row["prompt_id"], row["packet_kind"], row["candidate_token"]))
    token_rows.sort(key=lambda row: (row["packet_id"], row["candidate_token"]))
    main_packets.sort(key=lambda row: row["packet_id"])
    tail_packets.sort(key=lambda row: row["packet_id"])
    all_packet_ids = [row["packet_id"] for row in main_packets] + [row["packet_id"] for row in tail_packets]
    if len(queue_rows) != 528 or len(main_packets) != 528 or sum(len(row["main_allocation"]) for row in queue_rows) != 3168 or len({(row["prompt_id"], row["canonical_source_sha256"]) for row in pair_rows}) != len(pair_rows) or len(all_packet_ids) != len(set(all_packet_ids)) or len({(row["packet_id"], row["candidate_token"]) for row in token_rows}) != len(token_rows):
        raise SystemExit("K=6 queue cardinality or pair uniqueness invariant failed")

    proposal_config = {
        "config_version": "rq2b_nc_phase4_option1_k6_proposal_v1",
        "inherited_base_navigation_fields": {"path": str(BASE_NAVIGATION_PROTOCOL.relative_to(WORKSPACE)), "sha256": sha(BASE_NAVIGATION_PROTOCOL), "subtrees": ["normaliser", "channels.N_NAME_DESCRIPTION", "channels.H_HEADINGS", "channels.A_ARTIFACT_PROCESS_ANCHORS", "anchor_classes", "provider_product_tokens_excluded_from_relevance_text"]},
        "relevance_fields": ["prompt", "relevance_source_name", "relevance_source_description", "relevance_heading_profile"],
        "tie_break": "score_descending_then_canonical_source_sha256_ascending",
        "selection": amendment["main_pool_rule"],
        "tail_per_prompt_group": {"group_unit": "one_prompt_id", "phrase": "highest positive H-ranked candidate outside main pool", "residual": "first unrepresented reporting role in frozen order, then minimum SHA256(prompt_sha256:candidate_sha256)", "maximum": 2, "positive_tail_response": "METHOD_GATE_OPEN"},
        "opaque_tokens": {"algorithm": "SHA256(TOKEN_SALT + NUL + prompt_sha256 + NUL + canonical_source_sha256) truncated to 16 uppercase hexadecimal characters", "salt_identifier": TOKEN_SALT, "collision_policy": "FAIL_CLOSED", "reviewer_visible_main_candidate_order": "candidate_token_ascending"},
    }
    summary = {
        "status": "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS",
        "claim_boundary": "This is a frozen prospective audit input, not an acceptable-set result, a retrieval metric, a reranking result, or a final benchmark.",
        "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in inputs.values()},
        "implementation": {"path": str(Path(__file__).relative_to(WORKSPACE)), "sha256": sha(Path(__file__).resolve()), "python": sys.version},
        "counts": {"prompt_queues": len(queue_rows), "main_review_packets": len(main_packets), "main_pool_pairs_exact_k6": sum(len(row["main_allocation"]) for row in queue_rows), "tail_review_packets": len(tail_packets), "source_visible_review_pairs": len(pair_rows), "pairs_by_lane": dict(sorted(lane_pair_counts.items())), "pairs_by_reporting_stratum": dict(sorted(Counter(row["reporting_stratum"] for row in queue_rows).items())), "zero_score_coverage_fallback_main_slots": zero_fallback_count, "tails": dict(sorted(tail_counts.items()))},
        "outputs": {},
        "outcome_blind_firewall": {"fields_read_for_scores": proposal_config["relevance_fields"], "fields_not_read_for_scores": ["historical_gold", "target", "local_label", "acceptable_set", "origin", "repository", "provider", "path", "licence", "retrieval", "reranking", "provider_output", "metric"], "reviewer_packets_exclude": ["lane_id", "reporting_stratum", "reporting_group", "allocation_slot", "selection_channel", "rank_position", "channel_score", "canonical_source_sha256", "target", "label"]},
    }
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    output_rows = {"prompt_k6_allocation_ledger.jsonl": queue_rows, "source_visible_review_pairs.jsonl": pair_rows, "opaque_token_join.jsonl": token_rows, "main_blind_review_packets.jsonl": main_packets, "tail_blind_review_packets.jsonl": tail_packets}
    for name, rows in output_rows.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "candidate_proposal_config.json").write_text(json.dumps(proposal_config, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary["outputs"]["candidate_proposal_config.json"] = sha(out / "candidate_proposal_config.json")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"counts": summary["counts"], "output_dir": str(out), "status": summary["status"]}, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
