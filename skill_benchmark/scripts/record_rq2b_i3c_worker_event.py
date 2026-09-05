#!/usr/bin/env python3
"""Append one manifest-bound RQ2b I3C worker event after explicit validation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from validate_rq2b_i3c_chunk import DEFAULT_MANIFEST, validate_chunk


VERSION_ID = "rq2b-full-library-v1.1-2026-08-15"
EVENT_PATH = Path(
    "skill_benchmark/rq2b_full_library/rq2b-full-library-v1-2026-08-02/"
    "i3c_extraction/worker_events.jsonl"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def existing_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-index", type=int, required=True)
    parser.add_argument("--attempt-index", type=int, required=True)
    parser.add_argument("--worker-id", required=True)
    parser.add_argument("--started-at", type=float, required=True)
    parser.add_argument("--completed-at", type=float, required=True)
    parser.add_argument("--status", choices=("completed", "failed"), required=True)
    parser.add_argument("--failure-reason")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--event-path", type=Path, default=EVENT_PATH)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    event_path = args.event_path if args.event_path.is_absolute() else root / args.event_path
    if args.completed_at < args.started_at:
        raise ValueError("completed-at must not precede started-at")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    chunks = {int(chunk["chunk_index"]): chunk for chunk in manifest["chunks"]}
    if args.chunk_index not in chunks:
        raise ValueError(f"Unknown chunk index: {args.chunk_index}")
    chunk = chunks[args.chunk_index]
    prior = existing_events(event_path)
    if any(event.get("worker_id") == args.worker_id for event in prior):
        raise ValueError("worker-id is already recorded")
    if any(event.get("chunk_index") == args.chunk_index and event.get("attempt_index") == args.attempt_index for event in prior):
        raise ValueError("chunk attempt is already recorded")
    if args.status == "completed":
        if args.failure_reason is not None:
            raise ValueError("completed event cannot have failure reason")
        report = validate_chunk(root, manifest_path, args.chunk_index)
        output_path = root / report["output_path"]
        output_path_value: str | None = report["output_path"]
        output_sha256: str | None = sha256_file(output_path)
        output_rows = report["rows"]
        failure_reason = None
    else:
        if not args.failure_reason:
            raise ValueError("failed event needs failure reason")
        output_path_value = None
        output_sha256 = None
        output_rows = 0
        failure_reason = args.failure_reason
    event = {
        "attempt_index": args.attempt_index,
        "automatic_retry": False,
        "chunk_index": args.chunk_index,
        "completed_at_epoch_seconds": args.completed_at,
        "external_api_calls": 0,
        "failure_reason": failure_reason,
        "input_path": chunk["input_path"],
        "input_sha256": chunk["input_sha256"],
        "network_calls": 0,
        "output_path": output_path_value,
        "output_rows": output_rows,
        "output_sha256": output_sha256,
        "schema_version": "rq2b-i3c-worker-event-v1",
        "started_at_epoch_seconds": args.started_at,
        "status": args.status,
        "version_id": VERSION_ID,
        "worker_id": args.worker_id,
    }
    event_path.parent.mkdir(parents=True, exist_ok=True)
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
    print(json.dumps(event, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
