#!/usr/bin/env python3
"""Create zero-network Wave 039 source-only proposal-discovery batches."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BATCHES = {
    "RQ1B-V3-W39-T0S-B01": {"business_legal_finance_operations", "financial-services risk and compliance", "SOC 2 policy management"},
    "RQ1B-V3-W39-T0S-B02": {"3D geospatial data", "geospatial data processing"},
    "RQ1B-V3-W39-T0S-B03": {"infrastructure_cloud_sre_deployment"},
    "RQ1B-V3-W39-T0S-B04": {"application security review", "security and privacy threat modelling"},
    "RQ1B-V3-W39-T0S-B05": {"document_media_design_education"},
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_batches")
    sources = []
    for row in read_jsonl(args.amendment):
        canonical = row["canonical"]
        path = Path(canonical["local_raw_path"])
        if not path.is_file() or sha256_file(path) != canonical["source_sha256"]:
            raise SystemExit(f"source_binding_failure:{row['amendment_source_id']}")
        sources.append({
            "source_id": row["amendment_source_id"],
            "intake_lane": row["intake_lane"],
            "origin_url": row["origin_url"],
            "repository_ref": canonical["repository_ref"],
            "artifact_path": canonical["artifact_path"],
            "local_raw_path": canonical["local_raw_path"],
            "source_sha256": canonical["source_sha256"],
        })
    rows = []
    assigned = set()
    for batch_id, lanes in BATCHES.items():
        members = sorted((row for row in sources if row["intake_lane"] in lanes), key=lambda row: (row["origin_url"], row["artifact_path"], row["source_id"]))
        if not members:
            raise SystemExit(f"empty_batch:{batch_id}")
        overlap = assigned.intersection(row["source_id"] for row in members)
        if overlap:
            raise SystemExit(f"batch_overlap:{batch_id}")
        assigned.update(row["source_id"] for row in members)
        rows.append({
            "batch_id": batch_id,
            "status": "RQ1B_V3_W39_T0S_SOURCE_ONLY_PROPOSAL_DISCOVERY_ASSIGNED_NOT_A_CLUSTER",
            "source_count": len(members),
            "origin_count": len({row["origin_url"] for row in members}),
            "lanes": sorted(lanes),
            "members": members,
            "claim_boundary": "This is source-only candidate discovery. It has no prompt, gold label, selector, metric, retrieval or field-effect result.",
        })
    if assigned != {row["source_id"] for row in sources}:
        raise SystemExit("unassigned_amendment_source")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W39_T0S_BATCH_BUILD_PASS_NOT_A_CLUSTER",
        "batch_count": len(rows),
        "source_count": len(sources),
        "source_disjoint": True,
        "network_calls": 0,
        "texts_transmitted": 0,
        "boundary": "The batches bind local public originals for source-only draft discovery; no candidate has a prompt, label, selector, metric or result.",
    }
    (args.output.parent / "W39_T0S_BATCH_AUDIT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
