#!/usr/bin/env python3
"""Classify frozen RQ1b clusters as RQ2b-NC prompt or source-intake leads.

This is a local, hash-based compatibility audit. It does not copy RQ1 prompts
or labels, construct an RQ2 prompt, establish semantic validity, or compute a
retrieval metric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_V3_IDENTITY = ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
DEFAULT_WAVE_001 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_001_frozen_manifest.jsonl"
DEFAULT_WAVE_002 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_002_frozen_manifest.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "rq2b_naturalistic_confusability/manifests/rq1_frozen_cluster_compatibility_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v3-identity", type=Path, default=DEFAULT_V3_IDENTITY)
    parser.add_argument("--wave-001", type=Path, default=DEFAULT_WAVE_001)
    parser.add_argument("--wave-002", type=Path, default=DEFAULT_WAVE_002)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = [args.v3_identity, args.wave_001, args.wave_002]
    missing = [str(path) for path in inputs if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    v3_rows = read_jsonl(args.v3_identity)
    v3_by_hash: dict[str, list[str]] = {}
    for row in v3_rows:
        source_hash = str(row["source_sha256"])
        v3_by_hash.setdefault(source_hash, []).append(str(row["skill_id"]))
    for skill_ids in v3_by_hash.values():
        skill_ids.sort()

    parent_rows = [
        ("wave_001", args.wave_001, read_jsonl(args.wave_001)),
        ("wave_002", args.wave_002, read_jsonl(args.wave_002)),
    ]
    output_rows: list[dict[str, Any]] = []
    seen_rq1_skill_ids: set[str] = set()
    seen_cluster_ids: set[str] = set()

    for parent_wave, parent_path, rows in parent_rows:
        for row in rows:
            cluster_id = str(row["cluster_id"])
            if cluster_id in seen_cluster_ids:
                raise SystemExit(f"Duplicate RQ1 cluster id: {cluster_id}")
            seen_cluster_ids.add(cluster_id)

            candidate_ids = [str(value) for value in row["candidate_skill_ids"]]
            source_hashes_raw = {str(key): str(value) for key, value in dict(row["source_hashes"]).items()}
            if set(candidate_ids) != set(source_hashes_raw):
                raise SystemExit(f"Candidate/source key mismatch in {cluster_id}")
            duplicate_ids = sorted(set(candidate_ids) & seen_rq1_skill_ids)
            if duplicate_ids:
                raise SystemExit(f"Frozen RQ1 candidate reuse across clusters: {cluster_id}: {duplicate_ids}")
            seen_rq1_skill_ids.update(candidate_ids)

            mappings = [
                {
                    "rq1_candidate_skill_id": skill_id,
                    "source_sha256": source_hashes_raw[skill_id],
                    "v3_skill_ids_with_exact_source": v3_by_hash.get(source_hashes_raw[skill_id], []),
                }
                for skill_id in candidate_ids
            ]
            v3_count = sum(bool(item["v3_skill_ids_with_exact_source"]) for item in mappings)
            arm = (
                "NC-P_EXISTING_V3_PROMPT_LEAD"
                if v3_count == len(mappings)
                else "NC-S_NEW_SOURCE_INTAKE_LEAD"
                if v3_count == 0
                else "MIXED_REQUIRES_FINAL_LIBRARY_RESOLUTION"
            )
            output_rows.append(
                {
                    "nc_lead_id": f"NC-RQ1-FROZEN-{cluster_id}",
                    "parent_rq1_wave": parent_wave,
                    "parent_rq1_manifest": str(parent_path.relative_to(ROOT)),
                    "parent_rq1_cluster_id": cluster_id,
                    "candidate_cardinality": len(candidate_ids),
                    "primary_field": row.get("primary_field"),
                    "candidate_source_mappings": mappings,
                    "v3_exact_candidate_count": v3_count,
                    "nc_intake_arm": arm,
                    "status": "FROZEN_RQ1_CURATION_LEAD_PENDING_NC_PROVENANCE_CLUSTER_CUE_AND_ADEQUACY_REVIEW",
                    "non_transfer_rule": (
                        "No RQ1 prompt, strict label, acceptable set, field effect, or selector result is copied. "
                        "The RQ1 record is only curation provenance and a source/cluster lead."
                    ),
                }
            )

    output_rows.sort(key=lambda row: row["parent_rq1_cluster_id"])
    counts = Counter(row["nc_intake_arm"] for row in output_rows)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    leads_path = output_dir / "rq1_frozen_cluster_nc_leads.jsonl"
    write_jsonl(leads_path, output_rows)

    summary = {
        "status": "PASS_HASH_COMPATIBILITY_AUDIT_NOT_AN_NC_FREEZE_OR_RESULT",
        "claim_boundary": [
            "Exact hash inclusion only; title and semantic similarity do not count as a V3 reuse.",
            "NC-P means a new RQ2 prompt may later be reviewed over an existing V3 candidate, not that a prompt or label was imported.",
            "NC-S means every candidate still needs NC provenance, licence, cluster, prompt, label and representation gates.",
            "No retrieval, embedding, reranking, model, external API or network call occurred.",
        ],
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in inputs},
        "v3_identity_rows": len(v3_rows),
        "v3_unique_source_hashes": len(v3_by_hash),
        "rq1_frozen_cluster_count": len(output_rows),
        "rq1_frozen_unique_candidate_count": len(seen_rq1_skill_ids),
        "nc_intake_arm_counts": dict(sorted(counts.items())),
        "artifacts": {
            "rq1_frozen_cluster_nc_leads.jsonl": sha256_file(leads_path),
        },
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
