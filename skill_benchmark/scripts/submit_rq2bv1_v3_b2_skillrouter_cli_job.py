#!/usr/bin/env python3
"""Submit the frozen RQ2b V3 B2 SkillRouter Docker job via the HF CLI.

The CLI's ``--secrets HF_TOKEN`` form binds the locally authenticated,
write-capable credential as an encrypted job secret. The command deliberately
installs the pinned Hub/Transformers helpers before executing the bootstrap;
the base PyTorch image does not provide them.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = ROOT / "skill_benchmark/scripts/hf_rq2bv1_v3_b2_skillrouter_docker_bootstrap.py"
IMAGE = "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime"
REPOSITORY = "baechuer1/honour-thesis-rq2b-checkpoints"
BUNDLE_PATH = "rq2bv1/skillrouter-reranker-b2-top20-v3/input_bundle.tar.gz"
BUNDLE_SHA256 = "583cdc62fb7584f16d54e60261da0eb6e6ee6e38089838e76b8d2880517bba28"
DEPENDENCIES = ["huggingface-hub==0.36.2", "transformers==4.57.6", "safetensors==0.7.0"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_command(*, bundle_path: str = BUNDLE_PATH, bundle_sha256: str = BUNDLE_SHA256) -> tuple[list[str], dict[str, object]]:
    source = BOOTSTRAP.read_bytes()
    bootstrap_b64 = base64.b64encode(source).decode("ascii")
    bootstrap_command = (
        "import base64; source=base64.b64decode(" + repr(bootstrap_b64) + "); "
        "exec(compile(source, '<rq2bv1_b2_skillrouter_bootstrap>', 'exec'))"
    )
    inner_command = " ".join(
        [
            "python -m pip install --no-cache-dir " + " ".join(DEPENDENCIES),
            "&&",
            "python -c " + repr(bootstrap_command),
        ]
    )
    command = [
        "hf",
        "jobs",
        "run",
        "-d",
        "--flavor",
        "a10g-small",
        "--timeout",
        "6h",
        "--secrets",
        "HF_TOKEN",
        "--env",
        f"RQ2BV1_B2_SR_INPUT_REPOSITORY={REPOSITORY}",
        "--env",
        f"RQ2BV1_B2_SR_INPUT_BUNDLE_PATH={bundle_path}",
        "--env",
        f"RQ2BV1_B2_SR_INPUT_BUNDLE_SHA256={bundle_sha256}",
        IMAGE,
        "bash",
        "-lc",
        inner_command,
    ]
    summary: dict[str, object] = {
        "image": IMAGE,
        "flavor": "a10g-small",
        "timeout": "6h",
        "secret_key": "HF_TOKEN",
        "dependency_install": DEPENDENCIES,
        "bootstrap": {"path": str(BOOTSTRAP.relative_to(ROOT)), "sha256": sha256_file(BOOTSTRAP)},
        "bundle": {"repository": REPOSITORY, "path": bundle_path, "sha256": bundle_sha256},
        "network_submission": True,
    }
    return command, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--bundle-path", default=BUNDLE_PATH)
    parser.add_argument("--bundle-sha256", default=BUNDLE_SHA256)
    args = parser.parse_args()
    command, summary = build_command(bundle_path=args.bundle_path, bundle_sha256=args.bundle_sha256)
    if args.dry_run:
        print(json.dumps({"command_prefix": command[:18], "summary": summary}, sort_keys=True))
        return 0
    subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
