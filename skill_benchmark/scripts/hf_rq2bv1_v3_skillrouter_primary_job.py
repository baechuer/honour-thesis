#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "huggingface-hub>=0.30",
#   "safetensors>=0.5",
#   "tokenizers>=0.20",
#   "transformers>=4.51",
# ]
# ///
"""Recoverable Hugging Face Jobs wrapper for one approved SkillRouter B1 run.

The wrapper only executes after an exact local approval has been materialised
into the sealed input bundle. It uses no gold labels: it restores cached
embeddings, executes missing native-encoder batches, then uploads immutable
checkpoint archives. A checkpoint upload failure is fatal and is never retried.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


JOB_VERSION = "rq2bv1-v3-skillrouter-primary-hf-job-v1"
RUNTIME_CONFIG = "hf_checkpoint_runtime.json"


def _sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        for member in members:
            pure = PurePosixPath(member.name)
            if pure.is_absolute() or ".." in pure.parts or member.issym() or member.islnk():
                raise RuntimeError(f"Unsafe archive member in {archive.name}: {member.name}")
        try:
            handle.extractall(destination, members=members, filter="data")
        except TypeError:  # Python < 3.12; the checks above remain mandatory.
            handle.extractall(destination, members=members)


def _require_token() -> str:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is required for the approved checkpoint repository")
    return token


def _config_path(root: Path) -> Path:
    return root / "skill_benchmark/rq2bv1/preflight/skillrouter_primary_v3" / RUNTIME_CONFIG


def _load_config(root: Path) -> dict[str, Any]:
    config = _read_json(_config_path(root))
    if config.get("schema_version") != "rq2bv1-v3-skillrouter-primary-hf-runtime-v1":
        raise RuntimeError("HF runtime configuration schema drift")
    return config


def _validate_bound_files(root: Path, config: dict[str, Any]) -> None:
    for binding in config["execution_scripts"]:
        path = root / str(binding["path"])
        if not path.is_file() or _sha256_file(path) != binding["sha256"]:
            raise RuntimeError(f"Bound execution script drift: {path}")
    for binding in config["sealed_artifacts"]:
        path = root / str(binding["path"])
        if not path.is_file() or _sha256_file(path) != binding["sha256"]:
            raise RuntimeError(f"Sealed artifact drift: {path}")


def _staging_path(root: Path, config: dict[str, Any]) -> Path:
    output_root = root / str(config["output_dir"])
    staging = output_root.parent / f".{output_root.name}.staging"
    complete = output_root
    if staging.exists():
        return staging
    if complete.exists():
        return complete
    raise RuntimeError("No hosted SkillRouter staging/completed directory exists")


def _state_path(root: Path) -> Path:
    return root / "skill_benchmark/rq2bv1/preflight/skillrouter_primary_v3/hf_checkpoint_state.json"


def _load_state(root: Path) -> dict[str, Any]:
    path = _state_path(root)
    if not path.exists():
        return {"schema_version": "rq2bv1-v3-skillrouter-primary-hf-checkpoint-state-v1", "uploaded_records": [], "archives": []}
    state = _read_json(path)
    if state.get("schema_version") != "rq2bv1-v3-skillrouter-primary-hf-checkpoint-state-v1":
        raise RuntimeError("Checkpoint state schema drift")
    return state


def _record_cache_files(root: Path, record: dict[str, Any]) -> list[Path]:
    from run_rq2bv1_v3_skillrouter_primary import ExactEmbeddingCache
    from rq2b_common import read_jsonl

    config = _load_config(root)
    inventory_path = root / str(config["text_inventory"]["path"])
    inventory = {str(row["text_id"]): row for row in read_jsonl(inventory_path)}
    cache = ExactEmbeddingCache(root / str(config["cache_root"]))
    paths: list[Path] = []
    for text_id in record["text_ids"]:
        row = inventory.get(str(text_id))
        if row is None:
            raise RuntimeError(f"Checkpoint record references unknown text ID: {text_id}")
        path = cache.path(str(row["text"]))
        if not path.is_file():
            raise RuntimeError(f"Checkpoint cache is missing: {path}")
        paths.append(path)
    return paths


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _build_archive(root: Path, files: list[Path], manifest: dict[str, Any], target: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-checkpoint-") as directory:
        temporary_root = Path(directory)
        manifest_path = temporary_root / "checkpoint_manifest.json"
        _write_json(manifest_path, manifest)
        with tarfile.open(target, "w:gz") as handle:
            for path in sorted(files, key=lambda value: _relative(root, value)):
                handle.add(path, arcname=_relative(root, path), recursive=False)
            handle.add(manifest_path, arcname="checkpoint_manifest.json", recursive=False)


def _upload_once(api: Any, path: Path, *, repo_id: str, path_in_repo: str, message: str) -> None:
    print(f"UPLOAD_START path={path_in_repo}", flush=True)
    api.upload_file(
        path_or_fileobj=str(path),
        path_in_repo=path_in_repo,
        repo_id=repo_id,
        repo_type="dataset",
        commit_message=message,
    )
    print(f"UPLOAD_DONE path={path_in_repo}", flush=True)


def checkpoint_hook(root: Path, record_id: str, *, force: bool = False) -> dict[str, Any]:
    from huggingface_hub import HfApi
    from rq2bv1_v3_skillrouter_primary_constants import HF_CHECKPOINT_EVERY_FORWARDS, HF_MAX_CHECKPOINT_ARCHIVES

    root = root.resolve()
    config = _load_config(root)
    _validate_bound_files(root, config)
    staging = _staging_path(root, config)
    record_root = staging / "forward_records"
    records = {path.stem: path for path in record_root.glob("forward-*.json")}
    if record_id not in records:
        raise RuntimeError(f"Checkpoint trigger record is absent: {record_id}")
    state = _load_state(root)
    uploaded = set(str(value) for value in state["uploaded_records"])
    pending = sorted(set(records) - uploaded)
    if not force and len(pending) < HF_CHECKPOINT_EVERY_FORWARDS:
        print(f"CHECKPOINT_DEFERRED pending_records={len(pending)}", flush=True)
        return {"state": "deferred", "pending_records": len(pending)}
    if not pending:
        print("CHECKPOINT_NOT_NEEDED", flush=True)
        return {"state": "not_needed", "pending_records": 0}
    checkpoint_number = len(state["archives"]) + 1
    if checkpoint_number > HF_MAX_CHECKPOINT_ARCHIVES:
        raise RuntimeError("Checkpoint archive ceiling exceeded")
    record_paths = [records[key] for key in pending]
    parsed_records = [_read_json(path) for path in record_paths]
    cache_paths = [path for record in parsed_records for path in _record_cache_files(root, record)]
    unique_cache_paths = sorted(set(cache_paths), key=lambda path: _relative(root, path))
    manifest = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hf-checkpoint-v1",
        "run_id": config["run_id"],
        "checkpoint_number": checkpoint_number,
        "packet": config["packet"],
        "records": [
            {"record_id": path.stem, "path": _relative(root, path), "sha256": _sha256_file(path)}
            for path in record_paths
        ],
        "cache_entries": [
            {"path": _relative(root, path), "sha256": _sha256_file(path)} for path in unique_cache_paths
        ],
    }
    if checkpoint_number == 1:
        run_started = staging / "run_started.json"
        if not run_started.is_file():
            raise RuntimeError("First checkpoint lacks run_started.json")
        manifest["run_started"] = {"path": _relative(root, run_started), "sha256": _sha256_file(run_started)}
        archive_files = [run_started, *record_paths, *unique_cache_paths]
    else:
        archive_files = [*record_paths, *unique_cache_paths]
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-upload-") as directory:
        archive = Path(directory) / f"checkpoint-{checkpoint_number:03d}.tar.gz"
        _build_archive(root, archive_files, manifest, archive)
        digest = _sha256_file(archive)
        remote_path = f"{config['output_prefix']}/checkpoints/checkpoint-{checkpoint_number:03d}-{digest[:16]}.tar.gz"
        api = HfApi(token=_require_token())
        _upload_once(
            api,
            archive,
            repo_id=str(config["checkpoint_dataset_repository"]),
            path_in_repo=remote_path,
            message=f"RQ2b SkillRouter B1 immutable checkpoint {checkpoint_number:03d}",
        )
    state["uploaded_records"] = sorted(uploaded | set(pending))
    state["archives"].append({"number": checkpoint_number, "path": remote_path, "sha256": digest, "records": pending})
    _write_json(_state_path(root), state)
    print(f"CHECKPOINT_PERSISTED number={checkpoint_number} records={len(pending)}", flush=True)
    return {"state": "persisted", "checkpoint_number": checkpoint_number, "records": len(pending), "path": remote_path}


def _restore_archives(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    from huggingface_hub import HfApi, hf_hub_download

    api = HfApi(token=_require_token())
    prefix = f"{config['output_prefix']}/checkpoints/"
    remote_paths = sorted(path for path in api.list_repo_files(repo_id=config["checkpoint_dataset_repository"], repo_type="dataset") if path.startswith(prefix) and path.endswith(".tar.gz"))
    uploaded: set[str] = set()
    archives: list[dict[str, Any]] = []
    for remote_path in remote_paths:
        archive = Path(
            hf_hub_download(
                repo_id=config["checkpoint_dataset_repository"],
                repo_type="dataset",
                filename=remote_path,
                token=_require_token(),
            )
        )
        with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-restore-") as directory:
            temporary = Path(directory)
            _safe_extract(archive, temporary)
            manifest = _read_json(temporary / "checkpoint_manifest.json")
            if manifest.get("schema_version") != "rq2bv1-v3-skillrouter-primary-hf-checkpoint-v1":
                raise RuntimeError(f"Checkpoint schema drift: {remote_path}")
            if manifest.get("packet") != config["packet"]:
                raise RuntimeError(f"Checkpoint packet binding drift: {remote_path}")
            record_ids = [str(row["record_id"]) for row in manifest["records"]]
            if uploaded & set(record_ids):
                raise RuntimeError(f"Duplicate checkpoint records in remote archive: {remote_path}")
            for binding in [*manifest["records"], *manifest["cache_entries"], *([manifest["run_started"]] if "run_started" in manifest else [])]:
                candidate = temporary / binding["path"]
                if not candidate.is_file() or _sha256_file(candidate) != binding["sha256"]:
                    raise RuntimeError(f"Checkpoint file hash drift: {remote_path}:{binding['path']}")
            _safe_extract(archive, root)
            uploaded.update(record_ids)
            archives.append({"number": manifest["checkpoint_number"], "path": remote_path, "sha256": _sha256_file(archive), "records": record_ids})
    if archives:
        _write_json(
            _state_path(root),
            {
                "schema_version": "rq2bv1-v3-skillrouter-primary-hf-checkpoint-state-v1",
                "uploaded_records": sorted(uploaded),
                "archives": sorted(archives, key=lambda row: int(row["number"])),
            },
        )
    print(f"CHECKPOINT_RESTORE archives={len(archives)} records={len(uploaded)}", flush=True)
    return {"archives": len(archives), "records": len(uploaded)}


def _upload_completion(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    from huggingface_hub import HfApi

    output_root = root / str(config["output_dir"])
    files = [output_root / "manifest.json", output_root / "embedding_ledger.json"]
    if not all(path.is_file() for path in files):
        raise RuntimeError("Hosted runner did not create its completion files")
    state = _load_state(root)
    manifest = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hf-completion-v1",
        "run_id": config["run_id"],
        "packet": config["packet"],
        "checkpoint_archives": state["archives"],
        "files": [{"path": _relative(root, path), "sha256": _sha256_file(path)} for path in files],
    }
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-completion-") as directory:
        archive = Path(directory) / "completion.tar.gz"
        _build_archive(root, files, manifest, archive)
        digest = _sha256_file(archive)
        remote_path = f"{config['output_prefix']}/completion/completion-{digest[:16]}.tar.gz"
        _upload_once(
            HfApi(token=_require_token()),
            archive,
            repo_id=str(config["checkpoint_dataset_repository"]),
            path_in_repo=remote_path,
            message="RQ2b SkillRouter B1 immutable hosted completion",
        )
    print(f"COMPLETION_PERSISTED path={remote_path}", flush=True)
    return {"path": remote_path, "sha256": digest}


def execute_hosted(bundle: Path, expected_bundle_sha256: str) -> dict[str, Any]:
    from huggingface_hub import HfApi, hf_hub_download

    token = _require_token()
    bundle = bundle.resolve()
    if not bundle.is_file() or _sha256_file(bundle) != expected_bundle_sha256:
        raise RuntimeError("Downloaded input bundle hash mismatch")
    workspace = Path("/tmp/rq2bv1_skillrouter_primary")
    if workspace.exists():
        shutil.rmtree(workspace)
    _safe_extract(bundle, workspace)
    config = _load_config(workspace)
    _validate_bound_files(workspace, config)
    api = HfApi(token=token)
    api.repo_info(repo_id=config["checkpoint_dataset_repository"], repo_type="dataset")
    restored = _restore_archives(workspace, config)
    snapshot = Path(
        hf_hub_download(
            repo_id=str(config["model"]),
            repo_type="model",
            filename="config.json",
            revision=str(config["model_revision"]),
            token=token,
        )
    ).parent
    # Fetch precisely the bound files; no remote code or unbound source files.
    for filename, expected_sha256 in config["model_file_sha256"].items():
        local = Path(
            hf_hub_download(
                repo_id=str(config["model"]),
                repo_type="model",
                filename=filename,
                revision=str(config["model_revision"]),
                token=token,
            )
        )
        if _sha256_file(local) != expected_sha256:
            raise RuntimeError(f"Model-file hash mismatch: {filename}")
    os.chdir(workspace)
    sys.path.insert(0, str(workspace / "skill_benchmark/scripts"))
    hook = workspace / "skill_benchmark/scripts/hf_rq2bv1_v3_skillrouter_primary_job.py"
    os.environ["RQ2BV1_SKILLROUTER_CHECKPOINT_HOOK"] = str(hook)
    runner = workspace / "skill_benchmark/scripts/run_rq2bv1_v3_skillrouter_primary.py"
    command = [sys.executable, str(runner), "--root", str(workspace), "--execute", "--model-snapshot", str(snapshot)]
    staging = workspace / str(config["output_dir"]).replace("/hosted_embedding", "")
    if (staging / ".hosted_embedding.staging").exists():
        command.append("--resume")
    subprocess.run(command, check=True)
    checkpoint_hook(workspace, "forward-00001", force=True)
    completion = _upload_completion(workspace, config)
    result = {"state": "hosted_embedding_persisted_pending_local_scoring", "restored": restored, "completion": completion}
    print("HOSTED_COMPLETION_JSON " + json.dumps(result, sort_keys=True), flush=True)
    return result


def run_remote_entrypoint() -> int:
    input_repo = os.environ.get("RQ2BV1_SKILLROUTER_INPUT_REPOSITORY")
    input_path = os.environ.get("RQ2BV1_SKILLROUTER_INPUT_BUNDLE_PATH")
    expected_sha = os.environ.get("RQ2BV1_SKILLROUTER_INPUT_BUNDLE_SHA256")
    if not input_repo or not input_path or not expected_sha:
        raise RuntimeError("Missing bound input-bundle environment variables")
    from huggingface_hub import hf_hub_download

    local = Path(hf_hub_download(repo_id=input_repo, repo_type="dataset", filename=input_path, token=_require_token()))
    execute_hosted(local, expected_sha)
    return 0


def self_test() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-hf-job-test-") as directory:
        root = Path(directory)
        source = root / "a/b/example.json"
        source.parent.mkdir(parents=True)
        source.write_text('{"ok":true}\n', encoding="utf-8")
        target = root / "archive.tar.gz"
        _build_archive(root, [source], {"schema_version": "synthetic"}, target)
        restored = root / "restored"
        _safe_extract(target, restored)
        if (restored / "a/b/example.json").read_text(encoding="utf-8") != '{"ok":true}\n':
            raise RuntimeError("Checkpoint archive round-trip regression")
    return {"state": "self_test_passed_no_network_no_model_forward", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-hosted", action="store_true")
    parser.add_argument("--checkpoint-hook", action="store_true")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--record-id")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    modes = int(args.execute_hosted) + int(args.checkpoint_hook) + int(args.self_test)
    if modes != 1:
        raise SystemExit("Choose exactly one mode")
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
        return 0
    if args.checkpoint_hook:
        if args.root is None or not args.record_id:
            raise SystemExit("Checkpoint hook requires --root and --record-id")
        print(json.dumps(checkpoint_hook(args.root, args.record_id, force=args.force), sort_keys=True))
        return 0
    return run_remote_entrypoint()


if __name__ == "__main__":
    raise SystemExit(main())
