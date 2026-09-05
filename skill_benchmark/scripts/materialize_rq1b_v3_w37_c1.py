#!/usr/bin/env python3
"""Materialise Wave 037 C1 packets from literal-valid source-only T0 returns."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


FINAL_BATCHES = {
    "RQ1B-V3-W37-T0-B01": ("W37_T0_B01_R1_RAW_RETURN.json", "W37_T0_B01_R1_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B02": ("W37_T0_B02_R2_RAW_RETURN.json", "W37_T0_B02_R2_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B03": ("W37_T0_B03_R2_RAW_RETURN.json", "W37_T0_B03_R2_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B04": ("W37_T0_B04_RAW_RETURN.json", "W37_T0_B04_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B05": ("W37_T0_B05_RAW_RETURN.json", "W37_T0_B05_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B06": ("W37_T0_B06_RAW_RETURN.json", "W37_T0_B06_LITERAL_AUDIT.json"),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batches", type=Path, required=True)
    parser.add_argument("--return-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise SystemExit("refusing_to_overwrite_existing_output_dir")
    by_batch = {row["batch_id"]: row for row in read_jsonl(args.batches)}
    ready = []
    for batch_id, (return_name, audit_name) in FINAL_BATCHES.items():
        if batch_id not in by_batch:
            raise SystemExit(f"unknown_batch:{batch_id}")
        audit = json.loads((args.audit_dir / audit_name).read_text(encoding="utf-8"))
        if audit.get("failure_count") != 0:
            raise SystemExit(f"invalid_final_return:{batch_id}")
        returned = json.loads((args.return_dir / return_name).read_text(encoding="utf-8"))
        triads = {row["t0_review_id"]: row for row in by_batch[batch_id]["triads"]}
        for decision in returned["screened"]:
            if decision.get("outcome") == "READY_FOR_C1":
                triad = triads.get(decision.get("t0_review_id"))
                if triad is None:
                    raise SystemExit(f"unknown_ready_triad:{batch_id}")
                ready.append(triad)
    if len(ready) != 3:
        raise SystemExit(f"expected_three_ready_triads:{len(ready)}")
    used = set()
    packets = []
    for index, triad in enumerate(ready, start=1):
        member_ids = [member["source_id"] for member in triad["members"]]
        if used.intersection(member_ids):
            raise SystemExit(f"source_reuse_across_packets:{triad['t0_review_id']}")
        used.update(member_ids)
        members = []
        for member in triad["members"]:
            source = Path(member["absolute_path"])
            if not source.is_file() or sha256_file(source) != member["sha256"]:
                raise SystemExit(f"source_binding_failure:{member['source_id']}")
            members.append({
                "source_id": member["source_id"],
                "absolute_path": member["absolute_path"],
                "sha256": member["sha256"],
                "origin_key": member["origin_key"],
                "relative_path": member["relative_path"],
            })
        packets.append({
            "c1_review_id": f"RQ1B-V3-W37-C1-{index:03d}",
            "candidate_count": 3,
            "members": members,
            "review_scope": "SOURCE_ONLY_C1_EVIDENCE_CARD",
            "review_status": "UNREVIEWED_SOURCE_ONLY",
            "claim_boundary": "This packet has no prompt, intended winner, gold label, acceptable set, representation, selector output or metric. A C1 pass only permits later prompt construction.",
        })
    staging = args.output_dir.parent / f".{args.output_dir.name}.staging"
    staging.mkdir(parents=True)
    try:
        roster = staging / "c1_review_roster.jsonl"
        roster.write_text("".join(json.dumps(packet, sort_keys=True) + "\n" for packet in packets), encoding="utf-8")
        manifest = {
            "status": "RQ1B_V3_W37_C1_MATERIALISED_LOCAL_ONLY_NOT_A_CLUSTER",
            "packet_count": len(packets),
            "source_count": len(used),
            "source_reuse": False,
            "network_calls": 0,
            "texts_transmitted": 0,
            "roster_sha256": sha256_file(roster),
            "boundary": "C1 construction has no prompt, label, selector, metric, retrieval or field-effect result.",
        }
        (staging / "c1_review_manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        (staging / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json").write_text(json.dumps({
            "status": "RQ1B_V3_W37_C1_SOURCE_BINDING_AUDIT_PASS_NOT_A_CLUSTER",
            "packet_count": len(packets), "source_count": len(used), "source_reuse": False,
            "hash_drift": False, "boundary": "Source binding only; no validity or result judgement.",
        }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        staging.replace(args.output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
