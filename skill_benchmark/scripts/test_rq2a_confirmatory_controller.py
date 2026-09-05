#!/usr/bin/env python3
"""Offline unit tests for the sealed RQ2a confirmatory controller."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import run_rq2a_confirmatory_sequence as controller
import run_rq2a_fixed_candidate_matrix as fixed_runner
from build_rq2a_cost_ledger import guarded_attempt_history
from rq2a_selector_common import (
    audit_token_count,
    sha256_file,
    sha256_json,
    sha256_text,
)
from rq2a_selector_common import validate_confirmatory_execution_grant
from run_rq2a_fixed_candidate_matrix import RQ2aEmbeddingClient


def fake_packet() -> dict[str, Any]:
    return {
        "external_service_scope": {
            "outbound_request_attempt_ceiling": 2,
            "successful_api_call_ceiling": 2,
            "local_audit_token_ceiling": 100,
            "provider_total_token_ceiling": 200,
        }
    }


def fake_preflight(texts: list[str]) -> dict[str, Any]:
    hashes = sorted(sha256_text(text) for text in texts)
    category = {"missing_text_sha256": hashes}
    return {
        "categories": {
            "single_vector_documents": category,
            "combined_unique_payload": category,
        }
    }


def test_guard_accepts_allowlisted_batch(root: Path) -> None:
    texts = ["approved alpha", "approved beta"]
    calls = 0

    def transport(
        url: str,
        api_key: str,
        payload: dict[str, Any],
        timeout: int,
    ) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        assert url == f"{controller.QWEN_BASE_URL}/embeddings"
        assert api_key == "secret"
        assert timeout == 5
        return {
            "data": [
                {"index": index, "embedding": [float(index)] * 1024}
                for index, _ in enumerate(payload["input"])
            ],
            "usage": {"total_tokens": 12, "prompt_tokens": 12},
        }

    old_guard = controller.GUARD_DIR
    old_client = controller.exact_cache_client
    cache_root = root / "cache"
    controller.GUARD_DIR = root / "guard"

    def local_client() -> RQ2aEmbeddingClient:
        return RQ2aEmbeddingClient(
            provider="qwen",
            base_url=controller.QWEN_BASE_URL,
            api_key="unused",
            model=controller.QWEN_MODEL,
            dimensions=controller.QWEN_DIMENSIONS,
            cache_dir=cache_root,
            timeout_seconds=1,
            max_audit_tokens=8192,
            legacy_cache_dir=None,
        )

    controller.exact_cache_client = local_client
    try:
        guard = controller.GuardedDashScopeTransport(
            category="single_vector_documents",
            preflight=fake_preflight(texts),
            packet=fake_packet(),
            allow_new_requests=True,
            transport=transport,
        )
        response = guard.post_json(
            f"{controller.QWEN_BASE_URL}/embeddings",
            "secret",
            {
                "model": controller.QWEN_MODEL,
                "dimensions": controller.QWEN_DIMENSIONS,
                "input": texts,
            },
            5,
        )
        assert calls == 1
        assert response["usage"]["total_tokens"] == 12
        attempts = guard.attempts()
        assert len(attempts) == 1
        assert attempts[0]["state"] == "complete"
        for text in texts:
            assert local_client().cache_path(text).is_file()
        try:
            guard.post_json(
                f"{controller.QWEN_BASE_URL}/embeddings",
                "secret",
                {
                    "model": controller.QWEN_MODEL,
                    "dimensions": controller.QWEN_DIMENSIONS,
                    "input": [texts[0]],
                },
                5,
            )
        except ValueError as exc:
            assert "already-sent" in str(exc)
        else:
            raise AssertionError("Guard permitted duplicate paid text")
        assert calls == 1
    finally:
        controller.GUARD_DIR = old_guard
        controller.exact_cache_client = old_client


def test_guard_provenance_survives_embedding_client(root: Path) -> None:
    text = "guarded persisted text"
    cache_root = root / "guard-preserved-cache"
    old_guard = controller.GUARD_DIR
    old_client_factory = controller.exact_cache_client
    old_post = fixed_runner.post_json
    controller.GUARD_DIR = root / "guard-preserved"

    def local_client() -> RQ2aEmbeddingClient:
        return RQ2aEmbeddingClient(
            provider="qwen",
            base_url=controller.QWEN_BASE_URL,
            api_key="secret",
            model=controller.QWEN_MODEL,
            dimensions=controller.QWEN_DIMENSIONS,
            cache_dir=cache_root,
            timeout_seconds=1,
            max_audit_tokens=8192,
            legacy_cache_dir=None,
        )

    def transport(*args: Any) -> dict[str, Any]:
        return {
            "data": [{"index": 0, "embedding": [0.25] * 1024}],
            "usage": {"prompt_tokens": 4, "total_tokens": 4},
        }

    controller.exact_cache_client = local_client
    try:
        guard = controller.GuardedDashScopeTransport(
            category="single_vector_documents",
            preflight=fake_preflight([text]),
            packet=fake_packet(),
            allow_new_requests=True,
            transport=transport,
        )
        fixed_runner.post_json = guard.post_json
        client = local_client()
        vectors = client.embed_many(
            [text],
            batch_size=10,
            progress_label="guard-preservation-test",
        )
        assert vectors[text][0] == 0.25
        payload = json.loads(client.cache_path(text).read_text(encoding="utf-8"))
        assert payload["provenance"]["kind"] == "confirmatory_guard_response"
        attempt_path = Path(guard.attempts()[0]["_path"])
        assert payload["provenance"]["attempt_sha256"] == sha256_file(
            attempt_path
        )
    finally:
        fixed_runner.post_json = old_post
        controller.exact_cache_client = old_client_factory
        controller.GUARD_DIR = old_guard


def test_guard_rejects_drift(root: Path) -> None:
    text = "approved"
    old_guard = controller.GUARD_DIR
    controller.GUARD_DIR = root / "guard-drift"
    calls = 0

    def transport(*args: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {}

    try:
        guard = controller.GuardedDashScopeTransport(
            category="single_vector_documents",
            preflight=fake_preflight([text]),
            packet=fake_packet(),
            allow_new_requests=True,
            transport=transport,
        )
        bad_payloads = [
            (
                "https://example.invalid/embeddings",
                {
                    "model": controller.QWEN_MODEL,
                    "dimensions": controller.QWEN_DIMENSIONS,
                    "input": [text],
                },
            ),
            (
                f"{controller.QWEN_BASE_URL}/embeddings",
                {
                    "model": "wrong-model",
                    "dimensions": controller.QWEN_DIMENSIONS,
                    "input": [text],
                },
            ),
            (
                f"{controller.QWEN_BASE_URL}/embeddings",
                {
                    "model": controller.QWEN_MODEL,
                    "dimensions": controller.QWEN_DIMENSIONS,
                    "input": ["not approved"],
                },
            ),
        ]
        for url, payload in bad_payloads:
            try:
                guard.post_json(url, "secret", payload, 5)
            except ValueError:
                pass
            else:
                raise AssertionError("Guard accepted endpoint/model/text drift")
        assert calls == 0
    finally:
        controller.GUARD_DIR = old_guard


def test_warm_guard_never_calls(root: Path) -> None:
    text = "approved"
    old_guard = controller.GUARD_DIR
    controller.GUARD_DIR = root / "guard-warm"
    calls = 0

    def transport(*args: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {}

    try:
        guard = controller.GuardedDashScopeTransport(
            category="single_vector_documents",
            preflight=fake_preflight([text]),
            packet=fake_packet(),
            allow_new_requests=False,
            transport=transport,
        )
        try:
            guard.post_json(
                f"{controller.QWEN_BASE_URL}/embeddings",
                "secret",
                {
                    "model": controller.QWEN_MODEL,
                    "dimensions": controller.QWEN_DIMENSIONS,
                    "input": [text],
                },
                5,
            )
        except RuntimeError as exc:
            assert "Warm verification" in str(exc)
        else:
            raise AssertionError("Warm guard permitted an external request")
        assert calls == 0
    finally:
        controller.GUARD_DIR = old_guard


def test_exclusive_process_lock(root: Path) -> None:
    lock = root / "exclusive.lock"
    holder = subprocess.Popen(
        [
            sys.executable,
            "-c",
            (
                "import fcntl,sys,time; "
                "h=open(sys.argv[1],'a+'); "
                "fcntl.flock(h.fileno(),fcntl.LOCK_EX); "
                "print('locked',flush=True); time.sleep(5)"
            ),
            str(lock),
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert holder.stdout is not None
        assert holder.stdout.readline().strip() == "locked"
        try:
            with controller.exclusive_file_lock(lock):
                pass
        except RuntimeError as exc:
            assert "Another confirmatory process" in str(exc)
        else:
            raise AssertionError("Second process acquired the paid-run lock")
    finally:
        holder.terminate()
        holder.wait(timeout=5)


def test_stale_analysis_rejected(root: Path) -> None:
    old_root = controller.CONFIRMATORY_ROOT
    controller.CONFIRMATORY_ROOT = root / "confirmatory-runs"
    try:
        for run_id in controller.PRIMARY_RUN_IDS:
            directory = controller.CONFIRMATORY_ROOT / run_id
            directory.mkdir(parents=True)
            (directory / "manifest.json").write_text(
                json.dumps({"run_id": run_id}) + "\n", encoding="utf-8"
            )
            (directory / "rows.jsonl").write_text(
                json.dumps({"run_id": run_id}) + "\n", encoding="utf-8"
            )
        provenance = controller.current_run_provenance(
            controller.PRIMARY_RUN_IDS
        )
        report = root / "analysis.json"
        report.write_text(
            json.dumps(
                {
                    "split": "confirmatory",
                    "row_count": 13_200,
                    "quality_checks": {
                        "unique_condition_prompt_rows": "pass"
                    },
                    "runs": [
                        {"run_id": run_id, **hashes}
                        for run_id, hashes in provenance.items()
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        controller.validate_analysis_output("analysis", report)
        changed = (
            controller.CONFIRMATORY_ROOT
            / controller.PRIMARY_RUN_IDS[0]
            / "rows.jsonl"
        )
        changed.write_text('{"changed": true}\n', encoding="utf-8")
        try:
            controller.validate_analysis_output("analysis", report)
        except ValueError as exc:
            assert "stale" in str(exc)
        else:
            raise AssertionError("Stale analysis survived changed run hashes")
    finally:
        controller.CONFIRMATORY_ROOT = old_root


def test_current_cache_metadata_is_exact(root: Path) -> None:
    client = RQ2aEmbeddingClient(
        provider="qwen",
        base_url=controller.QWEN_BASE_URL,
        api_key="unused",
        model=controller.QWEN_MODEL,
        dimensions=controller.QWEN_DIMENSIONS,
        cache_dir=root / "cache-metadata",
        timeout_seconds=1,
        max_audit_tokens=8192,
        legacy_cache_dir=None,
    )
    text = "metadata-bound text"
    path = client.cache_path(text)
    path.write_text(
        json.dumps(
            {
                "schema_version": "rq2a-embedding-cache-v1",
                "provider": "wrong-provider",
                "base_url": controller.QWEN_BASE_URL,
                "model": controller.QWEN_MODEL,
                "dimensions": controller.QWEN_DIMENSIONS,
                "text_sha256": sha256_text(text),
                "audit_token_count": 3,
                "embedding": [0.0] * controller.QWEN_DIMENSIONS,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    try:
        client.embed_many(
            [text],
            batch_size=10,
            progress_label="metadata-test",
            allow_api=False,
        )
    except ValueError as exc:
        assert "metadata mismatch" in str(exc)
    else:
        raise AssertionError("Current cache accepted wrong provider metadata")


def test_frozen_current_cache_hash_rejects_vector_substitution(root: Path) -> None:
    text = "frozen cache text"
    client = RQ2aEmbeddingClient(
        provider="qwen",
        base_url=controller.QWEN_BASE_URL,
        api_key="unused",
        model=controller.QWEN_MODEL,
        dimensions=controller.QWEN_DIMENSIONS,
        cache_dir=root / "cache-frozen",
        timeout_seconds=1,
        max_audit_tokens=8192,
        legacy_cache_dir=None,
    )
    path = client.cache_path(text)
    payload = {
        "schema_version": "rq2a-embedding-cache-v1",
        "provider": "qwen",
        "base_url": controller.QWEN_BASE_URL,
        "model": controller.QWEN_MODEL,
        "dimensions": controller.QWEN_DIMENSIONS,
        "text_sha256": sha256_text(text),
        "audit_token_count": audit_token_count(text),
        "embedding": [0.0] * controller.QWEN_DIMENSIONS,
    }
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    category = {
        "unique_text_count": 1,
        "current_cache_hits": 1,
        "legacy_exact_hits": 0,
        "missing_text_sha256": [],
        "current_cache_entries": [
            {
                "text_sha256": sha256_text(text),
                "path": str(path),
                "file_sha256": sha256_file(path),
            }
        ],
        "legacy_cache_entries": [],
    }
    preflight = {
        "categories": {
            name: category
            for name in (
                "single_vector_documents",
                "queries",
                "field_components",
                "combined_unique_payload",
            )
        }
    }
    old_payload_texts = controller.payload_texts
    old_client = controller.exact_cache_client
    old_guard = controller.GUARD_DIR
    controller.payload_texts = lambda: {
        name: {text}
        for name in (
            "single_vector_documents",
            "queries",
            "field_components",
            "combined_unique_payload",
        )
    }
    controller.exact_cache_client = lambda: client
    controller.GUARD_DIR = root / "no-guard-attempts"
    try:
        controller.validate_current_payload_state(preflight)
        payload["embedding"][0] = 1.0
        path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        try:
            controller.validate_current_payload_state(preflight)
        except ValueError as exc:
            assert "frozen current cache hash drift" in str(exc)
        else:
            raise AssertionError("Frozen cache accepted substituted vector")
    finally:
        controller.payload_texts = old_payload_texts
        controller.exact_cache_client = old_client
        controller.GUARD_DIR = old_guard


def test_guarded_cost_history_is_authoritative(root: Path) -> None:
    attempts = root / "cost-attempts"
    attempts.mkdir()
    attempt = attempts / "0001-test.json"
    attempt.write_text(
        json.dumps(
            {
                "schema_version": "rq2a-guarded-dashscope-attempt-v1",
                "state": "complete",
                "category": "single_vector_documents",
                "url": f"{controller.QWEN_BASE_URL}/embeddings",
                "model": controller.QWEN_MODEL,
                "dimensions": controller.QWEN_DIMENSIONS,
                "text_sha256": [sha256_text("paid text")],
                "audit_token_counts": [2],
                "response": {
                    "data": [{"index": 0, "embedding": [0.0] * 1024}],
                    "usage": {"prompt_tokens": 3, "total_tokens": 3},
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    history = guarded_attempt_history(attempts)
    assert history["successful_api_calls"] == 1
    assert history["provider_usage"]["total_tokens"] == 3
    assert history["local_audit_tokens"] == 2
    assert history["files"][0]["sha256"] == sha256_file(attempt)


def test_independent_review_binding(root: Path) -> None:
    packet = root / "packet.json"
    seal = root / "seal.json"
    review = root / "review.json"
    packet_payload = {"approval_scope_digest": {"maximum_calls": 2}}
    packet.write_text(json.dumps(packet_payload) + "\n", encoding="utf-8")
    seal.write_text('{"sealed": true}\n', encoding="utf-8")
    review.write_text(
        json.dumps(
            {
                "schema_version": "rq2a-confirmatory-independent-review-pass-v1",
                "state": "pass",
                "verdict": "PASS",
                "reviewer_agent_id": "independent-agent",
                "packet_sha256": sha256_file(packet),
                "execution_seal_sha256": sha256_file(seal),
                "approval_scope_sha256": sha256_json(
                    packet_payload["approval_scope_digest"]
                ),
                "network_or_scoring_performed": False,
                "can_authorise_spending": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    controller.validate_independent_review(
        review, packet, seal, packet_payload
    )
    packet.write_text('{"changed": true}\n', encoding="utf-8")
    try:
        controller.validate_independent_review(
            review, packet, seal, {"approval_scope_digest": {}}
        )
    except ValueError as exc:
        assert "hash mismatch" in str(exc)
    else:
        raise AssertionError("Independent review survived packet drift")


def test_complete_grant_chain(root: Path) -> None:
    packet_path = root / "grant-packet.json"
    seal_path = root / "grant-seal.json"
    review_path = root / "grant-review.json"
    authorisation_path = root / "grant-authorisation.json"
    grant_path = root / "grant.json"
    scope = {"maximum_calls": 2}
    packet = {
        "schema_version": "rq2a-confirmatory-authorisation-packet-v1",
        "state": "awaiting_independent_review_and_user_authorisation",
        "approval_scope_digest": scope,
    }
    seal = {
        "schema_version": "rq2a-confirmatory-execution-seal-v1",
        "state": "sealed_before_user_authorisation",
    }
    packet_path.write_text(json.dumps(packet) + "\n", encoding="utf-8")
    seal_path.write_text(json.dumps(seal) + "\n", encoding="utf-8")
    review = {
        "schema_version": "rq2a-confirmatory-independent-review-pass-v1",
        "state": "pass",
        "verdict": "PASS",
        "reviewer_agent_id": "independent-agent",
        "packet_sha256": sha256_file(packet_path),
        "execution_seal_sha256": sha256_file(seal_path),
        "approval_scope_sha256": sha256_json(scope),
        "network_or_scoring_performed": False,
        "can_authorise_spending": False,
    }
    review_path.write_text(json.dumps(review) + "\n", encoding="utf-8")
    authorisation = {
        "schema_version": "rq2a-confirmatory-user-authorisation-v1",
        "state": "authorised",
        "packet_sha256": sha256_file(packet_path),
        "execution_seal_sha256": sha256_file(seal_path),
        "approved_scope": scope,
    }
    authorisation_path.write_text(
        json.dumps(authorisation) + "\n", encoding="utf-8"
    )
    invocation = {"exact": True}
    artifacts = {
        "packet": {"path": str(packet_path), "sha256": sha256_file(packet_path)},
        "seal": {"path": str(seal_path), "sha256": sha256_file(seal_path)},
        "independent_review": {
            "path": str(review_path),
            "sha256": sha256_file(review_path),
        },
        "user_authorisation": {
            "path": str(authorisation_path),
            "sha256": sha256_file(authorisation_path),
        },
    }
    grant = {
        "schema_version": "rq2a-confirmatory-controller-grant-v1",
        "state": "active_for_exact_invocation",
        "action": "fixed_scoring",
        "invocation_sha256": sha256_json(invocation),
        "authorisation_artifacts": artifacts,
    }
    grant_path.write_text(json.dumps(grant) + "\n", encoding="utf-8")
    validate_confirmatory_execution_grant(
        grant_path,
        action="fixed_scoring",
        invocation=invocation,
    )
    review["verdict"] = "FAIL"
    review_path.write_text(json.dumps(review) + "\n", encoding="utf-8")
    artifacts["independent_review"]["sha256"] = sha256_file(review_path)
    grant["authorisation_artifacts"] = artifacts
    grant_path.write_text(json.dumps(grant) + "\n", encoding="utf-8")
    try:
        validate_confirmatory_execution_grant(
            grant_path,
            action="fixed_scoring",
            invocation=invocation,
        )
    except ValueError as exc:
        assert "not a PASS" in str(exc)
    else:
        raise AssertionError("Grant accepted a failed independent review")


def test_orphan_run_has_no_grant_provenance() -> None:
    spec = controller.RUN_SPECS[0]
    args = SimpleNamespace(freeze=controller.DEFAULT_FREEZE)
    try:
        controller.validate_run_grant_provenance({}, spec, args)
    except ValueError as exc:
        assert "grant path mismatch" in str(exc)
    else:
        raise AssertionError("Orphan result manifest passed grant provenance")


def test_completed_run_summary_revalidation(root: Path) -> None:
    rows = [
        {
            "selector": "bm25",
            "representation": "shared-only",
            "prompt_id": "prompt-1",
            "cluster_id": "cluster-1",
            "field": "input_precondition",
            "prompt_variant": "direct",
            "top1_tie_adjusted": 1.0,
            "mrr_tie_adjusted": 1.0,
            "gold_margin": 0.5,
            "near_neighbour_strict_confusion": 0.0,
            "any_top_tie": 0.0,
            "top_tie_size": 1,
            "score_latency_seconds": 0.0,
        }
    ]
    summary_path = root / "completed-run-summary.json"
    summary_path.write_text(
        json.dumps(controller.summarise_result_rows(rows)) + "\n",
        encoding="utf-8",
    )
    controller.validate_run_summary_artifact(
        summary_path,
        rows,
        "synthetic-complete-run",
    )
    mutated = controller.summarise_result_rows(rows)
    mutated["row_count"] = 2
    summary_path.write_text(json.dumps(mutated) + "\n", encoding="utf-8")
    try:
        controller.validate_run_summary_artifact(
            summary_path,
            rows,
            "synthetic-complete-run",
        )
    except ValueError as exc:
        assert "summary does not match result rows" in str(exc)
    else:
        raise AssertionError("Completed-run validation accepted a mutated summary")


def test_successful_state_transition_clears_stale_failure_metadata() -> None:
    state = {
        "state": "failed",
        "failed_step": "confirmatory-bm25-all-v1",
        "failure": "old failure",
        "completed_steps": [],
    }
    removed = controller.clear_stale_failure_metadata(state)
    assert removed == {
        "failed_step": "confirmatory-bm25-all-v1",
        "failure": "old failure",
    }
    assert "failed_step" not in state
    assert "failure" not in state
    assert controller.clear_stale_failure_metadata(state) == {}


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="rq2a-confirmatory-controller-") as raw:
        root = Path(raw)
        test_guard_accepts_allowlisted_batch(root)
        test_guard_provenance_survives_embedding_client(root)
        test_guard_rejects_drift(root)
        test_warm_guard_never_calls(root)
        test_exclusive_process_lock(root)
        test_stale_analysis_rejected(root)
        test_current_cache_metadata_is_exact(root)
        test_frozen_current_cache_hash_rejects_vector_substitution(root)
        test_guarded_cost_history_is_authoritative(root)
        test_independent_review_binding(root)
        test_complete_grant_chain(root)
        test_orphan_run_has_no_grant_provenance()
        test_completed_run_summary_revalidation(root)
        test_successful_state_transition_clears_stale_failure_metadata()
        try:
            validate_confirmatory_execution_grant(
                None,
                action="fixed_scoring",
                invocation={},
            )
        except ValueError as exc:
            assert "exact controller grant" in str(exc)
        else:
            raise AssertionError("Confirmatory entry point accepted no grant")
    assert len(controller.EXPECTED_PRIMARY_CONDITIONS) == 22
    assert sum(
        spec.expected_rows for spec in controller.RUN_SPECS if spec.role == "primary"
    ) == 13_200
    assert set(controller.PRIMARY_RUN_IDS) == {
        "confirmatory-bm25-all-v1",
        "confirmatory-skillrouter-core-v1",
        "confirmatory-qwen-all-v1",
        "confirmatory-field-aware-v1",
    }
    print("RQ2a confirmatory controller tests: PASS")


if __name__ == "__main__":
    main()
