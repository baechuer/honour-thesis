#!/usr/bin/env python3
"""Recover immutable hosted SkillRouter B1 artifacts for local-only scoring."""

from __future__ import annotations

import argparse
import json
import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from rq2bv1_v3_skillrouter_primary_constants import HF_CHECKPOINT_REPOSITORY, HF_MAX_CHECKPOINT_ARCHIVES, HF_OUTPUT_PREFIX, PREFLIGHT_ROOT
from rq2b_common import relative, repo_root, require, sha256_file, write_json_new
from run_rq2bv1_v3_skillrouter_primary import _load_packet, _validate_authorisation


AUTHORISATION_PATH = "skill_benchmark/rq2bv1/approvals/skillrouter_primary_v3_execution_authorisation.json"
RECOVERY_ROOT = "skill_benchmark/rq2bv1/results/skillrouter_primary_v3/recovery"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def _safe_extract(archive: Path, destination: Path) -> None:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        for member in members:
            path = PurePosixPath(member.name)
            require(not path.is_absolute() and ".." not in path.parts and not member.issym() and not member.islnk(), f"Unsafe archive member: {member.name}")
        try:
            handle.extractall(destination, members=members, filter="data")
        except TypeError:  # Python < 3.12; the checks above remain mandatory.
            handle.extractall(destination, members=members)


def _copy_bound(root: Path, temporary: Path, bindings: list[dict[str, Any]]) -> None:
    for binding in bindings:
        source = temporary / str(binding["path"])
        target = root / str(binding["path"])
        require(source.is_file() and sha256_file(source) == binding["sha256"], f"Recovered archive hash drift: {binding['path']}")
        if target.exists():
            require(sha256_file(target) == binding["sha256"], f"Refusing to overwrite divergent recovered file: {target}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def recover(root: Path) -> dict[str, Any]:
    from huggingface_hub import HfApi, hf_hub_download

    root = root.resolve()
    packet_path, packet = _load_packet(root)
    authorisation = root / AUTHORISATION_PATH
    _validate_authorisation(root, authorisation, packet_path, packet)
    persistence = packet["hosting_and_persistence"]
    require(persistence["checkpoint_dataset_repository"] == HF_CHECKPOINT_REPOSITORY, "Checkpoint repository drift")
    require(persistence["output_prefix"] == HF_OUTPUT_PREFIX, "Checkpoint output-prefix drift")
    import os

    token = os.environ.get("HF_TOKEN")
    require(bool(token), "HF_TOKEN is required to recover the approved hosted artifacts")
    api = HfApi(token=token)
    files = api.list_repo_files(repo_id=HF_CHECKPOINT_REPOSITORY, repo_type="dataset")
    checkpoint_prefix = f"{HF_OUTPUT_PREFIX}/checkpoints/"
    completion_prefix = f"{HF_OUTPUT_PREFIX}/completion/"
    checkpoint_paths = sorted(path for path in files if path.startswith(checkpoint_prefix) and path.endswith(".tar.gz"))
    completion_paths = sorted(path for path in files if path.startswith(completion_prefix) and path.endswith(".tar.gz"))
    require(0 < len(checkpoint_paths) <= HF_MAX_CHECKPOINT_ARCHIVES, "Checkpoint archive count is outside the authorised bound")
    require(len(completion_paths) == 1, "Expected exactly one immutable completion archive")
    packet_binding = {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}
    seen_records: set[str] = set()
    recovered_archives: list[dict[str, Any]] = []
    for remote_path in checkpoint_paths:
        archive = Path(hf_hub_download(repo_id=HF_CHECKPOINT_REPOSITORY, repo_type="dataset", filename=remote_path, token=token))
        with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-recover-") as directory:
            temporary = Path(directory)
            _safe_extract(archive, temporary)
            manifest = _read_json(temporary / "checkpoint_manifest.json")
            require(manifest.get("schema_version") == "rq2bv1-v3-skillrouter-primary-hf-checkpoint-v1", "Checkpoint schema drift")
            require(manifest.get("packet") == packet_binding, "Checkpoint packet binding drift")
            records = list(manifest["records"])
            record_ids = {str(row["record_id"]) for row in records}
            require(not (seen_records & record_ids), f"Duplicate recovered forward record: {remote_path}")
            seen_records.update(record_ids)
            bindings = [*records, *list(manifest["cache_entries"])]
            if "run_started" in manifest:
                bindings.append(manifest["run_started"])
            _copy_bound(root, temporary, bindings)
            recovered_archives.append({"path": remote_path, "sha256": sha256_file(archive), "records": len(records)})
    completion_remote = completion_paths[0]
    completion = Path(hf_hub_download(repo_id=HF_CHECKPOINT_REPOSITORY, repo_type="dataset", filename=completion_remote, token=token))
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-completion-recover-") as directory:
        temporary = Path(directory)
        _safe_extract(completion, temporary)
        manifest = _read_json(temporary / "checkpoint_manifest.json")
        require(manifest.get("schema_version") == "rq2bv1-v3-skillrouter-primary-hf-completion-v1", "Completion schema drift")
        require(manifest.get("packet") == packet_binding, "Completion packet binding drift")
        _copy_bound(root, temporary, list(manifest["files"]))
    recovery_root = root / RECOVERY_ROOT
    require(not recovery_root.exists(), f"Refusing to overwrite recovery manifest: {recovery_root}")
    recovery_root.mkdir(parents=True, exist_ok=False)
    result = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hf-recovery-v1",
        "state": "hosted_artifacts_recovered_and_verified_pending_local_scoring",
        "packet": packet_binding,
        "checkpoint_archives": recovered_archives,
        "completion_archive": {"path": completion_remote, "sha256": sha256_file(completion)},
        "recovered_forward_records": len(seen_records),
        "network_calls": "Hub artifact download only; no model forward or scoring",
    }
    write_json_new(recovery_root / "recovery_manifest.json", result)
    return result


def self_test() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="rq2bv1-sr-recover-test-") as directory:
        root = Path(directory)
        source = root / "source/a.json"
        source.parent.mkdir(parents=True)
        source.write_text('{"a":1}\n', encoding="utf-8")
        archive = root / "sample.tar.gz"
        with tarfile.open(archive, "w:gz") as handle:
            handle.add(source, arcname="source/a.json", recursive=False)
        destination = root / "destination"
        _safe_extract(archive, destination)
        require((destination / "source/a.json").read_text(encoding="utf-8") == '{"a":1}\n', "Archive extraction regression")
    return {"state": "self_test_passed_no_network_no_model_forward", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--recover", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.recover != args.self_test, "Choose exactly one of --recover or --self-test")
    result = recover(args.root) if args.recover else self_test()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
