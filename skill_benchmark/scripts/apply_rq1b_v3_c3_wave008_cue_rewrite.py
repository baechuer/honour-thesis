#!/usr/bin/env python3
"""Apply C3 cue-only Wave 008 prompt rewrites without overwriting C2 drafts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    parser.add_argument("--reviews", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_c3r1_output")

    records = read_jsonl(args.input)
    by_packet = {str(row["c2_packet_id"]): row for row in records}
    sealed = {str(row["blind_packet_id"]): str(row["c2_packet_id"]) for row in json.loads(args.sealed_mapping.read_text(encoding="utf-8"))}
    reviews = {str(row["blind_packet_id"]): row for row in read_jsonl(args.reviews)}
    if len(by_packet) != len(records) or set(sealed) != set(reviews):
        raise SystemExit("c3r1_coverage_or_uniqueness_failure")

    changed: list[str] = []
    for blind_id, review in reviews.items():
        if review.get("disposition") != "REWRITE_CUE_ONLY" or not review.get("cue_only_rewrite"):
            raise SystemExit(f"unexpected_nonrewrite_review:{blind_id}")
        packet_id = sealed[blind_id]
        record = by_packet.get(packet_id)
        if record is None:
            raise SystemExit(f"missing_c2_packet:{blind_id}")
        prior = str(record["prompt_text"])
        record["prompt_text"] = str(review["cue_only_rewrite"])
        record["c3_revision_lineage"] = {
            "revision": "c3r1_cue_only",
            "blind_packet_id": blind_id,
            "prior_prompt_sha256": hashlib.sha256(prior.encode("utf-8")).hexdigest(),
            "change_boundary": "C3 cue-only rewrite. Sealed target, source binding, intended constraints, and all non-prompt fields are unchanged.",
        }
        changed.append(packet_id)

    ordered = sorted(records, key=lambda row: (str(row["c1_review_id"]), str(row["sealed_target_source_id"]), str(row["variant"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in ordered), encoding="utf-8")
    audit = {
        "status": "C3R1_CUE_ONLY_REWRITE_PASS_NOT_A_LABEL_OR_RESULT",
        "input_c2_ledger_sha256": digest(args.input),
        "sealed_mapping_sha256": digest(args.sealed_mapping),
        "review_ledger_sha256": digest(args.reviews),
        "output_c2_ledger_sha256": digest(args.output),
        "record_count": len(ordered),
        "changed_prompt_count": len(changed),
        "changed_packet_ids": sorted(changed),
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": ["No C3 safety proof, C4 adequacy decision, label, selector input, model call, metric, or result was created."],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
