#!/usr/bin/env python3
"""Canonically normalise Round 23 C0B agent ledger field names.

Some reviewers may return the semantically equivalent legacy keys ``candidates``
and ``literal_source_substrings``. This tool permits only that mechanical key
normalisation; it never edits statuses, candidate membership, evidence text, or
any assessment/rationale. The resulting ledger is then independently checked
against exact packet-original text by the normal C0B validator.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalise(row: dict[str, Any]) -> dict[str, Any]:
    value = dict(row)
    evidence = value.get("candidate_evidence")
    aliases = [key for key in ("candidates", "candidate_reviews") if value.get(key) is not None]
    if evidence is not None and aliases:
        raise ValueError(f"two_evidence_keys:{value.get('proposal_id')}")
    if len(aliases) > 1:
        raise ValueError(f"multiple_legacy_evidence_keys:{value.get('proposal_id')}")
    if evidence is None:
        legacy_key = aliases[0] if aliases else None
        legacy = value.get(legacy_key) if legacy_key else None
        if not isinstance(legacy, list):
            raise ValueError(f"missing_candidate_evidence:{value.get('proposal_id')}")
        evidence = legacy
        value.pop(legacy_key, None)
    if not isinstance(evidence, list):
        raise ValueError(f"candidate_evidence_not_list:{value.get('proposal_id')}")
    canonical: list[dict[str, Any]] = []
    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError(f"non_object_candidate_evidence:{value.get('proposal_id')}")
        entry = dict(item)
        literals = entry.get("literal_source_substrings")
        explicit = entry.get("evidence_substrings")
        if literals is not None and explicit is not None:
            raise ValueError(f"two_substring_keys:{value.get('proposal_id')}:{entry.get('skill_id')}")
        if explicit is None:
            if not isinstance(literals, list):
                raise ValueError(f"missing_evidence_substrings:{value.get('proposal_id')}:{entry.get('skill_id')}")
            entry["evidence_substrings"] = literals
            entry.pop("literal_source_substrings", None)
        canonical.append(entry)
    value["candidate_evidence"] = canonical
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    rows: list[dict[str, Any]] = []
    source_rows = 0
    normalised_key_count = 0
    for input_path in args.input:
        for row in read_jsonl(input_path):
            source_rows += 1
            before = json.dumps(row, ensure_ascii=True, sort_keys=True)
            transformed = normalise(row)
            after = json.dumps(transformed, ensure_ascii=True, sort_keys=True)
            if before != after:
                normalised_key_count += 1
            transformed["c0b_agent_raw_ledger_path"] = str(input_path)
            rows.append(transformed)
    proposal_ids = [str(row.get("proposal_id", "")) for row in rows]
    if not all(proposal_ids) or len(proposal_ids) != len(set(proposal_ids)):
        raise SystemExit("missing_or_duplicate_proposal_id")
    rows.sort(key=lambda row: str(row["proposal_id"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C0B_ROUND23_AGENT_LEDGER_SCHEMA_NORMALISED_PENDING_LITERAL_VALIDATION_NOT_A_CLUSTER_OR_RESULT",
        "input_count": len(args.input),
        "source_row_count": source_rows,
        "output_row_count": len(rows),
        "rows_with_mechanical_key_normalisation": normalised_key_count,
        "allowed_transforms": [
            "candidates -> candidate_evidence",
            "candidate_reviews -> candidate_evidence",
            "literal_source_substrings -> evidence_substrings",
        ],
        "prohibited_transforms": [
            "status changes",
            "candidate membership changes",
            "evidence text changes",
            "assessment or rationale changes",
        ],
        "exclusions": [
            "This is not a source validation, prompt, label, acceptable-set, retrieval, model, metric, or result step.",
        ],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "output_row_count", "rows_with_mechanical_key_normalisation")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
