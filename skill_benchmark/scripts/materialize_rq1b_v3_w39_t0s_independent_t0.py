#!/usr/bin/env python3
"""Materialise source-only T0 packets from Wave 039 T0S drafts without cues."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal-ledger", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_t0_packets")
    ledger = json.loads(args.proposal_ledger.read_text(encoding="utf-8"))
    sources = {row["amendment_source_id"]: row for row in read_jsonl(args.amendment)}
    batches = []
    used_sources = set()
    for index, proposal in enumerate(ledger.get("literal_valid_proposals", []), start=1):
        members = []
        for source_id in proposal["candidate_source_ids"]:
            source = sources.get(source_id)
            if source is None:
                raise SystemExit(f"unknown_source:{source_id}")
            canonical = source["canonical"]
            path = Path(canonical["local_raw_path"])
            if not path.is_file() or sha256_file(path) != canonical["source_sha256"]:
                raise SystemExit(f"source_binding_failure:{source_id}")
            members.append({
                "source_id": source_id,
                "source_sha256": canonical["source_sha256"],
                "origin_url": source["origin_url"],
                "repository_ref": canonical["repository_ref"],
                "artifact_path": canonical["artifact_path"],
                "local_raw_path": canonical["local_raw_path"],
            })
        if len({member["origin_url"] for member in members}) != len(members):
            raise SystemExit(f"non_distinct_origin:{proposal['proposal_id']}")
        if used_sources.intersection(member["source_id"] for member in members):
            raise SystemExit(f"cross_packet_source_reuse:{proposal['proposal_id']}")
        used_sources.update(member["source_id"] for member in members)
        triad = {
            "t0_review_id": f"RQ1B-V3-W39-T0I-{index:03d}",
            "candidate_count": len(members),
            "members": members,
            "allowed_outcomes": ["READY_FOR_C1", "LIKELY_NONPARALLEL", "NO_PLAUSIBLE_TRIAD", "NEEDS_PARENT_REVIEW"],
            "claim_boundary": "Independent source-only T0 review. The reviewer receives candidate membership and original sources only; no T0S envelope, rationale, risks, prompt, label, target, representation, selector, metric or result.",
        }
        batches.append({
            "batch_id": f"RQ1B-V3-W39-T0I-B{index:02d}",
            "status": "RQ1B_V3_W39_T0I_INDEPENDENT_SOURCE_ONLY_REVIEW_ASSIGNED_NOT_A_CLUSTER",
            "triad_count": 1,
            "source_count": len(members),
            "triads": [triad],
            "boundary": triad["claim_boundary"],
        })
    if not batches:
        raise SystemExit("no_literal_valid_proposals")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(batch, sort_keys=True) + "\n" for batch in batches), encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W39_T0S_TO_INDEPENDENT_T0_MATERIALISATION_PASS_NOT_A_CLUSTER",
        "packet_count": len(batches),
        "source_count": len(used_sources),
        "source_reuse": False,
        "network_calls": 0,
        "texts_transmitted": 0,
        "boundary": "Packets preserve only independently reviewable source membership and bindings. They exclude all proposal rationale and any prompt/label/target/selector/result information.",
    }
    (args.output.parent / "T0I_PACKET_AUDIT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
