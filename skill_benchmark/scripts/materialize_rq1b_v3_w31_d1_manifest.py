#!/usr/bin/env python3
"""Materialise W31 D1 source-bound C1 candidates from audited T0 consensus."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def title_from_path(path: str) -> str:
    parent = Path(path).parent.name
    return parent.replace("-", " ").replace("_", " ").title()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consensus", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wave-label", default="W31")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_w31_d1_manifest")
    consensus = json.loads(args.consensus.read_text(encoding="utf-8"))
    expected_status = f"RQ1B_V3_{args.wave_label}_T0_STRUCTURAL_CONSENSUS_READY_FOR_C1_NOT_A_CLUSTER"
    if consensus.get("status") != expected_status:
        raise SystemExit("unexpected_consensus_status")
    sources = {row["amendment_source_id"]: row for row in read_jsonl(args.amendment)}
    seen_source_ids: set[str] = set()
    rows = []
    for draft in consensus["ready_for_d1"]:
        members = []
        for source_id in draft["source_ids"]:
            source = sources.get(source_id)
            if source is None:
                raise SystemExit(f"missing_source:{source_id}")
            canonical = source["canonical"]
            raw_path = Path(canonical["local_raw_path"])
            if not raw_path.is_file() or sha256_file(raw_path) != canonical["source_sha256"]:
                raise SystemExit(f"source_binding_failure:{source_id}")
            if source_id in seen_source_ids:
                raise SystemExit(f"cross_draft_source_reuse:{source_id}")
            seen_source_ids.add(source_id)
            members.append({
                "source_id": source_id,
                "sha256": canonical["source_sha256"],
                "origin_key": canonical["repository_ref"],
                "relative_path": canonical["artifact_path"],
                "absolute_path": canonical["local_raw_path"],
                "title": title_from_path(canonical["artifact_path"]),
            })
        rows.append({
            "d1_draft_id": draft["d1_draft_id"],
            "discovery_lane": draft["discovery_lane"],
            "shared_envelope": draft["shared_envelope"],
            "composition_concerns": draft["cue_risk_for_later_stages"],
            "source_triage_id": draft["source_triage_id"],
            "members": members,
            "claim_boundary": consensus["claim_boundary"],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "status": f"RQ1B_V3_{args.wave_label}_D1_MANIFEST_BINDING_PASS_NOT_A_C1_RESULT",
        "consensus_sha256": sha256_file(args.consensus),
        "amendment_sha256": sha256_file(args.amendment),
        "output_sha256": sha256_file(args.output),
        "draft_count": len(rows),
        "source_count": len(seen_source_ids),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": consensus["claim_boundary"],
    }
    args.output.with_name(f"D1_{args.wave_label}_INPUT_BINDING_AUDIT.json").write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
