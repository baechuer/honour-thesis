#!/usr/bin/env python3
"""Build source-hash-bound profiles for outcome-blind alternative discovery."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK_ROOT = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK_ROOT / "rq2b_naturalistic_confusability"
UNION = NC_ROOT / "manifests/current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
OVERLAY_DIR = NC_ROOT / "manifests/description_remediation_wave_001_pre_freeze_2026-08-31"
OVERLAYS = OVERLAY_DIR / "description_overlay.jsonl"
OVERLAY_DECISION = OVERLAY_DIR / "root_admission_decision.json"
PROTOCOL = NC_ROOT / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_PROTOCOL_2026-08-31.json"
OUTPUT_DIR = NC_ROOT / "manifests/whole_library_navigation_profiles_prefreeze_2026-08-31"
OUTPUT_JSONL = OUTPUT_DIR / "navigation_profiles.jsonl"
OUTPUT_SUMMARY = OUTPUT_DIR / "summary.json"

FRONTMATTER_RE = re.compile(
    r"\A(?:\ufeff)?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
HEADING_RE = re.compile(r"^#{1,3}\s+(.+?)\s*$")
BLOCK_MARKERS = {">", "|", ">-", "|-", ">+", "|+"}
DESCRIPTION_LIMIT = 1200
BODY_FALLBACK_LIMIT = 480
HEADING_LIMIT = 16
DEFAULT_RELEVANCE_EXCLUSIONS = {"anthropic", "chatgpt", "claude", "codex", "gemini", "openai"}


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        prefix = ""
        marker = raw
        if inline_block:
            prefix = inline_block.group(1).strip()
            marker = inline_block.group(2)
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
        separator = " " if marker.startswith(">") else "\n"
        value = separator.join(continuation)
        if prefix:
            value = f"{prefix} {value}"
            return normalise_space(value), "NONSTANDARD_INLINE_BLOCK_SCALAR"
        return normalise_space(value), "STANDARD_BLOCK_SCALAR"
    return "", "MISSING"


def split_source(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


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
        if (
            line.startswith(("#", "<!--", "|", ">", "- ", "* "))
            or re.match(r"^\d+[.)]\s+", line)
        ):
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


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    if raw.startswith("skill_benchmark/"):
        return WORKSPACE / path
    return BENCHMARK_ROOT / path


def source_aliases_and_paths(row: dict) -> tuple[list[str], list[Path]]:
    role = row["final_intake_role"]
    aliases: list[str] = []
    raw_paths: list[str] = []
    if role == "PARENT_V3_CANONICAL_SOURCE":
        for record in row["v3_identity_records"]:
            aliases.append(str(record["skill_id"]))
            raw_paths.append(str(record["source_path"]))
    elif row.get("rq1_records"):
        for record in row["rq1_records"]:
            aliases.append(str(record["skill_id"]))
            raw_paths.append(str(record["source_path"]))
    else:
        aliases.append(str(row["canonical_candidate_id"]))
        raw_paths.append(str(row["source_path"]))
    return sorted(set(aliases)), sorted({resolve_path(value) for value in raw_paths})


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


def relevance_safe(value: str, excluded_terms: set[str]) -> str:
    output = value
    for term in sorted(excluded_terms, key=lambda item: (-len(item), item)):
        output = re.sub(rf"(?i)\b{re.escape(term)}\b", " ", output)
    return normalise_space(output)


def parser_regression_checks() -> None:
    value, mode = parse_scalar("description: >\n  first line\n  second line", "description")
    assert (value, mode) == ("first line second line", "STANDARD_BLOCK_SCALAR")
    value, mode = parse_scalar(
        "description: Use this skill when >\n  the user needs one thing\n  and another",
        "description",
    )
    assert (value, mode) == (
        "Use this skill when the user needs one thing and another",
        "NONSTANDARD_INLINE_BLOCK_SCALAR",
    )
    value, mode = parse_scalar('description: "ordinary scalar"', "description")
    assert (value, mode) == ("ordinary scalar", "PLAIN_SCALAR")
    value, mode = parse_scalar('description: ">"', "description")
    assert (value, mode) == ("", "EMPTY_BLOCK_SCALAR")


def main() -> None:
    parser_regression_checks()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    relevance_exclusions = set(protocol["provider_product_tokens_excluded_from_relevance_text"])
    assert relevance_exclusions == DEFAULT_RELEVANCE_EXCLUSIONS
    union_rows = read_jsonl(UNION)
    overlay_decision = json.loads(OVERLAY_DECISION.read_text(encoding="utf-8"))
    assert overlay_decision["status"] == "PASS_FOR_FUTURE_FINAL_LIBRARY_REPRESENTATION_BUILD"
    admitted_hashes = {
        row["canonical_source_sha256"] for row in overlay_decision["admitted_overlays"]
    }
    overlay_by_hash = {
        row["canonical_source_sha256"]: row["final_library_description_overlay"]
        for row in read_jsonl(OVERLAYS)
        if row["canonical_source_sha256"] in admitted_hashes
    }
    assert set(overlay_by_hash) == admitted_hashes
    assert len(union_rows) == 3094

    profiles: list[dict] = []
    origin_counts: Counter[str] = Counter()
    role_counts: Counter[str] = Counter()
    for row in union_rows:
        source_hash = str(row["canonical_source_sha256"])
        aliases, paths = source_aliases_and_paths(row)
        assert aliases
        assert paths
        observed_hashes = []
        for path in paths:
            assert path.is_file(), path
            observed_hashes.append(sha256(path))
        assert set(observed_hashes) == {source_hash}, (source_hash, paths, observed_hashes)

        canonical_path = paths[0]
        source_text = canonical_path.read_text(encoding="utf-8-sig")
        frontmatter, body = split_source(source_text)
        source_name, _ = parse_scalar(frontmatter, "name")
        source_name = source_name or aliases[0]
        preserved_description, description_parse_mode = parse_scalar(frontmatter, "description")
        if source_hash in overlay_by_hash:
            description = overlay_by_hash[source_hash]
            description_origin = "ADMITTED_SOURCE_GROUNDED_OVERLAY"
        elif preserved_description:
            description = preserved_description
            description_origin = (
                "PRESERVED_NONSTANDARD_INLINE_BLOCK_SCALAR"
                if description_parse_mode == "NONSTANDARD_INLINE_BLOCK_SCALAR"
                else "PRESERVED_FRONTMATTER"
            )
        else:
            description = first_body_paragraph(body)
            description_origin = "SOURCE_BODY_FALLBACK_NAVIGATION_ONLY"
        heading_values = headings(body)
        description = bounded(description, DESCRIPTION_LIMIT)
        source_name = bounded(source_name, 240)
        assert source_name
        raw_heading_profile = normalise_space(" ".join(heading_values))
        relevance_source_name = relevance_safe(source_name, relevance_exclusions)
        relevance_source_description = relevance_safe(description, relevance_exclusions)
        relevance_heading_profile = relevance_safe(raw_heading_profile, relevance_exclusions)
        assert relevance_source_name or relevance_source_description or relevance_heading_profile

        profile = {
            "canonical_source_sha256": source_hash,
            "candidate_alias_ids": aliases,
            "source_paths": [relative_path(path) for path in paths],
            "final_intake_role": row["final_intake_role"],
            "source_name": source_name,
            "source_description": description,
            "source_description_origin": description_origin,
            "source_headings": heading_values,
            "name_description_profile": normalise_space(f"{source_name} {description}"),
            "heading_profile": raw_heading_profile,
            "relevance_source_name": relevance_source_name,
            "relevance_source_description": relevance_source_description,
            "relevance_heading_profile": relevance_heading_profile,
            "relevance_excluded_provider_product_tokens": sorted(relevance_exclusions),
            "profile_schema_version": "rq2b_whole_library_navigation_profile_v2",
            "scope_boundary": (
                "OUTCOME_BLIND_NAVIGATION_ONLY_NOT_A_FINAL_REPRESENTATION_LABEL_RANKING_OR_METRIC"
            ),
        }
        profiles.append(profile)
        origin_counts[description_origin] += 1
        role_counts[str(row["final_intake_role"])] += 1

    profiles.sort(key=lambda row: row["canonical_source_sha256"])
    assert len(profiles) == len({row["canonical_source_sha256"] for row in profiles}) == 3094
    assert all(row["name_description_profile"] for row in profiles)
    assert not any(
        re.search(
            rf"(?i)\b(?:{'|'.join(re.escape(term) for term in sorted(relevance_exclusions))})\b",
            " ".join(
                [
                    row["relevance_source_name"],
                    row["relevance_source_description"],
                    row["relevance_heading_profile"],
                ]
            ),
        )
        for row in profiles
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSONL.open("w", encoding="utf-8", newline="\n") as handle:
        for profile in profiles:
            handle.write(json.dumps(profile, ensure_ascii=False, sort_keys=True) + "\n")

    summary = {
        "status": "PASS_SOURCE_HASH_BOUND_NAVIGATION_PROFILE_MATERIALISATION_NOT_A_DISCOVERY_RUN",
        "bound_inputs": {
            str(UNION.relative_to(BENCHMARK_ROOT)): sha256(UNION),
            str(OVERLAYS.relative_to(BENCHMARK_ROOT)): sha256(OVERLAYS),
            str(OVERLAY_DECISION.relative_to(BENCHMARK_ROOT)): sha256(OVERLAY_DECISION),
            str(PROTOCOL.relative_to(BENCHMARK_ROOT)): sha256(PROTOCOL),
        },
        "counts": {
            "profile_rows": len(profiles),
            "final_intake_roles": dict(sorted(role_counts.items())),
            "description_origins": dict(sorted(origin_counts.items())),
            "profiles_with_empty_description": sum(
                not row["source_description"] for row in profiles
            ),
            "profiles_with_no_headings": sum(not row["source_headings"] for row in profiles),
            "source_hash_or_path_failures": 0,
            "profiles_with_nonstandard_inline_block_scalar": sum(
                row["source_description_origin"] == "PRESERVED_NONSTANDARD_INLINE_BLOCK_SCALAR"
                for row in profiles
            ),
            "relevance_profiles_with_excluded_provider_product_token": 0,
        },
        "profile_limits": {
            "description_characters_after_nfkc_whitespace_folding": DESCRIPTION_LIMIT,
            "first_h1_to_h3_headings": HEADING_LIMIT,
            "source_path_tokens_used_for_relevance": False,
            "origin_pin_licence_used_for_relevance": False,
            "source_body_fallback_scope": "navigation only; not a description repair or final representation",
            "source_body_fallback_character_limit": BODY_FALLBACK_LIMIT,
            "relevance_excluded_provider_product_tokens": sorted(relevance_exclusions),
            "explicit_relevance_safe_fields_emitted": True,
        },
        "output": {
            "path": str(OUTPUT_JSONL.relative_to(BENCHMARK_ROOT)),
            "sha256": sha256(OUTPUT_JSONL),
        },
        "claim_boundary": [
            "This output contains source-visible navigation profiles only.",
            "No prompt is ranked and no discovery queue, label, acceptable set, selector output or metric is created.",
            "The two admitted description overlays are applied without modifying preserved source bytes or historical V3 representations.",
            "Body fallback for malformed descriptions is a discovery aid and cannot be promoted to a final representation without separate review.",
        ],
    }
    OUTPUT_SUMMARY.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
