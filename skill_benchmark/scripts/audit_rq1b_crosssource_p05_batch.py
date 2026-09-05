#!/usr/bin/env python3
"""Audit P0.5 blind-coder responses before any coordinator field decision.

The script validates JSON shape and literal evidence membership, then writes a
review-comparison table. It deliberately does not determine field consensus,
unblind strict gold, create a mask, or emit a scientific result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


VALID_CODES = {
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
    "MULTI_FIELD_OR_NONCODEABLE",
}


def read_json(path: Path) -> object:
    return json.loads(path.read_text())


def validate_response(packet: dict, family_dir: Path, response_path: Path) -> dict:
    try:
        response = read_json(response_path)
    except Exception as error:
        return {"valid": False, "failures": [f"json_parse:{error}"]}
    if not isinstance(response, dict):
        return {"valid": False, "failures": ["response_not_object"]}
    failures = []
    if response.get("family_id") != packet.get("family_id"):
        failures.append("family_id_mismatch")
    prompt_by_variant = {item["variant"]: item["text"] for item in packet["prompts"]}
    candidate_by_label = {
        item["label"]: (family_dir / item["text_path"]).read_text() for item in packet["candidates"]
    }
    rows = response.get("per_prompt")
    if not isinstance(rows, list) or len(rows) != len(prompt_by_variant):
        failures.append("prompt_variant_coverage_mismatch")
        rows = rows if isinstance(rows, list) else []
    seen_variants = set()
    compact = []
    for item in rows:
        if not isinstance(item, dict):
            failures.append("per_prompt_item_not_object")
            continue
        variant = item.get("variant")
        if variant not in prompt_by_variant:
            failures.append(f"unknown_variant:{variant}")
            continue
        if variant in seen_variants:
            failures.append(f"duplicate_variant:{variant}")
        seen_variants.add(variant)
        code = item.get("code")
        if code not in VALID_CODES:
            failures.append(f"invalid_code:{variant}:{code}")
        clauses = item.get("prompt_clauses")
        if not isinstance(clauses, list) or not clauses:
            failures.append(f"missing_prompt_clause:{variant}")
            clauses = []
        for quote in clauses:
            if not isinstance(quote, str) or not quote or quote not in prompt_by_variant[variant]:
                failures.append(f"prompt_quote_not_exact:{variant}:{quote!r}")
        evidence = item.get("candidate_evidence")
        if not isinstance(evidence, dict):
            failures.append(f"candidate_evidence_not_object:{variant}")
            evidence = {}
        exact_candidate_quotes = 0
        for label, quotes in evidence.items():
            if label not in candidate_by_label:
                failures.append(f"unknown_candidate:{variant}:{label}")
                continue
            if not isinstance(quotes, list):
                failures.append(f"candidate_quotes_not_list:{variant}:{label}")
                continue
            for quote in quotes:
                if not isinstance(quote, str) or not quote or quote not in candidate_by_label[label]:
                    failures.append(f"candidate_quote_not_exact:{variant}:{label}:{quote!r}")
                else:
                    exact_candidate_quotes += 1
        if code != "MULTI_FIELD_OR_NONCODEABLE" and exact_candidate_quotes == 0:
            failures.append(f"missing_exact_candidate_evidence:{variant}")
        compact.append(
            {
                "variant": variant,
                "code": code,
                "prompt_clauses": clauses,
                "candidate_quote_count": exact_candidate_quotes,
            }
        )
    if seen_variants != set(prompt_by_variant):
        failures.append("variant_set_mismatch")
    return {"valid": not failures, "failures": failures, "compact": sorted(compact, key=lambda row: row["variant"])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-dir", type=Path, required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    manifest = read_json(args.batch_dir / "agent_packet_manifest.json")
    if not isinstance(manifest, list):
        raise SystemExit("agent packet manifest is not a list")
    records = []
    for item in manifest:
        family_id = item["family_id"]
        family_dir = args.batch_dir / family_id
        packet = read_json(family_dir / "field_coding_packet.json")
        response_path = args.batch_dir / "reviews" / args.reviewer / f"{family_id}.json"
        if response_path.is_file():
            audited = validate_response(packet, family_dir, response_path)
        else:
            audited = {"valid": False, "failures": ["response_missing"]}
        records.append(
            {
                "family_id": family_id,
                "response_path": str(response_path),
                **audited,
            }
        )
    output = args.batch_dir / "audits" / f"p05_{args.reviewer}_response_audit.json"
    output.parent.mkdir(exist_ok=True)
    payload = {
        "status": "P05_RESPONSE_AUDIT_NOT_A_CONSENSUS_OR_RESULT",
        "reviewer": args.reviewer,
        "counts": {"families": len(records), "valid": sum(record["valid"] for record in records)},
        "records": records,
        "exclusions": [
            "This audit does not lock a field.",
            "This audit does not unblind strict gold.",
            "No mask, selector, embedding, retrieval, API call, metric, or result exists.",
        ],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), **payload["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
