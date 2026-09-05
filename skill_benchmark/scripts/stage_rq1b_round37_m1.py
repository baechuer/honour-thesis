#!/usr/bin/env python3
"""Byte-stage the preselected Round 37 sources without executing them."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = Path("/private/tmp/rq1b-round37-m1-2026-08-28")
STAGED_ROOT = ROOT / "rq1b_cross_source_public_benchmark" / "staged_sources"
STAGER = ROOT / "scripts" / "stage_rq1b_public_source_set.py"
ORIGINAL = "SKILL.original.md"
LICENCE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md")
SELECTION_STATUS = "M1_ROUND37_BOUNDED_DIVERSE_STAGING_SELECTION_NOT_A_CLUSTER_OR_RESULT"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def run(command: list[str]) -> str:
    return subprocess.run(command, text=True, capture_output=True, check=True).stdout.strip()


def root_for(origin: str, commit: str) -> Path:
    root = TEMP_ROOT / origin.replace("/", "--")
    actual = run(["git", "-C", str(root), "rev-parse", "FETCH_HEAD"])
    if actual != commit:
        raise RuntimeError(f"pinned_tree_missing_or_mismatched:{origin}:{actual}:{commit}")
    return root


def skill_paths(root: Path, commit: str) -> list[str]:
    names = run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", commit]).splitlines()
    return [name for name in names if name == "SKILL.md" or name.endswith("/SKILL.md")]


def root_licence(root: Path, commit: str) -> str | None:
    names = set(run(["git", "-C", str(root), "ls-tree", "--name-only", commit]).splitlines())
    return next((name for name in LICENCE_NAMES if name in names), None)


def materialise(root: Path, commit: str, paths: list[str]) -> None:
    for start in range(0, len(paths), 80):
        run(["git", "-C", str(root), "checkout", commit, "--", *paths[start:start + 80]])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--out-manifest", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    selection: dict[str, Any] = json.loads(args.selection.read_text(encoding="utf-8"))
    if selection.get("status") != SELECTION_STATUS:
        raise SystemExit(f"unexpected_selection_status:{selection.get('status')}")
    sources = list(selection.get("sources", []))
    existing_payload = json.loads(args.output.read_text(encoding="utf-8")) if args.output.exists() else {"results": []}
    if existing_payload.get("selection") not in {None, str(args.selection)}:
        raise SystemExit("invalid_existing_stage_checkpoint")
    prior = {int(row["source_position"]): row for row in existing_payload.get("results", [])}

    results: list[dict[str, Any]] = []
    for ordinal, source in enumerate(sources, start=1):
        position = int(source["plan_position"])
        record = prior.get(position)
        if record is None:
            print(json.dumps({"M1_STAGE_PROGRESS": f"{ordinal}/{len(sources)}", "origin": source["origin"], "event": "begin"}, sort_keys=True), flush=True)
            try:
                root = root_for(str(source["origin"]), str(source["pinned_commit"]))
                paths = skill_paths(root, str(source["pinned_commit"]))
                if len(paths) != int(source["skill_md_path_count"]):
                    raise RuntimeError(f"tree_count_mismatch:{len(paths)}:{source['skill_md_path_count']}")
                licence = root_licence(root, str(source["pinned_commit"]))
                materialise(root, str(source["pinned_commit"]), paths + ([licence] if licence else []))
                destination = STAGED_ROOT / f"round37-m1-{str(source['origin']).replace('/', '--').lower()}-{str(source['pinned_commit'])[:8]}"
                summary_path = destination / "source_expansion_summary.json"
                if destination.exists() and any(destination.iterdir()):
                    staged_summary = json.loads(summary_path.read_text(encoding="utf-8"))
                    stage_status = "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT"
                else:
                    command = [
                        sys.executable, str(STAGER), "--source-root", str(root), "--source-search-root", ".",
                        "--destination", str(destination), "--origin", str(source["origin"]),
                        "--repository-url", str(source["repository_url"]), "--pinned-commit", str(source["pinned_commit"]),
                        "--skill-prefix", f"r37m1-{str(source['origin']).replace('/', '-')}",
                        "--existing-source-roots", str(ROOT / "skills" / "public_imported_background"),
                        str(ROOT / "rq1b_naturalistic_public_replication" / "staged_sources"), str(STAGED_ROOT),
                    ]
                    if licence:
                        command.extend(["--license-id", "DECLARED_REPOSITORY_LICENSE_UNCLASSIFIED", "--license-path", licence])
                    else:
                        command.extend(["--license-id", "NO_DECLARED_REPOSITORY_LICENSE", "--allow-no-license"])
                    staged_summary = json.loads(run(command))
                    stage_status = "M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT"
                record = {
                    "source_position": position, "origin": source["origin"], "repository_url": source["repository_url"],
                    "pinned_commit": source["pinned_commit"], "m1_stage_status": stage_status,
                    "discovered_skill_path_count": len(paths), "staging_destination": str(destination),
                    "staging_summary": staged_summary, "staging_summary_sha256": sha256(summary_path),
                }
            except Exception as error:
                record = {
                    "source_position": position, "origin": source["origin"], "repository_url": source["repository_url"],
                    "pinned_commit": source["pinned_commit"], "m1_stage_status": "M1_SOURCE_STAGE_FAILED_NOT_ADMITTED_NOT_A_RESULT",
                    "error": f"{type(error).__name__}:{error}",
                }
        results.append(record)
        payload = {"status": "M1_ROUND37_STAGING_IN_PROGRESS_OR_COMPLETE_NOT_A_CLUSTER_OR_RESULT", "selection": str(args.selection), "results": results}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"M1_STAGE_PROGRESS": f"{ordinal}/{len(sources)}", "origin": source["origin"], "event": "complete_or_recovered", "status": record["m1_stage_status"]}, sort_keys=True), flush=True)

    staged: list[dict[str, Any]] = []
    non_admissions: list[dict[str, Any]] = []
    integrity_failures: list[str] = []
    all_source_rows = 0
    for record in results:
        if record["m1_stage_status"] not in {"M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT", "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT"}:
            non_admissions.append({"origin": record["origin"], "status": record["m1_stage_status"], "error": record.get("error")})
            continue
        destination = Path(str(record["staging_destination"])).resolve()
        source_manifest = destination / "source_expansion_manifest.jsonl"
        source_summary = destination / "source_expansion_summary.json"
        if not source_manifest.is_file() or not source_summary.is_file() or sha256(source_summary) != record["staging_summary_sha256"]:
            integrity_failures.append(f"staging_summary_drift:{record['origin']}")
            continue
        source_rows = read_jsonl(source_manifest)
        all_source_rows += len(source_rows)
        for source in source_rows:
            if source.get("source_status") != "STAGED_SOURCE_ONLY_NOT_A_CLUSTER":
                continue
            skill_id = str(source["skill_id"])
            original = destination / "skills" / skill_id / "source" / ORIGINAL
            if not original.is_file() or sha256(original) != str(source.get("source_sha256", "")):
                integrity_failures.append(f"source_hash_or_presence_failure:{record['origin']}:{skill_id}")
                continue
            staged.append({
                "source_admission_status": "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER",
                "skill_id": skill_id, "origin": source["origin"], "repository_url": source["repository_url"],
                "pinned_commit": source["pinned_commit"], "source_repository_path": source["source_repository_path"],
                "source_url": source["source_url"], "source_sha256": source["source_sha256"],
                "source_bytes": original.stat().st_size, "license": source["license"], "license_status": source["license_status"],
                "frontmatter_name": source.get("frontmatter_name"), "frontmatter_description": source.get("frontmatter_description"),
                "stage_directory": destination.name, "local_original_path": str(original.relative_to(Path.cwd())),
                "m1_source_position": record["source_position"],
            })
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in staged:
        by_hash[str(row["source_sha256"])].append(row)
    canonical = [sorted(group, key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))[0] for _, group in sorted(by_hash.items())]
    canonical.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    write_jsonl(args.out_manifest, canonical)
    summary = {
        "status": "M1_PASS_ROUND37_PINNED_BYTE_VERIFIED_NOT_A_CLUSTER_OR_RESULT" if not integrity_failures else "M1_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "selection": str(args.selection), "all_source_stage_rows": all_source_rows,
        "pre_canonical_source_count": len(staged), "m1_staged_source_count": len(canonical),
        "origin_count": len({str(row["origin"]) for row in canonical}),
        "by_origin": dict(sorted(Counter(str(row["origin"]) for row in canonical).items())),
        "exact_duplicate_source_count_excluded_from_navigation": len(staged) - len(canonical),
        "non_admitted_source_count": len(non_admissions), "non_admitted_sources": non_admissions,
        "integrity_failures": integrity_failures,
        "exclusions": [
            "No source content was executed.",
            "No semantic grouping, cluster, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output.write_text(json.dumps({"status": "M1_ROUND37_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT", "selection": str(args.selection), "results": results}, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "m1_staged_source_count", "origin_count", "non_admitted_source_count", "integrity_failures")}, sort_keys=True))
    return 0 if not integrity_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
