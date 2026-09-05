#!/usr/bin/env python3
"""Build a source-free, exact RQ2b v1.2 I3C assignment approval packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
ROOT_RELATIVE = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
SOURCE_MANIFEST = f"{ROOT_RELATIVE}/source_manifest.jsonl"
PREFLIGHT_REPORT = f"{ROOT_RELATIVE}/assembled_source_preflight.json"
CHUNK_PLAN = f"{ROOT_RELATIVE}/i3c_chunk_plan_metadata.json"
OVERLAY_MANIFEST = f"{ROOT_RELATIVE}/source_overlay_manifest.json"
EXTRACTION_PROMPT = "skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md"
PACKET_PATH = f"{ROOT_RELATIVE}/i3c_source_assignment_approval_packet.json"
MAX_REPLACEMENTS = 6
MAX_ACTIVE_WORKERS = 6
ALLOWED_INPUT_KEYS = {
    "source_row_index",
    "skill_id",
    "name",
    "description",
    "family",
    "source",
    "source_sha256",
    "text",
}
PROHIBITED_KEYS = {
    "prompt",
    "prompt_id",
    "gold_skill",
    "acceptable_skills",
    "valid_skills",
    "closest_alternatives",
    "stratum",
    "group",
    "role",
    "retrieval_result",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical_jsonl(rows: list[dict[str, Any]]) -> bytes:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
    ).encode("utf-8")


def planned_input_row(root: Path, source: dict[str, Any]) -> dict[str, Any]:
    raw = (root / source["source_path"]).read_bytes()
    text = raw.decode("utf-8")
    if sha256_bytes(raw) != source["source_sha256"]:
        raise ValueError(f"Source drift: {source['skill_id']}")
    row = {
        "source_row_index": source["source_row_index"],
        "skill_id": source["skill_id"],
        "name": source["source_name"],
        "description": source["source_description"],
        "family": source["family"],
        "source": source["source_path"],
        "source_sha256": source["source_sha256"],
        "text": text,
    }
    if set(row) != ALLOWED_INPUT_KEYS or set(row) & PROHIBITED_KEYS:
        raise ValueError(f"Planned input schema violation: {source['skill_id']}")
    return row


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    output = root / PACKET_PATH
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite approval packet: {output}")
    sources = read_jsonl(root / SOURCE_MANIFEST)
    report = read_json(root / PREFLIGHT_REPORT)
    plan = read_json(root / CHUNK_PLAN)
    if report["state"] != "local_assembled_source_preflight_complete_extraction_unauthorised":
        raise ValueError("Assembled-source preflight is incomplete")
    if plan["state"] != "local_chunk_plan_only_no_worker_inputs":
        raise ValueError("Chunk plan has unsafe state")
    if len(sources) != 2433 or report["assembled_source_manifest"]["sha256"] != sha256_file(root / SOURCE_MANIFEST):
        raise ValueError("Source manifest identity mismatch")
    if plan["source_manifest"]["sha256"] != sha256_file(root / SOURCE_MANIFEST):
        raise ValueError("Chunk plan source-manifest mismatch")

    source_by_index = {row["source_row_index"]: row for row in sources}
    if sorted(source_by_index) != list(range(2433)):
        raise ValueError("Source row indices are not contiguous")

    records = []
    for planned in plan["chunks"]:
        indexes = range(planned["first_source_row_index"], planned["last_source_row_index"] + 1)
        source_rows = [source_by_index[index] for index in indexes]
        if len(source_rows) != planned["row_count"]:
            raise ValueError(f"Chunk row count mismatch: {planned['chunk_index']}")
        identity = [
            {
                "source_row_index": row["source_row_index"],
                "skill_id": row["skill_id"],
                "source_sha256": row["source_sha256"],
            }
            for row in source_rows
        ]
        identity_sha = sha256_bytes(json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        if identity_sha != planned["identity_sha256"]:
            raise ValueError(f"Chunk identity drift: {planned['chunk_index']}")
        payload = canonical_jsonl([planned_input_row(root, row) for row in source_rows])
        first_index = source_rows[0]["source_row_index"]
        last_index = source_rows[-1]["source_row_index"]
        filename = f"i3c_input_{planned['chunk_index']:04d}_{first_index:04d}_{last_index:04d}.jsonl"
        records.append({
            "chunk_index": planned["chunk_index"],
            "input_path": f"{ROOT_RELATIVE}/i3c_extraction/inputs/{filename}",
            "planned_input_sha256": sha256_bytes(payload),
            "expected_output_path": f"{ROOT_RELATIVE}/i3c_extraction/outputs/{filename.replace('i3c_input_', 'i3c_output_')}",
            "row_count": planned["row_count"],
            "first_source_row_index": first_index,
            "last_source_row_index": last_index,
            "qwen_proxy_tokens": planned["qwen_proxy_tokens"],
            "input_utf8_bytes": len(payload),
            "identity_sha256": identity_sha,
            "contains_source_text": False,
        })

    if sum(record["row_count"] for record in records) != 2433:
        raise ValueError("Packet chunk coverage mismatch")
    largest_rows = sorted(records, key=lambda row: (row["row_count"], -row["chunk_index"]), reverse=True)[:MAX_REPLACEMENTS]
    largest_bytes = sorted(records, key=lambda row: (row["input_utf8_bytes"], -row["chunk_index"]), reverse=True)[:MAX_REPLACEMENTS]
    largest_tokens = sorted(records, key=lambda row: (row["qwen_proxy_tokens"], -row["chunk_index"]), reverse=True)[:MAX_REPLACEMENTS]
    packet = {
        "schema_version": "rq2b-v12-i3c-source-assignment-approval-packet-v1",
        "version_id": VERSION_ID,
        "state": "draft_pending_explicit_source_assignment_approval",
        "purpose": "Bounded local Codex-worker I3C extraction only after explicit approval",
        "source_manifest": {"path": SOURCE_MANIFEST, "sha256": sha256_file(root / SOURCE_MANIFEST), "rows": len(sources)},
        "preflight_report": {"path": PREFLIGHT_REPORT, "sha256": sha256_file(root / PREFLIGHT_REPORT)},
        "chunk_plan": {"path": CHUNK_PLAN, "sha256": sha256_file(root / CHUNK_PLAN)},
        "background_overlay": {"path": OVERLAY_MANIFEST, "sha256": sha256_file(root / OVERLAY_MANIFEST)},
        "extraction_prompt": {"path": EXTRACTION_PROMPT, "sha256": sha256_file(root / EXTRACTION_PROMPT)},
        "implementation": {
            "packet_builder": "skill_benchmark/scripts/build_rq2b_v12_i3c_source_assignment_packet.py",
            "packet_builder_sha256": sha256_file(Path(__file__).resolve()),
            "future_materializer_required": True,
        },
        "scope": {
            "destination": "Codex subagents only",
            "texts": 2433,
            "source_utf8_bytes": sum(row["source_utf8_bytes"] for row in sources),
            "local_qwen_proxy_tokens": sum(record["qwen_proxy_tokens"] for record in records),
            "chunks": len(records),
            "maximum_active_workers": MAX_ACTIVE_WORKERS,
            "worker_reasoning": "low",
            "flush_every_completed_rows": 10,
            "maximum_replacement_assignments": MAX_REPLACEMENTS,
            "maximum_total_assignment_attempts": len(records) + MAX_REPLACEMENTS,
            "maximum_assigned_source_rows": 2433 + sum(row["row_count"] for row in largest_rows),
            "maximum_assigned_source_utf8_bytes": sum(record["input_utf8_bytes"] for record in records) + sum(row["input_utf8_bytes"] for row in largest_bytes),
            "maximum_assigned_qwen_proxy_tokens": sum(record["qwen_proxy_tokens"] for record in records) + sum(row["qwen_proxy_tokens"] for row in largest_tokens),
        },
        "worker_contract": {
            "input_fields": sorted(ALLOWED_INPUT_KEYS),
            "prohibited_source_metadata": sorted(PROHIBITED_KEYS),
            "output": "exactly one JSON object per input row at the bound output path",
            "required_validation_before_completion": [
                "JSONL parses",
                "row count equals input",
                "skill_id and source_row_index identity align",
                "evidence fields are exact source substrings",
            ],
        },
        "authorises_if_approved": [
            "materialise only the hash-bound I3C input JSONL files",
            "assign only those input JSONL files to at most six local Codex workers",
            "perform I3C extraction under the bound prompt",
            "run local automatic merge, identity, evidence, heading-only, duplicate-ID, and missing-ID gates",
            "build but not complete a fresh blinded manual-QA packet after automatic gates pass",
        ],
        "does_not_authorise": [
            "internet or external APIs",
            "DashScope/Qwen text transfer or paid calls",
            "hosted SkillRouter transfer or model execution",
            "scientific BM25, Qwen, or SkillRouter scoring",
            "manual-QA completion on the user's behalf",
            "thesis LaTeX/PDF result integration",
            "transfer of prompts, gold labels, alternatives, strata, groups, or retrieval outcomes",
        ],
        "packet_contains_source_text": False,
        "network_calls": 0,
        "external_api_calls": 0,
        "worker_count": 0,
        "chunks": records,
    }
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "packet": PACKET_PATH,
        "packet_sha256": sha256_file(output),
        "state": packet["state"],
        "scope": packet["scope"],
        "packet_contains_source_text": packet["packet_contains_source_text"],
        "network_calls": 0,
        "external_api_calls": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
