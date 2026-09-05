#!/usr/bin/env python3
"""Build a source-free approval packet for the V3 repaired-output final merge."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, repo_root, require, sha256_file, write_json_new


VERSION_ID = "rq2b-i3c-v3-2026-08-18"
V3_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
V12_ROOT = "skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16"
ORIGINAL_PACKET = f"{V3_ROOT}/source_assignment_approval_packet_sealed.json"
ORIGINAL_RECEIPT = f"{V3_ROOT}/source_assignment_approval_receipt.json"
EXTRACTION_MANIFEST = f"{V3_ROOT}/i3c_extraction/manifest.json"
SOURCE_MANIFEST = f"{V12_ROOT}/source_manifest.jsonl"
MERGER = "skill_benchmark/scripts/merge_rq2b_i3c_v3_final.py"
OUTPUT = f"{V3_ROOT}/finalisation_approval_packet.json"


def current_worker_rows(root: Path, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for chunk in chunks:
        input_path = root / chunk["input_path"]
        output_path = root / chunk["expected_output_path"]
        require(input_path.is_file() and output_path.is_file(), f"missing worker artifact: {chunk['chunk_index']}")
        require(sha256_file(input_path) == chunk["planned_input_sha256"], f"input hash drift: {chunk['chunk_index']}")
        inputs = read_jsonl(input_path)
        outputs = read_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["row_count"], f"worker row count drift: {chunk['chunk_index']}")
        for input_row, output_row in zip(inputs, outputs, strict=True):
            for key in ("skill_id", "name", "description", "family", "source"):
                require(output_row.get(key) == input_row[key], f"worker identity drift: {chunk['chunk_index']}:{key}")
            rows.append(output_row)
    require(len(rows) == 2433 and len({row["skill_id"] for row in rows}) == 2433, "worker corpus identity drift")
    return rows


def root_coverage(root: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    sources = read_jsonl(root / SOURCE_MANIFEST)
    source_by_id = {row["skill_id"]: row for row in sources}
    require(len(sources) == len(source_by_id) == len(rows) == 2433, "source inventory drift")
    fieldless: list[str] = []
    use_when_fieldless: list[str] = []
    for row in rows:
        source = source_by_id[row["skill_id"]]
        description = str(source.get("source_description") or "").strip()
        if source["source_policy"] != "public_original" or not description:
            continue
        if not any(row["fields"].values()):
            fieldless.append(row["skill_id"])
            if "use when" in description.lower():
                use_when_fieldless.append(row["skill_id"])
    public_descriptions = [row for row in sources if row["source_policy"] == "public_original" and str(row.get("source_description") or "").strip()]
    public_use_when = [row for row in public_descriptions if "use when" in str(row["source_description"]).lower()]
    return {
        "public_original_nonempty_description_rows": len(public_descriptions),
        "public_original_description_contains_use_when_rows": len(public_use_when),
        "fieldless_nonempty_public_description_rows": len(fieldless),
        "fieldless_public_description_contains_use_when_rows": len(use_when_fieldless),
        "fieldless_skill_ids": fieldless,
    }


def exact_source_duplicate_groups(root: Path) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in read_jsonl(root / SOURCE_MANIFEST):
        groups[row["source_sha256"]].append(row["skill_id"])
    return [
        {"source_sha256": digest, "skill_ids": sorted(skill_ids)}
        for digest, skill_ids in sorted(groups.items())
        if len(skill_ids) > 1
    ]


def build(root: Path) -> dict[str, Any]:
    output = root / OUTPUT
    require(not output.exists(), "refusing to overwrite finalisation packet")
    original_packet = read_json(root / ORIGINAL_PACKET)
    original_receipt = read_json(root / ORIGINAL_RECEIPT)
    extraction = read_json(root / EXTRACTION_MANIFEST)
    require(original_receipt.get("state") == "explicitly_approved_for_v3_i3c_source_assignment_once", "V3 source assignment is not approved")
    require(original_receipt["approved_packet"]["sha256"] == sha256_file(root / ORIGINAL_PACKET), "V3 source packet receipt drift")
    require(extraction["counts"]["input_rows"] == 2433 and len(original_packet["chunks"]) == 57, "V3 extraction plan drift")
    rows = current_worker_rows(root, original_packet["chunks"])
    coverage = root_coverage(root, rows)
    require(coverage["fieldless_nonempty_public_description_rows"] == 0, "V3 root coverage remains incomplete")
    require(coverage["fieldless_public_description_contains_use_when_rows"] == 0, "V3 use-when root coverage remains incomplete")
    packet = {
        "schema_version": "rq2b-i3c-v3-finalisation-approval-packet-v1",
        "version_id": VERSION_ID,
        "state": "awaiting_explicit_finalisation_approval",
        "packet_contains_source_text": False,
        "purpose": "Bind the repaired V3 worker outputs to one immutable local final merge before calibrated blinded QA packaging.",
        "basis": {
            "source_assignment_packet": {"path": ORIGINAL_PACKET, "sha256": sha256_file(root / ORIGINAL_PACKET)},
            "source_assignment_receipt": {"path": ORIGINAL_RECEIPT, "sha256": sha256_file(root / ORIGINAL_RECEIPT)},
            "source_manifest": {"path": SOURCE_MANIFEST, "sha256": sha256_file(root / SOURCE_MANIFEST), "rows": 2433},
            "initial_merge_retained_as_stale_audit_artifact": {
                "path": f"{V3_ROOT}/i3c_merged/manifest.json",
                "sha256": sha256_file(root / V3_ROOT / "i3c_merged" / "manifest.json"),
                "reason": "chunk 49 was re-extracted after the initial merge's root-coverage check",
            },
        },
        "implementation": {"merger": MERGER, "merger_sha256": sha256_file(root / MERGER)},
        "worker_outputs": [
            {
                "chunk_index": chunk["chunk_index"],
                "input_path": chunk["input_path"],
                "input_sha256": chunk["planned_input_sha256"],
                "output_path": chunk["expected_output_path"],
                "output_sha256": sha256_file(root / chunk["expected_output_path"]),
                "rows": chunk["row_count"],
            }
            for chunk in original_packet["chunks"]
        ],
        "root_coverage": coverage,
        "exact_source_duplicate_groups": exact_source_duplicate_groups(root),
        "authorises_if_approved": [
            "run the bound local final merger once into a new immutable V3 final-artifact location",
            "re-check JSONL, row count, identity, exact evidence, heading-only, duplicate-ID, missing-ID, root coverage, and selector-text duplicate observations",
            "write only merge, root-coverage, and completion-checkpoint artifacts",
        ],
        "does_not_authorise": [
            "any new source assignment or worker extraction",
            "manual QA completion or reviewer assignment",
            "network, external API, provider, or hosted compute use",
            "BM25, embedding, reranking, retrieval, or thesis-result writing",
        ],
        "network_calls": 0,
        "external_api_calls": 0,
    }
    write_json_new(output, packet)
    return packet


def main() -> int:
    print(json.dumps(build(repo_root()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
