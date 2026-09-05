#!/usr/bin/env python3
"""Sparse-acquire and byte-stage one pinned Round 19 RQ1b M1 source batch.

Public Git operations fetch only the pinned commit tree and selected SKILL.md
and root licence blobs. Source content is never executed. This is source
admission bookkeeping, not semantic grouping or an experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
STAGED_ROOT = ROOT / "rq1b_cross_source_public_benchmark" / "staged_sources"
TEMP_ROOT = Path("/private/tmp/rq1b-round19-m1-2026-08-27")
PLAN = MANIFEST / "m1_round19_source_batch_plan_2026-08-27.json"
STAGER = ROOT / "scripts" / "stage_rq1b_public_source_set.py"
LICENCE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(command, check=True, text=True, capture_output=capture)
    return completed.stdout.strip() if capture else ""


def clone_path(origin: str) -> Path:
    return TEMP_ROOT / origin.replace("/", "--")


def stage_path(origin: str, commit: str) -> Path:
    return STAGED_ROOT / f"round19-m1-{origin.replace('/', '--').lower()}-{commit[:8]}"


def local_skill_paths(source_root: Path, commit: str) -> list[str]:
    tree = run(["git", "-C", str(source_root), "ls-tree", "-r", "--name-only", commit], capture=True)
    return [path for path in tree.splitlines() if path == "SKILL.md" or path.endswith("/SKILL.md")]


def root_licence(source_root: Path, commit: str) -> str | None:
    root_tree = set(run(["git", "-C", str(source_root), "ls-tree", "--name-only", commit], capture=True).splitlines())
    return next((name for name in LICENCE_NAMES if name in root_tree), None)


def materialise_paths(source_root: Path, commit: str, paths: list[str]) -> None:
    for start in range(0, len(paths), 80):
        run(["git", "-C", str(source_root), "checkout", commit, "--", *paths[start:start + 80]])


def prepare_clone(origin: str, repository_url: str, commit: str) -> Path:
    source_root = clone_path(origin)
    if source_root.exists():
        actual = run(["git", "-C", str(source_root), "rev-parse", "FETCH_HEAD"], capture=True)
        if actual != commit:
            raise RuntimeError(f"existing_fetch_head_mismatch:{origin}:{actual}:{commit}")
        return source_root
    source_root.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "--quiet", str(source_root)])
    run(["git", "-C", str(source_root), "remote", "add", "origin", repository_url])
    run([
        "git", "-C", str(source_root), "-c", "protocol.version=2", "fetch",
        "--depth=1", "--filter=blob:none", "origin", commit,
    ])
    actual = run(["git", "-C", str(source_root), "rev-parse", "FETCH_HEAD"], capture=True)
    if actual != commit:
        raise RuntimeError(f"pinned_commit_mismatch:{origin}:{actual}:{commit}")
    return source_root


def stage_one(source: dict[str, Any]) -> dict[str, Any]:
    origin = str(source["origin"])
    repository_url = str(source["repository_url"])
    commit = str(source["pinned_commit"])
    source_root = prepare_clone(origin, repository_url, commit)
    skill_paths = local_skill_paths(source_root, commit)
    if not skill_paths:
        return {
            "origin": origin,
            "repository_url": repository_url,
            "pinned_commit": commit,
            "m1_stage_status": "M1_NO_SKILL_MD_AT_PINNED_COMMIT_NOT_ADMITTED_NOT_A_RESULT",
            "discovered_skill_path_count": 0,
        }
    licence_path = root_licence(source_root, commit)
    materialise_paths(source_root, commit, skill_paths + ([licence_path] if licence_path else []))
    destination = stage_path(origin, commit)
    summary_path = destination / "source_expansion_summary.json"
    if destination.exists() and any(destination.iterdir()):
        if not summary_path.is_file():
            raise RuntimeError(f"incomplete_existing_stage:{origin}")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("origin") != origin or summary.get("pinned_commit") != commit:
            raise RuntimeError(f"existing_stage_provenance_mismatch:{origin}")
        return {
            "origin": origin,
            "repository_url": repository_url,
            "pinned_commit": commit,
            "m1_stage_status": "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT",
            "discovered_skill_path_count": len(skill_paths),
            "staging_destination": str(destination),
            "staging_summary": summary,
            "staging_summary_sha256": sha256(summary_path),
        }
    command = [
        sys.executable, str(STAGER),
        "--source-root", str(source_root),
        "--source-search-root", ".",
        "--destination", str(destination),
        "--origin", origin,
        "--repository-url", repository_url,
        "--pinned-commit", commit,
        "--skill-prefix", f"r18m1-{origin.replace('/', '-')}",
        "--existing-source-roots", str(ROOT / "skills" / "public_imported_background"),
        str(ROOT / "rq1b_naturalistic_public_replication" / "staged_sources"),
        str(STAGED_ROOT),
    ]
    if licence_path:
        command.extend(["--license-id", "DECLARED_REPOSITORY_LICENSE_UNCLASSIFIED", "--license-path", licence_path])
    else:
        command.extend(["--license-id", "NO_DECLARED_REPOSITORY_LICENSE", "--allow-no-license"])
    staged_summary = json.loads(run(command, capture=True))
    if not summary_path.is_file() or json.loads(summary_path.read_text(encoding="utf-8")) != staged_summary:
        raise RuntimeError(f"staging_summary_mismatch:{origin}")
    return {
        "origin": origin,
        "repository_url": repository_url,
        "pinned_commit": commit,
        "m1_stage_status": "M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT",
        "discovered_skill_path_count": len(skill_paths),
        "staging_destination": str(destination),
        "staging_summary": staged_summary,
        "staging_summary_sha256": sha256(summary_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=None, help="One-based inclusive source position in plan order.")
    parser.add_argument("--end", type=int, default=None, help="One-based inclusive source position in plan order.")
    parser.add_argument(
        "--source-index",
        type=int,
        action="append",
        default=[],
        help="One-based plan position; repeat for a non-contiguous source batch.",
    )
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("status") != "M1_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT":
        raise SystemExit("unexpected_round19_m1_plan_status")
    sources = plan.get("sources", [])
    if args.source_index:
        if args.start is not None or args.end is not None:
            raise SystemExit("source_index_cannot_mix_with_start_end")
        positions = sorted(set(args.source_index))
        if len(positions) != len(args.source_index) or any(position < 1 or position > len(sources) for position in positions):
            raise SystemExit(f"invalid_source_indexes:{positions}:{len(sources)}")
    else:
        if args.start is None or args.end is None or not (1 <= args.start <= args.end <= len(sources)):
            raise SystemExit(f"invalid_source_window:{args.start}:{args.end}:{len(sources)}")
        positions = list(range(args.start, args.end + 1))

    results: list[dict[str, Any]] = []
    for ordinal, position in enumerate(positions, start=1):
        source = sources[position - 1]
        print(json.dumps({"M1_STAGE_PROGRESS": f"{ordinal}/{len(positions)}", "plan_position": position, "origin": source.get("origin"), "event": "begin"}, sort_keys=True), flush=True)
        try:
            row = stage_one(source)
        except Exception as error:  # fail closed for this source; never retry automatically
            row = {
                "origin": source.get("origin"),
                "repository_url": source.get("repository_url"),
                "pinned_commit": source.get("pinned_commit"),
                "m1_stage_status": "M1_SOURCE_STAGE_FAILED_NOT_ADMITTED_NOT_A_RESULT",
                "error": f"{type(error).__name__}:{error}",
            }
        row["plan_position"] = position
        results.append(row)
        print(json.dumps({"M1_STAGE_PROGRESS": f"{ordinal}/{len(positions)}", "plan_position": position, "origin": source.get("origin"), "event": "complete", "status": row["m1_stage_status"], "discovered_skill_path_count": row.get("discovered_skill_path_count")}, sort_keys=True), flush=True)
    payload = {
        "status": "M1_ROUND19_BATCH_COMPLETE_WITH_PER_SOURCE_STATUS_NOT_A_CLUSTER_OR_RESULT",
        "batch_id": args.batch_id,
        "plan_positions": positions,
        "plan": str(PLAN),
        "plan_sha256": sha256(PLAN),
        "results": results,
        "totals": {
            "source_count": len(results),
            "staged_source_count": sum(row["m1_stage_status"] == "M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT" for row in results),
            "recovered_stage_count": sum(row["m1_stage_status"] == "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT" for row in results),
            "no_skill_md_count": sum(row["m1_stage_status"] == "M1_NO_SKILL_MD_AT_PINNED_COMMIT_NOT_ADMITTED_NOT_A_RESULT" for row in results),
            "failed_source_count": sum(row["m1_stage_status"] == "M1_SOURCE_STAGE_FAILED_NOT_ADMITTED_NOT_A_RESULT" for row in results),
            "discovered_skill_path_count": sum(int(row.get("discovered_skill_path_count", 0)) for row in results),
            "byte_staged_source_count": sum(int(row.get("staging_summary", {}).get("staged_sources", 0)) for row in results),
        },
        "exclusions": [
            "No source content was executed.",
            "No candidate composition, prompt, gold label, acceptable set, retrieval input, embedding, selector call, metric, or result was created.",
            "A failed source remains an explicit M1 non-admission and is not retried by this program.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "batch_id": args.batch_id, "totals": payload["totals"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
