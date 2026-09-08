#!/usr/bin/env python3
"""Traceably promote validated C2 micro-reissues without overwriting raw evidence."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_c2_targeted_reissue_2026_09_08_v1"
ACTIVE = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-2026-09-08-v1" / "coordinator_2"
REISSUE = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-c2-targeted-reissue-2026-09-08-v1" / "coordinator_2_microreissue"
ARCHIVE = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-rationale-duplicate-replaced-2026-09-08-v1" / "coordinator_2"
PROMOTION = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_c2_targeted_reissue_promotion_2026_09_08_v1"
VERIFY = WORKSPACE / "skill_benchmark" / "scripts" / "verify_rq2b_nc_phase5_v7_c2_rationale_targeted_reissue.py"


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    ledger = load_jsonl(DISPATCH / "sealed_admin_reissue_selection_ledger.jsonl")
    if len(ledger) != 18 or len({row["coordinator_dispatch_id"] for row in ledger}) != 18:
        raise SystemExit("targeted selection ledger identity/cardinality drift")
    validation = subprocess.run(
        [sys.executable, str(VERIFY), "--dispatch", str(DISPATCH), "--return-root", str(REISSUE)],
        cwd=WORKSPACE, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if validation.returncode:
        raise SystemExit(f"microreissue validation failed:\n{validation.stdout}\n{validation.stderr}")
    validation_result = json.loads(validation.stdout)
    if validation_result["status"] != "PASS_V7_C2_TARGETED_RATIONALE_REISSUE_COMPLETE":
        raise SystemExit(f"unexpected microreissue status: {validation_result['status']}")
    for row in ledger:
        dispatch_id = row["coordinator_dispatch_id"]
        old_path = ACTIVE / f"{dispatch_id}.json"
        new_path = REISSUE / f"{dispatch_id}.json"
        if not old_path.is_file() or sha_path(old_path) != row["prior_active_return_sha256"]:
            raise SystemExit(f"old active return drift: {dispatch_id}")
        if not new_path.is_file():
            raise SystemExit(f"missing validated microreissue return: {dispatch_id}")
    if ARCHIVE.exists() or PROMOTION.exists():
        raise SystemExit("refusing to overwrite archive or promotion record")

    ARCHIVE.mkdir(parents=True)
    for row in ledger:
        dispatch_id = row["coordinator_dispatch_id"]
        old_path = ACTIVE / f"{dispatch_id}.json"
        archive_path = ARCHIVE / old_path.name
        if archive_path.exists():
            raise SystemExit(f"archive collision: {archive_path}")
        shutil.move(str(old_path), str(archive_path))
        if sha_path(archive_path) != row["prior_active_return_sha256"]:
            raise SystemExit(f"archive hash drift after move: {dispatch_id}")
        new_path = REISSUE / f"{dispatch_id}.json"
        active_path = ACTIVE / new_path.name
        if active_path.exists():
            raise SystemExit(f"active collision after archive move: {active_path}")
        shutil.copy2(new_path, active_path)
        if sha_path(active_path) != sha_path(new_path):
            raise SystemExit(f"selected reissue copy hash drift: {dispatch_id}")

    ARCHIVE.parent.joinpath("README.md").write_text(
        "# Coordinator-2 duplicate-rationale replacements\n\n"
        "This archive preserves exactly 18 raw coordinator-2 returns that were schema-valid but failed the targeted exact-duplicate-rationale quality check across distinct prompt/source inputs. They are unselected; each replacement is traceable in the promotion manifest. No raw return was overwritten.\n",
        encoding="utf-8",
    )
    selection_rows: list[dict[str, Any]] = []
    for row in ledger:
        dispatch_id = row["coordinator_dispatch_id"]
        raw_reissue = REISSUE / f"{dispatch_id}.json"
        selected_active = ACTIVE / f"{dispatch_id}.json"
        selection_rows.append({
            **row,
            "archived_prior_return_path": str((ARCHIVE / f"{dispatch_id}.json").relative_to(WORKSPACE)),
            "raw_reissue_return_path": str(raw_reissue.relative_to(WORKSPACE)),
            "raw_reissue_return_sha256": sha_path(raw_reissue),
            "selected_active_return_path": str(selected_active.relative_to(WORKSPACE)),
            "selected_active_return_sha256": sha_path(selected_active),
            "selection_status": "ACTIVE_REISSUE_SELECTED_PRIOR_RAW_RETURN_PRESERVED_UNSELECTED",
        })
    PROMOTION.mkdir(parents=True)
    (PROMOTION / "selection_ledger.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in selection_rows), encoding="utf-8"
    )
    report = {
        "schema_version": "rq2b_nc_phase5_v7_c2_targeted_reissue_promotion_v1",
        "status": "PASS_C2_TARGETED_REISSUE_PROMOTED_WITH_RAW_PRESERVATION",
        "claim_boundary": "Selection and raw-evidence preservation only; no target join, acceptable set, library update, retrieval result, metric, or thesis result update.",
        "counts": {"replaced_active_returns": len(selection_rows), "preserved_unselected_prior_returns": len(selection_rows)},
        "validation": validation_result,
        "paths": {
            "sealed_dispatch": str(DISPATCH.relative_to(WORKSPACE)),
            "raw_microreissue_returns": str(REISSUE.relative_to(WORKSPACE)),
            "prior_raw_return_archive": str(ARCHIVE.relative_to(WORKSPACE)),
            "selected_active_returns": str(ACTIVE.relative_to(WORKSPACE)),
        },
    }
    (PROMOTION / "integrity_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (PROMOTION / "README.md").write_text(
        "# C2 targeted rationale reissue promotion\n\n"
        "The `selection_ledger.jsonl` binds each of the 18 replaced active paths to its unchanged archived prior raw return and its validated raw microreissue return. The selected active copy is byte-identical to the raw microreissue. This is not a target join, acceptable set, library update, or retrieval result.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "replaced": len(selection_rows), "promotion": str(PROMOTION)}, sort_keys=True))


if __name__ == "__main__":
    main()
