#!/usr/bin/env python3
"""Resumable hosted scorer for the frozen RQ2b V3 SkillRouter B2 pair set.

The worker is executed only from a sealed input bundle.  It scores the fixed
strict-gold-free query/window pairs with the pinned SkillRouter cross-encoder,
persists score-only shards to the approved Hugging Face dataset, and stops on
the first upload/model/hash error.  A later job can resume only complete,
validated shards; it never regenerates candidates or reuses legacy labels.
"""

from __future__ import annotations

import argparse
import gc
import gzip
import hashlib
import json
import math
import os
import shutil
import sys
import tarfile
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Any


JOB_VERSION = "rq2bv1-v3-b2-skillrouter-reranker-hf-job-v2-streaming-resume"
MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
MODEL_FILE_SHA256 = {
    "config.json": "17f3b5063350823bfda01f740ac14b9d1cd9cb80c738cbe0d9939c4988ac6b39",
    "tokenizer.json": "ab19c66299579df20542864f9e27b79898ca05f35acc97fd9259aee385a07d4a",
    "model.safetensors": "34064850b1b512168309481a9cebe4ecaf55d0821bf22608f657b40033ed36d7",
}
INSTRUCTION = "Given a task description, judge whether the skill document is relevant and useful for completing the task"
BODY_FORMAT = "<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {document}"
PREFIX = "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\".<|im_end|>\n<|im_start|>user\n"
SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
MAX_PAIR_TOKENS = 2048
# The model returns full-vocabulary logits for every input position. Keep the
# batch deliberately small in the resumed GPU job to bound peak host and VRAM.
DEFAULT_BATCH_SIZE = 2
WORKSPACE = Path("/tmp/rq2bv1_v3_b2_skillrouter_reranker")
RUNTIME_RELATIVE_PATH = "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2/hf_skillrouter_runtime.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(result, dict), f"Expected JSON object: {path}")
    return result


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        for member in members:
            pure = PurePosixPath(member.name)
            require(not pure.is_absolute() and ".." not in pure.parts and not member.issym() and not member.islnk(), f"Unsafe bundle member: {member.name}")
        try:
            handle.extractall(destination, members=members, filter="data")
        except TypeError:
            handle.extractall(destination, members=members)


def require_token() -> str:
    token = os.environ.get("HF_TOKEN")
    require(bool(token), "HF_TOKEN is required for input recovery and score checkpoints")
    return str(token)


def build_input_ids(tokenizer: Any, query: str, document: str) -> list[int]:
    body = BODY_FORMAT.format(instruction=INSTRUCTION, query=query, document=document)
    return tokenizer.encode(PREFIX, add_special_tokens=False) + tokenizer.encode(body, add_special_tokens=False) + tokenizer.encode(SUFFIX, add_special_tokens=False)


def iter_pair_shards(path: Path, shard_size: int) -> Any:
    """Yield validated source pairs one shard at a time without retaining the library."""
    require(shard_size == 5000, "Hosted B2 shard size drift")
    seen: set[str] = set()
    total_tokens = 0
    total_pairs = 0
    shard: list[dict[str, Any]] = []
    shard_index = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            require(row.get("schema_version") == "rq2bv1-v3-b2-top20-pair-v1", "Hosted B2 pair schema drift")
            pair_id = str(row.get("pair_id", ""))
            require(pair_id and pair_id not in seen, "Hosted B2 pair identity drift")
            seen.add(pair_id)
            count = int(row.get("pair_input_token_count", -1))
            require(0 < count <= 2032, "Hosted B2 pair token-limit drift")
            total_tokens += count
            total_pairs += 1
            require(not any(key in row for key in ("gold_skill", "valid_skills", "group", "stratum", "cluster", "metric", "result")), "B2 score worker received a label-like field")
            shard.append(row)
            if len(shard) == shard_size:
                shard_index += 1
                yield shard_index, shard
                shard = []
    if shard:
        shard_index += 1
        yield shard_index, shard
    require(total_pairs == 73415, "Hosted B2 pair count drift")
    require(total_tokens == 36350664, "Hosted B2 total input-token drift")
    require(shard_index == 15, "Hosted B2 shard count drift")


def score_shard_name(index: int, total: int) -> str:
    return f"shard-{index:04d}-of-{total:04d}.jsonl.gz"


def read_score_shard(path: Path, expected_pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    require(len(rows) == len(expected_pairs), f"Checkpoint score row count drift: {path}")
    for score_row, pair in zip(rows, expected_pairs, strict=True):
        require(score_row.get("schema_version") == "rq2bv1-v3-b2-skillrouter-score-v1", "Checkpoint score schema drift")
        require(score_row.get("pair_id") == pair["pair_id"], "Checkpoint pair order drift")
        require(int(score_row.get("pair_input_token_count", -1)) == int(pair["pair_input_token_count"]), "Checkpoint token binding drift")
        score = float(score_row.get("score", float("nan")))
        require(math.isfinite(score), "Checkpoint score is non-finite")
    return rows


def write_score_shard(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    with gzip.open(temporary, "wt", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def load_model(runtime: dict[str, Any]) -> tuple[Any, Any, Any, int, int]:
    import torch
    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM, AutoTokenizer

    require(torch.cuda.is_available(), "SkillRouter B2 requires a CUDA Hugging Face Job")
    model_spec = runtime["model"]
    snapshot = Path(snapshot_download(repo_id=MODEL, revision=REVISION, token=require_token(), allow_patterns=["*.json", "merges.txt", "vocab.json", "model.safetensors"]))
    for filename, expected in MODEL_FILE_SHA256.items():
        candidate = snapshot / filename
        require(candidate.is_file() and sha256_file(candidate) == expected, f"Pinned reranker file hash mismatch: {filename}")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, padding_side="left", local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False, torch_dtype=torch.float16, use_safetensors=True).eval().to("cuda")
    yes = tokenizer.encode("yes", add_special_tokens=False)
    no = tokenizer.encode("no", add_special_tokens=False)
    require(len(yes) == len(no) == 1, "SkillRouter yes/no token contract drift")
    require(tokenizer.pad_token_id is not None or tokenizer.eos_token_id is not None, "SkillRouter tokenizer lacks padding")
    require(model_spec == {"name": MODEL, "revision": REVISION, "files": MODEL_FILE_SHA256, "trust_remote_code": False}, "Runtime model binding drift")
    return torch, tokenizer, model, yes[0], no[0]


def score_pairs(pairs: list[dict[str, Any]], *, torch: Any, tokenizer: Any, model: Any, yes_token: int, no_token: int, batch_size: int, shard_index: int, shard_total: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(batch_size > 0, "SkillRouter batch size must be positive")
    pad_token = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    scores: list[dict[str, Any]] = []
    batch_elapsed_seconds = 0.0
    input_preparation_seconds = 0.0
    for start in range(0, len(pairs), batch_size):
        batch_pairs = pairs[start : start + batch_size]
        token_started = time.perf_counter()
        batch = []
        for pair in batch_pairs:
            input_ids = build_input_ids(tokenizer, str(pair["query"]), str(pair["window_text"]))
            require(len(input_ids) == int(pair["pair_input_token_count"]), f"Pair tokenizer drift: {pair['pair_id']}")
            require(len(input_ids) <= MAX_PAIR_TOKENS, f"Pair exceeds max tokens: {pair['pair_id']}")
            batch.append((pair, input_ids))
        input_preparation_seconds += time.perf_counter() - token_started
        maximum = max(len(ids) for _, ids in batch)
        inputs = torch.full((len(batch), maximum), pad_token, dtype=torch.long, device="cuda")
        attention = torch.zeros_like(inputs)
        for offset, (_, input_ids) in enumerate(batch):
            inputs[offset, -len(input_ids):] = torch.tensor(input_ids, dtype=torch.long, device="cuda")
            attention[offset, -len(input_ids):] = 1
        started = time.perf_counter()
        with torch.inference_mode():
            logits = model(input_ids=inputs, attention_mask=attention).logits[:, -1, :]
        values = (logits[:, yes_token] - logits[:, no_token]).detach().float().cpu().tolist()
        elapsed = time.perf_counter() - started
        batch_elapsed_seconds += elapsed
        per_pair_seconds = elapsed / len(batch)
        for (pair, input_ids), score in zip(batch, values, strict=True):
            scores.append({"schema_version": "rq2bv1-v3-b2-skillrouter-score-v1", "pair_id": pair["pair_id"], "pair_input_token_count": len(input_ids), "score": float(score), "amortised_model_forward_seconds": per_pair_seconds})
        completed = start + len(batch)
        del logits, values, attention, inputs, batch
        if completed % 800 == 0 or completed == len(pairs):
            print(f"SCORE_PROGRESS shard={shard_index}/{shard_total} pairs={completed}/{len(pairs)}", flush=True)
        if completed % 400 == 0:
            torch.cuda.empty_cache()
            gc.collect()
    return scores, {"pairs": len(pairs), "input_tokens": sum(int(pair["pair_input_token_count"]) for pair in pairs), "input_preparation_seconds": input_preparation_seconds, "model_forward_seconds": batch_elapsed_seconds, "batch_size": batch_size}


def execute_hosted() -> dict[str, Any]:
    from huggingface_hub import HfApi, hf_hub_download

    input_repository = os.environ.get("RQ2BV1_B2_SR_INPUT_REPOSITORY")
    input_path = os.environ.get("RQ2BV1_B2_SR_INPUT_BUNDLE_PATH")
    input_sha256 = os.environ.get("RQ2BV1_B2_SR_INPUT_BUNDLE_SHA256")
    require(input_repository and input_path and input_sha256, "Missing bound B2 SkillRouter input-bundle environment")
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)
    bundle = Path(hf_hub_download(repo_id=input_repository, repo_type="dataset", filename=input_path, token=require_token()))
    require(sha256_file(bundle) == input_sha256, "Downloaded B2 SkillRouter input bundle hash mismatch")
    safe_extract(bundle, WORKSPACE)
    runtime = read_json(WORKSPACE / RUNTIME_RELATIVE_PATH)
    require(runtime.get("schema_version") == "rq2bv1-v3-b2-skillrouter-hf-runtime-v1", "B2 SkillRouter runtime schema drift")
    worker_binding = runtime["worker"]
    worker = WORKSPACE / str(worker_binding["path"])
    require(worker.is_file() and sha256_file(worker) == worker_binding["sha256"], "B2 SkillRouter worker binding drift")
    pair_binding = runtime["unique_pairs"]
    pair_path = WORKSPACE / str(pair_binding["path"])
    require(pair_path.is_file() and sha256_file(pair_path) == pair_binding["sha256"], "B2 SkillRouter pair binding drift")
    checkpointing = runtime["checkpointing"]
    repository = str(checkpointing["repository"])
    output_prefix = str(checkpointing["output_prefix"])
    shard_size = int(checkpointing["pairs_per_score_shard"])
    require(checkpointing["automatic_retries"] == 0 and shard_size == 5000, "B2 checkpoint policy drift")
    api = HfApi(token=require_token())
    remote_paths = set(api.list_repo_files(repo_id=repository, repo_type="dataset"))
    shard_total = 15
    recovered = 0
    all_shards: list[dict[str, Any]] = []
    torch = tokenizer = model = yes_token = no_token = None
    model_load_seconds = 0.0
    started = time.perf_counter()
    local_scores = WORKSPACE / "scores"
    for shard_index, expected_pairs in iter_pair_shards(pair_path, shard_size):
        name = score_shard_name(shard_index, shard_total)
        remote_path = f"{output_prefix}/checkpoints/{name}"
        local_path = local_scores / name
        if remote_path in remote_paths:
            downloaded = Path(hf_hub_download(repo_id=repository, repo_type="dataset", filename=remote_path, token=require_token(), local_dir=local_scores))
            rows = read_score_shard(downloaded, expected_pairs)
            recovered += len(rows)
            all_shards.append({"name": name, "state": "recovered", "rows": len(rows), "sha256": sha256_file(downloaded)})
            print(f"CHECKPOINT_RECOVERED shard={shard_index}/{shard_total} pairs={len(rows)}", flush=True)
            continue
        if torch is None:
            load_started = time.perf_counter()
            torch, tokenizer, model, yes_token, no_token = load_model(runtime)
            model_load_seconds = time.perf_counter() - load_started
            print(f"MODEL_READY device=cuda model_load_seconds={model_load_seconds:.3f}", flush=True)
        rows, timing = score_pairs(expected_pairs, torch=torch, tokenizer=tokenizer, model=model, yes_token=yes_token, no_token=no_token, batch_size=DEFAULT_BATCH_SIZE, shard_index=shard_index, shard_total=shard_total)
        write_score_shard(local_path, rows)
        require(len(read_score_shard(local_path, expected_pairs)) == len(expected_pairs), "Local checkpoint validation failed")
        print(f"CHECKPOINT_UPLOAD_START shard={shard_index}/{shard_total} pairs={len(rows)}", flush=True)
        api.upload_file(path_or_fileobj=str(local_path), path_in_repo=remote_path, repo_id=repository, repo_type="dataset", commit_message=f"RQ2b V3 B2 SkillRouter score shard {shard_index:04d}/{shard_total:04d}")
        remote_paths.add(remote_path)
        all_shards.append({"name": name, "state": "scored_uploaded", "rows": len(rows), "sha256": sha256_file(local_path), "timing": timing})
        print(f"CHECKPOINT_UPLOAD_DONE shard={shard_index}/{shard_total} pairs={len(rows)}", flush=True)
    completion = {"schema_version": "rq2bv1-v3-b2-skillrouter-hosted-completion-v1", "state": "completed_score_shards_pending_local_aggregation", "job_version": JOB_VERSION, "input_bundle": {"repository": input_repository, "path": input_path, "sha256": input_sha256}, "runtime_sha256": sha256_file(WORKSPACE / RUNTIME_RELATIVE_PATH), "model": runtime["model"], "scope": runtime["scope"], "checkpointing": {"repository": repository, "output_prefix": output_prefix, "pairs_recovered": recovered, "score_shards": all_shards, "automatic_retries": 0}, "timing": {"job_elapsed_seconds": time.perf_counter() - started, "model_load_seconds": model_load_seconds}, "thesis_result_writing": False}
    completion_path = WORKSPACE / "completion.json"
    write_json(completion_path, completion)
    remote_completion = f"{output_prefix}/completion/completion.json"
    require(remote_completion not in remote_paths, "B2 SkillRouter completion already exists; refuse overwrite")
    print("COMPLETION_UPLOAD_START", flush=True)
    api.upload_file(path_or_fileobj=str(completion_path), path_in_repo=remote_completion, repo_id=repository, repo_type="dataset", commit_message="RQ2b V3 B2 SkillRouter hosted score completion")
    print("COMPLETION_UPLOAD_DONE", flush=True)
    print("HOSTED_COMPLETION_JSON " + json.dumps(completion, sort_keys=True), flush=True)
    return completion


def self_test() -> dict[str, Any]:
    payload = {"schema_version": "rq2bv1-v3-b2-skillrouter-score-v1", "pair_id": "p", "pair_input_token_count": 1, "score": 0.0, "amortised_model_forward_seconds": 0.0}
    with tempfile.TemporaryDirectory(prefix="rq2bv1-b2-sr-test-") as directory:
        path = Path(directory) / "score.jsonl.gz"
        write_score_shard(path, [payload])
        rows = read_score_shard(path, [{"pair_id": "p", "pair_input_token_count": 1}])
        require(rows == [payload], "Score-shard synthetic round-trip failed")
    return {"state": "passed_local_zero_network_no_model_forward", "job_version": JOB_VERSION, "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-hosted", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.execute_hosted != args.self_test, "Choose exactly one of --execute-hosted or --self-test")
    result = execute_hosted() if args.execute_hosted else self_test()
    if args.self_test:
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
