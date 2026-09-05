#!/usr/bin/env python3
"""Execute the hash-sealed RQ2a confirmatory sequence without free-form knobs.

The public CLI has two safe modes:

* ``--preflight-only`` validates the frozen protocol, approval packet, execution
  seal, payload audit, local runtime, and output state without network access.
* ``--execute`` additionally requires a user-authorisation record bound to the
  packet and seal hashes, then runs the exact preregistered sequence.

Two hidden child modes are used only by the controller.  They invoke the frozen
Qwen runners with a guarded replacement for their HTTP function.  The guard
accepts only pre-audited text hashes, makes one outbound attempt per batch,
persists the response before returning it, and enforces aggregate ceilings.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from audit_rq2a_qwen_cache import (
    ALL_REPRESENTATIONS,
    cache_state,
)
from build_rq2a_cost_ledger import guarded_attempt_history
from rq2a_selector_common import (
    FIELD_ORDER,
    PROTOCOL_VERSION,
    RESULT_SCHEMA_VERSION,
    RUN_MANIFEST_SCHEMA_VERSION,
    SERIALISER_VERSION,
    audit_token_count,
    load_run_data,
    read_jsonl,
    repo_root,
    sha256_file,
    sha256_json,
    sha256_text,
    summarise_result_rows,
    utc_timestamp,
    validate_confirmatory_execution_grant,
    validate_confirmatory_freeze_manifest,
    write_json_atomic,
)
from run_rq2a_field_aware_selector import (
    REPRESENTATION as FIELD_AWARE_REPRESENTATION,
    field_component_text,
)
from run_rq2a_fixed_candidate_matrix import (
    CORE_REPRESENTATIONS,
    QWEN_BASE_URL,
    QWEN_DIMENSIONS,
    QWEN_MODEL,
    RQ2aEmbeddingClient,
    SKILLROUTER_MODEL,
    SKILLROUTER_REVISION,
)


ROOT = repo_root()
WORKSPACE = ROOT.parent
INPUT_DIR = ROOT / "rq2a_matched_content"
CONFIRMATORY_ROOT = ROOT / "outputs" / "rq2a_matched_content" / "confirmatory"
ANALYSIS_ROOT = ROOT / "outputs" / "rq2a_matched_content" / "analysis"
CONTROLLER_ID = "confirmatory-controller-v1"
CONTROLLER_DIR = ANALYSIS_ROOT / CONTROLLER_ID
LOG_DIR = CONTROLLER_DIR / "logs"
GUARD_DIR = CONTROLLER_DIR / "qwen_guard"
STATE_PATH = CONTROLLER_DIR / "controller_state.json"
DEFAULT_FREEZE = INPUT_DIR / "confirmatory_freeze_manifest.json"
DEFAULT_PREFLIGHT = (
    ANALYSIS_ROOT
    / "confirmatory-qwen-cache-preflight-v2"
    / "qwen_cache_audit.json"
)
DEFAULT_PACKET = INPUT_DIR / "confirmatory_authorisation_packet.json"
DEFAULT_SEAL = INPUT_DIR / "confirmatory_execution_seal.json"
DEFAULT_AUTHORISATION = INPUT_DIR / "confirmatory_user_authorisation.json"
DEFAULT_INDEPENDENT_REVIEW = (
    INPUT_DIR / "confirmatory_independent_review_pass.json"
)
DEFAULT_FAILURE_SPEC = INPUT_DIR / "confirmatory_failure_spec.json"
AGGREGATION_CHOICE = (
    ROOT
    / "outputs"
    / "rq2a_matched_content"
    / "development"
    / "development-field-aware-v1"
    / "aggregation_choice.json"
)

ALL_REPRESENTATIONS_TUPLE = tuple(ALL_REPRESENTATIONS)
CORE_REPRESENTATIONS_TUPLE = tuple(CORE_REPRESENTATIONS)


@dataclass(frozen=True)
class RunSpec:
    run_id: str
    runner: str
    role: str
    selectors: tuple[str, ...]
    representations: tuple[str, ...]
    aggregations: tuple[str, ...]
    expected_rows: int
    guarded_category: str | None = None


RUN_SPECS: tuple[RunSpec, ...] = (
    RunSpec(
        "confirmatory-bm25-all-v1",
        "fixed",
        "primary",
        ("bm25",),
        ALL_REPRESENTATIONS_TUPLE,
        (),
        4_800,
    ),
    RunSpec(
        "confirmatory-skillrouter-core-v1",
        "fixed",
        "primary",
        ("skillrouter-cross-encoder",),
        CORE_REPRESENTATIONS_TUPLE,
        (),
        3_000,
    ),
    RunSpec(
        "confirmatory-qwen-all-v1",
        "guarded-fixed",
        "primary",
        ("qwen-single-vector",),
        ALL_REPRESENTATIONS_TUPLE,
        (),
        4_800,
        "single_vector_documents",
    ),
    RunSpec(
        "confirmatory-field-aware-v1",
        "guarded-field",
        "primary",
        ("qwen-field-aware-uniform-top-two",),
        (FIELD_AWARE_REPRESENTATION,),
        ("uniform-top-two",),
        600,
        "field_components",
    ),
    RunSpec(
        "confirmatory-skillrouter-core-warm-v1",
        "fixed",
        "verification",
        ("skillrouter-cross-encoder",),
        CORE_REPRESENTATIONS_TUPLE,
        (),
        3_000,
    ),
    RunSpec(
        "confirmatory-qwen-all-warm-v1",
        "guarded-fixed",
        "verification",
        ("qwen-single-vector",),
        ALL_REPRESENTATIONS_TUPLE,
        (),
        4_800,
        "single_vector_documents",
    ),
    RunSpec(
        "confirmatory-field-aware-warm-v1",
        "guarded-field",
        "verification",
        ("qwen-field-aware-uniform-top-two",),
        (FIELD_AWARE_REPRESENTATION,),
        ("uniform-top-two",),
        600,
        "field_components",
    ),
)
RUN_BY_ID = {spec.run_id: spec for spec in RUN_SPECS}
PRIMARY_RUN_IDS = tuple(spec.run_id for spec in RUN_SPECS if spec.role == "primary")
VERIFICATION_RUN_IDS = tuple(
    spec.run_id for spec in RUN_SPECS if spec.role == "verification"
)
EXPECTED_PRIMARY_CONDITIONS = {
    ("bm25", representation) for representation in ALL_REPRESENTATIONS_TUPLE
} | {
    ("skillrouter-cross-encoder", representation)
    for representation in CORE_REPRESENTATIONS_TUPLE
} | {
    ("qwen-single-vector", representation)
    for representation in ALL_REPRESENTATIONS_TUPLE
} | {
    ("qwen-field-aware-uniform-top-two", FIELD_AWARE_REPRESENTATION)
}


@contextmanager
def exclusive_file_lock(path: Path):
    """Hold an exclusive non-blocking process lock for one critical section."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"Another confirmatory process holds {path}") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected one JSON object: {path}")
    return payload


def workspace_path(raw: str | Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else WORKSPACE / path


def require_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(f"{label} hash mismatch: {actual} != {expected}")


def expected_prompt_identity() -> tuple[set[str], set[str]]:
    _, prompts, _ = load_run_data(
        INPUT_DIR,
        "confirmatory",
        ["shared-only"],
        None,
    )
    return (
        {row["prompt_id"] for row in prompts},
        {row["cluster_id"] for row in prompts},
    )


def payload_texts() -> dict[str, set[str]]:
    protocol, prompts, indexes = load_run_data(
        INPUT_DIR,
        "confirmatory",
        list(ALL_REPRESENTATIONS_TUPLE),
        None,
    )
    documents = {
        row["selector_visible_text"]
        for index in indexes.values()
        for row in index.values()
    }
    queries = {row["query_text"] for row in prompts}
    components: set[str] = set()
    for key, row in indexes[FIELD_AWARE_REPRESENTATION].items():
        for field in FIELD_ORDER:
            text = field_component_text(
                field,
                row["canonical_fields"][field],
                protocol["field_labels"],
            )
            if text not in row["selector_visible_text"]:
                raise ValueError(f"{key}/{field}: component is not an exact block")
            components.add(text)
    return {
        "single_vector_documents": documents,
        "queries": queries,
        "field_components": components,
        "combined_unique_payload": documents | queries | components,
    }


def validate_packet_and_seal(
    packet_path: Path,
    seal_path: Path,
    freeze_path: Path,
    preflight_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    packet = load_json(packet_path)
    seal = load_json(seal_path)
    preflight = load_json(preflight_path)
    if packet.get("schema_version") != "rq2a-confirmatory-authorisation-packet-v1":
        raise ValueError("Confirmatory authorisation packet schema mismatch")
    if packet.get("state") != "awaiting_independent_review_and_user_authorisation":
        raise ValueError("Confirmatory packet state is not immutable/pre-execution")
    if seal.get("schema_version") != "rq2a-confirmatory-execution-seal-v1":
        raise ValueError("Confirmatory execution seal schema mismatch")
    if seal.get("state") != "sealed_before_user_authorisation":
        raise ValueError("Confirmatory execution seal is not frozen")
    if preflight.get("schema_version") != "rq2a-qwen-cache-audit-v2":
        raise ValueError("Confirmatory payload audit schema mismatch")
    sealed_artifacts = seal.get("sealed_artifacts", {})
    if not isinstance(sealed_artifacts, dict) or not sealed_artifacts:
        raise ValueError("Confirmatory execution seal has no artifacts")
    for raw_path, expected in sealed_artifacts.items():
        require_hash(workspace_path(raw_path), expected, "sealed artifact")
    if str(Path(__file__).resolve()) not in {
        str(workspace_path(raw_path).resolve())
        for raw_path in sealed_artifacts
    }:
        raise ValueError("Execution seal does not bind this controller")
    execution = packet.get("execution_control", {})
    require_hash(
        seal_path,
        execution.get("execution_seal_sha256", ""),
        "execution seal",
    )
    if workspace_path(execution.get("execution_seal_path", "")).resolve() != seal_path.resolve():
        raise ValueError("Packet references a different execution seal")
    freeze = validate_confirmatory_freeze_manifest(
        freeze_path,
        input_dir=INPUT_DIR,
        output_dir=CONFIRMATORY_ROOT,
    )
    require_hash(
        freeze_path,
        packet["frozen_provenance"]["freeze_manifest_sha256"],
        "confirmatory freeze",
    )
    require_hash(
        preflight_path,
        packet["offline_payload_audit"]["sha256"],
        "offline payload audit",
    )
    scope = packet["scientific_scope"]
    if (
        scope.get("split") != "confirmatory"
        or scope.get("cluster_count") != 280
        or scope.get("prompt_count") != 600
        or scope.get("frozen_condition_count") != 22
        or scope.get("expected_primary_result_rows") != 13_200
    ):
        raise ValueError("Packet scientific scope differs from the frozen plan")
    external = packet["external_service_scope"]
    required_external = {
        "base_url": QWEN_BASE_URL,
        "model": QWEN_MODEL,
        "dimensions": QWEN_DIMENSIONS,
        "batch_size": 10,
        "successful_api_call_ceiling": 667,
        "outbound_request_attempt_ceiling": 667,
        "local_audit_token_ceiling": 1_130_034,
        "provider_total_token_ceiling": 1_500_000,
        "standard_list_price_usd_ceiling": 0.11,
    }
    for key, expected in required_external.items():
        if external.get(key) != expected:
            raise ValueError(f"Packet external scope mismatch for {key}")
    if preflight.get("network_requests") != 0:
        raise ValueError("Payload preflight was not offline")
    if preflight.get("split") != "confirmatory":
        raise ValueError("Payload preflight split mismatch")
    if (
        preflight.get("base_url") != QWEN_BASE_URL
        or preflight.get("model") != QWEN_MODEL
        or preflight.get("dimensions") != QWEN_DIMENSIONS
        or preflight.get("batch_size") != 10
    ):
        raise ValueError("Payload preflight provider configuration mismatch")
    combined = preflight["categories"]["combined_unique_payload"]
    if (
        combined.get("cache_misses") != 6_661
        or combined.get("estimated_api_calls") != 667
        or combined.get("missing_audit_tokens") != 1_130_034
        or combined.get("maximum_audit_tokens") != 262
    ):
        raise ValueError("Payload preflight counts differ from the approved packet")
    if freeze.get("aggregation_choice", {}).get("selected_selector") != (
        "qwen-field-aware-uniform-top-two"
    ):
        raise ValueError("Frozen field-aware selector mismatch")
    return packet, seal, preflight


def validate_authorisation(
    authorisation_path: Path,
    packet_path: Path,
    seal_path: Path,
    packet: dict[str, Any],
) -> dict[str, Any]:
    authorisation = load_json(authorisation_path)
    if authorisation.get("schema_version") != "rq2a-confirmatory-user-authorisation-v1":
        raise ValueError("User authorisation schema mismatch")
    if authorisation.get("state") != "authorised":
        raise ValueError("Confirmatory execution is not user-authorised")
    if authorisation.get("authorised_by") != "Jacky Zhang":
        raise ValueError("Unexpected confirmatory authorisation principal")
    if not authorisation.get("explicit_user_statement"):
        raise ValueError("Authorisation has no explicit user statement")
    require_hash(
        packet_path,
        authorisation.get("packet_sha256", ""),
        "authorised packet",
    )
    require_hash(
        seal_path,
        authorisation.get("execution_seal_sha256", ""),
        "authorised execution seal",
    )
    if authorisation.get("approved_scope") != packet.get("approval_scope_digest"):
        raise ValueError("User-approved scope differs from the packet")
    return authorisation


def validate_independent_review(
    review_path: Path,
    packet_path: Path,
    seal_path: Path,
    packet: dict[str, Any],
) -> dict[str, Any]:
    review = load_json(review_path)
    if review.get("schema_version") != (
        "rq2a-confirmatory-independent-review-pass-v1"
    ):
        raise ValueError("Independent review schema mismatch")
    if review.get("state") != "pass" or review.get("verdict") != "PASS":
        raise ValueError("Independent review is not a PASS")
    if not review.get("reviewer_agent_id"):
        raise ValueError("Independent review has no reviewer identity")
    require_hash(packet_path, review.get("packet_sha256", ""), "reviewed packet")
    require_hash(
        seal_path,
        review.get("execution_seal_sha256", ""),
        "reviewed execution seal",
    )
    if review.get("approval_scope_sha256") != sha256_json(
        packet.get("approval_scope_digest")
    ):
        raise ValueError("Independent review approval-scope hash mismatch")
    if review.get("network_or_scoring_performed") is not False:
        raise ValueError("Independent review execution boundary is not recorded")
    if review.get("can_authorise_spending") is not False:
        raise ValueError("Independent review incorrectly claims spending authority")
    return review


def exact_cache_client() -> RQ2aEmbeddingClient:
    return RQ2aEmbeddingClient(
        provider="qwen",
        base_url=QWEN_BASE_URL,
        api_key="unused-controller-audit",
        model=QWEN_MODEL,
        dimensions=QWEN_DIMENSIONS,
        cache_dir=ROOT / "cache" / "rq2a",
        timeout_seconds=1,
        max_audit_tokens=8192,
        legacy_cache_dir=ROOT / "runtime" / "provider_cache",
    )


def completed_guard_attempts_by_text() -> dict[str, str]:
    attempt_dir = GUARD_DIR / "attempts"
    result: dict[str, str] = {}
    if not attempt_dir.exists():
        return result
    for path in sorted(attempt_dir.glob("*.json")):
        row = load_json(path)
        if row.get("schema_version") != "rq2a-guarded-dashscope-attempt-v1":
            raise ValueError(f"Guard attempt schema mismatch: {path}")
        if row.get("state") != "complete":
            raise RuntimeError(
                "Guard attempt is not complete and cannot justify cache reuse: "
                f"{path}"
            )
        attempt_sha256 = sha256_file(path)
        hashes = row.get("text_sha256")
        if not isinstance(hashes, list) or not hashes:
            raise ValueError(f"Guard attempt has no text hashes: {path}")
        for digest in hashes:
            if digest in result:
                raise ValueError("Guard attempts contain a duplicate text hash")
            result[digest] = attempt_sha256
    return result


def validate_current_payload_state(preflight: dict[str, Any]) -> dict[str, Any]:
    texts = payload_texts()
    client = exact_cache_client()
    guarded = completed_guard_attempts_by_text()
    report: dict[str, Any] = {}
    for category, category_texts in texts.items():
        frozen = preflight["categories"][category]
        expected_hashes = {
            sha256_text(text) for text in category_texts
        }
        if len(expected_hashes) != frozen["unique_text_count"]:
            raise ValueError(f"{category}: current unique text count drift")
        initial_missing = set(frozen["missing_text_sha256"])
        frozen_current = {
            row["text_sha256"]: row
            for row in frozen.get("current_cache_entries", [])
        }
        frozen_legacy = {
            row["text_sha256"]: row
            for row in frozen.get("legacy_cache_entries", [])
        }
        if len(frozen_current) != frozen.get("current_cache_hits"):
            raise ValueError(f"{category}: frozen current-cache inventory mismatch")
        if len(frozen_legacy) != frozen.get("legacy_exact_hits"):
            raise ValueError(f"{category}: frozen legacy-cache inventory mismatch")
        if set(frozen_current) | set(frozen_legacy) | initial_missing != expected_hashes:
            raise ValueError(f"{category}: frozen cache partition is incomplete")
        current_missing: set[str] = set()
        current_tokens = 0
        for text in category_texts:
            digest = sha256_text(text)
            state, raw_path = cache_state(client, text)
            if digest in frozen_current:
                expected = frozen_current[digest]
                if state != "current" or raw_path is None:
                    raise ValueError(f"{category}: frozen current cache entry disappeared")
                if Path(raw_path).resolve() != Path(expected["path"]).resolve():
                    raise ValueError(f"{category}: frozen current cache path drift")
                if sha256_file(Path(raw_path)) != expected["file_sha256"]:
                    raise ValueError(f"{category}: frozen current cache hash drift")
            elif digest in frozen_legacy:
                expected = frozen_legacy[digest]
                if state != "legacy" or raw_path is None:
                    raise ValueError(f"{category}: frozen legacy cache entry drift")
                if Path(raw_path).resolve() != Path(expected["path"]).resolve():
                    raise ValueError(f"{category}: frozen legacy cache path drift")
                if sha256_file(Path(raw_path)) != expected["file_sha256"]:
                    raise ValueError(f"{category}: frozen legacy cache hash drift")
            elif state == "current":
                if raw_path is None or digest not in guarded:
                    raise ValueError(
                        f"{category}: post-audit cache entry lacks guarded provenance"
                    )
                payload = load_json(Path(raw_path))
                provenance = payload.get("provenance", {})
                if (
                    provenance.get("kind") != "confirmatory_guard_response"
                    or provenance.get("attempt_sha256") != guarded[digest]
                ):
                    raise ValueError(
                        f"{category}: guarded cache provenance mismatch"
                    )
            elif state == "legacy":
                raise ValueError(
                    f"{category}: unaudited legacy cache entry appeared after preflight"
                )
            if state == "missing":
                current_missing.add(digest)
                current_tokens += audit_token_count(text)
        if not current_missing <= initial_missing:
            raise ValueError(f"{category}: unaudited text would be sent externally")
        report[category] = {
            "unique_text_count": len(expected_hashes),
            "current_missing": len(current_missing),
            "current_missing_audit_tokens": current_tokens,
            "frozen_missing_ceiling": len(initial_missing),
        }
    if report["queries"]["current_missing"] != 0:
        raise ValueError("Confirmatory query cache regressed; query transfer is not approved")
    return report


def validate_runtime_environment(require_api_key: bool) -> dict[str, Any]:
    if require_api_key:
        dotenv = WORKSPACE / ".env"
        if dotenv.is_file():
            for raw_line in dotenv.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(
                        key.strip(), value.strip().strip('"').strip("'")
                    )
        if not os.environ.get("DASHSCOPE_API_KEY"):
            raise RuntimeError("DASHSCOPE_API_KEY is unavailable")
    snapshot = (
        Path(
            os.environ.get(
                "HF_HOME",
                str(Path.home() / ".cache" / "huggingface"),
            )
        )
        / "hub"
        / "models--pipizhao--SkillRouter-Reranker-0.6B"
        / "snapshots"
        / SKILLROUTER_REVISION
    )
    if not snapshot.is_dir():
        raise FileNotFoundError(f"Pinned SkillRouter snapshot is missing: {snapshot}")
    try:
        import torch
        import transformers
    except ImportError as exc:
        raise RuntimeError(
            "Use skill_benchmark/.venv-rq2a/bin/python for confirmatory execution"
        ) from exc
    return {
        "python": sys.executable,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "skillrouter_snapshot": str(snapshot),
        "dashscope_key_present": bool(os.environ.get("DASHSCOPE_API_KEY")),
    }


def run_dir(spec: RunSpec) -> Path:
    return CONFIRMATORY_ROOT / spec.run_id


def validate_result_row(row: dict[str, Any], spec: RunSpec) -> None:
    if row.get("schema_version") != RESULT_SCHEMA_VERSION:
        raise ValueError(f"{spec.run_id}: result schema mismatch")
    if row.get("run_id") != spec.run_id or row.get("split") != "confirmatory":
        raise ValueError(f"{spec.run_id}: row provenance mismatch")
    if (row.get("selector"), row.get("representation")) not in {
        (selector, representation)
        for selector in spec.selectors
        for representation in spec.representations
    }:
        raise ValueError(f"{spec.run_id}: unexpected condition row")
    if sha256_text(row.get("query_text", "")) != row.get("query_text_sha256"):
        raise ValueError(f"{spec.run_id}: query hash mismatch")
    candidates = row.get("candidate_skill_ids", [])
    scores = row.get("scores", [])
    if len(candidates) != 3 or len(set(candidates)) != 3 or len(scores) != 3:
        raise ValueError(f"{spec.run_id}: malformed candidates or scores")
    if row.get("gold_skill_id") not in candidates:
        raise ValueError(f"{spec.run_id}: gold candidate mismatch")
    numeric = [
        *scores,
        row.get("top1_tie_adjusted"),
        row.get("mrr_tie_adjusted"),
        row.get("gold_margin"),
    ]
    if any(
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(float(value))
        for value in numeric
    ):
        raise ValueError(f"{spec.run_id}: non-finite metric")


def validate_run_grant_provenance(
    manifest: dict[str, Any],
    spec: RunSpec,
    args: argparse.Namespace,
) -> None:
    grant_artifact = manifest.get("input_artifacts", {}).get(
        "confirmatory_controller_grant", {}
    )
    expected_grant_path = grant_path(spec.run_id)
    if Path(str(grant_artifact.get("path", ""))).resolve() != (
        expected_grant_path.resolve()
    ):
        raise ValueError(f"{spec.run_id}: controller grant path mismatch")
    if grant_artifact.get("sha256") != sha256_file(expected_grant_path):
        raise ValueError(f"{spec.run_id}: controller grant hash mismatch")
    if spec.runner.endswith("field"):
        grant_action = "field_aware_scoring"
        grant_invocation = field_run_invocation(spec, args)
    else:
        grant_action = "fixed_scoring"
        grant_invocation = fixed_run_invocation(spec, args)
    if (
        grant_artifact.get("action") != grant_action
        or grant_artifact.get("invocation_sha256")
        != sha256_json(grant_invocation)
    ):
        raise ValueError(f"{spec.run_id}: controller grant invocation mismatch")
    validate_confirmatory_execution_grant(
        expected_grant_path,
        action=grant_action,
        invocation=grant_invocation,
    )


def validate_run_summary_artifact(
    summary_path: Path,
    rows: list[dict[str, Any]],
    run_id: str,
) -> None:
    if load_json(summary_path) != summarise_result_rows(rows):
        raise ValueError(f"{run_id}: summary does not match result rows")


def validate_run(spec: RunSpec, args: argparse.Namespace) -> dict[str, Any]:
    directory = run_dir(spec)
    manifest_path = directory / "manifest.json"
    rows_path = directory / "rows.jsonl"
    summary_path = directory / "summary.json"
    summary_md_path = directory / "summary.md"
    for path in (manifest_path, rows_path, summary_path, summary_md_path):
        if not path.is_file():
            raise FileNotFoundError(f"{spec.run_id}: missing {path.name}")
    manifest = load_json(manifest_path)
    if manifest.get("schema_version") != RUN_MANIFEST_SCHEMA_VERSION:
        raise ValueError(f"{spec.run_id}: manifest schema mismatch")
    exact = {
        "run_id": spec.run_id,
        "state": "complete",
        "split": "confirmatory",
        "evidence_role": spec.role,
        "clusters_per_field": None,
        "prompt_count": 600,
        "cluster_count": 280,
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
    }
    for key, expected in exact.items():
        if manifest.get(key) != expected:
            raise ValueError(f"{spec.run_id}: manifest mismatch for {key}")
    if spec.runner.endswith("field"):
        if tuple(manifest.get("aggregations", [])) != spec.aggregations:
            raise ValueError(f"{spec.run_id}: aggregation mismatch")
        if manifest.get("representation") != FIELD_AWARE_REPRESENTATION:
            raise ValueError(f"{spec.run_id}: field-aware representation mismatch")
    else:
        if tuple(manifest.get("selectors", [])) != spec.selectors:
            raise ValueError(f"{spec.run_id}: selector mismatch")
        if tuple(manifest.get("representations", [])) != spec.representations:
            raise ValueError(f"{spec.run_id}: representation mismatch")
    frozen = manifest.get("input_artifacts", {}).get(
        "confirmatory_freeze_manifest", {}
    )
    if (
        Path(str(frozen.get("path", ""))).resolve() != args.freeze.resolve()
        or frozen.get("sha256") != sha256_file(args.freeze)
    ):
        raise ValueError(f"{spec.run_id}: confirmatory freeze reference mismatch")
    validate_run_grant_provenance(manifest, spec, args)
    output = manifest.get("output_artifacts", {}).get("rows_jsonl", {})
    if output.get("row_count") != spec.expected_rows:
        raise ValueError(f"{spec.run_id}: manifest row count mismatch")
    if output.get("sha256") != sha256_file(rows_path):
        raise ValueError(f"{spec.run_id}: rows hash mismatch")
    quality = manifest.get("quality_checks", {})
    for key in ("candidate_alignment", "finite_scores"):
        if quality.get(key) != "pass":
            raise ValueError(f"{spec.run_id}: quality check {key} failed")
    if quality.get("no_thesis_write") is not True:
        raise ValueError(f"{spec.run_id}: thesis-write boundary missing")
    rows = read_jsonl(rows_path)
    if len(rows) != spec.expected_rows:
        raise ValueError(f"{spec.run_id}: actual row count mismatch")
    _, prompts, indexes = load_run_data(
        INPUT_DIR,
        "confirmatory",
        list(spec.representations),
        None,
    )
    expected_prompts = {row["prompt_id"]: row for row in prompts}
    seen: set[tuple[str, str, str]] = set()
    condition_counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        validate_result_row(row, spec)
        prompt = expected_prompts.get(row["prompt_id"])
        if prompt is None:
            raise ValueError(f"{spec.run_id}: unexpected prompt")
        expected_prompt_fields = {
            "cluster_id": prompt["cluster_id"],
            "field": prompt["field"],
            "prompt_variant": prompt["prompt_variant"],
            "query_text": prompt["query_text"],
            "query_text_sha256": sha256_text(prompt["query_text"]),
            "gold_skill_id": prompt["gold_skill_id"],
            "candidate_skill_ids": prompt["candidate_skill_ids"],
        }
        for key, expected in expected_prompt_fields.items():
            if row.get(key) != expected:
                raise ValueError(
                    f"{spec.run_id}: frozen prompt mismatch for {row['prompt_id']}/{key}"
                )
        representation_index = indexes[row["representation"]]
        expected_candidates = [
            representation_index[(prompt["cluster_id"], skill_id)]
            for skill_id in prompt["candidate_skill_ids"]
        ]
        if row.get("candidate_text_sha256") != [
            candidate["selector_visible_text_sha256"]
            for candidate in expected_candidates
        ]:
            raise ValueError(
                f"{spec.run_id}: frozen candidate-text mismatch for {row['prompt_id']}"
            )
        if row.get("candidate_audit_token_counts") != [
            candidate["audit_token_count"] for candidate in expected_candidates
        ]:
            raise ValueError(
                f"{spec.run_id}: frozen candidate-length mismatch for {row['prompt_id']}"
            )
        config_key = (
            row["selector"].removeprefix("qwen-field-aware-")
            if row["selector"].startswith("qwen-field-aware-")
            else row["selector"]
        )
        if row.get("selector_config_sha256") != sha256_json(
            manifest["selector_configurations"][config_key]
        ):
            raise ValueError(
                f"{spec.run_id}: selector configuration hash mismatch"
            )
        identity = (row["selector"], row["representation"], row["prompt_id"])
        if identity in seen:
            raise ValueError(f"{spec.run_id}: duplicate result identity")
        seen.add(identity)
        condition_counts[(row["selector"], row["representation"])] += 1
    expected_conditions = {
        (selector, representation)
        for selector in spec.selectors
        for representation in spec.representations
    }
    if set(condition_counts) != expected_conditions:
        raise ValueError(f"{spec.run_id}: condition set mismatch")
    if any(count != 600 for count in condition_counts.values()):
        raise ValueError(f"{spec.run_id}: incomplete condition")
    validate_run_summary_artifact(summary_path, rows, spec.run_id)
    if "skillrouter-cross-encoder" in spec.selectors:
        runtime = manifest["runtime"]["skillrouter-cross-encoder"]
        config = manifest["selector_configurations"]["skillrouter-cross-encoder"]
        if (
            config.get("model") != SKILLROUTER_MODEL
            or config.get("revision") != SKILLROUTER_REVISION
            or config.get("maximum_input_tokens") != 2048
            or config.get("truncation") is not False
            or runtime.get("truncated_pairs") != 0
        ):
            raise ValueError(f"{spec.run_id}: SkillRouter configuration drift")
        if spec.role == "verification" and (
            runtime.get("cache_misses") != 0
            or runtime.get("scored_pairs") != 0
            or abs(float(runtime.get("model_elapsed_seconds", 0.0))) > 1e-12
        ):
            raise ValueError(f"{spec.run_id}: warm SkillRouter recomputed scores")
    if "qwen-single-vector" in spec.selectors:
        config = manifest["selector_configurations"]["qwen-single-vector"]
        runtime = manifest["runtime"]["qwen-single-vector"]
        if (
            config.get("base_url") != QWEN_BASE_URL
            or config.get("model") != QWEN_MODEL
            or config.get("dimensions") != QWEN_DIMENSIONS
            or config.get("truncation") is not False
        ):
            raise ValueError(f"{spec.run_id}: Qwen configuration drift")
        if spec.role == "verification" and (
            runtime["cumulative_embedding_stats"].get("api_calls") != 0
            or runtime["cumulative_embedding_stats"].get("cache_misses") != 0
        ):
            raise ValueError(f"{spec.run_id}: warm Qwen used external work")
    if spec.runner.endswith("field"):
        runtime = manifest["runtime"]
        config = manifest["selector_configurations"]["uniform-top-two"]
        if (
            config.get("base_url") != QWEN_BASE_URL
            or config.get("model") != QWEN_MODEL
            or config.get("dimensions") != QWEN_DIMENSIONS
            or config.get("aggregation") != "uniform-top-two"
            or config.get("truncation") is not False
        ):
            raise ValueError(f"{spec.run_id}: field-aware configuration drift")
        if spec.role == "verification" and (
            runtime["cumulative_embedding_stats"].get("api_calls") != 0
            or runtime["cumulative_embedding_stats"].get("cache_misses") != 0
        ):
            raise ValueError(f"{spec.run_id}: warm field-aware used external work")
    return {
        "run_id": spec.run_id,
        "role": spec.role,
        "rows": len(rows),
        "manifest_sha256": sha256_file(manifest_path),
        "rows_sha256": sha256_file(rows_path),
    }


def scientific_rows_digest(path: Path) -> str:
    projected: list[dict[str, Any]] = []
    for row in read_jsonl(path):
        projected.append(
            {
                key: value
                for key, value in row.items()
                if key not in {"run_id", "score_latency_seconds"}
            }
        )
    projected.sort(
        key=lambda row: (row["selector"], row["representation"], row["prompt_id"])
    )
    return sha256_json(projected)


def validate_warm_reproduction() -> dict[str, str]:
    pairs = (
        ("confirmatory-skillrouter-core-v1", "confirmatory-skillrouter-core-warm-v1"),
        ("confirmatory-qwen-all-v1", "confirmatory-qwen-all-warm-v1"),
        ("confirmatory-field-aware-v1", "confirmatory-field-aware-warm-v1"),
    )
    result: dict[str, str] = {}
    for primary, verification in pairs:
        left = scientific_rows_digest(CONFIRMATORY_ROOT / primary / "rows.jsonl")
        right = scientific_rows_digest(CONFIRMATORY_ROOT / verification / "rows.jsonl")
        if left != right:
            raise ValueError(f"Warm reproduction mismatch: {primary} vs {verification}")
        result[f"{primary}::{verification}"] = left
    return result


def validate_complete_primary_matrix() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for run_id in PRIMARY_RUN_IDS:
        rows.extend(read_jsonl(CONFIRMATORY_ROOT / run_id / "rows.jsonl"))
    if len(rows) != 13_200:
        raise ValueError(f"Primary matrix has {len(rows)} rows, expected 13200")
    identities = {
        (row["selector"], row["representation"], row["prompt_id"])
        for row in rows
    }
    if len(identities) != 13_200:
        raise ValueError("Primary matrix has duplicate condition-prompt rows")
    conditions: Counter[tuple[str, str]] = Counter(
        (row["selector"], row["representation"]) for row in rows
    )
    if set(conditions) != EXPECTED_PRIMARY_CONDITIONS:
        raise ValueError("Primary matrix condition set mismatch")
    if any(count != 600 for count in conditions.values()):
        raise ValueError("Primary matrix has an incomplete condition")
    if len({row["cluster_id"] for row in rows}) != 280:
        raise ValueError("Primary matrix does not cover 280 clusters")
    return {
        "row_count": len(rows),
        "condition_count": len(conditions),
        "prompt_count": len({row["prompt_id"] for row in rows}),
        "cluster_count": len({row["cluster_id"] for row in rows}),
    }


def incomplete_run_files(directory: Path) -> list[dict[str, Any]]:
    return [
        {
            "path": str(path.relative_to(directory)),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    ]


def quarantine_incomplete(spec: RunSpec, reason: str) -> Path | None:
    directory = run_dir(spec)
    if not directory.exists() or not any(directory.iterdir()):
        return None
    quarantine_root = CONTROLLER_DIR / "quarantine"
    quarantine_root.mkdir(parents=True, exist_ok=True)
    destination = quarantine_root / (
        f"{spec.run_id}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    )
    if destination.exists():
        raise FileExistsError(f"Quarantine destination exists: {destination}")
    inventory = incomplete_run_files(directory)
    shutil.move(str(directory), str(destination))
    write_json_atomic(
        destination / "quarantine_manifest.json",
        {
            "schema_version": "rq2a-confirmatory-quarantine-v1",
            "created_utc": utc_timestamp(),
            "run_id": spec.run_id,
            "reason": reason,
            "files_before_move": inventory,
        },
    )
    return destination


def validate_confirmatory_root(
    args: argparse.Namespace | None = None,
) -> dict[str, Any]:
    if not CONFIRMATORY_ROOT.exists():
        return {"state": "absent", "complete_runs": []}
    complete: list[str] = []
    incomplete: list[str] = []
    for child in sorted(CONFIRMATORY_ROOT.iterdir()):
        if child.name not in RUN_BY_ID or not child.is_dir():
            raise ValueError(f"Unexpected confirmatory artifact: {child}")
        if not any(child.iterdir()):
            incomplete.append(child.name)
            continue
        manifest_path = child / "manifest.json"
        if not manifest_path.is_file():
            incomplete.append(child.name)
            continue
        if args is None:
            raise ValueError(
                "Pre-existing complete confirmatory output requires the "
                "authorised execution controller"
            )
        validate_run(RUN_BY_ID[child.name], args)
        complete.append(child.name)
    return {
        "state": "present",
        "complete_runs": complete,
        "incomplete_known_runs": incomplete,
    }


class GuardedDashScopeTransport:
    """One-attempt, hash-allowlisted transport with crash-safe response replay."""

    def __init__(
        self,
        *,
        category: str,
        preflight: dict[str, Any],
        packet: dict[str, Any],
        allow_new_requests: bool,
        transport: Callable[[str, str, dict[str, Any], int], dict[str, Any]] | None = None,
    ) -> None:
        self.category = category
        self.preflight = preflight
        self.packet = packet
        self.allow_new_requests = allow_new_requests
        self.transport = transport or self._network_once
        self.attempt_dir = GUARD_DIR / "attempts"
        self.attempt_dir.mkdir(parents=True, exist_ok=True)
        self.allowed_hashes = set(
            preflight["categories"][category]["missing_text_sha256"]
        )
        self.all_allowed_hashes = set(
            preflight["categories"]["combined_unique_payload"][
                "missing_text_sha256"
            ]
        )
        self.external = packet["external_service_scope"]

    @staticmethod
    def _network_once(
        url: str,
        api_key: str,
        payload: dict[str, Any],
        timeout_seconds: int,
    ) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                parsed = json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(f"Guarded DashScope request failed once: {exc}") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("DashScope returned a non-object JSON response")
        return parsed

    def attempts(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for path in sorted(self.attempt_dir.glob("*.json")):
            row = load_json(path)
            row["_path"] = str(path)
            rows.append(row)
        return rows

    def _validate_attempt_history(self) -> dict[str, Any]:
        rows = self.attempts()
        hashes: set[str] = set()
        provider_tokens = 0
        local_tokens = 0
        successful = 0
        for row in rows:
            if row.get("schema_version") != "rq2a-guarded-dashscope-attempt-v1":
                raise ValueError("Guard attempt schema mismatch")
            batch_hashes = row.get("text_sha256", [])
            if not set(batch_hashes) <= self.all_allowed_hashes:
                raise ValueError("Guard history contains an unaudited text hash")
            if set(batch_hashes) & hashes:
                raise ValueError("Guard history contains a duplicate outbound text")
            hashes.update(batch_hashes)
            local_tokens += sum(int(value) for value in row.get("audit_token_counts", []))
            if row.get("state") == "complete":
                successful += 1
                usage = row.get("response", {}).get("usage", {})
                provider_tokens += int(usage.get("total_tokens", 0))
            elif row.get("state") in {"started", "failed"}:
                raise RuntimeError(
                    "A guarded outbound attempt is unresolved or failed; stop for review: "
                    f"{row['_path']}"
                )
            else:
                raise ValueError("Unknown guarded attempt state")
        if len(rows) > self.external["outbound_request_attempt_ceiling"]:
            raise ValueError("Outbound request-attempt ceiling exceeded")
        if successful > self.external["successful_api_call_ceiling"]:
            raise ValueError("Successful API-call ceiling exceeded")
        if local_tokens > self.external["local_audit_token_ceiling"]:
            raise ValueError("Local audit-token ceiling exceeded")
        if provider_tokens > self.external["provider_total_token_ceiling"]:
            raise ValueError("Provider token ceiling exceeded")
        return {
            "attempts": len(rows),
            "successful": successful,
            "unique_hashes": len(hashes),
            "sent_text_sha256": sorted(hashes),
            "local_audit_tokens": local_tokens,
            "provider_total_tokens": provider_tokens,
        }

    def _cache_client(self) -> RQ2aEmbeddingClient:
        return exact_cache_client()

    def restore_completed_responses(self, text_by_hash: dict[str, str]) -> None:
        client = self._cache_client()
        for row in self.attempts():
            if row.get("state") != "complete":
                continue
            response = row["response"]
            data = sorted(response.get("data", []), key=lambda item: item.get("index", 0))
            hashes = row["text_sha256"]
            if len(data) != len(hashes):
                raise ValueError("Stored guard response count mismatch")
            for digest, item in zip(hashes, data, strict=True):
                text = text_by_hash.get(digest)
                if text is None:
                    raise ValueError("Stored guard response is not in the current payload")
                embedding = item.get("embedding")
                if not isinstance(embedding, list) or len(embedding) != QWEN_DIMENSIONS:
                    raise ValueError("Stored guard response dimension mismatch")
                write_json_atomic(
                    client.cache_path(text),
                    {
                        "schema_version": "rq2a-embedding-cache-v1",
                        "provider": "qwen",
                        "base_url": QWEN_BASE_URL,
                        "model": QWEN_MODEL,
                        "dimensions": QWEN_DIMENSIONS,
                        "text_sha256": digest,
                        "audit_token_count": audit_token_count(text),
                        "embedding": [float(value) for value in embedding],
                        "provenance": {
                            "kind": "confirmatory_guard_response",
                            "attempt_sha256": sha256_file(Path(row["_path"])),
                        },
                    },
                )

    def cache_completed_batch(
        self,
        texts: list[str],
        response: dict[str, Any],
        attempt_path: Path,
    ) -> None:
        client = self._cache_client()
        data = sorted(response.get("data", []), key=lambda item: item.get("index", 0))
        for text, item in zip(texts, data, strict=True):
            digest = sha256_text(text)
            write_json_atomic(
                client.cache_path(text),
                {
                    "schema_version": "rq2a-embedding-cache-v1",
                    "provider": "qwen",
                    "base_url": QWEN_BASE_URL,
                    "model": QWEN_MODEL,
                    "dimensions": QWEN_DIMENSIONS,
                    "text_sha256": digest,
                    "audit_token_count": audit_token_count(text),
                    "embedding": [float(value) for value in item["embedding"]],
                    "provenance": {
                        "kind": "confirmatory_guard_response",
                        "attempt_sha256": sha256_file(attempt_path),
                    },
                },
            )

    def post_json(
        self,
        url: str,
        api_key: str,
        payload: dict[str, Any],
        timeout_seconds: int,
    ) -> dict[str, Any]:
        with exclusive_file_lock(GUARD_DIR / "transport.lock"):
            return self._post_json_locked(
                url,
                api_key,
                payload,
                timeout_seconds,
            )

    def _post_json_locked(
        self,
        url: str,
        api_key: str,
        payload: dict[str, Any],
        timeout_seconds: int,
    ) -> dict[str, Any]:
        history = self._validate_attempt_history()
        if not self.allow_new_requests:
            raise RuntimeError("Warm verification attempted an external request")
        if url != f"{QWEN_BASE_URL}/embeddings":
            raise ValueError("Guard rejected a non-approved endpoint")
        if payload.get("model") != QWEN_MODEL or payload.get("dimensions") != QWEN_DIMENSIONS:
            raise ValueError("Guard rejected model or dimension drift")
        texts = payload.get("input")
        if not isinstance(texts, list) or not texts or len(texts) > 10:
            raise ValueError("Guard rejected an invalid batch")
        if any(not isinstance(text, str) or not text for text in texts):
            raise ValueError("Guard rejected a non-text input")
        hashes = [sha256_text(text) for text in texts]
        if len(set(hashes)) != len(hashes):
            raise ValueError("Guard rejected duplicate texts within a batch")
        if not set(hashes) <= self.allowed_hashes:
            raise ValueError("Guard rejected text outside the category allowlist")
        if set(hashes) & set(history["sent_text_sha256"]):
            raise ValueError("Guard rejected an already-sent text hash")
        counts = [audit_token_count(text) for text in texts]
        if max(counts) > 262:
            raise ValueError("Guard rejected text above the preflight maximum")
        if history["attempts"] + 1 > self.external["outbound_request_attempt_ceiling"]:
            raise ValueError("No outbound request-attempt budget remains")
        if history["local_audit_tokens"] + sum(counts) > self.external["local_audit_token_ceiling"]:
            raise ValueError("No local audit-token budget remains")
        # Reserve twice the local batch count before sending.  The observed
        # development provider/local ratio was about 1.05, so this guard still
        # leaves a substantial conservative margin under the authorised cap.
        if history["provider_total_tokens"] + 2 * sum(counts) > self.external[
            "provider_total_token_ceiling"
        ]:
            raise ValueError("Insufficient provider-token headroom for this batch")
        index = history["attempts"] + 1
        attempt_path = self.attempt_dir / (
            f"{index:04d}-{self.category}-{sha256_json(hashes)[:16]}.json"
        )
        started = {
            "schema_version": "rq2a-guarded-dashscope-attempt-v1",
            "state": "started",
            "created_utc": utc_timestamp(),
            "category": self.category,
            "url": url,
            "model": QWEN_MODEL,
            "dimensions": QWEN_DIMENSIONS,
            "text_sha256": hashes,
            "audit_token_counts": counts,
            "plaintext_persisted": False,
        }
        write_json_atomic(attempt_path, started)
        try:
            response = self.transport(url, api_key, payload, timeout_seconds)
        except Exception as exc:
            write_json_atomic(
                attempt_path,
                {**started, "state": "failed", "finished_utc": utc_timestamp(), "error": str(exc)},
            )
            raise
        data = sorted(response.get("data", []), key=lambda item: item.get("index", 0))
        if len(data) != len(texts):
            raise RuntimeError("Guarded response embedding count mismatch")
        for item in data:
            embedding = item.get("embedding")
            if not isinstance(embedding, list) or len(embedding) != QWEN_DIMENSIONS:
                raise RuntimeError("Guarded response embedding dimension mismatch")
        usage = response.get("usage")
        if not isinstance(usage, dict) or not isinstance(usage.get("total_tokens"), int):
            raise RuntimeError("Guarded response has no auditable total_tokens usage")
        if history["provider_total_tokens"] + usage["total_tokens"] > self.external[
            "provider_total_token_ceiling"
        ]:
            raise RuntimeError("Provider token ceiling exceeded by returned usage")
        write_json_atomic(
            attempt_path,
            {
                **started,
                "state": "complete",
                "finished_utc": utc_timestamp(),
                "response": response,
            },
        )
        self.cache_completed_batch(texts, response, attempt_path)
        return response


def guarded_child(
    spec: RunSpec,
    packet_path: Path,
    seal_path: Path,
    freeze_path: Path,
    preflight_path: Path,
    independent_review_path: Path,
    authorisation_path: Path,
    grant_path: Path,
) -> None:
    packet, _, preflight = validate_packet_and_seal(
        packet_path, seal_path, freeze_path, preflight_path
    )
    validate_independent_review(
        independent_review_path,
        packet_path,
        seal_path,
        packet,
    )
    validate_authorisation(authorisation_path, packet_path, seal_path, packet)
    texts = payload_texts()
    text_by_hash = {
        sha256_text(text): text
        for text in texts["combined_unique_payload"]
    }
    guard = GuardedDashScopeTransport(
        category=spec.guarded_category or "",
        preflight=preflight,
        packet=packet,
        allow_new_requests=spec.role == "primary",
    )
    with exclusive_file_lock(GUARD_DIR / "transport.lock"):
        guard.restore_completed_responses(text_by_hash)
    import run_rq2a_fixed_candidate_matrix as fixed

    original_post = fixed.post_json
    original_argv = sys.argv

    def guarded_post_json(
        url: str,
        api_key: str,
        payload: dict[str, Any],
        timeout_seconds: int,
    ) -> dict[str, Any]:
        return guard.post_json(url, api_key, payload, timeout_seconds)

    setattr(
        guarded_post_json,
        "_rq2a_confirmatory_grant_sha256",
        sha256_file(grant_path),
    )
    fixed.post_json = guarded_post_json
    try:
        common = [
            "--split",
            "confirmatory",
            "--output-dir",
            str(CONFIRMATORY_ROOT),
            "--run-id",
            spec.run_id,
            "--evidence-role",
            spec.role,
            "--confirmatory-freeze-manifest",
            str(freeze_path),
            "--confirmatory-controller-grant",
            str(grant_path),
            "--qwen-base-url",
            QWEN_BASE_URL,
            "--qwen-model",
            QWEN_MODEL,
            "--qwen-dimensions",
            str(QWEN_DIMENSIONS),
            "--qwen-batch-size",
            "10",
            "--max-audit-tokens",
            "8192",
        ]
        if spec.runner == "guarded-fixed":
            sys.argv = [
                str(Path(fixed.__file__)),
                *common,
                "--selectors",
                "qwen-single-vector",
                "--representations",
                *spec.representations,
            ]
            fixed.main()
        elif spec.runner == "guarded-field":
            import run_rq2a_field_aware_selector as fielded

            sys.argv = [
                str(Path(fielded.__file__)),
                *common,
                "--aggregations",
                "uniform-top-two",
                "--aggregation-choice-file",
                str(AGGREGATION_CHOICE),
            ]
            fielded.main()
        else:
            raise ValueError(f"Not a guarded run: {spec.run_id}")
    finally:
        fixed.post_json = original_post
        sys.argv = original_argv


def grant_path(label: str) -> Path:
    return CONTROLLER_DIR / "grants" / f"{label}.json"


def fixed_run_invocation(spec: RunSpec, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "entry_point": "run_rq2a_fixed_candidate_matrix.py",
        "split": "confirmatory",
        "output_dir": str(CONFIRMATORY_ROOT.resolve()),
        "run_id": spec.run_id,
        "evidence_role": spec.role,
        "selectors": list(spec.selectors),
        "representations": list(spec.representations),
        "clusters_per_field": None,
        "overwrite": False,
        "confirmatory_freeze_sha256": sha256_file(args.freeze),
        "bm25_k1": 1.5,
        "bm25_b": 0.75,
        "qwen_base_url": QWEN_BASE_URL,
        "qwen_model": QWEN_MODEL,
        "qwen_dimensions": QWEN_DIMENSIONS,
        "qwen_batch_size": 10,
        "max_audit_tokens": 8192,
        "skillrouter_model": SKILLROUTER_MODEL,
        "skillrouter_revision": SKILLROUTER_REVISION,
        "skillrouter_max_length": 2048,
        "skillrouter_batch_size": 4,
        "skillrouter_local_files_only": (
            "skillrouter-cross-encoder" in spec.selectors
        ),
    }


def field_run_invocation(spec: RunSpec, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "entry_point": "run_rq2a_field_aware_selector.py",
        "split": "confirmatory",
        "output_dir": str(CONFIRMATORY_ROOT.resolve()),
        "run_id": spec.run_id,
        "evidence_role": spec.role,
        "aggregations": list(spec.aggregations),
        "representation": FIELD_AWARE_REPRESENTATION,
        "clusters_per_field": None,
        "overwrite": False,
        "freeze_aggregation_choice": False,
        "aggregation_choice_sha256": sha256_file(AGGREGATION_CHOICE),
        "confirmatory_freeze_sha256": sha256_file(args.freeze),
        "qwen_base_url": QWEN_BASE_URL,
        "qwen_model": QWEN_MODEL,
        "qwen_dimensions": QWEN_DIMENSIONS,
        "qwen_batch_size": 10,
        "max_audit_tokens": 8192,
    }


def analysis_invocation(args: argparse.Namespace) -> dict[str, Any]:
    primary_dirs = sorted(
        str((CONFIRMATORY_ROOT / run_id).resolve())
        for run_id in PRIMARY_RUN_IDS
    )
    return {
        "entry_point": "analyze_rq2a_matched_content.py",
        "run_dirs": primary_dirs,
        "analysis_spec_sha256": sha256_file(INPUT_DIR / "analysis_spec.json"),
        "output_dir": str(ANALYSIS_ROOT.resolve()),
        "analysis_id": "confirmatory-complete-v1",
        "allow_confirmatory": True,
        "confirmatory_freeze_sha256": sha256_file(args.freeze),
    }


def ensure_grant(
    label: str,
    *,
    action: str,
    invocation: dict[str, Any],
    args: argparse.Namespace,
) -> Path:
    path = grant_path(label)
    payload = {
        "schema_version": "rq2a-confirmatory-controller-grant-v1",
        "state": "active_for_exact_invocation",
        "created_utc": utc_timestamp(),
        "label": label,
        "action": action,
        "invocation": invocation,
        "invocation_sha256": sha256_json(invocation),
        "authorisation_artifacts": {
            "packet": {
                "path": str(args.packet.resolve()),
                "sha256": sha256_file(args.packet),
            },
            "seal": {
                "path": str(args.seal.resolve()),
                "sha256": sha256_file(args.seal),
            },
            "independent_review": {
                "path": str(args.independent_review_record.resolve()),
                "sha256": sha256_file(args.independent_review_record),
            },
            "user_authorisation": {
                "path": str(args.authorisation_record.resolve()),
                "sha256": sha256_file(args.authorisation_record),
            },
        },
    }
    if path.is_file():
        existing = load_json(path)
        comparable = {**payload, "created_utc": existing.get("created_utc")}
        if existing != comparable:
            raise ValueError(f"Existing controller grant differs: {path}")
        return path
    write_json_atomic(path, payload)
    return path


def ensure_run_grant(spec: RunSpec, args: argparse.Namespace) -> Path:
    if spec.runner.endswith("field"):
        action = "field_aware_scoring"
        invocation = field_run_invocation(spec, args)
    else:
        action = "fixed_scoring"
        invocation = fixed_run_invocation(spec, args)
    return ensure_grant(
        spec.run_id,
        action=action,
        invocation=invocation,
        args=args,
    )


def direct_command(spec: RunSpec, args: argparse.Namespace) -> list[str]:
    controller_grant = ensure_run_grant(spec, args)
    if spec.runner.startswith("guarded"):
        return [
            sys.executable,
            str(Path(__file__).resolve()),
            "--internal-guarded-run",
            spec.run_id,
            "--packet",
            str(args.packet),
            "--seal",
            str(args.seal),
            "--freeze",
            str(args.freeze),
            "--preflight",
            str(args.preflight),
            "--independent-review-record",
            str(args.independent_review_record),
            "--authorisation-record",
            str(args.authorisation_record),
            "--confirmatory-controller-grant",
            str(controller_grant),
        ]
    command = [
        sys.executable,
        str(ROOT / "scripts" / "run_rq2a_fixed_candidate_matrix.py"),
        "--split",
        "confirmatory",
        "--output-dir",
        str(CONFIRMATORY_ROOT),
        "--run-id",
        spec.run_id,
        "--evidence-role",
        spec.role,
        "--confirmatory-freeze-manifest",
        str(args.freeze),
        "--confirmatory-controller-grant",
        str(controller_grant),
        "--selectors",
        *spec.selectors,
        "--representations",
        *spec.representations,
    ]
    if "skillrouter-cross-encoder" in spec.selectors:
        command.extend(
            [
                "--skillrouter-model",
                SKILLROUTER_MODEL,
                "--skillrouter-revision",
                SKILLROUTER_REVISION,
                "--skillrouter-max-length",
                "2048",
                "--skillrouter-batch-size",
                "4",
                "--skillrouter-local-files-only",
            ]
        )
    return command


def run_logged_step(label: str, command: list[str]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{label}.log"
    started = time.monotonic()
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n===== controller attempt {utc_timestamp()} / {label} =====\n"
        )
        handle.flush()
        process = subprocess.Popen(
            command,
            cwd=WORKSPACE,
            stdout=handle,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(f"{label}: started", flush=True)
        while True:
            try:
                process.wait(timeout=30)
                break
            except subprocess.TimeoutExpired:
                elapsed = time.monotonic() - started
                print(f"{label}: running, elapsed {elapsed:.0f}s", flush=True)
    if process.returncode != 0:
        tail = log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-30:]
        raise RuntimeError(
            f"{label} failed with exit code {process.returncode}; log tail:\n"
            + "\n".join(tail)
        )
    print(f"{label}: complete in {time.monotonic() - started:.1f}s", flush=True)


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {
            "schema_version": "rq2a-confirmatory-controller-state-v1",
            "controller_id": CONTROLLER_ID,
            "state": "not_started",
            "completed_steps": [],
            "step_records": [],
        }
    return load_json(STATE_PATH)


def clear_stale_failure_metadata(state: dict[str, Any]) -> dict[str, Any]:
    """Remove failure-only fields before a fresh or successful state transition."""
    return {
        key: state.pop(key)
        for key in ("failed_step", "failure")
        if key in state
    }


def record_step(state: dict[str, Any], label: str, record: dict[str, Any]) -> None:
    if label not in state["completed_steps"]:
        state["completed_steps"].append(label)
        state["step_records"].append(
            {"step": label, "completed_utc": utc_timestamp(), **record}
        )
    state["state"] = "running"
    state["updated_utc"] = utc_timestamp()
    write_json_atomic(STATE_PATH, state)


def analysis_commands(args: argparse.Namespace) -> list[tuple[str, list[str]]]:
    primary_dirs = [str(CONFIRMATORY_ROOT / run_id) for run_id in PRIMARY_RUN_IDS]
    analysis = [
        sys.executable,
        str(ROOT / "scripts" / "analyze_rq2a_matched_content.py"),
    ]
    for directory in primary_dirs:
        analysis.extend(["--run-dir", directory])
    controller_grant = ensure_grant(
        "confirmatory-complete-analysis",
        action="confirmatory_analysis",
        invocation=analysis_invocation(args),
        args=args,
    )
    analysis.extend(
        [
            "--analysis-id",
            "confirmatory-complete-v1",
            "--allow-confirmatory",
            "--confirmatory-freeze-manifest",
            str(args.freeze),
            "--confirmatory-controller-grant",
            str(controller_grant),
        ]
    )
    cost = [
        sys.executable,
        str(ROOT / "scripts" / "build_rq2a_cost_ledger.py"),
        "--run-root",
        str(CONFIRMATORY_ROOT),
        "--split",
        "confirmatory",
        "--ledger-id",
        "confirmatory-complete-cost-v1",
        "--qwen-input-price-per-million",
        "0.07",
        "--price-currency",
        "USD",
        "--price-source",
        "https://www.alibabacloud.com/help/en/model-studio/embedding",
        "--price-date",
        "2026-08-01",
        "--guard-attempt-dir",
        str(GUARD_DIR / "attempts"),
    ]
    failures = [
        sys.executable,
        str(ROOT / "scripts" / "analyze_rq2a_confirmatory_failures.py"),
    ]
    for directory in primary_dirs:
        failures.extend(["--run-dir", directory])
    failures.extend(
        [
            "--failure-spec",
            str(DEFAULT_FAILURE_SPEC),
            "--confirmatory-freeze-manifest",
            str(args.freeze),
            "--analysis-id",
            "confirmatory-failures-v1",
        ]
    )
    return [
        ("confirmatory-complete-analysis", analysis),
        ("confirmatory-complete-cost", cost),
        ("confirmatory-failures", failures),
    ]


def quarantine_analysis_output(label: str, output_file: Path) -> Path | None:
    directory = output_file.parent
    if not directory.exists() or not any(directory.iterdir()):
        return None
    quarantine_root = CONTROLLER_DIR / "quarantine-analysis"
    quarantine_root.mkdir(parents=True, exist_ok=True)
    destination = quarantine_root / (
        f"{directory.name}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    )
    if destination.exists():
        raise FileExistsError(f"Analysis quarantine destination exists: {destination}")
    inventory = incomplete_run_files(directory)
    shutil.move(str(directory), str(destination))
    write_json_atomic(
        destination / "quarantine_manifest.json",
        {
            "schema_version": "rq2a-confirmatory-analysis-quarantine-v1",
            "created_utc": utc_timestamp(),
            "step": label,
            "reason": "expected final output missing before safe resume",
            "files_before_move": inventory,
        },
    )
    return destination


def current_run_provenance(run_ids: tuple[str, ...]) -> dict[str, dict[str, str]]:
    return {
        run_id: {
            "manifest_sha256": sha256_file(
                CONFIRMATORY_ROOT / run_id / "manifest.json"
            ),
            "rows_sha256": sha256_file(
                CONFIRMATORY_ROOT / run_id / "rows.jsonl"
            ),
        }
        for run_id in run_ids
    }


def validate_analysis_output(label: str, path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Missing confirmatory {label} output: {path}")
    payload = load_json(path)
    primary = current_run_provenance(PRIMARY_RUN_IDS)
    if label == "analysis":
        if payload.get("split") != "confirmatory":
            raise ValueError("Confirmatory analysis split mismatch")
        if payload.get("row_count") != 13_200:
            raise ValueError("Confirmatory analysis row count mismatch")
        if payload.get("quality_checks", {}).get(
            "unique_condition_prompt_rows"
        ) != "pass":
            raise ValueError("Confirmatory analysis identity check failed")
        recorded = {
            row["run_id"]: {
                "manifest_sha256": row["manifest_sha256"],
                "rows_sha256": row["rows_sha256"],
            }
            for row in payload.get("runs", [])
        }
        if recorded != primary:
            raise ValueError("Confirmatory analysis is stale for current primary runs")
    elif label == "cost":
        all_runs = current_run_provenance(tuple(RUN_BY_ID))
        recorded = {
            row["run_id"]: {
                "manifest_sha256": row["manifest_sha256"],
                "rows_sha256": row["rows_sha256"],
            }
            for row in payload.get("runs", [])
        }
        if recorded != all_runs:
            raise ValueError("Confirmatory cost ledger is stale for current runs")
        current_guarded = guarded_attempt_history(GUARD_DIR / "attempts")
        if payload.get("guarded_attempt_history") != current_guarded:
            raise ValueError(
                "Confirmatory cost ledger is stale for guarded paid usage"
            )
    elif label == "failures":
        if payload.get("primary_row_count") != 13_200:
            raise ValueError("Failure report did not use the full primary matrix")
        recorded = {
            row["run_id"]: {
                "manifest_sha256": row["manifest_sha256"],
                "rows_sha256": row["rows_sha256"],
            }
            for row in payload.get("primary_runs", [])
        }
        if recorded != primary:
            raise ValueError("Confirmatory failure report is stale for current runs")
    else:
        raise ValueError(f"Unknown analysis output label: {label}")
    return sha256_file(path)


def validate_analysis_outputs() -> dict[str, str]:
    expected = {
        "analysis": ANALYSIS_ROOT / "confirmatory-complete-v1" / "analysis.json",
        "cost": ANALYSIS_ROOT / "confirmatory-complete-cost-v1" / "cost_ledger.json",
        "failures": ANALYSIS_ROOT / "confirmatory-failures-v1" / "failure_report.json",
    }
    return {
        label: validate_analysis_output(label, path)
        for label, path in expected.items()
    }


def _execute_locked(args: argparse.Namespace) -> None:
    packet, _, preflight = validate_packet_and_seal(
        args.packet, args.seal, args.freeze, args.preflight
    )
    review = validate_independent_review(
        args.independent_review_record,
        args.packet,
        args.seal,
        packet,
    )
    authorisation = validate_authorisation(
        args.authorisation_record, args.packet, args.seal, packet
    )
    runtime = validate_runtime_environment(require_api_key=True)
    payload = validate_current_payload_state(preflight)
    root_state = validate_confirmatory_root(args)
    CONTROLLER_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    clear_stale_failure_metadata(state)
    state.update(
        {
            "state": "running",
            "packet_sha256": sha256_file(args.packet),
            "seal_sha256": sha256_file(args.seal),
            "authorisation_sha256": sha256_file(args.authorisation_record),
            "independent_review_sha256": sha256_file(
                args.independent_review_record
            ),
            "independent_reviewer_agent_id": review.get("reviewer_agent_id"),
            "authorisation_created_utc": authorisation.get("created_utc"),
            "runtime": runtime,
            "payload_state_at_start": payload,
            "confirmatory_root_at_start": root_state,
        }
    )
    write_json_atomic(STATE_PATH, state)

    for spec in RUN_SPECS:
        label = spec.run_id
        if run_dir(spec).is_dir() and (run_dir(spec) / "manifest.json").is_file():
            record = validate_run(spec, args)
            record_step(state, label, {**record, "resume_action": "validated_and_skipped"})
            continue
        if run_dir(spec).exists() and any(run_dir(spec).iterdir()):
            quarantine_incomplete(spec, "incomplete_before_controller_resume")
        command = direct_command(spec, args)
        try:
            run_logged_step(label, command)
            record = validate_run(spec, args)
        except Exception as exc:
            quarantine_incomplete(spec, f"step_failed: {exc}")
            state["state"] = "failed"
            state["failed_step"] = label
            state["failure"] = str(exc)
            state["updated_utc"] = utc_timestamp()
            write_json_atomic(STATE_PATH, state)
            raise
        record_step(state, label, record)

    matrix = validate_complete_primary_matrix()
    warm = validate_warm_reproduction()
    record_step(state, "complete-matrix-gate", {"matrix": matrix, "warm_digests": warm})

    for label, command in analysis_commands(args):
        output_label, output_exists = {
            "confirmatory-complete-analysis": (
                "analysis",
                ANALYSIS_ROOT / "confirmatory-complete-v1" / "analysis.json",
            ),
            "confirmatory-complete-cost": (
                "cost",
                ANALYSIS_ROOT
                / "confirmatory-complete-cost-v1"
                / "cost_ledger.json",
            ),
            "confirmatory-failures": (
                "failures",
                ANALYSIS_ROOT
                / "confirmatory-failures-v1"
                / "failure_report.json",
            ),
        }[label]
        valid_existing = False
        if output_exists.is_file():
            try:
                validate_analysis_output(output_label, output_exists)
                valid_existing = True
            except (KeyError, TypeError, ValueError):
                quarantine_analysis_output(label, output_exists)
        if not valid_existing:
            quarantine_analysis_output(label, output_exists)
            run_logged_step(label, command)
        output_sha256 = validate_analysis_output(output_label, output_exists)
        record_step(
            state,
            label,
            {"output": str(output_exists), "sha256": output_sha256},
        )

    outputs = validate_analysis_outputs()
    guard = GuardedDashScopeTransport(
        category="single_vector_documents",
        preflight=preflight,
        packet=packet,
        allow_new_requests=False,
    )._validate_attempt_history()
    guard.pop("sent_text_sha256", None)
    clear_stale_failure_metadata(state)
    state.update(
        {
            "state": "complete_pending_user_results_review",
            "completed_utc": utc_timestamp(),
            "matrix": matrix,
            "warm_reproduction": warm,
            "guard_totals": guard,
            "analysis_outputs": outputs,
            "thesis_write": "not_performed_pending_user_review",
        }
    )
    write_json_atomic(STATE_PATH, state)
    print(
        json.dumps(
            {
                "status": "PASS",
                "state": state["state"],
                "primary_rows": matrix["row_count"],
                "conditions": matrix["condition_count"],
                "guard": guard,
                "analysis_outputs": outputs,
                "thesis_write": "not_performed",
            },
            indent=2,
        )
    )


def execute(args: argparse.Namespace) -> None:
    CONTROLLER_DIR.mkdir(parents=True, exist_ok=True)
    with exclusive_file_lock(CONTROLLER_DIR / "sequence.lock"):
        _execute_locked(args)


def preflight(args: argparse.Namespace) -> None:
    packet, _, frozen_preflight = validate_packet_and_seal(
        args.packet, args.seal, args.freeze, args.preflight
    )
    review = validate_independent_review(
        args.independent_review_record,
        args.packet,
        args.seal,
        packet,
    )
    runtime = validate_runtime_environment(require_api_key=False)
    payload = validate_current_payload_state(frozen_preflight)
    root = validate_confirmatory_root()
    commands = {
        spec.run_id: {
            "runner": spec.runner,
            "role": spec.role,
            "selectors": list(spec.selectors),
            "representations": list(spec.representations),
            "aggregations": list(spec.aggregations),
            "expected_rows": spec.expected_rows,
            "controller_grant": str(grant_path(spec.run_id)),
        }
        for spec in RUN_SPECS
    }
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": "offline_preflight_only",
                "network_requests": 0,
                "packet_sha256": sha256_file(args.packet),
                "seal_sha256": sha256_file(args.seal),
                "freeze_sha256": sha256_file(args.freeze),
                "preflight_sha256": sha256_file(args.preflight),
                "independent_review_sha256": sha256_file(
                    args.independent_review_record
                ),
                "independent_reviewer_agent_id": review.get(
                    "reviewer_agent_id"
                ),
                "runtime": runtime,
                "payload": payload,
                "confirmatory_root": root,
                "closed_sequence_commands": commands,
                "user_authorised": False,
            },
            indent=2,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight-only", action="store_true")
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--internal-guarded-run", choices=sorted(RUN_BY_ID))
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--seal", type=Path, default=DEFAULT_SEAL)
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--preflight", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument(
        "--authorisation-record",
        type=Path,
        default=DEFAULT_AUTHORISATION,
    )
    parser.add_argument(
        "--independent-review-record",
        type=Path,
        default=DEFAULT_INDEPENDENT_REVIEW,
    )
    parser.add_argument("--confirmatory-controller-grant", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.internal_guarded_run:
        spec = RUN_BY_ID[args.internal_guarded_run]
        if not spec.runner.startswith("guarded"):
            raise ValueError("Internal guarded mode accepts only frozen Qwen runs")
        guarded_child(
            spec,
            args.packet,
            args.seal,
            args.freeze,
            args.preflight,
            args.independent_review_record,
            args.authorisation_record,
            args.confirmatory_controller_grant,
        )
    elif args.preflight_only:
        preflight(args)
    else:
        execute(args)


if __name__ == "__main__":
    main()
