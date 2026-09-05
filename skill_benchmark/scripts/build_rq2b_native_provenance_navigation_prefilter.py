#!/usr/bin/env python3
"""Create a fail-closed provenance-first navigation subset for RQ2 discovery.

The output is only a discovery aid.  It excludes the existing RQ2 union and
Batch 001 hypotheses, but does not admit a source, make a cluster, or create a
prompt or label.  The eligibility check deliberately mirrors Batch 001's local
source pin and declared-licence precondition so Batch 002 does not spend its
bounded semantic-reading budget on sources which cannot enter the library.
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
NAVIGATION = BASE / (
    "manifests/rq2b_native_discovery_universe_live_reconciled_2026-08-31/"
    "rq2_native_source_navigation.jsonl"
)
CURRENT_UNION = BASE / (
    "manifests/current_pre_freeze_consolidated_2026-08-31/"
    "canonical_candidate_union_current_pre_freeze.jsonl"
)
BATCH_001 = BASE / "candidates/rq2_native_supplementary_discovery_batch_001_2026-09-03.jsonl"
PROTOCOL = BASE / "review/USER_AUTHORIZED_SUPPLEMENTARY_RQ2_NATIVE_DISCOVERY_PROTOCOL_2026-09-03.md"
OUTPUT = BASE / (
    "manifests/rq2b_native_discovery_provenance_first_prefilter_2026-09-03/"
    "rq2_native_source_navigation_provenance_first_excluding_current_and_b001.jsonl"
)
SUMMARY = BASE / (
    "manifests/rq2b_native_discovery_provenance_first_prefilter_2026-09-03/"
    "rq2_native_source_navigation_provenance_first_excluding_current_and_b001_summary.json"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def local_provenance_status(source: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Return only locally observable permission/provenance metadata."""
    source_path = Path(str(source["source_path"]))
    import_path = source_path.parent / "IMPORT.json"
    if not import_path.is_file():
        return "BLOCK_NO_LOCAL_IMPORT_PROVENANCE_RECORD", {"import_path": str(import_path)}
    try:
        imported = json.loads(import_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "BLOCK_MALFORMED_LOCAL_IMPORT_PROVENANCE_RECORD", {"import_path": str(import_path)}
    pin = str(imported.get("pinned_commit") or "")
    licence_status = str(imported.get("license_status") or "")
    licence_path = str(imported.get("license_path") or "")
    licence_sha = str(imported.get("license_sha256") or "")
    import_source_sha = str(imported.get("source_sha256") or "")
    eligible = (
        bool(re.fullmatch(r"[0-9a-f]{40}", pin))
        and licence_status == "DECLARED_REPOSITORY_LICENSE"
        and bool(licence_path)
        and bool(re.fullmatch(r"[0-9a-f]{64}", licence_sha))
        and import_source_sha == str(source["source_sha256"])
    )
    return (
        "PASS_LOCAL_PIN_AND_LICENSE_PRECONDITION_PENDING_SEMANTIC_SCREEN"
        if eligible else "BLOCK_LOCAL_PIN_OR_LICENSE_PRECONDITION",
        {
            "import_path": str(import_path),
            "pinned_commit": pin or None,
            "license_status": licence_status or None,
            "license_path": licence_path or None,
            "license_sha256": licence_sha or None,
            "import_source_sha256": import_source_sha or None,
        },
    )


def main() -> int:
    required = [NAVIGATION, CURRENT_UNION, BATCH_001, PROTOCOL]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required inputs: {missing}")

    current_hashes = {str(row["canonical_source_sha256"]) for row in read_jsonl(CURRENT_UNION)}
    if len(current_hashes) != 3094:
        raise SystemExit("Current candidate union is not the fixed 3,094-source checkpoint")
    batch_rows = read_jsonl(BATCH_001)
    batch_hashes = {
        str(candidate["source_sha256"])
        for row in batch_rows if row.get("record_type") == "contrast_family_lead"
        for candidate in row["candidates"]
    }
    if len(batch_hashes) != 75:
        raise SystemExit("Batch 001 source-hash set must contain exactly 75 entries")

    navigation = read_jsonl(NAVIGATION)
    if len(navigation) != 31197:
        raise SystemExit(f"Expected 31,197 active navigation sources, found {len(navigation)}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    out: list[dict[str, Any]] = [{
        "record_type": "prefilter_scope",
        "method": "local source-pin and declared-licence precondition only",
        "input_navigation_source_count": len(navigation),
        "excluded_current_union_source_count": len(current_hashes),
        "excluded_batch_001_hypothesis_source_count": len(batch_hashes),
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "explicit_exclusions": [
            "source admission", "cluster validity", "prompt authoring", "adequacy labels",
            "acceptable sets", "representations", "selectors", "metrics", "thesis results",
        ],
        "claim_boundary": (
            "A PASS record is an auditable source-reading navigation lead only; it is not an admitted RQ2 candidate."
        ),
    }]
    statuses: Counter[str] = Counter()
    origins: Counter[str] = Counter()
    duplicate_hashes: set[str] = set()
    seen_pass_hashes: set[str] = set()
    excluded_counts: Counter[str] = Counter()
    source_byte_failures = 0
    for source in navigation:
        source_hash = str(source["source_sha256"])
        if source_hash in current_hashes:
            excluded_counts["EXCLUDE_ALREADY_IN_CURRENT_UNION"] += 1
            continue
        if source_hash in batch_hashes:
            excluded_counts["EXCLUDE_ALREADY_SCREENED_IN_BATCH_001"] += 1
            continue
        source_path = Path(str(source["source_path"]))
        if not source_path.is_file() or sha256_file(source_path) != source_hash:
            source_byte_failures += 1
            continue
        status, evidence = local_provenance_status(source)
        statuses[status] += 1
        if status != "PASS_LOCAL_PIN_AND_LICENSE_PRECONDITION_PENDING_SEMANTIC_SCREEN":
            continue
        if source_hash in seen_pass_hashes:
            duplicate_hashes.add(source_hash)
            continue
        seen_pass_hashes.add(source_hash)
        origins[str(source["origin_key"])] += 1
        out.append({
            "record_type": "provenance_first_source_reading_lead",
            "source_id": source["source_id"],
            "source_sha256": source_hash,
            "source_path": str(source_path),
            "source_name": source.get("source_name"),
            "source_description": source.get("source_description"),
            "heading_preview": source.get("heading_preview"),
            "origin_key": source.get("origin_key"),
            "source_root": source.get("source_root"),
            "repository_ref": source.get("repository_ref"),
            "source_byte_replay": "PASS_SHA256_MATCH",
            "local_provenance": evidence,
            "status": status,
            "next_gate": (
                "Use only in a new, source-disjoint contrast-family hypothesis; then pass full-source semantic, "
                "cue-safe prompt, target-blind adequacy, and whole-library K=6 gates before admission."
            ),
        })
    if duplicate_hashes:
        raise SystemExit(f"Duplicate passing source hashes require reconciliation: {len(duplicate_hashes)}")
    if source_byte_failures:
        raise SystemExit(f"Source-byte replay failed for {source_byte_failures} navigation entries")
    OUTPUT.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in out),
        encoding="utf-8",
    )
    summary = {
        "status": "PASS_PROVENANCE_FIRST_NAVIGATION_PREFILTER_NOT_A_CANDIDATE_LIBRARY",
        "input_navigation_source_count": len(navigation),
        "excluded_counts": dict(sorted(excluded_counts.items())),
        "local_provenance_status_counts_after_exclusions": dict(sorted(statuses.items())),
        "eligible_source_reading_lead_count": len(seen_pass_hashes),
        "eligible_origin_count": len(origins),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {str(OUTPUT.relative_to(ROOT)): sha256_file(OUTPUT)},
        "claim_boundary": [
            "The 31,197-source navigation frame remains a discovery frame, not the evaluated RQ2 candidate library.",
            "A local provenance PASS does not demonstrate semantic confusability, prompt validity, or label validity.",
            "No existing candidate, Batch 001 lead, source, cluster, prompt, label, representation, selector, or metric is changed by this prefilter.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
