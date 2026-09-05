#!/usr/bin/env python3
"""Build the approved, minimal HF Jobs input bundle for native SkillRouter B1.

This local tool performs no network operation.  It is deliberately unavailable
until the exact user authorisation receipt is present and validated.  A later
separate submission step uploads the one produced tarball to the bound
checkpoint dataset and starts a Hugging Face Job.
"""

from __future__ import annotations

import argparse
import json
import tarfile
import tempfile
from pathlib import Path
from typing import Any

from rq2bv1_v3_skillrouter_primary_constants import (
    CACHE_ROOT,
    EXECUTION_PACKET_NAME,
    HF_CHECKPOINT_EVERY_FORWARDS,
    HF_CHECKPOINT_REPOSITORY,
    HF_INPUT_BUNDLE_PATH,
    HF_JOB_IMAGE,
    HF_JOB_FLAVOR,
    HF_JOB_TIMEOUT,
    HF_MAXIMUM_HARDWARE_COST_USD,
    HF_OUTPUT_PREFIX,
    MODEL,
    MODEL_FILE_SHA256,
    PREFLIGHT_ROOT,
    RESULT_ROOT,
    REVISION,
    RUN_ID,
)
from rq2b_common import relative, repo_root, require, sha256_file, write_json_new
from run_rq2bv1_v3_skillrouter_primary import _load_packet, _validate_authorisation


BUNDLE_VERSION = "rq2bv1-v3-skillrouter-primary-hf-input-bundle-v1"
AUTHORISATION_PATH = "skill_benchmark/rq2bv1/approvals/skillrouter_primary_v3_execution_authorisation.json"
BUNDLE_ROOT = "skill_benchmark/rq2bv1/hosted_packages/skillrouter_primary_v3"
BUNDLE_NAME = "input_bundle.tar.gz"
RUNTIME_CONFIG_NAME = "hf_checkpoint_runtime.json"


def _binding(root: Path, path: str) -> dict[str, str]:
    candidate = root / path
    require(candidate.is_file(), f"Required bundle input is absent: {candidate}")
    return {"path": path, "sha256": sha256_file(candidate)}


def _runtime_config(root: Path, packet_path: Path, packet: dict[str, Any], authorisation_path: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    execution_scripts = list(packet["execution_scripts"])
    sealed_paths = [
        str(packet["payload"]["path"]),
        str(packet["hosted_text_transfer"]["only_text_artifact"]["path"]),
        relative(packet_path, root),
        relative(authorisation_path, root),
    ]
    sealed_artifacts = [_binding(root, path) for path in sealed_paths]
    for binding in execution_scripts:
        require(_binding(root, str(binding["path"])) == binding, f"Execution-script hash drift: {binding['path']}")
    persistence = packet["hosting_and_persistence"]
    require(persistence["checkpoint_dataset_repository"] == HF_CHECKPOINT_REPOSITORY, "Checkpoint repo drift")
    require(persistence["input_bundle_path"] == HF_INPUT_BUNDLE_PATH, "Input bundle path drift")
    require(persistence["output_prefix"] == HF_OUTPUT_PREFIX, "Output prefix drift")
    require(
        persistence["job_image"] == HF_JOB_IMAGE
        and persistence["job_flavor"] == HF_JOB_FLAVOR
        and persistence["job_timeout"] == HF_JOB_TIMEOUT
        and float(persistence["maximum_hardware_cost_usd"]) == HF_MAXIMUM_HARDWARE_COST_USD,
        "HF Job envelope drift",
    )
    config = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hf-runtime-v1",
        "run_id": RUN_ID,
        "packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "execution_scripts": execution_scripts,
        "sealed_artifacts": sealed_artifacts,
        "text_inventory": packet["hosted_text_transfer"]["only_text_artifact"],
        "model": MODEL,
        "model_revision": REVISION,
        "model_file_sha256": MODEL_FILE_SHA256,
        "output_dir": RESULT_ROOT,
        "cache_root": CACHE_ROOT,
        "checkpoint_dataset_repository": HF_CHECKPOINT_REPOSITORY,
        "input_bundle_path": HF_INPUT_BUNDLE_PATH,
        "output_prefix": HF_OUTPUT_PREFIX,
        "checkpoint_every_model_forward_batches": HF_CHECKPOINT_EVERY_FORWARDS,
        "job_flavor": HF_JOB_FLAVOR,
        "job_timeout": HF_JOB_TIMEOUT,
        "job_image": HF_JOB_IMAGE,
        "maximum_hardware_cost_usd": HF_MAXIMUM_HARDWARE_COST_USD,
        "trust_remote_code": False,
        "gold_labels_transferred": False,
        "hosted_scoring": False,
        "automatic_retries": 0,
    }
    package_files = [*execution_scripts, *sealed_artifacts]
    deduplicated: dict[str, dict[str, str]] = {str(binding["path"]): binding for binding in package_files}
    return config, [deduplicated[path] for path in sorted(deduplicated)]


def build(root: Path) -> dict[str, Any]:
    root = root.resolve()
    packet_path, packet = _load_packet(root)
    authorisation_path = root / AUTHORISATION_PATH
    _validate_authorisation(root, authorisation_path, packet_path, packet)
    config, package_files = _runtime_config(root, packet_path, packet, authorisation_path)
    output_root = root / BUNDLE_ROOT
    output_root.mkdir(parents=True, exist_ok=True)
    bundle_path = output_root / BUNDLE_NAME
    require(not bundle_path.exists(), f"Refusing to overwrite input bundle: {bundle_path}")
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-bundle-") as directory:
        staging = Path(directory)
        runtime_path = staging / PREFLIGHT_ROOT / RUNTIME_CONFIG_NAME
        write_json_new(runtime_path, config)
        manifest = {
            "schema_version": BUNDLE_VERSION,
            "state": "sealed_local_bundle_pending_one_approved_hf_upload",
            "packet": config["packet"],
            "runtime_config": {"path": f"{PREFLIGHT_ROOT}/{RUNTIME_CONFIG_NAME}", "sha256": sha256_file(runtime_path)},
            "files": package_files,
            "hosted_text_transfer": packet["hosted_text_transfer"],
            "excluded_source_data": packet["hosted_text_transfer"]["excluded_source_data"],
            "network_calls": 0,
        }
        manifest_path = staging / "bundle_manifest.json"
        write_json_new(manifest_path, manifest)
        with tarfile.open(bundle_path, "w:gz") as archive:
            for binding in package_files:
                archive.add(root / binding["path"], arcname=binding["path"], recursive=False)
            archive.add(runtime_path, arcname=f"{PREFLIGHT_ROOT}/{RUNTIME_CONFIG_NAME}", recursive=False)
            archive.add(manifest_path, arcname="bundle_manifest.json", recursive=False)
    result = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hf-bundle-manifest-v1",
        "state": "built_locally_pending_explicit_hf_upload_and_job_submission",
        "bundle": {"path": relative(bundle_path, root), "sha256": sha256_file(bundle_path), "bytes": bundle_path.stat().st_size},
        "bundle_manifest": manifest,
        "network_calls": 0,
    }
    write_json_new(output_root / "bundle_build_manifest.json", result)
    return result


def self_test() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-bundle-test-") as directory:
        path = Path(directory) / "sample.json"
        write_json_new(path, {"ok": True})
        require(_binding(Path(directory), "sample.json")["sha256"] == sha256_file(path), "Bundle binding regression")
    return {"state": "self_test_passed_no_network_no_model_forward", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.build != args.self_test, "Choose exactly one of --build or --self-test")
    result = build(args.root) if args.build else self_test()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
