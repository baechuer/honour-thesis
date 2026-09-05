#!/usr/bin/env python3
"""Materialise source-deidentified C3 residual-cue review packets.

C3 reviewers inspect a prompt alongside all original candidates to decide
whether wording is an accidental source cue or a necessary operational
constraint.  They must not receive the sealed construction target.  This
script creates their packets and a separate principal-only mapping.

It creates review material only: no cue-safety proof, adequacy decision, gold
label, selector input, scoring, model call, metric, or result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


INSTRUCTIONS = (
    "C3 residual-cue review only. For each anonymous request, compare it with "
    "all three unlabelled source originals. Decide whether it contains an "
    "accidental source identifier (title, copied heading, repository-specific "
    "term, command/package/template name, or distinctive clause) or only a "
    "necessary real operational constraint. Return JSON records with "
    "blind_packet_id, residual_cue_risk (low|medium|high), disposition "
    "(ALLOW_AS_OPERATIONAL|REWRITE_CUE_ONLY|REJECT_UNSAFE_CUE), exact cue "
    "phrases if any, and a concise rationale. Do not judge which candidate is "
    "adequate, do not infer a gold label, and do not use or open any sealed "
    "mapping, C1/C4 results, selectors, embeddings, scores, or online sources."
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--c1-roster", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise SystemExit(f"refusing_to_overwrite:{args.output_dir}")

    c1_rows = {str(row["c1_review_id"]): row for row in read_jsonl(args.c1_roster)}
    by_c1: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(args.c2_ledger):
        if row.get("c2_disposition") == "C2_DRAFT_FOR_C3":
            by_c1[str(row["c1_review_id"])].append(row)

    args.output_dir.mkdir(parents=True)
    sealed: list[dict[str, str]] = []
    public_manifest: list[dict[str, Any]] = []
    for c1_id, prompts in sorted(by_c1.items()):
        c1 = c1_rows.get(c1_id)
        if c1 is None:
            raise SystemExit(f"missing_c1_roster:{c1_id}")
        candidates = []
        for letter, member in zip(("A", "B", "C", "D"), c1["members"]):
            source_path = Path(member["absolute_path"])
            if not source_path.is_file():
                raise SystemExit(f"missing_source:{source_path}")
            candidates.append({
                "blind_candidate_id": letter,
                "source_original": source_path.read_text(encoding="utf-8"),
                "source_sha256": member["sha256"],
            })
        packets = []
        for ordinal, c2 in enumerate(sorted(prompts, key=lambda r: str(r["c2_packet_id"])), start=1):
            blind_packet_id = f"{c1_id.rsplit('-', 1)[-1]}-P{ordinal:02d}"
            packets.append({
                "blind_packet_id": blind_packet_id,
                "request_text": c2["prompt_text"],
                "variant": c2["variant"],
            })
            sealed.append({
                "blind_packet_id": blind_packet_id,
                "c2_packet_id": str(c2["c2_packet_id"]),
                "sealed_target_source_id": str(c2["sealed_target_source_id"]),
            })
        public_packet = {
            "claim_boundary": "C3 source-deidentified residual-cue review packet only; not a label, adequacy judgment, selector input, metric, or result.",
            "review_instructions": INSTRUCTIONS,
            "anonymous_composition_id": c1_id.rsplit("-", 1)[-1],
            "candidates": candidates,
            "packets": packets,
        }
        public_path = args.output_dir / f"c3_blind_packet_{c1_id.rsplit('-', 1)[-1].lower()}.json"
        public_path.write_text(json.dumps(public_packet, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        public_manifest.append({
            "c1_review_id": c1_id,
            "blind_packet_path": str(public_path),
            "packet_count": len(packets),
            "candidate_count": len(candidates),
        })

    sealed_path = args.output_dir / "C3_PRINCIPAL_ONLY_SEALED_MAPPING.json"
    sealed_path.write_text(json.dumps(sealed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path = args.output_dir / "C3_BLIND_PACKET_MANIFEST.json"
    manifest_path.write_text(json.dumps({
        "status": "C3_BLIND_PACKET_MATERIALISATION_PASS_NOT_A_LABEL_OR_RESULT",
        "c2_ledger_sha256": sha256(args.c2_ledger),
        "c1_roster_sha256": sha256(args.c1_roster),
        "composition_count": len(public_manifest),
        "packet_count": len(sealed),
        "public_packets": public_manifest,
        "sealed_mapping_path": str(sealed_path),
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No C4 adequacy review, strict gold label, selector input, model/API call, metric, or routing result was created.",
        ],
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"compositions": len(public_manifest), "packets": len(sealed), "output_dir": str(args.output_dir)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
