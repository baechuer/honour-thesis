#!/usr/bin/env python3
"""Freeze the reconciled 39-row V7 source-grounded I1 identity overlay."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from prepare_rq2b_v7_first_matrix import safe_path


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
RECON = PREP / "v7_phase7_i1_identity_overlay_reconciliation_2026_09_09_v1"
RECON_CACHE = Path("skill_benchmark/cache/rq2b_v7_i1_identity_overlay_reconciliation_2026_09_09_v1")
OUTPUT = PREP / "v7_phase7_i1_identity_overlay_final_2026_09_09_v1"
INSTRUCTION = Path("skill_benchmark/extraction_prompts/I1_IDENTITY_OVERLAY_COORDINATOR_V1.md")
ALLOWED_DECISIONS = {"SELECT_A", "SELECT_B", "SOURCE_GROUNDED_ALTERNATIVE", "UNRESOLVED"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def build() -> dict[str, bytes]:
    report = json.loads((ROOT / RECON / "integrity_report.json").read_bytes())
    direct = rows(ROOT / RECON / "direct_selection.jsonl")
    dockets = rows(ROOT / RECON / "coordinator_manifest.jsonl")
    coordinator_input = rows(ROOT / RECON_CACHE / "coordinator_input.jsonl")
    if len(dockets) != len(coordinator_input):
        raise ValueError("coordinator docket/input mismatch")
    coordinator_data = b""
    coordinator_rows: list[dict] = []
    if dockets:
        coordinator_path = ROOT / RECON_CACHE / "coordinator_return.jsonl"
        coordinator_data = coordinator_path.read_bytes()
        coordinator_rows = [json.loads(line) for line in coordinator_data.splitlines()]
        if len(coordinator_rows) != len(dockets):
            raise ValueError("coordinator return count mismatch")
    required = {"docket_id", "skill_id", "status", "decision", "selected_description", "source_evidence", "rationale"}
    resolved = []
    for docket, inp, row in zip(dockets, coordinator_input, coordinator_rows, strict=True):
        if set(row) != required:
            raise ValueError(f"coordinator schema mismatch: {docket['docket_id']}")
        if row["docket_id"] != docket["docket_id"] or row["skill_id"] != docket["skill_id"]:
            raise ValueError("coordinator identity/order mismatch")
        if row["status"] != "COMPLETE" or row["decision"] not in ALLOWED_DECISIONS:
            raise ValueError("coordinator status/decision mismatch")
        if row["decision"] == "UNRESOLVED":
            raise ValueError(f"unresolved identity cannot enter final overlay: {docket['docket_id']}")
        if not row["selected_description"].strip() or row["source_evidence"] not in inp["source_text"]:
            raise ValueError("coordinator description/evidence mismatch")
        resolved.append({
            "review_id": docket["review_id"],
            "skill_id": docket["skill_id"],
            "source_row_index": docket["source_row_index"],
            "source_path": docket["source_path"],
            "source_sha256": docket["source_sha256"],
            "selection_status": "SOURCE_ONLY_COORDINATOR_RESOLVED",
            "decision": row["decision"],
            "selected_description": row["selected_description"],
            "source_evidence": row["source_evidence"],
        })
    overlay = sorted([*direct, *resolved], key=lambda row: row["source_row_index"])
    if len(overlay) != 39 or len({row["skill_id"] for row in overlay}) != 39:
        raise ValueError("final identity overlay coverage mismatch")
    for row in overlay:
        raw = safe_path(ROOT, row["source_path"]).read_bytes()
        if sha(raw) != row["source_sha256"] or row["source_evidence"] not in raw.decode("utf-8"):
            raise ValueError("final overlay source binding mismatch")
        if row["selected_description"].strip().lower() in {">", "|", "use this skill when >", "use this skill when |"}:
            raise ValueError("unusable final overlay description")
    files = {"identity_overlay.jsonl": rows_bytes(overlay)}
    if dockets:
        files["coordinator_return.jsonl"] = coordinator_data
    final_report = {
        "schema_version": "rq2b-v7-i1-source-grounded-identity-overlay-final-v1",
        "state": "PASS_39_SOURCE_GROUNDED_IDENTITY_OVERLAYS_FROZEN",
        "formal_execution_ready": False,
        "counts": {"overlay_rows": 39, "direct_exact_agreements": len(direct), "coordinator_resolved": len(resolved), "unresolved": 0},
        "bindings": {
            "reconciliation_report_sha256": sha((ROOT / RECON / "integrity_report.json").read_bytes()),
            "direct_selection_sha256": sha((ROOT / RECON / "direct_selection.jsonl").read_bytes()),
            "coordinator_manifest_sha256": sha((ROOT / RECON / "coordinator_manifest.jsonl").read_bytes()),
            "coordinator_input_sha256": sha((ROOT / RECON_CACHE / "coordinator_input.jsonl").read_bytes()),
            "coordinator_instruction_sha256": sha((ROOT / INSTRUCTION).read_bytes()),
            "coordinator_return_sha256": sha(coordinator_data),
            "script_sha256": sha(Path(__file__).read_bytes()),
        },
        "artifacts": {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()},
        "method_boundary": "These 39 descriptions are explicitly source-grounded overlays, not source-native frontmatter. Source bytes and V7 benchmark scope remain unchanged; I2 remains byte-exact.",
        "next_gate": "Rebuild I1 and perform a full source-only I3 V4 re-extraction before drawing a fresh blinded QA sample.",
    }
    files["integrity_report.json"] = json_bytes(final_report)
    files["README.md"] = (
        "# V7 source-grounded I1 identity overlay final\n\n"
        "State: `PASS_39_SOURCE_GROUNDED_IDENTITY_OVERLAYS_FROZEN`. The overlay repairs only malformed identity descriptions and is applied prospectively before formal selector execution. It does not modify source bytes, prompts, labels, acceptable sets, or retrieval outcomes.\n\n"
        "These descriptions must be reported as source-grounded overlays rather than native frontmatter. Replay: `python3 -B skill_benchmark/scripts/finalize_rq2b_v7_i1_identity_overlay.py --verify`.\n"
    ).encode()
    return files


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
    files = build()
    if args.verify:
        for name, data in files.items():
            require_equal(ROOT / OUTPUT / name, data)
        status = "PASS_V7_I1_IDENTITY_OVERLAY_FINAL_REPLAY"
    else:
        if (ROOT / OUTPUT).exists():
            raise FileExistsError("refusing to overwrite versioned final identity overlay")
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        status = "PASS_V7_I1_IDENTITY_OVERLAY_FINAL_CREATED"
    print(json.dumps({"status": status, "overlay_rows": 39}, sort_keys=True))


if __name__ == "__main__":
    main()
