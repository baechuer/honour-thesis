#!/usr/bin/env python3
"""Freeze a targeted, target-blind reissue for distinct-input duplicate rationales."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
PARENT = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_2026_09_08_v1"
ACTIVE = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-2026-09-08-v1" / "coordinator_2"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_c2_targeted_reissue_2026_09_08_v1"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen targeted reissue package: {output}")

    parent_manifest = load_jsonl(PARENT / "coordinator_2_reviewer_manifest.jsonl")
    parent_packets = load_jsonl(PARENT / "coordinator_2_sealed_packets.jsonl")
    by_id = {row["coordinator_dispatch_id"]: row for row in parent_packets}
    manifest_by_id = {row["coordinator_dispatch_id"]: row for row in parent_manifest}
    if len(by_id) != 766 or set(by_id) != set(manifest_by_id):
        raise ValueError("parent coordinator-2 packet identity drift")
    returns: dict[str, dict[str, Any]] = {}
    for path in sorted(ACTIVE.glob("*.json")):
        returns[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    if set(returns) != set(by_id):
        raise ValueError("active coordinator-2 return identity drift")

    by_rationale: dict[str, list[str]] = defaultdict(list)
    for dispatch_id, returned in returns.items():
        by_rationale[returned["rationale"]].append(dispatch_id)
    selected: set[str] = set()
    for rationale, dispatch_ids in by_rationale.items():
        distinct_inputs = {
            (by_id[dispatch_id]["prompt"], by_id[dispatch_id]["fresh_source_visible_skill"])
            for dispatch_id in dispatch_ids
        }
        if len(dispatch_ids) > 1 and len(distinct_inputs) > 1:
            selected.update(dispatch_ids)
    if len(selected) != 18:
        raise ValueError(f"expected 18 distinct-input duplicate-rationale returns, got {len(selected)}")

    packet_rows = [by_id[dispatch_id] for dispatch_id in sorted(selected)]
    reviewer_rows = [manifest_by_id[dispatch_id] for dispatch_id in sorted(selected)]
    admin_rows = [{
        "coordinator_dispatch_id": dispatch_id,
        "parent_packet_sha256": manifest_by_id[dispatch_id]["packet_sha256"],
        "prior_active_return_path": str((ACTIVE / f"{dispatch_id}.json").relative_to(WORKSPACE)),
        "prior_active_return_sha256": sha_path(ACTIVE / f"{dispatch_id}.json"),
        "selection_reason": "DUPLICATE_RATIONALE_ACROSS_DISTINCT_PROMPT_SOURCE_INPUTS",
        "selected_reissue_owner": "coordinator_2_microreissue",
    } for dispatch_id in sorted(selected)]
    output.mkdir(parents=True)
    write_jsonl(output / "coordinator_2_microreissue_reviewer_manifest.jsonl", reviewer_rows)
    write_jsonl(output / "coordinator_2_microreissue_sealed_packets.jsonl", packet_rows)
    write_json(output / "coordinator_return_schema.json", json.loads((PARENT / "coordinator_return_schema.json").read_text(encoding="utf-8")))
    write_jsonl(output / "sealed_admin_reissue_selection_ledger.jsonl", admin_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_prompt_bound_c2_targeted_reissue_dispatch_v1",
        "status": "PASS_TARGETED_RATIONALE_REISSUE_DISPATCH_PENDING_RETURNS",
        "claim_boundary": "Target-blind targeted reissue input only; no target join, acceptable set, library update, retrieval result, metric, or thesis result update.",
        "bound_inputs": {
            "parent_dispatch": str(PARENT.relative_to(WORKSPACE)),
            "parent_integrity_sha256": sha_path(PARENT / "integrity_report.json"),
            "parent_schema_sha256": sha_path(PARENT / "coordinator_return_schema.json"),
        },
        "counts": {"targeted_reissue_returns": len(packet_rows), "parent_coordinator_2_returns": len(by_id)},
        "selection_rule": "Exact duplicate rationale across distinct prompt/source input pairs; all 18 selected packets are reissued together without exposing the selection ledger to the reviewer.",
        "prohibitions_honoured": ["no target join", "no K change", "no reconciliation or library update"],
    }
    write_json(output / "integrity_report.json", report)
    (output / "integrity_report.md").write_text(
        "# Coordinator-2 targeted rationale reissue integrity report\n\n"
        f"- Targeted reissue packets: {len(packet_rows)}\n"
        "- Selection: exact duplicate rationale across distinct prompt/source inputs\n\n"
        "The reviewer receives only the target-blind packet, manifest and schema. The selection ledger is sealed administrative material. Reissue outputs must be validated before replacing the 18 active selections.\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# Targeted prompt-bound coordinator reissue\n\n"
        "Read only `coordinator_2_microreissue_reviewer_manifest.jsonl`, `coordinator_2_microreissue_sealed_packets.jsonl`, and `coordinator_return_schema.json`. Do not inspect the sealed selection ledger, prior active returns, target join, provenance, rank, main/tail role, retrieval, acceptable-set material, or other reviewer work.\n\n"
        "For every manifest row, create one fresh strict-schema return in the assigned reissue directory. Rationale must identify a specific material prompt requirement and source-visible support/limitation; do not reuse an exact rationale string across different packets.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(output), "selected": len(packet_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
