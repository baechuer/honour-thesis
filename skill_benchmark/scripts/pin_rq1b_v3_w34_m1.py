#!/usr/bin/env python3
"""Pin Wave 034 GitHub roots and enumerate skill paths without fetching bodies.

This is a provenance-only M1 step.  Each selected public root receives at most
one commit request and one recursive-tree request, with no retry.  It records
both successful metadata and failures; no source artifact body is downloaded.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leads", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--max-roots", type=int, default=17)
    return parser.parse_args()


def request_json(url: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "rq1b-v3-wave034-m1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            value = json.loads(response.read().decode("utf-8"))
        if not isinstance(value, dict):
            return None, {"type": "non_object_json", "url": url}
        return value, None
    except urllib.error.HTTPError as error:
        return None, {"type": "http_error", "url": url, "status": error.code, "reason": str(error.reason)}
    except Exception as error:  # retained as a terminal no-retry attempt
        return None, {"type": type(error).__name__, "url": url, "reason": str(error)}


def safe_name(owner: str, repository: str) -> str:
    return f"{owner}-{repository}".lower().replace("_", "-")


def main() -> int:
    args = parse_args()
    leads = json.loads(args.leads.read_text(encoding="utf-8"))
    if not isinstance(leads, list):
        raise SystemExit("lead_list_not_array")
    selected = [row for row in leads if isinstance(row, dict) and row.get("priority") == "high"][: args.max_roots]
    if len(selected) != args.max_roots:
        raise SystemExit(f"insufficient_high_priority_roots:{len(selected)}")

    metadata_dir = args.output_root / "m1_pinned_metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    path_rows: list[dict[str, Any]] = []
    root_rows: list[dict[str, Any]] = []
    for index, lead in enumerate(selected, start=1):
        root = str(lead.get("root", ""))
        match = ROOT_RE.fullmatch(root)
        if not match:
            root_rows.append({"root": root, "status": "M1_REJECT_INVALID_ROOT", "attempt_count": 0})
            continue
        owner, repository = match.groups()
        slug = safe_name(owner, repository)
        commit_url = f"https://api.github.com/repos/{owner}/{repository}/commits/HEAD"
        commit, commit_error = request_json(commit_url)
        if commit_error is not None:
            root_rows.append({"root": root, "status": "M1_COMMIT_FETCH_FAILED", "attempt_count": 1, "error": commit_error})
            continue
        (metadata_dir / f"{slug}-commit.json").write_text(json.dumps(commit, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        sha = str(commit.get("sha", ""))
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            root_rows.append({"root": root, "status": "M1_INVALID_COMMIT_SHA", "attempt_count": 1, "commit_sha": sha})
            continue
        tree_url = f"https://api.github.com/repos/{owner}/{repository}/git/trees/{sha}?recursive=1"
        tree, tree_error = request_json(tree_url)
        if tree_error is not None:
            root_rows.append({"root": root, "status": "M1_TREE_FETCH_FAILED", "attempt_count": 2, "commit_sha": sha, "error": tree_error})
            continue
        (metadata_dir / f"{slug}-tree.json").write_text(json.dumps(tree, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        entries = tree.get("tree", [])
        if not isinstance(entries, list):
            root_rows.append({"root": root, "status": "M1_INVALID_TREE", "attempt_count": 2, "commit_sha": sha})
            continue
        paths = []
        for entry in entries:
            if not isinstance(entry, dict) or entry.get("type") != "blob":
                continue
            path = str(entry.get("path", ""))
            if path.lower().endswith("skill.md"):
                paths.append(path)
        for path in sorted(set(paths)):
            path_rows.append(
                {
                    "status": "RQ1B_V3_W34_M1_PATH_ONLY_NOT_A_SOURCE_BODY_OR_RESULT",
                    "root": root,
                    "domain": lead.get("domain"),
                    "scout": lead.get("scout"),
                    "commit_sha": sha,
                    "repository_path": path,
                }
            )
        root_rows.append(
            {
                "root": root,
                "domain": lead.get("domain"),
                "status": "M1_PIN_AND_TREE_PASS",
                "attempt_count": 2,
                "commit_sha": sha,
                "skill_path_count": len(set(paths)),
            }
        )
        print(f"M1_PROGRESS roots={index}/{len(selected)} paths={len(path_rows)}", flush=True)

    (args.output_root / "m1_pinned_skill_paths.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in path_rows), encoding="utf-8"
    )
    summary = {
        "status": "RQ1B_V3_W34_M1_PINNED_METADATA_COMPLETE_NOT_A_SOURCE_OR_RESULT",
        "selected_root_count": len(selected),
        "root_rows": root_rows,
        "successful_root_count": sum(row.get("status") == "M1_PIN_AND_TREE_PASS" for row in root_rows),
        "failed_root_count": sum(row.get("status") != "M1_PIN_AND_TREE_PASS" for row in root_rows),
        "path_only_skill_count": len(path_rows),
        "network_request_attempt_ceiling": len(selected) * 2,
        "network_request_attempt_count": sum(int(row.get("attempt_count", 0)) for row in root_rows),
        "retry_policy": "none",
        "body_capture_count": 0,
        "boundary": "Commit/tree metadata and paths only; this has no source bodies, triage, prompt, gold, selector, metric, or result.",
    }
    (args.output_root / "M1_PINNED_ROOTS_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("selected_root_count", "successful_root_count", "failed_root_count", "path_only_skill_count", "network_request_attempt_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
