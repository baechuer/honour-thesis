#!/usr/bin/env python3
"""Prepare/replay a source-only full-corpus V7 I3 V4 re-extraction."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from audit_rq2b_preflight import parse_frontmatter
from prepare_rq2b_v7_first_matrix import safe_path


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
SOURCE_PACKAGE = PREP / "v7_first_matrix_2026_09_08_v1"
I1_I2_V2 = PREP / "v7_phase7_i1_i2_2026_09_09_v2"
OVERLAY_PACKAGE = PREP / "v7_phase7_i1_identity_overlay_final_2026_09_09_v1"
OLD_I3 = PREP / "v7_phase7_i3_merged_2026_09_08_v1"
FAILED_QA = PREP / "v7_phase7_i3_blinded_qa_final_2026_09_09_v2"
OUTPUT = PREP / "v7_phase7_i3_full_reextraction_2026_09_09_v4"
CACHE = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_full_reextraction_2026_09_09_v4")
INSTRUCTION = Path("skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V4.md")
BATCH_SIZE = 40
EXTRACTOR_GROUPS = 3


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def build() -> tuple[dict[str, bytes], dict[str, bytes]]:
    sources = rows(ROOT / SOURCE_PACKAGE / "source_manifest.jsonl")
    overlays = rows(ROOT / OVERLAY_PACKAGE / "identity_overlay.jsonl")
    overlay_by_sha = {row["source_sha256"]: row for row in overlays}
    old_fresh_ids = {row["skill_id"] for row in rows(ROOT / OLD_I3 / "fresh_worker_outputs.jsonl")}
    if len(sources) != 3798 or len(overlay_by_sha) != 39 or len(old_fresh_ids) != 1368:
        raise ValueError("V7 source/overlay/lineage coverage mismatch")
    qa = json.loads((ROOT / FAILED_QA / "qa_final_report.json").read_bytes())
    if qa.get("state") != "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE":
        raise ValueError("full re-extraction must bind to frozen QA failure")

    all_inputs = []
    lineage = Counter()
    for source_row_index, source in enumerate(sources):
        raw = safe_path(ROOT, source["path"]).read_bytes()
        if sha(raw) != source["sha256"] or len(raw) != source["bytes"]:
            raise ValueError(f"source drift: {source['path']}")
        text = raw.decode("utf-8")
        native = parse_frontmatter(text)
        name = native.get("name", "").strip()
        overlay = overlay_by_sha.get(source["sha256"])
        description = overlay["selected_description"].strip() if overlay else native.get("description", "").strip()
        if not name or not description or description.lower() in {">", "|", "use this skill when >", "use this skill when |"}:
            raise ValueError(f"unusable repaired identity: {source['path']}")
        skill_id = "sha256-" + source["sha256"]
        previous_lineage = "FORMERLY_FRESH_V3" if skill_id in old_fresh_ids else "FORMERLY_REUSED_V3"
        lineage[previous_lineage] += 1
        all_inputs.append({
            "source_row_index": source_row_index,
            "skill_id": skill_id,
            "name": name,
            "description": description,
            "family": "v7-source-hash-unique",
            "source": source["path"],
            "source_sha256": source["sha256"],
            "text": text,
            "identity_provenance": "SOURCE_GROUNDED_IDENTITY_OVERLAY" if overlay else "NATIVE_FRONTMATTER",
            "previous_extraction_lineage": previous_lineage,
            "fresh_extraction_reason": "FULL_CORPUS_REPAIR_AFTER_BLINDED_QA_V2_FAILURE",
        })
    if lineage != Counter({"FORMERLY_REUSED_V3": 2430, "FORMERLY_FRESH_V3": 1368}):
        raise ValueError("previous extraction lineage mismatch")

    cache_payloads: dict[str, bytes] = {}
    assignments = []
    group_rows = Counter()
    for batch_index, start in enumerate(range(0, len(all_inputs), BATCH_SIZE), 1):
        batch = all_inputs[start:start + BATCH_SIZE]
        batch_id = f"I3V4-{batch_index:03d}"
        input_name = f"inputs/i3v4_input_{batch_index:03d}.jsonl"
        output_name = f"outputs/i3v4_output_{batch_index:03d}.jsonl"
        data = rows_bytes(batch)
        cache_payloads[input_name] = data
        extractor_group = ((batch_index - 1) % EXTRACTOR_GROUPS) + 1
        group_rows[extractor_group] += len(batch)
        assignments.append({
            "batch_id": batch_id,
            "row_count": len(batch),
            "first_source_row_index": batch[0]["source_row_index"],
            "last_source_row_index": batch[-1]["source_row_index"],
            "input_path": str(CACHE / input_name),
            "input_sha256": sha(data),
            "expected_output_path": str(CACHE / output_name),
            "instruction_path": str(INSTRUCTION),
            "instruction_sha256": sha((ROOT / INSTRUCTION).read_bytes()),
            "extractor_group": extractor_group,
            "state": "UNSTARTED",
        })
    if len(assignments) != math.ceil(3798 / BATCH_SIZE) or len(assignments) != 95:
        raise ValueError("V4 batch count mismatch")
    if sum(row["row_count"] for row in assignments) != 3798 or assignments[-1]["row_count"] != 38:
        raise ValueError("V4 assignment coverage mismatch")

    files = {"full_reextraction_assignment_manifest.jsonl": rows_bytes(assignments)}
    report = {
        "schema_version": "rq2b-v7-phase7-i3-full-reextraction-preparation-v4",
        "state": "PENDING_3798_SOURCE_ONLY_V4_EXTRACTIONS",
        "formal_execution_ready": False,
        "network_calls": 0,
        "selector_runs": 0,
        "counts": {
            "sources": 3798,
            "batches": len(assignments),
            "batch_size_max": BATCH_SIZE,
            "last_batch_rows": assignments[-1]["row_count"],
            "former_reused_lineage": lineage["FORMERLY_REUSED_V3"],
            "former_fresh_lineage": lineage["FORMERLY_FRESH_V3"],
            "source_grounded_identity_overlays": 39,
            "extractor_group_rows": {str(key): group_rows[key] for key in sorted(group_rows)},
        },
        "bindings": {
            "source_manifest_sha256": sha((ROOT / SOURCE_PACKAGE / "source_manifest.jsonl").read_bytes()),
            "i1_i2_v2_report_sha256": sha((ROOT / I1_I2_V2 / "mechanical_report.json").read_bytes()),
            "identity_overlay_report_sha256": sha((ROOT / OVERLAY_PACKAGE / "integrity_report.json").read_bytes()),
            "old_i3_manifest_sha256": sha((ROOT / OLD_I3 / "manifest.json").read_bytes()),
            "failed_qa_report_sha256": sha((ROOT / FAILED_QA / "qa_final_report.json").read_bytes()),
            "instruction_sha256": sha((ROOT / INSTRUCTION).read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "tracked_artifacts": {"full_reextraction_assignment_manifest.jsonl": {"sha256": sha(files["full_reextraction_assignment_manifest.jsonl"]), "rows": len(assignments)}},
        "local_inputs": {"rows": 3798, "batches": 95, "aggregate_sha256": sha(b"".join(cache_payloads[name] for name in sorted(cache_payloads)))},
        "method_boundary": "Prospective source-only repair under the same seven fields. No historical semantic payload is reused. V7 prompts, K=6, labels, acceptable sets and source bytes are unchanged.",
        "completion_gates": [
            "95/95 outputs pass identity, schema, exact-substring and V4 lexical safety validation",
            "all warnings and mechanical risk candidates receive source-only disposition",
            "I3C and I3-flat are regenerated from one canonical extraction corpus",
            "a genuinely fresh 120-row blinded QA sample passes the unchanged v2 thresholds",
        ],
    }
    files["preparation_report.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 Phase-7 I3 full re-extraction V4\n\n"
        "State: `PENDING_3798_SOURCE_ONLY_V4_EXTRACTIONS`. This prospective repair was triggered by the frozen blinded-QA v2 failure. It re-extracts all 3,798 source-hash-unique artifacts under the same seven-field representation schema; no historical semantic payload is selected.\n\n"
        "There are 95 indivisible batches (94 x 40 rows, one x 38), deterministically assigned to three extraction groups. Workers may read only their input and `I3C_SUBAGENT_EXTRACTION_V4.md`. No benchmark prompt, target, label, acceptable set or result is permitted.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i3_full_reextraction_v4.py --verify`.\n"
    ).encode()
    return files, cache_payloads


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
        status = "PASS_V7_I3_V4_FULL_REEXTRACTION_PREPARATION_REPLAY"
    else:
        if (ROOT / OUTPUT).exists() or (ROOT / CACHE).exists():
            raise FileExistsError("refusing to overwrite V4 re-extraction preparation")
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            write_new(ROOT / CACHE / name, data)
        status = "PASS_V7_I3_V4_FULL_REEXTRACTION_PREPARATION_CREATED"
    print(json.dumps({"status": status, "sources": 3798, "batches": 95}, sort_keys=True))


if __name__ == "__main__":
    main()
