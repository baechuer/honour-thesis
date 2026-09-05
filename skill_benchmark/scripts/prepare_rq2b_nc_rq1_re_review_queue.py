#!/usr/bin/env python3
"""Prepare a source-only re-review queue for all 79 frozen RQ1 clusters.

The queue carries source identities and a risk-priority heuristic only.  It
does not copy RQ1 prompts, gold labels, acceptable sets, or selector results.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMPATIBILITY = ROOT / "rq2b_naturalistic_confusability/manifests/rq1_frozen_cluster_compatibility_2026-08-31/rq1_frozen_cluster_nc_leads.jsonl"
PROVENANCE = ROOT / "rq2b_naturalistic_confusability/manifests/rq1_frozen_source_provenance_2026-08-31/source_provenance_audit.jsonl"
V3_IDENTITY = ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
OUTPUT_DIR = ROOT / "rq2b_naturalistic_confusability/review/rq1_frozen_cluster_re_review_queue_2026-08-31"


FIELD_PRIORITY = {
    "dependency_resource": (1, "hard resource/platform compatibility is often promptable, but provider-name leakage must be controlled"),
    "input_precondition": (1, "input state can define a natural first-route boundary"),
    "output_artifact": (2, "output distinction is promising but phase/container overlap must be checked"),
    "success_verification": (2, "verification requirement can separate peers but may be compositional"),
    "workflow_procedure": (3, "procedure differences may be implementation choices rather than routing necessities"),
    "use_condition": (4, "broad activation conditions often create multi-acceptable or hierarchical relations"),
    "boundary_not_for": (4, "negative boundaries require source reading and are vulnerable to artificial distractor cues"),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    required = [COMPATIBILITY, PROVENANCE, V3_IDENTITY]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    compatibility_rows = read_jsonl(COMPATIBILITY)
    if len(compatibility_rows) != 79:
        raise SystemExit(f"Expected 79 RQ1 cluster leads, found {len(compatibility_rows)}")
    provenance_by_hash = {str(row["source_sha256"]): row for row in read_jsonl(PROVENANCE)}
    v3_paths_by_hash: dict[str, list[str]] = defaultdict(list)
    for row in read_jsonl(V3_IDENTITY):
        v3_paths_by_hash[str(row["source_sha256"])].append(str(row["source"]))

    queue_rows: list[dict[str, Any]] = []
    field_counts: Counter[str] = Counter()
    arm_counts: Counter[str] = Counter()
    for cluster in compatibility_rows:
        primary_field = str(cluster["primary_field"])
        priority, risk_note = FIELD_PRIORITY.get(primary_field, (5, "unclassified field requires manual source reading"))
        source_packets: list[dict[str, Any]] = []
        for candidate in cluster["candidate_source_mappings"]:
            source_hash = str(candidate["source_sha256"])
            provenance = provenance_by_hash[source_hash]
            possible_paths = v3_paths_by_hash.get(source_hash, [])
            if possible_paths:
                source_path = ROOT.parent / possible_paths[0]
                source_binding = "PARENT_V3_EXACT_SOURCE"
            else:
                selected = provenance.get("selected_provenance_binding")
                if not selected:
                    raise SystemExit(f"No selected provenance binding for new source {source_hash}")
                source_path = ROOT / str(selected["original_path"])
                source_binding = "PINNED_RQ1_STAGED_ORIGINAL"
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"Source replay failed for {source_hash}: {source_path}")
            source_packets.append(
                {
                    "candidate_skill_id": candidate["rq1_candidate_skill_id"],
                    "source_sha256": source_hash,
                    "source_path": str(source_path),
                    "source_binding": source_binding,
                    "provenance_status": provenance["status"],
                }
            )

        # Triads are useful for richer ambiguity but cost more to adjudicate;
        # keep the field-risk tier primary and use cardinality only as a tie-break.
        queue_rows.append(
            {
                "review_queue_id": f"RQ2B-NC-RQ1-REVIEW-{len(queue_rows) + 1:03d}",
                "parent_rq1_cluster_id": cluster["parent_rq1_cluster_id"],
                "nc_lead_id": cluster["nc_lead_id"],
                "nc_intake_arm": cluster["nc_intake_arm"],
                "candidate_cardinality": cluster["candidate_cardinality"],
                "primary_field": primary_field,
                "priority_tier": priority,
                "initial_risk_note": risk_note,
                "candidate_sources": source_packets,
                "review_requirements": [
                    "Read full preserved sources without consulting any RQ1 prompt/gold or selector result.",
                    "State one bounded common user-task envelope shared by every candidate.",
                    "Identify the necessary task condition that makes each candidate non-substitutable.",
                    "Reject hierarchy, adapter, workflow-phase, broad-container, or generic-provider-only relations.",
                    "Decide whether a natural prompt can establish the boundary without target title/provider/path leakage.",
                    "Classify PROMOTE_TO_RQ2_PROMPT_AUTHORING, DEFER, or REJECT with source evidence.",
                ],
                "status": "SOURCE_ONLY_RQ2_RE_REVIEW_QUEUE_NOT_A_CLUSTER_OR_LABEL_DECISION",
            }
        )
        field_counts[primary_field] += 1
        arm_counts[str(cluster["nc_intake_arm"])] += 1

    queue_rows.sort(
        key=lambda row: (
            int(row["priority_tier"]),
            -int(row["candidate_cardinality"]),
            str(row["parent_rq1_cluster_id"]),
        )
    )
    for index, row in enumerate(queue_rows, start=1):
        row["review_order"] = index

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    queue_path = OUTPUT_DIR / "rq1_frozen_cluster_source_only_re_review_queue.jsonl"
    write_jsonl(queue_path, queue_rows)
    summary = {
        "status": "PASS_SOURCE_ONLY_RQ1_RE_REVIEW_QUEUE_NOT_A_RQ2_DECISION",
        "cluster_count": len(queue_rows),
        "candidate_source_reference_count": sum(len(row["candidate_sources"]) for row in queue_rows),
        "arm_counts": dict(sorted(arm_counts.items())),
        "primary_field_counts": dict(sorted(field_counts.items())),
        "priority_tier_counts": dict(sorted(Counter(str(row["priority_tier"]) for row in queue_rows).items())),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {queue_path.name: sha256_file(queue_path)},
        "claim_boundary": [
            "All 79 frozen RQ1 clusters are review candidates, not automatic RQ2 admissions.",
            "No RQ1 prompt, gold label, acceptable set, field effect, selector result, or metric is included.",
            "Priority is a workload heuristic only; every promotion requires full-source semantic review and new RQ2 prompt/adequacy review.",
        ],
    }
    summary_path = OUTPUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
