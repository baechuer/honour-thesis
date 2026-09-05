#!/usr/bin/env python3
"""Build fresh source-native navigation profiles after the Phase-4 amendment.

The script deliberately refuses to write a profile package until a separate,
hash-bound amendment document records the legacy two-member allocation and the
three nested-provenance path fallbacks.  ``--validate-only`` is safe before
that decision: it replays only source bytes and parses source-native fields.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
PHASE3 = NC_ROOT / "manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
METHOD_GATE = NC_ROOT / "manifests/rq2b_nc_phase4_option1_method_gate_preflight_2026-09-05"
AMENDMENT = NC_ROOT / "review/RQ2B_NC_PHASE4_OPTION1_LEGACY_AMENDMENT_2026-09-05.json"
OUT = NC_ROOT / "manifests/rq2b_nc_phase4_navigation_profiles_2026-09-05"

FRONTMATTER_RE = re.compile(r"\A(?:\ufeff)?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,3}\s+(.+?)\s*$")
BLOCK_MARKERS = {">", "|", ">-", "|-", ">+", "|+"}
DESCRIPTION_LIMIT = 1200
BODY_FALLBACK_LIMIT = 480
HEADING_LIMIT = 16
RELEVANCE_EXCLUSIONS = {"anthropic", "chatgpt", "claude", "codex", "gemini", "openai"}
EXPECTED_AMENDMENT_STATUS = "USER_APPROVED_PHASE4_OPTION1_LEGACY_2LOCAL_K6_AND_NESTED_PATH_FALLBACK"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def bounded(value: str, limit: int) -> str:
    value = normalise_space(value)
    return value if len(value) <= limit else value[:limit].rstrip()


def parse_scalar(frontmatter: str, key: str) -> tuple[str, str]:
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^{re.escape(key)}\s*:\s*(.*)$", line)
        if not match:
            continue
        raw = match.group(1).strip()
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
            raw = raw[1:-1]
        inline_block = re.match(r"^(.*\S)\s+([>|][+-]?)$", raw)
        if raw not in BLOCK_MARKERS and not inline_block:
            return normalise_space(raw), "PLAIN_SCALAR"
        prefix, marker = "", raw
        if inline_block:
            prefix, marker = inline_block.group(1).strip(), inline_block.group(2)
        continuation: list[str] = []
        for following in lines[index + 1 :]:
            if not following.strip():
                if continuation:
                    continuation.append("")
                continue
            if not following.startswith((" ", "\t")):
                break
            continuation.append(following.strip())
        if not continuation:
            return "", "EMPTY_BLOCK_SCALAR"
        value = (" " if marker.startswith(">") else "\n").join(continuation)
        return normalise_space(f"{prefix} {value}" if prefix else value), (
            "NONSTANDARD_INLINE_BLOCK_SCALAR" if prefix else "STANDARD_BLOCK_SCALAR"
        )
    return "", "MISSING"


def split_source(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    return ("", text) if not match else (match.group(1), text[match.end() :])


def headings(body: str) -> list[str]:
    output: list[str] = []
    for line in body.splitlines():
        match = HEADING_RE.match(line.strip())
        if not match:
            continue
        value = bounded(re.sub(r"[`*_]", "", match.group(1)), 200)
        if value and value not in output:
            output.append(value)
        if len(output) == HEADING_LIMIT:
            break
    return output


def first_body_paragraph(body: str) -> str:
    paragraphs: list[list[str]] = []
    current: list[str] = []
    in_fence = False
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not line:
            if current:
                paragraphs.append(current)
                current = []
            continue
        if line.startswith(("#", "<!--", "|", ">", "- ", "* ")) or re.match(r"^\d+[.)]\s+", line):
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append(current)
    for paragraph in paragraphs:
        value = bounded(" ".join(paragraph), BODY_FALLBACK_LIMIT)
        if len(value) >= 24:
            return value
    return ""


def relevance_safe(value: str) -> str:
    output = value
    for term in sorted(RELEVANCE_EXCLUSIONS, key=lambda item: (-len(item), item)):
        output = re.sub(rf"(?i)\b{re.escape(term)}\b", " ", output)
    return normalise_space(output)


def resolve_stored_path(raw: str) -> Path:
    candidates = [WORKSPACE / raw, BENCHMARK / raw]
    paths = [path.resolve() for path in candidates if path.is_file()]
    if not paths:
        raise SystemExit(f"Bound source path is missing: {raw}")
    return sorted(set(paths), key=lambda path: str(path))[0]


def historical_direct_paths(historical: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    for key, tier in (("v3_identity_records", "V3_IDENTITY_RECORD"), ("rq1_records", "RQ1_RECORD"), ("rq1_exact_reuse_records", "RQ1_EXACT_REUSE_RECORD")):
        records = historical.get(key)
        if isinstance(records, list) and records:
            paths = sorted({record["source_path"] for record in records if isinstance(record, dict) and isinstance(record.get("source_path"), str)})
            aliases = sorted({record["skill_id"] for record in records if isinstance(record, dict) and isinstance(record.get("skill_id"), str)})
            if paths:
                return tier, paths, aliases
    paths: set[str] = set()
    aliases: set[str] = set()
    for key in ("source_path",):
        if isinstance(historical.get(key), str):
            paths.add(historical[key])
    binding = historical.get("provenance_binding")
    if isinstance(binding, dict) and isinstance(binding.get("source_path"), str):
        paths.add(binding["source_path"])
    if isinstance(historical.get("canonical_candidate_id"), str):
        aliases.add(historical["canonical_candidate_id"])
    return "HISTORICAL_DIRECT_RECORD", sorted(paths), sorted(aliases)


def resolve_source(row: dict[str, Any]) -> tuple[str, list[Path], list[str], list[str]]:
    """Return selected path tier, paths, aliases and declared stored paths."""
    source = row.get("canonical_source_sha256")
    if not isinstance(source, str) or len(source) != 64:
        raise SystemExit("Malformed canonical source SHA")
    historical = row.get("historical_base_candidate")
    if isinstance(historical, dict):
        tier, stored_paths, aliases = historical_direct_paths(historical)
        if stored_paths:
            paths = [resolve_stored_path(raw) for raw in stored_paths]
            if any(sha(path) != source for path in paths):
                raise SystemExit(f"Historical source-byte replay drift: {source}")
            return tier, sorted(set(paths), key=lambda path: str(path)), aliases, stored_paths
    origins = row.get("local_nc_origin_records")
    if not isinstance(origins, list) or not origins:
        raise SystemExit(f"No source path binding for {source}")
    direct = sorted({path for origin in origins if isinstance(origin, dict) for path in origin.get("source_paths", []) if isinstance(path, str)})
    aliases = sorted({str(origin.get("member_token")) for origin in origins if isinstance(origin, dict) and origin.get("member_token")})
    if direct:
        paths = [resolve_stored_path(raw) for raw in direct]
        if any(sha(path) != source for path in paths):
            raise SystemExit(f"Local source-byte replay drift: {source}")
        return "LOCAL_ORIGIN_DIRECT", sorted(set(paths), key=lambda path: str(path)), aliases, direct
    nested: set[str] = set()
    for origin in origins:
        provenance = origin.get("provenance_record") if isinstance(origin, dict) else None
        if not isinstance(provenance, dict) or provenance.get("canonical_source_sha256") != source:
            raise SystemExit(f"Nested provenance identity drift: {source}")
        if provenance.get("source_byte_replay") != "PASS_SHA256_MATCH" or not str(provenance.get("provenance_preflight_status", "")).startswith("PASS_"):
            raise SystemExit(f"Nested provenance is not a PASS byte binding: {source}")
        values = provenance.get("source_paths")
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise SystemExit(f"Nested provenance paths are malformed: {source}")
        nested.update(values)
    if len(nested) != 1:
        raise SystemExit(f"Nested provenance fallback is not unique: {source}")
    paths = [resolve_stored_path(raw) for raw in sorted(nested)]
    if any(sha(path) != source for path in paths):
        raise SystemExit(f"Nested provenance source-byte replay drift: {source}")
    return "NESTED_PROVENANCE_FALLBACK", paths, aliases, sorted(nested)


def source_role(row: dict[str, Any]) -> str:
    historical = row.get("historical_base_candidate")
    if isinstance(historical, dict) and isinstance(historical.get("final_intake_role"), str):
        return historical["final_intake_role"]
    return "RQ2B_NC_SOURCE_NATIVE_CANDIDATE"


def parser_regression_checks() -> None:
    assert parse_scalar("description: >\n  first line\n  second line", "description") == ("first line second line", "STANDARD_BLOCK_SCALAR")
    assert parse_scalar("description: Use this skill when >\n  the user needs one thing\n  and another", "description") == ("Use this skill when the user needs one thing and another", "NONSTANDARD_INLINE_BLOCK_SCALAR")
    assert parse_scalar('description: "ordinary scalar"', "description") == ("ordinary scalar", "PLAIN_SCALAR")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--authorised-phase4-method-amendment", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if not args.validate_only:
        if not args.authorised_phase4_method_amendment:
            raise SystemExit("Refusing to write profiles before explicit Phase-4 amendment authorisation")
        if out.exists():
            raise SystemExit(f"Refusing to overwrite navigation profiles: {out}")
        if not AMENDMENT.is_file():
            raise SystemExit(f"Missing explicit Phase-4 amendment: {AMENDMENT}")
        amendment = json.loads(AMENDMENT.read_text(encoding="utf-8"))
        if amendment.get("status") != EXPECTED_AMENDMENT_STATUS:
            raise SystemExit("Phase-4 amendment is not user-approved for this profile policy")

    parser_regression_checks()
    inputs = {
        "controlling_sop": SOP,
        "phase3_summary": PHASE3 / "summary.json",
        "candidate_source_union": PHASE3 / "candidate_source_union_for_phase4.jsonl",
        "method_gate_summary": METHOD_GATE / "summary.json",
    }
    for path in inputs.values():
        if not path.is_file():
            raise SystemExit(f"Missing required profile input: {path}")
    phase3_summary = json.loads(inputs["phase3_summary"].read_text(encoding="utf-8"))
    if phase3_summary.get("status") != "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE":
        raise SystemExit("Phase-3 closure does not permit profile preflight")
    union = read_jsonl(inputs["candidate_source_union"])
    by_source = {row.get("canonical_source_sha256"): row for row in union}
    if len(union) != len(by_source) != 3798:
        raise SystemExit("Candidate union cardinality drift")

    profiles: list[dict[str, Any]] = []
    path_rows: list[dict[str, Any]] = []
    description_counts: Counter[str] = Counter()
    path_tier_counts: Counter[str] = Counter()
    role_counts: Counter[str] = Counter()
    for source, row in sorted(by_source.items()):
        if not isinstance(source, str) or len(source) != 64:
            raise SystemExit("Malformed source key in frozen union")
        tier, paths, aliases, declared_paths = resolve_source(row)
        selected_path = paths[0]
        source_text = selected_path.read_text(encoding="utf-8-sig")
        frontmatter, body = split_source(source_text)
        source_name, _ = parse_scalar(frontmatter, "name")
        source_name = bounded(source_name or (aliases[0] if aliases else selected_path.parent.name), 240)
        description, parse_mode = parse_scalar(frontmatter, "description")
        if description:
            description_origin = "PRESERVED_NONSTANDARD_INLINE_BLOCK_SCALAR" if parse_mode == "NONSTANDARD_INLINE_BLOCK_SCALAR" else "PRESERVED_FRONTMATTER"
        else:
            description, description_origin = first_body_paragraph(body), "SOURCE_BODY_FALLBACK_NAVIGATION_ONLY"
        description = bounded(description, DESCRIPTION_LIMIT)
        heading_values = headings(body)
        raw_headings = normalise_space(" ".join(heading_values))
        relevance_name = relevance_safe(source_name)
        relevance_description = relevance_safe(description)
        relevance_headings = relevance_safe(raw_headings)
        if not source_name or not (relevance_name or relevance_description or relevance_headings):
            raise SystemExit(f"No relevance-safe source-native profile content: {source}")
        profiles.append({
            "canonical_source_sha256": source,
            "profile_schema_version": "rq2b_nc_phase4_source_native_navigation_profile_v1",
            "source_name": source_name,
            "source_description": description,
            "source_description_origin": description_origin,
            "source_headings": heading_values,
            "relevance_source_name": relevance_name,
            "relevance_source_description": relevance_description,
            "relevance_heading_profile": relevance_headings,
            "relevance_excluded_provider_product_tokens": sorted(RELEVANCE_EXCLUSIONS),
            "scope_boundary": "OUTCOME_BLIND_NAVIGATION_ONLY_NOT_A_LABEL_RANKING_OR_METRIC",
        })
        path_rows.append({
            "canonical_source_sha256": source,
            "declared_source_paths": declared_paths,
            "path_resolution_tier": tier,
            "selected_workspace_relative_path": str(selected_path.relative_to(WORKSPACE)),
            "selected_source_byte_sha256": sha(selected_path),
        })
        description_counts[description_origin] += 1
        path_tier_counts[tier] += 1
        role_counts[source_role(row)] += 1

    if len(profiles) != len({row["canonical_source_sha256"] for row in profiles}) != 3798:
        raise SystemExit("Profile cardinality drift")
    if description_counts["SOURCE_BODY_FALLBACK_NAVIGATION_ONLY"] != 22 or sum(not row["source_headings"] for row in profiles) != 4 or path_tier_counts["NESTED_PROVENANCE_FALLBACK"] != 3:
        raise SystemExit("Source-native profile preflight counts drift")
    counts = {
        "profile_rows": len(profiles),
        "description_origins": dict(sorted(description_counts.items())),
        "profiles_with_no_headings": sum(not row["source_headings"] for row in profiles),
        "path_resolution_tiers": dict(sorted(path_tier_counts.items())),
        "final_intake_roles_for_reporting_only": dict(sorted(role_counts.items())),
        "source_hash_or_path_failures": 0,
        "relevance_profiles_with_excluded_provider_product_token": 0,
    }
    summary = {
        "status": "PASS_SOURCE_NATIVE_NAVIGATION_PROFILE_PREFLIGHT_PENDING_APPROVED_PHASE4_AMENDMENT" if args.validate_only else "PASS_SOURCE_NATIVE_NAVIGATION_PROFILE_MATERIALISATION_OUTCOME_BLIND_ONLY",
        "claim_boundary": "Source-byte replay and source-native field parsing only; no prompt, target, acceptable-set label, retrieval/reranking output, selector output or metric is read or generated.",
        "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in inputs.values()},
        "implementation_sha256": sha(Path(__file__).resolve()),
        "counts": counts,
        "profile_policy": {
            "description_characters_after_nfkc_whitespace_folding": DESCRIPTION_LIMIT,
            "first_h1_to_h3_headings": HEADING_LIMIT,
            "source_body_fallback": "raw source only, navigation-only, 480-character maximum; no historical overlay is used",
            "nested_provenance_fallback": "only a unique existing PASS byte-bound path, after direct tiers are absent",
            "relevance_safe_fields": ["source_name", "source_description", "source_headings"],
            "forbidden_from_relevance": ["source_path", "alias", "origin", "provenance", "licence", "prompt", "target", "label", "retrieval", "reranking", "provider_output", "metric"],
        },
        "outputs": {},
    }
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    profiles.sort(key=lambda item: item["canonical_source_sha256"])
    path_rows.sort(key=lambda item: item["canonical_source_sha256"])
    for name, rows in {"navigation_profiles.jsonl": profiles, "source_path_resolution_ledger.jsonl": path_rows}.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    summary["bound_inputs"][str(AMENDMENT.relative_to(WORKSPACE))] = sha(AMENDMENT)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"counts": counts, "output_dir": str(out), "status": summary["status"]}, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
