#!/usr/bin/env python3
"""Replay a V7 1,077-group acceptable-set final-library freeze."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
MATERIALISER = WORKSPACE / "skill_benchmark" / "scripts" / "materialise_rq2b_nc_v7_acceptable_set_final_library_freeze.py"
DEFAULT = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability" / "manifests" / "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1"


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=DEFAULT)
    args = parser.parse_args()
    package = args.package.resolve()
    spec = importlib.util.spec_from_file_location("v7_final_freeze", MATERIALISER)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load final-freeze materialiser")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected_outputs, expected_decision, expected_report = module.build_freeze()
    report = json.loads((package / "integrity_report.json").read_text(encoding="utf-8"))
    for name, expected_rows in expected_outputs.items():
        path = package / name
        if not path.is_file() or sha_path(path) != report["output_hashes"][name]:
            raise SystemExit(f"output hash drift: {name}")
        if load_jsonl(path) != expected_rows:
            raise SystemExit(f"deterministic replay drift: {name}")
    decision_path = package / "scope_amendment.json"
    if sha_path(decision_path) != report["output_hashes"]["scope_amendment.json"]:
        raise SystemExit("scope-amendment hash drift")
    if json.loads(decision_path.read_text(encoding="utf-8")) != expected_decision:
        raise SystemExit("scope-amendment replay drift")
    if {key: value for key, value in report.items() if key != "output_hashes"} != expected_report:
        raise SystemExit("integrity report replay drift")
    if report["counts"]["frozen_final_library_groups"] != 1077 or report["counts"]["excluded_or_deferred_groups"] != 149:
        raise SystemExit("freeze scope count drift")
    print(json.dumps({"status": "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FREEZE_REPLAY", "package": str(package), "freeze_status": report["status"], "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
