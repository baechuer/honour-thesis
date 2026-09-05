#!/usr/bin/env python3
"""Shared constants and hash-safe I/O for the frozen RQ2b study."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Iterable


VERSION_ID = "rq2b-full-library-v1-2026-08-02"
APPROVED_SCOPE_SHA256 = (
    "f797343f85aa8ab01ecb4c43ca5eec2d6fbbe79eec61a6f1aa5466208f86f687"
)
APPROVED_PACKET_SHA256 = (
    "2a78d7fea84722121807b7690baf4b7a4863c4d1683d97aa8376082606b12c84"
)
APPROVED_PROTOCOL_SHA256 = (
    "190b186a256e5959ee99da99bf75f694020f6319c22e3d24dadfc0e5ef5535fb"
)
PROTOCOL_RELATIVE_PATH = (
    "thesis_notes/current/"
    "RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md"
)
APPROVAL_PACKET_RELATIVE_PATH = (
    "skill_benchmark/outputs/rq2b/preflight/protocol_approval_packet.json"
)
VERSION_RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
IMPLEMENTATION_SEAL_RELATIVE_PATH = f"{VERSION_RELATIVE_ROOT}/b1s_implementation_seal.json"
B1R_PACKET_RELATIVE_PATH = f"{VERSION_RELATIVE_ROOT}/b1r_authorisation_packet.json"
B1R_RECEIPT_RELATIVE_PATH = f"{VERSION_RELATIVE_ROOT}/b1r_approval_receipt.json"
B0F_A1_AMENDMENT_RELATIVE_PATH = (
    f"{VERSION_RELATIVE_ROOT}/b0f_a1_skillrouter_embedding_amendment.json"
)
B0F_A1_AMENDMENT_SHA256 = (
    "cb87d9f659f18288b92c55c06e2da8ac206a53b4ad0789dce92710b2148bac1d"
)
B0F_A1_RECEIPT_RELATIVE_PATH = (
    f"{VERSION_RELATIVE_ROOT}/b0f_a1_skillrouter_embedding_approval_receipt.json"
)
B1R_MAXIMUM_REPLACEMENTS = 6
B1R_MAXIMUM_ACTIVE_WORKERS = 6

LEXICAL_TOKEN_RE = re.compile(r"[a-z0-9]+")
WHITESPACE_RE = re.compile(r"\s+", re.UNICODE)

FIELD_SPECS = (
    ("use_conditions", "Use condition"),
    ("input_preconditions", "Input / precondition"),
    ("output_artifacts", "Output / artifact"),
    ("workflow_steps", "Workflow / procedure"),
    ("dependencies_resources", "Dependency / resource"),
    ("constraints_boundaries", "Boundary / not-for"),
    ("success_criteria", "Success / verification"),
)

RQ2B_IMPLEMENTATION_SCRIPT_PATHS = (
    "skill_benchmark/scripts/rq2b_common.py",
    "skill_benchmark/scripts/audit_rq2b_token_limits.py",
    "skill_benchmark/scripts/freeze_rq2b_protocol.py",
    "skill_benchmark/scripts/build_rq2b_representations.py",
    "skill_benchmark/scripts/build_rq2b_i3c_transfer_packet.py",
    "skill_benchmark/scripts/audit_rq2b_exact_source_bytes.py",
    "skill_benchmark/scripts/rq2b_chunking.py",
    "skill_benchmark/scripts/smoke_rq2b_chunking.py",
    "skill_benchmark/scripts/merge_rq2b_i3c.py",
    "skill_benchmark/scripts/build_rq2b_i3c_qa_packet.py",
    "skill_benchmark/scripts/finalize_rq2b_i3c_qa.py",
    "skill_benchmark/scripts/build_rq2b_i3c_execution_ledger.py",
    "skill_benchmark/scripts/run_rq2b_bm25.py",
    "skill_benchmark/scripts/run_rq2b_qwen.py",
    "skill_benchmark/scripts/build_rq2b_qwen_payload.py",
    "skill_benchmark/scripts/run_rq2b_skillrouter_embedding.py",
    "skill_benchmark/scripts/build_rq2b_skillrouter_embedding_payload.py",
    "skill_benchmark/scripts/run_rq2b_skillrouter.py",
    "skill_benchmark/scripts/build_rq2b_skillrouter_payload.py",
    "skill_benchmark/scripts/rq2b_statistics.py",
    "skill_benchmark/scripts/analyze_rq2b_results.py",
    "skill_benchmark/scripts/build_rq2b_cost_ledger.py",
    "skill_benchmark/scripts/verify_rq2b_warm_state.py",
    "skill_benchmark/scripts/test_rq2b_local_pipeline.py",
    "skill_benchmark/scripts/build_rq2b_implementation_seal.py",
    "skill_benchmark/scripts/build_rq2b_b1r_authorisation_packet.py",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def version_root(root: Path | None = None) -> Path:
    return (root or repo_root()) / VERSION_RELATIVE_ROOT


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_json(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def relative(path: Path, root: Path | None = None) -> str:
    base = (root or repo_root()).resolve()
    return path.resolve().relative_to(base).as_posix()


def b1r_chunk_inventory(extraction: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "chunk_index": row["chunk_index"],
            "input_path": row["input_path"],
            "input_sha256": row["input_sha256"],
            "expected_output_path": row["expected_output_path"],
            "row_count": row["row_count"],
            "qwen_proxy_tokens": row["qwen_proxy_tokens"],
            "utf8_bytes": row["utf8_bytes"],
        }
        for row in extraction["chunks"]
    ]


def b1r_scope_for_extraction(extraction: dict[str, Any]) -> dict[str, Any]:
    chunks = b1r_chunk_inventory(extraction)
    largest_by_rows = sorted(
        chunks,
        key=lambda row: (row["row_count"], -row["chunk_index"]),
        reverse=True,
    )[:B1R_MAXIMUM_REPLACEMENTS]
    largest_by_bytes = sorted(
        chunks,
        key=lambda row: (row["utf8_bytes"], -row["chunk_index"]),
        reverse=True,
    )[:B1R_MAXIMUM_REPLACEMENTS]
    largest_by_tokens = sorted(
        chunks,
        key=lambda row: (row["qwen_proxy_tokens"], -row["chunk_index"]),
        reverse=True,
    )[:B1R_MAXIMUM_REPLACEMENTS]
    return {
        "stage": "B1R",
        "version_id": VERSION_ID,
        "destination": "Codex subagents only",
        "purpose": "I3C extraction under I3C_SUBAGENT_EXTRACTION_V2",
        "texts": extraction["counts"]["input_rows"],
        "source_utf8_bytes": extraction["counts"]["total_source_utf8_bytes"],
        "local_qwen_proxy_tokens": extraction["counts"]["total_qwen_proxy_tokens"],
        "chunks": extraction["counts"]["chunks"],
        "maximum_replacement_assignments": B1R_MAXIMUM_REPLACEMENTS,
        "maximum_total_assignment_attempts": extraction["counts"]["chunks"] + B1R_MAXIMUM_REPLACEMENTS,
        "maximum_assigned_source_rows": extraction["counts"]["input_rows"]
        + sum(row["row_count"] for row in largest_by_rows),
        "maximum_assigned_source_utf8_bytes": extraction["counts"]["total_source_utf8_bytes"]
        + sum(row["utf8_bytes"] for row in largest_by_bytes),
        "maximum_assigned_qwen_proxy_tokens": extraction["counts"]["total_qwen_proxy_tokens"]
        + sum(row["qwen_proxy_tokens"] for row in largest_by_tokens),
        "maximum_active_workers": B1R_MAXIMUM_ACTIVE_WORKERS,
        "worker_reasoning": "low",
        "flush_every_completed_rows": 10,
        "authorises": [
            "send only the exact hash-bound chunk input text to Codex subagents",
            "write exactly one JSON object per input row to the bound output paths",
            "run automatic local merge, evidence, identity, heading, duplicate, and missing-ID gates",
            "build the blinded 120-row manual-QA packet after automatic gates pass",
        ],
        "does_not_authorise": [
            "internet or external API use",
            "DashScope/Qwen text transfer or paid calls",
            "hosted SkillRouter transfer or model execution",
            "scientific BM25, Qwen, or SkillRouter scoring",
            "manual-QA completion on the user's behalf",
            "thesis LaTeX/PDF result integration",
            "transfer of prompts, gold labels, alternatives, strata, groups, or retrieval outcomes",
        ],
    }


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue
            try:
                value = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected one JSON object")
            rows.append(value)
    return rows


def _atomic_replace(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_bytes_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen artifact: {path}")
    _atomic_replace(path, payload)


def write_text_new(path: Path, value: str) -> None:
    write_bytes_new(path, value.encode("utf-8"))


def write_json_new(path: Path, value: Any) -> None:
    write_text_new(
        path,
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen artifact: {path}")
    materialized = list(rows)
    payload = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
        for row in materialized
    )
    write_text_new(path, payload)
    return len(materialized)


def lexical_tokens(value: str) -> list[str]:
    return LEXICAL_TOKEN_RE.findall(value.lower())


def normalize_whitespace(value: str) -> str:
    normalized_lines = value.replace("\r\n", "\n").replace("\r", "\n")
    return WHITESPACE_RE.sub(" ", normalized_lines.strip())


def source_length_quartiles(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Assign deterministic equal-count selector-length quartiles."""
    require(bool(rows), "Cannot assign source-length quartiles to an empty corpus")
    require(len({row["skill_id"] for row in rows}) == len(rows), "Source-length quartile skill IDs are not unique")
    ordered = sorted(
        rows,
        key=lambda row: (
            int(row["selector_visible_counts"]["utf8_bytes"]),
            row["skill_id"],
        ),
    )
    return {
        row["skill_id"]: f"q{min(3, rank * 4 // len(ordered)) + 1}"
        for rank, row in enumerate(ordered)
    }


def serialize_i1(name: str, description: str) -> str:
    require(bool(name.strip()), "I1 source-native name is empty")
    require(bool(description.strip()), "I1 source-native description is empty")
    return f"name: {name}\ndescription: {description}"


def selector_evidence_spans(
    extraction: dict[str, Any],
    *,
    source_text: str,
    name: str,
    description: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fields = extraction.get("fields")
    require(isinstance(fields, dict), "I3C extraction fields must be an object")
    retained: list[dict[str, Any]] = []
    omitted: list[dict[str, Any]] = []
    blocked = {normalize_whitespace(name), normalize_whitespace(description)}
    seen = set(blocked)
    for field_index, (field_key, label) in enumerate(FIELD_SPECS):
        items = fields.get(field_key)
        require(isinstance(items, list), f"I3C field must be an array: {field_key}")
        ordered: list[tuple[int, str, int, dict[str, Any], str]] = []
        for input_index, item in enumerate(items):
            require(isinstance(item, dict), f"I3C item must be an object: {field_key}")
            evidence = item.get("evidence")
            require(isinstance(evidence, str), f"I3C evidence must be text: {field_key}")
            require(bool(evidence), f"I3C evidence must not be empty: {field_key}")
            source_position = source_text.find(evidence)
            require(source_position >= 0, f"I3C evidence is not an exact source substring: {field_key}")
            normalized = normalize_whitespace(evidence)
            require(bool(normalized), f"I3C evidence normalizes to empty text: {field_key}")
            ordered.append(
                (
                    source_position,
                    str(item.get("id") or ""),
                    input_index,
                    item,
                    normalized,
                )
            )
        for source_position, item_id, input_index, item, normalized in sorted(
            ordered, key=lambda value: (value[0], value[1], value[2])
        ):
            record = {
                "field_index": field_index,
                "field_key": field_key,
                "field_label": label,
                "item_id": item_id,
                "source_position": source_position,
                "evidence": item["evidence"],
                "selector_evidence": normalized,
            }
            if normalized in seen:
                record["omission_reason"] = (
                    "exact_name_or_description_duplicate"
                    if normalized in blocked
                    else "global_exact_evidence_duplicate"
                )
                omitted.append(record)
                continue
            seen.add(normalized)
            retained.append(record)
    return retained, omitted


def serialize_i3c(
    name: str,
    description: str,
    retained_spans: list[dict[str, Any]],
) -> str:
    sections = [serialize_i1(name, description)]
    for field_key, label in FIELD_SPECS:
        values = [
            row["selector_evidence"]
            for row in retained_spans
            if row["field_key"] == field_key
        ]
        if values:
            sections.append(f"{label}:\n" + "\n".join(f"- {value}" for value in values))
    return "\n\n".join(sections)


def serialize_i3_flat(
    name: str,
    description: str,
    retained_spans: list[dict[str, Any]],
) -> str:
    base = serialize_i1(name, description)
    if not retained_spans:
        return base
    return base + "\n\n" + "\n".join(
        f"- {row['selector_evidence']}" for row in retained_spans
    )


def selector_counts(value: str) -> dict[str, int]:
    return {
        "characters": len(value),
        "utf8_bytes": len(value.encode("utf-8")),
        "lexical_tokens": len(lexical_tokens(value)),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_approval_packet(root: Path | None = None) -> dict[str, Any]:
    base = (root or repo_root()).resolve()
    packet_path = base / APPROVAL_PACKET_RELATIVE_PATH
    protocol_path = base / PROTOCOL_RELATIVE_PATH
    require(packet_path.exists(), f"Approval packet missing: {packet_path}")
    require(protocol_path.exists(), f"Protocol missing: {protocol_path}")
    require(
        sha256_file(packet_path) == APPROVED_PACKET_SHA256,
        "Approval packet hash differs from the explicitly approved packet",
    )
    require(
        sha256_file(protocol_path) == APPROVED_PROTOCOL_SHA256,
        "Protocol hash differs from the explicitly approved protocol",
    )
    packet = read_json(packet_path)
    require(
        packet.get("scope_sha256") == APPROVED_SCOPE_SHA256,
        "Approval scope hash mismatch",
    )
    require(
        packet.get("state") == "awaiting_explicit_user_approval_not_frozen_not_result",
        "Unexpected approval packet state",
    )
    return packet


def verify_frozen_manifest(root: Path | None = None) -> dict[str, Any]:
    base = (root or repo_root()).resolve()
    frozen_root = version_root(base)
    manifest_path = frozen_root / "manifest.json"
    require(manifest_path.exists(), f"Frozen RQ2b manifest missing: {manifest_path}")
    manifest = read_json(manifest_path)
    require(
        manifest.get("schema_version") == "rq2b-frozen-corpus-manifest-v1",
        "Frozen manifest schema mismatch",
    )
    require(manifest.get("version_id") == VERSION_ID, "Frozen version mismatch")
    require(
        manifest.get("state") == "frozen_protocol_no_scientific_results",
        "Frozen manifest has an unsafe state",
    )
    require(
        manifest.get("approved_scope_sha256") == APPROVED_SCOPE_SHA256,
        "Frozen manifest scope mismatch",
    )
    for name, artifact in manifest.get("generated_artifacts", {}).items():
        path = base / artifact["path"]
        require(path.exists(), f"Frozen artifact missing ({name}): {path}")
        require(
            sha256_file(path) == artifact["sha256"],
            f"Frozen artifact drift ({name}): {path}",
        )
    file_manifest = read_jsonl(frozen_root / "file_manifest.jsonl")
    for row in file_manifest:
        if not row.get("live_hash_enforced"):
            continue
        path = base / row["path"]
        require(path.exists(), f"Frozen live input missing: {path}")
        require(
            sha256_file(path) == row["sha256"],
            f"Frozen live input drift: {path}",
        )
    return manifest


def verify_b0f_a1_amendment(
    root: Path | None = None,
    *,
    require_approval: bool = False,
) -> dict[str, Any]:
    """Verify the prospective SkillRouter-embedding amendment and optional receipt."""
    base = (root or repo_root()).resolve()
    amendment_path = base / B0F_A1_AMENDMENT_RELATIVE_PATH
    require(amendment_path.is_file(), f"B0F-A1 amendment missing: {amendment_path}")
    require(
        sha256_file(amendment_path) == B0F_A1_AMENDMENT_SHA256,
        "B0F-A1 amendment hash drift",
    )
    amendment = read_json(amendment_path)
    require(
        amendment.get("schema_version") == "rq2b-prospective-protocol-amendment-v1",
        "B0F-A1 amendment schema mismatch",
    )
    require(
        amendment.get("amendment_id")
        == "rq2b-b0f-a1-skillrouter-embedding-replication-v1",
        "B0F-A1 amendment identity mismatch",
    )
    require(
        amendment.get("frozen_parent_protocol", {}).get("sha256")
        == APPROVED_PROTOCOL_SHA256,
        "B0F-A1 parent protocol mismatch",
    )
    require(amendment.get("scientific_runs") == 0, "B0F-A1 records a scientific run")
    require(amendment.get("texts_transmitted") == 0, "B0F-A1 records text transfer")
    require(
        amendment.get("reporting_contract", {}).get("primary_hypotheses_unchanged")
        is True,
        "B0F-A1 changes the frozen primary family",
    )
    if not require_approval:
        return amendment

    receipt_path = base / B0F_A1_RECEIPT_RELATIVE_PATH
    require(receipt_path.is_file(), f"B0F-A1 approval receipt missing: {receipt_path}")
    receipt = read_json(receipt_path)
    require(
        receipt.get("schema_version") == "rq2b-b0f-a1-approval-receipt-v1",
        "B0F-A1 approval receipt schema mismatch",
    )
    require(
        receipt.get("state") == "approved_prospective_amendment_local_implementation_only",
        "B0F-A1 amendment has not received exact-hash approval",
    )
    require(
        receipt.get("approved_amendment_sha256") == B0F_A1_AMENDMENT_SHA256,
        "B0F-A1 receipt approves a different amendment",
    )
    require(
        receipt.get("scientific_execution_authorized") is False
        and receipt.get("external_text_transfer_authorized") is False,
        "B0F-A1 receipt crosses the scientific execution boundary",
    )
    return {"amendment": amendment, "receipt": receipt}


def verify_i3c_retrieval_ready(root: Path | None = None) -> dict[str, Any]:
    """Verify extraction execution, immutable merge, and separate manual QA."""
    base = (root or repo_root()).resolve()
    verify_frozen_manifest(base)
    # Imported lazily because the execution-ledger builder itself uses this module.
    from build_rq2b_i3c_execution_ledger import verify as verify_execution_ledger

    verify_execution_ledger(base)
    frozen_root = version_root(base)
    i3_manifest_path = frozen_root / "i3c_merged" / "manifest.json"
    qa_packet_path = frozen_root / "i3c_manual_qa" / "manifest.json"
    decision_path = frozen_root / "i3c_manual_qa" / "manual_qa_decision.json"
    require(i3_manifest_path.exists(), "Merged I3C manifest is missing")
    require(qa_packet_path.exists(), "I3C manual-QA packet is missing")
    require(decision_path.exists(), "I3C manual-QA decision is missing")

    i3_manifest = read_json(i3_manifest_path)
    require(
        i3_manifest.get("state") == "automatic_gates_passed_manual_qa_pending",
        "Merged I3C automatic-gate state mismatch",
    )
    for name, artifact in i3_manifest.get("artifacts", {}).items():
        path = base / artifact["path"]
        require(path.exists(), f"Merged I3C artifact missing ({name}): {path}")
        require(sha256_file(path) == artifact["sha256"], f"Merged I3C artifact drift: {name}")

    packet = read_json(qa_packet_path)
    require(packet.get("state") == "blinded_review_pending", "I3C QA packet state mismatch")
    require(
        packet.get("i3c_manifest_sha256") == sha256_file(i3_manifest_path),
        "I3C QA packet does not bind the current merge manifest",
    )
    for name, artifact in packet.get("artifacts", {}).items():
        path = base / artifact["path"]
        require(path.exists(), f"I3C QA artifact missing ({name}): {path}")
        require(sha256_file(path) == artifact["sha256"], f"I3C QA artifact drift: {name}")

    decision = read_json(decision_path)
    require(
        decision.get("schema_version") == "rq2b-i3c-manual-qa-decision-v1",
        "I3C QA decision schema mismatch",
    )
    require(decision.get("version_id") == VERSION_ID, "I3C QA decision version mismatch")
    require(
        decision.get("state") == "manual_qa_passed_retrieval_ready"
        and decision.get("retrieval_ready") is True,
        "I3C manual QA has not passed",
    )
    require(
        decision.get("packet_manifest", {}).get("sha256") == sha256_file(qa_packet_path),
        "I3C QA decision does not bind the current QA packet",
    )
    completed = decision.get("completed_review_form", {})
    completed_path = base / completed.get("path", "")
    require(completed_path.is_file(), "Completed I3C QA review form is missing")
    require(
        sha256_file(completed_path) == completed.get("sha256"),
        "Completed I3C QA review form drift",
    )
    require(completed.get("rows") == 120, "Completed I3C QA review row count mismatch")
    return decision


def verify_b1s_implementation_seal(root: Path | None = None) -> dict[str, Any]:
    """Verify the zero-network implementation seal and every artifact it binds."""
    base = (root or repo_root()).resolve()
    verify_frozen_manifest(base)
    verify_b0f_a1_amendment(base, require_approval=True)
    seal_path = base / IMPLEMENTATION_SEAL_RELATIVE_PATH
    require(seal_path.exists(), f"B1S implementation seal missing: {seal_path}")
    seal = read_json(seal_path)
    require(
        seal.get("schema_version") == "rq2b-b1s-implementation-seal-v1",
        "B1S implementation seal schema mismatch",
    )
    require(seal.get("version_id") == VERSION_ID, "B1S implementation seal version mismatch")
    require(
        seal.get("b0f_a1_amendment_sha256") == B0F_A1_AMENDMENT_SHA256,
        "B1S seal does not bind the approved B0F-A1 amendment",
    )
    require(
        seal.get("state") == "implementation_sealed_no_scientific_execution",
        "B1S implementation seal state mismatch",
    )
    require(seal.get("network_calls") == 0, "B1S implementation seal records network calls")
    require(seal.get("scientific_selector_runs") == 0, "B1S seal records scientific runs")
    require(seal.get("external_texts_transmitted") == 0, "B1S seal records external transfer")
    require(seal.get("thesis_results_written") is False, "B1S seal records thesis-result writing")
    for section in ("bound_artifacts", "implementation_scripts"):
        for name, artifact in seal.get(section, {}).items():
            path = base / artifact["path"]
            require(path.exists(), f"B1S bound file missing ({name}): {path}")
            require(sha256_file(path) == artifact["sha256"], f"B1S bound file drift: {name}")
    review = seal.get("independent_review", {})
    require(review.get("verdict") == "PASS", "B1S independent review did not pass")
    require(review.get("eligible_as_final_approval") is True, "B1S review is not eligible as final approval")
    require(review.get("network_calls") == 0, "B1S review used network")
    require(review.get("scientific_runs") == 0, "B1S review performed a scientific run")
    require(review.get("edits_made") is False, "B1S review was not read-only")
    require(
        review.get("prohibited_artifacts_read") is False,
        "B1S review read prohibited source or benchmark artifacts",
    )
    finding_counts = review.get("finding_counts")
    require(
        isinstance(finding_counts, dict)
        and set(finding_counts) == {"P0", "P1", "P2"}
        and all(
            isinstance(finding_counts[key], int)
            and not isinstance(finding_counts[key], bool)
            and finding_counts[key] >= 0
            for key in ("P0", "P1", "P2")
        ),
        "B1S review finding counts are invalid",
    )
    require(
        finding_counts["P0"] == finding_counts["P1"] == 0,
        "B1S review cannot pass with P0 or P1 findings",
    )
    boundaries = seal.get("production_boundaries", {})
    require(boundaries.get("i3c_worker_outputs") == 0, "B1S seal found I3C worker outputs")
    require(boundaries.get("i3c_merged_exists") is False, "B1S seal found merged I3C")
    require(boundaries.get("qwen_payload_exists") is False, "B1S seal found a Qwen payload")
    require(
        boundaries.get("skillrouter_embedding_payload_exists") is False,
        "B1S seal found a SkillRouter embedding payload",
    )
    require(
        len(seal.get("implementation_scripts", {}))
        == len(RQ2B_IMPLEMENTATION_SCRIPT_PATHS),
        "B1S implementation-script count mismatch",
    )
    return seal


def verify_b1r_execution_authorised(root: Path | None = None) -> dict[str, Any]:
    """Verify the later explicit B1R source-transfer approval receipt."""
    base = (root or repo_root()).resolve()
    seal = verify_b1s_implementation_seal(base)
    packet_path = base / B1R_PACKET_RELATIVE_PATH
    receipt_path = base / B1R_RECEIPT_RELATIVE_PATH
    require(packet_path.is_file(), f"B1R authorisation packet missing: {packet_path}")
    require(receipt_path.is_file(), f"B1R approval receipt missing: {receipt_path}")
    packet = read_json(packet_path)
    receipt = read_json(receipt_path)
    require(
        set(packet)
        == {
            "schema_version",
            "version_id",
            "state",
            "network_calls",
            "external_texts_transmitted",
            "workers_started",
            "scope",
            "scope_sha256",
            "implementation_seal",
            "i3c_extraction_manifest",
            "extraction_prompt",
            "chunks",
            "execution_requirements",
            "worker_event_ledger",
            "next_action",
            "approval_receipt_contract",
        },
        "B1R packet key mismatch",
    )
    require(packet.get("schema_version") == "rq2b-b1r-authorisation-packet-v1", "B1R packet schema mismatch")
    require(packet.get("version_id") == VERSION_ID, "B1R packet version mismatch")
    require(packet.get("state") == "awaiting_explicit_b1r_source_transfer_approval", "B1R packet state mismatch")
    require(packet.get("network_calls") == 0, "B1R packet records network calls")
    require(packet.get("external_texts_transmitted") == 0, "B1R packet records source transfer")
    require(packet.get("workers_started") == 0, "B1R packet records started workers")

    extraction_path = base / VERSION_RELATIVE_ROOT / "i3c_extraction" / "manifest.json"
    require(extraction_path.is_file(), "B1R extraction manifest is missing")
    extraction = read_json(extraction_path)
    require(extraction.get("state") == "built_not_transmitted", "B1R extraction packet state mismatch")
    require(extraction.get("external_texts_transmitted") == 0, "B1R extraction packet records transfer")
    require(extraction.get("worker_count") == 0, "B1R extraction packet records workers")
    expected_scope = b1r_scope_for_extraction(extraction)
    require(packet.get("scope") == expected_scope, "B1R packet scope differs from the frozen contract")
    require(packet.get("scope_sha256") == sha256_json(expected_scope), "B1R packet scope hash mismatch")
    require(expected_scope["maximum_active_workers"] == 6, "B1R active-worker ceiling is not six")
    require(packet.get("chunks") == b1r_chunk_inventory(extraction), "B1R chunk inventory drift")
    require(packet.get("extraction_prompt") == extraction.get("extraction_prompt"), "B1R extraction-prompt binding mismatch")
    require(
        packet.get("implementation_seal")
        == {
            "path": IMPLEMENTATION_SEAL_RELATIVE_PATH,
            "sha256": sha256_file(base / IMPLEMENTATION_SEAL_RELATIVE_PATH),
            "state": seal["state"],
        },
        "B1R implementation-seal binding mismatch",
    )
    require(
        packet.get("i3c_extraction_manifest")
        == {
            "path": f"{VERSION_RELATIVE_ROOT}/i3c_extraction/manifest.json",
            "sha256": sha256_file(extraction_path),
        },
        "B1R extraction-manifest binding mismatch",
    )
    require(
        packet.get("execution_requirements")
        == {
            "use_only_assigned_input_artifact_text": True,
            "read_frozen_extraction_prompt": True,
            "one_json_object_per_input_row": True,
            "validate_jsonl_row_identity_and_exact_evidence": True,
            "record_hash_bound_worker_event_per_explicit_assignment": True,
            "close_completed_or_failed_workers": True,
            "no_duplicate_active_assignments": True,
            "stop_on_hash_or_identity_failure": True,
            "no_automatic_retries": True,
            "replacement_assignments_must_be_explicit_and_event_logged": True,
        },
        "B1R execution-requirement contract mismatch",
    )
    require(
        packet.get("worker_event_ledger")
        == {
            "path": f"{VERSION_RELATIVE_ROOT}/i3c_extraction/worker_events.jsonl",
            "schema_version": "rq2b-i3c-worker-event-v1",
            "record_failed_replacements": True,
            "count_repeated_assignments_in_transfer_and_time_costs": True,
        },
        "B1R worker-event contract mismatch",
    )
    require(
        packet.get("approval_receipt_contract")
        == {
            "path": B1R_RECEIPT_RELATIVE_PATH,
            "schema_version": "rq2b-b1r-approval-receipt-v1",
            "state": "explicitly_approved_for_b1r_once",
            "must_bind_packet_and_scope_hashes": True,
        },
        "B1R approval-receipt contract mismatch",
    )
    require(
        packet.get("next_action")
        == "obtain explicit user approval of this packet and scope hash before spawning any worker",
        "B1R next-action contract mismatch",
    )
    require(receipt.get("schema_version") == "rq2b-b1r-approval-receipt-v1", "B1R receipt schema mismatch")
    require(receipt.get("version_id") == VERSION_ID, "B1R receipt version mismatch")
    require(receipt.get("state") == "explicitly_approved_for_b1r_once", "B1R source transfer is not approved")
    require(receipt.get("packet_sha256") == sha256_file(packet_path), "B1R receipt packet hash mismatch")
    require(receipt.get("scope_sha256") == packet.get("scope_sha256"), "B1R receipt scope hash mismatch")
    require(receipt.get("authorised_source_transfer") is True, "B1R receipt does not authorise source transfer")
    require(receipt.get("internet_or_external_api_authorised") is False, "B1R receipt unexpectedly authorises external APIs")
    require(receipt.get("scientific_scoring_authorised") is False, "B1R receipt unexpectedly authorises scientific scoring")
    require(receipt.get("thesis_result_writing_authorised") is False, "B1R receipt unexpectedly authorises thesis writing")
    return packet
