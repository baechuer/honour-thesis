#!/usr/bin/env python3
"""Integrate C3 Wave 002 cue reviews with explicit residual-risk boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


BOUNDARY = (
    "C3 records cue control and residual cue risk only. It is not a cue-safety proof, "
    "strict gold label, C4 adequacy decision, selector input, metric, or routing result."
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mechanical_resolution(record: dict[str, Any]) -> str:
    if record["source_phrase_hits"]:
        return (
            "Retained as a low-risk operational output description: the overlap is the generic request for a spreadsheet with one row per assessed item, not a source title, URL, command, package, or copied heading."
        )
    if record["title_phrase_hits"]:
        return (
            "Retained as a low-risk operational object/output overlap: the title-token detector matches non-contiguous generic invoice and reconciliation words, not a copied title string."
        )
    return "No mechanical title or source-phrase overlap was detected."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    parser.add_argument("--initial-reviews", type=Path, required=True)
    parser.add_argument("--recheck-reviews", type=Path, required=True)
    parser.add_argument("--mechanical-inventory", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.ledger.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_final_c3")

    c2_rows = read_jsonl(args.c2_ledger)
    mapping = {row["c2_packet_id"]: row for row in json.loads(args.sealed_mapping.read_text(encoding="utf-8"))}
    initial = {row["blind_packet_id"]: row for row in read_jsonl(args.initial_reviews)}
    recheck = {row["blind_packet_id"]: row for row in read_jsonl(args.recheck_reviews)}
    inventory = json.loads(args.mechanical_inventory.read_text(encoding="utf-8"))
    inventory_by_packet = {row["c2_packet_id"]: row for row in inventory["records"]}
    failures: list[str] = []
    final: list[dict[str, Any]] = []
    revision_blind_ids: set[str] = set()

    for c2 in c2_rows:
        packet_id = str(c2["c2_packet_id"])
        sealed = mapping.get(packet_id)
        mechanical = inventory_by_packet.get(packet_id)
        if sealed is None or mechanical is None:
            failures.append(f"lineage_missing:{packet_id}")
            continue
        blind_id = sealed["blind_packet_id"]
        revised = bool(c2.get("c3_cue_revision"))
        review = recheck.get(blind_id) if revised else initial.get(blind_id)
        if review is None:
            failures.append(f"review_missing:{blind_id}")
            continue
        if revised:
            revision_blind_ids.add(blind_id)
        if not revised and review["disposition"] != "ALLOW_AS_OPERATIONAL":
            failures.append(f"unrevised_nonallow_review:{blind_id}:{review['disposition']}")
            continue

        retained_high_risk = revised and review["disposition"] == "REJECT_UNSAFE_CUE"
        retained_medium_risk = revised and review["disposition"] == "REWRITE_CUE_ONLY"
        if retained_high_risk:
            principal_resolution = (
                "The recheck identifies a high operationally distinctive bundle but no title, URL, repository, package, command, template, or copied heading. Under C2 rule 2 and C3 handoff, retain it only with high residual-risk annotation; it may never be described as implicit semantic routing evidence."
            )
        elif retained_medium_risk:
            principal_resolution = (
                "The recheck identifies a medium operationally distinctive bundle after the cue-only rewrite but no accidental source identifier. Retain it with medium residual-risk annotation; it is not evidence of implicit semantic routing."
            )
        else:
            principal_resolution = "Independent C3 review found no remaining accidental source-identifying cue."

        final.append({
            "c2_packet_id": packet_id,
            "blind_packet_id": blind_id,
            "c1_review_id": c2["c1_review_id"],
            "sealed_target_source_id": c2["sealed_target_source_id"],
            "variant": c2["variant"],
            "c3_disposition": "C3_ALLOW_C4_WITH_RISK_ANNOTATION",
            "residual_cue_risk": review["residual_cue_risk"],
            "independent_review_disposition": review["disposition"],
            "independent_reviewer": review["reviewer"],
            "independent_exact_cue_phrases": review["exact_cue_phrases"],
            "independent_rationale": review["rationale"],
            "cue_only_revision_applied": revised,
            "retained_high_operational_risk": retained_high_risk,
            "retained_medium_operational_risk": retained_medium_risk,
            "principal_resolution": principal_resolution,
            "mechanical_overlap_resolution": mechanical_resolution(mechanical),
            "mechanical_title_phrase_hits": mechanical["title_phrase_hits"],
            "mechanical_short_name_token_hits": mechanical["short_source_name_token_hits"],
            "mechanical_source_phrase_hits": mechanical["source_phrase_hits"],
            "claim_boundary": BOUNDARY,
        })

    expected_revisions = {str(row["blind_packet_id"]) for row in mapping.values() if row["c2_packet_id"] in {str(c2["c2_packet_id"]) for c2 in c2_rows if c2.get("c3_cue_revision")}}
    if revision_blind_ids != expected_revisions:
        failures.append("recheck_coverage_mismatch")
    if inventory.get("failures"):
        failures.append("mechanical_inventory_failures")
    if len(final) != len(c2_rows):
        failures.append(f"final_coverage:{len(final)}:{len(c2_rows)}")
    if failures:
        raise SystemExit(";".join(failures))

    final.sort(key=lambda row: row["c2_packet_id"])
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    args.ledger.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in final),
        encoding="utf-8",
    )
    counts = Counter(row["residual_cue_risk"] for row in final)
    audit = {
        "status": "C3_FINAL_CUE_GATE_COMPLETE_WITH_RISK_ANNOTATIONS_NOT_A_LABEL_OR_RESULT",
        "packet_count": len(final),
        "allow_c4_count": len(final),
        "risk_counts": dict(sorted(counts.items())),
        "cue_only_revision_count": sum(row["cue_only_revision_applied"] for row in final),
        "retained_high_operational_risk_count": sum(row["retained_high_operational_risk"] for row in final),
        "retained_medium_operational_risk_count": sum(row["retained_medium_operational_risk"] for row in final),
        "c2_ledger_sha256": sha256(args.c2_ledger),
        "initial_reviews_sha256": sha256(args.initial_reviews),
        "recheck_reviews_sha256": sha256(args.recheck_reviews),
        "mechanical_inventory_sha256": sha256(args.mechanical_inventory),
        "final_ledger_sha256": sha256(args.ledger),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
        "exclusions": [
            "C4 adequacy review, strict gold labels, C5/C6 freeze, selector input, model/API calls, metrics and routing results remain unperformed.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
