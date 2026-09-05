#!/usr/bin/env python3
"""Pin public RQ1b V3 Wave 024 repositories and enumerate skill paths only."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from datetime import date
from pathlib import Path


ROOTS = [
    ("legal", "https://github.com/gfodor/legal-skills.git"),
    ("legal", "https://github.com/anthropics/knowledge-work-plugins.git"),
    ("finance", "https://github.com/anthropics/financial-services.git"),
    ("marketing", "https://github.com/coreyhaines31/marketingskills.git"),
    ("marketing", "https://github.com/vidual-labs/digital-marketing-skills.git"),
    ("content", "https://github.com/social-media-skills/skills.git"),
    ("content", "https://github.com/vstorm-co/content-skills.git"),
    ("product-design", "https://github.com/Uxcel-Lab/product-skills.git"),
    ("product-design", "https://github.com/assimovt/productskills.git"),
    ("health", "https://github.com/anthropics/healthcare.git"),
    ("health", "https://github.com/langcare/langcare-mcp-fhir.git"),
    ("health", "https://github.com/reason-healthcare/rh-skills.git"),
    ("education", "https://github.com/GarethManning/education-agent-skills.git"),
    ("research", "https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills.git"),
    ("infrastructure", "https://github.com/google/skills.git"),
    ("infrastructure", "https://github.com/oracle/skills.git"),
    ("infrastructure", "https://github.com/cloudflare/skills.git"),
    ("security", "https://github.com/RedHatProductSecurity/prodsec-skills.git"),
    ("security", "https://github.com/UnitOneAI/SecuritySkills.git"),
    ("operations", "https://github.com/arjunprabhulal/devops-skills.git"),
    ("operations", "https://github.com/NotHarshhaa/devops-skills.git"),
    ("operations", "https://github.com/iuliandita/skills.git"),
    ("operations", "https://github.com/OpenHands/extensions.git"),
    ("data", "https://github.com/prisma/skills.git"),
    ("data", "https://github.com/apollographql/skills.git"),
    ("health", "https://github.com/writer/skills.git"),
    ("health", "https://github.com/CaseMark/skills.git"),
    ("multi-domain", "https://github.com/claude-office-skills/skills.git"),
]


def run(argv: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)  # nosec B603: fixed git argv
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--per-root-path-cap", type=int, default=50)
    args = parser.parse_args()
    if args.per_root_path_cap < 1:
        raise SystemExit("per_root_path_cap_must_be_positive")

    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="rq1b-v3-w24-m1-") as temporary:
        workspace = Path(temporary)
        for ordinal, (lane, remote) in enumerate(ROOTS, start=1):
            record: dict[str, object] = {
                "root_id": f"RQ1B-V3-W24-M1-{ordinal:03d}",
                "lane": lane,
                "remote": remote,
                "attempt_policy": "ONE_SHOT_NO_AUTO_RETRY",
                "inspection_boundary": "Git commit and tree paths only; no raw skill body is read or executed.",
            }
            code, stdout, stderr = run(["git", "ls-remote", remote, "HEAD"])
            if code != 0 or not stdout:
                record.update({"status": "RQ1B_V3_W24_M1_PIN_FAILED_NOT_ADMITTED", "failure": stderr or "EMPTY_LS_REMOTE"})
                rows.append(record)
                continue
            commit = stdout.split()[0]
            checkout = workspace / f"root-{ordinal:03d}"
            code, _, stderr = run(["git", "init", "-q", str(checkout)])
            if code != 0:
                record.update({"status": "RQ1B_V3_W24_M1_TREE_FAILED_NOT_ADMITTED", "commit": commit, "failure": stderr or "GIT_INIT_FAILED"})
                rows.append(record)
                continue
            code, _, stderr = run(["git", "fetch", "-q", "--depth=1", "--filter=blob:none", remote, commit], checkout)
            if code != 0:
                record.update({"status": "RQ1B_V3_W24_M1_TREE_FAILED_NOT_ADMITTED", "commit": commit, "failure": stderr or "GIT_FETCH_FAILED"})
                rows.append(record)
                continue
            code, stdout, stderr = run(["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD"], checkout)
            if code != 0:
                record.update({"status": "RQ1B_V3_W24_M1_TREE_FAILED_NOT_ADMITTED", "commit": commit, "failure": stderr or "GIT_LS_TREE_FAILED"})
                rows.append(record)
                continue
            # Match the declared artifact filename exactly; names such as
            # `new-skill.md` and `rewrite-skill.md` are not skill artifacts.
            all_paths = [path for path in stdout.splitlines() if Path(path).name.lower() == "skill.md"]
            paths = all_paths[: args.per_root_path_cap]
            record.update(
                {
                    "status": "RQ1B_V3_W24_M1_PATH_CENSUS_COMPLETE_NOT_ADMITTED",
                    "commit": commit,
                    "skill_path_count": len(all_paths),
                    "selected_skill_paths": paths,
                    "path_cap": args.per_root_path_cap,
                    "path_cap_applied": len(all_paths) > len(paths),
                }
            )
            rows.append(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    status_counts: dict[str, int] = {}
    for row in rows:
        status = str(row["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
    summary = {
        "status": "RQ1B_V3_W24_M1_COMPLETE_NOT_A_SOURCE_OR_CLUSTER",
        "observed_on": date.today().isoformat(),
        "predeclared_root_count": len(ROOTS),
        "attempted_root_count": len(rows),
        "status_counts": status_counts,
        "total_selected_skill_paths": sum(len(row.get("selected_skill_paths", [])) for row in rows),
        "boundary": [
            "Each public root receives one ls-remote and one blobless git-tree attempt only.",
            "The process reads no raw artifact body and executes no source code.",
            "A visible path is navigation metadata, not source admission, an independent artifact, D1 composition, cluster, prompt, label, retrieval input, metric or result.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "roots": len(rows), "status_counts": status_counts, "selected_paths": summary["total_selected_skill_paths"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
