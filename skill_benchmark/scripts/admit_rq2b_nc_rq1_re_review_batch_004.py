#!/usr/bin/env python3
"""Admit passing RQ1-derived batch 004 while preserving cue/provenance strata."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
UNION_IN = BASE / "manifests/current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
DECISIONS = BASE / "review/rq1_frozen_cluster_re_review_batch_004_2026-08-31.jsonl"
AUTHORS = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_004_private_2026-08-31.jsonl"
PACKETS = BASE / "review/rq1_frozen_cluster_reauthored_batch_004_target_blinded_packets_2026-08-31.jsonl"
RESULTS = BASE / "review/rq1_frozen_cluster_reauthored_batch_004_target_blinded_results_2026-08-31.jsonl"
PROVENANCE = BASE / "manifests/rq1_frozen_source_provenance_2026-08-31/source_provenance_audit.jsonl"
OUTPUT = BASE / "manifests/rq1_re_review_batch_004_pre_freeze_admission_2026-08-31"
DEFER_ORDER = 78


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def build_union_row(audit: dict[str, Any], skill_id: str) -> dict[str, Any]:
    source_hash = str(audit["source_sha256"])
    binding = dict(audit["selected_provenance_binding"])
    source_path = ROOT / str(binding["original_path"])
    license_path = Path(str(binding["local_license_path"]))
    import_path = ROOT / str(binding["import_metadata_path"])
    if not source_path.is_file() or sha256_file(source_path) != source_hash:
        raise SystemExit(f"Source replay failed: {source_path}")
    if not license_path.is_file() or sha256_file(license_path) != str(binding["license_sha256"]):
        raise SystemExit(f"Licence replay failed: {license_path}")
    if not import_path.is_file() or sha256_file(import_path) != str(binding["import_metadata_sha256"]):
        raise SystemExit(f"Import metadata replay failed: {import_path}")
    return {
        "canonical_source_sha256": source_hash,
        "final_intake_role": "RQ2B_NC_RQ1_REVIEWED_NEW_SOURCE_CANDIDATE",
        "provenance_binding": {
            "import_metadata_path": binding["import_metadata_path"],
            "import_metadata_sha256": binding["import_metadata_sha256"],
            "license_declared": binding["license_declared"],
            "license_path": binding["license_path"],
            "license_sha256": binding["license_sha256"],
            "local_license_hash_matches_record": binding["local_license_hash_matches_record"],
            "local_license_path": str(license_path.relative_to(ROOT)),
            "origin": binding["origin"],
            "pinned_reference": binding["pinned_reference"],
            "repository_url": binding["repository_url"],
            "source_hash_matches_inventory": binding["original_hash_matches_source_sha256"],
            "source_path": binding["original_path"],
            "source_url": binding["source_url"],
            "status": audit["status"],
        },
        "rq1_duplicate_alias_count": 0,
        "rq1_records": [{
            "frontmatter_name": skill_id,
            "skill_id": skill_id,
            "source_path": str(source_path.relative_to(ROOT.parent)),
        }],
        "status": audit["status"],
    }


def main() -> int:
    required = [UNION_IN, DECISIONS, AUTHORS, PACKETS, RESULTS, PROVENANCE]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required artifacts: {missing}")
    union_rows = read_jsonl(UNION_IN)
    union_by_hash = {str(row["canonical_source_sha256"]): row for row in union_rows}
    if len(union_rows) != 3082 or len(union_by_hash) != 3082:
        raise SystemExit("Expected 3,082-row current pre-freeze union")

    all_promoted = [row for row in read_jsonl(DECISIONS) if row["disposition"] == "PROMOTE_TO_RQ2_PROMPT_AUTHORING"]
    admitted_decisions = [row for row in all_promoted if int(row["review_order"]) != DEFER_ORDER]
    deferred_decisions = [row for row in all_promoted if int(row["review_order"]) == DEFER_ORDER]
    if len(admitted_decisions) != 13 or len(deferred_decisions) != 1:
        raise SystemExit("Expected 13 admitted and one provenance-deferred batch-004 clusters")
    provenance_by_hash = {str(row["source_sha256"]): row for row in read_jsonl(PROVENANCE)}

    added_rows: list[dict[str, Any]] = []
    for decision in admitted_decisions:
        for boundary in decision["necessary_candidate_boundaries"]:
            evidence = boundary["source_evidence"]
            source_hash = str(evidence["source_sha256"])
            source_path = Path(str(evidence["source_path"]))
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"Source replay failed: {source_path}")
            if source_hash in union_by_hash:
                continue
            if decision["nc_intake_arm"] != "NC-S_NEW_SOURCE_INTAKE_LEAD":
                raise SystemExit(f"Absent NC-P parent source: {source_hash}")
            audit = provenance_by_hash.get(source_hash)
            if audit is None or audit["status"] != "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH":
                raise SystemExit(f"Absent NC-S source lacks full provenance pass: {source_hash}")
            row = build_union_row(audit, str(boundary["candidate_skill_id"]))
            union_by_hash[source_hash] = row
            added_rows.append(row)
    union_rows = sorted(union_by_hash.values(), key=lambda row: str(row["canonical_source_sha256"]))
    if len(added_rows) != 2 or len(union_rows) != 3084:
        raise SystemExit(f"Expected two added SEO sources and 3,084 union rows, found {len(added_rows)}/{len(union_rows)}")

    authors = {str(row["prompt_id"]): row for row in read_jsonl(AUTHORS)}
    packets = {str(row["prompt_id"]): row for row in read_jsonl(PACKETS)}
    results = {str(row["prompt_id"]): row for row in read_jsonl(RESULTS)}
    cluster_rows: list[dict[str, Any]] = []
    prompt_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []
    for decision in admitted_decisions:
        queue_id = str(decision["review_queue_id"])
        boundaries = decision["necessary_candidate_boundaries"]
        candidate_hashes = [str(row["source_evidence"]["source_sha256"]) for row in boundaries]
        queue_authors = [row for row in authors.values() if str(row["review_queue_id"]) == queue_id]
        if len(queue_authors) != len(boundaries):
            raise SystemExit(f"Prompt coverage mismatch: {queue_id}")
        prompt_ids: list[str] = []
        reviewed_targets: set[str] = set()
        cue_levels: list[str] = []
        for author in queue_authors:
            prompt_id = str(author["prompt_id"])
            packet = packets[prompt_id]
            result = results[prompt_id]
            if result["packet_id"] != packet["packet_id"]:
                raise SystemExit(f"Packet/result binding mismatch: {prompt_id}")
            full = [row for row in result["candidate_assessments"] if row["classification"] == "fully_adequate"]
            if len(full) != 1 or result["multi_full_risk"]["level"] != "low":
                raise SystemExit(f"Prompt lacks a single low-risk full route: {prompt_id}")
            if result["cueing"]["gratuitous"]:
                raise SystemExit(f"Prompt retains gratuitous cueing: {prompt_id}")
            full_source = next(row for row in packet["candidates"] if row["alias"] == full[0]["alias"])
            intended = str(author["author_intended_candidate_source_sha256"])
            if str(full_source["source_sha256"]) != intended:
                raise SystemExit(f"Blind review and author target disagree: {prompt_id}")
            if set(str(row["source_sha256"]) for row in packet["candidates"]) != set(candidate_hashes):
                raise SystemExit(f"Packet roster mismatch: {prompt_id}")
            prompt_ids.append(prompt_id)
            reviewed_targets.add(intended)
            cue_levels.append(str(result["source_body_echo"]["level"]))
            prompt_rows.append({
                "prompt_id": prompt_id,
                "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
                "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
                "nc_intake_arm": decision["nc_intake_arm"],
                "prompt": author["prompt"],
                "reviewed_single_fully_adequate_source_sha256": intended,
                "candidate_source_sha256": candidate_hashes,
                "cue_review": {
                    "cueing": result["cueing"],
                    "source_body_echo": result["source_body_echo"],
                    "reporting_stratum": "HIGH_OR_MODERATE_NECESSARY_SOURCE_PROXIMITY_NOT_UNIFORMLY_HARD",
                },
                "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_004_PENDING_FINAL_FREEZE",
            })
            reconciliation_rows.append({
                "prompt_id": prompt_id,
                "review_queue_id": queue_id,
                "author_intended_source_sha256": intended,
                "blind_review_fully_adequate_source_sha256": str(full_source["source_sha256"]),
                "result": "PASS_EXACT_AUTHOR_REVIEW_RECONCILIATION",
            })
        if reviewed_targets != set(candidate_hashes):
            raise SystemExit(f"Not every candidate has a passing prompt: {queue_id}")
        cluster_rows.append({
            "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
            "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
            "review_queue_id": queue_id,
            "nc_intake_arm": decision["nc_intake_arm"],
            "cluster_origin": "RQ1_SOURCE_MEMBERSHIP_REREAD_FROM_FULL_SOURCES_NO_PROMPT_OR_LABEL_TRANSFER",
            "common_envelope": decision["bounded_shared_envelope"],
            "candidate_ids": decision["candidate_skill_ids"],
            "candidate_source_sha256": candidate_hashes,
            "prompt_ids": sorted(prompt_ids),
            "cue_reporting_stratum": "HIGH_OR_MODERATE_NECESSARY_SOURCE_PROXIMITY_NOT_UNIFORMLY_HARD",
            "observed_source_body_echo_levels": sorted(set(cue_levels)),
            "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_004_PENDING_FINAL_FREEZE",
            "claim_boundary": "No RQ1 prompt or label transferred; high necessary cue proximity is retained for stratified reporting.",
        })

    deferred = [{
        "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
        "review_order": decision["review_order"],
        "candidate_ids": decision["candidate_skill_ids"],
        "disposition": "DEFER_CLUSTER_PROVENANCE_GATE",
        "reason": "Pinned sources exist, but the declared licence file was not independently hash verified.",
        "status": "NOT_ADMITTED_NOT_GOLD_NOT_EXPERIMENT_INPUT",
    } for decision in deferred_decisions]
    if len(cluster_rows) != 13 or len(prompt_rows) != 26:
        raise SystemExit(f"Expected 13 clusters and 26 prompts, found {len(cluster_rows)}/{len(prompt_rows)}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    union_path = OUTPUT / "canonical_candidate_union_rq1_batch_004.jsonl"
    cluster_path = OUTPUT / "admitted_cluster_manifest.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest.jsonl"
    reconciliation_path = OUTPUT / "author_review_reconciliation.jsonl"
    deferred_path = OUTPUT / "deferred_cluster_manifest.jsonl"
    write_jsonl(union_path, union_rows)
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)
    write_jsonl(reconciliation_path, reconciliation_rows)
    write_jsonl(deferred_path, deferred)
    summary = {
        "status": "PASS_RQ1_DERIVED_BATCH_004_PRE_FREEZE_ADMISSION_NOT_FINAL_GOLD_OR_RESULT",
        "parent_candidate_source_count": 3082,
        "candidate_source_count": len(union_rows),
        "new_source_rows_added": len(added_rows),
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "deferred_cluster_count": len(deferred),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {path.name: sha256_file(path) for path in [union_path, cluster_path, prompt_path, reconciliation_path, deferred_path]},
        "claim_boundary": [
            "Thirteen clusters and 26 prompts pass source replay, singleton adequacy, no-gratuitous-cue, low-multi-full, author-target reconciliation, and cluster-completeness gates.",
            "The prompts are retained in a high-or-moderate necessary source-proximity stratum and must not be described as uniformly hard.",
            "The scientific-writing/peer-review cluster is deferred because its licence file has not been independently hash verified.",
            "Two fully pinned SEO sources extend the current pre-freeze union from 3,082 to 3,084 rows.",
            "No final acceptable set, strict gold, representation, retrieval, metric, or thesis result is produced."
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
