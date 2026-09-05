#!/usr/bin/env python3
"""Bind the three Phase-4 missing-NC-prompt triads to existing approved prompts.

This is a provenance reconciliation only.  It neither authors prompt language nor
creates a selector, retrieval, embedding, provider, acceptable-set, or result
artifact.  A member is retained only when its original author prompt, final
local adequacy disposition, target source, triad source provenance, and
changed-scope Phase-3 linkage all replay without ambiguity.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase4_missing_nc_prompt_binding_2026-09-06_v1"
TARGETS = {
    ("B013", "F-59796e6dce627ba4"),
    ("B015", "F-1f956c52aa7f0c9d"),
    ("B015", "F-98199f9119042f1a"),
}

B013 = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_dense_lexical_union_b013_2026-09-04/batch_013_full_source_review_packets/reconciliation"
B015 = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_dense_lexical_union_b015_2026-09-04/batch_015_full_source_review_packets/reconciliation"
PHASE1 = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase1_reconciliation_2026-09-06_v1"
P3_PACKET = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1"
P3_RECON = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_changed_scope_qa_reconciliation_2026-09-06_v6"
P3_CLOSURE = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_closure_2026-09-06_v1"
P3_PREFLIGHT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_preflight_2026-09-06_v1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def batch_paths(reconciliation: Path) -> dict[str, Path]:
    author = reconciliation / "prompt_authoring/author_return.jsonl"
    blind = reconciliation / "prompt_authoring/target_blind_adequacy_packets"
    return {
        "author_return": author,
        "reviewer_a_return": blind / "reviewer_a_return.jsonl",
        "reviewer_b_return": blind / "reviewer_b_return.jsonl",
        "internal_reconciliation_key": blind / "internal_reconciliation_key.jsonl",
        "direct_agreements": blind / "reconciliation/direct_agreements.jsonl",
        "coordinator_return": blind / "reconciliation/coordinator_return.jsonl",
        "final_prompt_dispositions": blind / "reconciliation/final_prompt_dispositions/reconciled_prompt_dispositions.jsonl",
        "family_gate_dispositions": blind / "reconciliation/final_prompt_dispositions/family_gate_dispositions.jsonl",
        "source_provenance": reconciliation / "pass_provenance_preflight/pass_family_source_provenance_preflight.jsonl",
        "source_family_final": reconciliation / "final_dispositions/reconciled_family_dispositions.jsonl",
    }


def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"refusing to overwrite append-only output: {OUT}")

    bpaths = {"B013": batch_paths(B013), "B015": batch_paths(B015)}
    all_inputs: dict[str, Path] = {
        "master_phase1_source_union": PHASE1 / "source_union.jsonl",
        "master_phase1_family_ledger": PHASE1 / "family_state_ledger.jsonl",
        "phase3_preflight_candidate_union": P3_PREFLIGHT / "candidate_source_union.jsonl",
        "phase3_prompt_relation_packets": P3_PACKET / "prompt_relation_reviewer_packet.jsonl",
        "phase3_prompt_relation_screen": P3_PACKET / "prompt_relation_screen.jsonl",
        "phase3_prompt_cue_screen": P3_PACKET / "prompt_cue_screen.jsonl",
        "phase3_reconciliation_summary": P3_RECON / "summary.json",
        "phase3_final_record_status": P3_RECON / "final_record_status.jsonl",
        "phase3_closure_summary": P3_CLOSURE / "summary.json",
    }
    for batch, paths in bpaths.items():
        all_inputs.update({f"{batch}_{name}": path for name, path in paths.items()})
    for name, path in all_inputs.items():
        require(path.is_file(), f"missing required input {name}: {path}")

    phase1_union = jsonl(all_inputs["master_phase1_source_union"])
    phase1_by_family: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in phase1_union:
        key = (row["batch"], row["family_token"])
        if key in TARGETS:
            phase1_by_family.setdefault(key, []).append(row)
    require(set(phase1_by_family) == TARGETS, "target triads absent from Phase-1 terminal union")
    for key, rows in phase1_by_family.items():
        require(len(rows) == 3 and len({r["canonical_source_sha256"] for r in rows}) == 3, f"non-triad Phase-1 union for {key}")

    provenance: dict[tuple[str, str], list[dict[str, Any]]] = {}
    author_rows: dict[tuple[str, str, str], dict[str, Any]] = {}
    final_rows: dict[tuple[str, str, str], dict[str, Any]] = {}
    evidence_hashes: dict[str, dict[str, str]] = {}
    for batch, paths in bpaths.items():
        evidence_hashes[batch] = {name: digest(path) for name, path in paths.items()}
        for row in jsonl(paths["source_provenance"]):
            key = (batch, row["family_token"])
            if key in TARGETS:
                provenance.setdefault(key, []).append(row)
        for row in jsonl(paths["author_return"]):
            key = (batch, row["family_token"], row["target_member_token"])
            if key[:2] in TARGETS:
                require(key not in author_rows, f"duplicate author row {key}")
                author_rows[key] = row
        for row in jsonl(paths["final_prompt_dispositions"]):
            key = (batch, row["family_token"], row["intended_target_member_token"])
            if key[:2] in TARGETS:
                require(key not in final_rows, f"duplicate final disposition {key}")
                final_rows[key] = row

    for family_key, rows in provenance.items():
        require(len(rows) == 3, f"provenance is not a triad for {family_key}")
        require({r["canonical_source_sha256"] for r in rows} == {r["canonical_source_sha256"] for r in phase1_by_family[family_key]}, f"Phase-1/provenance mismatch {family_key}")
        for row in rows:
            require(row["source_byte_replay"] == "PASS_SHA256_MATCH", f"source byte replay failed {family_key} {row['member_token']}")
            paths = row.get("source_paths", [])
            require(len(paths) == 1, f"ambiguous source path {family_key} {row['member_token']}")
            source_path = ROOT / paths[0]
            require(source_path.is_file() and digest(source_path) == row["canonical_source_sha256"], f"source path does not replay {family_key} {row['member_token']}")

    # Phase-3 prompt relation packets carry complete original source text and the
    # source-visible prompt.  Index their linkage by the authoritative source
    # byte digest and exact prompt text, rather than the historical screen suffix.
    p3_packets = jsonl(all_inputs["phase3_prompt_relation_packets"])
    relation_prompt_id_by_packet = {
        row["screen_id"]: row["prompt_a_id"]
        for row in jsonl(all_inputs["phase3_prompt_relation_screen"])
    }
    p3_by_source_prompt: dict[tuple[str, str], list[str]] = {}
    p3_prompt_ids: dict[tuple[str, str], set[str]] = {}
    for packet in p3_packets:
        side_a = [x for x in packet.get("associated_source_sets", []) if x.get("side") == "A"]
        if len(side_a) != 1:
            continue
        source = side_a[0]
        if "complete_original_skill" not in source or "prompt" not in source:
            continue
        key = (text_digest(source["complete_original_skill"]), source["prompt"])
        p3_by_source_prompt.setdefault(key, []).append(packet["packet_id"])
        prompt_id = relation_prompt_id_by_packet.get(packet["packet_id"])
        if prompt_id:
            p3_prompt_ids.setdefault(key, set()).add(prompt_id)

    cue_by_prompt_id = {row["prompt_id"]: row for row in jsonl(all_inputs["phase3_prompt_cue_screen"])}
    final_status = {row["packet_id"]: row for row in jsonl(all_inputs["phase3_final_record_status"])}
    out_rows: list[dict[str, Any]] = []
    family_summary: list[dict[str, Any]] = []
    for batch, family in sorted(TARGETS):
        family_provenance = sorted(provenance[batch, family], key=lambda r: r["member_token"])
        candidate_set = []
        provenance_by_member = {}
        for source_row in family_provenance:
            source_path = ROOT / source_row["source_paths"][0]
            candidate = {
                "canonical_source_sha256": source_row["canonical_source_sha256"],
                "member_token": source_row["member_token"],
                "provenance_preflight_status": source_row["provenance_preflight_status"],
                "source_byte_replay": source_row["source_byte_replay"],
                "source_path": source_row["source_paths"][0],
                "source_path_sha256": digest(source_path),
            }
            candidate_set.append(candidate)
            provenance_by_member[source_row["member_token"]] = source_row

        family_rows: list[dict[str, Any]] = []
        for member in sorted(provenance_by_member):
            source = provenance_by_member[member]
            key = (batch, family, member)
            author = author_rows.get(key)
            final = final_rows.get(key)
            base = {
                "batch": batch,
                "family_token": family,
                "member_token": member,
                "target_canonical_source_sha256": source["canonical_source_sha256"],
                "source_visible_candidate_set": candidate_set,
                "phase1_evidence_hashes": evidence_hashes[batch],
                "claim_boundary": "Current NC prompt provenance binding only; no prompt authoring, selector, retrieval, embedding, provider, acceptable-set, metric, or result is established.",
            }
            blockers: list[str] = []
            if author is None:
                blockers.append("MISSING_AUTHOR_RETURN")
            if final is None:
                blockers.append("MISSING_FINAL_PROMPT_DISPOSITION")
            if author and author["target_source_sha256"] != source["canonical_source_sha256"]:
                blockers.append("AUTHOR_TARGET_SHA_MISMATCH")
            if final and final["final_prompt_disposition"] != "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT":
                blockers.append("NO_FINAL_ACCEPTED_LOCAL_PROMPT_DISPOSITION")
            if final and final["prompt_integrity"] != "CUE_SAFE":
                blockers.append("FINAL_PROMPT_NOT_CUE_SAFE")
            if final and final["intended_target_blind_decision"] != "MOST_SUITABLE":
                blockers.append("FINAL_TARGET_NOT_MOST_SUITABLE")

            if author:
                p3_key = (source["canonical_source_sha256"], author["prompt"])
                packet_ids = sorted(p3_by_source_prompt.get(p3_key, []))
                prompt_ids = sorted(p3_prompt_ids.get(p3_key, set()))
                if not packet_ids or len(prompt_ids) != 1:
                    blockers.append("AMBIGUOUS_OR_MISSING_PHASE3_PROMPT_RELATION_LINK")
                statuses = [final_status.get(packet_id) for packet_id in packet_ids]
                if any(status is None or status.get("status") != "RETAINED_AGREEMENT" or status.get("decision") != "RELATED_BUT_DISTINCT" for status in statuses):
                    blockers.append("PHASE3_SEMANTIC_LINK_NOT_RETAINED")
                cue_id = prompt_ids[0] if len(prompt_ids) == 1 else None
                cue = cue_by_prompt_id.get(cue_id) if cue_id else None
                if cue is None or cue.get("mechanical_disposition") != "PASS_NO_MECHANICAL_CUE_SIGNAL":
                    blockers.append("PHASE3_CUE_LINK_NOT_PASSING")
                base["phase3_linkage"] = {
                    "prompt_relation_packet_ids": packet_ids,
                    "prompt_relation_final_statuses": statuses,
                    "phase3_prompt_id": cue_id,
                    "prompt_cue_screen": cue,
                }
                base["author_prompt"] = author["prompt"]
                base["author_prompt_sha256"] = text_digest(author["prompt"])
                base["author_target_source_sha256"] = author["target_source_sha256"]
                base["source_supported_distinguishing_requirements"] = author["source_supported_distinguishing_requirements"]
                base["author_cue_audit"] = author["cue_audit"]
            if final:
                base["final_local_disposition"] = final
                base["canonical_prompt_id"] = final["prompt_token"]

            if blockers:
                base["binding_status"] = "BLOCKED_CURRENT_NC_PROMPT_BINDING"
                base["blockers"] = blockers
            else:
                base["binding_status"] = "PASS_CURRENT_NC_PROMPT_BINDING"
                base["blockers"] = []
            family_rows.append(base)
            out_rows.append(base)
        family_summary.append({
            "batch": batch,
            "family_token": family,
            "accepted_prompt_bindings": sum(r["binding_status"] == "PASS_CURRENT_NC_PROMPT_BINDING" for r in family_rows),
            "blocked_prompt_bindings": sum(r["binding_status"] != "PASS_CURRENT_NC_PROMPT_BINDING" for r in family_rows),
            "family_status": "PASS_COMPLETE_THREE_PROMPT_BINDING" if all(r["binding_status"] == "PASS_CURRENT_NC_PROMPT_BINDING" for r in family_rows) else "BLOCKED_INCOMPLETE_THREE_PROMPT_BINDING",
        })

    require(len(out_rows) == 9, f"expected exactly nine source-original prompts, got {len(out_rows)}")
    require(len({(r["batch"], r["family_token"], r["member_token"]) for r in out_rows}) == 9, "duplicate prompt binding rows")
    pass_count = sum(row["binding_status"] == "PASS_CURRENT_NC_PROMPT_BINDING" for row in out_rows)
    status = "PASS_CURRENT_NC_PROMPT_BINDING_COMPLETE" if pass_count == 9 else "BLOCKED_CURRENT_NC_PROMPT_BINDING_INCOMPLETE"

    OUT.mkdir(parents=True)
    write_jsonl(OUT / "prompt_binding_rows.jsonl", out_rows)
    input_hashes = {name: {"path": rel(path), "sha256": digest(path)} for name, path in all_inputs.items()}
    write_json(OUT / "input_hashes.json", input_hashes)
    manifest = {
        "status": status,
        "counts": {
            "target_triads": 3,
            "source_original_prompts": 9,
            "pass_current_nc_prompt_bindings": pass_count,
            "blocked_current_nc_prompt_bindings": 9 - pass_count,
            "families_with_complete_three_prompt_binding": sum(x["family_status"] == "PASS_COMPLETE_THREE_PROMPT_BINDING" for x in family_summary),
        },
        "family_summary": family_summary,
        "inputs": input_hashes,
        "implementation": {
            "script_path": rel(Path(__file__).resolve()),
            "script_sha256": digest(Path(__file__).resolve()),
        },
        "claim_boundary": "Append-only current NC prompt binding reconciliation for the three Phase-4 coverage-gap triads. Historical approved source prompts and local adequacy dispositions are rebound to current Phase-1 triad provenance and Phase-3 changed-scope semantic/cue records. No final library admission or experiment is established.",
        "no_experiment_operations": True,
        "prohibited_operations_not_performed": ["prompt_authoring", "selector", "retrieval", "embedding", "provider_call", "acceptable_set_audit", "metric", "result"],
    }
    write_json(OUT / "manifest.json", manifest)
    print(json.dumps({"output": rel(OUT), "status": status, "counts": manifest["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
