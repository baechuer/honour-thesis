#!/usr/bin/env python3
"""Integrate the prospective V4.1.3 warning repairs over selection-v2."""

from __future__ import annotations

import hashlib
import json
import tempfile
from collections import defaultdict
from pathlib import Path

import build_rq2b_v7_i3_v4_1_2_warning_repair_integration as atomic
import validate_rq2b_v7_i3_v4_1_2_batch as validator


ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation"
BASE = PREP / "v7_phase7_i3_v4_1_2_warning_repair_integration_2026_09_09_v3"
AUDIT = PREP / "v7_phase7_i3_v4_1_2_warning_audit_2026_09_09_v3"
PROPOSALS = PREP / "v7_phase7_i3_v4_1_3_warning_repair_proposals_2026_09_09_v1"
OUTPUT = PREP / "v7_phase7_i3_v4_1_3_warning_repair_integration_2026_09_09_v3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def obj(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def jsonl_bytes(values: list[dict]) -> bytes:
    return b"".join((json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode() for value in values)


def bind(path: Path, *, count: int | None = None) -> dict:
    value = {"path": rel(path), "sha256": sha(path)}
    if count is not None:
        value["rows"] = count
    return value


def proposal_binding(group: int, ledger_row: dict) -> tuple[Path, str]:
    if group == 1:
        return ROOT / ledger_row["proposal_output"]["path"], ledger_row["proposal_output"]["sha256"]
    return ROOT / ledger_row["proposal_output_path"], ledger_row["proposal_output_sha256"]


def main() -> int:
    require(not OUTPUT.exists(), f"refusing to overwrite: {OUTPUT}")
    selection_path = BASE / "selection_v2_ledger.jsonl"
    base_report_path = BASE / "integrity_report.json"
    selection = rows(selection_path)
    require(len(selection) == 95 and sum(row["row_count"] for row in selection) == 3798, "selection-v2 coverage drift")
    base_report = obj(base_report_path)
    require(base_report["state"] == "PASS_95_BATCHES_REPAIR_INTEGRATED_PENDING_FRESH_WARNING_QA", "selection-v2 state drift")
    require(base_report["output_bindings"]["selection_v2_ledger"]["sha256"] == sha(selection_path), "selection-v2 report binding drift")

    audit_returns = []
    for group in (1, 2, 3):
        path = AUDIT / f"returns/reviewer_group_{group}_return.jsonl"
        audit_returns.extend(rows(path))
    required_reissues = {row["issue_id"] for row in audit_returns if row["decision"] == "REISSUE_REQUIRED"}
    require(len(required_reissues) == 17, "fresh warning reissue count drift")

    ledgers: dict[int, list[dict]] = {}
    reports: dict[int, Path] = {}
    proposal_by_group_batch: dict[int, dict[str, list[dict]]] = {1: {}, 2: {}}
    input_bindings = [bind(selection_path, count=95), bind(base_report_path)]
    for group in (1, 2):
        ledger_path = PROPOSALS / f"group_{group}/issue_ledger.jsonl"
        report_path = PROPOSALS / f"group_{group}/validation_report.json"
        ledger = rows(ledger_path)
        report = obj(report_path)
        require(report["status"] == "PASS_PROSPECTIVE_V4_1_3_PROPOSAL_VALIDATION", f"group {group} proposal is not PASS")
        ledgers[group] = ledger
        reports[group] = report_path
        input_bindings.extend([bind(ledger_path, count=len(ledger)), bind(report_path)])
        by_batch: dict[str, list[dict]] = defaultdict(list)
        for row in ledger:
            by_batch[row["batch_id"]].append(row)
        for batch_id, batch_issues in by_batch.items():
            paths = {proposal_binding(group, row) for row in batch_issues}
            require(len(paths) == 1, f"group {group} proposal binding disagreement: {batch_id}")
            path, expected = paths.pop()
            require(path.is_file() and sha(path) == expected, f"group {group} proposal hash drift: {batch_id}")
            proposal_by_group_batch[group][batch_id] = rows(path)
            input_bindings.append(bind(path, count=len(proposal_by_group_batch[group][batch_id])))
    require({row["issue_id"] for group_rows in ledgers.values() for row in group_rows} == required_reissues, "proposal/reissue issue coverage mismatch")

    selection_by_batch = {row["batch_id"]: row for row in selection}
    repaired: dict[str, bytes] = {}
    ledger_out: list[dict] = []
    conflicts: list[dict] = []
    validations = []
    with tempfile.TemporaryDirectory(prefix="rq2b-i3-v4-1-3-", dir=ROOT / "skill_benchmark/cache") as temp_dir:
        temp = Path(temp_dir)
        for batch_id in sorted(selection_by_batch):
            base_entry = selection_by_batch[batch_id]
            base_path = ROOT / base_entry["selected_output_path"]
            require(sha(base_path) == base_entry["selected_output_sha256"], f"baseline hash drift: {batch_id}")
            base_rows = rows(base_path)
            merged_rows = []
            applied_groups: set[int] = set()
            applied_issues: set[str] = set()
            authorised_by_group = {
                group: {item["skill_id"] for item in ledgers[group] if item["batch_id"] == batch_id}
                for group in (1, 2)
            }
            for group in (1, 2):
                candidate = proposal_by_group_batch[group].get(batch_id)
                if candidate is None:
                    continue
                require(len(candidate) == len(base_rows), f"group {group} row count drift: {batch_id}")
                changed = {
                    row["skill_id"] for before, row in zip(base_rows, candidate)
                    if before != row
                }
                require(changed == authorised_by_group[group], f"group {group} changed-row scope drift: {batch_id}")
            for index, base_row in enumerate(base_rows):
                candidates = {
                    group: proposal_by_group_batch[group][batch_id][index]
                    for group in (1, 2)
                    if batch_id in proposal_by_group_batch[group]
                    and proposal_by_group_batch[group][batch_id][index] != base_row
                }
                if not candidates:
                    merged_rows.append(base_row)
                    continue
                merged, row_conflicts = atomic.merge_row(
                    base_row, candidates, batch_id=batch_id, source_row_index=index + 1
                )
                conflicts.extend(row_conflicts)
                merged_rows.append(merged)
                applied_groups.update(candidates)
                for group in candidates:
                    applied_issues.update(
                        item["issue_id"] for item in ledgers[group]
                        if item["batch_id"] == batch_id and item["skill_id"] == base_row["skill_id"]
                    )
            require(not conflicts, "V4.1.3 proposal merge conflict")
            data = jsonl_bytes(merged_rows)
            # JSONL serialisation in historical selected batches is not
            # necessarily canonical.  Equality of parsed rows, rather than
            # byte formatting, is the semantic no-op test.
            if merged_rows == base_rows:
                selected_path = base_path
                selected_data = base_path.read_bytes()
                selection_kind = "UNCHANGED_SELECTION_V2"
            else:
                selected_path = OUTPUT / "repaired_batches" / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_3.jsonl"
                repaired[batch_id] = data
                selected_data = data
                selection_kind = "REPAIRED_V4_1_3_REISSUE"
            validation_path = selected_path
            if batch_id in repaired:
                validation_path = temp / f"{batch_id}.jsonl"
                validation_path.write_bytes(data)
            result = validator.validate(batch_id, validation_path)
            require(result["status"] == "PASS_I3_V4_1_2_BATCH_VALIDATION", f"validator failure: {batch_id}")
            validations.append(result)
            ledger_out.append({
                "schema_version": "rq2b-v7-i3-v4.1.3-output-selection-v3",
                "batch_id": batch_id,
                "input_sha256": base_entry["input_sha256"],
                "row_count": base_entry["row_count"],
                "baseline_selection_v2_path": base_entry["selected_output_path"],
                "baseline_selection_v2_sha256": base_entry["selected_output_sha256"],
                "selection_kind": selection_kind,
                "selected_output_path": rel(selected_path),
                "selected_output_sha256": hashlib.sha256(selected_data).hexdigest(),
                "applied_issue_ids": sorted(applied_issues),
                "applied_reviewer_groups": sorted(applied_groups),
                "validator_status": result["status"],
            })

    require(sum(len(row["applied_issue_ids"]) for row in ledger_out) == 17, "integrated issue count drift")
    staging = OUTPUT.parent / f".{OUTPUT.name}.staging"
    require(not staging.exists(), f"stale staging path: {staging}")
    staging.mkdir(parents=True)
    try:
        repaired_dir = staging / "repaired_batches"
        repaired_dir.mkdir()
        for batch_id, data in repaired.items():
            (repaired_dir / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_3.jsonl").write_bytes(data)
        ledger_data = jsonl_bytes(ledger_out)
        (staging / "selection_v3_ledger.jsonl").write_bytes(ledger_data)
        report = {
            "schema_version": "rq2b-v7-i3-v4.1.3-warning-repair-integration-report-v1",
            "state": "PASS_95_BATCHES_V4_1_3_REPAIR_INTEGRATED_PENDING_FRESH_WARNING_AUDIT",
            "formal_execution_ready": False,
            "counts": {
                "batches": 95,
                "rows": 3798,
                "integrated_issues": 17,
                "repaired_batches": len(repaired),
                "unchanged_batches": 95 - len(repaired),
                "conflicts": 0,
                "validator_passes": len(validations),
            },
            "input_bindings": input_bindings,
            "output_bindings": {
                "builder": {"path": rel(Path(__file__)), "sha256": sha(Path(__file__))},
                "selection_v3_ledger": {"path": rel(OUTPUT / "selection_v3_ledger.jsonl"), "sha256": hashlib.sha256(ledger_data).hexdigest(), "rows": 95},
                "repaired_batches": [
                    {"batch_id": batch_id, "path": rel(OUTPUT / "repaired_batches" / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_3.jsonl"), "sha256": hashlib.sha256(data).hexdigest(), "rows": len(rows(BASE / "repaired_batches" / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_2.jsonl")) if (BASE / "repaired_batches" / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_2.jsonl").exists() else 40}
                    for batch_id, data in sorted(repaired.items())
                ],
            },
            "boundary": "Prospective source-only I3 repair. No query, source-union, label, acceptable set, selector, result, or metric is changed.",
        }
        (staging / "integrity_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        staging.rename(OUTPUT)
    except Exception:
        import shutil
        shutil.rmtree(staging)
        raise
    print(json.dumps({"state": report["state"], "counts": report["counts"], "report_sha256": sha(OUTPUT / "integrity_report.json")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
