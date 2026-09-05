#!/usr/bin/env python3
"""Fail-closed structural preflight for the frozen 201-cluster RQ2b NC audit input.

This is deliberately separate from the historical B001--B010 / 101-cluster
preflight.  It materialises audit *input* only: no acceptable-set labels,
retrieval result, metric, or final-library admission is produced here.
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
OUT = MANIFESTS / "rq2b_nc_audit_input_preflight_201_2026-09-04"

BASE_CANDIDATES = MANIFESTS / "current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
BASE_CLUSTERS = MANIFESTS / "curation_closed_checkpoint_2026-08-31/curation_eligible_clusters.jsonl"
BASE_PROMPTS = MANIFESTS / "curation_closed_checkpoint_2026-08-31/curation_eligible_prompts.jsonl"
PARENT_PROMPTS = WORKSPACE / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
SOP = REVIEW / "ACCEPTABLE_SET_AUDIT_INPUT_FREEZE_AND_K6_SOP_2026-09-04.md"
PROTOCOL = REVIEW / "SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CHANGE_CONTROL = REVIEW / "RQ2B_NC_EXPANSION_TO_200_CHANGE_CONTROL_2026-09-04.md"

# The declared cut line is all and only local families that completed every
# local gate by the 201-cluster freeze.  B035 contributes zero; B038 stopped
# after source review and is intentionally excluded rather than cherry-picked.
EXPECTED_ELIGIBLE_BY_BATCH = {
    "B001": 4, "B002": 2, "B003": 5, "B004": 2, "B005": 3,
    "B006": 7, "B007": 9, "B008": 6, "B009": 6, "B010": 3,
    "B011": 2, "B012": 4, "B016": 5, "B017": 8, "B018": 4,
    "B019": 9, "B021": 8, "B022": 4, "B023": 8, "B024": 2,
    "B025": 7, "B026": 6, "B027": 12, "B028": 4, "B029": 3,
    "B030": 1, "B031": 1, "B032": 3, "B033": 2, "B034": 2,
    "B036": 2, "B037": 3,
}
EXPECTED_LOCAL_CLUSTERS = 147
EXPECTED_TOTAL_CLUSTERS = 201


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
    number = int(label[1:])
    if number == 1:
        return REVIEW / "source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"
    if number == 2:
        return REVIEW / "source_native_lexical_continuation_2026-09-04/batch_002_full_source_review_packets"
    return REVIEW / f"source_native_dense_lexical_union_b{number:03d}_2026-09-04/batch_{number:03d}_full_source_review_packets"


def active_paths(root: Path) -> tuple[Path, Path]:
    authoring = root / "reconciliation/prompt_authoring"
    consolidations = sorted(authoring.glob("batch_*_post_cue_remediation_consolidation"))
    valid = [path for path in consolidations if (path / "family_gate_dispositions.jsonl").is_file() and (path / "active_prompt_dispositions.jsonl").is_file()]
    if len(valid) > 1:
        raise SystemExit(f"Fail closed: ambiguous active cue consolidation under {authoring}")
    if valid:
        return valid[0] / "family_gate_dispositions.jsonl", valid[0] / "active_prompt_dispositions.jsonl"
    final = authoring / "target_blind_adequacy_packets/reconciliation/final_prompt_dispositions"
    return final / "family_gate_dispositions.jsonl", final / "reconciled_prompt_dispositions.jsonl"


def active_prompt(row: dict[str, Any]) -> tuple[str, str, str]:
    token = row.get("active_prompt_token", row.get("prompt_token"))
    integrity = row.get("active_prompt_integrity", row.get("prompt_integrity"))
    disposition = row.get("active_prompt_disposition", row.get("final_prompt_disposition"))
    if not all(isinstance(value, str) and value for value in (token, integrity, disposition)):
        raise SystemExit(f"Malformed active prompt disposition: {row}")
    return token, integrity, disposition


def author_for_active(root: Path, row: dict[str, Any]) -> Path:
    if int(row.get("remediation_round", 0)) > 0:
        return root / "reconciliation/prompt_authoring/cue_remediation/author_return.jsonl"
    return root / "reconciliation/prompt_authoring/author_return.jsonl"


def require_file_inputs() -> None:
    for path in (BASE_CANDIDATES, BASE_CLUSTERS, BASE_PROMPTS, PARENT_PROMPTS, SOP, PROTOCOL, CHANGE_CONTROL):
        if not path.is_file():
            raise SystemExit(f"Missing required input: {path}")


def main() -> int:
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite existing preflight: {OUT}")
    require_file_inputs()

    base_candidates = read_jsonl(BASE_CANDIDATES)
    base_clusters = read_jsonl(BASE_CLUSTERS)
    base_prompts = read_jsonl(BASE_PROMPTS)
    parent_prompts = read_jsonl(PARENT_PROMPTS)
    if (len(base_clusters), len(base_prompts), len(parent_prompts)) != (54, 125, 381):
        raise SystemExit("Fail closed: frozen 54-cluster / 125-NC-prompt / 381-parent-prompt checkpoint drift")

    candidate_by_hash: dict[str, dict[str, Any]] = {}
    for row in base_candidates:
        source_hash = str(row.get("canonical_source_sha256", ""))
        if len(source_hash) != 64 or source_hash in candidate_by_hash:
            raise SystemExit("Fail closed: frozen parent candidate union is malformed or non-unique")
        candidate_by_hash[source_hash] = {"candidate_origin": "FROZEN_PARENT_CANDIDATE_UNION", **row}

    bound_inputs: dict[str, str] = {rel(path): sha(path) for path in (BASE_CANDIDATES, BASE_CLUSTERS, BASE_PROMPTS, PARENT_PROMPTS, SOP, PROTOCOL, CHANGE_CONTROL)}
    local_clusters: list[dict[str, Any]] = []
    local_prompts: list[dict[str, Any]] = []
    local_provenance: list[dict[str, Any]] = []
    seen_local_sources: set[str] = set()

    for label, expected_families in EXPECTED_ELIGIBLE_BY_BATCH.items():
        root = batch_root(label)
        family_path, prompt_path = active_paths(root)
        provenance_path = root / "reconciliation/pass_provenance_preflight/pass_family_source_provenance_preflight.jsonl"
        for path in (family_path, prompt_path, provenance_path):
            bound_inputs[rel(path)] = sha(path)
        families, prompts, provenance = read_jsonl(family_path), read_jsonl(prompt_path), read_jsonl(provenance_path)
        eligible = {str(row["family_token"]) for row in families if row.get("family_disposition") == "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"}
        if len(eligible) != expected_families:
            raise SystemExit(f"Fail closed: {label} expected {expected_families} local eligible families, got {len(eligible)}")

        by_family: dict[str, list[tuple[dict[str, Any], str]]] = defaultdict(list)
        for row in prompts:
            token, integrity, disposition = active_prompt(row)
            family = str(row.get("family_token", ""))
            if family in eligible:
                if integrity != "CUE_SAFE" or disposition != "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT":
                    raise SystemExit(f"Fail closed: {label} local prompt does not pass active gate: {token}")
                by_family[family].append((row, token))
        if set(by_family) != eligible or any(len(rows) != 3 for rows in by_family.values()):
            raise SystemExit(f"Fail closed: {label} eligible family must bind exactly three active prompts")

        provenance_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in provenance:
            family = str(row.get("family_token", ""))
            if family in eligible:
                if not str(row.get("provenance_preflight_status", "")).startswith("PASS_") or row.get("source_byte_replay") != "PASS_SHA256_MATCH":
                    raise SystemExit(f"Fail closed: {label} provenance failure for purportedly eligible source")
                provenance_by_family[family].append(row)
        if set(provenance_by_family) != eligible or any(len(rows) != 3 for rows in provenance_by_family.values()):
            raise SystemExit(f"Fail closed: {label} eligible family provenance must bind exactly three sources")

        authors_cache: dict[Path, dict[tuple[str, str], dict[str, Any]]] = {}
        for family, rows in sorted(by_family.items()):
            source_hashes: list[str] = []
            for source in provenance_by_family[family]:
                source_hash = str(source.get("canonical_source_sha256", ""))
                source_paths = source.get("source_paths")
                if len(source_hash) != 64 or not isinstance(source_paths, list) or not source_paths:
                    raise SystemExit(f"Fail closed: {label} source provenance is malformed")
                if source_hash in seen_local_sources:
                    raise SystemExit(f"Fail closed: local source re-used across eligible families: {source_hash}")
                seen_local_sources.add(source_hash)
                for source_path in source_paths:
                    file_path = WORKSPACE / str(source_path)
                    if not file_path.is_file() or sha(file_path) != source_hash:
                        raise SystemExit(f"Fail closed: local source byte replay failed: {file_path}")
                source_hashes.append(source_hash)
                candidate_by_hash.setdefault(source_hash, {
                    "candidate_origin": "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE",
                    "canonical_source_sha256": source_hash,
                    "source_paths": source_paths,
                    "provenance_binding": {
                        "preflight_status": source["provenance_preflight_status"],
                        "source_byte_replay": source["source_byte_replay"],
                        "population_membership": source.get("population_membership"),
                    },
                })
                local_provenance.append({"discovery_batch": label, **source})
            local_clusters.append({
                "audit_cluster_id": f"RQ2B-NC-SOURCE-NATIVE-{label}-{family}",
                "cluster_origin": "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE",
                "discovery_batch": label,
                "family_token": family,
                "candidate_source_sha256": sorted(source_hashes),
                "local_gate_disposition": "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT",
                "claim_boundary": "Audit input only; not a final cluster admission.",
            })
            for row, token in rows:
                author_path = author_for_active(root, row)
                if author_path not in authors_cache:
                    bound_inputs[rel(author_path)] = sha(author_path)
                    authors_cache[author_path] = {(str(item["family_token"]), str(item["target_member_token"])): item for item in read_jsonl(author_path)}
                author = authors_cache[author_path].get((family, str(row["intended_target_member_token"])))
                if author is None:
                    raise SystemExit(f"Fail closed: {label} cannot bind active prompt {token} to author return")
                text = author.get("prompt", author.get("revised_prompt"))
                if not isinstance(text, str) or not text.strip():
                    raise SystemExit(f"Fail closed: {label} author return has no usable text for {token}")
                local_prompts.append({
                    "audit_prompt_id": f"RQ2B-NC-SOURCE-NATIVE-{label}-{token}",
                    "prompt": text,
                    "prompt_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "prompt_origin": "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE",
                    "audit_cluster_id": f"RQ2B-NC-SOURCE-NATIVE-{label}-{family}",
                    "local_prompt_token": token,
                    "intended_target_source_sha256": author["target_source_sha256"],
                    "local_gate_disposition": "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT",
                    "claim_boundary": "Audit input only; no whole-library acceptable-set label exists yet.",
                })

    if (len(local_clusters), len(local_prompts)) != (EXPECTED_LOCAL_CLUSTERS, EXPECTED_LOCAL_CLUSTERS * 3):
        raise SystemExit("Fail closed: declared 201-cluster local cut line does not reconstruct")
    local_prompt_hashes = [str(row["prompt_text_sha256"]) for row in local_prompts]
    if len(local_prompt_hashes) != len(set(local_prompt_hashes)):
        raise SystemExit("Fail closed: duplicate local prompt text at the cut line")
    local_target_counts = Counter(str(row["intended_target_source_sha256"]) for row in local_prompts)
    if any(count != 1 for count in local_target_counts.values()):
        raise SystemExit("Fail closed: each local source must bind exactly one active intended prompt")

    clusters = [{"audit_cluster_id": row["cluster_id"], "cluster_origin": "FROZEN_CURATION_CHECKPOINT", **row} for row in base_clusters] + local_clusters
    prompts = ([{"audit_prompt_id": row["prompt_id"], "prompt_text_sha256": row["prompt_sha256"], "prompt_origin": "FROZEN_PARENT_V3", "claim_boundary": "Audit input only; no whole-library acceptable-set label exists yet.", **row} for row in parent_prompts] + [{"audit_prompt_id": row["prompt_id"], "prompt_text_sha256": hashlib.sha256(str(row["prompt"]).encode("utf-8")).hexdigest(), "prompt_origin": "FROZEN_CURATION_CHECKPOINT", **row} for row in base_prompts] + local_prompts)
    if len(clusters) != EXPECTED_TOTAL_CLUSTERS:
        raise SystemExit(f"Fail closed: expected {EXPECTED_TOTAL_CLUSTERS} audit clusters, got {len(clusters)}")
    all_prompt_hashes = [str(row["prompt_text_sha256"]) for row in prompts]
    if len(all_prompt_hashes) != len(set(all_prompt_hashes)):
        raise SystemExit("Fail closed: exact duplicate prompt text across full audit input")

    OUT.mkdir(parents=True)
    outputs = {
        "audit_input_cluster_manifest.jsonl": sorted(clusters, key=lambda row: row["audit_cluster_id"]),
        "audit_input_prompt_manifest.jsonl": sorted(prompts, key=lambda row: row["audit_prompt_id"]),
        "audit_input_candidate_source_union.jsonl": [candidate_by_hash[key] for key in sorted(candidate_by_hash)],
        "audit_input_local_provenance_ledger.jsonl": sorted(local_provenance, key=lambda row: (row["discovery_batch"], row["family_token"], row["member_token"])),
    }
    for name, rows in outputs.items():
        write_jsonl(OUT / name, rows)
    summary = {
        "status": "PASS_RQ2B_NC_201_AUDIT_INPUT_STRUCTURAL_PREFLIGHT_NOT_YET_SEALED_OR_LABELLED",
        "cut_line": "54 frozen checkpoint clusters plus all 147 locally gate-eligible B001--B037 families; B035 yielded zero; B038 is source-review-only reserve material and excluded.",
        "counts": {
            "frozen_checkpoint_clusters": 54,
            "frozen_checkpoint_nc_prompts": 125,
            "frozen_parent_prompts": 381,
            "new_local_gate_eligible_clusters": len(local_clusters),
            "new_local_gate_eligible_prompts": len(local_prompts),
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
            "semantic_near_copy_split_and_acceptable_set_review": "PENDING_SEALED_K6_AUDIT",
        },
        "bound_inputs": dict(sorted(bound_inputs.items())),
        "outputs": {name: sha(OUT / name) for name in outputs},
        "claim_boundary": "Structural audit-input preflight only. It creates no K proposal, acceptable-set label, retrieval result, metric, final benchmark, coverage claim, or final-library admission.",
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
