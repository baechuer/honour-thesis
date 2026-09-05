#!/usr/bin/env python3
"""Run the local, outcome-blind B0G candidate-discovery union.

This controller is deliberately separate from every primary RQ2b retriever.
It reads the frozen I2 sources and scored prompts only inside this process,
persists numeric embeddings locally, and emits an internal candidate manifest
containing identifiers, hashes, channel evidence, and scores only. It never
prints or writes raw benchmark text, gold labels, family labels, or retrieval
outcomes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np


SCRIPT_SCHEMA = "rq2b-b0g-candidate-discovery-v1"
SCORED_STRATA = frozenset({"controlled", "public_gold"})
SENTINEL_SEED = "2026080803"
TOP_K = 10


@dataclass(frozen=True)
class ChannelSpec:
    name: str
    revision: str
    raw_window_tokens: int
    overlap_tokens: int
    maximum_input_tokens: int
    document_prefix: str
    query_prefix: str
    pooling: str
    batch_token_budget: int
    maximum_batch_items: int


CHANNELS = (
    ChannelSpec(
        name="D1",
        revision="5617a9f61b028005a4858fdac845db406aefb181",
        raw_window_tokens=7500,
        overlap_tokens=256,
        maximum_input_tokens=8194,
        document_prefix="",
        query_prefix="",
        pooling="cls_l2",
        batch_token_budget=9000,
        maximum_batch_items=2,
    ),
    ChannelSpec(
        name="D2",
        revision="f169b11e22de13617baa190a028a32f3493550b6",
        raw_window_tokens=480,
        overlap_tokens=64,
        maximum_input_tokens=512,
        document_prefix="passage: ",
        query_prefix="query: ",
        pooling="masked_mean_l2",
        batch_token_budget=1920,
        maximum_batch_items=4,
    ),
)


@dataclass(frozen=True)
class SourceRecord:
    skill_id: str
    source_sha256: str
    source_path: str
    source_chars: int
    text: str


@dataclass(frozen=True)
class PromptRecord:
    prompt_id: str
    prompt_sha256: str
    text: str


@dataclass(frozen=True)
class ChunkRecord:
    descriptor_sha256: str
    skill_id: str
    source_sha256: str
    chunk_index: int
    start_char: int
    end_char: int
    token_start: int
    token_end: int
    raw_token_count: int
    text_sha256: str
    text: str

    def public_dict(self) -> dict[str, Any]:
        return {
            "chunk_index": self.chunk_index,
            "descriptor_sha256": self.descriptor_sha256,
            "end_char": self.end_char,
            "raw_token_count": self.raw_token_count,
            "skill_id": self.skill_id,
            "source_sha256": self.source_sha256,
            "start_char": self.start_char,
            "text_sha256": self.text_sha256,
            "token_end": self.token_end,
            "token_start": self.token_start,
        }


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value))


def decode_frozen_source(source_bytes: bytes) -> str:
    """Decode UTF-8 source bytes into the manifest's newline-normalised text."""
    return source_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"invalid JSONL at {path}:{line_number}") from error
            require(isinstance(row, dict), f"expected object at {path}:{line_number}")
            rows.append(row)
    return rows


def atomic_write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_json_new(path: Path, value: Any) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite frozen output: {path}")
    atomic_write_bytes(path, json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite frozen output: {path}")
    materialised = list(rows)
    payload = b"".join(canonical_json(row) + b"\n" for row in materialised)
    atomic_write_bytes(path, payload)
    return len(materialised)


def write_progress(path: Path, value: dict[str, Any]) -> None:
    atomic_write_bytes(path, json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def load_sources(source_manifest: Path, workspace_root: Path) -> list[SourceRecord]:
    records: list[SourceRecord] = []
    identifiers: set[str] = set()
    for row in read_jsonl(source_manifest):
        skill_id = row["skill_id"]
        require(isinstance(skill_id, str) and skill_id and skill_id not in identifiers, "invalid or duplicate skill_id")
        identifiers.add(skill_id)
        source_path = row["source_path"]
        require(isinstance(source_path, str) and source_path, f"missing source path for {skill_id}")
        disk_path = workspace_root / source_path
        # The frozen manifest binds original UTF-8 bytes. Path.read_text() uses
        # universal-newline conversion, which would falsely report drift for a
        # valid CRLF source before any model sees it.
        source_bytes = disk_path.read_bytes()
        require(sha256_bytes(source_bytes) == row["source_sha256"], f"source hash drift for {skill_id}")
        text = decode_frozen_source(source_bytes)
        require(len(text) == row["source_chars"], f"source character count drift for {skill_id}")
        records.append(
            SourceRecord(
                skill_id=skill_id,
                source_sha256=row["source_sha256"],
                source_path=source_path,
                source_chars=row["source_chars"],
                text=text,
            )
        )
    records.sort(key=lambda record: record.skill_id)
    require(len(records) == 2433, f"expected 2,433 frozen skills, found {len(records)}")
    return records


def load_prompts(prompt_manifest: Path) -> list[PromptRecord]:
    records: list[PromptRecord] = []
    identifiers: set[str] = set()
    for row in read_jsonl(prompt_manifest):
        if row.get("stratum") not in SCORED_STRATA:
            continue
        prompt_id = row["prompt_id"]
        text = row["prompt"]
        require(isinstance(prompt_id, str) and prompt_id and prompt_id not in identifiers, "invalid or duplicate prompt_id")
        require(isinstance(text, str) and text, f"empty prompt text for {prompt_id}")
        require(sha256_text(text) == row["prompt_sha256"], f"prompt hash drift for {prompt_id}")
        identifiers.add(prompt_id)
        records.append(PromptRecord(prompt_id=prompt_id, prompt_sha256=row["prompt_sha256"], text=text))
    records.sort(key=lambda record: record.prompt_id)
    require(len(records) == 389, f"expected 389 scored prompts, found {len(records)}")
    return records


def known_prompt_ids(prompt_manifest: Path) -> set[str]:
    identifiers = {row["prompt_id"] for row in read_jsonl(prompt_manifest)}
    require(len(identifiers) == 401, f"expected 401 frozen prompts, found {len(identifiers)}")
    return identifiers


def load_seed_pool(
    seed_pool: Path,
    scored_prompt_ids: set[str],
    all_prompt_ids: set[str],
    skill_ids: set[str],
) -> tuple[dict[str, set[str]], dict[str, int]]:
    grouped = {prompt_id: set() for prompt_id in scored_prompt_ids}
    rows = read_jsonl(seed_pool)
    excluded_stress_rows = 0
    for row in rows:
        prompt_id = row["prompt_id"]
        candidate_skill_id = row["candidate_skill_id"]
        require(prompt_id in all_prompt_ids, "seed pool includes an unknown prompt")
        require(candidate_skill_id in skill_ids, "seed pool includes an unknown skill")
        if prompt_id not in grouped:
            excluded_stress_rows += 1
            continue
        grouped[prompt_id].add(candidate_skill_id)
    included_rows = len(rows) - excluded_stress_rows
    require(len(rows) == 1914, f"expected 1,914 B0G-M v3 seed rows, found {len(rows)}")
    require(included_rows == 1862, f"expected 1,862 scored seed rows, found {included_rows}")
    require(excluded_stress_rows == 52, f"expected 52 descriptive stress rows, found {excluded_stress_rows}")
    return grouped, {
        "all_seed_rows": len(rows),
        "excluded_descriptive_stress_rows": excluded_stress_rows,
        "included_scored_seed_rows": included_rows,
    }


def token_windows(tokenizer: Any, text: str, window: int, overlap: int) -> list[tuple[int, int, int, int, int, int, str]]:
    """Return lossless character/token windows without retaining offsets externally."""
    require(window > 0 and 0 <= overlap < window, "invalid chunk configuration")
    # Planning may intentionally inspect text longer than the model context; no
    # forward pass occurs here, and each emitted window is checked before use.
    encoded = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True, verbose=False)
    token_ids = list(encoded["input_ids"])
    offsets = [tuple(map(int, pair)) for pair in encoded["offset_mapping"]]
    require(len(token_ids) == len(offsets), "tokenizer offsets do not align with token IDs")
    if not token_ids:
        require(bool(text), "empty source text is not permitted")
        return [(0, 0, 0, len(text), 0, 0, sha256_text(text))]

    records: list[tuple[int, int, int, int, int, int, str]] = []
    start = 0
    while start < len(token_ids):
        end = min(start + window, len(token_ids))
        start_char = 0 if start == 0 else offsets[start][0]
        end_char = len(text) if end == len(token_ids) else offsets[end][0]
        require(0 <= start_char < end_char <= len(text), "invalid token-derived character coverage")
        chunk_text = text[start_char:end_char]
        records.append((start, end, start_char, end_char, end - start, len(records), sha256_text(chunk_text)))
        if end == len(token_ids):
            break
        start = end - overlap
    require(records[0][2] == 0 and records[-1][3] == len(text), "token windows are not lossless")
    previous_end = 0
    for _, _, start_char, end_char, _, _, _ in records:
        require(start_char <= previous_end, "token windows have a character gap")
        previous_end = max(previous_end, end_char)
    return records


def build_chunks(tokenizer: Any, sources: list[SourceRecord], channel: ChannelSpec) -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    for source_index, source in enumerate(sources, start=1):
        for token_start, token_end, start_char, end_char, token_count, chunk_index, text_hash in token_windows(
            tokenizer, source.text, channel.raw_window_tokens, channel.overlap_tokens
        ):
            text = source.text[start_char:end_char]
            descriptor = {
                "channel": channel.name,
                "chunk_index": chunk_index,
                "end_char": end_char,
                "raw_token_count": token_count,
                "skill_id": source.skill_id,
                "source_sha256": source.source_sha256,
                "start_char": start_char,
                "text_sha256": text_hash,
                "token_end": token_end,
                "token_start": token_start,
            }
            chunks.append(
                ChunkRecord(
                    descriptor_sha256=sha256_json(descriptor),
                    skill_id=source.skill_id,
                    source_sha256=source.source_sha256,
                    chunk_index=chunk_index,
                    start_char=start_char,
                    end_char=end_char,
                    token_start=token_start,
                    token_end=token_end,
                    raw_token_count=token_count,
                    text_sha256=text_hash,
                    text=text,
                )
            )
        if source_index % 100 == 0 or source_index == len(sources):
            print(f"{channel.name} chunk plan: {source_index}/{len(sources)} skills, {len(chunks)} chunks", file=sys.stderr, flush=True)
    return chunks


def verify_model_input_bounds(
    tokenizer: Any,
    chunks: list[ChunkRecord],
    prompts: list[PromptRecord],
    channel: ChannelSpec,
) -> dict[str, int]:
    """Check every actual prefixed input before any forward pass is permitted."""
    maximum_document_tokens = 0
    maximum_query_tokens = 0
    for chunk in chunks:
        count = len(
            tokenizer(
                channel.document_prefix + chunk.text,
                add_special_tokens=True,
                truncation=False,
                verbose=False,
            )["input_ids"]
        )
        maximum_document_tokens = max(maximum_document_tokens, count)
        require(count <= channel.maximum_input_tokens, f"{channel.name} document input ceiling exceeded")
    for prompt in prompts:
        count = len(
            tokenizer(
                channel.query_prefix + prompt.text,
                add_special_tokens=True,
                truncation=False,
                verbose=False,
            )["input_ids"]
        )
        maximum_query_tokens = max(maximum_query_tokens, count)
        require(count <= channel.maximum_input_tokens, f"{channel.name} query input ceiling exceeded")
    return {
        "maximum_document_input_tokens": maximum_document_tokens,
        "maximum_query_input_tokens": maximum_query_tokens,
    }


def cache_config(channel: ChannelSpec, source_manifest_sha256: str, script_sha256: str) -> dict[str, Any]:
    return {
        "channel": channel.name,
        "model_revision": channel.revision,
        "pooling": channel.pooling,
        "raw_window_tokens": channel.raw_window_tokens,
        "overlap_tokens": channel.overlap_tokens,
        "maximum_input_tokens": channel.maximum_input_tokens,
        "document_prefix": channel.document_prefix,
        "query_prefix": channel.query_prefix,
        "source_manifest_sha256": source_manifest_sha256,
        "script_sha256": script_sha256,
        "schema": SCRIPT_SCHEMA,
    }


def load_model_and_tokenizer(model_root: Path, channel: ChannelSpec) -> tuple[Any, Any]:
    import torch
    from transformers import AutoModel, AutoTokenizer

    model_path = model_root / channel.name
    require(model_path.is_dir(), f"missing local model directory for {channel.name}")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
    model = AutoModel.from_pretrained(model_path, local_files_only=True, trust_remote_code=False).eval()
    require(not torch.cuda.is_available(), "B0G-CD controller is bound to local CPU only")
    return model, tokenizer


def load_tokenizer(model_root: Path, channel: ChannelSpec) -> Any:
    from transformers import AutoTokenizer

    model_path = model_root / channel.name
    require(model_path.is_dir(), f"missing local model directory for {channel.name}")
    return AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)


def encode_texts(model: Any, tokenizer: Any, texts: list[str], channel: ChannelSpec) -> np.ndarray:
    import torch

    require(texts, "cannot encode an empty batch")
    encoded = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
    input_width = int(encoded["input_ids"].shape[1])
    require(input_width <= channel.maximum_input_tokens, f"{channel.name} batch exceeds input ceiling")
    with torch.no_grad():
        hidden = model(**encoded).last_hidden_state
    if channel.pooling == "cls_l2":
        vectors = hidden[:, 0, :]
    elif channel.pooling == "masked_mean_l2":
        mask = encoded["attention_mask"].unsqueeze(-1).to(hidden.dtype)
        vectors = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1)
    else:
        raise RuntimeError(f"unsupported pooling rule: {channel.pooling}")
    vectors = torch.nn.functional.normalize(vectors, p=2, dim=1)
    result = vectors.detach().cpu().numpy().astype(np.float32, copy=False)
    require(result.ndim == 2 and result.shape[1] == 1024, f"unexpected {channel.name} embedding shape")
    require(bool(np.isfinite(result).all()), f"non-finite {channel.name} embedding")
    return result


def batched_indices(chunks: list[ChunkRecord], channel: ChannelSpec) -> list[list[int]]:
    batches: list[list[int]] = []
    current: list[int] = []
    current_tokens = 0
    for index, chunk in enumerate(chunks):
        estimated_tokens = chunk.raw_token_count + 4
        if current and (
            len(current) >= channel.maximum_batch_items
            or current_tokens + estimated_tokens > channel.batch_token_budget
        ):
            batches.append(current)
            current = []
            current_tokens = 0
        current.append(index)
        current_tokens += estimated_tokens
    if current:
        batches.append(current)
    return batches


def atomic_save_npz(path: Path, **arrays: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            np.savez_compressed(handle, **arrays)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def load_or_embed_chunks(
    model: Any,
    tokenizer: Any,
    chunks: list[ChunkRecord],
    channel: ChannelSpec,
    cache_root: Path,
    run_state: Path,
) -> np.ndarray:
    batches = batched_indices(chunks, channel)
    vectors: list[np.ndarray] = []
    cache_root.mkdir(parents=True, exist_ok=True)
    for batch_index, indexes in enumerate(batches, start=1):
        destination = cache_root / f"batch-{batch_index:05d}.npz"
        expected_descriptors = np.asarray([chunks[index].descriptor_sha256 for index in indexes], dtype="U64")
        if destination.exists():
            with np.load(destination, allow_pickle=False) as cached:
                require(np.array_equal(cached["descriptor_sha256"], expected_descriptors), "cached descriptor mismatch")
                embedded = cached["embeddings"].astype(np.float32, copy=False)
            require(embedded.shape == (len(indexes), 1024), "cached embedding shape mismatch")
            source = "cache"
        else:
            texts = [channel.document_prefix + chunks[index].text for index in indexes]
            embedded = encode_texts(model, tokenizer, texts, channel)
            atomic_save_npz(destination, descriptor_sha256=expected_descriptors, embeddings=embedded)
            source = "computed"
        vectors.append(embedded)
        if batch_index % 25 == 0 or batch_index == len(batches):
            write_progress(
                run_state,
                {
                    "stage": "B0G-CD",
                    "state": "RUNNING",
                    "channel": channel.name,
                    "chunk_batches_complete": batch_index,
                    "chunk_batches_total": len(batches),
                    "chunk_count": len(chunks),
                    "last_batch_source": source,
                    "benchmark_text_emitted": False,
                    "external_requests": 0,
                    "provider_calls": 0,
                    "semantic_review_run": False,
                    "primary_results_consumed": False,
                },
            )
            print(f"{channel.name} embeddings: {batch_index}/{len(batches)} batches ({source})", file=sys.stderr, flush=True)
    return np.vstack(vectors)


def load_or_embed_queries(
    model: Any,
    tokenizer: Any,
    prompts: list[PromptRecord],
    channel: ChannelSpec,
    cache_root: Path,
) -> np.ndarray:
    destination = cache_root / "queries.npz"
    expected_prompt_ids = np.asarray([prompt.prompt_id for prompt in prompts], dtype="U256")
    expected_hashes = np.asarray([prompt.prompt_sha256 for prompt in prompts], dtype="U64")
    if destination.exists():
        with np.load(destination, allow_pickle=False) as cached:
            require(np.array_equal(cached["prompt_id"], expected_prompt_ids), "cached query IDs mismatch")
            require(np.array_equal(cached["prompt_sha256"], expected_hashes), "cached query hashes mismatch")
            vectors = cached["embeddings"].astype(np.float32, copy=False)
        require(vectors.shape == (len(prompts), 1024), "cached query embedding shape mismatch")
        return vectors

    outputs: list[np.ndarray] = []
    batch_size = 32
    for start in range(0, len(prompts), batch_size):
        texts = [channel.query_prefix + prompt.text for prompt in prompts[start : start + batch_size]]
        outputs.append(encode_texts(model, tokenizer, texts, channel))
    vectors = np.vstack(outputs)
    atomic_save_npz(destination, prompt_id=expected_prompt_ids, prompt_sha256=expected_hashes, embeddings=vectors)
    return vectors


def top_skill_rows(query: np.ndarray, chunks: list[ChunkRecord], embeddings: np.ndarray) -> list[dict[str, Any]]:
    require(embeddings.shape == (len(chunks), 1024), "document embeddings do not align with chunks")
    scores = embeddings @ query
    best: dict[str, tuple[float, ChunkRecord]] = {}
    for score, chunk in zip(scores.tolist(), chunks):
        previous = best.get(chunk.skill_id)
        current_key = (float(score), -chunk.chunk_index, -chunk.start_char)
        previous_key = None if previous is None else (previous[0], -previous[1].chunk_index, -previous[1].start_char)
        if previous_key is None or current_key > previous_key:
            best[chunk.skill_id] = (float(score), chunk)
    ordered = sorted(best.items(), key=lambda item: (-item[1][0], item[0]))[:TOP_K]
    require(len(ordered) == TOP_K, "top-K candidate discovery underflow")
    return [
        {
            "rank": rank,
            "score": round(score, 9),
            "winning_chunk": chunk.public_dict(),
        }
        for rank, (_, (score, chunk)) in enumerate(ordered, start=1)
    ]


def top_skill_ids(query: np.ndarray, chunks: list[ChunkRecord], embeddings: np.ndarray) -> list[tuple[str, dict[str, Any]]]:
    rows = top_skill_rows(query, chunks, embeddings)
    return [(row["winning_chunk"]["skill_id"], row) for row in rows]


def sentinel_ids(prompt_id: str, excluded: set[str], ordered_skill_ids: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
    selected: list[str] = []
    audit: list[dict[str, Any]] = []
    ordinal = 0
    while len(selected) < 2:
        digest = hashlib.sha256(f"{SENTINEL_SEED}:{prompt_id}:{ordinal}".encode("utf-8")).digest()
        candidate = ordered_skill_ids[int.from_bytes(digest, "big") % len(ordered_skill_ids)]
        accepted = candidate not in excluded and candidate not in selected
        audit.append(
            {
                "accepted": accepted,
                "candidate_skill_id": candidate,
                "draw_ordinal": ordinal,
                "draw_sha256": digest.hex(),
                "prompt_id": prompt_id,
            }
        )
        if accepted:
            selected.append(candidate)
        ordinal += 1
        require(ordinal <= len(ordered_skill_ids) * 20, "unable to sample two unique sentinels")
    return selected, audit


def candidate_rows(
    prompts: list[PromptRecord],
    sources: list[SourceRecord],
    seeds: dict[str, set[str]],
    d1_chunks: list[ChunkRecord],
    d1_embeddings: np.ndarray,
    d1_queries: np.ndarray,
    d2_chunks: list[ChunkRecord],
    d2_embeddings: np.ndarray,
    d2_queries: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    source_by_id = {source.skill_id: source for source in sources}
    ordered_skill_ids = sorted(source_by_id)
    rows: list[dict[str, Any]] = []
    sentinel_audit: list[dict[str, Any]] = []
    channel_counts = {"D1": 0, "D2": 0, "Q0": 0, "S0": 0}
    for prompt_index, prompt in enumerate(prompts, start=1):
        candidates: dict[str, dict[str, Any]] = {}
        for skill_id in sorted(seeds[prompt.prompt_id]):
            candidates.setdefault(skill_id, {"S0": {"present": True}})
            channel_counts["S0"] += 1
        for channel_name, query, chunks, embeddings in (
            ("D1", d1_queries[prompt_index - 1], d1_chunks, d1_embeddings),
            ("D2", d2_queries[prompt_index - 1], d2_chunks, d2_embeddings),
        ):
            for skill_id, evidence in top_skill_ids(query, chunks, embeddings):
                candidates.setdefault(skill_id, {})[channel_name] = evidence
                channel_counts[channel_name] += 1
        sentinels, audit = sentinel_ids(prompt.prompt_id, set(candidates), ordered_skill_ids)
        sentinel_audit.extend(audit)
        for ordinal, skill_id in enumerate(sentinels, start=1):
            candidates.setdefault(skill_id, {})["Q0"] = {"sentinel_ordinal": ordinal}
            channel_counts["Q0"] += 1
        for skill_id in sorted(candidates):
            rows.append(
                {
                    "candidate_skill_id": skill_id,
                    "candidate_source_sha256": source_by_id[skill_id].source_sha256,
                    "channels": candidates[skill_id],
                    "prompt_id": prompt.prompt_id,
                    "prompt_sha256": prompt.prompt_sha256,
                }
            )
        if prompt_index % 50 == 0 or prompt_index == len(prompts):
            print(f"candidate union: {prompt_index}/{len(prompts)} prompts", file=sys.stderr, flush=True)
    return rows, sentinel_audit, channel_counts


def run_self_test(model_root: Path) -> None:
    """Exercise chunk coverage and sentinel determinism using generated text only."""
    from transformers import AutoTokenizer

    for channel in CHANNELS:
        tokenizer = AutoTokenizer.from_pretrained(model_root / channel.name, local_files_only=True, trust_remote_code=False)
        text = ("synthetic coverage sentence. " * (channel.raw_window_tokens // 3 + 50)).strip()
        windows = token_windows(tokenizer, text, channel.raw_window_tokens, channel.overlap_tokens)
        require(windows[0][2] == 0 and windows[-1][3] == len(text), "synthetic coverage failed")
        require(all(window[2] <= previous[3] for previous, window in zip(windows, windows[1:])), "synthetic window gap")
    choices = [f"synthetic-skill-{index:04d}" for index in range(25)]
    first = sentinel_ids("synthetic-prompt", {choices[0]}, choices)
    second = sentinel_ids("synthetic-prompt", {choices[0]}, choices)
    require(first == second and len(first[0]) == 2, "sentinel sampling is not deterministic")
    crlf_bytes = b"synthetic\r\nsource\r\n"
    require(sha256_bytes(crlf_bytes) != sha256_text(crlf_bytes.decode("utf-8").replace("\r\n", "\n")), "CRLF regression setup failed")
    require(decode_frozen_source(crlf_bytes) == "synthetic\nsource\n", "CRLF normalisation regression")
    print("B0G-CD self-test PASS: synthetic text only; no benchmark text read", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--source-manifest", type=Path)
    parser.add_argument("--prompt-manifest", type=Path)
    parser.add_argument("--seed-review-pool", type=Path)
    parser.add_argument("--cache-root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--workspace-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()

    if args.self_test:
        run_self_test(args.model_root)
        return 0
    required = ["source_manifest", "prompt_manifest", "seed_review_pool", "output_dir"]
    if not args.plan_only:
        required.append("cache_root")
    for name in required:
        require(getattr(args, name) is not None, f"--{name.replace('_', '-')} is required")
    require(not args.output_dir.exists(), "output directory already exists; frozen discovery outputs are immutable")

    script_sha256 = sha256_file(Path(__file__))
    source_manifest_sha256 = sha256_file(args.source_manifest)
    prompt_manifest_sha256 = sha256_file(args.prompt_manifest)
    seed_pool_sha256 = sha256_file(args.seed_review_pool)
    args.output_dir.mkdir(parents=True)
    run_state = args.output_dir / "run_state.json"
    started = time.monotonic()
    write_progress(
        run_state,
        {
            "stage": "B0G-CD",
            "state": "STARTED",
            "benchmark_text_emitted": False,
            "external_requests": 0,
            "provider_calls": 0,
            "semantic_review_run": False,
            "primary_results_consumed": False,
        },
    )
    try:
        sources = load_sources(args.source_manifest, args.workspace_root)
        prompts = load_prompts(args.prompt_manifest)
        source_ids = {source.skill_id for source in sources}
        seeds, seed_stats = load_seed_pool(
            args.seed_review_pool,
            {prompt.prompt_id for prompt in prompts},
            known_prompt_ids(args.prompt_manifest),
            source_ids,
        )
        if args.plan_only:
            plan_channels: dict[str, dict[str, Any]] = {}
            for channel in CHANNELS:
                tokenizer = load_tokenizer(args.model_root, channel)
                chunks = build_chunks(tokenizer, sources, channel)
                bounds = verify_model_input_bounds(tokenizer, chunks, prompts, channel)
                plan_channels[channel.name] = {
                    "chunk_count": len(chunks),
                    "lossless_source_coverage_verified": True,
                    "maximum_input_tokens": channel.maximum_input_tokens,
                    "overlap_tokens": channel.overlap_tokens,
                    "raw_window_tokens": channel.raw_window_tokens,
                    "revision": channel.revision,
                    **bounds,
                }
            plan = {
                "schema_version": SCRIPT_SCHEMA,
                "stage": "B0G-CD plan-only",
                "state": "PASS_NO_EMBEDDINGS",
                "benchmark_text_emitted": False,
                "external_requests": 0,
                "input_manifest": {
                    "prompt_manifest_sha256": prompt_manifest_sha256,
                    "scored_prompt_count": len(prompts),
                    "seed_review_pool_sha256": seed_pool_sha256,
                    "seed_review_rows": seed_stats,
                    "source_manifest_sha256": source_manifest_sha256,
                    "source_skill_count": len(sources),
                },
                "primary_results_consumed": False,
                "provider_calls": 0,
                "semantic_review_run": False,
                "source_chunk_plan": plan_channels,
                "wall_seconds": round(time.monotonic() - started, 3),
            }
            write_json_new(args.output_dir / "discovery_plan.json", plan)
            write_progress(args.output_dir / "run_state.json", plan)
            print("B0G-CD plan-only PASS: no embeddings, candidates, or semantic reviews created", file=sys.stderr)
            return 0
        all_channel_state: dict[str, dict[str, Any]] = {}
        embedded: dict[str, tuple[list[ChunkRecord], np.ndarray, np.ndarray]] = {}
        for channel in CHANNELS:
            model, tokenizer = load_model_and_tokenizer(args.model_root, channel)
            config = cache_config(channel, source_manifest_sha256, script_sha256)
            channel_cache = args.cache_root / channel.name.lower()
            config_path = channel_cache / "cache_config.json"
            if config_path.exists():
                require(json.loads(config_path.read_text(encoding="utf-8")) == config, f"cache configuration drift for {channel.name}")
            else:
                atomic_write_bytes(config_path, json.dumps(config, ensure_ascii=True, indent=2, sort_keys=True).encode("utf-8") + b"\n")
            chunks = build_chunks(tokenizer, sources, channel)
            bounds = verify_model_input_bounds(tokenizer, chunks, prompts, channel)
            embeddings = load_or_embed_chunks(model, tokenizer, chunks, channel, channel_cache / "document_batches", run_state)
            queries = load_or_embed_queries(model, tokenizer, prompts, channel, channel_cache)
            all_channel_state[channel.name] = {
                "chunk_count": len(chunks),
                "document_embedding_dimensions": int(embeddings.shape[1]),
                **bounds,
                "query_embedding_dimensions": int(queries.shape[1]),
                "revision": channel.revision,
                "cache_config_sha256": sha256_json(config),
            }
            embedded[channel.name] = (chunks, embeddings, queries)
            del model

        candidates, sentinel_audit, channel_counts = candidate_rows(
            prompts,
            sources,
            seeds,
            *embedded["D1"],
            *embedded["D2"],
        )
        pre_dedup_ceiling = 1862 + len(prompts) * (TOP_K + TOP_K + 2)
        require(len(candidates) <= pre_dedup_ceiling, "candidate ceiling exceeded")
        require(len({(row["prompt_id"], row["candidate_skill_id"]) for row in candidates}) == len(candidates), "duplicate candidate rows")

        input_manifest = {
            "prompt_manifest_sha256": prompt_manifest_sha256,
            "scored_prompt_count": len(prompts),
            "seed_review_pool_sha256": seed_pool_sha256,
            "seed_review_rows": seed_stats,
            "source_manifest_sha256": source_manifest_sha256,
            "source_skill_count": len(sources),
        }
        write_json_new(args.output_dir / "input_manifest.json", input_manifest)
        for channel_name, (chunks, _, _) in embedded.items():
            write_jsonl_new(args.output_dir / f"{channel_name.lower()}_chunk_manifest.jsonl", (chunk.public_dict() for chunk in chunks))
        write_jsonl_new(args.output_dir / "candidate_pool.jsonl", candidates)
        write_jsonl_new(args.output_dir / "q0_sentinel_audit.jsonl", sentinel_audit)
        summary = {
            "schema_version": SCRIPT_SCHEMA,
            "stage": "B0G-CD",
            "state": "PASS",
            "audit_only_channels": ["S0", "D1", "D2", "Q0"],
            "benchmark_text_emitted": False,
            "candidate_count": len(candidates),
            "candidate_ceiling_pre_deduplication": pre_dedup_ceiling,
            "channel_draw_counts_pre_deduplication": channel_counts,
            "channels": all_channel_state,
            "external_requests": 0,
            "input_manifest": input_manifest,
            "primary_results_consumed": False,
            "provider_calls": 0,
            "script_sha256": script_sha256,
            "semantic_review_run": False,
            "sentinel_seed": SENTINEL_SEED,
            "wall_seconds": round(time.monotonic() - started, 3),
        }
        write_json_new(args.output_dir / "discovery_manifest.json", summary)
        write_progress(args.output_dir / "run_state.json", summary)
        print(
            f"B0G-CD PASS: {len(candidates)} candidates across {len(prompts)} prompts; semantic review not run",
            file=sys.stderr,
        )
        return 0
    except BaseException as error:
        write_progress(
            run_state,
            {
                "stage": "B0G-CD",
                "state": "FAILED_CLOSED",
                "error_type": type(error).__name__,
                "error": str(error) or "interrupted without a message",
                "benchmark_text_emitted": False,
                "external_requests": 0,
                "provider_calls": 0,
                "semantic_review_run": False,
                "primary_results_consumed": False,
            },
        )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
