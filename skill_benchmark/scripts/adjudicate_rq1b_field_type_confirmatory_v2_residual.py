#!/usr/bin/env python3
"""Bind two opaque source-card residual reviews into the complete residual ledger."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import load_list, load_object, sha256_file, write_json
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze


def assessment_labels(response: dict, expected: set[tuple[str, str]]) -> dict[tuple[str, str], str]:
    rows = response.get("candidate_assessments")
    if not isinstance(rows, list):
        raise ValueError("residual response assessments are missing")
    labels = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("residual response assessment is invalid")
        key = (row.get("candidate"), row.get("field"))
        label = row.get("residual_label")
        if key not in expected or key in labels or label not in {"none", "partial", "substantial"}:
            raise ValueError("residual response target/label is invalid")
        labels[key] = label
    if set(labels) != expected:
        raise ValueError("residual response target set does not match packet")
    return labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--packet-id", required=True)
    parser.add_argument("--first-reviewer", required=True)
    parser.add_argument("--second-reviewer", required=True)
    args = parser.parse_args()
    if args.first_reviewer == args.second_reviewer:
        raise ValueError("two distinct residual reviewers are required")
    root = args.root
    verify_freeze(root)
    manifest_ids = {
        row.get("packet_id")
        for row in load_list(root / "residual_packet_manifest_opaque.json")
        if isinstance(row, dict)
    }
    maps = [
        row for row in load_list(root / "residual_packet_private_map.json")
        if isinstance(row, dict) and row.get("packet_id") == args.packet_id
    ]
    if args.packet_id not in manifest_ids or len(maps) != 1:
        raise ValueError("residual packet is absent from the frozen opaque manifest/map")
    packet_path = root / "residual_packets_opaque" / f"{args.packet_id}.json"
    packet = load_object(packet_path)
    if packet.get("packet_id") != args.packet_id or maps[0].get("packet_sha256") != sha256_file(packet_path):
        raise ValueError("residual packet binding is invalid")
    targets = packet.get("targets")
    expected = {
        (row.get("candidate"), row.get("field"))
        for row in targets
        if isinstance(row, dict)
    } if isinstance(targets, list) else set()
    if not expected or len(expected) != len(targets):
        raise ValueError("residual packet targets are invalid")
    reviewer_data = {}
    for reviewer in (args.first_reviewer, args.second_reviewer):
        response_path = root / "residual_reviews_opaque" / reviewer / f"{args.packet_id}.json"
        audit_path = root / "audits" / f"{args.packet_id}_{reviewer}_residual_review_audit.json"
        response, audit = load_object(response_path), load_object(audit_path)
        if (
            audit.get("valid") is not True
            or audit.get("packet_id") != args.packet_id
            or audit.get("reviewer") != reviewer
            or audit.get("packet_sha256") != sha256_file(packet_path)
            or audit.get("response_sha256") != sha256_file(response_path)
        ):
            raise ValueError(f"residual audit/response binding invalid: {reviewer}")
        reviewer_data[reviewer] = {
            "response_sha256": sha256_file(response_path),
            "audit_sha256": sha256_file(audit_path),
            "labels": assessment_labels(response, expected),
        }
    first, second = reviewer_data[args.first_reviewer], reviewer_data[args.second_reviewer]
    rows = []
    for candidate, field in sorted(expected):
        first_label, second_label = first["labels"][(candidate, field)], second["labels"][(candidate, field)]
        rows.append({
            "candidate": candidate,
            "field": field,
            "first_label": first_label,
            "second_label": second_label,
            "residual_label": first_label if first_label == second_label else "disagreed",
            "exact_agreement": first_label == second_label,
        })
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_OPAQUE_RESIDUAL_CONSENSUS_LEDGER_NOT_A_RESULT",
        "packet_id": args.packet_id,
        "packet_sha256": sha256_file(packet_path),
        "first_reviewer": args.first_reviewer,
        "second_reviewer": args.second_reviewer,
        "first_response_sha256": first["response_sha256"],
        "second_response_sha256": second["response_sha256"],
        "first_audit_sha256": first["audit_sha256"],
        "second_audit_sha256": second["audit_sha256"],
        "target_count": len(rows),
        "exact_agreement_count": sum(row["exact_agreement"] for row in rows),
        "rows": rows,
        "exclusions": [
            "No prompt, strict-gold join, field attribution, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    write_json(root / "residual_ledger_opaque" / f"{args.packet_id}.json", payload)
    print({"packet_id": args.packet_id, "target_count": len(rows), "exact_agreement_count": payload["exact_agreement_count"]})


if __name__ == "__main__":
    main()
