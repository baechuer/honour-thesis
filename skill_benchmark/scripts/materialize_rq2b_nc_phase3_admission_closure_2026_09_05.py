#!/usr/bin/env python3
"""Close Phase-3 QA by making only pre-authorised exclusions/deferments."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
PREFLIGHT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
SEMANTIC = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_semantic_qa_300plus_2026-09-05_v2"
REUSE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cross_cluster_reuse_adjudication_2026-09-05"
PROMPT_CUE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_prompt_cue_adjudication_2026-09-05_v2"
CUE_CLOSURE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_001_closure_2026-09-05"
WAVE2_CLOSURE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_closure_2026-09-05"
WAVE2 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_2026-09-05"
WAVE3_CLOSURE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_closure_2026-09-05"
WAVE3 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_2026-09-05"
PARENT_CLOSURE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_parent_v3_validity_audit_closure_2026-09-05"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def cluster_identifier(row: dict[str, Any]) -> str:
    value = row.get("audit_cluster_id", row.get("cluster_id"))
    if not isinstance(value, str):
        raise SystemExit(f"Cluster lacks a stable ID: {row}")
    return value


def prompt_identifier(row: dict[str, Any]) -> str:
    value = row.get("audit_prompt_id", row.get("prompt_id"))
    if not isinstance(value, str):
        raise SystemExit(f"Prompt lacks a stable ID: {row}")
    return value


def with_status(row: dict[str, Any], status: str, reason: str) -> dict[str, Any]:
    return {**row, "phase3_admission_status": status, "phase3_admission_reason": reason}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite Phase-3 admission closure: {out}")

    paths = {
        "sop": SOP,
        "preflight_summary": PREFLIGHT / "summary.json",
        "preflight_clusters": PREFLIGHT / "nc_cluster_manifest.jsonl",
        "preflight_prompts": PREFLIGHT / "nc_prompt_manifest.jsonl",
        "preflight_parents": PREFLIGHT / "parent_prompt_manifest.jsonl",
        "preflight_union": PREFLIGHT / "candidate_source_union.jsonl",
        "semantic_source_screen": SEMANTIC / "source_relation_screen.jsonl",
        "reuse_summary": REUSE / "summary.json",
        "reuse_final": REUSE / "final_cross_cluster_dispositions.jsonl",
        "cue_final": PROMPT_CUE / "final_prompt_cue_dispositions.jsonl",
        "relation_final": PROMPT_CUE / "final_prompt_relation_dispositions.jsonl",
        "cue_closure_summary": CUE_CLOSURE / "summary.json",
        "cue_closure_final": CUE_CLOSURE / "final_remediation_dispositions.jsonl",
        "wave2_closure_summary": WAVE2_CLOSURE / "summary.json",
        "wave2_closure_final": WAVE2_CLOSURE / "final_remediation_dispositions.jsonl",
        "wave2_author": WAVE2 / "author_return.jsonl",
        "wave3_closure_summary": WAVE3_CLOSURE / "summary.json",
        "wave3_closure_final": WAVE3_CLOSURE / "final_remediation_dispositions.jsonl",
        "wave3_author": WAVE3 / "author_return.jsonl",
        "parent_closure_summary": PARENT_CLOSURE / "summary.json",
        "parent_closure_final": PARENT_CLOSURE / "final_parent_v3_validity_dispositions.jsonl",
    }
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Required Phase-3 closure binding is missing: {path}")

    clusters = read_jsonl(paths["preflight_clusters"])
    prompts = read_jsonl(paths["preflight_prompts"])
    parents = read_jsonl(paths["preflight_parents"])
    union = read_jsonl(paths["preflight_union"])
    cluster_by_id = {cluster_identifier(row): row for row in clusters}
    prompt_by_id = {prompt_identifier(row): row for row in prompts}
    if len(clusters) != 304 or len(cluster_by_id) != 304 or len(prompts) != 875 or len(prompt_by_id) != 875 or len(parents) != 381 or len(union) != 3810:
        raise SystemExit("Phase-3 preflight counts or identifiers drifted")

    # The eight exact-reuse screens identify five local family IDs. All are
    # retained in an excluded ledger; none is merged or treated as independent.
    reuse_screens = read_jsonl(paths["semantic_source_screen"])
    reuse_final = read_jsonl(paths["reuse_final"])
    reuse_cluster_ids = sorted({cluster_id for row in reuse_screens for cluster_id in row["local_cluster_ids"]})
    if len(reuse_screens) != 8 or len(reuse_final) != 8 or len(reuse_cluster_ids) != 5:
        raise SystemExit("Exact-source reuse roster drift")
    if any(row["phase3_admission_disposition"] != "BLOCKED_PENDING_EXCLUSION_OR_EXPLICIT_METHOD_DECISION" or row["triad_independence_preserved"] or row["source_disjoint_final_nc_library"] for row in reuse_final):
        raise SystemExit("Cross-reuse closure no longer supports exclusion-only resolution")
    if not set(reuse_cluster_ids).issubset(cluster_by_id):
        raise SystemExit("Cross-reuse screen names an absent NC cluster")

    # All seven avoidable local prompt cues close one of three ways: B001/B063
    # exhausted their single remediation and defer; four successors pass a
    # fresh review; the remaining prompt lies in an excluded source-reuse family.
    cue_final = read_jsonl(paths["cue_final"])
    local_cue_rows = [row for row in cue_final if row["phase3_disposition"] == "BLOCKED_LOCAL_PROMPT_REMEDIATION_AND_FRESH_BLIND_REVIEW_REQUIRED"]
    capped_rows = read_jsonl(paths["cue_closure_final"])
    wave2_rows = read_jsonl(paths["wave2_closure_final"])
    wave3_rows = read_jsonl(paths["wave3_closure_final"])
    wave2_authors = {row["original_audit_prompt_id"]: row for row in read_jsonl(paths["wave2_author"])}
    wave3_authors = {row["original_audit_prompt_id"]: row for row in read_jsonl(paths["wave3_author"])}
    remediation_authors = wave2_authors | wave3_authors
    local_cue_ids = {row["prompt_id"] for row in local_cue_rows}
    capped_ids = {row["original_audit_prompt_id"] for row in capped_rows}
    wave2_ids = {row["original_audit_prompt_id"] for row in wave2_rows}
    wave3_ids = {row["original_audit_prompt_id"] for row in wave3_rows}
    if len(local_cue_rows) != 7 or len(local_cue_ids) != 7 or len(capped_rows) != 2 or len(capped_ids) != 2 or not capped_ids.issubset(local_cue_ids) or len(wave2_rows) != 3 or len(wave2_ids) != 3 or wave2_ids != set(wave2_authors) or len(wave3_rows) != 1 or len(wave3_ids) != 1 or wave3_ids != set(wave3_authors) or not (wave2_ids | wave3_ids).issubset(local_cue_ids) or wave2_ids & wave3_ids:
        raise SystemExit("Local cue closure roster drift")
    if any(row["family_disposition"] != "DEFERRED_UNADMITTED_FAMILY_ALL_THREE_GATE_NO_LONGER_SATISFIED" or row["second_remediation_permitted"] for row in capped_rows):
        raise SystemExit("Capped cue remediation no longer supports deferment")
    if any(not row["fresh_target_blind_most_suitable"] or row["final_cue_decision"] != "CUE_SAFE" or row["second_remediation_permitted"] for row in wave2_rows):
        raise SystemExit("Wave-2 remediation no longer supports reinstatement")
    if any(not row["fresh_target_blind_most_suitable"] or row["final_cue_decision"] != "CUE_SAFE" or row["second_remediation_permitted"] for row in wave3_rows):
        raise SystemExit("Wave-3 remediation no longer supports reinstatement")
    if not local_cue_ids.issubset(prompt_by_id):
        raise SystemExit("A local cue blocker is absent from the NC prompt manifest")
    deferred_cluster_ids = sorted({cluster_identifier(prompt_by_id[prompt_id]) for prompt_id in capped_ids})
    remaining_cue_ids = local_cue_ids - capped_ids - wave2_ids - wave3_ids
    if len(deferred_cluster_ids) != 2 or len(remaining_cue_ids) != 1 or not {cluster_identifier(prompt_by_id[prompt_id]) for prompt_id in remaining_cue_ids}.issubset(set(reuse_cluster_ids)):
        raise SystemExit("Every unremediated local cue blocker must close through whole-family source-reuse exclusion")
    if set(reuse_cluster_ids) & set(deferred_cluster_ids):
        raise SystemExit("A local family received incompatible Phase-3 exclusion and deferment routes")

    # The parent V3 audit resolves the one relation case and seven cue cases by
    # exclusion only; it never changes V3 text, historical gold or results.
    relation_final = read_jsonl(paths["relation_final"])
    parent_final = read_jsonl(paths["parent_closure_final"])
    parent_excluded_ids = {prompt_id for row in parent_final if row["final_decision"].startswith("EXCLUDE") for prompt_id in row["parent_prompt_ids"]}
    relation_blockers = [row for row in relation_final if row["phase3_disposition"] == "BLOCKED_PARENT_V3_VALIDITY_AUDIT"]
    if len(relation_final) != 61 or len(relation_blockers) != 1 or len(parent_final) != 8 or len(parent_excluded_ids) != 9:
        raise SystemExit("Parent V3 validity closure roster drift")
    if any(not row["no_v3_rewrite"] or row["later_acceptable_set_decision"] for row in parent_final):
        raise SystemExit("Parent V3 validity closure violates immutability boundary")
    parent_by_id = {row["prompt_id"]: row for row in parents}
    if not parent_excluded_ids.issubset(parent_by_id):
        raise SystemExit("Parent validity closure names an absent parent prompt")

    excluded_cluster_ids = set(reuse_cluster_ids)
    deferred_cluster_id_set = set(deferred_cluster_ids)
    retained_clusters = [with_status(row, "ADMITTED_FOR_PHASE4_AUDIT_INPUT_FREEZE", "Passed Phase-3 source, prompt, cue and split-leakage closure; no acceptable-set label has been assigned.") for row in clusters if cluster_identifier(row) not in excluded_cluster_ids | deferred_cluster_id_set]
    excluded_clusters = [with_status(row, "EXCLUDED_PHASE3_EXACT_SOURCE_REUSE", "Exact source-hash reuse removed source-disjointness and triad independence; exclusion is the pre-authorised closure route.") for row in clusters if cluster_identifier(row) in excluded_cluster_ids]
    deferred_clusters = [with_status(row, "DEFERRED_PHASE3_CUE_REMEDIATION_CAPPED", "A fresh one-time source-grounded remediation retained target-most-suitable status but failed the cue gate; no second remediation is permitted.") for row in clusters if cluster_identifier(row) in deferred_cluster_id_set]
    retained_ids = {cluster_identifier(row) for row in retained_clusters}
    if len(retained_clusters) != 297 or len(excluded_clusters) != 5 or len(deferred_clusters) != 2:
        raise SystemExit("Unexpected NC cluster closure counts")

    retained_prompts, superseded_prompts = [], []
    for row in prompts:
        if cluster_identifier(row) not in retained_ids:
            continue
        original_id = prompt_identifier(row)
        if original_id in remediation_authors:
            author = remediation_authors[original_id]
            successor_id = f"{original_id}-R1"
            successor = with_status({**row, "audit_prompt_id": successor_id, "local_prompt_token": f"{row['local_prompt_token']}-R1", "prompt": author["revised_prompt"], "prompt_text_sha256": hashlib.sha256(author["revised_prompt"].encode("utf-8")).hexdigest(), "supersedes_audit_prompt_id": original_id, "active_prompt_version": "R1", "source_grounded_remediation_packet_id": author["packet_id"]}, "ADMITTED_FOR_PHASE4_AUDIT_INPUT_FREEZE", "One permitted source-grounded remediation passed fresh target-blind and cue review; no acceptable-set label has been assigned.")
            retained_prompts.append(successor)
            superseded_prompts.append(with_status({**row, "superseded_by_audit_prompt_id": successor_id, "supersession_reason": "One permitted Phase-3 cue remediation produced the active R1 successor after fresh blinded review."}, "SUPERSEDED_PHASE3_REMEDIATION", "Historical prompt retained for lineage only; its R1 successor is the prospective active audit prompt."))
        else:
            retained_prompts.append(with_status(row, "ADMITTED_FOR_PHASE4_AUDIT_INPUT_FREEZE", "Cluster retained after Phase-3 closure; no acceptable-set label has been assigned."))
    excluded_prompts = [with_status(row, "EXCLUDED_PHASE3_EXACT_SOURCE_REUSE", "Parent family excluded for cross-cluster exact source reuse.") for row in prompts if cluster_identifier(row) in excluded_cluster_ids]
    deferred_prompts = [with_status(row, "DEFERRED_PHASE3_CUE_REMEDIATION_CAPPED", "Parent family deferred after the one permitted cue remediation failed.") for row in prompts if cluster_identifier(row) in deferred_cluster_id_set]
    if len(retained_prompts) != 854 or len(superseded_prompts) != 4 or len(excluded_prompts) != 15 or len(deferred_prompts) != 6:
        raise SystemExit("Unexpected NC prompt closure counts")

    retained_local_clusters = [row for row in retained_clusters if row.get("cluster_origin") == "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE_UNADMITTED"]
    retained_checkpoint_clusters = [row for row in retained_clusters if row.get("cluster_origin") != "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE_UNADMITTED"]
    retained_local_prompts = [row for row in retained_prompts if row.get("audit_cluster_id") in {cluster_identifier(cluster) for cluster in retained_local_clusters}]
    if len(retained_local_clusters) != 243 or len(retained_checkpoint_clusters) != 54 or len(retained_local_prompts) != 729:
        raise SystemExit("NC origin-stratum count drift after closure")

    # Rebuild the prospective source union, never bulk-dropping a historical
    # canonical candidate. A source purely introduced by an excluded/deferred
    # local family disappears; an historical-base source remains, with only its
    # obsolete local-origin lineage pruned from the future audit universe.
    nonadmitted_family_tokens = {str(cluster_by_id[cluster_id]["family_token"]) for cluster_id in excluded_cluster_ids | deferred_cluster_id_set}
    final_union, pruned_origin_rows, removed_candidate_rows = [], [], []
    for row in union:
        origins = list(row.get("local_nc_origin_records", []))
        kept_origins = [origin for origin in origins if str(origin.get("family_token")) not in nonadmitted_family_tokens]
        removed_origins = [origin for origin in origins if str(origin.get("family_token")) in nonadmitted_family_tokens]
        if removed_origins:
            pruned_origin_rows.append({"canonical_source_sha256": row["canonical_source_sha256"], "pruned_local_nc_origin_records": removed_origins, "reason": "Origin family is excluded or deferred in Phase-3 closure; source bytes remain preserved in historical lineage."})
        if row.get("historical_base_candidate") is not None or kept_origins:
            final_union.append({**row, "local_nc_origin_records": kept_origins})
        else:
            if not removed_origins:
                raise SystemExit("A source cannot vanish without nonadmitted local-origin evidence")
            removed_candidate_rows.append({"canonical_source_sha256": row["canonical_source_sha256"], "removed_local_nc_origin_records": removed_origins, "reason": "Source was introduced only by a deferred/excluded local family and is absent from the prospective Phase-4 candidate universe."})
    final_union_shas = {row["canonical_source_sha256"] for row in final_union}
    if len(final_union) >= len(union) or any(row.get("historical_base_candidate") is not None for row in removed_candidate_rows):
        raise SystemExit("Prospective candidate union removal violates historical-base preservation")
    if any(source not in final_union_shas for cluster in retained_clusters for source in cluster["candidate_source_sha256"]):
        raise SystemExit("A retained NC cluster source is absent from the rebuilt candidate union")
    if any(str(row["gold_skill"]) == "" for row in parents):
        raise SystemExit("Parent manifest malformed")

    retained_parents = [with_status(row, "PENDING_PHASE5_PARENT_DELTA_AUDIT", "Immutable V3 parent retained after validity closure; historical identity/result binding remains unchanged.") for row in parents if row["prompt_id"] not in parent_excluded_ids]
    excluded_parents = [with_status(row, "EXCLUDED_PARENT_V3_VALIDITY", "Immutable V3 parent failed the outcome-blind validity audit; it is excluded, not rewritten.") for row in parents if row["prompt_id"] in parent_excluded_ids]
    if len(retained_parents) != 372 or len(excluded_parents) != 9:
        raise SystemExit("Unexpected parent validity closure counts")

    status_ledger = []
    for row in retained_clusters + excluded_clusters + deferred_clusters:
        status_ledger.append({"record_type": "NC_CLUSTER", "cluster_id": cluster_identifier(row), "family_token": row.get("family_token"), "phase3_admission_status": row["phase3_admission_status"], "phase3_admission_reason": row["phase3_admission_reason"]})
    for row in superseded_prompts:
        status_ledger.append({"record_type": "NC_PROMPT", "prompt_id": prompt_identifier(row), "phase3_admission_status": row["phase3_admission_status"], "phase3_admission_reason": row["phase3_admission_reason"], "superseded_by_audit_prompt_id": row["superseded_by_audit_prompt_id"]})
    for row in retained_parents + excluded_parents:
        status_ledger.append({"record_type": "PARENT_PROMPT", "prompt_id": row["prompt_id"], "phase3_admission_status": row["phase3_admission_status"], "phase3_admission_reason": row["phase3_admission_reason"]})

    counts = {
        "historical_phase1_structural_progress_clusters": 304,
        "historical_phase3_preflight_nc_clusters": len(clusters),
        "historical_phase3_preflight_nc_prompts": len(prompts),
        "phase3_source_reuse_excluded_nc_clusters": len(excluded_clusters),
        "phase3_cue_capped_deferred_nc_clusters": len(deferred_clusters),
        "phase3_admitted_nc_clusters_for_phase4": len(retained_clusters),
        "phase3_admitted_nc_prompts_for_phase4": len(retained_prompts),
        "phase3_remediated_active_nc_prompts_for_phase4": len(superseded_prompts),
        "phase3_admitted_source_native_nc_clusters_for_phase4": len(retained_local_clusters),
        "phase3_admitted_source_native_nc_prompts_for_phase4": len(retained_local_prompts),
        "phase3_admitted_checkpoint_nc_clusters_for_phase4": len(retained_checkpoint_clusters),
        "phase3_parent_v3_excluded_prompts": len(excluded_parents),
        "phase3_parent_v3_prompts_for_phase5": len(retained_parents),
        "historical_preflight_canonical_candidates": len(union),
        "phase3_prospective_canonical_candidates_for_phase4": len(final_union),
        "phase3_local_origin_records_pruned": sum(len(row["pruned_local_nc_origin_records"]) for row in pruned_origin_rows),
        "phase3_local_only_candidates_removed": len(removed_candidate_rows),
    }
    if counts["phase3_admitted_nc_clusters_for_phase4"] + counts["phase3_source_reuse_excluded_nc_clusters"] + counts["phase3_cue_capped_deferred_nc_clusters"] != 304:
        raise SystemExit("NC closure counts do not partition the preflight pool")

    summary = {
        "status": "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE",
        "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in paths.values()},
        "counts": counts,
        "claim_boundary": "This is a Phase-3 structural, provenance, cue, split-leakage and validity closure. It preserves historical records, makes only pre-authorised exclusions/deferments, and has not generated candidate proposals, K=6 packets, acceptable-set labels, retrieval/reranking output, metrics or a final benchmark.",
        "next_gate": "Phase 4 must resolve the predeclared total-K=6 main-pool aggregation/tie rule and freeze outcome-blind audit inputs before any acceptable-set review.",
        "outputs": {},
    }
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {
        "phase3_status_ledger.jsonl": status_ledger,
        "nc_cluster_manifest_for_phase4.jsonl": retained_clusters,
        "nc_prompt_manifest_for_phase4.jsonl": retained_prompts,
        "nc_prompt_superseded_phase3_remediation.jsonl": superseded_prompts,
        "nc_cluster_excluded_phase3.jsonl": excluded_clusters,
        "nc_prompt_excluded_phase3.jsonl": excluded_prompts,
        "nc_cluster_deferred_phase3.jsonl": deferred_clusters,
        "nc_prompt_deferred_phase3.jsonl": deferred_prompts,
        "candidate_source_union_for_phase4.jsonl": final_union,
        "candidate_local_origin_records_pruned_phase3.jsonl": pruned_origin_rows,
        "candidate_local_only_removed_phase3.jsonl": removed_candidate_rows,
        "parent_prompt_manifest_for_phase5.jsonl": retained_parents,
        "parent_prompt_excluded_validity_phase3.jsonl": excluded_parents,
    }
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": counts, "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
