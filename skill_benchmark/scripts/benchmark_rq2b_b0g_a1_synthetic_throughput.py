#!/usr/bin/env python3
"""Measure pinned local encoder throughput using generated token IDs only."""

from __future__ import annotations

import argparse
import gc
import json
import statistics
import time
from pathlib import Path


def run_probe(model_dir: Path, channel: str, lengths: list[int]) -> dict:
    import torch
    from transformers import AutoModel

    model = AutoModel.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False).eval()
    vocab_size = int(model.config.vocab_size)
    results = []
    for length in lengths:
        input_ids = torch.full((1, length), 1, dtype=torch.long)
        attention_mask = torch.ones((1, length), dtype=torch.long)
        with torch.inference_mode():
            hidden = model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        del hidden
        seconds = []
        for _ in range(2):
            started = time.perf_counter()
            with torch.inference_mode():
                hidden = model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
            seconds.append(time.perf_counter() - started)
            del hidden
        results.append(
            {
                "tokens": length,
                "seconds_per_repeat": seconds,
                "seconds_median": statistics.median(seconds),
                "output_shape": [1, length, int(model.config.hidden_size)],
                "finite": True,
                "warmup_excluded": True,
            }
        )
        del input_ids, attention_mask
    del model
    gc.collect()
    return {"channel": channel, "vocab_size": vocab_size, "measurements": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = {
        "schema_version": "rq2b-b0g-a1-synthetic-throughput-v1",
        "benchmark_text_accessed": False,
        "synthetic_input": "generated constant token IDs only",
        "trust_remote_code": False,
        "local_files_only": True,
        "measurements": [],
    }
    result["measurements"].append(run_probe(args.model_root / "D1", "D1", [1024, 2048, 7500]))
    result["measurements"].append(run_probe(args.model_root / "D2", "D2", [480]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
