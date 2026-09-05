#!/usr/bin/env python3
"""Materialise the structural preflight for the 2026-09-04 RQ2b NC audit cut-line.

This is intentionally an audit-input preflight, not a final-library freeze.
It makes the B001--B010 cut-line reproducible and fail-closed before a
whole-library K=6 proposal/controller is allowed to be materialised.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
MANIFESTS = NC / "manifests"
OUT = MANIFESTS / "rq2b_nc_audit_input_preflight_2026-09-04"

BASE_CANDIDATES = MANIFESTS / "current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
BASE_CLUSTERS = MANIFESTS / "curation_closed_checkpoint_2026-08-31/curation_eligible_clusters.jsonl"
BASE_PROMPTS = MANIFESTS / "curation_closed_checkpoint_2026-08-31/curation_eligible_prompts.jsonl"
PARENT_PROMPTS = WORKSPACE / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
SOP = REVIEW / "ACCEPTABLE_SET_AUDIT_INPUT_FREEZE_AND_K6_SOP_2026-09-04.md"


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def batch_root(label: str) -> Path:
    n = int(label[1:])
    if n == 1:
        return REVIEW / "source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"
    if n == 2:
        return REVIEW / "source_native_lexical_continuation_2026-09-04/batch_002_full_source_review_packets"
    return REVIEW / f"source_native_dense_lexical_union_b{n:03d}_2026-09-04/batch_{n:03d}_full_source_review_packets"


def active_paths(label: str) -> tuple[Path, Path]:
    root = batch_root(label) / "reconciliation/prompt_authoring"
    if label in {"B001", "B002", "B004", "B006", "B007"}:
        leaf = root / f"batch_{int(label[1:]):03d}_post_cue_remediation_consolidation"
        return leaf / "family_gate_dispositions.jsonl", leaf / "active_prompt_dispositions.jsonl"
    leaf = root / "target_blind_adequacy_packets/reconciliation/final_prompt_dispositions"
    return leaf / "family_gate_dispositions.jsonl", leaf / "reconciled_prompt_dispositions.jsonl"


def active_prompt(row: dict[str, Any]) -> tuple[str, str, str]:
    token = row.get("active_prompt_token", row.get("prompt_token"))
    integrity = row.get("active_prompt_integrity", row.get("prompt_integrity"))
    disposition = row.get("active_prompt_disposition", row.get("final_prompt_disposition"))
    if not all(isinstance(x, str) and x for x in (token, integrity, disposition)):
        raise SystemExit(f"Malformed active prompt disposition: {row}")
    return token, integrity, disposition


def author_for_active(root: Path, row: dict[str, Any]) -> Path:
    # Only post-cue records carry a remediation round.  Round zero uses the
    # original author return; a positive round uses the rewrite return.
    if int(row.get("remediation_round", 0)) > 0:
        return root / "reconciliation/prompt_authoring/cue_remediation/author_return.jsonl"
    return root / "reconciliation/prompt_authoring/author_return.jsonl"


def main() -> int:
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite existing preflight: {OUT}")
    for path in (BASE_CANDIDATES, BASE_CLUSTERS, BASE_PROMPTS, PARENT_PROMPTS, SOP):
        if not path.is_file():
            raise SystemExit(f"Missing required input: {path}")

    base_candidates = read_jsonl(BASE_CANDIDATES)
    base_clusters = read_jsonl(BASE_CLUSTERS)
    base_prompts = read_jsonl(BASE_PROMPTS)
    parent_prompts = read_jsonl(PARENT_PROMPTS)
    if (len(base_clusters), len(base_prompts)) != (54, 125):
        raise SystemExit("Fail closed: historical curation checkpoint must be exactly 54 clusters / 125 prompts")
    if len(parent_prompts) != 381:
        raise SystemExit("Fail closed: whole-library parent prompt universe must contain exactly 381 prompts")

    candidate_by_hash: dict[str, dict[str, Any]] = {}
    for row in base_candidates:
        key = str(row.get("canonical_source_sha256", ""))
        if len(key) != 64 or key in candidate_by_hash:
            raise SystemExit("Fail closed: base candidate source union is malformed or non-unique")
        candidate_by_hash[key] = {"candidate_origin": "FROZEN_PARENT_CANDIDATE_UNION", **row}

    local_clusters: list[dict[str, Any]] = []
    local_prompts: list[dict[str, Any]] = []
    local_provenance: list[dict[str, Any]] = []
    bound_inputs: dict[str, str] = {
        rel(BASE_CANDIDATES): sha(BASE_CANDIDATES),
        rel(BASE_CLUSTERS): sha(BASE_CLUSTERS),
        rel(BASE_PROMPTS): sha(BASE_PROMPTS),
        rel(PARENT_PROMPTS): sha(PARENT_PROMPTS),
        rel(SOP): sha(SOP),
    }

    for label in (f"B{i:03d}" for i in range(1, 11)):
        root = batch_root(label)
        family_path, prompt_path = active_paths(label)
        provenance_path = root / "reconciliation/pass_provenance_preflight/pass_family_source_provenance_preflight.jsonl"
        for path in (family_path, prompt_path, provenance_path):
            bound_inputs[rel(path)] = sha(path)
        families = read_jsonl(family_path)
        prompts = read_jsonl(prompt_path)
        provenance = read_jsonl(provenance_path)
        eligible = {
            str(row["family_token"])
            for row in families
            if row.get("family_disposition") == "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
        }
        if not eligible:
            raise SystemExit(f"Fail closed: {label} has no eligible families at the declared cut-line")
        active = []
        for row in prompts:
            token, integrity, disposition = active_prompt(row)
            if row.get("family_token") in eligible:
                if disposition != "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT" or integrity != "CUE_SAFE":
                    raise SystemExit(f"Fail closed: {label} active prompt does not pass local gate: {token}")
                active.append((row, token))
        by_family: dict[str, list[tuple[dict[str, Any], str]]] = defaultdict(list)
        for item in active:
            by_family[str(item[0]["family_token"])].append(item)
        if set(by_family) != eligible or any(len(rows) != 3 for rows in by_family.values()):
            raise SystemExit(f"Fail closed: {label} eligible families must each have exactly three active prompts")

        provenance_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in provenance:
            if row.get("family_token") in eligible:
                if not str(row.get("provenance_preflight_status", "")).startswith("PASS_") or row.get("source_byte_replay") != "PASS_SHA256_MATCH":
                    raise SystemExit(f"Fail closed: {label} provenance failure for a purportedly eligible source")
                provenance_by_family[str(row["family_token"])].append(row)
        if set(provenance_by_family) != eligible or any(len(rows) != 3 for rows in provenance_by_family.values()):
            raise SystemExit(f"Fail closed: {label} eligible family provenance must bind exactly three sources")

        authors_cache: dict[Path, dict[tuple[str, str], dict[str, Any]]] = {}
        for family, rows in sorted(by_family.items()):
            sources = sorted(str(item["canonical_source_sha256"]) for item in provenance_by_family[family])
            local_clusters.append({
                "audit_cluster_id": f"RQ2B-NC-SOURCE-NATIVE-{label}-{family}",
                "cluster_origin": "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE",
                "discovery_batch": label,
                "family_token": family,
                "candidate_source_sha256": sources,
                "local_gate_disposition": "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT",
                "claim_boundary": "Audit input only; not a final cluster admission.",
            })
            for source in provenance_by_family[family]:
                source_hash = str(source["canonical_source_sha256"])
                source_paths = source.get("source_paths")
                if not isinstance(source_paths, list) or not source_paths:
                    raise SystemExit(f"Fail closed: {label} source lacks replay path")
                for source_path in source_paths:
                    file_path = WORKSPACE / str(source_path)
                    if not file_path.is_file() or sha(file_path) != source_hash:
                        raise SystemExit(f"Fail closed: local byte replay failed: {file_path}")
                if source_hash not in candidate_by_hash:
                    candidate_by_hash[source_hash] = {
                        "candidate_origin": "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE",
                        "canonical_source_sha256": source_hash,
                        "source_paths": source_paths,
                        "provenance_binding": {
                            "preflight_status": source["provenance_preflight_status"],
                            "source_byte_replay": source["source_byte_replay"],
                            "population_membership": source.get("population_membership"),
                        },
                    }
                local_provenance.append({"discovery_batch": label, **source})
            for row, token in rows:
                author_path = author_for_active(root, row)
                if author_path not in authors_cache:
                    bound_inputs[rel(author_path)] = sha(author_path)
                    authors_cache[author_path] = {
                        (str(x["family_token"]), str(x["target_member_token"])): x
                        for x in read_jsonl(author_path)
                    }
                author = authors_cache[author_path].get((family, str(row["intended_target_member_token"])))
                if author is None:
                    raise SystemExit(f"Fail closed: {label} cannot bind active prompt {token} to its authored prompt text")
                prompt_text = author.get("prompt", author.get("revised_prompt"))
                if not isinstance(prompt_text, str) or not prompt_text.strip():
                    raise SystemExit(f"Fail closed: {label} author record has no usable prompt text for {token}")
                local_prompts.append({
                    "audit_prompt_id": f"RQ2B-NC-SOURCE-NATIVE-{label}-{token}",
                    "prompt": prompt_text,
                    "prompt_text_sha256": hashlib.sha256(prompt_text.encode("utf-8")).hexdigest(),
                    "audit_cluster_id": f"RQ2B-NC-SOURCE-NATIVE-{label}-{family}",
                    "local_prompt_token": token,
                    "intended_target_source_sha256": author["target_source_sha256"],
                    "local_gate_disposition": "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT",
                    "claim_boundary": "Audit input only; no whole-library acceptable-set label exists yet.",
                })

    if len(local_clusters) != 47 or len(local_prompts) != 141:
        raise SystemExit(f"Fail closed: expected B001--B010 cut-line 47 clusters / 141 prompts, got {len(local_clusters)} / {len(local_prompts)}")
    prompt_hashes = [str(row["prompt_text_sha256"]) for row in local_prompts]
    if len(prompt_hashes) != len(set(prompt_hashes)):
        raise SystemExit("Fail closed: duplicate local prompt text at audit cut-line")
    source_prompt = Counter(str(row["intended_target_source_sha256"]) for row in local_prompts)
    if any(count != 1 for count in source_prompt.values()):
        raise SystemExit("Fail closed: a local target source must bind exactly one active prompt")

    OUT.mkdir(parents=True)
    clusters = [{"audit_cluster_id": row["cluster_id"], "cluster_origin": "FROZEN_CURATION_CHECKPOINT", **row} for row in base_clusters] + local_clusters
    prompts = [
        {
            "audit_prompt_id": row["prompt_id"],
            "prompt_text_sha256": row["prompt_sha256"],
            "prompt_origin": "FROZEN_PARENT_V3",
            "claim_boundary": "Audit input only; no whole-library acceptable-set label exists yet.",
            **row,
        }
        for row in parent_prompts
    ] + [
        {
            "audit_prompt_id": row["prompt_id"],
            "prompt_text_sha256": hashlib.sha256(str(row["prompt"]).encode("utf-8")).hexdigest(),
            "prompt_origin": "FROZEN_CURATION_CHECKPOINT",
            **row,
        }
        for row in base_prompts
    ] + local_prompts
    prompt_text_hashes = [str(row["prompt_text_sha256"]) for row in prompts]
    if len(prompt_text_hashes) != len(set(prompt_text_hashes)):
        raise SystemExit("Fail closed: exact duplicate prompt text across parent and NC audit input")
    if (len(clusters), len(prompts)) != (101, 647):
        raise SystemExit(f"Fail closed: audit input must be 101 clusters / 647 total prompts, got {len(clusters)} / {len(prompts)}")

    paths = {
        "audit_input_cluster_manifest.jsonl": sorted(clusters, key=lambda x: x["audit_cluster_id"]),
        "audit_input_prompt_manifest.jsonl": sorted(prompts, key=lambda x: x["audit_prompt_id"]),
        "audit_input_candidate_source_union.jsonl": [candidate_by_hash[key] for key in sorted(candidate_by_hash)],
        "audit_input_local_provenance_ledger.jsonl": sorted(local_provenance, key=lambda x: (x["family_token"], x["member_token"])),
    }
    for name, rows in paths.items():
        write_jsonl(OUT / name, rows)
    summary = {
        "status": "PASS_RQ2B_NC_AUDIT_INPUT_STRUCTURAL_PREFLIGHT_NOT_YET_SEALED_OR_LABELLED",
        "cut_line": "B001--B010; B011+ remain post-freeze prospective material and are excluded from this audit input.",
        "counts": {
            "frozen_parent_clusters": 54,
            "frozen_parent_prompts": 381,
            "frozen_parent_nc_prompts": 125,
            "new_local_gate_eligible_clusters": 47,
            "new_local_gate_eligible_prompts": 141,
            "audit_input_clusters": len(clusters),
            "audit_input_nc_prompts": len(base_prompts) + len(local_prompts),
            "audit_input_total_prompts": len(prompts),
            "audit_candidate_sources_exact_hash_unique": len(candidate_by_hash),
        },
        "structural_checks": {
            "exact_duplicate_prompt_text": "PASS_NONE",
            "one_local_active_prompt_per_target_source": "PASS",
            "new_local_source_byte_replay": "PASS",
            "local_provenance_dispositions": "PASS",
            "semantic_near_copy_and_split_review": "PENDING_SEALED_AUDIT_QA",
        },
        "bound_inputs": dict(sorted(bound_inputs.items())),
        "outputs": {name: sha(OUT / name) for name in paths},
        "claim_boundary": "This is a reproducible structural preflight only. It creates no K proposal, acceptable-set label, retrieval result, metric, final benchmark, or coverage claim.",
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
