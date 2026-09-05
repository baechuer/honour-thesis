#!/usr/bin/env python3
"""Fail-closed pre-freeze admission for reviewed RQ1-derived batch 002.

The RQ1 source clusters are leads only.  This controller replays the preserved
source bytes, checks the target-blinded rewrite review, and emits pre-freeze
admission manifests only.  It neither transfers RQ1 labels nor creates final
gold, representations, selector results, or metrics.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
UNION = BASE / "manifests/rq1_re_review_batch_004_pre_freeze_admission_2026-08-31/canonical_candidate_union_rq1_batch_004.jsonl"
DECISIONS = BASE / "review/rq1_frozen_cluster_re_review_batch_002_2026-08-31.jsonl"
AUTHORS = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_002_rewrite_private_2026-08-31.jsonl"
PACKETS = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_packets_2026-08-31.jsonl"
ORIGINAL_RESULTS = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_results_2026-08-31.jsonl"
RESULTS = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_results_clerical_corrected_2026-08-31.jsonl"
CORRECTION_RECORD = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_results_clerical_correction_2026-08-31.json"
ORIGINAL_DEFERRED = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_deferred_after_blind_review_2026-08-31.jsonl"
PROVENANCE_AUDIT = BASE / "manifests/rq1_frozen_source_provenance_2026-08-31/source_provenance_audit.jsonl"
OUTPUT = BASE / "manifests/rq1_re_review_batch_002_pre_freeze_admission_2026-08-31"

DEFER_REVIEW_ORDER = 27
EXPECTED_UNION_COUNT = 3084
EXPECTED_ADMITTED_CLUSTERS = 10
EXPECTED_ADMITTED_PROMPTS = 20
CORRECTION_PROMPT_ID = "RQ2B-NC-RQ1-REAUTH-B002-R1-030-02"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def source_path_from_evidence(evidence: dict[str, Any]) -> Path:
    """Resolve the recorded absolute source path without guessing a substitute."""
    source_path = Path(str(evidence["source_path"]))
    if not source_path.is_file():
        raise SystemExit(f"Recorded source is unavailable: {source_path}")
    return source_path


def verify_disclosed_clerical_correction() -> None:
    """Allow only the recorded alias swap; every other result row stays byte-identical."""
    record = json.loads(CORRECTION_RECORD.read_text(encoding="utf-8"))
    if record.get("prompt_id") != CORRECTION_PROMPT_ID:
        raise SystemExit("Correction record targets an unexpected prompt")
    expected_hashes = {
        "original_results_sha256": sha256_file(ORIGINAL_RESULTS),
        "packet_sha256": sha256_file(PACKETS),
        "corrected_results_sha256": sha256_file(RESULTS),
    }
    if any(record.get(key) != value for key, value in expected_hashes.items()):
        raise SystemExit("Correction record hash replay failed")
    if record.get("classification_before") != [
        {"alias": "A", "classification": "inadequate"},
        {"alias": "B", "classification": "fully_adequate"},
    ] or record.get("classification_after") != [
        {"alias": "A", "classification": "fully_adequate"},
        {"alias": "B", "classification": "inadequate"},
    ]:
        raise SystemExit("Correction record does not describe only the disclosed alias swap")
    if not record.get("no_scientific_judgment_drift", {}).get("unchanged_prompt_source_roster_rationales"):
        raise SystemExit("Correction record lacks no-scientific-judgment-drift attestation")

    original_raw = {
        str(row["prompt_id"]): line
        for line in ORIGINAL_RESULTS.read_text(encoding="utf-8").splitlines() if line.strip()
        for row in [json.loads(line)]
    }
    corrected_raw = {
        str(row["prompt_id"]): line
        for line in RESULTS.read_text(encoding="utf-8").splitlines() if line.strip()
        for row in [json.loads(line)]
    }
    if set(original_raw) != set(corrected_raw) or len(original_raw) != EXPECTED_ADMITTED_PROMPTS:
        raise SystemExit("Corrected result roster differs from the original roster")
    for prompt_id, original_line in original_raw.items():
        if prompt_id != CORRECTION_PROMPT_ID and corrected_raw[prompt_id] != original_line:
            raise SystemExit(f"Non-target result row changed: {prompt_id}")

    original_target = json.loads(original_raw[CORRECTION_PROMPT_ID])
    corrected_target = json.loads(corrected_raw[CORRECTION_PROMPT_ID])
    expected_target = json.loads(json.dumps(original_target))
    for candidate in expected_target["candidates"]:
        candidate["classification"] = "fully_adequate" if candidate["alias"] == "A" else "inadequate"
    if corrected_target != expected_target:
        raise SystemExit("Corrected target changes more than the disclosed classifications")


def main() -> int:
    required = [
        UNION,
        DECISIONS,
        AUTHORS,
        PACKETS,
        ORIGINAL_RESULTS,
        RESULTS,
        CORRECTION_RECORD,
        ORIGINAL_DEFERRED,
        PROVENANCE_AUDIT,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required artifacts: {missing}")
    verify_disclosed_clerical_correction()

    union_rows = read_jsonl(UNION)
    union_hashes = [str(row["canonical_source_sha256"]) for row in union_rows]
    union_hash_set = set(union_hashes)
    if len(union_rows) != EXPECTED_UNION_COUNT or len(union_hash_set) != EXPECTED_UNION_COUNT:
        raise SystemExit(f"Expected a {EXPECTED_UNION_COUNT}-row hash-unique current union")

    decisions = read_jsonl(DECISIONS)
    promoted = [row for row in decisions if row["disposition"] == "PROMOTE_TO_RQ2_PROMPT_AUTHORING"]
    admitted_decisions = [row for row in promoted if int(row["review_order"]) != DEFER_REVIEW_ORDER]
    deferred_decisions = [row for row in promoted if int(row["review_order"]) == DEFER_REVIEW_ORDER]
    if len(promoted) != EXPECTED_ADMITTED_CLUSTERS + 1:
        raise SystemExit("Expected exactly 11 promoted batch-002 source decisions")
    if len(admitted_decisions) != EXPECTED_ADMITTED_CLUSTERS or len(deferred_decisions) != 1:
        raise SystemExit("Expected ten admitted clusters and review_order 27 as the sole deferred cluster")

    authors = {str(row["prompt_id"]): row for row in read_jsonl(AUTHORS)}
    packets = {str(row["prompt_id"]): row for row in read_jsonl(PACKETS)}
    results = {str(row["prompt_id"]): row for row in read_jsonl(RESULTS)}
    if len(authors) != EXPECTED_ADMITTED_PROMPTS or set(authors) != set(packets) or set(authors) != set(results):
        raise SystemExit("Rewrite author, packet, and result prompt rosters must be identical 20-prompt sets")

    provenance_by_hash = {str(row["source_sha256"]): row for row in read_jsonl(PROVENANCE_AUDIT)}
    cluster_rows: list[dict[str, Any]] = []
    prompt_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []
    nc_p_source_hashes: set[str] = set()
    nc_s_source_hashes: set[str] = set()

    for decision in admitted_decisions:
        queue_id = str(decision["review_queue_id"])
        boundaries = list(decision["necessary_candidate_boundaries"])
        candidate_hashes = [str(row["source_evidence"]["source_sha256"]) for row in boundaries]
        if len(boundaries) != 2 or len(candidate_hashes) != len(set(candidate_hashes)):
            raise SystemExit(f"Expected two distinct source candidates: {queue_id}")
        if not set(candidate_hashes).issubset(union_hash_set):
            absent = sorted(set(candidate_hashes) - union_hash_set)
            raise SystemExit(f"Cluster source absent from current union: {queue_id}: {absent}")

        for boundary in boundaries:
            evidence = dict(boundary["source_evidence"])
            source_hash = str(evidence["source_sha256"])
            source_path = source_path_from_evidence(evidence)
            if sha256_file(source_path) != source_hash:
                raise SystemExit(f"Source-byte replay failed: {source_path}")
            if decision["nc_intake_arm"] == "NC-S_NEW_SOURCE_INTAKE_LEAD":
                audit = provenance_by_hash.get(source_hash)
                if audit is None or audit["status"] != "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH":
                    raise SystemExit(f"NC-S source lacks passing provenance audit: {source_path}")
                nc_s_source_hashes.add(source_hash)
            elif decision["nc_intake_arm"] == "NC-P_EXISTING_V3_PROMPT_LEAD":
                nc_p_source_hashes.add(source_hash)
            else:
                raise SystemExit(f"Unknown NC intake arm: {decision['nc_intake_arm']}")

        queue_authors = [row for row in authors.values() if str(row["review_queue_id"]) == queue_id]
        if len(queue_authors) != len(boundaries):
            raise SystemExit(f"Rewritten prompt coverage mismatch: {queue_id}")
        prompt_ids: list[str] = []
        reviewed_targets: set[str] = set()
        echo_levels: list[str] = []
        for author in sorted(queue_authors, key=lambda row: str(row["prompt_id"])):
            prompt_id = str(author["prompt_id"])
            packet = packets[prompt_id]
            result = results[prompt_id]
            if str(packet["packet_id"]) != str(result["packet_id"]):
                raise SystemExit(f"Packet/result binding mismatch: {prompt_id}")
            if str(packet["prompt"]) != str(author["prompt"]):
                raise SystemExit(f"Author/packet prompt mismatch: {prompt_id}")
            if str(result["source_sha256_verification"]) != "all_packet_sources_verified":
                raise SystemExit(f"Packet source verification failed: {prompt_id}")
            packet_hashes = {str(row["source_sha256"]) for row in packet["candidates"]}
            if packet_hashes != set(candidate_hashes):
                raise SystemExit(f"Packet roster mismatch: {prompt_id}")
            full = [row for row in result["candidates"] if row["classification"] == "fully_adequate"]
            if len(full) != 1:
                raise SystemExit(f"Expected exactly one fully adequate alias: {prompt_id}")
            if str(result["relationship_assessment"]["multi_full_risk"]).lower() not in {"no", "low"}:
                raise SystemExit(f"Multi-full risk is not low/no: {prompt_id}")
            if "not required" not in str(result["relationship_assessment"]["composition"]).lower():
                raise SystemExit(f"Required workflow composition remains: {prompt_id}")
            if str(result["cueing_assessment"]["gratuitous_cues"]).lower() not in {"none", "none identified"}:
                raise SystemExit(f"Prompt retains gratuitous cueing: {prompt_id}")
            echo = str(result["cueing_assessment"]["source_body_echo"])
            if not echo.lower().startswith(("low", "moderate")):
                raise SystemExit(f"Source proximity is outside the low/moderate stratum: {prompt_id}")
            aliases = {str(row["alias"]): str(row["source_sha256"]) for row in packet["candidates"]}
            full_alias = str(full[0]["alias"])
            if full_alias not in aliases:
                raise SystemExit(f"Full alias absent from packet: {prompt_id}")
            intended = str(author["author_intended_candidate_source_sha256"])
            full_source = aliases[full_alias]
            if full_source != intended:
                raise SystemExit(f"Blind full source and private author target disagree: {prompt_id}")

            prompt_ids.append(prompt_id)
            reviewed_targets.add(intended)
            echo_levels.append(echo.split(";", 1)[0].strip().upper())
            prompt_rows.append({
                "prompt_id": prompt_id,
                "supersedes_prompt_id": author["supersedes_prompt_id"],
                "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
                "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
                "review_queue_id": queue_id,
                "nc_intake_arm": decision["nc_intake_arm"],
                "prompt": author["prompt"],
                "reviewed_single_fully_adequate_source_sha256": intended,
                "candidate_source_sha256": candidate_hashes,
                "cue_review": result["cueing_assessment"],
                "relationship_review": result["relationship_assessment"],
                "cue_reporting_stratum": "LOW_OR_MODERATE_NECESSARY_SOURCE_PROXIMITY",
                "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_002_PENDING_FINAL_FREEZE",
            })
            reconciliation_rows.append({
                "prompt_id": prompt_id,
                "review_queue_id": queue_id,
                "author_intended_source_sha256": intended,
                "blind_review_fully_adequate_alias": full_alias,
                "blind_review_fully_adequate_source_sha256": full_source,
                "result": "PASS_EXACT_AUTHOR_REVIEW_RECONCILIATION",
            })
        if reviewed_targets != set(candidate_hashes):
            raise SystemExit(f"Not every cluster member has one passing rewritten prompt: {queue_id}")
        cluster_rows.append({
            "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
            "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
            "review_queue_id": queue_id,
            "review_order": decision["review_order"],
            "nc_intake_arm": decision["nc_intake_arm"],
            "cluster_origin": "RQ1_SOURCE_MEMBERSHIP_REREAD_FROM_FULL_SOURCES_NO_PROMPT_OR_LABEL_TRANSFER",
            "common_envelope": decision["bounded_shared_envelope"],
            "candidate_ids": decision["candidate_skill_ids"],
            "candidate_source_sha256": candidate_hashes,
            "prompt_ids": prompt_ids,
            "provenance_stratum": (
                "PINNED_NEW_SOURCE_INTAKE" if decision["nc_intake_arm"] == "NC-S_NEW_SOURCE_INTAKE_LEAD"
                else "LEGACY_PARENT_V3_EXACT_SOURCE_PROMPT_ONLY"
            ),
            "cue_reporting_stratum": "LOW_OR_MODERATE_NECESSARY_SOURCE_PROXIMITY",
            "observed_source_body_echo_levels": sorted(set(echo_levels)),
            "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_002_PENDING_FINAL_FREEZE",
            "claim_boundary": "No RQ1 prompt, label, selector output, metric, or result was transferred.",
        })

    deferred_original_rows = read_jsonl(ORIGINAL_DEFERRED)
    if len(deferred_original_rows) != 1:
        raise SystemExit("Expected exactly one original deferred-after-review record")
    deferred_original = deferred_original_rows[0]
    deferred_decision = deferred_decisions[0]
    if (
        str(deferred_original["review_queue_id"]) != str(deferred_decision["review_queue_id"])
        or str(deferred_original["parent_rq1_cluster_id"]) != str(deferred_decision["parent_rq1_cluster_id"])
    ):
        raise SystemExit("Original deferred manifest does not bind to review_order 27")
    if "provider cue" not in str(deferred_original["reason"]).lower():
        raise SystemExit("Deferred review_order 27 must remain deferred for the provider-cue reason")
    deferred_rows = [{
        "cluster_id": f"RQ2B-NC-RQ1-{deferred_decision['parent_rq1_cluster_id']}",
        "review_order": deferred_decision["review_order"],
        "review_queue_id": deferred_decision["review_queue_id"],
        "parent_rq1_cluster_id": deferred_decision["parent_rq1_cluster_id"],
        "candidate_ids": deferred_decision["candidate_skill_ids"],
        "candidate_source_sha256": [
            str(row["source_evidence"]["source_sha256"])
            for row in deferred_decision["necessary_candidate_boundaries"]
        ],
        "disposition": "DEFER_CLUSTER_AFTER_TARGET_BLINDED_REVIEW",
        "reason": deferred_original["reason"],
        "status": "NOT_ADMITTED_NOT_GOLD_NOT_EXPERIMENT_INPUT",
    }]

    if len(cluster_rows) != EXPECTED_ADMITTED_CLUSTERS or len(prompt_rows) != EXPECTED_ADMITTED_PROMPTS:
        raise SystemExit(
            f"Expected {EXPECTED_ADMITTED_CLUSTERS} clusters and {EXPECTED_ADMITTED_PROMPTS} prompts, "
            f"found {len(cluster_rows)}/{len(prompt_rows)}"
        )
    if len(deferred_rows) != 1:
        raise SystemExit("Expected exactly one deferred cluster")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    cluster_path = OUTPUT / "admitted_cluster_manifest.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest.jsonl"
    reconciliation_path = OUTPUT / "author_review_reconciliation.jsonl"
    deferred_path = OUTPUT / "deferred_cluster_manifest.jsonl"
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)
    write_jsonl(reconciliation_path, reconciliation_rows)
    write_jsonl(deferred_path, deferred_rows)
    output_paths = [cluster_path, prompt_path, reconciliation_path, deferred_path]
    summary = {
        "status": "PASS_RQ1_DERIVED_BATCH_002_PRE_FREEZE_ADMISSION_NOT_FINAL_GOLD_OR_RESULT",
        "current_pre_freeze_candidate_union_count": len(union_rows),
        "new_source_rows_added_to_union": 0,
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "deferred_cluster_count": len(deferred_rows),
        "admitted_distinct_source_count": len({source for row in cluster_rows for source in row["candidate_source_sha256"]}),
        "nc_p_cluster_count": sum(row["nc_intake_arm"] == "NC-P_EXISTING_V3_PROMPT_LEAD" for row in cluster_rows),
        "nc_s_cluster_count": sum(row["nc_intake_arm"] == "NC-S_NEW_SOURCE_INTAKE_LEAD" for row in cluster_rows),
        "nc_p_source_count": len(nc_p_source_hashes),
        "nc_s_source_count": len(nc_s_source_hashes),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {path.name: sha256_file(path) for path in output_paths},
        "claim_boundary": [
            "Ten clusters and 20 rewritten prompts pass source-byte replay, current-union membership, singleton adequacy, low/no multi-full, no-required-composition, no-gratuitous-cue, author-target reconciliation, and full-member coverage gates.",
            "Low and moderate necessary source proximity is retained as a reporting stratum; it is not a claim that every case is equally difficult.",
            "NC-P cases preserve the legacy parent-V3 exact-source stratum, while NC-S cases preserve passing pinned-source provenance audit evidence.",
            "Review order 27 remains deferred: its platform-specific source would require a provider-name cue to become fully adequate.",
            "No final acceptable set, strict gold, representation, selector output, retrieval run, metric, or thesis result is produced.",
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
