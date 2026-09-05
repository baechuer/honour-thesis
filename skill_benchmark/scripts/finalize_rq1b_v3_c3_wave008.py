#!/usr/bin/env python3
"""Finalise Wave 008 C3R1 cue control from a source-deidentified review."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


BOUNDARY = (
    "C3 records cue control and residual cue risk only. It is not a cue-safety proof, "
    "strict gold label, C4 adequacy decision, selector input, metric, or routing result."
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    parser.add_argument("--final-reviews", type=Path, required=True)
    parser.add_argument("--mechanical-inventory", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.ledger.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_final_c3")

    c2 = {str(row["c2_packet_id"]): row for row in read_jsonl(args.c2_ledger)}
    mapping_rows = json.loads(args.sealed_mapping.read_text(encoding="utf-8"))
    mapping = {str(row["c2_packet_id"]): row for row in mapping_rows}
    reviews = {str(row["blind_packet_id"]): row for row in read_jsonl(args.final_reviews)}
    mechanical = json.loads(args.mechanical_inventory.read_text(encoding="utf-8"))
    mechanical_by_packet = {str(row["c2_packet_id"]): row for row in mechanical["records"]}
    expected_blind = {str(row["blind_packet_id"]) for row in mapping_rows}
    if set(c2) != set(mapping) or set(reviews) != expected_blind or mechanical.get("failures"):
        raise SystemExit("lineage_or_review_coverage_failure")

    final: list[dict[str, Any]] = []
    for packet_id, record in c2.items():
        sealed = mapping[packet_id]
        review = reviews[str(sealed["blind_packet_id"])]
        inventory = mechanical_by_packet.get(packet_id)
        if inventory is None or review.get("final_disposition") != "ALLOW_AS_OPERATIONAL":
            raise SystemExit(f"not_allowed_for_c4:{packet_id}")
        final.append({
            "c2_packet_id": packet_id,
            "blind_packet_id": sealed["blind_packet_id"],
            "c1_review_id": record["c1_review_id"],
            "sealed_target_source_id": record["sealed_target_source_id"],
            "variant": record["variant"],
            "c3_disposition": "C3_ALLOW_C4_WITH_RISK_ANNOTATION",
            "residual_cue_risk": review["final_residual_cue_risk"],
            "final_review_disposition": review["final_disposition"],
            "final_exact_accidental_cue_phrases": review["exact_accidental_cue_phrases"],
            "final_rationale": review["rationale"],
            "cue_only_revision_applied": bool(record.get("c3_revision_lineage")),
            "mechanical_title_phrase_hits": inventory["title_phrase_hits"],
            "mechanical_short_name_token_hits": inventory["short_source_name_token_hits"],
            "mechanical_source_phrase_hits": inventory["source_phrase_hits"],
            "mechanical_resolution": "Title and short-name hits are shared task vocabulary only; C3R1 found no accidental identifier or distinctive coupled procedure.",
            "claim_boundary": BOUNDARY,
        })

    final.sort(key=lambda row: row["c2_packet_id"])
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    args.ledger.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in final), encoding="utf-8")
    audit = {
        "status": "C3_FINAL_CUE_GATE_COMPLETE_WITH_RISK_ANNOTATIONS_NOT_A_LABEL_OR_RESULT",
        "packet_count": len(final),
        "allow_c4_count": len(final),
        "risk_counts": {"low": sum(row["residual_cue_risk"] == "low" for row in final)},
        "cue_only_revision_count": sum(row["cue_only_revision_applied"] for row in final),
        "c2_ledger_sha256": digest(args.c2_ledger),
        "sealed_mapping_sha256": digest(args.sealed_mapping),
        "final_review_sha256": digest(args.final_reviews),
        "mechanical_inventory_sha256": digest(args.mechanical_inventory),
        "final_ledger_sha256": digest(args.ledger),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
        "exclusions": ["C4 adequacy review, strict labels, C5/C6 freeze, selector input, model/API calls, metrics, and routing results remain unperformed."],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
