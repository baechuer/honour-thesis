# /// script
# dependencies = [
#   "huggingface-hub",
#   "transformers",
#   "torch",
#   "accelerate",
#   "safetensors",
#   "scikit-learn",
#   "rank-bm25",
#   "numpy",
# ]
# ///

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tarfile
import time
import traceback

from huggingface_hub import HfApi, hf_hub_download, whoami


REPO_ID = "baechuer1/honour-thesis-skillrouter-benchmark-snapshot"
SNAPSHOT_NAME = "skill_benchmark_snapshot_v0_4_2026_06_17.tar.gz"
OUT_PREFIX = "skillrouter_v0_4_2026_06_17_retry2"


def run_condition(name: str, cmd: list[str]) -> dict[str, object]:
    print(f"\n=== RUN {name} ===", flush=True)
    start = time.time()
    subprocess.run(cmd, check=True)
    path = pathlib.Path("skill_benchmark/outputs") / f"{name}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    metrics = data["metrics"]
    row = {
        "name": name,
        "json": str(path),
        "md": str(path).replace(".json", ".md"),
        "top1": metrics["top1_accuracy"],
        "acceptable_top1": metrics["acceptable_top1_accuracy"],
        "top5": metrics["top5_recall"],
        "acceptable_top5": metrics["acceptable_top5_recall"],
        "mrr": metrics["mrr"],
        "non_main_top1": metrics["non_main_top1_rate"],
        "elapsed_sec": round(time.time() - start, 2),
    }
    print(
        "RESULT "
        f"{name}: top1={row['top1']:.1%}, "
        f"acceptable_top1={row['acceptable_top1']:.1%}, "
        f"top5={row['top5']:.1%}, "
        f"acceptable_top5={row['acceptable_top5']:.1%}, "
        f"mrr={row['mrr']:.3f}, "
        f"non_main_top1={row['non_main_top1']:.1%}",
        flush=True,
    )
    return row


def write_summary(summary: list[dict[str, object]]) -> tuple[pathlib.Path, pathlib.Path]:
    output_dir = pathlib.Path("skill_benchmark/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_json = output_dir / f"{OUT_PREFIX}_summary.json"
    summary_md = output_dir / f"{OUT_PREFIX}_summary.md"
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# SkillRouter frozen v0.4 retry summary",
        "",
        "| Condition | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Non-main top-1 | Elapsed sec |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| `{row['name']}` | {row['top1']:.1%} | {row['acceptable_top1']:.1%} | "
            f"{row['top5']:.1%} | {row['acceptable_top5']:.1%} | {row['mrr']:.3f} | "
            f"{row['non_main_top1']:.1%} | {row['elapsed_sec']} |"
        )
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + summary_md.read_text(encoding="utf-8"), flush=True)
    return summary_json, summary_md


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is required")

    print("whoami:", whoami(token=token).get("name"), flush=True)
    print("downloading snapshot", SNAPSHOT_NAME, flush=True)
    archive = hf_hub_download(
        repo_id=REPO_ID,
        filename=SNAPSHOT_NAME,
        repo_type="dataset",
        token=token,
    )
    work = pathlib.Path("/tmp/skillrouter_v0_4_retry2")
    work.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(work)
    os.chdir(work)
    print("cwd", os.getcwd(), flush=True)

    base_cmd = [
        sys.executable,
        "skill_benchmark/scripts/run_skillrouter_selectors.py",
        "--scale",
        "current_full",
        "--device",
        "cuda",
        "--embedding-batch-size",
        "4",
        "--embedding-max-length",
        "2048",
        "--reranker-max-length",
        "2048",
        "--cache-dir",
        "skill_benchmark/runtime/provider_cache",
    ]

    conditions: list[tuple[str, list[str]]] = []
    prompt_sets = [
        (
            "controlled",
            "skill_benchmark/prompts/*.json",
            "skill_benchmark/annotations/acceptable_alternatives.json",
        ),
        (
            "public_gold",
            "skill_benchmark/prompts_public_gold/*.json",
            "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
        ),
    ]
    for prompt_set, prompt_glob, acceptable in prompt_sets:
        for rep in ["r1", "r2", "full"]:
            stem = f"{OUT_PREFIX}_{prompt_set}_{rep}"
            common = [
                "--prompts",
                prompt_glob,
                "--acceptable-alternatives",
                acceptable,
                "--embedding-representation",
                rep,
            ]
            conditions.append(
                (
                    f"{stem}_embedding",
                    base_cmd
                    + common
                    + [
                        "--no-reranker",
                        "--output-md",
                        f"skill_benchmark/outputs/{stem}_embedding.md",
                        "--output-json",
                        f"skill_benchmark/outputs/{stem}_embedding.json",
                    ],
                )
            )
            conditions.append(
                (
                    f"{stem}_rerank_top20",
                    base_cmd
                    + common
                    + [
                        "--rerank-candidates",
                        "20",
                        "--output-md",
                        f"skill_benchmark/outputs/{stem}_rerank_top20.md",
                        "--output-json",
                        f"skill_benchmark/outputs/{stem}_rerank_top20.json",
                    ],
                )
            )

    summary: list[dict[str, object]] = []
    summary_json = summary_md = None
    for name, cmd in conditions:
        row = run_condition(name, cmd)
        summary.append(row)
        summary_json, summary_md = write_summary(summary)

    assert summary_json is not None and summary_md is not None

    api = HfApi(token=token)
    print("uploading compact summaries...", flush=True)
    try:
        for path in [summary_json, summary_md]:
            api.upload_file(
                path_or_fileobj=str(path),
                path_in_repo=path.name,
                repo_id=REPO_ID,
                repo_type="dataset",
                commit_message="Upload SkillRouter frozen v0.4 retry summary",
            )
            print("uploaded", path.name, flush=True)
    except Exception:
        print("WARNING: compact summary upload failed", flush=True)
        traceback.print_exc()

    out_tar = pathlib.Path(f"{OUT_PREFIX}_outputs.tar.gz")
    with tarfile.open(out_tar, "w:gz") as tar:
        for path in pathlib.Path("skill_benchmark/outputs").glob(f"{OUT_PREFIX}*"):
            tar.add(path, arcname=str(path))
    print("uploading full output archive", out_tar.name, flush=True)
    try:
        api.upload_file(
            path_or_fileobj=str(out_tar),
            path_in_repo=out_tar.name,
            repo_id=REPO_ID,
            repo_type="dataset",
            commit_message="Upload SkillRouter frozen v0.4 retry outputs",
        )
        print("uploaded", out_tar.name, flush=True)
    except Exception:
        print("WARNING: full archive upload failed", flush=True)
        traceback.print_exc()

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
