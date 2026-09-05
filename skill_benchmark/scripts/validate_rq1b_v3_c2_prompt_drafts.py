#!/usr/bin/env python3
"""Validate local RQ1b V3 C2 prompt-draft coverage and source-card bindings.

This is a mechanical C2 check only. It creates neither a strict gold label nor
a C3 cue decision, C4 adequacy decision, C5/C6 freeze, retrieval input, model
call, metric, or result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_VARIANTS = {"direct", "paraphrase"}
ALLOWED_DISPOSITIONS = {
    "C2_DRAFT_FOR_C3",
    "C2_REJECT_UNSAFE_OR_MULTI_ADEQUATE_RISK",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--draft", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument(
        "--assign-c2-packet-ids",
        action="store_true",
        help="Assign deterministic packet IDs to legacy draft rows that lack them.",
    )
    args = parser.parse_args()

    roster_rows = read_jsonl(args.roster)
    expected_by_c1: dict[str, set[str]] = {}
    failures: list[str] = []
    for row in roster_rows:
        ledger = Path(str(row["ledger_path"]))
        if not ledger.is_file():
            failures.append(f"missing_c1_ledger:{ledger}")
            continue
        if sha256_file(ledger) != row["ledger_sha256"]:
            failures.append(f"c1_ledger_hash_drift:{row['c1_review_id']}")
            continue
        matching = [record for record in read_jsonl(ledger) if record.get("c1_review_id") == row["c1_review_id"]]
        if len(matching) != 1:
            failures.append(f"c1_ledger_coverage:{row['c1_review_id']}:{len(matching)}")
            continue
        record = matching[0]
        if record.get("final_c1_outcome") != "ADVANCE_C2_PROMPT_CONSTRUCTION":
            failures.append(f"c1_not_advanced:{row['c1_review_id']}")
            continue
        expected_by_c1[str(row["c1_review_id"])] = set(record["member_source_ids"])

    rows = [record for path in args.draft for record in read_jsonl(path)]
    if args.assign_c2_packet_ids:
        for record in rows:
            if record.get("c2_packet_id"):
                continue
            c1_id = str(record.get("c1_review_id", ""))
            target = str(record.get("sealed_target_source_id", ""))
            variant = str(record.get("variant", "")).upper()
            c1_parts = c1_id.split("-")
            target_suffix = target.rsplit("-", 1)[-1]
            if len(c1_parts) < 3 or not target_suffix or variant not in {"DIRECT", "PARAPHRASE"}:
                failures.append(f"cannot_assign_c2_packet_id:{c1_id}:{target}:{variant}")
                continue
            c1_token = "-".join(c1_parts[-2:])
            record["c2_packet_id"] = f"RQ1B-V3-D1-C2-{c1_token}-{target_suffix}-{variant}"
    counts: Counter[tuple[str, str, str]] = Counter()
    for index, record in enumerate(rows, start=1):
        c1_id = str(record.get("c1_review_id", ""))
        target = str(record.get("sealed_target_source_id", ""))
        variant = str(record.get("variant", ""))
        disposition = str(record.get("c2_disposition", ""))
        prefix = f"row:{index}:{c1_id}:{target}:{variant}"
        if c1_id not in expected_by_c1:
            failures.append(f"{prefix}:unexpected_c1_review")
        elif target not in expected_by_c1[c1_id]:
            failures.append(f"{prefix}:target_not_member")
        if variant not in ALLOWED_VARIANTS:
            failures.append(f"{prefix}:invalid_variant")
        if disposition not in ALLOWED_DISPOSITIONS:
            failures.append(f"{prefix}:invalid_disposition")
        prompt = record.get("prompt_text")
        if disposition == "C2_DRAFT_FOR_C3":
            if not isinstance(prompt, str) or not prompt.strip():
                failures.append(f"{prefix}:blank_draft_prompt")
            for key in ("intended_operational_constraints", "construction_rationale", "avoided_source_cues"):
                value = record.get(key)
                if not value:
                    failures.append(f"{prefix}:missing_{key}")
        if disposition == "C2_REJECT_UNSAFE_OR_MULTI_ADEQUATE_RISK":
            if not isinstance(record.get("rejection_reason"), str) or not record["rejection_reason"].strip():
                failures.append(f"{prefix}:missing_rejection_reason")
        counts[(c1_id, target, variant)] += 1

    for c1_id, targets in sorted(expected_by_c1.items()):
        for target in sorted(targets):
            for variant in sorted(ALLOWED_VARIANTS):
                count = counts[(c1_id, target, variant)]
                if count != 1:
                    failures.append(f"coverage:{c1_id}:{target}:{variant}:{count}")

    rows.sort(key=lambda item: (
        str(item.get("c1_review_id", "")),
        str(item.get("sealed_target_source_id", "")),
        str(item.get("variant", "")),
    ))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    draft_count = sum(row.get("c2_disposition") == "C2_DRAFT_FOR_C3" for row in rows)
    rejection_count = sum(row.get("c2_disposition") == "C2_REJECT_UNSAFE_OR_MULTI_ADEQUATE_RISK" for row in rows)
    summary = {
        "status": "C2_DRAFT_BINDING_PASS_NOT_A_LABEL_OR_RESULT" if not failures else "C2_DRAFT_BINDING_FAIL_NOT_A_LABEL_OR_RESULT",
        "roster_rows": len(roster_rows),
        "c1_approved_compositions": len(expected_by_c1),
        "expected_candidate_variant_records": 2 * sum(len(ids) for ids in expected_by_c1.values()),
        "received_records": len(rows),
        "c2_draft_records": draft_count,
        "c2_rejection_records": rejection_count,
        "failures": failures,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No C3 cue disposition, C4 adequacy decision, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
