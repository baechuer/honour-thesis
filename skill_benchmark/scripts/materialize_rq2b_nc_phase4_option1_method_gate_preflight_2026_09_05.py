#!/usr/bin/env python3
"""Materialise the outcome-blind Phase-4 Option-1 method-gate preflight.

This is deliberately not an audit-input queue.  It binds the Phase-3 closure,
proves the exact K=6 cardinality issue in the frozen legacy NC stratum, and
records the only source-path schema fallbacks that a later, explicitly
authorised profile builder could use.  It reads no adequacy labels, retrieval
outputs, selector outcomes, or source text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
PHASE3 = NC_ROOT / "manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
PARENT_IDENTITIES = BENCHMARK / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
OUT = NC_ROOT / "manifests/rq2b_nc_phase4_option1_method_gate_preflight_2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def cluster_id(row: dict[str, Any]) -> str:
    value = row.get("audit_cluster_id", row.get("cluster_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit("NC cluster has no stable identifier")
    return value


def prompt_id(row: dict[str, Any]) -> str:
    value = row.get("audit_prompt_id", row.get("prompt_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit("NC prompt has no stable identifier")
    return value


def prompt_cluster_id(row: dict[str, Any]) -> str:
    value = row.get("audit_cluster_id", row.get("cluster_id"))
    if not isinstance(value, str) or not value:
        raise SystemExit("NC prompt has no stable cluster identifier")
    return value


def source_hashes(cluster: dict[str, Any]) -> list[str]:
    values = cluster.get("candidate_source_sha256")
    if not isinstance(values, list) or not all(isinstance(value, str) and len(value) == 64 for value in values):
        raise SystemExit(f"Malformed source roster for {cluster_id(cluster)}")
    if len(values) != len(set(values)):
        raise SystemExit(f"Duplicate source roster member for {cluster_id(cluster)}")
    return sorted(values)


def direct_source_paths(row: dict[str, Any]) -> list[str]:
    """Return only the schema's direct (not nested-provenance) source paths."""
    paths: set[str] = set()
    historical = row.get("historical_base_candidate")
    if isinstance(historical, dict):
        if isinstance(historical.get("source_path"), str):
            paths.add(historical["source_path"])
        for key in ("rq1_records", "rq1_exact_reuse_records", "v3_identity_records"):
            for candidate in historical.get(key, []):
                if isinstance(candidate, dict) and isinstance(candidate.get("source_path"), str):
                    paths.add(candidate["source_path"])
        binding = historical.get("provenance_binding")
        if isinstance(binding, dict) and isinstance(binding.get("source_path"), str):
            paths.add(binding["source_path"])
    for origin in row.get("local_nc_origin_records", []):
        if isinstance(origin, dict):
            for path in origin.get("source_paths", []):
                if isinstance(path, str):
                    paths.add(path)
    return sorted(paths)


def nested_provenance_fallback_paths(row: dict[str, Any], source: str) -> list[str]:
    """Resolve a unique, already hash-bound fallback without changing sources."""
    paths: set[str] = set()
    origins = row.get("local_nc_origin_records")
    if not isinstance(origins, list) or not origins:
        return []
    for origin in origins:
        if not isinstance(origin, dict):
            raise SystemExit(f"Malformed local origin record for {source}")
        provenance = origin.get("provenance_record")
        if not isinstance(provenance, dict):
            raise SystemExit(f"No hash-bound provenance fallback for {source}")
        if provenance.get("canonical_source_sha256") != source:
            raise SystemExit(f"Fallback provenance identity drift for {source}")
        if provenance.get("source_byte_replay") != "PASS_SHA256_MATCH" or not str(provenance.get("provenance_preflight_status", "")).startswith("PASS_"):
            raise SystemExit(f"Fallback provenance is not an existing PASS binding for {source}")
        values = provenance.get("source_paths")
        if not isinstance(values, list) or not values or not all(isinstance(value, str) for value in values):
            raise SystemExit(f"Fallback provenance lacks replayable source paths for {source}")
        paths.update(values)
    return sorted(paths)


def replay_paths(source: str, paths: list[str], *, context: str) -> list[str]:
    if not paths:
        raise SystemExit(f"No paths available for {context}/{source}")
    resolved: list[str] = []
    for stored in paths:
        # Historical ledgers predate a single relative-root convention: V3
        # records are workspace-relative while some RQ1 records are benchmark-
        # relative.  Resolve only these two declared roots; never search.
        candidates = [WORKSPACE / stored, BENCHMARK / stored]
        existing = [path for path in candidates if path.is_file()]
        if not existing:
            raise SystemExit(f"Missing source path for {context}/{source}: {stored}")
        if any(sha(path) != source for path in existing):
            raise SystemExit(f"Source-byte drift for {context}/{source}: {stored}")
        resolved.append(stored)
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite method-gate preflight: {out}")

    paths = {
        "controlling_sop": SOP,
        "phase3_summary": PHASE3 / "summary.json",
        "candidate_source_union": PHASE3 / "candidate_source_union_for_phase4.jsonl",
        "nc_clusters": PHASE3 / "nc_cluster_manifest_for_phase4.jsonl",
        "nc_prompts": PHASE3 / "nc_prompt_manifest_for_phase4.jsonl",
        "parent_prompts": PHASE3 / "parent_prompt_manifest_for_phase5.jsonl",
        "parent_v3_identities": PARENT_IDENTITIES,
    }
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Missing required Phase-4 input: {path}")

    phase3_summary = json.loads(paths["phase3_summary"].read_text(encoding="utf-8"))
    if phase3_summary.get("status") != "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE":
        raise SystemExit("Phase-3 closure is not in the required audit-input state")

    union = read_jsonl(paths["candidate_source_union"])
    clusters = read_jsonl(paths["nc_clusters"])
    prompts = read_jsonl(paths["nc_prompts"])
    parents = read_jsonl(paths["parent_prompts"])
    parent_identity_rows = read_jsonl(paths["parent_v3_identities"])
    union_by_source = {row.get("canonical_source_sha256"): row for row in union}
    if len(union) != 3798 or len(union_by_source) != 3798 or any(not isinstance(value, str) or len(value) != 64 for value in union_by_source):
        raise SystemExit("Candidate union canonical-source cardinality drift")
    cluster_by_id = {cluster_id(row): row for row in clusters}
    prompt_by_id = {prompt_id(row): row for row in prompts}
    if len(clusters) != 297 or len(cluster_by_id) != 297 or len(prompts) != 854 or len(prompt_by_id) != 854 or len(parents) != 372:
        raise SystemExit("Phase-3 admission cardinality drift")

    prompts_by_cluster: dict[str, list[str]] = defaultdict(list)
    for prompt in prompts:
        prompts_by_cluster[prompt_cluster_id(prompt)].append(prompt_id(prompt))
    if set(prompts_by_cluster) != set(cluster_by_id):
        raise SystemExit("NC prompt-to-cluster partition drift")

    cardinality_rows: list[dict[str, Any]] = []
    by_source_count: Counter[int] = Counter()
    by_prompt_count: Counter[int] = Counter()
    two_source_prompt_count = 0
    for identifier, cluster in sorted(cluster_by_id.items()):
        roster = source_hashes(cluster)
        cluster_prompts = sorted(prompts_by_cluster[identifier])
        if len(cluster_prompts) != len(roster):
            raise SystemExit(f"All-three-family cardinality mismatch for {identifier}")
        if not set(roster).issubset(union_by_source):
            raise SystemExit(f"Cluster source lies outside frozen union: {identifier}")
        by_source_count[len(roster)] += 1
        by_prompt_count[len(cluster_prompts)] += 1
        if len(roster) == 2:
            two_source_prompt_count += len(cluster_prompts)
            cardinality_rows.append({
                "active_prompt_ids": cluster_prompts,
                "canonical_source_sha256": roster,
                "cluster_id": identifier,
                "cluster_origin_reporting_stratum": cluster.get("cluster_origin", "UNSPECIFIED"),
                "current_member_count": 2,
                "current_prompt_count": len(cluster_prompts),
                "phase4_option1_disposition": "BLOCKED_PENDING_EXPLICIT_THREE_MEMBER_FAMILY_FORM_DECISION",
                "reason": "The approved triad rule (3 local + N + H + A) cannot be applied to a two-source frozen checkpoint without changing the family form or excluding the records.",
            })
        elif len(roster) != 3:
            raise SystemExit(f"Unsupported NC source cardinality for {identifier}: {len(roster)}")

    parent_sources = {row.get("source_sha256") for row in parent_identity_rows}
    # I3C identities are chunk rows, so the hash-bound V3 source population is
    # the distinct source SHA set rather than the raw identity-row count.
    if any(not isinstance(source, str) or len(source) != 64 for source in parent_sources) or len(parent_sources) != 2431 or not parent_sources.issubset(union_by_source):
        raise SystemExit("Parent V3 identity binding drift")
    parent_delta = set(union_by_source) - parent_sources
    if len(parent_delta) != 1367:
        raise SystemExit("Parent delta cardinality drift")

    fallback_rows: list[dict[str, Any]] = []
    direct_count = 0
    fallback_count = 0
    for source, row in sorted(union_by_source.items()):
        direct_paths = direct_source_paths(row)
        if direct_paths:
            replay_paths(source, direct_paths, context="direct")
            direct_count += 1
            continue
        fallback_paths = nested_provenance_fallback_paths(row, source)
        replay_paths(source, fallback_paths, context="nested-provenance-fallback")
        fallback_count += 1
        fallback_rows.append({
            "canonical_source_sha256": source,
            "fallback_paths": fallback_paths,
            "path_resolution_disposition": "PENDING_EXPLICIT_PROFILE_METHOD_FREEZE",
            "reason": "No direct source_paths value is usable in the frozen union; the unique nested provenance binding has an existing PASS status and byte replay match.",
        })
    if direct_count != 3795 or fallback_count != 3:
        raise SystemExit("Unexpected source-path schema coverage")

    counts = {
        "candidate_sources": len(union_by_source),
        "nc_clusters": len(cluster_by_id),
        "nc_prompts": len(prompt_by_id),
        "parent_prompts": len(parents),
        "parent_v3_identity_manifest_rows": len(parent_identity_rows),
        "parent_v3_sources": len(parent_sources),
        "parent_delta_sources": len(parent_delta),
        "nc_clusters_by_source_member_count": {str(key): by_source_count[key] for key in sorted(by_source_count)},
        "nc_clusters_by_active_prompt_count": {str(key): by_prompt_count[key] for key in sorted(by_prompt_count)},
        "two_source_nc_clusters_requiring_method_decision": len(cardinality_rows),
        "two_source_nc_prompts_requiring_method_decision": two_source_prompt_count,
        "direct_source_path_bindings": direct_count,
        "nested_provenance_path_fallbacks_requiring_method_freeze": fallback_count,
    }
    if counts["nc_clusters_by_source_member_count"] != {"2": 37, "3": 260} or counts["nc_clusters_by_active_prompt_count"] != {"2": 37, "3": 260}:
        raise SystemExit("NC legacy/source-native cardinality partition drift")

    summary = {
        "status": "BLOCKED_PENDING_EXPLICIT_SOP_SECTION_15_METHOD_DECISION",
        "claim_boundary": "Outcome-blind structural and byte-replay preflight only. This artifact does not select candidates, create a queue, view acceptable-set labels, or alter the source universe.",
        "blocking_rule": "SOP section 3(5)-(6) and section 15 require an explicit decision before changing the three-member family form or proceeding with a systemic integrity defect.",
        "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in paths.values()},
        "implementation_sha256": sha(Path(__file__).resolve()),
        "counts": counts,
        "required_explicit_decisions": [
            "How the 37 frozen two-source NC clusters are handled under exact total K=6: exclude them, supply a valid third local member through a method amendment, or authorise a separately specified two-local allocation.",
            "Whether the three unique hash-bound nested provenance paths are permitted as a prospective, deterministic navigation-profile path-resolution fallback.",
        ],
        "outputs": {},
    }
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0

    out.mkdir(parents=True)
    outputs = {
        "two_source_nc_clusters_requiring_method_amendment.jsonl": cardinality_rows,
        "nested_provenance_path_fallback_candidates.jsonl": fallback_rows,
    }
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"counts": counts, "output_dir": str(out), "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
