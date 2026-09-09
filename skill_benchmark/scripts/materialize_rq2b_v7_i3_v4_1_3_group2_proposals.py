#!/usr/bin/env python3
"""Materialise the two source-only V4.1.3 group-2 warning proposals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import validate_rq2b_v7_i3_v4_1_2_batch as validator


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_3_warning_repair_proposals_2026_09_09_v1/group_2"
LEDGER = GROUP / "issue_ledger.jsonl"
REPORT = GROUP / "validation_report.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def canonical_jsonl(rows: list[dict]) -> bytes:
    return b"".join((json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode() for row in rows)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    issues = read_jsonl(LEDGER)
    require(len(issues) == 2 and len({row["issue_id"] for row in issues}) == 2, "group-2 issue coverage drift")
    validations = []
    for issue in sorted(issues, key=lambda row: row["batch_id"]):
        source = ROOT / issue["selected_v2_output_path"]
        output = ROOT / issue["proposal_output_path"]
        require(source.is_file() and sha(source) == issue["selected_v2_output_sha256"], f"baseline drift: {issue['batch_id']}")
        require(not output.exists(), f"refusing to overwrite: {output}")
        rows = read_jsonl(source)
        matches = [row for row in rows if row["skill_id"] == issue["skill_id"]]
        require(len(matches) == 1, f"target row mismatch: {issue['issue_id']}")
        target = matches[0]
        before = issue["before_warning"]
        require(target["qa_warnings"].count(before) == 1, f"warning binding drift: {issue['issue_id']}")
        source_text = (ROOT / target["source"]).read_text(encoding="utf-8")
        require(all(anchor in source_text for anchor in issue["source_anchors"]), f"source anchor drift: {issue['issue_id']}")
        index = target["qa_warnings"].index(before)
        after = issue["after_warning"]
        if after is None:
            target["qa_warnings"].pop(index)
        else:
            target["qa_warnings"][index] = after
        data = canonical_jsonl(rows)
        require(hashlib.sha256(data).hexdigest() == issue["proposal_output_sha256"], f"deterministic output drift: {issue['issue_id']}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        result = validator.validate(issue["batch_id"], output)
        require(result["status"] == "PASS_I3_V4_1_2_BATCH_VALIDATION", f"validator failure: {issue['batch_id']}")
        validations.append(result)
    report = {
        "schema_version": "rq2b-v7-i3-v4.1.3-warning-repair-proposal-validation-v1",
        "status": "PASS_PROSPECTIVE_V4_1_3_PROPOSAL_VALIDATION",
        "proposal_only": True,
        "canonical_promotion_authorised": False,
        "counts": {"issues": 2, "affected_batches": 2, "affected_rows": 2, "total_output_rows": 80},
        "checks": {
            "selected_v2_hashes": "PASS",
            "source_anchors_exact_substrings": "PASS",
            "row_identity_and_order": "PASS",
            "extracted_fields_unchanged": "PASS",
            "only_warning_metadata_changed": "PASS",
            "official_v4_1_2_validator": "2/2 PASS",
        },
        "bindings": {
            "issue_ledger": {"path": rel(LEDGER), "sha256": sha(LEDGER), "rows": 2},
            "validator": {"path": rel(Path(validator.__file__).resolve()), "sha256": sha(Path(validator.__file__).resolve())},
            "outputs": [
                {"batch_id": row["batch_id"], "path": row["proposal_output_path"], "sha256": row["proposal_output_sha256"], "rows": 40}
                for row in sorted(issues, key=lambda value: value["batch_id"])
            ],
        },
        "validator_results": validations,
        "boundary": "Source-only proposal materialisation. No canonical selection, selector, label, result, or metric is changed.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": rel(REPORT), "sha256": sha(REPORT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
