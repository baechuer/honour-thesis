#!/usr/bin/env python3
"""Build the second prospective source-only V7 I3 class repair (V4.1.5).

V4.1.5 repairs the classes exposed by the preserved failed QA v5.  It
replays every V4.1.4 row, completes evidence against full-document markdown
blocks, interprets explicit inline context cues, removes non-operational
template fragments, and does not cap dependency/resource or input lists.
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

import build_rq2b_v7_i3_class_repair_v4_1_4 as prior
from merge_rq2b_i3c import FIELD_KEYS, representation_row, summarize
from rq2b_common import FIELD_SPECS, normalize_whitespace, serialize_i3_flat, serialize_i3c
from validate_rq2b_v7_i3_v4_1_2_batch import (
    canonical_extraction_v4_1_2,
    validate_v4_1_2_semantics,
)
from validate_rq2b_v7_i3_v4_1_batch import NOT_FOR_USE


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PACKAGE = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_class_repair_2026_09_09_v4_1_4"
)
FAILED_QA_REPORT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_blinded_qa_final_2026_09_09_v5/qa_final_report.json"
)
OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_class_repair_2026_09_09_v4_1_5"
)
MERGER_VERSION = "rq2b-v7-i3-full-corpus-v4.1.5-class-repair-v1"
SCHEMA_VERSION = "rq2b-v7-phase7-i3-class-repair-v4.1.5"
LEDGER_SCHEMA = "rq2b-v7-i3-class-repair-ledger-v4.1.5"
FIELD_INDEX = {field: index for index, (field, _) in enumerate(FIELD_SPECS)}

ATX_HEADING = prior.ATX_HEADING
BOLD_HEADING = prior.BOLD_HEADING
LIST_ITEM = prior.LIST_ITEM
NON_PROSE = prior.NON_PROSE

PURE_RESOURCE_LINK = re.compile(
    r"^(?:[-+*]\s*)?(?:\[[^\]]+\]\([^)]+\)|https?://\S+)(?:\s*[-—:]\s*[^.]+)?$",
    re.I,
)
USE_CUE = re.compile(
    r"^(?:[-+*]\s*)?(?:use\s+(?:this\s+)?(?:skill\s+)?(?:when|for)\b|"
    r"when\s+to\s+use\b|trigger\s*:)",
    re.I,
)
INPUT_LABEL = re.compile(
    r"^(?:[-+*]\s*)?(?:full|short|embed|shorts|video)?\s*url\s*:|"
    r"^(?:[-+*]\s*)?(?:caller|user|project|source)\s+(?:input|context)\s*:",
    re.I,
)
OUTPUT_TOKEN = re.compile(
    r"\b(?:packet|file|report|brief|checklist|manifest|ledger|map|timeline|"
    r"transcript|subtitle|frontmatter|artifact|deliverable|output)\b",
    re.I,
)
HARD_PROHIBITION = re.compile(
    r"^(?:[-+*]\s*|\d+[.)]\s*)?(?:do\s+not|don't|never|must\s+not|not\s+for)\b|"
    r"\bdo\s+not\s+use\b",
    re.I,
)
ROUTE_OUT = re.compile(r"^(?:[-+*]\s*)?for\s+[^.]{1,120},\s*use\s+", re.I)
OPERATIONAL_VERB = re.compile(
    r"\b(?:add|analyse|analyze|apply|ask|build|check|choose|collect|compare|"
    r"configure|create|deploy|derive|determine|document|emit|ensure|estimate|"
    r"extract|flag|generate|identify|include|inspect|install|keep|load|map|"
    r"measure|normalize|open|place|prepare|prioritize|read|record|recommend|"
    r"return|review|run|save|select|separate|set|structure|submit|test|"
    r"translate|use|validate|verify|write)\b",
    re.I,
)
BARE_TEMPLATE_LABEL = re.compile(
    r"^(?:[-+*]\s*)?(?:slide|impact|visual\s+or\s+communication\s+issue|"
    r"recommended\s+(?:adjustment|change)|clause(?:\s*/\s*section)?|"
    r"location|finding|issue|risk\s+rating|summary|status)\s*:?[ 	]*$",
    re.I,
)
VERSION_FRAGMENT = re.compile(r"(?:>=?\s*)?\d+\.$|\bAPI\s+\d+\.$", re.I)


@dataclass(frozen=True)
class ContextBlock:
    start: int
    end: int
    evidence: str
    field: str | None
    kind: str
    heading_title: str
    context_reason: str


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


def clean_label(value: str) -> str:
    value = normalize_whitespace(value)
    value = re.sub(r"^(?:[-+*]|\d+[.)])\s+", "", value)
    value = re.sub(r"[`*_#]", "", value).strip().rstrip(":")
    value = re.sub(r"^step\s+\d+(?:\.\d+)*\s*[:.)-]?\s*", "", value, flags=re.I)
    return value.lower()


def classify_heading(title: str) -> str | None:
    normalized = clean_label(title)
    extended: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("dependencies_resources", (
            "related skill", "related skills", "references", "reference links", "prerequisite",
            "prerequisites", "requirements and dependencies",
        )),
        ("input_preconditions", (
            "gather", "gather context", "gather the minimum context", "required information",
            "information to provide", "provide the following information", "if you need more context",
            "before starting", "before you begin", "before you start", "initial assessment",
        )),
        ("output_artifacts", (
            "return format", "response format", "return packet", "packet types", "output files",
            "file naming", "output packet", "final output",
        )),
        ("use_conditions", ("trigger", "triggers", "use this skill when", "invocation")),
        ("success_criteria", ("goal", "goals", "key metrics", "metrics")),
        ("workflow_steps", ("typical sequence",)),
    )
    for field, phrases in extended:
        if any(
            normalized == phrase
            or normalized.startswith(phrase + " ")
            or normalized.endswith(" " + phrase)
            for phrase in phrases
        ):
            return field
    # A content catalogue titled "... Reference" is not itself a resource
    # section.  Only explicit API/command/reference-link headings carry the
    # dependency meaning.
    if normalized.endswith(" reference") and normalized not in {
        "api reference", "command reference", "reference links", "quick reference",
    }:
        return None
    return prior.classify_heading(title)


def markdown_headings(source: str) -> list[prior.Heading]:
    raw: list[tuple[int, int, int, str, str | None]] = []
    offset = 0
    in_frontmatter = False
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
    return [
        prior.Heading(start, content_start, raw[index + 1][0] if index + 1 < len(raw) else len(source), level, title, field)
        for index, (start, content_start, level, title, field) in enumerate(raw)
    ]


def inline_context(value: str) -> tuple[str | None, str | None, str]:
    """Return own-field, following-field, and rule for an inline cue."""
    normalized = clean_label(value)
    rules: tuple[tuple[str, tuple[str, ...], str], ...] = (
        ("input_preconditions", (
            "provide the following information", "if you need more context", "gather",
            "gather context", "gather the minimum context", "required information",
            "before you start", "before starting", "before you begin",
        ), "inline_input_context"),
        ("dependencies_resources", ("related skill", "related skills", "resources", "references"), "inline_dependency_context"),
        ("use_conditions", ("trigger", "triggers"), "inline_trigger_context"),
        ("success_criteria", ("goal", "goals", "key metrics", "metrics"), "inline_success_context"),
        ("workflow_steps", ("typical sequence",), "inline_workflow_context"),
        ("output_artifacts", (
            "return one of these packet types", "return one of the following packet types",
            "packet types", "output files", "file naming", "deliverables", "outputs",
            "every answer should include", "every output must include",
        ), "inline_output_context"),
        ("use_conditions", (
            "task-estimation owns", "this skill owns", "recommend a split when",
            "recommend a spike when",
        ), "inline_use_context"),
    )
    label = normalized.split(":", 1)[0].strip()
    for field, phrases, reason in rules:
        if any(label == phrase or label.startswith(phrase + " ") for phrase in phrases):
            own = "workflow_steps" if label.startswith("return one of") else field
            return own, field, reason
    return None, None, ""


def _line_inventory(source: str) -> list[tuple[int, int, str]]:
    values: list[tuple[int, int, str]] = []
    offset = 0
    for line in source.splitlines(keepends=True):
        values.append((offset, offset + len(line), line))
        offset += len(line)
    return values


def document_blocks(source: str) -> tuple[list[prior.Heading], list[ContextBlock]]:
    """Parse logical blocks across the full markdown body, not only known headings."""
    headings = markdown_headings(source)
    heading_by_start = {heading.start: heading for heading in headings}
    lines = _line_inventory(source)
    blocks: list[ContextBlock] = []
    inline_field: str | None = None
    inline_consumed_list = False
    index = 0
    in_frontmatter = bool(lines and lines[0][2].strip() == "---")
    while index < len(lines):
        start, _, line = lines[index]
        stripped = line.rstrip("\r\n")
        if in_frontmatter:
            if index > 0 and stripped.strip() in {"---", "..."}:
                in_frontmatter = False
            index += 1
            continue
        if start in heading_by_start:
            inline_field = None
            inline_consumed_list = False
            index += 1
            continue
        if not stripped.strip() or re.fullmatch(r"\s*(?:---+|\*\*\*+)\s*", stripped):
            index += 1
            continue
        own_inline, following_inline, inline_reason = inline_context(stripped)
        if inline_field is not None and inline_consumed_list and LIST_ITEM.match(stripped) is None and own_inline is None:
            inline_field = None
            inline_consumed_list = False
        heading = prior.containing_heading(headings, start)
        base_field = inline_field or (heading.field if heading else None)
        heading_title = heading.title if heading else ""
        field = own_inline or base_field
        kind = "paragraph"
        block_start = start
        fence = re.match(r"^[ \t]*(```+|~~~+)", stripped)
        list_match = LIST_ITEM.match(stripped)
        if fence:
            kind = "fence"
            marker = fence.group(1)[0]
            index += 1
            while index < len(lines):
                if re.match(rf"^[ \t]*{re.escape(marker)}{{3,}}", lines[index][2]):
                    index += 1
                    break
                index += 1
        elif stripped.lstrip().startswith("|"):
            kind = "table"
            index += 1
        elif list_match:
            kind = "list_item"
            base_indent = len(list_match.group("indent").expandtabs(4))
            index += 1
            while index < len(lines):
                candidate = lines[index][2].rstrip("\r\n")
                if not candidate.strip():
                    break
                if lines[index][0] in heading_by_start:
                    break
                next_list = LIST_ITEM.match(candidate)
                next_indent = len(candidate) - len(candidate.lstrip(" \t"))
                if next_list and next_indent <= base_indent:
                    break
                if next_indent <= base_indent and not candidate.startswith(("    ", "\t")):
                    break
                index += 1
        else:
            index += 1
            while index < len(lines):
                candidate_start, _, candidate_line = lines[index]
                candidate = candidate_line.rstrip("\r\n")
                if (
                    not candidate.strip()
                    or candidate_start in heading_by_start
                    or LIST_ITEM.match(candidate)
                    or candidate.lstrip().startswith("|")
                    or re.match(r"^[ \t]*(```+|~~~+)", candidate)
                    or inline_context(candidate)[0] is not None
                ):
                    break
                index += 1
        block_end = lines[index - 1][1]
        evidence = source[block_start:block_end].strip()
        if evidence and not NON_PROSE.fullmatch(evidence):
            blocks.append(ContextBlock(
                block_start,
                block_end,
                evidence,
                field,
                kind,
                heading_title,
                inline_reason or ("inline_carry" if inline_field else "heading" if heading and heading.field else "unclassified"),
            ))
        if following_inline is not None:
            inline_field = following_inline
            inline_consumed_list = False
        elif list_match and inline_field is not None:
            inline_consumed_list = True
    return headings, blocks


def all_occurrences(source: str, evidence: str) -> list[int]:
    starts: list[int] = []
    cursor = source.find(evidence)
    while cursor >= 0:
        starts.append(cursor)
        cursor = source.find(evidence, cursor + 1)
    return starts


def choose_block(
    blocks: list[ContextBlock], source: str, evidence: str, old_field: str, hint: int
) -> tuple[int, ContextBlock | None]:
    occurrences = all_occurrences(source, evidence)
    require(bool(occurrences), "old evidence absent from source")
    ranked: list[tuple[tuple[int, int, int, int], int, ContextBlock | None]] = []
    for position in occurrences:
        block = next((value for value in blocks if value.start <= position < value.end), None)
        score = (
            1 if block and block.field == old_field else 0,
            1 if block and block.field is not None else 0,
            1 if block and block.kind not in {"fence", "table"} else 0,
            -abs(position - hint),
        )
        ranked.append((score, position, block))
    _, position, block = max(ranked, key=lambda row: (row[0], -row[1]))
    return position, block


def source_text_for_item(evidence: str) -> str:
    value = normalize_whitespace(evidence)
    return re.sub(r"^(?:[-+*]|\d+[.)])\s+", "", value)


def special_field(evidence: str, current_field: str | None, block: ContextBlock | None) -> str | None:
    normalized = normalize_whitespace(evidence)
    if HARD_PROHIBITION.search(normalized) or ROUTE_OUT.search(normalized):
        return "constraints_boundaries"
    if USE_CUE.search(normalized):
        return "constraints_boundaries" if NOT_FOR_USE.search(normalized) else "use_conditions"
    if INPUT_LABEL.search(normalized) or normalized.rstrip().endswith("?") and block and block.field == "input_preconditions":
        return "input_preconditions"
    if PURE_RESOURCE_LINK.fullmatch(normalized):
        return "dependencies_resources"
    if block and block.field:
        if block.field == "use_conditions" and NOT_FOR_USE.search(normalized):
            return "constraints_boundaries"
        return block.field
    if prior.PROHIBITION.search(normalized) or NOT_FOR_USE.search(normalized):
        return "constraints_boundaries"
    if current_field in {"input_preconditions", "output_artifacts"} and (
        prior.RESOURCE_ONLY.search(normalized)
        or (len(normalized) <= 240 and prior.INSTALL_RESOURCE.search(normalized))
    ):
        return "dependencies_resources"
    if prior.NUMBERED_IMPERATIVE.search(normalized):
        return "workflow_steps"
    return current_field


def non_selection_fragment(evidence: str, field: str, block: ContextBlock | None) -> str | None:
    normalized = normalize_whitespace(evidence)
    plain = re.sub(r"^(?:[-+*]|\d+[.)])\s+", "", normalized).strip(" `*_|")
    if block and block.kind == "fence" and field == "output_artifacts":
        interior = re.sub(r"^(?:```|~~~)[^\n]*\n?|(?:```|~~~)\s*$", "", evidence.strip(), flags=re.M).strip()
        return None if interior else "formatting_only"
    if not plain or plain == "*" or NON_PROSE.fullmatch(normalized):
        return "formatting_only"
    if BARE_TEMPLATE_LABEL.fullmatch(normalized):
        return "bare_table_or_template_label"
    if block and block.kind == "table":
        cells = [cell.strip() for cell in normalized.strip("|").split("|")]
        header_words = {
            "format", "extension", "description", "operation", "method", "key parameters",
            "variable", "default", "required", "field", "column", "value",
        }
        if all(re.fullmatch(r"[-: ]+", cell) for cell in cells) or all(
            clean_label(cell) in header_words for cell in cells
        ):
            return "bare_table_or_template_label"
    if field == "workflow_steps":
        if PURE_RESOURCE_LINK.fullmatch(normalized):
            return None
        if OUTPUT_TOKEN.search(plain) and block and block.field == "output_artifacts":
            return None
        if len(plain.split()) <= 14 and not OPERATIONAL_VERB.search(plain):
            return "non_operational_workflow_fragment"
    return None


def complete_evidence(evidence: str, block: ContextBlock | None) -> tuple[str, bool]:
    if block is None or (block.kind == "fence" and block.field != "output_artifacts") or evidence == block.evidence:
        return evidence, False
    normalized = normalize_whitespace(evidence)
    block_normalized = normalize_whitespace(block.evidence)
    fragment = (
        VERSION_FRAGMENT.search(normalized) is not None
        or len(normalized) < 24
        or normalized in block_normalized
    )
    if fragment:
        return block.evidence, True
    return evidence, False


def repair_row(
    canonical: dict[str, Any], worker: dict[str, Any], source: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    _, blocks = document_blocks(source)
    candidates: list[dict[str, Any]] = []
    actions: Counter[str] = Counter()
    old_items = sum(len(items) for items in worker["fields"].values())

    for old_field in FIELD_KEYS:
        for item in worker["fields"][old_field]:
            hint = prior.evidence_position(canonical, old_field, item, source)
            position, block = choose_block(blocks, source, item["evidence"], old_field, hint)
            evidence, completed = complete_evidence(item["evidence"], block)
            if completed:
                position = block.start if block else position
                actions["expanded_to_complete_full_document_block"] += 1
            new_field = special_field(evidence, old_field, block) or old_field
            if new_field != old_field:
                actions[f"reclassified_{old_field}_to_{new_field}"] += 1
            omission = non_selection_fragment(evidence, new_field, block)
            if omission:
                actions[f"removed_{omission}"] += 1
                continue
            repaired = copy.deepcopy(item)
            repaired["evidence"] = evidence
            repaired["text"] = source_text_for_item(evidence)
            candidates.append({
                "field": new_field,
                "position": position,
                "item": repaired,
                "origin": "existing_repaired",
            })

    existing_normalized = {normalize_whitespace(row["item"]["evidence"]) for row in candidates}
    field_normalized = {
        field: {normalize_whitespace(row["item"]["evidence"]) for row in candidates if row["field"] == field}
        for field in FIELD_KEYS
    }
    bounded_caps = {
        "use_conditions": 24,
        "output_artifacts": 24,
        "workflow_steps": 32,
        "constraints_boundaries": 24,
        "success_criteria": 24,
    }
    for block in blocks:
        if block.field is None or (block.kind == "fence" and block.field != "output_artifacts"):
            continue
        field = special_field(block.evidence, block.field, block) or block.field
        omission = non_selection_fragment(block.evidence, field, block)
        if omission:
            continue
        normalized = normalize_whitespace(block.evidence)
        if normalized in existing_normalized:
            continue
        cap = bounded_caps.get(field)
        if cap is not None and len(field_normalized[field]) >= cap:
            actions[f"bounded_supplement_cap_reached_{field}"] += 1
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
            "origin": "full_document_structural_supplement",
        })
        existing_normalized.add(normalized)
        field_normalized[field].add(normalized)
        actions[f"supplemented_{field}"] += 1
        if field in {"dependencies_resources", "input_preconditions"}:
            actions[f"uncapped_list_item_{field}"] += 1

    # Prefer a structurally classified full block over an inherited item when
    # two candidates normalize to the same selector evidence.
    candidates.sort(key=lambda row: (
        row["position"],
        0 if row["origin"] == "full_document_structural_supplement" else 1,
        FIELD_INDEX[row["field"]],
        row["item"]["evidence"],
    ))
    deduplicated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = normalize_whitespace(candidate["item"]["evidence"])
        if normalized in seen:
            actions["normalized_evidence_deduplicated"] += 1
            continue
        seen.add(normalized)
        deduplicated.append(candidate)

    repaired_worker = copy.deepcopy(worker)
    repaired_worker["fields"] = {field: [] for field in FIELD_KEYS}
    per_field_ids: Counter[str] = Counter()
    for candidate in deduplicated:
        field = candidate["field"]
        per_field_ids[field] += 1
        item = candidate["item"]
        item["id"] = f"{prior.FIELD_PREFIX[field]}{per_field_ids[field]}"
        repaired_worker["fields"][field].append(item)
    repaired_worker["absent_fields"] = sorted(
        field for field in FIELD_KEYS if not repaired_worker["fields"][field]
    )
    ledger = {
        "schema_version": LEDGER_SCHEMA,
        "source_row_index": canonical["source_row_index"],
        "skill_id": canonical["skill_id"],
        "source_path": canonical["source"],
        "source_sha256": canonical["source_sha256"],
        "input_worker_output_sha256": canonical["worker_output_sha256"],
        "changed": repaired_worker != worker,
        "old_item_count": old_items,
        "new_item_count": sum(len(items) for items in repaired_worker["fields"].values()),
        "actions": dict(sorted(actions.items())),
    }
    return repaired_worker, ledger


def build() -> dict[str, bytes]:
    source_root = ROOT / SOURCE_PACKAGE
    source_manifest_path = source_root / "manifest.json"
    failed_qa_path = ROOT / FAILED_QA_REPORT
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    failed_qa = json.loads(failed_qa_path.read_text(encoding="utf-8"))
    require(source_manifest["state"] == "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", "source V4.1.4 state mismatch")
    require(source_manifest["counts"] == {"sources": 3798, "fresh_full_corpus": 3798, "batches": 95}, "source V4.1.4 counts mismatch")
    require(failed_qa["state"] == "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE", "bound QA v5 is not the preserved failed gate")
    require(failed_qa["counts"]["major_error_rows"] == 13, "unexpected QA v5 major count")
    require(failed_qa["counts"]["critical_error_rows"] == 0, "unexpected QA v5 critical count")

    canonical_input = load_rows(source_root / "canonical_extractions.jsonl")
    worker_input = load_rows(source_root / "worker_outputs.jsonl")
    require(len(canonical_input) == len(worker_input) == 3798, "V4.1.4 row coverage mismatch")
    failed_sources = {row["source_sha256"] for row in failed_qa["error_details"]}

    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    worker_rows: list[dict[str, Any]] = []
    ledger_rows: list[dict[str, Any]] = []
    aggregate_actions: Counter[str] = Counter()
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
    require(changed_failed_sources == failed_sources, "not every failed-QA-v5 source changed")
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
            "source_v4_1_4_manifest_sha256": sha(source_manifest_path.read_bytes()),
            "source_v4_1_4_canonical_extractions_sha256": sha((source_root / "canonical_extractions.jsonl").read_bytes()),
            "source_v4_1_4_worker_outputs_sha256": sha((source_root / "worker_outputs.jsonl").read_bytes()),
            "failed_fresh_qa_v5_report_sha256": sha(failed_qa_path.read_bytes()),
            "assignment_manifest_sha256": source_manifest["bindings"]["assignment_manifest_sha256"],
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "automatic_summary": summary,
        "class_repair": {
            "rows_processed": 3798,
            "rows_changed": sum(row["changed"] for row in ledger_rows),
            "rows_unchanged": sum(not row["changed"] for row in ledger_rows),
            "failed_qa_v5_sources_bound": len(failed_sources),
            "failed_qa_v5_sources_changed": len(changed_failed_sources),
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
            "failed_v5_sample_preserved": True,
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
        "# V7 Phase-7 I3 V4.1.5 source-only class repair\n\n"
        "This second prospective class repair replays all 3,798 V4.1.4 sources. "
        "It completes selector evidence against full-document markdown blocks, uses "
        "explicit inline context cues, removes bare template fragments, routes source-exact "
        "resource links and output packet/file labels, and leaves dependency/resource and "
        "input lists uncapped. The failed QA v5 is bound and preserved.\n\n"
        "No query, label, acceptable set, result, metric, or provider output is read. "
        "I3C and I3-flat are serialized from one retained evidence sequence. A fresh "
        "blinded 120-row QA is still required.\n\n"
        "Create: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_class_repair_v4_1_5.py`.\n\n"
        "Exact replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_class_repair_v4_1_5.py --verify`.\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payloads = build()
    output = ROOT / OUTPUT
    if args.verify:
        require(output.is_dir(), "V4.1.5 package missing")
        require({path.name for path in output.iterdir()} == set(payloads), "V4.1.5 file-set drift")
        for name, data in payloads.items():
            require((output / name).read_bytes() == data, f"V4.1.5 artifact drift: {name}")
        status = "PASS_V7_I3_V4_1_5_CLASS_REPAIR_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite V4.1.5 class repair package")
        output.mkdir(parents=True)
        for name, data in payloads.items():
            (output / name).write_bytes(data)
        status = "PASS_V7_I3_V4_1_5_CLASS_REPAIR_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
