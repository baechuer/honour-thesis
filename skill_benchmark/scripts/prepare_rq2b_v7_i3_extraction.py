#!/usr/bin/env python3
"""Prepare/replay source-only V7 I3 reuse and fresh-extraction packets.

The one-time import preserves four exact historical V3 artifacts. Source-hash
identical, unambiguous extraction rows are rebound to current source identities;
all other rows become fresh, label-free subagent inputs in ignored cache.
No historical semantic-QA pass is inherited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from audit_rq2b_preflight import parse_frontmatter
from merge_rq2b_i3c import canonical_extraction
from prepare_rq2b_v7_first_matrix import safe_path

ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
SOURCE_PACKAGE = PREP / "v7_first_matrix_2026_09_08_v1"
OUTPUT = PREP / "v7_phase7_i3_extraction_2026_09_08_v1"
CACHE = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_extraction_2026_09_08_v1")
LEGACY_BASE = Path("skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18")
PROMPT = Path("skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V3.md")
BATCH_SIZE = 40
LEGACY_FILES = {
    "historical_v3_canonical_extractions.jsonl": (LEGACY_BASE / "i3c_merged_final/canonical_extractions.jsonl", "0f9f1e717e7236c033a093303a03340de739c702023aaf084c18429969b22588"),
    "historical_v3_final_manifest.json": (LEGACY_BASE / "i3c_merged_final/manifest.json", "50220955aadafa66f4f5032763ceb5ed4e68b88c04bc2b3b5cab98f1f253b661"),
    "historical_v3_automatic_integrity_report.json": (LEGACY_BASE / "automatic_integrity_freeze/automatic_integrity_freeze_report.json", "a3fe05dda00c6e7935262d8be30a69ddb45b15eeeef7426fbfc642a7071c988f"),
    "historical_v3_invalid_manual_qa_attempt.json": (LEGACY_BASE / "i3c_manual_qa_calibrated_v1/manual_qa_attempt_audit.json", "bced55730410711bdf5dbce2b2442911ae6bad476cb14494e1e92c86fa6ed163"),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def rows_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def current_input(index: int, source: dict) -> dict:
    raw = safe_path(ROOT, source["path"]).read_bytes()
    if sha(raw) != source["sha256"] or len(raw) != source["bytes"]:
        raise ValueError(f"current source drift: {source['path']}")
    text = raw.decode("utf-8")
    native = parse_frontmatter(text)
    name, description = native.get("name", "").strip(), native.get("description", "").strip()
    if not name or not description:
        raise ValueError(f"missing native identity: {source['path']}")
    return {"source_row_index": index, "skill_id": "sha256-" + source["sha256"],
            "name": name, "description": description, "family": "v7-source-hash-unique",
            "source": source["path"], "source_sha256": source["sha256"], "text": text}


def worker_from_legacy(inp: dict, old: dict) -> dict:
    return {"schema_version": "I3C_SUBAGENT_EXTRACTION_V2", "parser": "codex_subagent",
            "family": inp["family"], "skill": None, "skill_id": inp["skill_id"],
            "name": inp["name"], "description": inp["description"], "source": inp["source"],
            "fields": old["fields"], "absent_fields": old["absent_fields"],
            "field_warnings": old["field_warnings"], "qa_warnings": old["qa_warnings"]}


def semantic_payload(row: dict) -> bytes:
    return json.dumps({key: row[key] for key in ("fields", "absent_fields", "field_warnings", "qa_warnings")},
                      ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def get_legacy(import_root: Path | None) -> dict[str, bytes]:
    found = {}
    for name, (relative, expected) in LEGACY_FILES.items():
        path = (import_root / relative) if import_root else (ROOT / OUTPUT / name)
        data = path.read_bytes()
        if sha(data) != expected:
            raise ValueError(f"historical artifact hash mismatch: {name}")
        found[name] = data
    manifest = json.loads(found["historical_v3_final_manifest.json"])
    automatic = json.loads(found["historical_v3_automatic_integrity_report.json"])
    invalid_qa = json.loads(found["historical_v3_invalid_manual_qa_attempt.json"])
    if manifest.get("state") != "automatic_gates_passed_manual_qa_pending":
        raise ValueError("historical extraction state mismatch")
    if automatic.get("state") != "automatic_integrity_verification_passed":
        raise ValueError("historical automatic integrity did not pass")
    if invalid_qa.get("state") != "manual_qa_attempt_protocol_invalid_no_extraction_fidelity_decision":
        raise ValueError("historical invalid-QA disposition mismatch")
    return found


def build(import_root: Path | None) -> tuple[dict[str, bytes], dict[str, bytes]]:
    legacy = get_legacy(import_root)
    source_manifest = (ROOT / SOURCE_PACKAGE / "source_manifest.jsonl").read_bytes()
    sources = rows(source_manifest)
    if len(sources) != 3798 or len({row["sha256"] for row in sources}) != 3798:
        raise ValueError("current source scope mismatch")
    historical = rows(legacy["historical_v3_canonical_extractions.jsonl"])
    if len(historical) != 2433:
        raise ValueError("historical extraction row count mismatch")
    old_by_sha: dict[str, list[dict]] = defaultdict(list)
    for row in historical:
        old_by_sha[row["source_sha256"]].append(row)

    reused, reuse_ledger, fresh = [], [], []
    for index, source in enumerate(sources):
        inp = current_input(index, source)
        candidates = old_by_sha.get(source["sha256"], [])
        payloads = {semantic_payload(row) for row in candidates}
        if candidates and len(payloads) == 1:
            selected = min(candidates, key=lambda row: (row["source_row_index"], row["skill_id"]))
            output = worker_from_legacy(inp, selected)
            # Full current-source validation: identities, schema and every exact span.
            canonical_extraction(inp, output)
            reused.append(output)
            reuse_ledger.append({"source_sha256": source["sha256"], "current_source_row_index": index,
                                 "current_source_path": source["path"], "reuse_status": "REUSED_PENDING_FRESH_CURRENT_QA",
                                 "historical_source_row_indices": sorted(row["source_row_index"] for row in candidates),
                                 "historical_skill_ids": sorted(row["skill_id"] for row in candidates),
                                 "historical_worker_output_sha256": selected["worker_output_sha256"],
                                 "semantic_payload_sha256": sha(semantic_payload(selected))})
        else:
            reason = "NO_HISTORICAL_SOURCE_HASH_MATCH" if not candidates else "AMBIGUOUS_HISTORICAL_EXTRACTOR_OUTPUTS"
            fresh.append({**inp, "fresh_extraction_reason": reason})
    if len(reused) != 2430 or len(fresh) != 1368:
        raise ValueError(f"unexpected reuse split: {len(reused)}/{len(fresh)}")
    if sum(row["fresh_extraction_reason"] == "AMBIGUOUS_HISTORICAL_EXTRACTOR_OUTPUTS" for row in fresh) != 1:
        raise ValueError("ambiguous historical row count mismatch")

    payloads, assignments = {}, []
    for batch_index, start in enumerate(range(0, len(fresh), BATCH_SIZE), 1):
        batch = fresh[start:start + BATCH_SIZE]
        input_name = f"inputs/i3_input_{batch_index:03d}.jsonl"
        output_name = f"outputs/i3_output_{batch_index:03d}.jsonl"
        data = rows_bytes(batch)
        payloads[input_name] = data
        assignments.append({"batch_id": f"I3-{batch_index:03d}", "row_count": len(batch),
                            "first_source_row_index": batch[0]["source_row_index"],
                            "last_source_row_index": batch[-1]["source_row_index"],
                            "input_path": str(CACHE / input_name), "input_sha256": sha(data),
                            "expected_output_path": str(CACHE / output_name),
                            "instruction_path": str(PROMPT), "instruction_sha256": sha((ROOT / PROMPT).read_bytes()),
                            "state": "UNSTARTED"})
    if len(assignments) != 35 or sum(row["row_count"] for row in assignments) != 1368:
        raise ValueError("fresh assignment coverage mismatch")
    files = {**legacy, "reused_worker_outputs.jsonl": rows_bytes(reused),
             "reuse_ledger.jsonl": rows_bytes(reuse_ledger),
             "fresh_assignment_manifest.jsonl": rows_bytes(assignments)}
    report = {"schema_version": "rq2b-v7-phase7-i3-extraction-preparation-v1",
              "status": "PASS_I3_REUSE_AND_FRESH_INPUTS_PREPARED_PENDING_1368_EXTRACTIONS_AND_FRESH_QA",
              "formal_execution_ready": False, "network_calls": 0, "selector_runs": 0,
              "bindings": {"source_manifest_sha256": sha(source_manifest),
                           "instruction_sha256": sha((ROOT / PROMPT).read_bytes()),
                           "script_sha256": sha(Path(__file__).read_bytes())},
              "counts": {"current_sources": 3798, "historical_rows": 2433,
                         "historical_unique_source_hashes": len(old_by_sha),
                         "reused_source_hashes_pending_current_qa": len(reused),
                         "fresh_extraction_rows": len(fresh), "fresh_batches": len(assignments),
                         "ambiguous_historical_hashes_requiring_fresh_extraction": 1},
              "historical_qa_boundary": "Automatic integrity passed. The historical 120-row semantic-QA attempt was explicitly invalid and provides no pass/fail decision. No current semantic-QA status is inherited.",
              "fresh_inputs": {"contains_source_text": True, "contains_prompt_or_label_or_role": False,
                               "storage": "ignored local cache; exactly regenerated from tracked frozen sources"},
              "completion_requirements": ["35 output batches validate with one row per input and exact source spans",
                                           "all 3798 rows merge and I3C/I3-flat evidence multisets match",
                                           "fresh current stratified blinded QA under an unambiguous codebook passes master-SOP gates"]}
    report["tracked_artifact_sha256"] = {name: sha(data) for name, data in files.items()}
    report["cache_input_sha256"] = {name: sha(data) for name, data in payloads.items()}
    files["preparation_report.json"] = json_bytes(report)
    return files, payloads


def check(path: Path, expected: bytes) -> None:
    if path.read_bytes() != expected:
        raise ValueError(f"artifact drift: {path}")


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--import-legacy-workspace", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify and args.import_legacy_workspace:
        parser.error("verify uses the preserved tracked historical artifacts")
    if not args.verify and not args.import_legacy_workspace:
        parser.error("initial materialisation requires --import-legacy-workspace")
    if not args.verify and (ROOT / OUTPUT).exists():
        raise FileExistsError("refusing to overwrite versioned I3 preparation")
    files, payloads = build(args.import_legacy_workspace)
    if args.verify:
        for name, data in files.items():
            check(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            check(ROOT / CACHE / name, data)
    else:
        (ROOT / OUTPUT).mkdir(parents=True)
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            write_new(ROOT / CACHE / name, data)
    print(json.dumps({"status": "PASS_I3_PREPARATION_REPLAY" if args.verify else "PASS_I3_PREPARATION_CREATED",
                      "reused_pending_current_qa": 2430, "fresh_rows": 1368, "fresh_batches": 35,
                      "formal_execution_ready": False}, sort_keys=True))


if __name__ == "__main__":
    main()
