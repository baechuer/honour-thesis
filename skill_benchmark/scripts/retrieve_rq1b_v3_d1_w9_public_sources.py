#!/usr/bin/env python3
"""Retrieve a versioned public raw-skill intake once and persist byte provenance.

No retry is attempted.  A fetch failure, non-UTF-8 response, oversized file or
HTML-shaped response is retained in the manifest as a failure rather than
silently repaired.  This is source acquisition only; it does not mutate the
prior frozen source frame or decide D1/C1 eligibility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


MAX_BYTES = 1_000_000
DEFAULT_STATUS = "RQ1B_V3_D1_W9_PUBLIC_SOURCE_INTAKE_DRAFT_NOT_A_CLUSTER"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_row_not_object:{path}:{number}")
            rows.append(value)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", type=Path, action="append", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=20)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--expected-status", default=DEFAULT_STATUS)
    parser.add_argument("--status-prefix", default="RQ1B_V3_D1_W9")
    return parser.parse_args()


def response_record(row: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {
        "status": extra.pop("status"),
        "lane": row.get("lane"),
        "origin_url": row.get("origin_url"),
        "repository_ref": row.get("repository_ref"),
        "artifact_path": row.get("artifact_path"),
        "raw_artifact_url": row.get("raw_artifact_url"),
        **extra,
    }


def main() -> int:
    args = parse_args()
    output_root = args.output_root
    raw_dir = output_root / "raw_artifacts"
    raw_dir.mkdir(parents=True, exist_ok=True)
    if args.progress_every <= 0:
        raise SystemExit("progress_every_must_be_positive")
    rows = [row for path in args.draft for row in read_jsonl(path)]
    manifest_path = output_root / "retrieval_manifest.jsonl"
    manifest = read_jsonl(manifest_path) if manifest_path.is_file() else []
    recorded_by_url = {str(item.get("raw_artifact_url", "")): item for item in manifest}
    if len(recorded_by_url) != len(manifest):
        raise SystemExit("existing_manifest_duplicate_or_missing_url")
    input_urls: set[str] = set()
    new_attempts = 0

    def persist(item: dict[str, Any]) -> None:
        manifest.append(item)
        recorded_by_url[str(item["raw_artifact_url"])] = item
        with manifest_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(item, ensure_ascii=True, sort_keys=True) + "\n")
            handle.flush()

    for row in rows:
        if row.get("status") != args.expected_status:
            raise SystemExit(f"unexpected_intake_status:{row.get('raw_artifact_url')}")
        url = str(row.get("raw_artifact_url", ""))
        if not url or url in input_urls:
            raise SystemExit(f"missing_or_duplicate_raw_url:{url}")
        input_urls.add(url)
        if url in recorded_by_url:
            continue
        new_attempts += 1
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "RQ1b-V3-public-source-intake/1.0"})
            with urllib.request.urlopen(request, timeout=args.timeout_seconds) as response:
                body = response.read(MAX_BYTES + 1)
                content_type = str(response.headers.get("Content-Type", ""))
                status_code = getattr(response, "status", None)
        except urllib.error.HTTPError as error:
            record = response_record(row, status=f"{args.status_prefix}_DOWNLOAD_HTTP_FAILURE_NOT_A_CLUSTER", http_status=error.code, error=str(error.reason))
        except Exception as error:  # urllib exposes several transport exceptions.
            record = response_record(row, status=f"{args.status_prefix}_DOWNLOAD_TRANSPORT_FAILURE_NOT_A_CLUSTER", error=f"{type(error).__name__}:{error}")
        else:
            if len(body) > MAX_BYTES:
                record = response_record(row, status=f"{args.status_prefix}_DOWNLOAD_OVERSIZE_NOT_A_CLUSTER", http_status=status_code, content_type=content_type, byte_count=len(body))
            else:
                try:
                    text = body.decode("utf-8")
                except UnicodeDecodeError as error:
                    record = response_record(row, status=f"{args.status_prefix}_DOWNLOAD_NON_UTF8_NOT_A_CLUSTER", http_status=status_code, content_type=content_type, byte_count=len(body), error=str(error))
                else:
                    if not text.strip() or re.match(r"^\s*(?:<!doctype html|<html|<head|<body)\b", text, flags=re.IGNORECASE):
                        record = response_record(row, status=f"{args.status_prefix}_DOWNLOAD_NON_ARTIFACT_RESPONSE_NOT_A_CLUSTER", http_status=status_code, content_type=content_type, byte_count=len(body))
                    else:
                        body_sha256 = hashlib.sha256(body).hexdigest()
                        raw_path = raw_dir / f"{body_sha256}.md"
                        raw_path.write_bytes(body)
                        record = response_record(
                            row,
                            status=f"{args.status_prefix}_DOWNLOAD_SUCCESS_NOT_A_CLUSTER",
                            http_status=status_code,
                            content_type=content_type,
                            byte_count=len(body),
                            source_sha256=body_sha256,
                            local_raw_path=str(raw_path),
                        )
        persist(record)
        if new_attempts % args.progress_every == 0:
            success_count = sum(item["status"] == f"{args.status_prefix}_DOWNLOAD_SUCCESS_NOT_A_CLUSTER" for item in manifest)
            print(json.dumps({"status": "DOWNLOAD_PROGRESS", "new_attempts": new_attempts, "recorded": len(manifest), "successes": success_count}, sort_keys=True), flush=True)
    success_status = f"{args.status_prefix}_DOWNLOAD_SUCCESS_NOT_A_CLUSTER"
    successes = [item for item in manifest if item["status"] == success_status]
    report = {
        "status": f"{args.status_prefix}_DOWNLOAD_COMPLETED_NOT_A_CLUSTER",
        "request_attempts": len(manifest),
        "request_attempts_this_run": new_attempts,
        "success_count": len(successes),
        "failure_count": len(manifest) - len(successes),
        "unique_downloaded_sha256_count": len({item["source_sha256"] for item in successes}),
        "failure_status_counts": {
            status: sum(item["status"] == status for item in manifest)
            for status in sorted({item["status"] for item in manifest if item["status"] != success_status})
        },
        "boundary": "Downloaded public source bytes only. Existing source-frame membership, source quality, D1/C1 eligibility, cluster membership, prompt, label, selector, metric and result remain undecided.",
    }
    (output_root / "retrieval_report.json").write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
