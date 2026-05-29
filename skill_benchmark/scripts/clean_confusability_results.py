#!/usr/bin/env python3

import argparse
from pathlib import Path


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    parser = argparse.ArgumentParser(
        description="Remove raw confusability result files and optionally the manifest."
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=repo_root / "runtime" / "confusability_results",
        help="Directory containing confusability outputs.",
    )
    parser.add_argument(
        "--keep-manifest",
        action="store_true",
        help="Keep manifest.csv while deleting prompt/stdout/stderr files.",
    )
    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"No results directory found at {args.results_dir}")
        return 0

    deleted = 0
    for path in args.results_dir.iterdir():
        if path.name == "manifest.csv" and args.keep_manifest:
            continue
        if path.is_file():
            path.unlink()
            deleted += 1

    print(f"Deleted {deleted} file(s) from {args.results_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
