#!/usr/bin/env python3
"""Stage a pinned public `SKILL.md` source set for RQ1b discovery only.

The input must already be a local clone. This script never downloads or
executes source content. It byte-copies original skill files and their source
provenance into an RQ1b-only staging directory; nothing it writes is a cluster,
prompt, label, review decision, selector input, or experimental result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


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


def existing_hashes(roots: list[Path]) -> set[str]:
    hashes: set[str] = set()
    for root in roots:
        if root.exists():
            hashes.update(sha256_bytes(path.read_bytes()) for path in root.rglob(ORIGINAL_FILE))
    return hashes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True, help="Local clone of one pinned public repository.")
    parser.add_argument("--source-search-root", type=Path, default=Path("."), help="Path under source root in which to find SKILL.md files.")
    parser.add_argument(
        "--source-file-list-json",
        type=Path,
        default=None,
        help=(
            "Optional repository-relative JSON selection file. Accepts either a list of "
            "SKILL.md paths or an object with a `components` list containing `path` values."
        ),
    )
    parser.add_argument(
        "--exclude-source-prefix",
        action="append",
        default=[],
        help="Repository-relative source-file prefix to exclude; repeatable.",
    )
    parser.add_argument("--destination", type=Path, required=True, help="Empty RQ1b source-only staging directory.")
    parser.add_argument("--origin", required=True, help="Repository owner/name recorded in provenance.")
    parser.add_argument("--repository-url", required=True, help="Canonical public repository URL.")
    parser.add_argument("--pinned-commit", required=True, help="Exact checked-out commit SHA.")
    parser.add_argument("--license-path", type=Path, default=Path("LICENSE"), help="Licence path relative to source root.")
    parser.add_argument("--license-id", required=True, help="Declared repository licence identifier, or NO_DECLARED_REPOSITORY_LICENSE.")
    parser.add_argument(
        "--allow-no-license",
        action="store_true",
        help=(
            "Permit a public source with no repository licence file. Such a source is "
            "labelled local-analysis-only and its licence is never inferred or copied."
        ),
    )
    parser.add_argument("--skill-prefix", required=True, help="Stable prefix for staged skill identifiers.")
    parser.add_argument("--require-frontmatter-license", default=None, help="If set, only stage files with this exact frontmatter licence.")
    parser.add_argument(
        "--existing-source-roots",
        type=Path,
        nargs="*",
        default=[
            Path("skill_benchmark/skills/public_imported_background"),
            Path("skill_benchmark/rq1b_naturalistic_public_replication/staged_sources"),
        ],
        help="Roots used only for exact-byte duplicate screening.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    search_root = (source_root / args.source_search_root).resolve()
    destination = args.destination.resolve()
    license_path = (source_root / args.license_path).resolve()

    if not source_root.is_dir() or not search_root.is_dir():
        raise SystemExit(f"Missing source root or search root: {source_root} / {search_root}")
    has_license_file = license_path.is_file()
    if not has_license_file and not args.allow_no_license:
        raise SystemExit(f"Missing source licence: {license_path}")
    if not has_license_file and args.license_id != "NO_DECLARED_REPOSITORY_LICENSE":
        raise SystemExit("A no-licence source must use license-id NO_DECLARED_REPOSITORY_LICENSE")
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"Destination must be absent or empty: {destination}")

    if args.source_file_list_json:
        selection_path = (source_root / args.source_file_list_json).resolve()
        if not selection_path.is_file():
            raise SystemExit(f"Missing source selection file: {selection_path}")
        payload = json.loads(selection_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload = payload.get("components", payload.get("paths"))
        if not isinstance(payload, list):
            raise SystemExit("Selection JSON must be a list or an object with a `components` list")
        relative_paths: list[str] = []
        for item in payload:
            value = item.get("path") if isinstance(item, dict) else item
            if not isinstance(value, str) or not value.endswith("SKILL.md"):
                raise SystemExit(f"Invalid selected SKILL.md path: {item!r}")
            if any(value.startswith(prefix) for prefix in args.exclude_source_prefix):
                continue
            relative_paths.append(value)
        if len(relative_paths) != len(set(relative_paths)):
            raise SystemExit("Selection JSON contains duplicate source paths")
        source_files = sorted((source_root / value).resolve() for value in relative_paths)
        if any(not path.is_file() or source_root not in path.parents for path in source_files):
            raise SystemExit("Selection JSON references a missing or outside-source file")
    else:
        source_files = sorted(
            path for path in search_root.rglob("SKILL.md") if ".git" not in path.parts
        )
    if not source_files:
        raise SystemExit(f"No SKILL.md files found below {search_root}")

    license_bytes = license_path.read_bytes() if has_license_file else None
    license_sha256 = sha256_bytes(license_bytes) if license_bytes is not None else None
    license_status = (
        "DECLARED_REPOSITORY_LICENSE"
        if license_bytes is not None
        else "NO_DECLARED_REPOSITORY_LICENSE_LOCAL_ANALYSIS_ONLY"
    )
    license_line = (
        f"- Licence: `{args.license_id}` (verbatim copy in `LICENSE`)\n"
        if license_bytes is not None
        else "- Licence: `NO_DECLARED_REPOSITORY_LICENSE_LOCAL_ANALYSIS_ONLY`; no licence is inferred or copied.\n"
    )
    prior_hashes = existing_hashes([root.resolve() for root in args.existing_source_roots])
    records: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    destination.mkdir(parents=True, exist_ok=True)

    for source_file in source_files:
        raw = source_file.read_bytes()
        source_sha256 = sha256_bytes(raw)
        relative_source = source_file.relative_to(source_root).as_posix()
        relative_skill_dir = source_file.parent.relative_to(search_root).as_posix()
        skill_id = f"{args.skill_prefix}-{slugify(relative_skill_dir)}"
        if skill_id in seen_ids:
            # Non-ASCII repository paths can normalise to the same ASCII slug.
            # Preserve the readable base while making the staged identity stable.
            skill_id = f"{skill_id}-{sha256_bytes(relative_skill_dir.encode('utf-8'))[:10]}"
        if skill_id in seen_ids:
            raise SystemExit(f"Slug collision after stable path suffix: {skill_id}")
        seen_ids.add(skill_id)

        text = raw.decode("utf-8", errors="replace")
        frontmatter_license = frontmatter_value(text, "license")
        record: dict[str, object] = {
            "skill_id": skill_id,
            "source_status": "STAGED_SOURCE_ONLY_NOT_A_CLUSTER",
            "origin": args.origin,
            "repository_url": args.repository_url,
            "pinned_commit": args.pinned_commit,
            "source_repository_path": relative_source,
            "source_url": f"{args.repository_url}/blob/{args.pinned_commit}/{relative_source}",
            "license": args.license_id,
            "license_status": license_status,
            "license_path": args.license_path.as_posix() if has_license_file else None,
            "license_sha256": license_sha256,
            "frontmatter_license": frontmatter_license,
            "source_sha256": source_sha256,
            "source_bytes": len(raw),
            "frontmatter_name": frontmatter_value(text, "name"),
            "frontmatter_description": frontmatter_value(text, "description"),
            "screening": [],
        }

        if source_sha256 in prior_hashes:
            record["source_status"] = "SKIPPED_EXACT_DUPLICATE_OF_EXISTING_SOURCE"
            record["screening"].append("exact_byte_duplicate")
        elif not record["frontmatter_name"] or not record["frontmatter_description"]:
            record["source_status"] = "SKIPPED_MISSING_REQUIRED_FRONTMATTER"
            record["screening"].append("missing_name_or_description")
        elif args.require_frontmatter_license and frontmatter_license != args.require_frontmatter_license:
            record["source_status"] = "SKIPPED_FRONTMATTER_LICENSE_MISMATCH"
            record["screening"].append("frontmatter_license_mismatch")
        else:
            target_source_dir = destination / "skills" / skill_id / "source"
            target_source_dir.mkdir(parents=True, exist_ok=False)
            target_original = target_source_dir / ORIGINAL_FILE
            shutil.copyfile(source_file, target_original)
            if sha256_bytes(target_original.read_bytes()) != source_sha256:
                raise SystemExit(f"Integrity failure copying {source_file}")
            (target_source_dir / "IMPORT.json").write_text(
                json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        records.append(record)

    if license_bytes is not None:
        (destination / "LICENSE").write_bytes(license_bytes)
    (destination / "SOURCESET.md").write_text(
        "# RQ1b Staged Public Source Set\n\n"
        f"- Origin: [{args.repository_url}]({args.repository_url})\n"
        f"- Pinned commit: `{args.pinned_commit}`\n"
        f"{license_line}"
        "- Acquisition: locally cloned repository; no source script was executed.\n"
        "- Role: source-candidate expansion only. These files are not RQ1b clusters, prompts, gold labels, acceptable sets, or retrieval results.\n"
        "- Eligibility: each eventual card requires independent original-source review, source-evidence spans, and later blinded acceptability review.\n",
        encoding="utf-8",
    )
    (destination / "source_expansion_manifest.jsonl").write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8"
    )
    summary = {
        "status": "LOCAL_STAGED_SOURCE_EXPANSION_ONLY_NOT_A_BENCHMARK_OR_RESULT",
        "origin": args.origin,
        "repository_url": args.repository_url,
        "pinned_commit": args.pinned_commit,
        "license": args.license_id,
        "license_sha256": license_sha256,
        "license_status": license_status,
        "discovered_skill_files": len(source_files),
        "staged_sources": sum(record["source_status"] == "STAGED_SOURCE_ONLY_NOT_A_CLUSTER" for record in records),
        "skipped_exact_duplicates": sum(record["source_status"] == "SKIPPED_EXACT_DUPLICATE_OF_EXISTING_SOURCE" for record in records),
        "skipped_missing_frontmatter": sum(record["source_status"] == "SKIPPED_MISSING_REQUIRED_FRONTMATTER" for record in records),
        "skipped_frontmatter_license_mismatch": sum(record["source_status"] == "SKIPPED_FRONTMATTER_LICENSE_MISMATCH" for record in records),
        "source_file_list_json": args.source_file_list_json.as_posix() if args.source_file_list_json else None,
        "excluded_source_prefixes": args.exclude_source_prefix,
        "exclusions": [
            "No downloaded source content was executed.",
            "No prompt, gold label, acceptable-set judgement, retrieval score, embedding, model call, or experiment was created.",
            "Staging a source does not establish semantic-neighbour validity or RQ1b eligibility.",
        ],
    }
    (destination / "source_expansion_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
