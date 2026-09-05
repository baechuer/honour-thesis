#!/usr/bin/env python3
"""Assemble the local-only RQ2b v1.2 source manifest and chunk-plan metadata."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from audit_rq2b_preflight import parse_frontmatter


PARENT_VERSION = "rq2b-full-library-v1-2026-08-02"
VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
PARENT_SOURCE_MANIFEST = f"skill_benchmark/rq2b_full_library/{PARENT_VERSION}/source_manifest.jsonl"
VERSION_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
OVERLAY_MANIFEST = f"{VERSION_ROOT}/source_overlay_manifest.json"
APPROVAL_RECEIPT = f"{VERSION_ROOT}/v12_assembled_source_preflight_approval_receipt.json"
SOURCE_MANIFEST = f"{VERSION_ROOT}/source_manifest.jsonl"
PREFLIGHT_REPORT = f"{VERSION_ROOT}/assembled_source_preflight.json"
CHUNK_PLAN = f"{VERSION_ROOT}/i3c_chunk_plan_metadata.json"

QWEN_PROXY_MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
QWEN_PROXY_REVISION = "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
MAX_ROWS_PER_CHUNK = 50
MAX_PROXY_TOKENS_PER_CHUNK = 60_000
BANNED_BACKGROUND = {
    "benchmark_scale_explanation": r"background scale skill used to create realistic retrieval pressure in the benchmark|background scale skill|retrieval pressure",
    "benchmark_gold_label": r"gold-label core benchmark skill|core benchmark skill",
    "benchmark_confusability": r"neighboring confusable skill|neighboring skill",
    "benchmark_artifact_reference": r"expected artifact below",
    "benchmark_switch_rule": r"do not silently switch to a more specific benchmark core skill",
    "old_generic_template": r"## Workflow\n\n1\. Read the user request and identify the intended operational goal\.|## Why this skill is distinct",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json_new(path: Path, value: Any) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen artifact: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl_new(path: Path, rows: list[dict[str, Any]]) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen artifact: {path}")
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def local_tokenizer() -> tuple[Any, Path, str]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    snapshot = Path.home() / ".cache" / "huggingface" / "hub" / (
        "models--" + QWEN_PROXY_MODEL.replace("/", "--")
    ) / "snapshots" / QWEN_PROXY_REVISION
    tokenizer_json = snapshot / "tokenizer.json"
    if not tokenizer_json.exists():
        raise FileNotFoundError(f"Missing cached proxy tokenizer: {tokenizer_json}")
    return AutoTokenizer.from_pretrained(snapshot, local_files_only=True), snapshot, sha256_file(tokenizer_json)


def chunk_records(rows: list[dict[str, Any]], token_counts: dict[str, int]) -> list[dict[str, Any]]:
    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_tokens = 0
    for row in rows:
        tokens = token_counts[row["skill_id"]]
        if tokens > MAX_PROXY_TOKENS_PER_CHUNK:
            raise ValueError(f"Single source exceeds chunk ceiling: {row['skill_id']}")
        if current and (len(current) >= MAX_ROWS_PER_CHUNK or current_tokens + tokens > MAX_PROXY_TOKENS_PER_CHUNK):
            chunks.append(current)
            current = []
            current_tokens = 0
        current.append(row)
        current_tokens += tokens
    if current:
        chunks.append(current)
    records = []
    for index, chunk in enumerate(chunks):
        ids = [row["skill_id"] for row in chunk]
        identity = [{"source_row_index": row["source_row_index"], "skill_id": row["skill_id"], "source_sha256": row["source_sha256"]} for row in chunk]
        records.append({
            "chunk_index": index,
            "first_source_row_index": chunk[0]["source_row_index"],
            "last_source_row_index": chunk[-1]["source_row_index"],
            "row_count": len(chunk),
            "qwen_proxy_tokens": sum(token_counts[skill_id] for skill_id in ids),
            "source_utf8_bytes": sum(row["source_utf8_bytes"] for row in chunk),
            "identity_sha256": sha256_text(json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
            "contains_source_text": False,
        })
    return records


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    version_root = root / VERSION_ROOT
    output_paths = [root / SOURCE_MANIFEST, root / PREFLIGHT_REPORT, root / CHUNK_PLAN]
    if any(path.exists() for path in output_paths):
        raise FileExistsError(f"Refusing to overwrite preflight output: {[path for path in output_paths if path.exists()]}")

    parent_path = root / PARENT_SOURCE_MANIFEST
    overlay_path = root / OVERLAY_MANIFEST
    receipt_path = root / APPROVAL_RECEIPT
    parent_rows = read_jsonl(parent_path)
    overlay = read_json(overlay_path)
    receipt = read_json(receipt_path)
    if receipt["state"] != "explicitly_approved_for_local_v12_assembled_source_preflight_once":
        raise ValueError("Local preflight receipt is not approved")
    if len(parent_rows) != 2433 or overlay["scope"]["skill_count"] != 1800:
        raise ValueError("Unexpected parent or overlay inventory count")

    overlay_rows = {row["skill_id"]: row for row in overlay["rows"]}
    parent_background_ids = {row["skill_id"] for row in parent_rows if row["family"] == "background_scale"}
    if parent_background_ids != set(overlay_rows):
        raise ValueError("Overlay skill set does not exactly replace the parent background_scale family")

    assembled: list[dict[str, Any]] = []
    reused_unchanged = []
    background_lint = Counter()
    nonbackground_keyword_matches: list[dict[str, str]] = []
    for expected_index, original in enumerate(parent_rows):
        if original["source_row_index"] != expected_index:
            raise ValueError("Parent source row indices are not contiguous")
        row = dict(original)
        if row["family"] == "background_scale":
            replacement = overlay_rows[row["skill_id"]]
            source_path = root / replacement["path"]
            raw = source_path.read_bytes()
            text = raw.decode("utf-8")
            if sha256_bytes(raw) != replacement["sha256"] or len(raw) != replacement["utf8_bytes"]:
                raise ValueError(f"Overlay drift: {row['skill_id']}")
            for label, pattern in BANNED_BACKGROUND.items():
                background_lint[label] += int(bool(re.search(pattern, text, flags=re.IGNORECASE)))
            frontmatter = parse_frontmatter(text)
            name = frontmatter.get("name", "").strip()
            description = frontmatter.get("description", "").strip()
            if name != row["skill_id"] or not description:
                raise ValueError(f"Overlay frontmatter invalid: {row['skill_id']}")
            row.update({
                "source_path": replacement["path"],
                "source_sha256": replacement["sha256"],
                "source_utf8_bytes": len(raw),
                "source_chars": len(text),
                "source_tokens_approx_chars_div_4": math.ceil(len(text) / 4),
                "source_name": name,
                "source_name_sha256": sha256_text(name),
                "source_description": description,
                "source_description_sha256": sha256_text(description),
                "wrapper_path": replacement["path"],
                "wrapper_sha256": replacement["sha256"],
            })
        else:
            source_path = root / row["source_path"]
            raw = source_path.read_bytes()
            if sha256_bytes(raw) != row["source_sha256"]:
                raise ValueError(f"Unchanged source drift: {row['skill_id']}")
            reused_unchanged.append(row["skill_id"])
            text = raw.decode("utf-8")
            for label, pattern in BANNED_BACKGROUND.items():
                if re.search(pattern, text, flags=re.IGNORECASE):
                    nonbackground_keyword_matches.append({
                        "skill_id": row["skill_id"],
                        "family": row["family"],
                        "pattern": label,
                    })
        assembled.append(row)

    if any(background_lint.values()):
        raise ValueError(f"Background scaffold lint failed: {dict(background_lint)}")
    if len(assembled) != 2433 or len({row['skill_id'] for row in assembled}) != 2433:
        raise ValueError("Assembled manifest identity coverage failed")
    if len(reused_unchanged) != 633:
        raise ValueError("Unexpected unchanged-source count")

    tokenizer, tokenizer_snapshot, tokenizer_sha = local_tokenizer()
    token_counts = {
        row["skill_id"]: len(
            tokenizer.encode(
                (root / row["source_path"]).read_bytes().decode("utf-8"),
                add_special_tokens=False,
            )
        )
        for row in assembled
    }
    chunks = chunk_records(assembled, token_counts)
    if sum(chunk["row_count"] for chunk in chunks) != 2433:
        raise ValueError("Chunk plan coverage failed")

    write_jsonl_new(root / SOURCE_MANIFEST, assembled)
    chunk_plan = {
        "schema_version": "rq2b-v12-i3c-chunk-plan-metadata-v1",
        "version_id": VERSION_ID,
        "state": "local_chunk_plan_only_no_worker_inputs",
        "source_manifest": {"path": SOURCE_MANIFEST, "sha256": sha256_file(root / SOURCE_MANIFEST), "rows": len(assembled)},
        "tokenizer": {
            "local_proxy_tokenizer_model": QWEN_PROXY_MODEL,
            "local_proxy_tokenizer_revision": QWEN_PROXY_REVISION,
            "local_proxy_tokenizer_snapshot": str(tokenizer_snapshot),
            "local_proxy_tokenizer_sha256": tokenizer_sha,
        },
        "chunk_policy": {
            "maximum_rows": MAX_ROWS_PER_CHUNK,
            "maximum_qwen_proxy_tokens": MAX_PROXY_TOKENS_PER_CHUNK,
            "ordering": "parent_frozen_source_row_index_ascending",
        },
        "counts": {
            "source_rows": len(assembled),
            "chunks": len(chunks),
            "total_qwen_proxy_tokens": sum(token_counts.values()),
            "maximum_source_qwen_proxy_tokens": max(token_counts.values()),
            "total_source_utf8_bytes": sum(row["source_utf8_bytes"] for row in assembled),
        },
        "chunks": chunks,
        "network_calls": 0,
        "external_api_calls": 0,
        "external_texts_transmitted": 0,
        "worker_count": 0,
        "contains_source_text": False,
        "not_authorised": ["I3C worker input generation", "source text assignment", "I3C extraction", "retrieval", "embedding", "reranking"],
    }
    write_json_new(root / CHUNK_PLAN, chunk_plan)

    report = {
        "schema_version": "rq2b-v12-assembled-source-preflight-v1",
        "version_id": VERSION_ID,
        "state": "local_assembled_source_preflight_complete_extraction_unauthorised",
        "approval_receipt": {"path": APPROVAL_RECEIPT, "sha256": sha256_file(receipt_path)},
        "parent_source_manifest": {"path": PARENT_SOURCE_MANIFEST, "sha256": sha256_file(parent_path), "rows": len(parent_rows)},
        "background_overlay_manifest": {"path": OVERLAY_MANIFEST, "sha256": sha256_file(overlay_path), "rows": len(overlay_rows)},
        "assembled_source_manifest": {"path": SOURCE_MANIFEST, "sha256": sha256_file(root / SOURCE_MANIFEST), "rows": len(assembled)},
        "reuse": {"replacement_family": "background_scale", "replaced_sources": len(overlay_rows), "unchanged_sources_exactly_reused": len(reused_unchanged)},
        "integrity": {
            "source_row_indices_contiguous": [row["source_row_index"] for row in assembled] == list(range(2433)),
            "unique_skill_ids": len({row["skill_id"] for row in assembled}),
            "families": dict(sorted(Counter(row["family"] for row in assembled).items())),
            "background_scaffold_lint_match_counts": dict(sorted(background_lint.items())),
            "nonbackground_keyword_matches": nonbackground_keyword_matches,
        },
        "chunk_plan": {"path": CHUNK_PLAN, "sha256": sha256_file(root / CHUNK_PLAN), **chunk_plan["counts"]},
        "network_calls": 0,
        "external_api_calls": 0,
        "external_texts_transmitted": 0,
        "worker_count": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_results_written": False,
        "next_gate": "build and review a new exact source-text assignment approval packet before generating worker inputs or assigning extraction",
    }
    write_json_new(root / PREFLIGHT_REPORT, report)
    print(json.dumps({
        "source_manifest_sha256": report["assembled_source_manifest"]["sha256"],
        "chunk_plan_sha256": report["chunk_plan"]["sha256"],
        "report_sha256": sha256_file(root / PREFLIGHT_REPORT),
        "reuse": report["reuse"],
        "chunk_counts": chunk_plan["counts"],
        "nonbackground_keyword_match_count": len(nonbackground_keyword_matches),
        "network_calls": 0,
        "external_api_calls": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
