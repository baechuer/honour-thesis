#!/usr/bin/env python3
"""Focused no-inference tests for the V7 SkillRouter B2 runner."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "skill_benchmark/scripts/run_rq2b_v7_skillrouter_reranker_b2.py"
VALIDATOR_PATH = ROOT / "skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = load_module("rq2b_v7_skillrouter_reranker_b2", RUNNER_PATH)
validator = load_module("rq2b_v7_runner_output_validator_for_b2_test", VALIDATOR_PATH)


class CharacterTokenizer:
    """Deterministic offset-aware tokenizer used only by synthetic tests."""

    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        if add_special_tokens:
            raise AssertionError("B2 prompt construction must not add tokenizer specials")
        return [ord(character) + 1 for character in text]

    def __call__(
        self, text: str, *, add_special_tokens: bool,
        return_offsets_mapping: bool,
    ) -> dict[str, object]:
        if add_special_tokens or not return_offsets_mapping:
            raise AssertionError("Unexpected tokenizer mode")
        return {
            "input_ids": self.encode(text),
            "offset_mapping": [(index, index + 1) for index in range(len(text))],
        }


def zero_cost(*, b2: bool) -> dict[str, int | float]:
    value: dict[str, int | float] = {
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
    if b2:
        value["candidate_pairs"] = 20
    return value


class SkillRouterRerankerB2Tests(unittest.TestCase):
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

    def tearDown(self) -> None:
        self.assertNotIn("torch", sys.modules)
        self.assertNotIn("transformers", sys.modules)

    def test_self_test_is_no_inference(self) -> None:
        result = runner.self_test()
        self.assertEqual(
            result["status"],
            "PASS_SYNTHETIC_NO_MODEL_LOAD_NO_FORWARD_NO_NETWORK",
        )
        self.assertEqual(result["model_loads"], 0)
        self.assertEqual(result["model_forwards"], 0)
        self.assertEqual(result["network_calls"], 0)

    def test_released_prompt_and_lossless_windows(self) -> None:
        tokenizer = CharacterTokenizer()
        query = "route this task"
        document = "alpha\n\nbeta-gamma\n\ndelta"
        ids = runner.build_pair_ids(tokenizer, query, document)
        expected = runner.PREFIX + runner.BODY_FORMAT.format(
            instruction=runner.INSTRUCTION, query=query, document=document
        ) + runner.SUFFIX
        self.assertEqual(ids, tokenizer.encode(expected))
        windows = runner.lossless_markdown_windows(
            tokenizer, document, maximum_content_tokens=10, overlap_tokens=3
        )
        self.assertGreater(len(windows), 1)
        self.assertTrue(all(row["content_token_count"] <= 10 for row in windows))
        reconstructed = ""
        end = 0
        for window in windows:
            reconstructed += document[max(end, window["source_start_char"]):window["source_end_char"]]
            end = max(end, window["source_end_char"])
        self.assertEqual(reconstructed, document)

    def test_exact_length_batches_never_pad_and_cap_at_16(self) -> None:
        pairs = [
            {"pair_id": f"pair-{index:02d}", "pair_input_tokens": 9 if index < 17 else 11}
            for index in range(35)
        ]
        batches = runner.exact_length_batches(pairs, 16)
        self.assertEqual([len(batch) for batch in batches], [16, 1, 16, 2])
        self.assertTrue(all(len({row["pair_input_tokens"] for row in batch}) == 1 for batch in batches))

    def test_exact_score_cache_is_hash_bound_and_no_overwrite(self) -> None:
        pair = {
            "pair_id": "1" * 64,
            "pair_input_ids_sha256": "2" * 64,
            "pair_input_tokens": 123,
        }
        with tempfile.TemporaryDirectory() as raw:
            cache = runner.ExactScoreCache(Path(raw))
            self.assertIsNone(cache.load(pair))
            path = cache.store(pair, -0.75)
            self.assertTrue(path.is_file())
            self.assertEqual(cache.load(pair), -0.75)
            with self.assertRaisesRegex(ValueError, "overwrite"):
                cache.store(pair, -0.75)

    def test_max_window_exact_tie_and_sha_tie_break(self) -> None:
        candidates = [
            {"source_sha256": "b" * 64, "input_rank": 1, "pair_ids": ["b1", "b2"]},
            {"source_sha256": "a" * 64, "input_rank": 2, "pair_ids": ["a1"]},
        ]
        ranked, ties = runner.rank_candidate_scores(
            candidates, {"b1": -9.0, "b2": 3.0, "a1": 3.0}
        )
        self.assertEqual([row["source_sha256"] for row in ranked], ["a" * 64, "b" * 64])
        self.assertEqual([row["score"] for row in ranked], [3.0, 3.0])
        self.assertEqual(ties, [{"score": 3.0, "source_sha256": ["a" * 64, "b" * 64]}])

    def test_official_b1_and_b2_row_schema_compatibility(self) -> None:
        prompt_id, prompt = next(iter(self.authority.prompts.items()))
        sources = sorted(self.authority.sources)[:100]
        b1_condition = self.authority.b1_conditions["B01-G0"]
        b1 = {
            "schema_version": runner.B1_SCHEMA,
            "status": "SUCCESS",
            "run_id": "synthetic-no-inference",
            "condition_id": "B01-G0",
            "first_stage_cell_id": "B01",
            "prompt_id": prompt_id,
            "prompt_sha256": prompt["prompt_sha256"],
            "representation": b1_condition["representation"],
            "retriever": b1_condition["retriever"],
            "persisted_candidate_source": b1_condition["persisted_candidate_source"],
            "source_union_sha256": b1_condition["source_union_sha256"],
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
            "cost": zero_cost(b2=False),
        }
        validator.validate_b1_row(b1, self.authority, 1)

        condition = self.authority.b2_conditions["B01-GS"]
        inputs = [
            {
                "input_rank": rank,
                "source_sha256": source,
                "candidate_view_sha256": runner.text_sha256(f"view-{source}"),
            }
            for rank, source in enumerate(sources[:20], 1)
        ]
        outputs = [
            {"rank": rank, "input_rank": rank, "source_sha256": source, "score": float(21 - rank)}
            for rank, source in enumerate(sources[:20], 1)
        ]
        b2 = {
            "schema_version": runner.B2_SCHEMA,
            "status": "SUCCESS",
            "run_id": "synthetic-no-inference",
            "condition_id": "B01-GS",
            "phase": condition["phase"],
            "prompt_id": prompt_id,
            "prompt_sha256": prompt["prompt_sha256"],
            "representation": condition["representation"],
            "first_stage_retriever": condition["retriever"],
            "reranker": condition["reranker"],
            "persisted_candidate_source": condition["persisted_candidate_source"],
            "source_union_sha256": condition["source_union_sha256"],
            "input_top20_binding_sha256": b1["top20_binding_sha256"],
            "reranker_input_sha256": runner.reranker_input_sha256(
                condition_id="B01-GS",
                prompt_id=prompt_id,
                prompt_sha256=prompt["prompt_sha256"],
                input_top20_binding_sha256=b1["top20_binding_sha256"],
                input_candidates=inputs,
            ),
            "score_semantics": "HIGHER_IS_BETTER",
            "input_candidates": inputs,
            "reranked_candidates": outputs,
            "cost": zero_cost(b2=True),
        }
        validator.validate_b2_row(b2, self.authority, {("B01-G0", prompt_id): b1}, 1)

    def test_cpu_sensitivity_plan_is_deterministic_and_pending(self) -> None:
        pairs = {}
        for representation_index, representation in enumerate(runner.REPRESENTATIONS):
            for index in range(9):
                pair_id = f"{representation_index:x}{index:x}".ljust(64, "0")
                pairs[pair_id] = {
                    "pair_id": pair_id,
                    "representation": representation,
                    "prompt_id": f"prompt-{index}",
                    "source_sha256": f"{representation_index + 1:x}" * 64,
                    "window_index": index,
                    "pair_input_ids_sha256": f"{index + 1:x}" * 64,
                    "pair_input_tokens": 100 + index,
                }
        first = runner.cpu_sensitivity_plan(pairs)
        second = runner.cpu_sensitivity_plan(dict(reversed(list(pairs.items()))))
        self.assertEqual(first, second)
        self.assertEqual(first["state"], "PENDING_SEPARATE_EXPLICIT_AUTHORISATION_NOT_EXECUTED")
        self.assertEqual(first["model_loads"], 0)
        self.assertTrue(all(len(rows) == 8 for rows in first["selections"].values()))

    def test_scientific_scope_and_external_phase8_bindings(self) -> None:
        self.assertEqual(len(runner.MATERIALISED_CONDITIONS), 15)
        self.assertNotIn("C2-S", runner.MATERIALISED_CONDITIONS)
        self.assertEqual(runner.EXPECTED_B2_ROWS, 15 * 1077)
        self.assertTrue(all(runner.is_sha256(value) for value in runner.MODEL_FILE_SHA256.values()))
        self.assertIn("v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1", runner.FIXED_REPRESENTATION_INPUTS["I1-discovery"]["path"])
        self.assertIn("v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1", runner.FIXED_REPRESENTATION_INPUTS["I2-original"]["path"])
        self.assertNotIn("I3C-fielded", runner.FIXED_REPRESENTATION_INPUTS)
        self.assertNotIn("I3-flat", runner.FIXED_REPRESENTATION_INPUTS)
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaisesRegex(ValueError, "authorisation is missing"):
                runner.validate_root_release(Path(raw), Path(raw) / "absent-release.json")

    def test_preexisting_score_cache_blocks_before_model_or_authority_load(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "skill_benchmark/cache") as raw:
            base = Path(raw)
            cache_dir = base / "score_cache"
            cache_dir.mkdir()
            release = {
                "attempt_id": "synthetic-attempt",
                "_destinations": {
                    "output_dir": base / "output",
                    "cache_dir": cache_dir,
                    "attempt_dir": base / "attempt",
                },
            }
            with (
                mock.patch.object(runner, "validate_root_release", return_value=(release, base / "payload.json", {})),
                mock.patch.object(runner, "load_authority", side_effect=AssertionError("authority loaded")) as load_authority,
            ):
                with self.assertRaisesRegex(ValueError, "pre-existing score cache"):
                    runner.execute(ROOT, base / "release.json")
            load_authority.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
