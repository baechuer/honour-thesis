#!/usr/bin/env python3
"""Build the V7 Phase-8 B2 dispatch without running either reranker.

The builder has two explicit stages.  ``--write-b1-receipt`` replays the
official label-free output validator over complete persisted B1 artifacts and
writes a hash-bound receipt.  ``--materialize`` replays that receipt and the
Phase-8 root, creates the exact runner-native Qwen and SkillRouter payloads,
runs only their tokenisation/preflight paths, and issues two unused one-use
releases.  No provider request, model load/forward, label join, metric, or
offline analysis is performed here.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


BUILDER_VERSION = "rq2b-v7-phase8-b2-dispatch-builder-v1"
B1_RECEIPT_SCHEMA = "rq2b-v7-phase8-b1-official-validation-receipt-v1"
APPROVAL_SCHEMA = "rq2b-v7-b36-c6-b2-user-execution-approval-v1"
DISPATCH_SCHEMA = "rq2b-v7-phase8-b2-dispatch-manifest-v1"
LEDGER_SCHEMA = "rq2b-v7-phase8-b2-one-use-release-ledger-v1"
INTEGRITY_SCHEMA = "rq2b-v7-phase8-b2-dispatch-integrity-v1"
PHASE8_ROOT_SCHEMA = "rq2b-v7-phase8-final-execution-root-v1"
PHASE8_RECEIPT_SCHEMA = "rq2b-v7-phase8-readiness-receipt-v1"
PHASE8_READY = "READY_FOR_FORMAL_EXPERIMENT"

EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
EXPECTED_B1_CELLS = 12
EXPECTED_B1_ROWS = EXPECTED_QUERIES * EXPECTED_B1_CELLS
EXPECTED_B2_MATERIALISED_CONDITIONS = 30
EXPECTED_B2_ROWS = EXPECTED_QUERIES * EXPECTED_B2_MATERIALISED_CONDITIONS
EXPECTED_CORE_OUTCOMES = 36
EXPECTED_DIAGNOSTIC_OUTCOMES = 6
TOP_K = 20
QWEN_PROVIDER_TOKEN_MULTIPLIER = 2
QWEN_WALL_SECONDS = 7 * 24 * 60 * 60
SKILLROUTER_WALL_SECONDS = 7 * 24 * 60 * 60

SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"

RUNTIME_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl"
)
SOURCE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/source_manifest.jsonl"
)
CORE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl"
)
BRIDGE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/fixed_candidate_bridge_conditions.jsonl"
)
VALIDATOR_REL = Path("skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py")

FIXED_INPUTS = {
    "runtime": {
        "path": RUNTIME_REL.as_posix(),
        "sha256": "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
        "rows": EXPECTED_QUERIES,
    },
    "source_manifest": {
        "path": SOURCE_REL.as_posix(),
        "sha256": "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
        "rows": EXPECTED_SOURCES,
    },
    "core_conditions": {
        "path": CORE_REL.as_posix(),
        "sha256": "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
        "rows": EXPECTED_CORE_OUTCOMES,
    },
    "bridge_conditions": {
        "path": BRIDGE_REL.as_posix(),
        "sha256": "d659ff98a5a2534478f68ab44794e4df7d89b23eb3a44a2fbf335cdca42366f7",
        "rows": EXPECTED_DIAGNOSTIC_OUTCOMES,
    },
}

RUNNER_SPECS = {
    "qwen_reranker_b2": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_qwen_reranker_b2.py",
        "runner_version": "rq2b-v7-qwen-reranker-b2-runner-v1",
        "payload_schema": "rq2b-v7-qwen-reranker-b2-phase8-payload-v1",
        "authorisation_schema": "rq2b-v7-qwen-reranker-b2-root-release-v1",
    },
    "skillrouter_reranker_b2": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_skillrouter_reranker_b2.py",
        "runner_version": "rq2b-v7-skillrouter-reranker-b2-runner-v1",
        "payload_schema": "rq2b-v7-skillrouter-reranker-b2-phase8-payload-v1",
        "authorisation_schema": "rq2b-v7-skillrouter-reranker-b2-root-release-v1",
    },
}

B1_CONDITIONS = tuple(f"B{index:02d}-G0" for index in range(1, 13))
I1_I2_ROOT_ROLES = {
    "I1-discovery": ("i1_discovery_v2", "SOURCE_NATIVE_PHASE7_V2"),
    "I2-original": ("i2_original_v2", "SOURCE_NATIVE_PHASE7_V2"),
}
I3_ROOT_ROLES = {
    "I3C-fielded": ("i3c_fielded", "I3C_SUBAGENT_EXTRACTION_V4_1"),
    "I3-flat": ("i3_flat", "I3C_SUBAGENT_EXTRACTION_V4_1"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    context = (
        gzip.open(path, "rt", encoding="utf-8", newline="")
        if path.suffix == ".gz"
        else path.open("r", encoding="utf-8", newline="")
    )
    rows: list[dict[str, Any]] = []
    with context as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected JSON object: {path}:{line_number}")
            rows.append(value)
    return rows


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def root_path(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: relative path required")
    supplied = Path(value)
    require(not supplied.is_absolute(), f"{field}: absolute path forbidden")
    resolved = (root / supplied).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return resolved


def write_json_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text_new(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(value)


def implementation_binding(root: Path, rel: Path) -> dict[str, str]:
    path = root / rel
    require(path.is_file(), f"Implementation missing: {rel}")
    return {"path": rel.as_posix(), "sha256": file_sha256(path)}


def literal_constants(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    wanted = {"RUNNER_VERSION", "PAYLOAD_SCHEMA", "AUTHORISATION_SCHEMA"}
    result: dict[str, Any] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                try:
                    result[target.id] = ast.literal_eval(node.value)
                except (TypeError, ValueError):
                    pass
    return result


def validate_approval(root: Path, path: Path) -> dict[str, Any]:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Approval record must be inside repository root") from error
    value = read_json(path)
    require(value.get("schema_version") == APPROVAL_SCHEMA, "Approval schema drift")
    require(value.get("decision") == "APPROVED", "B2 execution has not been explicitly approved")
    scope = value.get("scope", {})
    require(scope.get("frozen_library") == "V7_3798_SOURCES_1077_QUERIES", "Approval library scope drift")
    require(scope.get("experiment") == "B36_CORE_PLUS_C6_DIAGNOSTIC", "Approval experiment scope drift")
    require(scope.get("phase8_b2_prerequisite") is True, "Approval does not cover B2")
    require(scope.get("external_qwen_reranker") is True, "Approval does not cover Qwen reranking")
    require(scope.get("local_skillrouter_reranker") is True, "Approval does not cover SkillRouter reranking")
    require(value.get("secrets_recorded") is False, "Approval record must not contain secrets")
    quoted = value.get("user_instruction", {}).get("verbatim")
    require(
        isinstance(quoted, str) and "36个核心配置+6个诊断" in quoted,
        "Approval verbatim B36+C6 scope missing",
    )
    return value


def validate_runner_root_binding(root: Path, root_manifest: dict[str, Any], role: str) -> None:
    expected = RUNNER_SPECS[role]
    actual = root_manifest.get("runners", {}).get(role)
    require(isinstance(actual, dict), f"Phase-8 root missing runner: {role}")
    path = root / expected["path"]
    constants = literal_constants(path)
    require(constants.get("RUNNER_VERSION") == expected["runner_version"], f"{role}: runner literal drift")
    require(constants.get("PAYLOAD_SCHEMA") == expected["payload_schema"], f"{role}: payload literal drift")
    require(constants.get("AUTHORISATION_SCHEMA") == expected["authorisation_schema"], f"{role}: release literal drift")
    for key in ("path", "runner_version", "payload_schema", "authorisation_schema"):
        require(actual.get(key) == expected[key], f"{role}: Phase-8 root {key} drift")
    require(actual.get("sha256") == file_sha256(path), f"{role}: Phase-8 root runner hash drift")


def validate_phase8(
    root: Path, receipt_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, dict[str, dict[str, Any]]]:
    scripts = str((root / "skill_benchmark/scripts").resolve())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import build_rq2b_v7_phase8_b1_dispatch as b1_builder

    receipt, root_manifest, root_manifest_path, representations = b1_builder.validate_phase8(
        root, receipt_path
    )
    require(root_manifest.get("schema_version") == PHASE8_ROOT_SCHEMA, "Phase-8 root schema drift")
    require(root_manifest.get("status") == PHASE8_READY, "Phase-8 root is not READY")
    for role in RUNNER_SPECS:
        validate_runner_root_binding(root, root_manifest, role)
    return receipt, root_manifest, root_manifest_path, representations


def _official_b1_replay(root: Path, artifacts: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    scripts = str((root / "skill_benchmark/scripts").resolve())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import validate_rq2b_v7_runner_outputs as validator

    rows: list[dict[str, Any]] = []
    for index, item in enumerate(artifacts):
        require(set(item) == {"path", "sha256", "rows"}, f"B1 artifact {index}: fields drift")
        require(is_sha256(item["sha256"]), f"B1 artifact {index}: invalid SHA-256")
        path = root_path(root, item["path"], field=f"b1_artifacts[{index}].path")
        require(path.is_file(), f"B1 artifact {index}: missing")
        require(file_sha256(path) == item["sha256"], f"B1 artifact {index}: hash drift")
        artifact_rows = read_jsonl(path)
        require(len(artifact_rows) == item["rows"], f"B1 artifact {index}: row-count drift")
        rows.extend(artifact_rows)
    require(len(rows) == EXPECTED_B1_ROWS, "Persisted B1 row coverage is not exactly 12 x 1,077")
    authority = validator.RunnerAuthority.load()
    report = validator.validate_outputs(rows, [], authority, require_complete=False)
    condition_ids = sorted({str(row.get("condition_id")) for row in rows})
    require(condition_ids == list(B1_CONDITIONS), "Persisted B1 condition coverage drift")
    require(report == {
        "status": "PASS_LABEL_FREE_RUNNER_OUTPUT_VALIDATION",
        "queries": EXPECTED_QUERIES,
        "b1_cells": EXPECTED_B1_CELLS,
        "b2_materialised_conditions": EXPECTED_B2_MATERIALISED_CONDITIONS,
        "outcome_conditions": EXPECTED_CORE_OUTCOMES + EXPECTED_DIAGNOSTIC_OUTCOMES,
        "b1_rows": EXPECTED_B1_ROWS,
        "b2_rows": 0,
        "c2_alias_rows": 0,
        "complete_scope_required": False,
    }, "Official B1 replay report drift")
    return report, rows


def write_b1_receipt(
    *, root: Path, phase8_receipt_path: Path, artifact_paths: Iterable[Path], output_path: Path,
) -> dict[str, Any]:
    root = root.resolve()
    require(not output_path.exists(), "B1 validation receipt overwrite forbidden")
    try:
        output_path.resolve().relative_to(root)
    except ValueError as error:
        raise ValueError("B1 validation receipt must be inside repository root") from error
    _, _, root_manifest_path, _ = validate_phase8(root, phase8_receipt_path)
    artifacts: list[dict[str, Any]] = []
    for raw in artifact_paths:
        path = raw.resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise ValueError("B1 artifact must be inside repository root") from error
        rows = read_jsonl(path)
        artifacts.append({
            "path": relative(path, root),
            "sha256": file_sha256(path),
            "rows": len(rows),
        })
    require(bool(artifacts), "At least one B1 artifact is required")
    report, _ = _official_b1_replay(root, artifacts)
    receipt = {
        "schema_version": B1_RECEIPT_SCHEMA,
        "status": "PASS_FRESH_OFFICIAL_LABEL_FREE_B1_VALIDATION",
        "phase8": {
            "receipt": {"path": relative(phase8_receipt_path, root), "sha256": file_sha256(phase8_receipt_path)},
            "root_manifest": {"path": relative(root_manifest_path, root), "sha256": file_sha256(root_manifest_path)},
        },
        "official_validator": implementation_binding(root, VALIDATOR_REL),
        "b1_artifacts": artifacts,
        "b1_artifacts_bundle_sha256": canonical_sha256(artifacts),
        "condition_ids": list(B1_CONDITIONS),
        "b1_cells": EXPECTED_B1_CELLS,
        "b1_rows": EXPECTED_B1_ROWS,
        "official_report": report,
        "validation_mode": "CURRENT_VALIDATOR_REPLAY_COMPLETE_B1_WITH_EMPTY_B2",
        "validated_at_utc": utc_now(),
        "label_isolation": {
            "label_files_read": False,
            "acceptable_sets_read": False,
            "b2_results_read": False,
            "offline_scorer_run": False,
        },
    }
    write_json_new(output_path, receipt)
    return receipt


def validate_b1_receipt(
    root: Path, path: Path, *, phase8_receipt_path: Path, root_manifest_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    receipt = read_json(path)
    required = {
        "schema_version", "status", "phase8", "official_validator", "b1_artifacts",
        "b1_artifacts_bundle_sha256", "condition_ids", "b1_cells", "b1_rows",
        "official_report", "validation_mode", "validated_at_utc", "label_isolation",
    }
    require(set(receipt) == required, "B1 validation receipt fields drift")
    require(receipt["schema_version"] == B1_RECEIPT_SCHEMA, "B1 validation receipt schema drift")
    require(receipt["status"] == "PASS_FRESH_OFFICIAL_LABEL_FREE_B1_VALIDATION", "B1 receipt is not PASS")
    require(receipt["phase8"] == {
        "receipt": {"path": relative(phase8_receipt_path, root), "sha256": file_sha256(phase8_receipt_path)},
        "root_manifest": {"path": relative(root_manifest_path, root), "sha256": file_sha256(root_manifest_path)},
    }, "B1 receipt Phase-8 binding drift")
    require(receipt["official_validator"] == implementation_binding(root, VALIDATOR_REL), "B1 validator binding drift")
    artifacts = receipt["b1_artifacts"]
    require(isinstance(artifacts, list) and artifacts, "B1 artifact binding missing")
    require(receipt["b1_artifacts_bundle_sha256"] == canonical_sha256(artifacts), "B1 artifact bundle hash drift")
    report, rows = _official_b1_replay(root, artifacts)
    require(receipt["official_report"] == report, "B1 official replay receipt is stale")
    require(receipt["condition_ids"] == list(B1_CONDITIONS), "B1 receipt condition scope drift")
    require(receipt["b1_cells"] == EXPECTED_B1_CELLS and receipt["b1_rows"] == EXPECTED_B1_ROWS, "B1 receipt counts drift")
    require(receipt["validation_mode"] == "CURRENT_VALIDATOR_REPLAY_COMPLETE_B1_WITH_EMPTY_B2", "B1 receipt validation mode drift")
    require(receipt["label_isolation"] == {
        "label_files_read": False,
        "acceptable_sets_read": False,
        "b2_results_read": False,
        "offline_scorer_run": False,
    }, "B1 receipt label-isolation drift")
    return receipt, rows


def phase8_binding(receipt_path: Path, root: Path) -> dict[str, Any]:
    return {
        "status": "PASS",
        "receipt": {"path": relative(receipt_path, root), "sha256": file_sha256(receipt_path)},
        "final_v4_1_i3_hashes_bound": True,
    }


def build_payload(
    *, root: Path, role: str, phase8_receipt_path: Path,
    representations: dict[str, dict[str, Any]], b1_receipt_path: Path,
    b1_receipt: dict[str, Any],
) -> dict[str, Any]:
    require(role in RUNNER_SPECS, f"Unknown B2 role: {role}")
    if role == "qwen_reranker_b2":
        import run_rq2b_v7_qwen_reranker_b2 as runner
        implementation = {
            "runner": implementation_binding(root, Path(RUNNER_SPECS[role]["path"])),
            "qwen_contract_helper": implementation_binding(root, runner.HELPER_REL),
            "exact_chunker_v1": implementation_binding(root, runner.CHUNKER_V1_REL),
            "exact_chunker_v2": implementation_binding(root, runner.CHUNKER_V2_REL),
            "official_output_validator": implementation_binding(root, VALIDATOR_REL),
        }
        inputs = {
            **FIXED_INPUTS,
            "proxy_tokenizer": runner.PROXY_TOKENIZER,
            "representations": representations,
            "b1_artifacts": b1_receipt["b1_artifacts"],
        }
        alias_key = "c2_q_alias_rows"
    else:
        import run_rq2b_v7_skillrouter_reranker_b2 as runner
        implementation = {
            "runner": implementation_binding(root, Path(RUNNER_SPECS[role]["path"])),
            "official_output_validator": implementation_binding(root, VALIDATOR_REL),
        }
        inputs = {
            **FIXED_INPUTS,
            "representations": representations,
            "b1_artifacts": b1_receipt["b1_artifacts"],
        }
        alias_key = "c2_s_alias_rows"
    return {
        "schema_version": RUNNER_SPECS[role]["payload_schema"],
        "state": "SEALED_LABEL_FREE_PHASE8_B1_BOUND_PAYLOAD",
        "runner_version": RUNNER_SPECS[role]["runner_version"],
        "implementation": implementation,
        "phase8": phase8_binding(phase8_receipt_path, root),
        "inputs": inputs,
        "b1_validation": {
            "status": "PASS_12_PERSISTED_B1_CELLS",
            "receipt": {"path": relative(b1_receipt_path, root), "sha256": file_sha256(b1_receipt_path)},
            "condition_ids": list(B1_CONDITIONS),
            "rows": EXPECTED_B1_ROWS,
        },
        "counts": {
            "queries": EXPECTED_QUERIES,
            "sources": EXPECTED_SOURCES,
            "persisted_b1_cells": EXPECTED_B1_CELLS,
            "persisted_b1_rows": EXPECTED_B1_ROWS,
            "materialised_b2_conditions": 15,
            "materialised_b2_rows": 15 * EXPECTED_QUERIES,
            alias_key: 0,
        },
        "method": runner.method_contract(),
        "label_isolation": {
            "labels_or_results_read": False,
            "b1_candidates_regenerated": False,
            "offline_scorer_run": False,
        },
    }


def qwen_exact_counts(root: Path, payload: dict[str, Any]) -> dict[str, int]:
    import run_rq2b_v7_qwen_reranker_b2 as runner

    prompts, conditions, views, b1_by_key, _ = runner.load_authority(root, payload)
    tokenizer = runner.load_proxy_tokenizer(root)
    counts = runner.empty_workload_counts()
    window_caches: dict[str, dict[str, list[dict[str, Any]]]] = {
        representation: {} for representation in runner.REPRESENTATIONS
    }
    for condition_id in runner.MATERIALISED_CONDITIONS:
        condition = conditions[condition_id]
        representation_rows = views[condition["representation"]]
        source_b1_condition = runner.b1_condition_id(condition)
        for prompt in prompts:
            work = runner.build_condition_work(
                tokenizer,
                condition,
                prompt,
                b1_by_key[(source_b1_condition, prompt["prompt_id"])],
                representation_rows,
                window_cache=window_caches[condition["representation"]],
            )
            runner.add_workload_counts(counts, work)
    require(counts["rows"] == 15 * EXPECTED_QUERIES, "Qwen workload row-count drift")
    return counts


def qwen_ceilings(counts: dict[str, int]) -> dict[str, int]:
    return {
        "maximum_request_attempts": counts["requests"],
        "maximum_successful_calls": counts["requests"],
        "maximum_external_documents": counts["documents"],
        "maximum_external_submission_proxy_tokens": counts["proxy_tokens"],
        "maximum_external_submission_utf8_bytes": counts["utf8_bytes"],
        "maximum_provider_total_tokens": counts["proxy_tokens"] * QWEN_PROVIDER_TOKEN_MULTIPLIER,
        "maximum_wall_time_seconds": QWEN_WALL_SECONDS,
    }


def skillrouter_preflight(
    *, root: Path, payload: dict[str, Any], root_manifest: dict[str, Any], cache_dir: Path,
) -> dict[str, Any]:
    import run_rq2b_v7_skillrouter_reranker_b2 as runner
    from transformers import AutoTokenizer

    snapshot = root_manifest.get("models", {}).get("skillrouter_reranker")
    require(isinstance(snapshot, dict), "Phase-8 root lacks SkillRouter reranker snapshot")
    require(snapshot.get("repository") == runner.MODEL, "SkillRouter reranker repository drift")
    require(snapshot.get("revision") == runner.REVISION, "SkillRouter reranker revision drift")
    require(snapshot.get("files") == runner.MODEL_FILE_SHA256, "SkillRouter reranker model-file drift")
    snapshot_path = root_path(root, snapshot.get("snapshot_path"), field="models.skillrouter_reranker.snapshot_path")
    require(snapshot_path.is_dir(), "Pinned SkillRouter reranker snapshot is absent")
    for name, expected in runner.MODEL_FILE_SHA256.items():
        path = snapshot_path / name
        require(path.is_file() and file_sha256(path) == expected, f"SkillRouter snapshot hash drift: {name}")
    require(not cache_dir.exists(), "SkillRouter B2 cache namespace already exists")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    tokenizer = AutoTokenizer.from_pretrained(
        snapshot_path, local_files_only=True, trust_remote_code=False
    )
    prompts, _, conditions, views, b1_by_key = runner.load_authority(root, payload)
    pair_by_id, condition_work, summary = runner.build_pair_inventory(
        tokenizer, prompts, conditions, views, b1_by_key
    )
    pairs = list(pair_by_id.values())
    batches = runner.exact_length_batches(pairs, runner.MAX_BATCH_SIZE)
    ceilings = {
        "maximum_new_cache_entries": len(pairs),
        "maximum_model_input_instances": len(pairs),
        "maximum_model_input_tokens": sum(item["pair_input_tokens"] for item in pairs),
        "maximum_model_forward_batches": len(batches),
        "maximum_wall_time_seconds": SKILLROUTER_WALL_SECONDS,
    }
    return {
        "schema_version": "rq2b-v7-skillrouter-reranker-b2-zero-inference-preflight-v1",
        "status": "PASS_EXACT_TOKENISATION_NO_MODEL_LOAD_NO_FORWARD",
        "runner_version": runner.RUNNER_VERSION,
        "payload_sha256": canonical_sha256(payload),
        "model_snapshot": {
            "path": relative(snapshot_path, root),
            "repository": runner.MODEL,
            "revision": runner.REVISION,
            "files": runner.MODEL_FILE_SHA256,
        },
        "scope": {
            "conditions": list(runner.MATERIALISED_CONDITIONS),
            "condition_count": 15,
            "queries": EXPECTED_QUERIES,
            "rows": len(condition_work),
            "candidate_pairs_per_row": TOP_K,
            "c2_s_alias_rows": 0,
        },
        "workload": summary,
        "ceilings": ceilings,
        "runtime": {
            "device": "mps",
            "dtype": "bfloat16",
            "attention_implementation": "default_sdpa",
            "exact_model_input_token_length_batches": True,
            "padding": False,
            "batch_size": runner.MAX_BATCH_SIZE,
            "maximum_batch_size": runner.MAX_BATCH_SIZE,
            "automatic_retries": 0,
            "local_files_only": True,
            "trust_remote_code": False,
        },
        "external_activity": {
            "network_calls": 0,
            "provider_calls": 0,
            "model_loads": 0,
            "model_forwards": 0,
        },
    }


def deterministic_ids(root_sha: str, b1_receipt_sha: str, role: str) -> dict[str, str]:
    require(is_sha256(root_sha) and is_sha256(b1_receipt_sha), "Invalid release seed SHA")
    require(role in RUNNER_SPECS, "Unknown B2 release role")
    suffix = hashlib.sha256(f"{root_sha}|{b1_receipt_sha}|{role}".encode()).hexdigest()[:16]
    stem = role.replace("_", "-").upper()
    return {
        "root_release_id": f"RQ2B-V7-P8-{stem}-{suffix}-R1",
        "run_id": f"RQ2B-V7-P8-{stem}-{suffix}",
        "attempt_id": f"RQ2B-V7-P8-{stem}-{suffix}-A1",
        "namespace_suffix": suffix,
    }


def cache_prefix(root_sha: str, b1_receipt_sha: str) -> str:
    suffix = hashlib.sha256(f"{root_sha}|{b1_receipt_sha}|B2".encode()).hexdigest()[:16]
    return f"skill_benchmark/cache/rq2b_v7_phase8_b2_{suffix}"


def build_qwen_release(
    *, root: Path, payload_path: Path, payload: dict[str, Any], pending_path: Path,
    preflight_path: Path, ceilings: dict[str, Any], destinations: dict[str, str],
    root_sha: str, b1_receipt_sha: str, approval_path: Path, approval: dict[str, Any],
) -> dict[str, Any]:
    import run_rq2b_v7_qwen_reranker_b2 as runner

    ids = deterministic_ids(root_sha, b1_receipt_sha, "qwen_reranker_b2")
    return {
        "schema_version": runner.AUTHORISATION_SCHEMA,
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_B1_BOUND_EXECUTION",
        **{key: ids[key] for key in ("root_release_id", "run_id", "attempt_id")},
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "phase8": {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]},
        "b1_validation_receipt_sha256": payload["b1_validation"]["receipt"]["sha256"],
        "approval": {
            "path": relative(approval_path, root),
            "sha256": file_sha256(approval_path),
            "decision": approval["decision"],
            "scope": approval["scope"],
        },
        "provider": {
            "endpoint": runner.ENDPOINT,
            "model": runner.MODEL,
            "api_key_env": runner.API_KEY_ENV,
            "timeout_seconds": runner.DEFAULT_TIMEOUT_SECONDS,
            "automatic_retries": 0,
        },
        "preflight": {
            "pending_release": {"path": relative(pending_path, root), "sha256": file_sha256(pending_path)},
            "receipt": {"path": relative(preflight_path, root), "sha256": file_sha256(preflight_path)},
        },
        "destinations": destinations,
        "ceilings": ceilings,
    }


def build_skillrouter_release(
    *, root: Path, payload_path: Path, payload: dict[str, Any], preflight: dict[str, Any],
    destinations: dict[str, str], root_sha: str, b1_receipt_sha: str,
    approval_path: Path, approval: dict[str, Any],
) -> dict[str, Any]:
    import run_rq2b_v7_skillrouter_reranker_b2 as runner

    ids = deterministic_ids(root_sha, b1_receipt_sha, "skillrouter_reranker_b2")
    return {
        "schema_version": runner.AUTHORISATION_SCHEMA,
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_B1_BOUND_EXECUTION",
        **{key: ids[key] for key in ("root_release_id", "run_id", "attempt_id")},
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "phase8": {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]},
        "b1_validation_receipt_sha256": payload["b1_validation"]["receipt"]["sha256"],
        "approval": {
            "path": relative(approval_path, root),
            "sha256": file_sha256(approval_path),
            "decision": approval["decision"],
            "scope": approval["scope"],
        },
        "model_snapshot": preflight["model_snapshot"],
        "runtime": preflight["runtime"],
        "cpu_fp32_sensitivity": {
            "required": True,
            "execute_during_primary": False,
            "samples_per_representation": 8,
            "maximum_samples": 32,
            "selection_namespace": runner.CPU_SELECTION_NAMESPACE,
            "state": "PENDING_SEPARATE_EXPLICIT_AUTHORISATION",
        },
        "destinations": destinations,
        "ceilings": preflight["ceilings"],
    }


def render_readme(manifest: dict[str, Any]) -> str:
    commands = manifest["execution_commands"]
    return f"""# V7 Phase-8 B2 dispatch

Status: `{manifest['status']}`.

This package was created only after a fresh replay of all 12 persisted B1
cells (12,924 rows) with the current official label-free validator. It binds
the final Phase-8 root, the four current representations, each B1 Top-20
candidate list, both B2 runner/method/chunker or model-snapshot contracts, and
an explicit B36+C6 user approval.

The two machine-readable releases are one-use and currently unconsumed. Qwen
and SkillRouter have distinct output/attempt namespaces; SkillRouter also has
a distinct exact-score cache namespace. Automatic retries are zero. The two
omitted C2 materialisations are frozen aliases (C2-Q=B05-GQ and C2-S=B05-GS),
so the 30 materialised reranker conditions plus the persisted 12 B1 cells
cover exactly the frozen 36 core and 6 diagnostic outcomes.

Exact execution commands (run from the repository root after loading
`DASHSCOPE_API_KEY` without printing it):

```sh
{commands['qwen_reranker_b2']}
{commands['skillrouter_reranker_b2']}
```

These releases do not authorise the later CPU-fp32 sensitivity hook, label
join, acceptable-set join, metrics, offline analysis, or thesis result edits.
Do not regenerate B1 candidates and do not reuse either release after any
attempt receipt exists.
"""


def materialize(
    *, root: Path, phase8_receipt_path: Path, b1_receipt_path: Path,
    approval_path: Path, output_dir: Path, qwen_preflight_path: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    require(not output_dir.exists(), "B2 dispatch output already exists; overwrite forbidden")
    for label, path in (
        ("B2 dispatch output", output_dir),
        ("B1 validation receipt", b1_receipt_path),
        ("approval", approval_path),
    ):
        try:
            path.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError(f"{label} must be inside repository root") from error
    if qwen_preflight_path is not None:
        try:
            qwen_preflight_path.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError("Qwen B2 preflight receipt must be inside repository root") from error
    require(
        relative(output_dir, root).startswith(
            "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        ),
        "B2 dispatch output must be a versioned preparation package",
    )

    approval = validate_approval(root, approval_path)
    _, root_manifest, root_manifest_path, representations = validate_phase8(root, phase8_receipt_path)
    b1_receipt, _ = validate_b1_receipt(
        root, b1_receipt_path,
        phase8_receipt_path=phase8_receipt_path,
        root_manifest_path=root_manifest_path,
    )
    root_sha = file_sha256(root_manifest_path)
    b1_receipt_sha = file_sha256(b1_receipt_path)
    prefix = cache_prefix(root_sha, b1_receipt_sha)
    expected_preflight = root / prefix / "qwen/preflight_receipt.json"
    if qwen_preflight_path is None:
        qwen_preflight_path = expected_preflight
    require(qwen_preflight_path == expected_preflight, "Qwen preflight path must use deterministic B2 namespace")
    require(not qwen_preflight_path.exists(), "Qwen B2 preflight receipt already exists")
    require(relative(qwen_preflight_path, root).startswith("skill_benchmark/cache/"), "Qwen B2 preflight must be under cache")

    qwen_payload = build_payload(
        root=root, role="qwen_reranker_b2", phase8_receipt_path=phase8_receipt_path,
        representations=representations, b1_receipt_path=b1_receipt_path,
        b1_receipt=b1_receipt,
    )
    skillrouter_payload = build_payload(
        root=root, role="skillrouter_reranker_b2", phase8_receipt_path=phase8_receipt_path,
        representations=representations, b1_receipt_path=b1_receipt_path,
        b1_receipt=b1_receipt,
    )

    qwen_payload_path = output_dir / "payloads/qwen_reranker_b2_payload.json"
    skillrouter_payload_path = output_dir / "payloads/skillrouter_reranker_b2_payload.json"
    write_json_new(qwen_payload_path, qwen_payload)
    write_json_new(skillrouter_payload_path, skillrouter_payload)

    import run_rq2b_v7_qwen_reranker_b2 as qwen_runner
    import run_rq2b_v7_skillrouter_reranker_b2 as skillrouter_runner

    qwen_runner.validate_payload(root, qwen_payload_path)
    skillrouter_runner.validate_payload(root, skillrouter_payload_path)

    qwen_destinations = {
        "output_dir": f"{prefix}/qwen/output",
        "attempt_dir": f"{prefix}/qwen/attempt",
    }
    skillrouter_destinations = {
        "output_dir": f"{prefix}/skillrouter/output",
        "cache_dir": f"{prefix}/skillrouter/score_cache",
        "attempt_dir": f"{prefix}/skillrouter/attempt",
    }
    all_destinations = [root / value for value in [*qwen_destinations.values(), *skillrouter_destinations.values()]]
    require(len(set(all_destinations)) == len(all_destinations), "B2 output/attempt/cache namespaces overlap")
    require(all(not path.exists() for path in all_destinations), "A B2 destination namespace already exists")

    qwen_counts = qwen_exact_counts(root, qwen_payload)
    qwen_ceiling_values = qwen_ceilings(qwen_counts)
    qwen_pending = {
        "schema_version": qwen_runner.PENDING_RELEASE_SCHEMA,
        "state": "PENDING_NO_PROVIDER_PREFLIGHT_NOT_EXECUTABLE",
        "payload": {"path": relative(qwen_payload_path, root), "sha256": file_sha256(qwen_payload_path)},
        "provider": {
            "endpoint": qwen_runner.ENDPOINT,
            "model": qwen_runner.MODEL,
            "api_key_env": qwen_runner.API_KEY_ENV,
            "timeout_seconds": qwen_runner.DEFAULT_TIMEOUT_SECONDS,
            "automatic_retries": 0,
        },
        "planned_destinations": qwen_destinations,
        "ceilings": qwen_ceiling_values,
    }
    qwen_pending_path = output_dir / "preflights/qwen_pending_release.json"
    write_json_new(qwen_pending_path, qwen_pending)
    qwen_runner.run_preflight(root, qwen_pending_path, qwen_preflight_path)
    qwen_runner.validate_preflight_receipt(
        read_json(qwen_preflight_path),
        payload_sha256=file_sha256(qwen_payload_path),
        pending_release_sha256=file_sha256(qwen_pending_path),
        ceilings=qwen_ceiling_values,
        root=root,
    )

    skillrouter_cache = root / skillrouter_destinations["cache_dir"]
    sr_preflight = skillrouter_preflight(
        root=root, payload=skillrouter_payload, root_manifest=root_manifest,
        cache_dir=skillrouter_cache,
    )
    sr_preflight_path = output_dir / "preflights/skillrouter_zero_inference_preflight.json"
    write_json_new(sr_preflight_path, sr_preflight)

    qwen_release = build_qwen_release(
        root=root, payload_path=qwen_payload_path, payload=qwen_payload,
        pending_path=qwen_pending_path, preflight_path=qwen_preflight_path,
        ceilings=qwen_ceiling_values, destinations=qwen_destinations,
        root_sha=root_sha, b1_receipt_sha=b1_receipt_sha,
        approval_path=approval_path, approval=approval,
    )
    sr_release = build_skillrouter_release(
        root=root, payload_path=skillrouter_payload_path, payload=skillrouter_payload,
        preflight=sr_preflight, destinations=skillrouter_destinations,
        root_sha=root_sha, b1_receipt_sha=b1_receipt_sha,
        approval_path=approval_path, approval=approval,
    )
    release_paths = {
        "qwen_reranker_b2": output_dir / "authorisations/qwen_reranker_b2.one_use.json",
        "skillrouter_reranker_b2": output_dir / "authorisations/skillrouter_reranker_b2.one_use.json",
    }
    write_json_new(release_paths["qwen_reranker_b2"], qwen_release)
    write_json_new(release_paths["skillrouter_reranker_b2"], sr_release)
    qwen_runner.validate_root_release(root, release_paths["qwen_reranker_b2"])
    skillrouter_runner.validate_root_release(root, release_paths["skillrouter_reranker_b2"])

    commands = {
        "qwen_reranker_b2": (
            ".venv-rq2b-v7/bin/python3 -B skill_benchmark/scripts/"
            "run_rq2b_v7_qwen_reranker_b2.py --execute --authorisation "
            f"{relative(release_paths['qwen_reranker_b2'], root)}"
        ),
        "skillrouter_reranker_b2": (
            ".venv-rq2b-v7/bin/python3 -B skill_benchmark/scripts/"
            "run_rq2b_v7_skillrouter_reranker_b2.py --execute --authorisation "
            f"{relative(release_paths['skillrouter_reranker_b2'], root)}"
        ),
    }
    ledger = {
        "schema_version": LEDGER_SCHEMA,
        "status": "READY_TWO_UNUSED_ONE_USE_B2_RELEASES",
        "approval_record": {"path": relative(approval_path, root), "sha256": file_sha256(approval_path), "decision": approval["decision"]},
        "phase8": {
            "receipt": {"path": relative(phase8_receipt_path, root), "sha256": file_sha256(phase8_receipt_path)},
            "root_manifest": {"path": relative(root_manifest_path, root), "sha256": root_sha},
        },
        "b1_validation": {
            "receipt": {"path": relative(b1_receipt_path, root), "sha256": b1_receipt_sha},
            "artifacts": b1_receipt["b1_artifacts"],
            "cells": EXPECTED_B1_CELLS,
            "rows": EXPECTED_B1_ROWS,
        },
        "matrix_scope": {
            "core_outcomes": EXPECTED_CORE_OUTCOMES,
            "diagnostic_outcomes": EXPECTED_DIAGNOSTIC_OUTCOMES,
            "persisted_b1_cells": EXPECTED_B1_CELLS,
            "materialised_b2_conditions": EXPECTED_B2_MATERIALISED_CONDITIONS,
            "materialised_b2_rows": EXPECTED_B2_ROWS,
            "c2_aliases_materialised": 0,
        },
        "releases": {
            role: {
                "path": relative(path, root),
                "sha256": file_sha256(path),
                "root_release_id": release["root_release_id"],
                "run_id": release["run_id"],
                "attempt_id": release["attempt_id"],
                "one_use": True,
                "consumed": False,
                "automatic_retries": 0,
                "destinations": release["destinations"],
                "ceilings": release["ceilings"],
            }
            for role, path, release in (
                ("qwen_reranker_b2", release_paths["qwen_reranker_b2"], qwen_release),
                ("skillrouter_reranker_b2", release_paths["skillrouter_reranker_b2"], sr_release),
            )
        },
        "label_isolation": {
            "label_files_read": False,
            "acceptable_sets_read": False,
            "b1_result_semantics_interpreted": False,
            "offline_scoring_run": False,
        },
        "external_activity_during_build": {
            "network_calls": 0,
            "provider_calls": 0,
            "model_loads": 0,
            "model_forwards": 0,
        },
    }
    ledger_path = output_dir / "one_use_release_ledger.json"
    write_json_new(ledger_path, ledger)
    manifest = {
        "schema_version": DISPATCH_SCHEMA,
        "status": "READY_TWO_ONE_USE_B2_RELEASES_NOT_YET_CONSUMED",
        "builder": implementation_binding(root, Path(__file__).resolve().relative_to(root)),
        "approval_record": ledger["approval_record"],
        "phase8": ledger["phase8"],
        "b1_validation": ledger["b1_validation"],
        "payloads": {
            "qwen_reranker_b2": {"path": relative(qwen_payload_path, root), "sha256": file_sha256(qwen_payload_path)},
            "skillrouter_reranker_b2": {"path": relative(skillrouter_payload_path, root), "sha256": file_sha256(skillrouter_payload_path)},
        },
        "preflights": {
            "qwen_reranker_b2": {"path": relative(qwen_preflight_path, root), "sha256": file_sha256(qwen_preflight_path)},
            "skillrouter_reranker_b2": {"path": relative(sr_preflight_path, root), "sha256": file_sha256(sr_preflight_path)},
        },
        "release_ledger": {"path": relative(ledger_path, root), "sha256": file_sha256(ledger_path)},
        "execution_commands": commands,
        "next_gate": "EXECUTE_BOTH_RELEASES_THEN_COMBINE_AND_OFFICIALLY_VALIDATE_B36_PLUS_C6",
    }
    manifest_path = output_dir / "dispatch_manifest.json"
    write_json_new(manifest_path, manifest)
    readme_path = output_dir / "README.md"
    write_text_new(readme_path, render_readme(manifest))
    artifact_paths = [
        qwen_payload_path, skillrouter_payload_path, qwen_pending_path,
        qwen_preflight_path, sr_preflight_path, *release_paths.values(),
        ledger_path, manifest_path, readme_path,
    ]
    integrity = {
        "schema_version": INTEGRITY_SCHEMA,
        "status": "PASS_B2_PAYLOADS_AND_UNUSED_ONE_USE_RELEASES_MATERIALISED",
        "phase8_root_sha256": root_sha,
        "b1_validation_receipt_sha256": b1_receipt_sha,
        "approval_record_sha256": file_sha256(approval_path),
        "artifacts": [
            {"path": relative(path, root), "sha256": file_sha256(path), "bytes": path.stat().st_size}
            for path in artifact_paths
        ],
        "assertions": {
            "phase8_root_and_two_b2_runners_replayed": "PASS",
            "four_final_representation_hashes_replayed": "PASS",
            "complete_12_cell_b1_replayed": "PASS",
            "all_b1_top20_bindings_replayed": "PASS",
            "b36_core_plus_c6_diagnostic_scope_bound": "PASS",
            "qwen_exact_no_provider_preflight": "PASS",
            "skillrouter_exact_tokenisation_no_forward_preflight": "PASS",
            "explicit_user_approval_bound": "PASS",
            "two_releases_one_use_unconsumed_zero_retries": "PASS",
            "output_attempt_cache_namespaces_disjoint": "PASS",
            "provider_calls_during_build": 0,
            "model_forwards_during_build": 0,
        },
    }
    write_json_new(output_dir / "integrity_report.json", integrity)
    return {
        "status": integrity["status"],
        "output_dir": relative(output_dir, root),
        "phase8_root_sha256": root_sha,
        "b1_validation_receipt_sha256": b1_receipt_sha,
        "qwen_release_sha256": file_sha256(release_paths["qwen_reranker_b2"]),
        "skillrouter_release_sha256": file_sha256(release_paths["skillrouter_reranker_b2"]),
        "network_calls": 0,
        "provider_calls": 0,
        "model_forwards": 0,
    }


def self_test() -> dict[str, Any]:
    counts = {
        "requests": 7,
        "documents": 101,
        "proxy_tokens": 1234,
        "utf8_bytes": 9876,
    }
    ceilings = qwen_ceilings(counts)
    require(ceilings["maximum_request_attempts"] == 7, "Qwen exact request ceiling self-test failed")
    require(ceilings["maximum_provider_total_tokens"] == 2468, "Qwen provider ceiling self-test failed")
    ids_a = deterministic_ids("a" * 64, "b" * 64, "qwen_reranker_b2")
    ids_b = deterministic_ids("a" * 64, "b" * 64, "qwen_reranker_b2")
    require(ids_a == ids_b and ids_a["attempt_id"].endswith("-A1"), "Deterministic one-use identity failed")
    require(cache_prefix("a" * 64, "b" * 64).startswith("skill_benchmark/cache/"), "Cache namespace self-test failed")
    return {
        "status": "PASS_PHASE8_B2_DISPATCH_BUILDER_SYNTHETIC_NO_INFERENCE",
        "network_calls": 0,
        "provider_calls": 0,
        "model_loads": 0,
        "model_forwards": 0,
        "checks": {
            "deterministic_release_ids": True,
            "exact_predictable_qwen_ceilings": True,
            "zero_retry_contract": True,
            "separate_cache_namespace": True,
        },
    }


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--write-b1-receipt", action="store_true")
    mode.add_argument("--materialize", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--phase8-receipt", type=Path)
    parser.add_argument("--b1-artifact", type=Path, action="append", default=[])
    parser.add_argument("--b1-validation-receipt", type=Path)
    parser.add_argument("--approval-record", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--qwen-preflight-receipt", type=Path)
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    root = args.root.resolve()
    require(args.phase8_receipt is not None, "--phase8-receipt is required")
    phase8 = resolve(root, args.phase8_receipt)
    if args.write_b1_receipt:
        require(args.b1_artifact, "--b1-artifact is required at least once")
        require(args.b1_validation_receipt is not None, "--b1-validation-receipt output is required")
        receipt = write_b1_receipt(
            root=root,
            phase8_receipt_path=phase8,
            artifact_paths=[resolve(root, path) for path in args.b1_artifact],
            output_path=resolve(root, args.b1_validation_receipt),
        )
        print(json.dumps({
            "status": receipt["status"],
            "b1_cells": receipt["b1_cells"],
            "b1_rows": receipt["b1_rows"],
            "receipt_sha256": file_sha256(resolve(root, args.b1_validation_receipt)),
            "provider_calls": 0,
            "model_forwards": 0,
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    for value, message in (
        (args.b1_validation_receipt, "--b1-validation-receipt is required"),
        (args.approval_record, "--approval-record is required"),
        (args.output_dir, "--output-dir is required"),
    ):
        require(value is not None, message)
    result = materialize(
        root=root,
        phase8_receipt_path=phase8,
        b1_receipt_path=resolve(root, args.b1_validation_receipt),
        approval_path=resolve(root, args.approval_record),
        output_dir=resolve(root, args.output_dir),
        qwen_preflight_path=(
            resolve(root, args.qwen_preflight_receipt)
            if args.qwen_preflight_receipt is not None
            else None
        ),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
