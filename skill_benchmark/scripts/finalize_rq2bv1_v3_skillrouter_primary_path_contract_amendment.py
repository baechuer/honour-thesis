#!/usr/bin/env python3
"""Run the approved local SkillRouter finaliser with its verified result-root path."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import finalize_rq2bv1_v3_skillrouter_primary as base
from rq2b_common import read_json, repo_root, require, sha256_file
from run_rq2bv1_v3_skillrouter_primary import _load_packet


AMENDMENT_VERSION = "rq2bv1-v3-skillrouter-primary-local-path-contract-amendment-v3"
BASE_FINALIZER_SHA256 = "1460931ee5a32cd9ee6cb49748a26b3f627eaa5bedfe7c33dffb2895cb46e231"
AMENDED_LOCAL_OUTPUT_ROOT = "skill_benchmark/rq2bv1/results/skillrouter_primary_v3/local_scoring_path_contract_amendment"


def _materialise_forward_records(root: Path, output_root: Path) -> int:
    manifest = read_json(output_root / "manifest.json")
    records = list(manifest["forward_records"])
    require(len(records) == 1501, "Hosted forward-record count drift")
    staging = output_root.parent / f".{output_root.name}.staging" / "forward_records"
    copied = 0
    for binding in records:
        target = root / str(binding["path"])
        expected = str(binding["sha256"])
        if target.is_file():
            require(sha256_file(target) == expected, f"Final forward-record hash drift: {target}")
            continue
        source = staging / target.name
        require(source.is_file() and sha256_file(source) == expected, f"Recovered staging record drift: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        require(sha256_file(target) == expected, f"Materialised forward-record hash drift: {target}")
        copied += 1
    return copied


def finalise(root: Path) -> dict[str, object]:
    root = root.resolve()
    base_path = root / "skill_benchmark/scripts/finalize_rq2bv1_v3_skillrouter_primary.py"
    require(sha256_file(base_path) == BASE_FINALIZER_SHA256, "Approved base finaliser hash drift")
    _, packet = _load_packet(root)
    expected_root = root / str(packet["output_dir"])
    require(expected_root == root / base.RESULT_ROOT, "Packet output-root drift")
    require((expected_root / "manifest.json").is_file(), "Recovered hosted manifest is absent")
    require(not (expected_root / "hosted_embedding").exists(), "Unexpected legacy hosted-embedding subdirectory")
    copied = _materialise_forward_records(root, expected_root)
    interrupted_output = root / base.LOCAL_OUTPUT_ROOT
    if interrupted_output.exists():
        require(interrupted_output.is_dir() and not any(interrupted_output.iterdir()), "Interrupted base local-scoring output is not empty")
    require(not (root / AMENDED_LOCAL_OUTPUT_ROOT).exists(), "Amended local-scoring output already exists")

    # The hosted runner and packet bind output_dir directly; the base finaliser
    # accidentally inserted an extra hosted_embedding path segment.
    base.HOSTED_ROOT = base.RESULT_ROOT
    base.LOCAL_OUTPUT_ROOT = AMENDED_LOCAL_OUTPUT_ROOT
    base.FINALIZER_VERSION = AMENDMENT_VERSION
    result = base.finalise(root)
    result["path_contract_amendment"] = {
        "version": AMENDMENT_VERSION,
        "base_finalizer_sha256": BASE_FINALIZER_SHA256,
        "hosted_manifest_path": str((expected_root / "manifest.json").relative_to(root)),
        "materialised_forward_records": copied,
        "network_calls_added": 0,
        "model_forwards_added": 0,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--finalise", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.finalise != args.self_test, "Choose exactly one of --finalise or --self-test")
    result = base.self_test() if args.self_test else finalise(args.root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
