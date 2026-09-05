#!/usr/bin/env python3
"""Create the local-only RQ2b V3 B4 explanatory result-review artifacts.

This script consumes only frozen V3 source/provenance and B3-v2 result data.
It performs no retrieval, embedding, reranking, network request, or thesis
writing. Its information census is provenance-bounded: an I3 item's original
source evidence is description-visible only when its whitespace-folded source
text occurs in the frozen native I1 metadata description. Selector evidence is
also whitespace-normalised for retrieval, so it is not used for
source-grounding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
B3_JSON = ROOT / "skill_benchmark/rq2bv1/results/b3_v3_v2/b3_v2_local_analysis.json"
CANONICAL_EXTRACTIONS = ROOT / (
    "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/"
    "i3c_merged_final/canonical_extractions.jsonl"
)
SOURCE_MANIFEST = ROOT / (
    "skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16/"
    "source_manifest.jsonl"
)
STRICT_PROMPTS = ROOT / (
    "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/"
    "b1l_preflight_v3/strict_scored_prompts.jsonl"
)
OUTPUT_ROOT = ROOT / "skill_benchmark/rq2bv1/results/b4_v3"

EXPECTED_SOURCE_MANIFEST_SHA256 = "6f7accc1274ee1c410bfeaba2f32b41b7dc5168a81ef55343b7f56e37abce0c3"
PRIMARY_STRATA = ("controlled", "public_gold")
REPRESENTATIONS = ("i1-discovery", "i2-original", "i3-flat-evidence", "i3c-fielded-evidence")
RETRIEVERS = ("bm25", "qwen", "skillrouter")
RERANKERS = ("qwen", "skillrouter")
FIELD_ORDER = (
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "success_criteria",
    "constraints_boundaries",
    "dependencies_resources",
)
FIELD_LABELS = {
    "use_conditions": "Use condition",
    "input_preconditions": "Input / precondition",
    "output_artifacts": "Output / artifact",
    "workflow_steps": "Workflow / procedure",
    "success_criteria": "Success / verification",
    "constraints_boundaries": "Boundary / not-for",
    "dependencies_resources": "Dependency / resource",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fold_whitespace(text: str) -> str:
    """Match YAML folded metadata without relaxing words or punctuation."""
    return " ".join(text.split())


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    escaped_headers = [header.replace("|", "\\|") for header in headers]
    lines = ["| " + " | ".join(escaped_headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
    return "\n".join(lines)


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def friendly_representation(value: str) -> str:
    return {
        "i1-discovery": "I1",
        "i2-original": "I2",
        "i3-flat-evidence": "I3-flat",
        "i3c-fielded-evidence": "I3C",
    }[value]


def validate_b3() -> dict[str, Any]:
    require(B3_JSON.is_file(), f"Missing B3-v2 report: {B3_JSON}")
    report = read_json(B3_JSON)
    require(report["state"] == "completed_local_only_post_hoc_synthesis_pending_user_review_not_thesis_text", "Unexpected B3-v2 state")
    require(report["local_validation"]["condition_summary_rows"] == 108, "B3 summary count drift")
    require(report["local_validation"]["contrast_rows"] == 636, "B3 contrast count drift")
    require(report["local_validation"]["no_p_values_or_holm"] is True, "B3 inference-policy drift")
    for stage in ("b1", "b2"):
        for binding in report["inputs"][stage].values():
            path = ROOT / binding["path"]
            require(path.is_file(), f"Missing frozen {stage} input: {path}")
            require(sha256_file(path) == binding["sha256"], f"Frozen {stage} hash drift: {path}")
    return report


def load_source_manifest() -> dict[str, dict[str, Any]]:
    require(SOURCE_MANIFEST.is_file(), f"Missing V3 source manifest: {SOURCE_MANIFEST}")
    require(sha256_file(SOURCE_MANIFEST) == EXPECTED_SOURCE_MANIFEST_SHA256, "V3 source manifest hash drift")
    rows = read_jsonl(SOURCE_MANIFEST)
    require(len(rows) == 2433, "Expected 2,433 V3 source rows")
    mapping = {row["skill_id"]: row for row in rows}
    require(len(mapping) == 2433, "Duplicate source-manifest skill ID")
    return mapping


def new_aggregate() -> dict[str, Any]:
    return {
        "units": 0,
        "retained_spans": 0,
        "description_visible_spans": 0,
        "body_only_spans": 0,
        "units_with_any_retained_span": 0,
        "units_with_any_description_visible_span": 0,
        "units_with_any_body_only_span": 0,
        "units_with_mixed_span_locations": 0,
        "field_spans": Counter(),
        "field_description_visible_spans": Counter(),
        "field_body_only_spans": Counter(),
        "field_units": Counter(),
        "field_description_visible_units": Counter(),
        "field_body_only_units": Counter(),
    }


def add_profile(aggregate: dict[str, Any], profile: dict[str, Any]) -> None:
    aggregate["units"] += 1
    aggregate["retained_spans"] += profile["retained_span_count"]
    aggregate["description_visible_spans"] += profile["description_visible_span_count"]
    aggregate["body_only_spans"] += profile["body_only_span_count"]
    aggregate["units_with_any_retained_span"] += int(profile["retained_span_count"] > 0)
    aggregate["units_with_any_description_visible_span"] += int(profile["description_visible_span_count"] > 0)
    aggregate["units_with_any_body_only_span"] += int(profile["body_only_span_count"] > 0)
    aggregate["units_with_mixed_span_locations"] += int(
        profile["description_visible_span_count"] > 0 and profile["body_only_span_count"] > 0
    )
    for field_key in FIELD_ORDER:
        field = profile["fields"][field_key]
        aggregate["field_spans"][field_key] += field["span_count"]
        aggregate["field_description_visible_spans"][field_key] += field["description_visible_span_count"]
        aggregate["field_body_only_spans"][field_key] += field["body_only_span_count"]
        aggregate["field_units"][field_key] += int(field["span_count"] > 0)
        aggregate["field_description_visible_units"][field_key] += int(field["description_visible_span_count"] > 0)
        aggregate["field_body_only_units"][field_key] += int(field["body_only_span_count"] > 0)


def serialise_aggregate(aggregate: dict[str, Any]) -> dict[str, Any]:
    result = {key: value for key, value in aggregate.items() if not isinstance(value, Counter)}
    result["fields"] = {
        field_key: {
            "span_count": aggregate["field_spans"][field_key],
            "description_visible_span_count": aggregate["field_description_visible_spans"][field_key],
            "body_only_span_count": aggregate["field_body_only_spans"][field_key],
            "units_with_field": aggregate["field_units"][field_key],
            "units_with_description_visible_field": aggregate["field_description_visible_units"][field_key],
            "units_with_body_only_field": aggregate["field_body_only_units"][field_key],
        }
        for field_key in FIELD_ORDER
    }
    return result


def build_availability_census(source_manifest: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(CANONICAL_EXTRACTIONS.is_file(), f"Missing canonical extraction: {CANONICAL_EXTRACTIONS}")
    rows = read_jsonl(CANONICAL_EXTRACTIONS)
    require(len(rows) == 2433, "Expected 2,433 canonical extractions")
    profiles: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    aggregate = new_aggregate()

    for extraction in rows:
        skill_id = extraction["skill_id"]
        require(skill_id not in seen_ids, f"Duplicate canonical skill ID: {skill_id}")
        seen_ids.add(skill_id)
        source = source_manifest.get(skill_id)
        require(source is not None, f"Canonical skill missing from V3 source manifest: {skill_id}")
        require(source["source_sha256"] == extraction["source_sha256"], f"Manifest/canonical hash mismatch: {skill_id}")
        require(source["source_path"] == extraction["source"], f"Manifest/canonical source-path mismatch: {skill_id}")
        source_path = ROOT / extraction["source"]
        require(source_path.is_file(), f"Canonical source missing: {source_path}")
        require(sha256_file(source_path) == extraction["source_sha256"], f"Canonical source hash drift: {skill_id}")
        source_text = source_path.read_text(encoding="utf-8")
        description = extraction["description"]
        require(description == source["source_description"], f"Description drift: {skill_id}")
        require(bool(description), f"Empty frozen I1 description: {skill_id}")

        fields = {
            key: {
                "span_count": 0,
                "description_visible_span_count": 0,
                "body_only_span_count": 0,
            }
            for key in FIELD_ORDER
        }
        retained_spans = extraction["retained_selector_spans"]
        for span in retained_spans:
            field_key = span["field_key"]
            require(field_key in fields, f"Unknown field key in {skill_id}: {field_key}")
            source_evidence = span["evidence"]
            selector_evidence = span["selector_evidence"]
            require(bool(source_evidence), f"Empty original evidence: {skill_id}/{span['item_id']}")
            require(bool(selector_evidence), f"Empty selector evidence: {skill_id}/{span['item_id']}")
            require(source_evidence in source_text, f"Original evidence no longer source-grounded: {skill_id}/{span['item_id']}")
            fields[field_key]["span_count"] += 1
            if fold_whitespace(source_evidence) in fold_whitespace(description):
                fields[field_key]["description_visible_span_count"] += 1
            else:
                fields[field_key]["body_only_span_count"] += 1

        description_visible = sum(field["description_visible_span_count"] for field in fields.values())
        body_only = sum(field["body_only_span_count"] for field in fields.values())
        profile = {
            "skill_id": skill_id,
            "source_row_index": extraction["source_row_index"],
            "family": extraction["family"],
            "source": extraction["source"],
            "source_sha256": extraction["source_sha256"],
            "name": extraction["name"],
            "description": description,
            "retained_span_count": len(retained_spans),
            "description_visible_span_count": description_visible,
            "body_only_span_count": body_only,
            "fields": fields,
        }
        require(description_visible + body_only == len(retained_spans), f"Span-location accounting mismatch: {skill_id}")
        profiles.append(profile)
        add_profile(aggregate, profile)

    require(seen_ids == set(source_manifest), "Canonical/source-manifest ID coverage mismatch")
    return profiles, serialise_aggregate(aggregate)


def gold_prompt_availability(profiles: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(STRICT_PROMPTS.is_file(), f"Missing strict prompts: {STRICT_PROMPTS}")
    prompts = read_jsonl(STRICT_PROMPTS)
    require(len(prompts) == 381, "Expected 381 strict prompts")
    profile_by_id = {profile["skill_id"]: profile for profile in profiles}
    aggregates = {"all": new_aggregate(), **{stratum: new_aggregate() for stratum in PRIMARY_STRATA}}
    records: list[dict[str, Any]] = []
    seen_prompt_ids: set[str] = set()

    for prompt in prompts:
        prompt_id = prompt["prompt_id"]
        require(prompt_id not in seen_prompt_ids, f"Duplicate strict prompt ID: {prompt_id}")
        seen_prompt_ids.add(prompt_id)
        stratum = prompt["stratum"]
        require(stratum in PRIMARY_STRATA, f"Unexpected strict prompt stratum: {stratum}")
        profile = profile_by_id.get(prompt["gold_skill"])
        require(profile is not None, f"Strict gold absent from canonical extraction: {prompt['gold_skill']}")
        record = {
            "prompt_id": prompt_id,
            "prompt_sha256": prompt["prompt_sha256"],
            "prompt": prompt["prompt"],
            "group": prompt["group"],
            "stratum": stratum,
            "gold_skill": prompt["gold_skill"],
            "gold_name": profile["name"],
            "gold_i1_description": profile["description"],
            "gold_retained_span_count": profile["retained_span_count"],
            "gold_description_visible_span_count": profile["description_visible_span_count"],
            "gold_body_only_span_count": profile["body_only_span_count"],
            "gold_fields": profile["fields"],
        }
        records.append(record)
        add_profile(aggregates["all"], profile)
        add_profile(aggregates[stratum], profile)

    return records, {name: serialise_aggregate(value) for name, value in aggregates.items()}


def matrix_rows(b3: dict[str, Any]) -> list[dict[str, Any]]:
    summary_index = {
        (row["stratum"], row["stage"], row["first_stage_retriever"], row["representation"]): row
        for row in b3["condition_summaries"]
    }
    rows: list[dict[str, Any]] = []
    for stratum in PRIMARY_STRATA:
        for retriever in RETRIEVERS:
            for representation in REPRESENTATIONS:
                b1 = summary_index[(stratum, "b1", retriever, representation)]
                qwen_b2 = summary_index[(stratum, "qwen_b2", retriever, representation)]
                sr_b2 = summary_index[(stratum, "skillrouter_b2", retriever, representation)]
                rows.append({
                    "stratum": stratum,
                    "retriever": retriever,
                    "representation": representation,
                    "b1_hit_at_1_cluster_macro": b1["hit_at_1_cluster_macro"],
                    "b1_mrr_at_20_cluster_macro": b1["mrr_at_20_cluster_macro"],
                    "b1_recall_at_20_cluster_macro": b1["recall_at_20_cluster_macro"],
                    "qwen_b2_hit_at_1_cluster_macro": qwen_b2["hit_at_1_cluster_macro"],
                    "skillrouter_b2_hit_at_1_cluster_macro": sr_b2["hit_at_1_cluster_macro"],
                })
    require(len(rows) == 24, "B4 primary matrix row count mismatch")
    return rows


def failure_comparisons(b3: dict[str, Any]) -> list[dict[str, Any]]:
    primary_rows = [row for row in b3["failure_analysis"] if row["stratum"] in PRIMARY_STRATA]
    require(len(primary_rows) == 48, "B4 primary failure row count mismatch")
    indexed = {
        (row["stratum"], row["reranker"], row["first_stage_retriever"], row["representation"]): row
        for row in primary_rows
    }
    comparisons: list[dict[str, Any]] = []

    def failure_rate(row: dict[str, Any], name: str) -> float:
        # B3 omits zero-count categories from a compact JSON row.
        count = row["counts"].get(name, 0)
        observed_rate = row["rates"].get(name, 0.0)
        expected_rate = count / row["n_prompts"]
        require(abs(observed_rate - expected_rate) < 1e-12, f"Failure rate/count mismatch: {name}")
        return observed_rate

    for stratum in PRIMARY_STRATA:
        for reranker in RERANKERS:
            for retriever in RETRIEVERS:
                for right in ("i1-discovery", "i2-original"):
                    left_row = indexed[(stratum, reranker, retriever, "i3c-fielded-evidence")]
                    right_row = indexed[(stratum, reranker, retriever, right)]
                    require(left_row["n_prompts"] == right_row["n_prompts"], "Failure denominator mismatch")
                    comparisons.append({
                        "stratum": stratum,
                        "reranker": reranker,
                        "first_stage_retriever": retriever,
                        "left": "i3c-fielded-evidence",
                        "right": right,
                        "n_prompts": left_row["n_prompts"],
                        "rate_deltas_left_minus_right": {
                            name: failure_rate(left_row, name) - failure_rate(right_row, name)
                            for name in ("candidate_miss", "ordering_error", "reranker_correction", "reranker_regression", "persistent_top1_error")
                        },
                    })
    require(len(comparisons) == 24, "B4 failure comparison row count mismatch")
    return comparisons


def serialise_b3_cost(b3: dict[str, Any]) -> dict[str, Any]:
    cost = b3["cost"]
    require(len(cost["b1_per_condition"]) == 12, "B4 B1 cost row count mismatch")
    require(len(cost["b2_per_condition"]) == 24, "B4 B2 cost row count mismatch")
    require(cost["shared_i3_extraction"]["durable_wall_time_or_invoice"] == "not available", "Unexpected I3 cost boundary")
    return cost


def markdown_availability(availability: dict[str, Any]) -> str:
    corpus = availability["corpus"]
    gold = availability["gold_prompt_records"]
    lines = [
        "# RQ2b V3 B4 Information Availability And Retention Census",
        "",
        "Status: `LOCAL-ONLY / POST-HOC EXPLANATORY AUDIT / NOT THESIS TEXT`",
        "",
        "## Classification Rule",
        "",
        "A retained I3 item is `description_visible` only when its original source evidence, after whitespace folding only, occurs in the frozen source-native I1 metadata description after the same folding. Otherwise it is `body_only`. The selector text may normalise whitespace, so B4 does not incorrectly require selector text itself to be a raw-source substring. This is provenance-bounded availability, not a semantic determination that a span is required by a prompt or that a body-only span is decisive.",
        "",
        "## Full 2,433-Skill Corpus",
        "",
        markdown_table(
            ["Skills", "Retained spans", "Description-visible", "Body-only", "Skills with any description-visible", "Skills with any body-only", "Mixed-location skills"],
            [[
                str(corpus["units"]),
                str(corpus["retained_spans"]),
                f"{corpus['description_visible_spans']} ({pct(corpus['description_visible_spans'] / corpus['retained_spans']) if corpus['retained_spans'] else 'n/a'})",
                f"{corpus['body_only_spans']} ({pct(corpus['body_only_spans'] / corpus['retained_spans']) if corpus['retained_spans'] else 'n/a'})",
                str(corpus["units_with_any_description_visible_span"]),
                str(corpus["units_with_any_body_only_span"]),
                str(corpus["units_with_mixed_span_locations"]),
            ]],
        ),
        "",
        "## Field Census Across The Full Corpus",
        "",
        markdown_table(
            ["Field", "Spans", "Description-visible spans", "Body-only spans", "Skills with field", "Skills with visible field", "Skills with body-only field"],
            [[
                FIELD_LABELS[field_key],
                str(corpus["fields"][field_key]["span_count"]),
                str(corpus["fields"][field_key]["description_visible_span_count"]),
                str(corpus["fields"][field_key]["body_only_span_count"]),
                str(corpus["fields"][field_key]["units_with_field"]),
                str(corpus["fields"][field_key]["units_with_description_visible_field"]),
                str(corpus["fields"][field_key]["units_with_body_only_field"]),
            ] for field_key in FIELD_ORDER],
        ),
        "",
        "## Strict-Gold Prompt Records",
        "",
        markdown_table(
            ["Stratum", "Prompt records", "Retained spans", "Description-visible", "Body-only", "Golds with any visible span", "Golds with any body-only span"],
            [[
                stratum,
                str(gold[stratum]["units"]),
                str(gold[stratum]["retained_spans"]),
                str(gold[stratum]["description_visible_spans"]),
                str(gold[stratum]["body_only_spans"]),
                str(gold[stratum]["units_with_any_description_visible_span"]),
                str(gold[stratum]["units_with_any_body_only_span"]),
            ] for stratum in PRIMARY_STRATA],
        ),
        "",
        "The machine-readable `B4_PROMPT_AVAILABILITY_RECORDS.jsonl` preserves one record per strict prompt. It is review material only; it does not identify the decisive field for a prompt or create a new field-effect metric.",
        "",
    ]
    return "\n".join(lines)


def markdown_review(report: dict[str, Any]) -> str:
    matrix = report["matrix"]
    availability = report["availability"]
    cost = report["cost"]
    failures = report["failure_comparisons"]
    lines = [
        "# RQ2b V3 B4 Local Result Review",
        "",
        "Status: `LOCAL-ONLY POST-HOC EXPLANATORY AUDIT / COMPLETE PENDING USER REVIEW / NOT THESIS TEXT`",
        "",
        "## Scope And Claim Boundary",
        "",
        "- Uses only frozen B3-v2 results, V3 prompts, sources, and canonical I3 evidence. No model/API call, new selector, source/extraction edit, or thesis write occurred.",
        "- Strict metrics are agreement with the frozen single gold label, not unique routing correctness or downstream task success.",
        "- The availability census is source/metadata provenance after whitespace folding only. It cannot establish that an I1-visible span is sufficient for a prompt, that a body-only span is decisive, or that an information field caused a ranking change.",
        "",
        "## B4.1 Primary Cluster-Macro H@1 Matrix",
        "",
        markdown_table(
            ["Stratum", "First stage", "Representation", "B1 H@1", "Qwen B2 end-to-end H@1", "SkillRouter B2 end-to-end H@1"],
            [[
                row["stratum"],
                row["retriever"],
                friendly_representation(row["representation"]),
                f"{row['b1_hit_at_1_cluster_macro']:.3f}",
                f"{row['qwen_b2_hit_at_1_cluster_macro']:.3f}",
                f"{row['skillrouter_b2_hit_at_1_cluster_macro']:.3f}",
            ] for row in matrix],
        ),
        "",
        "The complete B3-v2 contrast matrix, including all representation/retriever/reranker paired intervals, remains the authoritative table: `../b3_v3_v2/B3_V2_COMPLETE_CONTRASTS.md`.",
        "",
        "## B4.2 Availability Summary",
        "",
        f"- Across the full corpus, {availability['corpus']['description_visible_spans']} of {availability['corpus']['retained_spans']} retained I3 items are source/metadata-visible in I1 descriptions after whitespace folding only; {availability['corpus']['body_only_spans']} are body-only under the protocol rule.",
        f"- Across 381 strict-gold prompt records, controlled has {availability['gold_prompt_records']['controlled']['description_visible_spans']} visible and {availability['gold_prompt_records']['controlled']['body_only_spans']} body-only retained spans; public_gold has {availability['gold_prompt_records']['public_gold']['description_visible_spans']} visible and {availability['gold_prompt_records']['public_gold']['body_only_spans']} body-only retained spans.",
        "- See `B4_INFORMATION_AVAILABILITY_CENSUS.md` for the full field and stratum census. This reports availability, not a causal field-effect result.",
        "",
        "## B4.2 Interpretation, Limited To This Census",
        "",
        f"- The census does **not** support the simple explanation that I1 wins because retained I3 operational content was already duplicated in its native description: only {availability['corpus']['description_visible_spans']}/{availability['corpus']['retained_spans']} ({pct(availability['corpus']['description_visible_spans'] / availability['corpus']['retained_spans'])}) retained items are visible corpus-wide, and {availability['gold_prompt_records']['all']['description_visible_spans']}/{availability['gold_prompt_records']['all']['retained_spans']} ({pct(availability['gold_prompt_records']['all']['description_visible_spans'] / availability['gold_prompt_records']['all']['retained_spans'])}) across strict-gold prompt records.",
        "- I1 may instead be competitive because its names/descriptions expose coarse task or category cues, because of fixed benchmark/prompt-label properties, or because extraction/formatting changes matching behaviour. B4 does not identify which explanation is responsible and must not call one causal.",
        "- In the public B2 rows, I3C is below I2 in five of six first-stage-retriever/reranker combinations. I3C-minus-I2 candidate-miss deltas are non-negative in every B4 comparison, which is consistent with I2 retaining useful candidate-inclusion detail under this fixed benchmark but does not prove which omitted text caused a miss.",
        "- Relative to I2, I3C reduces selector-visible corpus tokens by 72.3% (BM25), 76.0% (Qwen), and 75.9% (SkillRouter); it reduces measured document/index time by 64.5%, 66.4%, and 78.9% respectively. These are B1 representation/index costs only, not total I3 construction cost.",
        "",
        "## B4.3 I3C Failure-Mechanism Deltas",
        "",
        "Rates below are I3C minus the named comparison representation. Positive candidate-miss or persistent-top1-error values are worse for I3C; positive correction values mean more B2 corrections after I3C candidate generation. These are descriptive prompt rates, not paired causal estimates.",
        "",
        markdown_table(
            ["Stratum", "Reranker", "B1 retriever", "I3C minus", "Candidate-miss delta", "Ordering-error delta", "Correction delta", "Regression delta", "Persistent-top1 delta"],
            [[
                row["stratum"],
                row["reranker"],
                row["first_stage_retriever"],
                friendly_representation(row["right"]),
                f"{row['rate_deltas_left_minus_right']['candidate_miss']:+.3f}",
                f"{row['rate_deltas_left_minus_right']['ordering_error']:+.3f}",
                f"{row['rate_deltas_left_minus_right']['reranker_correction']:+.3f}",
                f"{row['rate_deltas_left_minus_right']['reranker_regression']:+.3f}",
                f"{row['rate_deltas_left_minus_right']['persistent_top1_error']:+.3f}",
            ] for row in failures],
        ),
        "",
        "## B4.4 Measured Cost Frontier",
        "",
        "Observed deployment decomposition: `shared representation/extraction footprint + document embedding/index work + N * B1 query work + N * B2 rerank work`.",
        "",
        markdown_table(
            ["B1 retriever", "Representation", "One-time document/index seconds", "Mean query seconds", "Selector-visible corpus tokens"],
            [[
                row["retriever"],
                friendly_representation(row["representation"]),
                f"{row['one_time_document_embedding_or_index_seconds']:.3f}",
                f"{row['query_seconds']['mean']:.6f}",
                str(row["selector_visible_corpus_tokens"]),
            ] for row in cost["b1_per_condition"]],
        ),
        "",
        f"Shared I3 construction footprint: {cost['shared_i3_extraction']['source_rows']} source rows, {cost['shared_i3_extraction']['source_chunks']} source chunks, and {cost['shared_i3_extraction']['input_proxy_tokens']} proxy input tokens. Durable comparable I3 extraction wall-time/invoice: `{cost['shared_i3_extraction']['durable_wall_time_or_invoice']}`. Therefore B4 does not calculate a total I3 cost or break-even query count.",
        "",
        "## B4 Claim Gate",
        "",
        "B4 supports fixed-benchmark statements about observed representation/retriever/reranker accuracy-cost trade-offs and source/metadata availability of retained evidence. It does not prove universal information-field value, causal enrichment effects, complete I3 total cost, unique correct routing, or failure of every field-aware architecture. User review is required before B5 thesis integration.",
        "",
    ]
    return "\n".join(lines)


def validate_output(report: dict[str, Any], profiles: list[dict[str, Any]], prompt_records: list[dict[str, Any]]) -> dict[str, Any]:
    require(len(report["matrix"]) == 24, "Invalid B4 matrix output")
    require(len(report["failure_comparisons"]) == 24, "Invalid B4 failure output")
    require(len(profiles) == 2433, "Invalid B4 corpus census output")
    require(len(prompt_records) == 381, "Invalid B4 prompt census output")
    corpus = report["availability"]["corpus"]
    require(corpus["description_visible_spans"] + corpus["body_only_spans"] == corpus["retained_spans"], "Invalid B4 corpus span accounting")
    for stratum in PRIMARY_STRATA:
        aggregate = report["availability"]["gold_prompt_records"][stratum]
        require(aggregate["description_visible_spans"] + aggregate["body_only_spans"] == aggregate["retained_spans"], f"Invalid B4 {stratum} span accounting")
    return {
        "state": "pass",
        "b3_report_sha256": sha256_file(B3_JSON),
        "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
        "canonical_extractions_sha256": sha256_file(CANONICAL_EXTRACTIONS),
        "strict_prompts_sha256": sha256_file(STRICT_PROMPTS),
        "matrix_rows": len(report["matrix"]),
        "failure_comparison_rows": len(report["failure_comparisons"]),
        "skill_availability_rows": len(profiles),
        "prompt_availability_rows": len(prompt_records),
        "external_or_model_calls": 0,
        "thesis_result_writing": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    args = parser.parse_args()
    output_root = args.output_root.resolve()
    require(not output_root.exists(), f"Refusing to overwrite existing B4 output: {output_root}")

    b3 = validate_b3()
    source_manifest = load_source_manifest()
    profiles, corpus_aggregate = build_availability_census(source_manifest)
    prompt_records, gold_aggregates = gold_prompt_availability(profiles)
    report: dict[str, Any] = {
        "schema_version": "rq2bv1-v3-b4-local-result-review-v1",
        "state": "completed_local_only_post_hoc_explanatory_audit_pending_user_review_not_thesis_text",
        "protocol": "skill_benchmark/rq2bv1/analysis_protocols/B4_RESULT_REVIEW_PROTOCOL.md",
        "b3_v2_report": {
            "path": str(B3_JSON.relative_to(ROOT)),
            "sha256": sha256_file(B3_JSON),
        },
        "matrix": matrix_rows(b3),
        "availability": {
            "classification_rule": "An item's original source evidence after whitespace folding only occurring in the frozen native I1 metadata description after the same folding is description_visible; otherwise body_only. Whitespace-normalised selector_evidence is validated as non-empty but is not used for raw-source substring checks.",
            "corpus": corpus_aggregate,
            "gold_prompt_records": gold_aggregates,
        },
        "failure_comparisons": failure_comparisons(b3),
        "cost": serialise_b3_cost(b3),
    }
    report["validation"] = validate_output(report, profiles, prompt_records)

    output_root.mkdir(parents=True, exist_ok=False)
    (output_root / "b4_result_review.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_jsonl(output_root / "B4_SKILL_AVAILABILITY_CENSUS.jsonl", profiles)
    write_jsonl(output_root / "B4_PROMPT_AVAILABILITY_RECORDS.jsonl", prompt_records)
    (output_root / "B4_RESULT_REVIEW.md").write_text(markdown_review(report), encoding="utf-8")
    (output_root / "B4_INFORMATION_AVAILABILITY_CENSUS.md").write_text(markdown_availability(report["availability"]), encoding="utf-8")
    (output_root / "B4_VALIDATION.json").write_text(json.dumps(report["validation"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_root": str(output_root), "validation": report["validation"]}, indent=2))


if __name__ == "__main__":
    main()
