#!/usr/bin/env python3
"""Validate two identity-overlay lanes and prepare a source-only coordinator queue."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from prepare_rq2b_v7_first_matrix import safe_path


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
INPUT_PACKAGE = PREP / "v7_phase7_i1_identity_overlay_review_2026_09_09_v1"
INPUT_CACHE = Path("skill_benchmark/cache/rq2b_v7_i1_identity_overlay_review_2026_09_09_v1")
OUTPUT = PREP / "v7_phase7_i1_identity_overlay_reconciliation_2026_09_09_v1"
OUTPUT_CACHE = Path("skill_benchmark/cache/rq2b_v7_i1_identity_overlay_reconciliation_2026_09_09_v1")
ALLOWED_DECISIONS = {"RECOVER_FRONTMATTER_CONTINUATION", "SOURCE_GROUNDED_BODY_OVERLAY", "UNRESOLVED"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_from_bytes(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def validate_lane(lane: str, inputs: list[dict], data: bytes) -> list[dict]:
    rows = rows_from_bytes(data)
    if len(rows) != len(inputs):
        raise ValueError(f"lane {lane} row count mismatch")
    required = {"review_id", "skill_id", "reviewer_lane", "status", "decision", "proposed_description", "source_evidence", "notes"}
    for inp, row in zip(inputs, rows, strict=True):
        if set(row) != required:
            raise ValueError(f"lane {lane} schema mismatch: {inp['review_id']}")
        if row["review_id"] != inp["review_id"] or row["skill_id"] != inp["skill_id"]:
            raise ValueError(f"lane {lane} identity/order mismatch")
        if row["reviewer_lane"] != lane or row["status"] != "COMPLETE" or row["decision"] not in ALLOWED_DECISIONS:
            raise ValueError(f"lane {lane} status/decision mismatch")
        if not isinstance(row["notes"], str) or len(row["notes"]) > 1000:
            raise ValueError(f"lane {lane} notes mismatch")
        unresolved = row["decision"] == "UNRESOLVED"
        if unresolved != (not row["proposed_description"] and not row["source_evidence"]):
            raise ValueError(f"lane {lane} unresolved payload mismatch")
        if not unresolved:
            if not isinstance(row["proposed_description"], str) or not row["proposed_description"].strip():
                raise ValueError(f"lane {lane} missing proposed description")
            if not isinstance(row["source_evidence"], str) or row["source_evidence"] not in inp["source_text"]:
                raise ValueError(f"lane {lane} non-source evidence")
            lowered = row["proposed_description"].strip().lower()
            if lowered in {">", "|", "use this skill when >", "use this skill when |"}:
                raise ValueError(f"lane {lane} unusable proposed description")
    return rows


def build() -> tuple[dict[str, bytes], dict[str, bytes]]:
    input_data = (ROOT / INPUT_CACHE / "review_input_lane_a.jsonl").read_bytes()
    if input_data != (ROOT / INPUT_CACHE / "review_input_lane_b.jsonl").read_bytes():
        raise ValueError("A/B source-only inputs differ")
    inputs = rows_from_bytes(input_data)
    candidates = rows_from_bytes((ROOT / INPUT_PACKAGE / "candidate_manifest.jsonl").read_bytes())
    if len(inputs) != len(candidates) != 39:
        raise ValueError("identity candidate coverage mismatch")
    return_data = {}
    lane_rows = {}
    for lane, name in (("A", "lane_a_return.jsonl"), ("B", "lane_b_return.jsonl")):
        data = (ROOT / INPUT_CACHE / "returns" / name).read_bytes()
        return_data[lane] = data
        lane_rows[lane] = validate_lane(lane, inputs, data)

    direct, coordinator_manifest, coordinator_inputs = [], [], []
    for inp, a, b in zip(inputs, lane_rows["A"], lane_rows["B"], strict=True):
        comparison_keys = ("decision", "proposed_description", "source_evidence")
        exact = all(a[key] == b[key] for key in comparison_keys) and a["decision"] != "UNRESOLVED"
        if exact:
            direct.append({
                "review_id": inp["review_id"],
                "skill_id": inp["skill_id"],
                "source_row_index": inp["source_row_index"],
                "source_path": inp["source_path"],
                "source_sha256": inp["source_sha256"],
                "selection_status": "DIRECT_EXACT_A_B_AGREEMENT",
                "decision": a["decision"],
                "selected_description": a["proposed_description"],
                "source_evidence": a["source_evidence"],
            })
            continue
        docket_id = "V7-I1-COORD-" + sha((inp["skill_id"] + "|identity-coordinator-v1").encode())[:16].upper()
        coordinator_manifest.append({
            "docket_id": docket_id,
            "review_id": inp["review_id"],
            "skill_id": inp["skill_id"],
            "source_row_index": inp["source_row_index"],
            "source_path": inp["source_path"],
            "source_sha256": inp["source_sha256"],
            "reason": "A_B_DISAGREEMENT_OR_UNRESOLVED",
            "state": "PENDING_SOURCE_ONLY_COORDINATOR",
        })
        coordinator_inputs.append({
            "docket_id": docket_id,
            "review_id": inp["review_id"],
            "skill_id": inp["skill_id"],
            "source_row_index": inp["source_row_index"],
            "source_path": inp["source_path"],
            "source_sha256": inp["source_sha256"],
            "parsed_name": inp["parsed_name"],
            "malformed_parsed_description": inp["malformed_parsed_description"],
            "malformation_class": inp["malformation_class"],
            "source_text": inp["source_text"],
            "lane_a": {key: a[key] for key in comparison_keys},
            "lane_b": {key: b[key] for key in comparison_keys},
        })

    files = {
        "reviewer_returns/lane_a_return.jsonl": return_data["A"],
        "reviewer_returns/lane_b_return.jsonl": return_data["B"],
        "direct_selection.jsonl": rows_bytes(direct),
        "coordinator_manifest.jsonl": rows_bytes(coordinator_manifest),
    }
    payloads = {"coordinator_input.jsonl": rows_bytes(coordinator_inputs)}
    report = {
        "schema_version": "rq2b-v7-i1-identity-overlay-reconciliation-v1",
        "state": "PENDING_SOURCE_ONLY_COORDINATOR" if coordinator_inputs else "PASS_ALL_39_DIRECT_EXACT_AGREEMENTS",
        "formal_execution_ready": False,
        "counts": {"candidates": 39, "direct_exact_agreements": len(direct), "coordinator_dockets": len(coordinator_inputs)},
        "bindings": {
            "preparation_report_sha256": sha((ROOT / INPUT_PACKAGE / "integrity_report.json").read_bytes()),
            "candidate_manifest_sha256": sha((ROOT / INPUT_PACKAGE / "candidate_manifest.jsonl").read_bytes()),
            "input_sha256": sha(input_data),
            "lane_a_return_sha256": sha(return_data["A"]),
            "lane_b_return_sha256": sha(return_data["B"]),
            "script_sha256": sha(Path(__file__).read_bytes()),
        },
        "artifacts": {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()},
        "local_coordinator_input": {"sha256": sha(payloads["coordinator_input.jsonl"]), "rows": len(coordinator_inputs)},
        "boundary": "No benchmark or retrieval evidence is used. Exact A/B agreement is mechanical selection; all other cases remain unresolved until source-only coordination.",
    }
    files["integrity_report.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 I1 identity overlay reconciliation\n\n"
        f"State: `{report['state']}`. Two independent source-only lanes cover all 39 malformed descriptions. "
        f"{len(direct)} exact non-unresolved agreements are selected mechanically; {len(coordinator_inputs)} dockets require a source-only coordinator.\n\n"
        "No original source, I1/I2 artifact, or reviewer return is overwritten. Replay: `python3 -B skill_benchmark/scripts/reconcile_rq2b_v7_i1_identity_overlay_review.py --verify`.\n"
    ).encode()
    return files, payloads


def require_equal(path: Path, data: bytes) -> None:
    if path.read_bytes() != data:
        raise ValueError(f"artifact drift: {path}")


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    files, payloads = build()
    if args.verify:
        for name, data in files.items():
            require_equal(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            require_equal(ROOT / OUTPUT_CACHE / name, data)
        status = "PASS_V7_I1_IDENTITY_RECONCILIATION_REPLAY"
    else:
        if (ROOT / OUTPUT).exists() or (ROOT / OUTPUT_CACHE).exists():
            raise FileExistsError("refusing to overwrite versioned identity reconciliation")
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            write_new(ROOT / OUTPUT_CACHE / name, data)
        status = "PASS_V7_I1_IDENTITY_RECONCILIATION_CREATED"
    print(json.dumps({"status": status, "candidates": 39}, sort_keys=True))


if __name__ == "__main__":
    main()
