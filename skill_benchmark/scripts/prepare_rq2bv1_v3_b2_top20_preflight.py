#!/usr/bin/env python3
"""Prepare the V3 strict-only RQ2b B2 Top-20 reranking payload locally.

This is deliberately separate from the legacy RQ2b reranker runners.  It
binds only the completed V3 B1 strict rows, preserves each persisted Top-20
candidate list byte-for-byte, and constructs lossless, query-specific windows
that both B2 rerankers must use.  It makes no network request and never calls a
model forward pass.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_v11_execution_contract import B1_SCHEMA, validate_b1_row
from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight


ROOT = Path(__file__).resolve().parents[2]
VERSION_ID = "rq2b-full-library-v1.1-2026-08-15"
PREFLIGHT_DIR = "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2"
PREFLIGHT_SCHEMA = "rq2bv1-v3-b2-top20-preflight-v1"
CONDITION_SCHEMA = "rq2bv1-v3-b2-top20-condition-v1"
PAIR_SCHEMA = "rq2bv1-v3-b2-top20-pair-v1"
PRIMARY_K = 20
PAIR_MAX_TOKENS = 2048
PAIR_SAFETY_TOKENS = 16
PAIR_OVERLAP_TOKENS = 128

SKILLROUTER_MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
SKILLROUTER_REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
SKILLROUTER_TOKENIZER_SHA256 = "ab19c66299579df20542864f9e27b79898ca05f35acc97fd9259aee385a07d4a"
SKILLROUTER_PROMPT_SHA256 = "face140f238119fc19ba12de90131d1031ada388f08f73e641d0dffd6a00817e"

INSTRUCTION = (
    "Given a task description, judge whether the skill document "
    "is relevant and useful for completing the task"
)
BODY_FORMAT = "<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {document}"
PREFIX = (
    "<|im_start|>system\nJudge whether the Document meets the requirements "
    "based on the Query and the Instruct provided. Note that the answer can "
    'only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
)
SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

B1_RESULT_SOURCES = (
    (
        "bm25",
        "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/"
        "b1l_preflight_v3/b1l_local_bm25_run/b1l_strict_results.jsonl",
        "bm25",
    ),
    (
        "qwen_embedding",
        "skill_benchmark/rq2bv1/results/qwen_primary_v3/qwen_primary_strict_results.jsonl",
        "qwen-text-embedding-v4",
    ),
    (
        "skillrouter_embedding",
        "skill_benchmark/rq2bv1/results/skillrouter_primary_v3/"
        "local_scoring_path_contract_amendment/skillrouter_primary_strict_results.jsonl",
        "skillrouter-embedding-0.6b",
    ),
)

FORBIDDEN_PROVIDER_KEYS = {
    "gold_skill",
    "valid_skills",
    "acceptable_skill",
    "acceptable_skills",
    "strict_gold_rank",
    "strict_hit_at_1",
    "strict_recall_at_20",
    "stratum",
    "group",
}

BLANK_BREAK_RE = re.compile(r"\n(?:[ \t]*\n)+")
HEADING_RE = re.compile(r"(?m)^(?:#{1,6}[ \t]+|[^\n]+\n(?:=+|-+)[ \t]*\n)")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while data := handle.read(1024 * 1024):
            digest.update(data)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


def relative(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def path_reference(path: Path, root: Path) -> str:
    """Use workspace-relative paths for artifacts and absolute paths for pinned caches."""

    try:
        return relative(path, root)
    except ValueError:
        return str(path.resolve())


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            require(bool(line.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(line)
            require(isinstance(value, dict), f"Non-object JSONL row: {path}:{line_number}")
            rows.append(value)
    return rows


def write_json(path: Path, value: Any) -> None:
    require(not path.exists(), f"Refusing to overwrite immutable artifact: {path}")
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    require(not path.exists(), f"Refusing to overwrite immutable artifact: {path}")
    with path.open("x", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n")


def build_pair_ids(tokenizer: Any, query: str, document: str) -> list[int]:
    body = BODY_FORMAT.format(instruction=INSTRUCTION, query=query, document=document)
    return (
        tokenizer.encode(PREFIX, add_special_tokens=False)
        + tokenizer.encode(body, add_special_tokens=False)
        + tokenizer.encode(SUFFIX, add_special_tokens=False)
    )


def lossless_markdown_windows(
    tokenizer: Any,
    text: str,
    *,
    maximum_tokens: int,
    overlap_tokens: int,
) -> list[dict[str, Any]]:
    """Fast, lossless source-substring windows for an already over-budget text.

    The older generic chunker probes many character endpoints for every
    document.  Here the source tokenizer offsets give an initial token-aligned
    ceiling, then each emitted substring is re-tokenised and checked directly.
    This preserves the real safety properties needed by the B2 model payload:
    exact source substrings, complete character coverage, overlap, and a hard
    per-window token limit.
    """

    require(bool(text), "Cannot window an empty selector text")
    require(0 <= overlap_tokens < maximum_tokens, "Invalid reranker overlap")
    encoded_full = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    full_offsets = [tuple(map(int, offset)) for offset in encoded_full["offset_mapping"] if int(offset[1]) > int(offset[0])]
    require(full_offsets, "Selector text contains no tokenizer spans")
    token_ends = [end for _, end in full_offsets]
    preferred = {len(text)}
    preferred.update(match.end() for match in BLANK_BREAK_RE.finditer(text))
    preferred.update(match.start() for match in HEADING_RE.finditer(text) if match.start() > 0)
    preferred_boundaries = sorted(boundary for boundary in preferred if 0 < boundary <= len(text))

    windows: list[dict[str, Any]] = []
    start = 0
    while start < len(text):
        first_token = bisect.bisect_right(token_ends, start)
        require(first_token < len(full_offsets), "Window start advanced beyond final tokenizer span")
        last_token = min(first_token + maximum_tokens - 1, len(full_offsets) - 1)
        hard_end = len(text) if last_token == len(full_offsets) - 1 else full_offsets[last_token][1]
        boundary_index = bisect.bisect_right(preferred_boundaries, hard_end) - 1
        end = preferred_boundaries[boundary_index] if boundary_index >= 0 and preferred_boundaries[boundary_index] > start else hard_end
        require(start < end <= len(text), "Unable to construct a nonempty reranker window")

        while True:
            encoded = tokenizer(text[start:end], add_special_tokens=False, return_offsets_mapping=True)
            token_ids = list(encoded["input_ids"])
            offsets = [tuple(map(int, offset)) for offset in encoded["offset_mapping"] if int(offset[1]) > int(offset[0])]
            if len(token_ids) <= maximum_tokens:
                break
            require(len(offsets) >= 2, "Cannot reduce an over-budget reranker window")
            end = start + offsets[-2][1]
            require(start < end, "Over-budget reranker window cannot advance")
        window_text = text[start:end]
        require(window_text == text[start:end], "Reranker window is not an exact source substring")
        windows.append(
            {
                "window_index": len(windows),
                "text": window_text,
                "text_sha256": sha256_text(window_text),
                "source_start_char": start,
                "source_end_char": end,
                "window_token_count": len(token_ids),
            }
        )
        if end == len(text):
            break
        if len(token_ids) <= overlap_tokens:
            next_start = end
        else:
            next_start = start + offsets[len(token_ids) - overlap_tokens][0]
        require(start < next_start <= end, "Reranker overlap did not make progress")
        start = next_start

    require(windows[0]["source_start_char"] == 0, "Reranker windows do not start at source zero")
    require(windows[-1]["source_end_char"] == len(text), "Reranker windows do not cover source end")
    previous_end = 0
    reconstructed = ""
    for expected_index, window in enumerate(windows):
        require(window["window_index"] == expected_index, "Reranker window indexes are not contiguous")
        require(window["source_start_char"] <= previous_end, "Reranker windows leave a source gap")
        require(window["text"] == text[window["source_start_char"] : window["source_end_char"]], "Reranker window source mismatch")
        append_start = max(previous_end, window["source_start_char"])
        reconstructed += text[append_start : window["source_end_char"]]
        previous_end = max(previous_end, window["source_end_char"])
    require(reconstructed == text, "Reranker windows do not reconstruct exact selector text")
    return windows


def load_tokenizer() -> tuple[Any, Path]:
    from transformers import AutoTokenizer

    snapshot = (
        Path.home()
        / ".cache/huggingface/hub/models--pipizhao--SkillRouter-Reranker-0.6B/snapshots"
        / SKILLROUTER_REVISION
    )
    tokenizer_path = snapshot / "tokenizer.json"
    require(snapshot.is_dir(), f"Pinned SkillRouter reranker snapshot is absent: {snapshot}")
    require(tokenizer_path.is_file(), f"Pinned SkillRouter tokenizer is absent: {tokenizer_path}")
    require(
        sha256_file(tokenizer_path) == SKILLROUTER_TOKENIZER_SHA256,
        "Pinned SkillRouter reranker tokenizer hash drift",
    )
    return AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False), snapshot


def _validate_prompt_rows(prompts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    required = {
        "schema_version",
        "prompt_id",
        "prompt",
        "prompt_sha256",
        "stratum",
        "group",
        "gold_skill",
    }
    indexed: dict[str, dict[str, Any]] = {}
    for row in prompts:
        require(set(row) == required, f"Strict prompt schema drift: {row.get('prompt_id')}")
        prompt_id = row["prompt_id"]
        require(isinstance(prompt_id, str) and prompt_id, "Strict prompt ID is invalid")
        require(prompt_id not in indexed, f"Duplicate strict prompt ID: {prompt_id}")
        require(isinstance(row["prompt"], str) and row["prompt"].strip(), f"Empty strict prompt: {prompt_id}")
        require(row["prompt_sha256"] == sha256_text(row["prompt"]), f"Strict prompt hash drift: {prompt_id}")
        indexed[prompt_id] = row
    require(len(indexed) == 381, "V3 B2 expects exactly 381 strict prompts")
    require(Counter(row["stratum"] for row in prompts) == {"controlled": 243, "public_gold": 138}, "Strict strata drift")
    return indexed


def _validate_representations(representations: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, dict[str, Any]]]:
    expected = {"i1-discovery", "i2-original", "i3c-fielded-evidence", "i3-flat-evidence"}
    require(set(representations) == expected, "V3 B2 representation set drift")
    indexed: dict[str, dict[str, dict[str, Any]]] = {}
    for representation, rows in representations.items():
        by_skill: dict[str, dict[str, Any]] = {}
        for row in rows:
            require(row.get("representation") == representation, f"Representation identity drift: {representation}")
            skill_id = row.get("skill_id")
            text = row.get("selector_text")
            require(isinstance(skill_id, str) and skill_id, f"Missing skill ID: {representation}")
            require(skill_id not in by_skill, f"Duplicate representation skill: {representation}/{skill_id}")
            require(isinstance(text, str) and text, f"Empty selector text: {representation}/{skill_id}")
            require(row.get("selector_text_sha256") == sha256_text(text), f"Selector text hash drift: {representation}/{skill_id}")
            by_skill[skill_id] = row
        require(len(by_skill) == 2433, f"Representation size drift: {representation}")
        indexed[representation] = by_skill
    return indexed


def _load_b1_rows(root: Path, prompts: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    expected_representations = {"i1-discovery", "i2-original", "i3c-fielded-evidence", "i3-flat-evidence"}
    seen_conditions: set[tuple[str, str, str]] = set()
    for source_name, source_relative, expected_retriever in B1_RESULT_SOURCES:
        path = root / source_relative
        require(path.is_file(), f"Missing completed B1 source: {path}")
        source_rows = read_jsonl(path)
        require(len(source_rows) == 1524, f"B1 source row count drift: {source_name}")
        sources.append(
            {
                "source_name": source_name,
                "path": relative(path, root),
                "sha256": sha256_file(path),
                "rows": len(source_rows),
                "retriever": expected_retriever,
            }
        )
        source_seen: set[tuple[str, str]] = set()
        for row in source_rows:
            require(row.get("schema_version") == B1_SCHEMA, f"Unexpected B1 schema: {source_name}")
            require(row.get("version_id") == VERSION_ID, f"Unexpected B1 version: {source_name}")
            require(row.get("retriever") == expected_retriever, f"B1 retriever drift: {source_name}")
            prompt_id = row.get("prompt_id")
            require(prompt_id in prompts, f"B1 row uses unknown strict prompt: {source_name}/{prompt_id}")
            validate_b1_row(row, prompts[prompt_id], f"b2-preflight/{source_name}/{row.get('representation')}/{prompt_id}")
            representation = row["representation"]
            require(representation in expected_representations, f"Unexpected B1 representation: {representation}")
            key = (representation, prompt_id)
            require(key not in source_seen, f"Duplicate B1 source condition: {source_name}/{key}")
            source_seen.add(key)
            global_key = (expected_retriever, representation, prompt_id)
            require(global_key not in seen_conditions, f"Duplicate B1 condition across sources: {global_key}")
            seen_conditions.add(global_key)
            rows.append({**row, "_b1_source": source_name})
        expected_source_conditions = {(representation, prompt_id) for representation in expected_representations for prompt_id in prompts}
        require(source_seen == expected_source_conditions, f"Incomplete B1 source matrix: {source_name}")
    require(len(rows) == 4572, "B2 must bind exactly 4,572 completed B1 conditions")
    return rows, sources


def _condition_id(row: dict[str, Any]) -> str:
    return sha256_json(
        {
            "b1_source": row["_b1_source"],
            "retriever": row["retriever"],
            "representation": row["representation"],
            "prompt_id": row["prompt_id"],
            "top20": row["top_20_skill_ids"],
        }
    )


def _provider_condition(condition: dict[str, Any]) -> dict[str, Any]:
    require(not (set(condition) & FORBIDDEN_PROVIDER_KEYS), "Provider condition has label leakage")
    return condition


def build_preflight(root: Path, output_dir: Path) -> dict[str, Any]:
    require(not output_dir.exists(), f"Refusing to overwrite existing B2 preflight: {output_dir}")
    report, representations, prompts_raw = verify_preflight(root)
    prompt_by_id = _validate_prompt_rows(prompts_raw)
    representation_by_skill = _validate_representations(representations)
    b1_rows, b1_sources = _load_b1_rows(root, prompt_by_id)
    tokenizer, snapshot = load_tokenizer()

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    # A preflight can take several minutes to derive lossless windows.  Make an
    # interrupted attempt self-contained rather than blocking a later rerun;
    # only the final immutable output directory is a scientific artifact.
    staging = output_dir.with_name(f".{output_dir.name}.staging-{os.getpid()}")
    require(not staging.exists(), f"Unexpected live B2 staging directory collision: {staging}")
    staging.mkdir()

    condition_rows: list[dict[str, Any]] = []
    pair_rows_by_id: dict[str, dict[str, Any]] = {}
    condition_private_bindings: list[dict[str, Any]] = []
    budgets: list[int] = []
    candidate_window_counts: list[int] = []
    total_candidate_occurrences = 0
    # The three B1 retrievers can nominate the same query/representation/skill
    # pair. Chunking depends only on that tuple and the query-specific budget,
    # never on the first-stage retriever, so it is safe to reuse exactly.
    window_template_cache: dict[tuple[str, str, str, str, int], list[dict[str, Any]]] = {}
    window_template_cache_hits = 0
    window_template_cache_misses = 0
    single_window_fast_paths = 0

    for index, b1_row in enumerate(sorted(b1_rows, key=lambda row: (row["_b1_source"], row["representation"], row["prompt_id"]))):
        prompt = prompt_by_id[b1_row["prompt_id"]]
        representation = b1_row["representation"]
        query = prompt["prompt"]
        empty_pair_tokens = len(build_pair_ids(tokenizer, query, ""))
        document_budget = PAIR_MAX_TOKENS - empty_pair_tokens - PAIR_SAFETY_TOKENS
        require(document_budget > 0, f"No SkillRouter document budget for prompt: {prompt['prompt_id']}")
        budgets.append(document_budget)
        candidate_skill_ids = list(b1_row["top_20_skill_ids"])
        require(len(candidate_skill_ids) == len(set(candidate_skill_ids)) == PRIMARY_K, "Persisted B1 Top-20 is invalid")
        condition_id = _condition_id(b1_row)
        provider_candidates: list[dict[str, Any]] = []
        private_candidates: list[dict[str, Any]] = []
        for first_stage_rank, skill_id in enumerate(candidate_skill_ids, start=1):
            representation_row = representation_by_skill[representation].get(skill_id)
            require(representation_row is not None, f"B1 Top-20 skill missing from representation: {representation}/{skill_id}")
            selector_text = representation_row["selector_text"]
            template_key = (
                representation,
                prompt["prompt_sha256"],
                skill_id,
                representation_row["selector_text_sha256"],
                document_budget,
            )
            templates = window_template_cache.get(template_key)
            if templates is None:
                window_template_cache_misses += 1
                selector_token_ids = tokenizer.encode(selector_text, add_special_tokens=False)
                if len(selector_token_ids) <= document_budget:
                    # This direct branch is exactly one complete source string:
                    # it needs no chunk boundary search or offset-map replay.
                    chunks = [
                        {
                            "window_index": 0,
                            "text": selector_text,
                            "text_sha256": sha256_text(selector_text),
                            "source_start_char": 0,
                            "source_end_char": len(selector_text),
                            "window_token_count": len(selector_token_ids),
                        }
                    ]
                    single_window_fast_paths += 1
                else:
                    chunks = lossless_markdown_windows(
                        tokenizer,
                        selector_text,
                        maximum_tokens=document_budget,
                        overlap_tokens=PAIR_OVERLAP_TOKENS,
                    )
                templates = []
                for chunk in chunks:
                    pair_input_tokens = len(build_pair_ids(tokenizer, query, chunk["text"]))
                    require(pair_input_tokens <= PAIR_MAX_TOKENS, "SkillRouter pair token limit was exceeded after chunking")
                    templates.append({**chunk, "pair_input_token_count": pair_input_tokens})
                window_template_cache[template_key] = templates
            else:
                window_template_cache_hits += 1
            provider_windows: list[dict[str, Any]] = []
            private_windows: list[dict[str, Any]] = []
            for chunk in templates:
                pair_input_tokens = int(chunk["pair_input_token_count"])
                pair_id = sha256_json(
                    {
                        "representation": representation,
                        "prompt_sha256": prompt["prompt_sha256"],
                        "skill_id": skill_id,
                        "window_index": chunk["window_index"],
                        "window_text_sha256": chunk["text_sha256"],
                        "reranker_prompt_sha256": SKILLROUTER_PROMPT_SHA256,
                    }
                )
                pair = {
                    "schema_version": PAIR_SCHEMA,
                    "pair_id": pair_id,
                    "representation": representation,
                    "prompt_id": prompt["prompt_id"],
                    "prompt_sha256": prompt["prompt_sha256"],
                    "query": query,
                    "query_sha256": prompt["prompt_sha256"],
                    "skill_id": skill_id,
                    "window_index": chunk["window_index"],
                    "window_text": chunk["text"],
                    "window_text_sha256": chunk["text_sha256"],
                    "source_start_char": chunk["source_start_char"],
                    "source_end_char": chunk["source_end_char"],
                    "window_token_count": chunk["window_token_count"],
                    "pair_input_token_count": pair_input_tokens,
                }
                existing = pair_rows_by_id.get(pair_id)
                if existing is None:
                    pair_rows_by_id[pair_id] = pair
                else:
                    require(existing == pair, f"Pair hash collision or nondeterministic payload: {pair_id}")
                provider_windows.append(
                    {
                        "window_index": chunk["window_index"],
                        "text": chunk["text"],
                        "text_sha256": chunk["text_sha256"],
                        "skillrouter_window_tokens": chunk["window_token_count"],
                        "pair_id": pair_id,
                    }
                )
                private_windows.append(
                    {
                        "pair_id": pair_id,
                        "source_start_char": chunk["source_start_char"],
                        "source_end_char": chunk["source_end_char"],
                        "pair_input_token_count": pair_input_tokens,
                    }
                )
            require(provider_windows, f"Candidate generated zero windows: {skill_id}")
            provider_candidates.append({"first_stage_rank": first_stage_rank, "skill_id": skill_id, "windows": provider_windows})
            private_candidates.append({"first_stage_rank": first_stage_rank, "skill_id": skill_id, "windows": private_windows})
        total_candidate_occurrences += len(candidate_skill_ids)
        condition = _provider_condition(
            {
                "schema_version": CONDITION_SCHEMA,
                "condition_id": condition_id,
                "b1_source": b1_row["_b1_source"],
                "first_stage_retriever": b1_row["retriever"],
                "representation": representation,
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
                "query": query,
                "query_sha256": prompt["prompt_sha256"],
                "candidate_skill_ids": candidate_skill_ids,
                "candidate_list_sha256": sha256_json(candidate_skill_ids),
                "skillrouter_empty_pair_tokens": empty_pair_tokens,
                "skillrouter_document_budget": document_budget,
                "candidates": provider_candidates,
            }
        )
        require(set(condition) == {
            "schema_version", "condition_id", "b1_source", "first_stage_retriever", "representation",
            "prompt_id", "prompt_sha256", "query", "query_sha256", "candidate_skill_ids",
            "candidate_list_sha256", "skillrouter_empty_pair_tokens", "skillrouter_document_budget", "candidates",
        }, "Provider condition schema drift")
        require(condition["candidate_skill_ids"] == [candidate["skill_id"] for candidate in provider_candidates], "Candidate ordering drift")
        candidate_window_counts.append(sum(len(candidate["windows"]) for candidate in provider_candidates))
        condition_rows.append(condition)
        condition_private_bindings.append(
            {
                "condition_id": condition_id,
                "gold_skill": prompt["gold_skill"],
                "stratum": prompt["stratum"],
                "group": prompt["group"],
                "first_stage_strict_top1": int(candidate_skill_ids[0] == prompt["gold_skill"]),
                "strict_candidate_positive": int(prompt["gold_skill"] in candidate_skill_ids),
                "candidates": private_candidates,
            }
        )
        if (index + 1) % 100 == 0 or index + 1 == len(b1_rows):
            print(f"B2 preflight: built {index + 1}/{len(b1_rows)} conditions", flush=True)

    condition_rows.sort(key=lambda row: row["condition_id"])
    condition_private_bindings.sort(key=lambda row: row["condition_id"])
    pair_rows = [pair_rows_by_id[pair_id] for pair_id in sorted(pair_rows_by_id)]
    require(len(condition_rows) == len(condition_private_bindings) == 4572, "B2 condition coverage drift")
    require(len({row["condition_id"] for row in condition_rows}) == 4572, "Duplicate B2 condition IDs")
    require(all(len(row["candidate_skill_ids"]) == PRIMARY_K for row in condition_rows), "Top-20 length drift")
    require(all(not (set(row) & FORBIDDEN_PROVIDER_KEYS) for row in condition_rows), "Label leakage in provider condition")
    require(all(math.isfinite(float(row["pair_input_token_count"])) for row in pair_rows), "Nonfinite pair token count")

    condition_path = staging / "conditions.jsonl"
    private_path = staging / "strict_bindings.jsonl"
    pair_path = staging / "unique_pairs.jsonl"
    write_jsonl(condition_path, condition_rows)
    write_jsonl(private_path, condition_private_bindings)
    write_jsonl(pair_path, pair_rows)

    condition_by_representation = Counter(row["representation"] for row in condition_rows)
    condition_by_retriever = Counter(row["first_stage_retriever"] for row in condition_rows)
    final_condition_path = output_dir / condition_path.name
    final_private_path = output_dir / private_path.name
    final_pair_path = output_dir / pair_path.name
    report_payload = {
        "schema_version": PREFLIGHT_SCHEMA,
        "state": "prepared_local_zero_network_no_reranker_execution",
        "scope": {
            "version_id": VERSION_ID,
            "candidate_library_skills": 2433,
            "strict_prompts": 381,
            "b1_conditions": 4572,
            "candidate_occurrences": total_candidate_occurrences,
            "reranker_conditions_per_reranker": 4572,
            "reranker_condition_outcomes_for_two_rerankers": 9144,
            "primary_k": PRIMARY_K,
            "representations": sorted(condition_by_representation),
            "first_stage_retrievers": sorted(condition_by_retriever),
        },
        "boundary": {
            "network_calls": 0,
            "provider_text_submissions": 0,
            "model_forward_passes": 0,
            "candidate_regeneration": False,
            "query_rewrite": False,
            "label_fields_excluded_from_provider_conditions": sorted(FORBIDDEN_PROVIDER_KEYS),
        },
        "skillrouter_windowing": {
            "model": SKILLROUTER_MODEL,
            "revision": SKILLROUTER_REVISION,
            "tokenizer_path": path_reference(snapshot / "tokenizer.json", root),
            "tokenizer_sha256": SKILLROUTER_TOKENIZER_SHA256,
            "prompt_sha256": SKILLROUTER_PROMPT_SHA256,
            "max_pair_tokens": PAIR_MAX_TOKENS,
            "safety_tokens": PAIR_SAFETY_TOKENS,
            "overlap_tokens": PAIR_OVERLAP_TOKENS,
            "document_budget_min": min(budgets),
            "document_budget_max": max(budgets),
            "unique_query_document_windows": len(pair_rows),
            "unique_model_input_tokens": sum(row["pair_input_token_count"] for row in pair_rows),
            "max_pair_input_tokens": max(row["pair_input_token_count"] for row in pair_rows),
            "window_template_cache": {
                "entries": len(window_template_cache),
                "hits": window_template_cache_hits,
                "misses": window_template_cache_misses,
                "single_window_fast_paths": single_window_fast_paths,
            },
        },
        "qwen_reranker_shared_visibility": {
            "policy": "uses the identical raw prompt and exact SkillRouter-safe selector-text windows for each candidate; provider documents are not regenerated or expanded",
            "max_documents_in_one_condition": max(candidate_window_counts),
            "condition_window_count_p50": sorted(candidate_window_counts)[(len(candidate_window_counts) - 1) // 2],
            "condition_window_count_p95": sorted(candidate_window_counts)[math.ceil(len(candidate_window_counts) * 0.95) - 1],
        },
        "input_bindings": {
            "b1_sources": b1_sources,
            "strict_prompt_artifact": report["strict_scored_prompts"],
            "representations": report["representations"],
        },
        "artifacts": {
            "conditions": {"path": relative(final_condition_path, root), "sha256": sha256_file(condition_path), "rows": len(condition_rows)},
            "strict_bindings": {"path": relative(final_private_path, root), "sha256": sha256_file(private_path), "rows": len(condition_private_bindings)},
            "unique_pairs": {"path": relative(final_pair_path, root), "sha256": sha256_file(pair_path), "rows": len(pair_rows)},
        },
    }
    report_path = staging / "preflight_report.json"
    write_json(report_path, report_payload)
    manifest = {
        "schema_version": "rq2bv1-v3-b2-top20-preflight-manifest-v1",
        "state": "prepared_local_zero_network_no_reranker_execution",
        "preflight_report": {"path": relative(output_dir / report_path.name, root), "sha256": sha256_file(report_path)},
        "artifacts": report_payload["artifacts"],
    }
    manifest_path = staging / "manifest.json"
    write_json(manifest_path, manifest)
    staging.replace(output_dir)
    return report_payload


def self_test() -> dict[str, Any]:
    candidate_ids = [f"skill-{index:02d}" for index in range(PRIMARY_K)]
    condition = {
        "schema_version": CONDITION_SCHEMA,
        "condition_id": "synthetic",
        "b1_source": "synthetic",
        "first_stage_retriever": "synthetic",
        "representation": "i3c-fielded-evidence",
        "prompt_id": "synthetic-prompt",
        "prompt_sha256": sha256_text("synthetic query"),
        "query": "synthetic query",
        "query_sha256": sha256_text("synthetic query"),
        "candidate_skill_ids": candidate_ids,
        "candidate_list_sha256": sha256_json(candidate_ids),
        "skillrouter_empty_pair_tokens": 10,
        "skillrouter_document_budget": 100,
        "candidates": [],
    }
    _provider_condition(condition)
    require(not (set(condition) & FORBIDDEN_PROVIDER_KEYS), "Synthetic provider-condition leakage")
    try:
        _provider_condition({**condition, "gold_skill": "skill-19"})
    except RuntimeError:
        leakage_rejected = True
    else:
        leakage_rejected = False
    require(leakage_rejected, "Synthetic label leakage was not rejected")
    external_path_is_explicit = path_reference(Path.home() / ".cache" / "synthetic-tokenizer.json", ROOT).startswith("/")
    require(external_path_is_explicit, "Synthetic external model-path reference failed")
    return {
        "state": "pass_synthetic_zero_network_no_reranker_execution",
        "network_calls": 0,
        "model_forward_passes": 0,
        "top20_identity_preserved": condition["candidate_list_sha256"] == sha256_json(candidate_ids),
        "provider_label_leakage_rejected": leakage_rejected,
        "external_model_path_is_explicit": external_path_is_explicit,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path(PREFLIGHT_DIR))
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.prepare, "Use --prepare to build the local B2 preflight")
        root = args.root.resolve()
        output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        result = build_preflight(root, output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
