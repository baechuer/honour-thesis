#!/usr/bin/env python3
"""Stage the pinned RQ1b cross-source Round 17 M1 intake locally.

This driver is deliberately offline. It consumes already-acquired public
repository working copies, verifies their exact commits, and delegates only
byte copying and source integrity checks to the existing source-set stager.
No source content is executed and no cluster or evaluation artifact is made.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = Path("/private/tmp/rq1b-round17-m1-2026-08-27")
STAGED_ROOT = ROOT / "rq1b_cross_source_public_benchmark" / "staged_sources"
MANIFEST_DIR = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
PLAN = MANIFEST_DIR / "m1_round17_source_batch_plan_2026-08-27.json"
SUMMARY = MANIFEST_DIR / "m1_round17_staging_summary_2026-08-27.json"
STAGE_SCRIPT = ROOT / "scripts" / "stage_rq1b_public_source_set.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clone_path(origin: str) -> Path:
    return TEMP_ROOT / origin.replace("/", "--")


def destination(origin: str, commit: str) -> Path:
    return STAGED_ROOT / f"round17-m1-{origin.replace('/', '--').lower()}-{commit[:8]}"


def licence(source_root: Path) -> tuple[str, str | None]:
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md"):
        if (source_root / name).is_file():
            return "DECLARED_REPOSITORY_LICENSE_UNCLASSIFIED", name
    return "NO_DECLARED_REPOSITORY_LICENSE", None


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("status") != "M1_BATCH_PLAN_PINNED_NOT_YET_STAGED_NOT_A_CLUSTER_OR_RESULT":
        raise SystemExit("Round 17 plan is not in the expected pinned state")

    results: list[dict[str, object]] = []
    STAGED_ROOT.mkdir(parents=True, exist_ok=True)
    for source in plan["sources"]:
        origin = str(source["origin"])
        commit = str(source["pinned_commit"])
        source_root = clone_path(origin)
        actual = subprocess.check_output(["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True).strip()
        if actual != commit:
            raise SystemExit(f"Pinned commit mismatch for {origin}: {actual} != {commit}")
        target = destination(origin, commit)
        licence_id, licence_path = licence(source_root)
        summary_path = target / "source_expansion_summary.json"
        if target.exists() and any(target.iterdir()):
            # A bounded execution window may finish a per-source stage before
            # this aggregate driver writes its final summary. Resume only from
            # a complete, provenance-matching stage; never overwrite it.
            if not summary_path.is_file():
                raise SystemExit(f"Incomplete existing staged source: {target}")
            staged_summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if (
                staged_summary.get("origin") != origin
                or staged_summary.get("pinned_commit") != commit
                or staged_summary.get("repository_url") != f"https://github.com/{origin}"
            ):
                raise SystemExit(f"Existing staged-source provenance mismatch: {target}")
            results.append({
                "origin": origin,
                "pinned_commit": commit,
                "clone_path": str(source_root),
                "staging_destination": str(target),
                "license_id": licence_id,
                "license_path": licence_path,
                "staging_summary": staged_summary,
                "staging_summary_sha256": sha256(summary_path),
                "recovered_existing_stage": True,
            })
            continue
        command = [
            sys.executable,
            str(STAGE_SCRIPT),
            "--source-root", str(source_root),
            "--source-search-root", ".",
            "--destination", str(target),
            "--origin", origin,
            "--repository-url", f"https://github.com/{origin}",
            "--pinned-commit", commit,
            "--license-id", licence_id,
            "--skill-prefix", f"r17m1-{origin.replace('/', '-')}",
            "--existing-source-roots", str(ROOT / "skills" / "public_imported_background"),
            str(ROOT / "rq1b_naturalistic_public_replication" / "staged_sources"),
            str(STAGED_ROOT),
        ]
        if licence_path is None:
            command.append("--allow-no-license")
        else:
            command.extend(["--license-path", licence_path])
        stdout = subprocess.check_output(command, text=True).strip()
        staged_summary = json.loads(stdout)
        if not summary_path.is_file() or json.loads(summary_path.read_text(encoding="utf-8")) != staged_summary:
            raise SystemExit(f"Stage summary mismatch for {origin}")
        results.append({
            "origin": origin,
            "pinned_commit": commit,
            "clone_path": str(source_root),
            "staging_destination": str(target),
            "license_id": licence_id,
            "license_path": licence_path,
            "staging_summary": staged_summary,
            "staging_summary_sha256": sha256(summary_path),
        })

    aggregate = {
        "status": "M1_LOCAL_BYTE_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "round": "RQ1b cross-source Round 17",
        "plan": str(PLAN),
        "plan_sha256": sha256(PLAN),
        "source_count": len(results),
        "results": results,
        "totals": {
            "discovered_skill_files": sum(int(row["staging_summary"]["discovered_skill_files"]) for row in results),
            "staged_sources": sum(int(row["staging_summary"]["staged_sources"]) for row in results),
            "skipped_exact_duplicates": sum(int(row["staging_summary"]["skipped_exact_duplicates"]) for row in results),
            "skipped_missing_frontmatter": sum(int(row["staging_summary"]["skipped_missing_frontmatter"]) for row in results),
        },
        "exclusions": [
            "No public source content was executed.",
            "No cluster, prompt, label, acceptable set, retrieval input, embedding, selector call, metric, or result was created.",
            "No-declared-licence source records remain reference-only for any later release.",
        ],
    }
    SUMMARY.write_text(json.dumps(aggregate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": aggregate["status"], "totals": aggregate["totals"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
