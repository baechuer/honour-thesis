#!/usr/bin/env python3
"""Repair declared Round 36 C3 evidence citations without changing judgments."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


REPLACEMENTS = {
    (
        "R36-C0A-SOFTWARE_ENGINEERING-01",
        "r36m1-rustyrazorblade-skills-plugins-dev-skills-skills-refactor",
        "direct",
        "List every test you expect to die.",
    ): "List every test you expect to die",
    (
        "R36-C0A-SOFTWARE_ENGINEERING-01",
        "r36m1-rustyrazorblade-skills-plugins-dev-skills-skills-refactor",
        "direct",
        "Name the prerequisites.",
    ): "Name the prerequisites",
    (
        "R36-C0A-SOFTWARE_ENGINEERING-01",
        "r36m1-rustyrazorblade-skills-plugins-dev-skills-skills-refactor",
        "paraphrase",
        "To remove an API that callers depend on, use parallel change.",
    ): "to remove an API that callers depend on, use parallel change.",
    (
        "R36-C0A-web_automation-01",
        "r36m1-brightdata-skills-skills-scrape",
        "direct",
        "Expected markers present for the task",
    ): "**Expected markers present**",
    (
        "R36-C0A-web_automation-01",
        "r36m1-inference-gateway-browser-agent-agents-skills-web-scraping",
        "direct",
        "Persist - write the result to disk so the user can download it:",
    ): "**Persist** - write the result to disk so the user can download it:",
    (
        "R36-C0A-web_automation-01",
        "r36m1-inference-gateway-browser-agent-agents-skills-web-scraping",
        "paraphrase",
        "JSON, CSV, list of records",
    ): "JSON, CSV, list of",
    (
        "R36-C0A-web_automation-02",
        "r36m1-joe-qai-qa-skills-agent-browser",
        "paraphrase",
        "Snapshot: `agent-browser snapshot -i` (get element refs like `@e1`, `@e2`)",
    ): "agent-browser snapshot -i",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(row: dict[str, Any], evidence: str) -> tuple[str, str, str, str]:
    return (
        str(row["proposal_id"]),
        str(row["intended_candidate_skill_id"]),
        str(row["variant"]),
        evidence,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()

    original = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    revised = copy.deepcopy(original)
    applied: list[dict[str, str]] = []
    for row in revised:
        evidence = row.get("source_evidence_substrings")
        if not isinstance(evidence, list):
            raise SystemExit("invalid_evidence_shape")
        repaired: list[str] = []
        for excerpt in evidence:
            replacement = REPLACEMENTS.get(key(row, str(excerpt)), excerpt)
            if replacement != excerpt:
                applied.append({
                    "proposal_id": str(row["proposal_id"]),
                    "intended_candidate_skill_id": str(row["intended_candidate_skill_id"]),
                    "variant": str(row["variant"]),
                    "old_evidence": str(excerpt),
                    "replacement_exact_substring": replacement,
                })
            repaired.append(replacement)
        row["source_evidence_substrings"] = repaired
    if len(applied) != len(REPLACEMENTS):
        raise SystemExit(f"repair_coverage_mismatch:{len(applied)}:{len(REPLACEMENTS)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in revised), encoding="utf-8")
    args.repair_log.write_text(json.dumps({
        "status": "C3_ROUND36_EVIDENCE_EXACTNESS_REPAIR_ONLY_PENDING_REVALIDATION_NOT_A_JUDGMENT_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "repairs": applied,
        "invariant": "Only seven source_evidence_substrings changed to exact source substrings. No disposition, risk, rationale, prompt, candidate, label, adequacy, retrieval input, model result, or metric changed.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"repair_count": len(applied), "status": "repair_written"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
