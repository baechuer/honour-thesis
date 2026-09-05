#!/usr/bin/env python3
"""One-shot capture of Wave 039 pinned SKILL.md bodies from a frozen M2 roster."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/?$")


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    roster = [json.loads(line) for line in args.roster.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not roster or any(row.get("m2_status") != "RQ1B_V3_W39_M2_PATH_ROSTER_NOT_A_SOURCE_OR_RESULT" for row in roster):
        raise SystemExit("invalid_m2_roster")
    raw_dir = args.output_root / "raw"
    raw_dir.mkdir(parents=True, exist_ok=False)
    capture_rows = []
    for index, row in enumerate(roster, start=1):
        match = ROOT_RE.fullmatch(row["root"])
        if not match:
            raise SystemExit(f"invalid_root:{row['capture_id']}")
        owner, repo = match.groups()
        quoted_path = urllib.parse.quote(row["repository_path"], safe="/")
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{row['commit_sha']}/{quoted_path}"
        request = urllib.request.Request(url, headers={"User-Agent": "rq1b-v3-w39-m3"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
            destination = raw_dir / f"{row['capture_id']}--{slug(owner)}--{slug(repo)}--{hashlib.sha256(row['repository_path'].encode('utf-8')).hexdigest()[:16]}.md"
            destination.write_bytes(body)
            capture_rows.append({**row, "raw_url": url, "status": "RQ1B_V3_W39_M3_CAPTURE_PASS_NOT_ADMITTED", "http_attempt_count": 1, "byte_count": len(body), "sha256": hashlib.sha256(body).hexdigest(), "relative_capture_path": destination.relative_to(args.output_root).as_posix()})
        except urllib.error.HTTPError as error:
            capture_rows.append({**row, "raw_url": url, "status": "RQ1B_V3_W39_M3_CAPTURE_HTTP_FAILURE_NOT_ADMITTED", "http_attempt_count": 1, "http_status": error.code, "error": str(error.reason)})
        except Exception as error:
            capture_rows.append({**row, "raw_url": url, "status": "RQ1B_V3_W39_M3_CAPTURE_FAILURE_NOT_ADMITTED", "http_attempt_count": 1, "error_type": type(error).__name__, "error": str(error)[:400]})
        print(f"M3_PROGRESS captures={index}/{len(roster)} passes={sum(item['status'] == 'RQ1B_V3_W39_M3_CAPTURE_PASS_NOT_ADMITTED' for item in capture_rows)}", flush=True)
    args.output_root.joinpath("capture_manifest.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in capture_rows), encoding="utf-8")
    passes = sum(row["status"] == "RQ1B_V3_W39_M3_CAPTURE_PASS_NOT_ADMITTED" for row in capture_rows)
    summary = {
        "status": "RQ1B_V3_W39_M3_ONE_SHOT_CAPTURE_COMPLETE_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "roster_count": len(roster),
        "successful_capture_count": passes,
        "failed_capture_count": len(roster) - passes,
        "network_request_attempt_count": len(roster),
        "retry_policy": "none",
        "claim_boundary": "This is public raw-source capture at pinned commits. It is not source-frame admission, deduplication, triage, cluster construction, prompt construction, label, selector input, metric or result.",
    }
    args.output_root.joinpath("retrieval_report.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("roster_count", "successful_capture_count", "failed_capture_count")}, sort_keys=True))
    return 0 if passes == len(roster) else 1


if __name__ == "__main__":
    raise SystemExit(main())
