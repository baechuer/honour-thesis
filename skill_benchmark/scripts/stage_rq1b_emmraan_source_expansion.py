#!/usr/bin/env python3
"""Stage a pinned public skill source set for RQ1b without touching RQ2 inputs.

This is a local-only provenance-preserving import. It does not download code,
execute source content, generate prompts, create labels, or run any selector.
The staged files are source candidates only; RQ1b cards still require manual
original-source review before they may enter the naturalistic replication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


REPO_URL = "https://github.com/Emmraan/agent-skills"
PINNED_COMMIT = "1124ce406f47ba7c5c54e18c5f86f70ebd51c33d"
LICENSE_ID = "MIT"
SKILL_FILE = "SKILL.md"
ORIGINAL_FILE = "SKILL.original.md"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def slugify(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return result or "unknown"


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.match(r"^---\s*\n([\s\S]*?)\n---", text)
    if not match:
        return None
    field = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", match.group(1), re.MULTILINE)
    if not field:
        return None
    value = field.group(1).strip().strip("\"'")
    return " ".join(value.split()) or None


def source_hashes(root: Path) -> set[str]:
    hashes: set[str] = set()
    if not root.exists():
        return hashes
    for path in root.rglob(ORIGINAL_FILE):
        hashes.add(sha256_bytes(path.read_bytes()))
    return hashes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True, help="Local clone of the pinned source repository.")
    parser.add_argument("--destination", type=Path, required=True, help="Empty RQ1b staging directory to create.")
    parser.add_argument(
        "--existing-source-root",
        type=Path,
        default=Path("skill_benchmark/skills/public_imported_background"),
        help="Existing originals used only for exact-byte duplicate screening.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    skill_root = source_root / "skills"
    destination = args.destination.resolve()
    existing_root = args.existing_source_root.resolve()
    license_path = source_root / "LICENSE"

    if not skill_root.is_dir():
        raise SystemExit(f"Missing source skill root: {skill_root}")
    if not license_path.is_file():
        raise SystemExit(f"Missing source licence: {license_path}")
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"Destination must be absent or empty: {destination}")

    source_files = sorted(skill_root.rglob(SKILL_FILE))
    if not source_files:
        raise SystemExit(f"No {SKILL_FILE} files found below {skill_root}")

    existing_hashes = source_hashes(existing_root)
    license_bytes = license_path.read_bytes()
    license_sha256 = sha256_bytes(license_bytes)
    records: list[dict[str, object]] = []
    seen_ids: set[str] = set()

    destination.mkdir(parents=True, exist_ok=True)
    for source_file in source_files:
        raw = source_file.read_bytes()
        source_sha256 = sha256_bytes(raw)
        relative_source = source_file.relative_to(source_root).as_posix()
        relative_skill_dir = source_file.parent.relative_to(skill_root).as_posix()
        skill_id = f"public-emmraan-{slugify(relative_skill_dir)}"
        if skill_id in seen_ids:
            raise SystemExit(f"Slug collision: {skill_id}")
        seen_ids.add(skill_id)

        text = raw.decode("utf-8", errors="replace")
        source_url = f"{REPO_URL}/blob/{PINNED_COMMIT}/{relative_source}"
        record: dict[str, object] = {
            "skill_id": skill_id,
            "source_status": "STAGED_SOURCE_ONLY_NOT_A_CLUSTER",
            "origin": "Emmraan/agent-skills",
            "repository_url": REPO_URL,
            "pinned_commit": PINNED_COMMIT,
            "source_repository_path": relative_source,
            "source_url": source_url,
            "license": LICENSE_ID,
            "license_path": "LICENSE",
            "license_sha256": license_sha256,
            "source_sha256": source_sha256,
            "source_bytes": len(raw),
            "frontmatter_name": frontmatter_value(text, "name"),
            "frontmatter_description": frontmatter_value(text, "description"),
            "screening": [],
        }

        if source_sha256 in existing_hashes:
            record["source_status"] = "SKIPPED_EXACT_DUPLICATE_OF_EXISTING_SOURCE"
            record["screening"].append("exact_byte_duplicate")
            records.append(record)
            continue
        if not record["frontmatter_name"] or not record["frontmatter_description"]:
            record["source_status"] = "SKIPPED_MISSING_REQUIRED_FRONTMATTER"
            record["screening"].append("missing_name_or_description")
            records.append(record)
            continue

        target_source_dir = destination / "skills" / skill_id / "source"
        target_source_dir.mkdir(parents=True, exist_ok=False)
        target_original = target_source_dir / ORIGINAL_FILE
        shutil.copyfile(source_file, target_original)
        target_hash = sha256_bytes(target_original.read_bytes())
        if target_hash != source_sha256:
            raise SystemExit(f"Integrity failure copying {source_file}")
        (target_source_dir / "IMPORT.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        records.append(record)

    (destination / "LICENSE").write_bytes(license_bytes)
    (destination / "SOURCESET.md").write_text(
        "# RQ1b Staged Public Source Set\n\n"
        f"- Origin: [{REPO_URL}]({REPO_URL})\n"
        f"- Pinned commit: `{PINNED_COMMIT}`\n"
        f"- Licence: `{LICENSE_ID}` (verbatim copy in `LICENSE`)\n"
        "- Acquisition: local clone only; no source script was executed.\n"
        "- Role: source-candidate expansion only. These files are not RQ1b clusters, "
        "prompts, gold labels, acceptable sets, or retrieval results.\n"
        "- Eligibility: each eventual card requires independent manual original-source "
        "review, source-evidence spans, and later blinded acceptability review.\n",
        encoding="utf-8",
    )
    (destination / "source_expansion_manifest.jsonl").write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    summary = {
        "status": "LOCAL_STAGED_SOURCE_EXPANSION_ONLY_NOT_A_BENCHMARK_OR_RESULT",
        "origin": "Emmraan/agent-skills",
        "repository_url": REPO_URL,
        "pinned_commit": PINNED_COMMIT,
        "license": LICENSE_ID,
        "license_sha256": license_sha256,
        "discovered_skill_files": len(source_files),
        "staged_sources": sum(record["source_status"] == "STAGED_SOURCE_ONLY_NOT_A_CLUSTER" for record in records),
        "skipped_exact_duplicates": sum(record["source_status"] == "SKIPPED_EXACT_DUPLICATE_OF_EXISTING_SOURCE" for record in records),
        "skipped_missing_frontmatter": sum(record["source_status"] == "SKIPPED_MISSING_REQUIRED_FRONTMATTER" for record in records),
        "exclusions": [
            "No downloaded source content was executed.",
            "No prompt, gold label, acceptable-set judgement, retrieval score, embedding, model call, or experiment was created.",
            "Staging a source does not establish semantic-neighbour validity or RQ1b eligibility.",
        ],
    }
    (destination / "source_expansion_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
