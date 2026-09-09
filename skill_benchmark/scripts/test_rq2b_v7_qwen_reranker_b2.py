#!/usr/bin/env python3
"""Focused no-provider tests for the V7 qwen3-rerank B2 runner."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skill_benchmark/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
RUNNER_PATH = SCRIPTS / "run_rq2b_v7_qwen_reranker_b2.py"
VALIDATOR_PATH = SCRIPTS / "validate_rq2b_v7_runner_outputs.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = load_module("rq2b_v7_qwen_reranker_b2", RUNNER_PATH)
validator = load_module("rq2b_v7_runner_validator_for_qwen_b2_test", VALIDATOR_PATH)


def zero_b1_cost() -> dict[str, int | float]:
    return {
        "wall_time_ms": 0.0,
        "provider_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "window_forwards": 0,
        "cache_hits": 0,
        "retry_count": 0,
        "timeout_count": 0,
        "failure_count": 0,
    }


class FakeResponse:
    def __init__(self, value: dict[str, object]) -> None:
        self.raw = json.dumps(value).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def read(self) -> bytes:
        return self.raw


class QwenRerankerB2Tests(unittest.TestCase):
    def test_phase8_b1_wrapper_receipt_status_is_accepted_but_raw_status_is_not(self) -> None:
        receipt = {
            "schema_version": runner.B1_VALIDATION_RECEIPT_SCHEMA,
            "status": "PASS_FRESH_OFFICIAL_LABEL_FREE_B1_VALIDATION",
            "official_report": {"status": "PASS_LABEL_FREE_RUNNER_OUTPUT_VALIDATION"},
        }
        runner.validate_b1_validation_receipt(receipt)
        receipt["status"] = "PASS_LABEL_FREE_RUNNER_OUTPUT_VALIDATION"
        with self.assertRaisesRegex(ValueError, "receipt status drift"):
            runner.validate_b1_validation_receipt(receipt)

    @classmethod
    def setUpClass(cls) -> None:
        cls.authority = validator.RunnerAuthority.load()

    def test_self_test_loads_no_provider_runtime(self) -> None:
        result = runner.self_test()
        self.assertEqual(result["status"], "PASS_SYNTHETIC_NO_PROVIDER_NO_NETWORK")
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["provider_calls"], 0)
        self.assertNotIn("transformers", sys.modules)

    def test_frozen_method_and_materialised_scope(self) -> None:
        method = runner.method_contract()
        self.assertEqual(method["endpoint"], runner.ENDPOINT)
        self.assertEqual(method["model"], "qwen3-rerank")
        self.assertEqual(method["document_window_proxy_tokens"], 3500)
        self.assertEqual(method["document_window_overlap_proxy_tokens"], 256)
        self.assertEqual(method["timeout_seconds"], 120)
        self.assertEqual(method["automatic_retries"], 0)
        self.assertEqual(method["stable_tie_break"], "source_sha256_ascending")
        self.assertEqual(len(runner.MATERIALISED_CONDITIONS), 15)
        self.assertNotIn("C2-Q", runner.MATERIALISED_CONDITIONS)
        self.assertEqual(runner.EXPECTED_B2_ROWS, 15 * 1077)

    def test_exact_source_binding_regression(self) -> None:
        work = runner.synthetic_work()
        runner.validate_condition(work["condition"], work["trusted_binding"])
        self.assertEqual(
            [row["skill_id"] for row in work["condition"]["candidate_windows"]],
            work["condition"]["candidate_skill_ids"],
        )
        changed = {
            **work["condition"],
            "candidate_windows": [dict(row) for row in work["condition"]["candidate_windows"]],
        }
        changed["candidate_windows"][0]["text"] += "changed"
        changed["candidate_windows"][0]["text_sha256"] = runner.text_sha256(
            changed["candidate_windows"][0]["text"]
        )
        with self.assertRaisesRegex(ValueError, "binding drift"):
            runner.validate_condition(changed, work["trusted_binding"])

    def test_source_sha_is_only_exact_score_tie_break(self) -> None:
        work = runner.synthetic_work()
        windows = work["condition"]["candidate_windows"]
        scores = {
            (row["skill_id"], row["window_index"], row["text_sha256"]): 2.0
            for row in windows
        }
        ranked, ties = runner.rank_candidate_scores(
            list(reversed(work["condition"]["candidate_skill_ids"])),
            windows,
            scores,
        )
        self.assertEqual(
            [row["source_sha256"] for row in ranked],
            sorted(work["condition"]["candidate_skill_ids"]),
        )
        self.assertEqual(len(ties), 1)

    def test_provider_response_requires_exact_unique_finite_coverage(self) -> None:
        valid = {
            "output": {
                "results": [
                    {"index": 1, "relevance_score": -0.5},
                    {"index": 0, "relevance_score": 1.25},
                ]
            }
        }
        self.assertEqual(runner.parse_response_scores(valid, 2), [1.25, -0.5])
        with self.assertRaises(ValueError):
            runner.parse_response_scores(
                {"output": {"results": [{"index": 0, "relevance_score": 1.0}]}},
                2,
            )
        with self.assertRaises(ValueError):
            runner.parse_response_scores(
                {"output": {"results": [
                    {"index": 0, "relevance_score": 1.0},
                    {"index": 0, "relevance_score": 0.0},
                ]}},
                2,
            )

    def test_request_contract_is_exact_and_timeout_is_forwarded_without_network(self) -> None:
        work = runner.synthetic_work()
        payload = work["batches"][0]["payload"]
        captured: dict[str, object] = {}

        def fake_urlopen(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse({
                "output": {
                    "results": [
                        {"index": index, "relevance_score": float(-index)}
                        for index in range(len(payload["input"]["documents"]))
                    ]
                },
                "usage": {"total_tokens": 321},
            })

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            response = runner.request_once(payload, "not-a-real-key", 120)
        request = captured["request"]
        self.assertEqual(captured["timeout"], 120)
        self.assertEqual(request.full_url, runner.ENDPOINT)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer not-a-real-key")
        self.assertEqual(json.loads(request.data.decode("utf-8")), payload)
        self.assertEqual(runner.parse_provider_usage(response)["total_tokens"], 321)

    def test_failed_attempt_is_receipted_once_and_never_retried(self) -> None:
        work = runner.synthetic_work()
        ledger = runner.empty_ledger()
        calls = 0

        def fail_once(payload, api_key, timeout):
            nonlocal calls
            calls += 1
            raise runner.ProviderRequestError("synthetic timeout", timed_out=True)

        ceilings = {
            "maximum_request_attempts": 2,
            "maximum_successful_calls": 2,
            "maximum_external_documents": 100,
            "maximum_external_submission_proxy_tokens": 1_000_000,
            "maximum_external_submission_utf8_bytes": 1_000_000,
            "maximum_provider_total_tokens": 1_000_000,
            "maximum_wall_time_seconds": 60,
        }
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            attempt = root / "attempt"
            attempt.mkdir()
            with self.assertRaisesRegex(runner.ProviderRequestError, "synthetic timeout"):
                runner.score_work(
                    work,
                    request_fn=fail_once,
                    api_key="not-a-real-key",
                    timeout_seconds=120,
                    ceilings=ceilings,
                    ledger=ledger,
                    attempt_dir=attempt,
                    request_index=[],
                    started_at=runner.time.monotonic(),
                    root=root,
                )
            self.assertEqual(calls, 1)
            self.assertEqual(ledger["request_attempts"], 1)
            self.assertEqual(ledger["successful_calls"], 0)
            self.assertEqual(ledger["failures"], 1)
            self.assertEqual(ledger["timeouts"], 1)
            self.assertTrue((attempt / "request-000001-started.json").is_file())
            self.assertTrue((attempt / "request-000001-failed.json").is_file())

    def test_generated_row_passes_official_b2_validator(self) -> None:
        prompt_id, prompt = next(iter(self.authority.prompts.items()))
        sources = sorted(self.authority.sources)[:100]
        b1_authority = self.authority.b1_conditions["B01-G0"]
        b1 = {
            "schema_version": runner.B1_SCHEMA,
            "status": "SUCCESS",
            "run_id": "synthetic-no-provider",
            "condition_id": "B01-G0",
            "first_stage_cell_id": "B01",
            "prompt_id": prompt_id,
            "prompt_sha256": prompt["prompt_sha256"],
            "representation": b1_authority["representation"],
            "retriever": b1_authority["retriever"],
            "persisted_candidate_source": b1_authority["persisted_candidate_source"],
            "source_union_sha256": b1_authority["source_union_sha256"],
            "top_k": 100,
            "score_semantics": "HIGHER_IS_BETTER",
            "top20_binding_sha256": runner.top20_binding_sha256(
                condition_id="B01-G0",
                prompt_id=prompt_id,
                prompt_sha256=prompt["prompt_sha256"],
                ordered_source_sha256=sources[:20],
            ),
            "ranked_candidates": [
                {"rank": rank, "source_sha256": source, "score": float(101 - rank)}
                for rank, source in enumerate(sources, 1)
            ],
            "cost": zero_b1_cost(),
        }
        validator.validate_b1_row(b1, self.authority, 1)
        condition = self.authority.b2_conditions["B01-GQ"]
        views = {
            source: {
                "selector_text": f"Synthetic source representation {source}",
                "selector_text_sha256": runner.text_sha256(f"Synthetic source representation {source}"),
            }
            for source in sources[:20]
        }
        work = runner.build_condition_work(
            runner.CharacterTokenizer(), condition, prompt, b1, views
        )
        windows = work["condition"]["candidate_windows"]
        scores = {
            (window["skill_id"], window["window_index"], window["text_sha256"]): float(index)
            for index, window in enumerate(windows)
        }
        ranked, _ = runner.rank_candidate_scores(sources[:20], windows, scores)
        delta = {key: 0 for key in runner.empty_ledger()}
        delta["successful_calls"] = 1
        delta["external_submission_proxy_tokens"] = 1000
        delta["external_documents"] = 20
        row = runner.make_b2_row(
            run_id="synthetic-no-provider",
            condition_authority=condition,
            prompt=prompt,
            work=work,
            ranked=ranked,
            delta=delta,
            wall_time_ms=1.0,
        )
        validator.validate_b2_row(row, self.authority, {("B01-G0", prompt_id): b1}, 1)

    def test_missing_root_release_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(ValueError, "authorisation is missing"):
                runner.validate_root_release(root, root / "absent.json")

    def _preflight_fixture(self, *, payload_sha: str = "a" * 64):
        counts = runner.empty_workload_counts()
        counts.update({
            "rows": runner.EXPECTED_B2_ROWS,
            "requests": runner.EXPECTED_B2_ROWS,
            "documents": runner.EXPECTED_B2_ROWS * 20,
            "proxy_tokens": runner.EXPECTED_B2_ROWS * 2000,
            "utf8_bytes": runner.EXPECTED_B2_ROWS * 4000,
            "candidate_windows": runner.EXPECTED_B2_ROWS * 20,
            "maximum_documents_in_one_request": 20,
            "maximum_proxy_tokens_in_one_request": 2000,
            "maximum_utf8_bytes_in_one_request": 4000,
        })
        ceilings = {
            "maximum_request_attempts": counts["requests"],
            "maximum_successful_calls": counts["requests"],
            "maximum_external_documents": counts["documents"],
            "maximum_external_submission_proxy_tokens": counts["proxy_tokens"],
            "maximum_external_submission_utf8_bytes": counts["utf8_bytes"],
            "maximum_provider_total_tokens": 999_999_999,
            "maximum_wall_time_seconds": 999_999,
        }
        receipt = {
            "schema_version": runner.PREFLIGHT_SCHEMA,
            "status": "PASS_EXACT_NO_PROVIDER_PREFLIGHT",
            "runner_version": runner.RUNNER_VERSION,
            "payload_sha256": payload_sha,
            "pending_release_sha256": "b" * 64,
            "implementation": {
                "runner_sha256": runner.file_sha256(RUNNER_PATH),
                "qwen_contract_helper_sha256": runner.file_sha256(ROOT / runner.HELPER_REL),
                "exact_chunker_v1_sha256": runner.file_sha256(ROOT / runner.CHUNKER_V1_REL),
                "exact_chunker_v2_sha256": runner.file_sha256(ROOT / runner.CHUNKER_V2_REL),
                "official_output_validator_sha256": runner.file_sha256(ROOT / runner.VALIDATOR_REL),
            },
            "proxy_tokenizer": runner.PROXY_TOKENIZER,
            "method_sha256": runner.canonical_sha256(runner.method_contract()),
            "scope": {
                "conditions": list(runner.MATERIALISED_CONDITIONS),
                "condition_count": 15,
                "queries": runner.EXPECTED_QUERIES,
                "rows": runner.EXPECTED_B2_ROWS,
                "candidate_pairs_per_row": runner.TOP_K,
                "c2_q_alias_rows": 0,
            },
            "counts": counts,
            "chunker_parity": {
                "status": "PASS_EXACT_V1_V2_PARITY",
                "v1": {
                    "version": runner.CHUNKER_V1_VERSION,
                    "path": runner.CHUNKER_V1_REL.as_posix(),
                    "sha256": runner.file_sha256(ROOT / runner.CHUNKER_V1_REL),
                    "counts_sha256": runner.canonical_sha256(counts),
                },
                "v2": {
                    "version": runner.CHUNKER_V2_VERSION,
                    "path": runner.CHUNKER_V2_REL.as_posix(),
                    "sha256": runner.file_sha256(ROOT / runner.CHUNKER_V2_REL),
                    "counts_sha256": runner.canonical_sha256(counts),
                },
                "compared_rows": runner.EXPECTED_B2_ROWS,
                "different_rows": 0,
                "same_window_boundaries": True,
                "same_request_partitioning": True,
                "differences_sha256": runner.canonical_sha256([]),
                "difference_samples": [],
                "decision": "V1_FROZEN_METHOD_SAFE_TO_EXECUTE",
            },
            "ceilings": ceilings,
            "ceiling_headroom": runner.ceiling_headroom(counts, ceilings, preflight_seconds=1.0),
            "all_pre_execution_predictable_ceilings_sufficient": True,
            "provider_calls": 0,
            "network_calls": 0,
            "preflight_wall_time_seconds": 1.0,
            "completed_at_utc": "2026-09-09T00:00:00Z",
        }
        return receipt, ceilings

    def test_stale_preflight_receipt_is_rejected(self) -> None:
        receipt, ceilings = self._preflight_fixture()
        with self.assertRaisesRegex(ValueError, "payload binding is stale"):
            runner.validate_preflight_receipt(
                receipt,
                payload_sha256="c" * 64,
                pending_release_sha256="b" * 64,
                ceilings=ceilings,
                root=ROOT,
            )

    def test_insufficient_preflight_ceiling_is_rejected(self) -> None:
        receipt, ceilings = self._preflight_fixture()
        receipt["ceiling_headroom"]["maximum_request_attempts"]["headroom"] = -1
        receipt["ceiling_headroom"]["maximum_request_attempts"]["sufficient"] = False
        receipt["all_pre_execution_predictable_ceilings_sufficient"] = False
        with self.assertRaisesRegex(ValueError, "predictable ceilings are insufficient"):
            runner.validate_preflight_receipt(
                receipt,
                payload_sha256="a" * 64,
                pending_release_sha256="b" * 64,
                ceilings=ceilings,
                root=ROOT,
            )

    def test_chunker_boundary_or_request_difference_blocks_execution(self) -> None:
        receipt, ceilings = self._preflight_fixture()
        receipt["chunker_parity"]["status"] = "FAIL_METHOD_DOCKET_REQUIRED"
        receipt["chunker_parity"]["different_rows"] = 1
        receipt["chunker_parity"]["same_window_boundaries"] = False
        receipt["chunker_parity"]["decision"] = (
            "FAIL_CLOSED_DO_NOT_EXECUTE_OPEN_METHOD_DOCKET_NO_AUTOMATIC_CHUNKER_SWAP"
        )
        with self.assertRaisesRegex(ValueError, "chunker parity is not PASS"):
            runner.validate_preflight_receipt(
                receipt,
                payload_sha256="a" * 64,
                pending_release_sha256="b" * 64,
                ceilings=ceilings,
                root=ROOT,
            )

    def test_full_scope_preflight_never_calls_provider(self) -> None:
        work = runner.synthetic_work()
        counts = runner.empty_workload_counts()
        for _ in range(runner.EXPECTED_B2_ROWS):
            runner.add_workload_counts(counts, work)
        ceilings = {
            "maximum_request_attempts": counts["requests"],
            "maximum_successful_calls": counts["requests"],
            "maximum_external_documents": counts["documents"],
            "maximum_external_submission_proxy_tokens": counts["proxy_tokens"],
            "maximum_external_submission_utf8_bytes": counts["utf8_bytes"],
            "maximum_provider_total_tokens": 999_999_999,
            "maximum_wall_time_seconds": 999_999,
        }
        pending = {
            "ceilings": ceilings,
        }
        prompts = [{"prompt_id": f"p-{index}"} for index in range(runner.EXPECTED_QUERIES)]
        conditions = {
            condition_id: {
                "condition_id": condition_id,
                "representation": "I1-discovery",
                "persisted_candidate_source": condition_id[:3] if condition_id.startswith("B") else "B05",
            }
            for condition_id in runner.MATERIALISED_CONDITIONS
        }
        b1 = {
            (f"B{index:02d}-G0", prompt["prompt_id"]): {}
            for index in range(1, 13)
            for prompt in prompts
        }
        with tempfile.TemporaryDirectory(dir=ROOT / "skill_benchmark/cache") as raw:
            temp = Path(raw)
            payload_path = temp / "payload.json"
            pending_path = temp / "pending.json"
            payload_path.write_text("{}\n", encoding="utf-8")
            pending_path.write_text("{}\n", encoding="utf-8")
            receipt_path = temp / "receipt.json"
            with (
                mock.patch.object(
                    runner,
                    "validate_pending_release",
                    return_value=(pending, payload_path, {}),
                ),
                mock.patch.object(
                    runner,
                    "load_authority",
                    return_value=(prompts, conditions, {"I1-discovery": {}}, b1, object()),
                ),
                mock.patch.object(runner, "load_proxy_tokenizer", return_value=runner.CharacterTokenizer()),
                mock.patch.object(runner, "build_condition_work", return_value=work),
                mock.patch.object(runner, "request_once", side_effect=AssertionError("provider called")) as provider,
            ):
                receipt = runner.run_preflight(ROOT, pending_path, receipt_path)
            self.assertEqual(receipt["counts"]["rows"], runner.EXPECTED_B2_ROWS)
            self.assertEqual(receipt["provider_calls"], 0)
            self.assertEqual(receipt["network_calls"], 0)
            provider.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
