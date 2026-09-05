#!/usr/bin/env python3
"""Seal the two-reviewer/packet-only-coordinator adjudication of exact reuse."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
SEMANTIC = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_semantic_qa_300plus_2026-09-05_v2"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cross_cluster_reuse_adjudication_2026-09-05"

# These are verbatim structured decisions returned by the two independent
# Terra-high reviewers in this task.  The coordinator values below are its
# packet-only resolutions of the two disagreements, not fresh source reviews.
A = {
    "SRCREL-001": ("RELATED_BUT_DISTINCT", "The shared Unit Economics source is used in distinct cluster contexts: TAM/MRR modelling versus gym client-financed acquisition/financial planning."),
    "SRCREL-002": ("RELATED_BUT_DISTINCT", "NDA review versus tabular extraction differs from the legal-document-type contrast."),
    "SRCREL-003": ("RELATED_BUT_DISTINCT", "Employment review versus tabular extraction differs from the three-document-type legal-review contrast."),
    "SRCREL-004": ("RELATED_BUT_DISTINCT", "Shareholder review versus tabular extraction differs from the three-document-type legal-review contrast."),
    "SRCREL-005": ("DUPLICATE_CLUSTER", "The complete two-source deliverability contrast is contained unchanged in the local triad."),
    "SRCREL-006": ("RELATED_BUT_DISTINCT", "Broad research synthesis versus interview affinity mapping differs from interview-only/general/mixed-method synthesis alternatives."),
    "SRCREL-007": ("RELATED_BUT_DISTINCT", "MSA drafting-versus-review differs from commercial-purchase/SaaS/general MSA-review alternatives."),
    "SRCREL-008": ("DUPLICATE_CLUSTER", "The same complete two-source deliverability contrast is contained unchanged in the local triad."),
}
B = {
    "SRCREL-001": ("DUPLICATE_CLUSTER", "Both triads centre the same Unit Economics CAC, contribution, LTV and payback procedure; surrounding finance members do not restore independence."),
    "SRCREL-002": ("RELATED_BUT_DISTINCT", "The shared NDA-review workflow removes source independence, but the triad-level contrast differs."),
    "SRCREL-003": ("RELATED_BUT_DISTINCT", "The shared employment-review workflow removes source independence, but the triad-level contrast differs."),
    "SRCREL-004": ("RELATED_BUT_DISTINCT", "The shared shareholder-review workflow removes source independence, but the triad-level contrast differs."),
    "SRCREL-005": ("DUPLICATE_CLUSTER", "The checkpoint deliverability pair is embedded unchanged in the local triad."),
    "SRCREL-006": ("DUPLICATE_CLUSTER", "The shared Interview Synthesis workflow is the same raw-interview, affinity-mapping, theme/frequency/quote/saturation task."),
    "SRCREL-007": ("RELATED_BUT_DISTINCT", "The shared MSA-review source removes source independence, but the triad-level contrast differs."),
    "SRCREL-008": ("DUPLICATE_CLUSTER", "The checkpoint deliverability pair is embedded unchanged in the local triad."),
}
COORDINATOR = {
    "SRCREL-001": ("BLOCKED_OR_UNCLEAR", "Both reviewers agree the triads are not independent but disagree whether the shared Unit Economics core makes them duplicate or neighbouring workflows."),
    "SRCREL-006": ("BLOCKED_OR_UNCLEAR", "Both reviewers agree the triads are not independent but disagree whether interview-only affinity mapping is distinct or a specialization of the same task."),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite cross-reuse adjudication: {out}")
    packet_path = SEMANTIC / "source_relation_reviewer_packet.jsonl"
    screen_path = SEMANTIC / "source_relation_screen.jsonl"
    if not SOP.is_file() or not packet_path.is_file() or not screen_path.is_file():
        raise SystemExit("Required Phase-3 semantic-QA binding is missing")
    packets = read_jsonl(packet_path)
    ids = [str(row.get("packet_id")) for row in packets]
    if ids != [f"SRCREL-{index:03d}" for index in range(1, 9)] or set(A) != set(ids) or set(B) != set(ids):
        raise SystemExit("Source-relation packet/return identity drift")
    base = {
        "review_protocol": "AI-assisted independent structured review; no retrieval, reranking, rank, acceptable-set, or result information was supplied.",
        "reviewer_model": "gpt-5.6-terra", "reasoning_effort": "high",
        "source_relation_packet_sha256": sha(packet_path),
        "triad_independence_preserved": False,
        "source_disjoint_final_nc_library": False,
    }
    reviewer_a = [{**base, "packet_id": key, "reviewer": "A", "relation_decision": decision, "rationale": rationale} for key, (decision, rationale) in A.items()]
    reviewer_b = [{**base, "packet_id": key, "reviewer": "B", "relation_decision": decision, "rationale": rationale} for key, (decision, rationale) in B.items()]
    coordinator_packet = [{
        "packet_id": key, "review_boundary": "Sealed reviewer disagreement only; do not inspect source files, prompt labels, retrieval, or results.",
        "reviewer_a_return": next(row for row in reviewer_a if row["packet_id"] == key),
        "reviewer_b_return": next(row for row in reviewer_b if row["packet_id"] == key),
    } for key in COORDINATOR]
    coordinator_return = [{
        "packet_id": key, "reviewer": "COORDINATOR", "reviewer_model": "gpt-5.6-terra", "reasoning_effort": "high",
        "relation_decision": decision, "rationale": rationale,
        "source_disjoint_final_nc_library": False,
    } for key, (decision, rationale) in COORDINATOR.items()]
    final = []
    for key in ids:
        decision = A[key][0] if A[key][0] == B[key][0] else COORDINATOR[key][0]
        final.append({
            "packet_id": key,
            "final_cross_cluster_disposition": decision,
            "triad_independence_preserved": False,
            "source_disjoint_final_nc_library": False,
            "phase3_admission_disposition": "BLOCKED_PENDING_EXCLUSION_OR_EXPLICIT_METHOD_DECISION",
            "claim_boundary": "A relation decision is not a final acceptable-set label or a retrieval result. No affected record may enter the Phase-4 audit-input freeze until this admission block is resolved.",
        })
    summary = {
        "status": "BLOCKED_PHASE3_CROSS_CLUSTER_SOURCE_REUSE_REQUIRES_EXCLUSION_OR_METHOD_DECISION",
        "bound_inputs": {
            str(SOP.relative_to(WORKSPACE)): sha(SOP),
            str(packet_path.relative_to(WORKSPACE)): sha(packet_path),
            str(screen_path.relative_to(WORKSPACE)): sha(screen_path),
        },
        "counts": {"reviewed_exact_reuses": 8, "duplicate_cluster": sum(row["final_cross_cluster_disposition"] == "DUPLICATE_CLUSTER" for row in final), "related_but_distinct": sum(row["final_cross_cluster_disposition"] == "RELATED_BUT_DISTINCT" for row in final), "blocked_or_unclear": sum(row["final_cross_cluster_disposition"] == "BLOCKED_OR_UNCLEAR" for row in final), "admission_blocked": 8},
        "claim_boundary": "This package preserves two independent reviews and sealed coordinator resolutions. It does not silently merge clusters, waive source-disjointness, change the source universe, or freeze audit input.",
        "outputs": {},
    }
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    files = {"reviewer_a_return.jsonl": reviewer_a, "reviewer_b_return.jsonl": reviewer_b, "coordinator_packet.jsonl": coordinator_packet, "coordinator_return.jsonl": coordinator_return, "final_cross_cluster_dispositions.jsonl": final}
    for name, rows in files.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
