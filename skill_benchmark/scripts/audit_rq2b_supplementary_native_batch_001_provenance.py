#!/usr/bin/env python3
"""Fail-closed local provenance preflight for supplementary Batch 001.

This decides only whether a source-reading hypothesis may proceed to full-source
semantic screening.  It is not candidate admission, cluster validation, prompt
authoring, labelling, representation extraction, or a scientific result.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
QUEUE = BASE / "candidates/rq2_native_supplementary_discovery_batch_001_2026-09-03.jsonl"
OUTPUT = BASE / "review/rq2_native_supplementary_batch_001_provenance_preflight_2026-09-03.jsonl"
SUMMARY = BASE / "review/rq2_native_supplementary_batch_001_provenance_preflight_2026-09-03_summary.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def import_preflight(candidate: dict[str, Any]) -> dict[str, Any]:
    source_path = Path(str(candidate["source_path"]))
    import_path = source_path.parent / "IMPORT.json"
    if not import_path.is_file():
        return {
            "source_id": candidate["source_id"],
            "source_sha256": candidate["source_sha256"],
            "import_path": str(import_path),
            "status": "BLOCK_NO_LOCAL_IMPORT_PROVENANCE_RECORD",
            "reason": "No adjacent source/IMPORT.json captures a pinned source and declared repository licence.",
        }
    imported = json.loads(import_path.read_text(encoding="utf-8"))
    pin = str(imported.get("pinned_commit") or "")
    licence_status = str(imported.get("license_status") or "")
    licence_path = str(imported.get("license_path") or "")
    licence_sha = str(imported.get("license_sha256") or "")
    source_hash = str(imported.get("source_sha256") or "")
    source_hash_matches = source_hash == str(candidate["source_sha256"])
    eligible = (
        bool(re.fullmatch(r"[0-9a-f]{40}", pin))
        and licence_status == "DECLARED_REPOSITORY_LICENSE"
        and bool(licence_path)
        and bool(re.fullmatch(r"[0-9a-f]{64}", licence_sha))
        and source_hash_matches
    )
    return {
        "source_id": candidate["source_id"],
        "source_sha256": candidate["source_sha256"],
        "import_path": str(import_path),
        "pinned_commit": pin or None,
        "license_status": licence_status or None,
        "license_path": licence_path or None,
        "license_sha256": licence_sha or None,
        "import_source_sha256": source_hash or None,
        "status": (
            "PASS_LOCAL_PIN_AND_LICENSE_PRECONDITION_PENDING_SEMANTIC_SCREEN"
            if eligible
            else "BLOCK_LOCAL_PIN_OR_LICENSE_PRECONDITION"
        ),
        "reason": (
            "Local import record binds source bytes, a 40-hex commit, and a declared licence file hash."
            if eligible
            else "Pinned commit, licence status/path/hash, or source-hash binding is absent or does not meet the declared precondition."
        ),
    }


def main() -> int:
    if not QUEUE.is_file():
        raise SystemExit(f"Missing source-reading queue: {QUEUE}")
    rows = read_jsonl(QUEUE)
    leads = [row for row in rows if row.get("record_type") == "contrast_family_lead"]
    if len(leads) != 25:
        raise SystemExit(f"Expected 25 contrast-family leads, found {len(leads)}")

    output_rows: list[dict[str, Any]] = [{
        "record_type": "preflight_scope",
        "queue": str(QUEUE.relative_to(ROOT)),
        "queue_sha256": sha256_file(QUEUE),
        "scope": "local source pin and declared licence precondition only",
        "explicit_exclusions": [
            "cluster validity", "prompt authoring", "adequacy labels", "acceptable sets",
            "representation", "selector/reranker", "metrics", "final candidate admission",
        ],
    }]
    source_statuses: Counter[str] = Counter()
    family_statuses: Counter[str] = Counter()
    passing_source_count = 0
    for lead in leads:
        evidence = [import_preflight(candidate) for candidate in lead["candidates"]]
        for row in evidence:
            source_statuses[str(row["status"])] += 1
        eligible = all(
            row["status"] == "PASS_LOCAL_PIN_AND_LICENSE_PRECONDITION_PENDING_SEMANTIC_SCREEN"
            for row in evidence
        )
        family_status = (
            "ADVANCE_TO_FULL_SOURCE_SEMANTIC_SCREEN"
            if eligible
            else "BLOCK_BEFORE_SEMANTIC_SCREEN_INCOMPLETE_PROVENANCE_OR_LICENSE"
        )
        family_statuses[family_status] += 1
        passing_source_count += sum(
            row["status"] == "PASS_LOCAL_PIN_AND_LICENSE_PRECONDITION_PENDING_SEMANTIC_SCREEN"
            for row in evidence
        )
        output_rows.append({
            "record_type": "family_preflight",
            "family_id": lead["family_id"],
            "source_ids": lead["source_ids"],
            "source_preflight": evidence,
            "family_status": family_status,
            "next_gate": (
                "Read all three preserved sources and test bounded common envelope plus pairwise operational contrast."
                if eligible
                else "Retain as a blocked lead; do not read as an admission candidate or repair missing provenance/licence by assumption."
            ),
            "claim_boundary": "Passing this preflight is not source admission, cluster validity, a prompt, a label, or a result.",
        })

    write_jsonl(OUTPUT, output_rows)
    summary = {
        "status": "PASS_BATCH_001_PROVENANCE_PREFLIGHT_NOT_A_CLUSTER_OR_ADMISSION",
        "family_count": len(leads),
        "source_appearance_count": sum(len(lead["candidates"]) for lead in leads),
        "source_preflight_status_counts": dict(sorted(source_statuses.items())),
        "source_pass_count": passing_source_count,
        "family_status_counts": dict(sorted(family_statuses.items())),
        "advance_family_ids": [
            row["family_id"] for row in output_rows
            if row.get("family_status") == "ADVANCE_TO_FULL_SOURCE_SEMANTIC_SCREEN"
        ],
        "input_sha256": {str(QUEUE.relative_to(ROOT)): sha256_file(QUEUE)},
        "artifacts": {str(OUTPUT.relative_to(ROOT)): sha256_file(OUTPUT)},
        "claim_boundary": [
            "A navigation manifest's empty licence field does not override an adjacent captured import record.",
            "A blocked source has no inferred permission, candidate admission, or adequacy label.",
            "An advanced family still needs full-source semantic screening, cluster and prompt gates, target-blinded review, and whole-library K=6 adjudication.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
