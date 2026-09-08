#!/usr/bin/env python3
"""Prepare source portability and a label-free matrix; never run a selector.

--source-workspace restores only missing, frozen-ledger-bound Markdown files.
--verify is read-only and replays the resulting preparation package.
This is not a representation materialiser or experiment-authorisation seal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path("skill_benchmark/rq2b_naturalistic_confusability/manifests")
FREEZE = BASE / "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1"
PATHS = BASE / "rq2b_nc_phase4_navigation_profiles_2026-09-05/source_path_resolution_ledger.jsonl"
UNION = BASE / "rq2b_nc_phase3_admission_closure_300plus_2026-09-05/candidate_source_union_for_phase4.jsonl"
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1")
EXPECTED_PROMPTS = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
EXPECTED_UNION = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
SECRETS = re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|AKIA[0-9A-Z]{16}|sk-proj-[A-Za-z0-9_-]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)")
PLACEHOLDER = b"-----BEGIN PRIVATE KEY-----\n    ...\n    -----END PRIVATE KEY-----"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def jsonl_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def safe_path(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if not rel.parts or rel.is_absolute() or ".." in rel.parts or rel.parts[0] != "skill_benchmark" or rel.suffix != ".md":
        raise ValueError(f"source path outside frozen Markdown scope: {relative}")
    result = root / rel
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"source symlink escapes workspace: {relative}")
    return result


def build(source_workspace: Path | None, restore: bool) -> tuple[dict[str, bytes], int]:
    prompt_path = ROOT / FREEZE / "final_library_prompt_manifest.jsonl"
    if sha(prompt_path.read_bytes()) != EXPECTED_PROMPTS or sha((ROOT / UNION).read_bytes()) != EXPECTED_UNION:
        raise ValueError("frozen prompt/source manifest hash mismatch")
    prompts = rows(prompt_path)
    union = rows(ROOT / UNION)
    path_rows = rows(ROOT / PATHS)
    expected_sources = {row["canonical_source_sha256"] for row in union}
    if len(prompts) != 1077 or len({row["prompt_id"] for row in prompts}) != 1077:
        raise ValueError("prompt coverage mismatch")
    if len(union) != 3798 or len(expected_sources) != 3798 or len(path_rows) != 3798:
        raise ValueError("source coverage mismatch")
    if {row["canonical_source_sha256"] for row in path_rows} != expected_sources:
        raise ValueError("path-ledger source coverage mismatch")
    selected_paths = [row["selected_workspace_relative_path"] for row in path_rows]
    if len(set(selected_paths)) != len(selected_paths):
        raise ValueError("source path collision")

    # Validate the complete bounded source intake before writing any source.
    intake = []
    placeholder_paths = []
    for row in sorted(path_rows, key=lambda item: item["canonical_source_sha256"]):
        relative = row["selected_workspace_relative_path"]
        dest = safe_path(ROOT, relative)
        src = dest if dest.is_file() else safe_path(source_workspace, relative) if source_workspace else dest
        data = src.read_bytes()
        if sha(data) != row["canonical_source_sha256"]:
            raise ValueError(f"source hash mismatch: {relative}")
        if SECRETS.search(data):
            if PLACEHOLDER in data and not SECRETS.search(data.replace(PLACEHOLDER, b"DOCUMENTED_PRIVATE_KEY_PLACEHOLDER")):
                placeholder_paths.append(relative)
            else:
                raise ValueError(f"credential-pattern review required; value not printed: {relative}")
        intake.append((dest, data, relative, row["canonical_source_sha256"]))
    restored = 0
    for dest, data, relative, expected in intake:
        if not dest.exists():
            if not restore:
                raise ValueError(f"source missing from checkout: {relative}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("xb") as handle:
                handle.write(data)
            restored += 1
        if sha(dest.read_bytes()) != expected:
            raise ValueError(f"destination hash mismatch: {relative}")

    common = {"scope": "V7_1077_FROZEN", "prompt_manifest_sha256": EXPECTED_PROMPTS,
              "source_union_sha256": EXPECTED_UNION, "query_count": 1077,
              "runtime_rerank_k": 20, "audit_main_k": 6, "execution_authorised": False}
    core = []
    cell = 0
    for rep in ["I1-discovery", "I2-original", "I3C-fielded", "I3-flat"]:
        for retriever in ["BM25", "Qwen-text-embedding-v4", "SkillRouter-Embedding-0.6B"]:
            cell += 1
            for reranker in ["NONE", "Qwen-qwen3-rerank", "SkillRouter-Reranker-0.6B"]:
                suffix = {"NONE": "G0", "Qwen-qwen3-rerank": "GQ", "SkillRouter-Reranker-0.6B": "GS"}[reranker]
                core.append({**common, "condition_id": f"B{cell:02d}-{suffix}", "phase": "FIRST_CORE_MATRIX",
                             "representation": rep, "retriever": retriever, "reranker": reranker,
                             "persisted_candidate_source": f"B{cell:02d}"})
    bridge = []
    for label, rep in [(1, "I1-discovery"), (3, "I3C-fielded"), (4, "I3-flat")]:
        for suffix, reranker in [("Q", "Qwen-qwen3-rerank"), ("S", "SkillRouter-Reranker-0.6B")]:
            bridge.append({**common, "condition_id": f"C{label}-{suffix}", "phase": "FIXED_CANDIDATE_BRIDGE",
                           "representation": rep, "retriever": "Qwen-text-embedding-v4",
                           "reranker": reranker, "persisted_candidate_source": "B05"})
    source_manifest = [{"path": relative, "sha256": expected, "bytes": len(data)} for _, data, relative, expected in intake]
    report = {
        "status": "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED",
        "counts": {"sources": 3798, "prompts": 1077, "labels": dict(Counter(row["final_label_type"] for row in prompts)),
                   "lanes": dict(Counter(row["lane_id"] for row in prompts)),
                   "strata": dict(Counter(row["reporting_stratum"] for row in prompts)),
                   "core_configurations": len(core), "new_bridge_configurations": len(bridge),
                   "source_bytes": sum(len(data) for _, data, _, _ in intake)},
        "bindings": {"prompt_manifest_sha256": EXPECTED_PROMPTS, "source_union_sha256": EXPECTED_UNION,
                     "path_resolution_ledger_sha256": sha((ROOT / PATHS).read_bytes()),
                     "acceptable_freeze_report_sha256": sha((ROOT / FREEZE / "integrity_report.json").read_bytes()),
                     "preparation_script_sha256": sha(Path(__file__).read_bytes())},
        "credential_pattern_screen": {"unresolved_flags": 0, "documented_ellipsis_private_key_placeholders": placeholder_paths,
                                      "limitation": "Narrow pattern screen, not a guarantee that all sensitive content is absent."},
        "remaining_gates": ["V7-complete I1/I2/I3C/I3-flat materialisation and semantic QA",
                            "final execution root, model/chunking/instruction/analysis hashes",
                            "grouped dependence/exposure and cost preflight", "payload-specific compute and transfer authorisation"],
        "scope_boundary": "No retrieval, embedding, reranking, new adequacy judging or result metrics. V7 labels unchanged; 528 successor deferred.",
        "source_scope": "Exact frozen primary Markdown bytes only. This does not independently replay every upstream licence or auxiliary-resource byte.",
    }
    outputs = {"first_matrix_conditions.jsonl": jsonl_bytes(core), "fixed_candidate_bridge_conditions.jsonl": jsonl_bytes(bridge),
               "source_manifest.jsonl": jsonl_bytes(source_manifest),
               "source_paths.txt": ("\n".join(row["path"] for row in source_manifest) + "\n").encode()}
    report["output_sha256"] = {name: sha(data) for name, data in outputs.items()}
    outputs["readiness_report.json"] = json_bytes(report)
    return outputs, restored


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-workspace", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify and args.source_workspace:
        parser.error("verification must use only this checkout")
    output = ROOT / OUTPUT
    if not args.verify and output.exists():
        raise SystemExit("refusing to overwrite preparation package")
    outputs, restored = build(args.source_workspace, restore=not args.verify)
    if args.verify:
        for name, expected in outputs.items():
            if (output / name).read_bytes() != expected:
                raise SystemExit(f"preparation replay mismatch: {name}")
    else:
        output.mkdir(parents=True)
        for name, data in outputs.items():
            with (output / name).open("xb") as handle:
                handle.write(data)
    print(json.dumps({"status": "PASS_PREPARATION_REPLAY" if args.verify else "PASS_PREPARATION_CREATED",
                      "sources_restored_without_overwrite": restored, "source_count": 3798,
                      "core_configurations": 36, "new_bridge_configurations": 6,
                      "formal_execution_ready": False}, sort_keys=True))


if __name__ == "__main__":
    main()
