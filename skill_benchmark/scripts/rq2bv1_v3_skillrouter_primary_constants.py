"""Immutable identifiers shared by the RQ2b V3 native SkillRouter run."""

from __future__ import annotations

from pathlib import Path


PREFLIGHT_VERSION = "rq2bv1-v3-skillrouter-primary-preflight-v2"
PREFLIGHT_ROOT = "skill_benchmark/rq2bv1/preflight/skillrouter_primary_v3"
TEXT_INVENTORY_NAME = "text_inventory.jsonl"
PAYLOAD_NAME = "payload_manifest.json"
REPORT_NAME = "preflight_report.json"
CHECKPOINT_NAME = "preflight_checkpoint.json"
EXECUTION_PACKET_NAME = "execution_approval_packet.json"

MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
REVISION = "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
DIMENSIONS = 1024
MAX_MODEL_TOKENS = 32768
QUERY_INSTRUCTION = (
    "Instruct: Given a task description, retrieve the most relevant "
    "skill document that would help an agent complete the task\nQuery:"
)

# The exact revision has a standard Transformers implementation.  Remote code
# is intentionally disabled, and every model/tokenizer file it needs is bound.
MODEL_FILE_SHA256 = {
    "added_tokens.json": "c0284b582e14987fbd3d5a2cb2bd139084371ed9acbae488829a1c900833c680",
    "config.json": "02b34f6be10ee6a35304e32b67ac37be4b2b04e327efff49a689136b0913a0e8",
    "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "model.safetensors": "cbab45b8a3c786b8c23aedb24fb22aff74d0e9b62a52369a3090c37f26b00360",
    "special_tokens_map.json": "76862e765266b85aa9459767e33cbaf13970f327a0e88d1c65846c2ddd3a1ecd",
    "tokenizer.json": "def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a",
    "tokenizer_config.json": "7f33cbb21bae9b2ed4a7396d68f9f10d6280d75332d04911cd6c5a0967bd10c9",
    "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
}
TOKENIZER_SHA256 = MODEL_FILE_SHA256["tokenizer.json"]
MODEL_CONFIG_SHA256 = MODEL_FILE_SHA256["config.json"]
MODEL_WEIGHTS_SHA256 = MODEL_FILE_SHA256["model.safetensors"]
TOKENIZER_BLOB = Path.home() / (
    ".cache/huggingface/hub/models--pipizhao--SkillRouter-Embedding-0.6B/"
    f"blobs/{TOKENIZER_SHA256}"
)

REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3-flat-evidence",
    "i3c-fielded-evidence",
)
RUN_ID = "rq2bv1-v3-skillrouter-primary-001"
RESULT_ROOT = "skill_benchmark/rq2bv1/results/skillrouter_primary_v3"
CACHE_ROOT = "skill_benchmark/cache/rq2bv1/embeddings/skillrouter-primary-v3"
MAX_BATCH_SIZE = 8
MAX_PADDED_MODEL_TOKENS_PER_FORWARD = 32768

HF_CHECKPOINT_REPOSITORY = "baechuer1/honour-thesis-rq2b-checkpoints"
HF_INPUT_BUNDLE_PATH = "rq2bv1/skillrouter-primary-v3-001/input_bundle.tar.gz"
HF_OUTPUT_PREFIX = "rq2bv1/skillrouter-primary-v3-001"
HF_CHECKPOINT_EVERY_FORWARDS = 25
HF_MAX_CHECKPOINT_ARCHIVES = 61
HF_JOB_FLAVOR = "a10g-small"
HF_JOB_TIMEOUT = "6h"
HF_JOB_IMAGE = "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime"
HF_MAXIMUM_HARDWARE_COST_USD = 6.00
