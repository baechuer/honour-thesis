#!/usr/bin/env python3
"""Upload one sealed RQ2b V3 SkillRouter input bundle to Hugging Face.

This is the sole input-bundle uploader for the native SkillRouter B1 job.  It
is fail-closed: it requires the exact execution receipt, validates both the
packet and the local bundle, makes at most one repository-creation attempt and
one content-upload attempt, and never retries either action.  A remote bundle
that already has the same digest is reused without a write; a different object
at the sealed path is an error.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from materialize_rq2bv1_v3_skillrouter_primary_hf_bundle import (
    AUTHORISATION_PATH,
    BUNDLE_ROOT,
)
from rq2b_common import read_json, relative, repo_root, require, sha256_file, write_json_new
from rq2bv1_v3_skillrouter_primary_constants import (
    EXECUTION_PACKET_NAME,
    HF_CHECKPOINT_REPOSITORY,
    HF_INPUT_BUNDLE_PATH,
    PREFLIGHT_ROOT,
)
from run_rq2bv1_v3_skillrouter_primary import _load_packet, _validate_authorisation


UPLOAD_RECEIPT_NAME = "input_bundle_upload_receipt.json"


def _load_build_manifest(root: Path, packet_path: Path) -> tuple[Path, dict[str, Any], Path]:
    manifest_path = root / BUNDLE_ROOT / "bundle_build_manifest.json"
    require(manifest_path.is_file(), "Local SkillRouter input-bundle manifest is absent")
    manifest = read_json(manifest_path)
    require(
        manifest.get("schema_version") == "rq2bv1-v3-skillrouter-primary-hf-bundle-manifest-v1",
        "SkillRouter input-bundle manifest schema drift",
    )
    require(
        manifest.get("state") == "built_locally_pending_explicit_hf_upload_and_job_submission",
        "SkillRouter input bundle is not pending its one approved upload",
    )
    require(
        manifest.get("bundle_manifest", {}).get("packet")
        == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "SkillRouter input-bundle packet binding drift",
    )
    bundle = root / str(manifest.get("bundle", {}).get("path", ""))
    require(bundle.is_file(), "Local SkillRouter input bundle is absent")
    require(sha256_file(bundle) == manifest["bundle"]["sha256"], "Local SkillRouter input-bundle hash drift")
    return manifest_path, manifest, bundle


def _remote_same_or_absent(api: Any, token: str, bundle: Path) -> str:
    """Return whether the sealed remote path is absent, or already exact."""

    from huggingface_hub import hf_hub_download
    from huggingface_hub.errors import RepositoryNotFoundError

    try:
        remote_paths = set(api.list_repo_files(repo_id=HF_CHECKPOINT_REPOSITORY, repo_type="dataset"))
    except RepositoryNotFoundError:
        return "repository_absent"
    if HF_INPUT_BUNDLE_PATH not in remote_paths:
        return "path_absent"
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-upload-verify-") as directory:
        downloaded = Path(
            hf_hub_download(
                repo_id=HF_CHECKPOINT_REPOSITORY,
                repo_type="dataset",
                filename=HF_INPUT_BUNDLE_PATH,
                token=token,
                local_dir=directory,
            )
        )
        require(sha256_file(downloaded) == sha256_file(bundle), "Remote input bundle exists but has a different hash")
    return "already_exact"


def upload(root: Path) -> dict[str, Any]:
    root = root.resolve()
    packet_path, packet = _load_packet(root)
    _validate_authorisation(root, root / AUTHORISATION_PATH, packet_path, packet)
    manifest_path, manifest, bundle = _load_build_manifest(root, packet_path)
    persistence = packet["hosting_and_persistence"]
    require(persistence["checkpoint_dataset_repository"] == HF_CHECKPOINT_REPOSITORY, "Checkpoint repository drift")
    require(persistence["input_bundle_path"] == HF_INPUT_BUNDLE_PATH, "Input bundle path drift")
    token = os.environ.get("HF_TOKEN")
    require(bool(token), "HF_TOKEN is required for the approved one-time bundle upload")

    from huggingface_hub import HfApi

    api = HfApi(token=token)
    remote_state = _remote_same_or_absent(api, token, bundle)
    repository_creation_attempts = 0
    upload_attempts = 0
    if remote_state == "repository_absent":
        repository_creation_attempts = 1
        api.create_repo(repo_id=HF_CHECKPOINT_REPOSITORY, repo_type="dataset", exist_ok=False)
        remote_state = "path_absent"
    if remote_state == "path_absent":
        upload_attempts = 1
        api.upload_file(
            path_or_fileobj=str(bundle),
            path_in_repo=HF_INPUT_BUNDLE_PATH,
            repo_id=HF_CHECKPOINT_REPOSITORY,
            repo_type="dataset",
            commit_message="RQ2b V3 SkillRouter sealed input bundle",
        )
        outcome = "uploaded_once"
    else:
        require(remote_state == "already_exact", "Unexpected remote input-bundle state")
        outcome = "already_uploaded_exact_no_write"

    receipt = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hf-input-upload-receipt-v1",
        "state": outcome,
        "packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "bundle_manifest": {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)},
        "bundle": {"path": relative(bundle, root), "sha256": sha256_file(bundle), "bytes": bundle.stat().st_size},
        "repository": HF_CHECKPOINT_REPOSITORY,
        "path_in_repository": HF_INPUT_BUNDLE_PATH,
        "repository_creation_attempts": repository_creation_attempts,
        "upload_attempts": upload_attempts,
        "automatic_retries": 0,
        "job_submission": {
            "wrapper": {
                "path": "skill_benchmark/scripts/hf_rq2bv1_v3_skillrouter_primary_job.py",
                "sha256": next(
                    row["sha256"]
                    for row in packet["execution_scripts"]
                    if row["path"] == "skill_benchmark/scripts/hf_rq2bv1_v3_skillrouter_primary_job.py"
                ),
            },
            "environment": {
                "RQ2BV1_SKILLROUTER_INPUT_REPOSITORY": HF_CHECKPOINT_REPOSITORY,
                "RQ2BV1_SKILLROUTER_INPUT_BUNDLE_PATH": HF_INPUT_BUNDLE_PATH,
                "RQ2BV1_SKILLROUTER_INPUT_BUNDLE_SHA256": sha256_file(bundle),
            },
        },
    }
    receipt_path = root / BUNDLE_ROOT / UPLOAD_RECEIPT_NAME
    require(not receipt_path.exists(), f"Refusing to overwrite input-upload receipt: {receipt_path}")
    write_json_new(receipt_path, receipt)
    return receipt


def self_test() -> dict[str, Any]:
    return {
        "state": "self_test_passed_no_network_no_model_forward",
        "upload_attempts": 0,
        "automatic_retries": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.upload != args.self_test, "Choose exactly one of --upload or --self-test")
    result = upload(args.root) if args.upload else self_test()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
