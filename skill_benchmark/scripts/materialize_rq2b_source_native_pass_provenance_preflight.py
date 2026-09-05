#!/usr/bin/env python3
"""Replay provenance prerequisites for source-native family-review passes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
POPULATION = NC_ROOT / "manifests/background_corpus_extended_union_23450_2026-09-03/candidate_population.jsonl"
CURRENT_UNION = NC_ROOT / "manifests/current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"


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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def background_pass(row: dict[str, Any], source_hash: str) -> bool:
    binding = row.get("provenance_binding")
    return isinstance(binding, dict) and binding.get("source_byte_replay") == "PASS_SHA256_MATCH" and binding.get("import_source_sha256") == source_hash and bool(re.fullmatch(r"[0-9a-f]{40}", str(binding.get("pinned_commit") or ""))) and binding.get("license_status") == "DECLARED_REPOSITORY_LICENSE" and bool(binding.get("license_path")) and bool(re.fullmatch(r"[0-9a-f]{64}", str(binding.get("license_sha256") or "")))


def current_pass(row: dict[str, Any] | None) -> bool:
    if not isinstance(row, dict):
        return False
    binding = row.get("provenance_binding")
    if isinstance(binding, dict) and binding.get("status") == "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH":
        return True
    return str(row.get("status")) == "ADMITTED_NC_SOURCE_CANDIDATE_PENDING_REPRESENTATION_AND_FINAL_FREEZE"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay provenance prerequisites for full-source family-review passes.")
    parser.add_argument("--review-dir", type=Path, default=REVIEW_DIR)
    parser.add_argument("--expected-pass-families", type=int, default=4)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_pass_families < 1:
        raise SystemExit("--expected-pass-families must be positive")
    review_dir = args.review_dir.resolve()
    final_path = review_dir / "reconciliation/final_dispositions/reconciled_family_dispositions.jsonl"
    key_path = review_dir / "internal_reconciliation_key.jsonl"
    output_dir = review_dir / "reconciliation/pass_provenance_preflight"
    required = [final_path, key_path, CORPUS, POPULATION, CURRENT_UNION]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    pass_tokens = {str(row["family_token"]) for row in read_jsonl(final_path) if row.get("final_decision") == "PASS_TO_PROMPT_AUTHORING"}
    if len(pass_tokens) != args.expected_pass_families:
        raise SystemExit(f"Expected exactly {args.expected_pass_families} source-family passes from {args.batch_label}")
    key_rows = [row for row in read_jsonl(key_path) if str(row["family_token"]) in pass_tokens]
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in key_rows:
        by_family[str(row["family_token"])].append(row)
    if set(by_family) != pass_tokens or any(len(rows) != 3 for rows in by_family.values()):
        raise SystemExit("Pass-family reconciliation key is incomplete")
    corpus_by_hash = {str(row["canonical_source_sha256"]): row for row in read_jsonl(CORPUS)}
    population_by_hash = {str(row["canonical_source_sha256"]): row for row in read_jsonl(POPULATION)}
    current_by_hash = {str(row["canonical_source_sha256"]): row for row in read_jsonl(CURRENT_UNION)}

    source_rows: list[dict[str, Any]] = []
    family_rows: list[dict[str, Any]] = []
    for family_token in sorted(pass_tokens):
        statuses: list[str] = []
        for key_row in sorted(by_family[family_token], key=lambda row: str(row["member_token"])):
            source_hash = str(key_row["canonical_source_sha256"])
            corpus = corpus_by_hash.get(source_hash)
            population = population_by_hash.get(source_hash)
            if corpus is None or population is None:
                raise SystemExit(f"Pass source missing from bound corpus/population: {source_hash}")
            byte_ok = True
            for raw_path in corpus["source_paths"]:
                path = WORKSPACE / str(raw_path)
                byte_ok = byte_ok and path.is_file() and sha256_file(path) == source_hash
            membership = str(population["population_membership"])
            if membership == "UNADJUDICATED_PROVENANCE_BOUND_BACKGROUND_CANDIDATE":
                status = "PASS_BACKGROUND_PIN_LICENSE_AND_BYTE_REPLAY" if byte_ok and background_pass(population, source_hash) else "DEFER_BACKGROUND_PROVENANCE_REPLAY_FAILURE"
            elif membership == "RETAINED_CURRENT_PREFREEZE_CANDIDATE_UNION":
                status = "PASS_CURRENT_PRE_FREEZE_PROVENANCE_BINDING" if byte_ok and current_pass(current_by_hash.get(source_hash)) else "DEFER_CURRENT_SOURCE_PROVENANCE_UPGRADE_REQUIRED"
            else:
                raise SystemExit(f"Unexpected population membership: {membership}")
            statuses.append(status)
            source_rows.append({
                "family_token": family_token,
                "member_token": key_row["member_token"],
                "canonical_source_sha256": source_hash,
                "population_membership": membership,
                "source_paths": corpus["source_paths"],
                "source_byte_replay": "PASS_SHA256_MATCH" if byte_ok else "FAIL_SHA256_REPLAY",
                "provenance_preflight_status": status,
                "claim_boundary": "Source preflight only; not source admission, cluster, prompt or final-library result.",
            })
        family_rows.append({
            "family_token": family_token,
            "family_provenance_preflight_status": "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE" if all(status.startswith("PASS_") for status in statuses) else "DEFER_BEFORE_PROMPT_AUTHORING_PROVENANCE_UPGRADE_REQUIRED",
            "member_statuses": statuses,
            "claim_boundary": "Even eligible family still needs cue-safe prompt authoring and target-blind adequacy review; no cluster is admitted.",
        })
    output_dir.mkdir(parents=True)
    sources_path = output_dir / "pass_family_source_provenance_preflight.jsonl"
    families_path = output_dir / "pass_family_provenance_dispositions.jsonl"
    write_jsonl(sources_path, source_rows)
    write_jsonl(families_path, family_rows)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_PASS_FAMILY_PROVENANCE_PREFLIGHT_NO_PROMPT",
        "bound_inputs": {relative(final_path): sha256_file(final_path), relative(key_path): sha256_file(key_path), relative(CORPUS): sha256_file(CORPUS), relative(POPULATION): sha256_file(POPULATION), relative(CURRENT_UNION): sha256_file(CURRENT_UNION)},
        "counts": {"pass_families": len(family_rows), "pass_sources": len(source_rows), "family_dispositions": dict(sorted(Counter(row["family_provenance_preflight_status"] for row in family_rows).items())), "source_dispositions": dict(sorted(Counter(row["provenance_preflight_status"] for row in source_rows).items()))},
        "outputs": {"pass_family_source_provenance_preflight.jsonl": sha256_file(sources_path), "pass_family_provenance_dispositions.jsonl": sha256_file(families_path)},
        "claim_boundary": "Preflight does not author prompts or admit any family as a final cluster/source/prompt.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
