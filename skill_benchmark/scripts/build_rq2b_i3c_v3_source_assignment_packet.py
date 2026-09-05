#!/usr/bin/env python3
"""Build the source-free RQ2b I3C V3 local-extraction approval packet.

V3 is an extraction-policy correction over the unchanged V1.2 source corpus.
This builder never materialises or emits source text: it rebinds the already
hash-planned V1.2 input chunks, with a new extractor prompt and new output root.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
SOURCE_ROOT = f"skill_benchmark/rq2b_full_library/{SOURCE_VERSION_ID}"
V3_VERSION_ID = "rq2b-i3c-v3-2026-08-18"
V3_ROOT = f"skill_benchmark/rq2b_full_library/{V3_VERSION_ID}"
V2_PACKET = f"{SOURCE_ROOT}/i3c_source_assignment_approval_packet.json"
V2_PACKET_SHA256 = "472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe"
SOURCE_MANIFEST = f"{SOURCE_ROOT}/source_manifest.jsonl"
CHUNK_PLAN = f"{SOURCE_ROOT}/i3c_chunk_plan_metadata.json"
FAILURE_AUDIT = f"{SOURCE_ROOT}/i3c_manual_qa_calibrated_v6/failure_audit.json"
EXTRACTION_PROMPT = "skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V3.md"
MATERIALIZER = "skill_benchmark/scripts/materialize_rq2b_i3c_v3_inputs.py"
MERGER = "skill_benchmark/scripts/merge_rq2b_i3c_v3.py"
PACKET_PATH = f"{V3_ROOT}/source_assignment_approval_packet_sealed.json"

MAX_ACTIVE_WORKERS = 6
MAX_REPLACEMENT_ASSIGNMENTS = 6
PROHIBITED_SOURCE_METADATA = {
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
ALLOWED_INPUT_FIELDS = {
    "source_row_index",
    "skill_id",
    "name",
    "description",
    "family",
    "source",
    "source_sha256",
    "text",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    output = root / PACKET_PATH
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite V3 approval packet: {output}")

    v2_packet_path = root / V2_PACKET
    source_manifest_path = root / SOURCE_MANIFEST
    chunk_plan_path = root / CHUNK_PLAN
    audit_path = root / FAILURE_AUDIT
    prompt_path = root / EXTRACTION_PROMPT
    if sha256_file(v2_packet_path) != V2_PACKET_SHA256:
        raise ValueError("V1.2 approved source-assignment packet hash drift")
    materializer_path = root / MATERIALIZER
    merger_path = root / MERGER
    if not prompt_path.is_file() or not audit_path.is_file() or not materializer_path.is_file() or not merger_path.is_file():
        raise ValueError("V3 prompt, runner, or bound failure audit is missing")

    v2_packet = read_json(v2_packet_path)
    audit = read_json(audit_path)
    if v2_packet["source_manifest"]["sha256"] != sha256_file(source_manifest_path):
        raise ValueError("V1.2 source manifest does not match approved packet")
    if v2_packet["chunk_plan"]["sha256"] != sha256_file(chunk_plan_path):
        raise ValueError("V1.2 chunk plan does not match approved packet")
    if v2_packet["scope"]["texts"] != 2433 or len(v2_packet["chunks"]) != 57:
        raise ValueError("Unexpected V1.2 source scope")
    if audit["fieldless_public_description_audit"]["all_fields_empty_rows"] != 149:
        raise ValueError("Unexpected V3 correction-audit basis")

    chunks: list[dict[str, Any]] = []
    for v2_chunk in v2_packet["chunks"]:
        index = int(v2_chunk["chunk_index"])
        first = int(v2_chunk["first_source_row_index"])
        last = int(v2_chunk["last_source_row_index"])
        filename = f"i3c_input_{index:04d}_{first:04d}_{last:04d}.jsonl"
        chunks.append(
            {
                "chunk_index": index,
                "input_path": f"{V3_ROOT}/i3c_extraction/inputs/{filename}",
                "expected_output_path": f"{V3_ROOT}/i3c_extraction/outputs/{filename.replace('i3c_input_', 'i3c_output_')}",
                "planned_input_sha256": v2_chunk["planned_input_sha256"],
                "identity_sha256": v2_chunk["identity_sha256"],
                "row_count": int(v2_chunk["row_count"]),
                "first_source_row_index": first,
                "last_source_row_index": last,
                "input_utf8_bytes": int(v2_chunk["input_utf8_bytes"]),
                "qwen_proxy_tokens": int(v2_chunk["qwen_proxy_tokens"]),
                "contains_source_text": False,
            }
        )
    if sum(chunk["row_count"] for chunk in chunks) != 2433:
        raise ValueError("V3 packet row coverage mismatch")

    largest_by_rows = sorted(chunks, key=lambda chunk: (chunk["row_count"], -chunk["chunk_index"]), reverse=True)[:MAX_REPLACEMENT_ASSIGNMENTS]
    largest_by_bytes = sorted(chunks, key=lambda chunk: (chunk["input_utf8_bytes"], -chunk["chunk_index"]), reverse=True)[:MAX_REPLACEMENT_ASSIGNMENTS]
    largest_by_tokens = sorted(chunks, key=lambda chunk: (chunk["qwen_proxy_tokens"], -chunk["chunk_index"]), reverse=True)[:MAX_REPLACEMENT_ASSIGNMENTS]
    packet = {
        "schema_version": "rq2b-i3c-v3-source-assignment-approval-packet-v1",
        "version_id": V3_VERSION_ID,
        "state": "draft_pending_explicit_source_assignment_approval",
        "purpose": "Bounded local Codex-worker I3C V3 correction extraction only after explicit approval",
        "source_corpus": {
            "version_id": SOURCE_VERSION_ID,
            "source_manifest": {"path": SOURCE_MANIFEST, "sha256": sha256_file(source_manifest_path), "rows": 2433},
            "chunk_plan": {"path": CHUNK_PLAN, "sha256": sha256_file(chunk_plan_path), "chunks": 57},
            "prior_approved_packet": {"path": V2_PACKET, "sha256": V2_PACKET_SHA256},
        },
        "correction_basis": {
            "failure_audit": {"path": FAILURE_AUDIT, "sha256": sha256_file(audit_path)},
            "fieldless_public_original_rows": 149,
            "explicit_use_when_descriptions_in_fieldless_rows": 74,
            "requirements": [
                "inspect source-native YAML/frontmatter name and description before declaring a field absent",
                "use an exact raw source substring when a description is folded or line-wrapped",
                "retain canonical field placement even when serializer later omits an exact duplicate of fixed name/description metadata",
                "prefer a distinctive positive output artifact over a generic negative output statement",
                "do not selectively repair only sampled QA rows",
            ],
        },
        "extraction_prompt": {"path": EXTRACTION_PROMPT, "sha256": sha256_file(prompt_path)},
        "implementation": {
            "packet_builder": "skill_benchmark/scripts/build_rq2b_i3c_v3_source_assignment_packet.py",
            "packet_builder_sha256": sha256_file(Path(__file__).resolve()),
            "materializer": MATERIALIZER,
            "materializer_sha256": sha256_file(materializer_path),
            "merger": MERGER,
            "merger_sha256": sha256_file(merger_path),
            "future_qa_packet_builder_required": True,
        },
        "scope": {
            "destination": "local Codex subagents only",
            "texts": 2433,
            "source_utf8_bytes": sum(chunk["input_utf8_bytes"] for chunk in chunks),
            "local_qwen_proxy_tokens": sum(chunk["qwen_proxy_tokens"] for chunk in chunks),
            "chunks": len(chunks),
            "maximum_active_workers": MAX_ACTIVE_WORKERS,
            "worker_reasoning": "low",
            "flush_every_completed_rows": 10,
            "maximum_replacement_assignments": MAX_REPLACEMENT_ASSIGNMENTS,
            "maximum_total_assignment_attempts": len(chunks) + MAX_REPLACEMENT_ASSIGNMENTS,
            "maximum_assigned_source_rows": 2433 + sum(chunk["row_count"] for chunk in largest_by_rows),
            "maximum_assigned_source_utf8_bytes": sum(chunk["input_utf8_bytes"] for chunk in chunks) + sum(chunk["input_utf8_bytes"] for chunk in largest_by_bytes),
            "maximum_assigned_qwen_proxy_tokens": sum(chunk["qwen_proxy_tokens"] for chunk in chunks) + sum(chunk["qwen_proxy_tokens"] for chunk in largest_by_tokens),
        },
        "worker_contract": {
            "input_fields": sorted(ALLOWED_INPUT_FIELDS),
            "prohibited_source_metadata": sorted(PROHIBITED_SOURCE_METADATA),
            "output": "exactly one V2-schema JSON object per input row at the bound output path",
            "required_validation_before_completion": [
                "JSONL parses",
                "row count equals input",
                "skill_id and source_row_index identity align",
                "every evidence string is an exact source substring",
            ],
        },
        "authorises_if_approved": [
            "materialise only the hash-bound V3 input JSONL files from the already-local V1.2 source corpus",
            "assign only those input JSONL files to at most six local Codex workers",
            "perform I3C V3 extraction under the bound V3 prompt",
            "run local automatic identity, evidence, heading-only, duplicate-ID, and missing-ID gates",
            "build but not complete a fresh calibrated blinded extraction-fidelity QA packet after automatic gates pass",
        ],
        "does_not_authorise": [
            "internet or external APIs",
            "DashScope/Qwen text transfer or paid calls",
            "hosted SkillRouter transfer or model execution",
            "scientific BM25, Qwen, or SkillRouter scoring",
            "manual QA completion on the user's behalf",
            "thesis LaTeX/PDF result integration",
            "transfer of prompts, gold labels, alternatives, strata, groups, or retrieval outcomes",
        ],
        "packet_contains_source_text": False,
        "network_calls": 0,
        "external_api_calls": 0,
        "worker_count": 0,
        "chunks": chunks,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "packet": PACKET_PATH,
                "packet_sha256": sha256_file(output),
                "state": packet["state"],
                "scope": packet["scope"],
                "packet_contains_source_text": packet["packet_contains_source_text"],
                "network_calls": 0,
                "external_api_calls": 0,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
