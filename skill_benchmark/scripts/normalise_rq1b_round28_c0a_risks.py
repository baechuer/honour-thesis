#!/usr/bin/env python3
"""Apply the only permitted Round 28 C0A v1-to-v2 schema correction.

Early C0A workers emitted one non-empty ``c0b_risks`` string where the frozen
structural validator requires a list of non-empty strings.  This utility keeps
the raw ledger intact and writes a v2 copy that wraps that exact string in a
one-element list.  It rejects every other shape and never changes membership,
status, envelope, proposal identifier, or risk text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise SystemExit(f"non_object:{path}:{number}")
            rows.append(value)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    args.output_directory.mkdir(parents=True, exist_ok=True)
    output_rows = 0
    transforms = 0
    outputs: list[dict[str, object]] = []
    seen_proposals: set[str] = set()
    for source in args.input:
        rows = read_jsonl(source)
        changed: list[dict[str, Any]] = []
        for row in rows:
            proposal_id = str(row.get("proposal_id", ""))
            if not proposal_id or proposal_id in seen_proposals:
                raise SystemExit(f"missing_or_duplicate_proposal_id:{source}:{proposal_id}")
            seen_proposals.add(proposal_id)
            risk = row.get("c0b_risks")
            if not isinstance(risk, str) or not risk.strip():
                raise SystemExit(f"not_nonempty_string_risk:{source}:{proposal_id}")
            revised = dict(row)
            revised["c0b_risks"] = [risk]
            if revised["c0b_risks"][0] != risk:
                raise SystemExit(f"risk_text_changed:{source}:{proposal_id}")
            changed.append(revised)
            transforms += 1
        target = args.output_directory / f"{source.stem}_v2.jsonl"
        target.write_text(
            "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in changed),
            encoding="utf-8",
        )
        outputs.append({
            "input": str(source),
            "input_sha256": sha256(source),
            "output": str(target),
            "output_sha256": sha256(target),
            "row_count": len(changed),
            "permitted_transform": "c0b_risks non-empty string -> one-element list containing exact original string",
        })
        output_rows += len(changed)
    summary = {
        "status": "C0A_ROUND28_V1_TO_V2_MECHANICAL_RISK_SCHEMA_NORMALISATION_NOT_A_CLUSTER_OR_RESULT",
        "input_file_count": len(args.input),
        "output_row_count": output_rows,
        "transformed_row_count": transforms,
        "outputs": outputs,
        "allowed_transform": "c0b_risks non-empty string -> one-element list with exact preserved text",
        "prohibited_transforms": [
            "proposal identifier changes",
            "status changes",
            "candidate membership or origin changes",
            "tentative shared-envelope changes",
            "risk-text changes",
        ],
        "exclusions": [
            "This is a mechanical schema repair, not C0A semantic review, C0B source review, a candidate composition, prompt, label, model call, metric, or result.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "transformed_row_count": transforms}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
