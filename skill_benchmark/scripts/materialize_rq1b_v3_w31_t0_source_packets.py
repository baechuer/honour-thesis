#!/usr/bin/env python3
"""Materialise bounded, source-only W31 T0 triage packets for reviewers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--triads-per-packet", type=int, default=3)
    parser.add_argument(
        "--expected-status",
        default="RQ1B_V3_W31_T0_SOURCE_ONLY_CANDIDATE_READING_BATCH_NOT_A_CLUSTER",
    )
    parser.add_argument("--wave-label", default="W31")
    args = parser.parse_args()
    if args.triads_per_packet < 1 or args.output_dir.exists():
        raise SystemExit("invalid_packet_size_or_output_already_exists")

    manifest = json.loads(args.candidate_manifest.read_text(encoding="utf-8"))
    if manifest.get("status") != args.expected_status:
        raise SystemExit("unexpected_candidate_manifest_status")
    sources = {row["amendment_source_id"]: row for row in read_jsonl(args.amendment)}
    triads = manifest.get("candidate_triads")
    if not isinstance(triads, list) or not triads:
        raise SystemExit("missing_candidate_triads")

    seen_members: set[str] = set()
    materialised: list[dict] = []
    for triad in triads:
        source_ids = triad.get("members")
        if not isinstance(source_ids, list) or len(source_ids) not in {3, 4}:
            raise SystemExit(f"invalid_member_count:{triad.get('triad_id')}")
        if len(set(source_ids)) != len(source_ids):
            raise SystemExit(f"duplicate_member_within_triad:{triad.get('triad_id')}")
        overlap = seen_members.intersection(source_ids)
        if overlap:
            raise SystemExit(f"cross_triad_member_reuse:{sorted(overlap)}")
        seen_members.update(source_ids)
        members = []
        for source_id in source_ids:
            source = sources.get(source_id)
            if source is None:
                raise SystemExit(f"unknown_source_id:{source_id}")
            canonical = source["canonical"]
            members.append({
                "source_id": source_id,
                "artifact_path": canonical["artifact_path"],
                "local_raw_path": canonical["local_raw_path"],
                "source_sha256": canonical["source_sha256"],
                "repository_ref": canonical["repository_ref"],
            })
        materialised.append({
            "triad_id": triad["triad_id"],
            "reading_rationale": triad["reading_rationale"],
            "members": members,
        })

    args.output_dir.mkdir(parents=True)
    packet_paths = []
    for start in range(0, len(materialised), args.triads_per_packet):
        number = start // args.triads_per_packet + 1
        packet = {
            "status": f"RQ1B_V3_{args.wave_label}_T0_SOURCE_ONLY_REVIEW_PACKET_NOT_A_CLUSTER",
            "packet_id": f"RQ1B-V3-{args.wave_label}-T0-PACKET-{number:02d}",
            "claim_boundary": manifest["review_boundary"],
            "excluded_actions": ["no prompts", "no intended winners", "no gold labels", "no selector outputs", "no metrics", "no network", "no source-code execution"],
            "review_questions": manifest["review_questions"],
            "allowed_structural_decisions": manifest["allowed_structural_decisions"],
            "candidate_triads": materialised[start : start + args.triads_per_packet],
        }
        packet_path = args.output_dir / f"packet_{number:02d}.json"
        packet_path.write_text(json.dumps(packet, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        packet_paths.append(str(packet_path))
    report = {
        "status": f"RQ1B_V3_{args.wave_label}_T0_SOURCE_ONLY_PACKET_MATERIALISATION_PASS_NOT_A_CLUSTER",
        "candidate_manifest": str(args.candidate_manifest),
        "amendment": str(args.amendment),
        "triad_count": len(materialised),
        "source_count": len(seen_members),
        "packet_count": len(packet_paths),
        "packet_paths": packet_paths,
        "boundary": "Packets bind only frozen source provenance to bounded source-only readings. They contain no prompt, target, label, selector, metric, or result.",
    }
    (args.output_dir / "materialisation_report.json").write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
