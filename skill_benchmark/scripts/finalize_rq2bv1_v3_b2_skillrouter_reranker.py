#!/usr/bin/env python3
"""Recover, validate, and strictly aggregate RQ2b V3 SkillRouter B2 shards.

The hosted worker emits one score per frozen query/window pair, without gold
labels.  This local tool downloads only those score shards after job completion,
validates their exact pair bindings, then joins them to the local strict B2
conditions.  It is deliberately unable to rebuild candidates or overwrite a
previous result directory.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import shutil
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from prepare_rq2bv1_v3_b2_top20_preflight import PREFLIGHT_DIR, ROOT, read_json, read_jsonl, relative, require, sha256_file, write_json, write_jsonl
from verify_rq2bv1_v3_b2_top20_preflight import verify as verify_preflight


RUNNER_VERSION = "rq2bv1-v3-b2-skillrouter-reranker-finalizer-v2-resume-binding"
MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
REPOSITORY = "baechuer1/honour-thesis-rq2b-checkpoints"
OUTPUT_PREFIX = "rq2bv1/skillrouter-reranker-b2-top20-v3"
HOSTED_PACKAGE = ROOT / "skill_benchmark/rq2bv1/hosted_packages/skillrouter_b2_top20_v3"
HOSTED_BUILD_MANIFEST = HOSTED_PACKAGE / "bundle_build_manifest.json"
RESUME_HOSTED_PACKAGE = ROOT / "skill_benchmark/rq2bv1/hosted_packages/skillrouter_b2_top20_v3_resume_v2_streaming"
RESUME_HOSTED_BUILD_MANIFEST = RESUME_HOSTED_PACKAGE / "bundle_build_manifest.json"
ALLOWED_HOSTED_BUILD_MANIFESTS = (HOSTED_BUILD_MANIFEST, RESUME_HOSTED_BUILD_MANIFEST)
LOCAL_RECOVERY_ROOT = ROOT / "skill_benchmark/rq2bv1/recovered/skillrouter_reranker_top20_v3"
OUTPUT_DIR = ROOT / "skill_benchmark/rq2bv1/results/skillrouter_reranker_top20_v3"


def sha256_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _shard_name(index: int, total: int) -> str:
    return f"shard-{index:04d}-of-{total:04d}.jsonl.gz"


def _read_gzip_jsonl(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _select_hosted_build_manifest(root: Path, bundle_sha256: str) -> tuple[Path, dict[str, Any]]:
    """Choose only a locally sealed bundle whose hash matches completion."""

    for candidate in ALLOWED_HOSTED_BUILD_MANIFESTS:
        manifest = root / candidate.relative_to(ROOT)
        if not manifest.is_file():
            continue
        build = read_json(manifest)
        if build.get("bundle", {}).get("sha256") == bundle_sha256:
            return manifest, build
    raise RuntimeError("Hosted B2 completion does not bind to an allowed sealed bundle")


def _load_local_contract(root: Path, preflight_dir: Path, hosted_build_manifest: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    build = read_json(hosted_build_manifest)
    require(build["state"] == "built_locally_pending_upload_and_hosted_job", "B2 SkillRouter package state drift")
    runtime = build["runtime"]
    pair_path = root / str(runtime["unique_pairs"]["path"])
    require(pair_path.is_file() and sha256_file(pair_path) == runtime["unique_pairs"]["sha256"], "B2 local pair asset drift")
    pairs = read_jsonl(pair_path)
    require(len(pairs) == 73415, "B2 local pair count drift")
    require(sum(int(row["pair_input_token_count"]) for row in pairs) == 36350664, "B2 local pair token total drift")
    require(runtime["model"]["name"] == MODEL and runtime["model"]["revision"] == REVISION, "B2 local model binding drift")
    preflight_manifest = root / str(runtime["preflight_manifest"]["path"])
    require(preflight_manifest == preflight_dir / "manifest.json" and sha256_file(preflight_manifest) == runtime["preflight_manifest"]["sha256"], "B2 preflight binding drift")
    return runtime, pairs


def recover(root: Path, recovery_dir: Path) -> dict[str, Any]:
    """Download completed score-only artifacts once, rejecting an incomplete job."""

    from huggingface_hub import HfApi, hf_hub_download

    token = os.environ.get("HF_TOKEN")
    require(bool(token), "HF_TOKEN is required to recover B2 score checkpoints")
    require(not recovery_dir.exists(), f"Refusing to overwrite B2 recovery directory: {recovery_dir}")
    api = HfApi(token=token)
    remote_paths = set(api.list_repo_files(repo_id=REPOSITORY, repo_type="dataset"))
    completion_remote = f"{OUTPUT_PREFIX}/completion/completion.json"
    require(completion_remote in remote_paths, "Hosted B2 completion is absent; do not recover a partial run")
    recovery_dir.mkdir(parents=True)
    completion = Path(hf_hub_download(repo_id=REPOSITORY, repo_type="dataset", filename=completion_remote, token=token, local_dir=recovery_dir))
    completion_value = read_json(completion)
    require(completion_value["state"] == "completed_score_shards_pending_local_aggregation", "Hosted B2 completion state drift")
    hosted_build_manifest, hosted_build = _select_hosted_build_manifest(root, str(completion_value["input_bundle"]["sha256"]))
    runtime, pairs = _load_local_contract(root, root / PREFLIGHT_DIR, hosted_build_manifest)
    require(completion_value["input_bundle"]["sha256"] == hosted_build["bundle"]["sha256"], "Hosted B2 bundle binding drift")
    require(completion_value["input_bundle"]["path"] == runtime["checkpointing"]["input_bundle_path"], "Hosted B2 input bundle path drift")
    require(completion_value["model"]["name"] == MODEL and completion_value["model"]["revision"] == REVISION, "Hosted B2 completion model binding drift")
    require(int(completion_value["scope"]["unique_pairs"]) == len(pairs), "Hosted B2 completion pair count drift")
    require(int(completion_value["scope"]["unique_model_input_tokens"]) == sum(int(row["pair_input_token_count"]) for row in pairs), "Hosted B2 completion token binding drift")
    shard_size = int(runtime["checkpointing"]["pairs_per_score_shard"])
    total = (len(pairs) + shard_size - 1) // shard_size
    shard_paths: list[dict[str, Any]] = []
    for zero in range(total):
        name = _shard_name(zero + 1, total)
        remote = f"{OUTPUT_PREFIX}/checkpoints/{name}"
        require(remote in remote_paths, f"Hosted B2 score shard missing: {remote}")
        local = Path(hf_hub_download(repo_id=REPOSITORY, repo_type="dataset", filename=remote, token=token, local_dir=recovery_dir / "checkpoints"))
        shard_paths.append({"name": name, "path": str(local.relative_to(recovery_dir)), "sha256": sha256_file(local), "rows": len(_read_gzip_jsonl(local))})
    receipt = {"schema_version": "rq2bv1-v3-b2-skillrouter-score-recovery-v2-resume-binding", "state": "recovered_complete_score_shards_pending_local_aggregation", "repository": REPOSITORY, "output_prefix": OUTPUT_PREFIX, "completion": {"path": str(completion.relative_to(recovery_dir)), "sha256": sha256_file(completion)}, "sealed_bundle": {"build_manifest": relative(hosted_build_manifest, root), "build_manifest_sha256": sha256_file(hosted_build_manifest), "bundle_sha256": hosted_build["bundle"]["sha256"]}, "shards": shard_paths, "network_calls": len(shard_paths) + 2, "automatic_retries": 0, "thesis_result_writing": False}
    write_json(recovery_dir / "recovery_receipt.json", receipt)
    return receipt


def _load_scores(recovery_dir: Path, pairs: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    receipt = read_json(recovery_dir / "recovery_receipt.json")
    require(receipt["state"] == "recovered_complete_score_shards_pending_local_aggregation", "B2 recovery receipt state drift")
    score_by_pair: dict[str, dict[str, Any]] = {}
    ordered_pairs = iter(pairs)
    elapsed = 0.0
    for binding in receipt["shards"]:
        path = recovery_dir / str(binding["path"])
        require(path.is_file() and sha256_file(path) == binding["sha256"], f"B2 recovered shard hash drift: {path}")
        rows = _read_gzip_jsonl(path)
        require(len(rows) == binding["rows"], f"B2 recovered shard count drift: {path}")
        for score_row in rows:
            pair = next(ordered_pairs, None)
            require(pair is not None, "B2 recovered more scores than frozen pairs")
            require(score_row.get("schema_version") == "rq2bv1-v3-b2-skillrouter-score-v1", "B2 score schema drift")
            require(score_row.get("pair_id") == pair["pair_id"], "B2 score pair identity/order drift")
            require(int(score_row.get("pair_input_token_count", -1)) == int(pair["pair_input_token_count"]), "B2 score token binding drift")
            score = float(score_row.get("score", float("nan")))
            pair_time = float(score_row.get("amortised_model_forward_seconds", float("nan")))
            require(math.isfinite(score) and math.isfinite(pair_time) and pair_time >= 0.0, "B2 score value/time drift")
            score_by_pair[str(pair["pair_id"])] = score_row
            elapsed += pair_time
    require(next(ordered_pairs, None) is None and len(score_by_pair) == len(pairs), "B2 recovered score coverage drift")
    return score_by_pair, {"score_rows": len(score_by_pair), "amortised_model_forward_seconds": elapsed}


def _aggregate(condition: dict[str, Any], strict: dict[str, Any], score_by_pair: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_skill: dict[str, list[float]] = defaultdict(list)
    condition_compute = 0.0
    for candidate in condition["candidates"]:
        for window in candidate["windows"]:
            score = score_by_pair[str(window["pair_id"])]
            by_skill[str(candidate["skill_id"])].append(float(score["score"]))
            condition_compute += float(score["amortised_model_forward_seconds"])
    require(set(by_skill) == set(condition["candidate_skill_ids"]) and all(by_skill.values()), "B2 candidate score coverage drift")
    first_rank = {skill_id: index for index, skill_id in enumerate(condition["candidate_skill_ids"], start=1)}
    ranked = sorted(((skill_id, max(values)) for skill_id, values in by_skill.items()), key=lambda row: (-row[1], first_rank[row[0]], row[0]))
    reranked_ids = [skill_id for skill_id, _ in ranked]
    gold = str(strict["gold_skill"])
    gold_rank = reranked_ids.index(gold) + 1 if gold in reranked_ids else None
    candidate_positive = int(gold in condition["candidate_skill_ids"])
    first_top1 = int(condition["candidate_skill_ids"][0] == gold)
    reranked_top1 = int(reranked_ids[0] == gold)
    return {"schema_version": "rq2bv1-v3-b2-strict-result-row-v1", "runner_version": RUNNER_VERSION, "reranker": MODEL, "reranker_revision": REVISION, "first_stage_retriever": condition["first_stage_retriever"], "representation": condition["representation"], "prompt_id": condition["prompt_id"], "prompt_sha256": condition["prompt_sha256"], "stratum": strict["stratum"], "group": strict["group"], "gold_skill": gold, "candidate_skill_ids": condition["candidate_skill_ids"], "candidate_list_sha256": condition["candidate_list_sha256"], "reranked_skill_ids": reranked_ids, "reranked_scores": [score for _, score in ranked], "strict_candidate_positive": candidate_positive, "first_stage_strict_top1": first_top1, "reranked_strict_top1": reranked_top1, "conditional_strict_top1_numerator": int(candidate_positive and reranked_top1), "conditional_strict_top1_denominator": candidate_positive, "end_to_end_strict_top1": reranked_top1, "end_to_end_strict_mrr_at_20": 0.0 if gold_rank is None else 1.0 / gold_rank, "strict_reranker_gain": int(candidate_positive and reranked_top1 and not first_top1), "strict_reranker_regression": int(first_top1 and not reranked_top1), "primary_window_aggregation": "maximum_window_score", "model_window_count": sum(len(candidate["windows"]) for candidate in condition["candidates"]), "amortised_model_forward_seconds": condition_compute, "score_source": "hosted_deduplicated_pair_score_shards"}


def _timing(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)
    def pct(q: float) -> float:
        return float(ordered[max(0, math.ceil(q * len(ordered)) - 1)])
    return {"mean_seconds": mean(values), "p50_seconds": pct(0.50), "p95_seconds": pct(0.95), "max_seconds": max(values)}


def _metric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if int(row["strict_candidate_positive"])]
    return {"conditions": len(rows), "first_stage_recall_at_20": mean(float(row["strict_candidate_positive"]) for row in rows), "first_stage_strict_hit_at_1": mean(float(row["first_stage_strict_top1"]) for row in rows), "conditional_strict_hit_at_1": None if not eligible else mean(float(row["reranked_strict_top1"]) for row in eligible), "conditional_denominator": len(eligible), "end_to_end_strict_hit_at_1": mean(float(row["end_to_end_strict_top1"]) for row in rows), "end_to_end_strict_mrr_at_20": mean(float(row["end_to_end_strict_mrr_at_20"]) for row in rows), "reranker_gains": sum(int(row["strict_reranker_gain"]) for row in rows), "reranker_regressions": sum(int(row["strict_reranker_regression"]) for row in rows), "amortised_model_compute": _timing([float(row["amortised_model_forward_seconds"]) for row in rows]), "model_windows": {"total": sum(int(row["model_window_count"]) for row in rows), "mean_per_condition": mean(float(row["model_window_count"]) for row in rows), "max_per_condition": max(int(row["model_window_count"]) for row in rows)}}


def finalize(root: Path, recovery_dir: Path, output_dir: Path, preflight_dir: Path) -> dict[str, Any]:
    require(not output_dir.exists(), f"Refusing to overwrite B2 SkillRouter result: {output_dir}")
    preflight = verify_preflight(root, preflight_dir)
    recovery_receipt = read_json(recovery_dir / "recovery_receipt.json")
    hosted_build_manifest = root / str(recovery_receipt["sealed_bundle"]["build_manifest"])
    allowed_paths = {root / candidate.relative_to(ROOT) for candidate in ALLOWED_HOSTED_BUILD_MANIFESTS}
    require(hosted_build_manifest in allowed_paths, "B2 recovery sealed bundle manifest is not an allowed local artifact")
    require(hosted_build_manifest.is_file() and sha256_file(hosted_build_manifest) == recovery_receipt["sealed_bundle"]["build_manifest_sha256"], "B2 recovery sealed bundle manifest drift")
    runtime, pairs = _load_local_contract(root, preflight_dir, hosted_build_manifest)
    score_by_pair, ledger = _load_scores(recovery_dir, pairs)
    conditions = read_jsonl(preflight_dir / "conditions.jsonl")
    strict = read_jsonl(preflight_dir / "strict_bindings.jsonl")
    strict_by_id = {str(row["condition_id"]): row for row in strict}
    require(len(conditions) == len(strict) == 4572 and len(strict_by_id) == 4572, "B2 local strict condition coverage drift")
    rows = [_aggregate(condition, strict_by_id[str(condition["condition_id"])], score_by_pair) for condition in conditions]
    output_dir.mkdir(parents=True)
    rows_path = output_dir / "rows.jsonl"
    write_jsonl(rows_path, rows)
    hosted_completion = read_json(recovery_dir / str(recovery_receipt["completion"]["path"]))
    ledger.update({"schema_version": "rq2bv1-v3-b2-skillrouter-model-ledger-v1", "unique_pair_scores": len(score_by_pair), "score_shards": len(recovery_receipt["shards"]), "hosted_job_elapsed_seconds": float(hosted_completion["timing"]["job_elapsed_seconds"]), "hosted_model_load_seconds": float(hosted_completion["timing"]["model_load_seconds"]), "automatic_retries": 0})
    ledger_path = output_dir / "ledger.json"
    write_json(ledger_path, ledger)
    manifest = {"schema_version": "rq2bv1-v3-b2-skillrouter-run-manifest-v1", "state": "completed_pending_local_integrity_verification", "method": {"model": MODEL, "revision": REVISION, "window_aggregation": "maximum_window_score", "pair_scoring": "pinned_cross_encoder_yes_minus_no_logit", "score_source": "hosted_deduplicated_pair_score_shards"}, "preflight_manifest": {"path": relative(preflight_dir / "manifest.json", root), "sha256": sha256_file(preflight_dir / "manifest.json")}, "recovery_receipt": {"path": relative(recovery_dir / "recovery_receipt.json", root), "sha256": sha256_file(recovery_dir / "recovery_receipt.json")}, "artifacts": {"rows": {"path": relative(rows_path, root), "sha256": sha256_file(rows_path), "rows": len(rows)}, "ledger": {"path": relative(ledger_path, root), "sha256": sha256_file(ledger_path)}}, "thesis_result_writing": False}
    write_json(output_dir / "manifest.json", manifest)
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["first_stage_retriever"], row["representation"], row["stratum"])].append(row)
    summary = {"schema_version": "rq2bv1-v3-b2-skillrouter-post-run-summary-v1", "state": "completed_pending_user_result_review", "scope": {"reranker": MODEL, "revision": REVISION, "top_k": 20, "conditions": len(rows), "representations": ["i1-discovery", "i2-original", "i3-flat-evidence", "i3c-fielded-evidence"], "first_stage_retrievers": ["bm25", "qwen-text-embedding-v4", "skillrouter-embedding-0.6b"]}, "model_execution": ledger, "by_first_stage_and_representation": {f"{retriever}/{representation}": {"overall": _metric([row for row in rows if row["first_stage_retriever"] == retriever and row["representation"] == representation]), "controlled": _metric(groups[(retriever, representation, "controlled")]), "public_gold": _metric(groups[(retriever, representation, "public_gold")])} for retriever in ("bm25", "qwen-text-embedding-v4", "skillrouter-embedding-0.6b") for representation in ("i1-discovery", "i2-original", "i3-flat-evidence", "i3c-fielded-evidence")}, "interpretation_boundary": "This validates pinned SkillRouter B2 cross-encoder reranking over frozen V3 strict-gold-only Top-20 candidates. The model-compute values are amortised pair-forward equivalents from deduplicated hosted shards, not end-to-end interactive latency.", "thesis_result_writing": False}
    verification = {"schema_version": "rq2bv1-v3-b2-skillrouter-post-run-verification-v1", "state": "passed_local_post_run_integrity_verification", "preflight": {"path": relative(preflight_dir / "manifest.json", root), "sha256": sha256_file(preflight_dir / "manifest.json")}, "checks": {**preflight["checks"], "strict_b2_rows_validated": len(rows), "unique_pair_scores_validated": len(score_by_pair), "warm_aggregation_replay_conditions": len(rows), "automatic_retries": 0}, "thesis_result_writing": False}
    write_json(output_dir / "post_run_verification.json", verification)
    write_json(output_dir / "post_run_summary.json", summary)
    return {"state": verification["state"], "result_dir": relative(output_dir, root), "rows": len(rows), "unique_pair_scores": len(score_by_pair)}


def self_test() -> dict[str, Any]:
    condition = {"candidate_skill_ids": ["a", "b"], "candidates": [{"skill_id": "a", "windows": [{"pair_id": "p1"}]}, {"skill_id": "b", "windows": [{"pair_id": "p2"}]}], "first_stage_retriever": "synthetic", "representation": "synthetic", "prompt_id": "p", "prompt_sha256": "x", "candidate_list_sha256": sha256_json(["a", "b"])}
    row = _aggregate(condition, {"gold_skill": "b", "stratum": "controlled", "group": "synthetic"}, {"p1": {"score": 0.1, "amortised_model_forward_seconds": 0.0}, "p2": {"score": 0.9, "amortised_model_forward_seconds": 0.0}})
    require(row["reranked_skill_ids"] == ["b", "a"] and row["end_to_end_strict_top1"] == 1, "Synthetic B2 aggregation failed")
    return {"state": "passed_local_synthetic_aggregation_no_network_no_model_forward", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recover", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--recovery-dir", type=Path, default=LOCAL_RECOVERY_ROOT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--preflight-dir", type=Path, default=Path(PREFLIGHT_DIR))
    args = parser.parse_args()
    require(int(args.recover) + int(args.finalize) + int(args.self_test) == 1, "Choose exactly one mode")
    recovery = args.recovery_dir if args.recovery_dir.is_absolute() else ROOT / args.recovery_dir
    output = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    preflight = args.preflight_dir if args.preflight_dir.is_absolute() else ROOT / args.preflight_dir
    result = self_test() if args.self_test else (recover(ROOT, recovery) if args.recover else finalize(ROOT, recovery, output, preflight))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
