#!/usr/bin/env python3
"""Download pinned audit-only encoders and run a zero-benchmark-text smoke test."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path


MAX_STORAGE_BYTES = 8 * 1024**3
DOWNLOAD_TIMEOUT_SECONDS = 900
SYNTHETIC_TEXTS = [
    "synthetic audit query for local runtime verification",
    "synthetic audit passage for local runtime verification",
]
MODELS = [
    {
        "channel": "D1",
        "repository": "BAAI/bge-m3",
        "revision": "5617a9f61b028005a4858fdac845db406aefb181",
        "files": [
            "config.json",
            "pytorch_model.bin",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "sentencepiece.bpe.model",
        ],
    },
    {
        "channel": "D2",
        "repository": "intfloat/e5-large-v2",
        "revision": "f169b11e22de13617baa190a028a32f3493550b6",
        "files": [
            "config.json",
            "model.safetensors",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
        ],
    },
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def directory_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def download_model(model: dict, model_root: Path) -> dict:
    target = model_root / model["channel"]
    target.mkdir(parents=True, exist_ok=True)
    before = directory_bytes(model_root)
    require(before <= MAX_STORAGE_BYTES, "A1 storage ceiling already exceeded before download")
    files = []
    for relative in model["files"]:
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".a1-partial")
        url = f"https://huggingface.co/{model['repository']}/resolve/{model['revision']}/{relative}"
        command = [
            "curl",
            "--fail",
            "--location",
            "--retry",
            "0",
            "--connect-timeout",
            "30",
            "--max-time",
            str(DOWNLOAD_TIMEOUT_SECONDS),
            "--silent",
            "--show-error",
            "--output",
            str(temporary),
        ]
        if temporary.exists() and temporary.stat().st_size > 0:
            command.extend(["--continue-at", "-"])
        command.append(url)
        try:
            completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=DOWNLOAD_TIMEOUT_SECONDS + 30)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(
                f"download timed out for {model['channel']}/{relative} after {DOWNLOAD_TIMEOUT_SECONDS} seconds"
            ) from error
        require(completed.returncode == 0, f"download failed for {model['channel']}/{relative}: {completed.stderr.strip()}")
        require(temporary.is_file() and temporary.stat().st_size > 0, f"empty download for {model['channel']}/{relative}")
        os.replace(temporary, path)
        require(directory_bytes(model_root) <= MAX_STORAGE_BYTES, "A1 storage ceiling exceeded during download")
        require(path.is_file(), f"missing downloaded file: {path}")
        files.append(
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    after = directory_bytes(model_root)
    return {
        "channel": model["channel"],
        "repository": model["repository"],
        "revision": model["revision"],
        "download_mechanism": "curl --location --retry 0 against immutable Hugging Face resolve URLs",
        "storage_before_bytes": before,
        "storage_after_bytes": after,
        "files": files,
    }


def smoke_model(channel: str, target: Path) -> dict:
    import torch
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(target, local_files_only=True, trust_remote_code=False)
    model = AutoModel.from_pretrained(target, local_files_only=True, trust_remote_code=False).eval()
    encoded = tokenizer(SYNTHETIC_TEXTS, padding=True, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**encoded).last_hidden_state
    mask = encoded["attention_mask"].unsqueeze(-1).to(hidden.dtype)
    vectors = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1)
    values = vectors.flatten().tolist()
    require(all(math.isfinite(value) for value in values), f"non-finite synthetic vector value for {channel}")
    return {
        "channel": channel,
        "synthetic_text_count": len(SYNTHETIC_TEXTS),
        "input_shape": list(encoded["input_ids"].shape),
        "embedding_shape": list(vectors.shape),
        "model_max_position_embeddings": int(getattr(model.config, "max_position_embeddings", -1)),
        "dtype": str(hidden.dtype),
        "trust_remote_code": False,
        "local_files_only": True,
        "finite_values": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    result = {
        "schema_version": "rq2b-b0g-a1-local-model-preflight-v1",
        "stage": "B0G Stage A1",
        "state": "STARTED",
        "benchmark_text_accessed": False,
        "provider_or_paid_calls": 0,
        "automatic_retries": 0,
        "trust_remote_code": False,
        "synthetic_texts_only": True,
        "max_storage_bytes": MAX_STORAGE_BYTES,
        "models": [],
        "smoke": [],
    }
    try:
        for model in MODELS:
            result["models"].append(download_model(model, args.model_root))
        for model in MODELS:
            result["smoke"].append(smoke_model(model["channel"], args.model_root / model["channel"]))
        result["state"] = "PASS"
    except BaseException as error:
        result["state"] = "FAILED_CLOSED"
        result["error_type"] = type(error).__name__
        result["error"] = str(error) or "execution interrupted without a message"
        write_json(args.output_dir / "a1_result.json", result)
        return 130 if isinstance(error, KeyboardInterrupt) else 1
    write_json(args.output_dir / "a1_result.json", result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
