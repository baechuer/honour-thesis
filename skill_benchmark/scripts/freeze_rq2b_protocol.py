#!/usr/bin/env python3
"""Freeze the explicitly approved RQ2b protocol and corpus inputs."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from audit_rq2b_preflight import parse_frontmatter
from rq2b_common import (
    APPROVAL_PACKET_RELATIVE_PATH,
    APPROVED_PACKET_SHA256,
    APPROVED_PROTOCOL_SHA256,
    APPROVED_SCOPE_SHA256,
    PROTOCOL_RELATIVE_PATH,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    verify_approval_packet,
    verify_frozen_manifest,
    version_root,
    write_bytes_new,
    write_json_new,
    write_jsonl_new,
)


PREFLIGHT_ROOT = Path("skill_benchmark/outputs/rq2b/preflight")
ENFORCED_PACKET_INPUTS = {
    "skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md",
    "skill_benchmark/annotations/acceptable_alternatives.json",
    "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    "skill_benchmark/annotations/low_information_acceptables.json",
}


def load_frozen_prompts(
    root: Path,
    preflight_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_cache: dict[str, list[dict[str, Any]]] = {}
    frozen: list[dict[str, Any]] = []
    for row in preflight_rows:
        source_path = row["source_path"]
        if source_path not in source_cache:
            payload = read_json(root / source_path)
            require(isinstance(payload, list), f"Prompt file is not an array: {source_path}")
            require(
                sha256_file(root / source_path) == row["source_file_sha256"],
                f"Prompt file drift: {source_path}",
            )
            source_cache[source_path] = payload
        source_rows = source_cache[source_path]
        source_index = int(row["source_row_index"])
        require(source_index < len(source_rows), f"Prompt row out of range: {source_path}")
        raw = source_rows[source_index]
        require(raw.get("id") == row["prompt_id"], f"Prompt identity drift: {source_path}")
        prompt = str(raw.get("prompt") or "")
        require(sha256_text(prompt) == row["prompt_sha256"], f"Prompt text drift: {row['prompt_id']}")
        require(raw.get("gold_skill") == row["gold_skill"], f"Gold drift: {row['prompt_id']}")
        require(
            list(raw.get("closest_alternatives") or []) == row["closest_alternatives"],
            f"Alternative drift: {row['prompt_id']}",
        )
        frozen.append({**row, "prompt": prompt})
    return frozen


def add_file(
    records: dict[str, dict[str, Any]],
    root: Path,
    path_text: str,
    role: str,
    *,
    live_hash_enforced: bool,
    expected_hash: str | None = None,
) -> None:
    path = root / path_text
    require(path.exists(), f"Frozen file input missing: {path_text}")
    digest = sha256_file(path)
    if expected_hash is not None:
        require(digest == expected_hash, f"Frozen file input drift: {path_text}")
    existing = records.get(path_text)
    if existing is None:
        records[path_text] = {
            "path": path_text,
            "sha256": digest,
            "utf8_bytes": path.stat().st_size,
            "roles": [role],
            "live_hash_enforced": live_hash_enforced,
        }
        return
    require(existing["sha256"] == digest, f"Conflicting hash for {path_text}")
    if role not in existing["roles"]:
        existing["roles"].append(role)
        existing["roles"].sort()
    existing["live_hash_enforced"] = bool(
        existing["live_hash_enforced"] or live_hash_enforced
    )


def freeze(root: Path) -> dict[str, Any]:
    packet = verify_approval_packet(root)
    frozen_root = version_root(root)
    require(not frozen_root.exists(), f"Frozen version already exists: {frozen_root}")
    staging_root = frozen_root.parent / f".{VERSION_ID}.staging"
    require(not staging_root.exists(), f"Stale freeze staging directory: {staging_root}")

    preflight_root = root / PREFLIGHT_ROOT
    sources = read_jsonl(preflight_root / "source_inventory.jsonl")
    prompts = read_jsonl(preflight_root / "prompt_inventory.jsonl")
    require(len(sources) == 2433, "Source inventory must contain 2,433 rows")
    require(len(prompts) == 401, "Prompt inventory must contain 401 rows")

    skill_ids: set[str] = set()
    source_paths: set[str] = set()
    for row_index, row in enumerate(sources):
        require(row["source_row_index"] == row_index, "Source row indices are not contiguous")
        skill_id = row["skill_id"]
        require(skill_id not in skill_ids, f"Duplicate skill ID: {skill_id}")
        skill_ids.add(skill_id)
        source_path = root / row["source_path"]
        require(source_path.exists(), f"Source missing: {source_path}")
        require(sha256_file(source_path) == row["source_sha256"], f"Source drift: {skill_id}")
        text = source_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        require(frontmatter.get("name", "").strip() == row["source_name"], f"Name drift: {skill_id}")
        require(
            frontmatter.get("description", "").strip() == row["source_description"],
            f"Description drift: {skill_id}",
        )
        source_paths.add(row["source_path"])

    frozen_prompts = load_frozen_prompts(root, prompts)
    prompt_ids = [row["prompt_id"] for row in frozen_prompts]
    require(len(prompt_ids) == len(set(prompt_ids)), "Duplicate frozen prompt IDs")
    for row in frozen_prompts:
        require(row["gold_skill"] in skill_ids, f"Missing gold skill: {row['prompt_id']}")
        require(set(row["valid_skills"]).issubset(skill_ids), f"Invalid acceptable skill: {row['prompt_id']}")

    packet_files = {row["path"]: row for row in packet["files"]}
    file_records: dict[str, dict[str, Any]] = {}
    for path_text, packet_row in packet_files.items():
        add_file(
            file_records,
            root,
            path_text,
            "approved_protocol_context",
            live_hash_enforced=path_text in ENFORCED_PACKET_INPUTS,
            expected_hash=packet_row["sha256"],
        )
    for source_path in sorted(source_paths):
        add_file(
            file_records,
            root,
            source_path,
            "i2_source",
            live_hash_enforced=True,
        )
    for prompt_path in sorted({row["source_path"] for row in frozen_prompts}):
        add_file(
            file_records,
            root,
            prompt_path,
            "raw_prompt_source",
            live_hash_enforced=True,
        )

    staging_root.mkdir(parents=True, exist_ok=False)
    protocol_snapshot = staging_root / "protocol_snapshot.md"
    packet_snapshot = staging_root / "b0f_approval_packet.json"
    approval_receipt_path = staging_root / "b0f_approval_receipt.json"
    source_manifest_path = staging_root / "source_manifest.jsonl"
    prompt_manifest_path = staging_root / "prompt_manifest.jsonl"
    file_manifest_path = staging_root / "file_manifest.jsonl"

    write_bytes_new(protocol_snapshot, (root / PROTOCOL_RELATIVE_PATH).read_bytes())
    write_bytes_new(packet_snapshot, (root / APPROVAL_PACKET_RELATIVE_PATH).read_bytes())
    approval_receipt = {
        "schema_version": "rq2b-b0f-approval-receipt-v1",
        "state": "approved_scientific_protocol_freeze_only",
        "approved_by": "Jacky Zhang",
        "approved_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "approved_scope_sha256": APPROVED_SCOPE_SHA256,
        "approved_packet_sha256": APPROVED_PACKET_SHA256,
        "approved_protocol_sha256": APPROVED_PROTOCOL_SHA256,
        "authorises": packet["scope"]["authorises"],
        "does_not_authorise": packet["scope"]["does_not_authorise"],
    }
    write_json_new(approval_receipt_path, approval_receipt)
    write_jsonl_new(source_manifest_path, sources)
    write_jsonl_new(prompt_manifest_path, frozen_prompts)
    write_jsonl_new(
        file_manifest_path,
        (file_records[path] for path in sorted(file_records)),
    )

    generated_paths = {
        "protocol_snapshot": (protocol_snapshot, frozen_root / protocol_snapshot.name),
        "approval_packet_snapshot": (packet_snapshot, frozen_root / packet_snapshot.name),
        "approval_receipt": (approval_receipt_path, frozen_root / approval_receipt_path.name),
        "source_manifest": (source_manifest_path, frozen_root / source_manifest_path.name),
        "prompt_manifest": (prompt_manifest_path, frozen_root / prompt_manifest_path.name),
        "file_manifest": (file_manifest_path, frozen_root / file_manifest_path.name),
    }
    counts = defaultdict(int)
    for row in frozen_prompts:
        counts[row["stratum"]] += 1
    manifest = {
        "schema_version": "rq2b-frozen-corpus-manifest-v1",
        "version_id": VERSION_ID,
        "state": "frozen_protocol_no_scientific_results",
        "approved_scope_sha256": APPROVED_SCOPE_SHA256,
        "approved_packet_sha256": APPROVED_PACKET_SHA256,
        "approved_protocol_sha256": APPROVED_PROTOCOL_SHA256,
        "network_calls": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "counts": {
            "skills": len(sources),
            "prompts": len(frozen_prompts),
            "controlled_prompts": counts["controlled"],
            "public_gold_prompts": counts["public_gold"],
            "stress_prompts": counts["stress"],
            "file_manifest_rows": len(file_records),
        },
        "seeds": {
            "grouped_bootstrap": 2026080201,
            "grouped_sign_flip": 2026080202,
        },
        "primary_contract": {
            "rerank_k": 20,
            "noninferiority_margin": -0.03,
            "qwen_model": "text-embedding-v4",
            "qwen_dimensions": 1024,
            "qwen_chunk_tokens": 7500,
            "qwen_overlap_tokens": 256,
            "skillrouter_revision": "78986e1142d12857cfd85b8005e62902cd42d858",
            "skillrouter_max_pair_tokens": 2048,
            "skillrouter_overlap_tokens": 128,
        },
        "generated_artifacts": {
            name: {
                "path": relative(final_path, root),
                "sha256": sha256_file(staging_path),
                "utf8_bytes": staging_path.stat().st_size,
            }
            for name, (staging_path, final_path) in generated_paths.items()
        },
    }
    write_json_new(staging_root / "manifest.json", manifest)
    staging_root.replace(frozen_root)
    return verify_frozen_manifest(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--approved-scope-sha256", required=True)
    parser.add_argument("--approved-packet-sha256", required=True)
    args = parser.parse_args()
    require(
        args.approved_scope_sha256 == APPROVED_SCOPE_SHA256,
        "CLI scope hash does not match the approved scope",
    )
    require(
        args.approved_packet_sha256 == APPROVED_PACKET_SHA256,
        "CLI packet hash does not match the approved packet",
    )
    root = args.root.resolve()
    manifest = verify_frozen_manifest(root) if args.verify_only else freeze(root)
    print(
        json.dumps(
            {
                "version_id": manifest["version_id"],
                "state": manifest["state"],
                "counts": manifest["counts"],
                "network_calls": manifest["network_calls"],
                "root": relative(version_root(root), root),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
