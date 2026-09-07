#!/usr/bin/env python3
"""Preserve and remove an extra terminal blank line from JSON reviewer returns.

This is a format-only operation. The command accepts exact repo-relative return
paths and creates a separate, versioned preservation package before replacing
only trailing newline bytes with one final newline.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
REVIEW_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--return-path", action="append", required=True)
    parser.add_argument(
        "--complete-existing-archive",
        action="store_true",
        help="write a ledger for a prior interrupted run that already preserved the raw bytes",
    )
    args = parser.parse_args()

    destination = REVIEW_ROOT / args.package_name
    if destination.exists() and not args.complete_existing_archive:
        raise SystemExit(f"refusing to overwrite a preservation package: {destination}")
    archive = destination / "raw_original_returns_base64"
    archive.mkdir(parents=True, exist_ok=args.complete_existing_archive)

    entries = []
    for raw_relative in args.return_path:
        path = WORKSPACE / raw_relative
        raw = path.read_bytes()
        archived_path = archive / f"{path.stem}.base64"
        preexisting = raw.endswith(b"\n") and not raw.endswith(b"\n\n")
        if preexisting and args.complete_existing_archive and archived_path.is_file():
            original = base64.b64decode(archived_path.read_bytes())
            if not original.endswith(b"\n\n") or original.rstrip(b"\n") + b"\n" != raw:
                raise RuntimeError(f"existing archive does not replay the normalisation for {path}")
            repaired = raw
            transformation = "prior interrupted run already removed terminal blank line(s); archive replay verified and ledger materialised"
        else:
            if not raw.endswith(b"\n\n"):
                raise SystemExit(f"{path} does not have an extra terminal blank line")
            repaired = raw.rstrip(b"\n") + b"\n"
            json.loads(repaired.decode("utf-8"))
            archived_path.write_bytes(base64.b64encode(raw) + b"\n")
            if base64.b64decode(archived_path.read_bytes()) != raw:
                raise RuntimeError(f"archive replay mismatch for {path}")
            path.write_bytes(repaired)
            transformation = "remove trailing blank line(s), retain exactly one final newline"
        entries.append(
            {
                "return_path": raw_relative,
                "preserved_raw_base64_path": str(archived_path.relative_to(WORKSPACE)),
                "original_sha256": sha256(raw),
                "repaired_sha256": sha256(repaired),
                "transformation": transformation,
                "semantic_change": False,
                "archive_replay_verified": True,
            }
        )

    ledger = {
        "schema_version": "rq2b_nc_phase5_v7_final_newline_preservation_repair_v1",
        "scope": "format repair only; no review semantics or target information touched",
        "entries": entries,
    }
    (destination / "format_repair_ledger.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )
    (destination / "README.md").write_text(
        "# Preserved final-newline format repair\n\n"
        "The original reviewer byte stream is retained as a base64 artifact. The canonical "
        "copy only has terminal blank-line bytes normalised to one final newline; no review "
        "content is changed.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
