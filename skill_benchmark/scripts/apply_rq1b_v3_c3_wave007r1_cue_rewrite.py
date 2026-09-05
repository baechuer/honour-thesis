#!/usr/bin/env python3
"""Apply four C3 cue-only revisions without overwriting the W7 C2 ledger.

This uses a source-deidentified C3 rewrite response. It changes surface
wording only, retains the same sealed targets and all other C2 records, and
creates a separately bound r1 ledger for a fresh C3 review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REVISIONS = {
    "RQ1B-V3-C2-W7R1-005-P02-DIRECT": {
        "blind_packet_id": "005-P03",
        "prompt_text": (
            "Help us move this code-defined data asset project to a new scheduling "
            "platform. Before work begins, check that the target supports the needed "
            "data-segmentation capability; if it does not, say that an upgrade is "
            "needed. Preserve the existing dependency structure and schedule behavior, "
            "perform the migration incrementally, validate each converted unit, and "
            "deliver a report recording the status of each item in scope, any deferrals, "
            "and any changes to automated start behavior."
        ),
    },
    "RQ1B-V3-C2-W7R1-005-P02-PARAPHRASE": {
        "blind_packet_id": "005-P04",
        "prompt_text": (
            "Please convert our data-product codebase for a different orchestration "
            "environment. First confirm that it has the needed data-segmentation support, "
            "recommending an upgrade when it does not. Keep the existing dependencies and "
            "automated timing, carry out the work in stages, and verify each converted unit. "
            "The final handover should show the status of each item in scope, explain "
            "anything postponed, and note any change to automated start behavior."
        ),
    },
    "RQ1B-V3-C2-W7R1-005-P03-DIRECT": {
        "blind_packet_id": "005-P05",
        "prompt_text": (
            "Convert our cloud data-workflow configurations into pipeline definitions for "
            "the replacement analytics workspace. Create target connections from the shared "
            "connection settings, integrate each data configuration directly into the work "
            "step that uses it, and move shared parameters into shared deployment settings. "
            "Prepare referenced notebook assets before their pipeline entries and use durable "
            "references for them in the pipeline. Exclude timing rules from this conversion, "
            "and call out activity types that need manual redesign."
        ),
    },
    "RQ1B-V3-C2-W7R1-005-P03-PARAPHRASE": {
        "blind_packet_id": "005-P06",
        "prompt_text": (
            "I need existing integration workflows rewritten as pipeline artifacts for a "
            "new analytics workspace. Map shared service settings to usable connections, "
            "keep each step's input and output configuration with that step, and relocate "
            "common values to shared deployment settings. Link each referenced notebook only "
            "after it is available in the destination, using a durable reference. Omit timing "
            "rules, and mark unsupported task kinds for follow-up."
        ),
    },
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_c3r1_output")

    input_sha = sha256_file(args.input)
    records = read_jsonl(args.input)
    by_id = {str(record.get("c2_packet_id")): record for record in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate_or_blank_c2_packet_id")
    if set(REVISIONS) - set(by_id):
        raise SystemExit("missing_revision_packet")

    raw_revision_rows: list[dict[str, str]] = []
    changed = 0
    for record in records:
        packet_id = str(record["c2_packet_id"])
        revision = REVISIONS.get(packet_id)
        if revision is None:
            continue
        original_prompt = str(record["prompt_text"])
        record["prompt_text"] = revision["prompt_text"]
        record["c3_revision_lineage"] = {
            "revision": "c3r1_cue_only",
            "blind_packet_id": revision["blind_packet_id"],
            "prior_prompt_sha256": hashlib.sha256(original_prompt.encode("utf-8")).hexdigest(),
            "change_boundary": "C3 cue-only rewrite. Sealed target, C1 source binding, C2 intended constraints and all non-prompt fields are unchanged.",
        }
        raw_revision_rows.append({
            "blind_packet_id": revision["blind_packet_id"],
            "c2_packet_id": packet_id,
            "prior_prompt": original_prompt,
            "rewritten_prompt": revision["prompt_text"],
            "boundary": "Source-deidentified C3 cue-only rewrite suggestion; not a label, adequacy decision, selector input, metric or result.",
        })
        changed += 1

    records.sort(key=lambda item: (str(item["c1_review_id"]), str(item["sealed_target_source_id"]), str(item["variant"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    revision_path = args.output.with_name("C3_CUE_ONLY_REWRITE_R1.json")
    revision_path.write_text(json.dumps(raw_revision_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = {
        "status": "C3R1_CUE_ONLY_REWRITE_PASS_NOT_A_LABEL_OR_RESULT",
        "input_c2_ledger_sha256": input_sha,
        "output_c2_ledger_sha256": sha256_file(args.output),
        "record_count": len(records),
        "changed_prompt_count": changed,
        "changed_packet_ids": sorted(REVISIONS),
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No cue-safety proof, adequacy decision, strict label, selector input, model call, metric or routing result was created.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
