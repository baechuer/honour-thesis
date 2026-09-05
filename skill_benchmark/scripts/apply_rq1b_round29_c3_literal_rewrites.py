#!/usr/bin/env python3
"""Apply audited Round 29 C3 literal-cue rewrites without mutating C2 drafts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


LITERAL_PASS = "C3_LITERAL_CUE_PASS_NOT_A_LABEL_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")), str(row.get("variant", "")))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2", type=Path, required=True)
    parser.add_argument("--c3-audit", type=Path, required=True)
    parser.add_argument("--rewrites", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    args = parser.parse_args()

    c2_rows = read_jsonl(args.c2)
    c2_by_key = {key(row): row for row in c2_rows}
    if len(c2_by_key) != len(c2_rows):
        raise SystemExit("duplicate_c2_prompt_key")
    audit = json.loads(args.c3_audit.read_text(encoding="utf-8"))
    audit_targets = {key(row) for row in audit.get("records", []) if row.get("c3_status") != LITERAL_PASS}
    rewrites = read_jsonl(args.rewrites)
    rewrite_by_key = {key(row): row for row in rewrites}
    if len(rewrite_by_key) != len(rewrites):
        raise SystemExit("duplicate_rewrite_key")
    if set(rewrite_by_key) != audit_targets:
        raise SystemExit("rewrite_keys_do_not_match_literal_audit_targets")
    if not audit_targets <= set(c2_by_key):
        raise SystemExit("literal_audit_target_missing_from_c2")

    final_rows: list[dict[str, Any]] = []
    amendments: list[dict[str, Any]] = []
    for item_key, row in c2_by_key.items():
        if item_key not in rewrite_by_key:
            final_rows.append(row)
            continue
        replacement = str(rewrite_by_key[item_key].get("replacement_prompt", "")).strip()
        rationale = str(rewrite_by_key[item_key].get("c3_rewrite_rationale", "")).strip()
        if not replacement or not rationale:
            raise SystemExit(f"blank_replacement_or_rationale:{':'.join(item_key)}")
        amended = dict(row)
        amended["prompt"] = replacement
        final_rows.append(amended)
        amendments.append({
            "proposal_id": item_key[0],
            "intended_candidate_skill_id": item_key[1],
            "variant": item_key[2],
            "old_prompt_sha256": digest(str(row["prompt"])),
            "new_prompt_sha256": digest(replacement),
            "c3_rewrite_rationale": rationale,
            "boundary": "literal_cue_wording_only; candidate_membership_and_construction_target_unchanged",
        })
    final_rows.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in final_rows), encoding="utf-8")
    payload = {
        "status": "C3_ROUND29_LITERAL_REWRITE_AMENDMENT_NOT_A_LABEL_OR_RESULT",
        "input_c2": str(args.c2),
        "input_c3_literal_audit": str(args.c3_audit),
        "raw_rewrite_proposals": str(args.rewrites),
        "target_count": len(audit_targets),
        "amendments": amendments,
        "exclusions": [
            "The original C2 drafts remain preserved.",
            "Only literal cue wording changed; no candidate, source text, proposal membership, or construction target changed.",
            "This amendment is not a label, adequacy judgment, retrieval input, model result, metric, or frozen benchmark result.",
        ],
    }
    args.amendment.parent.mkdir(parents=True, exist_ok=True)
    args.amendment.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "target_count": len(audit_targets), "final_prompt_count": len(final_rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
