#!/usr/bin/env python3
"""Recompute Phase-5 execution state without inspecting adequacy outcomes.

The frozen V7 manifest retains its original pending status by design.  This
controller-only reconciliation derives a separate current state from canonical
review artefacts, so progress reporting never relies on stale manifest labels
or prose counts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V7_MANIFEST = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery/"
    "unified_prompt_group_batch_manifest.jsonl"
)
RETURN_ROOT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
)
RECON_ROOT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase4-v7-strict-unified-reconciliation-2026-09-05"
)
DEFAULT_OUTPUT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_v1"
)
FINAL_STATUS = "PASS_V7_VALIDATED_BATCH_DISPOSITIONS_PENDING_LIBRARY_LEVEL_CLOSURE"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number} is not an object")
            rows.append(row)
    return rows


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def expected_groups() -> dict[str, dict[str, object]]:
    rows = read_jsonl(V7_MANIFEST)
    groups: dict[str, dict[str, object]] = {}
    for row in rows:
        batch_id = row.get("batch_id")
        blind_packet_id = row.get("blind_packet_id")
        if not isinstance(batch_id, str) or not isinstance(blind_packet_id, str):
            raise ValueError("V7 manifest row lacks string batch_id/blind_packet_id")
        if batch_id in groups:
            raise ValueError(f"duplicate V7 batch_id: {batch_id}")
        groups[batch_id] = row
    return groups


def reviewer_return_exists(reviewer: str, batch_id: str) -> bool:
    return (RETURN_ROOT / reviewer / f"{batch_id}.json").is_file()


def state_for_group(
    batch_id: str, manifest_row: dict[str, object]
) -> dict[str, object]:
    final_path = RECON_ROOT / batch_id / "final_disposition.json"
    reconciliation_path = RECON_ROOT / batch_id / "reconciliation_ledger.json"
    a_return = reviewer_return_exists("reviewer_A", batch_id)
    b_return = reviewer_return_exists("reviewer_B", batch_id)
    record: dict[str, object] = {
        "batch_id": batch_id,
        "blind_packet_id": manifest_row["blind_packet_id"],
        "reviewer_a_return_present": a_return,
        "reviewer_b_return_present": b_return,
        "reconciliation_ledger_present": reconciliation_path.is_file(),
        "final_disposition_present": final_path.is_file(),
    }
    if final_path.is_file():
        final = read_json(final_path)
        if not isinstance(final, dict):
            record.update(state="DEFECT", reason="final_disposition_not_object")
        elif (
            final.get("batch_id") != batch_id
            or final.get("blind_packet_id") != manifest_row["blind_packet_id"]
            or final.get("status") != FINAL_STATUS
        ):
            record.update(state="DEFECT", reason="final_disposition_binding_or_status_drift")
        else:
            record.update(state="FINALISED", reason="validated_final_disposition")
    elif a_return or b_return or reconciliation_path.is_file():
        record.update(state="STARTED_INCOMPLETE", reason="review_or_reconciliation_without_final")
    else:
        record.update(state="UNSTARTED", reason="no_canonical_execution_artifact")
    return record


def reconcile() -> dict[str, object]:
    groups = expected_groups()
    records = [state_for_group(batch_id, groups[batch_id]) for batch_id in sorted(groups)]
    final_dirs = {
        path.parent.name
        for path in RECON_ROOT.glob("*/final_disposition.json")
    }
    unexpected_final_dispositions = sorted(final_dirs.difference(groups))
    state_counts = Counter(str(record["state"]) for record in records)
    unresolved = [
        record["batch_id"]
        for record in records
        if record["state"] != "FINALISED"
    ]
    payload: dict[str, object] = {
        "schema_version": "rq2b_nc_phase5_execution_state_reconciliation_v1",
        "claim_boundary": (
            "Controller-only execution-state reconciliation. It does not read, "
            "aggregate, expose, or interpret candidate adequacy outcomes, "
            "acceptable sets, tail positivity, retrieval, reranking, or metrics."
        ),
        "bound_inputs": {
            str(V7_MANIFEST.relative_to(ROOT)): sha256(V7_MANIFEST),
            str(RETURN_ROOT.relative_to(ROOT)): "directory_state_not_hashable",
            str(RECON_ROOT.relative_to(ROOT)): "directory_state_not_hashable",
        },
        "expected_v7_prompt_groups": len(groups),
        "state_counts": dict(sorted(state_counts.items())),
        "unexpected_final_disposition_batch_ids": unexpected_final_dispositions,
        "closure_gate": {
            "status": (
                "PASS_EXECUTION_STATE_RECONCILED"
                if not unresolved and not unexpected_final_dispositions
                else "BLOCKED_OUTSTANDING_OR_DEFECTIVE_V7_GROUPS"
            ),
            "outstanding_or_defective_batch_ids": unresolved,
        },
        "records": records,
    }
    payload["reconciliation_sha256"] = hashlib.sha256(
        canonical_json(payload)
    ).hexdigest()
    return payload


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def materialise(output_dir: Path) -> None:
    output = output_dir / "execution_state_reconciliation.json"
    if output.exists():
        raise ValueError(f"refusing to overwrite execution-state reconciliation: {output}")
    write_json(output, reconcile())
    print(json.dumps({"output": str(output), "status": "PASS_MATERIALISED"}, sort_keys=True))


def validate(output_dir: Path) -> None:
    output = output_dir / "execution_state_reconciliation.json"
    stored = read_json(output)
    current = reconcile()
    if stored != current:
        raise ValueError("execution-state reconciliation drift")
    print(
        json.dumps(
            {
                "output": str(output),
                "state_counts": current["state_counts"],
                "status": "PASS_REPLAYED_EXECUTION_STATE_RECONCILIATION",
            },
            sort_keys=True,
        )
    )


def validate_handoff(handoff_dir: Path) -> None:
    """Validate a state-pinned two-machine dispatch without reading outcomes.

    This deliberately validates the reconciliation snapshot named by the
    handoff's bound-input ledger.  It does not replace that snapshot with a
    fresh filesystem scan, because that would silently change its frozen work
    allocation.
    """
    report_path = handoff_dir / "integrity_report.json"
    assignment_path = handoff_dir / "phase5_v7_pending_assignment_v1.jsonl"
    machine_paths = {
        "machine_a": handoff_dir / "machine_a_manifest.jsonl",
        "machine_b": handoff_dir / "machine_b_manifest.jsonl",
    }
    if not report_path.is_file() or not assignment_path.is_file() or any(not path.is_file() for path in machine_paths.values()):
        raise ValueError("handoff package has required-file drift")
    report = read_json(report_path)
    state_relative = report.get("bound_inputs", {}).get("state_file")
    # V1 records the absolute reference as a normal relative workspace path
    # rather than trusting a caller-provided state directory.
    if not isinstance(state_relative, str):
        state_relative = next((key for key in report.get("bound_inputs", {}) if key.endswith("execution_state_reconciliation.json")), None)
    if not isinstance(state_relative, str):
        raise ValueError("handoff is missing its execution-state binding")
    state_path = (ROOT / state_relative).resolve()
    if not state_path.is_relative_to(ROOT) or not state_path.is_file():
        raise ValueError("handoff execution-state binding is unavailable")
    if report["bound_inputs"].get(state_relative) != sha256(state_path):
        raise ValueError("handoff execution-state hash binding drift")
    state = read_json(state_path)
    records = state.get("records")
    if not isinstance(records, list):
        raise ValueError("handoff execution-state records are unavailable")
    finalised = {record.get("batch_id") for record in records if isinstance(record, dict) and record.get("state") == "FINALISED"}
    assignments = read_jsonl(assignment_path)
    assigned_ids = {row.get("batch_id") for row in assignments}
    if len(assignments) != 1079 or len(assigned_ids) != 1079 or any(not isinstance(item, str) for item in assigned_ids):
        raise ValueError("handoff pending cardinality or identity drift")
    if assigned_ids & finalised:
        raise ValueError("handoff allocates a finalised snapshot batch")
    owners = {}
    for owner, path in machine_paths.items():
        rows = read_jsonl(path)
        ids = {row.get("batch_id") for row in rows}
        if any(row.get("owner_machine") != owner for row in rows):
            raise ValueError(f"handoff owner binding drift: {owner}")
        owners[owner] = ids
    if len(owners["machine_a"]) != 540 or len(owners["machine_b"]) != 539:
        raise ValueError("handoff machine allocation count drift")
    if owners["machine_a"] & owners["machine_b"] or owners["machine_a"] | owners["machine_b"] != assigned_ids:
        raise ValueError("handoff machine allocation membership drift")
    print(json.dumps({"handoff_dir": str(handoff_dir), "pending": 1079, "machine_a": 540, "machine_b": 539, "status": "PASS_STATE_PINNED_TWO_MACHINE_HANDOFF_RECOGNITION"}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("materialise", "validate"):
        command = subparsers.add_parser(name)
        command.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    handoff = subparsers.add_parser("validate-handoff")
    handoff.add_argument("--handoff-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "materialise":
        materialise(args.output_dir)
    elif args.command == "validate":
        validate(args.output_dir)
    else:
        validate_handoff(args.handoff_dir.resolve())


if __name__ == "__main__":
    main()
