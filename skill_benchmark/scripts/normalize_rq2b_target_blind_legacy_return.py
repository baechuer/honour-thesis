#!/usr/bin/env python3
"""Fail-closed schema-only normalizer for legacy target-blind return fields."""
from __future__ import annotations

import json
from pathlib import Path
import argparse


def rows(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite normalized return")
    expected = {str(row.get("prompt_token")) for row in rows(args.packet)}
    raw = rows(args.input)
    if len(raw) != len(expected) or {str(row.get("prompt_token")) for row in raw} != expected:
        raise SystemExit("Input does not exactly reconstruct packet prompts")
    out = []
    for row in raw:
        # Two earlier packet variants used `candidate_reviews` or retained the
        # old per-candidate `candidate_decision` key.  This is a field-shape
        # migration only: the reviewer decision/evidence remain byte-for-byte
        # represented in the new controlled schema.
        reviews = row.get("candidate_reviews", row.get("candidate_assessments", row.get("assessments", row.get("candidate_decisions", row.get("candidates")))))
        if row.get("prompt_integrity") not in {"CUE_SAFE", "CUE_RISK", "SOURCE_UNSUPPORTED_OR_MALFORMED"} or not isinstance(reviews, list) or len(reviews) != 3:
            raise SystemExit("Legacy row is not safely normalizable")
        assessments = []
        for item in reviews:
            token = item.get("candidate_token")
            decision = item.get("candidate_decision", item.get("decision"))
            evidence = item.get("evidence")
            if decision == "UNCLEAR":
                decision = "UNCLEAR_FROM_SOURCE"
            if isinstance(evidence, str):
                evidence = [evidence]
            if token not in {"C-1", "C-2", "C-3"} or decision not in {"MOST_SUITABLE", "FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR_FROM_SOURCE"} or not isinstance(evidence, list) or not evidence or not all(isinstance(value, str) and value for value in evidence):
                raise SystemExit("Legacy candidate assessment is invalid")
            assessments.append({"candidate_token": token, "decision": decision, "evidence": evidence})
        if {item["candidate_token"] for item in assessments} != {"C-1", "C-2", "C-3"}:
            raise SystemExit("Legacy candidate tokens do not reconstruct C-1/C-2/C-3")
        # One early reviewer variant serialised its single prompt-level
        # integrity evidence item as a one-element list and called the summary
        # simply `summary`.  Accept only that lossless shape: multi-item lists
        # are deliberately rejected rather than silently collapsed.
        integrity_evidence = row.get("prompt_integrity_evidence", row.get("integrity_evidence"))
        if isinstance(integrity_evidence, list):
            if len(integrity_evidence) != 1 or not isinstance(integrity_evidence[0], str) or not integrity_evidence[0]:
                raise SystemExit("Legacy prompt-level integrity evidence is not losslessly normalizable")
            integrity_evidence = integrity_evidence[0]
        summary = row.get("prompt_adequacy_summary", row.get("summary", row.get("prompt_summary", row.get("reviewer_summary"))))
        if not isinstance(integrity_evidence, str) or not integrity_evidence or not isinstance(summary, str) or not summary:
            raise SystemExit("Legacy prompt-level evidence is not safely normalizable")
        out.append({"prompt_token": row["prompt_token"], "prompt_integrity": row["prompt_integrity"], "prompt_integrity_evidence": integrity_evidence, "candidate_assessments": assessments, "prompt_adequacy_summary": summary})
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in out), encoding="utf-8")
    print(json.dumps({"status": "PASS_SCHEMA_ONLY_TARGET_BLIND_NORMALIZATION", "prompts": len(out)}))


if __name__ == "__main__":
    main()
