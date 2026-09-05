#!/usr/bin/env python3
"""Merge and mechanically validate Round 17 C2 prompt drafts.

This C2-only operation checks prompt identity and direct/paraphrase coverage.
It does not decide adequacy, create a frozen prompt, or produce a model result.
"""

from __future__ import annotations

import json
import argparse
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKING = ROOT / "rq1b_cross_source_public_benchmark" / "working"
MANIFEST = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
C1 = MANIFEST / "c1_round17_integrity_2026-08-27.jsonl"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except json.JSONDecodeError as error:
        raise SystemExit(f"json_parse_error:{path}:{error}") from error


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", choices=("initial", "c3v2"), default="initial")
    args = parser.parse_args()
    prefix = "c2_round17_" if args.revision == "c3v2" else "c2_round17_draft_"
    suffix = "_c3v2" if args.revision == "c3v2" else ""
    inputs = [WORKING / f"{prefix}{proposal}{suffix}.jsonl" for proposal in ("201_204", "206_207", "210_212", "215_217", "219_222")]
    output_suffix = "_v2" if args.revision == "c3v2" else ""
    output = MANIFEST / f"c2_prompt_drafts_round17{output_suffix}_2026-08-27.jsonl"
    summary_path = MANIFEST / f"c2_prompt_drafts_round17{output_suffix}_summary_2026-08-27.json"
    rows = [row for path in inputs for row in read_jsonl(path)]
    c1_rows = read_jsonl(C1)
    expected = {
        (str(c1["proposal_id"]), str(skill_id))
        for c1 in c1_rows
        if c1.get("c1_status") == "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT"
        for skill_id in c1["candidate_skill_ids"]
    }
    counts: Counter[tuple[str, str, str]] = Counter()
    failures: list[str] = []
    for row in rows:
        proposal_id = str(row.get("proposal_id", ""))
        skill_id = str(row.get("intended_candidate_skill_id", ""))
        variant = str(row.get("variant", ""))
        prompt = row.get("prompt")
        if (proposal_id, skill_id) not in expected:
            failures.append(f"unexpected_candidate:{proposal_id}:{skill_id}")
        if variant not in {"direct", "paraphrase"}:
            failures.append(f"invalid_variant:{proposal_id}:{skill_id}:{variant}")
        if not isinstance(prompt, str) or not prompt.strip():
            failures.append(f"blank_prompt:{proposal_id}:{skill_id}:{variant}")
        counts[(proposal_id, skill_id, variant)] += 1
    for proposal_id, skill_id in sorted(expected):
        for variant in ("direct", "paraphrase"):
            if counts[(proposal_id, skill_id, variant)] != 1:
                failures.append(f"variant_count:{proposal_id}:{skill_id}:{variant}:{counts[(proposal_id, skill_id, variant)]}")
    if len(rows) != 2 * len(expected):
        failures.append(f"row_count:{len(rows)}:expected:{2 * len(expected)}")
    rows.sort(key=lambda row: (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"])))
    output.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C2_MERGE_VALID_NOT_A_LABEL_OR_RESULT" if not failures else "C2_MERGE_INVALID_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(rows),
        "candidate_count": len(expected),
        "direct_count": sum(str(row.get("variant")) == "direct" for row in rows),
        "paraphrase_count": sum(str(row.get("variant")) == "paraphrase" for row in rows),
        "failures": failures,
        "exclusions": ["No C3 cue disposition, C4 adequacy decision, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was produced."],
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
