#!/usr/bin/env python3
"""Run RQ2a selectors over fixed three-candidate matched-content decisions."""

from __future__ import annotations

import argparse
import http.client
import json
import math
import os
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    EPSILON,
    PROTOCOL_VERSION,
    RUN_MANIFEST_SCHEMA_VERSION,
    SERIALISER_VERSION,
    audit_token_count,
    bm25_scores,
    build_result_row,
    cosine,
    load_run_data,
    render_summary_markdown,
    representation_documents,
    repo_root,
    self_test,
    sha256_file,
    sha256_json,
    sha256_text,
    slug,
    summarise_result_rows,
    utc_timestamp,
    validate_confirmatory_execution_grant,
    validate_confirmatory_freeze_manifest,
    write_json_atomic,
    write_jsonl_atomic,
)


CORE_REPRESENTATIONS = [
    "shared-only",
    "same-facts-fielded",
    "same-facts-flat",
    "same-facts-prose",
    "same-facts-diluted-2x",
]
SELECTORS = ["bm25", "qwen-single-vector", "skillrouter-cross-encoder"]
QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "text-embedding-v4"
QWEN_DIMENSIONS = 1024
SKILLROUTER_MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
SKILLROUTER_REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
SKILLROUTER_PROMPT_VERSION = "skillrouter-reranker-prompt-v1"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def post_json(
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
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                parsed = json.loads(response.read().decode("utf-8"))
                if not isinstance(parsed, dict):
                    raise RuntimeError(f"{url} returned a non-object JSON response")
                return parsed
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 3:
                raise RuntimeError(
                    f"{url} returned HTTP {exc.code}: {detail[:1000]}"
                ) from exc
        except (
            TimeoutError,
            urllib.error.URLError,
            http.client.IncompleteRead,
        ) as exc:
            if attempt == 3:
                raise RuntimeError(f"{url} failed after retries: {exc}") from exc
        time.sleep(2**attempt)
    raise RuntimeError(f"{url} failed after retries")


class RQ2aEmbeddingClient:
    """OpenAI-compatible embedding client with exact-text persistent caching."""

    def __init__(
        self,
        *,
        provider: str,
        base_url: str,
        api_key: str,
        model: str,
        dimensions: int,
        cache_dir: Path,
        timeout_seconds: int,
        max_audit_tokens: int,
        legacy_cache_dir: Path | None = None,
    ) -> None:
        self.provider = provider
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions
        self.timeout_seconds = timeout_seconds
        self.max_audit_tokens = max_audit_tokens
        self.legacy_cache_dir = legacy_cache_dir
        self.cache_dir = (
            cache_dir
            / "embeddings"
            / slug(provider)
            / slug(model)
            / str(dimensions)
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.stats: dict[str, Any] = {
            "requested_unique_texts": 0,
            "cache_hits": 0,
            "legacy_cache_hits": 0,
            "cache_misses": 0,
            "api_calls": 0,
            "api_elapsed_seconds": 0.0,
            "provider_usage": {},
            "maximum_audit_tokens": 0,
        }

    def config(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "base_url": self.base_url,
            "model": self.model,
            "dimensions": self.dimensions,
            "max_audit_tokens": self.max_audit_tokens,
            "cache_key": "provider+base_url+model+dimensions+exact_text",
            "truncation": False,
        }

    def cache_path(self, text: str) -> Path:
        key = sha256_json({**self.config(), "text": text})
        return self.cache_dir / f"{key}.json"

    def load_current_cache(self, text: str, path: Path) -> list[float]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        expected = {
            "schema_version": "rq2a-embedding-cache-v1",
            "provider": self.provider,
            "base_url": self.base_url,
            "model": self.model,
            "dimensions": self.dimensions,
            "text_sha256": sha256_text(text),
            "audit_token_count": audit_token_count(text),
        }
        for key, value in expected.items():
            if payload.get(key) != value:
                raise ValueError(
                    f"Embedding cache metadata mismatch for {key}: {path}"
                )
        vector = payload.get("embedding")
        if not isinstance(vector, list) or len(vector) != self.dimensions:
            raise ValueError(f"Invalid embedding cache entry: {path}")
        converted = [float(value) for value in vector]
        if any(not math.isfinite(value) for value in converted):
            raise ValueError(f"Non-finite embedding cache entry: {path}")
        return converted

    def legacy_cache_paths(self, text: str) -> list[tuple[Path, int | None]]:
        if self.legacy_cache_dir is None:
            return []
        paths: list[tuple[Path, int | None]] = []
        for requested_dimensions in (self.dimensions, None):
            payload = {
                "provider": self.provider,
                "base_url": self.base_url,
                "model": self.model,
                "dimensions": requested_dimensions,
                "text": text,
            }
            # run_provider_selectors.py used default json separators.
            key = sha256_text(
                json.dumps(
                    payload,
                    sort_keys=True,
                    ensure_ascii=False,
                )
            )
            paths.append(
                (
                    self.legacy_cache_dir
                    / "embeddings"
                    / slug(self.provider)
                    / slug(self.model)
                    / f"{key}.json",
                    requested_dimensions,
                )
            )
        return paths

    def _load_legacy_exact_cache(
        self,
        text: str,
        destination: Path,
    ) -> list[float] | None:
        for legacy_path, requested_dimensions in self.legacy_cache_paths(text):
            if not legacy_path.exists():
                continue
            payload = json.loads(legacy_path.read_text(encoding="utf-8"))
            vector = payload.get("embedding")
            if not isinstance(vector, list) or len(vector) != self.dimensions:
                raise ValueError(f"Invalid legacy embedding cache entry: {legacy_path}")
            converted = [float(value) for value in vector]
            if any(not math.isfinite(value) for value in converted):
                raise ValueError(
                    f"Non-finite legacy embedding cache entry: {legacy_path}"
                )
            write_json_atomic(
                destination,
                {
                    "schema_version": "rq2a-embedding-cache-v1",
                    "provider": self.provider,
                    "base_url": self.base_url,
                    "model": self.model,
                    "dimensions": self.dimensions,
                    "text_sha256": sha256_text(text),
                    "audit_token_count": audit_token_count(text),
                    "embedding": converted,
                    "provenance": {
                        "kind": "legacy_exact_request_cache",
                        "source_path": str(legacy_path),
                        "source_sha256": sha256_file(legacy_path),
                        "legacy_requested_dimensions": requested_dimensions,
                        "verified_returned_dimensions": len(converted),
                    },
                },
            )
            self.stats["legacy_cache_hits"] += 1
            return converted
        return None

    def snapshot(self) -> dict[str, Any]:
        return json.loads(json.dumps(self.stats))

    def _record_usage(self, usage: Any) -> None:
        if not isinstance(usage, dict):
            return
        aggregate = self.stats["provider_usage"]
        for key, value in usage.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                aggregate[key] = aggregate.get(key, 0) + value

    def embed_many(
        self,
        texts: list[str],
        *,
        batch_size: int,
        progress_label: str,
        allow_api: bool = True,
    ) -> dict[str, list[float]]:
        unique_texts = list(dict.fromkeys(texts))
        self.stats["requested_unique_texts"] += len(unique_texts)
        vectors: dict[str, list[float]] = {}
        missing: list[tuple[str, Path]] = []
        for text in unique_texts:
            token_count = audit_token_count(text)
            self.stats["maximum_audit_tokens"] = max(
                self.stats["maximum_audit_tokens"],
                token_count,
            )
            if token_count > self.max_audit_tokens:
                raise ValueError(
                    f"{progress_label}: audit length {token_count} exceeds the "
                    f"no-truncation guard {self.max_audit_tokens}"
                )
            path = self.cache_path(text)
            if path.exists():
                vectors[text] = self.load_current_cache(text, path)
                self.stats["cache_hits"] += 1
            else:
                legacy_vector = self._load_legacy_exact_cache(text, path)
                if legacy_vector is not None:
                    vectors[text] = legacy_vector
                else:
                    missing.append((text, path))
                    self.stats["cache_misses"] += 1

        if missing and not allow_api:
            raise RuntimeError(
                f"{progress_label}: {len(missing)} exact texts are absent from "
                "both current and legacy caches; API access is disabled"
            )
        for start in range(0, len(missing), batch_size):
            batch = missing[start : start + batch_size]
            print(
                f"{progress_label}: embedding {start + 1}-"
                f"{start + len(batch)} of {len(missing)} cache misses",
                flush=True,
            )
            payload = {
                "model": self.model,
                "input": [text for text, _ in batch],
                "dimensions": self.dimensions,
            }
            started = time.perf_counter()
            response = post_json(
                f"{self.base_url}/embeddings",
                self.api_key,
                payload,
                self.timeout_seconds,
            )
            self.stats["api_elapsed_seconds"] += time.perf_counter() - started
            self.stats["api_calls"] += 1
            self._record_usage(response.get("usage"))
            data = sorted(
                response.get("data", []),
                key=lambda row: row.get("index", 0),
            )
            if len(data) != len(batch):
                raise RuntimeError(
                    f"{progress_label}: expected {len(batch)} embeddings, "
                    f"received {len(data)}"
                )
            for (text, path), item in zip(batch, data, strict=True):
                embedding = item.get("embedding")
                if not isinstance(embedding, list):
                    raise RuntimeError(
                        f"{progress_label}: embedding response has no vector"
                    )
                if len(embedding) != self.dimensions:
                    raise RuntimeError(
                        f"{progress_label}: vector dimension {len(embedding)} "
                        f"!= {self.dimensions}"
                    )
                vector = [float(value) for value in embedding]
                cache_payload = {
                    "schema_version": "rq2a-embedding-cache-v1",
                    "provider": self.provider,
                    "base_url": self.base_url,
                    "model": self.model,
                    "dimensions": self.dimensions,
                    "text_sha256": sha256_text(text),
                    "audit_token_count": audit_token_count(text),
                    "embedding": vector,
                    "provenance": {
                        "kind": "direct_provider_response",
                    },
                }
                if path.exists():
                    persisted = self.load_current_cache(text, path)
                    if persisted != vector:
                        raise RuntimeError(
                            f"{progress_label}: persisted guard vector differs "
                            f"from the returned response for {path}"
                        )
                else:
                    write_json_atomic(path, cache_payload)
                vectors[text] = vector
        if len(vectors) != len(unique_texts):
            raise RuntimeError(
                f"{progress_label}: embedded {len(vectors)} of {len(unique_texts)} texts"
            )
        return vectors


class SkillRouterCrossEncoder:
    """Batched direct scoring with the released SkillRouter reranker."""

    def __init__(
        self,
        *,
        model_id: str,
        revision: str,
        cache_dir: Path,
        max_length: int,
        device: str,
        token: str | None,
        local_files_only: bool,
    ) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "SkillRouter cross-encoder requires torch and transformers. "
                "Run this adapter in the prepared Hugging Face GPU environment "
                "or install the declared model runtime first."
            ) from exc

        self.torch = torch
        self.model_id = model_id
        self.revision = revision
        self.max_length = max_length
        self.device = self._resolve_device(device)
        self.cache_dir = (
            cache_dir
            / "cross_encoder"
            / slug(model_id)
            / slug(revision)
            / SKILLROUTER_PROMPT_VERSION
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.stats: dict[str, Any] = {
            "cache_hits": 0,
            "cache_misses": 0,
            "scored_pairs": 0,
            "model_elapsed_seconds": 0.0,
            "maximum_model_tokens": 0,
            "minimum_model_tokens": None,
            "truncated_pairs": 0,
        }
        print(
            f"Loading {model_id}@{revision} on {self.device}...",
            flush=True,
        )
        model_source: str | Path = model_id
        if local_files_only:
            hub_root = Path(
                os.environ.get(
                    "HF_HOME",
                    str(Path.home() / ".cache" / "huggingface"),
                )
            ) / "hub"
            repository_dir = (
                "models--"
                + model_id.replace("/", "--")
            )
            snapshot_path = hub_root / repository_dir / "snapshots" / revision
            if not snapshot_path.is_dir():
                raise FileNotFoundError(
                    f"Pinned local SkillRouter snapshot is missing: {snapshot_path}"
                )
            model_source = snapshot_path
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_source,
            padding_side="left",
            token=token,
            local_files_only=local_files_only,
        )
        dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            model_source,
            dtype=dtype,
            token=token,
            local_files_only=local_files_only,
        ).eval()
        self.model.to(self.device)
        yes_tokens = self.tokenizer.encode("yes", add_special_tokens=False)
        no_tokens = self.tokenizer.encode("no", add_special_tokens=False)
        if len(yes_tokens) != 1 or len(no_tokens) != 1:
            raise RuntimeError(
                f"Expected single yes/no tokens, got {yes_tokens} and {no_tokens}"
            )
        self.token_yes = yes_tokens[0]
        self.token_no = no_tokens[0]
        self.pad_token_id = (
            self.tokenizer.pad_token_id
            if self.tokenizer.pad_token_id is not None
            else self.tokenizer.eos_token_id
        )
        if self.pad_token_id is None:
            raise RuntimeError("SkillRouter tokenizer has no pad or EOS token")
        print("SkillRouter cross-encoder loaded.", flush=True)

    def _resolve_device(self, requested: str) -> str:
        if requested != "auto":
            return requested
        if self.torch.cuda.is_available():
            return "cuda"
        if (
            getattr(self.torch.backends, "mps", None)
            and self.torch.backends.mps.is_available()
        ):
            return "mps"
        return "cpu"

    def config(self) -> dict[str, Any]:
        return {
            "model": self.model_id,
            "revision": self.revision,
            "prompt_version": SKILLROUTER_PROMPT_VERSION,
            "maximum_input_tokens": self.max_length,
            "truncation": False,
            "score": "yes_logit_minus_no_logit",
            "device": self.device,
            "candidate_generation": "none_direct_three_candidate_scoring",
        }

    @staticmethod
    def format_prompt(query: str, document: str) -> str:
        instruction = (
            "Given a task description, judge whether the skill document "
            "is relevant and useful for completing the task"
        )
        return (
            f"<Instruct>: {instruction}\n\n"
            f"<Query>: {query}\n\n"
            f"<Document>: {document}"
        )

    def build_input_ids(self, query: str, document: str) -> list[int]:
        prefix = (
            "<|im_start|>system\nJudge whether the Document meets the requirements "
            'based on the Query and the Instruct provided. Note that the answer can '
            'only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
        )
        suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        prompt = self.format_prompt(query, document)
        input_ids = (
            self.tokenizer.encode(prefix, add_special_tokens=False)
            + self.tokenizer.encode(prompt, add_special_tokens=False)
            + self.tokenizer.encode(suffix, add_special_tokens=False)
        )
        token_count = len(input_ids)
        self.stats["maximum_model_tokens"] = max(
            self.stats["maximum_model_tokens"],
            token_count,
        )
        minimum = self.stats["minimum_model_tokens"]
        self.stats["minimum_model_tokens"] = (
            token_count if minimum is None else min(minimum, token_count)
        )
        if token_count > self.max_length:
            raise ValueError(
                f"SkillRouter pair needs {token_count} tokens, exceeding "
                f"the no-truncation limit {self.max_length}"
            )
        return input_ids

    def cache_path(self, query: str, document: str) -> Path:
        key = sha256_json(
            {
                **self.config(),
                "query": query,
                "document": document,
            }
        )
        return self.cache_dir / f"{key}.json"

    def score_pairs(
        self,
        pairs: list[tuple[str, str]],
        *,
        batch_size: int,
    ) -> dict[tuple[str, str], float]:
        unique_pairs = list(dict.fromkeys(pairs))
        scores: dict[tuple[str, str], float] = {}
        missing: list[tuple[tuple[str, str], Path, list[int]]] = []
        for pair in unique_pairs:
            path = self.cache_path(*pair)
            if path.exists():
                payload = json.loads(path.read_text(encoding="utf-8"))
                scores[pair] = float(payload["score"])
                self.stats["cache_hits"] += 1
                token_count = int(payload["model_token_count"])
                self.stats["maximum_model_tokens"] = max(
                    self.stats["maximum_model_tokens"],
                    token_count,
                )
                minimum = self.stats["minimum_model_tokens"]
                self.stats["minimum_model_tokens"] = (
                    token_count if minimum is None else min(minimum, token_count)
                )
            else:
                input_ids = self.build_input_ids(*pair)
                missing.append((pair, path, input_ids))
                self.stats["cache_misses"] += 1

        for start in range(0, len(missing), batch_size):
            batch = missing[start : start + batch_size]
            print(
                f"SkillRouter: scoring {start + 1}-{start + len(batch)} "
                f"of {len(missing)} cache misses",
                flush=True,
            )
            maximum_length = max(len(input_ids) for _, _, input_ids in batch)
            input_tensor = self.torch.full(
                (len(batch), maximum_length),
                self.pad_token_id,
                dtype=self.torch.long,
                device=self.device,
            )
            attention_mask = self.torch.zeros_like(input_tensor)
            for row_index, (_, _, input_ids) in enumerate(batch):
                length = len(input_ids)
                input_tensor[row_index, -length:] = self.torch.tensor(
                    input_ids,
                    dtype=self.torch.long,
                    device=self.device,
                )
                attention_mask[row_index, -length:] = 1
            started = time.perf_counter()
            with self.torch.no_grad():
                logits = self.model(
                    input_ids=input_tensor,
                    attention_mask=attention_mask,
                ).logits[:, -1, :]
            batch_scores = (
                logits[:, self.token_yes] - logits[:, self.token_no]
            ).detach().float().cpu().tolist()
            self.stats["model_elapsed_seconds"] += time.perf_counter() - started
            for (pair, path, input_ids), score in zip(
                batch,
                batch_scores,
                strict=True,
            ):
                score = float(score)
                write_json_atomic(
                    path,
                    {
                        "schema_version": "rq2a-cross-encoder-cache-v1",
                        **self.config(),
                        "query_sha256": sha256_text(pair[0]),
                        "document_sha256": sha256_text(pair[1]),
                        "model_token_count": len(input_ids),
                        "score": score,
                    },
                )
                scores[pair] = score
                self.stats["scored_pairs"] += 1
        if len(scores) != len(unique_pairs):
            raise RuntimeError(
                f"SkillRouter scored {len(scores)} of {len(unique_pairs)} pairs"
            )
        return scores


def stats_delta(after: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in after.items():
        if isinstance(value, dict):
            result[key] = stats_delta(value, before.get(key, {}))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            result[key] = value - before.get(key, 0)
        else:
            result[key] = value
    return result


def selector_configuration(args: argparse.Namespace, selector: str) -> dict[str, Any]:
    if selector == "bm25":
        return {
            "selector": selector,
            "tokenizer": "[a-z0-9]+ lowercased",
            "k1": args.bm25_k1,
            "b": args.bm25_b,
            "corpus": "three_sibling_candidates_per_decision",
            "epsilon": EPSILON,
        }
    if selector == "qwen-single-vector":
        return {
            "selector": selector,
            "provider": "qwen",
            "base_url": args.qwen_base_url,
            "model": args.qwen_model,
            "dimensions": args.qwen_dimensions,
            "score": "cosine",
            "truncation": False,
            "maximum_audit_tokens": args.max_audit_tokens,
            "epsilon": EPSILON,
        }
    if selector == "skillrouter-cross-encoder":
        return {
            "selector": selector,
            "model": args.skillrouter_model,
            "revision": args.skillrouter_revision,
            "prompt_version": SKILLROUTER_PROMPT_VERSION,
            "score": "yes_logit_minus_no_logit",
            "maximum_input_tokens": args.skillrouter_max_length,
            "truncation": False,
            "candidate_generation": "none_direct_three_candidate_scoring",
            "epsilon": EPSILON,
        }
    raise ValueError(f"Unknown selector: {selector}")


def confirmatory_invocation(args: argparse.Namespace) -> dict[str, Any]:
    """Return the exact safety-relevant invocation bound by a controller grant."""
    freeze_sha256 = (
        sha256_file(args.confirmatory_freeze_manifest)
        if args.confirmatory_freeze_manifest is not None
        and args.confirmatory_freeze_manifest.is_file()
        else None
    )
    return {
        "entry_point": "run_rq2a_fixed_candidate_matrix.py",
        "split": args.split,
        "output_dir": str(args.output_dir.resolve()),
        "run_id": args.run_id,
        "evidence_role": args.evidence_role,
        "selectors": list(args.selectors),
        "representations": list(args.representations),
        "clusters_per_field": args.clusters_per_field,
        "overwrite": bool(args.overwrite),
        "confirmatory_freeze_sha256": freeze_sha256,
        "bm25_k1": args.bm25_k1,
        "bm25_b": args.bm25_b,
        "qwen_base_url": args.qwen_base_url,
        "qwen_model": args.qwen_model,
        "qwen_dimensions": args.qwen_dimensions,
        "qwen_batch_size": args.qwen_batch_size,
        "max_audit_tokens": args.max_audit_tokens,
        "skillrouter_model": args.skillrouter_model,
        "skillrouter_revision": args.skillrouter_revision,
        "skillrouter_max_length": args.skillrouter_max_length,
        "skillrouter_batch_size": args.skillrouter_batch_size,
        "skillrouter_local_files_only": bool(
            args.skillrouter_local_files_only
        ),
    }


def score_bm25(
    *,
    run_id: str,
    prompts: list[dict[str, Any]],
    indexes: dict[str, dict[tuple[str, str], dict[str, Any]]],
    representations: list[str],
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for representation in representations:
        index = indexes[representation]
        for prompt in prompts:
            documents, candidate_rows = representation_documents(prompt, index)
            score_started = time.perf_counter()
            scores = bm25_scores(
                prompt["query_text"],
                documents,
                k1=config["k1"],
                b=config["b"],
            )
            rows.append(
                build_result_row(
                    run_id=run_id,
                    selector="bm25",
                    selector_config=config,
                    representation=representation,
                    prompt=prompt,
                    candidate_rows=candidate_rows,
                    scores=scores,
                    score_latency_seconds=time.perf_counter() - score_started,
                )
            )
    return rows, {"wall_seconds": time.perf_counter() - started}


def score_qwen(
    *,
    run_id: str,
    prompts: list[dict[str, Any]],
    indexes: dict[str, dict[tuple[str, str], dict[str, Any]]],
    representations: list[str],
    config: dict[str, Any],
    client: RQ2aEmbeddingClient,
    batch_size: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    documents = sorted(
        {
            row["selector_visible_text"]
            for representation in representations
            for row in indexes[representation].values()
        }
    )
    queries = sorted({prompt["query_text"] for prompt in prompts})
    before_documents = client.snapshot()
    document_started = time.perf_counter()
    document_vectors = client.embed_many(
        documents,
        batch_size=batch_size,
        progress_label="RQ2a documents",
    )
    document_wall = time.perf_counter() - document_started
    after_documents = client.snapshot()
    query_started = time.perf_counter()
    query_vectors = client.embed_many(
        queries,
        batch_size=batch_size,
        progress_label="RQ2a queries",
    )
    query_wall = time.perf_counter() - query_started
    after_queries = client.snapshot()

    rows: list[dict[str, Any]] = []
    score_total_started = time.perf_counter()
    for representation in representations:
        index = indexes[representation]
        for prompt in prompts:
            candidate_documents, candidate_rows = representation_documents(
                prompt,
                index,
            )
            score_started = time.perf_counter()
            query_vector = query_vectors[prompt["query_text"]]
            scores = [
                cosine(query_vector, document_vectors[document])
                for document in candidate_documents
            ]
            rows.append(
                build_result_row(
                    run_id=run_id,
                    selector="qwen-single-vector",
                    selector_config=config,
                    representation=representation,
                    prompt=prompt,
                    candidate_rows=candidate_rows,
                    scores=scores,
                    score_latency_seconds=time.perf_counter() - score_started,
                )
            )
    return rows, {
        "document_prepare_wall_seconds": document_wall,
        "query_prepare_wall_seconds": query_wall,
        "score_wall_seconds": time.perf_counter() - score_total_started,
        "document_embedding_stats": stats_delta(
            after_documents,
            before_documents,
        ),
        "query_embedding_stats": stats_delta(after_queries, after_documents),
        "cumulative_embedding_stats": after_queries,
    }


def score_skillrouter(
    *,
    run_id: str,
    prompts: list[dict[str, Any]],
    indexes: dict[str, dict[tuple[str, str], dict[str, Any]]],
    representations: list[str],
    config: dict[str, Any],
    cross_encoder: SkillRouterCrossEncoder,
    batch_size: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pairs: list[tuple[str, str]] = []
    for representation in representations:
        index = indexes[representation]
        for prompt in prompts:
            documents, _ = representation_documents(prompt, index)
            pairs.extend((prompt["query_text"], document) for document in documents)
    prepare_started = time.perf_counter()
    pair_scores = cross_encoder.score_pairs(pairs, batch_size=batch_size)
    pair_wall = time.perf_counter() - prepare_started

    rows: list[dict[str, Any]] = []
    scoring_started = time.perf_counter()
    for representation in representations:
        index = indexes[representation]
        for prompt in prompts:
            documents, candidate_rows = representation_documents(prompt, index)
            score_started = time.perf_counter()
            scores = [
                pair_scores[(prompt["query_text"], document)]
                for document in documents
            ]
            rows.append(
                build_result_row(
                    run_id=run_id,
                    selector="skillrouter-cross-encoder",
                    selector_config=config,
                    representation=representation,
                    prompt=prompt,
                    candidate_rows=candidate_rows,
                    scores=scores,
                    score_latency_seconds=time.perf_counter() - score_started,
                )
            )
    return rows, {
        "pair_prepare_and_model_wall_seconds": pair_wall,
        "score_lookup_wall_seconds": time.perf_counter() - scoring_started,
        **cross_encoder.stats,
    }


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=root / "rq2a_matched_content",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "development",
    )
    parser.add_argument("--split", choices=["development", "confirmatory"], default="development")
    parser.add_argument(
        "--representations",
        nargs="+",
        default=CORE_REPRESENTATIONS,
    )
    parser.add_argument(
        "--selectors",
        nargs="+",
        choices=SELECTORS,
        default=["bm25"],
    )
    parser.add_argument("--clusters-per-field", type=int)
    parser.add_argument("--run-id")
    parser.add_argument(
        "--evidence-role",
        choices=["primary", "verification"],
        default="primary",
        help=(
            "Whether this run supplies one canonical development condition "
            "or only verifies reproducibility/cache behaviour."
        ),
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--confirmatory-freeze-manifest",
        type=Path,
        help="Required for confirmatory scoring; created only after development freeze.",
    )
    parser.add_argument(
        "--confirmatory-controller-grant",
        type=Path,
        help="Required exact-invocation grant for every confirmatory run.",
    )
    parser.add_argument("--bm25-k1", type=float, default=1.5)
    parser.add_argument("--bm25-b", type=float, default=0.75)
    parser.add_argument("--dotenv", type=Path, default=root.parent / ".env")
    parser.add_argument("--cache-dir", type=Path, default=root / "cache" / "rq2a")
    parser.add_argument(
        "--legacy-cache-dir",
        type=Path,
        default=root / "runtime" / "provider_cache",
        help="Read-only exact-key fallback for earlier provider embeddings.",
    )
    parser.add_argument("--qwen-base-url", default=QWEN_BASE_URL)
    parser.add_argument("--qwen-api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--qwen-model", default=QWEN_MODEL)
    parser.add_argument("--qwen-dimensions", type=int, default=QWEN_DIMENSIONS)
    parser.add_argument("--qwen-batch-size", type=int, default=10)
    parser.add_argument("--qwen-timeout-seconds", type=int, default=180)
    parser.add_argument("--max-audit-tokens", type=int, default=8192)
    parser.add_argument("--skillrouter-model", default=SKILLROUTER_MODEL)
    parser.add_argument("--skillrouter-revision", default=SKILLROUTER_REVISION)
    parser.add_argument("--skillrouter-max-length", type=int, default=2048)
    parser.add_argument("--skillrouter-batch-size", type=int, default=4)
    parser.add_argument("--skillrouter-device", default="auto")
    parser.add_argument("--skillrouter-local-files-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    self_test()
    if args.self_test:
        print("RQ2a selector common self-test: PASS")
        return
    confirmatory_freeze: dict[str, Any] | None = None
    confirmatory_grant: dict[str, Any] | None = None
    if args.split == "confirmatory":
        freeze = args.confirmatory_freeze_manifest
        if freeze is None or not freeze.exists():
            raise ValueError(
                "Confirmatory scoring is blocked until a development freeze "
                "manifest is supplied."
            )
        confirmatory_freeze = validate_confirmatory_freeze_manifest(
            freeze,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
        )
        confirmatory_grant = validate_confirmatory_execution_grant(
            args.confirmatory_controller_grant,
            action="fixed_scoring",
            invocation=confirmatory_invocation(args),
        )
        if "qwen-single-vector" in args.selectors:
            expected_guard = sha256_file(args.confirmatory_controller_grant)
            if (
                getattr(
                    post_json,
                    "_rq2a_confirmatory_grant_sha256",
                    None,
                )
                != expected_guard
            ):
                raise ValueError(
                    "Confirmatory Qwen scoring requires the controller-installed "
                    "guarded transport"
                )

    load_dotenv(args.dotenv)
    run_id = args.run_id or (
        f"rq2a-{args.split}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    )
    run_dir = args.output_dir / run_id
    if run_dir.exists() and any(run_dir.iterdir()) and not args.overwrite:
        raise FileExistsError(
            f"Run directory already contains artifacts: {run_dir}. "
            "Use a new --run-id; confirmatory outputs must never be overwritten."
        )
    run_dir.mkdir(parents=True, exist_ok=True)

    started_utc = utc_timestamp()
    wall_started = time.perf_counter()
    protocol, prompts, indexes = load_run_data(
        args.input_dir,
        args.split,
        args.representations,
        args.clusters_per_field,
    )
    selector_configs = {
        selector: selector_configuration(args, selector)
        for selector in args.selectors
    }
    all_rows: list[dict[str, Any]] = []
    runtime: dict[str, Any] = {}

    if "bm25" in args.selectors:
        rows, selector_runtime = score_bm25(
            run_id=run_id,
            prompts=prompts,
            indexes=indexes,
            representations=args.representations,
            config=selector_configs["bm25"],
        )
        all_rows.extend(rows)
        runtime["bm25"] = selector_runtime

    if "qwen-single-vector" in args.selectors:
        api_key = os.environ.get(args.qwen_api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Qwen selector requires environment variable {args.qwen_api_key_env}"
            )
        client = RQ2aEmbeddingClient(
            provider="qwen",
            base_url=args.qwen_base_url,
            api_key=api_key,
            model=args.qwen_model,
            dimensions=args.qwen_dimensions,
            cache_dir=args.cache_dir,
            timeout_seconds=args.qwen_timeout_seconds,
            max_audit_tokens=args.max_audit_tokens,
            legacy_cache_dir=args.legacy_cache_dir,
        )
        rows, selector_runtime = score_qwen(
            run_id=run_id,
            prompts=prompts,
            indexes=indexes,
            representations=args.representations,
            config=selector_configs["qwen-single-vector"],
            client=client,
            batch_size=args.qwen_batch_size,
        )
        all_rows.extend(rows)
        runtime["qwen-single-vector"] = selector_runtime

    if "skillrouter-cross-encoder" in args.selectors:
        cross_encoder = SkillRouterCrossEncoder(
            model_id=args.skillrouter_model,
            revision=args.skillrouter_revision,
            cache_dir=args.cache_dir,
            max_length=args.skillrouter_max_length,
            device=args.skillrouter_device,
            token=os.environ.get("HF_TOKEN"),
            local_files_only=args.skillrouter_local_files_only,
        )
        selector_configs["skillrouter-cross-encoder"] = {
            **selector_configs["skillrouter-cross-encoder"],
            "resolved_device": cross_encoder.device,
        }
        rows, selector_runtime = score_skillrouter(
            run_id=run_id,
            prompts=prompts,
            indexes=indexes,
            representations=args.representations,
            config=selector_configs["skillrouter-cross-encoder"],
            cross_encoder=cross_encoder,
            batch_size=args.skillrouter_batch_size,
        )
        all_rows.extend(rows)
        runtime["skillrouter-cross-encoder"] = selector_runtime

    all_rows.sort(
        key=lambda row: (
            row["selector"],
            row["representation"],
            row["prompt_id"],
        )
    )
    expected_rows = (
        len(prompts) * len(args.representations) * len(args.selectors)
    )
    if len(all_rows) != expected_rows:
        raise RuntimeError(
            f"Result row count {len(all_rows)} != expected {expected_rows}"
        )
    identity_keys = {
        (row["selector"], row["representation"], row["prompt_id"])
        for row in all_rows
    }
    if len(identity_keys) != expected_rows:
        raise RuntimeError("Duplicate selector/representation/prompt result identity")

    rows_path = run_dir / "rows.jsonl"
    write_jsonl_atomic(rows_path, all_rows)
    summary = summarise_result_rows(all_rows)
    manifest = {
        "schema_version": RUN_MANIFEST_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "run_id": run_id,
        "state": "complete",
        "started_utc": started_utc,
        "finished_utc": utc_timestamp(),
        "split": args.split,
        "clusters_per_field": args.clusters_per_field,
        "evidence_role": args.evidence_role,
        "prompt_count": len(prompts),
        "cluster_count": len({prompt["cluster_id"] for prompt in prompts}),
        "representations": list(args.representations),
        "selectors": list(args.selectors),
        "selector_configurations": selector_configs,
        "input_artifacts": {
            "protocol_json": {
                "path": str(args.input_dir / "protocol.json"),
                "sha256": sha256_file(args.input_dir / "protocol.json"),
            },
            "prompts_jsonl": {
                "path": str(args.input_dir / "prompts.jsonl"),
                "sha256": sha256_file(args.input_dir / "prompts.jsonl"),
            },
            "representations": {
                representation: {
                    "path": str(
                        args.input_dir
                        / "representations"
                        / f"{representation}.jsonl"
                    ),
                    "sha256": sha256_file(
                        args.input_dir
                        / "representations"
                        / f"{representation}.jsonl"
                    ),
                }
                for representation in args.representations
            },
            **(
                {
                    "confirmatory_freeze_manifest": {
                        "path": str(args.confirmatory_freeze_manifest),
                        "sha256": sha256_file(
                            args.confirmatory_freeze_manifest
                        ),
                        "state": confirmatory_freeze["state"],
                    }
                }
                if confirmatory_freeze is not None
                else {}
            ),
            **(
                {
                    "confirmatory_controller_grant": {
                        "path": str(args.confirmatory_controller_grant),
                        "sha256": sha256_file(
                            args.confirmatory_controller_grant
                        ),
                        "action": confirmatory_grant["action"],
                        "invocation_sha256": confirmatory_grant[
                            "invocation_sha256"
                        ],
                    }
                }
                if confirmatory_grant is not None
                else {}
            ),
        },
        "output_artifacts": {
            "rows_jsonl": {
                "path": str(rows_path),
                "row_count": len(all_rows),
                "sha256": sha256_file(rows_path),
            }
        },
        "runtime": {
            **runtime,
            "total_wall_seconds": time.perf_counter() - wall_started,
        },
        "quality_checks": {
            "common_self_test": "pass",
            "row_count_expected": expected_rows,
            "row_count_actual": len(all_rows),
            "unique_result_identities": len(identity_keys),
            "candidate_alignment": "pass",
            "finite_scores": "pass",
            "no_thesis_write": bool(
                protocol["thesis_write_blocked_pending_user_review"]
            ),
        },
    }
    write_json_atomic(run_dir / "summary.json", summary)
    write_json_atomic(run_dir / "manifest.json", manifest)
    (run_dir / "summary.md").write_text(
        render_summary_markdown(summary, manifest),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "run_id": run_id,
                "run_dir": str(run_dir),
                "prompt_count": len(prompts),
                "cluster_count": manifest["cluster_count"],
                "row_count": len(all_rows),
                "conditions": summary["conditions"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
