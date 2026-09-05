#!/usr/bin/env python3
"""Reconcile the live public source frame for RQ2-native discovery.

The latest-chain ACTIVE layer is the frozen 29,292-source base plus every
standard source-frame amendment manifest.  Wave 024's clean 87-source
amendment is retained as a disjoint QUARANTINE layer because the latest
cumulative Wave 039 report excludes it.  The script then applies the existing
181-hash RQ1/prior-NC exclusion policy to ACTIVE only.

Outputs are navigation and provenance artifacts only.  This script does not
create clusters, prompts, labels, selector runs, or scientific results.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SOURCE_FRAME_ROOT = ROOT / "rq1b_v3_public_source_frame"
BASE_FRAME = SOURCE_FRAME_ROOT / "source_frame_2026-08-29/canonical_sources.jsonl"
BASE_CERTIFICATE = SOURCE_FRAME_ROOT / "source_frame_2026-08-29/SOURCE_FRAME_FREEZE_CERTIFICATE.json"
WAVE24_MANIFEST = (
    SOURCE_FRAME_ROOT
    / "d1_source_intake_wave_024_2026-08-30/source_frame_amendment_clean/canonical_sources_amendment.jsonl"
)
WAVE24_REPORT = WAVE24_MANIFEST.with_name("source_frame_amendment_report.json")

RQ1_WAVE_001 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_001_frozen_manifest.jsonl"
RQ1_WAVE_002 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_002_frozen_manifest.jsonl"
COMPLETE_C6_LEADS = ROOT / "rq2b_naturalistic_confusability/candidates/rq1_complete_c6_cluster_leads_2026-08-31.jsonl"
INITIAL_NC_AUTHORS = ROOT / "rq2b_naturalistic_confusability/prompts/initial_authoring_drafts_private_2026-08-31.jsonl"

OLD_BASE_ONLY_DIR = (
    ROOT
    / "rq2b_naturalistic_confusability/manifests/rq2b_native_discovery_universe_2026-08-31"
)
OUTPUT_DIR = (
    ROOT
    / "rq2b_naturalistic_confusability/manifests/rq2b_native_discovery_universe_live_reconciled_2026-08-31"
)

EXPECTED_BASE_COUNT = 29_292
EXPECTED_ACTIVE_COUNT = 31_378
EXPECTED_WAVE24_QUARANTINE_COUNT = 87
EXPECTED_RAW_UNION_COUNT = 31_465
EXPECTED_PRIOR_EXCLUSION_COUNT = 181
EXPECTED_FROZEN_RQ1_CLUSTER_HASH_COUNT = 163
WAVE_PATTERN = re.compile(r"d1_source_intake_wave_(\d{3})_")


def sha256_and_size(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def sha256_file(path: Path) -> str:
    return sha256_and_size(path)[0]


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise SystemExit(f"Expected JSON object at {path}:{line_number}")
        rows.append(value)
    return rows


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def relative_to_root(path: Path) -> str:
    return str(path.relative_to(ROOT))


def resolve_local_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == ROOT.name:
        return (REPO_ROOT / path).resolve()
    return (ROOT / path).resolve()


def wave_number(path: Path) -> int:
    match = WAVE_PATTERN.search(str(path))
    if not match:
        raise SystemExit(f"Cannot derive source-intake wave from path: {path}")
    return int(match.group(1))


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


def normalise_base_row(row: dict[str, Any]) -> dict[str, Any]:
    canonical = dict(row["canonical"])
    source_hash = str(row["sha256"])
    if str(canonical["sha256"]) != source_hash:
        raise SystemExit(f"Base row contains conflicting hashes: {row.get('source_id')}")
    return {
        "source_id": str(row["source_id"]),
        "source_sha256": source_hash,
        "source_bytes": int(row["byte_count"]),
        "source_root": str(canonical["source_root"]),
        "origin_key": str(canonical["origin_key"]),
        "source_path": str(resolve_local_path(str(canonical["absolute_path"]))),
        "source_frame_layer": "LATEST_CHAIN_ACTIVE_BASE",
        "source_wave": None,
        "source_manifest_path": relative_to_root(BASE_FRAME),
        "source_record_status": str(row["source_status"]),
        "repository_ref": None,
        "artifact_path": str(canonical["relative_path"]),
    }


def normalise_amendment_row(
    row: dict[str, Any], manifest_path: Path, disposition: str
) -> dict[str, Any]:
    canonical = dict(row["canonical"])
    wave = wave_number(manifest_path)
    return {
        "source_id": str(row["amendment_source_id"]),
        "source_sha256": str(canonical["source_sha256"]),
        "source_bytes": int(row["byte_count"]),
        "source_root": "source_frame_amendment",
        "origin_key": str(canonical["repository_ref"]),
        "source_path": str(resolve_local_path(str(canonical["local_raw_path"]))),
        "source_frame_layer": disposition,
        "source_wave": wave,
        "source_manifest_path": relative_to_root(manifest_path),
        "source_record_status": str(row["source_status"]),
        "repository_ref": str(canonical["repository_ref"]),
        "artifact_path": str(canonical["artifact_path"]),
    }


def validate_amendment_manifest(manifest_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report_path = manifest_path.with_name("source_frame_amendment_report.json")
    if not report_path.is_file():
        raise SystemExit(f"Missing amendment report: {report_path}")
    rows = read_jsonl(manifest_path)
    report = read_json(report_path)
    if int(report["failure_count"]) != 0:
        raise SystemExit(f"Amendment report is not fail-closed: {report_path}")
    if int(report["accepted_amendment_source_count"]) != len(rows):
        raise SystemExit(f"Amendment report/manifest count mismatch: {manifest_path}")
    if int(report["input_novel_manifest_record_count"]) != len(rows):
        raise SystemExit(f"Amendment input/manifest count mismatch: {manifest_path}")
    return rows, report


def verify_local_sources(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        source_path = Path(str(row["source_path"]))
        if not source_path.is_file():
            raise SystemExit(f"Missing local source: {source_path}")
        actual_hash, actual_bytes = sha256_and_size(source_path)
        if actual_hash != row["source_sha256"]:
            raise SystemExit(f"Local source hash mismatch: {source_path}")
        if actual_bytes != row["source_bytes"]:
            raise SystemExit(f"Local source byte-count mismatch: {source_path}")
        row["local_bytes_verified"] = True


def assert_hash_unique(rows: list[dict[str, Any]], label: str) -> None:
    counts = Counter(str(row["source_sha256"]) for row in rows)
    duplicates = sorted(source_hash for source_hash, count in counts.items() if count > 1)
    if duplicates:
        raise SystemExit(f"{label} is not source-hash unique; first duplicates: {duplicates[:5]}")


def build_prior_exclusions() -> dict[str, set[str]]:
    exclusions: dict[str, set[str]] = {}

    def add(source_hash: str, reason: str) -> None:
        exclusions.setdefault(source_hash, set()).add(reason)

    for manifest_path in (RQ1_WAVE_001, RQ1_WAVE_002):
        for cluster in read_jsonl(manifest_path):
            for source_hash in dict(cluster["source_hashes"]).values():
                add(str(source_hash), "MEMBER_OF_79_FROZEN_RQ1_CLUSTERS")

    for lead in read_jsonl(COMPLETE_C6_LEADS):
        for source_hash in lead["candidate_source_sha256"]:
            add(str(source_hash), "MEMBER_OF_PRIOR_RQ1_COMPLETE_C6_LEAD")

    for author in read_jsonl(INITIAL_NC_AUTHORS):
        add(
            str(author["author_intended_candidate_source_sha256"]),
            "MEMBER_OF_INITIAL_NC_REVIEW_LEAD",
        )
    return exclusions


def main() -> int:
    exclusion_inputs = [RQ1_WAVE_001, RQ1_WAVE_002, COMPLETE_C6_LEADS, INITIAL_NC_AUTHORS]
    required = [BASE_FRAME, BASE_CERTIFICATE, WAVE24_MANIFEST, WAVE24_REPORT, *exclusion_inputs]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    certificate = read_json(BASE_CERTIFICATE)
    if certificate["artifact_hashes"][BASE_FRAME.name] != sha256_file(BASE_FRAME):
        raise SystemExit("Frozen base source-frame hash does not match its certificate")
    base_rows = [normalise_base_row(row) for row in read_jsonl(BASE_FRAME)]
    if len(base_rows) != EXPECTED_BASE_COUNT:
        raise SystemExit(f"Expected {EXPECTED_BASE_COUNT:,} base rows, found {len(base_rows):,}")

    active_manifest_paths = sorted(
        SOURCE_FRAME_ROOT.glob(
            "d1_source_intake_wave_*/source_frame_amendment/canonical_sources_amendment.jsonl"
        ),
        key=wave_number,
    )
    if not active_manifest_paths:
        raise SystemExit("No standard source-frame amendments found")
    if any(wave_number(path) == 24 for path in active_manifest_paths):
        raise SystemExit("Wave 024 unexpectedly appears in the standard ACTIVE amendment chain")

    active_rows = list(base_rows)
    active_reports: list[tuple[Path, dict[str, Any]]] = []
    for manifest_path in active_manifest_paths:
        rows, report = validate_amendment_manifest(manifest_path)
        active_rows.extend(
            normalise_amendment_row(row, manifest_path, "LATEST_CHAIN_ACTIVE_AMENDMENT")
            for row in rows
        )
        active_reports.append((manifest_path.with_name("source_frame_amendment_report.json"), report))

    wave24_rows_raw, wave24_report = validate_amendment_manifest(WAVE24_MANIFEST)
    quarantine_rows = [
        normalise_amendment_row(row, WAVE24_MANIFEST, "WAVE24_QUARANTINE")
        for row in wave24_rows_raw
    ]

    assert_hash_unique(active_rows, "Latest-chain ACTIVE frame")
    assert_hash_unique(quarantine_rows, "Wave24 QUARANTINE frame")
    active_hashes = {str(row["source_sha256"]) for row in active_rows}
    quarantine_hashes = {str(row["source_sha256"]) for row in quarantine_rows}
    overlap = active_hashes & quarantine_hashes
    if overlap:
        raise SystemExit(f"ACTIVE/QUARANTINE hash overlap; first hashes: {sorted(overlap)[:5]}")

    raw_union_count = len(active_hashes | quarantine_hashes)
    if len(active_rows) != EXPECTED_ACTIVE_COUNT:
        raise SystemExit(f"Expected {EXPECTED_ACTIVE_COUNT:,} ACTIVE rows, found {len(active_rows):,}")
    if len(quarantine_rows) != EXPECTED_WAVE24_QUARANTINE_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_WAVE24_QUARANTINE_COUNT} Wave24 rows, found {len(quarantine_rows)}"
        )
    if raw_union_count != EXPECTED_RAW_UNION_COUNT:
        raise SystemExit(f"Expected {EXPECTED_RAW_UNION_COUNT:,} raw-union hashes, found {raw_union_count:,}")

    latest_report_path, latest_report = active_reports[-1]
    latest_report_output_count = (
        int(latest_report["frozen_source_frame_record_count"])
        + int(latest_report["accepted_amendment_source_count"])
    )
    if latest_report_output_count != len(active_rows):
        raise SystemExit(
            f"Latest amendment report implies {latest_report_output_count:,}, "
            f"but derived ACTIVE has {len(active_rows):,}"
        )

    # Rehash every source in both partitions before applying RQ2 exclusions.
    verify_local_sources(active_rows)
    verify_local_sources(quarantine_rows)

    exclusions = build_prior_exclusions()
    if len(exclusions) != EXPECTED_PRIOR_EXCLUSION_COUNT:
        raise SystemExit(f"Expected 181 prior-source exclusions, found {len(exclusions)}")
    frozen_rq1_hash_count = sum(
        "MEMBER_OF_79_FROZEN_RQ1_CLUSTERS" in reasons for reasons in exclusions.values()
    )
    if frozen_rq1_hash_count != EXPECTED_FROZEN_RQ1_CLUSTER_HASH_COUNT:
        raise SystemExit(f"Expected 163 frozen-RQ1 hashes, found {frozen_rq1_hash_count}")

    active_by_hash = {str(row["source_sha256"]): row for row in active_rows}
    excluded_in_active = set(exclusions) & active_hashes
    absent_from_active = set(exclusions) - active_hashes

    navigation_rows: list[dict[str, Any]] = []
    excluded_rows: list[dict[str, Any]] = []
    root_counts: Counter[str] = Counter()
    metadata_counts: Counter[str] = Counter()
    for row in active_rows:
        source_hash = str(row["source_sha256"])
        if source_hash in excluded_in_active:
            excluded_rows.append(
                {
                    **row,
                    "exclusion_reasons": sorted(exclusions[source_hash]),
                    "status": "EXCLUDED_FROM_RQ2_NATIVE_DISCOVERY_ONLY",
                }
            )
            continue
        source_path = Path(str(row["source_path"]))
        name, description, headings = extract_navigation_metadata(source_path)
        root_counts[str(row["source_root"])] += 1
        metadata_counts["with_name"] += bool(name)
        metadata_counts["with_description"] += bool(description)
        navigation_rows.append(
            {
                **row,
                "source_name": name,
                "source_description": description,
                "heading_preview": headings,
                "status": "RQ2_NATIVE_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_LABEL",
            }
        )

    absent_rows = [
        {
            "source_sha256": source_hash,
            "exclusion_reasons": sorted(exclusions[source_hash]),
            "status": "PRIOR_SOURCE_EXCLUSION_HASH_ABSENT_FROM_LATEST_CHAIN_ACTIVE",
        }
        for source_hash in sorted(absent_from_active)
    ]

    if len(navigation_rows) + len(excluded_rows) != len(active_rows):
        raise SystemExit("RQ2 navigation/exclusion partition does not cover ACTIVE")

    active_rows.sort(key=lambda row: str(row["source_sha256"]))
    quarantine_rows.sort(key=lambda row: str(row["source_sha256"]))
    navigation_rows.sort(key=lambda row: str(row["source_sha256"]))
    excluded_rows.sort(key=lambda row: str(row["source_sha256"]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    active_path = OUTPUT_DIR / "latest_chain_active_sources.jsonl"
    quarantine_path = OUTPUT_DIR / "wave24_quarantine_sources.jsonl"
    navigation_path = OUTPUT_DIR / "rq2_native_source_navigation.jsonl"
    excluded_path = OUTPUT_DIR / "excluded_prior_cluster_sources.jsonl"
    absent_path = OUTPUT_DIR / "prior_source_exclusions_absent_from_active.jsonl"
    write_jsonl(active_path, active_rows)
    write_jsonl(quarantine_path, quarantine_rows)
    write_jsonl(navigation_path, navigation_rows)
    write_jsonl(excluded_path, excluded_rows)
    write_jsonl(absent_path, absent_rows)

    old_summary_path = OLD_BASE_ONLY_DIR / "summary.json"
    old_navigation_path = OLD_BASE_ONLY_DIR / "rq2_native_source_navigation.jsonl"
    old_excluded_path = OLD_BASE_ONLY_DIR / "excluded_prior_cluster_sources.jsonl"
    old_required = [old_summary_path, old_navigation_path, old_excluded_path]
    old_missing = [str(path) for path in old_required if not path.is_file()]
    if old_missing:
        raise SystemExit(f"Missing preserved base-only audit artifact(s): {old_missing}")
    old_summary = read_json(old_summary_path)
    if int(old_summary["rq2_native_discovery_source_count"]) != 29_120:
        raise SystemExit("The preserved base-only audit no longer reports 29,120 sources")

    supersession_notice_path = OLD_BASE_ONLY_DIR / "SUPERSESSION_NOTICE.json"
    supersession_notice = {
        "status": "SUPERSEDED_BASE_ONLY_AUDIT_PRESERVED_NOT_CURRENT_LIVE_UNIVERSE",
        "historical_scope": "29,292 frozen base only, before subsequent source-frame amendments",
        "historical_rq2_native_discovery_source_count": 29_120,
        "historical_artifacts_unchanged": {
            relative_to_root(path): sha256_file(path) for path in old_required
        },
        "successor_summary": relative_to_root(OUTPUT_DIR / "summary.json"),
        "reason": (
            "The current RQ2 discovery universe must use the reconciled latest-chain ACTIVE frame; "
            "the original files remain an auditable base-only snapshot."
        ),
    }
    write_json(supersession_notice_path, supersession_notice)

    input_paths = [BASE_FRAME, BASE_CERTIFICATE, WAVE24_MANIFEST, WAVE24_REPORT, *exclusion_inputs]
    for manifest_path in active_manifest_paths:
        input_paths.extend([manifest_path, manifest_path.with_name("source_frame_amendment_report.json")])

    artifact_paths = [
        active_path,
        quarantine_path,
        navigation_path,
        excluded_path,
        absent_path,
        supersession_notice_path,
    ]
    summary = {
        "status": "PASS_RQ2_LIVE_PUBLIC_UNIVERSE_RECONCILIATION_NOT_A_CLUSTER_OR_RESULT",
        "source_frame_reconciliation": {
            "frozen_base_source_count": len(base_rows),
            "standard_active_amendment_manifest_count": len(active_manifest_paths),
            "standard_active_amendment_source_count": len(active_rows) - len(base_rows),
            "latest_chain_active_source_count": len(active_rows),
            "wave24_quarantine_source_count": len(quarantine_rows),
            "active_quarantine_hash_overlap_count": len(overlap),
            "raw_union_source_count": raw_union_count,
            "all_source_files_rehashed": len(active_rows) + len(quarantine_rows),
            "active_amendment_waves": [wave_number(path) for path in active_manifest_paths],
            "latest_cumulative_report": {
                "path": relative_to_root(latest_report_path),
                "reported_prior_count": int(latest_report["frozen_source_frame_record_count"]),
                "reported_addition_count": int(latest_report["accepted_amendment_source_count"]),
                "implied_output_count": latest_report_output_count,
            },
            "wave24_reported_addition_count": int(wave24_report["accepted_amendment_source_count"]),
        },
        "prior_source_exclusions": {
            "frozen_rq1_cluster_source_hash_count": frozen_rq1_hash_count,
            "all_prior_lead_exclusion_hash_count": len(exclusions),
            "prior_lead_exclusion_hashes_present_in_active": len(excluded_in_active),
            "prior_lead_exclusion_hashes_absent_from_active": len(absent_from_active),
        },
        "rq2_native_discovery": {
            "source_count": len(navigation_rows),
            "source_root_counts": dict(sorted(root_counts.items())),
            "metadata_counts": dict(sorted(metadata_counts.items())),
            "scope": "LATEST_CHAIN_ACTIVE_MINUS_PRIOR_SOURCE_EXCLUSIONS",
        },
        "supersedes": {
            "base_only_summary": relative_to_root(old_summary_path),
            "base_only_rq2_native_count": 29_120,
            "preservation": "Historical artifacts retained unchanged; supersession notice added.",
        },
        "input_sha256": {
            relative_to_root(path): sha256_file(path) for path in sorted(set(input_paths))
        },
        "artifacts": {
            relative_to_root(path): sha256_file(path) for path in artifact_paths
        },
        "claim_boundary": [
            "ACTIVE is the hash-unique union of the frozen base and all standard source_frame_amendment manifests.",
            "Wave24's 87 hash-unique sources are retained but quarantined because the latest cumulative amendment report excludes them.",
            "RQ2-native navigation is ACTIVE minus the existing 181-hash prior-source exclusion policy.",
            "Every ACTIVE and QUARANTINE local source file was rehashed and byte-count checked.",
            "Navigation metadata is not a cluster, prompt, label, selector score, retrieval result, or scientific result.",
        ],
    }
    summary_path = OUTPUT_DIR / "summary.json"
    write_json(summary_path, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
