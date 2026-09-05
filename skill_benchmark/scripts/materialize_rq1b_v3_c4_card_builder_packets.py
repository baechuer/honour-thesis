#!/usr/bin/env python3
"""Materialise local anonymous RQ1b V3 C4A field-card builder packets.

Creates no card, prompt-review packet, label, selector input, model/API call,
embedding, metric or retrieval result. Public packets omit the prompt, source
ID, title, provenance and sealed construction target.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any


FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
SLOT_SCHEMA_VERSION = "rq1b-v3-c4a-v1.2"
SLOT_INCLUSION_RULES = {
    "use_condition": "Literal applicability, user goal, or situation in which the skill should be used; exclude bare topic mentions.",
    "input_precondition": "Literal consumed or required pre-existing artifact, data, state, access condition, or environment; uploaded material is input, not a dependency/resource.",
    "output_artifact": "Literal artifact, structured result, state change, or delivered format that the skill creates, returns, exports, or writes; exclude a line that only says to read or inspect an existing result.",
    "workflow_procedure": "Literal action, ordered step, transformation, or method performed by the skill; a stated inspection action may qualify.",
    "success_verification": "Literal pass/fail check, threshold, comparison, test, validation, measurement, or acceptance condition; exclude ordinary completion, artifact existence, reading an output, and generic care advice.",
    "boundary_not_for": "Literal exclusion, route-out, unsupported scope, prohibition, or limitation; do not infer an unstated boundary.",
    "dependency_resource": "Literal named external package, API, service, runtime, credential, tool, account, hardware, or data resource whose availability is explicitly required; exclude user inputs and output artifacts.",
}
BOUNDARY = (
    "C4A materialises anonymous original-source packets for later card construction only. "
    "It is not a card, strict label, selector input, metric or routing result."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def anonymous_labels(composition_id: str, source_ids: list[str]) -> dict[str, str]:
    ordered = sorted(
        source_ids,
        key=lambda source_id: hashlib.sha256(f"{composition_id}:{source_id}".encode()).hexdigest(),
    )
    return {source_id: f"Candidate {chr(ord('A') + index)}" for index, source_id in enumerate(ordered)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-roster", type=Path, required=True)
    parser.add_argument("--c3-ledger", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing_to_overwrite_existing_output:{args.output}")

    roster = read_jsonl(args.c2_roster)
    c3_rows = read_jsonl(args.c3_ledger)
    sources = {row["source_id"]: row for row in read_jsonl(args.source_manifest)}
    allowed_by_c1: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in c3_rows:
        if row.get("c3_disposition") != "C3_ALLOW_C4_WITH_RISK_ANNOTATION":
            raise SystemExit(f"c3_not_allow_c4:{row.get('c2_packet_id')}")
        allowed_by_c1[str(row["c1_review_id"])].append(row)
    if {row["c1_review_id"] for row in roster} != set(allowed_by_c1):
        raise SystemExit("c2_roster_and_c3_composition_coverage_mismatch")

    args.output.mkdir(parents=True)
    public_manifest: list[dict[str, Any]] = []
    private_manifest: list[dict[str, Any]] = []
    for roster_row in roster:
        c1_id = str(roster_row["c1_review_id"])
        c3_for_composition = allowed_by_c1[c1_id]
        expected_count = int(roster_row["candidate_count"]) * len(roster_row["prompt_variants_per_candidate"])
        if len(c3_for_composition) != expected_count:
            raise SystemExit(f"c3_packet_count_mismatch:{c1_id}")
        c1_rows = read_jsonl(Path(roster_row["ledger_path"]))
        matches = [row for row in c1_rows if row.get("c1_review_id") == c1_id]
        if len(matches) != 1 or matches[0].get("final_c1_outcome") != "ADVANCE_C2_PROMPT_CONSTRUCTION":
            raise SystemExit(f"invalid_c1_lineage:{c1_id}")
        source_ids = list(matches[0]["member_source_ids"])
        if len(source_ids) not in (3, 4) or len(set(source_ids)) != len(source_ids):
            raise SystemExit(f"invalid_candidate_set:{c1_id}")
        composition_id = str(roster_row["composition_id"])
        labels = anonymous_labels(composition_id, source_ids)
        packet_id = f"C4A-{composition_id}"
        packet_dir = args.output / "builder_packets" / packet_id
        source_dir = packet_dir / "sources"
        source_dir.mkdir(parents=True)
        public_candidates: list[dict[str, str]] = []
        private_candidates: list[dict[str, str]] = []
        for source_id in sorted(source_ids, key=lambda item: labels[item]):
            source = sources.get(source_id)
            if not source:
                raise SystemExit(f"missing_source_manifest_record:{source_id}")
            canonical = source["canonical"]
            original = Path(canonical["absolute_path"])
            expected_sha = str(source["sha256"])
            if not original.is_file() or sha256_file(original) != expected_sha:
                raise SystemExit(f"source_hash_or_path_failure:{source_id}")
            filename = labels[source_id].lower().replace(" ", "_") + ".md"
            copied = source_dir / filename
            shutil.copyfile(original, copied)
            if sha256_file(copied) != expected_sha:
                raise SystemExit(f"copied_source_hash_failure:{source_id}")
            public_candidates.append({
                "label": labels[source_id],
                "source_sha256": expected_sha,
                "text_path": f"sources/{filename}",
            })
            private_candidates.append({
                "label": labels[source_id],
                "source_id": source_id,
                "source_sha256": expected_sha,
                "original_path": str(original),
            })
        public_packet = {
            "status": "RQ1B_V3_C4A_ANONYMOUS_SOURCE_PACKET_NOT_A_RESULT",
            "packet_id": packet_id,
            "instructions": [
                "Read only this packet and its anonymous source copies.",
                "Do not inspect any prompt, construction target, source map, provenance, selector, embedding, metric, result or online material.",
                "Do not choose a candidate or infer a user request.",
                "For every candidate, fill all seven slots with EVIDENCE (one or more exact contiguous source excerpts) or NOT_STATED.",
                "Slots are not mutually exclusive: repeat the same exact contiguous excerpt in every slot it explicitly supports. For example, a sentence that names an input, transformation and returned deliverable belongs in input_precondition, workflow_procedure and output_artifact.",
                "Use each slot only for the supplied v1.2 literal inclusion rule. In particular, a user-supplied artifact is input_precondition rather than dependency_resource; only an explicit test, threshold, comparison, validation, measurement, or acceptance condition is success_verification; and reading a result is not success_verification.",
                "Do not paraphrase, merge non-contiguous excerpts, invent facts, quote YAML frontmatter, a title, heading, URL, source ID, repository name or local path.",
                "Return only the required JSON object. This is card transcription, not routing.",
            ],
            "field_order": list(FIELDS),
            "slot_schema_version": SLOT_SCHEMA_VERSION,
            "slot_inclusion_rules": SLOT_INCLUSION_RULES,
            "field_schema": {"status": "EVIDENCE or NOT_STATED", "quotes": ["exact contiguous source excerpt"]},
            "candidates": public_candidates,
            "claim_boundary": BOUNDARY,
        }
        write_json(packet_dir / "field_card_builder_packet.json", public_packet)
        public_manifest.append({
            "packet_id": packet_id,
            "candidate_count": len(public_candidates),
            "builder_packet_path": str(packet_dir / "field_card_builder_packet.json"),
            "status": "READY_FOR_TWO_INDEPENDENT_C4A_BUILDERS_NOT_A_RESULT",
        })
        private_manifest.append({
            "packet_id": packet_id,
            "composition_id": composition_id,
            "c1_review_id": c1_id,
            "c1_ledger_path": roster_row["ledger_path"],
            "c1_ledger_sha256": roster_row["ledger_sha256"],
            "c2_packets": sorted(row["c2_packet_id"] for row in c3_for_composition),
            "c3_packet_ledger_sha256": sha256_file(args.c3_ledger),
            "c3_risk_counts": {risk: sum(row["residual_cue_risk"] == risk for row in c3_for_composition) for risk in ("high", "medium", "low")},
            "candidates": private_candidates,
        })

    write_json(args.output / "builder_packet_manifest.json", public_manifest)
    write_json(args.output / "private_lineage_manifest.json", private_manifest)
    audit = {
        "status": "RQ1B_V3_C4A_BUILDER_PACKET_MATERIALISATION_PASS_NOT_A_RESULT",
        "composition_count": len(public_manifest),
        "candidate_count": sum(row["candidate_count"] for row in public_manifest),
        "c2_roster_sha256": sha256_file(args.c2_roster),
        "c3_ledger_sha256": sha256_file(args.c3_ledger),
        "source_manifest_sha256": sha256_file(args.source_manifest),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
        "exclusions": ["No card, C4 review, strict label, selector input, embedding, metric or routing result was created."],
    }
    write_json(args.output / "C4A_BUILDER_PACKET_AUDIT.json", audit)
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
