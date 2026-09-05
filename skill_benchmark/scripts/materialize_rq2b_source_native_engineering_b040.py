#!/usr/bin/env python3
"""Materialise the bounded B040 engineering-only discovery packets.

This is a discovery-only replay over the frozen lexical reciprocal-triangle
index.  It deliberately does not read source bodies to decide family quality;
the only B040 selection filter is a documented developer-engineering category
intersection over literal native descriptions already in the frozen corpus.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
PROTOCOL = REVIEW / "SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS = NC / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
CORPUS_SUMMARY = CORPUS.parent / "summary.json"
HYPOTHESES = REVIEW / "source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl"
BOOTSTRAP_SUMMARY = HYPOTHESES.parent / "summary.json"
OUTPUT = REVIEW / "source_native_engineering_lexical_continuation_b040_2026-09-04"

# Matching is confined to the original native description (lower-cased only for
# deterministic matching).  A retained family needs a category shared by all
# three members; this makes B040 independent from general end-user and
# research/data-analysis families without using names, paths, source bodies or
# previous review outcomes to prioritise candidates.
CATEGORY_PATTERNS = {
    "source_control": (
        r"\bgit\b", r"\bgithub\b", r"\bgitlab\b", r"\bsource control\b",
        r"\bversion control\b", r"\bpull request\b", r"\bmerge request\b",
        r"\bcommit(?:s|ting)?\b", r"\bbranch(?:es|ing)?\b",
    ),
    "testing": (
        r"\btest(?:ing|s)?\b", r"\bunit test", r"\bintegration test",
        r"\be2e\b", r"\bend-to-end\b", r"\bqa\b", r"\bdebug(?:ging)?\b",
        r"\btest suite\b", r"\btest case\b", r"\bmutation testing\b",
    ),
    "ci_cd": (
        r"\bci/cd\b", r"\bcontinuous integration\b", r"\bcontinuous delivery\b",
        r"\bcontinuous deployment\b", r"\bbuild pipeline\b", r"\bgithub actions\b",
        r"\bgitlab ci\b", r"\bjenkins\b",
    ),
    "devops_cloud_infrastructure": (
        r"\bdevops\b", r"\binfrastructure\b", r"\bkubernetes\b", r"\bdocker\b",
        r"\bterraform\b", r"\bcloud deployment\b", r"\bcloud resource",
        r"\bcontainer(?:s|ized|isation|ization)?\b", r"\bhelm\b",
    ),
    "code_generation": (
        r"\bcode generation\b", r"\bgenerate code\b", r"\bscaffold(?:ing)?\b",
        r"\bboilerplate\b", r"\bcodegen\b", r"\bcreate (?:a |an )?(?:python|typescript|javascript|java|rust|go|swift|api)\b",
    ),
    "package_dependency_management": (
        r"\bpackage management\b", r"\bdependency(?:ies)?\b", r"\bnpm\b",
        r"\bpip\b", r"\bpnpm\b", r"\byarn\b", r"\bpoetry\b", r"\bcomposer\b",
        r"\bcargo\b", r"\bgradle\b", r"\bmaven\b",
    ),
    "developer_tooling": (
        r"\bcodebase\b", r"\bdeveloper tool", r"\bide\b", r"\bcommand line\b",
        r"\bcli\b", r"\blinter\b", r"\bstatic analysis\b", r"\bcode review\b",
        r"\bapi development\b", r"\bsoftware development\b",
    ),
}
COMPILED_PATTERNS = {category: tuple(re.compile(p, re.I) for p in patterns)
                     for category, patterns in CATEGORY_PATTERNS.items()}
ENGINEERING_CONTEXT = tuple(re.compile(p, re.I) for p in (
    r"\bcode\b", r"\bsoftware\b", r"\brepository\b", r"\brepo\b",
    r"\bapplication\b", r"\bapp\b", r"\bapi\b", r"\bdeveloper\b",
    r"\bcli\b", r"\bsource(?:\s+set)?\b", r"\bpython\b", r"\bjava\b",
    r"\bjavascript\b", r"\btypescript\b", r"\bandroid\b", r"\bweb\b",
    r"\bbrowser\b", r"\bgradle\b", r"\blibrary\b", r"\bpackage\b",
    r"\bcontainer\b", r"\bkubernetes\b", r"\binfrastructure\b",
))
# These are only scope-exclusion indicators.  They stop common lexical
# homonyms (for example marketing A/B tests, media pipelines and operations
# "packages") from entering a developer-engineering-only batch.
NON_ENGINEERING_SCOPE = tuple(re.compile(p, re.I) for p in (
    r"\bdashboard", r"\bvisuali[sz]ation", r"\bbusiness intelligence\b",
    r"\bcrm\b", r"\blead(?:s)?\b", r"\bprospect", r"\bmarketing\b",
    r"\bsales\b", r"\bcustomer\b", r"\bvideo\b", r"\baudio\b",
    r"\btravel\b", r"\bmeeting\b", r"\bevent planning\b", r"\bgrant\b",
    r"\bthesis\b", r"\bapp store\b", r"\bconversion\b", r"\bpricing\b",
    r"\bhuman resources\b", r"\bchief (?:human resources|financial|product) officer\b",
    r"\bmerchant(?:s)?\b", r"\bshopify\b", r"\bstart selling\b",
    r"\bfairlearn\b", r"\bmodel cards?\b", r"\bdrift monitoring\b",
))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def matching_categories(description: str) -> list[str]:
    if any(pattern.search(description) for pattern in NON_ENGINEERING_SCOPE):
        return []
    matched = [category for category, patterns in COMPILED_PATTERNS.items()
               if any(pattern.search(description) for pattern in patterns)]
    has_engineering_context = any(pattern.search(description) for pattern in ENGINEERING_CONTEXT)
    # Generic "testing" and "dependency" wording is accepted only where the
    # native text itself also establishes a technical/software context.
    return [category for category in matched
            if category not in {"testing", "package_dependency_management"} or has_engineering_context]


def prior_review_keys() -> dict[str, Path]:
    found: dict[str, Path] = {}
    pattern = re.compile(r"batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$")
    for path in REVIEW.glob("**/internal_reconciliation_key.jsonl"):
        match = pattern.search(str(path.relative_to(WORKSPACE)))
        if match and 1 <= int(match.group(1)) <= 38:
            found[f"B{int(match.group(1)):03d}"] = path
    expected = {f"B{i:03d}" for i in range(1, 39)}
    if set(found) != expected:
        missing = sorted(expected - set(found))
        extra = sorted(set(found) - expected)
        raise SystemExit(f"prior ledger mismatch; missing={missing}; extra={extra}")
    return dict(sorted(found.items()))


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"output already exists: {OUTPUT}")
    corpus_rows = read_jsonl(CORPUS)
    corpus_by_hash = {row["canonical_source_sha256"]: row for row in corpus_rows}
    if len(corpus_by_hash) != 23450:
        raise SystemExit("corpus source count mismatch")
    keys = prior_review_keys()
    prior_hashes: set[str] = set()
    for batch, path in keys.items():
        rows = read_jsonl(path)
        if len(rows) != 75:
            raise SystemExit(f"{batch} ledger does not contain 75 sources")
        prior_hashes.update(row["canonical_source_sha256"] for row in rows)
    if len(prior_hashes) != 2850:
        raise SystemExit(f"expected 2,850 distinct B001-B038 hashes; found {len(prior_hashes)}")

    hypotheses = read_jsonl(HYPOTHESES)
    hypotheses.sort(key=lambda row: (-row["reciprocal_link_count"], -row["rank_fusion_score"],
                                      row["member_source_sha256"]))
    selected: list[dict] = []
    used_hashes: set[str] = set()
    exclusion_counts: Counter[str] = Counter()
    for hypothesis in hypotheses:
        member_hashes = hypothesis["member_source_sha256"]
        if any(source_hash not in corpus_by_hash for source_hash in member_hashes):
            raise SystemExit(f"hypothesis member absent from corpus: {hypothesis['family_id']}")
        if set(member_hashes) & prior_hashes:
            exclusion_counts["prior_B001_B038_overlap"] += 1
            continue
        if set(member_hashes) & used_hashes:
            exclusion_counts["within_B040_source_collision"] += 1
            continue
        member_categories = [set(matching_categories(corpus_by_hash[source_hash]["native_description"]))
                             for source_hash in member_hashes]
        shared_categories = sorted(set.intersection(*member_categories))
        if not shared_categories:
            exclusion_counts["no_shared_developer_engineering_category"] += 1
            continue
        selected.append({
            **hypothesis,
            "batch_id": "SN-LEX-B040",
            "batch_rank": len(selected) + 1,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "selection_scope": "DEVELOPER_FACING_ENGINEERING_FAMILIES_ONLY",
            "source_native_category_intersection": shared_categories,
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "claim_boundary": "Fresh-source, developer-engineering lexical reading priority only; not a cluster result.",
        })
        used_hashes.update(member_hashes)
        if len(selected) == 25:
            break
    if len(selected) != 25 or len(used_hashes) != 75 or used_hashes & prior_hashes:
        raise SystemExit("B040 selection failure")

    OUTPUT.mkdir(parents=True)
    queue = OUTPUT / "batch_040_full_source_review_queue_internal.jsonl"
    queue.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in selected))

    # These packets preserve the complete original sources verbatim alongside
    # source-native text and the already-frozen neighbour evidence.  They are
    # explicitly UNREVIEWED and do not introduce a source card or summary.
    packets = OUTPUT / "batch_040_full_original_source_packets.jsonl"
    packet_rows: list[dict] = []
    for family in selected:
        members = []
        for source_hash, description_hash, source_paths in zip(
            family["member_source_sha256"], family["member_native_description_sha256"], family["member_source_paths"]):
            corpus = corpus_by_hash[source_hash]
            if corpus["native_description_sha256"] != description_hash:
                raise SystemExit(f"native-description hash mismatch: {source_hash}")
            preserved_paths = corpus["source_paths"]
            if source_paths != preserved_paths:
                raise SystemExit(f"source-path mismatch: {source_hash}")
            full_sources = []
            for relative_path in preserved_paths:
                absolute_path = WORKSPACE / relative_path
                source_bytes = absolute_path.read_bytes()
                if hashlib.sha256(source_bytes).hexdigest() != source_hash:
                    raise SystemExit(f"source replay failed: {relative_path}")
                full_sources.append({
                    "source_path": relative_path,
                    "canonical_source_sha256": source_hash,
                    "preserved_original_skill_utf8": source_bytes.decode("utf-8"),
                })
            members.append({
                "canonical_source_sha256": source_hash,
                "native_description": corpus["native_description"],
                "native_description_sha256": description_hash,
                "native_description_origin": corpus["native_description_origin"],
                "native_description_literal_replay_status": corpus["native_description_replay_status"],
                "source_byte_replay": corpus["source_byte_replay"],
                "source_native_developer_engineering_categories": matching_categories(corpus["native_description"]),
                "preserved_complete_original_sources": full_sources,
            })
        packet_rows.append({
            "record_type": "source_native_confusable_family_full_original_source_packet",
            "batch_id": "SN-LEX-B040",
            "batch_rank": family["batch_rank"],
            "family_id": family["family_id"],
            "selection_scope": family["selection_scope"],
            "source_native_category_intersection": family["source_native_category_intersection"],
            "reciprocal_neighbour_provenance": {
                "reciprocal_link_count": family["reciprocal_link_count"],
                "mutual_directional_ranks": family["mutual_directional_ranks"],
                "rank_fusion_score": family["rank_fusion_score"],
                "hypothesis_source_hashes": family["member_source_sha256"],
            },
            "members": members,
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "claim_boundary": "Packet only; no source review, prompt, adequacy, acceptable-set, admission or metric result.",
        })
    packets.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in packet_rows))

    validation = {
        "status": "PASS_B040_DISCOVERY_ONLY_SOURCE_NATIVE_ENGINEERING_FAMILY_PACKETS",
        "bound_inputs": {
            "protocol": sha256_file(PROTOCOL),
            "source_native_description_corpus": sha256_file(CORPUS),
            "source_native_description_corpus_summary": sha256_file(CORPUS_SUMMARY),
            "frozen_lexical_mutual_triangle_hypotheses": sha256_file(HYPOTHESES),
            "frozen_lexical_bootstrap_summary": sha256_file(BOOTSTRAP_SUMMARY),
            "prior_B001_B038_internal_reconciliation_keys": {
                batch: sha256_file(path) for batch, path in keys.items()
            },
        },
        "method": {
            "route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, then member source hashes",
            "developer_engineering_filter": "all three literal source-native descriptions share at least one predeclared permitted category; categories and regexes are recorded in this script",
            "permitted_categories": list(CATEGORY_PATTERNS),
            "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "provenance status", "prior review outcome", "prompt", "label", "cluster membership"],
            "fresh_source_policy": "exclude every B001-B038 inspected source hash; require source-disjoint members within B040",
        },
        "counts": {
            "frozen_corpus_sources": len(corpus_rows),
            "frozen_hypotheses": len(hypotheses),
            "prior_batches": len(keys),
            "prior_inspected_source_hashes_B001_B038": len(prior_hashes),
            "b040_families": len(selected),
            "b040_source_hashes": len(used_hashes),
            "source_hash_overlap_B040_vs_B001_B038": len(used_hashes & prior_hashes),
            "selection_exclusions_encountered_before_completion": dict(sorted(exclusion_counts.items())),
            "family_shared_category_counts": dict(sorted(Counter(
                category for row in selected for category in row["source_native_category_intersection"]
            ).items())),
        },
        "outputs": {
            queue.name: sha256_file(queue),
            packets.name: sha256_file(packets),
        },
        "limitations": [
            "A lexical reciprocal-neighbour priority is not semantic similarity ground truth or a retrieval metric.",
            "The developer-engineering description filter is a scope restriction, not a source-quality, family-validity or eligibility decision.",
            "No full-source review, provenance review, prompt authoring, prompt adequacy, acceptable-set work, admission or final-library eligibility has occurred.",
            "The dense source-native route remains unexecuted; this B040 continuation does not repair that limitation or establish dense-versus-lexical coverage.",
        ],
        "claim_boundary": "Discovery packets only. These 25 hypotheses are not reviewed clusters, RQ2 cases, final-library entries, acceptable alternatives, retrieval results or metrics.",
    }
    (OUTPUT / "summary.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUTPUT), "counts": validation["counts"], "output_hashes": validation["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
