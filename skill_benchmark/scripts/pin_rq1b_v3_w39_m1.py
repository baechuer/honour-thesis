#!/usr/bin/env python3
"""Pin Wave 039 public roots and enumerate SKILL.md paths without reading bodies."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/?$")


def run_once(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, text=True, capture_output=True, timeout=90)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roots", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    roots = json.loads(args.roots.read_text(encoding="utf-8"))
    if not isinstance(roots, list) or not roots:
        raise SystemExit("invalid_roots")
    if any(row.get("priority") != "high" for row in roots):
        raise SystemExit("priority_mismatch")
    output_root = args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    root_rows, path_rows = [], []
    with tempfile.TemporaryDirectory(prefix="rq1b-v3-w39-m1-") as scratch_root:
        scratch_root_path = Path(scratch_root)
        for index, lead in enumerate(roots, start=1):
            root = str(lead.get("root", ""))
            match = ROOT_RE.fullmatch(root)
            if not match:
                root_rows.append({"root": root, "status": "RQ1B_V3_W39_M1_REJECT_INVALID_ROOT", "attempt_count": 0})
                continue
            owner, repository = match.groups()
            slug = f"{owner}-{repository}".lower().replace("_", "-")
            pin = run_once(["git", "ls-remote", root, "HEAD"])
            if pin.returncode != 0:
                root_rows.append({"root": root, "domain": lead["domain"], "status": "RQ1B_V3_W39_M1_PIN_FAILED", "attempt_count": 1, "stderr": pin.stderr.strip()[-400:]})
                continue
            tokens = pin.stdout.strip().split()
            sha = tokens[0] if len(tokens) == 2 and re.fullmatch(r"[0-9a-f]{40}", tokens[0]) else ""
            if not sha:
                root_rows.append({"root": root, "domain": lead["domain"], "status": "RQ1B_V3_W39_M1_INVALID_PIN", "attempt_count": 1, "stdout": pin.stdout.strip()[-400:]})
                continue
            clone_target = scratch_root_path / f"{index:02d}-{slug}"
            tree = run_once(["git", "-c", "protocol.version=2", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1", "--single-branch", root, str(clone_target)])
            if tree.returncode != 0:
                root_rows.append({"root": root, "domain": lead["domain"], "status": "RQ1B_V3_W39_M1_TREE_FAILED", "attempt_count": 2, "commit_sha": sha, "stderr": tree.stderr.strip()[-400:]})
                shutil.rmtree(clone_target, ignore_errors=True)
                continue
            resolved = run_once(["git", "-C", str(clone_target), "rev-parse", "HEAD"])
            if resolved.returncode != 0 or resolved.stdout.strip() != sha:
                root_rows.append({"root": root, "domain": lead["domain"], "status": "RQ1B_V3_W39_M1_PIN_DRIFT", "attempt_count": 2, "commit_sha": sha, "resolved_sha": resolved.stdout.strip(), "stderr": resolved.stderr.strip()[-400:]})
                shutil.rmtree(clone_target, ignore_errors=True)
                continue
            filter_check = run_once(["git", "-C", str(clone_target), "config", "--get", "remote.origin.partialclonefilter"])
            if filter_check.returncode != 0 or filter_check.stdout.strip() != "blob:none":
                root_rows.append({"root": root, "domain": lead["domain"], "status": "RQ1B_V3_W39_M1_FILTER_UNVERIFIED", "attempt_count": 2, "commit_sha": sha, "filter_value": filter_check.stdout.strip()})
                shutil.rmtree(clone_target, ignore_errors=True)
                continue
            listing = run_once(["git", "-C", str(clone_target), "ls-tree", "-r", "--name-only", "HEAD"])
            if listing.returncode != 0:
                root_rows.append({"root": root, "domain": lead["domain"], "status": "RQ1B_V3_W39_M1_TREE_LIST_FAILED", "attempt_count": 2, "commit_sha": sha, "stderr": listing.stderr.strip()[-400:]})
                shutil.rmtree(clone_target, ignore_errors=True)
                continue
            paths = sorted({line for line in listing.stdout.splitlines() if line.lower().endswith("skill.md")})
            for path in paths:
                path_rows.append({"status": "RQ1B_V3_W39_M1_PATH_ONLY_NOT_A_SOURCE_OR_RESULT", "root": root, "domain": lead["domain"], "discovery_id": lead["discovery_id"], "commit_sha": sha, "repository_path": path})
            root_rows.append({"root": root, "domain": lead["domain"], "discovery_id": lead["discovery_id"], "status": "RQ1B_V3_W39_M1_PIN_AND_TREE_PASS", "attempt_count": 2, "commit_sha": sha, "skill_path_count": len(paths)})
            shutil.rmtree(clone_target, ignore_errors=True)
            print(f"M1_PROGRESS roots={index}/{len(roots)} paths={len(path_rows)}", flush=True)
    (output_root / "m1_pinned_skill_paths.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in path_rows), encoding="utf-8")
    passed = sum(row["status"] == "RQ1B_V3_W39_M1_PIN_AND_TREE_PASS" for row in root_rows)
    summary = {
        "status": "RQ1B_V3_W39_M1_PINNED_METADATA_COMPLETE_NOT_A_SOURCE_OR_RESULT",
        "selected_root_count": len(roots),
        "root_rows": root_rows,
        "successful_root_count": passed,
        "failed_root_count": len(root_rows) - passed,
        "path_only_skill_count": len(path_rows),
        "network_request_attempt_ceiling": len(roots) * 2,
        "network_request_attempt_count": sum(int(row["attempt_count"]) for row in root_rows),
        "retry_policy": "none",
        "source_body_capture_count": 0,
        "source_body_reads": 0,
        "claim_boundary": "Git metadata and tree paths only. The blob filter and no-checkout clone enumerate paths without reading skill bodies; no source is admitted and no triage, prompt, label, selector, metric or result exists.",
    }
    (output_root / "M1_PINNED_ROOTS_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("selected_root_count", "successful_root_count", "failed_root_count", "path_only_skill_count", "network_request_attempt_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
