#!/usr/bin/env python3
"""Materialise the two prompt-free Wave 035 C1 source-evidence packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


SELECTIONS = [
    ("RQ1B-V3-W35-C1-001", ["RQ1B-V3-W35-SRC-0039", "RQ1B-V3-W35-SRC-0047", "RQ1B-V3-W35-SRC-0049", "RQ1B-V3-W35-SRC-0054"]),
    ("RQ1B-V3-W35-C1-002", ["RQ1B-V3-W35-SRC-0091", "RQ1B-V3-W35-SRC-0100", "RQ1B-V3-W35-SRC-0109", "RQ1B-V3-W35-SRC-0114"]),
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise SystemExit(f"refusing_to_overwrite_existing_output:{args.output_dir}")
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    if ledger.get("status") != "RQ1B_V3_W35_T0_COMPLETE_TWO_C1_CANDIDATES_NOT_A_CLUSTER":
        raise SystemExit("unexpected_t0_ledger_status")
    records = [json.loads(line) for line in args.amendment.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_id = {record["amendment_source_id"]: record for record in records}
    staging = args.output_dir.parent / f".{args.output_dir.name}.staging"
    if staging.exists():
        raise SystemExit(f"stale_staging_dir:{staging}")
    staging.mkdir(parents=True)
    try:
        packets = []
        used_ids = set()
        for review_id, member_ids in SELECTIONS:
            if len(member_ids) != 4 or len(set(member_ids)) != 4:
                raise SystemExit(f"invalid_selection:{review_id}")
            if used_ids & set(member_ids):
                raise SystemExit(f"source_reuse_across_c1_packets:{review_id}")
            used_ids.update(member_ids)
            members = []
            for source_id in member_ids:
                record = by_id.get(source_id)
                if record is None:
                    raise SystemExit(f"unknown_source:{source_id}")
                canonical = record["canonical"]
                original = Path(canonical["local_raw_path"])
                sha = str(canonical["source_sha256"])
                if not original.is_file() or sha256_file(original) != sha:
                    raise SystemExit(f"source_binding_failure:{source_id}")
                members.append({
                    "source_id": source_id,
                    "absolute_path": str(original.resolve()),
                    "sha256": sha,
                    "repository_ref": canonical["repository_ref"],
                    "artifact_path": canonical["artifact_path"],
                })
            packets.append({
                "c1_review_id": review_id,
                "candidate_count": 4,
                "members": members,
                "review_scope": "SOURCE_ONLY_C1_EVIDENCE_CARD",
                "review_status": "UNREVIEWED_SOURCE_ONLY",
                "claim_boundary": "This packet has no prompt, intended winner, gold label, acceptable set, representation, selector output or metric. A C1 pass only permits later prompt construction.",
            })
        roster = staging / "c1_review_roster.jsonl"
        roster.write_text("".join(json.dumps(packet, sort_keys=True) + "\n" for packet in packets), encoding="utf-8")
        manifest = {
            "status": "RQ1B_V3_W35_C1_SOURCE_EVIDENCE_WAVE_MATERIALISED_LOCAL_ONLY",
            "packet_count": len(packets),
            "source_count": sum(packet["candidate_count"] for packet in packets),
            "unique_source_count": len(used_ids),
            "network_calls": 0,
            "texts_transmitted": 0,
            "artifacts": {"c1_review_roster.jsonl": sha256_file(roster)},
            "claim_boundary": "Source-only C1 packet construction. No prompt, label, selector, metric or result is created.",
        }
        (staging / "c1_review_manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        audit = {
            "status": "RQ1B_V3_W35_C1_SOURCE_BINDING_AUDIT_PASS_NOT_A_CLUSTER",
            "packet_count": len(packets),
            "source_count": sum(packet["candidate_count"] for packet in packets),
            "unique_source_count": len(used_ids),
            "source_reuse": False,
            "hash_drift": False,
            "boundary": "This checks only roster membership, local original paths and hashes. It does not validate peer parallelism, operational contrast, prompt fitness, label validity, retrieval or a result.",
        }
        (staging / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json").write_text(json.dumps(audit, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        staging.replace(args.output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
