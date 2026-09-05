#!/usr/bin/env python3
"""Stage the pinned RQ1b cross-source Round 16 M1 intake locally.

The public repositories must already be sparse-cloned at the commits recorded
below. This driver performs no network operation and never executes source
content. It delegates byte-copy, duplicate, and frontmatter screening to the
existing source-set stager, then records an aggregate M1 provenance summary.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = Path("/private/tmp/rq1b-round16-m1-2026-08-27")
STAGE_SCRIPT = ROOT / "scripts" / "stage_rq1b_public_source_set.py"
STAGED_ROOT = ROOT / "rq1b_cross_source_public_benchmark" / "staged_sources"
MANIFEST_DIR = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
PLAN = MANIFEST_DIR / "m1_round16_source_batch_plan_2026-08-27.json"
SUMMARY = MANIFEST_DIR / "m1_round16_staging_summary_2026-08-27.json"


SOURCES = [
    ("panaversity/agentfactory-business-plugins", "4497a99e149ffe2447eeaeed1d7706cd91c2edfb", "APACHE-2.0", "LICENSE"),
    ("gfodor/legal-skills", "3c98f2599bafa60cce7fd519636822ab2a00d314", "GPL-3.0-only", "LICENSE"),
    ("astDeniss/business-skills", "208245b7066f1101b09fbfd728a53717a47837d4", "NO_DECLARED_REPOSITORY_LICENSE", None),
    ("product-on-purpose/pm-skills", "6247529860dcab19222932e6dea5885ef18018b3", "APACHE-2.0", "LICENSE"),
    ("K-Dense-AI/scientific-agent-skills", "36d8f13a1e754618794bf42f417884940077b4ae", "MIT", "LICENSE.md"),
    ("YuliaNuzhnenko/bioinformatics-agent-skills", "9b9dbfe1802ef721a76c1e04efd305242042d1ca", "MIT", "LICENSE"),
    ("TerminalSkills/skills", "7a5cc96749b07bcbd33d4f27e98a26a3dba456ca", "APACHE-2.0", "LICENSE"),
    ("dazhiyang/scientific-plotting-skill", "980cbf9328b4224268dd5fff99c1f2f8158e69cc", "MIT", "LICENSE"),
    ("jkitchin/skillz", "b28fcf4c9f882cd890a3b59a160a2ff1b7d3e3de", "MIT", "LICENSE"),
    ("getsentry/skills", "c2f99a5b04b4cd992ec3022d7c2c3e23e938d241", "APACHE-2.0", "LICENSE"),
    ("arjunprabhulal/devops-skills", "0c89b7ed911082d77b0674759fc3a7ac3814c354", "MIT", "LICENSE"),
    ("cloudflare/security-audit-skill", "8bac42001ddd90a4dcd8d5a5045199283a8eba75", "MIT", "LICENSE"),
    ("github/awesome-copilot", "71f7c9b1dc5044287b62fc700efc034da4065f87", "MIT", "LICENSE"),
    ("astronomer/agents", "dbd9bb79c4f7b7ac9c1cdd2b4b75213c81f423e5", "APACHE-2.0", "LICENSE"),
    ("wshobson/agents", "38e19c20d2b154510b0e624a2e3e186b19b5c527", "MIT", "LICENSE"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clone_path(origin: str) -> Path:
    return TEMP_ROOT / origin.replace("/", "--")


def destination(origin: str, commit: str) -> Path:
    return STAGED_ROOT / f"round16-m1-{origin.replace('/', '--').lower()}-{commit[:8]}"


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if len(plan["sources"]) != len(SOURCES):
        raise SystemExit("Round 16 plan/source driver count mismatch")
    expected_origins = {row[0] for row in SOURCES}
    if {str(row["origin"]) for row in plan["sources"]} != expected_origins:
        raise SystemExit("Round 16 plan/source driver origin mismatch")

    results: list[dict[str, object]] = []
    STAGED_ROOT.mkdir(parents=True, exist_ok=True)
    for origin, commit, licence, licence_path in SOURCES:
        source_root = clone_path(origin)
        actual = subprocess.check_output(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
        ).strip()
        if actual != commit:
            raise SystemExit(f"Pinned commit mismatch for {origin}: {actual} != {commit}")
        target = destination(origin, commit)
        if target.exists() and any(target.iterdir()):
            raise SystemExit(f"Refusing to overwrite staged source: {target}")

        command = [
            sys.executable,
            str(STAGE_SCRIPT),
            "--source-root", str(source_root),
            "--source-search-root", ".",
            "--destination", str(target),
            "--origin", origin,
            "--repository-url", f"https://github.com/{origin}",
            "--pinned-commit", commit,
            "--license-id", licence,
            "--skill-prefix", f"r16m1-{origin.replace('/', '-')}",
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
        summary_path = target / "source_expansion_summary.json"
        if not summary_path.is_file():
            raise SystemExit(f"Missing stage summary for {origin}")
        disk_summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if disk_summary != staged_summary:
            raise SystemExit(f"Stage summary mismatch for {origin}")
        results.append(
            {
                "origin": origin,
                "pinned_commit": commit,
                "clone_path": str(source_root),
                "staging_destination": str(target),
                "staging_summary": staged_summary,
                "staging_summary_sha256": sha256(summary_path),
            }
        )

    aggregate = {
        "status": "M1_LOCAL_BYTE_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "round": "RQ1b cross-source Round 16",
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
