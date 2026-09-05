#!/usr/bin/env python3
"""Bind D1 W5 C1-queue source IDs to frozen canonical originals.

This local preparatory script emits only a D1 manifest for source-only C1
review. It does not create prompts, labels, card masks, selector inputs,
embeddings, metrics, or routing results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


BOUNDARY = (
    "This prepares source-bound C1 review inputs only. It is not a C1 pass, "
    "valid cluster, prompt, gold label, acceptable set, selector input, "
    "representation, field effect, or routing result."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing_to_overwrite_existing_output:{args.output}")

    triage = json.loads(args.triage.read_text(encoding="utf-8"))
    sources = {row["source_id"]: row for row in read_jsonl(args.source_manifest)}
    drafts: list[dict[str, Any]] = []
    source_ids: list[str] = []
    for item in triage["drafts"]:
        if item["status"] != "READY_FOR_C1_SOURCE_EVIDENCE_REVIEW":
            continue
        members: list[dict[str, str]] = []
        for member in item["members"]:
            record = sources.get(member["source_id"])
            if not record:
                raise SystemExit(f"missing_source_manifest_record:{member['source_id']}")
            canonical = record["canonical"]
            original = Path(canonical["absolute_path"])
            expected_sha = str(record["sha256"])
            if not original.is_file() or sha256_file(original) != expected_sha:
                raise SystemExit(f"source_binding_failure:{member['source_id']}")
            members.append({
                "source_id": member["source_id"],
                "sha256": expected_sha,
                "origin_key": canonical["origin_key"],
                "relative_path": canonical["relative_path"],
                "absolute_path": str(original),
                "title": member["title"],
            })
            source_ids.append(member["source_id"])
        if len(members) not in {3, 4} or len({member["source_id"] for member in members}) != len(members):
            raise SystemExit(f"invalid_member_set:{item['draft_id']}")
        drafts.append({
            "d1_draft_id": item["draft_id"],
            "discovery_lane": "D1-W5-C1-QUEUE",
            "shared_envelope": item["shared_envelope"],
            "composition_concerns": item["risks"],
            "members": members,
            "claim_boundary": BOUNDARY,
        })
    if len(drafts) != 7:
        raise SystemExit(f"expected_7_c1_queue_drafts_got:{len(drafts)}")
    if len(source_ids) != len(set(source_ids)):
        raise SystemExit("candidate_reuse_within_w5_c1_queue")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in drafts), encoding="utf-8")
    audit = {
        "status": "RQ1B_V3_D1_W5_C1_INPUT_BINDING_PASS_NOT_A_C1_RESULT",
        "triage_sha256": sha256_file(args.triage),
        "source_manifest_sha256": sha256_file(args.source_manifest),
        "output_sha256": sha256_file(args.output),
        "draft_count": len(drafts),
        "source_count": len(source_ids),
        "unique_source_count": len(set(source_ids)),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    audit_path = args.output.with_name("D1_W5_C1_INPUT_BINDING_AUDIT.json")
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
