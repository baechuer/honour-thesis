#!/usr/bin/env python3
"""Capture the fixed Wave 034 public raw-skill roster exactly once per path.

The program accepts only a pre-built M2 roster.  It fetches public raw files
serially, makes no retry, stores successful UTF-8 bodies by SHA-256, flushes
the retained manifest every 25 rows, and records terminal failures in place.
It does not parse, execute, embed, score, or triage any source text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SUCCESS = "RQ1B_V3_W34_DOWNLOAD_SUCCESS_NOT_A_CLUSTER"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"roster_row_not_object:{index}")
            records.append(value)
    return records


def fetch(url: str) -> tuple[bytes | None, dict[str, Any] | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "rq1b-v3-wave034-m3"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read(), None
    except urllib.error.HTTPError as error:
        return None, {"type": "http_error", "status": error.code, "reason": str(error.reason)}
    except Exception as error:  # terminal, no-retry capture outcome
        return None, {"type": type(error).__name__, "reason": str(error)}


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    args = parse_args()
    roster = read_jsonl(args.roster)
    if not roster:
        raise SystemExit("empty_roster")
    if len({str(row.get("raw_url", "")) for row in roster}) != len(roster):
        raise SystemExit("duplicate_raw_urls_in_roster")
    artifact_dir = args.output_root / "raw_artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_root / "retrieval_manifest.jsonl"
    manifest: list[dict[str, Any]] = []
    for index, row in enumerate(roster, start=1):
        url = str(row.get("raw_url", ""))
        payload, error = fetch(url)
        base = {
            "origin_url": row.get("root"),
            "lane": row.get("domain"),
            "repository_ref": f"{row.get('root', '').removeprefix('https://github.com/')}@{row.get('commit_sha')}",
            "artifact_path": row.get("repository_path"),
            "raw_artifact_url": url,
        }
        if error is not None:
            manifest.append({**base, "status": "RQ1B_V3_W34_DOWNLOAD_FAILED_NOT_A_CLUSTER", "error": error})
        else:
            assert payload is not None
            try:
                payload.decode("utf-8")
            except UnicodeDecodeError as decode_error:
                manifest.append({**base, "status": "RQ1B_V3_W34_DOWNLOAD_INVALID_UTF8_NOT_A_CLUSTER", "error": {"type": "UnicodeDecodeError", "reason": str(decode_error)}})
            else:
                sha = hashlib.sha256(payload).hexdigest()
                artifact_path = artifact_dir / f"{sha}.md"
                if artifact_path.exists() and hashlib.sha256(artifact_path.read_bytes()).hexdigest() != sha:
                    raise SystemExit(f"local_artifact_hash_collision:{artifact_path}")
                if not artifact_path.exists():
                    artifact_path.write_bytes(payload)
                manifest.append({**base, "status": SUCCESS, "source_sha256": sha, "byte_count": len(payload), "local_raw_path": str(artifact_path)})
        if index % 25 == 0 or index == len(roster):
            write_jsonl(manifest_path, manifest)
            print(f"M3_CAPTURE_PROGRESS rows={index}/{len(roster)} success={sum(item['status'] == SUCCESS for item in manifest)}", flush=True)
    report = {
        "status": "RQ1B_V3_W34_M3_CAPTURE_COMPLETE_NOT_A_CLUSTER",
        "roster_count": len(roster),
        "retrieval_record_count": len(manifest),
        "successful_capture_count": sum(item["status"] == SUCCESS for item in manifest),
        "failed_capture_count": sum(item["status"] != SUCCESS for item in manifest),
        "network_request_attempt_count": len(manifest),
        "retry_policy": "none",
        "body_capture_count": sum(item["status"] == SUCCESS for item in manifest),
        "boundary": "Public raw source capture only; no parsing, triage, prompt, gold, selector, metric, or result occurs here.",
    }
    (args.output_root / "retrieval_report.json").write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
