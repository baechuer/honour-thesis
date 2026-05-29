#!/usr/bin/env python3

import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def default_paths(repo_root: Path) -> dict[str, Path]:
    return {
        "prompts": repo_root / "prompts" / "reply_messaging_confusability.json",
        "runtime": repo_root / "runtime" / "nanobot-thesis",
        "results": repo_root / "runtime" / "confusability_results",
        "workspace": repo_root / "runtime" / "nanobot_flat_workspace",
    }


def load_prompts(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Prompt file must contain a JSON list.")
    return data


def load_prompt_sources(
    prompt_paths: list[Path] | None = None,
    prompt_globs: list[str] | None = None,
) -> list[dict]:
    resolved_paths: list[Path] = []

    for path in prompt_paths or []:
        resolved_paths.append(path)

    for pattern in prompt_globs or []:
        matched = [Path(p) for p in sorted(glob.glob(pattern))]
        if not matched:
            raise FileNotFoundError(f"No prompt files matched glob: {pattern}")
        resolved_paths.extend(matched)

    if not resolved_paths:
        raise ValueError("No prompt files were provided.")

    unique_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for path in resolved_paths:
        resolved = path.resolve()
        if resolved in seen_paths:
            continue
        seen_paths.add(resolved)
        unique_paths.append(resolved)

    prompts: list[dict] = []
    seen_ids: dict[str, Path] = {}
    for path in unique_paths:
        for prompt in load_prompts(path):
            prompt_id = prompt.get("id")
            if not prompt_id:
                raise ValueError(f"Prompt in {path} is missing required 'id'.")
            if prompt_id in seen_ids:
                raise ValueError(
                    f"Duplicate prompt id '{prompt_id}' found in {path} and {seen_ids[prompt_id]}"
                )
            seen_ids[prompt_id] = path
            prompts.append(prompt)
    return prompts


SKILL_PATH_RE = re.compile(
    r"(?:/workspace|…)(?:/skills)?(?:/[^/\s]+)*/(?P<skill>[^/\s]+)/SKILL\.md"
)
SKILL_HINT_RE = re.compile(r"↳\s*skill (?P<skill>[A-Za-z0-9][A-Za-z0-9._-]*)\b")


def discover_valid_skills(workspace_dir: Path) -> set[str]:
    skills_dir = workspace_dir / "skills"
    if not skills_dir.exists():
        return set()

    valid: set[str] = set()
    for child in skills_dir.iterdir():
        if child.is_dir() and (child / "SKILL.md").exists():
            valid.add(child.name)
    return valid


def extract_selected_skills(output_text: str, valid_skills: set[str] | None = None) -> list[str]:
    seen: list[str] = []
    for match in SKILL_PATH_RE.finditer(output_text):
        skill = match.group("skill")
        if valid_skills is not None and skill not in valid_skills:
            continue
        if skill not in seen:
            seen.append(skill)
    for match in SKILL_HINT_RE.finditer(output_text):
        skill = match.group("skill")
        if valid_skills is not None and skill not in valid_skills:
            continue
        if skill not in seen:
            seen.append(skill)
    return seen


def run_one(
    docker_bin: str,
    docker_image: str,
    config_host_dir: Path,
    workspace_host_dir: Path,
    session_id: str,
    prompt: str,
) -> subprocess.CompletedProcess:
    cmd = [
        docker_bin,
        "run",
        "-i",
        "--rm",
        "-v",
        f"{config_host_dir}:/home/nanobot/.nanobot",
        "-v",
        f"{workspace_host_dir}:/workspace",
        docker_image,
        "agent",
        "--config",
        "/home/nanobot/.nanobot/config.json",
        "--workspace",
        "/workspace",
        "--session",
        session_id,
        "--no-markdown",
        "-m",
        prompt,
    ]
    return subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
    )


def resolve_docker_bin(cli_value: str | None = None) -> str:
    candidates = []
    if cli_value:
        candidates.append(cli_value)
    env_value = os.environ.get("DOCKER_BIN")
    if env_value:
        candidates.append(env_value)
    which_value = shutil.which("docker")
    if which_value:
        candidates.append(which_value)
    candidates.extend([
        "/Applications/Docker.app/Contents/Resources/bin/docker",
        "/usr/local/bin/docker",
        "/opt/homebrew/bin/docker",
    ])

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate

    raise FileNotFoundError(
        "Could not find Docker CLI. Pass --docker-bin, set DOCKER_BIN, or add docker to PATH."
    )


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    paths = default_paths(repo_root)

    parser = argparse.ArgumentParser(
        description="Run reproducible nanobot confusability checks against the benchmark workspace."
    )
    parser.add_argument(
        "--prompts",
        action="append",
        type=Path,
        default=None,
        help="Path to a JSON prompt file. Can be used multiple times.",
    )
    parser.add_argument(
        "--prompts-glob",
        action="append",
        default=None,
        help="Glob pattern for JSON prompt files. Can be used multiple times.",
    )
    parser.add_argument(
        "--runtime-dir",
        type=Path,
        default=paths["runtime"],
        help="Host directory containing nanobot config.json.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=paths["workspace"],
        help="Host workspace directory mounted to /workspace.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=paths["results"],
        help="Directory for raw outputs and manifest CSV.",
    )
    parser.add_argument(
        "--docker-image",
        default="nanobot",
        help="Docker image name to run.",
    )
    parser.add_argument(
        "--docker-bin",
        default=None,
        help="Path to the Docker CLI binary. Optional on systems where docker is already on PATH.",
    )
    parser.add_argument(
        "--id",
        action="append",
        dest="ids",
        help="Only run the given prompt id. Can be used multiple times.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of repetitions per prompt.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selected prompt ids without executing Docker.",
    )
    args = parser.parse_args()

    prompt_paths = args.prompts or [paths["prompts"]]
    prompts = load_prompt_sources(prompt_paths=prompt_paths, prompt_globs=args.prompts_glob)
    if args.ids:
        wanted = set(args.ids)
        prompts = [p for p in prompts if p.get("id") in wanted]

    if not prompts:
        print("No prompts selected.", file=sys.stderr)
        return 1

    try:
        docker_bin = resolve_docker_bin(args.docker_bin)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    args.results_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.results_dir / "manifest.csv"
    manifest_exists = manifest_path.exists()
    valid_skills = discover_valid_skills(args.workspace)

    if args.dry_run:
        for prompt in prompts:
            print(prompt["id"])
        return 0

    with manifest_path.open("a", encoding="utf-8", newline="") as manifest_file:
        writer = csv.DictWriter(
            manifest_file,
            fieldnames=[
                "timestamp",
                "prompt_id",
                "run_index",
                "session_id",
                "gold_skill",
                "closest_alternatives",
                "selected_skills",
                "stdout_file",
                "stderr_file",
                "exit_code",
            ],
        )
        if not manifest_exists:
            writer.writeheader()

        for prompt_row in prompts:
            for run_index in range(1, args.repeat + 1):
                timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                stem = f"{timestamp}__{prompt_row['id']}__run{run_index}"
                session_id = f"bench:{prompt_row['id']}:{timestamp}:run{run_index}"
                stdout_path = args.results_dir / f"{stem}.stdout.txt"
                stderr_path = args.results_dir / f"{stem}.stderr.txt"
                prompt_path = args.results_dir / f"{stem}.prompt.txt"

                prompt_path.write_text(prompt_row["prompt"], encoding="utf-8")

                print(f"Running {prompt_row['id']} (run {run_index})...")
                completed = run_one(
                    docker_bin=docker_bin,
                    docker_image=args.docker_image,
                    config_host_dir=args.runtime_dir,
                    workspace_host_dir=args.workspace,
                    session_id=session_id,
                    prompt=prompt_row["prompt"],
                )

                stdout_path.write_text(completed.stdout, encoding="utf-8")
                stderr_path.write_text(completed.stderr, encoding="utf-8")
                selected_skills = extract_selected_skills(
                    completed.stdout + "\n" + completed.stderr,
                    valid_skills=valid_skills,
                )

                writer.writerow(
                    {
                        "timestamp": timestamp,
                        "prompt_id": prompt_row["id"],
                        "run_index": run_index,
                        "session_id": session_id,
                        "gold_skill": prompt_row["gold_skill"],
                        "closest_alternatives": "|".join(prompt_row.get("closest_alternatives", [])),
                        "selected_skills": "|".join(selected_skills),
                        "stdout_file": stdout_path.name,
                        "stderr_file": stderr_path.name,
                        "exit_code": completed.returncode,
                    }
                )
                manifest_file.flush()

                if completed.returncode != 0:
                    print(
                        f"Run failed for {prompt_row['id']} (run {run_index}). "
                        f"See {stderr_path}.",
                        file=sys.stderr,
                    )

    print(f"Finished. Results written to {args.results_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
