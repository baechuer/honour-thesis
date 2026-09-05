#!/usr/bin/env python3
"""Apply the two C3-approved literal cue rewrites to Round 31 C2 drafts."""

from __future__ import annotations

import json
from pathlib import Path


INPUT = Path(
    "skill_benchmark/rq1b_cross_source_public_benchmark/working/"
    "c2_round31_validated_prompt_drafts_2026-08-28.jsonl"
)
OUTPUT = Path(
    "skill_benchmark/rq1b_cross_source_public_benchmark/working/"
    "c2_round31_final_prompt_drafts_after_c3_literal_rewrite_2026-08-28.jsonl"
)

REWRITES = {
    (
        "r31-documents_creative-c0a-01",
        "r31m1-xiaoshuai1024-skills-skills-blog-writing",
        "paraphrase",
    ): (
        "Do not invent metrics beyond my source material.",
        "Keep any performance claims limited to the material I provide.",
    ),
    (
        "r31-software_systems-c0a-01",
        "r31m1-khasky-awesome-agent-skills-skills-awesome-code-review",
        "paraphrase",
    ): (
        "Scale the depth to the size and risk of the change,",
        "Match the assessment effort to the scope and potential impact of the patch,",
    ),
}


def main() -> int:
    rows = [json.loads(line) for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed: set[tuple[str, str, str]] = set()
    for row in rows:
        key = (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))
        rewrite = REWRITES.get(key)
        if rewrite is None:
            continue
        old, new = rewrite
        prompt = str(row["prompt"])
        if prompt.count(old) != 1:
            raise SystemExit(f"unexpected_literal_count:{':'.join(key)}")
        row["prompt"] = prompt.replace(old, new)
        changed.add(key)
    if changed != set(REWRITES):
        raise SystemExit(f"rewrite_coverage:{sorted(set(REWRITES) - changed)}")
    OUTPUT.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(json.dumps({"changed_prompt_count": len(changed), "output": str(OUTPUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
