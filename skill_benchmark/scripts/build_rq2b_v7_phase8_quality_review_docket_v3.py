#!/usr/bin/env python3
"""Build target-blind Phase-8 quality review packets and a blocking docket.

This builder replays the restored Phase-3 evidence chain plus the final V7
label-free prompt, source, and dependency scope.  It deliberately emits no
quality PASS report: lexical/metadata screens nominate review records but do
not prove that semantic near-copies are absent.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import itertools
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


BUILDER_VERSION = "rq2b-v7-phase8-quality-review-docket-builder-v3"
DOCKET_SCHEMA = "rq2b-v7-phase8-quality-review-blocking-docket-v3"
READAUDIT_SCHEMA = "rq2b-v7-phase3-evidence-reaudit-v3"
INTEGRITY_SCHEMA = "rq2b-v7-phase8-quality-review-docket-integrity-v3"
PACKET_SCHEMA = "rq2b-v7-phase8-target-blind-quality-review-packet-v3"
DECISION_TEMPLATE_SCHEMA = "rq2b-v7-phase8-quality-decision-template-v3"
BLOCKED_STATUS = "BLOCKED_PHASE8_FINAL_SEMANTIC_AND_SPLIT_DISPOSITIONS_PENDING"

EXPECTED_PROMPTS = 1077
EXPECTED_SOURCES = 3798
EXPECTED_SOURCE_BYTES = 19_662_831
EXPECTED_DEPENDENCY_GROUPS = 355
EXPECTED_PARENT_PROMPTS = 363
EXPECTED_NC_PROMPTS = 714
EXPECTED_PHASE3_BOUND_INPUTS = 21
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
EXPECTED_MIXED_GROUPS = {
    "D-4542222952D86809",
    "D-4FB180C98024AE17",
    "D-7EF530E0C3769462",
    "D-AF6B0790C8B793A9",
    "D-D1872BC8FBDFA53E",
    "D-E582B8FFB096C3DC",
}

WORD = re.compile(r"[a-z0-9]+")
STOPWORDS = frozenset(
    "a an and are as at be by for from has have in into is it its of on or that the their this to with your you".split()
)


@dataclass(frozen=True)
class FixedArtifact:
    path: str
    sha256: str
    opaque: bool = False


FIXED_ARTIFACTS = {
    "approved_plan": FixedArtifact(
        "thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md",
        "b54d3d8c6816b2bb5f75b2b946448063fcc800c1f9927e27babd767e3468d4d8",
    ),
    "master_sop": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md",
        "68f7a8e4e802317208d72155b6b3490d0f3587324aaebb67cfac0341241b8835",
    ),
    "plan_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/rq2_approved_research_plan_2026_09_08_v1/plan_freeze.json",
        "c91b459babec83409b5b17d254cc299a77081afc94fc813173ad3ae7f80eb097",
    ),
    "phase3_closure": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05/summary.json",
        "469363a5ef69c5d1a35b8724967f98d485cb4d4ac0ddae3778b2a43454d2238a",
    ),
    "phase3_source_union": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05/candidate_source_union_for_phase4.jsonl",
        SOURCE_UNION_SHA256,
    ),
    "final_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/integrity_report.json",
        "f77df13f55fd151a2831ba448c6efa4bf760942f9e925f837eeb9a365c8eed4a",
    ),
    "final_prompt_manifest": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/final_library_prompt_manifest.jsonl",
        PROMPT_MANIFEST_SHA256,
        opaque=True,
    ),
    "first_matrix_readiness": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/readiness_report.json",
        "55f666bc3daa96f3e37f7209761b4a0c06eb7aaf14484db0a4b7d6aea94725e0",
    ),
    "source_manifest": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/source_manifest.jsonl",
        "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    ),
    "analysis_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/freeze_report.json",
        "1b27a1a6f7423871c7e9b7206736d60e3838e405af1cf2f5b078f0db58f784f7",
    ),
    "dependency_ledger": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/dependency_ledger.jsonl",
        "4226cfe2c9943d40026a4f1a9a38dbbc379ae9b8f39bd9b4c40aea8009e97fc7",
    ),
    "exposure_ledger": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/exposure_ledger.jsonl",
        "3749a72735a1c7034fd679fad24d4ce5ff40a8274144b15d8265bfb1c608dce3",
        opaque=True,
    ),
    "label_free_runtime": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl",
        "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(row) for row in rows)


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def root_path(root: Path, value: str, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: path missing")
    raw = Path(value)
    path = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def exact_keys(value: Any, expected: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: expected object")
    require(set(value) == expected, f"{field}: key drift: {sorted(set(value) ^ expected)}")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected object: {path}:{line_number}")
            rows.append(value)
    return rows


def validate_fixed(root: Path, fixed: dict[str, FixedArtifact]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role, artifact in fixed.items():
        path = root_path(root, artifact.path, field=role)
        require(path.is_file(), f"Missing fixed artifact: {role}")
        require(file_sha256(path) == artifact.sha256, f"Fixed artifact hash drift: {role}")
        result[role] = {
            "path": artifact.path,
            "sha256": artifact.sha256,
            "bytes": path.stat().st_size,
            "content_access": "HASH_ONLY_OPAQUE_PROVENANCE" if artifact.opaque else "HASH_VERIFIED_CANONICAL_INPUT",
        }
    return result


def normal(value: str) -> str:
    return " ".join(WORD.findall(value.lower()))


def frontmatter_value(text: str, key: str) -> str:
    header = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else text[:1600]
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)", header)
    return match.group(1).strip().strip("\"'") if match else ""


def validate_runtime(path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_PROMPTS, "Runtime prompt count drift")
    by_id: dict[str, dict[str, Any]] = {}
    hashes: set[str] = set()
    for index, row in enumerate(rows, 1):
        exact_keys(row, {"schema_version", "prompt_id", "prompt_sha256", "prompt"}, f"runtime[{index}]")
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", f"runtime[{index}]: schema drift")
        require(isinstance(row["prompt_id"], str) and row["prompt_id"], f"runtime[{index}]: prompt ID drift")
        require(isinstance(row["prompt"], str) and row["prompt"], f"runtime[{index}]: prompt text drift")
        require(row["prompt_sha256"] == text_sha256(row["prompt"]), f"runtime[{index}]: prompt hash drift")
        require(row["prompt_id"] not in by_id and row["prompt_sha256"] not in hashes, "Exact prompt identity/text duplicate")
        by_id[row["prompt_id"]] = row
        hashes.add(row["prompt_sha256"])
    return rows, by_id


def validate_sources(root: Path, path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], int]:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_SOURCES, "Source count drift")
    profiles: dict[str, dict[str, Any]] = {}
    paths: set[str] = set()
    total_bytes = 0
    for index, row in enumerate(rows, 1):
        exact_keys(row, {"path", "sha256", "bytes"}, f"source[{index}]")
        require(re.fullmatch(r"[0-9a-f]{64}", str(row["sha256"])) is not None, f"source[{index}]: invalid SHA")
        require(row["sha256"] not in profiles and row["path"] not in paths, "Exact source identity/path duplicate")
        source_path = root_path(root, row["path"], field=f"source[{index}].path")
        require(source_path.is_file(), f"source[{index}]: source file missing")
        require(source_path.stat().st_size == row["bytes"], f"source[{index}]: byte count drift")
        require(file_sha256(source_path) == row["sha256"], f"source[{index}]: SHA drift")
        text = source_path.read_text(encoding="utf-8", errors="replace")
        title = frontmatter_value(text, "name")
        if not title:
            heading = re.search(r"(?m)^#\s+(.+)$", text)
            title = heading.group(1).strip() if heading else ""
        description = frontmatter_value(text, "description")
        profiles[row["sha256"]] = {
            "source_sha256": row["sha256"],
            "source_path": row["path"],
            "title": title,
            "description": description,
            "normalised_full_sha256": text_sha256(normal(text)),
        }
        paths.add(row["path"])
        total_bytes += row["bytes"]
    require(total_bytes == EXPECTED_SOURCE_BYTES, "Source byte total drift")
    return rows, profiles, total_bytes


def validate_phase3_source_union(path: Path, source_hashes: set[str]) -> None:
    rows = read_jsonl(path)
    found: set[str] = set()
    for index, row in enumerate(rows, 1):
        value = row.get("canonical_source_sha256")
        require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None, f"phase3 source[{index}]: invalid SHA")
        require(value not in found, f"phase3 source[{index}]: duplicate SHA")
        found.add(value)
    require(len(rows) == EXPECTED_SOURCES and found == source_hashes, "Phase-3/final source scope drift")


def validate_dependency(path: Path, prompts: dict[str, dict[str, Any]], source_hashes: set[str]) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_PROMPTS, "Dependency coverage drift")
    by_prompt: dict[str, dict[str, Any]] = {}
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    lanes = Counter()
    for index, row in enumerate(rows, 1):
        exact_keys(
            row,
            {"schema_version", "prompt_id", "prompt_sha256", "dependency_group", "lane_id", "reporting_group", "dependency_anchor_source_sha256", "edge_policy"},
            f"dependency[{index}]",
        )
        require(row["schema_version"] == "rq2b-v7-dependency-ledger-v1", f"dependency[{index}]: schema drift")
        prompt = prompts.get(row["prompt_id"])
        require(prompt is not None and prompt["prompt_sha256"] == row["prompt_sha256"], f"dependency[{index}]: prompt binding drift")
        require(row["prompt_id"] not in by_prompt, f"dependency[{index}]: duplicate prompt")
        require(row["dependency_anchor_source_sha256"] in source_hashes, f"dependency[{index}]: source anchor outside scope")
        require(row["lane_id"] in {"A_PARENT_DELTA", "B_NC_FULL_UNION"}, f"dependency[{index}]: lane drift")
        by_prompt[row["prompt_id"]] = row
        by_group[row["dependency_group"]].append(row)
        lanes[row["lane_id"]] += 1
    require(set(by_prompt) == set(prompts), "Dependency prompt scope drift")
    require(len(by_group) == EXPECTED_DEPENDENCY_GROUPS, "Dependency-group count drift")
    require(lanes == {"A_PARENT_DELTA": EXPECTED_PARENT_PROMPTS, "B_NC_FULL_UNION": EXPECTED_NC_PROMPTS}, "Dependency lane count drift")
    mixed = {group for group, members in by_group.items() if len({row["lane_id"] for row in members}) > 1}
    require(mixed == EXPECTED_MIXED_GROUPS, "Mixed-lane dependency-group roster drift")
    return rows, dict(by_group)


def validate_authority_reports(root: Path, fixed: dict[str, FixedArtifact]) -> dict[str, Any]:
    final_freeze = read_json(root / fixed["final_freeze"].path)
    require(final_freeze.get("status") == "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION", "Final freeze status drift")
    require(final_freeze.get("counts", {}).get("frozen_final_library_groups") == EXPECTED_PROMPTS, "Final freeze prompt count drift")
    require(final_freeze.get("output_hashes", {}).get("final_library_prompt_manifest.jsonl") == PROMPT_MANIFEST_SHA256, "Final prompt-manifest binding drift")

    matrix = read_json(root / fixed["first_matrix_readiness"].path)
    require(matrix.get("status") == "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED", "First-matrix status drift")
    require(matrix.get("counts", {}).get("prompts") == EXPECTED_PROMPTS and matrix.get("counts", {}).get("sources") == EXPECTED_SOURCES, "First-matrix scope drift")
    require(matrix.get("bindings", {}).get("prompt_manifest_sha256") == PROMPT_MANIFEST_SHA256, "First-matrix prompt binding drift")
    require(matrix.get("bindings", {}).get("source_union_sha256") == SOURCE_UNION_SHA256, "First-matrix source binding drift")

    analysis = read_json(root / fixed["analysis_freeze"].path)
    require(analysis.get("status") == "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE", "Analysis-freeze status drift")
    require(analysis.get("counts", {}).get("prompts") == EXPECTED_PROMPTS and analysis.get("counts", {}).get("candidates") == EXPECTED_SOURCES, "Analysis-freeze scope drift")
    for role, filename in (("dependency_ledger", "dependency_ledger.jsonl"), ("exposure_ledger", "exposure_ledger.jsonl"), ("label_free_runtime", "label_free_query_runtime.jsonl")):
        artifact = analysis.get("artifacts", {}).get(filename, {})
        require(artifact.get("rows") == EXPECTED_PROMPTS and artifact.get("sha256") == fixed[role].sha256, f"Analysis-freeze binding drift: {filename}")
    require(analysis.get("label_isolation", {}).get("runtime_file") == "label_free_query_runtime.jsonl", "Analysis-freeze runtime isolation drift")
    return {"final_freeze_status": final_freeze["status"], "matrix_status": matrix["status"], "analysis_status": analysis["status"]}


def bound_path(bound: dict[str, str], suffix: str) -> str:
    matches = [path for path in bound if path.endswith(suffix)]
    require(len(matches) == 1, f"Phase-3 evidence path missing or ambiguous: {suffix}")
    return matches[0]


def grouped_count(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field)) for row in rows).items()))


def reaudit_phase3(root: Path, phase3_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    phase3 = read_json(phase3_path)
    require(phase3.get("status") == "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE", "Phase-3 closure status drift")
    expected_counts = {
        "historical_phase1_structural_progress_clusters": 304,
        "historical_phase3_preflight_nc_clusters": 304,
        "historical_phase3_preflight_nc_prompts": 875,
        "historical_preflight_canonical_candidates": 3810,
        "phase3_admitted_checkpoint_nc_clusters_for_phase4": 54,
        "phase3_admitted_nc_clusters_for_phase4": 297,
        "phase3_admitted_nc_prompts_for_phase4": 854,
        "phase3_admitted_source_native_nc_clusters_for_phase4": 243,
        "phase3_admitted_source_native_nc_prompts_for_phase4": 729,
        "phase3_cue_capped_deferred_nc_clusters": 2,
        "phase3_local_only_candidates_removed": 12,
        "phase3_local_origin_records_pruned": 21,
        "phase3_parent_v3_excluded_prompts": 9,
        "phase3_parent_v3_prompts_for_phase5": 372,
        "phase3_prospective_canonical_candidates_for_phase4": 3798,
        "phase3_remediated_active_nc_prompts_for_phase4": 4,
        "phase3_source_reuse_excluded_nc_clusters": 5,
    }
    require(phase3.get("counts") == expected_counts, "Phase-3 closure count drift")
    require(phase3.get("outputs", {}).get("candidate_source_union_for_phase4.jsonl") == SOURCE_UNION_SHA256, "Phase-3 source-union output drift")

    bound = phase3.get("bound_inputs")
    require(isinstance(bound, dict) and len(bound) == EXPECTED_PHASE3_BOUND_INPUTS, "Phase-3 bound-input roster drift")
    replay: list[dict[str, Any]] = []
    for path_value, expected_sha in sorted(bound.items()):
        path = root_path(root, path_value, field="phase3 bound input")
        require(path.is_file(), f"Restored Phase-3 evidence missing: {path_value}")
        actual = file_sha256(path)
        require(actual == expected_sha, f"Restored Phase-3 evidence hash drift: {path_value}")
        replay.append({"path": path_value, "sha256": actual, "hash_matches": True})

    output_replay: list[dict[str, Any]] = []
    for filename, expected_sha in sorted(phase3.get("outputs", {}).items()):
        path = phase3_path.parent / filename
        exists = path.is_file()
        actual = file_sha256(path) if exists else None
        require(not exists or actual == expected_sha, f"Phase-3 closure output hash drift: {filename}")
        output_replay.append({"path": relative(path, root), "expected_sha256": expected_sha, "actual_sha256": actual, "exists": exists, "hash_matches": exists and actual == expected_sha})
    require(len(output_replay) == 13, "Phase-3 closure output roster drift")
    require(all(row["hash_matches"] for row in output_replay), "Phase-3 closure outputs are not 13/13 present and hash-exact")

    cross_summary = read_json(root / bound_path(bound, "rq2b_nc_phase3_cross_cluster_reuse_adjudication_2026-09-05/summary.json"))
    cue1_summary = read_json(root / bound_path(bound, "rq2b_nc_phase3_cue_remediation_wave_001_closure_2026-09-05/summary.json"))
    cue2_summary = read_json(root / bound_path(bound, "rq2b_nc_phase3_cue_remediation_wave_002_closure_2026-09-05/summary.json"))
    cue3_summary = read_json(root / bound_path(bound, "rq2b_nc_phase3_cue_remediation_wave_003_closure_2026-09-05/summary.json"))
    parent_summary = read_json(root / bound_path(bound, "rq2b_nc_parent_v3_validity_audit_closure_2026-09-05/summary.json"))
    require(cross_summary.get("counts") == {"admission_blocked": 8, "blocked_or_unclear": 2, "duplicate_cluster": 2, "related_but_distinct": 4, "reviewed_exact_reuses": 8}, "Cross-reuse summary drift")
    require(cue1_summary.get("counts", {}).get("deferred_local_families") == 2 and cue1_summary.get("counts", {}).get("cue_gate_failed_after_capped_remediation") == 2, "Cue wave-1 closure drift")
    require(cue2_summary.get("counts", {}).get("cue_safe_after_resolution") == 3 and cue2_summary.get("counts", {}).get("reinstated_local_families") == 2, "Cue wave-2 closure drift")
    require(cue3_summary.get("counts", {}).get("cue_safe_after_resolution") == 1 and cue3_summary.get("counts", {}).get("reinstated_local_families") == 1, "Cue wave-3 closure drift")
    require(parent_summary.get("counts", {}).get("excluded_parent_prompt_ids") == 9 and parent_summary.get("counts", {}).get("blocked_parent_prompt_ids") == 0, "Parent validity closure drift")

    cross_rows = read_jsonl(root / bound_path(bound, "final_cross_cluster_dispositions.jsonl"))
    source_screen = read_jsonl(root / bound_path(bound, "source_relation_screen.jsonl"))
    cue_rows = read_jsonl(root / bound_path(bound, "final_prompt_cue_dispositions.jsonl"))
    relation_rows = read_jsonl(root / bound_path(bound, "final_prompt_relation_dispositions.jsonl"))
    require(len(cross_rows) == len(source_screen) == 8, "Cross-reuse row count drift")
    require(grouped_count(cross_rows, "phase3_admission_disposition") == {"BLOCKED_PENDING_EXCLUSION_OR_EXPLICIT_METHOD_DECISION": 8}, "Cross-reuse disposition drift")
    require(grouped_count(cue_rows, "final_cue_decision") == {"AVOIDABLE_IDENTITY_CUE": 14, "DECLARED_NECESSARY_CUE_STRATUM": 16}, "Cue decision roster drift")
    require(grouped_count(relation_rows, "final_relation_decision") == {"RELATED_BUT_DISTINCT": 60, "TRANSFORMED_DUPLICATE": 1}, "Prompt relation decision roster drift")

    return {
        "schema_version": READAUDIT_SCHEMA,
        "status": "PASS_RESTORED_PHASE3_BOUND_INPUTS_AND_CLOSURE_OUTPUTS_HASH_EXACT",
        "phase3_bound_inputs": len(replay),
        "phase3_bound_inputs_hash_matching": len(replay),
        "phase3_closure_outputs": len(output_replay),
        "phase3_closure_outputs_present_and_hash_matching": sum(row["hash_matches"] for row in output_replay),
        "phase3_closure_outputs_missing": sum(not row["exists"] for row in output_replay),
        "mechanical_findings": {
            "cross_cluster_exact_source_reuse_rows": 8,
            "source_reuse_clusters_excluded_by_phase3_closure": 5,
            "cue_findings_adjudicated": 30,
            "cue_capped_families_deferred": 2,
            "cue_remediated_prompts_reinstated": 4,
            "parent_validity_prompts_excluded": 9,
            "prompt_relation_candidates_adjudicated": 61,
            "prompt_relation_related_but_distinct": 60,
            "prompt_relation_transformed_duplicate": 1,
        },
        "sufficiency_boundary": "The restored chain proves all 21 closure-bound inputs and all 13 closure outputs at their recorded hashes. It does not turn the original lexical candidate screen into exhaustive final-scope semantic-near-copy evidence, and it does not explicitly disposition current mixed-lane dependency components.",
        "bound_input_replay": replay,
        "closure_output_replay": output_replay,
        "labels_results_metrics_content_read": False,
    }, replay


def prompt_relation_candidates(rows: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any], dict[str, float]]]:
    profiles: list[tuple[str, set[str], set[tuple[str, ...]]]] = []
    for row in rows:
        raw = normal(row["prompt"])
        words = [word for word in WORD.findall(raw) if word not in STOPWORDS]
        grams = {tuple(words[index:index + 4]) for index in range(max(0, len(words) - 3))}
        profiles.append((raw, set(words), grams))
    found: list[tuple[dict[str, Any], dict[str, Any], dict[str, float]]] = []
    for left, right in itertools.combinations(range(len(rows)), 2):
        text_a, words_a, grams_a = profiles[left]
        text_b, words_b, grams_b = profiles[right]
        if text_a == text_b or text_a in text_b or text_b in text_a:
            jaccard = sequence = coverage = 1.0
        else:
            jaccard = len(words_a & words_b) / len(words_a | words_b) if words_a | words_b else 0.0
            coverage = len(grams_a & grams_b) / min(len(grams_a), len(grams_b)) if grams_a and grams_b else 0.0
            if jaccard < 0.52 and coverage < 0.50:
                continue
            sequence = difflib.SequenceMatcher(None, text_a, text_b, autojunk=False).ratio()
            if not ((jaccard >= 0.52 and sequence >= 0.66) or coverage >= 0.50 or sequence >= 0.84):
                continue
        found.append((rows[left], rows[right], {"content_token_jaccard": round(jaccard, 6), "character_sequence_ratio": round(sequence, 6), "four_gram_coverage_shorter": round(coverage, 6)}))
    return sorted(found, key=lambda item: tuple(sorted((item[0]["prompt_id"], item[1]["prompt_id"]))))


def build_prompt_relation_packets(runtime_rows: list[dict[str, Any]], dependency_by_prompt: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    packets = []
    for index, (left, right, signals) in enumerate(prompt_relation_candidates(runtime_rows), 1):
        members = []
        for row in sorted((left, right), key=lambda item: item["prompt_id"]):
            dependency = dependency_by_prompt[row["prompt_id"]]
            members.append({
                "prompt_id": row["prompt_id"],
                "prompt_sha256": row["prompt_sha256"],
                "prompt": row["prompt"],
                "lane_id": dependency["lane_id"],
                "reporting_group": dependency["reporting_group"],
                "dependency_group": dependency["dependency_group"],
            })
        packets.append({
            "schema_version": PACKET_SCHEMA,
            "packet_id": f"P8-PRREL-{index:04d}",
            "gate": "semantic_near_copy",
            "signal": "HIGH_SPECIFICITY_LEXICAL_PROMPT_RELATION_CANDIDATE",
            "members": members,
            "mechanical_scores": signals,
            "review_boundary": "Adjudicate operational-instance duplication, transformed near-copy, and split leakage from these prompt texts only. Do not use hidden identity, label, acceptable-set, retrieval, or metric data.",
            "required_return": {"packet_id": f"P8-PRREL-{index:04d}", "decision": "RELATED_BUT_DISTINCT | SPLIT_LEAKAGE | TRANSFORMED_DUPLICATE | BLOCKED_OR_UNCLEAR", "rationale": "", "source_anchors": []},
        })
    return packets


def build_mixed_lane_packets(
    by_group: dict[str, list[dict[str, Any]]],
    prompts: dict[str, dict[str, Any]],
    profiles: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    packets = []
    for index, group in enumerate(sorted(EXPECTED_MIXED_GROUPS), 1):
        members = []
        for dependency in sorted(by_group[group], key=lambda row: row["prompt_id"]):
            prompt = prompts[dependency["prompt_id"]]
            members.append({
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
                "prompt": prompt["prompt"],
                "lane_id": dependency["lane_id"],
                "reporting_group": dependency["reporting_group"],
                "dependency_anchor_source_sha256": dependency["dependency_anchor_source_sha256"],
                "edge_policy": dependency["edge_policy"],
            })
        packet_id = f"P8-SPLIT-MIXED-{index:03d}"
        anchors = sorted({member["dependency_anchor_source_sha256"] for member in members})
        packets.append({
            "schema_version": PACKET_SCHEMA,
            "packet_id": packet_id,
            "gate": "split",
            "signal": "DEPENDENCY_COMPONENT_SPANS_PARENT_AND_NC_REPORTING_LANES",
            "dependency_group": group,
            "members": members,
            "source_context": [
                {key: profiles[source_hash][key] for key in ("source_sha256", "source_path", "title", "description")}
                for source_hash in anchors
            ],
            "review_boundary": "Decide whether this cross-lane component is a legitimate pre-outcome shared-source dependency that must remain intact for resampling, or unresolved split leakage. Review prompt and cited source bytes only.",
            "required_return": {"packet_id": packet_id, "decision": "DEPENDENCY_BOUND_NOT_SPLIT_LEAKAGE | SPLIT_LEAKAGE | BLOCKED_OR_UNCLEAR", "rationale": "", "source_anchors": []},
        })
    return packets


def build_cue_packets(runtime_rows: list[dict[str, Any]], profiles: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    titles: dict[str, list[str]] = defaultdict(list)
    for source_hash, profile in profiles.items():
        value = normal(profile["title"])
        if len(value.split()) >= 2 and len(value) >= 6:
            titles[value].append(source_hash)
    patterns = {
        "REPOSITORY_URL_LITERAL": re.compile(r"github\.com", re.IGNORECASE),
        "BENCHMARK_OR_SKILL_PATH_LITERAL": re.compile(r"(?:rq2b|rq1b|/skills/|sha256)", re.IGNORECASE),
        "LITERAL_SHA256": re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE),
        "SKILL_FILE_ARTIFACT_LITERAL": re.compile(r"skill\.md", re.IGNORECASE),
    }
    packets = []
    for row in runtime_rows:
        prompt_normal = normal(row["prompt"])
        findings: list[dict[str, Any]] = []
        for title in sorted(value for value in titles if value in prompt_normal):
            findings.append({"signal": "ANY_LIBRARY_SOURCE_TITLE_PHRASE", "matched_text": title, "matching_source_sha256": sorted(titles[title])})
        for signal, pattern in patterns.items():
            if pattern.search(row["prompt"]):
                findings.append({"signal": signal, "matched_text": None, "matching_source_sha256": []})
        if not findings:
            continue
        packet_id = f"P8-CUE-{len(packets) + 1:04d}"
        packets.append({
            "schema_version": PACKET_SCHEMA,
            "packet_id": packet_id,
            "gate": "cue",
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "prompt": row["prompt"],
            "findings": findings,
            "review_boundary": "Classify only whether each visible phrase is an avoidable identity cue, a necessary task condition, or not a cue. This any-source-title screen is target-blind and does not identify the intended source.",
            "required_return": {"packet_id": packet_id, "decision": "AVOIDABLE_IDENTITY_CUE | NECESSARY_TASK_CONDITION | NOT_A_CUE | BLOCKED_OR_UNCLEAR", "rationale": "", "source_anchors": []},
        })
    return packets


def build_source_relation_packets(profiles: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    normalised_full: dict[str, list[str]] = defaultdict(list)
    for source_hash, profile in profiles.items():
        for signal, field in (("NORMALISED_TITLE_COLLISION", "title"), ("NORMALISED_DESCRIPTION_COLLISION", "description")):
            value = normal(profile[field])
            if value:
                groups[(signal, value)].append(source_hash)
        normalised_full[profile["normalised_full_sha256"]].append(source_hash)
    candidates: list[tuple[str, str, list[str]]] = []
    for (signal, value), members in groups.items():
        if len(members) > 1:
            candidates.append((signal, text_sha256(value), sorted(members)))
    exact_normalised_groups = 0
    for value_hash, members in normalised_full.items():
        if len(members) > 1:
            exact_normalised_groups += 1
            candidates.append(("NORMALISED_FULL_SOURCE_MATCH", value_hash, sorted(members)))
    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    merged: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for signal, value_hash, members in candidates:
        merged[tuple(members)].append({"signal": signal, "normalised_value_sha256": value_hash})
    packets = []
    for index, (member_tuple, signals) in enumerate(sorted(merged.items()), 1):
        packet_id = f"P8-SRCREL-{index:04d}"
        packets.append({
            "schema_version": PACKET_SCHEMA,
            "packet_id": packet_id,
            "gates": ["duplication", "semantic_near_copy"],
            "signals": sorted(signals, key=lambda item: (item["signal"], item["normalised_value_sha256"])),
            "members": [{key: profiles[source_hash][key] for key in ("source_sha256", "source_path", "title", "description")} for source_hash in member_tuple],
            "review_boundary": "Review only the cited source bytes and provenance paths. Decide whether these are aliases, forks, transformed copies, related-but-distinct skills, or unclear.",
            "required_return": {"packet_id": packet_id, "decision": "ALIAS_OR_FORK | TRANSFORMED_COPY | RELATED_BUT_DISTINCT | BLOCKED_OR_UNCLEAR", "rationale": "", "source_anchors": []},
        })
    return packets, exact_normalised_groups


def assert_packets_target_blind(packet_sets: dict[str, list[dict[str, Any]]]) -> None:
    prohibited_keys = {"target", "gold", "acceptable_set", "selector_result", "metric", "outcome"}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            require(not (set(value) & prohibited_keys), f"Review packet contains prohibited key: {sorted(set(value) & prohibited_keys)}")
            for nested in value.values():
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)

    for rows in packet_sets.values():
        walk(rows)


def audit_canonical(root: Path, fixed: dict[str, FixedArtifact] | None = None) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    fixed = FIXED_ARTIFACTS if fixed is None else fixed
    bindings = validate_fixed(root, fixed)
    authorities = validate_authority_reports(root, fixed)
    runtime_rows, prompts = validate_runtime(root / fixed["label_free_runtime"].path)
    source_rows, profiles, source_bytes = validate_sources(root, root / fixed["source_manifest"].path)
    source_hashes = set(profiles)
    validate_phase3_source_union(root / fixed["phase3_source_union"].path, source_hashes)
    dependency_rows, by_group = validate_dependency(root / fixed["dependency_ledger"].path, prompts, source_hashes)
    dependency_by_prompt = {row["prompt_id"]: row for row in dependency_rows}
    phase3_reaudit, _ = reaudit_phase3(root, root / fixed["phase3_closure"].path)

    prompt_packets = build_prompt_relation_packets(runtime_rows, dependency_by_prompt)
    mixed_packets = build_mixed_lane_packets(by_group, prompts, profiles)
    cue_packets = build_cue_packets(runtime_rows, profiles)
    source_packets, normalised_source_duplicate_groups = build_source_relation_packets(profiles)
    packet_sets = {
        "mixed_lane_split_review_packets.jsonl": mixed_packets,
        "prompt_relation_review_packets.jsonl": prompt_packets,
        "cue_review_packets.jsonl": cue_packets,
        "source_relation_review_packets.jsonl": source_packets,
    }
    assert_packets_target_blind(packet_sets)

    gates = [
        {
            "gate": "split",
            "status": "BLOCKED_PENDING_MIXED_LANE_AND_PROMPT_RELATION_DISPOSITIONS",
            "mechanically_established": [f"All {EXPECTED_PROMPTS} prompt identities and {EXPECTED_DEPENDENCY_GROUPS} dependency components replay.", f"Exactly {len(mixed_packets)} dependency components span parent and NC lanes."],
            "blockers": ["No final disposition says whether each mixed-lane component is legitimate shared-source dependence or split leakage.", "Lexically nominated final-scope prompt relations also require disposition."],
        },
        {
            "gate": "cue",
            "status": "BLOCKED_PENDING_FINAL_SCOPE_TARGET_BLIND_CUE_REVIEW",
            "mechanically_established": ["The restored Phase-3 chain proves its 30 flagged cue dispositions and bounded remediations/exclusions.", f"The current target-blind replay nominates {len(cue_packets)} final-scope prompts by any-source-title or literal artifact/path signals."],
            "blockers": ["The Phase-3 closure does not bind the original cue-screen inventory, so negative-screen coverage cannot be replayed from the restored set.", "A final method decision must state whether target-blind any-source screening satisfies the target-title contract without exposing hidden identity mappings."],
        },
        {
            "gate": "duplication",
            "status": "BLOCKED_PENDING_SOURCE_RELATION_DISPOSITIONS_AND_COVERAGE_DECISION",
            "mechanically_established": ["Exact source SHA/path duplicates and exact prompt ID/text duplicates are zero.", f"Normalised complete-source duplicates are {normalised_source_duplicate_groups}; metadata collisions nominate {len(source_packets)} source review packets."],
            "blockers": ["Exact and metadata screens do not rule out aliases, forks, or transformed copies.", "A final source-scope semantic coverage decision and all nominated dispositions are absent."],
        },
        {
            "gate": "semantic_near_copy",
            "status": "BLOCKED_PENDING_FINAL_PROMPT_AND_SOURCE_SEMANTIC_DISPOSITIONS",
            "mechanically_established": [f"The final prompt lexical replay nominates {len(prompt_packets)} pairs.", "The restored Phase-3 evidence verifies 61 earlier candidate dispositions and their downstream exclusions/remediations."],
            "blockers": ["The original Phase-3 QA explicitly limits a negative lexical screen: it is not proof that no semantic near-copy exists.", "The restored closure does not bind the original prompt relation screen/packet identity map, and no exhaustive final 1,077/3,798 semantic receipt exists."],
        },
        {
            "gate": "coverage",
            "status": "MECHANICALLY_REPLAYED_PASS_CANDIDATE_NOT_PHASE8_PASS",
            "mechanically_established": [f"{len(runtime_rows)} unique label-free prompts replay.", f"{len(source_rows)} unique source paths and SHA-256 identities replay over {source_bytes} bytes.", f"The restored Phase-3 evidence chain is {phase3_reaudit['phase3_bound_inputs_hash_matching']}/{phase3_reaudit['phase3_bound_inputs']} hash-exact.", "Final freeze, analysis freeze, dependency scope, source union and exclusion scope are hash-bound."],
            "blockers": ["The official Phase-8 quality package remains blocked until all four semantic gates have final zero-unresolved receipts."],
        },
    ]
    docket = {
        "schema_version": DOCKET_SCHEMA,
        "status": BLOCKED_STATUS,
        "formal_execution_ready": False,
        "quality_pass_reports_emitted": 0,
        "labels_results_metrics_content_read": False,
        "selector_provider_model_metric_runs": 0,
        "scope": {"prompts": EXPECTED_PROMPTS, "sources": EXPECTED_SOURCES, "source_bytes": source_bytes, "source_union_sha256": SOURCE_UNION_SHA256, "prompt_manifest_sha256": PROMPT_MANIFEST_SHA256},
        "authorities": authorities,
        "fixed_artifacts": bindings,
        "restored_phase3_evidence_assessment": phase3_reaudit,
        "packet_counts": {name: len(rows) for name, rows in sorted(packet_sets.items())},
        "gates": gates,
        "decision_rule": "Do not create rq2b-v7-phase8-quality-gate-v2 PASS reports until every packet has a versioned final return, all unresolved findings are zero, and an explicit final-scope semantic coverage decision is hash-bound.",
        "boundary": "These packets nominate bounded source/prompt-only review work. They are not semantic verdicts, labels, retrieval results, metrics, or experiment authorisation.",
    }
    decision_template = {
        "schema_version": DECISION_TEMPLATE_SCHEMA,
        "status": "PENDING_REVIEW_NOT_A_QUALITY_PASS",
        "execution_authorised": False,
        "packet_files": {name: {"rows": len(rows), "sha256": hashlib.sha256(rows_bytes(rows)).hexdigest()} for name, rows in sorted(packet_sets.items())},
        "gate_decisions": {row["gate"]: {"status": "PENDING", "unresolved_findings": None, "final_receipt_path": None, "final_receipt_sha256": None} for row in gates if row["gate"] != "coverage"},
        "semantic_coverage_decision": {"status": "PENDING", "scope": "1077 prompts and 3798 complete sources", "rationale": None, "authorised_reviewer_or_method_gate": None},
        "coverage_gate": {"status": "MECHANICALLY_REPLAYED_PENDING_SEMANTIC_CLOSURE", "unresolved_findings": 0},
        "boundary": "Template only. Filling a path or hash does not create PASS unless a future fail-closed closure builder verifies the complete receipt and zero unresolved findings.",
    }
    return docket, packet_sets, decision_template


def render_readme(docket: dict[str, Any]) -> str:
    counts = docket["packet_counts"]
    return f"""# V7 Phase-8 target-blind quality review docket v3

Status: `{BLOCKED_STATUS}`.

The restored Phase-3 evidence is complete and exact: all 21 closure-bound
inputs (the 20 restored artifacts plus the master SOP) and all 13 closure
outputs replay at their recorded SHA-256 values. This repairs the missing
evidence gaps recorded by the immutable v1 and pre-restoration v2 blocking
snapshots without overwriting either snapshot.

The evidence still does not justify the five official Phase-8 PASS reports.
The original semantic-QA method explicitly states that a negative lexical
screen is not proof that no semantic near-copy exists, its prompt relation
screen/packet identity map is not closure-bound, and the six final mixed-lane
dependency components have no explicit final split disposition.

This package therefore emits zero quality PASS reports and prepares only
source/prompt-only, target-blind review inputs:

- {counts['mixed_lane_split_review_packets.jsonl']} mixed-lane split packets;
- {counts['prompt_relation_review_packets.jsonl']} final-scope prompt relation packets;
- {counts['cue_review_packets.jsonl']} final-scope cue packets; and
- {counts['source_relation_review_packets.jsonl']} source metadata/normalisation relation packets.

The screens are candidate generators, not semantic verdicts. A final closure
still needs versioned returns for every packet and an explicit decision that
the semantic review coverage is adequate for all 1,077 prompts and 3,798
complete sources. `quality_decision_template.json` remains PENDING and cannot
authorise execution.

No final prompt-label manifest content, exposure-outcome content, selector
output, acceptable set, metric, provider, model, retrieval, or reranking run is
read or executed. The final prompt manifest and exposure ledger are hash-only
opaque bindings.

Audit without writing:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_review_docket_v3.py --audit
```

Verify the immutable package:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_review_docket_v3.py \
  --verify --output-dir skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_quality_review_docket_2026_09_09_v3
```
"""


def expected_files(root: Path, *, builder_path: Path | None = None) -> dict[str, bytes]:
    docket, packet_sets, decision_template = audit_canonical(root)
    implementation = (builder_path or Path(__file__)).resolve()
    try:
        implementation.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Builder implementation must be inside repository root") from error
    files = {
        "blocking_docket.json": canonical_bytes(docket),
        "phase3_evidence_reaudit.json": canonical_bytes(docket["restored_phase3_evidence_assessment"]),
        "quality_decision_template.json": canonical_bytes(decision_template),
        "README.md": render_readme(docket).encode("utf-8"),
        **{name: rows_bytes(rows) for name, rows in packet_sets.items()},
    }
    integrity = {
        "schema_version": INTEGRITY_SCHEMA,
        "status": BLOCKED_STATUS,
        "formal_execution_ready": False,
        "quality_pass_reports_emitted": 0,
        "builder": {"path": relative(implementation, root), "sha256": file_sha256(implementation), "version": BUILDER_VERSION},
        "artifacts": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for name, data in sorted(files.items())},
        "external_activity": {"network_calls": 0, "selector_runs": 0, "provider_calls": 0, "model_forwards": 0, "retrieval_or_reranking_runs": 0, "metric_runs": 0},
    }
    files["integrity_report.json"] = canonical_bytes(integrity)
    return files


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def materialize(root: Path, output_dir: Path, *, builder_path: Path | None = None) -> dict[str, Any]:
    require(not output_dir.exists(), f"Refusing to overwrite output: {output_dir}")
    files = expected_files(root, builder_path=builder_path)
    staging = output_dir.parent / f".{output_dir.name}.staging-{os.getpid()}"
    require(not staging.exists(), f"Stale staging directory: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        write_new(staging / name, data)
    staging.rename(output_dir)
    return {"status": BLOCKED_STATUS, "output": relative(output_dir, root), "files": len(files), "quality_pass_reports_emitted": 0, "formal_execution_ready": False}


def verify(root: Path, output_dir: Path, *, builder_path: Path | None = None) -> dict[str, Any]:
    require(output_dir.is_dir(), "Review docket package is missing")
    expected = expected_files(root, builder_path=builder_path)
    require({path.name for path in output_dir.iterdir()} == set(expected), "Review docket package file-set drift")
    for name, data in expected.items():
        require((output_dir / name).read_bytes() == data, f"Review docket package drift: {name}")
    return {"status": "PASS_EXACT_REPLAY_OF_BLOCKING_REVIEW_DOCKET_NOT_A_QUALITY_PASS", "output": relative(output_dir, root), "quality_pass_reports_emitted": 0, "formal_execution_ready": False}


def self_test() -> dict[str, Any]:
    require("PASS" not in BLOCKED_STATUS, "Blocked status must not masquerade as PASS")
    require(len(EXPECTED_MIXED_GROUPS) == 6, "Mixed-lane group roster drift")
    require(PACKET_SCHEMA.endswith("-v3"), "Packet schema drift")
    return {"status": "PASS_SYNTHETIC_DOCKET_SELF_TEST_NO_QUALITY_PASS", "quality_pass_reports_emitted": 0, "formal_execution_ready": False, "network_calls": 0, "selector_runs": 0, "model_forwards": 0, "metric_runs": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--audit", action="store_true")
    mode.add_argument("--materialize", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.self_test:
        result = self_test()
    elif args.audit:
        docket, _, _ = audit_canonical(root)
        result = docket
    else:
        require(args.output_dir is not None, "--output-dir is required")
        output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        output = output.resolve()
        try:
            output.relative_to(root)
        except ValueError as error:
            raise ValueError("Output directory must be inside repository root") from error
        result = materialize(root, output) if args.materialize else verify(root, output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
