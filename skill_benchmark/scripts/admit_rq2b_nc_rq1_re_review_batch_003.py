#!/usr/bin/env python3
"""Fail-closed pre-freeze admission for the reviewed batch-003 R1 prompts.

This is an admission controller, not a label producer.  RQ1 memberships are
only source leads, and the controller retains just the five legal review versus
tabular-extraction clusters whose one permitted rewrite passed the stated
target-blinded gates.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
UNION_IN = BASE / "manifests/rq1_re_review_batch_004_pre_freeze_admission_2026-08-31/canonical_candidate_union_rq1_batch_004.jsonl"
DECISIONS = BASE / "review/rq1_frozen_cluster_re_review_batch_003_2026-08-31.jsonl"
AUTHORS_INITIAL = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_003_private_2026-08-31.jsonl"
AUTHORS_R1 = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_003_rewrite_private_2026-08-31.jsonl"
PACKETS_R1 = BASE / "review/rq1_frozen_cluster_reauthored_batch_003_rewrite_target_blinded_packets_2026-08-31.jsonl"
RESULTS_R1 = BASE / "review/rq1_frozen_cluster_reauthored_batch_003_rewrite_target_blinded_results_2026-08-31.jsonl"
PROVENANCE_AUDIT = BASE / "manifests/rq1_frozen_source_provenance_2026-08-31/source_provenance_audit.jsonl"
OUTPUT = BASE / "manifests/rq1_re_review_batch_003_pre_freeze_admission_2026-08-31"

ADMIT_ORDERS = frozenset({41, 42, 43, 44, 45})
DEFER_ORDERS = frozenset({46, 47, 48, 50, 56})
PASSING_PROVENANCE = "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH"
ALLOWED_ECHO_LEVELS = frozenset({"low", "moderate"})


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def require_unique_index(rows: list[dict[str, Any]], key: str, artifact: str) -> dict[str, dict[str, Any]]:
    index = {str(row[key]): row for row in rows}
    if len(index) != len(rows):
        raise SystemExit(f"Duplicate {key} in {artifact}")
    return index


def replay_missing_nc_s_source(audit: dict[str, Any], skill_id: str) -> dict[str, Any]:
    """Replay all three pinned artefacts before adding an absent NC-S source."""
    if audit["status"] != PASSING_PROVENANCE:
        raise SystemExit(f"Missing NC-S source lacks fully pinned provenance: {audit['source_sha256']}")
    binding = dict(audit["selected_provenance_binding"])
    source_path = ROOT / str(binding["original_path"])
    import_path = ROOT / str(binding["import_metadata_path"])
    license_path = Path(str(binding["local_license_path"]))
    checks = (
        (source_path, str(audit["source_sha256"]), "source"),
        (import_path, str(binding["import_metadata_sha256"]), "import metadata"),
        (license_path, str(binding["license_sha256"]), "licence"),
    )
    for path, expected_hash, label in checks:
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise SystemExit(f"NC-S {label} replay failed: {path}")
    if not binding.get("original_hash_matches_source_sha256") or not binding.get("local_license_hash_matches_record"):
        raise SystemExit(f"NC-S provenance binding is not internally verified: {audit['source_sha256']}")
    return {
        "canonical_source_sha256": str(audit["source_sha256"]),
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


def validate_direct_r1_rewrite(author: dict[str, Any], initial_authors: dict[str, dict[str, Any]]) -> None:
    old_id = str(author.get("supersedes_prompt_id", ""))
    expected_id = old_id.replace("REAUTH-B003-", "REAUTH-B003-R1-")
    if not old_id or str(author["prompt_id"]) != expected_id or old_id not in initial_authors:
        raise SystemExit(f"Prompt is not exactly one direct batch-003 R1 rewrite: {author['prompt_id']}")
    initial = initial_authors[old_id]
    for key in ("review_queue_id", "parent_rq1_cluster_id", "candidate_skill_id", "author_intended_candidate_source_sha256"):
        if author[key] != initial[key]:
            raise SystemExit(f"R1 rewrite changed protected {key}: {author['prompt_id']}")


def validate_final_prompt(
    author: dict[str, Any],
    packet: dict[str, Any],
    result: dict[str, Any],
    candidate_hashes: list[str],
) -> tuple[str, str]:
    """Return the reconciled full-source hash and retained echo level."""
    prompt_id = str(author["prompt_id"])
    if packet["prompt_id"] != prompt_id or result["prompt_id"] != prompt_id:
        raise SystemExit(f"Prompt/packet/result identifier mismatch: {prompt_id}")
    if result["packet_id"] != packet["packet_id"] or not result["source_sha256_verification"].get("all_match"):
        raise SystemExit(f"Target-blinded packet binding or source verification failed: {prompt_id}")
    packet_by_alias = {str(row["alias"]): row for row in packet["candidates"]}
    if len(packet_by_alias) != len(packet["candidates"]):
        raise SystemExit(f"Duplicate target-blinded packet alias: {prompt_id}")
    if set(str(row["source_sha256"]) for row in packet_by_alias.values()) != set(candidate_hashes):
        raise SystemExit(f"Target-blinded packet roster mismatch: {prompt_id}")
    assessments = result["candidate_assessments"]
    assessment_by_alias = {str(row["alias"]): row for row in assessments}
    if set(assessment_by_alias) != set(packet_by_alias) or len(assessment_by_alias) != len(assessments):
        raise SystemExit(f"Target-blinded assessment roster mismatch: {prompt_id}")
    full_aliases = [alias for alias, row in assessment_by_alias.items() if row.get("adequacy") == "fully_adequate"]
    if len(full_aliases) != 1:
        raise SystemExit(f"Expected exactly one fully adequate alias: {prompt_id}")
    diagnostics = result["diagnostics"]
    if diagnostics.get("multi_full_risk") is not False or diagnostics.get("composition") != "not_required":
        raise SystemExit(f"Multi-full or required composition risk remains: {prompt_id}")
    echo_level = str(diagnostics.get("source_body_echo", "")).lower()
    if echo_level not in ALLOWED_ECHO_LEVELS:
        raise SystemExit(f"Source-body echo is not low/moderate after R1: {prompt_id}")
    full_hash = str(packet_by_alias[full_aliases[0]]["source_sha256"])
    intended_hash = str(author["author_intended_candidate_source_sha256"])
    if full_hash != intended_hash:
        raise SystemExit(f"Blind full route does not equal private author target: {prompt_id}")
    return full_hash, echo_level


def main() -> int:
    required = [
        UNION_IN, DECISIONS, AUTHORS_INITIAL, AUTHORS_R1, PACKETS_R1, RESULTS_R1, PROVENANCE_AUDIT,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required artifacts: {missing}")

    union_rows = read_jsonl(UNION_IN)
    union_by_hash = require_unique_index(union_rows, "canonical_source_sha256", "current union")
    if len(union_rows) != 3084:
        raise SystemExit("Expected a 3,084-row hash-unique current pre-freeze union")
    decision_rows = read_jsonl(DECISIONS)
    decisions_by_order = require_unique_index(decision_rows, "review_order", "batch-003 decisions")
    promoted_orders = {int(row["review_order"]) for row in decision_rows if row["disposition"] == "PROMOTE_TO_RQ2_PROMPT_AUTHORING"}
    if promoted_orders != ADMIT_ORDERS | DEFER_ORDERS:
        raise SystemExit(f"Unexpected promoted batch-003 orders: {sorted(promoted_orders)}")
    if not ADMIT_ORDERS | DEFER_ORDERS <= {int(order) for order in decisions_by_order}:
        raise SystemExit("Required batch-003 decision order is absent")

    initial_authors = require_unique_index(read_jsonl(AUTHORS_INITIAL), "prompt_id", "initial private authors")
    authors_r1 = require_unique_index(read_jsonl(AUTHORS_R1), "prompt_id", "R1 private authors")
    packets_r1 = require_unique_index(read_jsonl(PACKETS_R1), "prompt_id", "R1 target-blinded packets")
    results_r1 = require_unique_index(read_jsonl(RESULTS_R1), "prompt_id", "R1 target-blinded results")
    provenance_by_hash = require_unique_index(read_jsonl(PROVENANCE_AUDIT), "source_sha256", "provenance audit")

    admitted = [decisions_by_order[str(order)] for order in sorted(ADMIT_ORDERS)]
    deferred_decisions = [decisions_by_order[str(order)] for order in sorted(DEFER_ORDERS)]
    added_rows: list[dict[str, Any]] = []
    cluster_rows: list[dict[str, Any]] = []
    prompt_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []

    for decision in admitted:
        if decision["disposition"] != "PROMOTE_TO_RQ2_PROMPT_AUTHORING" or decision["nc_intake_arm"] != "NC-S_NEW_SOURCE_INTAKE_LEAD":
            raise SystemExit(f"Admitted order is not an NC-S promoted lead: {decision['review_order']}")
        queue_id = str(decision["review_queue_id"])
        boundaries = decision["necessary_candidate_boundaries"]
        candidate_hashes = [str(boundary["source_evidence"]["source_sha256"]) for boundary in boundaries]
        if len(candidate_hashes) != 2 or len(candidate_hashes) != len(set(candidate_hashes)):
            raise SystemExit(f"Admitted cluster is not a two-source singleton-routing boundary: {queue_id}")
        for boundary in boundaries:
            evidence = boundary["source_evidence"]
            source_path = Path(str(evidence["source_path"]))
            source_hash = str(evidence["source_sha256"])
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"Full source replay failed: {source_path}")
            if source_hash not in union_by_hash:
                added = replay_missing_nc_s_source(provenance_by_hash[source_hash], str(boundary["candidate_skill_id"]))
                union_by_hash[source_hash] = added
                added_rows.append(added)
        queue_authors = [row for row in authors_r1.values() if str(row["review_queue_id"]) == queue_id]
        if len(queue_authors) != len(boundaries):
            raise SystemExit(f"R1 private-author prompt coverage mismatch: {queue_id}")
        reviewed_targets: set[str] = set()
        prompt_ids: list[str] = []
        echo_levels: list[str] = []
        for author in sorted(queue_authors, key=lambda row: str(row["prompt_id"])):
            prompt_id = str(author["prompt_id"])
            validate_direct_r1_rewrite(author, initial_authors)
            if prompt_id not in packets_r1 or prompt_id not in results_r1:
                raise SystemExit(f"R1 target-blinded packet/result absent: {prompt_id}")
            full_hash, echo_level = validate_final_prompt(author, packets_r1[prompt_id], results_r1[prompt_id], candidate_hashes)
            reviewed_targets.add(full_hash)
            prompt_ids.append(prompt_id)
            echo_levels.append(echo_level)
            prompt_rows.append({
                "prompt_id": prompt_id,
                "supersedes_prompt_id": author["supersedes_prompt_id"],
                "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
                "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
                "nc_intake_arm": decision["nc_intake_arm"],
                "prompt": author["prompt"],
                "reviewed_single_fully_adequate_source_sha256": full_hash,
                "candidate_source_sha256": candidate_hashes,
                "cue_review": {
                    "source_body_echo_level": echo_level,
                    "multi_full_risk": False,
                    "workflow_composition": "not_required",
                },
                "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_003_PENDING_FINAL_FREEZE",
            })
            reconciliation_rows.append({
                "prompt_id": prompt_id,
                "review_queue_id": queue_id,
                "author_intended_source_sha256": str(author["author_intended_candidate_source_sha256"]),
                "blind_review_fully_adequate_source_sha256": full_hash,
                "result": "PASS_EXACT_AUTHOR_REVIEW_RECONCILIATION",
            })
        if reviewed_targets != set(candidate_hashes):
            raise SystemExit(f"Every cluster member does not have one reconciled R1 prompt: {queue_id}")
        cluster_rows.append({
            "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
            "parent_rq1_cluster_id": decision["parent_rq1_cluster_id"],
            "review_queue_id": queue_id,
            "nc_intake_arm": decision["nc_intake_arm"],
            "cluster_origin": "RQ1_SOURCE_MEMBERSHIP_REREAD_FROM_FULL_SOURCES_NO_PROMPT_OR_LABEL_TRANSFER",
            "common_envelope": decision["bounded_shared_envelope"],
            "candidate_ids": decision["candidate_skill_ids"],
            "candidate_source_sha256": candidate_hashes,
            "prompt_ids": prompt_ids,
            "observed_source_body_echo_levels": sorted(set(echo_levels)),
            "provenance_stratum": "PINNED_NEW_SOURCE_INTAKE",
            "admission_status": "ADMITTED_RQ1_DERIVED_BATCH_003_PENDING_FINAL_FREEZE",
            "claim_boundary": "No RQ1 prompt, label, selector output, or metric was transferred.",
        })

    deferred_rows: list[dict[str, Any]] = []
    for decision in deferred_decisions:
        queue_id = str(decision["review_queue_id"])
        final_authors = sorted(
            [row for row in authors_r1.values() if str(row["review_queue_id"]) == queue_id],
            key=lambda row: str(row["prompt_id"]),
        )
        if len(final_authors) != len(decision["necessary_candidate_boundaries"]):
            raise SystemExit(f"Deferred R1 prompt coverage mismatch: {queue_id}")
        high_echo_ids: list[str] = []
        no_full_ids: list[str] = []
        for author in final_authors:
            prompt_id = str(author["prompt_id"])
            validate_direct_r1_rewrite(author, initial_authors)
            result = results_r1.get(prompt_id)
            packet = packets_r1.get(prompt_id)
            if result is None or packet is None or result["packet_id"] != packet["packet_id"]:
                raise SystemExit(f"Deferred R1 target-blinded packet/result binding failed: {prompt_id}")
            if str(result["diagnostics"].get("source_body_echo", "")).lower() == "high":
                high_echo_ids.append(prompt_id)
            if not any(row.get("adequacy") == "fully_adequate" for row in result["candidate_assessments"]):
                no_full_ids.append(prompt_id)
        if not high_echo_ids:
            raise SystemExit(f"Deferred order does not retain high source-body echo: {decision['review_order']}")
        if int(decision["review_order"]) == 47:
            if len(no_full_ids) != 1:
                raise SystemExit("Order 47 must retain exactly one no-full prompt/source mismatch")
            reason = "HIGH_SOURCE_BODY_ECHO_AND_NO_FULL_ROUTE_AUTHOR_TARGET_UNRECONCILED"
        elif no_full_ids:
            raise SystemExit(f"Unexpected no-full deferred prompt outside order 47: {no_full_ids}")
        else:
            reason = "HIGH_SOURCE_BODY_ECHO_AFTER_ONE_ALLOWED_REWRITE"
        deferred_rows.append({
            "cluster_id": f"RQ2B-NC-RQ1-{decision['parent_rq1_cluster_id']}",
            "review_order": decision["review_order"],
            "review_queue_id": queue_id,
            "candidate_ids": decision["candidate_skill_ids"],
            "disposition": "DEFER_CLUSTER_R1_ADMISSION_GATE",
            "reason": reason,
            "high_source_body_echo_prompt_ids": high_echo_ids,
            "no_full_prompt_ids": no_full_ids,
            "status": "NOT_ADMITTED_NOT_GOLD_NOT_EXPERIMENT_INPUT",
        })

    union_rows = sorted(union_by_hash.values(), key=lambda row: str(row["canonical_source_sha256"]))
    if len(added_rows) != 10 or len(union_rows) != 3094:
        raise SystemExit(f"Expected ten new pinned legal/tabular sources and a 3,094-row union, found {len(added_rows)}/{len(union_rows)}")
    if len(cluster_rows) != 5 or len(prompt_rows) != 10 or len(reconciliation_rows) != 10 or len(deferred_rows) != 5:
        raise SystemExit("Unexpected admission/defer manifest cardinality")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    union_path = OUTPUT / "canonical_candidate_union_rq1_batch_003.jsonl"
    cluster_path = OUTPUT / "admitted_cluster_manifest.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest.jsonl"
    reconciliation_path = OUTPUT / "author_review_reconciliation.jsonl"
    deferred_path = OUTPUT / "deferred_cluster_manifest.jsonl"
    write_jsonl(union_path, union_rows)
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)
    write_jsonl(reconciliation_path, reconciliation_rows)
    write_jsonl(deferred_path, deferred_rows)
    summary = {
        "status": "PASS_RQ1_DERIVED_BATCH_003_PRE_FREEZE_ADMISSION_NOT_FINAL_GOLD_OR_RESULT",
        "parent_candidate_source_count": 3084,
        "candidate_source_count": len(union_rows),
        "new_source_rows_added": len(added_rows),
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "deferred_cluster_count": len(deferred_rows),
        "admitted_review_orders": sorted(ADMIT_ORDERS),
        "deferred_review_orders": sorted(DEFER_ORDERS),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            path.name: sha256_file(path)
            for path in [union_path, cluster_path, prompt_path, reconciliation_path, deferred_path]
        },
        "claim_boundary": [
            "Only five legal review-versus-tabular-extraction clusters pass source replay, exact R1 packet roster, singleton adequacy, no-multi-full, no-required-composition, low-or-moderate echo, author-target reconciliation, and member-coverage gates.",
            "Orders 46, 47, 48, 50, and 56 remain deferred because at least one R1 prompt retains high source-body echo; order 47 additionally has one no-full route and cannot reconcile that private target.",
            "Ten fully pinned NC-S legal/tabular sources pass source, import-metadata, and licence-hash replay before extending the current union from 3,084 to 3,094 rows.",
            "No final acceptable set, strict gold, representation, selector/retrieval run, metric, or thesis result is produced.",
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
