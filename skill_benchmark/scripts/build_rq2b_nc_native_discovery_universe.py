#!/usr/bin/env python3
"""Build an RQ2-native public-source discovery universe.

The output excludes every source hash already used by the 79 frozen RQ1
clusters and every additional source used by the first NC lead/review wave.
It is navigation metadata only: no cluster, prompt, label, model score, or
retrieval result is produced.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FRAME = ROOT / "rq1b_v3_public_source_frame/source_frame_2026-08-29/canonical_sources.jsonl"
SOURCE_FRAME_CERTIFICATE = ROOT / "rq1b_v3_public_source_frame/source_frame_2026-08-29/SOURCE_FRAME_FREEZE_CERTIFICATE.json"
RQ1_WAVE_001 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_001_frozen_manifest.jsonl"
RQ1_WAVE_002 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_002_frozen_manifest.jsonl"
COMPLETE_C6_LEADS = ROOT / "rq2b_naturalistic_confusability/candidates/rq1_complete_c6_cluster_leads_2026-08-31.jsonl"
INITIAL_NC_AUTHORS = ROOT / "rq2b_naturalistic_confusability/prompts/initial_authoring_drafts_private_2026-08-31.jsonl"
OUTPUT_DIR = ROOT / "rq2b_naturalistic_confusability/manifests/rq2b_native_discovery_universe_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return " ".join(value.replace("\\n", " ").split())


def frontmatter_value(lines: list[str], key: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(key)}\s*:\s*(.*)$", re.IGNORECASE)
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        value = match.group(1).strip()
        if value not in {"", ">", "|", ">-", "|-"}:
            return strip_scalar(value)
        continuation: list[str] = []
        for later in lines[index + 1 :]:
            if not later.startswith((" ", "\t")):
                break
            continuation.append(later.strip())
        return " ".join(part for part in continuation if part) or None
    return None


def extract_navigation_metadata(path: Path) -> tuple[str | None, str | None, list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    frontmatter: list[str] = []
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            frontmatter.append(line)
    name = frontmatter_value(frontmatter, "name")
    description = frontmatter_value(frontmatter, "description")
    headings = [
        re.sub(r"^#+\s*", "", line).strip()
        for line in lines
        if re.match(r"^#{1,3}\s+\S", line)
    ][:12]
    if not name and headings:
        name = headings[0]
    return name, description, headings


def main() -> int:
    required = [
        SOURCE_FRAME,
        SOURCE_FRAME_CERTIFICATE,
        RQ1_WAVE_001,
        RQ1_WAVE_002,
        COMPLETE_C6_LEADS,
        INITIAL_NC_AUTHORS,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    frame_rows = read_jsonl(SOURCE_FRAME)
    if len(frame_rows) != 29292:
        raise SystemExit(f"Expected 29,292 frozen source-frame rows, found {len(frame_rows)}")
    frame_hashes = [str(row["sha256"]) for row in frame_rows]
    if len(set(frame_hashes)) != len(frame_hashes):
        raise SystemExit("Frozen source frame is not source-hash unique")

    exclusions: dict[str, set[str]] = {}

    def add_exclusion(source_hash: str, reason: str) -> None:
        exclusions.setdefault(source_hash, set()).add(reason)

    for manifest_path in (RQ1_WAVE_001, RQ1_WAVE_002):
        for cluster in read_jsonl(manifest_path):
            for source_hash in dict(cluster["source_hashes"]).values():
                add_exclusion(str(source_hash), "MEMBER_OF_79_FROZEN_RQ1_CLUSTERS")

    for lead in read_jsonl(COMPLETE_C6_LEADS):
        for source_hash in lead["candidate_source_sha256"]:
            add_exclusion(str(source_hash), "MEMBER_OF_PRIOR_RQ1_COMPLETE_C6_LEAD")

    for author in read_jsonl(INITIAL_NC_AUTHORS):
        add_exclusion(
            str(author["author_intended_candidate_source_sha256"]),
            "MEMBER_OF_INITIAL_NC_REVIEW_LEAD",
        )

    frame_hash_set = set(frame_hashes)
    excluded_in_frame = set(exclusions) & frame_hash_set
    missing_exclusion_hashes = set(exclusions) - frame_hash_set

    navigation_rows: list[dict[str, Any]] = []
    excluded_rows: list[dict[str, Any]] = []
    root_counts: Counter[str] = Counter()
    metadata_counts: Counter[str] = Counter()
    for frame_row in frame_rows:
        source_hash = str(frame_row["sha256"])
        canonical = dict(frame_row["canonical"])
        source_path = Path(str(canonical["absolute_path"]))
        if source_hash in excluded_in_frame:
            excluded_rows.append(
                {
                    "source_id": frame_row["source_id"],
                    "source_sha256": source_hash,
                    "exclusion_reasons": sorted(exclusions[source_hash]),
                    "source_root": canonical["source_root"],
                    "source_path": str(source_path),
                    "status": "EXCLUDED_FROM_RQ2_NATIVE_DISCOVERY_ONLY",
                }
            )
            continue
        if not source_path.is_file():
            raise SystemExit(f"Missing frozen local source: {source_path}")
        if sha256_file(source_path) != source_hash:
            raise SystemExit(f"Frozen local source hash mismatch: {source_path}")
        name, description, headings = extract_navigation_metadata(source_path)
        root_counts[str(canonical["source_root"])] += 1
        metadata_counts["with_name"] += bool(name)
        metadata_counts["with_description"] += bool(description)
        navigation_rows.append(
            {
                "source_id": frame_row["source_id"],
                "source_sha256": source_hash,
                "source_bytes": int(frame_row["byte_count"]),
                "source_root": canonical["source_root"],
                "origin_key": canonical["origin_key"],
                "source_path": str(source_path),
                "source_name": name,
                "source_description": description,
                "heading_preview": headings,
                "status": "RQ2_NATIVE_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_LABEL",
            }
        )

    if len(navigation_rows) + len(excluded_rows) != len(frame_rows):
        raise SystemExit("Discovery/exclusion partition does not cover the frozen frame")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    navigation_path = OUTPUT_DIR / "rq2_native_source_navigation.jsonl"
    excluded_path = OUTPUT_DIR / "excluded_prior_cluster_sources.jsonl"
    write_jsonl(navigation_path, navigation_rows)
    write_jsonl(excluded_path, sorted(excluded_rows, key=lambda row: row["source_sha256"]))

    summary = {
        "status": "PASS_RQ2_NATIVE_NAVIGATION_UNIVERSE_NOT_A_CLUSTER_OR_RESULT",
        "frozen_source_frame_count": len(frame_rows),
        "frozen_rq1_cluster_source_hash_count": sum(
            "MEMBER_OF_79_FROZEN_RQ1_CLUSTERS" in reasons for reasons in exclusions.values()
        ),
        "all_prior_lead_exclusion_hash_count": len(exclusions),
        "prior_lead_exclusion_hashes_present_in_frame": len(excluded_in_frame),
        "prior_lead_exclusion_hashes_absent_from_frame": len(missing_exclusion_hashes),
        "rq2_native_discovery_source_count": len(navigation_rows),
        "source_root_counts": dict(sorted(root_counts.items())),
        "metadata_counts": dict(sorted(metadata_counts.items())),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {
            navigation_path.name: sha256_file(navigation_path),
            excluded_path.name: sha256_file(excluded_path),
        },
        "claim_boundary": [
            "Every member of the 79 frozen RQ1 clusters is excluded by exact source hash.",
            "Additional prior RQ1/NC lead sources are excluded so new discovery cannot silently recycle the first wave.",
            "Frontmatter and headings are navigation metadata only; semantic-confusability requires full-source reading and independent review.",
            "No RQ1 prompt, label, acceptable set, selector score, or cluster decision is transferred.",
        ],
    }
    summary_path = OUTPUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
