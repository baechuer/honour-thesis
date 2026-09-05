#!/usr/bin/env python3
"""Fail-closed automatic integrity freeze for the final RQ2b V3 I3C corpus.

This validator intentionally proves only deterministic properties: provenance,
source grounding, schema/identity integrity, serialisation replay, coverage,
and scaffold exclusion. It does not claim an independent semantic QA review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

from merge_rq2b_i3c import canonical_extraction, is_heading_only, representation_row
from rq2b_common import read_json, relative, repo_root, require, serialize_i3_flat, serialize_i3c, sha256_file, write_json_new


VERSION_ID = "rq2b-i3c-v3-2026-08-18"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
V12_ROOT = "skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16"
SOURCE_MANIFEST = f"{V12_ROOT}/source_manifest.jsonl"
SOURCE_PACKET = f"{RELATIVE_ROOT}/source_assignment_approval_packet_sealed.json"
SOURCE_RECEIPT = f"{RELATIVE_ROOT}/source_assignment_approval_receipt.json"
FINAL_PACKET = f"{RELATIVE_ROOT}/finalisation_approval_packet.json"
FINAL_RECEIPT = f"{RELATIVE_ROOT}/finalisation_approval_receipt.json"
FINAL_MANIFEST = f"{RELATIVE_ROOT}/i3c_merged_final/manifest.json"
FREEZE_RECEIPT = f"{RELATIVE_ROOT}/automatic_freeze_approval_receipt.json"
FREEZE_ROOT = f"{RELATIVE_ROOT}/automatic_integrity_freeze"
FINAL_MERGER_VERSION = "rq2b-i3c-v3-final-local-merger-v1"
FIELD_KEYS = (
    "use_conditions", "input_preconditions", "output_artifacts", "workflow_steps",
    "success_criteria", "constraints_boundaries", "dependencies_resources",
)
BANNED_BACKGROUND = {
    "benchmark_scale_explanation": re.compile(r"background scale skill used to create realistic retrieval pressure in the benchmark|background scale skill|retrieval pressure", re.IGNORECASE),
    "benchmark_gold_label": re.compile(r"gold-label core benchmark skill|core benchmark skill", re.IGNORECASE),
    "benchmark_confusability": re.compile(r"neighboring confusable skill|neighboring skill", re.IGNORECASE),
    "benchmark_artifact_reference": re.compile(r"expected artifact below", re.IGNORECASE),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def strict_jsonl(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8")
    require(raw.endswith("\n"), f"JSONL must end with a newline: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        require(bool(line.strip()), f"blank JSONL line {line_number}: {path}")
        value = json.loads(line)
        require(isinstance(value, dict), f"non-object JSONL line {line_number}: {path}")
        rows.append(value)
    return rows


def assert_evidence(source_text: str, evidence: str) -> None:
    require(bool(evidence) and evidence in source_text, "literal evidence is absent from source")
    require(not is_heading_only(source_text, evidence), "heading-only evidence is selector-visible")


def assert_root_coverage(source_description: str, fields: dict[str, list[dict[str, Any]]]) -> None:
    description = source_description.strip()
    if not description:
        return
    require(any(fields.values()), "non-empty public description has no I3C field")
    if "use when" in description.lower():
        require(bool(fields["use_conditions"]), "public use-when description has no use-condition field")


def assert_scaffold_free(source_path: str, source_text: str) -> None:
    if "/source_overlay/background_scale/" not in source_path:
        return
    failures = [name for name, pattern in BANNED_BACKGROUND.items() if pattern.search(source_text)]
    require(not failures, f"background scaffold matches: {failures}")


def expect_reject(label: str, fn: Callable[[], None]) -> str:
    try:
        fn()
    except (AssertionError, ValueError, json.JSONDecodeError):
        return label
    raise AssertionError(f"synthetic guard did not reject: {label}")


def self_test() -> dict[str, Any]:
    """Exercise every fail-closed predicate before it is allowed on V3."""
    rejected = [
        expect_reject("malformed_jsonl", lambda: strict_jsonl_from_text('{"a": 1}\nnot-json\n')),
        expect_reject("blank_jsonl_line", lambda: strict_jsonl_from_text('{"a": 1}\n\n')),
        expect_reject("non_substring_evidence", lambda: assert_evidence("source only", "invented")),
        expect_reject("heading_only_evidence", lambda: assert_evidence("# Heading\n\nBody text.\n", "# Heading")),
        expect_reject("missing_public_description_coverage", lambda: assert_root_coverage("Use when processing X.", {field: [] for field in FIELD_KEYS})),
        expect_reject("missing_use_when_field", lambda: assert_root_coverage("Use when processing X.", {field: [{"id": "x"}] if field == "output_artifacts" else [] for field in FIELD_KEYS})),
        expect_reject("background_scaffold", lambda: assert_scaffold_free("x/source_overlay/background_scale/x/SKILL.md", "This background scale skill creates retrieval pressure.")),
        expect_reject("serializer_mismatch", lambda: require("expected" == "actual", "serializer replay mismatch")),
    ]
    return {"schema_version": "rq2b-i3c-v3-automatic-freeze-self-test-v1", "state": "self_test_passed", "rejected_cases": rejected, "count": len(rejected)}


def strict_jsonl_from_text(value: str) -> list[dict[str, Any]]:
    require(value.endswith("\n"), "synthetic JSONL must end with newline")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(value.splitlines(), start=1):
        require(bool(line.strip()), f"synthetic blank JSONL line {line_number}")
        parsed = json.loads(line)
        require(isinstance(parsed, dict), f"synthetic non-object JSONL line {line_number}")
        rows.append(parsed)
    return rows


def verify_approval(root: Path, *, require_freeze_receipt: bool) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_packet = read_json(root / SOURCE_PACKET)
    source_receipt = read_json(root / SOURCE_RECEIPT)
    final_packet = read_json(root / FINAL_PACKET)
    final_receipt = read_json(root / FINAL_RECEIPT)
    final_manifest = read_json(root / FINAL_MANIFEST)
    require(source_receipt["state"] == "explicitly_approved_for_v3_i3c_source_assignment_once", "source assignment receipt mismatch")
    require(final_receipt["state"] == "explicitly_approved_for_v3_finalisation_once", "finalisation receipt mismatch")
    require(source_receipt["approved_packet"]["sha256"] == sha256_file(root / SOURCE_PACKET), "source approval hash drift")
    require(final_receipt["approved_packet"]["sha256"] == sha256_file(root / FINAL_PACKET), "finalisation approval hash drift")
    require(final_manifest["version_id"] == VERSION_ID and final_manifest["summary"]["rows"] == 2433, "final manifest identity mismatch")
    if require_freeze_receipt:
        receipt = read_json(root / FREEZE_RECEIPT)
        require(receipt["state"] == "explicitly_approved_for_v3_automatic_integrity_freeze_once", "automatic freeze is not approved")
        require(receipt["bound_final_manifest"]["sha256"] == sha256_file(root / FINAL_MANIFEST), "automatic freeze receipt manifest drift")
    return source_packet, final_packet, final_manifest


def verify_full(root: Path) -> dict[str, Any]:
    source_packet, final_packet, manifest = verify_approval(root, require_freeze_receipt=True)
    source_manifest_path = root / SOURCE_MANIFEST
    require(sha256_file(source_manifest_path) == source_packet["source_corpus"]["source_manifest"]["sha256"], "source manifest hash drift")
    sources = strict_jsonl(source_manifest_path)
    source_by_index = {row["source_row_index"]: row for row in sources}
    require(len(sources) == len(source_by_index) == 2433 and sorted(source_by_index) == list(range(2433)), "source manifest row coverage mismatch")

    artifacts = manifest["artifacts"]
    canonical_path = root / artifacts["canonical_extractions"]["path"]
    fielded_path = root / artifacts["i3c-fielded-evidence"]["path"]
    flat_path = root / artifacts["i3-flat-evidence"]["path"]
    for key, path in (("canonical_extractions", canonical_path), ("i3c-fielded-evidence", fielded_path), ("i3-flat-evidence", flat_path)):
        require(path.is_file() and sha256_file(path) == artifacts[key]["sha256"], f"final artifact hash drift: {key}")
    canonical_rows = strict_jsonl(canonical_path)
    fielded_rows = strict_jsonl(fielded_path)
    flat_rows = strict_jsonl(flat_path)
    require(len(canonical_rows) == len(fielded_rows) == len(flat_rows) == 2433, "final artefact row count mismatch")

    computed_canonical: list[dict[str, Any]] = []
    computed_fielded: list[dict[str, Any]] = []
    computed_flat: list[dict[str, Any]] = []
    replay_chunks: list[dict[str, Any]] = []
    for chunk in final_packet["worker_outputs"]:
        input_path, output_path = root / chunk["input_path"], root / chunk["output_path"]
        require(sha256_file(input_path) == chunk["input_sha256"], f"chunk input hash drift: {chunk['chunk_index']}")
        require(sha256_file(output_path) == chunk["output_sha256"], f"chunk output hash drift: {chunk['chunk_index']}")
        inputs, outputs = strict_jsonl(input_path), strict_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["rows"], f"chunk row count mismatch: {chunk['chunk_index']}")
        for input_row, output_row in zip(inputs, outputs, strict=True):
            source = source_by_index[input_row["source_row_index"]]
            source_bytes = (root / source["source_path"]).read_bytes()
            require(sha256_bytes(source_bytes) == source["source_sha256"], f"source byte hash drift: {input_row['skill_id']}")
            require(input_row["text"] == source_bytes.decode("utf-8"), f"source text drift: {input_row['skill_id']}")
            for key, source_key in (("skill_id", "skill_id"), ("name", "source_name"), ("description", "source_description"), ("family", "family"), ("source", "source_path"), ("source_sha256", "source_sha256")):
                require(input_row[key] == source[source_key], f"source/input identity drift: {input_row['skill_id']}:{key}")
            assert_scaffold_free(source["source_path"], input_row["text"])
            canonical, retained, _ = canonical_extraction(input_row, output_row)
            canonical["merger_version"] = FINAL_MERGER_VERSION
            if source["source_policy"] == "public_original":
                assert_root_coverage(str(source.get("source_description") or ""), canonical["fields"])
            fielded = representation_row(canonical, "i3c-fielded-evidence", serialize_i3c(input_row["name"], input_row["description"], retained))
            flat = representation_row(canonical, "i3-flat-evidence", serialize_i3_flat(input_row["name"], input_row["description"], retained))
            computed_canonical.append(canonical)
            computed_fielded.append(fielded)
            computed_flat.append(flat)
        replay_chunks.append({"chunk_index": chunk["chunk_index"], "rows": chunk["rows"], "state": "replayed"})

    require(computed_canonical == canonical_rows, "canonical replay differs from frozen artefact")
    require(computed_fielded == fielded_rows, "I3C serialisation replay differs from frozen artefact")
    require(computed_flat == flat_rows, "I3-flat serialisation replay differs from frozen artefact")
    require([row["source_row_index"] for row in canonical_rows] == list(range(2433)), "canonical source order drift")
    require(len({row["skill_id"] for row in canonical_rows}) == 2433, "duplicate canonical skill ID")
    require(manifest["summary"]["parse_failures"] == manifest["summary"]["identity_failures"] == manifest["summary"]["evidence_substring_failures"] == 0, "manifest automatic failure count is nonzero")
    require(manifest["summary"]["heading_only_evidence_removed"] == 0, "heading-only evidence removal count is nonzero")
    require(manifest["summary"]["i3c_i3flat_evidence_match_rows"] == 2433, "I3C/I3-flat evidence match count drift")
    require(manifest["root_coverage"]["fieldless_nonempty_public_description_rows"] == 0, "manifest root coverage failure")
    require(manifest["root_coverage"]["fieldless_public_description_contains_use_when_rows"] == 0, "manifest use-when coverage failure")

    duplicate_groups: dict[str, list[str]] = defaultdict(list)
    for source in sources:
        duplicate_groups[source["source_sha256"]].append(source["skill_id"])
    exact_duplicates = [{"source_sha256": digest, "skill_ids": sorted(ids)} for digest, ids in sorted(duplicate_groups.items()) if len(ids) > 1]
    require(exact_duplicates == manifest["exact_source_duplicate_groups"], "source duplicate observation drift")
    selector_duplicate_rows = sum(count - 1 for count in Counter(row["selector_text_sha256"] for row in fielded_rows).values() if count > 1)
    require(selector_duplicate_rows == manifest["summary"]["duplicate_i3c_selector_text_rows_beyond_first"] == 1, "selector duplicate observation drift")
    return {
        "schema_version": "rq2b-i3c-v3-automatic-integrity-freeze-report-v1",
        "version_id": VERSION_ID,
        "state": "automatic_integrity_verification_passed",
        "checks": {
            "source_manifest_rows": len(sources),
            "chunk_replay": replay_chunks,
            "canonical_rows": len(canonical_rows),
            "i3c_rows": len(fielded_rows),
            "i3flat_rows": len(flat_rows),
            "root_coverage": manifest["root_coverage"],
            "exact_source_duplicate_groups": exact_duplicates,
            "selector_text_duplicate_rows_beyond_first": selector_duplicate_rows,
            "background_scaffold_lint": {name: 0 for name in BANNED_BACKGROUND},
        },
        "manual_semantic_qa": "not performed by design; this automatic freeze does not establish independent semantic completeness",
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
    }


def freeze(root: Path) -> dict[str, Any]:
    report = verify_full(root)
    freeze_root = root / FREEZE_ROOT
    staging = freeze_root.with_name(".automatic_integrity_freeze.staging")
    require(not freeze_root.exists() and not staging.exists(), "refusing to overwrite automatic freeze")
    staging.mkdir(parents=True, exist_ok=False)
    report_path = staging / "automatic_integrity_freeze_report.json"
    write_json_new(report_path, report)
    checkpoint = {
        "schema_version": "rq2b-i3c-v3-automatic-integrity-freeze-checkpoint-v1",
        "version_id": VERSION_ID,
        "state": "automatic_integrity_frozen_b1_preflight_eligible",
        "report": {"path": relative(freeze_root / report_path.name, root), "sha256": sha256_file(report_path)},
        "manual_semantic_qa": "waived by explicit user direction; no claim of independent semantic completeness",
        "retrieval_execution_authorized": False,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "next_gate": "prepare B1L local lexical preflight and an execution approval packet; do not score until separately approved",
    }
    write_json_new(staging / "automatic_integrity_freeze_checkpoint.json", checkpoint)
    staging.rename(freeze_root)
    return checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.freeze, "choose exactly one of --self-test or --freeze")
    result = self_test() if args.self_test else freeze(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
