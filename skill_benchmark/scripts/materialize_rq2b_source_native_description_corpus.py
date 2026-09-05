#!/usr/bin/env python3
"""Materialise a hash-bound native-description corpus for cluster discovery.

The indexable text is exactly the preserved source_description field when that
text can be replayed against the complete original source bytes.  This program
does not generate summaries/cards, rank candidates, create clusters, labels,
prompts, representations, selectors, or metrics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
INPUT_DIR = NC_ROOT / "manifests/background_corpus_extended_union_23450_2026-09-03"
PROFILES = INPUT_DIR / "navigation_profiles.jsonl"
POPULATION = INPUT_DIR / "candidate_population.jsonl"
DEFAULT_OUTPUT = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04"

EXPECTED_SOURCES = 23_450
EXPECTED_CURRENT = 3_094
EXPECTED_BACKGROUND = 20_356


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def file_sha256(path: Path) -> str:
    return sha256_file(path)


def workspace_relative(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError as error:
        raise SystemExit(f"Source lies outside workspace: {path}") from error


def source_paths_and_replay(profile: dict[str, Any], source_hash: str) -> tuple[list[str], list[bytes]]:
    raw_paths = profile.get("source_paths")
    if not isinstance(raw_paths, list) or not raw_paths:
        raise SystemExit(f"Missing source_paths: {source_hash}")
    source_paths: list[str] = []
    source_bytes: list[bytes] = []
    for raw_path in raw_paths:
        path = WORKSPACE / str(raw_path)
        if not path.is_file():
            raise SystemExit(f"Source path missing: {path}")
        if sha256_file(path) != source_hash:
            raise SystemExit(f"Source hash mismatch: {path}")
        source_paths.append(workspace_relative(path))
        source_bytes.append(path.read_bytes())
    return source_paths, source_bytes


def description_status(description: str, source_bytes: list[bytes]) -> str:
    if not description.strip():
        return "NO_NATIVE_DESCRIPTION"
    needle = normalise_space(description)
    if not needle:
        return "NO_NATIVE_DESCRIPTION"
    for raw in source_bytes:
        decoded = raw.decode("utf-8", errors="replace")
        if needle in normalise_space(decoded):
            return "LITERAL_REPLAY_PASS"
    return "DESCRIPTION_NOT_LITERAL_REPLAYABLE"


def corpus_digest(rows: list[dict[str, Any]]) -> str:
    payload = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    ).encode("utf-8")
    return sha256_bytes(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    required = [PROTOCOL, PROFILES, POPULATION]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if args.output_dir.exists():
        raise SystemExit(f"Output directory already exists: {args.output_dir}")

    profiles = read_jsonl(PROFILES)
    population = read_jsonl(POPULATION)
    profile_by_hash = {str(row["canonical_source_sha256"]): row for row in profiles}
    population_by_hash = {str(row["canonical_source_sha256"]): row for row in population}
    if len(profiles) != len(profile_by_hash) != EXPECTED_SOURCES:
        raise SystemExit("Navigation profiles must contain exactly 23,450 source-unique records")
    if len(population) != len(population_by_hash) != EXPECTED_SOURCES:
        raise SystemExit("Population must contain exactly 23,450 source-unique records")
    if set(profile_by_hash) != set(population_by_hash):
        raise SystemExit("Population and navigation-profile hash sets disagree")

    rows: list[dict[str, Any]] = []
    membership_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    origin_counts: Counter[str] = Counter()
    for source_hash in sorted(profile_by_hash):
        profile = profile_by_hash[source_hash]
        population_row = population_by_hash[source_hash]
        source_paths, source_bytes = source_paths_and_replay(profile, source_hash)
        description = str(profile.get("source_description") or "")
        status = description_status(description, source_bytes)
        membership = str(population_row.get("population_membership"))
        membership_counts[membership] += 1
        status_counts[status] += 1
        description_origin = str(profile.get("source_description_origin") or "MISSING")
        origin_counts[description_origin] += 1
        rows.append({
            "record_type": "rq2b_source_native_description",
            "canonical_source_sha256": source_hash,
            "source_paths": source_paths,
            "source_byte_replay": "PASS_SHA256_MATCH",
            "population_membership": membership,
            "final_intake_role": str(profile.get("final_intake_role")),
            "native_description": description,
            "native_description_sha256": sha256_text(description),
            "native_description_origin": description_origin,
            "native_description_replay_status": status,
            "index_eligibility": status == "LITERAL_REPLAY_PASS",
            "index_scope": "EXACT_NATIVE_DESCRIPTION_ONLY_NO_TITLE_HEADING_CARD_OR_LABEL",
            "full_source_review_scope": "PRESERVED_COMPLETE_ORIGINAL_SKILL_IS_AUTHORITATIVE",
            "claim_boundary": "Discovery corpus record only; not a cluster, admission, label, selector output, or metric.",
        })

    current_count = membership_counts["RETAINED_CURRENT_PREFREEZE_CANDIDATE_UNION"]
    background_count = membership_counts["UNADJUDICATED_PROVENANCE_BOUND_BACKGROUND_CANDIDATE"]
    if current_count != EXPECTED_CURRENT or background_count != EXPECTED_BACKGROUND:
        raise SystemExit("Unexpected population-membership counts")

    args.output_dir.mkdir(parents=True)
    corpus_path = args.output_dir / "source_native_description_corpus.jsonl"
    summary_path = args.output_dir / "summary.json"
    write_jsonl(corpus_path, rows)
    summary = {
        "status": "PASS_HASH_BOUND_SOURCE_NATIVE_DESCRIPTION_CORPUS_NO_RANKING_OR_CLUSTER_RESULT",
        "protocol": workspace_relative(PROTOCOL),
        "bound_inputs": {
            workspace_relative(PROFILES): file_sha256(PROFILES),
            workspace_relative(POPULATION): file_sha256(POPULATION),
        },
        "counts": {
            "sources": len(rows),
            "population_membership": dict(sorted(membership_counts.items())),
            "native_description_replay_status": dict(sorted(status_counts.items())),
            "native_description_origin": dict(sorted(origin_counts.items())),
            "index_eligible_sources": sum(row["index_eligibility"] for row in rows),
        },
        "outputs": {
            "source_native_description_corpus.jsonl": file_sha256(corpus_path),
            "canonical_corpus_digest": corpus_digest(rows),
        },
        "claim_boundary": [
            "Indexable text is exact native description only; no generated source card or summary exists.",
            "Full original source is required for every semantic-family and later admission decision.",
            "This corpus has no ranking, cluster, prompt, label, acceptable-set, selector, or metric output.",
        ],
    }
    with summary_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
