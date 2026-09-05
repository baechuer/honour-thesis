#!/usr/bin/env python3
"""Close the RQ2b-NC curation set without creating final whole-library gold."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


BENCHMARK_ROOT = Path(__file__).resolve().parents[1]
NC_ROOT = BENCHMARK_ROOT / "rq2b_naturalistic_confusability"
CURRENT = NC_ROOT / "manifests/current_pre_freeze_consolidated_2026-08-31"
CLUSTERS = CURRENT / "admitted_cluster_manifest_current_pre_freeze.jsonl"
PROMPTS = CURRENT / "admitted_prompt_manifest_current_pre_freeze.jsonl"
RECONCILIATION = NC_ROOT / "review/acceptable_set_local_reconciliation_2026-08-31/reconciled_local_acceptable_set_ledger.jsonl"
STOP_DECISION = NC_ROOT / "review/EXPANSION_STOP_DECISION_2026-08-31.json"
PDF_DECISION = NC_ROOT / "review/PDF_BLOCKED_CLUSTER_ROOT_DISPOSITION_2026-08-31.json"
OUTPUT = NC_ROOT / "manifests/curation_closed_checkpoint_2026-08-31"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> None:
    cluster_rows = read_jsonl(CLUSTERS)
    prompt_rows = read_jsonl(PROMPTS)
    review_rows = read_jsonl(RECONCILIATION)
    review_by_prompt = {row["prompt_id"]: row for row in review_rows}
    prompt_by_id = {row["prompt_id"]: row for row in prompt_rows}
    prompts_by_cluster: dict[str, list[dict]] = defaultdict(list)
    for row in prompt_rows:
        prompts_by_cluster[row["cluster_id"]].append(row)

    assert len(cluster_rows) == 56, len(cluster_rows)
    assert len(prompt_rows) == 129, len(prompt_rows)
    assert len(review_rows) == 129, len(review_rows)
    assert set(prompt_by_id) == set(review_by_prompt)

    excluded: dict[str, dict] = {}
    tentative_ids: set[str] = set()
    for prompt_id, review in review_by_prompt.items():
        if review["local_disposition"] == "BLOCK_NO_FULL":
            excluded[prompt_id] = {
                "prompt_id": prompt_id,
                "cluster_id": review["cluster_id"],
                "exclusion_stage": "CLUSTER_LOCAL_ADEQUACY",
                "reason": "No reviewed cluster member was fully acceptable for the prompt as written.",
                "local_disposition": "BLOCK_NO_FULL",
                "original_prompt_record": prompt_by_id[prompt_id],
            }
        else:
            tentative_ids.add(prompt_id)

    eligible_clusters: list[dict] = []
    incomplete_clusters: list[dict] = []
    for cluster in cluster_rows:
        cluster_id = cluster["cluster_id"]
        surviving = [
            row for row in prompts_by_cluster[cluster_id] if row["prompt_id"] in tentative_ids
        ]
        target_hashes = {
            review_by_prompt[row["prompt_id"]]["most_suitable_source_sha256"]
            for row in surviving
        }
        member_hashes = set(cluster["candidate_source_sha256"])
        missing_targets = sorted(member_hashes - target_hashes)
        if missing_targets:
            incomplete_clusters.append(
                {
                    "cluster_id": cluster_id,
                    "missing_member_target_source_sha256": missing_targets,
                    "surviving_prompt_ids_before_cluster_gate": sorted(
                        row["prompt_id"] for row in surviving
                    ),
                }
            )
            for row in surviving:
                prompt_id = row["prompt_id"]
                tentative_ids.remove(prompt_id)
                excluded[prompt_id] = {
                    "prompt_id": prompt_id,
                    "cluster_id": cluster_id,
                    "exclusion_stage": "POST_BLOCK_CLUSTER_COMPLETENESS",
                    "reason": (
                        "A sibling prompt was blocked, leaving at least one cluster member without "
                        "an independently most-suitable testcase; retaining the remainder would violate "
                        "the frozen every-member-has-a-prompt rule."
                    ),
                    "local_disposition": review_by_prompt[prompt_id]["local_disposition"],
                    "original_prompt_record": row,
                }
            continue
        admitted = dict(cluster)
        admitted["curation_close_status"] = (
            "CURATION_ELIGIBLE_PENDING_WHOLE_LIBRARY_AUDIT_REPRESENTATION_AND_FINAL_FREEZE"
        )
        admitted["prompt_ids"] = sorted(row["prompt_id"] for row in surviving)
        eligible_clusters.append(admitted)

    eligible_prompts: list[dict] = []
    for prompt_id in sorted(tentative_ids):
        source = prompt_by_id[prompt_id]
        review = review_by_prompt[prompt_id]
        row = dict(source)
        row["curation_close_status"] = (
            "CURATION_ELIGIBLE_PENDING_WHOLE_LIBRARY_AUDIT_REPRESENTATION_AND_FINAL_FREEZE"
        )
        row["cluster_local_disposition"] = review["local_disposition"]
        row["cluster_local_most_suitable_source_sha256"] = review[
            "most_suitable_source_sha256"
        ]
        row["cluster_local_acceptable_set_source_sha256"] = review[
            "acceptable_set_source_sha256"
        ]
        eligible_prompts.append(row)

    eligible_clusters.sort(key=lambda row: row["cluster_id"])
    eligible_prompts.sort(key=lambda row: row["prompt_id"])
    excluded_rows = [excluded[key] for key in sorted(excluded)]

    assert len(eligible_clusters) == 54, len(eligible_clusters)
    assert len(eligible_prompts) == 125, len(eligible_prompts)
    assert len(excluded_rows) == 4, len(excluded_rows)
    assert len(incomplete_clusters) == 2, incomplete_clusters

    OUTPUT.mkdir(parents=True, exist_ok=True)
    cluster_out = OUTPUT / "curation_eligible_clusters.jsonl"
    prompt_out = OUTPUT / "curation_eligible_prompts.jsonl"
    excluded_out = OUTPUT / "excluded_prompts.jsonl"
    write_jsonl(cluster_out, eligible_clusters)
    write_jsonl(prompt_out, eligible_prompts)
    write_jsonl(excluded_out, excluded_rows)

    disposition_counts = Counter(
        row["cluster_local_disposition"] for row in eligible_prompts
    )
    summary = {
        "status": "PASS_CURATION_CLOSED_CHECKPOINT_NOT_FINAL_GOLD_OR_EXPERIMENT_INPUT",
        "bound_inputs": {
            str(CLUSTERS.relative_to(BENCHMARK_ROOT)): sha256(CLUSTERS),
            str(PROMPTS.relative_to(BENCHMARK_ROOT)): sha256(PROMPTS),
            str(RECONCILIATION.relative_to(BENCHMARK_ROOT)): sha256(RECONCILIATION),
            str(STOP_DECISION.relative_to(BENCHMARK_ROOT)): sha256(STOP_DECISION),
            str(PDF_DECISION.relative_to(BENCHMARK_ROOT)): sha256(PDF_DECISION),
        },
        "counts": {
            "reviewed_nc_prompts_before_fail_closed_filter": len(prompt_rows),
            "curation_eligible_nc_prompts": len(eligible_prompts),
            "curation_eligible_clusters": len(eligible_clusters),
            "excluded_prompts": len(excluded_rows),
            "cluster_local_dispositions_among_eligible": dict(
                sorted(disposition_counts.items())
            ),
            "parent_v3_prompts_unchanged": 381,
            "combined_parent_plus_curation_eligible_checkpoint": 381
            + len(eligible_prompts),
            "candidate_union_unique_sources_unchanged": 3094,
        },
        "incomplete_clusters_removed": incomplete_clusters,
        "outputs": {
            cluster_out.name: sha256(cluster_out),
            prompt_out.name: sha256(prompt_out),
            excluded_out.name: sha256(excluded_out),
        },
        "claim_boundary": [
            "Collection is closed under the prospective low-yield rule.",
            "The 125 prompts are eligible for whole-library alternative discovery, not final strict gold.",
            "The combined count 506 is a curation checkpoint; parent delta audit or whole-library NC audit may exclude prompts or expand acceptable sets.",
            "No representation, selector output, metric, or experiment result is created.",
        ],
    }
    (OUTPUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
