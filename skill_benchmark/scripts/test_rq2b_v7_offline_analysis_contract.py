#!/usr/bin/env python3
"""Synthetic-only tests for the V7 runner/output and offline analysis contract."""

from __future__ import annotations

import hashlib
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from analyse_rq2b_v7_offline_outputs import OfflineAuthority, analyse
from validate_rq2b_v7_runner_outputs import (
    ROOT,
    RunnerAuthority,
    reranker_input_sha256,
    read_jsonl,
    top20_binding_sha256,
    validate_outputs,
)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def cost(*, b2: bool) -> dict[str, Any]:
    value = {
        "wall_time_ms": 1.0,
        "provider_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "window_forwards": 1,
        "cache_hits": 0,
        "retry_count": 0,
        "timeout_count": 0,
        "failure_count": 0,
    }
    if b2:
        value["candidate_pairs"] = 20
    return value


def synthetic_fixture() -> tuple[list[dict[str, Any]], list[dict[str, Any]], OfflineAuthority]:
    source_list = [sha(f"source-{index}") for index in range(120)]
    prompts = {
        f"P{index}": {
            "schema_version": "synthetic-runtime",
            "prompt_id": f"P{index}",
            "prompt_sha256": sha(f"prompt-{index}"),
            "prompt": f"synthetic query {index}",
        }
        for index in range(4)
    }
    union_sha = sha("source-union")
    b1_conditions: dict[str, dict[str, Any]] = {}
    b2_conditions: dict[str, dict[str, Any]] = {}
    for index in range(1, 13):
        cell = f"B{index:02d}"
        b1_conditions[f"{cell}-G0"] = {
            "condition_id": f"{cell}-G0", "phase": "FIRST_CORE_MATRIX",
            "representation": f"R-{cell}", "retriever": f"T-{cell}",
            "reranker": "NONE", "persisted_candidate_source": cell,
            "source_union_sha256": union_sha,
        }
        for suffix, reranker in (("GQ", "Qwen-qwen3-rerank"), ("GS", "SkillRouter-Reranker-0.6B")):
            condition_id = f"{cell}-{suffix}"
            b2_conditions[condition_id] = {
                **b1_conditions[f"{cell}-G0"], "condition_id": condition_id,
                "reranker": reranker,
            }
    for bridge in ("C1", "C3", "C4"):
        for suffix, reranker in (("Q", "Qwen-qwen3-rerank"), ("S", "SkillRouter-Reranker-0.6B")):
            condition_id = f"{bridge}-{suffix}"
            b2_conditions[condition_id] = {
                "condition_id": condition_id, "phase": "FIXED_CANDIDATE_BRIDGE",
                "representation": f"R-{bridge}", "retriever": "T-B05",
                "reranker": reranker, "persisted_candidate_source": "B05",
                "source_union_sha256": union_sha,
            }
    runner = RunnerAuthority(prompts, set(source_list), b1_conditions, b2_conditions)
    b1_rows: list[dict[str, Any]] = []
    b1_map: dict[tuple[str, str], dict[str, Any]] = {}
    for condition_id, condition in b1_conditions.items():
        cell = condition_id.removesuffix("-G0")
        cell_index = int(cell[1:])
        for prompt_index, (prompt_id, prompt) in enumerate(prompts.items()):
            offset = (cell_index + prompt_index) % 4
            ranking = source_list[offset:] + source_list[:offset]
            binding = top20_binding_sha256(
                condition_id=condition_id, prompt_id=prompt_id,
                prompt_sha256=prompt["prompt_sha256"],
                ordered_source_sha256=ranking[:20],
            )
            row = {
                "schema_version": "rq2b-v7-b1-runner-output-v1", "status": "SUCCESS",
                "run_id": "synthetic-b1", "condition_id": condition_id,
                "first_stage_cell_id": cell, "prompt_id": prompt_id,
                "prompt_sha256": prompt["prompt_sha256"],
                "representation": condition["representation"], "retriever": condition["retriever"],
                "persisted_candidate_source": cell, "source_union_sha256": union_sha,
                "top_k": 100, "score_semantics": "HIGHER_IS_BETTER",
                "top20_binding_sha256": binding,
                "ranked_candidates": [
                    {"rank": rank, "source_sha256": source, "score": float(101 - rank)}
                    for rank, source in enumerate(ranking[:100], 1)
                ],
                "cost": cost(b2=False),
            }
            b1_rows.append(row)
            b1_map[(condition_id, prompt_id)] = row
    b2_rows: list[dict[str, Any]] = []
    for condition_id, condition in b2_conditions.items():
        for prompt_id, prompt in prompts.items():
            source_cell = condition["persisted_candidate_source"]
            first = b1_map[(f"{source_cell}-G0", prompt_id)]
            sources = [item["source_sha256"] for item in first["ranked_candidates"][:20]]
            inputs = [
                {"input_rank": rank, "source_sha256": source, "candidate_view_sha256": sha(f"{condition_id}/{source}")}
                for rank, source in enumerate(sources, 1)
            ]
            # Reverse only SkillRouter outputs, exercising identity-preserving rerank.
            output_sources = list(reversed(sources)) if condition_id.endswith(("GS", "-S")) else sources
            input_rank = {source: rank for rank, source in enumerate(sources, 1)}
            row = {
                "schema_version": "rq2b-v7-b2-runner-output-v1", "status": "SUCCESS",
                "run_id": "synthetic-b2", "condition_id": condition_id,
                "phase": condition["phase"], "prompt_id": prompt_id,
                "prompt_sha256": prompt["prompt_sha256"],
                "representation": condition["representation"],
                "first_stage_retriever": condition["retriever"], "reranker": condition["reranker"],
                "persisted_candidate_source": source_cell, "source_union_sha256": union_sha,
                "input_top20_binding_sha256": first["top20_binding_sha256"],
                "reranker_input_sha256": reranker_input_sha256(
                    condition_id=condition_id, prompt_id=prompt_id,
                    prompt_sha256=prompt["prompt_sha256"],
                    input_top20_binding_sha256=first["top20_binding_sha256"],
                    input_candidates=inputs,
                ),
                "score_semantics": "HIGHER_IS_BETTER", "input_candidates": inputs,
                "reranked_candidates": [
                    {"rank": rank, "input_rank": input_rank[source], "source_sha256": source, "score": float(21 - rank)}
                    for rank, source in enumerate(output_sources, 1)
                ],
                "cost": cost(b2=True),
            }
            b2_rows.append(row)
    labels: dict[str, dict[str, Any]] = {}
    dependencies: dict[str, dict[str, Any]] = {}
    exposures: dict[str, dict[str, Any]] = {}
    dq: dict[str, dict[str, dict[str, Any]]] = {}
    for index, (prompt_id, prompt) in enumerate(prompts.items()):
        acceptable = [source_list[index]] if index < 3 else [source_list[3], source_list[4]]
        judged = [
            {"candidate_source_sha256": source, "adequacy": "FULLY_ACCEPTABLE"}
            for source in acceptable
        ]
        distractor = source_list[(index + 1) % 4]
        if distractor in acceptable:
            distractor = source_list[5]
        judged.append({"candidate_source_sha256": distractor, "adequacy": "INADEQUATE"})
        labels[prompt_id] = {
            "prompt_id": prompt_id, "prompt_sha256": prompt["prompt_sha256"],
            "acceptable_set_source_sha256": acceptable,
            "judged_candidate_dispositions": judged,
            "lane_id": "B_NC_FULL_UNION",
            "reporting_stratum": "source_native_three_member" if index < 3 else "legacy_2member_checkpoint",
            "final_label_type": "STRICT" if len(acceptable) == 1 else "ACCEPTABLE_SET",
            "library_source_count": len(source_list),
            "unjudged_source_count": len(source_list) - len(judged),
        }
        group = f"D{index // 2}"
        dependencies[prompt_id] = {"prompt_id": prompt_id, "prompt_sha256": prompt["prompt_sha256"], "dependency_group": group}
        exposures[prompt_id] = {
            "prompt_id": prompt_id, "prompt_sha256": prompt["prompt_sha256"],
            "dependency_group": group, "analysis_disposition": "NC_PRIMARY_WITH_SOURCE_NATIVE_SENSITIVITY",
            "prompt_level_exposure": "SYNTHETIC", "global_design_exposure": "SYNTHETIC",
        }
        dq[prompt_id] = {distractor: {
            "candidate_source_sha256": distractor, "final_adequacy": "INADEQUATE",
            "relation_rule": "SYNTHETIC_CONFUSABLE",
        }}
    return b1_rows, b2_rows, OfflineAuthority(runner, labels, dependencies, exposures, dq)


class ContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.b1, self.b2, self.authority = synthetic_fixture()

    def test_complete_contract_and_analysis(self) -> None:
        validation = validate_outputs(self.b1, self.b2, self.authority.runner)
        self.assertEqual(validation["outcome_conditions"], 42)
        report = analyse(
            self.b1, self.b2, self.authority,
            bootstrap_replicates=200, sign_flip_replicates=500,
        )
        self.assertEqual(report["counts"]["materialised_outcome_conditions"], 42)
        self.assertEqual(report["counts"]["materialised_outcome_rows"], 168)
        self.assertEqual(report["counts"]["c2_alias_input_rows"], 0)
        self.assertEqual(report["aliases"]["C2-Q"], "B05-GQ")
        self.assertEqual(set(report["primary_comparisons"]), {"P1", "P2", "P3", "P4", "P5"})
        self.assertIn("noninferiority", report["primary_comparisons"]["P2"])
        self.assertIn("paired_group_sign_flip", report["primary_comparisons"]["P5"])
        summary = report["condition_summaries"]["B05-GQ"]["nc_primary"]
        self.assertAlmostEqual(summary["acceptable_known_a"]["identity_residual"], 0.0)
        self.assertEqual(summary["strict_singleton"]["prompts"], 3)

    def test_runner_rejects_label_key(self) -> None:
        broken = dict(self.b1[0])
        broken["gold_source_sha256"] = sha("leak")
        with self.assertRaisesRegex(ValueError, "prohibited"):
            validate_outputs([broken, *self.b1[1:]], self.b2, self.authority.runner)

    def test_runner_rejects_rerank_identity_drift(self) -> None:
        broken_b2 = [dict(row) for row in self.b2]
        broken_b2[0] = dict(broken_b2[0])
        broken_b2[0]["reranked_candidates"] = [dict(item) for item in broken_b2[0]["reranked_candidates"]]
        broken_b2[0]["reranked_candidates"][0]["source_sha256"] = sha("not-an-input")
        with self.assertRaisesRegex(ValueError, "not in frozen input"):
            validate_outputs(self.b1, broken_b2, self.authority.runner)

    def test_json_schemas_are_strict_and_parseable(self) -> None:
        package = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_runner_output_analysis_contract_2026_09_09_v1"
        for name in ("b1_runner_output_schema.json", "b2_runner_output_schema.json", "analysis_contract.json"):
            value = json.loads((package / name).read_text())
            self.assertIsInstance(value, dict)
        self.assertFalse(json.loads((package / "b1_runner_output_schema.json").read_text())["additionalProperties"])
        self.assertFalse(json.loads((package / "b2_runner_output_schema.json").read_text())["additionalProperties"])

    def test_deterministic_gzip_jsonl_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl.gz"
            with path.open("wb") as raw:
                with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                    compressed.write(b'{"row":1}\n{"row":2}\n')
            self.assertEqual(read_jsonl(path), [{"row": 1}, {"row": 2}])


if __name__ == "__main__":
    unittest.main()
