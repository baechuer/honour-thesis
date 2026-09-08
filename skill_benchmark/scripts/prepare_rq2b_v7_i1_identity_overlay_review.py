#!/usr/bin/env python3
"""Prepare/replay two independent source-only reviews of malformed V7 I1 descriptions."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_rq2b_preflight import parse_frontmatter
from prepare_rq2b_v7_first_matrix import safe_path


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
SOURCE_PACKAGE = PREP / "v7_first_matrix_2026_09_08_v1"
FAILED_QA = PREP / "v7_phase7_i3_blinded_qa_final_2026_09_09_v2"
I1_I2 = PREP / "v7_phase7_i1_i2_2026_09_08_v1"
OUTPUT = PREP / "v7_phase7_i1_identity_overlay_review_2026_09_09_v1"
CACHE = Path("skill_benchmark/cache/rq2b_v7_i1_identity_overlay_review_2026_09_09_v1")
INSTRUCTION = Path("skill_benchmark/extraction_prompts/I1_IDENTITY_OVERLAY_REVIEW_V1.md")
INVALID_EXACT = {">", "|"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def jsonl_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def invalid_description(value: str) -> bool:
    description = value.strip()
    return description in INVALID_EXACT or description.endswith(" >") or description.endswith(" |")


def build() -> tuple[dict[str, bytes], dict[str, bytes]]:
    source_manifest_bytes = (ROOT / SOURCE_PACKAGE / "source_manifest.jsonl").read_bytes()
    sources = rows(ROOT / SOURCE_PACKAGE / "source_manifest.jsonl")
    if len(sources) != 3798:
        raise ValueError("V7 source count mismatch")
    qa = json.loads((ROOT / FAILED_QA / "qa_final_report.json").read_bytes())
    if qa.get("state") != "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE":
        raise ValueError("identity overlay must be prospective from frozen failed QA")
    old_i1 = json.loads((ROOT / I1_I2 / "mechanical_report.json").read_bytes())
    if old_i1.get("counts", {}).get("i1_rows") != 3798:
        raise ValueError("old I1 package mismatch")

    candidates: list[dict] = []
    inputs: list[dict] = []
    for source_row_index, source in enumerate(sources):
        raw = safe_path(ROOT, source["path"]).read_bytes()
        if sha(raw) != source["sha256"] or len(raw) != source["bytes"]:
            raise ValueError(f"source drift: {source['path']}")
        text = raw.decode("utf-8")
        native = parse_frontmatter(text)
        description = native.get("description", "").strip()
        if not invalid_description(description):
            continue
        skill_id = "sha256-" + source["sha256"]
        review_id = "V7-I1-ID-" + sha((skill_id + "|overlay-review-v1").encode())[:16].upper()
        kind = "ORPHAN_BLOCK_MARKER_WITH_PREFIX" if description.endswith((" >", " |")) else "LITERAL_BLOCK_MARKER"
        candidates.append({
            "review_id": review_id,
            "skill_id": skill_id,
            "source_row_index": source_row_index,
            "source_path": source["path"],
            "source_sha256": source["sha256"],
            "parsed_name": native.get("name", "").strip(),
            "malformed_parsed_description": description,
            "malformation_class": kind,
            "required_reviewer_lanes": ["A", "B"],
            "state": "PENDING_TWO_INDEPENDENT_SOURCE_ONLY_RETURNS",
        })
        inputs.append({
            "review_id": review_id,
            "skill_id": skill_id,
            "source_row_index": source_row_index,
            "source_path": source["path"],
            "source_sha256": source["sha256"],
            "parsed_name": native.get("name", "").strip(),
            "malformed_parsed_description": description,
            "malformation_class": kind,
            "source_text": text,
        })
    if len(candidates) != 39:
        raise ValueError(f"expected 39 malformed descriptions, got {len(candidates)}")
    if sum(row["malformation_class"] == "ORPHAN_BLOCK_MARKER_WITH_PREFIX" for row in candidates) != 17:
        raise ValueError("orphan block-marker count mismatch")
    if sum(row["malformation_class"] == "LITERAL_BLOCK_MARKER" for row in candidates) != 22:
        raise ValueError("literal block-marker count mismatch")

    payloads = {
        "review_input_lane_a.jsonl": jsonl_bytes(inputs),
        "review_input_lane_b.jsonl": jsonl_bytes(inputs),
    }
    files = {"candidate_manifest.jsonl": jsonl_bytes(candidates)}
    report = {
        "schema_version": "rq2b-v7-i1-identity-overlay-review-preparation-v1",
        "state": "PENDING_TWO_INDEPENDENT_SOURCE_ONLY_IDENTITY_REVIEWS",
        "formal_execution_ready": False,
        "selector_runs": 0,
        "provider_calls": 0,
        "counts": {
            "v7_sources": 3798,
            "identity_candidates": 39,
            "orphan_block_marker_with_prefix": 17,
            "literal_block_marker": 22,
            "required_returns": 78,
        },
        "bindings": {
            "source_manifest_sha256": sha(source_manifest_bytes),
            "failed_qa_final_report_sha256": sha((ROOT / FAILED_QA / "qa_final_report.json").read_bytes()),
            "old_i1_i2_report_sha256": sha((ROOT / I1_I2 / "mechanical_report.json").read_bytes()),
            "instruction_sha256": sha((ROOT / INSTRUCTION).read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "tracked_artifacts": {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()},
        "local_inputs": {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in payloads.items()},
        "boundary": "Source-grounded I1 identity repair only. V7 prompts, K=6 packets, labels, acceptable sets and retrieval outcomes are neither read nor changed.",
        "next_gate": "Reconcile exact A/B agreement; disagreements or unresolved rows require a source-only coordinator before a versioned I1 materializer amendment.",
    }
    files["integrity_report.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 I1 identity overlay source-only review\n\n"
        "State: `PENDING_TWO_INDEPENDENT_SOURCE_ONLY_IDENTITY_REVIEWS`. The failed Phase-7 QA exposed 39 malformed native descriptions: 17 orphan block-marker declarations and 22 literal `>` values. No source or historical representation is overwritten.\n\n"
        "Each reviewer reads only one identical local input and the frozen instruction, returns all 39 rows independently, and does not inspect the other lane. Exact agreement can be reconciled mechanically; disagreements go to a source-only coordinator.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i1_identity_overlay_review.py --verify`.\n"
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
            require_equal(ROOT / CACHE / name, data)
        status = "PASS_V7_I1_IDENTITY_OVERLAY_REVIEW_PREPARATION_REPLAY"
    else:
        if (ROOT / OUTPUT).exists() or (ROOT / CACHE).exists():
            raise FileExistsError("refusing to overwrite versioned identity-review package")
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            write_new(ROOT / CACHE / name, data)
        status = "PASS_V7_I1_IDENTITY_OVERLAY_REVIEW_PREPARATION_CREATED"
    print(json.dumps({"status": status, "identity_candidates": 39, "required_returns": 78}, sort_keys=True))


if __name__ == "__main__":
    main()
