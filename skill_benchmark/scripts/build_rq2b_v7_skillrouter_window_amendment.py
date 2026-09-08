#!/usr/bin/env python3
"""Build/replay the prospective V7 SkillRouter embedding window amendment.

This is a source-only tokenizer audit.  It neither approves the amendment nor
loads a model, ranks a query, reads labels/results, or contacts a provider.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation"
OUTPUT = PREP / "v7_skillrouter_embedding_window_amendment_2026_09_09_v1"
I1I2 = PREP / "v7_phase7_i1_i2_2026_09_08_v1"
I1I2_CACHE = ROOT / "skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1"
I3 = PREP / "v7_phase7_i3_merged_2026_09_08_v1"
RUNTIME = PREP / "v7_first_matrix_runtime_preflight_2026_09_09_v1"
PLAN = ROOT / "thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md"
REPRESENTATIONS = {
    "I1-discovery": I1I2_CACHE / "i1-discovery.jsonl",
    "I2-original": I1I2_CACHE / "i2-original.jsonl",
    "I3C-fielded": I3 / "i3c_fielded.jsonl",
    "I3-flat": I3 / "i3_flat.jsonl",
}
WINDOW_TOKENS = 7500
OVERLAP_TOKENS = 256


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_path(path: Path) -> str:
    return sha(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_bytes())


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def percentile(values: list[int], fraction: float) -> int:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int((len(ordered) - 1) * fraction))]


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(rows: list[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def build() -> dict[str, bytes]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    runtime_inventory_path = RUNTIME / "runtime_inventory.json"
    runtime_report_path = RUNTIME / "integrity_report.json"
    runtime_inventory = read_json(runtime_inventory_path)
    runtime_report = read_json(runtime_report_path)
    require(runtime_report["status"] == "PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY", "runtime preflight state drift")
    model = runtime_inventory["local_models"]["skillrouter_embedding"]
    snapshot = ROOT / model["snapshot_path"]
    require(sha_path(snapshot / "tokenizer.json") == model["files"]["tokenizer.json"], "embedding tokenizer drift")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=True)

    i1i2_report = read_json(I1I2 / "mechanical_report.json")
    merged_manifest = read_json(I3 / "manifest.json")
    for name, path in REPRESENTATIONS.items():
        require(path.is_file(), f"representation missing: {name}")
        if name in {"I1-discovery", "I2-original"}:
            expected = i1i2_report["local_derived_artifacts"][path.name]["sha256"]
        else:
            expected = merged_manifest["artifacts"][path.name]["sha256"]
        require(sha_path(path) == expected, f"representation drift: {name}")

    summary: dict[str, dict[str, Any]] = {}
    over_rows: list[dict[str, Any]] = []
    for representation, path in REPRESENTATIONS.items():
        rows = read_rows(path)
        require(len(rows) == 3798, f"representation coverage drift: {representation}")
        counts: list[int] = []
        for row in rows:
            text = str(row["selector_text"])
            count = len(tokenizer.encode(text, add_special_tokens=False))
            counts.append(count)
            if count > WINDOW_TOKENS:
                over_rows.append({
                    "representation": representation,
                    "source_sha256": row["source_sha256"],
                    "selector_text_sha256": row["selector_text_sha256"],
                    "token_count": count,
                    "minimum_stride_window_count": 1 + math.ceil((count - WINDOW_TOKENS) / (WINDOW_TOKENS - OVERLAP_TOKENS)),
                })
        summary[representation] = {
            "rows": len(rows),
            "total_tokens": sum(counts),
            "p50_tokens": percentile(counts, 0.50),
            "p95_tokens": percentile(counts, 0.95),
            "p99_tokens": percentile(counts, 0.99),
            "maximum_tokens": max(counts),
            "rows_above_7500": sum(value > WINDOW_TOKENS for value in counts),
            "rows_above_model_32768": sum(value > 32768 for value in counts),
        }
    over_rows.sort(key=lambda row: (row["representation"], row["source_sha256"]))
    require(len(over_rows) == 30, "prospective window-scope count drift")
    require(summary["I2-original"]["rows_above_7500"] == 28, "I2 overflow count drift")
    require(summary["I3C-fielded"]["rows_above_7500"] == summary["I3-flat"]["rows_above_7500"] == 1, "I3 overflow count drift")

    audit = {
        "schema_version": "rq2b-v7-skillrouter-embedding-window-audit-v1",
        "status": "PASS_SOURCE_ONLY_TOKEN_AUDIT_PENDING_METHOD_APPROVAL",
        "network_calls": 0,
        "model_forwards": 0,
        "labels_or_results_read": 0,
        "tokenizer": {
            "model": model["repository"],
            "revision": model["revision"],
            "tokenizer_sha256": model["files"]["tokenizer.json"],
        },
        "representation_summary": summary,
        "proposed_scope": {
            "document_representation_rows_windowed": len(over_rows),
            "document_representation_rows_total": 3798 * 4,
            "window_tokens": WINDOW_TOKENS,
            "overlap_tokens": OVERLAP_TOKENS,
            "coverage": "exact lossless character coverage using the existing frozen exact-markdown chunker",
            "aggregation": "maximum query-to-window cosine per source",
            "unwindowed_rows": 3798 * 4 - len(over_rows),
        },
        "bindings": {
            "runtime_inventory_sha256": sha_path(runtime_inventory_path),
            "runtime_integrity_report_sha256": sha_path(runtime_report_path),
            "i1_i2_mechanical_report_sha256": sha_path(I1I2 / "mechanical_report.json"),
            "i3_merged_manifest_sha256": sha_path(I3 / "manifest.json"),
            "approved_plan_sha256": sha_path(PLAN),
            "builder_sha256": sha_path(Path(__file__)),
        },
    }
    amendment = {
        "schema_version": "rq2b-v7-skillrouter-embedding-window-method-amendment-v1",
        "state": "AWAITING_EXPLICIT_USER_APPROVAL_NOT_EXECUTION_AUTHORITY",
        "reason": "The frozen SkillRouter checkpoint has max_position_embeddings=32768, one I2 row has 56648 proxy tokens, and this 16-GB M1 host failed closed at 20000/30000 tokens with invalid-buffer allocations. No candidate may be truncated or excluded.",
        "proposal": audit["proposed_scope"],
        "affected_first_stage_cells": ["B03", "B06", "B09", "B12"],
        "affected_rows_by_representation": {name: value["rows_above_7500"] for name, value in summary.items()},
        "does_not_change": [
            "V7 1077 prompt scope or acceptable sets",
            "3798 candidate identities or source bytes",
            "K_audit=6 or k_route=20",
            "Qwen embedding chunk contract",
            "either reranker window contract",
        ],
        "interpretation_boundary": "If approved, TS is the tested SkillRouter max-window pipeline for 30 over-limit representation rows, not a claim that every candidate used one full-context vector. The other 15162 document-view rows remain single-vector.",
        "alternatives_rejected_without_execution": [
            "silent truncation",
            "candidate exclusion",
            "raising the checkpoint position limit",
            "calling a method with hardware-infeasible full-context forwards complete",
        ],
        "audit_sha256": None,
    }
    audit_data = json_bytes(audit)
    amendment["audit_sha256"] = sha(audit_data)
    amendment_data = json_bytes(amendment)
    over_data = rows_bytes(over_rows)
    readme = (
        "# Prospective V7 SkillRouter embedding window amendment\n\n"
        "State: `AWAITING_EXPLICIT_USER_APPROVAL_NOT_EXECUTION_AUTHORITY`. This source-only audit found 30 of 15,192 document-representation rows above the tested 7,500-token host ceiling: I2=28, I3C=1, I3-flat=1, I1=0. The proposal uses exact lossless 7,500-token windows, 256-token overlap and max-window cosine only for those rows. It never truncates or excludes a candidate.\n\n"
        "This package does not authorise model execution. Replay: `.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/build_rq2b_v7_skillrouter_window_amendment.py --verify`.\n"
    ).encode()
    return {
        "token_audit.json": audit_data,
        "over_limit_rows.jsonl": over_data,
        "method_amendment.json": amendment_data,
        "README.md": readme,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.verify:
        require(OUTPUT.is_dir(), "window-amendment package missing")
        require({path.name for path in OUTPUT.iterdir()} == set(expected), "window-amendment file-set drift")
        for name, data in expected.items():
            require((OUTPUT / name).read_bytes() == data, f"window-amendment drift: {name}")
        status = "PASS_PROSPECTIVE_WINDOW_AMENDMENT_REPLAY"
    else:
        require(not OUTPUT.exists(), "refusing to overwrite versioned window-amendment package")
        OUTPUT.mkdir(parents=True)
        for name, data in expected.items():
            (OUTPUT / name).write_bytes(data)
        status = "PASS_PROSPECTIVE_WINDOW_AMENDMENT_CREATED_PENDING_APPROVAL"
    print(json.dumps({"status": status, "output": str(OUTPUT.relative_to(ROOT))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
