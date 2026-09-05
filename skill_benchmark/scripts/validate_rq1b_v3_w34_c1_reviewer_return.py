#!/usr/bin/env python3
"""Validate byte binding and literal evidence in one Wave 034 C1 return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ALLOWED_OUTCOMES = {
    "ADVANCE_C2_PROMPT_CONSTRUCTION",
    "REJECT_SOURCE_BINDING",
    "REJECT_ABSENT_OPERATIONAL_CHAIN",
    "REJECT_NO_COMMON_ENVELOPE",
    "REJECT_NONPARALLEL_OR_COMPONENT",
    "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
    "NEEDS_PARENT_REVIEW",
}
FIELDS = ("trigger", "operation", "output", "boundary")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--reviewer-return", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--c1-review-id", action="append")
    parser.add_argument("--status-prefix", default="RQ1B_V3_W34")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    args = parse_args()
    roster = {
        row["c1_review_id"]: row
        for row in (
            json.loads(line)
            for line in args.roster.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    if args.c1_review_id:
        requested = set(args.c1_review_id)
        unknown = requested - set(roster)
        if unknown:
            raise SystemExit(f"unknown_c1_review_ids:{','.join(sorted(unknown))}")
        roster = {review_id: row for review_id, row in roster.items() if review_id in requested}
    returned = json.loads(args.reviewer_return.read_text(encoding="utf-8"))
    reviews = returned.get("reviews") if isinstance(returned, dict) else returned
    if not isinstance(reviews, list):
        raise SystemExit("missing_reviews")

    expected = set(roster)
    observed = {review.get("c1_review_id") for review in reviews}
    failures = []
    if observed != expected:
        failures.append({"problem": "review_id_set_mismatch", "expected": sorted(expected), "observed": sorted(str(value) for value in observed)})
    audits = []
    for review in reviews:
        review_id = review.get("c1_review_id")
        packet = roster.get(review_id)
        if packet is None:
            continue
        outcome = review.get("allowed_outcome")
        if outcome not in ALLOWED_OUTCOMES:
            failures.append({"c1_review_id": review_id, "problem": "invalid_allowed_outcome"})
        evidence = review.get("source_evidence")
        if not isinstance(evidence, list):
            failures.append({"c1_review_id": review_id, "problem": "source_evidence_not_list"})
            continue
        members = {member["source_id"]: member for member in packet["members"]}
        cells = []
        evidence_ids = {item.get("source_id") for item in evidence if isinstance(item, dict)}
        if evidence_ids != set(members):
            failures.append({"c1_review_id": review_id, "problem": "source_evidence_id_mismatch"})
        for item in evidence:
            source_id = item.get("source_id")
            member = members.get(source_id)
            if member is None:
                continue
            path = Path(member["absolute_path"])
            text = path.read_text(encoding="utf-8", errors="strict") if path.is_file() else ""
            hash_ok = path.is_file() and sha256(path) == member["sha256"]
            field_status = {}
            for field in FIELDS:
                value = item.get(field)
                valid = isinstance(value, str) and (value == "NOT STATED" or value in text)
                field_status[field] = valid
                if not valid:
                    failures.append({"c1_review_id": review_id, "source_id": source_id, "problem": f"invalid_literal_{field}"})
            if not hash_ok:
                failures.append({"c1_review_id": review_id, "source_id": source_id, "problem": "source_hash_mismatch"})
            cells.append({"source_id": source_id, "source_hash_ok": hash_ok, "field_literal_validity": field_status})
        audits.append({"c1_review_id": review_id, "literal_cells": cells})

    report = {
        "status": (
            f"{args.status_prefix}_C1_REVIEWER_LITERAL_AUDIT_PASS"
            if not failures
            else f"{args.status_prefix}_C1_REVIEWER_LITERAL_AUDIT_FAIL"
        ),
        "reviewer_return": str(args.reviewer_return),
        "review_count": len(reviews),
        "failure_count": len(failures),
        "failures": failures,
        "audits": audits,
        "boundary": "The audit verifies only review coverage, source-byte binding and returned exact evidence spans. It does not determine common envelope, peer parallelism, C1 outcome validity, prompt fitness, label validity, selector behaviour, metric or result.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "review_count", "failure_count")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
