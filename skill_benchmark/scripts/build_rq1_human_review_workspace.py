#!/usr/bin/env python3
"""Build prospective RQ1 review packets with blind and unblinded routes."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import random
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


CORE_FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)

FIELD_LABELS = {
    "use_condition": "Use condition",
    "input_precondition": "Input / precondition",
    "output_artifact": "Output / artifact",
    "workflow_procedure": "Workflow / procedure",
    "success_verification": "Success / verification",
    "boundary_not_for": "Boundary / not-for",
    "dependency_resource": "Dependency / resource",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    write_text(path, "\n".join(canonical_json(row) for row in rows))


def relative_repo_path(repo: Path, path: Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def file_link(path: Path, label: str) -> str:
    return f"[{label}](<{path.resolve().as_posix()}>)"


def reveal_frozen_gold(
    packet_text: str,
    disclosures: list[dict[str, str]],
    intro: str,
) -> str:
    lines = packet_text.splitlines()
    first_quote = next((index for index, line in enumerate(lines) if line.startswith("> ")), None)
    if first_quote is None:
        raise RuntimeError("Review packet has no introductory blockquote")
    lines[first_quote] = f"> {intro}"
    packet_text = "\n".join(lines)
    for disclosure in disclosures:
        heading_pattern = re.compile(
            rf"^(## {re.escape(disclosure['review_id'])}(?::[^\n]*)?)$",
            re.MULTILINE,
        )
        disclosure_text = (
            f"> **Frozen gold shown for quick confirmation:** Candidate "
            f"`{disclosure['candidate_label']}` - `{disclosure['skill_id']}` "
            f"({disclosure['candidate_link']}). Choose `APPROVE` only if this "
            "candidate is still the unique fully adequate choice and the "
            "packet checks pass.\n\n"
            f"**Quick decision:** `{disclosure['review_id']} | frozen gold="
            f"{disclosure['candidate_label']} | APPROVE / REVISE / EXCLUDE | "
            "notes=`"
        )
        packet_text, replacement_count = heading_pattern.subn(
            rf"\1\n\n{disclosure_text}",
            packet_text,
            count=1,
        )
        if replacement_count != 1:
            raise RuntimeError(
                f"Missing or duplicate review marker ## {disclosure['review_id']}"
            )
    return packet_text


def display_value(value: Any) -> str:
    if isinstance(value, list):
        return "<br>".join(str(item) for item in value)
    if isinstance(value, dict):
        return "<br>".join(f"{key}: {item}" for key, item in value.items())
    return str(value)


def deterministic_labels(seed: str, count: int) -> list[str]:
    labels = [chr(ord("A") + index) for index in range(count)]
    rng_seed = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16], 16)
    random.Random(rng_seed).shuffle(labels)
    return labels


def ensure_fresh_output(output_root: Path, force: bool) -> None:
    if not output_root.exists():
        return
    ledgers = list(output_root.glob("**/review_ledger.jsonl"))
    for ledger in ledgers:
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip() and json.loads(line).get("review_status") != "PENDING":
                raise RuntimeError(
                    f"Refusing to overwrite a workspace with recorded decisions: {ledger}"
                )
    if not force:
        raise RuntimeError(f"Output already exists; rerun with --force: {output_root}")
    shutil.rmtree(output_root)


def build_controlled(repo: Path, output_root: Path) -> dict[str, Any]:
    source_root = repo / "skill_benchmark/rq1a_field_discriminability"
    review_root = output_root / "controlled"
    ledger_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    packet_paths: list[Path] = []
    confirmation_packet_paths: list[Path] = []
    review_index = 0

    for field in CORE_FIELDS:
        unit_paths = sorted((source_root / field / "clusters").glob("*/unit.json"))
        if len(unit_paths) != 50:
            raise RuntimeError(f"Expected 50 {field} units, found {len(unit_paths)}")
        for batch_start in range(0, len(unit_paths), 25):
            batch_number = batch_start // 25 + 1
            packet_path = review_root / "packets" / f"{field}_batch_{batch_number:02d}.md"
            packet_paths.append(packet_path)
            confirmation_path = review_root / "confirmation_packets" / f"{field}_confirmation_batch_{batch_number:02d}.md"
            confirmation_packet_paths.append(confirmation_path)
            disclosures: list[dict[str, str]] = []
            lines = [
                f"# Controlled Review: {FIELD_LABELS[field]} - Batch {batch_number}",
                "",
                "> Gold labels are hidden. Read each prompt and candidate view, then record one candidate label and a disposition in the ledger. Do not open `private_keys/` before this pass is complete.",
                "",
                "Allowed disposition: `APPROVE`, `REVISE`, or `EXCLUDE`.",
                "",
            ]
            for unit_path in unit_paths[batch_start : batch_start + 25]:
                review_index += 1
                review_id = f"C-{review_index:04d}"
                unit = json.loads(unit_path.read_text(encoding="utf-8"))
                skills = unit["skills"]
                shuffled_labels = deterministic_labels(review_id + unit["cluster_id"], len(skills))
                labelled_skills = list(zip(shuffled_labels, skills))
                labelled_skills.sort(key=lambda item: item[0])
                blinded_dir = review_root / "blinded_candidates" / review_id
                candidate_key: dict[str, dict[str, Any]] = {}

                for label, skill in labelled_skills:
                    field_value = skill[field]
                    candidate_key[label] = {
                        "skill_id": skill["skill_id"],
                        "is_frozen_gold": skill["skill_id"] == unit["gold_skill_id"],
                    }
                    sections = [
                        f"# Candidate {label}",
                        "",
                        "## Shared context",
                        "",
                        unit["shared_context"],
                        "",
                        f"## {FIELD_LABELS[field]}",
                        "",
                    ]
                    if isinstance(field_value, list):
                        sections.extend(f"- {item}" for item in field_value)
                    else:
                        sections.append(str(field_value))
                    write_text(blinded_dir / f"candidate_{label}.md", "\n".join(sections))

                key_payload = {
                    "review_id": review_id,
                    "cluster_id": unit["cluster_id"],
                    "candidate_key": candidate_key,
                    "frozen_gold_skill_id": unit["gold_skill_id"],
                    "source_unit_path": relative_repo_path(repo, unit_path),
                }
                commitment = sha256_bytes(canonical_json(key_payload).encode("utf-8"))
                key_rows.append({**key_payload, "gold_commitment_sha256": commitment})
                frozen_gold_label = next(
                    label
                    for label, value in candidate_key.items()
                    if value["is_frozen_gold"]
                )
                disclosures.append(
                    {
                        "review_id": review_id,
                        "candidate_label": frozen_gold_label,
                        "skill_id": unit["gold_skill_id"],
                        "candidate_link": file_link(
                            blinded_dir / f"candidate_{frozen_gold_label}.md",
                            "open frozen-gold review view",
                        ),
                    }
                )
                prompts = unit.get("prompt_variants", {"direct": unit["target_prompt"]})
                ledger_rows.append(
                    {
                        "schema_version": "RQ1_PROSPECTIVE_CONTROLLED_REVIEW_V1",
                        "review_id": review_id,
                        "field": field,
                        "cluster_id": unit["cluster_id"],
                        "source_unit_path": relative_repo_path(repo, unit_path),
                        "gold_commitment_sha256": commitment,
                        "active_review_mode": "UNBLINDED_FROZEN_GOLD_VISIBLE",
                        "frozen_gold_visible_to_reviewer": True,
                        "review_status": "PENDING",
                        "selected_candidate_label": None,
                        "unique_fully_adequate_candidate": None,
                        "alternatives_are_plausible_near_neighbours": None,
                        "non_target_information_is_shared": None,
                        "prompt_variants_preserve_intent": None,
                        "prompt_has_no_candidate_name_or_title_leak": None,
                        "reviewer": None,
                        "reviewed_at": None,
                        "notes": None,
                    }
                )

                lines.extend([f"## {review_id}: `{unit['cluster_id']}`", "", "**Prompts**", ""])
                for prompt_name, prompt_text in prompts.items():
                    lines.append(f"- `{prompt_name}`: {prompt_text}")
                lines.extend(["", f"**Shared context:** {unit['shared_context']}", "", "**Candidates**", ""])
                for label, skill in labelled_skills:
                    candidate_path = blinded_dir / f"candidate_{label}.md"
                    lines.append(
                        f"- Candidate `{label}`: {display_value(skill[field])} "
                        f"({file_link(candidate_path, 'review view')})"
                    )
                lines.extend(
                    [
                        "",
                        "**Record in ledger:** selected candidate; unique fully adequate candidate; plausible near-neighbours; non-target information shared; prompt fidelity; leakage; disposition; notes.",
                        "",
                        "---",
                        "",
                    ]
                )
            packet_text = "\n".join(lines)
            write_text(packet_path, packet_text)
            write_text(
                confirmation_path,
                reveal_frozen_gold(
                    packet_text,
                    disclosures,
                    "The frozen gold is visible for fast researcher confirmation. This is not a blinded review. Read every candidate before confirming it.",
                ),
            )

    write_jsonl(review_root / "review_ledger.jsonl", ledger_rows)
    write_jsonl(output_root / "private_keys/controlled_gold_keys.jsonl", key_rows)
    write_text(
        review_root / "README.md",
        """# Controlled RQ1 Human Review

Status: `REVIEW TRACKED IN ../STATUS.md`

Review unit: one of 350 three-sibling controlled clusters. The user-selected primary route is `confirmation_packets/`, where the frozen gold is visible. The reviewer confirms or rejects that label and separately checks near-neighbour plausibility, non-target-field equality, prompt fidelity, and leakage. Gold-hidden packets remain in `packets/` as an unused optional route.

Open `confirmation_packets/` and review one batch at a time. Decisions belong in `review_ledger.jsonl`; do not infer approval from an opened file.

Passing a row supports the wording `prospectively confirmed/reviewed by the researcher with the frozen label visible`. It does not support `blinded`, `independently reviewed`, or inter-rater agreement.
""",
    )
    return {
        "review_units": len(ledger_rows),
        "packet_files": len(packet_paths),
        "confirmation_packet_files": len(confirmation_packet_paths),
        "source_units_sha256": sha256_bytes(
            "".join(sha256_file(path) for path in sorted(source_root.glob("*/clusters/*/unit.json")) if path.parent.parent.parent.name in CORE_FIELDS).encode("utf-8")
        ),
    }


def public_family_records(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    # The review unit is the composition-family instance present in at least
    # one clean scoring case. The upstream paired pool has 199 families, but
    # five never enter a clean field denominator; 194 appear in this freeze.
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for case in freeze["cases"]:
        grouped[(case["composition_id"], case["routing_family_id"])].append(case)
    records: list[dict[str, Any]] = []
    for (composition_id, family_id), cases in grouped.items():
        base = cases[0]
        base_prompts = [(row["prompt_variant"], row["prompt"]) for row in base["prompt_variants"]]
        base_candidates = [row["skill_id"] for row in base["candidates"]]
        for case in cases[1:]:
            if case["strict_gold_skill_id"] != base["strict_gold_skill_id"]:
                raise RuntimeError(
                    f"Gold mismatch within composition-family {composition_id}/{family_id}"
                )
            if [(row["prompt_variant"], row["prompt"]) for row in case["prompt_variants"]] != base_prompts:
                raise RuntimeError(
                    f"Prompt mismatch within composition-family {composition_id}/{family_id}"
                )
            if [row["skill_id"] for row in case["candidates"]] != base_candidates:
                raise RuntimeError(
                    f"Candidate mismatch within composition-family {composition_id}/{family_id}"
                )
        records.append(base)
    return sorted(records, key=lambda row: (row["composition_id"], row["routing_family_id"]))


def build_public_gold(repo: Path, output_root: Path, freeze: dict[str, Any]) -> dict[str, Any]:
    review_root = output_root / "public_gold"
    families = public_family_records(freeze)
    if len(families) != 194:
        raise RuntimeError(f"Expected 194 scored public routing families, found {len(families)}")
    ledger_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    packet_paths: list[Path] = []
    confirmation_packet_paths: list[Path] = []

    for batch_start in range(0, len(families), 20):
        batch_number = batch_start // 20 + 1
        packet_path = review_root / "packets" / f"public_gold_batch_{batch_number:02d}.md"
        packet_paths.append(packet_path)
        confirmation_path = (
            review_root
            / "confirmation_packets"
            / f"public_gold_confirmation_batch_{batch_number:02d}.md"
        )
        confirmation_packet_paths.append(confirmation_path)
        disclosures: list[dict[str, str]] = []
        lines = [
            f"# Public Gold Review - Batch {batch_number}",
            "",
            "> Frozen gold labels and source IDs are hidden. Select the one fully adequate skill for both prompt variants. If more than one candidate is fully adequate, use `REVISE` or `EXCLUDE`; do not force a singleton.",
            "",
        ]
        for offset, case in enumerate(families[batch_start : batch_start + 20], start=batch_start + 1):
            review_id = f"P-{offset:04d}"
            candidates = case["candidates"]
            shuffled_labels = deterministic_labels(review_id + case["routing_family_id"], len(candidates))
            labelled_candidates = list(zip(shuffled_labels, candidates))
            labelled_candidates.sort(key=lambda item: item[0])
            blinded_dir = review_root / "blinded_candidates" / review_id
            candidate_key: dict[str, dict[str, Any]] = {}
            for label, candidate in labelled_candidates:
                source_path = repo / candidate["full_original"]["path"]
                if sha256_file(source_path) != candidate["full_original"]["sha256"]:
                    raise RuntimeError(f"Source hash mismatch: {source_path}")
                blinded_path = blinded_dir / f"candidate_{label}.md"
                blinded_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source_path, blinded_path)
                candidate_key[label] = {
                    "skill_id": candidate["skill_id"],
                    "source_path": candidate["full_original"]["path"],
                    "source_sha256": candidate["full_original"]["sha256"],
                    "is_frozen_gold": candidate["skill_id"] == case["strict_gold_skill_id"],
                }

            key_payload = {
                "review_id": review_id,
                "routing_family_id": case["routing_family_id"],
                "composition_id": case["composition_id"],
                "candidate_key": candidate_key,
                "frozen_gold_skill_id": case["strict_gold_skill_id"],
            }
            commitment = sha256_bytes(canonical_json(key_payload).encode("utf-8"))
            key_rows.append({**key_payload, "gold_commitment_sha256": commitment})
            frozen_gold_label = next(
                label
                for label, value in candidate_key.items()
                if value["is_frozen_gold"]
            )
            disclosures.append(
                {
                    "review_id": review_id,
                    "candidate_label": frozen_gold_label,
                    "skill_id": case["strict_gold_skill_id"],
                    "candidate_link": file_link(
                        blinded_dir / f"candidate_{frozen_gold_label}.md",
                        "open frozen-gold original",
                    ),
                }
            )
            ledger_rows.append(
                {
                    "schema_version": "RQ1_PROSPECTIVE_PUBLIC_GOLD_REVIEW_V1",
                    "review_id": review_id,
                    "routing_family_id": case["routing_family_id"],
                    "composition_id": case["composition_id"],
                    "candidate_count": len(candidates),
                    "gold_commitment_sha256": commitment,
                    "active_review_mode": "UNBLINDED_FROZEN_GOLD_VISIBLE",
                    "frozen_gold_visible_to_reviewer": True,
                    "review_status": "PENDING",
                    "selected_candidate_label": None,
                    "one_candidate_fully_adequate_for_both_prompts": None,
                    "other_candidates_are_plausible_near_neighbours": None,
                    "prompt_pair_preserves_one_intent": None,
                    "prompt_has_no_source_or_skill_name_leak": None,
                    "reviewer": None,
                    "reviewed_at": None,
                    "notes": None,
                }
            )
            lines.extend([f"## {review_id}", "", "**Prompts**", ""])
            for prompt in case["prompt_variants"]:
                lines.append(f"- `{prompt['prompt_variant']}`: {prompt['prompt']}")
            lines.extend(["", "**Candidate originals**", ""])
            for label, _candidate in labelled_candidates:
                lines.append(f"- Candidate `{label}`: {file_link(blinded_dir / f'candidate_{label}.md', 'open full original')}")
            lines.extend(
                [
                    "",
                    "**Record in ledger:** selected candidate; singleton adequacy for both prompts; near-neighbour plausibility; intent preservation; leakage; disposition; notes.",
                    "",
                    "---",
                    "",
                ]
            )
        packet_text = "\n".join(lines)
        write_text(packet_path, packet_text)
        write_text(
            confirmation_path,
            reveal_frozen_gold(
                packet_text,
                disclosures,
                "The frozen gold is visible for fast researcher confirmation. "
                "This is not a blinded review. Confirm it only after comparing "
                "all candidate originals.",
            ),
        )

    write_jsonl(review_root / "review_ledger.jsonl", ledger_rows)
    write_jsonl(output_root / "private_keys/public_gold_keys.jsonl", key_rows)
    write_text(
        review_root / "README.md",
        """# Public-Original Gold Confirmation

Status: `REVIEW TRACKED IN ../STATUS.md`

Review unit: one of 194 composition-family instances that occurs in at least one clean Round-3 scoring case. The upstream prompt/gold pool contains 199 paired families; five have no all-candidate-clear field condition and therefore never enter the scored 1,078 cases. Repeated field-removal cases within each scored family are intentionally collapsed so the researcher confirms each prompt/candidate/gold decision once.

The user-selected primary route is `confirmation_packets/`, where the frozen gold candidate and skill ID are visible. Compare every candidate original, then use `APPROVE` only when the displayed gold remains the one fully adequate skill for both prompt variants. If another candidate is better, or several candidates would satisfy the request, use `REVISE` or `EXCLUDE`. Gold-hidden packets remain in `packets/` as an unused optional route.

Approval supports the wording `prospectively confirmed/reviewed by the researcher with the frozen label visible`. It does not establish blinded review, independent annotation, inter-rater agreement, or downstream task success.
""",
    )
    return {
        "review_units": len(ledger_rows),
        "packet_files": len(packet_paths),
        "confirmation_packet_files": len(confirmation_packet_paths),
        "upstream_paired_family_pool": freeze["counts"]["paired_frozen_routing_families"],
        "families_absent_from_all_clean_field_denominators": freeze["counts"]["paired_frozen_routing_families"] - len(ledger_rows),
    }


def diff_text(full_path: Path, removed_path: Path, label: str) -> tuple[str, dict[str, Any]]:
    full_text = full_path.read_text(encoding="utf-8")
    removed_text = removed_path.read_text(encoding="utf-8")
    full_lines_for_diff = full_text.splitlines(keepends=True)
    removed_lines_for_diff = removed_text.splitlines(keepends=True)
    diff = "".join(
        difflib.unified_diff(
            full_lines_for_diff,
            removed_lines_for_diff,
            fromfile=f"{label}/full_original",
            tofile=f"{label}/field_removed",
            n=3,
        )
    )
    # The masking pipeline preserves source-line addresses. Splitting on the
    # newline delimiter keeps a final blanked source line visible even when the
    # original lacked a terminal newline and the masked file ends with one.
    full_lines = re.split(r"\r\n|\n|\r", full_text)
    removed_lines = re.split(r"\r\n|\n|\r", removed_text)
    line_count_preserved = len(full_lines) == len(removed_lines)
    changed_pairs = [
        (full_line, removed_line)
        for full_line, removed_line in zip(full_lines, removed_lines)
        if full_line != removed_line
    ]
    only_changed_to_blank = line_count_preserved and all(
        not removed_line.strip() for _full_line, removed_line in changed_pairs
    )
    return diff, {
        "full_line_count": len(full_lines),
        "removed_line_count": len(removed_lines),
        "line_count_preserved": line_count_preserved,
        "blanked_line_count": len(changed_pairs),
        "blanked_nonblank_line_count": sum(
            1 for full_line, _removed_line in changed_pairs if full_line.strip()
        ),
        "whitespace_only_normalisation_count": sum(
            1 for full_line, _removed_line in changed_pairs if not full_line.strip()
        ),
        "only_changed_source_lines_to_blank": only_changed_to_blank,
    }


def build_public_removal(repo: Path, output_root: Path, freeze: dict[str, Any]) -> dict[str, Any]:
    review_root = output_root / "public_removal"
    units: dict[str, dict[str, Any]] = {}
    for case in freeze["cases"]:
        units.setdefault(case["unit_id"], case)
    if len(units) != 402:
        raise RuntimeError(f"Expected 402 scored public removal units, found {len(units)}")
    sorted_units = sorted(units.values(), key=lambda row: (CORE_FIELDS.index(row["target_field"]), row["composition_id"]))
    ledger_rows: list[dict[str, Any]] = []
    packet_paths: list[Path] = []

    by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in sorted_units:
        by_field[case["target_field"]].append(case)

    review_index = 0
    for field in CORE_FIELDS:
        field_units = by_field[field]
        for batch_start in range(0, len(field_units), 20):
            batch_number = batch_start // 20 + 1
            packet_path = review_root / "packets" / f"{field}_batch_{batch_number:02d}.md"
            packet_paths.append(packet_path)
            lines = [
                f"# Public Removal Review: {FIELD_LABELS[field]} - Batch {batch_number}",
                "",
                "> This packet does not ask which skill should win. It asks whether the field-removal transformation faithfully removes the cited target information without adding or rewriting text. The edited skill need not remain executable.",
                "",
            ]
            for case in field_units[batch_start : batch_start + 20]:
                review_index += 1
                review_id = f"R-{review_index:04d}"
                candidate_audits: list[dict[str, Any]] = []
                combined_diffs: list[str] = []
                for candidate in case["candidates"]:
                    full_path = repo / candidate["full_original"]["path"]
                    removed_path = repo / candidate["remove_field_r3"]["path"]
                    if sha256_file(full_path) != candidate["full_original"]["sha256"]:
                        raise RuntimeError(f"Full source hash mismatch: {full_path}")
                    if sha256_file(removed_path) != candidate["remove_field_r3"]["sha256"]:
                        raise RuntimeError(f"Removed source hash mismatch: {removed_path}")
                    diff, audit = diff_text(full_path, removed_path, candidate["label"])
                    combined_diffs.append(diff or f"# {candidate['label']}: NO TEXTUAL CHANGE\n")
                    candidate_audits.append(
                        {
                            "candidate_label": candidate["label"],
                            "skill_id": candidate["skill_id"],
                            "full_original_path": candidate["full_original"]["path"],
                            "field_removed_path": candidate["remove_field_r3"]["path"],
                            "round3_clearance_status": candidate["round3_clearance_status"],
                            **audit,
                        }
                    )
                diff_path = review_root / "diffs" / field / f"{case['unit_id']}.diff"
                write_text(diff_path, "\n".join(combined_diffs))
                clearance_path = repo / case["clearance_record"]["path"]
                if sha256_file(clearance_path) != case["clearance_record"]["sha256"]:
                    raise RuntimeError(f"Clearance hash mismatch: {clearance_path}")
                ledger_rows.append(
                    {
                        "schema_version": "RQ1_PROSPECTIVE_PUBLIC_REMOVAL_REVIEW_V1",
                        "review_id": review_id,
                        "unit_id": case["unit_id"],
                        "composition_id": case["composition_id"],
                        "target_field": field,
                        "candidate_count": len(case["candidates"]),
                        "clearance_record_path": case["clearance_record"]["path"],
                        "diff_path": relative_repo_path(repo, diff_path),
                        "mechanical_line_blanking_only_for_all_candidates": all(
                            row["only_changed_source_lines_to_blank"]
                            for row in candidate_audits
                        ),
                        "candidate_audits": candidate_audits,
                        "review_status": "PENDING",
                        "target_information_removed_from_all_candidates": None,
                        "no_obvious_target_field_residue": None,
                        "candidate_identity_preserved": None,
                        "no_unlogged_addition_or_rewrite": None,
                        "reviewer": None,
                        "reviewed_at": None,
                        "notes": None,
                    }
                )
                lines.extend(
                    [
                        f"## {review_id}: `{case['unit_id']}`",
                        "",
                        f"- Composition: `{case['composition_id']}`",
                        f"- Target field: `{field}`",
                        f"- Candidate count: {len(case['candidates'])}",
                        f"- Combined diff: {file_link(diff_path, 'open deletion diff')}",
                        f"- Existing blind-clearance record: {file_link(clearance_path, 'open clearance record')}",
                        "",
                        "**Candidate documents**",
                        "",
                    ]
                )
                for candidate, audit in zip(case["candidates"], candidate_audits):
                    lines.append(
                        f"- `{candidate['label']}`: {file_link(repo / candidate['full_original']['path'], 'full')} / "
                        f"{file_link(repo / candidate['remove_field_r3']['path'], 'removed')} / "
                        f"blanked source lines `{audit['blanked_nonblank_line_count']}` / "
                        f"whitespace-only normalisations `{audit['whitespace_only_normalisation_count']}` / "
                        f"line-preserving blanking-only `{audit['only_changed_source_lines_to_blank']}`"
                    )
                lines.extend(
                    [
                        "",
                        "**Record in ledger:** target information removed; no obvious residue; identity preserved; no unlogged addition/rewrite; disposition; notes.",
                        "",
                        "---",
                        "",
                    ]
                )
            write_text(packet_path, "\n".join(lines))

    mechanical_failures = [
        row["unit_id"]
        for row in ledger_rows
        if not row["mechanical_line_blanking_only_for_all_candidates"]
    ]
    if mechanical_failures:
        raise RuntimeError(
            "Public-removal packet contains non-blanking edits: "
            + ", ".join(mechanical_failures[:10])
        )
    write_jsonl(review_root / "review_ledger.jsonl", ledger_rows)
    write_text(
        review_root / "README.md",
        """# Public-Original Removal Fidelity Review

Status: `PENDING PROSPECTIVE AUTHOR REVIEW`

Review unit: one of 402 unique composition-field transformations that occurs in the clean scoring freeze. The full technical pipeline generated and cleared 574 transformations, of which 439 were all-candidate `CLEAR`; 402 additionally had a paired prompt/gold binding and entered at least one scored case. Repeated prompt families are collapsed because the source edit is identical for those rows. Each packet links the intact originals, Round-3 field-removed documents, a diff, and the pre-existing model-assisted blind-clearance record. The implementation preserves line numbers by replacing removed source-line content with blank lines; it does not splice or rewrite the remaining text.

Approve only when the named field information has been removed from every candidate, no obvious target-field residue remains, candidate identity is preserved, and the edit contains no unlogged addition or rewrite. The edited document is allowed to be incomplete or non-executable because this experiment measures routing after information removal, not skill execution.

Approval supports `field-removal transformations were reviewed by the researcher`. It does not support independent annotation.
""",
    )
    return {
        "review_units": len(ledger_rows),
        "packet_files": len(packet_paths),
        "all_technical_units": freeze["counts"]["round3_units"],
        "all_candidate_clear_units": sum(
            row["fully_clear_units"] for row in freeze["field_summary"].values()
        ),
        "mechanical_blanking_failures": len(mechanical_failures),
    }


def build_workspace(repo: Path, output_root: Path, force: bool) -> None:
    ensure_fresh_output(output_root, force)
    output_root.mkdir(parents=True, exist_ok=True)
    freeze_path = repo / "skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_scoring_freeze/clean_only_scoring_freeze_v1.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))

    audit_paths = [
        repo / "skill_benchmark/rq1_public_original_exhaustive_ablation_v1/full_target_masks/audit/exact_diff_audit.json",
        repo / "skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_masks/audit/exact_diff_audit.json",
        repo / "skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_masks/audit/exact_diff_audit.json",
    ]
    technical_audits = []
    for audit_path in audit_paths:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        failures = audit.get("failures", [])
        if failures or "PASS" not in audit.get("status", ""):
            raise RuntimeError(f"Canonical exact-diff audit is not passing: {audit_path}")
        technical_audits.append(
            {
                "path": relative_repo_path(repo, audit_path),
                "sha256": sha256_file(audit_path),
                "status": audit["status"],
                "failure_count": len(failures),
            }
        )

    controlled_summary = build_controlled(repo, output_root)
    public_gold_summary = build_public_gold(repo, output_root, freeze)
    public_removal_summary = build_public_removal(repo, output_root, freeze)

    forbidden_blind_fields = (
        "gold_skill_id",
        "frozen_gold_skill_id",
        "strict_gold_skill_id",
        "is_frozen_gold",
        "candidate_key",
    )
    packet_paths = list((output_root / "controlled/packets").glob("*.md")) + list(
        (output_root / "public_gold/packets").glob("*.md")
    )
    blind_packet_leaks = []
    for packet_path in packet_paths:
        packet_text = packet_path.read_text(encoding="utf-8")
        if any(field in packet_text for field in forbidden_blind_fields):
            blind_packet_leaks.append(relative_repo_path(repo, packet_path))
    if blind_packet_leaks:
        raise RuntimeError(
            "Private gold fields leaked into blind packets: "
            + ", ".join(blind_packet_leaks[:10])
        )

    confirmation_packet_paths = list(
        (output_root / "controlled/confirmation_packets").glob("*.md")
    ) + list((output_root / "public_gold/confirmation_packets").glob("*.md"))
    expected_confirmation_packets = (
        controlled_summary["confirmation_packet_files"]
        + public_gold_summary["confirmation_packet_files"]
    )
    if len(confirmation_packet_paths) != expected_confirmation_packets:
        raise RuntimeError(
            "Confirmation packet count mismatch: "
            f"expected {expected_confirmation_packets}, found "
            f"{len(confirmation_packet_paths)}"
        )
    confirmation_packets_missing_gold = [
        relative_repo_path(repo, packet_path)
        for packet_path in confirmation_packet_paths
        if "Frozen gold shown for quick confirmation" not in packet_path.read_text(
            encoding="utf-8"
        )
    ]
    if confirmation_packets_missing_gold:
        raise RuntimeError(
            "Unblinded confirmation packets missing frozen-gold disclosure: "
            + ", ".join(confirmation_packets_missing_gold[:10])
        )

    manifest = {
        "schema_version": "RQ1_PROSPECTIVE_HUMAN_REVIEW_WORKSPACE_V1",
        "created_on": "2026-09-04",
        "status": "PENDING_RESEARCHER_REVIEW",
        "claim_boundary": {
            "before_completion": "Mechanically validated and model-assisted reviewed where recorded; unblinded prospective researcher confirmation pending.",
            "after_complete_author_review": "Prospectively confirmed/reviewed by the researcher with frozen labels visible.",
            "not_supported": "Blinded review, independent human annotation, inter-rater agreement, or downstream task correctness.",
        },
        "source_freeze": {
            "path": relative_repo_path(repo, freeze_path),
            "sha256": sha256_file(freeze_path),
        },
        "technical_exact_diff_audits": technical_audits,
        "blind_packet_private_field_leaks": len(blind_packet_leaks),
        "unblinded_confirmation_packet_count": len(confirmation_packet_paths),
        "unblinded_confirmation_packets_missing_gold": len(
            confirmation_packets_missing_gold
        ),
        "controlled": controlled_summary,
        "public_gold": public_gold_summary,
        "public_removal": public_removal_summary,
        "total_review_units": controlled_summary["review_units"]
        + public_gold_summary["review_units"]
        + public_removal_summary["review_units"],
    }
    write_json(output_root / "manifest.json", manifest)
    write_text(
        output_root / "VALIDATION.md",
        f"""# RQ1 Review Workspace Validation

Date: 2026-09-04
Status: `PASS / SCIENTIFIC DECISIONS STILL PENDING`

- JSONL review units: controlled `{controlled_summary['review_units']}`, public gold `{public_gold_summary['review_units']}`, public removal `{public_removal_summary['review_units']}`.
- All generated decisions begin as `PENDING`.
- Public removal transformations failing line-preserving blanking-only validation: `{public_removal_summary['mechanical_blanking_failures']}`.
- Blind controlled/public-gold packets containing private gold-key field names: `{len(blind_packet_leaks)}`.
- Unblinded controlled/public-gold confirmation packets generated: `{len(confirmation_packet_paths)}`.
- Unblinded confirmation packets missing their frozen-gold disclosure: `{len(confirmation_packets_missing_gold)}`.
- Canonical source-to-Round-1, Round-1-to-Round-2, and Round-2-to-Round-3 exact-diff audit records all report `PASS` with zero listed failures.
- Source freeze SHA-256: `{sha256_file(freeze_path)}`.

This validates package integrity and transformation mechanics only. Showing a frozen gold label does not approve it. It does not establish absence of all semantic residue or convert a `PENDING` row into researcher confirmation.
""",
    )
    write_text(
        output_root / "STATUS.md",
        f"""# RQ1 Human Review Status

Date: 2026-09-04

| Review stream | Units | Completed | Pending | Current claim |
| --- | ---: | ---: | ---: | --- |
| Controlled field-isolation | {controlled_summary['review_units']} | 0 | {controlled_summary['review_units']} | Retrospective author confirmation exists; unblinded prospective confirmation pending. |
| Public strict gold | {public_gold_summary['review_units']} | 0 | {public_gold_summary['review_units']} | Model-assisted/source-grounded checks exist; unblinded prospective gold confirmation pending. |
| Public removal fidelity | {public_removal_summary['review_units']} | 0 | {public_removal_summary['review_units']} | Mechanical and model-assisted clearance exists; prospective human transformation review pending. |
| **Total** | **{manifest['total_review_units']}** | **0** | **{manifest['total_review_units']}** | Do not claim completed researcher confirmation yet. |

This file is a generated starting state. A row counts as completed only after its ledger contains the reviewer, date, decision, and required judgements. Opening a packet is not approval.
""",
    )
    write_text(
        output_root / "README.md",
        """# RQ1 Prospective Human Review Workspace

Status: `READY FOR REVIEW / SEE STATUS.md FOR LIVE COUNTS`

This workspace separates three validity questions that were previously easy to blur:

1. `controlled/`: Is the frozen gold uniquely supported by the prompt, are the alternatives genuine near-neighbours, and is the tested field really isolated?
2. `public_gold/`: Does each natural prompt pair have one fully adequate public original among its candidate set?
3. `public_removal/`: Did the source edit remove the named information faithfully from every candidate without adding or rewriting text?

## Review order

Start with `public_gold/confirmation_packets/public_gold_confirmation_batch_01.md`. This is the user-selected fast route: each case displays the frozen gold candidate and skill ID. Compare it with every other candidate, then confirm, revise, or exclude the case. Continue through all ten public-gold confirmation batches, then review `controlled/confirmation_packets/` field by field. Review public-removal fidelity last because it is the largest stream and does not adjudicate the gold label.

For each row, write one disposition to the corresponding `review_ledger.jsonl`:

- `APPROVE`: every required judgement passes.
- `REVISE`: the case could be retained after a recorded prompt, label, or transformation correction. A revised case must be rerun if the scientific input changes.
- `EXCLUDE`: no defensible repair exists without redesigning the case.

The `packets/` directories preserve an optional gold-hidden route, but they are not the active review workflow. The `private_keys/` directory preserves frozen commitments and reconciliation keys for auditability; the confirmation packets reveal only the gold needed for quick review.

## Claim boundary

After Jacky completes and signs the ledgers, the thesis may truthfully state that the relevant benchmark units were `prospectively confirmed/reviewed by the researcher with frozen labels visible`. It may not call this process blinded or independent, report inter-rater agreement, or imply external validation unless another human completes a separately recorded review.

The earlier `rq1a_field_discriminability/human_review_2026-08-30/` receipt remains historical evidence of retrospective author confirmation. It is not erased and is not treated as this prospective review.
""",
    )
    write_text(
        output_root / "REVIEW_GUIDE.md",
        """# RQ1 Review Guide

All rows begin as `PENDING`. The active confirmation packets display the frozen gold. Read every candidate, then send or record one decision per review ID. A convenient response format is:

```text
P-0001 | frozen gold=B | APPROVE | notes=gold is the unique fully adequate candidate
```

Use `APPROVE` only when the displayed frozen gold is still the unique fully adequate candidate for both prompts after comparison with every alternative. Use `REVISE` when another candidate is better or the prompt/candidate set needs repair. Use `EXCLUDE` when multiple candidates are fully adequate or no defensible singleton exists.

For controlled rows, also judge whether non-target information is shared. For removal rows there is no gold confirmation: judge whether the named information is absent from every edited candidate, no obvious residue remains, identity is preserved, and no text was added or rewritten.

Use `REVISE` when the unit could be repaired but changing a prompt, gold label, candidate set, or source edit would alter the scientific input. Such a row must be rerun after repair. Use `EXCLUDE` when no defensible repair exists. Never force a singleton when several public skills fully satisfy the same request.

The first batch is `public_gold/confirmation_packets/public_gold_confirmation_batch_01.md`. Because the frozen answer is visible, this workflow is prospective researcher confirmation rather than blind adjudication; record that limitation explicitly.
""",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="skill_benchmark/rq1_human_review/2026-09-04")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    output_root = repo / args.output
    build_workspace(repo, output_root, args.force)


if __name__ == "__main__":
    main()
