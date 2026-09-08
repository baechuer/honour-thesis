#!/usr/bin/env python3
"""V7 exact Markdown chunker correction for short-boundary progress.

This preserves the frozen 7,500-token ceiling, at-most-256-token overlap,
preferred Markdown boundaries, exact-substring chunks, and lossless character
coverage.  It corrects the v1 edge case where a whole short chunk already fit
inside the overlap budget and the next chunk advanced by only one character.
"""

from __future__ import annotations

from typing import Any

from rq2b_chunking import (
    TextChunk,
    _largest_fitting_end,
    preferred_boundaries,
    tokenizer_ids,
    verify_exact_text_chunks,
)
from rq2b_common import require, sha256_json, sha256_text


CHUNKER_VERSION = "rq2b-v7-exact-markdown-chunker-v2-short-boundary-progress-fix"


def _overlap_start_v2(
    tokenizer: Any,
    text: str,
    chunk_start: int,
    chunk_end: int,
    overlap_tokens: int,
) -> int:
    if overlap_tokens <= 0:
        return chunk_end
    whole_chunk_tokens = len(tokenizer_ids(tokenizer, text[chunk_start:chunk_end]))
    if whole_chunk_tokens <= overlap_tokens:
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
    require(chunk_start < next_start <= chunk_end, "V2 overlap did not advance")
    require(
        len(tokenizer_ids(tokenizer, text[next_start:chunk_end])) <= overlap_tokens,
        "V2 overlap exceeds token ceiling",
    )
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
            tokenizer, text, start, maximum_tokens, boundaries
        )
        chunk_text = text[start:end]
        token_ids = tokenizer_ids(tokenizer, chunk_text)
        require(len(token_ids) <= maximum_tokens, "Chunk exceeds token ceiling")
        chunks.append(TextChunk(
            chunk_index=len(chunks),
            start_char=start,
            end_char=end,
            token_count=len(token_ids),
            text_sha256=sha256_text(chunk_text),
            token_ids_sha256=sha256_json(token_ids),
            ended_at_preferred_boundary=preferred,
            text=chunk_text,
        ))
        if end == len(text):
            break
        start = _overlap_start_v2(
            tokenizer, text, start, end, overlap_tokens
        )
    verify_exact_text_chunks(
        tokenizer, text, chunks, maximum_tokens=maximum_tokens
    )
    verify_v2_overlap_contract(
        tokenizer, text, chunks, overlap_tokens=overlap_tokens
    )
    return chunks


def verify_v2_overlap_contract(
    tokenizer: Any,
    text: str,
    chunks: list[TextChunk],
    *,
    overlap_tokens: int,
) -> None:
    for previous, current in zip(chunks, chunks[1:]):
        require(current.start_char <= previous.end_char, "V2 chunk gap")
        overlap = text[current.start_char:previous.end_char]
        overlap_count = len(tokenizer_ids(tokenizer, overlap))
        require(overlap_count <= overlap_tokens, "V2 overlap exceeds token ceiling")
        if previous.token_count <= overlap_tokens:
            require(
                current.start_char == previous.end_char,
                "V2 short chunk must advance directly to its end",
            )
