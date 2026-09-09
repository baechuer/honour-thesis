#!/usr/bin/env python3
"""Integrate source-only V4.1 warning repairs by a fail-closed three-way merge.

The selected V4.1 output is always the merge base.  A reviewer group's full
proposal is never copied over another group's work: instead, item-keyed field
and warning-keyed patches are derived against that base and combined only when
they agree or touch disjoint atoms.
"""
from __future__ import annotations

import argparse
import ast
import copy
import difflib
import hashlib
import json
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import merge_rq2b_i3c as shared
import validate_rq2b_v7_i3_v4_1_2_batch as validator


ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation"
SELECTION_DIR = PREP / "v7_phase7_i3_v4_1_output_selection_2026_09_09_v1"
WARNING_FINAL_DIR = PREP / "v7_phase7_i3_v4_1_warning_audit_final_2026_09_09_v1"
PROPOSAL_DIR = PREP / "v7_phase7_i3_v4_1_warning_repair_proposals_2026_09_09_v1"
SUPPLEMENT_V2_DIR = PREP / "v7_phase7_i3_v4_1_warning_repair_supplemental_2026_09_09_v2"
AMENDMENT_DIR = PREP / "v7_phase7_i3_v4_1_2_warning_evidence_amendment_2026_09_09_v1"
CONFLICT_RESOLUTION_DIR = PREP / "v7_phase7_i3_v4_1_2_warning_repair_conflict_resolution_2026_09_09_v1"
OUTPUT_DIR = PREP / "v7_phase7_i3_v4_1_2_warning_repair_integration_2026_09_09_v3"

SELECTION_LEDGER = SELECTION_DIR / "selection_ledger.jsonl"
SELECTION_REPORT = SELECTION_DIR / "integrity_report.json"
WARNING_LEDGER = WARNING_FINAL_DIR / "warning_disposition_ledger.jsonl"
WARNING_REPORT = WARNING_FINAL_DIR / "integrity_report.json"
AMENDMENT_README = AMENDMENT_DIR / "README.md"
AMENDMENT_REPORT = AMENDMENT_DIR / "integrity_report.json"
AUTHORITATIVE_CONFLICT_DOCKET = (
    PREP
    / "v7_phase7_i3_v4_1_2_warning_repair_integration_2026_09_09_v1"
    / "conflicts/conflict_docket_872aef28cc1072db.jsonl"
)
CONFLICT_RESOLUTION_LEDGER = CONFLICT_RESOLUTION_DIR / "resolution_ledger.jsonl"

GROUP_LEDGER = {
    1: PROPOSAL_DIR / "group_1/repair_ledger.jsonl",
    2: PROPOSAL_DIR / "group_2/issue_before_after_ledger.jsonl",
    3: PROPOSAL_DIR / "group_3/proposal_ledger.jsonl",
}
GROUP_REPORT = {
    1: PROPOSAL_DIR / "group_1/validation_report.json",
    2: PROPOSAL_DIR / "group_2/validation_report.json",
    3: PROPOSAL_DIR / "group_3/validation_report.json",
}
SUPPLEMENT_LEDGER = {
    1: PROPOSAL_DIR / "group_1/supplemental_ledger_v4_1_2_attempt_001.jsonl",
    2: SUPPLEMENT_V2_DIR / "group_2/supplemental_issue_before_after_ledger.jsonl",
    3: PROPOSAL_DIR / "group_3/proposal_ledger_v4_1_2_attempt_001.jsonl",
}
SUPPLEMENT_REPORT = {
    1: PROPOSAL_DIR / "group_1/validation_report_v4_1_2_supplemental_attempt_001.json",
    2: SUPPLEMENT_V2_DIR / "group_2/supplemental_validation_report.json",
    3: PROPOSAL_DIR / "group_3/validation_report_v4_1_2_attempt_001.json",
}

LEDGER_OUT = OUTPUT_DIR / "selection_v2_ledger.jsonl"
REPORT_OUT = OUTPUT_DIR / "integrity_report.json"
REPAIRED_DIR = OUTPUT_DIR / "repaired_batches"

ALLOWED_ROW_MUTABLE_KEYS = {"fields", "absent_fields", "qa_warnings"}
IDENTITY_KEYS = ("skill_id", "source")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_sha(value: Any) -> str:
    return sha_bytes(canonical(value).encode())


def jsonl_rows(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")
    result = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        require(bool(line), f"blank JSONL line: {path.relative_to(ROOT)}:{line_number}")
        value = json.loads(line)
        require(isinstance(value, dict), f"non-object JSONL row: {path.relative_to(ROOT)}:{line_number}")
        result.append(value)
    return result


def json_obj(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text())
    require(isinstance(value, dict), f"expected JSON object: {path.relative_to(ROOT)}")
    return value


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join((canonical(row) + "\n").encode() for row in rows)


def report_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def bind(path: Path, *, rows: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"path": rel(path), "sha256": sha(path)}
    if rows is not None:
        result["rows"] = rows
    return result


def same_identity(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return all(left.get(key) == right.get(key) for key in IDENTITY_KEYS)


def row_changed_keys(base: dict[str, Any], candidate: dict[str, Any]) -> set[str]:
    require(set(base) == set(candidate), "proposal changed top-level row key set")
    return {key for key in base if base[key] != candidate[key]}


def field_atom_map(row: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    result = {}
    for field in shared.FIELD_KEYS:
        for item in row["fields"][field]:
            key = (field, item["id"])
            require(key not in result, f"duplicate field item key: {key}")
            result[key] = item
    return result


@dataclass(frozen=True)
class Conflict:
    area: str
    atom: str
    groups: tuple[int, ...]
    reason: str
    baseline_sha256: str | None
    candidate_sha256: tuple[str | None, ...]

    def as_dict(self, *, batch_id: str, skill_id: str, source_row_index: int) -> dict[str, Any]:
        return {
            "schema_version": "rq2b-v7-i3-v4.1.2-warning-repair-conflict-v1",
            "batch_id": batch_id,
            "skill_id": skill_id,
            "source_row_index": source_row_index,
            "area": self.area,
            "atom": self.atom,
            "groups": list(self.groups),
            "reason": self.reason,
            "baseline_sha256": self.baseline_sha256,
            "candidate_sha256": list(self.candidate_sha256),
            "resolution": "BLOCKED_NO_GROUP_PRIORITY_OR_LAST_WRITER_WINS",
        }


def merge_atomic_map(
    base: dict[Any, Any], candidates: dict[int, dict[Any, Any]], *, area: str
) -> tuple[dict[Any, Any], list[Conflict]]:
    """Three-way merge mappings; missing means deletion and equality is canonical."""
    touched: dict[Any, list[tuple[int, Any]]] = defaultdict(list)
    for group, candidate in candidates.items():
        for key in set(base) | set(candidate):
            if base.get(key) != candidate.get(key) or (key in base) != (key in candidate):
                touched[key].append((group, candidate.get(key)))
    merged = copy.deepcopy(base)
    conflicts: list[Conflict] = []
    for key, edits in sorted(touched.items(), key=lambda pair: str(pair[0])):
        values = {canonical(value) for _, value in edits}
        if len(values) != 1:
            conflicts.append(Conflict(
                area=area,
                atom=str(key),
                groups=tuple(group for group, _ in edits),
                reason="DIVERGENT_BASELINE_RELATIVE_ATOMIC_EDITS",
                baseline_sha256=canonical_sha(base[key]) if key in base else None,
                candidate_sha256=tuple(canonical_sha(value) if value is not None else None for _, value in edits),
            ))
            continue
        value = edits[0][1]
        if value is None:
            merged.pop(key, None)
        else:
            merged[key] = copy.deepcopy(value)
    return merged, conflicts


def sequence_patch(base: list[Any], candidate: list[Any]) -> list[tuple[int, int, list[Any]]]:
    """Return exact base-coordinate edits, preserving duplicate list members."""
    left = [canonical(value) for value in base]
    right = [canonical(value) for value in candidate]
    matcher = difflib.SequenceMatcher(a=left, b=right, autojunk=False)
    return [
        (i1, i2, copy.deepcopy(candidate[j1:j2]))
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]


def sequence_edits_overlap(left: tuple[int, int, list[Any]], right: tuple[int, int, list[Any]]) -> bool:
    li, lj, _ = left
    ri, rj, _ = right
    if li == lj and ri == rj:
        return li == ri
    if li == lj:
        return ri <= li <= rj
    if ri == rj:
        return li <= ri <= lj
    return max(li, ri) < min(lj, rj)


def merge_sequence(
    base: list[Any], candidates: dict[int, list[Any]], *, area: str
) -> tuple[list[Any], list[Conflict]]:
    """Merge list edits in base coordinates; duplicates remain unambiguous."""
    accepted: list[tuple[int, int, list[Any], tuple[int, ...]]] = []
    conflicts: list[Conflict] = []
    for group, candidate in sorted(candidates.items()):
        for edit in sequence_patch(base, candidate):
            identical = next(
                (index for index, current in enumerate(accepted)
                 if current[:2] == edit[:2] and canonical(current[2]) == canonical(edit[2])),
                None,
            )
            if identical is not None:
                old = accepted[identical]
                accepted[identical] = (old[0], old[1], old[2], old[3] + (group,))
                continue
            overlaps = [current for current in accepted if sequence_edits_overlap(edit, current[:3])]
            if overlaps:
                other_groups = tuple(value for current in overlaps for value in current[3])
                conflicts.append(Conflict(
                    area=area,
                    atom=f"base_slice[{edit[0]}:{edit[1]}]",
                    groups=other_groups + (group,),
                    reason="DIVERGENT_BASELINE_RELATIVE_SEQUENCE_EDITS",
                    baseline_sha256=canonical_sha(base[edit[0]:edit[1]]),
                    candidate_sha256=tuple(canonical_sha(current[2]) for current in overlaps) + (canonical_sha(edit[2]),),
                ))
                continue
            accepted.append((edit[0], edit[1], edit[2], (group,)))
    merged = copy.deepcopy(base)
    for start, end, replacement, _ in sorted(accepted, key=lambda value: (value[0], value[1]), reverse=True):
        merged[start:end] = copy.deepcopy(replacement)
    return merged, conflicts


def merge_row(
    base: dict[str, Any], candidates: dict[int, dict[str, Any]], *, batch_id: str, source_row_index: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Merge one row using field item IDs and warning locators as atomic keys."""
    for group, candidate in candidates.items():
        require(same_identity(base, candidate), f"identity drift in {batch_id} row {source_row_index} group {group}")
        changed = row_changed_keys(base, candidate)
        require(changed <= ALLOWED_ROW_MUTABLE_KEYS, f"unauthorised row keys {sorted(changed)} in {batch_id} group {group}")
        expected_absent = [field for field in shared.FIELD_KEYS if not candidate["fields"][field]]
        require(candidate["absent_fields"] == expected_absent, f"bad proposal absent_fields in {batch_id} group {group}")

    base_fields = field_atom_map(base)
    candidate_fields = {group: field_atom_map(row) for group, row in candidates.items()}
    merged_fields, field_conflicts = merge_atomic_map(base_fields, candidate_fields, area="fields")

    merged_warnings, warning_conflicts = merge_sequence(
        base["qa_warnings"],
        {group: row["qa_warnings"] for group, row in candidates.items()},
        area="qa_warnings",
    )
    conflicts = field_conflicts + warning_conflicts

    result = copy.deepcopy(base)
    for field in shared.FIELD_KEYS:
        base_keys = [(field, item["id"]) for item in base["fields"][field]]
        kept = [key for key in base_keys if key in merged_fields]
        added = sorted(
            (key for key in merged_fields if key[0] == field and key not in base_fields),
            key=lambda key: key[1],
        )
        result["fields"][field] = [copy.deepcopy(merged_fields[key]) for key in kept + added]
    result["qa_warnings"] = merged_warnings
    result["absent_fields"] = [field for field in shared.FIELD_KEYS if not result["fields"][field]]
    docket = [
        conflict.as_dict(batch_id=batch_id, skill_id=base["skill_id"], source_row_index=source_row_index)
        for conflict in conflicts
    ]
    return result, docket


def proposal_status(group: int, row: dict[str, Any]) -> str:
    return row["proposal_status"] if group in (1, 2) else row["status"]


def is_applied(group: int, row: dict[str, Any]) -> bool:
    return proposal_status(group, row) in {"APPLIED", "PROPOSED_VALIDATED"}


def proposal_path(group: int, rows: list[dict[str, Any]], batch_id: str) -> Path:
    row = rows[0]
    if group == 1:
        return ROOT / row["proposal_output"]["path"]
    if group == 2:
        return PROPOSAL_DIR / f"group_2/proposed_outputs/i3v41_output_{batch_id[-3:]}_proposed_group_2.jsonl"
    return ROOT / row["proposed_output_path"]


def proposal_hash(group: int, row: dict[str, Any]) -> str:
    if group == 1:
        return row["proposal_output"]["sha256"]
    if group == 2:
        return row["proposed_output_sha256"]
    return row["proposed_output_sha256_after"]


def supplement_attempt_path(group: int, row: dict[str, Any]) -> Path:
    if group == 1:
        return ROOT / row["supplemental_output"]["path"]
    if group == 2:
        return SUPPLEMENT_V2_DIR / f"group_2/attempts/{row['batch_id']}/supplemental_attempt_001.jsonl"
    value = row.get("attempt_path") or row.get("proposed_output_path")
    require(isinstance(value, str), "supplement row lacks attempt_path/proposed_output_path")
    return ROOT / value


def supplement_attempt_hash(row: dict[str, Any]) -> str:
    value = (
        row.get("supplemental_output", {}).get("sha256")
        or row.get("supplemental_attempt_sha256")
        or row.get("attempt_sha256")
        or row.get("proposed_output_sha256_after")
        or row.get("proposed_output_sha256")
    )
    require(isinstance(value, str), "supplement row lacks attempt output hash")
    return value


def verify_supplement_delta(
    *, group: int, batch_id: str, base_proposal: list[dict[str, Any]],
    attempt: list[dict[str, Any]], ledger_rows: list[dict[str, Any]],
) -> None:
    """Replay each frozen supplemental schema without widening its authority."""
    require(len(base_proposal) == len(attempt), f"group {group} supplement row count drift: {batch_id}")
    authorised = {row["skill_id"] for row in ledger_rows}
    changed = set()
    evidence_changes = 0
    for index, (before, after) in enumerate(zip(base_proposal, attempt)):
        require(same_identity(before, after), f"group {group} supplement identity drift: {batch_id}/{index}")
        if before == after:
            continue
        changed.add(before["skill_id"])
        require(before.keys() == after.keys(), f"group {group} supplement top-level key drift: {batch_id}/{index}")
        changed_keys = row_changed_keys(before, after)
        require(changed_keys <= ALLOWED_ROW_MUTABLE_KEYS, f"group {group} supplement unauthorised row change: {batch_id}/{index}")
        if group == 3:
            require(
                all(before[key] == after[key] for key in before if key != "qa_warnings"),
                f"group {group} supplement changed selector-visible/non-warning content: {batch_id}/{index}",
            )
            require(len(before["qa_warnings"]) == len(after["qa_warnings"]), f"group {group} supplement warning count drift: {batch_id}/{index}")
            for warning_before, warning_after in zip(before["qa_warnings"], after["qa_warnings"]):
                require(warning_before.keys() == warning_after.keys(), f"group {group} supplement warning schema drift: {batch_id}/{index}")
                require(
                    all(warning_before[key] == warning_after[key] for key in warning_before if key != "evidence"),
                    f"group {group} supplement changed warning metadata beyond evidence: {batch_id}/{index}",
                )
                if warning_before["evidence"] != warning_after["evidence"]:
                    evidence_changes += 1
    require(changed == authorised, f"group {group} supplement changed-row/ledger mismatch: {batch_id}")
    if group == 3:
        require(evidence_changes >= len(authorised), f"group {group} supplement evidence-change coverage mismatch: {batch_id}")
    elif group == 1:
        require(
            all(row.get("supplemental_status") == "REPAIRED_SOURCE_GROUNDED" for row in ledger_rows),
            f"group {group} supplement status drift: {batch_id}",
        )
    else:
        after_by_skill = {row["skill_id"]: row for row in attempt}
        for ledger_row in ledger_rows:
            skill_id = ledger_row["skill_id"]
            before_snapshot = ledger_row["before"]
            after_snapshot = ledger_row["after"]
            require(set(before_snapshot) <= {"fields", "qa_warnings", "absent_fields"}, f"group 2 supplement before snapshot scope drift: {batch_id}/{skill_id}")
            require(set(after_snapshot) <= {"fields", "qa_warnings", "absent_fields"}, f"group 2 supplement after snapshot scope drift: {batch_id}/{skill_id}")
            # Group 2 applies multiple issues on some rows sequentially, so an
            # issue's before snapshot may be an intermediate state.  The final
            # after snapshot is the binding to the full supplemental attempt.
            require(
                all(after_snapshot[key] == after_by_skill[skill_id][key] for key in after_snapshot),
                f"group 2 supplement final after snapshot mismatch: {batch_id}/{skill_id}",
            )
            require(isinstance(ledger_row.get("actions"), list) and ledger_row["actions"], f"group 2 supplement lacks traceable actions: {batch_id}/{skill_id}")


def verify_amendment() -> list[dict[str, Any]]:
    report = json_obj(AMENDMENT_REPORT)
    bindings = report["bindings"]
    expected = bindings["v4_1_2_validator"]
    require(expected["path"] == rel(Path(validator.__file__).resolve()), "amendment validator path mismatch")
    require(expected["sha256"] == sha(Path(validator.__file__).resolve()), "amendment validator hash mismatch")
    require(report["change"]["representation_serialization_unchanged"] is True, "amendment changes serialization")
    require(report["change"]["field_item_evidence_contract_unchanged"] is True, "amendment changes field-item contract")
    return [bind(AMENDMENT_README), bind(AMENDMENT_REPORT), bind(Path(validator.__file__).resolve())]


def conflict_key(row: dict[str, Any]) -> tuple[str, int, str, str]:
    atom = row["atom"]
    if isinstance(atom, list):
        atom = str(tuple(atom))
    return row["batch_id"], row["source_row_index"], row["area"], atom


def load_conflict_resolutions() -> tuple[dict[tuple[str, int, str, str], dict[str, Any]], list[dict[str, Any]]]:
    docket = jsonl_rows(AUTHORITATIVE_CONFLICT_DOCKET)
    ledger = jsonl_rows(CONFLICT_RESOLUTION_LEDGER)
    require(len(docket) == len(ledger) == 3, "conflict-resolution coverage drift")
    docket_sha = sha(AUTHORITATIVE_CONFLICT_DOCKET)
    docket_by_key = {conflict_key(row): row for row in docket}
    require(len(docket_by_key) == 3, "duplicate authoritative conflict key")
    resolved: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for row_number, row in enumerate(ledger, 1):
        expected_keys = {
            "schema_version", "resolution_id", "conflict_docket", "batch_id",
            "source_row_index", "skill_id", "area", "atom", "baseline_sha256",
            "candidate_sha256", "decision", "selected_candidate_sha256",
            "final_item", "associated_warning", "source_anchors", "rationale",
        }
        require(set(row) == expected_keys, f"conflict-resolution key drift: row {row_number}")
        require(row["schema_version"] == "rq2b-v7-i3-v4.1.2-warning-repair-conflict-resolution-v1", f"conflict-resolution schema drift: row {row_number}")
        binding = row["conflict_docket"]
        require(binding == {"path": rel(AUTHORITATIVE_CONFLICT_DOCKET), "sha256": docket_sha, "row": row_number}, f"conflict-docket binding drift: row {row_number}")
        key = conflict_key(row)
        require(key in docket_by_key and key not in resolved, f"conflict-resolution identity drift: row {row_number}")
        conflict = docket_by_key[key]
        for field in ("batch_id", "source_row_index", "skill_id", "area", "baseline_sha256", "candidate_sha256"):
            require(row[field] == conflict[field], f"conflict-resolution {field} drift: row {row_number}")
        require(row["atom"] == list(ast.literal_eval(conflict["atom"])), f"conflict-resolution atom drift: row {row_number}")
        selected_group = {"SELECT_GROUP_1": 0, "SELECT_GROUP_2": 1}.get(row["decision"])
        require(selected_group is not None, f"unsupported conflict-resolution decision: row {row_number}")
        require(row["selected_candidate_sha256"] == conflict["candidate_sha256"][selected_group], f"selected conflict candidate drift: row {row_number}")
        require(row["final_item"] is not None and canonical_sha(row["final_item"]) == row["selected_candidate_sha256"], f"resolved item hash drift: row {row_number}")
        require(row["final_item"]["id"] == row["atom"][1], f"resolved item id drift: row {row_number}")
        require(isinstance(row["source_anchors"], list) and row["source_anchors"], f"missing resolution anchors: row {row_number}")
        require(isinstance(row["rationale"], str) and row["rationale"].strip(), f"missing resolution rationale: row {row_number}")
        for anchor in row["source_anchors"]:
            path = ROOT / anchor["path"]
            require(path.is_file() and sha(path) == anchor["sha256"], f"resolution anchor binding drift: row {row_number}")
        resolved[key] = row
    require(set(resolved) == set(docket_by_key), "conflict-resolution union drift")
    return resolved, [bind(AUTHORITATIVE_CONFLICT_DOCKET, rows=3), bind(CONFLICT_RESOLUTION_LEDGER, rows=3)]


def apply_field_resolution(row: dict[str, Any], resolution: dict[str, Any]) -> None:
    field, item_id = resolution["atom"]
    require(field in shared.FIELD_KEYS, f"resolved field drift: {field}")
    items = row["fields"][field]
    indexes = [index for index, item in enumerate(items) if item["id"] == item_id]
    require(len(indexes) <= 1, f"resolved item duplicate before apply: {field}/{item_id}")
    item = copy.deepcopy(resolution["final_item"])
    if indexes:
        items[indexes[0]] = item
    else:
        items.append(item)
    warning = resolution["associated_warning"]
    if warning is not None and warning not in row["qa_warnings"]:
        row["qa_warnings"].append(copy.deepcopy(warning))
    row["absent_fields"] = [name for name in shared.FIELD_KEYS if not row["fields"][name]]


@dataclass
class BuildPlan:
    ledger_rows: list[dict[str, Any]]
    repaired: dict[str, bytes]
    report: dict[str, Any]
    conflicts: list[dict[str, Any]]


def build_plan() -> BuildPlan:
    selection = jsonl_rows(SELECTION_LEDGER)
    require(len(selection) == 95, f"expected 95 selected batches, got {len(selection)}")
    require(len({row['batch_id'] for row in selection}) == 95, "duplicate selected batch")
    selection_report = json_obj(SELECTION_REPORT)
    require(selection_report["bindings"]["selection_ledger_sha256"] == sha(SELECTION_LEDGER), "selection-v1 report/ledger hash mismatch")

    warning_final = jsonl_rows(WARNING_LEDGER)
    warning_report = json_obj(WARNING_REPORT)
    require(warning_report["bindings"]["final_ledger_sha256"] == sha(WARNING_LEDGER), "warning-final report/ledger hash mismatch")
    require(warning_report["state"] == "BLOCKED_TRACEABLE_REISSUE_REQUIRED_NEW_SELECTION_AND_WARNING_AUDIT_VERSION", "unexpected warning-final state")
    reissue_by_group = {
        group: {row["issue_id"] for row in warning_final if row["decision"] == "REISSUE_REQUIRED" and row["reviewer_group"] == group}
        for group in (1, 2, 3)
    }
    source_index_by_skill: dict[str, int] = {}
    for row in warning_final:
        previous_index = source_index_by_skill.setdefault(row["skill_id"], row["source_row_index"])
        require(previous_index == row["source_row_index"], f"warning-final source index disagreement: {row['skill_id']}")

    input_bindings = [bind(SELECTION_LEDGER, rows=len(selection)), bind(SELECTION_REPORT), bind(WARNING_LEDGER, rows=len(warning_final)), bind(WARNING_REPORT)]
    input_bindings.extend(verify_amendment())
    conflict_resolutions, conflict_resolution_bindings = load_conflict_resolutions()
    input_bindings.extend(conflict_resolution_bindings)
    group_ledgers: dict[int, list[dict[str, Any]]] = {}
    supplements: dict[int, list[dict[str, Any]]] = {}
    for group in (1, 2, 3):
        ledger = jsonl_rows(GROUP_LEDGER[group])
        require({row["issue_id"] for row in ledger} == reissue_by_group[group], f"group {group} proposal issue coverage mismatch")
        require(all(row.get("reviewer_group", row.get("proposal_group")) == group for row in ledger), f"group {group} identity mismatch")
        group_ledgers[group] = ledger
        input_bindings.extend([bind(GROUP_LEDGER[group], rows=len(ledger)), bind(GROUP_REPORT[group])])
    for group in (1, 2, 3):
        ledger = jsonl_rows(SUPPLEMENT_LEDGER[group])
        require(all(row["issue_id"] in reissue_by_group[group] for row in ledger), f"group {group} supplement has foreign issue")
        require(len({row["issue_id"] for row in ledger}) == len(ledger), f"group {group} supplement duplicates issue")
        supplements[group] = ledger
        input_bindings.extend([bind(SUPPLEMENT_LEDGER[group], rows=len(ledger)), bind(SUPPLEMENT_REPORT[group])])
        report = json_obj(SUPPLEMENT_REPORT[group])
        bound_hash = (
            report.get("supplemental_ledger", {}).get("sha256")
            or report.get("supplemental_ledger_sha256")
            or report.get("ledger_sha256")
            or report.get("bindings", {}).get("supplemental_ledger_sha256")
        )
        require(bound_hash == sha(SUPPLEMENT_LEDGER[group]), f"group {group} supplement report/ledger hash mismatch")
        blocked_issue_ids = {row["issue_id"] for row in group_ledgers[group] if not is_applied(group, row)}
        require({row["issue_id"] for row in ledger} == blocked_issue_ids, f"group {group} supplement/blocked issue coverage mismatch")

    selected_by_batch = {row["batch_id"]: row for row in selection}
    baseline_rows: dict[str, list[dict[str, Any]]] = {}
    baseline_paths: dict[str, Path] = {}
    for batch_id, entry in selected_by_batch.items():
        path = ROOT / entry["selected_output_path"]
        require(sha(path) == entry["selected_output_sha256"], f"selected output hash mismatch: {batch_id}")
        rows = jsonl_rows(path)
        require(len(rows) == entry["row_count"], f"selected row count mismatch: {batch_id}")
        baseline_rows[batch_id] = rows
        baseline_paths[batch_id] = path

    ledgers_by_group_batch: dict[int, dict[str, list[dict[str, Any]]]] = {}
    supplement_by_group_batch: dict[int, dict[str, list[dict[str, Any]]]] = {}
    for group, ledger in group_ledgers.items():
        mapping: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in ledger:
            mapping[row["batch_id"]].append(row)
        ledgers_by_group_batch[group] = mapping
    for group, ledger in supplements.items():
        mapping = defaultdict(list)
        for row in ledger:
            mapping[row["batch_id"]].append(row)
        supplement_by_group_batch[group] = mapping

    candidates: dict[int, dict[str, list[dict[str, Any]]]] = {1: {}, 2: {}, 3: {}}
    applied_issues: dict[tuple[int, str, str], list[str]] = defaultdict(list)
    unresolved: list[dict[str, Any]] = []
    for group in (1, 2, 3):
        for batch_id, ledger_rows in ledgers_by_group_batch[group].items():
            base = baseline_rows[batch_id]
            supplement_rows = supplement_by_group_batch.get(group, {}).get(batch_id, [])
            if supplement_rows:
                paths = {supplement_attempt_path(group, row) for row in supplement_rows}
                hashes = {supplement_attempt_hash(row) for row in supplement_rows}
                require(len(paths) == len(hashes) == 1, f"group {group} supplement batch binding mismatch: {batch_id}")
                candidate_path = paths.pop()
                expected_hash = hashes.pop()
            else:
                candidate_path = proposal_path(group, ledger_rows, batch_id)
                expected_hash = proposal_hash(group, ledger_rows[0])
            require(all(proposal_hash(group, row) == proposal_hash(group, ledger_rows[0]) for row in ledger_rows), f"group {group} base proposal hash disagreement: {batch_id}")
            require(sha(candidate_path) == expected_hash, f"group {group} candidate hash mismatch: {batch_id}")
            candidate = jsonl_rows(candidate_path)
            require(len(candidate) == len(base), f"group {group} candidate row count mismatch: {batch_id}")
            if supplement_rows:
                base_candidate_path = proposal_path(group, ledger_rows, batch_id)
                base_candidate_hash = proposal_hash(group, ledger_rows[0])
                require(sha(base_candidate_path) == base_candidate_hash, f"group {group} base proposal hash mismatch: {batch_id}")
                for row in supplement_rows:
                    if "base_proposal_output" in row:
                        require(row["base_proposal_output"]["path"] == rel(base_candidate_path), f"group {group} supplement base path mismatch: {batch_id}")
                        require(row["base_proposal_output"]["sha256"] == base_candidate_hash, f"group {group} supplement base hash mismatch: {batch_id}")
                    if "base_proposal_path" in row:
                        require(row["base_proposal_path"] == rel(base_candidate_path), f"group {group} supplement base path mismatch: {batch_id}")
                    if "base_proposal_sha256" in row:
                        require(row["base_proposal_sha256"] == base_candidate_hash, f"group {group} supplement base hash mismatch: {batch_id}")
                verify_supplement_delta(
                    group=group, batch_id=batch_id,
                    base_proposal=jsonl_rows(base_candidate_path), attempt=candidate,
                    ledger_rows=supplement_rows,
                )
            validation = validator.validate(batch_id, candidate_path)
            require(validation["status"] == "PASS_I3_V4_1_2_BATCH_VALIDATION", f"group {group} candidate validator failure: {batch_id}")

            authorised_rows = {(row["skill_id"], row["source_row_index"]) for row in ledger_rows if is_applied(group, row)}
            for row in supplement_rows:
                authorised_rows.add((row["skill_id"], row["source_row_index"]))
            actual_rows = set()
            for index, (base_row, candidate_row) in enumerate(zip(base, candidate)):
                require(same_identity(base_row, candidate_row), f"group {group} row order/identity drift: {batch_id}/{index}")
                changed = row_changed_keys(base_row, candidate_row)
                require(changed <= ALLOWED_ROW_MUTABLE_KEYS, f"group {group} unauthorised top-level change: {batch_id}/{index}")
                if changed:
                    actual_rows.add((base_row["skill_id"], index + 1))
            # source_row_index is global, so compare by skill id for batch-local actual rows.
            authorised_skill_ids = {skill_id for skill_id, _ in authorised_rows}
            actual_skill_ids = {skill_id for skill_id, _ in actual_rows}
            require(actual_skill_ids == authorised_skill_ids, f"group {group} changed-row/ledger mismatch: {batch_id}")
            candidates[group][batch_id] = candidate
            supplement_issue_ids = {row["issue_id"] for row in supplement_rows}
            for row in ledger_rows:
                if is_applied(group, row) or row["issue_id"] in supplement_issue_ids:
                    applied_issues[(group, batch_id, row["skill_id"])].append(row["issue_id"])
                else:
                    unresolved.append({"reviewer_group": group, "issue_id": row["issue_id"], "batch_id": batch_id, "skill_id": row["skill_id"], "proposal_status": proposal_status(group, row)})

    merged_by_batch: dict[str, list[dict[str, Any]]] = {}
    conflicts: list[dict[str, Any]] = []
    used_conflict_resolutions: set[tuple[str, int, str, str]] = set()
    for batch_id in sorted(selected_by_batch):
        merged_rows = []
        base_rows = baseline_rows[batch_id]
        for index, base_row in enumerate(base_rows):
            row_candidates = {
                group: candidates[group][batch_id][index]
                for group in (1, 2, 3)
                if batch_id in candidates[group] and candidates[group][batch_id][index] != base_row
            }
            if not row_candidates:
                merged_rows.append(copy.deepcopy(base_row))
                continue
            require(base_row["skill_id"] in source_index_by_skill, f"changed row lacks warning-final source index: {base_row['skill_id']}")
            merged, row_conflicts = merge_row(
                base_row, row_candidates, batch_id=batch_id,
                source_row_index=source_index_by_skill[base_row["skill_id"]],
            )
            unresolved_row_conflicts = []
            for conflict in row_conflicts:
                key = conflict_key(conflict)
                resolution = conflict_resolutions.get(key)
                if resolution is None:
                    unresolved_row_conflicts.append(conflict)
                    continue
                apply_field_resolution(merged, resolution)
                used_conflict_resolutions.add(key)
            merged_rows.append(merged)
            conflicts.extend(unresolved_row_conflicts)
        merged_by_batch[batch_id] = merged_rows

    require(used_conflict_resolutions == set(conflict_resolutions), "unused or missing conflict resolution")

    if conflicts:
        return BuildPlan([], {}, {
            "schema_version": "rq2b-v7-i3-v4.1.2-warning-repair-integration-report-v1",
            "state": "BLOCKED_PATCH_CONFLICTS",
            "formal_execution_ready": False,
            "input_bindings": input_bindings,
            "counts": {"conflicts": len(conflicts), "unresolved_source_only_issues": len(unresolved)},
        }, sorted(conflicts, key=lambda row: (row["batch_id"], row["source_row_index"], row["area"], row["atom"])))

    repaired: dict[str, bytes] = {}
    validations: list[dict[str, Any]] = []
    ledger_out: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(
        prefix="rq2b-i3-v4-1-2-integration-",
        dir=ROOT / "skill_benchmark/cache",
    ) as temp_dir:
        temp = Path(temp_dir)
        for batch_id in sorted(selected_by_batch):
            entry = selected_by_batch[batch_id]
            data = rows_bytes(merged_by_batch[batch_id])
            base_data = baseline_paths[batch_id].read_bytes()
            issue_ids = sorted({issue for (group, batch, _), issues in applied_issues.items() if batch == batch_id for issue in issues})
            groups = sorted({group for (group, batch, _), issues in applied_issues.items() if batch == batch_id and issues})
            if merged_by_batch[batch_id] == baseline_rows[batch_id]:
                selected_path = baseline_paths[batch_id]
                selected_data = base_data
                selection_kind = "UNCHANGED_V1_SELECTION"
            else:
                selected_path = REPAIRED_DIR / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_2.jsonl"
                repaired[batch_id] = data
                selected_data = data
            validation_path = selected_path
            if batch_id in repaired:
                validation_path = temp / f"{batch_id}.jsonl"
                validation_path.write_bytes(data)
                selection_kind = "REPAIRED_V4_1_2_REISSUE"
            validation = validator.validate(batch_id, validation_path)
            validations.append(validation)
            ledger_out.append({
                "schema_version": "rq2b-v7-i3-v4.1.2-output-selection-v2",
                "batch_id": batch_id,
                "input_sha256": entry["input_sha256"],
                "row_count": entry["row_count"],
                "baseline_selected_output_path": entry["selected_output_path"],
                "baseline_selected_output_sha256": entry["selected_output_sha256"],
                "selection_kind": selection_kind,
                "selected_output_path": rel(selected_path),
                "selected_output_sha256": sha_bytes(selected_data),
                "applied_issue_ids": issue_ids,
                "applied_reviewer_groups": groups,
                "validator_status": validation["status"],
            })

    ledger_data = rows_bytes(ledger_out)
    report = {
        "schema_version": "rq2b-v7-i3-v4.1.2-warning-repair-integration-report-v1",
        "state": "PASS_95_BATCHES_REPAIR_INTEGRATED_PENDING_FRESH_WARNING_QA",
        "formal_execution_ready": False,
        "boundary": "Source-only warning repairs only; this package does not authorise selectors, retrieval, metrics, merge, or a quality PASS.",
        "input_bindings": input_bindings,
        "output_bindings": {
            "builder": bind(Path(__file__).resolve()),
            "selection_v2_ledger": {"path": rel(LEDGER_OUT), "sha256": sha_bytes(ledger_data), "rows": len(ledger_out)},
            "repaired_batches": [
                {"batch_id": batch_id, "path": rel(REPAIRED_DIR / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_2.jsonl"), "sha256": sha_bytes(data), "rows": len(merged_by_batch[batch_id])}
                for batch_id, data in sorted(repaired.items())
            ],
        },
        "counts": {
            "batches": len(ledger_out),
            "rows": sum(row["row_count"] for row in ledger_out),
            "repaired_batches": len(repaired),
            "unchanged_batches": len(ledger_out) - len(repaired),
            "integrated_issues": sum(len(row["applied_issue_ids"]) for row in ledger_out),
            "unresolved_source_only_issues": len(unresolved),
            "conflicts": 0,
            "v4_1_2_validator_passes": len(validations),
        },
        "unresolved_source_only_issues": sorted(unresolved, key=lambda row: (row["reviewer_group"], row["issue_id"])),
    }
    return BuildPlan(ledger_out, repaired, report, [])


def write_exclusive(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def conflict_path(conflicts: list[dict[str, Any]]) -> Path:
    fingerprint = sha_bytes(rows_bytes(conflicts))[:16]
    return OUTPUT_DIR / f"conflicts/conflict_docket_{fingerprint}.jsonl"


def materialize(plan: BuildPlan) -> None:
    if plan.conflicts:
        path = conflict_path(plan.conflicts)
        write_exclusive(path, rows_bytes(plan.conflicts))
        raise ValueError(f"integration blocked by {len(plan.conflicts)} conflicts; docket={rel(path)}")
    targets = [LEDGER_OUT, REPORT_OUT] + [REPAIRED_DIR / f"i3v41_output_{batch[-3:]}_repaired_v4_1_2.jsonl" for batch in plan.repaired]
    existing = [rel(path) for path in targets if path.exists()]
    require(not existing, f"refusing to overwrite generated artifacts: {existing}")
    for batch_id, data in sorted(plan.repaired.items()):
        write_exclusive(REPAIRED_DIR / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_2.jsonl", data)
    write_exclusive(LEDGER_OUT, rows_bytes(plan.ledger_rows))
    write_exclusive(REPORT_OUT, report_bytes(plan.report))


def verify() -> dict[str, Any]:
    plan = build_plan()
    require(not plan.conflicts, "cannot verify a conflicted integration")
    require(LEDGER_OUT.read_bytes() == rows_bytes(plan.ledger_rows), "selection-v2 ledger replay mismatch")
    require(REPORT_OUT.read_bytes() == report_bytes(plan.report), "integration report replay mismatch")
    for batch_id, data in plan.repaired.items():
        path = REPAIRED_DIR / f"i3v41_output_{batch_id[-3:]}_repaired_v4_1_2.jsonl"
        require(path.read_bytes() == data, f"repaired output replay mismatch: {batch_id}")
    return {"status": "PASS_EXACT_REPLAY", "batches": 95, "repaired_batches": len(plan.repaired)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true", help="validate and merge in memory without writing integration artifacts")
    mode.add_argument("--verify", action="store_true", help="rebuild in memory and compare every generated artifact")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(), sort_keys=True))
        return
    plan = build_plan()
    if args.preflight:
        print(json.dumps({"status": plan.report["state"], "conflicts": len(plan.conflicts), "repaired_batches": len(plan.repaired)}, sort_keys=True))
        if plan.conflicts:
            raise SystemExit(2)
        return
    materialize(plan)
    print(json.dumps({"status": plan.report["state"], "selection_v2_ledger_sha256": sha(LEDGER_OUT), "report_sha256": sha(REPORT_OUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
