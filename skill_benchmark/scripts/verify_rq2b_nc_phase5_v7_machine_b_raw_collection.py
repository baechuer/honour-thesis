#!/usr/bin/env python3
"""Replay Machine-B raw-return coverage without opening V7's target join.

This verifier is intentionally limited to packet/return integrity and raw
review coverage.  It does not reconcile disagreements or compute an
acceptable set.
"""

from __future__ import annotations

import glob
import hashlib
import json
import runpy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20/"
    "machine_b_manifest.jsonl"
)
AUDIT_LEDGER = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase5-v7-machine-b-audit-ledger-2026-09-07-v1/"
    "validated_existing_return_pairs.jsonl"
)
REISSUE_PLAN = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase5-v7-machine-b-existing-return-reissues-2026-09-08-v2"
)
RAW_RETURNS = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
)
REVIEW_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/review"
PROTOCOL = ROOT / (
    "skill_benchmark/scripts/"
    "rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
)
DEFAULT_OUTPUT = REVIEW_ROOT / "RQ2B-NC-phase5-v7-machine-b-full-raw-collection-validation-2026-09-08-v3"
FORMAT_REPAIR = REVIEW_ROOT / "RQ2B-NC-phase5-v7-machine-b-existing-return-reissues-format-repair-2026-09-08-v1"
EXPECTED_INCOMPLETE = "RQ2B-P4-V7-U0527"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> None:
    output = DEFAULT_OUTPUT
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing report: {output}")

    protocol = runpy.run_path(str(PROTOCOL))
    loader = protocol["load_validated_return"]
    namespace = loader.__globals__
    execution = namespace["verify_execution"]()
    audit = namespace["verify_audit"]()
    namespace["verify_execution"] = lambda: execution
    namespace["verify_audit"] = lambda: audit

    manifest_rows = read_jsonl(HANDOFF)
    machine_b_ids = [row["batch_id"] for row in manifest_rows]
    if len(machine_b_ids) != 533 or len(set(machine_b_ids)) != len(machine_b_ids):
        raise SystemExit("unexpected Machine-B handoff cardinality or duplicate batch id")

    ledger = {row["batch_id"]: row for row in read_jsonl(AUDIT_LEDGER)}
    existing_replay = {
        (row["batch_id"], row["lane"]): row
        for row in read_jsonl(REISSUE_PLAN / "existing_valid_reissue_replay.jsonl")
    }
    pending_reissue = {
        (row["batch_id"], row["lane"]): row
        for row in read_jsonl(REISSUE_PLAN / "pending_reissue_assignment.jsonl")
    }

    selections: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    packet_errors: list[str] = []
    for batch_id in sorted(machine_b_ids):
        sealed, reviewer_view = protocol["expected_packet"](batch_id)
        if (
            sealed["sealed_main_packet"]["candidate_count"] != 6
            or len(sealed["sealed_tail_packets"]) != 2
            or len(reviewer_view["candidates"]) != 8
        ):
            packet_errors.append(batch_id)
        for lane in ("A", "B"):
            source = "canonical_original"
            if batch_id in ledger:
                record = ledger[batch_id]["lanes"][lane]
                if record["validation"].startswith("PASS"):
                    path = ROOT / record["return_path"]
                elif (batch_id, lane) in existing_replay:
                    path = ROOT / existing_replay[(batch_id, lane)]["selected_existing_reissue_path"]
                    source = "historical_validated_reissue"
                else:
                    path = ROOT / pending_reissue[(batch_id, lane)]["required_reissue_return_path"]
                    source = "current_target_blind_reissue"
            else:
                candidates = sorted(
                    Path(value)
                    for value in glob.glob(
                        str(
                            REVIEW_ROOT
                            / f"RQ2B-NC-phase5-v7-machine-b-microbatch-*-lane-{lane.lower()}-reissue-*"
                            / "returns"
                            / f"reviewer_{lane}"
                            / f"{batch_id}.json"
                        )
                    )
                )
                path = next((candidate for candidate in candidates if candidate.exists()), None)
                if path is not None:
                    source = "continuation_traceable_reissue"
                else:
                    path = RAW_RETURNS / f"reviewer_{lane}" / f"{batch_id}.json"
            try:
                loader(batch_id, lane, path)
                validation = "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION"
            except Exception as exc:
                validation = "INVALID_RETAINED"
                failures.append({"batch_id": batch_id, "lane": lane, "error": str(exc)})
            selections.append(
                {
                    "batch_id": batch_id,
                    "lane": lane,
                    "return_path": str(path.relative_to(ROOT)),
                    "return_sha256": sha256_path(path),
                    "return_source": source,
                    "validation": validation,
                }
            )

    unexpected = [failure for failure in failures if failure["batch_id"] != EXPECTED_INCOMPLETE]
    expected_incomplete_lanes = [failure["lane"] for failure in failures if failure["batch_id"] == EXPECTED_INCOMPLETE]
    if unexpected or sorted(expected_incomplete_lanes) != ["A", "B"] or packet_errors:
        raise SystemExit(
            json.dumps(
                {
                    "unexpected_return_failures": unexpected,
                    "expected_incomplete_lanes": expected_incomplete_lanes,
                    "packet_errors": packet_errors,
                }
            )
        )

    valid_by_batch = {
        batch_id: sum(
            row["validation"].startswith("PASS")
            for row in selections
            if row["batch_id"] == batch_id
        )
        for batch_id in machine_b_ids
    }
    output.mkdir(parents=True)
    write_jsonl(output / "return_selection_replay.jsonl", selections)
    summary = {
        "schema_version": "rq2b_nc_phase5_v7_machine_b_full_raw_collection_validation_v3",
        "scope": "All 533 V7 Machine-B prompt groups; target-blind raw-return integrity and coverage only.",
        "claim_boundary": (
            "No reconciliation coordinator packet, final disposition, opaque target join, "
            "acceptable set, main-tail designation, retrieval claim, or library claim is materialised."
        ),
        "bound_inputs": {
            "machine_b_handoff_manifest": str(HANDOFF.relative_to(ROOT)),
            "machine_b_handoff_manifest_sha256": sha256_path(HANDOFF),
            "existing_return_audit_ledger": str(AUDIT_LEDGER.relative_to(ROOT)),
            "existing_return_audit_ledger_sha256": sha256_path(AUDIT_LEDGER),
            "reissue_plan_summary": str((REISSUE_PLAN / "summary.json").relative_to(ROOT)),
            "reissue_plan_summary_sha256": sha256_path(REISSUE_PLAN / "summary.json"),
            "format_repair_ledger": str((FORMAT_REPAIR / "format_repair_ledger.json").relative_to(ROOT)),
            "format_repair_ledger_sha256": sha256_path(FORMAT_REPAIR / "format_repair_ledger.json"),
            "frozen_protocol": str(PROTOCOL.relative_to(ROOT)),
            "frozen_protocol_sha256": sha256_path(PROTOCOL),
            "frozen_execution_replay_status": execution["status"],
        },
        "counts": {
            "machine_b_prompt_groups": len(machine_b_ids),
            "valid_two_return_groups": sum(value == 2 for value in valid_by_batch.values()),
            "started_incomplete_groups": sum(value != 2 for value in valid_by_batch.values()),
            "validated_lane_returns": sum(valid_by_batch.values()),
            "retained_invalid_lanes": len(failures),
            "historical_validated_reissue_lanes": sum(
                row["return_source"] == "historical_validated_reissue" for row in selections
            ),
            "current_target_blind_reissue_lanes": sum(
                row["return_source"] == "current_target_blind_reissue" for row in selections
            ),
            "continuation_traceable_reissue_lanes": sum(
                row["return_source"] == "continuation_traceable_reissue" for row in selections
            ),
        },
        "integrity": {
            "packet_k6_and_two_tail_replay_pass": not packet_errors,
            "full_machine_b_coverage_replayed": len(selections) == 2 * len(machine_b_ids),
            "only_expected_started_incomplete_group_remains": [EXPECTED_INCOMPLETE],
            "target_blindness_preserved": True,
        },
        "started_incomplete": failures,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "README.md").write_text(
        "# V7 Machine B full raw-collection validation\n\n"
        "Replay with:\n\n"
        "```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_machine_b_raw_collection.py\n```\n\n"
        "The verifier writes a new report only when all 533 Machine-B groups have "
        "two frozen-validator-passing raw returns except the retained, previously "
        "documented `RQ2B-P4-V7-U0527` A/B source-anchor failures. This is not a "
        "reconciliation or an acceptable-set result.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
