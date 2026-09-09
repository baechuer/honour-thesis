#!/usr/bin/env python3
"""Build the source-only V7 I3 V4.1.4 operational-class repair package.

The repair is prospective and deterministic.  It replays every one of the
3,798 frozen sources, uses only source markdown structure and source-exact
evidence, and preserves the failed V4 QA package as immutable evidence.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import FIELD_KEYS, representation_row, summarize
from rq2b_common import FIELD_SPECS, normalize_whitespace, serialize_i3_flat, serialize_i3c
from validate_rq2b_v7_i3_v4_1_2_batch import (
    canonical_extraction_v4_1_2,
    validate_v4_1_2_semantics,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PACKAGE = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_merged_2026_09_09_v4_1_3"
)
FAILED_QA_PACKAGE = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_blinded_qa_final_2026_09_09_v4"
)
OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_class_repair_2026_09_09_v4_1_4"
)
MERGER_VERSION = "rq2b-v7-i3-full-corpus-v4.1.4-class-repair-v1"
SCHEMA_VERSION = "rq2b-v7-phase7-i3-class-repair-v4.1.4"
FIELD_PREFIX = {
    "use_conditions": "use_",
    "input_preconditions": "input_",
    "output_artifacts": "output_",
    "workflow_steps": "workflow_",
    "dependencies_resources": "dependency_",
    "constraints_boundaries": "boundary_",
    "success_criteria": "success_",
}
FIELD_INDEX = {field: index for index, (field, _) in enumerate(FIELD_SPECS)}

ATX_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
BOLD_HEADING = re.compile(r"^[ \t]*\*\*([^*\n]{2,120}?)\*\*:?[ \t]*$")
LIST_ITEM = re.compile(r"^(?P<indent>[ \t]*)(?:[-+*]|\d+[.)])[ \t]+")
NUMBERED_IMPERATIVE = re.compile(
    r"^(?:\d+[.)][ \t]+|step[ \t]+\d+[:.)]?[ \t]+)"
    r"(?:add|analyse|analyze|apply|build|check|choose|collect|configure|create|"
    r"deploy|determine|document|extract|generate|identify|install|load|open|"
    r"prepare|record|return|review|run|save|select|submit|test|validate|verify|write)\b",
    re.I,
)
PROHIBITION = re.compile(
    r"\b(?:do[ \t]+not|don't|must[ \t]+not|never|not[ \t]+for|when[ \t]+not[ \t]+to[ \t]+use|"
    r"belongs[ \t]+elsewhere|rather[ \t]+than[ \t]+(?:doing|completing|performing)|"
    r"use[ \t]+[^.\n]{1,100}[ \t]+instead|route[ \t]+(?:away|to))\b",
    re.I,
)
RESOURCE_ONLY = re.compile(
    r"^(?:[-+*]\s*)?(?:documentation|docs?|reference|resources?|github|website|"
    r"api[ \t]+reference|installation)\s*:?[ \t]*(?:\[[^\]]+\]\([^)]+\)|https?://\S+|\S+/\S+)",
    re.I,
)
INSTALL_RESOURCE = re.compile(
    r"\b(?:brew[ \t]+install|pipx?[ \t]+install|npm[ \t]+install|cargo[ \t]+install|"
    r"apt(?:-get)?[ \t]+install|github\.com/|https?://)\b",
    re.I,
)
NON_PROSE = re.compile(r"^(?:[-:| \t]+|```[^\n]*|~~~[^\n]*)$")

HEADING_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("constraints_boundaries", (
        "do not", "don't", "not for", "when not to use", "boundaries", "boundary",
        "limitations", "limitation", "safety", "exclusions", "excluded", "forbidden",
        "guardrails", "anti patterns", "common pitfalls",
    )),
    ("success_criteria", (
        "quality bar", "quality criteria", "acceptance", "acceptance criteria",
        "success criteria", "definition of done", "validation", "verification",
        "completion criteria", "quality checks",
    )),
    ("output_artifacts", (
        "deliverable", "deliverables", "output", "outputs", "output format",
        "artifacts", "generated files", "files created", "expected files",
        "what you produce", "final deliverable",
    )),
    ("workflow_steps", (
        "procedure", "procedures", "workflow", "steps", "instructions", "how to use",
        "process", "execution", "implementation", "method", "runbook", "playbook",
        "agenda", "approach", "research process",
    )),
    ("dependencies_resources", (
        "dependencies", "dependency", "resources", "resource", "references",
        "reference", "tools", "tooling", "external resources", "installation",
        "prerequisites & environment", "prerequisites and environment", "environment",
        "technical requirements", "required tools",
    )),
    ("input_preconditions", (
        "inputs", "input", "input requirements", "required information", "information required",
        "preconditions", "context required", "required context", "context to collect",
        "inputs to collect", "before you start", "what you need", "caller inputs",
        "provide the following information", "negotiation context",
    )),
    ("use_conditions", (
        "use when", "when to use", "use cases", "usage scenarios", "scope",
        "appropriate use", "best for", "intended use",
    )),
)


@dataclass(frozen=True)
class Heading:
    start: int
    content_start: int
    body_end: int
    level: int
    title: str
    field: str | None


@dataclass(frozen=True)
class Block:
    start: int
    end: int
    evidence: str
    field: str | None


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(values: list[dict[str, Any]]) -> bytes:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in values
    ).encode()


def load_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def clean_heading(value: str) -> str:
    value = re.sub(r"[`*_]", "", value).strip().rstrip(":")
    value = re.sub(r"^\d+(?:\.\d+)*[.)]?[ \t]+", "", value)
    return normalize_whitespace(value).lower()


def classify_heading(title: str) -> str | None:
    normalized = clean_heading(title)
    for field, phrases in HEADING_RULES:
        if any(
            normalized == phrase
            or normalized.startswith(phrase + " ")
            or normalized.endswith(" " + phrase)
            for phrase in phrases
        ):
            return field
    return None


def markdown_headings(source: str) -> list[Heading]:
    raw: list[tuple[int, int, int, str, str | None]] = []
    offset = 0
    in_frontmatter = False
    frontmatter_done = False
    in_fence = False
    fence_marker = ""
    stack: list[tuple[int, str | None]] = []
    for line in source.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        if offset == 0 and stripped.strip() == "---":
            in_frontmatter = True
            offset += len(line)
            continue
        if in_frontmatter:
            if stripped.strip() in {"---", "..."}:
                in_frontmatter = False
                frontmatter_done = True
            offset += len(line)
            continue
        fence = re.match(r"^[ \t]*(```+|~~~+)", stripped)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence, fence_marker = False, ""
            offset += len(line)
            continue
        if in_fence:
            offset += len(line)
            continue
        match = ATX_HEADING.match(stripped)
        if match:
            level, title = len(match.group(1)), match.group(2)
        else:
            match = BOLD_HEADING.match(stripped)
            if not match:
                offset += len(line)
                continue
            level, title = 7, match.group(1)
        own_field = classify_heading(title)
        while stack and stack[-1][0] >= level:
            stack.pop()
        inherited = own_field or (stack[-1][1] if stack else None)
        raw.append((offset, offset + len(line), level, title, inherited))
        stack.append((level, inherited))
        offset += len(line)
    headings: list[Heading] = []
    for index, (start, content_start, level, title, field) in enumerate(raw):
        body_end = raw[index + 1][0] if index + 1 < len(raw) else len(source)
        headings.append(Heading(start, content_start, body_end, level, title, field))
    return headings


def _line_inventory(source: str) -> list[tuple[int, int, str]]:
    inventory = []
    offset = 0
    for line in source.splitlines(keepends=True):
        inventory.append((offset, offset + len(line), line))
        offset += len(line)
    if offset < len(source):
        inventory.append((offset, len(source), source[offset:]))
    return inventory


def markdown_blocks(source: str, headings: list[Heading]) -> list[Block]:
    lines = _line_inventory(source)
    blocks: list[Block] = []
    for heading in headings:
        index = next((i for i, row in enumerate(lines) if row[0] >= heading.content_start), len(lines))
        while index < len(lines) and lines[index][0] < heading.body_end:
            start, _, line = lines[index]
            if not line.strip():
                index += 1
                continue
            block_start = start
            list_match = LIST_ITEM.match(line.rstrip("\r\n"))
            fence_match = re.match(r"^[ \t]*(```+|~~~+)", line)
            if fence_match:
                marker = fence_match.group(1)[0]
                index += 1
                while index < len(lines) and lines[index][0] < heading.body_end:
                    if re.match(rf"^[ \t]*{re.escape(marker)}{{3,}}", lines[index][2]):
                        index += 1
                        break
                    index += 1
            elif list_match:
                base_indent = len(list_match.group("indent").expandtabs(4))
                index += 1
                while index < len(lines) and lines[index][0] < heading.body_end:
                    candidate = lines[index][2].rstrip("\r\n")
                    if not candidate.strip():
                        next_nonblank = index + 1
                        while next_nonblank < len(lines) and not lines[next_nonblank][2].strip():
                            next_nonblank += 1
                        if next_nonblank >= len(lines) or lines[next_nonblank][0] >= heading.body_end:
                            break
                        next_line = lines[next_nonblank][2].rstrip("\r\n")
                        next_indent = len(next_line) - len(next_line.lstrip(" \t"))
                        if next_indent <= base_indent:
                            break
                        index = next_nonblank
                        continue
                    next_list = LIST_ITEM.match(candidate)
                    next_indent = len(candidate) - len(candidate.lstrip(" \t"))
                    if next_list and next_indent <= base_indent:
                        break
                    if next_indent <= base_indent and not candidate.startswith(("    ", "\t")):
                        break
                    index += 1
            else:
                index += 1
                while index < len(lines) and lines[index][0] < heading.body_end:
                    candidate = lines[index][2]
                    if not candidate.strip() or LIST_ITEM.match(candidate.rstrip("\r\n")):
                        break
                    index += 1
            block_end = lines[index - 1][1]
            evidence = source[block_start:block_end].strip()
            if evidence and not NON_PROSE.fullmatch(evidence):
                blocks.append(Block(block_start, block_end, evidence, heading.field))
    return blocks


def containing_block(blocks: list[Block], position: int) -> Block | None:
    for block in blocks:
        if block.start <= position < block.end:
            return block
    return None


def containing_heading(headings: list[Heading], position: int) -> Heading | None:
    candidates = [heading for heading in headings if heading.content_start <= position < heading.body_end]
    return candidates[-1] if candidates else None


def evidence_position(canonical: dict[str, Any], field: str, item: dict[str, Any], source: str) -> int:
    candidates = [
        span["source_position"]
        for span in canonical.get("retained_selector_spans", []) + canonical.get("omitted_selector_spans", [])
        if span.get("field_key") == field and span.get("item_id") == item["id"]
    ]
    return candidates[0] if candidates else source.find(item["evidence"])


def is_truncated(evidence: str, source: str, position: int) -> bool:
    stripped = evidence.strip()
    if len(normalize_whitespace(stripped)) < 18:
        return True
    end = position + len(evidence)
    if position >= 0 and end < len(source) and evidence and evidence[-1].isalnum() and source[end].isalnum():
        return True
    return bool(re.search(r"\b(?:and|or|the|a|an|to|per|see|source|not)\s*$", stripped, re.I))


def source_text_for_item(evidence: str) -> str:
    value = normalize_whitespace(evidence)
    value = re.sub(r"^(?:[-+*]|\d+[.)])[ \t]+", "", value)
    return value


def polarity_field(evidence: str, current_field: str) -> str | None:
    if current_field != "constraints_boundaries" and PROHIBITION.search(evidence):
        return "constraints_boundaries"
    return None


def special_field(evidence: str, current_field: str) -> str | None:
    normalized = normalize_whitespace(evidence)
    if current_field in {"input_preconditions", "output_artifacts"} and (
        RESOURCE_ONLY.search(normalized)
        or (len(normalized) <= 240 and INSTALL_RESOURCE.search(normalized))
    ):
        return "dependencies_resources"
    if current_field in {"success_criteria", "output_artifacts"} and NUMBERED_IMPERATIVE.search(normalized):
        return "workflow_steps"
    return None


def selection_bearing(block: Block) -> bool:
    normalized = normalize_whitespace(block.evidence)
    if len(normalized) < 16 or NON_PROSE.fullmatch(normalized):
        return False
    if normalized.startswith(("![", "<img")):
        return False
    return True


def repair_row(
    canonical: dict[str, Any], worker: dict[str, Any], source: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    headings = markdown_headings(source)
    blocks = markdown_blocks(source, headings)
    candidates: list[dict[str, Any]] = []
    action_counts: Counter[str] = Counter()
    old_items = sum(len(items) for items in worker["fields"].values())

    for old_field in FIELD_KEYS:
        for item in worker["fields"][old_field]:
            position = evidence_position(canonical, old_field, item, source)
            require(position >= 0, f"V4.1.4 old evidence absent: {canonical['skill_id']} {item['id']}")
            block = containing_block(blocks, position)
            evidence = item["evidence"]
            if block is not None and is_truncated(evidence, source, position):
                evidence = block.evidence
                position = block.start
                action_counts["expanded_truncated_block"] += 1
            heading = containing_heading(headings, position)
            new_field = heading.field if heading and heading.field else old_field
            polarity = polarity_field(evidence, new_field)
            if polarity:
                new_field = polarity
                action_counts["polarity_to_constraints"] += 1
            special = special_field(evidence, new_field)
            if special:
                new_field = special
                action_counts[f"special_to_{special}"] += 1
            if new_field != old_field:
                action_counts[f"reclassified_{old_field}_to_{new_field}"] += 1
            repaired = copy.deepcopy(item)
            if evidence != item["evidence"]:
                repaired["evidence"] = evidence
                repaired["text"] = source_text_for_item(evidence)
            candidates.append({
                "field": new_field,
                "position": position,
                "item": repaired,
                "origin": "existing_repaired",
            })

    field_counts = Counter(row["field"] for row in candidates)
    existing_evidence = {row["item"]["evidence"] for row in candidates}
    for block in blocks:
        if block.field is None or not selection_bearing(block) or block.evidence in existing_evidence:
            continue
        field = polarity_field(block.evidence, block.field) or block.field
        field = special_field(block.evidence, field) or field
        if field_counts[field] >= 16:
            continue
        candidates.append({
            "field": field,
            "position": block.start,
            "item": {
                "id": "pending",
                "text": source_text_for_item(block.evidence),
                "evidence": block.evidence,
                "evidence_status": "explicit",
                "confidence": 1,
                "selector_usefulness": "high",
            },
            "origin": "strong_heading_supplement",
        })
        existing_evidence.add(block.evidence)
        field_counts[field] += 1
        action_counts[f"supplemented_{field}"] += 1

    # Exact evidence is allowed once only.  Prefer a strong-heading assignment,
    # then stable source/field order, so the same rule replays byte-for-byte.
    candidates.sort(key=lambda row: (
        row["position"],
        0 if row["origin"] == "strong_heading_supplement" else 1,
        FIELD_INDEX[row["field"]],
        row["item"]["evidence"],
    ))
    deduplicated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        evidence = candidate["item"]["evidence"]
        if evidence in seen:
            action_counts["exact_evidence_deduplicated"] += 1
            continue
        seen.add(evidence)
        deduplicated.append(candidate)

    repaired_worker = copy.deepcopy(worker)
    repaired_worker["fields"] = {field: [] for field in FIELD_KEYS}
    per_field_ids: Counter[str] = Counter()
    for candidate in deduplicated:
        field = candidate["field"]
        per_field_ids[field] += 1
        item = candidate["item"]
        item["id"] = f"{FIELD_PREFIX[field]}{per_field_ids[field]}"
        repaired_worker["fields"][field].append(item)
    repaired_worker["absent_fields"] = sorted(
        field for field in FIELD_KEYS if not repaired_worker["fields"][field]
    )
    new_items = sum(len(items) for items in repaired_worker["fields"].values())
    changed = repaired_worker != worker
    ledger = {
        "schema_version": "rq2b-v7-i3-class-repair-ledger-v1",
        "source_row_index": canonical["source_row_index"],
        "skill_id": canonical["skill_id"],
        "source_path": canonical["source"],
        "source_sha256": canonical["source_sha256"],
        "input_worker_output_sha256": canonical["worker_output_sha256"],
        "changed": changed,
        "old_item_count": old_items,
        "new_item_count": new_items,
        "actions": dict(sorted(action_counts.items())),
    }
    return repaired_worker, ledger


def build() -> dict[str, bytes]:
    source_root = ROOT / SOURCE_PACKAGE
    qa_report_path = ROOT / FAILED_QA_PACKAGE / "qa_final_report.json"
    manifest_path = source_root / "manifest.json"
    source_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failed_qa = json.loads(qa_report_path.read_text(encoding="utf-8"))
    require(source_manifest["state"] == "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", "source V4.1.3 state mismatch")
    require(source_manifest["counts"] == {"sources": 3798, "fresh_full_corpus": 3798, "batches": 95}, "source V4.1.3 counts mismatch")
    require(failed_qa["state"].startswith("FAIL"), "bound QA report is not a failed gate")
    require(failed_qa["counts"]["major_error_rows"] == 18, "unexpected failed-QA major count")
    require(failed_qa["counts"]["critical_error_rows"] == 0, "unexpected failed-QA critical count")

    canonical_input = load_rows(source_root / "canonical_extractions.jsonl")
    worker_input = load_rows(source_root / "worker_outputs.jsonl")
    require(len(canonical_input) == len(worker_input) == 3798, "V4.1.3 row coverage mismatch")

    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    worker_rows: list[dict[str, Any]] = []
    ledger_rows: list[dict[str, Any]] = []
    aggregate_actions: Counter[str] = Counter()
    failed_sources = {row["source_sha256"] for row in failed_qa["error_details"]}
    changed_failed_sources: set[str] = set()

    for canonical_old, worker_old in zip(canonical_input, worker_input, strict=True):
        require(canonical_old["skill_id"] == worker_old["skill_id"], "canonical/worker identity mismatch")
        source_path = ROOT / canonical_old["source"]
        source_data = source_path.read_bytes()
        require(sha(source_data) == canonical_old["source_sha256"], f"source hash drift: {canonical_old['skill_id']}")
        source = source_data.decode("utf-8")
        input_row = {
            "source_row_index": canonical_old["source_row_index"],
            "skill_id": canonical_old["skill_id"],
            "family": canonical_old["family"],
            "source": canonical_old["source"],
            "source_sha256": canonical_old["source_sha256"],
            "name": canonical_old["name"],
            "description": canonical_old["description"],
            "text": source,
        }
        worker_new, ledger = repair_row(canonical_old, worker_old, source)
        canonical_new, retained, _ = canonical_extraction_v4_1_2(input_row, worker_new)
        validate_v4_1_2_semantics(input_row, worker_new)
        canonical_new["merger_version"] = MERGER_VERSION
        worker_rows.append(worker_new)
        canonical_rows.append(canonical_new)
        fielded = representation_row(
            canonical_new,
            "I3C-fielded",
            serialize_i3c(input_row["name"], input_row["description"], retained),
        )
        flat = representation_row(
            canonical_new,
            "I3-flat",
            serialize_i3_flat(input_row["name"], input_row["description"], retained),
        )
        fielded["serializer_version"] = flat["serializer_version"] = MERGER_VERSION
        fielded_rows.append(fielded)
        flat_rows.append(flat)
        ledger_rows.append(ledger)
        aggregate_actions.update(ledger["actions"])
        if ledger["changed"] and canonical_old["source_sha256"] in failed_sources:
            changed_failed_sources.add(canonical_old["source_sha256"])

    require([row["source_row_index"] for row in canonical_rows] == list(range(3798)), "source order mismatch")
    require(len({row["source_sha256"] for row in canonical_rows}) == 3798, "source identity collision")
    require(changed_failed_sources == failed_sources, "not every failed-QA source was changed by class repair")
    summary = summarize(canonical_rows, fielded_rows, flat_rows)
    require(summary["rows"] == 3798, "summary row mismatch")
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "automatic integrity failure")
    require(summary["i3c_i3flat_evidence_match_rows"] == 3798, "I3C/I3-flat evidence mismatch")

    payloads = {
        "canonical_extractions.jsonl": rows_bytes(canonical_rows),
        "i3c_fielded.jsonl": rows_bytes(fielded_rows),
        "i3_flat.jsonl": rows_bytes(flat_rows),
        "worker_outputs.jsonl": rows_bytes(worker_rows),
        "class_repair_ledger.jsonl": rows_bytes(ledger_rows),
    }
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "state": "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING",
        "formal_execution_ready": False,
        "retrieval_or_reranking_runs": 0,
        "provider_calls": 0,
        "merger_version": MERGER_VERSION,
        "counts": {"sources": 3798, "fresh_full_corpus": 3798, "batches": 95},
        "bindings": {
            "source_v4_1_3_manifest_sha256": sha(manifest_path.read_bytes()),
            "source_v4_1_3_canonical_extractions_sha256": sha((source_root / "canonical_extractions.jsonl").read_bytes()),
            "source_v4_1_3_worker_outputs_sha256": sha((source_root / "worker_outputs.jsonl").read_bytes()),
            "failed_fresh_qa_v4_report_sha256": sha(qa_report_path.read_bytes()),
            "assignment_manifest_sha256": source_manifest["bindings"]["assignment_manifest_sha256"],
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "automatic_summary": summary,
        "class_repair": {
            "rows_processed": 3798,
            "rows_changed": sum(row["changed"] for row in ledger_rows),
            "rows_unchanged": sum(not row["changed"] for row in ledger_rows),
            "failed_qa_sources_bound": len(failed_sources),
            "failed_qa_sources_changed": len(changed_failed_sources),
            "actions": dict(sorted(aggregate_actions.items())),
        },
        "artifacts": {
            name: {"sha256": sha(data), "rows": len(data.splitlines()), "utf8_bytes": len(data)}
            for name, data in payloads.items()
        },
        "semantic_qa": {
            "required": True,
            "state": "PENDING_NEW_120_ROW_SOURCE_ONLY_SAMPLE",
            "historical_sample_inherited": False,
            "failed_v4_sample_preserved": True,
            "execution_authorised": False,
        },
        "safeguards": {
            "source_only": True,
            "queries_labels_results_metrics_accessed": False,
            "provider_calls": 0,
            "retrieval_or_reranking_runs": 0,
        },
    }
    payloads["manifest.json"] = json_bytes(manifest)
    payloads["README.md"] = (
        "# V7 Phase-7 I3 V4.1.4 source-only class repair\n\n"
        "This prospective repair replays all 3,798 V4.1.3 sources. It expands clearly "
        "truncated markdown list evidence, reclassifies evidence by strong enclosing headings "
        "and polarity, and supplements bounded source-exact blocks under operational headings. "
        "The failed fresh QA v4 is bound and preserved; it is not rewritten or treated as passing.\n\n"
        "The transformation does not read queries, labels, acceptable sets, retrieval results, or "
        "metrics, and performs no provider, retrieval, or reranking calls. I3C and I3-flat are "
        "serialized from the same retained evidence sequence. A new blinded 120-row QA is required.\n\n"
        "Create: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_class_repair_v4_1_4.py`.\n\n"
        "Exact replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_class_repair_v4_1_4.py --verify`.\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payloads = build()
    output = ROOT / OUTPUT
    if args.verify:
        require(output.is_dir(), "V4.1.4 package missing")
        require({path.name for path in output.iterdir()} == set(payloads), "V4.1.4 file-set drift")
        for name, data in payloads.items():
            require((output / name).read_bytes() == data, f"V4.1.4 artifact drift: {name}")
        status = "PASS_V7_I3_V4_1_4_CLASS_REPAIR_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite V4.1.4 class repair package")
        output.mkdir(parents=True)
        for name, data in payloads.items():
            (output / name).write_bytes(data)
        status = "PASS_V7_I3_V4_1_4_CLASS_REPAIR_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
