#!/usr/bin/env python3
"""Select only Round 41 prompts requiring fresh C3 semantic-cue review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REWORDED = "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--historical-c3", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    historical = read_jsonl(args.historical_c3)
    targets = {key(row) for row in historical if row.get("c3_disposition") == REWORDED}
    prompt_rows = read_jsonl(args.prompts)
    available = {key(row) for row in prompt_rows}
    missing = sorted(targets - available)
    if missing:
        raise SystemExit(f"missing_rewrite_candidates:{missing}")
    selected = [row for row in prompt_rows if key(row) in targets]
    selected.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in selected), encoding="utf-8")
    summary = {
        "status": "C3_ROUND41_SEMANTIC_REVIEW_CANDIDATES_READY_NOT_A_LABEL_OR_RESULT",
        "historical_reworded_count": len(targets),
        "selected_rewrite_candidate_count": len(selected),
        "exclusions": [
            "This selection does not overwrite historical C3 dispositions.",
            "No C4 review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
