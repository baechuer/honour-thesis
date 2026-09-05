#!/usr/bin/env python3
"""Fail closed on structural/source-identifier leakage in RQ1b V3 C4B packets.

The check validates only reviewer-input construction.  It does not judge
adequacy, unseal the construction target, select a gold skill, or score a
retriever.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FIELD_ORDER = {
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
}
ALLOWED_RESPONSES = {"ONE_FULLY_ADEQUATE", "MULTIPLE_ADEQUATE", "NONE_ADEQUATE", "UNCERTAIN"}
FORBIDDEN_KEYS = {"source_id", "source_sha256", "sealed_target_source_id", "canonical_card_label", "composition_id", "c2_packet_id"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_row_not_object:{path}:{number}")
            rows.append(value)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-packets", type=Path, action="append", required=True)
    parser.add_argument("--unpermutation-key", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    return parser.parse_args()


def contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(key in FORBIDDEN_KEYS or contains_forbidden_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_forbidden_key(item) for item in value)
    return False


def main() -> int:
    args = parse_args()
    key_rows = read_jsonl(args.unpermutation_key)
    key_by_id = {str(row.get("review_packet_id", "")): row for row in key_rows}
    failures: list[str] = []
    if len(key_by_id) != len(key_rows) or not key_by_id:
        failures.append("invalid_or_duplicate_key_rows")

    expected_ids: set[str] = set()
    reviewer_counts: list[int] = []
    for packet_path in args.reviewer_packets:
        rows = read_jsonl(packet_path)
        reviewer_counts.append(len(rows))
        local_ids: set[str] = set()
        for row in rows:
            packet_id = str(row.get("review_packet_id", ""))
            if not packet_id or packet_id in local_ids:
                failures.append(f"duplicate_or_missing_packet_id:{packet_path}:{packet_id}")
            local_ids.add(packet_id)
            expected_ids.add(packet_id)
            if packet_id not in key_by_id:
                failures.append(f"packet_not_in_key:{packet_id}")
            if row.get("status") != "RQ1B_V3_C4B_KEY_BLIND_ADEQUACY_PACKET_NOT_A_LABEL_OR_RESULT":
                failures.append(f"bad_status:{packet_id}")
            if contains_forbidden_key(row):
                failures.append(f"forbidden_key_in_reviewer_packet:{packet_id}")
            cards = row.get("candidate_cards")
            if not isinstance(cards, list) or len(cards) not in {3, 4}:
                failures.append(f"candidate_count:{packet_id}")
                continue
            labels = [str(card.get("card_label", "")) for card in cards if isinstance(card, dict)]
            if labels != [f"Candidate {chr(65 + index)}" for index in range(len(cards))]:
                failures.append(f"noncanonical_anonymous_labels:{packet_id}")
            if set(row.get("allowed_response_labels", [])) != ALLOWED_RESPONSES:
                failures.append(f"response_labels:{packet_id}")
            serialized = json.dumps(row, ensure_ascii=True, sort_keys=True)
            if re.search(r"https?://|github\\.com|RQ1B-V3-SRC-|[0-9a-f]{64}", serialized, re.IGNORECASE):
                failures.append(f"generic_identity_or_hash_marker:{packet_id}")
            for card in cards:
                card_body = card.get("card") if isinstance(card, dict) else None
                if not isinstance(card_body, dict) or set(card_body) != FIELD_ORDER:
                    failures.append(f"card_schema:{packet_id}")
                    continue
                for field in FIELD_ORDER:
                    value = card_body[field]
                    if not isinstance(value, dict) or value.get("status") not in {"EVIDENCE", "NOT_STATED"} or not isinstance(value.get("quotes"), list):
                        failures.append(f"field_schema:{packet_id}:{field}")

    if expected_ids != set(key_by_id):
        failures.append("reviewer_key_coverage_mismatch")
    report = {
        "status": "RQ1B_V3_C4B_BLINDNESS_AUDIT_PASS_NOT_A_RESULT" if not failures else "RQ1B_V3_C4B_BLINDNESS_AUDIT_FAIL_NOT_A_RESULT",
        "reviewer_packet_file_count": len(args.reviewer_packets),
        "reviewer_packet_counts": reviewer_counts,
        "unpermutation_key_rows": len(key_rows),
        "failures": sorted(set(failures)),
        "boundary": "This audit checks blind packet construction only; it does not create adequacy, strict-gold, retrieval, metric, or result evidence.",
    }
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    args.audit.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
