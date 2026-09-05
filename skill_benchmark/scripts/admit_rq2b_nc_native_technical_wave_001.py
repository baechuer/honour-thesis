#!/usr/bin/env python3
"""Fail-closed pre-freeze admission for RQ2-native technical wave 001.

This controller only records source-grounded curatorial admission evidence.  It
does not create final gold, representations, selector inputs, or results.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
UNION = BASE / (
    "manifests/rq1_re_review_batch_004_pre_freeze_admission_2026-08-31/"
    "canonical_candidate_union_rq1_batch_004.jsonl"
)
LEADS = BASE / "candidates/rq2_native_discovery_wave_001_technical_2026-08-31.jsonl"
AUTHORS = BASE / "prompts/rq2_native_technical_wave_001_authoring_private_2026-08-31.jsonl"
PACKETS = BASE / "review/rq2_native_technical_wave_001_target_blinded_packets_2026-08-31.jsonl"
RESULTS = BASE / "review/rq2_native_technical_wave_001_target_blinded_results_2026-08-31.jsonl"
OUTPUT = BASE / "manifests/rq2_native_technical_wave_001_pre_freeze_admission_2026-08-31"

EXPECTED_CLUSTER_COUNT = 9
EXPECTED_PROMPT_COUNT = 27
EXPECTED_UNION_COUNT = 3084
PROXIMITY_LEVELS = {"high", "moderate"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def require_unique_by(rows: list[dict[str, Any]], key: str, artifact: Path) -> dict[str, dict[str, Any]]:
    indexed = {str(row[key]): row for row in rows}
    if len(indexed) != len(rows):
        raise SystemExit(f"Duplicate {key} in {artifact}")
    return indexed


def proximity_level(source_body_echo: str, prompt_id: str) -> str:
    level = source_body_echo.split(";", 1)[0].strip().lower()
    if level not in PROXIMITY_LEVELS:
        raise SystemExit(f"Unexpected source/body proximity level for {prompt_id}: {source_body_echo}")
    return level


def composition_is_optional(note: str) -> bool:
    """Require the blinded reviewer to explicitly rule out required composition."""
    normalized = note.lower()
    return any(
        marker in normalized
        for marker in (
            "not required",
            "not a required",
            "not part of the requested",
            "none required",
            "none indicated",
            "no candidate composition is needed",
            "no other candidate is a necessary component",
            "not necessary",
            "not stated",
            "none are named",
            "not needed",
            "not requested",
            "does not require",
            "does not independently satisfy",
            "does not make the prompt multi-full",
            "not a substitute",
            "not the monitoring answer",
            "only apply if",
        )
    )


def main() -> int:
    required = [UNION, LEADS, AUTHORS, PACKETS, RESULTS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required artifacts: {missing}")

    union_rows = read_jsonl(UNION)
    union_by_hash = require_unique_by(union_rows, "canonical_source_sha256", UNION)
    if len(union_rows) != EXPECTED_UNION_COUNT:
        raise SystemExit(f"Expected the current {EXPECTED_UNION_COUNT}-row hash-unique union")

    lead_rows = read_jsonl(LEADS)
    promoted = [
        row for row in lead_rows
        if str(row["screen_disposition"]).startswith("PROMOTE_TO_RQ2_PROMPT_AUTHORING")
    ]
    promoted_by_id = require_unique_by(promoted, "cluster_lead_id", LEADS)
    if len(promoted) != EXPECTED_CLUSTER_COUNT:
        raise SystemExit(f"Expected {EXPECTED_CLUSTER_COUNT} promoted technical clusters")

    authors = require_unique_by(read_jsonl(AUTHORS), "prompt_id", AUTHORS)
    packets = require_unique_by(read_jsonl(PACKETS), "prompt_id", PACKETS)
    results = require_unique_by(read_jsonl(RESULTS), "prompt_id", RESULTS)
    if set(authors) != set(packets) or set(authors) != set(results):
        raise SystemExit("Private author, target-blinded packet, and result rosters must match exactly")
    if len(authors) != EXPECTED_PROMPT_COUNT:
        raise SystemExit(f"Expected {EXPECTED_PROMPT_COUNT} private prompts and blinded reviews")

    cluster_rows: list[dict[str, Any]] = []
    prompt_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []
    proximity_counts: Counter[str] = Counter()
    composition_counts: Counter[str] = Counter()

    for cluster_id in sorted(promoted_by_id):
        lead = promoted_by_id[cluster_id]
        candidates = list(lead["candidates"])
        candidate_hashes = [str(candidate["source_sha256"]) for candidate in candidates]
        candidate_by_hash = {str(candidate["source_sha256"]): candidate for candidate in candidates}
        if len(candidates) != 3 or len(candidate_by_hash) != 3:
            raise SystemExit(f"Expected a hash-unique three-member promoted cluster: {cluster_id}")
        if not set(candidate_hashes).issubset(union_by_hash):
            raise SystemExit(f"Cluster source absent from current union: {cluster_id}")

        # No source is added by this admission.  The current-union binding is
        # sufficient provenance input; replay all local source bytes here.
        for candidate in candidates:
            source_hash = str(candidate["source_sha256"])
            source_path = ROOT.parent / str(candidate["source_path"])
            union_record = union_by_hash[source_hash]
            binding = union_record.get("provenance_binding")
            if not isinstance(binding, dict) or not str(binding.get("status", "")).startswith("PASS_"):
                raise SystemExit(f"Current-union provenance binding does not pass: {source_hash}")
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"Source byte replay failed: {source_path}")

        cluster_authors = [row for row in authors.values() if str(row["cluster_lead_id"]) == cluster_id]
        if len(cluster_authors) != len(candidates):
            raise SystemExit(f"Every promoted cluster member needs one private prompt: {cluster_id}")

        prompt_ids: list[str] = []
        reviewed_targets: set[str] = set()
        cluster_proximity_levels: list[str] = []
        cluster_composition_strata: list[str] = []
        for author in sorted(cluster_authors, key=lambda row: str(row["prompt_id"])):
            prompt_id = str(author["prompt_id"])
            packet = packets[prompt_id]
            result = results[prompt_id]
            if str(packet["cluster_lead_id"]) != cluster_id or str(result["prompt_id"]) != prompt_id:
                raise SystemExit(f"Cluster or prompt binding mismatch: {prompt_id}")
            if str(result["packet_id"]) != str(packet["packet_id"]):
                raise SystemExit(f"Packet/result identifier mismatch: {prompt_id}")
            if str(result.get("review_status")) != "BLINDED_COMPLETE":
                raise SystemExit(f"Incomplete blinded review: {prompt_id}")
            if str(result.get("source_hash_verification")) != "all candidate SHA-256 values matched":
                raise SystemExit(f"Blinded source hash verification did not pass: {prompt_id}")

            packet_candidates = list(packet["candidates"])
            packet_aliases = [str(row["alias"]) for row in packet_candidates]
            packet_hashes = [str(row["source_sha256"]) for row in packet_candidates]
            assessments = list(result["alias_assessments"])
            assessment_aliases = [str(row["alias"]) for row in assessments]
            if (
                len(packet_candidates) != len(candidates)
                or len(set(packet_aliases)) != len(packet_aliases)
                or set(packet_hashes) != set(candidate_hashes)
                or set(assessment_aliases) != set(packet_aliases)
                or len(assessments) != len(packet_candidates)
            ):
                raise SystemExit(f"Target-blinded packet roster is not exact: {prompt_id}")
            packet_by_alias = {str(row["alias"]): row for row in packet_candidates}
            for assessment in assessments:
                alias = str(assessment["alias"])
                if (
                    str(assessment["source_sha256_expected"]) != str(packet_by_alias[alias]["source_sha256"])
                    or str(assessment["source_sha256_observed"]) != str(packet_by_alias[alias]["source_sha256"])
                ):
                    raise SystemExit(f"Blinded assessment source binding mismatch: {prompt_id}/{alias}")
            full = [row for row in assessments if str(row["classification"]) == "fully_adequate"]
            if len(full) != 1:
                raise SystemExit(f"Expected exactly one fully adequate alias: {prompt_id}")
            full_alias = str(full[0]["alias"])
            reviewed_hash = str(packet_by_alias[full_alias]["source_sha256"])
            intended_hash = str(author["author_intended_candidate_source_sha256"])
            if reviewed_hash != intended_hash:
                raise SystemExit(f"Blind fully adequate target differs from private author target: {prompt_id}")
            if reviewed_hash not in candidate_by_hash:
                raise SystemExit(f"Reviewed target is outside promoted cluster: {prompt_id}")

            cueing = result.get("cueing")
            relationships = result.get("relationships")
            if not isinstance(cueing, dict) or not isinstance(relationships, dict):
                raise SystemExit(f"Blinded cue/relationship assessment absent: {prompt_id}")
            if cueing.get("gratuitous_cues"):
                raise SystemExit(f"Gratuitous cue prevents admission: {prompt_id}")
            proximity = proximity_level(str(cueing.get("source_body_echo", "")), prompt_id)
            composition_note = str(relationships.get("composition", "")).strip()
            if not composition_note or not composition_is_optional(composition_note):
                raise SystemExit(f"Composition must be explicitly optional, not required: {prompt_id}")
            if str(relationships.get("multi_full_risk", "")).lower().startswith("high"):
                raise SystemExit(f"High multi-full risk prevents admission: {prompt_id}")

            composition_stratum = (
                "COMPOSITION_NOTED_OPTIONAL_NOT_REQUIRED"
                if composition_note.lower() not in {"none required", "none indicated", "no candidate composition is needed for the stated task."}
                else "NO_COMPOSITION_NOTED"
            )
            candidate = candidate_by_hash[reviewed_hash]
            prompt_ids.append(prompt_id)
            reviewed_targets.add(reviewed_hash)
            cluster_proximity_levels.append(proximity)
            cluster_composition_strata.append(composition_stratum)
            proximity_counts[proximity] += 1
            composition_counts[composition_stratum] += 1
            prompt_rows.append({
                "prompt_id": prompt_id,
                "cluster_id": cluster_id,
                "prompt": author["prompt"],
                "reviewed_single_fully_adequate_source_sha256": reviewed_hash,
                "reviewed_single_fully_adequate_candidate_id": candidate["skill_id"],
                "candidate_source_sha256": candidate_hashes,
                "source_proximity_reporting_stratum": f"{proximity.upper()}_NECESSARY_SOURCE_BODY_PROXIMITY_NOT_UNIFORMLY_HARD",
                "source_body_echo_note": cueing["source_body_echo"],
                "composition_reporting_stratum": composition_stratum,
                "composition_note": composition_note,
                "cue_assessment": {
                    "necessary_cues": cueing.get("necessary_cues", []),
                    "gratuitous_cues": cueing.get("gratuitous_cues", []),
                    "source_body_echo": cueing["source_body_echo"],
                },
                "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                "admission_status": "ADMITTED_RQ2_NATIVE_TECHNICAL_WAVE_001_PENDING_FINAL_FREEZE",
            })
            reconciliation_rows.append({
                "prompt_id": prompt_id,
                "cluster_id": cluster_id,
                "author_intended_source_sha256": intended_hash,
                "blind_review_fully_adequate_alias": full_alias,
                "blind_review_fully_adequate_source_sha256": reviewed_hash,
                "packet_candidate_source_sha256": packet_hashes,
                "result": "PASS_EXACT_AUTHOR_REVIEW_RECONCILIATION",
            })

        if reviewed_targets != set(candidate_hashes):
            raise SystemExit(f"Every promoted cluster member must have one admitted prompt: {cluster_id}")
        cluster_rows.append({
            "cluster_id": cluster_id,
            "cluster_origin": "RQ2_NATIVE_PUBLIC_POOL_DISCOVERY",
            "common_envelope": lead["common_envelope"],
            "candidate_ids": [candidate["skill_id"] for candidate in candidates],
            "candidate_source_sha256": candidate_hashes,
            "prompt_ids": prompt_ids,
            "origin_stratum": lead["origin_stratum"],
            "source_proximity_reporting_stratum": "HIGH_OR_MODERATE_NECESSARY_SOURCE_BODY_PROXIMITY_NOT_UNIFORMLY_HARD",
            "observed_source_body_proximity_levels": sorted(set(cluster_proximity_levels)),
            "composition_reporting_strata": sorted(set(cluster_composition_strata)),
            "admission_status": "ADMITTED_RQ2_NATIVE_TECHNICAL_WAVE_001_PENDING_FINAL_FREEZE",
            "claim_boundary": (
                "Source-grounded model-assisted curatorial admission with retained proximity and composition strata; "
                "not human annotation, final gold, uniform difficulty, representativeness, or a retrieval result."
            ),
        })

    if len(cluster_rows) != EXPECTED_CLUSTER_COUNT or len(prompt_rows) != EXPECTED_PROMPT_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_CLUSTER_COUNT} clusters and {EXPECTED_PROMPT_COUNT} prompts, "
            f"found {len(cluster_rows)}/{len(prompt_rows)}"
        )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    cluster_path = OUTPUT / "admitted_cluster_manifest.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest.jsonl"
    reconciliation_path = OUTPUT / "author_review_reconciliation.jsonl"
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)
    write_jsonl(reconciliation_path, reconciliation_rows)
    summary = {
        "status": "PASS_RQ2_NATIVE_TECHNICAL_WAVE_001_PRE_FREEZE_ADMISSION_NOT_FINAL_GOLD_OR_RESULT",
        "pre_freeze_candidate_union_count": len(union_rows),
        "new_source_rows_added_to_union": 0,
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "admitted_distinct_source_count": len({h for row in cluster_rows for h in row["candidate_source_sha256"]}),
        "source_proximity_reporting_strata": dict(sorted(proximity_counts.items())),
        "composition_reporting_strata": dict(sorted(composition_counts.items())),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            path.name: sha256_file(path)
            for path in [cluster_path, prompt_path, reconciliation_path]
        },
        "claim_boundary": [
            "Nine promoted clusters and 27 prompts pass current-union membership, source-byte replay, exact target-blinded packet roster, singleton adequacy, no-gratuitous-cue, author-target reconciliation, optional-composition, and cluster-completeness gates.",
            "All 27 sources were already present in the 3,084-source current pre-freeze union; no source is admitted or added by this controller.",
            "High and moderate necessary source/body proximity plus composition notes are retained as reporting strata; they do not establish uniform difficulty or ecological representativeness.",
            "No final acceptable set, strict gold, representation, retrieval run, metric, or thesis result is produced.",
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
