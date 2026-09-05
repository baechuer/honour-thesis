#!/usr/bin/env python3
"""Materialise the hash-bound 23,450-source RQ2 background-corpus population.

This builds a source/navigation manifest only.  It does not rank prompts,
create clusters, labels, representations, selectors, or metrics.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK_ROOT = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK_ROOT / "rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/USER_AUTHORIZED_BACKGROUND_CORPUS_K_CALIBRATION_PROTOCOL_2026-09-03.md"
CURRENT_UNION = NC_ROOT / (
    "manifests/current_pre_freeze_consolidated_2026-08-31/"
    "canonical_candidate_union_current_pre_freeze.jsonl"
)
CURRENT_PROFILES = NC_ROOT / (
    "manifests/whole_library_navigation_profiles_prefreeze_2026-08-31/"
    "navigation_profiles.jsonl"
)
BACKGROUND_PREFILTER = NC_ROOT / (
    "manifests/rq2b_native_discovery_provenance_first_prefilter_2026-09-03/"
    "rq2_native_source_navigation_provenance_first_excluding_current_and_b001.jsonl"
)
PARENT_IDENTITIES = BENCHMARK_ROOT / (
    "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
)
OUTPUT_DIR = NC_ROOT / "manifests/background_corpus_extended_union_23450_2026-09-03"
POPULATION_OUT = OUTPUT_DIR / "candidate_population.jsonl"
PROFILES_OUT = OUTPUT_DIR / "navigation_profiles.jsonl"
PARENT_DELTA_OUT = OUTPUT_DIR / "parent_non_gold_delta_source_hashes.jsonl"
SUMMARY_OUT = OUTPUT_DIR / "summary.json"

EXPECTED_CURRENT = 3094
EXPECTED_BACKGROUND = 20356
EXPECTED_EXTENDED = 23450
EXPECTED_PARENT = 2431
EXPECTED_PARENT_DELTA = 21019
EXCLUDED_TOKENS = {"anthropic", "chatgpt", "claude", "codex", "gemini", "openai"}


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


def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def bounded(value: str, limit: int) -> str:
    value = normalise_space(value)
    return value if len(value) <= limit else value[:limit].rstrip()


def relevance_safe(value: str) -> str:
    output = value
    for term in sorted(EXCLUDED_TOKENS, key=lambda item: (-len(item), item)):
        output = re.sub(rf"(?i)\b{re.escape(term)}\b", " ", output)
    return normalise_space(output)


def workspace_relative(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError as error:
        raise SystemExit(f"Source lies outside workspace: {path}") from error


def assert_provenance_lead(row: dict[str, Any]) -> None:
    local = row.get("local_provenance")
    if not isinstance(local, dict):
        raise SystemExit("Background source lacks local provenance object")
    if row.get("status") != "PASS_LOCAL_PIN_AND_LICENSE_PRECONDITION_PENDING_SEMANTIC_SCREEN":
        raise SystemExit(f"Background source has non-pass prefilter status: {row.get('status')}")
    if row.get("source_byte_replay") != "PASS_SHA256_MATCH":
        raise SystemExit("Background source lacks prior byte-replay pass")
    if not re.fullmatch(r"[0-9a-f]{40}", str(local.get("pinned_commit") or "")):
        raise SystemExit("Background source lacks a 40-hex pinned commit")
    if local.get("license_status") != "DECLARED_REPOSITORY_LICENSE":
        raise SystemExit("Background source lacks declared repository licence status")
    if not local.get("license_path") or not re.fullmatch(r"[0-9a-f]{64}", str(local.get("license_sha256") or "")):
        raise SystemExit("Background source lacks a recorded licence path/hash")


def current_population_row(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "rq2_candidate_population_member",
        "population_membership": "RETAINED_CURRENT_PREFREEZE_CANDIDATE_UNION",
        "canonical_source_sha256": profile["canonical_source_sha256"],
        "final_intake_role": profile["final_intake_role"],
        "candidate_alias_ids": profile["candidate_alias_ids"],
        "source_paths": profile["source_paths"],
        "provenance_status": "RETAINED_CURRENT_PREFREEZE_UNION_BINDING",
        "claim_boundary": "Retained source is not relabelled or newly admitted by the 23,450-source amendment.",
    }


def background_profile_and_population(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    assert_provenance_lead(row)
    source_path = Path(str(row["source_path"]))
    source_hash = str(row["source_sha256"])
    if not source_path.is_file() or sha256_file(source_path) != source_hash:
        raise SystemExit(f"Background source byte replay failed: {source_path}")
    source_name = bounded(str(row.get("source_name") or ""), 240)
    source_description = bounded(str(row.get("source_description") or ""), 1200)
    source_headings = [bounded(str(value), 200) for value in row.get("heading_preview") or []]
    source_headings = [value for value in source_headings if value]
    if not source_name and source_headings:
        source_name = source_headings[0]
    heading_profile = normalise_space(" ".join(source_headings))
    relevance_name = relevance_safe(source_name)
    relevance_description = relevance_safe(source_description)
    relevance_headings = relevance_safe(heading_profile)
    if not (relevance_name or relevance_description or relevance_headings):
        raise SystemExit(f"No relevance-safe navigation text: {source_path}")
    aliases = [str(row["source_id"])]
    local = row["local_provenance"]
    profile = {
        "canonical_source_sha256": source_hash,
        "candidate_alias_ids": aliases,
        "source_paths": [workspace_relative(source_path)],
        "final_intake_role": "UNADJUDICATED_PROVENANCE_BOUND_BACKGROUND_CANDIDATE",
        "source_name": source_name,
        "source_description": source_description,
        "source_description_origin": "PROVENANCE_PREFILTER_NAVIGATION_DESCRIPTION",
        "source_headings": source_headings,
        "name_description_profile": normalise_space(f"{source_name} {source_description}"),
        "heading_profile": heading_profile,
        "relevance_source_name": relevance_name,
        "relevance_source_description": relevance_description,
        "relevance_heading_profile": relevance_headings,
        "relevance_excluded_provider_product_tokens": sorted(EXCLUDED_TOKENS),
        "profile_schema_version": "rq2b_background_corpus_navigation_profile_v1",
        "scope_boundary": "OUTCOME_BLIND_NAVIGATION_ONLY_NOT_A_FINAL_REPRESENTATION_LABEL_RANKING_OR_METRIC",
    }
    population = {
        "record_type": "rq2_candidate_population_member",
        "population_membership": "UNADJUDICATED_PROVENANCE_BOUND_BACKGROUND_CANDIDATE",
        "canonical_source_sha256": source_hash,
        "final_intake_role": profile["final_intake_role"],
        "candidate_alias_ids": aliases,
        "source_paths": profile["source_paths"],
        "provenance_binding": {
            "source_byte_replay": row["source_byte_replay"],
            "import_path": workspace_relative(Path(str(local["import_path"]))),
            "pinned_commit": local["pinned_commit"],
            "license_status": local["license_status"],
            "license_path": local["license_path"],
            "license_sha256": local["license_sha256"],
            "import_source_sha256": local["import_source_sha256"],
        },
        "claim_boundary": (
            "Provenance-qualified background candidate only; not a semantic cluster member, "
            "negative distractor, adequacy label, acceptable-set member, or final-library admission."
        ),
    }
    return profile, population


def main() -> int:
    required = [PROTOCOL, CURRENT_UNION, CURRENT_PROFILES, BACKGROUND_PREFILTER, PARENT_IDENTITIES]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    current_union = read_jsonl(CURRENT_UNION)
    current_profiles = read_jsonl(CURRENT_PROFILES)
    parent_identities = read_jsonl(PARENT_IDENTITIES)
    prefilter_rows = read_jsonl(BACKGROUND_PREFILTER)
    background_rows = [
        row for row in prefilter_rows
        if row.get("record_type") == "provenance_first_source_reading_lead"
    ]

    current_hashes = {str(row["canonical_source_sha256"]) for row in current_union}
    profile_by_hash = {str(row["canonical_source_sha256"]): row for row in current_profiles}
    parent_hashes = {str(row["source_sha256"]) for row in parent_identities}
    background_hashes = {str(row["source_sha256"]) for row in background_rows}
    if len(current_union) != len(current_hashes) != EXPECTED_CURRENT:
        raise SystemExit("Current candidate union does not have 3,094 unique source hashes")
    if len(current_profiles) != len(profile_by_hash) != EXPECTED_CURRENT or set(profile_by_hash) != current_hashes:
        raise SystemExit("Current navigation profile binding is not the fixed 3,094-source union")
    if len(background_rows) != len(background_hashes) != EXPECTED_BACKGROUND:
        raise SystemExit("Provenance prefilter does not have 20,356 unique passing source hashes")
    if current_hashes & background_hashes:
        raise SystemExit("Background sources overlap the retained current union")
    if len(parent_hashes) != EXPECTED_PARENT or not parent_hashes <= current_hashes:
        raise SystemExit("Parent V3 identity set does not bind to the current union")

    profiles: list[dict[str, Any]] = []
    population: list[dict[str, Any]] = []
    for source_hash in sorted(current_hashes):
        profile = profile_by_hash[source_hash]
        observed = []
        for raw_path in profile["source_paths"]:
            source_path = WORKSPACE / str(raw_path)
            if not source_path.is_file():
                raise SystemExit(f"Retained source path missing: {source_path}")
            observed.append(sha256_file(source_path))
        if set(observed) != {source_hash}:
            raise SystemExit(f"Retained source byte replay failed: {source_hash}")
        profiles.append(profile)
        population.append(current_population_row(profile))
    for row in sorted(background_rows, key=lambda item: str(item["source_sha256"])):
        profile, member = background_profile_and_population(row)
        profiles.append(profile)
        population.append(member)

    profiles.sort(key=lambda row: str(row["canonical_source_sha256"]))
    population.sort(key=lambda row: str(row["canonical_source_sha256"]))
    extended_hashes = {str(row["canonical_source_sha256"]) for row in profiles}
    role_by_hash = {
        str(row["canonical_source_sha256"]): str(row["final_intake_role"])
        for row in profiles
    }
    if len(profiles) != len(population) != len(extended_hashes) != EXPECTED_EXTENDED:
        raise SystemExit("Extended population does not have exactly 23,450 unique source hashes")
    if {str(row["canonical_source_sha256"]) for row in population} != extended_hashes:
        raise SystemExit("Population and navigation-profile source sets disagree")

    parent_delta_hashes = extended_hashes - parent_hashes
    if len(parent_delta_hashes) != EXPECTED_PARENT_DELTA:
        raise SystemExit("Parent non-gold delta does not have exactly 21,019 sources")
    parent_delta = [
        {
            "record_type": "parent_non_gold_candidate",
            "canonical_source_sha256": source_hash,
            "final_intake_role": role_by_hash[source_hash],
            "scope_boundary": "Not a historical parent-V3 target source; eligible only for alternative discovery.",
        }
        for source_hash in sorted(parent_delta_hashes)
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(POPULATION_OUT, population)
    write_jsonl(PROFILES_OUT, profiles)
    write_jsonl(PARENT_DELTA_OUT, parent_delta)
    role_counts = Counter(str(row["final_intake_role"]) for row in profiles)
    membership_counts = Counter(str(row["population_membership"]) for row in population)
    summary = {
        "status": "PASS_HASH_BOUND_23450_SOURCE_BACKGROUND_CORPUS_MATERIALISATION_NOT_A_LABEL_OR_CLUSTER_RESULT",
        "protocol": str(PROTOCOL.relative_to(BENCHMARK_ROOT)),
        "bound_inputs": {
            str(path.relative_to(BENCHMARK_ROOT)): sha256_file(path)
            for path in required
        },
        "counts": {
            "retained_current_prefreeze_sources": len(current_hashes),
            "unadjudicated_provenance_bound_background_sources": len(background_hashes),
            "extended_candidate_population_sources": len(extended_hashes),
            "parent_v3_source_hashes_excluded_from_parent_alternative_lane": len(parent_hashes),
            "parent_non_gold_delta_sources": len(parent_delta_hashes),
            "population_membership": dict(sorted(membership_counts.items())),
            "final_intake_role": dict(sorted(role_counts.items())),
            "source_byte_replay_failures": 0,
            "cross_stratum_hash_duplicates": 0,
        },
        "outputs": {
            path.name: sha256_file(path)
            for path in [POPULATION_OUT, PROFILES_OUT, PARENT_DELTA_OUT]
        },
        "claim_boundary": [
            "The 20,356-source stratum is provenance-qualified but semantically unadjudicated.",
            "No background source is a distractor, negative label, adequate alternative, cluster, prompt, representation, selector output, or metric result merely by appearing here.",
            "The historical 3,094-source current union is preserved as a retained stratum and is not overwritten.",
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
