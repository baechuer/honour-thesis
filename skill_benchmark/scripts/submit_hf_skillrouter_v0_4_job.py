#!/usr/bin/env python3

from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import HfApi


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> None:
    load_dotenv(Path(".env"))
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN missing from .env or environment")

    api = HfApi(token=token)
    job = api.run_uv_job(
        "skill_benchmark/scripts/hf_skillrouter_v0_4_job.py",
        flavor="t4-small",
        timeout="6h",
        secrets={"HF_TOKEN": token},
        token=token,
        _repo="baechuer1/honour-thesis-hf-job-scripts",
    )
    print("job_id", job.id)
    print("url", f"https://huggingface.co/jobs/baechuer1/{job.id}")
    print("status", job.status.stage)


if __name__ == "__main__":
    main()
