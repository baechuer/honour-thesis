#!/usr/bin/env python3
"""Build the private, hash-verified P0 roster for RQ1b masked execution.

This is local lineage reconstruction only. It creates no blind agent packet,
mask, embedding, retrieval score, API request, metric, or scientific result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_cross_source_public_benchmark")
ROUND_RE = re.compile(r"round(\d+)")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

# This is an explicit lineage lock, not a filename-recency heuristic. The paths
# were independently audited against every C6 row before this builder was added.
C2_BY_ROUND = {
    "02": "manifest/c2_prompt_drafts_round02_2026-08-26.jsonl",
    "13": "manifest/c2_prompt_drafts_round13_2026-08-26.jsonl",
    "15": "manifest/c2_prompt_drafts_round15_v2_2026-08-26.jsonl",
    "16": "manifest/c2_prompt_drafts_round16_2026-08-27.jsonl",
    "17": "manifest/c2_prompt_drafts_round17_v2_2026-08-27.jsonl",
    "18": "manifest/c2_prompt_drafts_round18_2026-08-27.jsonl",
    "19": "manifest/c2_prompt_drafts_round19_v2_2026-08-27.jsonl",
    "20": "manifest/c2_round20_drafts_v2_validated_2026-08-27.jsonl",
    "21": "manifest/c2_round21_drafts_2026-08-27.jsonl",
    "22": "manifest/c2_round22_drafts_2026-08-27.jsonl",
    "25": "manifest/c2_round25_drafts_v2_2026-08-27.jsonl",
    "26": "manifest/c2_round26_drafts_v2_2026-08-27.jsonl",
    "27": "working/c2_round27_validated_prompt_drafts_v2_2026-08-28.jsonl",
    "28": "working/c2_round28_validated_prompt_drafts_2026-08-28.jsonl",
    "29": "working/c2_round29_final_prompt_drafts_after_c3_literal_rewrite_2026-08-28.jsonl",
    "30": "working/c2_round30_final_prompt_drafts_after_c3_literal_rewrite_2026-08-28.jsonl",
    "31": "working/c2_round31_final_prompt_drafts_after_c3_final_rewrites_2026-08-28.jsonl",
    "32": "working/c2_round32_final_prompt_drafts_after_c3_manual_rewrite_2026-08-28.jsonl",
    "34": "working/c2_round34_validated_prompt_drafts_v3_2026-08-28.jsonl",
    "35": "working/c2_round35_merged_drafts_c3_final_2026-08-28.jsonl",
    "36": "manifest/c2_round36_drafts_2026-08-28.jsonl",
    "38": "manifest/c2_round38_drafts_literal_repaired_2026-08-28.jsonl",
    "39": "manifest/c2_round39_drafts_2026-08-28.jsonl",
    "40": "manifest/c2_round40_drafts_final_c3_c4_candidate_2026-08-28.jsonl",
    "41": "manifest/c2_round41_drafts_after_c3_semantic_rewrite_v2_validated_2026-08-28.jsonl",
    "42": "manifest/c2_round42_drafts_after_c3_final_rewrite_2026-08-28.jsonl",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[tuple[int, dict]]:
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"non-object JSONL row: {path}:{line_number}")
            rows.append((line_number, value))
    return rows


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_under_root(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"source path escapes benchmark root: {path}") from error
    return resolved


def discover_source_occurrences() -> dict[tuple[str, str], list[dict]]:
    index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for manifest_path in sorted(ROOT.rglob("*.jsonl")):
        # The benchmark also retains some non-JSONL audit artifacts with a
        # .jsonl suffix. Only a file that declares the C0B path field enters
        # the strict source-manifest parser below.
        if '"packet_original_path"' not in manifest_path.read_text():
            continue
        for line_number, row in read_jsonl(manifest_path):
            required = {"skill_id", "source_sha256", "packet_original_path"}
            if not required.issubset(row):
                continue
            skill_id = row["skill_id"]
            source_sha = row["source_sha256"].lower()
            if not isinstance(skill_id, str) or not isinstance(row["source_sha256"], str) or not SHA_RE.fullmatch(source_sha):
                raise ValueError(f"malformed C0B identity: {manifest_path}:{line_number}")
            packet = require_under_root(Path(row["packet_original_path"]))
            if not packet.is_file() or packet.name != "SKILL.original.md" or packet.parent.name != skill_id:
                raise ValueError(f"invalid C0B source packet: {manifest_path}:{line_number}")
            actual_sha = sha256(packet)
            if actual_sha != source_sha:
                raise ValueError(f"C0B source hash mismatch: {manifest_path}:{line_number}")
            index[(skill_id, source_sha)].append(
                {
                    "source_manifest": relative(manifest_path),
                    "source_manifest_line": line_number,
                    "packet_original_path": str(packet),
                    "packet_realpath": str(packet.resolve()),
                    "source_sha256": source_sha,
                }
            )
    if not index:
        raise ValueError("no C0B source occurrences discovered")
    return index


def source_lineage(index: dict[tuple[str, str], list[dict]], skill_id: str, source_sha: str) -> dict:
    key = (skill_id, source_sha.lower())
    candidates = index.get(key, [])
    if not candidates:
        raise ValueError(f"no C0B source occurrence for {key}")
    deduplicated = {}
    for candidate in candidates:
        deduplicated[candidate["packet_realpath"]] = candidate
    matches = sorted(
        deduplicated.values(),
        key=lambda item: (item["source_manifest"], item["source_manifest_line"], item["packet_realpath"]),
    )
    canonical = matches[0]
    return {
        "skill_id": skill_id,
        "source_sha256": source_sha,
        "canonical_source": canonical,
        "lineage_matches": matches,
    }


def c2_index_for_round(round_id: str) -> tuple[dict[tuple[str, str, str], dict], dict]:
    rel = C2_BY_ROUND.get(round_id)
    if rel is None:
        raise ValueError(f"no explicit C2 lineage lock for C6 round {round_id}")
    path = ROOT / rel
    if not path.is_file():
        raise ValueError(f"locked C2 file missing: {rel}")
    index = {}
    for line_number, row in read_jsonl(path):
        required = {"proposal_id", "intended_candidate_skill_id", "variant", "prompt"}
        if not required.issubset(row):
            continue
        key = (row["proposal_id"], row["intended_candidate_skill_id"], row["variant"])
        if key in index:
            raise ValueError(f"duplicate C2 key in locked file {rel}: {key}")
        if not isinstance(row["prompt"], str) or not row["prompt"].strip():
            raise ValueError(f"empty C2 prompt in locked file {rel}:{line_number}")
        index[key] = {"line_number": line_number, "prompt": row["prompt"]}
    return index, {"round": round_id, "path": rel, "sha256": sha256(path), "row_count": len(index)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "working/masked_execution/p0_master_roster_2026-08-28.json",
    )
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite P0 roster: {args.output}")

    source_index = discover_source_occurrences()
    c6_paths = sorted((ROOT / "manifest").glob("c6*.jsonl"))
    if not c6_paths:
        raise ValueError("no C6 manifest files found")

    c2_indexes = {}
    c2_locks = {}
    rows = []
    seen_c6_keys = set()
    seen_rounds = set()
    for c6_path in c6_paths:
        match = ROUND_RE.search(c6_path.name)
        if not match:
            raise ValueError(f"cannot determine C6 round from file name: {c6_path.name}")
        round_id = match.group(1).zfill(2)
        if round_id in seen_rounds:
            raise ValueError(f"more than one C6 file for round {round_id}")
        seen_rounds.add(round_id)
        c2_indexes[round_id], c2_locks[round_id] = c2_index_for_round(round_id)
        c6_sha = sha256(c6_path)
        for line_number, row in read_jsonl(c6_path):
            if not str(row.get("c6_status", "")).startswith("C6_FROZEN_PRIMARY"):
                continue
            required = {"proposal_id", "strict_gold_skill_id", "prompt_variant", "candidate_skill_ids", "candidate_source_sha256"}
            if not required.issubset(row):
                raise ValueError(f"incomplete C6 row: {c6_path}:{line_number}")
            candidate_ids = row["candidate_skill_ids"]
            candidate_hashes = row["candidate_source_sha256"]
            if not isinstance(candidate_ids, list) or not isinstance(candidate_hashes, list) or len(candidate_ids) != len(candidate_hashes):
                raise ValueError(f"C6 candidate arrays mismatch: {c6_path}:{line_number}")
            pairs = []
            for skill_id, source_sha in zip(candidate_ids, candidate_hashes):
                if not isinstance(skill_id, str) or not isinstance(source_sha, str) or not SHA_RE.fullmatch(source_sha.lower()):
                    raise ValueError(f"malformed C6 candidate identity: {c6_path}:{line_number}")
                pairs.append((skill_id, source_sha.lower()))
            if len(set(pairs)) != len(pairs):
                raise ValueError(f"duplicate candidate in C6 row: {c6_path}:{line_number}")
            strict_gold = row["strict_gold_skill_id"]
            if strict_gold not in candidate_ids:
                raise ValueError(f"strict gold outside candidate set: {c6_path}:{line_number}")
            c6_key = (row["proposal_id"], strict_gold, row["prompt_variant"])
            if c6_key in seen_c6_keys:
                raise ValueError(f"duplicate C6 family/variant key: {c6_key}")
            seen_c6_keys.add(c6_key)
            c2 = c2_indexes[round_id].get(c6_key)
            if c2 is None:
                raise ValueError(f"missing locked C2 prompt for C6 key: {c6_key}")
            candidates = [source_lineage(source_index, skill_id, source_sha) for skill_id, source_sha in pairs]
            composition_key = tuple(sorted(f"{skill_id}:{source_sha}" for skill_id, source_sha in pairs))
            rows.append(
                {
                    "round": round_id,
                    "c6_manifest": relative(c6_path),
                    "c6_manifest_sha256": c6_sha,
                    "c6_manifest_line": line_number,
                    "proposal_id": row["proposal_id"],
                    "strict_gold_skill_id": strict_gold,
                    "prompt_variant": row["prompt_variant"],
                    "prompt": c2["prompt"],
                    "c2_lineage": {**c2_locks[round_id], "line_number": c2["line_number"]},
                    "candidate_composition_key": list(composition_key),
                    "candidates": candidates,
                }
            )

    compositions = {tuple(row["candidate_composition_key"]) for row in rows}
    families = {(tuple(row["candidate_composition_key"]), row["strict_gold_skill_id"]) for row in rows}
    expected = {"rows": 408, "families": 209, "compositions": 76}
    actual = {"rows": len(rows), "families": len(families), "compositions": len(compositions)}
    if actual != expected:
        raise ValueError(f"P0 cardinality mismatch: expected {expected}, got {actual}")

    output = {
        "status": "P0_MASTER_ROSTER_PRECHECK_PASS_NOT_A_RESULT",
        "scope": "local source/hash and C6-to-C2 lineage reconstruction only",
        "counts": actual,
        "c2_lineage_lock": [c2_locks[round_id] for round_id in sorted(c2_locks)],
        "source_resolution_rule": {
            "logical_candidate_key": ["skill_id", "source_sha256"],
            "canonical_physical_copy": "first sorted verified occurrence by source_manifest, source_manifest_line, packet_realpath",
            "all_equivalent_verified_occurrences_retained": True,
        },
        "rows": sorted(rows, key=lambda row: (row["round"], row["c6_manifest"], row["c6_manifest_line"])),
        "exclusions": [
            "No blind P0.5 packet was created.",
            "No source text was masked or altered.",
            "No selector, embedding, retrieval, API call, score, metric, or result was created.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "status": output["status"], **actual}, sort_keys=True))


if __name__ == "__main__":
    main()
