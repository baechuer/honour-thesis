#!/usr/bin/env python3
"""Assemble one current RQ2b-NC pre-freeze view from passed admissions.

The assembly preserves each intake stratum and admission provenance.  It is a
replaceable current ledger, not the immutable final gold or experiment input.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
RQ1_DIR = BASE / "manifests/rq1_re_review_batch_001_pre_freeze_admission_2026-08-31"
RQ1_BATCH2_DIR = BASE / "manifests/rq1_re_review_batch_002_pre_freeze_admission_2026-08-31"
RQ1_BATCH3_DIR = BASE / "manifests/rq1_re_review_batch_003_pre_freeze_admission_2026-08-31"
RQ1_BATCH4_DIR = BASE / "manifests/rq1_re_review_batch_004_pre_freeze_admission_2026-08-31"
WAVE_DIR = BASE / "manifests/reviewed_wave_001_admission_2026-08-31"
BUSINESS_DIR = BASE / "manifests/rq2_native_business_wave_001_pre_freeze_admission_2026-08-31"
TECHNICAL_DIR = BASE / "manifests/rq2_native_technical_wave_001_pre_freeze_admission_2026-08-31"
OUTPUT = BASE / "manifests/current_pre_freeze_consolidated_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    union_input = RQ1_BATCH3_DIR / "canonical_candidate_union_rq1_batch_003.jsonl"
    cluster_inputs = [
        WAVE_DIR / "reviewed_cluster_manifest.jsonl",
        BUSINESS_DIR / "admitted_cluster_manifest.jsonl",
        RQ1_DIR / "admitted_cluster_manifest.jsonl",
        RQ1_BATCH2_DIR / "admitted_cluster_manifest.jsonl",
        RQ1_BATCH3_DIR / "admitted_cluster_manifest.jsonl",
        RQ1_BATCH4_DIR / "admitted_cluster_manifest.jsonl",
        TECHNICAL_DIR / "admitted_cluster_manifest.jsonl",
    ]
    prompt_inputs = [
        WAVE_DIR / "reviewed_prompt_manifest.jsonl",
        BUSINESS_DIR / "admitted_prompt_manifest.jsonl",
        RQ1_DIR / "admitted_prompt_manifest.jsonl",
        RQ1_BATCH2_DIR / "admitted_prompt_manifest.jsonl",
        RQ1_BATCH3_DIR / "admitted_prompt_manifest.jsonl",
        RQ1_BATCH4_DIR / "admitted_prompt_manifest.jsonl",
        TECHNICAL_DIR / "admitted_prompt_manifest.jsonl",
    ]
    required = [union_input, *cluster_inputs, *prompt_inputs]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing admission inputs: {missing}")

    union_rows = read_jsonl(union_input)
    union_hashes = {str(row["canonical_source_sha256"]) for row in union_rows}
    if len(union_rows) != 3094 or len(union_hashes) != 3094:
        raise SystemExit("Expected the 3,094-row hash-unique latest admitted source union")

    cluster_rows: list[dict[str, Any]] = []
    for path in cluster_inputs:
        for row in read_jsonl(path):
            candidate_hashes = [str(value) for value in row["candidate_source_sha256"]]
            if not set(candidate_hashes).issubset(union_hashes):
                raise SystemExit(f"Cluster source absent from latest union: {row['cluster_id']}")
            cluster_rows.append({**row, "pre_freeze_origin_manifest": str(path.relative_to(ROOT))})
    cluster_ids = [str(row["cluster_id"]) for row in cluster_rows]
    if len(cluster_rows) != 56 or len(set(cluster_ids)) != 56:
        raise SystemExit(f"Expected 56 unique admitted clusters, found {len(cluster_rows)}/{len(set(cluster_ids))}")
    cluster_by_id = {str(row["cluster_id"]): row for row in cluster_rows}

    prompt_rows: list[dict[str, Any]] = []
    for path in prompt_inputs:
        for row in read_jsonl(path):
            prompt_id = str(row["prompt_id"])
            cluster_id = str(row["cluster_id"])
            if cluster_id not in cluster_by_id:
                raise SystemExit(f"Prompt refers to absent cluster: {prompt_id}")
            roster = {str(value) for value in row["candidate_source_sha256"]}
            cluster_roster = {str(value) for value in cluster_by_id[cluster_id]["candidate_source_sha256"]}
            if roster != cluster_roster:
                raise SystemExit(f"Prompt/cluster roster mismatch: {prompt_id}")
            reviewed = str(row["reviewed_single_fully_adequate_source_sha256"])
            if reviewed not in roster:
                raise SystemExit(f"Reviewed target outside cluster: {prompt_id}")
            prompt_rows.append({**row, "pre_freeze_origin_manifest": str(path.relative_to(ROOT))})
    prompt_ids = [str(row["prompt_id"]) for row in prompt_rows]
    if len(prompt_rows) != 129 or len(set(prompt_ids)) != 129:
        raise SystemExit(f"Expected 129 unique admitted prompts, found {len(prompt_rows)}/{len(set(prompt_ids))}")

    expected_by_cluster = {cluster_id: set() for cluster_id in cluster_ids}
    for row in prompt_rows:
        expected_by_cluster[str(row["cluster_id"])].add(str(row["prompt_id"]))
    for cluster_id, cluster in cluster_by_id.items():
        declared = {str(value) for value in cluster["prompt_ids"]}
        if declared != expected_by_cluster[cluster_id]:
            raise SystemExit(f"Cluster prompt coverage mismatch: {cluster_id}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    union_path = OUTPUT / "canonical_candidate_union_current_pre_freeze.jsonl"
    cluster_path = OUTPUT / "admitted_cluster_manifest_current_pre_freeze.jsonl"
    prompt_path = OUTPUT / "admitted_prompt_manifest_current_pre_freeze.jsonl"
    write_jsonl(union_path, union_rows)
    write_jsonl(cluster_path, sorted(cluster_rows, key=lambda row: str(row["cluster_id"])))
    write_jsonl(prompt_path, sorted(prompt_rows, key=lambda row: str(row["prompt_id"])))
    summary = {
        "status": "PASS_CURRENT_CONSOLIDATED_PRE_FREEZE_NOT_FINAL_GOLD_OR_EXPERIMENT_INPUT",
        "candidate_source_count": len(union_rows),
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "admission_strata": {
            "reviewed_wave_001": {"cluster_count": 3, "prompt_count": 9},
            "rq2_native_business_wave_001": {"cluster_count": 6, "prompt_count": 17},
            "rq2_native_technical_wave_001": {"cluster_count": 9, "prompt_count": 27},
            "rq1_derived_batch_001": {"cluster_count": 10, "prompt_count": 20},
            "rq1_derived_batch_002": {"cluster_count": 10, "prompt_count": 20},
            "rq1_derived_batch_003": {"cluster_count": 5, "prompt_count": 10},
            "rq1_derived_batch_004": {"cluster_count": 13, "prompt_count": 26},
        },
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            path.name: sha256_file(path)
            for path in [union_path, cluster_path, prompt_path]
        },
        "claim_boundary": [
            "This is the single current pre-freeze view and supersedes using individual admission manifests as the working union.",
            "It consolidates only already-passed admissions and preserves their intake/provenance strata.",
            "The 129 singleton-adequacy mappings hold within their reviewed cluster rosters and are model-assisted curation evidence, not human annotation or global final gold.",
            "Whole-library alternative-candidate discovery, acceptable-set adjudication, new-source representations, final split and cue integrity, immutable freeze, and all selector/reranker execution remain outstanding."
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
