#!/usr/bin/env python3
"""Promote the reviewed first NC wave into an admitted pre-freeze manifest.

This builder performs deterministic source-hash and target-blinded-review
reconciliation.  It does not produce I1/I2/I3 representations, a final gold
freeze, retrieval scores, or thesis results.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NC_ROOT = ROOT / "rq2b_naturalistic_confusability"
BASE_UNION = NC_ROOT / "manifests/candidate_union_preflight_2026-08-31/canonical_candidate_union_preflight.jsonl"
W32_RETRIEVAL = ROOT / "rq1b_v3_public_source_frame/d1_source_intake_wave_032_2026-08-30/retrieved_public_sources/retrieval_manifest.jsonl"
W33_RETRIEVAL = ROOT / "rq1b_v3_public_source_frame/d1_source_intake_wave_033_2026-08-30/retrieved_public_sources/retrieval_manifest.jsonl"
INITIAL_AUTHORS = NC_ROOT / "prompts/initial_authoring_drafts_private_2026-08-31.jsonl"
REWRITE_AUTHORS = NC_ROOT / "prompts/rewrite_authoring_drafts_private_2026-08-31.jsonl"
INITIAL_PACKETS = NC_ROOT / "review/initial_blinded_adequacy_packets_2026-08-31.jsonl"
REWRITE_PACKETS = NC_ROOT / "review/rewrite_target_blinded_adequacy_packets_2026-08-31.jsonl"
INITIAL_RESULTS = NC_ROOT / "review/initial_target_blinded_adequacy_results_2026-08-31.jsonl"
REWRITE_RESULTS = NC_ROOT / "review/rewrite_target_blinded_adequacy_results_2026-08-31.jsonl"
PROVENANCE_CHECKPOINT = NC_ROOT / "manifests/SELECTED_NC_LEAD_PROVENANCE_CHECKPOINT_2026-08-31.md"
OUTPUT_DIR = NC_ROOT / "manifests/reviewed_wave_001_admission_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


SOURCE_IDENTITIES = {
    "e60144d3a6a4e0b8bcb7a779a394372d88488293f451850bfefd663fe5b30d75": "rq2b-nc-bm629-security-prior-art-survey",
    "c4fe197392a6949510896d785280ca09d4f3b693f22f50909ab96020d52af2b3": "rq2b-nc-bm629-user-research-prior-art-survey",
    "02ef2eb0479f365830326f15fc551e305c61e328c5edcbd496b5dda0f3cdf873": "rq2b-nc-bm629-visual-prior-art-survey",
    "cbfbdd15464819bc566abbc9b8d2d85aa5ee213c4e1377379358875896af6510": "rq2b-nc-aipoch-gokegg",
    "f8dfcb232500578409ede54ab90e4c063b37cc8e7c78709b4f1547922fab1d4f": "rq2b-nc-aipoch-gsea",
    "5fc350c43e98d3137de0cbd6c30816635de0e80619dd8b7a64f0f6b7078d061b": "rq2b-nc-aipoch-gsva-analysis-and-visualization",
    "1204f71183ca27b476a326379b5a7988857d83df6afa1c54e19082c981ea7322": "public-emmraan-frontend-ui-react",
    "eba0d129cc4c2cf9c08116d4b136cc6800322985e831a9e04da4e97f3dca137a": "public-emmraan-frontend-ui-vue",
    "95bd0cd11d24927468cd0616bd6b4bcb3e3a7a4184b5eec8d61ce311916e7ebf": "public-emmraan-frontend-ui-angular",
}


CLUSTERS = [
    {
        "cluster_id": "RQ2B-NC-W001-PRIOR-ART-EVIDENCE-TYPE",
        "cluster_origin": "REVIEWED_RQ1_LEAD_REAUTHORED_FOR_RQ2",
        "common_envelope": "pre-build evidence survey for a proposed product",
        "candidate_source_sha256": [
            "e60144d3a6a4e0b8bcb7a779a394372d88488293f451850bfefd663fe5b30d75",
            "c4fe197392a6949510896d785280ca09d4f3b693f22f50909ab96020d52af2b3",
            "02ef2eb0479f365830326f15fc551e305c61e328c5edcbd496b5dda0f3cdf873",
        ],
        "prompt_ids": ["NC-REWRITE-001", "NC-REWRITE-002", "NC-REWRITE-003"],
        "cue_stratum": "MEDIUM_TO_MEDIUM_HIGH_SEMANTIC_SOURCE_PROXIMITY",
    },
    {
        "cluster_id": "RQ2B-NC-W001-PATHWAY-INPUT-OBJECT",
        "cluster_origin": "REVIEWED_RQ1_LEAD_REAUTHORED_FOR_RQ2",
        "common_envelope": "pathway-level analysis of bulk expression studies",
        "candidate_source_sha256": [
            "cbfbdd15464819bc566abbc9b8d2d85aa5ee213c4e1377379358875896af6510",
            "f8dfcb232500578409ede54ab90e4c063b37cc8e7c78709b4f1547922fab1d4f",
            "5fc350c43e98d3137de0cbd6c30816635de0e80619dd8b7a64f0f6b7078d061b",
        ],
        "prompt_ids": ["NC-DRAFT-004", "NC-DRAFT-005", "NC-DRAFT-006"],
        "cue_stratum": "LOW_TO_MEDIUM_LEGITIMATE_INPUT_OUTPUT_CUE",
    },
    {
        "cluster_id": "RQ2B-NC-W001-FRAMEWORK-PROJECT-ARTIFACT",
        "cluster_origin": "REVIEWED_RQ1_LEAD_REAUTHORED_FOR_RQ2",
        "common_envelope": "extend a typed component in an existing web application",
        "candidate_source_sha256": [
            "1204f71183ca27b476a326379b5a7988857d83df6afa1c54e19082c981ea7322",
            "eba0d129cc4c2cf9c08116d4b136cc6800322985e831a9e04da4e97f3dca137a",
            "95bd0cd11d24927468cd0616bd6b4bcb3e3a7a4184b5eec8d61ce311916e7ebf",
        ],
        "prompt_ids": ["NC-REWRITE-007", "NC-REWRITE-008", "NC-REWRITE-009"],
        "cue_stratum": "HIGH_LEGITIMATE_DEPENDENCY_ARTIFACT_CUE",
    },
]


def cluster_for_prompt(prompt_id: str) -> dict[str, Any]:
    matches = [cluster for cluster in CLUSTERS if prompt_id in cluster["prompt_ids"]]
    if len(matches) != 1:
        raise SystemExit(f"Prompt {prompt_id} maps to {len(matches)} clusters")
    return matches[0]


def main() -> int:
    required = [
        BASE_UNION,
        W32_RETRIEVAL,
        W33_RETRIEVAL,
        INITIAL_AUTHORS,
        REWRITE_AUTHORS,
        INITIAL_PACKETS,
        REWRITE_PACKETS,
        INITIAL_RESULTS,
        REWRITE_RESULTS,
        PROVENANCE_CHECKPOINT,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    base_rows = read_jsonl(BASE_UNION)
    base_by_hash = {str(row["canonical_source_sha256"]): row for row in base_rows}
    if len(base_rows) != 3070 or len(base_by_hash) != 3070:
        raise SystemExit("Expected a 3,070-row hash-unique base candidate union")

    retrieval_rows = read_jsonl(W32_RETRIEVAL) + read_jsonl(W33_RETRIEVAL)
    retrieval_by_hash = {str(row["source_sha256"]): row for row in retrieval_rows}
    selected_hashes = {source_hash for cluster in CLUSTERS for source_hash in cluster["candidate_source_sha256"]}
    if selected_hashes != set(SOURCE_IDENTITIES):
        raise SystemExit("Cluster candidates and source identities disagree")

    added_rows: list[dict[str, Any]] = []
    for source_hash in sorted(selected_hashes - set(base_by_hash)):
        retrieval = retrieval_by_hash.get(source_hash)
        if retrieval is None:
            raise SystemExit(f"No retrieval record for reviewed source {source_hash}")
        source_path = ROOT.parent / str(retrieval["local_raw_path"])
        if not source_path.is_file() or sha256_file(source_path) != source_hash:
            raise SystemExit(f"Reviewed source bytes fail hash replay: {source_hash}")
        repository_ref = str(retrieval["repository_ref"])
        if "@" not in repository_ref or repository_ref.endswith("@main"):
            raise SystemExit(f"Reviewed source lacks immutable repository ref: {source_hash}")
        repository, commit = repository_ref.split("@", 1)
        added_rows.append(
            {
                "canonical_source_sha256": source_hash,
                "canonical_candidate_id": SOURCE_IDENTITIES[source_hash],
                "final_intake_role": "RQ2B_NC_REVIEWED_SOURCE_CANDIDATE",
                "source_path": str(retrieval["local_raw_path"]),
                "source_bytes": int(retrieval["byte_count"]),
                "source_url": retrieval["raw_artifact_url"],
                "origin": repository,
                "pinned_reference": commit,
                "license_declared": "MIT",
                "license_evidence_url": f"https://github.com/{repository}/blob/{commit}/LICENSE",
                "license_evidence_checkpoint": str(PROVENANCE_CHECKPOINT.relative_to(ROOT)),
                "license_evidence_checkpoint_sha256": sha256_file(PROVENANCE_CHECKPOINT),
                "status": "ADMITTED_NC_SOURCE_CANDIDATE_PENDING_REPRESENTATION_AND_FINAL_FREEZE",
            }
        )

    union_rows = sorted(base_rows + added_rows, key=lambda row: str(row["canonical_source_sha256"]))
    union_hashes = [str(row["canonical_source_sha256"]) for row in union_rows]
    if len(union_rows) != 3076 or len(set(union_hashes)) != 3076:
        raise SystemExit("Reviewed wave must yield a 3,076-row hash-unique candidate union")
    if not selected_hashes.issubset(set(union_hashes)):
        raise SystemExit("A reviewed cluster candidate is absent from the admitted union")

    author_rows = read_jsonl(INITIAL_AUTHORS) + read_jsonl(REWRITE_AUTHORS)
    packet_rows = read_jsonl(INITIAL_PACKETS) + read_jsonl(REWRITE_PACKETS)
    result_rows = read_jsonl(INITIAL_RESULTS) + read_jsonl(REWRITE_RESULTS)
    authors = {str(row["prompt_id"]): row for row in author_rows}
    packets = {str(row["prompt_id"]): row for row in packet_rows}
    results = {str(row["prompt_id"]): row for row in result_rows}

    prompt_rows: list[dict[str, Any]] = []
    for cluster in CLUSTERS:
        for prompt_id in cluster["prompt_ids"]:
            author = authors[prompt_id]
            packet = packets[prompt_id]
            result = results[prompt_id]
            full_aliases = [alias for alias, grade in dict(result["alias_adequacy"]).items() if grade == "fully_adequate"]
            if int(result["unique_fully_adequate_count"]) != 1 or len(full_aliases) != 1:
                raise SystemExit(f"Prompt {prompt_id} lacks exactly one fully adequate candidate")
            full_candidate = next(candidate for candidate in packet["candidates"] if candidate["alias"] == full_aliases[0])
            intended_hash = str(author["author_intended_candidate_source_sha256"])
            if str(full_candidate["source_sha256"]) != intended_hash:
                raise SystemExit(f"Independent review does not match the intended source for {prompt_id}")
            if intended_hash not in cluster["candidate_source_sha256"]:
                raise SystemExit(f"Reviewed target is outside cluster for {prompt_id}")
            if set(str(candidate["source_sha256"]) for candidate in packet["candidates"]) != set(cluster["candidate_source_sha256"]):
                raise SystemExit(f"Review packet candidate set mismatch for {prompt_id}")
            prompt_rows.append(
                {
                    "prompt_id": prompt_id,
                    "cluster_id": cluster["cluster_id"],
                    "prompt": author["prompt"],
                    "reviewed_single_fully_adequate_source_sha256": intended_hash,
                    "reviewed_single_fully_adequate_candidate_id": SOURCE_IDENTITIES[intended_hash],
                    "candidate_source_sha256": cluster["candidate_source_sha256"],
                    "cue_stratum": result.get("cue_stratum") or result.get("cue_risk"),
                    "review_visibility": result["review_visibility"],
                    "label_status": "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE",
                    "admission_status": "ADMITTED_NC_WAVE_001_PENDING_REPRESENTATION_AND_FINAL_FREEZE",
                }
            )

    if len(prompt_rows) != 9 or len({row["prompt_id"] for row in prompt_rows}) != 9:
        raise SystemExit("Expected exactly nine unique admitted prompts")

    cluster_rows = []
    for cluster in CLUSTERS:
        cluster_rows.append(
            {
                **cluster,
                "candidate_ids": [SOURCE_IDENTITIES[source_hash] for source_hash in cluster["candidate_source_sha256"]],
                "reviewed_prompt_count": len(cluster["prompt_ids"]),
                "admission_status": "ADMITTED_NC_WAVE_001_PENDING_REPRESENTATION_AND_FINAL_FREEZE",
                "label_boundary": "No RQ1 label transferred; every task was reauthored and reconciled against target-blinded source adequacy review.",
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    union_path = OUTPUT_DIR / "canonical_candidate_union_reviewed_wave_001.jsonl"
    cluster_path = OUTPUT_DIR / "reviewed_cluster_manifest.jsonl"
    prompt_path = OUTPUT_DIR / "reviewed_prompt_manifest.jsonl"
    write_jsonl(union_path, union_rows)
    write_jsonl(cluster_path, cluster_rows)
    write_jsonl(prompt_path, prompt_rows)

    summary = {
        "status": "PASS_REVIEWED_NC_WAVE_001_ADMISSION_NOT_FINAL_BENCHMARK_FREEZE",
        "base_candidate_count": len(base_rows),
        "new_reviewed_source_candidate_count": len(added_rows),
        "reviewed_sources_already_in_base_union": len(selected_hashes & set(base_by_hash)),
        "admitted_candidate_count": len(union_rows),
        "admitted_cluster_count": len(cluster_rows),
        "admitted_prompt_count": len(prompt_rows),
        "reviewed_single_fully_adequate_count": sum(
            row["label_status"] == "REVIEWED_SINGLE_FULLY_ADEQUATE_NOT_FINAL_GOLD_FREEZE" for row in prompt_rows
        ),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            union_path.name: sha256_file(union_path),
            cluster_path.name: sha256_file(cluster_path),
            prompt_path.name: sha256_file(prompt_path),
        },
        "claim_boundary": [
            "The three clusters and nine prompts are admitted to the NC pre-freeze workspace after source-hash and target-blinded adequacy reconciliation.",
            "No RQ1 prompt or label is transferred.",
            "The nine reviewed single-fully-adequate mappings are not a final gold freeze and are not human annotation or inter-rater reliability evidence.",
            "The 3,076-source candidate union still lacks new-source I1/I2/I3 materialisation and final integrity freezing.",
            "No retrieval, embedding, reranking, metric, or thesis result is produced.",
        ],
    }
    summary_path = OUTPUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
