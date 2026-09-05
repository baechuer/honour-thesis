#!/usr/bin/env python3
"""Repair one declared Round 36 C0B citation without altering its decision."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


KEY = ("R36-C0A-web_automation-01", "r36m1-inference-gateway-browser-agent-agents-skills-web-scraping", 0)
OLD = "Use this when the user asks to pull structured data off one or more web pages and hand it back in a usable form (JSON, CSV, list of records)."
NEW = "Use this when the user asks to pull structured data off one or more"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    matched = 0
    for row in rows:
        for evidence in row.get("candidate_evidence", []):
            if (row.get("proposal_id"), evidence.get("skill_id"), 0) != KEY:
                continue
            substrings = evidence.get("evidence_substrings")
            if not isinstance(substrings, list) or substrings != [OLD]:
                raise SystemExit("unexpected_target_evidence")
            substrings[0] = NEW
            matched += 1
    if matched != 1:
        raise SystemExit(f"expected_one_repair:{matched}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    args.repair_log.write_text(json.dumps({"status": "C0B_ROUND36_LITERAL_EVIDENCE_REPAIRED_PENDING_INDEPENDENT_VALIDATION_NOT_A_CLUSTER_OR_RESULT", "input": str(args.input), "input_sha256": sha256(args.input), "output": str(args.output), "output_sha256": sha256(args.output), "repair": {"proposal_id": KEY[0], "skill_id": KEY[1], "evidence_index": KEY[2], "old_evidence": OLD, "replacement_exact_substring": NEW}, "invariant": "Only one evidence string changed; no status, candidate membership, source-review rationale, risk, prompt, label, acceptable set, retrieval input, model call, metric, or result changed."}, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "repair_written", "repair_count": matched}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
