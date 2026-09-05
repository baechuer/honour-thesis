#!/usr/bin/env python3
"""Admit fully reviewed RQ1-derived batch-001 clusters to NC pre-freeze.

RQ1 source memberships are treated only as leads.  This controller selects the
latest independently reviewed naturalistic prompt per candidate, reconciles it
to the private author intent, and records NC-P versus NC-S provenance strata.
It does not transfer an RQ1 prompt/label or create final gold.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
UNION = BASE / "manifests/reviewed_wave_001_admission_2026-08-31/canonical_candidate_union_reviewed_wave_001.jsonl"
DECISIONS = BASE / "review/rq1_frozen_cluster_re_review_batch_001_2026-08-31.jsonl"
AUTHORS_INITIAL = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_001_private_2026-08-31.jsonl"
AUTHORS_REWRITE = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_001_rewrite_private_2026-08-31.jsonl"
PACKETS_INITIAL = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_target_blinded_packets_2026-08-31.jsonl"
PACKETS_REWRITE = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_rewrite_target_blinded_packets_2026-08-31.jsonl"
RESULTS_INITIAL = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_target_blinded_results_2026-08-31.jsonl"
RESULTS_REWRITE = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_rewrite_target_blinded_results_2026-08-31.jsonl"
PROVENANCE_AUDIT = BASE / "manifests/rq1_frozen_source_provenance_2026-08-31/source_provenance_audit.jsonl"
OUTPUT = BASE / "manifests/rq1_re_review_batch_001_pre_freeze_admission_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def full_hash(result: dict[str, Any]) -> str:
    full = [row for row in result["candidate_reviews"] if row["adequacy"] == "fully_adequate"]
    if len(full) != 1:
        raise SystemExit(f"Expected one fully adequate candidate: {result['prompt_id']}")
    return str(full[0]["source_sha256"])


def main() -> int:
    required = [
        UNION, DECISIONS, AUTHORS_INITIAL, AUTHORS_REWRITE, PACKETS_INITIAL,
        PACKETS_REWRITE, RESULTS_INITIAL, RESULTS_REWRITE, PROVENANCE_AUDIT,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required artifacts: {missing}")

    union_rows = read_jsonl(UNION)
    union_by_hash = {str(row["canonical_source_sha256"]): row for row in union_rows}
    if len(union_rows) != 3076 or len(union_by_hash) != 3076:
        raise SystemExit("Expected 3,076-row hash-unique pre-freeze candidate union")

    promoted = [row for row in read_jsonl(DECISIONS) if row["disposition"] == "PROMOTE_TO_RQ2_PROMPT_AUTHORING"]
    if len(promoted) != 10:
        raise SystemExit(f"Expected 10 promoted clusters, found {len(promoted)}")

    initial_authors = {str(row["prompt_id"]): row for row in read_jsonl(AUTHORS_INITIAL)}
    rewrite_authors = {str(row["prompt_id"]): row for row in read_jsonl(AUTHORS_REWRITE)}
    initial_packets = {str(row["prompt_id"]): row for row in read_jsonl(PACKETS_INITIAL)}
    rewrite_packets = {str(row["prompt_id"]): row for row in read_jsonl(PACKETS_REWRITE)}
    initial_results = {str(row["prompt_id"]): row for row in read_jsonl(RESULTS_INITIAL)}
    rewrite_results = {str(row["prompt_id"]): row for row in read_jsonl(RESULTS_REWRITE)}
    rewrite_for_original = {str(row["supersedes_prompt_id"]): pid for pid, row in rewrite_authors.items()}

    provenance_by_hash = {str(row["source_sha256"]): row for row in read_jsonl(PROVENANCE_AUDIT)}
    added_source_rows: list[dict[str, Any]] = []
    for decision in promoted:
        for boundary in decision["necessary_candidate_boundaries"]:
            source_hash = str(boundary["source_evidence"]["source_sha256"])
            if source_hash in union_by_hash:
                continue
            if decision["nc_intake_arm"] != "NC-S_NEW_SOURCE_INTAKE_LEAD":
                raise SystemExit(f"NC-P candidate is unexpectedly absent from the parent union: {source_hash}")
            audit = provenance_by_hash.get(source_hash)
            if audit is None or audit["status"] != "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH":
                raise SystemExit(f"Missing passing provenance audit for NC-S source: {source_hash}")
            binding = dict(audit["selected_provenance_binding"])
            source_path = ROOT / str(binding["original_path"])
            license_path = Path(str(binding["local_license_path"]))
            import_path = ROOT / str(binding["import_metadata_path"])
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"NC-S source replay failed: {source_path}")
            if not license_path.is_file() or sha256_file(license_path) != str(binding["license_sha256"]):
                raise SystemExit(f"NC-S licence replay failed: {license_path}")
            if not import_path.is_file() or sha256_file(import_path) != str(binding["import_metadata_sha256"]):
                raise SystemExit(f"NC-S import metadata replay failed: {import_path}")
            provenance_binding = {
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
            }
            added = {
                "canonical_source_sha256": source_hash,
                "final_intake_role": "RQ2B_NC_RQ1_REVIEWED_NEW_SOURCE_CANDIDATE",
                "provenance_binding": provenance_binding,
                "rq1_duplicate_alias_count": 0,
                "rq1_records": [{
                    "frontmatter_name": boundary["candidate_skill_id"],
                    "skill_id": boundary["candidate_skill_id"],
                    "source_path": str(source_path.relative_to(ROOT.parent)),
                }],
                "status": audit["status"],
            }
            added_source_rows.append(added)
            union_by_hash[source_hash] = added

    union_rows = sorted(union_by_hash.values(), key=lambda row: str(row["canonical_source_sha256"]))
    if len(added_source_rows) != 6 or len(union_rows) != 3082:
        raise SystemExit(f"Expected six admitted NC-S sources and a 3,082-row union, found {len(added_source_rows)}/{len(union_rows)}")

    cluster_rows: list[dict[str, Any]] = []
    prompt_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []
    legacy_parent_source_hashes: set[str] = set()
    pinned_new_source_hashes: set[str] = set()
    for decision in promoted:
        queue_id = str(decision["review_queue_id"])
        boundaries = decision["necessary_candidate_boundaries"]
        candidate_hashes = [str(row["source_evidence"]["source_sha256"]) for row in boundaries]
        if len(candidate_hashes) != len(set(candidate_hashes)):
            raise SystemExit(f"Duplicate cluster source hash: {queue_id}")
        if not set(candidate_hashes).issubset(union_by_hash):
            raise SystemExit(f"Cluster source absent from union: {queue_id}")

        for boundary in boundaries:
            evidence = boundary["source_evidence"]
            source_path = Path(str(evidence["source_path"]))
            if not source_path.is_file() or sha256_file(source_path) != str(evidence["source_sha256"]):
                raise SystemExit(f"Source replay failed: {source_path}")
            if decision["nc_intake_arm"] == "NC-S_NEW_SOURCE_INTAKE_LEAD":
                if not str(evidence["provenance_status"]).startswith("PASS_"):
                    raise SystemExit(f"NC-S source lacks passing provenance: {source_path}")
                pinned_new_source_hashes.add(str(evidence["source_sha256"]))
            else:
                legacy_parent_source_hashes.add(str(evidence["source_sha256"]))

        initial_for_queue = [row for row in initial_authors.values() if str(row["review_queue_id"]) == queue_id]
        if len(initial_for_queue) != len(boundaries):
            raise SystemExit(f"Prompt coverage mismatch: {queue_id}")
        final_prompt_ids: list[str] = []
        reviewed_targets: set[str] = set()
        for initial_author in initial_for_queue:
            original_id = str(initial_author["prompt_id"])
            initial_result = initial_results[original_id]
            if initial_result["disposition"] == "REWRITE_REQUIRED":
                prompt_id = rewrite_for_original.get(original_id, "")
                if not prompt_id:
                    raise SystemExit(f"Required rewrite absent: {original_id}")
                author = rewrite_authors[prompt_id]
                packet = rewrite_packets[prompt_id]
                result = rewrite_results[prompt_id]
            else:
                prompt_id = original_id
                author = initial_author
                packet = initial_packets[prompt_id]
                result = initial_result
            if result["disposition"] not in {"ACCEPT", "ACCEPT_WITH_CAUTION"}:
                raise SystemExit(f"Final prompt does not pass: {prompt_id}")
            reviewed_hash = full_hash(result)
            intended_hash = str(author["author_intended_candidate_source_sha256"])
            if reviewed_hash != intended_hash:
                raise SystemExit(f"Blind review and author target disagree: {prompt_id}")
            if set(str(row["source_sha256"]) for row in packet["candidates"]) != set(candidate_hashes):
                raise SystemExit(f"Packet roster mismatch: {prompt_id}")
            reviewed_targets.add(reviewed_hash)
            final_prompt_ids.append(prompt_id)
            prompt_rows.append({
                "prompt_id": prompt_id,
                "supersedes_prompt_id": author.get("supersedes_prompt_id"),
                "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
                "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
                "nc_intake_arm": decision["nc_intake_arm"],
                "prompt": author["prompt"],
                "reviewed_single_fully_adequate_source_sha256": reviewed_hash,
                "candidate_source_sha256": candidate_hashes,
                "cue_review": result["cue_review"],
                "curatorial_disposition": result["disposition"],
                "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_001_PENDING_FINAL_FREEZE",
            })
            reconciliation_rows.append({
                "prompt_id": prompt_id,
                "review_queue_id": queue_id,
                "author_intended_source_sha256": intended_hash,
                "blind_review_fully_adequate_source_sha256": reviewed_hash,
                "result": "PASS_EXACT_AUTHOR_REVIEW_RECONCILIATION",
            })
        if reviewed_targets != set(candidate_hashes):
            raise SystemExit(f"Not every cluster candidate has one passing prompt: {queue_id}")
        cluster_rows.append({
            "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
            "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
            "review_queue_id": queue_id,
            "nc_intake_arm": decision["nc_intake_arm"],
            "cluster_origin": "RQ1_SOURCE_MEMBERSHIP_REREAD_FROM_FULL_SOURCES_NO_PROMPT_OR_LABEL_TRANSFER",
            "common_envelope": decision["bounded_shared_envelope"],
            "candidate_ids": decision["candidate_skill_ids"],
            "candidate_source_sha256": candidate_hashes,
            "prompt_ids": sorted(final_prompt_ids),
            "provenance_stratum": (
                "PINNED_NEW_SOURCE_INTAKE" if decision["nc_intake_arm"] == "NC-S_NEW_SOURCE_INTAKE_LEAD"
                else "LEGACY_PARENT_V3_EXACT_SOURCE_PROMPT_ONLY"
            ),
            "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_001_PENDING_FINAL_FREEZE",
            "claim_boundary": "No RQ1 prompt, label, selector output, or metric was transferred.",
        })

    if len(cluster_rows) != 10 or len(prompt_rows) != 20:
        raise SystemExit(f"Expected 10 clusters and 20 prompts, found {len(cluster_rows)}/{len(prompt_rows)}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    union_path = OUTPUT / "canonical_candidate_union_rq1_batch_001.jsonl"
    cluster_path = OUTPUT / "admitted_cluster_manifest.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest.jsonl"
    reconciliation_path = OUTPUT / "author_review_reconciliation.jsonl"
    write_jsonl(union_path, union_rows)
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)
    write_jsonl(reconciliation_path, reconciliation_rows)
    summary = {
        "status": "PASS_RQ1_DERIVED_BATCH_001_PRE_FREEZE_ADMISSION_NOT_FINAL_GOLD_OR_RESULT",
        "parent_pre_freeze_candidate_union_count": 3076,
        "pre_freeze_candidate_union_count": len(union_rows),
        "new_source_rows_added_to_union": len(added_source_rows),
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "admitted_distinct_source_count": len({h for row in cluster_rows for h in row["candidate_source_sha256"]}),
        "nc_p_cluster_count": sum(row["nc_intake_arm"] == "NC-P_EXISTING_V3_PROMPT_LEAD" for row in cluster_rows),
        "nc_s_cluster_count": sum(row["nc_intake_arm"] == "NC-S_NEW_SOURCE_INTAKE_LEAD" for row in cluster_rows),
        "legacy_parent_source_count": len(legacy_parent_source_hashes),
        "pinned_new_source_count": len(pinned_new_source_hashes),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            path.name: sha256_file(path)
            for path in [union_path, cluster_path, prompt_path, reconciliation_path]
        },
        "claim_boundary": [
            "Ten RQ1 source-membership leads were admitted only after full-source re-review, naturalistic reauthoring, target-blinded singleton adequacy review, cue review, and exact author-target reconciliation.",
            "Twelve source-shaped prompts were replaced by reviewed naturalistic rewrites; no RQ1 prompt or label was transferred.",
            "NC-P cases reuse existing parent-V3 candidates and carry a legacy-parent provenance tag; NC-S cases require passing pinned-source evidence.",
            "Six pinned Open-Legal-Products source originals were absent from the 3,076-source parent union and passed source, import-metadata, and licence-hash replay before extending the pre-freeze union to 3,082 rows.",
            "No final acceptable set, strict gold, representation, retrieval run, metric, or thesis result is produced."
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
