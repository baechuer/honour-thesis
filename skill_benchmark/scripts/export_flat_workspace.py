#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path


def find_skill_dirs(skills_root: Path, families: set[str] | None = None) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    for family_dir in sorted(skills_root.iterdir()):
        if not family_dir.is_dir():
            continue
        if families and family_dir.name not in families:
            continue
        for skill_dir in sorted(family_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            if (skill_dir / "SKILL.md").exists():
                found.append((family_dir.name, skill_dir))
    return found


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_placeholder_memory(workspace: Path) -> None:
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    (memory_dir / "history.jsonl").touch()


def copy_fixtures(
    repo_root: Path,
    output_dir: Path,
    families: set[str] | None = None,
) -> None:
    fixtures_root = repo_root / "fixtures"
    if not fixtures_root.exists():
        return

    dest_root = output_dir / "fixtures"
    dest_root.mkdir(parents=True, exist_ok=True)

    if families:
        copied_any = False
        for family in sorted(families):
            src = fixtures_root / family
            if not src.exists():
                continue
            shutil.copytree(src, dest_root / family)
            copied_any = True
        if copied_any:
            return

    for src in sorted(fixtures_root.iterdir()):
        dest = dest_root / src.name
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)


def export_flat_workspace(
    repo_root: Path,
    output_dir: Path,
    families: set[str] | None = None,
) -> tuple[int, list[tuple[str, str]]]:
    skills_root = repo_root / "skills"
    workspace_skills = output_dir / "skills"

    ensure_clean_dir(output_dir)
    workspace_skills.mkdir(parents=True, exist_ok=True)
    write_placeholder_memory(output_dir)
    copy_fixtures(repo_root, output_dir, families)

    copied: list[tuple[str, str]] = []
    for family_name, skill_dir in find_skill_dirs(skills_root, families):
        dest = workspace_skills / skill_dir.name
        shutil.copytree(skill_dir, dest)
        copied.append((family_name, skill_dir.name))

    return len(copied), copied


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    parser = argparse.ArgumentParser(
        description="Export a flat nanobot-compatible workspace from grouped benchmark skills."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "runtime" / "nanobot_flat_workspace",
        help="Destination workspace directory.",
    )
    parser.add_argument(
        "--family",
        action="append",
        dest="families",
        help="Only export the given family. Can be used multiple times.",
    )
    args = parser.parse_args()

    families = set(args.families) if args.families else None
    count, copied = export_flat_workspace(repo_root, args.output, families)

    print(f"Exported {count} skills to {args.output}")
    for family_name, skill_name in copied:
        print(f"- {skill_name} ({family_name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
