#!/usr/bin/env python3
"""Finalise the W7 C3 cue ledger without turning it into a routing result.

The initial independent C3 review covers all 12 C2 packets. Four packets
received a separately preserved cue-only r1 rewrite and independent recheck.
This script validates that lineage and records the final C3 disposition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    indexed = {str(row.get(key, "")): row for row in rows}
    if "" in indexed or len(indexed) != len(rows):
        raise SystemExit(f"duplicate_or_blank_{label}")
    return indexed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    parser.add_argument("--initial-c3", type=Path, required=True)
    parser.add_argument("--revision-lineage", type=Path, required=True)
    parser.add_argument("--recheck-c3", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_final_c3_output")

    c2_by_id = index_unique(read_jsonl(args.c2_ledger), "c2_packet_id", "c2_packet_id")
    sealed_by_blind = index_unique(read_json(args.sealed_mapping), "blind_packet_id", "blind_packet_id")
    if len(sealed_by_blind) != len(c2_by_id):
        raise SystemExit("sealed_mapping_c2_count_mismatch")
    mapping_c2_ids = {str(row.get("c2_packet_id", "")) for row in sealed_by_blind.values()}
    if mapping_c2_ids != set(c2_by_id):
        raise SystemExit("sealed_mapping_c2_coverage_mismatch")

    initial_by_blind = index_unique(read_jsonl(args.initial_c3), "blind_packet_id", "initial_c3_blind_packet_id")
    if set(initial_by_blind) != set(sealed_by_blind):
        raise SystemExit("initial_c3_coverage_mismatch")
    revision_rows = read_json(args.revision_lineage)
    revised_blind_ids = {str(row.get("blind_packet_id", "")) for row in revision_rows}
    if len(revised_blind_ids) != len(revision_rows) or not revised_blind_ids:
        raise SystemExit("invalid_revision_lineage")
    recheck_by_blind = index_unique(read_jsonl(args.recheck_c3), "blind_packet_id", "recheck_c3_blind_packet_id")
    if set(recheck_by_blind) != revised_blind_ids:
        raise SystemExit("recheck_c3_coverage_mismatch")

    final_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for blind_id, sealed in sorted(sealed_by_blind.items()):
        c2_id = str(sealed["c2_packet_id"])
        c2 = c2_by_id[c2_id]
        initial = initial_by_blind[blind_id]
        use_recheck = blind_id in revised_blind_ids
        review = recheck_by_blind[blind_id] if use_recheck else initial
        if use_recheck and initial.get("disposition") != "REWRITE_CUE_ONLY":
            failures.append(f"revision_without_initial_rewrite:{blind_id}")
        if not use_recheck and initial.get("disposition") != "ALLOW_AS_OPERATIONAL":
            failures.append(f"unresolved_initial_disposition:{blind_id}:{initial.get('disposition')}")
        if use_recheck and review.get("disposition") not in {"ALLOW_AS_OPERATIONAL", "REJECT_UNSAFE_CUE"}:
            failures.append(f"invalid_recheck_disposition:{blind_id}:{review.get('disposition')}")
        if str(sealed.get("sealed_target_source_id")) != str(c2.get("sealed_target_source_id")):
            failures.append(f"sealed_target_mismatch:{blind_id}")
        final_rows.append({
            "blind_packet_id": blind_id,
            "c2_packet_id": c2_id,
            "c1_review_id": c2["c1_review_id"],
            "sealed_target_source_id": c2["sealed_target_source_id"],
            "variant": c2["variant"],
            "prompt_text": c2["prompt_text"],
            "c3_review_round": "c3r1_recheck" if use_recheck else "c3_initial",
            "final_c3_residual_cue_risk": review["residual_cue_risk"],
            "final_c3_disposition": review["disposition"],
            "final_c3_exact_cue_phrases": review["exact_cue_phrases"],
            "final_c3_rationale": review["rationale"],
            "claim_boundary": "C3 cue disposition only. It is not a cue-safety proof, C4 adequacy decision, strict gold label, selector input, metric or routing result.",
        })
    if failures:
        raise SystemExit(";".join(failures))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in final_rows),
        encoding="utf-8",
    )
    disposition_counts: dict[str, int] = {}
    for row in final_rows:
        disposition = str(row["final_c3_disposition"])
        disposition_counts[disposition] = disposition_counts.get(disposition, 0) + 1
    audit = {
        "status": "RQ1B_V3_C3_W7R1_FINALISATION_PASS_NOT_A_LABEL_OR_RESULT",
        "c2_ledger_sha256": sha256_file(args.c2_ledger),
        "sealed_mapping_sha256": sha256_file(args.sealed_mapping),
        "initial_c3_sha256": sha256_file(args.initial_c3),
        "revision_lineage_sha256": sha256_file(args.revision_lineage),
        "recheck_c3_sha256": sha256_file(args.recheck_c3),
        "final_ledger_sha256": sha256_file(args.output),
        "packet_count": len(final_rows),
        "c4_eligible_packet_count": disposition_counts.get("ALLOW_AS_OPERATIONAL", 0),
        "unsafe_cue_reject_count": disposition_counts.get("REJECT_UNSAFE_CUE", 0),
        "final_disposition_counts": disposition_counts,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "C3 does not establish cue safety, semantic fidelity, a valid cluster, a gold label, C4 adequacy, selector performance, field recoverability, or routing quality.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
