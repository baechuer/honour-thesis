#!/usr/bin/env python3
"""Build and replay the V7 Phase-8 pre-outcome quality closure.

The builder closes only the quality-evidence gates required by the Phase-8
execution root.  It replays frozen source, prompt, dependency, exposure, review,
cue-disposition, and relation-disposition authorities.  It does not change a
source, prompt, label, acceptable set, result, metric, or selector input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_closure_2026_09_09_v1"
)
QUALITY_BUILDER_VERSION = "rq2b-v7-phase8-quality-closure-builder-v1"
QUALITY_SCHEMA = "rq2b-v7-phase8-quality-gate-v2"

EXPECTED_SOURCES = 3798
EXPECTED_PROMPTS = 1077
EXPECTED_SOURCE_BYTES = 19662831
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"

QUALITY_ASSERTIONS = {
    "split": {
        "prompt_scope_identity_replayed",
        "dependency_and_exposure_coverage_complete",
        "dependency_components_respected",
        "cross_lane_components_dispositioned",
        "no_unresolved_split_leakage",
    },
    "cue": {
        "final_prompt_scope_reviewed",
        "target_title_repository_provider_path_and_literal_source_cues_checked",
        "unavoidable_cues_stratified",
        "remediations_and_exclusions_replayed",
        "no_unresolved_cue_findings",
    },
    "duplication": {
        "source_sha_unique",
        "prompt_sha_unique",
        "aliases_forks_and_transformed_copies_reviewed",
        "dependency_edges_or_exclusions_bound",
        "no_unresolved_duplication",
    },
    "semantic_near_copy": {
        "final_prompt_scope_reviewed",
        "final_source_scope_reviewed",
        "semantic_near_copy_relations_adjudicated",
        "dependency_edges_or_exclusions_bound",
        "no_unresolved_semantic_near_copy",
    },
    "coverage": {
        "source_manifest_3798_replayed",
        "prompt_scope_1077_replayed",
        "dependency_exposure_1077_replayed",
        "source_bytes_replayed",
        "final_freeze_scope_and_exclusions_bound",
    },
}

FILES = {
    "source_union": (
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_phase3_admission_closure_300plus_2026-09-05/"
        "candidate_source_union_for_phase4.jsonl",
        SOURCE_UNION_SHA256,
    ),
    "source_manifest": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_2026_09_08_v1/source_manifest.jsonl",
        "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    ),
    "prompt_manifest": (
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/"
        "final_library_prompt_manifest.jsonl",
        PROMPT_MANIFEST_SHA256,
    ),
    "dependency_ledger": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/dependency_ledger.jsonl",
        "4226cfe2c9943d40026a4f1a9a38dbbc379ae9b8f39bd9b4c40aea8009e97fc7",
    ),
    "exposure_ledger": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/exposure_ledger.jsonl",
        "3749a72735a1c7034fd679fad24d4ce5ff40a8274144b15d8265bfb1c608dce3",
    ),
    "cue_packets": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_review_docket_2026_09_09_v3/cue_review_packets.jsonl",
        "d16d255fd49ff07833ffad1918afdd2ffa76b0218fe682a702f1b4eb28ffdb94",
    ),
    "split_packets": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_review_docket_2026_09_09_v3/mixed_lane_split_review_packets.jsonl",
        "deb28633c40e01090baea1c84735695a211e424714879ef69865795f3e947ffc",
    ),
    "prompt_relation_packets": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_review_docket_2026_09_09_v3/prompt_relation_review_packets.jsonl",
        "6cc051b58f5ffd8e5013f6aff1adc11a3b32c95ef512546bfa456739b92df8cd",
    ),
    "source_relation_packets": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_review_docket_2026_09_09_v3/source_relation_review_packets.jsonl",
        "fd7bf3b85fc727990881d35a6995806924b722ee1deb6036011cab02dd2b2107",
    ),
    "final_quality_decisions": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_coordinator_reconciliation_2026_09_09_v1/"
        "final_quality_decisions.jsonl",
        "660bbf861b3337ab888f37ec4a64ebfeea390edb424ac23d260243b4b5d853fc",
    ),
    "coordinator_integrity": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_coordinator_reconciliation_2026_09_09_v1/integrity_report.json",
        "99d68c40c159f35214dc1ab34696826e5cf59fb7e06e60f669339260389fe1e7",
    ),
    "blocked_cue_dispositions": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_cue_finding_disposition_2026_09_09_v1/"
        "blocked_cue_reissue_dispositions.jsonl",
        "5fe426195d7ccdd8aed9df59ab4d444f89df60b35a04b39fe2f3200fc9f96b83",
    ),
    "cue_sensitivity_recommendation": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_cue_finding_disposition_2026_09_09_v1/"
        "sensitivity_recommendation.json",
        "aab3d7487111c593005765ba78ac5341f458e28c401e6fd55397f1aa7bca6ec7",
    ),
    "final_source_relations": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_relation_disposition_2026_09_09_v1/final_source_relations.jsonl",
        "ce4d4601affd5d401cc85a0446303d36d699511848ad09e24eae25a954316b54",
    ),
    "source_equivalence_edges": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_relation_disposition_2026_09_09_v1/source_equivalence_edges.jsonl",
        "c29e5868a39c943e3821a2408a6e8d6f2d3ef6cd2a73cb227fa05325e61ccb4f",
    ),
    "prompt_dependency_edges": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_relation_disposition_2026_09_09_v1/prompt_dependency_edges.jsonl",
        "551201029e9a681ecc707a5357503c008c38c5e0a4220e86e4678e8775c01308",
    ),
    "relation_integrity": (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase8_quality_relation_disposition_2026_09_09_v1/integrity_report.json",
        "018bb47246d9c8c632ce6d038074ead690754b2da6c0f4553b3f01b391823040",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def pretty_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def jsonl_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(value) for value in values)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"expected JSON object: {path}:{line_number}")
            values.append(value)
    return values


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def repo_path(root: Path, value: str, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: empty path")
    supplied = Path(value)
    path = supplied.resolve() if supplied.is_absolute() else (root / supplied).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def binding(path: Path, root: Path, content_access: str) -> dict[str, str]:
    return {"path": relative(path, root), "sha256": file_sha256(path), "content_access": content_access}


def receipt_binding(path: Path, root: Path) -> dict[str, str]:
    return {"path": relative(path, root), "sha256": file_sha256(path)}


def validate_inputs(root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for role, (path_value, expected_sha) in FILES.items():
        path = repo_path(root, path_value, field=role)
        require(path.is_file(), f"missing input: {role}: {path_value}")
        require(file_sha256(path) == expected_sha, f"input hash drift: {role}")
        paths[role] = path
    return paths


def validate_authorities(root: Path, paths: dict[str, Path]) -> dict[str, Any]:
    union_rows = read_jsonl(paths["source_union"])
    require(len(union_rows) == EXPECTED_SOURCES, "source-union row-count drift")
    union_source_ids = {row.get("canonical_source_sha256") for row in union_rows}
    require(len(union_source_ids) == EXPECTED_SOURCES and None not in union_source_ids, "source-union identity drift")
    source_rows = read_jsonl(paths["source_manifest"])
    require(len(source_rows) == EXPECTED_SOURCES, "source manifest row-count drift")
    require(len({row.get("sha256") for row in source_rows}) == EXPECTED_SOURCES, "source SHA uniqueness drift")
    require(len({row.get("path") for row in source_rows}) == EXPECTED_SOURCES, "source path uniqueness drift")
    source_by_sha: dict[str, dict[str, Any]] = {}
    source_bytes = 0
    for row in source_rows:
        require(set(row) == {"path", "sha256", "bytes"}, "source manifest key drift")
        require(isinstance(row["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]), "invalid source SHA")
        path = repo_path(root, row["path"], field="source manifest path")
        require(path.is_file(), f"source file missing: {row['path']}")
        data = path.read_bytes()
        require(len(data) == row["bytes"], f"source byte-count drift: {row['path']}")
        require(sha256(data) == row["sha256"], f"source content hash drift: {row['path']}")
        source_bytes += len(data)
        source_by_sha[row["sha256"]] = row
    require(source_bytes == EXPECTED_SOURCE_BYTES, "source corpus byte-count drift")
    require(set(source_by_sha) == union_source_ids, "source manifest/source-union coverage drift")

    prompt_rows = read_jsonl(paths["prompt_manifest"])
    require(len(prompt_rows) == EXPECTED_PROMPTS, "prompt manifest row-count drift")
    prompt_by_id = {row.get("prompt_id"): row for row in prompt_rows}
    require(len(prompt_by_id) == EXPECTED_PROMPTS and None not in prompt_by_id, "prompt ID uniqueness drift")
    require(len({row.get("prompt_sha256") for row in prompt_rows}) == EXPECTED_PROMPTS, "prompt SHA uniqueness drift")
    prompt_identity = {(row["prompt_id"], row["prompt_sha256"]) for row in prompt_rows}

    dependency_rows = read_jsonl(paths["dependency_ledger"])
    exposure_rows = read_jsonl(paths["exposure_ledger"])
    for role, rows in (("dependency", dependency_rows), ("exposure", exposure_rows)):
        identities = {(row.get("prompt_id"), row.get("prompt_sha256")) for row in rows}
        require(len(rows) == EXPECTED_PROMPTS, f"{role} row-count drift")
        require(len(identities) == EXPECTED_PROMPTS, f"{role} identity uniqueness drift")
        require(identities == prompt_identity, f"{role} prompt coverage drift")
    dependency_by_prompt = {row["prompt_id"]: row for row in dependency_rows}
    exposure_by_prompt = {row["prompt_id"]: row for row in exposure_rows}
    require(
        all(dependency_by_prompt[prompt_id]["dependency_group"] == exposure_by_prompt[prompt_id]["dependency_group"] for prompt_id in prompt_by_id),
        "dependency/exposure group binding drift",
    )
    return {
        "source_rows": source_rows,
        "source_by_sha": source_by_sha,
        "source_bytes": source_bytes,
        "prompt_rows": prompt_rows,
        "prompt_by_id": prompt_by_id,
        "prompt_identity": prompt_identity,
        "dependency_by_prompt": dependency_by_prompt,
    }


def packet_map(paths: dict[str, Path], authorities: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    prompt_identity = authorities["prompt_identity"]
    source_by_sha = authorities["source_by_sha"]
    packets_by_gate: dict[str, list[dict[str, Any]]] = {
        "cue": read_jsonl(paths["cue_packets"]),
        "split": read_jsonl(paths["split_packets"]),
        "semantic_near_copy": read_jsonl(paths["prompt_relation_packets"]),
        "source_relation": read_jsonl(paths["source_relation_packets"]),
    }
    require({gate: len(rows) for gate, rows in packets_by_gate.items()} == {
        "cue": 129, "split": 6, "semantic_near_copy": 51, "source_relation": 55,
    }, "quality packet roster drift")
    result: dict[str, dict[str, Any]] = {}
    for gate, packets in packets_by_gate.items():
        for packet in packets:
            packet_id = packet.get("packet_id")
            require(isinstance(packet_id, str) and packet_id not in result, f"packet ID drift: {packet_id}")
            if gate == "cue":
                require((packet.get("prompt_id"), packet.get("prompt_sha256")) in prompt_identity, f"cue prompt binding drift: {packet_id}")
            elif gate in {"split", "semantic_near_copy"}:
                members = packet.get("members")
                require(isinstance(members, list) and len(members) >= 2, f"prompt member roster drift: {packet_id}")
                require(all((member.get("prompt_id"), member.get("prompt_sha256")) in prompt_identity for member in members), f"prompt member binding drift: {packet_id}")
                if gate == "split":
                    require(all(authorities["dependency_by_prompt"][member["prompt_id"]]["dependency_group"] == packet["dependency_group"] for member in members), f"split dependency binding drift: {packet_id}")
            else:
                members = packet.get("members")
                require(isinstance(members, list) and len(members) >= 2, f"source member roster drift: {packet_id}")
                require(all(member.get("source_sha256") in source_by_sha for member in members), f"source member binding drift: {packet_id}")
                require(all(source_by_sha[member["source_sha256"]]["path"] == member.get("source_path") for member in members), f"source path binding drift: {packet_id}")
            result[packet_id] = {
                "gate": gate,
                "packet": packet,
                "packet_sha256": sha256(canonical_bytes(packet)),
            }
    require(len(result) == 241, "quality packet union drift")
    return result, packets_by_gate


def validate_decisions(paths: dict[str, Path], packets: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    coordinator = read_json(paths["coordinator_integrity"])
    require(coordinator.get("state") == "BLOCKED_PENDING_FINDING_DISPOSITION_AND_QUALITY_CLOSURE", "coordinator reconciliation state drift")
    require(coordinator.get("counts", {}).get("final_packet_decisions") == 241, "coordinator reconciliation count drift")
    require(coordinator.get("bindings", {}).get("final_quality_decisions_sha256") == FILES["final_quality_decisions"][1], "coordinator final-decision binding drift")
    rows = read_jsonl(paths["final_quality_decisions"])
    require(len(rows) == 241, "final quality decision row-count drift")
    result = {row.get("packet_id"): row for row in rows}
    require(len(result) == 241 and set(result) == set(packets), "final quality decision coverage drift")
    for packet_id, row in result.items():
        packet = packets[packet_id]
        require(row.get("packet_sha256") == packet["packet_sha256"], f"decision packet hash drift: {packet_id}")
        require(row.get("gate") == packet["gate"], f"decision gate drift: {packet_id}")
    expected = {
        ("cue", "AVOIDABLE_IDENTITY_CUE"): 41,
        ("cue", "BLOCKED_OR_UNCLEAR"): 2,
        ("cue", "NECESSARY_TASK_CONDITION"): 80,
        ("cue", "NOT_A_CUE"): 6,
        ("semantic_near_copy", "RELATED_BUT_DISTINCT"): 48,
        ("semantic_near_copy", "TRANSFORMED_DUPLICATE"): 3,
        ("source_relation", "ALIAS_OR_FORK"): 5,
        ("source_relation", "BLOCKED_OR_UNCLEAR"): 30,
        ("source_relation", "RELATED_BUT_DISTINCT"): 19,
        ("source_relation", "TRANSFORMED_COPY"): 1,
        ("split", "DEPENDENCY_BOUND_NOT_SPLIT_LEAKAGE"): 6,
    }
    require(Counter((row["gate"], row["decision"]) for row in rows) == Counter(expected), "quality decision distribution drift")
    return result


def close_cues(paths: dict[str, Path], packets: dict[str, dict[str, Any]], decisions: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    cue_rows = {packet_id: row["decision"] for packet_id, row in decisions.items() if row["gate"] == "cue"}
    dispositions = read_jsonl(paths["blocked_cue_dispositions"])
    require(len(dispositions) == 2 and len({row.get("packet_id") for row in dispositions}) == 2, "blocked cue disposition count drift")
    for row in dispositions:
        packet_id = row["packet_id"]
        packet = packets.get(packet_id, {}).get("packet", {})
        require(cue_rows.get(packet_id) == "BLOCKED_OR_UNCLEAR", f"cue disposition does not replace blocked decision: {packet_id}")
        require(row.get("decision") == "NECESSARY_TASK_CONDITION", f"cue reissue decision drift: {packet_id}")
        require((row.get("prompt_id"), row.get("prompt_sha256")) == (packet.get("prompt_id"), packet.get("prompt_sha256")), f"cue reissue prompt binding drift: {packet_id}")
        require(row.get("findings") == packet.get("findings"), f"cue reissue finding binding drift: {packet_id}")
        cue_rows[packet_id] = row["decision"]
    require(Counter(cue_rows.values()) == {"AVOIDABLE_IDENTITY_CUE": 41, "NECESSARY_TASK_CONDITION": 82, "NOT_A_CUE": 6}, "final cue decision distribution drift")

    recommendation = read_json(paths["cue_sensitivity_recommendation"])
    require(recommendation.get("recommendation") == "RETAIN_FROZEN_EXCLUDE_PRIMARY_INCLUDE_SENSITIVITY_ONLY", "cue sensitivity policy drift")
    require(recommendation.get("population") == {"frozen_prompt_count": 1077, "avoidable_identity_cue_prompt_count": 41}, "cue sensitivity population drift")
    sensitivity = []
    for packet_id in sorted(packet_id for packet_id, decision in cue_rows.items() if decision == "AVOIDABLE_IDENTITY_CUE"):
        packet = packets[packet_id]["packet"]
        sensitivity.append({
            "schema_version": "rq2b-v7-phase8-cue-sensitivity-ledger-v1",
            "packet_id": packet_id,
            "packet_sha256": packets[packet_id]["packet_sha256"],
            "prompt_id": packet["prompt_id"],
            "prompt_sha256": packet["prompt_sha256"],
            "final_cue_decision": "AVOIDABLE_IDENTITY_CUE",
            "findings": packet["findings"],
            "analysis_disposition": "EXCLUDE_PRIMARY_INFERENTIAL_INCLUDE_SEPARATE_SENSITIVITY",
            "frozen_prompt_preserved": True,
            "primary_inferential_included": False,
            "sensitivity_included": True,
        })
    require(len(sensitivity) == 41 and len({row["prompt_id"] for row in sensitivity}) == 41, "cue sensitivity ledger coverage drift")
    return sensitivity, cue_rows


def close_relations(paths: dict[str, Path], packets: dict[str, dict[str, Any]], decisions: dict[str, dict[str, Any]], authorities: dict[str, Any]) -> dict[str, Any]:
    integrity = read_json(paths["relation_integrity"])
    require(integrity.get("state") == "PROSPECTIVE_OVERLAY_READY_WITH_DISCLOSED_ANCHOR_LIMITATION", "relation disposition state drift")
    require(integrity.get("counts") == {
        "by_decision": {"ALIAS_OR_FORK": 8, "RELATED_BUT_DISTINCT": 11, "TRANSFORMED_COPY": 17},
        "final_source_relations": 36,
        "prompt_dependency_edges": 3,
        "source_equivalence_edges": 25,
    }, "relation disposition count drift")
    require(integrity.get("preservation") == {
        "overlay_only": True, "prompt_mutation": False, "prompts": 1077,
        "source_mutation": False, "sources": 3798,
    }, "relation preservation boundary drift")
    for name, role in (("final_source_relations.jsonl", "final_source_relations"), ("source_equivalence_edges.jsonl", "source_equivalence_edges"), ("prompt_dependency_edges.jsonl", "prompt_dependency_edges")):
        require(integrity.get("outputs", {}).get(name, {}).get("sha256") == FILES[role][1], f"relation output binding drift: {name}")
    source_base = {packet_id: row["decision"] for packet_id, row in decisions.items() if row["gate"] == "source_relation" and row["decision"] != "BLOCKED_OR_UNCLEAR"}
    relation_rows = read_jsonl(paths["final_source_relations"])
    require(len(relation_rows) == 36 and len({row.get("packet_id") for row in relation_rows}) == 36, "final source relation count drift")
    for row in relation_rows:
        packet_id = row["packet_id"]
        require(packet_id in packets and packets[packet_id]["gate"] == "source_relation", f"source relation packet drift: {packet_id}")
        require(row["packet_sha256"] == packets[packet_id]["packet_sha256"], f"source relation packet hash drift: {packet_id}")
        require(row["decision"] in {"ALIAS_OR_FORK", "TRANSFORMED_COPY", "RELATED_BUT_DISTINCT"}, f"source relation decision drift: {packet_id}")
        packet_members = {(m["source_path"], m["source_sha256"]) for m in packets[packet_id]["packet"]["members"]}
        final_members = {(m["source_path"], m["source_sha256"]) for m in row["members"]}
        require(final_members == packet_members, f"source relation member drift: {packet_id}")
        source_base[packet_id] = row["decision"]
    require(len(source_base) == 55, "final source relation coverage drift")
    require(Counter(source_base.values()) == {"ALIAS_OR_FORK": 8, "RELATED_BUT_DISTINCT": 30, "TRANSFORMED_COPY": 17}, "final source relation distribution drift")

    prompt_final = {packet_id: row["decision"] for packet_id, row in decisions.items() if row["gate"] == "semantic_near_copy"}
    require(len(prompt_final) == 51, "final prompt relation coverage drift")
    require(Counter(prompt_final.values()) == {"RELATED_BUT_DISTINCT": 48, "TRANSFORMED_DUPLICATE": 3}, "final prompt relation distribution drift")

    source_edges = read_jsonl(paths["source_equivalence_edges"])
    require(len(source_edges) == 25 and len({row.get("edge_id") for row in source_edges}) == 25, "source equivalence edge count drift")
    equivalent_packets = {packet_id for packet_id, decision in source_base.items() if decision in {"ALIAS_OR_FORK", "TRANSFORMED_COPY"}}
    require({row.get("packet_id") for row in source_edges} == equivalent_packets, "source equivalence edge coverage drift")
    source_pairs = set()
    for row in source_edges:
        require(row.get("relation") == source_base[row["packet_id"]], f"source equivalence relation drift: {row['packet_id']}")
        members = row.get("members")
        require(isinstance(members, list) and len(members) == 2, f"source equivalence arity drift: {row['edge_id']}")
        member_set = {(m.get("source_path"), m.get("source_sha256")) for m in members}
        packet_set = {(m["source_path"], m["source_sha256"]) for m in packets[row["packet_id"]]["packet"]["members"]}
        require(member_set == packet_set, f"source equivalence member drift: {row['edge_id']}")
        require(all(source_sha in authorities["source_by_sha"] for _, source_sha in member_set), f"source equivalence scope drift: {row['edge_id']}")
        pair = tuple(sorted(source_sha for _, source_sha in member_set))
        require(pair not in source_pairs, f"duplicate source equivalence pair: {row['edge_id']}")
        source_pairs.add(pair)

    prompt_edges = read_jsonl(paths["prompt_dependency_edges"])
    require(len(prompt_edges) == 3 and len({row.get("edge_id") for row in prompt_edges}) == 3, "prompt dependency edge count drift")
    duplicate_packets = {packet_id for packet_id, decision in prompt_final.items() if decision == "TRANSFORMED_DUPLICATE"}
    require({row.get("packet_id") for row in prompt_edges} == duplicate_packets, "prompt dependency edge coverage drift")
    prompt_pairs = set()
    for row in prompt_edges:
        require(row.get("relation") == "TRANSFORMED_DUPLICATE", f"prompt dependency relation drift: {row['edge_id']}")
        members = row.get("members")
        require(isinstance(members, list) and len(members) == 2, f"prompt dependency arity drift: {row['edge_id']}")
        member_set = {(m.get("prompt_id"), m.get("prompt_sha256")) for m in members}
        packet_set = {(m["prompt_id"], m["prompt_sha256"]) for m in packets[row["packet_id"]]["packet"]["members"]}
        require(member_set == packet_set and member_set <= authorities["prompt_identity"], f"prompt dependency member drift: {row['edge_id']}")
        pair = tuple(sorted(prompt_id for prompt_id, _ in member_set))
        require(pair not in prompt_pairs, f"duplicate prompt dependency pair: {row['edge_id']}")
        prompt_pairs.add(pair)
    return {
        "source_final": source_base,
        "prompt_final": prompt_final,
        "source_edges": source_edges,
        "prompt_edges": prompt_edges,
    }


def decision_receipt(*, gate: str, counts: dict[str, int], bindings: dict[str, dict[str, str]], assertions: dict[str, bool], boundary: str) -> dict[str, Any]:
    require(all(assertions.values()), f"non-PASS receipt assertion: {gate}")
    return {
        "schema_version": "rq2b-v7-phase8-final-semantic-adjudication-receipt-v1",
        "gate": gate,
        "status": "PASS_FINAL_ADJUDICATION_COMPLETE",
        "source_union_sha256": SOURCE_UNION_SHA256,
        "prompt_manifest_sha256": PROMPT_MANIFEST_SHA256,
        "counts": counts,
        "unresolved_findings": 0,
        "bindings": bindings,
        "assertions": assertions,
        "boundary": boundary,
    }


def build(root: Path, output_dir: Path, builder_path: Path | None = None) -> dict[str, bytes]:
    builder_path = (builder_path or Path(__file__)).resolve()
    paths = validate_inputs(root)
    authorities = validate_authorities(root, paths)
    packets, _ = packet_map(paths, authorities)
    decisions = validate_decisions(paths, packets)
    sensitivity_rows, cue_final = close_cues(paths, packets, decisions)
    relations = close_relations(paths, packets, decisions, authorities)

    split_final = {packet_id: row["decision"] for packet_id, row in decisions.items() if row["gate"] == "split"}
    require(len(split_final) == 6 and set(split_final.values()) == {"DEPENDENCY_BOUND_NOT_SPLIT_LEAKAGE"}, "split closure drift")

    output_paths = {name: output_dir / name for name in (
        "cue_sensitivity_ledger.jsonl",
        "split_final_adjudication_receipt.json",
        "cue_final_adjudication_receipt.json",
        "duplication_final_adjudication_receipt.json",
        "semantic_near_copy_final_adjudication_receipt.json",
    )}
    payloads: dict[str, bytes] = {}
    payloads["cue_sensitivity_ledger.jsonl"] = jsonl_bytes(sensitivity_rows)

    split_receipt = decision_receipt(
        gate="split",
        counts={"reviewed_packets": 6, "dependency_bound_not_split_leakage": 6, "split_leakage": 0},
        bindings={
            "split_packets": receipt_binding(paths["split_packets"], root),
            "final_quality_decisions": receipt_binding(paths["final_quality_decisions"], root),
            "dependency_ledger": receipt_binding(paths["dependency_ledger"], root),
            "exposure_ledger": receipt_binding(paths["exposure_ledger"], root),
        },
        assertions={"six_cross_lane_components_reviewed": True, "all_six_dependency_bound": True, "no_split_leakage": True},
        boundary="Dependency components remain intact for grouped inference; no prompt or dependency record is rewritten here.",
    )
    cue_receipt = decision_receipt(
        gate="cue",
        counts={"reviewed_packets": 129, "avoidable_identity_cue": 41, "necessary_task_condition": 82, "not_a_cue": 6, "blocked_reissues": 2, "primary_prompts_after_sensitivity_exclusion": 1036},
        bindings={
            "cue_packets": receipt_binding(paths["cue_packets"], root),
            "final_quality_decisions": receipt_binding(paths["final_quality_decisions"], root),
            "blocked_cue_dispositions": receipt_binding(paths["blocked_cue_dispositions"], root),
            "sensitivity_recommendation": receipt_binding(paths["cue_sensitivity_recommendation"], root),
            "cue_sensitivity_ledger": {"path": relative(output_paths["cue_sensitivity_ledger.jsonl"], root), "sha256": sha256(payloads["cue_sensitivity_ledger.jsonl"])},
        },
        assertions={"two_blocked_packets_reissued": True, "all_cue_packets_final": True, "forty_one_sensitivity_prompts_frozen": True, "no_prompt_mutation": True},
        boundary="All 1,077 prompts remain frozen. The 41 avoidable-cue prompts are prospectively excluded only from primary inference and retained for separate sensitivity reporting.",
    )
    duplication_receipt = decision_receipt(
        gate="duplication",
        counts={"reviewed_source_relation_packets": 55, "alias_or_fork": 8, "transformed_copy": 17, "related_but_distinct": 30, "source_equivalence_edges": 25},
        bindings={
            "source_relation_packets": receipt_binding(paths["source_relation_packets"], root),
            "final_quality_decisions": receipt_binding(paths["final_quality_decisions"], root),
            "final_source_relations": receipt_binding(paths["final_source_relations"], root),
            "source_equivalence_edges": receipt_binding(paths["source_equivalence_edges"], root),
            "relation_integrity": receipt_binding(paths["relation_integrity"], root),
        },
        assertions={"all_source_relation_packets_final": True, "all_copy_or_alias_relations_have_equivalence_edges": True, "source_sha_and_paths_replayed": True, "no_source_mutation": True},
        boundary="The 25 edges are a prospective acceptable-source/offline-scoring equivalence overlay; all 3,798 source files remain separate and byte-frozen.",
    )
    semantic_receipt = decision_receipt(
        gate="semantic_near_copy",
        counts={"reviewed_prompt_relation_packets": 51, "prompt_related_but_distinct": 48, "prompt_transformed_duplicate": 3, "prompt_dependency_edges": 3, "reviewed_source_relation_packets": 55, "source_equivalence_edges": 25},
        bindings={
            "prompt_relation_packets": receipt_binding(paths["prompt_relation_packets"], root),
            "source_relation_packets": receipt_binding(paths["source_relation_packets"], root),
            "final_quality_decisions": receipt_binding(paths["final_quality_decisions"], root),
            "final_source_relations": receipt_binding(paths["final_source_relations"], root),
            "prompt_dependency_edges": receipt_binding(paths["prompt_dependency_edges"], root),
            "source_equivalence_edges": receipt_binding(paths["source_equivalence_edges"], root),
        },
        assertions={"all_prompt_relation_packets_final": True, "all_source_relation_packets_final": True, "three_prompt_duplicates_dependency_bound": True, "twenty_five_source_equivalences_bound": True, "no_prompt_or_source_mutation": True},
        boundary="Near-copy findings become only pre-outcome dependency/equivalence overlays. They are not retrieval features and do not alter prompts, sources, labels, or outcomes.",
    )
    receipts = {
        "split_final_adjudication_receipt.json": split_receipt,
        "cue_final_adjudication_receipt.json": cue_receipt,
        "duplication_final_adjudication_receipt.json": duplication_receipt,
        "semantic_near_copy_final_adjudication_receipt.json": semantic_receipt,
    }
    payloads.update({name: pretty_bytes(value) for name, value in receipts.items()})

    report_inputs = {
        "split": [paths["prompt_manifest"], paths["dependency_ledger"], paths["exposure_ledger"], paths["split_packets"], paths["final_quality_decisions"]],
        "cue": [paths["prompt_manifest"], paths["cue_packets"], paths["final_quality_decisions"], paths["blocked_cue_dispositions"], paths["cue_sensitivity_recommendation"], output_paths["cue_sensitivity_ledger.jsonl"]],
        "duplication": [paths["source_union"], paths["source_manifest"], paths["prompt_manifest"], paths["source_relation_packets"], paths["final_source_relations"], paths["source_equivalence_edges"], paths["relation_integrity"]],
        "semantic_near_copy": [paths["source_union"], paths["source_manifest"], paths["prompt_manifest"], paths["prompt_relation_packets"], paths["source_relation_packets"], paths["final_quality_decisions"], paths["final_source_relations"], paths["source_equivalence_edges"], paths["prompt_dependency_edges"]],
        "coverage": [paths["source_union"], paths["source_manifest"], paths["prompt_manifest"], paths["dependency_ledger"], paths["exposure_ledger"]],
    }
    report_names = {
        "split": "split_quality_report.json",
        "cue": "cue_quality_report.json",
        "duplication": "duplication_quality_report.json",
        "semantic_near_copy": "semantic_near_copy_quality_report.json",
        "coverage": "coverage_quality_report.json",
    }
    receipt_names = {
        "split": "split_final_adjudication_receipt.json",
        "cue": "cue_final_adjudication_receipt.json",
        "duplication": "duplication_final_adjudication_receipt.json",
        "semantic_near_copy": "semantic_near_copy_final_adjudication_receipt.json",
    }
    # Output files referenced by the reports do not exist yet during creation;
    # use their deterministic payload hashes and materialise them temporarily in
    # memory-aware bindings below.
    for role, name in report_names.items():
        evidence = []
        for path in report_inputs[role]:
            if path == output_paths["cue_sensitivity_ledger.jsonl"]:
                evidence.append({"path": relative(path, root), "sha256": sha256(payloads[path.name]), "content_access": "PARSED_MECHANICAL_REPLAY"})
            else:
                evidence.append(binding(path, root, "PARSED_MECHANICAL_REPLAY"))
        receipt_name = receipt_names.get(role)
        report = {
            "schema_version": QUALITY_SCHEMA,
            "gate": role,
            "status": "PASS",
            "formal_execution_ready": True,
            "source_union_sha256": SOURCE_UNION_SHA256,
            "prompt_manifest_sha256": PROMPT_MANIFEST_SHA256,
            "counts": {"prompts": EXPECTED_PROMPTS, "sources": EXPECTED_SOURCES, "unresolved_findings": 0},
            "assertions": {assertion: "PASS" for assertion in sorted(QUALITY_ASSERTIONS[role])},
            "evidence": evidence,
            "review_provenance": {
                "semantic_judgment_required": receipt_name is not None,
                "final_adjudication_receipt": ({"path": relative(output_dir / receipt_name, root), "sha256": sha256(payloads[receipt_name])} if receipt_name else None),
                "content_access": "HASH_ONLY_OPAQUE_FINAL_ADJUDICATION_PROVENANCE" if receipt_name else "NOT_APPLICABLE_MECHANICAL_GATE",
            },
            "quality_builder": {"path": relative(builder_path, root), "sha256": file_sha256(builder_path), "version": QUALITY_BUILDER_VERSION},
        }
        payloads[name] = pretty_bytes(report)

    readme = f"""# RQ2b-NC V7 Phase-8 quality closure v1

Status: `PASS_PHASE8_QUALITY_CLOSURE_PRE_OUTCOME`.

This versioned package closes the five strict quality-report interfaces used by
the Phase-8 execution root. It replays 3,798 exact source files, 1,077 prompt
identities, and complete 1,077-row dependency and exposure ledgers.

The final semantic evidence comprises six split decisions, 129 cue decisions
(including two traceable blocked-packet reissues), 55 final source-relation
decisions, and 51 prompt near-copy decisions. The 41 avoidable-cue prompts stay
byte-frozen, are excluded from primary inferential summaries, and remain in a
separate sensitivity-only stratum. The 25 source-equivalence edges and three
prompt-dependency edges are prospective offline-analysis overlays only.

No query, source, label, acceptable set, retrieval output, result, or metric is
created or modified. The package is a quality gate, not experiment authority.

Exact replay:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_closure.py --root "$PWD" --output-dir {OUTPUT.as_posix()} --verify
```
"""
    payloads["README.md"] = readme.encode()

    input_bindings = {role: {"path": relative(paths[role], root), "sha256": expected_sha} for role, (_, expected_sha) in FILES.items()}
    artifact_rows = {
        name: {"sha256": sha256(data), "bytes": len(data), **({"rows": len(data.splitlines())} if name.endswith(".jsonl") else {})}
        for name, data in sorted(payloads.items())
    }
    integrity = {
        "schema_version": "rq2b-v7-phase8-quality-closure-integrity-v1",
        "status": "PASS_PHASE8_QUALITY_CLOSURE_PRE_OUTCOME",
        "formal_execution_ready": True,
        "scope": {"sources": EXPECTED_SOURCES, "source_bytes": authorities["source_bytes"], "prompts": EXPECTED_PROMPTS, "source_union_sha256": SOURCE_UNION_SHA256, "prompt_manifest_sha256": PROMPT_MANIFEST_SHA256},
        "counts": {
            "split_packets_final": len(split_final),
            "cue_packets_final": len(cue_final),
            "blocked_cue_reissues": 2,
            "cue_sensitivity_prompts": len(sensitivity_rows),
            "primary_prompts_after_cue_sensitivity_exclusion": EXPECTED_PROMPTS - len(sensitivity_rows),
            "source_relations_final": len(relations["source_final"]),
            "prompt_relations_final": len(relations["prompt_final"]),
            "source_equivalence_edges": len(relations["source_edges"]),
            "prompt_dependency_edges": len(relations["prompt_edges"]),
            "unresolved_findings": 0,
            "quality_pass_reports": 5,
        },
        "assertions": {
            "all_3798_source_bytes_hash_replayed": True,
            "prompt_dependency_exposure_identity_union_is_1077": True,
            "cue_sensitivity_ledger_is_exactly_41": True,
            "two_blocked_cues_traceably_dispositioned": True,
            "all_six_split_packets_dependency_bound": True,
            "all_55_source_relations_final_without_unclear": True,
            "all_51_prompt_relations_final_without_unclear": True,
            "source_equivalence_edges_are_exactly_25": True,
            "prompt_dependency_edges_are_exactly_3": True,
            "no_frozen_input_mutation": True,
            "no_label_result_metric_or_selector_activity": True,
        },
        "inputs": input_bindings,
        "artifacts": artifact_rows,
        "builder": {"path": relative(builder_path, root), "sha256": file_sha256(builder_path), "version": QUALITY_BUILDER_VERSION},
        "replay_command": f"python3 -B {relative(builder_path, root)} --root {root} --output-dir {relative(output_dir, root)} --verify",
        "boundary": "Quality closure only. Prospective sensitivity/dependency/equivalence overlays do not mutate the 1,077 prompts, 3,798 sources, labels, acceptable sets, retrieval inputs, results, or metrics.",
    }
    payloads["integrity_report.json"] = pretty_bytes(integrity)
    return payloads


def verify(root: Path, output_dir: Path) -> dict[str, Any]:
    require(output_dir.is_dir(), "quality closure package missing")
    expected = build(root, output_dir)
    present = {path.name for path in output_dir.iterdir() if path.is_file()}
    require(present == set(expected), f"quality closure file-set drift: {sorted(present ^ set(expected))}")
    for name, data in expected.items():
        require((output_dir / name).read_bytes() == data, f"quality closure artifact drift: {name}")
    return json.loads(expected["integrity_report.json"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = repo_path(root, str(args.output_dir), field="output-dir")
    if args.verify:
        report = verify(root, output_dir)
        status = "PASS_V7_PHASE8_QUALITY_CLOSURE_REPLAY"
    else:
        require(not output_dir.exists(), f"refusing to overwrite output: {output_dir}")
        payloads = build(root, output_dir)
        output_dir.mkdir(parents=True)
        for name, data in payloads.items():
            with (output_dir / name).open("xb") as handle:
                handle.write(data)
        report = json.loads(payloads["integrity_report.json"])
        status = "PASS_V7_PHASE8_QUALITY_CLOSURE_CREATED"
    print(json.dumps({"status": status, "counts": report["counts"], "output": relative(output_dir, root)}, sort_keys=True))


if __name__ == "__main__":
    main()
