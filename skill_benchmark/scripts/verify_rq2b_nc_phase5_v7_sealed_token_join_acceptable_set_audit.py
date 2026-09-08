#!/usr/bin/env python3
"""Replay and verify a V7 sealed token-join acceptable-set audit package."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
SCRIPT = WORKSPACE / "skill_benchmark" / "scripts" / "materialise_rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit.py"
DEFAULT = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability" / "manifests" / "rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit_2026_09_08_v1"


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=DEFAULT)
    args = parser.parse_args()
    package = args.package.resolve()
    spec = importlib.util.spec_from_file_location("v7_sealed_join", SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load materialiser")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected_outputs, expected_report = module.audit()
    report = json.loads((package / "integrity_report.json").read_text(encoding="utf-8"))
    output_hashes = report.get("output_hashes", {})
    if set(output_hashes) != set(expected_outputs):
        raise SystemExit("output inventory drift")
    for name, expected_rows in expected_outputs.items():
        path = package / name
        if not path.is_file() or sha_path(path) != output_hashes[name]:
            raise SystemExit(f"output hash drift: {name}")
        if load_jsonl(path) != expected_rows:
            raise SystemExit(f"deterministic replay drift: {name}")
    comparable = {key: value for key, value in report.items() if key != "output_hashes"}
    if comparable != expected_report:
        raise SystemExit("integrity report replay drift")
    if report["counts"]["joined_candidate_dispositions"] != 9800 or report["counts"]["target_joined_reconciled_groups"] != 1225:
        raise SystemExit("coverage drift")
    print(json.dumps({"status": "PASS_V7_SEALED_TOKEN_JOIN_ACCEPTABLE_SET_AUDIT_REPLAY", "package": str(package), "overall_status": report["status"], "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
