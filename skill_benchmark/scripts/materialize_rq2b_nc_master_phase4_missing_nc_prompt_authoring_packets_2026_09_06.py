#!/usr/bin/env python3
"""Materialise source-authoring packets for the three Phase-3 changed triads.

This is deliberately a packet-construction-only helper.  It neither drafts a
prompt nor evaluates a prompt, and it refuses to overwrite the versioned
output directory.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_master_phase4_missing_nc_prompt_authoring_packets_2026-09-06_v1"
)
SOP = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
)
PHASE1_SOURCE_UNION = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_master_phase1_reconciliation_2026-09-06_v1/source_union.jsonl"
)
PHASE3_ROOT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_master_phase3_preflight_2026-09-06_v1"
)
PHASE3_CANDIDATE_UNION = PHASE3_ROOT / "candidate_source_union.jsonl"
PHASE3_TERMINAL_UNION = PHASE3_ROOT / "terminal_source_union.jsonl"
PHASE3_SUMMARY = PHASE3_ROOT / "summary.json"
PHASE3_CLOSURE = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_master_phase3_closure_2026-09-06_v1/summary.json"
)
BINDING_ROOT = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
    "rq2b_nc_master_phase4_missing_nc_prompt_binding_2026-09-06_v1"
)
BINDING_MANIFEST = BINDING_ROOT / "manifest.json"
BINDING_ROWS = BINDING_ROOT / "prompt_binding_rows.jsonl"

FAMILIES = {
    "F-59796e6dce627ba4": "B013",
    "F-1f956c52aa7f0c9d": "B015",
    "F-98199f9119042f1a": "B015",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def read_jsonl_with_line_sha(path: Path) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line:
            records.append({"record": json.loads(line), "line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest()})
    return records


def stable_write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite append-only output: {rel(OUT)}")

    bound_paths = [
        SOP,
        PHASE1_SOURCE_UNION,
        PHASE3_CANDIDATE_UNION,
        PHASE3_TERMINAL_UNION,
        PHASE3_SUMMARY,
        PHASE3_CLOSURE,
        BINDING_MANIFEST,
        BINDING_ROWS,
    ]
    bound_hashes = {rel(path): sha256_file(path) for path in bound_paths}
    for path in bound_paths:
        if not path.is_file():
            raise SystemExit(f"Missing bound input: {rel(path)}")

    binding_manifest = json.loads(BINDING_MANIFEST.read_text(encoding="utf-8"))
    if binding_manifest.get("status") != "BLOCKED_CURRENT_NC_PROMPT_BINDING_INCOMPLETE":
        raise SystemExit("Unexpected current prompt-binding manifest status")
    if binding_manifest.get("counts", {}).get("pass_current_nc_prompt_bindings") != 4:
        raise SystemExit("Expected exactly four current pass bindings")
    if binding_manifest.get("counts", {}).get("blocked_current_nc_prompt_bindings") != 5:
        raise SystemExit("Expected exactly five current blocked bindings")
    binding_index = {}
    for payload in read_jsonl_with_line_sha(BINDING_ROWS):
        row = payload["record"]
        key = (row.get("family_token"), row.get("member_token"))
        if key in binding_index:
            raise SystemExit(f"Duplicate current prompt-binding row: {key}")
        binding_index[key] = payload

    terminal_rows = [
        row for row in read_jsonl(PHASE3_TERMINAL_UNION)
        if row["family_token"] in FAMILIES
    ]
    if len(terminal_rows) != 9:
        raise SystemExit(f"Expected nine terminal rows for the changed triads, found {len(terminal_rows)}")

    candidate_index: dict[str, dict] = {}
    for row in read_jsonl(PHASE3_CANDIDATE_UNION):
        for origin in row.get("local_nc_origin_records", []):
            if (
                origin.get("family_token") in FAMILIES
                and origin.get("phase_stratum") == "MASTER_PHASE1"
            ):
                key = row["canonical_source_sha256"]
                if key in candidate_index:
                    raise SystemExit(f"Duplicate changed-scope source record: {key}")
                candidate_index[key] = {"row": row, "origin": origin}

    terminal_shas = {row["canonical_source_sha256"] for row in terminal_rows}
    if terminal_shas != set(candidate_index):
        raise SystemExit(
            "Terminal union and Phase-3 provenance records disagree for changed triads: "
            f"terminal_only={sorted(terminal_shas - set(candidate_index))}; "
            f"candidate_only={sorted(set(candidate_index) - terminal_shas)}"
        )

    family_members: dict[str, list[dict]] = {family: [] for family in FAMILIES}
    for terminal in terminal_rows:
        sha = terminal["canonical_source_sha256"]
        record = candidate_index[sha]
        origin = record["origin"]
        provenance = origin.get("provenance_record", {})
        paths = origin.get("source_paths", [])
        if len(paths) != 1:
            raise SystemExit(f"Expected exactly one original path for {sha}, found {paths}")
        original_path = ROOT / paths[0]
        if not original_path.is_file():
            raise SystemExit(f"Missing original skill for {sha}: {paths[0]}")
        source_bytes = original_path.read_bytes()
        source_hash = hashlib.sha256(source_bytes).hexdigest()
        if source_hash != sha or provenance.get("canonical_source_sha256") != sha:
            raise SystemExit(f"Source-byte/provenance hash mismatch for {sha}")
        source_text = source_bytes.decode("utf-8")
        if not source_text.strip():
            raise SystemExit(f"Empty original source for {sha}")
        family_members[terminal["family_token"]].append(
            {
                "batch": terminal["batch"],
                "canonical_source_sha256": sha,
                "complete_original_skill": source_text,
                "member_token": provenance.get("member_token"),
                "original_relative_path": paths[0],
                "provenance_preflight_status": provenance.get("provenance_preflight_status"),
                "source_byte_replay": provenance.get("source_byte_replay"),
                "source_text_sha256": source_hash,
                "terminal_union_origin": terminal["origin"],
            }
        )

    scope_rows = []
    authoring_packets = []
    for family_token in sorted(FAMILIES):
        members = sorted(family_members[family_token], key=lambda member: member["member_token"])
        tokens = [member["member_token"] for member in members]
        if tokens != ["S-1", "S-2", "S-3"]:
            raise SystemExit(f"Malformed triad for {family_token}: {tokens}")
        if len({member["canonical_source_sha256"] for member in members}) != 3:
            raise SystemExit(f"Non-unique source identity in {family_token}")
        if any(member["batch"] != FAMILIES[family_token] for member in members):
            raise SystemExit(f"Batch mismatch in {family_token}")

        for target in members:
            binding_payload = binding_index.get((family_token, target["member_token"]))
            if binding_payload is None:
                raise SystemExit(f"Missing prompt-binding row for {(family_token, target['member_token'])}")
            binding = binding_payload["record"]
            if binding.get("author_target_source_sha256") != target["canonical_source_sha256"]:
                raise SystemExit(f"Prompt-binding target source mismatch for {(family_token, target['member_token'])}")
            evidence = {
                "binding_record_line_sha256": binding_payload["line_sha256"],
                "binding_status": binding["binding_status"],
                "canonical_prompt_id": binding.get("canonical_prompt_id"),
                "historical_prompt_sha256": binding.get("author_prompt_sha256"),
                "blockers": binding.get("blockers", []),
            }
            common = {
                "author_packet_id": f"PH4-MISSING-NC-AUTH-{family_token[-6:]}-{target['member_token']}",
                "batch": FAMILIES[family_token],
                "family_token": family_token,
                "target_member_token": target["member_token"],
                "target_source_sha256": target["canonical_source_sha256"],
                "packet_bound_context_sha256": {
                    rel(SOP): bound_hashes[rel(SOP)],
                    rel(PHASE3_CLOSURE): bound_hashes[rel(PHASE3_CLOSURE)],
                },
                "current_prompt_binding_evidence": evidence,
            }
            if binding["binding_status"] == "PASS_CURRENT_NC_PROMPT_BINDING":
                scope_rows.append(
                    {
                        **common,
                        "authoring_eligibility": "NO_AUTHORING_PERMITTED_ALREADY_CURRENT_PASS",
                        "claim_boundary": (
                            "Scope ledger only. Existing prompt text is not copied into this package and no "
                            "new prompt may be authored for this current-pass record."
                        ),
                    }
                )
            elif binding["binding_status"] == "BLOCKED_CURRENT_NC_PROMPT_BINDING":
                scope_rows.append(
                    {
                        **common,
                        "authoring_eligibility": "ELIGIBLE_FOR_ONE_BOUNDED_REMEDIATION_AUTHORING_DRAFT",
                        "claim_boundary": (
                            "Scope ledger only. A single source-supported remediation draft may later be "
                            "authored and must receive fresh cue and target-blind review; this is not an "
                            "admission or approval."
                        ),
                    }
                )
                authoring_packets.append(
                    {
                        **common,
                        "claim_boundary": (
                            "PACKET_CONSTRUCTION_ONLY: write one source-supported remediation draft only "
                            "when an author is later assigned. This packet is not prompt text, target-blind "
                            "review, a cue or semantic decision, a local admission, an acceptable set, a "
                            "retrieval result, or a final-library record."
                        ),
                        "instructions": [
                            "Write exactly one natural operational user-task remediation draft for the designated target member.",
                            "This is the only permitted remediation draft for this record; do not overwrite or edit the historical prompt.",
                            "Read all three complete original skills and ground every requirement in the designated target's original source.",
                            "Make the intended first-route choice meaningful through the task goal, input object, required workflow, material constraint, or deliverable.",
                            "Do not mention or copy a title, provider, repository, path, benchmark/family/member token, hash, file name, source-unique command, or distinctive literal source phrase.",
                            "Do not claim strict uniqueness, adequacy, semantic separation, cue clearance, cluster admission, acceptable-set membership, retrieval performance, or any benchmark result.",
                            "Return the structured schema only; do not alter any canonical ledger."
                        ],
                        "members": members,
                        "target_designated_for_author_only": {
                            "target_member_token": target["member_token"],
                            "target_source_sha256": target["canonical_source_sha256"],
                        },
                    }
                )
            else:
                raise SystemExit(f"Unexpected prompt-binding status: {binding['binding_status']}")

    if len(scope_rows) != 9 or len(authoring_packets) != 5:
        raise SystemExit(
            f"Expected 9 transparent scope rows and 5 remediation-authoring packets, found "
            f"{len(scope_rows)} and {len(authoring_packets)}"
        )

    OUT.mkdir(parents=True)
    scope_ledger = OUT / "authoring_scope_ledger.jsonl"
    scope_ledger.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in scope_rows), encoding="utf-8"
    )
    author_packet = OUT / "author_packet.jsonl"
    author_packet.write_text(
        "".join(json.dumps(packet, sort_keys=True) + "\n" for packet in authoring_packets), encoding="utf-8"
    )
    stable_write_json(
        OUT / "author_return_template.json",
        {
            "author_packet_id": "PH4-MISSING-NC-AUTH-...",
            "family_token": "F-...",
            "prompt": "...",
            "prompt_version": "DRAFT_1_ONLY",
            "rationale": "Explain source-supported task boundary without making an adequacy or semantic claim.",
            "source_anchors": [
                {
                    "source_sha256": "...",
                    "anchor": "Short source-grounded pointer, not a copied distinctive literal.",
                }
            ],
            "source_supported_distinguishing_requirements": ["..."],
            "target_member_token": "S-1",
            "target_source_sha256": "...",
        },
    )
    stable_write_json(
        OUT / "summary.json",
        {
            "bound_inputs": bound_hashes,
            "claim_boundary": (
                "PACKET_CONSTRUCTION_ONLY. No prompt text has been authored, reused, reviewed, "
                "approved, or admitted by this package; no semantic/cue decision, retrieval, result, "
                "or acceptable set is present."
            ),
            "counts": {
                "families": len(FAMILIES),
                "full_original_source_materials_per_authoring_packet": 3,
                "one_bounded_remediation_authoring_packets": len(authoring_packets),
                "no_authoring_permitted_already_current_pass": 4,
                "transparent_scope_records": len(scope_rows),
                "terminal_source_members": len(terminal_rows),
            },
            "family_scope": [
                {"batch": FAMILIES[family], "family_token": family}
                for family in sorted(FAMILIES)
            ],
            "outputs": {
                "author_packet.jsonl": sha256_file(author_packet),
                "authoring_scope_ledger.jsonl": sha256_file(scope_ledger),
                "author_return_template.json": sha256_file(OUT / "author_return_template.json"),
            },
            "status": "PACKET_CONSTRUCTION_ONLY",
        },
    )
    print(json.dumps({"output": rel(OUT), "packets": len(authoring_packets), "scope_records": len(scope_rows), "status": "PACKET_CONSTRUCTION_ONLY"}))


if __name__ == "__main__":
    main()
