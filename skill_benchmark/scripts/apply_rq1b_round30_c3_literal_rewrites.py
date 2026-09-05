#!/usr/bin/env python3
"""Apply the sealed wording-only C3 amendment to three Round 30 C2 drafts.

This preserves the original C2 draft ledger and changes only the three
identified literal-cue phrases. It never changes proposal membership,
candidate identity, source text, construction intent, a label, or a result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REWRITES = {
    (
        "r30-business_operations-c0a-02",
        "r30m1-AgriciDaniel-claude-ads-skills-ads-audit",
        "direct",
    ): (
        "Assess the health of our paid campaigns across search, social, and marketplace channels using the account exports and screenshots I provide. Separate what the data directly shows from your diagnosis, note any gaps in tracking or channel coverage, and identify spend-allocation, advertisement, destination-page, policy, and measurement risks. Rank the recommended actions with an owner, effort estimate, expected effect, and a way to verify success."
    ),
    (
        "r30-documents_creative-c0a-03",
        "r30m1-andrewhowdencom-.agents-skills-documentation",
        "direct",
    ): (
        "Our repository just added CSV export. Draft the Markdown guide and reference changes for developers and users: refresh the main project page, add a guided first-use walkthrough, describe the export command and options, explain the key design choices, and include checks for internal links and the local site build."
    ),
    (
        "r30-documents_creative-c0a-03",
        "r30m1-andrewhowdencom-.agents-skills-documentation",
        "paraphrase",
    ): (
        "We shipped CSV export and the repository guides are now behind. Write the needed Markdown material for developers and users, covering an introductory example, instructions for completing an export, a precise command-and-option lookup, the reasoning behind the feature, and local verification of navigation and rendering."
    ),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    args = parser.parse_args()

    # Indexed assignment preserves every unlisted field exactly.
    rows = read_jsonl(args.input)
    applied = []
    for index, row in enumerate(rows):
        key = (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))
        replacement = REWRITES.get(key)
        if replacement is not None:
            amended = dict(row)
            amended["prompt"] = replacement
            rows[index] = amended
            applied.append({"proposal_id": key[0], "intended_candidate_skill_id": key[1], "variant": key[2], "original_prompt": str(row["prompt"]), "amended_prompt": replacement})

    if len(applied) != len(REWRITES):
        raise SystemExit(f"rewrite_coverage:{len(applied)}:expected:{len(REWRITES)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    amendment = {
        "status": "C3_LITERAL_REWRITE_AMENDMENT_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "output": str(args.output),
        "applied_rewrites": applied,
        "invariants": [
            "Original C2 ledger remains preserved.",
            "Only prompt wording changes.",
            "No proposal, candidate, source, intended construction target, label, adequacy judgment, retrieval input, model call, metric, or result changes.",
        ],
    }
    args.amendment.write_text(json.dumps(amendment, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": amendment["status"], "rewrite_count": len(applied)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
