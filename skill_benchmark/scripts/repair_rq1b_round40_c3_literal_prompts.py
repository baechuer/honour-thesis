#!/usr/bin/env python3
"""Rewrite two C3 literal cues without changing C2 coverage or targets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPAIRS = {
    (
        "R40-C0A-mobile_game_creative-02",
        "r40m1-majidmanzarpour-threejs-game-skills-skills-threejs-gameplay-systems",
        "direct",
    ): (
        "keep update order explicit and verify the real input path, rendered canvas, and browser console.",
        "keep the simulation sequencing deterministic and verify keyboard controls, rendered output, and browser-console behavior.",
    ),
    (
        "R40-C0A-mobile_game_creative-03",
        "r40m1-saschb2b-skills-skills-engineering-android-compose",
        "direct",
    ): (
        "immutable UI state is owned by a view model",
        "read-only screen data is owned by a presentation-layer state holder",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    matched = []
    for row in rows:
        key = (str(row.get("proposal_id")), str(row.get("intended_candidate_skill_id")), str(row.get("variant")))
        repair = REPAIRS.get(key)
        if repair is None:
            continue
        old, new = repair
        prompt = str(row.get("prompt", ""))
        if prompt.count(old) != 1:
            raise SystemExit(f"unexpected_prompt_occurrence:{key}")
        row["prompt"] = prompt.replace(old, new)
        matched.append({"proposal_id": key[0], "intended_candidate_skill_id": key[1], "variant": key[2], "old_fragment": old, "new_fragment": new})
    if len(matched) != len(REPAIRS):
        raise SystemExit(f"expected_repairs:{len(REPAIRS)}:actual:{len(matched)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    args.repair_log.write_text(json.dumps({
        "status": "C3_ROUND40_LITERAL_PROMPT_REWRITE_PENDING_REAUDIT_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input), "input_sha256": sha256(args.input),
        "output": str(args.output), "output_sha256": sha256(args.output),
        "repairs": matched,
        "invariant": "Only two cue-wording fragments changed; candidate membership, proposal identity, intended construction target, direct/paraphrase coverage, source text, labels, retrieval inputs, models, metrics, and results did not change.",
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status":"repair_written","repair_count":len(matched)},sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
