#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path

from run_confusability_check import default_paths, discover_valid_skills, extract_selected_skills


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def rewrite_manifest(
    manifest_path: Path,
    results_dir: Path,
    workspace_dir: Path,
) -> tuple[int, int]:
    rows = load_rows(manifest_path)
    if not rows:
        return 0, 0

    valid_skills = discover_valid_skills(workspace_dir)
    updated = 0

    for row in rows:
        stdout_path = results_dir / row["stdout_file"]
        stderr_path = results_dir / row["stderr_file"]
        stdout = stdout_path.read_text(encoding="utf-8", errors="replace") if stdout_path.exists() else ""
        stderr = stderr_path.read_text(encoding="utf-8", errors="replace") if stderr_path.exists() else ""
        selected = extract_selected_skills(stdout + "\n" + stderr, valid_skills=valid_skills)
        selected_raw = "|".join(selected)
        if row.get("selected_skills", "") != selected_raw:
            row["selected_skills"] = selected_raw
            updated += 1

    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), updated


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    defaults = default_paths(repo_root)
    default_manifest = defaults["results"] / "manifest.csv"

    parser = argparse.ArgumentParser(
        description="Re-parse stdout/stderr files and rebuild selected_skills in manifest.csv."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=default_manifest,
        help="Path to manifest.csv",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=defaults["results"],
        help="Directory containing stdout/stderr files referenced by the manifest.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=defaults["workspace"],
        help="Workspace directory used to determine the valid skill set.",
    )
    args = parser.parse_args()

    total, updated = rewrite_manifest(
        manifest_path=args.manifest,
        results_dir=args.results_dir,
        workspace_dir=args.workspace,
    )
    print(f"Rebuilt selected_skills for {total} rows; updated {updated} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
