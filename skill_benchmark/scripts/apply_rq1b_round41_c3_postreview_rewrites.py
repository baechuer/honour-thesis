#!/usr/bin/env python3
"""Apply the three declared Round 41 post-review C3 prompt rewrites only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


Key = tuple[str, str, str]


REWRITES: dict[Key, tuple[str, str]] = {
    (
        "R41-C0A-document_research-01",
        "r18m1-ShaishavMaisuria-research-paper-lifecycle-skills-skills-make-slides",
        "direct",
    ): (
        "Turn my research paper into a brief talk that fits a five-minute academic session.",
        "Could you help me make a short presentation from this research manuscript?",
    ),
    (
        "R41-C0A-document_research-01",
        "r35m1-LARi-UQAC-ResearchTools-claude-skills-paper2talk",
        "direct",
    ): (
        "Create a presentation from my accepted paper for an upcoming conference.",
        "Please turn this paper into a presentation for researchers.",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-omnitric-agent-skills-nature-paper2ppt",
        "direct",
    ): (
        "Make a Chinese-language slide presentation from my research paper for a group meeting.",
        "Please make a Chinese-language presentation from this scientific article.",
    ),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    seen: set[Key] = set()
    for row in rows:
        key = (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))
        replacement = REWRITES.get(key)
        if replacement is None:
            continue
        old_prompt, new_prompt = replacement
        if row.get("prompt") != old_prompt:
            raise SystemExit(f"unexpected_original_prompt:{key}")
        row["prompt"] = new_prompt
        seen.add(key)
    if seen != set(REWRITES):
        raise SystemExit(f"rewrite_coverage_mismatch:missing={sorted(set(REWRITES) - seen)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    audit = {
        "status": "C3_ROUND41_POSTREVIEW_SEMANTIC_CUE_REWRITES_APPLIED_REQUIRES_FRESH_C3_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "rewrite_count": len(seen),
        "rewrites": [
            {
                "proposal_id": proposal_id,
                "intended_candidate_skill_id": skill_id,
                "variant": variant,
                "old_prompt": old_prompt,
                "new_prompt": new_prompt,
            }
            for (proposal_id, skill_id, variant), (old_prompt, new_prompt) in sorted(REWRITES.items())
        ],
        "invariants": [
            "Only the three declared prompt strings changed.",
            "All earlier C3 records remain historical and are not overwritten.",
            "No candidate membership, source content, C0B judgment, C1 integrity decision, C4 adequacy review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result changed.",
        ],
    }
    args.audit.write_text(json.dumps(audit, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"rewrite_count": len(seen), "status": audit["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
