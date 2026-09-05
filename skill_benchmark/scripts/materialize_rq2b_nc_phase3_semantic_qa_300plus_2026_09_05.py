#!/usr/bin/env python3
"""Prepare a fail-closed, outcome-blind Phase-3 semantic-QA review package.

This is a *screen and packet materialiser*, never a semantic decision engine:
lexical signals only nominate records for independent review.  It deliberately
does not use embeddings, retrieval, rankings, or historical result values.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
PHASE3 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
V3 = BENCHMARK / "rq2b_full_library/rq2b-i3c-v3-2026-08-18"
OVERLAY = BENCHMARK / "rq2b_naturalistic_confusability/manifests/description_remediation_wave_001_pre_freeze_2026-08-31"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_semantic_qa_300plus_2026-09-05_v2"

WORD = re.compile(r"[a-z0-9]+")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def bind(bound: dict[str, str], path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing required bound input: {path}")
    bound[str(path.relative_to(WORKSPACE))] = digest(path)


def normal(text: str) -> str:
    return " ".join(WORD.findall(text.lower()))


def tokens(text: str) -> list[str]:
    return WORD.findall(text.lower())


def prompt_id(row: dict[str, Any]) -> str:
    value = row.get("audit_prompt_id", row.get("prompt_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit(f"Prompt has no stable identifier: {row}")
    return value


def source_paths(candidate: dict[str, Any]) -> list[str]:
    found: set[str] = set()
    base = candidate.get("historical_base_candidate")
    if isinstance(base, dict):
        if isinstance(base.get("source_path"), str):
            found.add(base["source_path"])
        provenance = base.get("provenance_binding")
        if isinstance(provenance, dict) and isinstance(provenance.get("source_path"), str):
            found.add(provenance["source_path"])
        for key in ("rq1_records", "v3_identity_records"):
            values = base.get(key)
            if isinstance(values, list):
                for value in values:
                    if isinstance(value, dict) and isinstance(value.get("source_path"), str):
                        found.add(value["source_path"])
    origins = candidate.get("local_nc_origin_records")
    if isinstance(origins, list):
        for origin in origins:
            if isinstance(origin, dict) and isinstance(origin.get("source_paths"), list):
                found.update(value for value in origin["source_paths"] if isinstance(value, str))
            provenance = origin.get("provenance_record") if isinstance(origin, dict) else None
            if isinstance(provenance, dict) and isinstance(provenance.get("source_paths"), list):
                found.update(value for value in provenance["source_paths"] if isinstance(value, str))
    if not found:
        raise SystemExit(f"Candidate lacks a source path: {candidate.get('canonical_source_sha256')}")
    return sorted(found)


def resolve_and_replay(source_hash: str, paths: list[str]) -> tuple[Path, str]:
    matches: list[Path] = []
    for stored in paths:
        choices = [WORKSPACE / stored]
        if not stored.startswith("skill_benchmark/"):
            choices.append(BENCHMARK / stored)
        matches.extend(path for path in choices if path.is_file() and digest(path) == source_hash)
    if not matches:
        raise SystemExit(f"Source byte replay failed for {source_hash}")
    path = sorted(set(matches))[0]
    return path, path.read_text(encoding="utf-8", errors="replace")


def frontmatter_value(text: str, key: str) -> str:
    header = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else text[:1600]
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)", header)
    return match.group(1).strip().strip("\"'") if match else ""


def source_profile(candidate: dict[str, Any]) -> dict[str, Any]:
    source_hash = str(candidate["canonical_source_sha256"])
    path, text = resolve_and_replay(source_hash, source_paths(candidate))
    title = frontmatter_value(text, "name")
    if not title:
        heading = re.search(r"(?m)^#\s+(.+)$", text)
        title = heading.group(1).strip() if heading else ""
    description = frontmatter_value(text, "description")
    return {
        "canonical_source_sha256": source_hash,
        "source_path": str(path.relative_to(WORKSPACE)),
        "complete_original_skill": text,
        "source_title": title,
        "source_title_normalised": normal(title),
        "source_description": description,
        "normalised_source_sha256": hashlib.sha256(normal(text).encode("utf-8")).hexdigest(),
    }


def target_hash(row: dict[str, Any], parent_gold: dict[str, str]) -> str | None:
    for key in (
        "intended_target_source_sha256",
        "reviewed_single_fully_adequate_source_sha256",
        "cluster_local_most_suitable_source_sha256",
    ):
        if isinstance(row.get(key), str):
            return row[key]
    gold = row.get("gold_skill")
    return parent_gold.get(gold) if isinstance(gold, str) else None


STOPWORDS = frozenset("a an and are as at be by for from has have in into is it its of on or that the their this to with your you".split())


def prompt_pairs(rows: list[dict[str, Any]]) -> list[tuple[int, int, float, float, float]]:
    """Pinned high-specificity lexical candidate screen, never a semantic verdict."""
    profiles: list[tuple[str, set[str], set[tuple[str, ...]]]] = []
    for row in rows:
        raw = normal(str(row["prompt"]))
        words = [word for word in tokens(raw) if word not in STOPWORDS]
        grams = {tuple(words[index:index + 4]) for index in range(max(0, len(words) - 3))}
        profiles.append((raw, set(words), grams))
    output: list[tuple[int, int, float, float, float]] = []
    for left, right in itertools.combinations(range(len(rows)), 2):
        text_a, words_a, grams_a = profiles[left]
        text_b, words_b, grams_b = profiles[right]
        if text_a == text_b or text_a in text_b or text_b in text_a:
            output.append((left, right, 1.0, 1.0, 1.0))
            continue
        jaccard = len(words_a & words_b) / len(words_a | words_b) if words_a | words_b else 0.0
        coverage = len(grams_a & grams_b) / min(len(grams_a), len(grams_b)) if grams_a and grams_b else 0.0
        # Sequence matching is quadratic-ish; a high sequence score necessarily
        # has strong content-token or four-gram overlap under this tokenizer.
        if jaccard < 0.52 and coverage < 0.50:
            continue
        sequence = difflib.SequenceMatcher(None, text_a, text_b, autojunk=False).ratio()
        if (jaccard >= 0.52 and sequence >= 0.66) or coverage >= 0.50 or sequence >= 0.84:
            output.append((left, right, round(jaccard, 6), round(sequence, 6), round(coverage, 6)))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite Phase-3 semantic-QA package: {out}")

    bound: dict[str, str] = {}
    inputs = [
        SOP,
        PHASE3 / "summary.json", PHASE3 / "candidate_source_union.jsonl", PHASE3 / "nc_cluster_manifest.jsonl",
        PHASE3 / "parent_prompt_manifest.jsonl", PHASE3 / "nc_prompt_manifest.jsonl",
        PHASE3 / "local_source_provenance_ledger.jsonl", PHASE3 / "historical_base_local_source_overlap.jsonl",
        PHASE3 / "checkpoint_local_cross_cluster_source_reuse.jsonl", PHASE3 / "exact_duplicate_prompt_text_groups.jsonl",
        V3 / "i3c_extraction/identity_manifest.jsonl", V3 / "b1l_preflight_v3/strict_scored_prompts.jsonl",
        V3 / "b1l_preflight_v3/b1l_local_bm25_run/b1l_strict_results.jsonl",
        OVERLAY / "description_overlay.jsonl", OVERLAY / "root_admission_decision.json",
    ]
    for path in inputs:
        bind(bound, path)

    candidates = read_jsonl(PHASE3 / "candidate_source_union.jsonl")
    parent = read_jsonl(PHASE3 / "parent_prompt_manifest.jsonl")
    nc = read_jsonl(PHASE3 / "nc_prompt_manifest.jsonl")
    clusters = read_jsonl(PHASE3 / "nc_cluster_manifest.jsonl")
    reuse = read_jsonl(PHASE3 / "checkpoint_local_cross_cluster_source_reuse.jsonl")
    exact_prompts = read_jsonl(PHASE3 / "exact_duplicate_prompt_text_groups.jsonl")
    identities = read_jsonl(V3 / "i3c_extraction/identity_manifest.jsonl")
    overlays = read_jsonl(OVERLAY / "description_overlay.jsonl")
    admission = json.loads((OVERLAY / "root_admission_decision.json").read_text(encoding="utf-8"))
    if (len(candidates), len(parent), len(nc), len(clusters), len(reuse), len(exact_prompts)) != (3810, 381, 875, 304, 8, 0):
        raise SystemExit("Phase-3 v2 input cardinality drift")
    if len({str(row["canonical_source_sha256"]) for row in candidates}) != 3810:
        raise SystemExit("Candidate source union is not exact-SHA unique")
    profiles = {str(row["canonical_source_sha256"]): source_profile(row) for row in candidates}
    parent_gold = {str(row["skill_id"]): str(row["source_sha256"]) for row in identities}
    all_prompts = [{"prompt_origin": "PARENT_V3", **row} for row in parent] + nc
    if len({prompt_id(row) for row in all_prompts}) != 1256:
        raise SystemExit("Prompt identifiers are not globally unique")

    cluster_sources: dict[str, list[str]] = {}
    for row in clusters:
        cluster_id = row.get("audit_cluster_id", row.get("cluster_id"))
        hashes = row.get("candidate_source_sha256")
        local = row.get("cluster_origin") == "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE_UNADMITTED"
        valid_size = len(hashes) == 3 if isinstance(hashes, list) and local else len(hashes) in {2, 3} if isinstance(hashes, list) else False
        if not isinstance(cluster_id, str) or not valid_size:
            raise SystemExit(f"Malformed NC cluster manifest row: {row}")
        cluster_sources[cluster_id] = sorted(str(value) for value in hashes)
    local_lookup = {
        (str(row.get("discovery_batch")), str(row.get("family_token"))): str(row["audit_cluster_id"])
        for row in clusters if row.get("cluster_origin") == "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE_UNADMITTED"
    }

    source_screen: list[dict[str, Any]] = []
    source_packets: list[dict[str, Any]] = []
    for index, row in enumerate(sorted(reuse, key=lambda value: str(value["canonical_source_sha256"])), 1):
        source_hash = str(row["canonical_source_sha256"])
        local = row["local_occurrences"]
        local_ids = [local_lookup.get((str(item["discovery_batch"]), str(item["family_token"]))) for item in local]
        if any(value is None for value in local_ids):
            raise SystemExit(f"Cross-reuse local cluster join failed: {row}")
        checkpoint_ids = [str(value) for value in row["checkpoint_cluster_ids"]]
        packet_id = f"SRCREL-{index:03d}"
        screen = {
            "screen_id": packet_id,
            "signal": "EXACT_SOURCE_SHA256_CROSS_CLUSTER_REUSE",
            "canonical_source_sha256": source_hash,
            "checkpoint_cluster_ids": checkpoint_ids,
            "local_cluster_ids": local_ids,
            "mechanical_disposition": "REVIEW_REQUIRED_NOT_AN_ADMISSION_OR_EXCLUSION_DECISION",
        }
        source_screen.append(screen)
        involved = checkpoint_ids + [str(value) for value in local_ids]
        source_packets.append({
            "packet_id": packet_id,
            "review_boundary": "Compare cluster meanings and source independence only. Do not infer targets, labels, ranks, retrieval outcomes, or acceptable sets.",
            "cluster_tokens": [
                {
                    "cluster_token": f"C{position + 1}",
                    "members": [
                        {"candidate_token": f"S{member + 1}", "canonical_source_sha256": digest_value,
                         "complete_original_skill": profiles[digest_value]["complete_original_skill"]}
                        for member, digest_value in enumerate(cluster_sources[cluster_id])
                    ],
                }
                for position, cluster_id in enumerate(involved)
            ],
            "shared_source_occurs_in_cluster_tokens": list(range(1, len(involved) + 1)),
            "return_schema": {
                "packet_id": packet_id,
                "relation_decision": "DUPLICATE_CLUSTER | RELATED_BUT_DISTINCT | BLOCKED_OR_UNCLEAR",
                "source_anchors": [], "rationale": "", "triad_independence_preserved": None,
            },
        })

    normalised_groups: dict[str, list[str]] = defaultdict(list)
    for source_hash, profile in profiles.items():
        normalised_groups[str(profile["normalised_source_sha256"])].append(source_hash)
    for group in sorted(normalised_groups.values()):
        if len(group) > 1:
            source_screen.append({
                "screen_id": f"SRCNORM-{len(source_screen) + 1:04d}", "signal": "NORMALISED_FULL_SOURCE_MATCH",
                "source_hashes": group, "mechanical_disposition": "REVIEW_REQUIRED_NOT_AN_ADMISSION_OR_EXCLUSION_DECISION",
            })

    prompt_screen: list[dict[str, Any]] = []
    prompt_packets: list[dict[str, Any]] = []
    for index, (left, right, score, sequence, coverage) in enumerate(prompt_pairs(all_prompts), 1):
        a, b = all_prompts[left], all_prompts[right]
        packet_id = f"PRREL-{index:04d}"
        origin_a, origin_b = a.get("prompt_origin", "SOURCE_NATIVE_LOCAL_GATE"), b.get("prompt_origin", "SOURCE_NATIVE_LOCAL_GATE")
        cluster_a = a.get("audit_cluster_id", a.get("cluster_id"))
        cluster_b = b.get("audit_cluster_id", b.get("cluster_id"))
        relation_scope = (
            "PARENT_V3_INTERNAL_VALIDITY_AUDIT"
            if origin_a == origin_b == "PARENT_V3"
            else "NC_INTERNAL_SAME_CLUSTER_CONTEXT"
            if origin_a != "PARENT_V3" and origin_b != "PARENT_V3" and cluster_a == cluster_b
            else "CROSS_STRATUM_OR_CROSS_CLUSTER_SPLIT_AUDIT"
        )
        prompt_screen.append({
            "screen_id": packet_id, "prompt_ids": [prompt_id(a), prompt_id(b)],
            "origins": [origin_a, origin_b], "relation_scope": relation_scope,
            "content_token_jaccard": score, "character_sequence_ratio": sequence, "four_gram_coverage_shorter": coverage,
            "mechanical_disposition": "REVIEW_REQUIRED_NOT_A_SEMANTIC_DUPLICATE_DECISION",
        })
        sources = []
        for side, row in (("A", a), ("B", b)):
            selected = target_hash(row, parent_gold)
            if selected and selected in profiles:
                sources.append({"side": side, "source_token": f"{side}1", "complete_original_skill": profiles[selected]["complete_original_skill"]})
        prompt_packets.append({
            "packet_id": packet_id,
            "review_boundary": "Assess duplicate operational instance, transformed near-copy, split leakage, and cue risk only; do not make acceptable-set, target, rank, or retrieval decisions.",
            "prompt_a": str(a["prompt"]), "prompt_b": str(b["prompt"]), "associated_source_sets": sources,
            "return_schema": {"packet_id": packet_id, "relation_decision": "RELATED_BUT_DISTINCT | SPLIT_LEAKAGE | TRANSFORMED_DUPLICATE | UNCLEAR", "source_anchors": [], "rationale": ""},
        })

    # Cue inventory is target-bound.  Searching every source label against every
    # prompt overflags generic topical vocabulary and is not a valid hard gate.
    cue_inventory: list[dict[str, Any]] = []
    for row in all_prompts:
        body = normal(str(row["prompt"]))
        selected = target_hash(row, parent_gold)
        title = str(profiles[selected]["source_title_normalised"]) if selected in profiles else ""
        if len(tokens(title)) >= 2 and title in body:
            cue_inventory.append({"prompt_id": prompt_id(row), "signal": "TARGET_SOURCE_TITLE", "matched_text": title, "source_hashes": [selected], "mechanical_disposition": "REVIEW_REQUIRED"})
        source_id = row.get("gold_skill", row.get("reviewed_single_fully_adequate_candidate_id"))
        source_id_text = normal(str(source_id)) if isinstance(source_id, str) else ""
        if len(tokens(source_id_text)) >= 2 and source_id_text in body:
            cue_inventory.append({"prompt_id": prompt_id(row), "signal": "TARGET_SOURCE_ID", "matched_text": source_id_text, "source_hashes": [selected] if selected else [], "mechanical_disposition": "REVIEW_REQUIRED"})
        lower = str(row["prompt"]).lower()
        for signal, pattern in (("SOURCE_REPOSITORY_URL", r"github\\.com"), ("SOURCE_PATH_OR_BENCHMARK_SLUG", r"(?:rq2b|rq1b|/skills/|sha256)"), ("LITERAL_SHA256", r"\\b[a-f0-9]{64}\\b"), ("SKILL_FILE_ARTIFACT", r"skill\\.md")):
            if re.search(pattern, lower):
                cue_inventory.append({"prompt_id": prompt_id(row), "signal": signal, "matched_text": None, "source_hashes": [], "mechanical_disposition": "REVIEW_REQUIRED"})
    cue_inventory = sorted({json.dumps(row, sort_keys=True): row for row in cue_inventory}.values(), key=lambda row: (row["prompt_id"], row["signal"], str(row["matched_text"])))
    cue_packets = [{
        "packet_id": f"CUE-{index:04d}", "prompt": next(row["prompt"] for row in all_prompts if prompt_id(row) == finding["prompt_id"]),
        "mechanical_finding": finding,
        "review_boundary": "Decide only whether the finding is an avoidable identity cue or a source-anchored necessary task condition. Do not decide target adequacy, labels, rank, or retrieval.",
        "return_schema": {"packet_id": f"CUE-{index:04d}", "cue_decision": "AVOIDABLE_IDENTITY_CUE | DECLARED_NECESSARY_CUE_STRATUM | NOT_A_CUE | UNCLEAR", "source_anchors": [], "rationale": ""},
    } for index, finding in enumerate(cue_inventory, 1)]

    overlay_replay = []
    admitted = {str(row["canonical_source_sha256"]): row for row in admission.get("admitted_overlays", [])}
    for row in overlays:
        source_hash = str(row["canonical_source_sha256"])
        overlay_replay.append({
            "canonical_source_sha256": source_hash,
            "source_present_in_current_union": source_hash in profiles,
            "root_admission_matches": admitted.get(source_hash, {}).get("description") == row.get("final_library_description_overlay"),
            "scope": row.get("overlay_scope"),
            "disposition": "BOUND_FUTURE_ONLY_OVERLAY" if source_hash in profiles and admitted.get(source_hash) else "BLOCKED_OVERLAY_BINDING_DRIFT",
        })
    if len(overlay_replay) != 2 or any(row["disposition"] != "BOUND_FUTURE_ONLY_OVERLAY" for row in overlay_replay):
        raise SystemExit("Description-overlay replay drift")

    affected = [
        {"record_type": "CROSS_CLUSTER_SOURCE_REUSE", "record_id": row["screen_id"], "disposition": "BLOCKED_PENDING_INDEPENDENT_REVIEW"}
        for row in source_screen if row["signal"] == "EXACT_SOURCE_SHA256_CROSS_CLUSTER_REUSE"
    ] + [
        {"record_type": "PROMPT_RELATION_SCREEN", "record_id": row["screen_id"], "disposition": "PENDING_INDEPENDENT_REVIEW"}
        for row in prompt_screen
    ] + [
        {"record_type": "PROMPT_CUE_SCREEN", "record_id": packet["packet_id"], "disposition": "PENDING_INDEPENDENT_REVIEW"}
        for packet in cue_packets
    ]
    summary = {
        "status": "PENDING_INDEPENDENT_PHASE3_SEMANTIC_QA_REVIEW",
        "claim_boundary": "Mechanical lexical findings nominate records for review only. This package creates no semantic verdict, audit-input freeze, acceptable-set label, retrieval result, or metric.",
        "counts": {"candidates": 3810, "parent_prompts": 381, "nc_prompts": 875, "source_relation_review_packets": len(source_packets), "prompt_relation_review_packets": len(prompt_packets), "cue_review_packets": len(cue_packets), "blocked_cross_cluster_source_reuses": 8},
        "bound_inputs": bound,
        "outputs": {},
        "required_before_phase4": ["Seal two independent reviewer returns and coordinator resolutions for every nominated source, prompt-relation, cue, and split-leakage record.", "Exclude or repair affected records without changing source universe, family form, rubric, or acceptable-set definition; otherwise open the SOP method gate.", "Do not treat a negative mechanical screen as proof that no semantic near-copy exists."],
    }
    output_rows = {
        "source_relation_screen.jsonl": source_screen,
        "source_relation_reviewer_packet.jsonl": source_packets,
        "prompt_relation_screen.jsonl": prompt_screen,
        "prompt_relation_reviewer_packet.jsonl": prompt_packets,
        "prompt_cue_mechanical_inventory.jsonl": cue_inventory,
        "prompt_cue_reviewer_packet.jsonl": cue_packets,
        "split_leakage_ledger.jsonl": prompt_screen,
        "description_overlay_replay.jsonl": overlay_replay,
        "affected_record_dispositions.jsonl": affected,
    }
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    for name, rows in output_rows.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = digest(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
