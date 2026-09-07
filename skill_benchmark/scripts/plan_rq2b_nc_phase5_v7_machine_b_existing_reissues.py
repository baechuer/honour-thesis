#!/usr/bin/env python3
"""Plan V7 Machine-B reissues without opening the opaque target join.

The existing-return ledger records original returns that fail the frozen
identity/binding check.  This script first replays any separately preserved
reissue returns under the frozen validator.  It then assigns only the still
missing lanes to one of three independent reviewer work contexts, while never
assigning both lanes of the same prompt group to one context.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import runpy
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase5-v7-machine-b-audit-ledger-2026-09-07-v1/"
    "validated_existing_return_pairs.jsonl"
)
RETURNS_ROOT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
)
PROTOCOL = ROOT / (
    "skill_benchmark/scripts/"
    "rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
)
V7_MANIFEST = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery/"
    "unified_prompt_group_batch_manifest.jsonl"
)
DEFAULT_OUTPUT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase5-v7-machine-b-existing-return-reissues-2026-09-08-v2"
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl_write(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def validated_existing_alternates(
    protocol: dict[str, Any], batch_id: str, lane: str
) -> list[Path]:
    """Return only alternate raw returns that pass the frozen validator."""
    loader = protocol["load_validated_return"]
    candidates = [
        Path(p)
        for p in glob.glob(
            str(RETURNS_ROOT / f"reviewer_{lane}" / f"{batch_id}.reissue-*.json")
        )
    ]
    candidates.extend(
        Path(p)
        for p in glob.glob(
            str(RETURNS_ROOT / f"reviewer_{lane}_reissue_*" / f"{batch_id}.json")
        )
    )
    valid: list[Path] = []
    for candidate in sorted(candidates):
        try:
            loader(batch_id, lane, candidate)
        except Exception:  # An invalid historical reissue is retained, not selected.
            continue
        valid.append(candidate)
    return valid


def worker_for_lane(
    batch_id: str, lane: str, prior_for_batch: dict[str, str], loads: Counter[str]
) -> str:
    """Deterministic least-loaded assignment, excluding a sibling-lane worker."""
    workers = ["review_context_1", "review_context_2", "review_context_3"]
    sibling = prior_for_batch.get("B" if lane == "A" else "A")
    allowed = [worker for worker in workers if worker != sibling]
    tie_order = sorted(
        allowed,
        key=lambda worker: (
            loads[worker],
            hashlib.sha256(f"{batch_id}|{lane}|{worker}".encode()).hexdigest(),
        ),
    )
    return tie_order[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output: Path = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing package: {output}")

    protocol = runpy.run_path(str(PROTOCOL))
    namespace = protocol["load_validated_return"].__globals__
    execution = namespace["verify_execution"]()
    audit = namespace["verify_audit"]()
    namespace["verify_execution"] = lambda: execution
    namespace["verify_audit"] = lambda: audit

    existing_replay: list[dict[str, Any]] = []
    needs_reissue: list[dict[str, Any]] = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        for lane, record in sorted(row["lanes"].items()):
            if not record["validation"].startswith("INVALID"):
                continue
            valid = validated_existing_alternates(protocol, row["batch_id"], lane)
            common = {
                "batch_id": row["batch_id"],
                "blind_packet_id": row["blind_packet_id"],
                "lane": lane,
                "original_return_path": record["return_path"],
                "original_return_sha256": record["return_file_sha256"],
                "original_validation": record["validation"],
                "failure_reason": record["failure_reason"],
                "frozen_protocol_sha256": sha256_path(PROTOCOL),
            }
            if valid:
                existing_replay.append(
                    {
                        **common,
                        "selected_existing_reissue_path": str(valid[0].relative_to(ROOT)),
                        "selected_existing_reissue_sha256": sha256_path(valid[0]),
                        "status": "PASS_FROZEN_VALIDATOR_EXISTING_REISSUE_REPLAYED",
                    }
                )
            else:
                needs_reissue.append(common)

    loads: Counter[str] = Counter()
    assigned_by_batch: dict[str, dict[str, str]] = {}
    assignments: list[dict[str, Any]] = []
    for row in sorted(needs_reissue, key=lambda item: (item["batch_id"], item["lane"])):
        prior = assigned_by_batch.setdefault(row["batch_id"], {})
        worker = worker_for_lane(row["batch_id"], row["lane"], prior, loads)
        prior[row["lane"]] = worker
        loads[worker] += 1
        required_path = (
            output
            / "returns"
            / f"reviewer_{row['lane']}"
            / f"{row['batch_id']}.json"
        )
        assignments.append(
            {
                **row,
                "owner_review_context": worker,
                "required_reissue_return_path": str(required_path.relative_to(ROOT)),
                "assignment_version": "v1",
                "status": "PENDING_TARGET_BLIND_SINGLE_LANE_REISSUE",
            }
        )

    output.mkdir(parents=True)
    jsonl_write(output / "existing_valid_reissue_replay.jsonl", existing_replay)
    jsonl_write(output / "pending_reissue_assignment.jsonl", assignments)
    summary = {
        "schema_version": "rq2b_nc_phase5_v7_machine_b_existing_return_reissue_plan_v1",
        "claim_boundary": (
            "Target-blind raw-return collection only. No target join, reconciliation, "
            "acceptable set, final disposition, or library claim is materialised."
        ),
        "inputs": {
            "existing_return_audit_ledger": str(LEDGER.relative_to(ROOT)),
            "existing_return_audit_ledger_sha256": sha256_path(LEDGER),
            "frozen_protocol": str(PROTOCOL.relative_to(ROOT)),
            "frozen_protocol_sha256": sha256_path(PROTOCOL),
            "v7_unified_manifest": str(V7_MANIFEST.relative_to(ROOT)),
            "v7_unified_manifest_sha256": sha256_path(V7_MANIFEST),
            "frozen_execution_replay_status": execution["status"],
        },
        "counts": {
            "invalid_original_lanes": len(existing_replay) + len(assignments),
            "validated_existing_reissues": len(existing_replay),
            "pending_single_lane_reissues": len(assignments),
            "assigned_by_review_context": dict(sorted(loads.items())),
        },
        "integrity": {
            "no_assigned_pair_shares_a_review_context": all(
                len(set(lanes.values())) == len(lanes)
                for lanes in assigned_by_batch.values()
            ),
            "original_returns_preserved_by_reference": True,
            "opaque_target_join_opened": False,
        },
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "README.md").write_text(
        "# V7 Machine B existing-return reissue plan\n\n"
        "This package replays historical alternate returns under the frozen strict "
        "validator and issues only missing invalid lanes for a target-blind re-review. "
        "Original raw returns are retained and are never overwritten. Work contexts "
        "must not share the A and B lane of any prompt group. The package is not a "
        "reconciliation, acceptable-set, final-disposition, or library result.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
