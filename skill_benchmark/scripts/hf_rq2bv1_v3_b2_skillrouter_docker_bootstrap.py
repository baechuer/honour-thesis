"""Docker entrypoint for the pinned RQ2b V3 SkillRouter B2 worker.

Hugging Face Jobs receives this exact source as an inline command only after
the selected PyTorch Docker image has installed the pinned Hub/Transformers
helpers.  Keeping it as a locally compiled source prevents submission-time
quoting errors from being mistaken for a reranker experiment failure.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath

from huggingface_hub import HfApi, hf_hub_download


WORKSPACE = Path("/tmp/rq2bv1_v3_b2_skillrouter_bootstrap")
WORKER_RELATIVE_PATH = "skill_benchmark/scripts/hf_rq2bv1_v3_b2_skillrouter_reranker_job.py"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_extract(archive: Path, destination: Path) -> None:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        for member in members:
            pure = PurePosixPath(member.name)
            if pure.is_absolute() or ".." in pure.parts or member.issym() or member.islnk():
                raise RuntimeError(f"Unsafe input bundle member: {member.name}")
        try:
            handle.extractall(destination, members=members, filter="data")
        except TypeError:
            handle.extractall(destination, members=members)


def main() -> int:
    token = os.environ["HF_TOKEN"]
    auth = HfApi(token=token).whoami().get("auth", {}).get("accessToken", {})
    auth_summary = {
        "role": auth.get("role"),
        "global_permissions": auth.get("fineGrained", {}).get("global", []),
        "scoped_permission_count": sum(
            len(scope.get("permissions", []))
            for scope in auth.get("fineGrained", {}).get("scoped", [])
        ),
    }
    print("JOB_TOKEN_AUTH " + json.dumps(auth_summary, sort_keys=True), flush=True)
    repository = os.environ["RQ2BV1_B2_SR_INPUT_REPOSITORY"]
    filename = os.environ["RQ2BV1_B2_SR_INPUT_BUNDLE_PATH"]
    expected_sha256 = os.environ["RQ2BV1_B2_SR_INPUT_BUNDLE_SHA256"]
    bundle = Path(
        hf_hub_download(
            repo_id=repository,
            repo_type="dataset",
            filename=filename,
            token=token,
        )
    )
    if _sha256_file(bundle) != expected_sha256:
        raise RuntimeError("Input bundle SHA-256 mismatch")
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)
    _safe_extract(bundle, WORKSPACE)
    worker = WORKSPACE / WORKER_RELATIVE_PATH
    if not worker.is_file():
        raise RuntimeError("B2 SkillRouter worker missing from input bundle")
    subprocess.run([sys.executable, str(worker), "--execute-hosted"], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
