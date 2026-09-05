#!/usr/bin/env python3
"""Exact-substring, lossless chunking shared by RQ2b dense and rerank runs."""

from __future__ import annotations

import bisect
import re
from dataclasses import asdict, dataclass
from typing import Any

from rq2b_common import require, sha256_json, sha256_text


CHUNKER_VERSION = "rq2b-exact-markdown-chunker-v1"
BLANK_BREAK_RE = re.compile(r"\n(?:[ \t]*\n)+")
HEADING_RE = re.compile(r"(?m)^(?:#{1,6}[ \t]+|[^\n]+\n(?:=+|-+)[ \t]*\n)")


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    start_char: int
    end_char: int
    token_count: int
    text_sha256: str
    token_ids_sha256: str
    ended_at_preferred_boundary: bool
    text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def tokenizer_ids(tokenizer: Any, text: str) -> list[int]:
    return list(tokenizer.encode(text, add_special_tokens=False))


def preferred_boundaries(text: str) -> list[int]:
    boundaries = {len(text)}
    boundaries.update(match.end() for match in BLANK_BREAK_RE.finditer(text))
    for match in HEADING_RE.finditer(text):
        if match.start() > 0:
            boundaries.add(match.start())
    return sorted(boundary for boundary in boundaries if boundary > 0)


def _fits(tokenizer: Any, text: str, start: int, end: int, maximum_tokens: int) -> bool:
    return len(tokenizer_ids(tokenizer, text[start:end])) <= maximum_tokens


def _largest_fitting_end(
    tokenizer: Any,
    text: str,
    start: int,
    maximum_tokens: int,
    boundaries: list[int],
) -> tuple[int, bool]:
    require(start < len(text), "Chunk start must be before the end of text")
    candidates = boundaries[bisect.bisect_right(boundaries, start) :]
    if candidates and _fits(tokenizer, text, start, candidates[-1], maximum_tokens):
        return candidates[-1], True

    low = 0
    high = len(candidates)
    while low < high:
        middle = (low + high) // 2
        if _fits(tokenizer, text, start, candidates[middle], maximum_tokens):
            low = middle + 1
        else:
            high = middle
    if low > 0:
        return candidates[low - 1], True

    low_char = start + 1
    high_char = len(text) + 1
    while low_char < high_char:
        middle = (low_char + high_char) // 2
        if _fits(tokenizer, text, start, middle, maximum_tokens):
            low_char = middle + 1
        else:
            high_char = middle
    end = low_char - 1
    require(end > start, "Unable to fit even one character in the chunk budget")
    while end > start and not _fits(tokenizer, text, start, end, maximum_tokens):
        end -= 1
    require(end > start, "Unable to produce a non-empty hard-split chunk")
    return end, False


def _overlap_start(
    tokenizer: Any,
    text: str,
    chunk_start: int,
    chunk_end: int,
    overlap_tokens: int,
) -> int:
    if overlap_tokens <= 0:
        return chunk_end
    low = chunk_start + 1
    high = chunk_end + 1
    while low < high:
        middle = (low + high) // 2
        tail_tokens = len(tokenizer_ids(tokenizer, text[middle:chunk_end]))
        if tail_tokens <= overlap_tokens:
            high = middle
        else:
            low = middle + 1
    next_start = min(low, chunk_end)
    if next_start <= chunk_start:
        return chunk_end
    return next_start


def exact_text_chunks(
    tokenizer: Any,
    text: str,
    *,
    maximum_tokens: int,
    overlap_tokens: int,
) -> list[TextChunk]:
    require(maximum_tokens > 0, "maximum_tokens must be positive")
    require(0 <= overlap_tokens < maximum_tokens, "Invalid overlap token budget")
    require(bool(text), "Cannot chunk empty selector text")
    boundaries = preferred_boundaries(text)
    chunks: list[TextChunk] = []
    start = 0
    while start < len(text):
        end, preferred = _largest_fitting_end(
            tokenizer,
            text,
            start,
            maximum_tokens,
            boundaries,
        )
        chunk_text = text[start:end]
        token_ids = tokenizer_ids(tokenizer, chunk_text)
        require(len(token_ids) <= maximum_tokens, "Chunk exceeds token ceiling")
        chunks.append(
            TextChunk(
                chunk_index=len(chunks),
                start_char=start,
                end_char=end,
                token_count=len(token_ids),
                text_sha256=sha256_text(chunk_text),
                token_ids_sha256=sha256_json(token_ids),
                ended_at_preferred_boundary=preferred,
                text=chunk_text,
            )
        )
        if end == len(text):
            break
        next_start = _overlap_start(
            tokenizer,
            text,
            start,
            end,
            overlap_tokens,
        )
        require(start < next_start <= end, "Chunk overlap did not advance")
        start = next_start
    verify_exact_text_chunks(
        tokenizer,
        text,
        chunks,
        maximum_tokens=maximum_tokens,
    )
    return chunks


def verify_exact_text_chunks(
    tokenizer: Any,
    text: str,
    chunks: list[TextChunk],
    *,
    maximum_tokens: int,
) -> None:
    require(bool(chunks), "Chunk list is empty")
    require(chunks[0].start_char == 0, "Chunk coverage does not start at character zero")
    require(chunks[-1].end_char == len(text), "Chunk coverage does not reach text end")
    previous_end = 0
    reconstructed = ""
    for expected_index, chunk in enumerate(chunks):
        require(chunk.chunk_index == expected_index, "Chunk indices are not contiguous")
        require(0 <= chunk.start_char < chunk.end_char <= len(text), "Invalid chunk character range")
        require(chunk.start_char <= previous_end, "Chunk character coverage has a gap")
        require(text[chunk.start_char : chunk.end_char] == chunk.text, "Chunk is not an exact source substring")
        ids = tokenizer_ids(tokenizer, chunk.text)
        require(len(ids) == chunk.token_count, "Chunk token count drift")
        require(len(ids) <= maximum_tokens, "Chunk token ceiling exceeded")
        require(sha256_text(chunk.text) == chunk.text_sha256, "Chunk text hash drift")
        require(sha256_json(ids) == chunk.token_ids_sha256, "Chunk token hash drift")
        append_start = max(previous_end, chunk.start_char)
        reconstructed += text[append_start : chunk.end_char]
        previous_end = max(previous_end, chunk.end_char)
    require(reconstructed == text, "Non-overlap chunk reconstruction differs from source text")

    try:
        encoded = tokenizer(
            text,
            add_special_tokens=False,
            return_offsets_mapping=True,
        )
        offsets = encoded.get("offset_mapping")
    except (TypeError, NotImplementedError, ValueError):
        offsets = None
    if offsets is not None:
        for token_index, pair in enumerate(offsets):
            token_start, token_end = int(pair[0]), int(pair[1])
            if token_end <= token_start:
                continue
            covered = any(
                chunk.start_char <= token_start and token_end <= chunk.end_char
                for chunk in chunks
            )
            require(covered, f"Source tokenizer span is not covered: token {token_index}")
