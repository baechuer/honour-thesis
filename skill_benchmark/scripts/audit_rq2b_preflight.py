#!/usr/bin/env python3
"""Build a zero-network, non-freezing RQ2b source and prompt audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
BLOCK_SCALAR_RE = re.compile(r"^([>|])([+-])?$", re.ASCII)
MAIN_EVALUATED_FAMILIES = {
    "api_backend_design",
    "api_mcp_tooling",
    "browser_web_automation",
    "code_github_workflow",
    "data_spreadsheet",
    "deployment_browser_qa",
    "documents_files",
    "github_ci_maintenance",
    "huggingface_ml_workflows",
    "implicit_field_stress",
    "metrics_observability",
    "news_monitoring",
    "observability_reliability",
    "office_artifact_workflows",
    "office_business_automation",
    "pdf_document_operations",
    "planning_meetings",
    "public_style_controlled",
    "reading_research",
    "reply_messaging",
    "security_appsec",
    "skill_lifecycle",
    "skill_representation_analysis",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def decode_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return str(json.loads(value))
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse the top-level scalar fields needed by the RQ2b I1 audit.

    The source corpus includes folded and literal block descriptions. This
    deliberately small parser handles those without adding a runtime package.
    """

    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    values: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith((" ", "\t")) or not line.strip():
            index += 1
            continue
        key_match = KEY_RE.match(line)
        if not key_match:
            index += 1
            continue
        key, raw = key_match.groups()
        raw = (raw or "").strip()
        block_match = BLOCK_SCALAR_RE.match(raw)
        if not block_match:
            values[key] = decode_scalar(raw)
            index += 1
            continue

        style = block_match.group(1)
        index += 1
        block: list[str] = []
        while index < len(lines):
            candidate = lines[index]
            if candidate and not candidate.startswith((" ", "\t")):
                break
            block.append(candidate)
            index += 1
        nonempty = [len(item) - len(item.lstrip()) for item in block if item.strip()]
        indent = min(nonempty) if nonempty else 0
        unindented = [item[indent:] if item.strip() else "" for item in block]
        if style == "|":
            values[key] = "\n".join(unindented).strip()
        else:
            paragraphs: list[str] = []
            current: list[str] = []
            for item in unindented:
                if item.strip():
                    current.append(item.strip())
                elif current:
                    paragraphs.append(" ".join(current))
                    current = []
            if current:
                paragraphs.append(" ".join(current))
            values[key] = "\n\n".join(paragraphs).strip()
    return values


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
            count += 1
    return count


def quantile(values: list[int], fraction: float) -> int:
    ordered = sorted(values)
    if not ordered:
        return 0
    index = min(len(ordered) - 1, int((len(ordered) - 1) * fraction))
    return ordered[index]


def source_inventory(root: Path, skills_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    wrappers = sorted(skills_root.glob("*/*/SKILL.md"))
    for source_index, wrapper in enumerate(wrappers):
        family = wrapper.parts[-3]
        skill_id = wrapper.parent.name
        original = wrapper.parent / "source" / "SKILL.original.md"
        import_metadata = wrapper.parent / "source" / "IMPORT.json"
        is_public = family == "public_imported_background"
        if is_public and not original.exists():
            errors.append(f"missing public original: {relative(wrapper, root)}")
        if is_public and not import_metadata.exists():
            errors.append(f"missing public import metadata: {relative(wrapper, root)}")
        source = original if is_public and original.exists() else wrapper
        text = source.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        name = frontmatter.get("name", "").strip()
        description = frontmatter.get("description", "").strip()
        if not name:
            errors.append(f"missing source-native name: {relative(source, root)}")
        if not description:
            errors.append(f"missing source-native description: {relative(source, root)}")
        import_row = read_json(import_metadata) if import_metadata.exists() else {}
        rows.append(
            {
                "source_row_index": source_index,
                "skill_id": skill_id,
                "family": family,
                "is_main_evaluated": family in MAIN_EVALUATED_FAMILIES,
                "source_policy": "public_original" if is_public else "authored_skill",
                "source_path": relative(source, root),
                "source_sha256": file_sha256(source),
                "source_utf8_bytes": len(text.encode("utf-8")),
                "source_chars": len(text),
                "source_tokens_approx_chars_div_4": max(1, (len(text) + 3) // 4),
                "source_name": name,
                "source_description": description,
                "source_name_sha256": sha256_text(name),
                "source_description_sha256": sha256_text(description),
                "wrapper_path": relative(wrapper, root),
                "wrapper_sha256": file_sha256(wrapper),
                "import_metadata_path": relative(import_metadata, root) if import_metadata.exists() else None,
                "import_metadata_sha256": file_sha256(import_metadata) if import_metadata.exists() else None,
                "public_origin": import_row.get("origin"),
                "public_source_url": import_row.get("source_url"),
                "public_import_status": import_row.get("import_status"),
            }
        )
    return rows, errors


def annotation_map(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = read_json(path)
    return data if isinstance(data, dict) else {}


def prompt_inventory(
    root: Path,
    prompt_specs: list[tuple[str, Path]],
    annotations: dict[str, dict[str, dict[str, Any]]],
    skills_by_id: dict[str, dict[str, Any]],
    exact_duplicates: dict[str, list[str]],
) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for stratum, directory in prompt_specs:
        for path in sorted(directory.glob("*.json")):
            source_rows = read_json(path)
            if not isinstance(source_rows, list):
                errors.append(f"prompt file is not an array: {relative(path, root)}")
                continue
            source_hash = file_sha256(path)
            for row_index, raw in enumerate(source_rows):
                prompt_id = str(raw.get("id") or "")
                gold = str(raw.get("gold_skill") or "")
                if not prompt_id:
                    errors.append(f"missing prompt id: {relative(path, root)}:{row_index}")
                elif prompt_id in seen:
                    errors.append(f"duplicate prompt id: {prompt_id}")
                seen.add(prompt_id)
                references = [gold, *(raw.get("closest_alternatives") or [])]
                for skill_id in references:
                    if skill_id not in skills_by_id:
                        errors.append(f"missing skill reference: {prompt_id}:{skill_id}")
                annotation = annotations.get(stratum, {}).get(prompt_id, {})
                acceptable = set(raw.get("acceptable_alternatives") or [])
                acceptable.update(annotation.get("acceptable") or [])
                base_valid = {gold, *acceptable}
                exact_equivalents: set[str] = set()
                for valid_skill in base_valid:
                    exact_equivalents.update(exact_duplicates.get(valid_skill, []))
                exact_equivalents.difference_update(base_valid)
                acceptable.update(exact_equivalents)
                valid_skills = {gold, *acceptable}
                prompt_text = str(raw.get("prompt") or "")
                if not prompt_text:
                    errors.append(f"missing prompt text: {prompt_id}")
                if raw.get("source_family"):
                    group_source_field = "source_family"
                elif raw.get("family"):
                    group_source_field = "family"
                else:
                    group_source_field = "stratum_fallback"
                group = raw.get("source_family") or raw.get("family") or stratum
                rows.append(
                    {
                        "prompt_id": prompt_id,
                        "stratum": stratum,
                        "group": group,
                        "group_source_field": group_source_field,
                        "source_path": relative(path, root),
                        "source_file_sha256": source_hash,
                        "source_row_index": row_index,
                        "prompt_sha256": sha256_text(prompt_text),
                        "prompt_chars": len(prompt_text),
                        "prompt_tokens_approx_chars_div_4": max(1, (len(prompt_text) + 3) // 4),
                        "gold_skill": gold,
                        "closest_alternatives": list(raw.get("closest_alternatives") or []),
                        "acceptable_skills": sorted(acceptable),
                        "valid_skills": sorted(valid_skills),
                        "borderline_skills": sorted(annotation.get("borderline") or []),
                        "exact_source_equivalents_added": sorted(exact_equivalents),
                    }
                )
    return rows, errors


def legacy_drift(root: Path, manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        return {"manifest_present": False, "checked": 0, "missing": [], "drifted": []}
    manifest = read_json(manifest_path)
    file_hashes = manifest.get("file_hashes") or {}
    missing: list[str] = []
    drifted: list[str] = []
    matched: list[str] = []
    for path_text, expected in sorted(file_hashes.items()):
        path = root / path_text
        if not path.exists():
            missing.append(path_text)
        elif file_sha256(path) != expected:
            drifted.append(path_text)
        else:
            matched.append(path_text)
    input_drift = [
        path
        for path in drifted
        if path.startswith(("skill_benchmark/prompts", "skill_benchmark/annotations", "skill_benchmark/representations"))
    ]
    output_drift = [path for path in drifted if path.startswith("skill_benchmark/outputs/")]
    return {
        "manifest_present": True,
        "manifest_version": manifest.get("version"),
        "checked": len(file_hashes),
        "matched_count": len(matched),
        "missing": missing,
        "drifted": drifted,
        "input_or_representation_drift": input_drift,
        "output_drift": output_drift,
        "has_per_skill_source_hashes": any("/skills/" in path for path in file_hashes),
    }


def render_markdown(report: dict[str, Any]) -> str:
    status = "PASS" if report["pass_preflight"] else "FAIL"
    source = report["source_summary"]
    prompt = report["prompt_summary"]
    legacy = report["legacy_freeze_drift"]
    lines = [
        "# RQ2b Prefreeze Source Audit",
        "",
        "Status: **PREFREEZE AUDIT ONLY / NOT A FROZEN PROTOCOL OR RESULT**",
        "",
        f"- Audit status: **{status}**",
        f"- Skills: {source['skill_count']}",
        f"- Authored skill sources: {source['authored_count']}",
        f"- Public original sources: {source['public_original_count']}",
        f"- Source UTF-8 bytes: {source['total_utf8_bytes']}",
        f"- Source Unicode characters: {source['total_chars']}",
        f"- Approximate source tokens (characters / 4): {source['total_tokens_approx_chars_div_4']}",
        f"- Longest source: {source['max_tokens_approx_chars_div_4']} approximate tokens",
        f"- Controlled prompts: {prompt['controlled_count']}",
        f"- Public-gold prompts: {prompt['public_gold_count']}",
        f"- Low-information stress prompts: {prompt['stress_count']}",
        f"- Exact duplicate source groups: {source['exact_duplicate_group_count']}",
        f"- Prompts whose acceptable set is extended by exact-source equivalence: {prompt['exact_equivalence_affected_prompts']}",
        "",
        "## Source Policy",
        "",
        "- `public_imported_background`: use `source/SKILL.original.md`.",
        "- Every other family: use its authored `SKILL.md`.",
        "- Normalised public wrappers remain provenance metadata only; they are not I2.",
        "- Candidate IDs and gold/role metadata are inventory-only and must never enter selector-visible text.",
        "",
        "## Legacy Freeze Drift",
        "",
        f"- Legacy manifest: `{legacy.get('manifest_version')}`",
        f"- Recorded files checked: {legacy.get('checked', 0)}",
        f"- Drifted files: {len(legacy.get('drifted', []))}",
        f"- Input/representation drift: {len(legacy.get('input_or_representation_drift', []))}",
        f"- Output drift: {len(legacy.get('output_drift', []))}",
        f"- Per-skill source hashes in legacy manifest: {legacy.get('has_per_skill_source_hashes', False)}",
        "",
        "The current RQ2b corpus therefore requires a new version and a complete per-source manifest. It must not be reported as an unchanged rerun of the legacy freeze.",
        "",
        "## Gates",
        "",
    ]
    for key, value in report["gates"].items():
        lines.append(f"- `{key}`: {'PASS' if value else 'FAIL'}")
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    lines.extend(
        [
            "",
            "## Exact Duplicate Sources",
            "",
        ]
    )
    for group in report["exact_duplicate_sources"]:
        lines.append(f"- `{group['source_sha256']}`: {', '.join(f'`{skill}`' for skill in group['skill_ids'])}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("skill_benchmark/outputs/rq2b/preflight"),
    )
    parser.add_argument(
        "--legacy-manifest",
        type=Path,
        default=Path("skill_benchmark/versions/benchmark-v0.4-2026-06-16.json"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    legacy_manifest = args.legacy_manifest if args.legacy_manifest.is_absolute() else root / args.legacy_manifest

    sources, source_errors = source_inventory(root, root / "skill_benchmark" / "skills")
    skills_by_id = {row["skill_id"]: row for row in sources}
    source_hash_groups: dict[str, list[str]] = defaultdict(list)
    for row in sources:
        source_hash_groups[row["source_sha256"]].append(row["skill_id"])
    exact_duplicate_groups = [
        {"source_sha256": digest, "skill_ids": sorted(skill_ids)}
        for digest, skill_ids in sorted(source_hash_groups.items())
        if len(skill_ids) > 1
    ]
    exact_duplicates: dict[str, list[str]] = {}
    for group in exact_duplicate_groups:
        for skill_id in group["skill_ids"]:
            exact_duplicates[skill_id] = group["skill_ids"]
    source_name_counts = Counter(row["source_name"] for row in sources)
    duplicate_source_name_groups = sorted(
        name for name, count in source_name_counts.items() if name and count > 1
    )

    annotations = {
        "controlled": annotation_map(root / "skill_benchmark" / "annotations" / "acceptable_alternatives.json"),
        "public_gold": annotation_map(root / "skill_benchmark" / "annotations" / "public_gold_acceptable_alternatives.json"),
        "stress": annotation_map(root / "skill_benchmark" / "annotations" / "low_information_acceptables.json"),
    }
    prompt_specs = [
        ("controlled", root / "skill_benchmark" / "prompts"),
        ("public_gold", root / "skill_benchmark" / "prompts_public_gold"),
        ("stress", root / "skill_benchmark" / "prompts_low_information"),
    ]
    prompts, prompt_errors = prompt_inventory(
        root,
        prompt_specs,
        annotations,
        skills_by_id,
        exact_duplicates,
    )

    policy_counts = Counter(row["source_policy"] for row in sources)
    stratum_counts = Counter(row["stratum"] for row in prompts)
    source_lengths = [int(row["source_tokens_approx_chars_div_4"]) for row in sources]
    exact_affected = sum(bool(row["exact_source_equivalents_added"]) for row in prompts)
    duplicate_skill_ids = sorted(skill for skill, count in Counter(row["skill_id"] for row in sources).items() if count > 1)
    duplicate_prompt_ids = sorted(prompt for prompt, count in Counter(row["prompt_id"] for row in prompts).items() if count > 1)
    errors = [*source_errors, *prompt_errors]
    if duplicate_skill_ids:
        errors.append(f"duplicate skill ids: {duplicate_skill_ids}")
    if duplicate_prompt_ids:
        errors.append(f"duplicate prompt ids: {duplicate_prompt_ids}")

    gates = {
        "skill_count_2433": len(sources) == 2433,
        "public_original_count_460": policy_counts["public_original"] == 460,
        "controlled_prompt_count_245": stratum_counts["controlled"] == 245,
        "public_gold_prompt_count_144": stratum_counts["public_gold"] == 144,
        "stress_prompt_count_12": stratum_counts["stress"] == 12,
        "unique_skill_ids": not duplicate_skill_ids,
        "unique_prompt_ids": not duplicate_prompt_ids,
        "all_references_resolve": not any("missing skill reference" in item for item in errors),
        "all_sources_have_name_and_description": not any(
            "missing source-native" in item for item in errors
        ),
        "all_public_sources_have_provenance": not any("public" in item and "missing" in item for item in errors),
    }
    legacy = legacy_drift(root, legacy_manifest)
    report = {
        "schema_version": "rq2b-prefreeze-audit-v1",
        "state": "prefreeze_audit_only_not_protocol_not_result",
        "network_calls": 0,
        "pass_preflight": all(gates.values()) and not errors,
        "gates": gates,
        "errors": errors,
        "source_summary": {
            "skill_count": len(sources),
            "authored_count": policy_counts["authored_skill"],
            "public_original_count": policy_counts["public_original"],
            "total_utf8_bytes": sum(int(row["source_utf8_bytes"]) for row in sources),
            "total_chars": sum(int(row["source_chars"]) for row in sources),
            "total_tokens_approx_chars_div_4": sum(source_lengths),
            "p50_tokens_approx_chars_div_4": quantile(source_lengths, 0.50),
            "p95_tokens_approx_chars_div_4": quantile(source_lengths, 0.95),
            "p99_tokens_approx_chars_div_4": quantile(source_lengths, 0.99),
            "max_tokens_approx_chars_div_4": max(source_lengths, default=0),
            "exact_duplicate_group_count": len(exact_duplicate_groups),
            "exact_duplicate_skill_count": sum(len(group["skill_ids"]) for group in exact_duplicate_groups),
            "duplicate_source_name_group_count": len(duplicate_source_name_groups),
        },
        "prompt_summary": {
            "controlled_count": stratum_counts["controlled"],
            "public_gold_count": stratum_counts["public_gold"],
            "stress_count": stratum_counts["stress"],
            "exact_equivalence_affected_prompts": exact_affected,
        },
        "exact_duplicate_sources": exact_duplicate_groups,
        "legacy_freeze_drift": legacy,
        "artifacts": {
            "source_inventory": relative(output_dir / "source_inventory.jsonl", root),
            "prompt_inventory": relative(output_dir / "prompt_inventory.jsonl", root),
            "audit_json": relative(output_dir / "audit.json", root),
            "audit_md": relative(output_dir / "audit.md", root),
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "source_inventory.jsonl", sources)
    write_jsonl(output_dir / "prompt_inventory.jsonl", prompts)
    (output_dir / "audit.json").write_text(
        json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "audit.md").write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "pass_preflight": report["pass_preflight"],
        "skill_count": len(sources),
        "prompt_counts": dict(stratum_counts),
        "legacy_drifted_files": len(legacy.get("drifted", [])),
        "exact_duplicate_groups": len(exact_duplicate_groups),
        "output_dir": relative(output_dir, root),
    }, indent=2, sort_keys=True))
    return 0 if report["pass_preflight"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
