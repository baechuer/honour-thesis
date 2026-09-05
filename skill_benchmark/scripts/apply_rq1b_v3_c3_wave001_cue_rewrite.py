#!/usr/bin/env python3
"""Create the lineage-preserved RQ1b V3 Wave 001 C2 r1 cue-only revision."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


TARGET_PACKET = "RQ1B-V3-D1-C1-W4R1-002-000006-direct"
OLD_PROMPT = (
    "In a Python analysis notebook, I already have a table with meaningful "
    "column names. Make a quick non-interactive exploratory figure that shows "
    "the relationship between two numeric columns and distinguishes a category, "
    "using clear sensible defaults; save it as a high-resolution image."
)
NEW_PROMPT = (
    "In a Python analysis notebook, I already have a table whose fields are "
    "clearly labelled. Make a quick non-interactive exploratory figure that shows "
    "the relationship between two numeric columns and distinguishes a category, "
    "using clear sensible defaults; save it as a high-resolution image."
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_r1")
    rows = read_jsonl(args.input)
    changed = 0
    rewritten: list[dict[str, Any]] = []
    for row in rows:
        clone = dict(row)
        if clone.get("c2_packet_id") == TARGET_PACKET:
            if clone.get("prompt_text") != OLD_PROMPT:
                raise SystemExit("unexpected_initial_prompt")
            clone["prompt_text"] = NEW_PROMPT
            clone["c3_cue_revision"] = {
                "revision": "r1",
                "reason": "Replaces the source-shaped phrase 'meaningful column names' with plain-language 'fields are clearly labelled' without changing input, runtime, requested operation, output, or sealed target.",
                "prior_prompt_text": OLD_PROMPT,
            }
            changed += 1
        rewritten.append(clone)
    if changed != 1:
        raise SystemExit(f"rewrite_count:{changed}")
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rewritten),
        encoding="utf-8",
    )
    audit = {
        "status": "C3_CUE_ONLY_REWRITE_APPLIED_NOT_A_LABEL_OR_RESULT",
        "input_sha256": sha256_file(args.input),
        "output_sha256": sha256_file(args.output),
        "row_count": len(rows),
        "changed_packet_id": TARGET_PACKET,
        "changed_fields": ["prompt_text", "c3_cue_revision"],
        "sealed_target_changed": False,
        "operational_intent_changed": False,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No C4 adequacy decision, gold label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
