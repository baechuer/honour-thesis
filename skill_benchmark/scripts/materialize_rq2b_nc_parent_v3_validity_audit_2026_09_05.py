#!/usr/bin/env python3
"""Prepare blinded validity-audit packets for immutable, affected V3 parents."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
PHASE3 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
ADJ = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_prompt_cue_adjudication_2026-09-05_v2"
V3 = BENCHMARK / "rq2b_full_library/rq2b-i3c-v3-2026-08-18"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_parent_v3_validity_audit_2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def redact_source(text: str) -> str:
    """Hide source identity; preserve operational source evidence for blind audit."""
    text = re.sub(r"(?ms)^---\n.*?\n---\n?", "", text)
    text = re.sub(r"(?m)^#\s+.*$", "# [redacted source heading]", text)
    text = re.sub(r"https?://\S+", "[redacted-url]", text)
    text = re.sub(r"(?im)^\s*(author|provider|repository|source path)\s*:\s*.*$", "[redacted identity metadata]", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite parent-V3 validity package: {out}")
    parent_path = PHASE3 / "parent_prompt_manifest.jsonl"
    identity_path = V3 / "i3c_extraction/identity_manifest.jsonl"
    result_path = V3 / "b1l_preflight_v3/b1l_local_bm25_run/b1l_strict_results.jsonl"
    relation_path = ADJ / "final_prompt_relation_dispositions.jsonl"
    cue_path = ADJ / "final_prompt_cue_dispositions.jsonl"
    for path in (SOP, parent_path, identity_path, result_path, relation_path, cue_path):
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    parents = {str(row["prompt_id"]): row for row in read_jsonl(parent_path)}
    identities = {str(row["skill_id"]): row for row in read_jsonl(identity_path)}
    relation = [row for row in read_jsonl(relation_path) if row["phase3_disposition"] == "BLOCKED_PARENT_V3_VALIDITY_AUDIT"]
    cues = [row for row in read_jsonl(cue_path) if row["phase3_disposition"] == "BLOCKED_PARENT_V3_VALIDITY_AUDIT"]
    if len(relation) != 1 or len(relation[0]["affected_parent_prompt_ids"]) != 2 or len(cues) != 7:
        raise SystemExit("Parent validity case roster drift")
    cases: list[dict[str, Any]] = [{"case_id": "PV3-REL-001", "case_type": "PROMPT_RELATION", "trigger": relation[0]["packet_id"], "prompt_ids": relation[0]["affected_parent_prompt_ids"]}]
    for index, row in enumerate(sorted(cues, key=lambda value: str(value["packet_id"])), 1):
        cases.append({"case_id": f"PV3-CUE-{index:03d}", "case_type": "TARGET_TITLE_CUE", "trigger": row["packet_id"], "prompt_ids": [row["prompt_id"]]})
    packets_a, packets_b, joins = [], [], []
    for case in cases:
        source_cards = []
        for number, prompt_identifier in enumerate(case["prompt_ids"], 1):
            parent = parents.get(prompt_identifier)
            if not parent:
                raise SystemExit(f"Parent manifest lacks validity-audit prompt: {prompt_identifier}")
            identity = identities.get(str(parent["gold_skill"]))
            if not identity:
                raise SystemExit(f"V3 identity manifest lacks historical gold source: {parent['gold_skill']}")
            source = WORKSPACE / str(identity["source"])
            if not source.is_file() or sha(source) != identity["source_sha256"]:
                raise SystemExit(f"Historical parent source byte replay failed: {source}")
            source_cards.append({"source_token": f"S-{number}", "source_evidence_card": redact_source(source.read_text(encoding="utf-8", errors="replace"))})
        base_packet = {"case_id": case["case_id"], "case_type": case["case_type"], "review_boundary": "Immutable V3 validity audit only. Do not infer parent ID, historical gold/source mapping, prior result, rank, retrieval outcome, acceptable-set label, or another reviewer view.", "prompts": [{"prompt_token": f"Q-{number}", "prompt": parents[prompt_identifier]["prompt"]} for number, prompt_identifier in enumerate(case["prompt_ids"], 1)], "source_evidence_cards": source_cards if case["case_type"] == "PROMPT_RELATION" else list(reversed(source_cards)), "suspect_phrase_instruction": "For cue cases, assess whether the obvious source-like phrase in the prompt is necessary task language or an avoidable identity cue; it is not identified as a target title.", "return_schema": {"case_id": case["case_id"], "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS | TRANSFORMED_DUPLICATE_OR_SPLIT_LEAK | UNCLEAR (relation case only)", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM | AVOIDABLE_IDENTITY_CUE | NOT_A_CUE | UNCLEAR (cue case only)", "source_anchors": [], "rationale": ""}}
        packets_a.append({**base_packet, "reviewer": "A"})
        packets_b.append({**base_packet, "reviewer": "B", "source_evidence_cards": list(reversed(base_packet["source_evidence_cards"]))})
        joins.append({"case_id": case["case_id"], "trigger": case["trigger"], "parent_prompt_ids": case["prompt_ids"], "historical_gold_skill_ids": [parents[prompt_identifier]["gold_skill"] for prompt_identifier in case["prompt_ids"]], "historical_gold_source_sha256": [identities[parents[prompt_identifier]["gold_skill"]]["source_sha256"] for prompt_identifier in case["prompt_ids"]], "historical_result_binding_sha256": sha(result_path), "no_v3_rewrite": True, "no_retrieval_or_acceptable_set_evidence": True})
    summary = {"status": "PENDING_TWO_INDEPENDENT_BLINDED_PARENT_V3_VALIDITY_REVIEWS", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in (SOP, parent_path, identity_path, result_path, relation_path, cue_path)}, "counts": {"validity_audit_cases": 8, "affected_parent_prompt_ids": 9, "relation_cases": 1, "cue_cases": 7, "reviewer_a_packets": 8, "reviewer_b_packets": 8}, "claim_boundary": "No V3 prompt, identity, historical gold, or result has been rewritten. A passing validity case only permits a later Lane-A delta audit; it does not decide the acceptable set.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {"reviewer_a_packet.jsonl": packets_a, "reviewer_b_packet.jsonl": packets_b, "internal_historical_join.jsonl": joins}
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
