#!/usr/bin/env python3
"""Pin selected Wave 025 public repositories and enumerate SKILL.md paths only.

Each predeclared root receives one metadata-only attempt. The script uses a
blobless Git tree and never reads or executes repository source bodies.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from datetime import date
from pathlib import Path


ROOTS = [
    ("research-science", "https://github.com/K-Dense-AI/scientific-agent-skills.git"),
    ("research-science", "https://github.com/ersilia-os/ersilia-skills.git"),
    ("healthcare", "https://github.com/salikkhann/openmedskills.git"),
    ("healthcare", "https://github.com/terravic/lab-report-to-fhir-skill.git"),
    ("finance-controls", "https://github.com/wildcat-finance/skills.git"),
    ("finance-controls", "https://github.com/OptimNow/cloud-finops-skills.git"),
    ("product-design", "https://github.com/wondelai/skills.git"),
    ("product-design", "https://github.com/afoninsky/skills.git"),
    ("content-media", "https://github.com/MatrixFounder/Universal-skills.git"),
    ("marketing-sales", "https://github.com/PostPlusAI/postplus-skills.git"),
    ("software-quality", "https://github.com/DaveKJohn/claude-code-specialists.git"),
    ("data-analysis", "https://github.com/byterefinery/skills.git"),
]


def run(argv: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)  # nosec B603: fixed metadata-only Git argv
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--root-config", type=Path)
    parser.add_argument("--status-prefix", default="RQ1B_V3_W25")
    parser.add_argument("--per-root-path-cap", type=int, default=80)
    args = parser.parse_args()
    if args.per_root_path_cap < 1:
        raise SystemExit("per_root_path_cap_must_be_positive")
    if args.output.exists() or args.summary.exists():
        raise SystemExit("refusing_to_overwrite_existing_w25_m1_output")

    roots = ROOTS
    if args.root_config is not None:
        loaded = json.loads(args.root_config.read_text(encoding="utf-8"))
        if not isinstance(loaded, list) or not all(
            isinstance(item, dict) and isinstance(item.get("lane"), str) and isinstance(item.get("remote"), str)
            for item in loaded
        ):
            raise SystemExit("root_config_must_be_a_list_of_lane_remote_objects")
        roots = [(item["lane"], item["remote"]) for item in loaded]
    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix=f"{args.status_prefix.lower()}-m1-") as temporary:
        workspace = Path(temporary)
        for ordinal, (lane, remote) in enumerate(roots, start=1):
            record: dict[str, object] = {
                "root_id": f"{args.status_prefix.replace('_', '-')}-M1-{ordinal:03d}",
                "lane": lane,
                "remote": remote,
                "attempt_policy": "ONE_SHOT_NO_AUTO_RETRY",
                "inspection_boundary": "Git commit and tree paths only; no raw skill body is read or executed.",
            }
            code, stdout, stderr = run(["git", "ls-remote", remote, "HEAD"])
            if code != 0 or not stdout:
                record.update({"status": f"{args.status_prefix}_M1_PIN_FAILED_NOT_ADMITTED", "failure": stderr or "EMPTY_LS_REMOTE"})
                rows.append(record)
                continue
            commit = stdout.split()[0]
            checkout = workspace / f"root-{ordinal:03d}"
            code, _, stderr = run(["git", "init", "-q", str(checkout)])
            if code != 0:
                record.update({"status": f"{args.status_prefix}_M1_TREE_FAILED_NOT_ADMITTED", "commit": commit, "failure": stderr or "GIT_INIT_FAILED"})
                rows.append(record)
                continue
            code, _, stderr = run(["git", "fetch", "-q", "--depth=1", "--filter=blob:none", remote, commit], checkout)
            if code != 0:
                record.update({"status": f"{args.status_prefix}_M1_TREE_FAILED_NOT_ADMITTED", "commit": commit, "failure": stderr or "GIT_FETCH_FAILED"})
                rows.append(record)
                continue
            code, stdout, stderr = run(["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD"], checkout)
            if code != 0:
                record.update({"status": f"{args.status_prefix}_M1_TREE_FAILED_NOT_ADMITTED", "commit": commit, "failure": stderr or "GIT_LS_TREE_FAILED"})
                rows.append(record)
                continue
            paths = [path for path in stdout.splitlines() if Path(path).name.lower() == "skill.md"]
            selected = paths[: args.per_root_path_cap]
            record.update(
                {
                    "status": f"{args.status_prefix}_M1_PATH_CENSUS_COMPLETE_NOT_ADMITTED",
                    "commit": commit,
                    "skill_path_count": len(paths),
                    "selected_skill_paths": selected,
                    "path_cap": args.per_root_path_cap,
                    "path_cap_applied": len(paths) > len(selected),
                }
            )
            rows.append(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    counts: dict[str, int] = {}
    for row in rows:
        status = str(row["status"])
        counts[status] = counts.get(status, 0) + 1
    summary = {
        "status": f"{args.status_prefix}_M1_COMPLETE_NOT_A_SOURCE_OR_CLUSTER",
        "observed_on": date.today().isoformat(),
        "predeclared_root_count": len(roots),
        "attempted_root_count": len(rows),
        "status_counts": counts,
        "total_selected_skill_paths": sum(len(row.get("selected_skill_paths", [])) for row in rows),
        "boundary": [
            "Each root receives one ls-remote and one blobless Git-tree attempt only.",
            "No raw artifact body is read or executed during this stage.",
            "Visible paths are navigation metadata, not admitted sources, clusters, prompts, labels, selector input, metrics, or results.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "roots": len(rows), "status_counts": counts, "selected_paths": summary["total_selected_skill_paths"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
