#!/usr/bin/env python3
"""Apply an explicit, cue-only RQ1b V3 C3 revision manifest to a C2 ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--revisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_c3_revision_output")

    records = read_jsonl(args.input)
    by_id = {str(record["c2_packet_id"]): record for record in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate_c2_packet_id")
    revisions = json.loads(args.revisions.read_text(encoding="utf-8"))
    if not isinstance(revisions, list) or not revisions:
        raise SystemExit("empty_or_invalid_revisions")
    revision_by_id = {str(row["c2_packet_id"]): row for row in revisions}
    if len(revision_by_id) != len(revisions) or set(revision_by_id) - set(by_id):
        raise SystemExit("revision_coverage_or_identity_failure")

    changed: list[dict[str, str]] = []
    for packet_id, revision in revision_by_id.items():
        rewritten = revision.get("rewritten_prompt")
        blind_packet_id = revision.get("blind_packet_id")
        rationale = revision.get("review_rationale")
        if not all(isinstance(value, str) and value.strip() for value in (rewritten, blind_packet_id, rationale)):
            raise SystemExit(f"invalid_revision:{packet_id}")
        record = by_id[packet_id]
        prior = str(record["prompt_text"])
        record["prompt_text"] = rewritten
        record["c3_revision_lineage"] = {
            "revision": "c3r1_cue_only",
            "blind_packet_id": blind_packet_id,
            "prior_prompt_sha256": hashlib.sha256(prior.encode("utf-8")).hexdigest(),
            "change_boundary": "C3 cue-only rewrite. Sealed target, source binding, intended constraints, and all non-prompt fields are unchanged.",
        }
        changed.append({
            "c2_packet_id": packet_id,
            "blind_packet_id": blind_packet_id,
            "prior_prompt": prior,
            "rewritten_prompt": rewritten,
            "review_rationale": rationale,
            "boundary": "Cue-only surface wording revision; not a label, adequacy decision, selector input, metric, or result.",
        })

    ordered = sorted(records, key=lambda row: (str(row["c1_review_id"]), str(row["sealed_target_source_id"]), str(row["variant"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in ordered), encoding="utf-8")
    args.audit.write_text(json.dumps({
        "status": "C3R1_CUE_ONLY_REWRITE_PASS_NOT_A_LABEL_OR_RESULT",
        "input_c2_ledger_sha256": digest(args.input),
        "revisions_sha256": digest(args.revisions),
        "output_c2_ledger_sha256": digest(args.output),
        "record_count": len(ordered),
        "changed_prompt_count": len(changed),
        "changed_packet_ids": sorted(revision_by_id),
        "revision_records": changed,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": ["No cue-safety proof, C4 adequacy decision, strict label, selector input, model call, metric, or routing result was created."],
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"record_count": len(ordered), "changed_prompt_count": len(changed), "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
