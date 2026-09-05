#!/usr/bin/env python3
"""Admit the validated portion of RQ2-native business wave 001 to pre-freeze.

Admission is fail-closed at cluster level: every candidate in a cluster must
have a naturalistic prompt with exactly one independently fully adequate source,
the reviewed source must match the private author intent, and the cue review
must pass.  This does not create final gold or run a selector experiment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
UNION = BASE / "manifests/reviewed_wave_001_admission_2026-08-31/canonical_candidate_union_reviewed_wave_001.jsonl"
LEADS = BASE / "candidates/rq2_native_discovery_wave_001_business_2026-08-31.jsonl"
AUTHORS_INITIAL = BASE / "prompts/rq2_native_business_wave_001_authoring_private_2026-08-31.jsonl"
AUTHORS_REWRITE = BASE / "prompts/rq2_native_business_wave_001_rewrite_private_2026-08-31.jsonl"
PACKETS_INITIAL = BASE / "review/rq2_native_business_wave_001_target_blinded_packets_2026-08-31.jsonl"
PACKETS_REWRITE = BASE / "review/rq2_native_business_wave_001_rewrite_target_blinded_packets_2026-08-31.jsonl"
RESULTS_INITIAL = BASE / "review/rq2_native_business_wave_001_target_blinded_results_2026-08-31.jsonl"
RESULTS_REWRITE = BASE / "review/rq2_native_business_wave_001_rewrite_target_blinded_results_2026-08-31.jsonl"
R3_RESULTS = BASE / "review/rq2_native_business_wave_001_rewrite_r3_target_blinded_results_2026-08-31.jsonl"
OUTPUT = BASE / "manifests/rq2_native_business_wave_001_pre_freeze_admission_2026-08-31"


ADMITTED_PROMPTS = {
    "RQ2B-NC-NATIVE-BIZ-001": ["NC-NATIVE-BIZ-W001-001", "NC-NATIVE-BIZ-W001-002", "NC-NATIVE-BIZ-W001-003"],
    "RQ2B-NC-NATIVE-BIZ-002": ["NC-NATIVE-BIZ-W001-004", "NC-NATIVE-BIZ-W001-005"],
    "RQ2B-NC-NATIVE-BIZ-003": ["NC-NATIVE-BIZ-W001-006", "NC-NATIVE-BIZ-W001-007", "NC-NATIVE-BIZ-W001-008"],
    "RQ2B-NC-NATIVE-BIZ-004": ["NC-NATIVE-BIZ-W001-R1-009", "NC-NATIVE-BIZ-W001-010", "NC-NATIVE-BIZ-W001-011"],
    "RQ2B-NC-NATIVE-BIZ-006": ["NC-NATIVE-BIZ-W001-014", "NC-NATIVE-BIZ-W001-015", "NC-NATIVE-BIZ-W001-016"],
    "RQ2B-NC-NATIVE-BIZ-007": ["NC-NATIVE-BIZ-W001-017", "NC-NATIVE-BIZ-W001-R1-018", "NC-NATIVE-BIZ-W001-019"],
}
DEFERRED_CLUSTER = "RQ2B-NC-NATIVE-BIZ-005"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def adequacy_map(result: dict[str, Any]) -> dict[str, str]:
    return {str(row["alias"]): str(row["adequacy"]) for row in result["alias_adequacy"]}


def main() -> int:
    required = [
        UNION, LEADS, AUTHORS_INITIAL, AUTHORS_REWRITE, PACKETS_INITIAL,
        PACKETS_REWRITE, RESULTS_INITIAL, RESULTS_REWRITE, R3_RESULTS,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing input artifacts: {missing}")

    union_rows = read_jsonl(UNION)
    union_hashes = {str(row["canonical_source_sha256"]) for row in union_rows}
    if len(union_rows) != 3076 or len(union_hashes) != 3076:
        raise SystemExit("Expected the reviewed 3,076-row hash-unique pre-freeze union")

    leads = {str(row["cluster_lead_id"]): row for row in read_jsonl(LEADS)}
    authors = {
        str(row["prompt_id"]): row
        for row in read_jsonl(AUTHORS_INITIAL) + read_jsonl(AUTHORS_REWRITE)
    }
    packets = {
        str(row["prompt_id"]): row
        for row in read_jsonl(PACKETS_INITIAL) + read_jsonl(PACKETS_REWRITE)
    }
    results = {
        str(row["prompt_id"]): row
        for row in read_jsonl(RESULTS_INITIAL) + read_jsonl(RESULTS_REWRITE)
    }

    cluster_rows: list[dict[str, Any]] = []
    prompt_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []
    for cluster_id, prompt_ids in ADMITTED_PROMPTS.items():
        lead = leads[cluster_id]
        candidates = lead["candidates"]
        candidate_hashes = [str(row["source_sha256"]) for row in candidates]
        if not set(candidate_hashes).issubset(union_hashes):
            raise SystemExit(f"Cluster source absent from pre-freeze union: {cluster_id}")
        if len(prompt_ids) != len(candidates):
            raise SystemExit(f"Every cluster member requires one reviewed prompt: {cluster_id}")
        for candidate in candidates:
            source_path = ROOT.parent / str(candidate["source_path"])
            if not source_path.is_file() or sha256_file(source_path) != str(candidate["source_sha256"]):
                raise SystemExit(f"Source byte replay failed: {source_path}")

        reviewed_targets: set[str] = set()
        for prompt_id in prompt_ids:
            author = authors[prompt_id]
            packet = packets[prompt_id]
            result = results[prompt_id]
            if str(author["cluster_lead_id"]) != cluster_id or str(packet["cluster_lead_id"]) != cluster_id:
                raise SystemExit(f"Cluster mapping mismatch: {prompt_id}")
            if str(result["disposition"]) != "PASS_CURATORIAL_SINGLETON_ADEQUATE":
                raise SystemExit(f"Non-passing review cannot be admitted: {prompt_id}")
            grades = adequacy_map(result)
            full_aliases = [alias for alias, grade in grades.items() if grade == "fully_adequate"]
            if len(full_aliases) != 1:
                raise SystemExit(f"Expected exactly one fully adequate alias: {prompt_id}")
            reviewed = next(row for row in packet["candidates"] if str(row["alias"]) == full_aliases[0])
            intended = str(author["author_intended_candidate_source_sha256"])
            if str(reviewed["source_sha256"]) != intended:
                raise SystemExit(f"Blind review and private author intent disagree: {prompt_id}")
            if set(str(row["source_sha256"]) for row in packet["candidates"]) != set(candidate_hashes):
                raise SystemExit(f"Packet roster differs from cluster: {prompt_id}")
            reviewed_targets.add(intended)
            candidate = next(row for row in candidates if str(row["source_sha256"]) == intended)
            prompt_rows.append({
                "prompt_id": prompt_id,
                "cluster_id": cluster_id,
                "prompt": author["prompt"],
                "reviewed_single_fully_adequate_source_sha256": intended,
                "reviewed_single_fully_adequate_candidate_id": candidate["skill_id"],
                "candidate_source_sha256": candidate_hashes,
                "cue_assessment": result["cue_assessment"],
                "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                "admission_status": "ADMITTED_RQ2_NATIVE_BUSINESS_WAVE_001_PENDING_FINAL_FREEZE",
            })
            reconciliation_rows.append({
                "prompt_id": prompt_id,
                "cluster_id": cluster_id,
                "author_intended_source_sha256": intended,
                "blind_review_fully_adequate_alias": full_aliases[0],
                "blind_review_fully_adequate_source_sha256": str(reviewed["source_sha256"]),
                "candidate_roster_sha256": sorted(candidate_hashes),
                "result": "PASS_EXACT_AUTHOR_REVIEW_RECONCILIATION",
            })
        if reviewed_targets != set(candidate_hashes):
            raise SystemExit(f"Not every cluster member has one admitted prompt: {cluster_id}")
        cluster_rows.append({
            "cluster_id": cluster_id,
            "cluster_origin": "RQ2_NATIVE_PUBLIC_POOL_DISCOVERY",
            "common_envelope": lead["common_envelope"],
            "candidate_ids": [row["skill_id"] for row in candidates],
            "candidate_source_sha256": candidate_hashes,
            "prompt_ids": prompt_ids,
            "origin_stratum": lead["origin_stratum"],
            "admission_status": "ADMITTED_RQ2_NATIVE_BUSINESS_WAVE_001_PENDING_FINAL_FREEZE",
            "claim_boundary": "Source-grounded model-assisted curatorial admission, not human annotation, final gold, representativeness, or a retrieval result.",
        })

    if len(cluster_rows) != 6 or len(prompt_rows) != 17:
        raise SystemExit(f"Expected 6 clusters and 17 prompts, found {len(cluster_rows)}/{len(prompt_rows)}")

    r3_rows = read_jsonl(R3_RESULTS)
    if len(r3_rows) != 1 or str(r3_rows[0].get("disposition")) != "DEFER":
        raise SystemExit("The competitive-moat R3 prompt must remain explicitly deferred")
    deferred = {
        "cluster_id": DEFERRED_CLUSTER,
        "disposition": "DEFER_CLUSTER_FAIL_CLOSED",
        "reason": (
            "One member's final rewrite remained avoidably close to the source worked example; "
            "cluster-level admission requires an independently passing naturalistic prompt for every member."
        ),
        "prompt_ids": ["NC-NATIVE-BIZ-W001-012", "NC-NATIVE-BIZ-W001-R3-013"],
        "status": "NOT_ADMITTED_NOT_GOLD_NOT_EXPERIMENT_INPUT",
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    cluster_path = OUTPUT / "admitted_cluster_manifest.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest.jsonl"
    reconciliation_path = OUTPUT / "author_review_reconciliation.jsonl"
    deferred_path = OUTPUT / "deferred_cluster_manifest.jsonl"
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)
    write_jsonl(reconciliation_path, reconciliation_rows)
    write_jsonl(deferred_path, [deferred])
    summary = {
        "status": "PASS_RQ2_NATIVE_BUSINESS_WAVE_001_PRE_FREEZE_ADMISSION_NOT_FINAL_GOLD_OR_RESULT",
        "pre_freeze_candidate_union_count": len(union_rows),
        "new_source_rows_added_to_union": 0,
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "admitted_distinct_source_count": len({h for row in cluster_rows for h in row["candidate_source_sha256"]}),
        "deferred_cluster_count": 1,
        "deferred_prompt_count": 2,
        "origin_strata": {"single_origin_SkillMedev_skills": len(cluster_rows)},
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            path.name: sha256_file(path)
            for path in [cluster_path, prompt_path, reconciliation_path, deferred_path]
        },
        "claim_boundary": [
            "Six clusters and seventeen prompts passed source-byte, roster, target-blinded singleton adequacy, author-target reconciliation, cue, and cluster-completeness gates.",
            "All seventeen source candidates were already present in the 3,076-source pre-freeze union; this admission does not enlarge the union.",
            "The competitive-intelligence versus competitive-moat cluster is deferred fail-closed because the moat prompt retained avoidable source-example echo after the final rewrite.",
            "The admitted wave is a single-origin source stratum and does not establish ecological representativeness.",
            "No final acceptable set, strict gold, representation, retrieval run, metric, or thesis result is produced."
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
