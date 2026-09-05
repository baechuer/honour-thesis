#!/usr/bin/env python3
"""Shared loading, validation, metrics, and output helpers for RQ2a selectors."""

from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


PROTOCOL_VERSION = "rq2a-matched-content-v1.0"
SERIALISER_VERSION = "rq2a-serialiser-v1.4"
RESULT_SCHEMA_VERSION = "rq2a-fixed-candidate-result-v1"
RUN_MANIFEST_SCHEMA_VERSION = "rq2a-selector-run-manifest-v1"
CONFIRMATORY_FREEZE_SCHEMA_VERSION = "rq2a-confirmatory-freeze-manifest-v1"
CONFIRMATORY_GRANT_SCHEMA_VERSION = "rq2a-confirmatory-controller-grant-v1"
CONFIRMATORY_REVIEW_SCHEMA_VERSION = (
    "rq2a-confirmatory-independent-review-pass-v1"
)
EPSILON = 1e-9
TOKEN_RE = re.compile(r"[a-z0-9]+")
AUDIT_TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)

FIELD_ORDER = [
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "dependency_resource",
    "boundary_not_for",
    "success_verification",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-._" else "_" for char in value)
    return cleaned.strip("_") or "default"


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def audit_token_count(text: str) -> int:
    return len(AUDIT_TOKEN_RE.findall(text))


def lexical_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected one JSON object")
            rows.append(row)
    return rows


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_jsonl_atomic(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError(f"Vector length mismatch: {len(left)} != {len(right)}")
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def bm25_scores(
    query: str,
    documents: list[str],
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[float]:
    """Score one query against its fixed three-document sibling corpus."""
    document_tokens = [lexical_tokens(document) for document in documents]
    query_terms = lexical_tokens(query)
    document_count = len(document_tokens)
    average_length = statistics.mean([len(row) for row in document_tokens] or [1]) or 1
    document_frequency = Counter(
        term
        for term in set(query_terms)
        for row in document_tokens
        if term in row
    )
    scores: list[float] = []
    for row in document_tokens:
        counts = Counter(row)
        document_length = len(row) or 1
        score = 0.0
        for term in query_terms:
            frequency = counts.get(term, 0)
            if not frequency:
                continue
            frequency_in_corpus = document_frequency.get(term, 0)
            inverse_document_frequency = math.log(
                1
                + (
                    document_count
                    - frequency_in_corpus
                    + 0.5
                )
                / (frequency_in_corpus + 0.5)
            )
            denominator = frequency + k1 * (
                1 - b + b * document_length / average_length
            )
            score += inverse_document_frequency * (
                frequency * (k1 + 1)
            ) / denominator
        scores.append(score)
    return scores


def tie_aware_metrics(
    candidate_ids: list[str],
    scores: list[float],
    gold_skill_id: str,
    *,
    epsilon: float = EPSILON,
) -> dict[str, Any]:
    if len(candidate_ids) != 3 or len(scores) != 3:
        raise ValueError("RQ2a requires exactly three candidates and three scores")
    if len(set(candidate_ids)) != 3:
        raise ValueError("RQ2a candidate identities must be unique")
    if gold_skill_id not in candidate_ids:
        raise ValueError(f"Gold skill {gold_skill_id} is not a candidate")
    if any(not math.isfinite(float(score)) for score in scores):
        raise ValueError("All selector scores must be finite")

    gold_index = candidate_ids.index(gold_skill_id)
    gold_score = float(scores[gold_index])
    alternative_scores = [
        float(score)
        for index, score in enumerate(scores)
        if index != gold_index
    ]
    greater = sum(score > gold_score + epsilon for score in scores)
    tied_with_gold = sum(abs(score - gold_score) <= epsilon for score in scores)
    rank_min = greater + 1
    rank_max = greater + tied_with_gold
    top1_tie_adjusted = (
        1.0 / tied_with_gold if greater == 0 and tied_with_gold else 0.0
    )
    mrr_tie_adjusted = statistics.mean(
        1.0 / rank for rank in range(rank_min, rank_max + 1)
    )

    deterministic_pairs = sorted(
        zip(candidate_ids, scores, strict=True),
        key=lambda item: (-float(item[1]), item[0]),
    )
    deterministic_ranking = [candidate_id for candidate_id, _ in deterministic_pairs]
    maximum_score = max(float(score) for score in scores)
    top_tie_size = sum(abs(float(score) - maximum_score) <= epsilon for score in scores)

    return {
        "deterministic_ranking": deterministic_ranking,
        "top1_deterministic_sensitivity": float(
            deterministic_ranking[0] == gold_skill_id
        ),
        "top1_tie_adjusted": top1_tie_adjusted,
        "mrr_tie_adjusted": mrr_tie_adjusted,
        "gold_rank_min": rank_min,
        "gold_rank_max": rank_max,
        "gold_tie_size": tied_with_gold,
        "gold_score": gold_score,
        "gold_margin": gold_score - max(alternative_scores),
        "near_neighbour_strict_confusion": float(
            max(alternative_scores) > gold_score + epsilon
        ),
        "any_top_tie": float(top_tie_size > 1),
        "top_tie_size": top_tie_size,
        "epsilon": epsilon,
    }


def selector_visible_counts(text: str) -> dict[str, int]:
    return {
        "character_count": len(text),
        "utf8_byte_count": len(text.encode("utf-8")),
        "word_count": len(text.split()),
        "audit_token_count": audit_token_count(text),
    }


def load_protocol(input_dir: Path) -> dict[str, Any]:
    protocol_path = input_dir / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if protocol.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError(
            f"Unexpected protocol version: {protocol.get('protocol_version')}"
        )
    if protocol.get("serialiser_version") != SERIALISER_VERSION:
        raise ValueError(
            f"Unexpected serialiser version: {protocol.get('serialiser_version')}"
        )
    if not protocol.get("thesis_write_blocked_pending_user_review"):
        raise ValueError("RQ2a thesis-write boundary is not present in protocol.json")
    return protocol


def validate_confirmatory_freeze_manifest(
    path: Path,
    *,
    input_dir: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Load a freeze manifest and prove its referenced state is unchanged."""
    if not path.exists():
        raise FileNotFoundError(f"Confirmatory freeze manifest is missing: {path}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Confirmatory freeze manifest must be a JSON object")
    if manifest.get("schema_version") != CONFIRMATORY_FREEZE_SCHEMA_VERSION:
        raise ValueError("Confirmatory freeze manifest schema mismatch")
    if manifest.get("state") != "frozen_before_confirmatory":
        raise ValueError("Confirmatory freeze manifest is not frozen")
    if manifest.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError("Confirmatory freeze protocol version mismatch")
    if manifest.get("serialiser_version") != SERIALISER_VERSION:
        raise ValueError("Confirmatory freeze serialiser version mismatch")

    def verify_hashes(label: str, entries: Any) -> None:
        if not isinstance(entries, dict) or not entries:
            raise ValueError(f"Confirmatory freeze has no {label} hashes")
        for raw_path, expected_hash in entries.items():
            referenced = Path(raw_path)
            if not referenced.exists():
                raise FileNotFoundError(
                    f"Confirmatory freeze {label} artifact is missing: {referenced}"
                )
            if sha256_file(referenced) != expected_hash:
                raise ValueError(
                    f"Confirmatory freeze {label} hash mismatch: {referenced}"
                )

    verify_hashes("input", manifest.get("input_artifacts"))
    verify_hashes("implementation", manifest.get("implementation_sha256"))

    development_runs = manifest.get("development_runs")
    if not isinstance(development_runs, list) or not development_runs:
        raise ValueError("Confirmatory freeze has no development-run provenance")
    seen_development_runs: set[str] = set()
    for row in development_runs:
        if not isinstance(row, dict):
            raise ValueError("Confirmatory freeze development-run row is malformed")
        run_id = row.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("Confirmatory freeze development run has no run_id")
        if run_id in seen_development_runs:
            raise ValueError("Confirmatory freeze has duplicate development runs")
        seen_development_runs.add(run_id)
        for kind in ("manifest", "rows"):
            raw_path = row.get(f"{kind}_path")
            expected_hash = row.get(f"{kind}_sha256")
            if not isinstance(raw_path, str) or not raw_path:
                raise ValueError(
                    f"Confirmatory freeze {run_id} has no {kind} path"
                )
            referenced = Path(raw_path)
            if not referenced.is_file():
                raise FileNotFoundError(
                    f"Confirmatory freeze {run_id} {kind} is missing: {referenced}"
                )
            if sha256_file(referenced) != expected_hash:
                raise ValueError(
                    f"Confirmatory freeze {run_id} {kind} hash mismatch"
                )
        development_manifest = json.loads(
            Path(row["manifest_path"]).read_text(encoding="utf-8")
        )
        if development_manifest.get("run_id") != run_id:
            raise ValueError(
                f"Confirmatory freeze development run_id mismatch: {run_id}"
            )

    frozen_input_dir = input_dir
    if frozen_input_dir is None:
        protocol_paths = [
            Path(raw_path)
            for raw_path in manifest["input_artifacts"]
            if Path(raw_path).name == "protocol.json"
        ]
        if len(protocol_paths) != 1:
            raise ValueError(
                "Confirmatory freeze must identify exactly one protocol.json"
            )
        frozen_input_dir = protocol_paths[0].parent
    representation_hashes = manifest.get("representation_sha256")
    if not isinstance(representation_hashes, dict) or not representation_hashes:
        raise ValueError("Confirmatory freeze has no representation hashes")
    for representation, expected_hash in representation_hashes.items():
        representation_path = (
            frozen_input_dir / "representations" / f"{representation}.jsonl"
        )
        if not representation_path.exists():
            raise FileNotFoundError(
                "Confirmatory freeze representation is missing: "
                f"{representation_path}"
            )
        if sha256_file(representation_path) != expected_hash:
            raise ValueError(
                "Confirmatory freeze representation hash mismatch: "
                f"{representation_path}"
            )

    aggregation = manifest.get("aggregation_choice")
    if not isinstance(aggregation, dict):
        raise ValueError("Confirmatory freeze aggregation choice is missing")
    aggregation_path_value = aggregation.get("path")
    if not isinstance(aggregation_path_value, str) or not aggregation_path_value:
        raise ValueError("Frozen aggregation choice path is missing")
    aggregation_path = Path(aggregation_path_value)
    if not aggregation_path.is_file():
        raise FileNotFoundError(
            f"Frozen aggregation choice is missing: {aggregation_path}"
        )
    if sha256_file(aggregation_path) != aggregation.get("sha256"):
        raise ValueError("Frozen aggregation choice hash mismatch")
    aggregation_payload = json.loads(
        aggregation_path.read_text(encoding="utf-8")
    )
    if aggregation_payload.get("state") != "frozen_development_choice":
        raise ValueError("Aggregation choice is not a frozen development choice")
    if (
        aggregation_payload.get("selected_selector")
        != aggregation.get("selected_selector")
    ):
        raise ValueError("Frozen aggregation selector mismatch")

    analysis = manifest.get("development_analysis")
    if not isinstance(analysis, dict):
        raise ValueError("Confirmatory freeze development analysis is missing")
    analysis_path_value = analysis.get("path")
    if not isinstance(analysis_path_value, str) or not analysis_path_value:
        raise ValueError("Frozen development analysis path is missing")
    analysis_path = Path(analysis_path_value)
    if not analysis_path.is_file():
        raise FileNotFoundError(
            f"Frozen development analysis is missing: {analysis_path}"
        )
    if sha256_file(analysis_path) != analysis.get("sha256"):
        raise ValueError("Frozen development analysis hash mismatch")

    if output_dir is not None:
        frozen_output = Path(str(manifest.get("confirmatory_output_root", "")))
        if frozen_output.resolve() != output_dir.resolve():
            raise ValueError(
                "Confirmatory output root differs from the frozen protocol"
            )
    return manifest


def validate_confirmatory_execution_grant(
    path: Path | None,
    *,
    action: str,
    invocation: dict[str, Any],
) -> dict[str, Any]:
    """Require one user-authorised, hash-bound controller grant.

    The grant does not carry a secret.  Its purpose is fail-closed provenance:
    generic entry points cannot run a confirmatory subset or altered condition,
    and Qwen entry points additionally require the controller-installed guarded
    transport marker.
    """
    if path is None or not path.is_file():
        raise ValueError(
            "Confirmatory execution requires an exact controller grant"
        )
    grant = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(grant, dict):
        raise ValueError("Confirmatory controller grant must be a JSON object")
    if grant.get("schema_version") != CONFIRMATORY_GRANT_SCHEMA_VERSION:
        raise ValueError("Confirmatory controller grant schema mismatch")
    if grant.get("state") != "active_for_exact_invocation":
        raise ValueError("Confirmatory controller grant is not active")
    if grant.get("action") != action:
        raise ValueError("Confirmatory controller grant action mismatch")
    if grant.get("invocation_sha256") != sha256_json(invocation):
        raise ValueError("Confirmatory controller grant invocation mismatch")

    artifacts = grant.get("authorisation_artifacts", {})
    required = {
        "packet": "rq2a-confirmatory-authorisation-packet-v1",
        "seal": "rq2a-confirmatory-execution-seal-v1",
        "independent_review": CONFIRMATORY_REVIEW_SCHEMA_VERSION,
        "user_authorisation": "rq2a-confirmatory-user-authorisation-v1",
    }
    loaded: dict[str, dict[str, Any]] = {}
    for name, schema in required.items():
        artifact = artifacts.get(name, {})
        artifact_path = Path(str(artifact.get("path", "")))
        if not artifact_path.is_file():
            raise FileNotFoundError(
                f"Confirmatory grant {name} artifact is missing: {artifact_path}"
            )
        if sha256_file(artifact_path) != artifact.get("sha256"):
            raise ValueError(f"Confirmatory grant {name} hash mismatch")
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != schema:
            raise ValueError(f"Confirmatory grant {name} schema mismatch")
        loaded[name] = payload

    packet = loaded["packet"]
    seal = loaded["seal"]
    review = loaded["independent_review"]
    authorisation = loaded["user_authorisation"]
    if packet.get("state") != "awaiting_independent_review_and_user_authorisation":
        raise ValueError(
            "Confirmatory packet is not the immutable review/authorisation packet"
        )
    if seal.get("state") != "sealed_before_user_authorisation":
        raise ValueError("Confirmatory execution seal state mismatch")
    if review.get("state") != "pass" or review.get("verdict") != "PASS":
        raise ValueError("Confirmatory independent review is not a PASS")
    if review.get("reviewer_agent_id") in {None, ""}:
        raise ValueError("Confirmatory independent review has no reviewer identity")
    if review.get("packet_sha256") != artifacts["packet"]["sha256"]:
        raise ValueError("Independent review does not bind the grant packet")
    if review.get("execution_seal_sha256") != artifacts["seal"]["sha256"]:
        raise ValueError("Independent review does not bind the grant seal")
    if review.get("approval_scope_sha256") != sha256_json(
        packet.get("approval_scope_digest")
    ):
        raise ValueError("Independent review does not bind the approval scope")
    if review.get("network_or_scoring_performed") is not False:
        raise ValueError("Independent review execution boundary is not recorded")
    if authorisation.get("state") != "authorised":
        raise ValueError("Confirmatory user authorisation is not active")
    if authorisation.get("packet_sha256") != artifacts["packet"]["sha256"]:
        raise ValueError("User authorisation does not bind the grant packet")
    if (
        authorisation.get("execution_seal_sha256")
        != artifacts["seal"]["sha256"]
    ):
        raise ValueError("User authorisation does not bind the grant seal")
    if authorisation.get("approved_scope") != packet.get(
        "approval_scope_digest"
    ):
        raise ValueError("User authorisation scope differs from the packet")
    return grant


def choose_clusters(
    input_dir: Path,
    split: str,
    clusters_per_field: int | None,
) -> set[str] | None:
    if clusters_per_field is None:
        return None
    if clusters_per_field < 1:
        raise ValueError("--clusters-per-field must be positive")
    split_manifest = json.loads((input_dir / "split.json").read_text(encoding="utf-8"))
    selected: set[str] = set()
    by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in split_manifest["clusters"]:
        if row["split"] == split:
            by_field[row["field"]].append(row)
    for field in FIELD_ORDER:
        ordered = sorted(
            by_field[field],
            key=lambda row: (row["split_digest"], row["cluster_id"]),
        )
        if len(ordered) < clusters_per_field:
            raise ValueError(
                f"{field}: requested {clusters_per_field} {split} clusters, "
                f"only {len(ordered)} exist"
            )
        selected.update(
            row["cluster_id"] for row in ordered[:clusters_per_field]
        )
    return selected


def load_prompts(
    input_dir: Path,
    split: str,
    clusters_per_field: int | None,
) -> list[dict[str, Any]]:
    if split not in {"development", "confirmatory"}:
        raise ValueError(f"Unsupported split: {split}")
    selected_clusters = choose_clusters(input_dir, split, clusters_per_field)
    rows = [
        row
        for row in read_jsonl(input_dir / "prompts.jsonl")
        if row["split"] == split
        and (selected_clusters is None or row["cluster_id"] in selected_clusters)
    ]
    if not rows:
        raise ValueError(f"No prompt rows selected for split {split}")
    prompt_ids = [row["prompt_id"] for row in rows]
    if len(prompt_ids) != len(set(prompt_ids)):
        raise ValueError("Duplicate prompt IDs in selected RQ2a rows")
    for row in rows:
        if row.get("protocol_version") != PROTOCOL_VERSION:
            raise ValueError(f"{row['prompt_id']}: protocol version mismatch")
        if len(row.get("candidate_skill_ids", [])) != 3:
            raise ValueError(f"{row['prompt_id']}: expected three candidates")
        if row["gold_skill_id"] not in row["candidate_skill_ids"]:
            raise ValueError(f"{row['prompt_id']}: gold is not a candidate")
    return sorted(rows, key=lambda row: row["prompt_id"])


def load_representation(
    input_dir: Path,
    representation: str,
    split: str,
    selected_cluster_ids: set[str],
) -> dict[tuple[str, str], dict[str, Any]]:
    path = input_dir / "representations" / f"{representation}.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"Representation does not exist: {path}")
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for row in read_jsonl(path):
        if row["split"] != split or row["cluster_id"] not in selected_cluster_ids:
            continue
        if row.get("protocol_version") != PROTOCOL_VERSION:
            raise ValueError(f"{path}: protocol version mismatch")
        if row.get("serialiser_version") != SERIALISER_VERSION:
            raise ValueError(f"{path}: serialiser version mismatch")
        if row.get("representation") != representation:
            raise ValueError(f"{path}: representation label mismatch")
        key = (row["cluster_id"], row["skill_id"])
        if key in index:
            raise ValueError(f"{path}: duplicate candidate identity {key}")
        if sha256_text(row["selector_visible_text"]) != row[
            "selector_visible_text_sha256"
        ]:
            raise ValueError(f"{path}: selector-visible text hash mismatch for {key}")
        index[key] = row
    expected = len(selected_cluster_ids) * 3
    if len(index) != expected:
        raise ValueError(
            f"{path}: selected row count {len(index)} != expected {expected}"
        )
    return index


def load_run_data(
    input_dir: Path,
    split: str,
    representations: list[str],
    clusters_per_field: int | None,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, dict[tuple[str, str], dict[str, Any]]],
]:
    protocol = load_protocol(input_dir)
    available = set(protocol["representations"])
    unknown = sorted(set(representations) - available)
    if unknown:
        raise ValueError(f"Unknown RQ2a representations: {unknown}")
    prompts = load_prompts(input_dir, split, clusters_per_field)
    selected_cluster_ids = {row["cluster_id"] for row in prompts}
    representation_indexes = {
        representation: load_representation(
            input_dir,
            representation,
            split,
            selected_cluster_ids,
        )
        for representation in representations
    }
    for prompt in prompts:
        for representation, index in representation_indexes.items():
            candidate_rows = [
                index.get((prompt["cluster_id"], skill_id))
                for skill_id in prompt["candidate_skill_ids"]
            ]
            if any(row is None for row in candidate_rows):
                raise ValueError(
                    f"{prompt['prompt_id']} / {representation}: candidate alignment failure"
                )
            source_hashes = {row["source_unit_sha256"] for row in candidate_rows}
            if source_hashes != {prompt["source_unit_sha256"]}:
                raise ValueError(
                    f"{prompt['prompt_id']} / {representation}: source hash mismatch"
                )
    return protocol, prompts, representation_indexes


def representation_documents(
    prompt: dict[str, Any],
    index: dict[tuple[str, str], dict[str, Any]],
) -> tuple[list[str], list[dict[str, Any]]]:
    rows = [
        index[(prompt["cluster_id"], skill_id)]
        for skill_id in prompt["candidate_skill_ids"]
    ]
    return [row["selector_visible_text"] for row in rows], rows


def build_result_row(
    *,
    run_id: str,
    selector: str,
    selector_config: dict[str, Any],
    representation: str,
    prompt: dict[str, Any],
    candidate_rows: list[dict[str, Any]],
    scores: list[float],
    score_latency_seconds: float,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metrics = tie_aware_metrics(
        prompt["candidate_skill_ids"],
        scores,
        prompt["gold_skill_id"],
    )
    row: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "run_id": run_id,
        "split": prompt["split"],
        "selector": selector,
        "selector_config_sha256": sha256_json(selector_config),
        "representation": representation,
        "prompt_id": prompt["prompt_id"],
        "cluster_id": prompt["cluster_id"],
        "field": prompt["field"],
        "prompt_variant": prompt["prompt_variant"],
        "query_text": prompt["query_text"],
        "query_text_sha256": sha256_text(prompt["query_text"]),
        "gold_skill_id": prompt["gold_skill_id"],
        "candidate_skill_ids": list(prompt["candidate_skill_ids"]),
        "candidate_text_sha256": [
            candidate["selector_visible_text_sha256"] for candidate in candidate_rows
        ],
        "candidate_audit_token_counts": [
            candidate["audit_token_count"] for candidate in candidate_rows
        ],
        "scores": [float(score) for score in scores],
        "score_latency_seconds": score_latency_seconds,
        **metrics,
    }
    if extra:
        row.update(extra)
    return row


def mean(values: Iterable[float]) -> float:
    materialised = list(values)
    return statistics.mean(materialised) if materialised else 0.0


def summarise_result_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"row_count": 0, "conditions": []}
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["selector"], row["representation"])].append(row)

    conditions: list[dict[str, Any]] = []
    for (selector, representation), group in sorted(grouped.items()):
        cluster_values: dict[str, list[dict[str, Any]]] = defaultdict(list)
        field_values: dict[str, list[dict[str, Any]]] = defaultdict(list)
        variant_values: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in group:
            cluster_values[row["cluster_id"]].append(row)
            field_values[row["field"]].append(row)
            variant_values[row["prompt_variant"]].append(row)
        cluster_top1 = [
            mean(item["top1_tie_adjusted"] for item in cluster_rows)
            for cluster_rows in cluster_values.values()
        ]
        conditions.append(
            {
                "selector": selector,
                "representation": representation,
                "prompt_count": len(group),
                "cluster_count": len(cluster_values),
                "top1_tie_adjusted_prompt_weighted": mean(
                    row["top1_tie_adjusted"] for row in group
                ),
                "top1_tie_adjusted_cluster_weighted": mean(cluster_top1),
                "mrr_tie_adjusted_prompt_weighted": mean(
                    row["mrr_tie_adjusted"] for row in group
                ),
                "gold_margin_mean": mean(row["gold_margin"] for row in group),
                "near_neighbour_strict_confusion_rate": mean(
                    row["near_neighbour_strict_confusion"] for row in group
                ),
                "top_tie_rate": mean(row["any_top_tie"] for row in group),
                "mean_top_tie_size": mean(row["top_tie_size"] for row in group),
                "score_latency_seconds_total": sum(
                    row["score_latency_seconds"] for row in group
                ),
                "by_field": [
                    {
                        "field": field,
                        "n": len(field_rows),
                        "top1_tie_adjusted": mean(
                            row["top1_tie_adjusted"] for row in field_rows
                        ),
                        "mrr_tie_adjusted": mean(
                            row["mrr_tie_adjusted"] for row in field_rows
                        ),
                        "gold_margin_mean": mean(
                            row["gold_margin"] for row in field_rows
                        ),
                    }
                    for field in FIELD_ORDER
                    for field_rows in [field_values.get(field, [])]
                    if field_rows
                ],
                "by_prompt_variant": [
                    {
                        "prompt_variant": variant,
                        "n": len(variant_rows),
                        "top1_tie_adjusted": mean(
                            row["top1_tie_adjusted"] for row in variant_rows
                        ),
                        "mrr_tie_adjusted": mean(
                            row["mrr_tie_adjusted"] for row in variant_rows
                        ),
                    }
                    for variant, variant_rows in sorted(variant_values.items())
                ],
            }
        )
    return {
        "row_count": len(rows),
        "prompt_count": len({row["prompt_id"] for row in rows}),
        "cluster_count": len({row["cluster_id"] for row in rows}),
        "conditions": conditions,
    }


def render_summary_markdown(
    summary: dict[str, Any],
    manifest: dict[str, Any],
) -> str:
    lines = [
        "# RQ2a Fixed-Candidate Selector Run",
        "",
        f"- Run ID: `{manifest['run_id']}`",
        f"- Split: `{manifest['split']}`",
        f"- Protocol: `{manifest['protocol_version']}`",
        f"- Serialiser: `{manifest['serialiser_version']}`",
        f"- Prompts: {summary.get('prompt_count', 0)}",
        f"- Clusters: {summary.get('cluster_count', 0)}",
        f"- Result rows: {summary.get('row_count', 0)}",
        "",
        "## Aggregate Results",
        "",
        "| Selector | Representation | n | Tie-adjusted Top-1 | Tie-adjusted MRR | Margin | Strict confusion | Top tie |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for condition in summary.get("conditions", []):
        lines.append(
            "| `{selector}` | `{representation}` | {n} | {top1:.3f} | "
            "{mrr:.3f} | {margin:.4f} | {confusion:.3f} | {ties:.3f} |".format(
                selector=condition["selector"],
                representation=condition["representation"],
                n=condition["prompt_count"],
                top1=condition["top1_tie_adjusted_cluster_weighted"],
                mrr=condition["mrr_tie_adjusted_prompt_weighted"],
                margin=condition["gold_margin_mean"],
                confusion=condition["near_neighbour_strict_confusion_rate"],
                ties=condition["top_tie_rate"],
            )
        )
    lines.extend(
        [
            "",
            "Primary accuracy is tie-adjusted and cluster-weighted. MRR and other "
            "diagnostics are prompt-weighted here; the final analysis script will "
            "use paired cluster resampling.",
            "",
            "## Runtime",
            "",
            "```json",
            json.dumps(manifest.get("runtime", {}), indent=2, sort_keys=True),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def self_test() -> None:
    identical = tie_aware_metrics(
        ["a", "b", "c"],
        [0.0, 0.0, 0.0],
        "a",
    )
    assert abs(identical["top1_tie_adjusted"] - 1 / 3) < 1e-12
    assert abs(identical["mrr_tie_adjusted"] - (1 + 1 / 2 + 1 / 3) / 3) < 1e-12
    assert identical["top_tie_size"] == 3

    clear = tie_aware_metrics(["a", "b", "c"], [2.0, 1.0, 0.0], "a")
    assert clear["top1_tie_adjusted"] == 1.0
    assert clear["mrr_tie_adjusted"] == 1.0
    assert clear["gold_margin"] == 1.0

    confused = tie_aware_metrics(["a", "b", "c"], [0.0, 2.0, 1.0], "a")
    assert confused["top1_tie_adjusted"] == 0.0
    assert confused["near_neighbour_strict_confusion"] == 1.0

    lexical = bm25_scores("scanned pdf", ["scanned pdf", "typed pdf", "audio"])
    assert lexical[0] > lexical[1] > lexical[2]
