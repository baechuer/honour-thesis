#!/usr/bin/env python3
"""Compose initial terminal dispositions with one capped cue-remediation closure.

The controller preserves every initial prompt disposition except the exact,
one-to-one cue-risk replacements recorded by the cap closure.  Thus a closure
covering only a rewritten family cannot erase initially clean all-three family
states.  It establishes local terminal state only: no final-library admission,
whole-library acceptable-set outcome, source-unique union, or metric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


PASS = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
CUE_RISK = "REMEDIATE_CUE_RISK"
ELIGIBLE = "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
UNADMITTED = "RETAIN_AS_UNADMITTED_REVIEW_RECORD"
CLAIM_BOUNDARY = (
    "Composite local terminal state only. This creates no final-library admission, "
    "whole-library acceptable-set result, source-unique union, retrieval result, or metric; "
    "the one permitted cue remediation round permits no second rewrite."
)
WORKSPACE = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_sha256(row: dict[str, Any]) -> str:
    encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSON input: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Canonical JSON object required: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSONL input: {path}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise SystemExit(f"Canonical JSONL object rows required: {path}")
    return rows


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8", newline="\n")


def require_text(row: dict[str, Any], key: str, context: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"Missing non-empty {key} in {context}: {row}")
    return value


def unique_by(rows: list[dict[str, Any]], key: str, context: str) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = require_text(row, key, context)
        if value in output:
            raise SystemExit(f"Duplicate {key} {value} in {context}")
        output[value] = row
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose initial source-native prompt dispositions with exactly one capped cue-remediation closure."
    )
    parser.add_argument("--initial-family-gates", type=Path, required=True)
    parser.add_argument("--initial-prompts", type=Path, required=True)
    parser.add_argument("--root-key", type=Path, required=True)
    parser.add_argument("--cap-closure-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--batch-label", required=True)
    parser.add_argument("--expected-families", type=int, required=True)
    parser.add_argument("--expected-initial-prompts", type=int, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_label.strip() or args.expected_families < 1 or args.expected_initial_prompts < 1:
        raise SystemExit("Batch label and expected coverage counts must be positive")
    paths = {
        "initial_family_gates": args.initial_family_gates.resolve(),
        "initial_prompts": args.initial_prompts.resolve(),
        "root_key": args.root_key.resolve(),
        "cap_summary": args.cap_closure_dir.resolve() / "summary.json",
        "cap_terminal_families": args.cap_closure_dir.resolve() / "terminal_family_dispositions.jsonl",
        "cap_terminal_prompts": args.cap_closure_dir.resolve() / "terminal_prompt_dispositions.jsonl",
    }
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Missing canonical composite input: {path}")
    out = args.output_dir.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite an existing composite closure: {out}")

    initial_prompt_rows = read_jsonl(paths["initial_prompts"])
    initial_by_prompt = unique_by(initial_prompt_rows, "prompt_token", str(paths["initial_prompts"]))
    initial_gate_rows = read_jsonl(paths["initial_family_gates"])
    initial_gate_by_family = unique_by(initial_gate_rows, "family_token", str(paths["initial_family_gates"]))
    if len(initial_gate_by_family) != args.expected_families or len(initial_by_prompt) != args.expected_initial_prompts:
        raise SystemExit("Initial terminal coverage does not match the explicit expected family/prompt counts")

    root_by_family_member: dict[tuple[str, str], str] = {}
    for row in read_jsonl(paths["root_key"]):
        family = require_text(row, "family_token", str(paths["root_key"]))
        member = require_text(row, "member_token", str(paths["root_key"]))
        source_hash = require_text(row, "canonical_source_sha256", str(paths["root_key"]))
        source_paths = row.get("source_paths")
        if (family, member) in root_by_family_member or len(source_hash) != 64 or not isinstance(source_paths, list) or len(source_paths) != 1:
            raise SystemExit("Root reconciliation key has an invalid source binding")
        source_path = WORKSPACE / source_paths[0]
        if not source_path.is_file() or sha256(source_path) != source_hash or row.get("source_byte_replay") != "PASS_SHA256_MATCH":
            raise SystemExit(f"Root key source byte binding failed: {source_path}")
        root_by_family_member[(family, member)] = source_hash

    initial_by_family: dict[str, list[dict[str, Any]]] = {}
    for row in initial_prompt_rows:
        family = require_text(row, "family_token", str(paths["initial_prompts"]))
        member = require_text(row, "intended_target_member_token", str(paths["initial_prompts"]))
        if (family, member) not in root_by_family_member:
            raise SystemExit(f"Initial prompt is not bound to a root-key source: {family}/{member}")
        initial_by_family.setdefault(family, []).append(row)
    if set(initial_by_family) != set(initial_gate_by_family) or any(len(rows) != 3 for rows in initial_by_family.values()):
        raise SystemExit("Initial prompt/family gate coverage is not exactly three prompts per family")
    for family, rows in initial_by_family.items():
        counts = dict(sorted(Counter(require_text(row, "final_prompt_disposition", str(paths["initial_prompts"])) for row in rows).items()))
        gate = initial_gate_by_family[family]
        if gate.get("prompt_count") != 3 or gate.get("prompt_disposition_counts") != counts:
            raise SystemExit(f"Initial family gate does not reproduce its prompt dispositions: {family}")

    cap_summary = read_json(paths["cap_summary"])
    cap_outputs = cap_summary.get("outputs")
    if not isinstance(cap_outputs, dict) or cap_outputs.get("terminal_family_dispositions.jsonl") != sha256(paths["cap_terminal_families"]) or cap_outputs.get("terminal_prompt_dispositions.jsonl") != sha256(paths["cap_terminal_prompts"]):
        raise SystemExit("Cap summary does not bind the supplied terminal artifacts")
    if "NO_SECOND_REWRITE" not in str(cap_summary.get("status", "")):
        raise SystemExit("Cap summary does not close the remediation round")
    cap_prompt_rows = read_jsonl(paths["cap_terminal_prompts"])
    cap_by_replaced = unique_by(cap_prompt_rows, "replaces_prompt_token", str(paths["cap_terminal_prompts"]))
    cap_tokens = unique_by(cap_prompt_rows, "terminal_prompt_token", str(paths["cap_terminal_prompts"]))
    cue_risk_tokens = {
        token for token, row in initial_by_prompt.items()
        if row.get("final_prompt_disposition") == CUE_RISK
    }
    if set(cap_by_replaced) != cue_risk_tokens:
        raise SystemExit("Cap closure must replace exactly the initial cue-risk prompts, and no other prompts")
    for old_token, cap_row in cap_by_replaced.items():
        initial = initial_by_prompt[old_token]
        family = require_text(initial, "family_token", str(paths["initial_prompts"]))
        member = require_text(initial, "intended_target_member_token", str(paths["initial_prompts"]))
        if cap_row.get("remediation_round") != 1 or cap_row.get("original_final_prompt_disposition") != CUE_RISK:
            raise SystemExit(f"Cap replacement is not the sole permitted cue remediation: {old_token}")
        if cap_row.get("original_final_record_sha256") != record_sha256(initial):
            raise SystemExit(f"Cap replacement does not bind the initial final record: {old_token}")
        if cap_row.get("family_token") != family or cap_row.get("intended_target_member_token") != member:
            raise SystemExit(f"Cap replacement changes its intended family/member: {old_token}")
        if cap_row.get("intended_target_source_sha256") != root_by_family_member[(family, member)]:
            raise SystemExit(f"Cap replacement changes its root-key source binding: {old_token}")

    cap_family_rows = read_jsonl(paths["cap_terminal_families"])
    cap_family_by_token = unique_by(cap_family_rows, "family_token", str(paths["cap_terminal_families"]))
    cap_counts = Counter(require_text(row, "family_token", str(paths["cap_terminal_prompts"])) for row in cap_prompt_rows)
    if set(cap_family_by_token) != set(cap_counts) or any(cap_counts[family] != row.get("terminal_prompt_count") for family, row in cap_family_by_token.items()):
        raise SystemExit("Cap terminal families do not exactly cover cap terminal prompts")

    composite_prompt_rows: list[dict[str, Any]] = []
    for token, initial in sorted(initial_by_prompt.items()):
        family = require_text(initial, "family_token", str(paths["initial_prompts"]))
        member = require_text(initial, "intended_target_member_token", str(paths["initial_prompts"]))
        cap_row = cap_by_replaced.get(token)
        if cap_row is None:
            terminal_token = token
            disposition = require_text(initial, "final_prompt_disposition", str(paths["initial_prompts"]))
            route = "INITIAL_FINAL_DISPOSITION_RETAINED"
        else:
            terminal_token = require_text(cap_row, "terminal_prompt_token", str(paths["cap_terminal_prompts"]))
            disposition = require_text(cap_row, "terminal_prompt_disposition", str(paths["cap_terminal_prompts"]))
            route = "ONE_TIME_CUE_REMEDIATION_REPLACEMENT"
        composite_prompt_rows.append({
            "family_token": family,
            "initial_prompt_token": token,
            "terminal_prompt_token": terminal_token,
            "terminal_route": route,
            "intended_target_member_token": member,
            "intended_target_source_sha256": root_by_family_member[(family, member)],
            "initial_final_record_sha256": record_sha256(initial),
            "initial_final_prompt_disposition": initial["final_prompt_disposition"],
            "terminal_prompt_disposition": disposition,
            "eligible_for_whole_library_acceptable_set_audit": disposition == PASS,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    if len({row["terminal_prompt_token"] for row in composite_prompt_rows}) != len(composite_prompt_rows):
        raise SystemExit("Composite terminal prompt tokens are not unique")

    composite_family_rows: list[dict[str, Any]] = []
    for family, rows in sorted({family: [row for row in composite_prompt_rows if row["family_token"] == family] for family in initial_by_family}.items()):
        members = sorted(str(row["intended_target_member_token"]) for row in rows)
        dispositions = Counter(str(row["terminal_prompt_disposition"]) for row in rows)
        all_three_pass = len(rows) == 3 and members == ["S-1", "S-2", "S-3"] and dispositions == Counter({PASS: 3})
        composite_family_rows.append({
            "family_token": family,
            "initial_family_gate_record_sha256": record_sha256(initial_gate_by_family[family]),
            "initial_family_gate_disposition": initial_gate_by_family[family]["family_disposition"],
            "terminal_family_disposition": ELIGIBLE if all_three_pass else UNADMITTED,
            "all_three_members_pass": all_three_pass,
            "terminal_prompt_count": len(rows),
            "terminal_member_tokens": members,
            "terminal_prompt_disposition_counts": dict(sorted(dispositions.items())),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    if len(composite_family_rows) != args.expected_families or sum(row["terminal_prompt_count"] for row in composite_family_rows) != args.expected_initial_prompts:
        raise SystemExit("Composite terminal coverage does not preserve all initial families/prompts")

    out.mkdir(parents=True)
    prompts_path = out / "composite_terminal_prompt_dispositions.jsonl"
    families_path = out / "composite_terminal_family_dispositions.jsonl"
    write_jsonl(prompts_path, composite_prompt_rows)
    write_jsonl(families_path, composite_family_rows)
    batch_path = out / "BATCH.md"
    batch_path.write_text("\n".join([
        f"# {args.batch_label} partial cue-remediation composite closure",
        "",
        "Initial clean terminal states are retained; only the one-to-one capped cue-risk replacements supersede their initial prompts.",
        "No second rewrite or final-library admission is created.",
        "",
        f"- Initial/terminal families: {len(composite_family_rows)}",
        f"- Initial/terminal prompts: {len(composite_prompt_rows)}",
        f"- All-three locally eligible families: {sum(row['terminal_family_disposition'] == ELIGIBLE for row in composite_family_rows)}",
        "",
    ]), encoding="utf-8", newline="\n")
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_PARTIAL_CUE_REMEDIATION_COMPOSITE_CLOSED_NO_FINAL_LIBRARY_ADMISSION_NO_SECOND_REWRITE",
        "claim_boundary": CLAIM_BOUNDARY,
        "bound_inputs": {str(path): sha256(path) for path in paths.values()},
        "counts": {
            "initial_families": len(initial_gate_by_family),
            "initial_prompts": len(initial_by_prompt),
            "one_time_cue_replacements": len(cap_by_replaced),
            "composite_terminal_families": len(composite_family_rows),
            "composite_terminal_prompts": len(composite_prompt_rows),
            "composite_terminal_family_dispositions": dict(sorted(Counter(row["terminal_family_disposition"] for row in composite_family_rows).items())),
            "composite_terminal_prompt_dispositions": dict(sorted(Counter(row["terminal_prompt_disposition"] for row in composite_prompt_rows).items())),
        },
        "outputs": {
            "composite_terminal_prompt_dispositions.jsonl": sha256(prompts_path),
            "composite_terminal_family_dispositions.jsonl": sha256(families_path),
            "BATCH.md": sha256(batch_path),
        },
    }
    write_json(out / "summary.json", summary)
    print(json.dumps({"output_dir": str(out), "status": summary["status"], "counts": summary["counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
