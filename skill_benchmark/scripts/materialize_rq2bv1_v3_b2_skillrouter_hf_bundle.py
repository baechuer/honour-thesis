#!/usr/bin/env python3
"""Build the minimal, immutable HF input bundle for RQ2b V3 B2 SkillRouter.

This is a local packaging step only.  It includes the strict-gold-free pair
inventory and the exact pinned reranker worker; it never contacts Hugging Face
or executes a model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT_DIR = ROOT / "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2"
BUNDLE_DIR = ROOT / "skill_benchmark/rq2bv1/hosted_packages/skillrouter_b2_top20_v3"
BUNDLE_PATH = BUNDLE_DIR / "input_bundle.tar.gz"
BUILD_MANIFEST_PATH = BUNDLE_DIR / "bundle_build_manifest.json"
WORKER_RELATIVE_PATH = "skill_benchmark/scripts/hf_rq2bv1_v3_b2_skillrouter_reranker_job.py"
PAIR_RELATIVE_PATH = "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2/unique_pairs.jsonl"
PREFLIGHT_MANIFEST_RELATIVE_PATH = "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2/manifest.json"
PREFLIGHT_REPORT_RELATIVE_PATH = "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2/preflight_report.json"
RUNTIME_RELATIVE_PATH = "skill_benchmark/rq2bv1/preflight/rq2bv1_v3_b2_top20_v2/hf_skillrouter_runtime.json"

MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
MODEL_FILE_SHA256 = {
    "config.json": "17f3b5063350823bfda01f740ac14b9d1cd9cb80c738cbe0d9939c4988ac6b39",
    "tokenizer.json": "ab19c66299579df20542864f9e27b79898ca05f35acc97fd9259aee385a07d4a",
    "model.safetensors": "34064850b1b512168309481a9cebe4ecaf55d0821bf22608f657b40033ed36d7",
}
CHECKPOINT_REPOSITORY = "baechuer1/honour-thesis-rq2b-checkpoints"
INPUT_BUNDLE_PATH = "rq2bv1/skillrouter-reranker-b2-top20-v3/input_bundle.tar.gz"
OUTPUT_PREFIX = "rq2bv1/skillrouter-reranker-b2-top20-v3"
SHARD_PAIR_COUNT = 5000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json_new(path: Path, value: dict[str, Any]) -> None:
    require(not path.exists(), f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _binding(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    require(path.is_file(), f"Required B2 input is missing: {path}")
    return {"path": relative_path, "sha256": sha256_file(path), "bytes": path.stat().st_size}


def _load_preflight() -> dict[str, Any]:
    manifest = json.loads((ROOT / PREFLIGHT_MANIFEST_RELATIVE_PATH).read_text(encoding="utf-8"))
    report = json.loads((ROOT / PREFLIGHT_REPORT_RELATIVE_PATH).read_text(encoding="utf-8"))
    require(manifest["state"] == "prepared_local_zero_network_no_reranker_execution", "B2 preflight state drift")
    pair = manifest["artifacts"]["unique_pairs"]
    require(pair == {"path": PAIR_RELATIVE_PATH, "rows": 73415, "sha256": "73d6a43feade33db3637c3274a37385348b880d04fb9ccd8ed91a6d2031ab9ea"}, "B2 pair inventory drift")
    skillrouter = report["skillrouter_windowing"]
    require(skillrouter["model"] == MODEL and skillrouter["revision"] == REVISION, "B2 SkillRouter model drift")
    require(skillrouter["unique_model_input_tokens"] == 36350664, "B2 token-total drift")
    require(skillrouter["max_pair_input_tokens"] == 2032, "B2 pair limit drift")
    return {"manifest": manifest, "report": report}


def build(*, bundle_dir: Path = BUNDLE_DIR, input_bundle_path: str = INPUT_BUNDLE_PATH, output_prefix: str = OUTPUT_PREFIX) -> dict[str, Any]:
    bundle_dir = bundle_dir.resolve()
    bundle_path = bundle_dir / "input_bundle.tar.gz"
    build_manifest_path = bundle_dir / "bundle_build_manifest.json"
    require(not bundle_path.exists() and not build_manifest_path.exists(), "Existing B2 SkillRouter bundle requires inspection; it will not be replaced")
    preflight = _load_preflight()
    bindings = [_binding(path) for path in (WORKER_RELATIVE_PATH, PAIR_RELATIVE_PATH, PREFLIGHT_MANIFEST_RELATIVE_PATH, PREFLIGHT_REPORT_RELATIVE_PATH)]
    runtime = {
        "schema_version": "rq2bv1-v3-b2-skillrouter-hf-runtime-v1",
        "state": "sealed_local_bundle_pending_one_hosted_job",
        "worker": next(item for item in bindings if item["path"] == WORKER_RELATIVE_PATH),
        "unique_pairs": next(item for item in bindings if item["path"] == PAIR_RELATIVE_PATH),
        "preflight_manifest": next(item for item in bindings if item["path"] == PREFLIGHT_MANIFEST_RELATIVE_PATH),
        "preflight_report": next(item for item in bindings if item["path"] == PREFLIGHT_REPORT_RELATIVE_PATH),
        "model": {"name": MODEL, "revision": REVISION, "files": MODEL_FILE_SHA256, "trust_remote_code": False},
        "scope": {"unique_pairs": 73415, "unique_model_input_tokens": 36350664, "max_pair_input_tokens": 2032, "strict_b2_conditions": 4572, "primary_k": 20},
        "checkpointing": {"repository": CHECKPOINT_REPOSITORY, "input_bundle_path": input_bundle_path, "output_prefix": output_prefix, "pairs_per_score_shard": SHARD_PAIR_COUNT, "automatic_retries": 0},
        "data_boundary": {"transferred_fields": ["pair_id", "query", "window_text", "pair_input_token_count", "representation", "skill_id", "prompt_id"], "excluded_fields": ["gold_skill", "valid_skills", "cluster", "group", "stratum", "candidate_list", "metric", "result"]},
    }
    bundle_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rq2bv1-b2-sr-bundle-") as temporary:
        staging = Path(temporary)
        runtime_path = staging / RUNTIME_RELATIVE_PATH
        runtime_path.parent.mkdir(parents=True, exist_ok=True)
        runtime_path.write_text(json.dumps(runtime, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        bundle_manifest = {
            "schema_version": "rq2bv1-v3-b2-skillrouter-hf-input-bundle-v1",
            "state": "sealed_local_bundle_pending_one_hosted_job",
            "files": bindings,
            "runtime": {"path": RUNTIME_RELATIVE_PATH, "sha256": sha256_file(runtime_path)},
            "network_calls": 0,
        }
        manifest_path = staging / "bundle_manifest.json"
        manifest_path.write_text(json.dumps(bundle_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with tarfile.open(bundle_path, "w:gz") as archive:
            for binding in bindings:
                archive.add(ROOT / binding["path"], arcname=binding["path"], recursive=False)
            archive.add(runtime_path, arcname=RUNTIME_RELATIVE_PATH, recursive=False)
            archive.add(manifest_path, arcname="bundle_manifest.json", recursive=False)
    result = {
        "schema_version": "rq2bv1-v3-b2-skillrouter-hf-bundle-build-v1",
        "state": "built_locally_pending_upload_and_hosted_job",
        "bundle": {"path": str(bundle_path.relative_to(ROOT)), "sha256": sha256_file(bundle_path), "bytes": bundle_path.stat().st_size},
        "runtime": runtime,
        "preflight": {"manifest_sha256": sha256_file(ROOT / PREFLIGHT_MANIFEST_RELATIVE_PATH), "report_sha256": sha256_file(ROOT / PREFLIGHT_REPORT_RELATIVE_PATH)},
        "network_calls": 0,
        "model_forward_passes": 0,
    }
    write_json_new(build_manifest_path, result)
    return result


def self_test() -> dict[str, Any]:
    preflight = _load_preflight()
    return {"state": "passed_local_zero_network_no_model_forward", "unique_pairs": preflight["manifest"]["artifacts"]["unique_pairs"]["rows"], "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--bundle-dir", default=str(BUNDLE_DIR))
    parser.add_argument("--input-bundle-path", default=INPUT_BUNDLE_PATH)
    parser.add_argument("--output-prefix", default=OUTPUT_PREFIX)
    args = parser.parse_args()
    require(args.build != args.self_test, "Choose exactly one of --build or --self-test")
    result = build(bundle_dir=Path(args.bundle_dir), input_bundle_path=args.input_bundle_path, output_prefix=args.output_prefix) if args.build else self_test()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
