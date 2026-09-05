#!/usr/bin/env python3
"""Build and validate the zero-network, metadata-only RQ2b B0G-M artefacts.

This tool deliberately consumes only prompt/source identity metadata and legacy
annotation files. It never reads a skill body, representation, model output,
or prompt text. It does not decide semantic suitability.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


VERSION_ID = "rq2b-full-library-v1-2026-08-02"
SCRIPT_RELATIVE_PATH = "skill_benchmark/scripts/build_rq2b_b0gm_reconciliation.py"
FROZEN_ROOT = Path("skill_benchmark/rq2b_full_library") / VERSION_ID
PREFLIGHT_PROMPTS = Path("skill_benchmark/outputs/rq2b/preflight/prompt_inventory.jsonl")
PREFLIGHT_SOURCES = Path("skill_benchmark/outputs/rq2b/preflight/source_inventory.jsonl")
FROZEN_SOURCE_MANIFEST = FROZEN_ROOT / "source_manifest.jsonl"
FROZEN_VERSION_MANIFEST = FROZEN_ROOT / "manifest.json"
FROZEN_FILE_MANIFEST = FROZEN_ROOT / "file_manifest.jsonl"
ANNOTATION_FILES = {
    "controlled": Path("skill_benchmark/annotations/acceptable_alternatives.json"),
    "public_gold": Path("skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
    "stress": Path("skill_benchmark/annotations/low_information_acceptables.json"),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"Blank JSONL line: {relative(path, repo_root())}:{line_number}")
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"Non-object JSONL row: {relative(path, repo_root())}:{line_number}")
        rows.append(payload)
    return rows


def write_json_new(path: Path, payload: Any) -> None:
    if path.exists():
        raise ValueError(f"Refusing to overwrite existing output: {relative(path, repo_root())}")
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    if path.exists():
        raise ValueError(f"Refusing to overwrite existing output: {relative(path, repo_root())}")
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
            count += 1
    return count


def require_string_list(row: dict[str, Any], field: str, prompt_id: str) -> list[str]:
    value = row.get(field, [])
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"Invalid {field} list for {prompt_id}")
    if len(value) != len(set(value)):
        raise ValueError(f"Duplicate {field} value for {prompt_id}")
    return list(value)


def load_annotations(root: Path) -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, dict[str, str]]]:
    annotations: dict[str, dict[str, dict[str, Any]]] = {}
    provenance: dict[str, dict[str, str]] = {}
    for stratum, relative_path in ANNOTATION_FILES.items():
        path = root / relative_path
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"Annotation file must be an object: {relative_path}")
        typed: dict[str, dict[str, Any]] = {}
        for prompt_id, value in payload.items():
            if not isinstance(prompt_id, str) or not isinstance(value, dict):
                raise ValueError(f"Invalid annotation entry in {relative_path}")
            acceptable = value.get("acceptable", [])
            borderline = value.get("borderline", [])
            if not isinstance(acceptable, list) or not isinstance(borderline, list):
                raise ValueError(f"Invalid annotation list in {relative_path}:{prompt_id}")
            if any(not isinstance(skill_id, str) or not skill_id for skill_id in acceptable + borderline):
                raise ValueError(f"Invalid annotation skill ID in {relative_path}:{prompt_id}")
            if len(acceptable) != len(set(acceptable)) or len(borderline) != len(set(borderline)):
                raise ValueError(f"Duplicate annotation skill ID in {relative_path}:{prompt_id}")
            typed[prompt_id] = {"acceptable": sorted(acceptable), "borderline": sorted(borderline)}
        annotations[stratum] = typed
        provenance[stratum] = {
            "path": relative_path.as_posix(),
            "sha256": sha256_file(path),
        }
    return annotations, provenance


def build(root: Path, output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"Output directory already exists: {relative(output_dir, root)}")
    prompts_path = root / PREFLIGHT_PROMPTS
    preflight_sources_path = root / PREFLIGHT_SOURCES
    frozen_sources_path = root / FROZEN_SOURCE_MANIFEST
    frozen_version_path = root / FROZEN_VERSION_MANIFEST
    frozen_file_manifest_path = root / FROZEN_FILE_MANIFEST
    for path in (prompts_path, preflight_sources_path, frozen_sources_path, frozen_version_path, frozen_file_manifest_path):
        if not path.exists():
            raise ValueError(f"Required input missing: {relative(path, root)}")

    prompts = read_jsonl(prompts_path)
    preflight_sources = read_jsonl(preflight_sources_path)
    frozen_sources = read_jsonl(frozen_sources_path)
    frozen_file_manifest = read_jsonl(frozen_file_manifest_path)
    frozen_version = read_json(frozen_version_path)
    generated_artifacts = frozen_version.get("generated_artifacts")
    if not isinstance(generated_artifacts, dict):
        raise ValueError("Frozen version manifest lacks generated artifacts")
    frozen_file_binding = generated_artifacts.get("file_manifest")
    if not isinstance(frozen_file_binding, dict):
        raise ValueError("Frozen version manifest lacks file manifest binding")
    if frozen_file_binding.get("path") != FROZEN_FILE_MANIFEST.as_posix():
        raise ValueError("Frozen file manifest path binding differs")
    if frozen_file_binding.get("sha256") != sha256_file(frozen_file_manifest_path):
        raise ValueError("Frozen file manifest hash binding differs")
    b0f_prompt_inventory_record = next(
        (row for row in frozen_file_manifest if row.get("path") == PREFLIGHT_PROMPTS.as_posix()),
        None,
    )
    if not isinstance(b0f_prompt_inventory_record, dict):
        raise ValueError("B0F file manifest lacks preflight prompt inventory")
    b0f_prompt_inventory_sha256 = str(b0f_prompt_inventory_record.get("sha256") or "")
    if b0f_prompt_inventory_sha256 != sha256_file(prompts_path):
        raise ValueError("B0F-bound preflight prompt inventory hash differs")
    if len(prompts) != 401:
        raise ValueError(f"Expected 401 prompt metadata rows, found {len(prompts)}")
    if len(preflight_sources) != 2433 or len(frozen_sources) != 2433:
        raise ValueError("Expected 2,433 preflight and frozen source identity rows")

    preflight_skill_ids = {str(row.get("skill_id") or "") for row in preflight_sources}
    frozen_sources_by_id = {str(row.get("skill_id") or ""): row for row in frozen_sources}
    frozen_skill_ids = set(frozen_sources_by_id)
    if "" in preflight_skill_ids or "" in frozen_skill_ids:
        raise ValueError("Blank skill identity in source metadata")
    if len(preflight_skill_ids) != 2433 or len(frozen_skill_ids) != 2433:
        raise ValueError("Duplicate source identity in metadata")
    if preflight_skill_ids != frozen_skill_ids:
        raise ValueError("Prefreeze and frozen source identity sets differ")
    frozen_source_sha256 = {skill_id: str(row.get("source_sha256") or "") for skill_id, row in frozen_sources_by_id.items()}
    if any(len(value) != 64 for value in frozen_source_sha256.values()):
        raise ValueError("Frozen source metadata contains invalid source SHA-256")

    annotations, annotation_provenance = load_annotations(root)
    known_annotation_ids = set().union(*(set(values) for values in annotations.values()))
    prompt_ids = {str(row.get("prompt_id") or "") for row in prompts}
    if "" in prompt_ids or len(prompt_ids) != len(prompts):
        raise ValueError("Blank or duplicate prompt identity in prompt metadata")
    unknown_annotation_ids = sorted(known_annotation_ids - prompt_ids)
    if unknown_annotation_ids:
        raise ValueError(f"Annotations reference unknown prompts: {unknown_annotation_ids}")

    initial_rows: list[dict[str, Any]] = []
    unresolved_rows: list[dict[str, Any]] = []
    review_pool: dict[tuple[str, str], dict[str, Any]] = {}
    differences: list[dict[str, Any]] = []
    counts = Counter()
    stratum_counts = Counter()

    def pool_row(prompt: dict[str, Any], skill_id: str) -> dict[str, Any]:
        key = (prompt["prompt_id"], skill_id)
        row = review_pool.get(key)
        if row is None:
            row = {
                "candidate_skill_id": skill_id,
                "candidate_source_identity_present": skill_id in frozen_skill_ids,
                "candidate_roles": [],
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
                "seed_review_pool_only": True,
                "stratum": prompt["stratum"],
            }
            review_pool[key] = row
        return row

    for prompt in sorted(prompts, key=lambda item: str(item["prompt_id"])):
        prompt_id = str(prompt.get("prompt_id") or "")
        stratum = str(prompt.get("stratum") or "")
        gold = str(prompt.get("gold_skill") or "")
        if stratum not in ANNOTATION_FILES:
            raise ValueError(f"Unknown prompt stratum for {prompt_id}: {stratum}")
        if not gold or gold not in frozen_skill_ids:
            raise ValueError(f"Invalid strict gold for {prompt_id}")
        gold_source_sha256 = frozen_source_sha256[gold]
        valid_skills = set(require_string_list(prompt, "valid_skills", prompt_id))
        inventory_acceptable = set(require_string_list(prompt, "acceptable_skills", prompt_id))
        inventory_borderline = set(require_string_list(prompt, "borderline_skills", prompt_id))
        closest = set(require_string_list(prompt, "closest_alternatives", prompt_id))
        exact_added = set(require_string_list(prompt, "exact_source_equivalents_added", prompt_id))
        if valid_skills != ({gold} | inventory_acceptable):
            raise ValueError(f"valid_skills is not strict gold plus acceptable skills for {prompt_id}")
        annotation = annotations[stratum].get(prompt_id, {"acceptable": [], "borderline": []})
        direct_acceptable = set(annotation["acceptable"])
        direct_borderline = set(annotation["borderline"])
        candidate_ids = {gold} | inventory_acceptable | direct_acceptable | exact_added
        for skill_id in candidate_ids | inventory_borderline | direct_borderline | closest:
            if skill_id not in frozen_skill_ids:
                raise ValueError(f"Candidate identity absent from frozen source metadata: {prompt_id}:{skill_id}")

        stratum_counts[stratum] += 1
        for skill_id in sorted(candidate_ids):
            if skill_id == gold:
                basis = "strict_gold_from_b0f_bound_prompt_inventory"
                metric_status = "included_strict_gold"
                provenance_status = "traced"
                annotation_path = PREFLIGHT_PROMPTS.as_posix()
                annotation_hash = b0f_prompt_inventory_sha256
            elif skill_id in exact_added:
                if frozen_source_sha256[skill_id] != gold_source_sha256:
                    raise ValueError(
                        f"Exact-I2 duplicate closure source hash mismatch: {prompt_id}:{skill_id}"
                    )
                basis = "exact_I2_duplicate_closure"
                metric_status = "included_exact_duplicate_closure"
                provenance_status = "traced"
                annotation_path = PREFLIGHT_PROMPTS.as_posix()
                annotation_hash = sha256_file(prompts_path)
            elif skill_id in direct_acceptable:
                basis = "direct_annotation_file"
                metric_status = "included_direct_annotation"
                provenance_status = "traced"
                annotation_path = annotation_provenance[stratum]["path"]
                annotation_hash = annotation_provenance[stratum]["sha256"]
            elif skill_id in inventory_acceptable:
                basis = "historical_prompt_inventory_migration"
                metric_status = "excluded_pending_provenance"
                provenance_status = "untraced"
                annotation_path = PREFLIGHT_PROMPTS.as_posix()
                annotation_hash = sha256_file(prompts_path)
            else:
                raise ValueError(f"No provenance basis for {prompt_id}:{skill_id}")

            row = {
                "basis": basis,
                "candidate_skill_id": skill_id,
                "candidate_source_identity_present": True,
                "included_in_pre_audit_acceptable_set": metric_status.startswith("included_"),
                "legacy_annotation_path": annotation_path,
                "legacy_annotation_sha256": annotation_hash,
                "metric_status": metric_status,
                "prompt_id": prompt_id,
                "prompt_sha256": prompt["prompt_sha256"],
                "provenance_status": provenance_status,
                "stratum": stratum,
            }
            if basis == "exact_I2_duplicate_closure":
                row["candidate_source_sha256"] = frozen_source_sha256[skill_id]
                row["strict_gold_source_sha256"] = gold_source_sha256
            role = "strict_gold" if skill_id == gold else "initial_acceptable_candidate"
            pool = pool_row(prompt, skill_id)
            if role not in pool["candidate_roles"]:
                pool["candidate_roles"].append(role)
            if row["included_in_pre_audit_acceptable_set"]:
                initial_rows.append(row)
            else:
                unresolved_rows.append(row)
            counts[f"basis:{basis}"] += 1
            counts[f"metric_status:{metric_status}"] += 1

        for skill_id in sorted(inventory_acceptable - direct_acceptable - exact_added):
            differences.append(
                {
                    "candidate_skill_id": skill_id,
                    "difference_type": "inventory_only_acceptable_requires_provenance",
                    "prompt_id": prompt_id,
                    "stratum": stratum,
                }
            )
        for skill_id in sorted(direct_acceptable - inventory_acceptable):
            differences.append(
                {
                    "candidate_skill_id": skill_id,
                    "difference_type": "direct_annotation_only_acceptable",
                    "prompt_id": prompt_id,
                    "stratum": stratum,
                }
            )
        for skill_id in sorted(exact_added - inventory_acceptable):
            differences.append(
                {
                    "candidate_skill_id": skill_id,
                    "difference_type": "exact_duplicate_closure_missing_from_inventory_acceptable",
                    "prompt_id": prompt_id,
                    "stratum": stratum,
                }
            )

        for skill_id in sorted(inventory_borderline | direct_borderline):
            pool = pool_row(prompt, skill_id)
            if "borderline_candidate" not in pool["candidate_roles"]:
                pool["candidate_roles"].append("borderline_candidate")
        for skill_id in sorted(closest):
            pool = pool_row(prompt, skill_id)
            if "closest_alternative" not in pool["candidate_roles"]:
                pool["candidate_roles"].append("closest_alternative")

    for row in review_pool.values():
        row["candidate_roles"].sort()
        row["included_in_initial_acceptable_set"] = any(
            initial["prompt_id"] == row["prompt_id"] and initial["candidate_skill_id"] == row["candidate_skill_id"]
            for initial in initial_rows
        )
    initial_rows.sort(key=lambda row: (row["prompt_id"], row["candidate_skill_id"]))
    unresolved_rows.sort(key=lambda row: (row["prompt_id"], row["candidate_skill_id"]))
    review_rows = sorted(review_pool.values(), key=lambda row: (row["prompt_id"], row["candidate_skill_id"]))
    differences.sort(key=lambda row: (row["difference_type"], row["prompt_id"], row["candidate_skill_id"]))

    output_dir.mkdir(parents=True, exist_ok=False)
    initial_path = output_dir / "initial_acceptable_set.jsonl"
    unresolved_path = output_dir / "unresolved_historical_migrations.jsonl"
    pool_path = output_dir / "seed_review_pool.jsonl"
    projection_path = output_dir / "b0f_bound_prompt_identity_projection.jsonl"
    difference_path = output_dir / "reconciliation_differences.json"
    projection_rows = [
        {
            "gold_skill": prompt["gold_skill"],
            "prompt_id": prompt["prompt_id"],
            "prompt_sha256": prompt["prompt_sha256"],
            "stratum": prompt["stratum"],
        }
        for prompt in sorted(prompts, key=lambda item: str(item["prompt_id"]))
    ]
    write_jsonl_new(initial_path, initial_rows)
    write_jsonl_new(unresolved_path, unresolved_rows)
    write_jsonl_new(pool_path, review_rows)
    write_jsonl_new(projection_path, projection_rows)
    write_json_new(difference_path, differences)

    report = {
        "schema_version": "b0g-m-metadata-reconciliation-v1",
        "stage": "B0G-M",
        "state": "COMPLETE_WITH_EXPLICIT_UNRESOLVED_HISTORICAL_MIGRATIONS",
        "semantic_suitability_decided": False,
        "source_skill_body_read": False,
        "prompt_text_parsed_or_exposed": False,
        "network_calls": 0,
        "provider_calls": 0,
        "inputs": {
            "frozen_version_manifest": {
                "path": FROZEN_VERSION_MANIFEST.as_posix(),
                "sha256": sha256_file(frozen_version_path),
                "content_read": True,
            },
            "b0f_bound_preflight_prompt_inventory": {
                "path": PREFLIGHT_PROMPTS.as_posix(),
                "sha256": b0f_prompt_inventory_sha256,
                "bound_by_file_manifest": FROZEN_FILE_MANIFEST.as_posix(),
                "prompt_text_parsed_or_exposed": False,
            },
            "frozen_file_manifest": {
                "path": FROZEN_FILE_MANIFEST.as_posix(),
                "sha256": sha256_file(frozen_file_manifest_path),
                "content_read": True,
            },
            "frozen_source_manifest": {
                "path": FROZEN_SOURCE_MANIFEST.as_posix(),
                "sha256": sha256_file(frozen_sources_path),
                "content_read": True,
            },
            "preflight_prompt_inventory": {
                "path": PREFLIGHT_PROMPTS.as_posix(),
                "sha256": sha256_file(prompts_path),
                "content_read": True,
            },
            "preflight_source_inventory": {
                "path": PREFLIGHT_SOURCES.as_posix(),
                "sha256": sha256_file(preflight_sources_path),
                "content_read": True,
            },
            "legacy_annotations": annotation_provenance,
            "builder": {
                "path": SCRIPT_RELATIVE_PATH,
                "sha256": sha256_file(root / SCRIPT_RELATIVE_PATH),
            },
        },
        "counts": {
            "frozen_skills": len(frozen_skill_ids),
            "prompts": len(prompts),
            "prompts_by_stratum": dict(sorted(stratum_counts.items())),
            "initial_acceptable_rows": len(initial_rows),
            "unresolved_historical_migration_rows": len(unresolved_rows),
            "seed_review_pool_rows": len(review_rows),
            "b0f_bound_prompt_identity_projection_rows": len(projection_rows),
            "reconciliation_differences": len(differences),
            "by_basis": {key.removeprefix("basis:"): value for key, value in sorted(counts.items()) if key.startswith("basis:")},
            "by_metric_status": {key.removeprefix("metric_status:"): value for key, value in sorted(counts.items()) if key.startswith("metric_status:")},
        },
        "outputs": {
            "initial_acceptable_set": relative(initial_path, root),
            "unresolved_historical_migrations": relative(unresolved_path, root),
            "seed_review_pool": relative(pool_path, root),
            "b0f_bound_prompt_identity_projection": relative(projection_path, root),
            "reconciliation_differences": relative(difference_path, root),
        },
        "next_gate": "Freeze and approve an outcome-blind candidate-discovery contract, then obtain a separate exact prompt-plus-source review authorization for B0G.",
    }
    report_path = output_dir / "reconciliation_report.json"
    write_json_new(report_path, report)
    manifest = {
        "schema_version": "b0g-m-output-manifest-v1",
        "report_sha256": sha256_file(report_path),
        "files": [
            {"path": relative(path, root), "sha256": sha256_file(path), "utf8_bytes": path.stat().st_size}
            for path in sorted((initial_path, unresolved_path, pool_path, projection_path, difference_path, report_path))
        ],
    }
    manifest_path = output_dir / "manifest.json"
    write_json_new(manifest_path, manifest)
    return {
        "output_dir": relative(output_dir, root),
        "report": report,
        "manifest": relative(manifest_path, root),
    }


def validate(root: Path, output_dir: Path) -> dict[str, Any]:
    report_path = output_dir / "reconciliation_report.json"
    manifest_path = output_dir / "manifest.json"
    if not report_path.exists() or not manifest_path.exists():
        raise ValueError("B0G-M output is incomplete")
    report = read_json(report_path)
    manifest = read_json(manifest_path)
    if (
        report.get("semantic_suitability_decided")
        or report.get("source_skill_body_read")
        or report.get("prompt_text_parsed_or_exposed")
    ):
        raise ValueError("B0G-M boundary violation recorded")
    if report.get("network_calls") != 0 or report.get("provider_calls") != 0:
        raise ValueError("B0G-M network/provider boundary violation recorded")
    inputs = report.get("inputs")
    if not isinstance(inputs, dict):
        raise ValueError("B0G-M report lacks input bindings")
    b0f_prompt_input = inputs.get("b0f_bound_preflight_prompt_inventory")
    b0f_version_input = inputs.get("frozen_version_manifest")
    b0f_file_input = inputs.get("frozen_file_manifest")
    if not all(isinstance(item, dict) for item in (b0f_prompt_input, b0f_version_input, b0f_file_input)):
        raise ValueError("B0G-M report lacks B0F input bindings")
    if b0f_prompt_input.get("sha256") != sha256_file(root / PREFLIGHT_PROMPTS):
        raise ValueError("B0F-bound prompt inventory input drift")
    if b0f_version_input.get("sha256") != sha256_file(root / FROZEN_VERSION_MANIFEST):
        raise ValueError("Frozen version manifest input drift")
    if b0f_file_input.get("sha256") != sha256_file(root / FROZEN_FILE_MANIFEST):
        raise ValueError("Frozen file manifest input drift")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("B0G-M manifest has no files")
    for row in files:
        path = root / str(row["path"])
        if not path.exists() or sha256_file(path) != row["sha256"]:
            raise ValueError(f"B0G-M output hash mismatch: {row['path']}")
    initial = read_jsonl(output_dir / "initial_acceptable_set.jsonl")
    unresolved = read_jsonl(output_dir / "unresolved_historical_migrations.jsonl")
    projection = read_jsonl(output_dir / "b0f_bound_prompt_identity_projection.jsonl")
    if any(row["provenance_status"] != "traced" for row in initial):
        raise ValueError("Initial acceptable set contains untraced candidate")
    if any(row["basis"] != "historical_prompt_inventory_migration" for row in unresolved):
        raise ValueError("Unresolved migration set has wrong provenance basis")
    if any(row["included_in_pre_audit_acceptable_set"] for row in unresolved):
        raise ValueError("Unresolved migration leaked into acceptable set")
    if len(projection) != 401 or len({row["prompt_id"] for row in projection}) != 401:
        raise ValueError("B0F-bound prompt identity projection is incomplete")
    projection_by_id = {row["prompt_id"]: row for row in projection}
    for row in initial:
        if row["basis"] == "strict_gold_from_b0f_bound_prompt_inventory":
            projected = projection_by_id.get(row["prompt_id"])
            if projected is None or any(
                projected.get(field) != row.get(field)
                for field in ("prompt_id", "prompt_sha256", "stratum")
            ) or projected.get("gold_skill") != row["candidate_skill_id"]:
                raise ValueError("Strict-gold row differs from B0F-bound identity projection")
        if row["basis"] == "exact_I2_duplicate_closure" and (
            row.get("candidate_source_sha256") != row.get("strict_gold_source_sha256")
        ):
            raise ValueError("Exact-I2 duplicate closure lacks equal source hashes")
    return {
        "state": "PASS",
        "initial_acceptable_rows": len(initial),
        "unresolved_historical_migration_rows": len(unresolved),
        "output_dir": relative(output_dir, root),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate an existing B0G-M output only.")
    parser.add_argument(
        "--output-dir",
        default=(FROZEN_ROOT / "b0g_m_v3_2026-08-08").as_posix(),
        help="Repository-relative output directory; creation refuses an existing directory.",
    )
    args = parser.parse_args()
    root = repo_root()
    output_dir = root / args.output_dir
    try:
        result = validate(root, output_dir) if args.check else build(root, output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"B0G-M ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
